"""1C integration demo/test against a mock 1C OData source.

Verifies the full loop: configure -> sync (entities land in the tenant's
DocumentStore) -> /ask grounds answers in live 1C data. With a real 1C the
only change is the base_url — the fetcher speaks standard OData.
Run:  cd apps/api && .venv/bin/python scripts/demo_1c.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.api import routes  # noqa: E402
from app.main import app  # noqa: E402

# Realistic mock of the 1C OData "value" payloads.
MOCK_1C = {
    "Catalog_Контрагенты": [
        {"Description": "Alfa Savdo MChJ", "ИНН": "305123456", "Code": "К-0001"},
        {"Description": "Beta Servis MChJ", "ИНН": "302987654", "Code": "К-0002"},
        {"Description": "Gamma Trans YaTT", "ИНН": "512345678", "Code": "К-0003"},
    ],
    "Document_РеализацияТоваровУслуг": [
        {"Number": "0000-000041", "Date": "2026-06-10T00:00:00",
         "Контрагент": "Alfa Savdo MChJ", "СуммаДокумента": 23968000},
        {"Number": "0000-000042", "Date": "2026-06-25T00:00:00",
         "Контрагент": "Gamma Trans YaTT", "СуммаДокумента": 5400000},
    ],
}

checks: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    checks.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def main() -> int:
    # Inject the mock fetcher (a real deployment uses the OData HTTP fetcher).
    routes._onec._fetch = lambda cfg, entity: MOCK_1C.get(entity, [])
    c = TestClient(app)

    print("== 1. Konfiguratsiya ==")
    r = c.post("/api/v1/integrations/1c/config",
               json={"base_url": "http://mock-1c/base1", "username": "odata"}).json()
    check("1C sozlandi", r.get("configured") is True)
    check("status configured", c.get("/api/v1/integrations/1c/status").json()["configured"])

    print("\n== 2. Sinxronlash ==")
    s = c.post("/api/v1/integrations/1c/sync").json()
    check("2 entity sinxronlandi, xatosiz",
          len(s.get("synced", [])) == 2 and not s.get("errors"))
    doc_ids = {x["doc"] for x in s["synced"]}
    docs = c.get("/api/v1/documents").json()
    check("1C hujjatlari DocumentStore'da", doc_ids <= {d["id"] for d in docs})

    print("\n== 3. /ask 1C ma'lumotiga tayanadi ==")
    for q, want in [
        ("1C da qaysi kontragentlar bor?", "Контрагенты"),
        ("Alfa Savdo bilan qancha summaga sotuv bo'lgan?", "Реализация"),
        ("Gamma Trans YaTT sotuvi qachon bo'lgan?", "Реализация"),
    ]:
        r = c.post("/api/v1/ask", json={"question": q}).json()
        got = [s["id"] for s in r["sources"]]
        ok = any(d in got for d in doc_ids)
        check(f"{q} -> 1C hujjati manbada {got}", ok)

    passed = sum(ok for _, ok in checks)
    print(f"\nNATIJA: {passed}/{len(checks)} PASS")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
