"""RFC-0002 metadata validation gate.

Fails if any asset is missing a required field or uses an invalid type/status.
Run:  cd apps/api && .venv/bin/python scripts/validate_metadata.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.config import get_settings  # noqa: E402
from app.services.knowledge_base import KB_DIRS  # noqa: E402

REQUIRED = [
    "id", "title", "type", "department", "role", "country", "language",
    "summary", "tags", "source", "source_url", "version", "confidence",
    "owner", "created", "updated", "last_review", "status",
]
TYPES = {"FACT", "RULE", "WORKFLOW", "SOP", "CHECKLIST", "TEMPLATE", "POLICY",
         "DECISION", "BEST_PRACTICE", "FAQ"}
STATUSES = {"Draft", "Review", "Approved", "Published", "Deprecated", "Archived"}


def main() -> int:
    root = get_settings().kb_root
    errors: list[str] = []
    checked = 0
    for d in KB_DIRS:
        for md in sorted((root / d).glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            checked += 1
            meta = frontmatter.load(md).metadata
            aid = meta.get("id", md.stem)
            for f in REQUIRED:
                v = meta.get(f)
                if v is None or (isinstance(v, str) and not v.strip()):
                    errors.append(f"{aid}: missing '{f}'")
            if meta.get("type") and meta["type"] not in TYPES:
                errors.append(f"{aid}: invalid type '{meta['type']}'")
            if meta.get("status") and meta["status"] not in STATUSES:
                errors.append(f"{aid}: invalid status '{meta['status']}'")

    print(f"Validated {checked} assets against RFC-0002.")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        print("\n".join("  " + e for e in errors))
        return 1
    print("All assets conform to RFC-0002.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
