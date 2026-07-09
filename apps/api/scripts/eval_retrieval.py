"""Retrieval evaluation harness.

Measures how often the correct asset is retrieved for a golden set of questions
(recall@k). This is how we quantify — and drive down — the error rate before
launch. Run:

    cd apps/api && .venv/bin/python scripts/eval_retrieval.py [top_k]

Exit code is non-zero if recall@k drops below THRESHOLD, so it can gate CI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import get_settings  # noqa: E402
from app.services.knowledge_base import KnowledgeBase  # noqa: E402

THRESHOLD = 0.90  # required recall@k to pass


def main() -> int:
    top_k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    settings = get_settings()
    kb = KnowledgeBase(settings.kb_root).load()
    eval_file = settings.kb_root / "datasets" / "benchmarks" / "accountant-eval.jsonl"

    cases = [json.loads(l) for l in eval_file.read_text().splitlines() if l.strip()]
    hits = 0
    misses: list[str] = []
    for c in cases:
        got = [a.id for a, _ in kb.search(c["q"], top_k, settings.retrieval_min_score)]
        if any(e in got for e in c["expect"]):
            hits += 1
        else:
            misses.append(f"  MISS: {c['q']!r}\n        expect {c['expect']} got {got}")

    total = len(cases)
    recall = hits / total if total else 0.0
    print(f"Assets loaded : {len(kb.assets)}")
    print(f"Eval cases    : {total}")
    print(f"Recall@{top_k}      : {recall:.0%}  ({hits}/{total})")
    if misses:
        print("\n".join(misses))
    ok = recall >= THRESHOLD
    print(f"\nRESULT: {'PASS' if ok else 'FAIL'} (threshold {THRESHOLD:.0%})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
