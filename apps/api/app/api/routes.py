from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.deps import get_store, require_tenant
from app.core.config import MODELS, get_settings, provider_key
from app.core.tenancy import Tenant
from app.services.documents import DocumentStore
from app.services.knowledge_base import KnowledgeBase
from app.services.llm import LLMEngine
from app.services.onec import OneCIntegration
from app.services.tasks import PRIORITIES, TaskStore

router = APIRouter()

_settings = get_settings()
_kb = KnowledgeBase(_settings.kb_root).load()
_llm = LLMEngine(_settings)
_docs = DocumentStore()
_tasks = TaskStore()
_onec = OneCIntegration()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, examples=["QQS hisobotini qachon topshiraman?"])
    model: str | None = None


class SourceRef(BaseModel):
    id: str
    source_url: str
    verified: str = ""


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceRef]
    grounded: bool
    mode: str = ""
    model: str = ""


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "assets_loaded": len(_kb.assets)}


@router.get("/models")
def models() -> list[dict]:
    """Available models for the selector; `available` reflects configured keys."""
    return [
        {
            "id": mid,
            "label": m["label"],
            "provider": m["provider"],
            "available": bool(provider_key(_settings, m["provider"])),
            "default": mid == _settings.default_model,
        }
        for mid, m in MODELS.items()
    ]


@router.get("/assets")
def assets() -> list[dict]:
    return [
        {
            "id": a.id,
            "title": a.title,
            "type": a.type,
            "role": a.role,
            "department": a.department,
            "summary": a.summary,
            "status": a.status,
            "confidence": a.confidence,
            "path": a.path,
        }
        for a in _kb.assets
    ]


@router.get("/workflows")
def workflows() -> list[dict]:
    """RFC-0003 structured workflow specs (consumable by a future workflow engine)."""
    return [
        {"id": a.id, "title": a.title, "type": a.type, "workflow": a.workflow}
        for a in _kb.assets
        if a.type in {"WORKFLOW", "SOP"} and a.workflow
    ]


@router.get("/me")
def me(tenant: Tenant = Depends(require_tenant)) -> dict:
    return {"id": tenant.id, "name": tenant.name, "plan": tenant.plan,
            "used": tenant.used, "remaining": tenant.remaining()}


class DocumentUpload(BaseModel):
    name: str = Field(..., min_length=1, examples=["schyot-faktura-158.md"])
    content: str = Field(..., min_length=10)


@router.post("/documents")
def upload_document(req: DocumentUpload, tenant: Tenant = Depends(require_tenant)) -> dict:
    doc = _docs.add(tenant.id, req.name, req.content)
    return {"id": doc.id, "title": doc.title, "summary": doc.summary}


@router.get("/documents")
def list_documents(tenant: Tenant = Depends(require_tenant)) -> list[dict]:
    return [
        {"id": d.id, "title": d.title, "summary": d.summary}
        for d in _docs.list(tenant.id)
    ]


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, tenant: Tenant = Depends(require_tenant)) -> AskResponse:
    # Search the shared KB and the tenant's own uploaded documents together.
    # The user's own documents get up to 2 reserved slots: when someone asks
    # about THEIR paperwork, it must not be crowded out by KB assets.
    top_k = _settings.retrieval_top_k
    kb_hits = _kb.search(req.question, top_k, _settings.retrieval_min_score)
    doc_hits = _docs.search(tenant.id, req.question, 2, _settings.retrieval_min_score)
    hits = doc_hits + kb_hits[: top_k - len(doc_hits)]
    hits.sort(key=lambda x: x[1], reverse=True)
    result = _llm.answer(req.question, hits, model=req.model)
    get_store().record_usage(tenant)
    # RFC-0004 Learning Rule: every interaction becomes a completed Task.
    _tasks.log_interaction(
        tenant.id, "ask", req.question,
        [s["id"] for s in result.get("sources", [])],
        model=result.get("model", ""),
    )
    return AskResponse(**result)


class GenerateRequest(BaseModel):
    instruction: str = Field(
        ...,
        min_length=2,
        examples=["Schyot-faktura tayyorla: sotuvchi OOO Alfa STIR 300..."],
    )
    model: str | None = None


@router.post("/generate")
def generate(req: GenerateRequest, tenant: Tenant = Depends(require_tenant)) -> dict:
    hits = _kb.search(req.instruction, _settings.retrieval_top_k, _settings.retrieval_min_score)
    result = _llm.generate(req.instruction, hits, model=req.model)
    get_store().record_usage(tenant)
    src = result.get("source") or {}
    _tasks.log_interaction(
        tenant.id, "generate", req.instruction,
        [src["id"]] if src.get("id") else [],
        model=result.get("model", ""),
    )
    return result


# ---- 1C integration (read-only OData sync) ----

class OneCConfigRequest(BaseModel):
    base_url: str = Field(..., min_length=8, examples=["http://1c-server/base1"])
    username: str = ""
    password: str = ""
    entities: list[str] | None = None


@router.post("/integrations/1c/config")
def onec_config(req: OneCConfigRequest, tenant: Tenant = Depends(require_tenant)) -> dict:
    cfg = _onec.configure(tenant.id, req.base_url, req.username, req.password, req.entities)
    return {"configured": True, "base_url": cfg.base_url, "entities": cfg.entities}


@router.get("/integrations/1c/status")
def onec_status(tenant: Tenant = Depends(require_tenant)) -> dict:
    return _onec.status(tenant.id)


@router.post("/integrations/1c/sync")
def onec_sync(tenant: Tenant = Depends(require_tenant)) -> dict:
    try:
        return _onec.sync(tenant.id, _docs)
    except ValueError as e:
        return {"error": str(e)}


# ---- Task Assets (RFC-0004) ----

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2)
    description: str = ""
    business_goal: str = ""
    role: str = ""
    department: str = ""
    priority: str = "Normal"
    deadline: str = ""
    related_workflow: str = ""
    deliverables: list[str] = []
    success_criteria: list[str] = []


class TaskTransition(BaseModel):
    status: str


@router.post("/tasks")
def create_task(req: TaskCreate, tenant: Tenant = Depends(require_tenant)) -> dict:
    if req.priority not in PRIORITIES:
        return {"error": f"priority must be one of {PRIORITIES}"}
    task = _tasks.create(tenant.id, requester=tenant.id, **req.model_dump())
    return task.to_dict()


@router.get("/tasks")
def list_tasks(status: str | None = None,
               tenant: Tenant = Depends(require_tenant)) -> list[dict]:
    return [t.to_dict() for t in _tasks.list(tenant.id, status)]


@router.get("/tasks/{task_id}")
def get_task(task_id: str, tenant: Tenant = Depends(require_tenant)) -> dict:
    task = _tasks.get(tenant.id, task_id)
    return task.to_dict() if task else {"error": "not found"}


@router.patch("/tasks/{task_id}/status")
def transition_task(task_id: str, req: TaskTransition,
                    tenant: Tenant = Depends(require_tenant)) -> dict:
    try:
        return _tasks.transition(tenant.id, task_id, req.status).to_dict()
    except KeyError:
        return {"error": "not found"}
    except ValueError as e:
        return {"error": str(e)}
