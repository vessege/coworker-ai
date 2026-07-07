"""End-to-end demo: upload real-style business documents, then ask
role-specific questions and verify the right document + KB assets ground
each answer. Run:  cd apps/api && .venv/bin/python scripts/demo_documents.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.config import get_settings  # noqa: E402
from app.main import app  # noqa: E402

DOCS_DIR = get_settings().kb_root / "datasets" / "raw" / "test-documents"

# (role, question, expected source: filename of the doc OR KB asset ids)
CASES = [
    ("Buxgalter", "Alfa Savdo fakturasida jami summa qancha QQS bilan?", ["ehf-158-alfa.md"]),
    ("Buxgalter", "158-sonli fakturada QQS summasi qancha?", ["ehf-158-alfa.md"]),
    ("HR", "Karimova bilan shartnomada sinov muddati qancha?", ["shartnoma-07-karimova.md"]),
    ("HR", "Karimovaning oylik ish haqi qancha?", ["shartnoma-07-karimova.md"]),
    ("Ofis-menejer", "Hokimlikdan kelgan xatga javob muddati qachon?", ["kiruvchi-xat-234.md"]),
    ("Ofis-menejer", "01-15/234 xat kimga ijroga berilgan?", ["kiruvchi-xat-234.md"]),
    # KB + doc aralash: umumiy savol baza asstlarini ham topishi kerak
    ("Buxgalter", "QQS stavkasi qancha?", ["ACC-FAQ-002", "ACC-KA-003"]),
]


def main() -> int:
    c = TestClient(app)

    print("== 1. Hujjatlarni yuklash ==")
    name_to_id: dict[str, str] = {}
    for f in sorted(DOCS_DIR.glob("*.md")):
        r = c.post("/api/v1/documents", json={"name": f.name, "content": f.read_text()})
        d = r.json()
        name_to_id[d["title"]] = d["id"]
        print(f"  {d['id']}  {d['title']}")

    docs = c.get("/api/v1/documents").json()
    print(f"  jami yuklandi: {len(docs)}")

    print("\n== 2. Rol bo'yicha savollar ==")
    passed = 0
    for role, q, expect in CASES:
        expect = [name_to_id.get(e, e) for e in expect]
        r = c.post("/api/v1/ask", json={"question": q}).json()
        got = [s["id"] for s in r["sources"]]
        ok = any(e in got for e in expect)
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] ({role}) {q}")
        print(f"         manbalar: {got}")
        if not ok:
            print(f"         kutilgan: {expect}")

    print(f"\nNATIJA: {passed}/{len(CASES)} PASS")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
