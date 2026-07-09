"""Training-data exporter: Knowledge Base -> instruct-tuning JSONL.

Converts the Company Brain into supervised fine-tuning pairs for a future
in-house model ("CoWorker-1"), realizing the Knowledge Factory -> Foundation
Model pipeline from the original vision:

- FAQ assets       -> direct Q/A pairs (uz + en sections parsed separately)
- KA/SOP/CHK/...   -> "explain <topic>" -> asset body (grounded exposition)
- TPL assets       -> "draft <document>" -> template body (generation tasks)
- eval set         -> retrieval-routing pairs (question -> relevant asset ids)

Output: datasets/training/instruct.jsonl  (one {"messages": [...]} per line,
chat format compatible with common SFT trainers: system/user/assistant).

Run:  python scripts/export_training_data.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]
KB_DIRS = ["knowledge-assets", "faq", "workflow-assets", "checklists", "templates",
           "business-rules", "decision-trees", "glossary", "policies"]
OUT = ROOT / "datasets" / "training" / "instruct.jsonl"

SYSTEM = ("Siz CoWorker AI — O'zbekiston kichik biznesi uchun AI hamkasbsiz. "
          "Faqat tekshirilgan bilimga tayanib, manba bilan javob bering.")

FAQ_RE = re.compile(r"\*\*[SQ]:\s*(.+?)\*\*\s*\n?\s*J?A?:?\s*(.+?)(?=\n\*\*[SQ]:|\n#|\n---|\Z)",
                    re.DOTALL)


def pair(user: str, assistant: str, meta: dict, kind: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user.strip()},
            {"role": "assistant", "content": assistant.strip()},
        ],
        "meta": {"source_asset": meta.get("id", ""), "kind": kind,
                 "source_url": str(meta.get("source_url", ""))},
    }


def faq_pairs(meta: dict, body: str) -> list[dict]:
    out = []
    for q, a in FAQ_RE.findall(body):
        q, a = q.strip(), re.sub(r"\n{3,}", "\n\n", a).strip()
        if len(q) > 5 and len(a) > 5:
            out.append(pair(q, a, meta, "faq-qa"))
    return out


def main() -> None:
    rows: list[dict] = []
    for d in KB_DIRS:
        for md in sorted((ROOT / d).glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            post = frontmatter.load(md)
            meta, body = post.metadata, post.content
            if str(meta.get("status", "")).lower() not in {"approved", "published"}:
                continue
            title_uz = str(meta.get("title", "")).split("/")[-1].strip() or md.stem
            atype = str(meta.get("type", ""))

            if atype == "FAQ":
                rows.extend(faq_pairs(meta, body))
            elif atype == "TEMPLATE":
                rows.append(pair(f"{title_uz} shablonini tayyorlab bering.",
                                 body, meta, "template-gen"))
            else:  # FACT / SOP / CHECKLIST / RULE / DECISION ...
                rows.append(pair(f"{title_uz} haqida tushuntirib bering.",
                                 body, meta, "explain"))
                summary = str(meta.get("summary", ""))
                if summary:
                    rows.append(pair(f"Qisqacha: {title_uz} nima?",
                                     summary, meta, "summary"))

    # Routing pairs from the golden eval set (question -> which assets answer it)
    eval_file = ROOT / "datasets" / "benchmarks" / "accountant-eval.jsonl"
    if eval_file.exists():
        for line in eval_file.read_text().splitlines():
            if not line.strip():
                continue
            case = json.loads(line)
            rows.append({
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user",
                     "content": f"Savol: {case['q']}\nQaysi bilim aktivlari bu savolga javob beradi?"},
                    {"role": "assistant", "content": ", ".join(case["expect"])},
                ],
                "meta": {"source_asset": "", "kind": "routing", "source_url": ""},
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r["meta"]["kind"]] = kinds.get(r["meta"]["kind"], 0) + 1
    print(f"Wrote {len(rows)} instruct pairs -> {OUT.relative_to(ROOT)}")
    for k, v in sorted(kinds.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
