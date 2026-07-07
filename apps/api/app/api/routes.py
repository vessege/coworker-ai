from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.services.knowledge_base import KnowledgeBase
from app.services.llm import LLMEngine

router = APIRouter()

_settings = get_settings()
_kb = KnowledgeBase(_settings.kb_root).load()
_llm = LLMEngine(_settings)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, examples=["QQS hisobotini qachon topshiraman?"])


class SourceRef(BaseModel):
    id: str
    source_url: str
    verified: str = ""


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceRef]
    grounded: bool
    mode: str = ""


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "assets_loaded": len(_kb.assets)}


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


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    hits = _kb.search(
        req.question, _settings.retrieval_top_k, _settings.retrieval_min_score
    )
    result = _llm.answer(req.question, hits)
    return AskResponse(**result)


class GenerateRequest(BaseModel):
    instruction: str = Field(
        ...,
        min_length=2,
        examples=["Schyot-faktura tayyorla: sotuvchi OOO Alfa STIR 300..."],
    )


@router.post("/generate")
def generate(req: GenerateRequest) -> dict:
    hits = _kb.search(req.instruction, _settings.retrieval_top_k, _settings.retrieval_min_score)
    return _llm.generate(req.instruction, hits)
