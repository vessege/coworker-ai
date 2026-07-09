"""RFC-0004 Task Asset demo/test: state machine, priorities, and the Learning
Rule (every /ask and /generate becomes a completed Task).
Run:  cd apps/api && .venv/bin/python scripts/demo_tasks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

checks: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    checks.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def main() -> int:
    c = TestClient(app)

    print("== 1. Task yaratish va holat mashinasi ==")
    t = c.post("/api/v1/tasks", json={
        "title": "Iyul oyi uchun QQS hisobotini tayyorlash",
        "business_goal": "File July VAT report on time",
        "role": "Accountant", "priority": "High", "deadline": "2026-08-20",
        "related_workflow": "ACC-SOP-001",
        "deliverables": ["Filed VAT declaration"],
        "success_criteria": ["Filed by the 20th"],
    }).json()
    check("task yaratildi (Created)", t["status"] == "Created" and t["id"].startswith("TASK-"))

    tid = t["id"]
    r = c.patch(f"/api/v1/tasks/{tid}/status", json={"status": "Running"}).json()
    check("Created -> Running ruxsat", r.get("status") == "Running")

    r = c.patch(f"/api/v1/tasks/{tid}/status", json={"status": "Archived"}).json()
    check("Running -> Archived taqiqlangan", "error" in r)

    r = c.patch(f"/api/v1/tasks/{tid}/status", json={"status": "Completed"}).json()
    check("Running -> Completed ruxsat", r.get("status") == "Completed")

    bad = c.post("/api/v1/tasks", json={"title": "x1", "priority": "Urgent"}).json()
    check("noto'g'ri priority rad etildi", "error" in bad)

    print("\n== 2. Learning Rule: interaksiyalar avto-Task bo'ladi ==")
    before = len(c.get("/api/v1/tasks").json())
    c.post("/api/v1/ask", json={"question": "QQS stavkasi qancha?"})
    c.post("/api/v1/generate", json={"instruction": "schyot-faktura tayyorla"})
    tasks = c.get("/api/v1/tasks").json()
    check("2 ta interaksiya task sifatida yozildi", len(tasks) == before + 2)

    logged = [t for t in tasks if t["title"].startswith("ask:")]
    check("ask-task Completed va manbalarga bog'langan",
          bool(logged) and logged[-1]["status"] == "Completed"
          and len(logged[-1]["related_knowledge"]) > 0)

    done = c.get("/api/v1/tasks", params={"status": "Completed"}).json()
    check("status bo'yicha filtr ishlaydi",
          bool(done) and all(t["status"] == "Completed" for t in done))

    passed = sum(ok for _, ok in checks)
    print(f"\nNATIJA: {passed}/{len(checks)} PASS")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
