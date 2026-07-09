"""Stale-content check.

Flags assets whose review is overdue based on `last_review` + `review_cycle`.
Volatile tax content must be re-verified on schedule or it becomes an error
source. Run:

    cd apps/api && .venv/bin/python scripts/check_stale.py

Exits non-zero if any asset is overdue (CI-gateable). Set env CHECK_STALE_WARN=1
to warn without failing.
"""

from __future__ import annotations

import os
import sys
from datetime import date, datetime
from pathlib import Path

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.config import get_settings  # noqa: E402
from app.services.knowledge_base import KB_DIRS  # noqa: E402

# Days allowed between reviews per cycle.
CYCLE_DAYS = {"monthly": 31, "quarterly": 93, "semiannual": 186, "annual": 366}


def _parse(d: str) -> date | None:
    try:
        return datetime.strptime(str(d), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def main() -> int:
    settings = get_settings()
    today = date.today()
    overdue: list[str] = []
    checked = 0

    for d in KB_DIRS:
        directory = settings.kb_root / d
        if not directory.is_dir():
            continue
        for md in sorted(directory.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            meta = frontmatter.load(md).metadata
            cycle = str(meta.get("review_cycle", "")).lower()
            if cycle not in CYCLE_DAYS:
                continue
            checked += 1
            last = _parse(meta.get("last_review", ""))
            if last is None:
                overdue.append(f"  {meta.get('id', md.stem)}: missing/invalid last_review")
                continue
            age = (today - last).days
            if age > CYCLE_DAYS[cycle]:
                overdue.append(
                    f"  {meta.get('id', md.stem)}: {age}d since review "
                    f"(cycle {cycle}={CYCLE_DAYS[cycle]}d)"
                )

    print(f"Checked {checked} assets with a review_cycle.")
    if overdue:
        print(f"OVERDUE ({len(overdue)}):")
        print("\n".join(overdue))
    else:
        print("All reviewed assets are up to date.")

    if overdue and not os.environ.get("CHECK_STALE_WARN"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
