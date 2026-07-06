"""LLM engine wrapper with grounding guardrails.

Design principle (see docs/blueprints/mvp-accountant.md):
answer ONLY from retrieved KB context; cite sources; refuse when unsure.
"""

from __future__ import annotations

from app.core.config import Settings
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

    def _client(self):
        # Imported lazily so the API boots even without the SDK/key configured.
        from anthropic import Anthropic

        return Anthropic(api_key=self.settings.anthropic_api_key)

    def answer(self, question: str, hits: list[tuple[Asset, float]]) -> dict:
        if not hits:
            return {"answer": REFUSAL, "sources": [], "grounded": False}

        sources = [
            {"id": a.id, "source_url": a.source_url, "verified": a.last_review}
            for a, _ in hits
        ]

        if not self.settings.anthropic_api_key:
            # Offline/dev mode: no key configured. Return retrieved context so the
            # pipeline is demonstrable without external calls.
            return {
                "answer": "[LLM key not configured — returning retrieved context]\n\n"
                + build_context(hits),
                "sources": sources,
                "grounded": True,
                "mode": "retrieval-only",
            }

        message = self._client().messages.create(
            model=self.settings.llm_model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"KNOWLEDGE CONTEXT:\n\n{build_context(hits)}\n\n"
                    f"USER QUESTION:\n{question}",
                }
            ],
        )
        text = "".join(b.text for b in message.content if b.type == "text")
        return {"answer": text, "sources": sources, "grounded": True, "mode": "llm"}
