"""LLM engine wrapper with grounding guardrails.

Design principle (see docs/blueprints/mvp-accountant.md):
answer ONLY from retrieved KB context; cite sources; refuse when unsure.
"""

from __future__ import annotations

from app.core.config import MODELS, Settings, provider_key
from app.services.knowledge_base import Asset

SYSTEM_PROMPT = """You are CoWorker AI, an AI coworker for Uzbek SME accountants \
and office managers. Rules:
1. Answer ONLY from the provided KNOWLEDGE CONTEXT. Never invent tax rules, \
dates, rates, or legal facts.
2. If the context does not confidently answer the question, say so and advise \
confirming with soliq.uz or the user's accountant. Do not guess.
3. Always cite the asset id and source_url you used, and the "verified as of" \
date (last_review / valid_from).
4. This is informational support, not official tax advice.
5. Reply in the same language the user asked in (Uzbek or Russian or English)."""

REFUSAL = (
    "Bazada bu savolga ishonchli javob topilmadi. Iltimos, soliq.uz rasmiy "
    "taqvimi yoki buxgalteringiz bilan tasdiqlang.\n\n"
    "(No confident answer found in the knowledge base — please verify with "
    "soliq.uz or your accountant.)"
)

GENERATE_SYSTEM = """You are CoWorker AI, generating a business document for an \
Uzbek SME. Rules:
1. Use ONLY the provided TEMPLATE structure and required fields. Do not invent \
requisites, tax rates, or legal wording beyond the template.
2. Fill placeholders with the user's provided values. Leave any missing value as \
its placeholder (e.g. [STIR]) and list what is still missing at the end.
3. Keep the official field structure and order. Output the finished document, \
then a short "Missing:" list.
4. Reply in the language of the user's request."""

NO_TEMPLATE = (
    "Bu hujjat turi uchun shablon bazada topilmadi.\n"
    "(No template for this document type found in the knowledge base.)"
)


def build_context(hits: list[tuple[Asset, float]]) -> str:
    blocks = []
    for asset, score in hits:
        blocks.append(
            f"### ASSET {asset.id} — {asset.title}\n"
            f"source_url: {asset.source_url}\n"
            f"verified: {asset.last_review or asset.valid_from}\n\n"
            f"{asset.excerpt()}"
        )
    return "\n\n---\n\n".join(blocks)


class LLMEngine:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _resolve(self, model: str | None) -> tuple[str, str, str]:
        """Return (model_id, provider, key). Falls back to the default model."""
        model_id = model if model in MODELS else self.settings.default_model
        provider = MODELS[model_id]["provider"]
        return model_id, provider, provider_key(self.settings, provider)

    def _complete(self, system: str, user: str, model_id: str, provider: str,
                  key: str, max_tokens: int) -> str:
        """Route a single completion to the chosen provider. Lazy SDK imports."""
        if provider == "anthropic":
            from anthropic import Anthropic

            msg = Anthropic(api_key=key).messages.create(
                model=model_id, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}],
            )
            return "".join(b.text for b in msg.content if b.type == "text")
        if provider == "openai":
            from openai import OpenAI

            resp = OpenAI(api_key=key).chat.completions.create(
                model=model_id, max_tokens=max_tokens,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
            )
            return resp.choices[0].message.content or ""
        if provider == "ollama":
            from openai import OpenAI

            resp = OpenAI(api_key="ollama", base_url=self.settings.ollama_base_url) \
                .chat.completions.create(
                    model=model_id, max_tokens=max_tokens,
                    messages=[{"role": "system", "content": system},
                              {"role": "user", "content": user}],
                )
            return resp.choices[0].message.content or ""
        raise ValueError(f"Unknown provider: {provider}")

    def answer(self, question: str, hits: list[tuple[Asset, float]],
               model: str | None = None) -> dict:
        if not hits:
            return {"answer": REFUSAL, "sources": [], "grounded": False}

        sources = [
            {"id": a.id, "source_url": a.source_url, "verified": a.last_review}
            for a, _ in hits
        ]
        model_id, provider, key = self._resolve(model)

        if not key:
            # No key for the chosen provider: return retrieved context so the
            # pipeline stays demonstrable without external calls.
            return {
                "answer": "[LLM key not configured — returning retrieved context]\n\n"
                + build_context(hits),
                "sources": sources, "grounded": True, "mode": "retrieval-only",
                "model": model_id,
            }

        user = f"KNOWLEDGE CONTEXT:\n\n{build_context(hits)}\n\nUSER QUESTION:\n{question}"
        text = self._complete(SYSTEM_PROMPT, user, model_id, provider, key, 1024)
        return {"answer": text, "sources": sources, "grounded": True,
                "mode": "llm", "model": model_id}

    def generate(self, instruction: str, hits: list[tuple[Asset, float]],
                 model: str | None = None) -> dict:
        templates = [(a, s) for a, s in hits if a.category == "template"]
        if not templates:
            return {"document": NO_TEMPLATE, "template": None, "grounded": False}

        asset = templates[0][0]
        source = {"id": asset.id, "source_url": asset.source_url, "verified": asset.last_review}
        model_id, provider, key = self._resolve(model)

        if not key:
            return {
                "document": "[LLM key not configured — returning template]\n\n" + asset.body,
                "template": asset.id, "source": source, "grounded": True,
                "mode": "template-only", "model": model_id,
            }

        user = f"TEMPLATE ({asset.id}):\n\n{asset.body}\n\nUSER REQUEST:\n{instruction}"
        text = self._complete(GENERATE_SYSTEM, user, model_id, provider, key, 1500)
        return {"document": text, "template": asset.id, "source": source,
                "grounded": True, "mode": "llm", "model": model_id}
