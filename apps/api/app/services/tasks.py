"""Task Assets (RFC-0004) — the executable work unit.

Knowledge explains, Workflow organizes, Task executes. This is the thin
runtime slice of RFC-0004: per-tenant task records with the canonical
metadata, a validated state machine, and the Learning Rule — every /ask and
/generate interaction is recorded as a completed Task (nothing is discarded).
In-memory for the MVP; Postgres is the production upgrade path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import count

# RFC-0004 task states and allowed transitions.
STATES = ["Created", "Planned", "Running", "Waiting", "Review", "Completed",
          "Archived", "Cancelled"]
TRANSITIONS: dict[str, set[str]] = {
    "Created": {"Planned", "Running", "Cancelled"},
    "Planned": {"Running", "Cancelled"},
    "Running": {"Waiting", "Review", "Completed", "Cancelled"},
    "Waiting": {"Running", "Cancelled"},
    "Review": {"Running", "Completed", "Cancelled"},
    "Completed": {"Archived"},
    "Archived": set(),
    "Cancelled": {"Archived"},  # cancelled tasks are kept for learning
}
PRIORITIES = ["Critical", "High", "Normal", "Low", "Background"]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    business_goal: str = ""
    role: str = ""
    department: str = ""
    priority: str = "Normal"
    status: str = "Created"
    deadline: str = ""
    requester: str = ""
    assigned_agent: str = "CoWorker AI"
    related_workflow: str = ""
    related_knowledge: list[str] = field(default_factory=list)
    related_documents: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        return dict(self.__dict__)


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, list[Task]] = {}  # tenant_id -> tasks
        self._seq: dict[str, count] = {}

    def create(self, tenant_id: str, **kwargs) -> Task:
        seq = self._seq.setdefault(tenant_id, count(1))
        priority = kwargs.pop("priority", "Normal")
        if priority not in PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}")
        task = Task(id=f"TASK-{next(seq):04d}", priority=priority, **kwargs)
        self._tasks.setdefault(tenant_id, []).append(task)
        return task

    def list(self, tenant_id: str, status: str | None = None) -> list[Task]:
        tasks = self._tasks.get(tenant_id, [])
        return [t for t in tasks if status is None or t.status == status]

    def get(self, tenant_id: str, task_id: str) -> Task | None:
        return next((t for t in self._tasks.get(tenant_id, []) if t.id == task_id), None)

    def transition(self, tenant_id: str, task_id: str, new_status: str) -> Task:
        task = self.get(tenant_id, task_id)
        if task is None:
            raise KeyError(task_id)
        if new_status not in STATES:
            raise ValueError(f"Unknown status: {new_status}")
        if new_status not in TRANSITIONS[task.status]:
            raise ValueError(f"Illegal transition {task.status} -> {new_status}")
        task.status = new_status
        task.updated_at = _now()
        return task

    def log_interaction(self, tenant_id: str, kind: str, request_text: str,
                        sources: list[str], role: str = "", model: str = "") -> Task:
        """RFC-0004 Learning Rule: record an /ask or /generate interaction as a
        completed Task so no completed work is discarded."""
        task = self.create(
            tenant_id,
            title=f"{kind}: {request_text[:80]}",
            description=request_text,
            business_goal="Answer/produce grounded output for the user",
            role=role,
            requester=tenant_id,
            related_knowledge=[s for s in sources if not s.startswith("DOC-")],
            related_documents=[s for s in sources if s.startswith("DOC-")],
            deliverables=[f"{kind} response ({model or 'retrieval-only'})"],
        )
        task.status = "Completed"  # interaction tasks are born completed
        task.updated_at = _now()
        return task
