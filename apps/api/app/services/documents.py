"""Per-tenant uploaded documents (Company Context v1).

Uploaded business documents are indexed with the same tokenizer/synonym
expansion as the KB and searched alongside it, so /ask can ground answers in
the tenant's own paperwork. In-memory (resets on restart) — the pgvector/
Postgres upgrade path replaces the store, not the interface.
"""

from __future__ import annotations

from app.services.knowledge_base import Asset, _expand, _index_tokens, _tokens


class DocumentStore:
    def __init__(self) -> None:
        self._docs: dict[str, list[Asset]] = {}  # tenant_id -> docs

    def add(self, tenant_id: str, name: str, content: str) -> Asset:
        docs = self._docs.setdefault(tenant_id, [])
        doc = Asset(
            id=f"DOC-{len(docs) + 1:03d}",
            title=name,
            category="uploaded-document",
            path=f"tenant://{tenant_id}/{name}",
            source_url="uploaded by tenant",
            valid_from="",
            last_review="",
            body=content,
            tags=[],
            type="DOCUMENT",
            role="",
            department="",
            summary=content.strip().splitlines()[0][:150] if content.strip() else "",
            status="Published",
            confidence=1.0,
        )
        doc._tokens = _index_tokens(doc.title + " " + doc.body)
        docs.append(doc)
        return doc

    def list(self, tenant_id: str) -> list[Asset]:
        return self._docs.get(tenant_id, [])

    def search(self, tenant_id: str, query: str, top_k: int,
               min_score: float) -> list[tuple[Asset, float]]:
        q = _expand(_tokens(query))
        if not q:
            return []
        scored: list[tuple[Asset, float]] = []
        for doc in self._docs.get(tenant_id, []):
            title_tokens = _index_tokens(doc.title)
            score = 0.0
            for term in q:
                if term in title_tokens:
                    score += 2.0
                elif term in doc._tokens:
                    score += 1.0
            if score >= min_score:
                scored.append((doc, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
