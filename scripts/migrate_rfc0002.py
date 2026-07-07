"""One-time migration: bring every Knowledge Asset up to the RFC-0002 (KAS v1.0)
metadata standard while preserving existing fields and body content.

Adds: type, department, role, summary, status, confidence, owner, created,
updated; converts flat `related` into structured `relationships`.

Deterministic, idempotent. Run from repo root:  python scripts/migrate_rfc0002.py
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter

ROOT = Path(__file__).resolve().parents[1]
KB_DIRS = [
    "knowledge-assets", "faq", "workflow-assets", "checklists", "templates",
    "business-rules", "decision-trees", "glossary", "policies",
]

# category (+ id hint) -> RFC-0002 Type enum
TYPE_BY_CATEGORY = {
    "knowledge-asset": "FACT",
    "faq": "FAQ",
    "workflow-asset": "WORKFLOW",
    "checklist": "CHECKLIST",
    "template": "TEMPLATE",
    "business-rule": "RULE",
    "decision-tree": "DECISION",
    "glossary": "FACT",
    "policy": "POLICY",
}
ROLE_BY_PREFIX = {"OM": "Office Manager", "ACC": "Accountant"}
DEPT_BY_DOMAIN = {
    "office-management": "Administration",
    "accounting": "Finance & Accounting",
}
STATUS_BY_QUALITY = {"draft": "Draft", "reviewed": "Approved", "production-ready": "Published"}
CONFIDENCE_BY_QUALITY = {"draft": 0.5, "reviewed": 0.8, "production-ready": 0.9}

_SKIP_LINE = re.compile(r"^\s*(#|>|\||```|---|\*|-|\d+\.)")


def derive_type(meta: dict) -> str:
    if "-SOP-" in str(meta.get("id", "")):
        return "SOP"
    return TYPE_BY_CATEGORY.get(str(meta.get("category", "")), "FACT")


def derive_summary(body: str) -> str:
    """First real sentence of the body (skip headings/quotes/tables)."""
    for raw in body.splitlines():
        line = raw.strip()
        if not line or _SKIP_LINE.match(line):
            continue
        return (line[:197] + "...") if len(line) > 200 else line
    return ""


def migrate_file(path: Path) -> bool:
    post = frontmatter.load(path)
    m = dict(post.metadata)
    prefix = str(m.get("id", "")).split("-")[0]
    quality = str(m.get("quality", "reviewed"))
    reviewed = str(m.get("last_review", "")) or str(m.get("valid_from", ""))

    m.setdefault("type", derive_type(m))
    m.setdefault("department", DEPT_BY_DOMAIN.get(str(m.get("domain", "")), "General"))
    m.setdefault("role", ROLE_BY_PREFIX.get(prefix, "General"))
    if not m.get("summary"):
        m["summary"] = derive_summary(post.content)
    m.setdefault("status", STATUS_BY_QUALITY.get(quality, "Approved"))
    m.setdefault("confidence", CONFIDENCE_BY_QUALITY.get(quality, 0.7))
    m.setdefault("owner", "CKO / Knowledge Factory")
    m.setdefault("created", str(m.get("valid_from", "")) or reviewed)
    m.setdefault("updated", reviewed)

    # Flat related -> structured relationships (default relation: related_to).
    if "related" in m and "relationships" not in m:
        m["relationships"] = [{"type": "related_to", "target": t} for t in (m.get("related") or [])]
        del m["related"]

    post.metadata = m
    path.write_text(frontmatter.dumps(post) + "\n")
    return True


def main() -> None:
    count = 0
    for d in KB_DIRS:
        for md in sorted((ROOT / d).glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            if migrate_file(md):
                count += 1
                print(f"  migrated {md.relative_to(ROOT)}")
    print(f"Done. {count} assets migrated to RFC-0002.")


if __name__ == "__main__":
    main()
