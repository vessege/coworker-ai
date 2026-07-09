"""Export the knowledge base as a graph (RFC-0007 forward-compatibility).

Emits nodes (assets) and directed edges (relationships) to
datasets/processed/knowledge-graph.json. This is the cheap, static precursor
to the future Enterprise Knowledge Graph — no engine, just structured export.

Run:  python scripts/export_knowledge_graph.py
"""

from __future__ import annotations

import json
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]
KB_DIRS = [
    "knowledge-assets", "faq", "workflow-assets", "checklists", "templates",
    "business-rules", "decision-trees", "glossary", "policies",
]


def main() -> None:
    nodes, edges = [], []
    for d in KB_DIRS:
        for md in sorted((ROOT / d).glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            m = frontmatter.load(md).metadata
            aid = str(m.get("id", md.stem))
            nodes.append({
                "id": aid,
                "title": m.get("title", ""),
                "type": m.get("type", ""),
                "role": m.get("role", ""),
                "department": m.get("department", ""),
                "status": m.get("status", ""),
                "confidence": m.get("confidence", 0),
            })
            for rel in (m.get("relationships") or []):
                edges.append({
                    "source": aid,
                    "type": rel.get("type", "related_to"),
                    "target": rel.get("target", ""),
                })

    out = ROOT / "datasets" / "processed" / "knowledge-graph.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2) + "\n")
    print(f"Exported {len(nodes)} nodes, {len(edges)} edges -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
