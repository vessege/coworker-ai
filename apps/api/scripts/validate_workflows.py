"""RFC-0003 (Workflow Asset Standard) validation gate.

Every WORKFLOW/SOP asset must carry a structured `workflow` block with the
required fields and well-formed steps. Run:
    cd apps/api && .venv/bin/python scripts/validate_workflows.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import frontmatter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.config import get_settings  # noqa: E402
from app.services.knowledge_base import KB_DIRS  # noqa: E402

WF_REQUIRED = [
    "business_goal", "difficulty", "estimated_duration", "automation_score",
    "required_inputs", "expected_outputs", "success_criteria",
    "failure_conditions", "steps",
]
STEP_REQUIRED = ["number", "title", "actor", "ai_capability", "expected_result", "validation_rule"]
AI_CAPS = {"Observe", "Suggest", "Draft", "Automate", "Execute", "Review", "Escalate"}


def main() -> int:
    root = get_settings().kb_root
    errors: list[str] = []
    checked = 0
    for d in KB_DIRS:
        for md in sorted((root / d).glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            meta = frontmatter.load(md).metadata
            if str(meta.get("type", "")) not in {"WORKFLOW", "SOP"}:
                continue
            checked += 1
            aid = meta.get("id", md.stem)
            wf = meta.get("workflow")
            if not isinstance(wf, dict):
                errors.append(f"{aid}: missing structured 'workflow' block")
                continue
            for f in WF_REQUIRED:
                if f not in wf or wf[f] in (None, "", []):
                    errors.append(f"{aid}: workflow missing '{f}'")
            for i, step in enumerate(wf.get("steps") or [], 1):
                for f in STEP_REQUIRED:
                    if f not in step or step[f] in (None, ""):
                        errors.append(f"{aid}: step {i} missing '{f}'")
                cap = step.get("ai_capability")
                if cap and cap not in AI_CAPS:
                    errors.append(f"{aid}: step {i} invalid ai_capability '{cap}'")

    print(f"Validated {checked} workflow/SOP assets against RFC-0003.")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        print("\n".join("  " + e for e in errors))
        return 1
    print("All workflow assets conform to RFC-0003.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
