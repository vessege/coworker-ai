from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.deps import get_store, require_tenant
from app.core.config import MODELS, get_settings, provider_key
from app.core.tenancy import Tenant
from app.services.knowledge_base import KnowledgeBase
from app.services.llm import LLMEngine

router = APIRouter()

_settings = get_settings()
_kb = KnowledgeBase(_settings.kb_root).load()
_llm = LLMEngine(_settings)


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


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest, tenant: Tenant = Depends(require_tenant)) -> AskResponse:
    hits = _kb.search(
        req.question, _settings.retrieval_top_k, _settings.retrieval_min_score
    )
    result = _llm.answer(req.question, hits, model=req.model)
    get_store().record_usage(tenant)
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
    return result
