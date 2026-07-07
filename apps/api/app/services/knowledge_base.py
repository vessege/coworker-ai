"""Knowledge Base loader + lexical retrieval.

MVP retrieval: loads the markdown assets from the repo's knowledge directories,
parses YAML front-matter, and scores by term overlap. This is intentionally
dependency-free (no vector DB) so the API runs anywhere for the pilot.
Upgrade path: replace `search()` internals with pgvector embeddings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter

# Directories under the KB root that hold assets.
KB_DIRS = [
    "knowledge-assets",
    "faq",
    "workflow-assets",
    "checklists",
    "templates",
    "business-rules",
    "glossary",
    "policies",
    "decision-trees",
]

_WORD_RE = re.compile(r"[\wʼ'-]+", re.UNICODE)

# Cross-language / synonym groups (uz / ru / en + common misspellings).
# A query term in any group is expanded to the whole group before scoring, so
# "ндс", "nds" or "vat" all match assets that say "qqs". This is the main lever
# against retrieval misses on multilingual SME input.
_SYNONYM_GROUPS = [
    {"qqs", "ндс", "nds", "vat"},
    {"aylanma", "оборот", "оборотный", "oborot", "turnover"},
    {"foyda", "прибыль", "pribil", "profit"},
    {"soliq", "налог", "nalog", "tax"},
    {"muddat", "срок", "srok", "deadline", "qachon", "когда", "kogda", "when"},
    {"jarima", "штраф", "shtraf", "penya", "пеня", "penalty", "fine"},
    {"stavka", "ставка", "rate", "foiz", "процент", "percent"},
    {"schyot", "счет", "счёт", "faktura", "фактура", "invoice", "hisobvaraq"},
    {"akt", "акт", "act", "dalolatnoma"},
    {"ijtimoiy", "социальный", "social"},
    {"rejim", "режим", "regime"},
    {"yatt", "ип", "ip", "tadbirkor"},
    {"xat", "письмо", "pismo", "letter"},
    {"hujjat", "документ", "dokument", "document"},
    {"royxat", "регистрация", "register", "registratsiya"},
    {"shablon", "шаблон", "template", "namuna"},
    {"sinov", "испытательный", "probation", "ispitatelniy"},
    {"muddat", "срок", "term"},
    {"tatil", "отпуск", "otpusk", "leave", "ta'til", "taʼtil"},
    {"buyruq", "приказ", "prikaz", "order"},
    {"mehnat", "трудовой", "labour", "labor", "trudovoy"},
    {"xodim", "сотрудник", "работник", "employee", "ishchi"},
    {"malumotnoma", "ma'lumotnoma", "справка", "spravka", "certificate"},
    {"ishonchnoma", "доверенность", "doverennost"},
]
_ALIAS: dict[str, set[str]] = {}
for _g in _SYNONYM_GROUPS:
    for _w in _g:
        _ALIAS.setdefault(_w, set()).update(_g)


# Light suffix stripping for Uzbek/Russian agglutination, so "fakturada"
# matches "faktura" and "muddati" matches "muddat". Longest suffixes first;
# stems shorter than 3 chars are not produced.
_SUFFIXES = [
    "larining", "laridan", "larini", "larga", "lardan", "larda", "larni",
    "lari", "ning", "dagi", "idan", "ida", "ini", "iga", "lar",
    "dan", "da", "ga", "ni", "im", "si", "i",
    "ами", "ями", "ого", "его", "ой", "ый", "ая", "ые", "ов", "ах", "ам", "ом", "е", "ы", "а", "и", "у",
]


def _stems(token: str) -> set[str]:
    out = {token}
    for suf in _SUFFIXES:
        if token.endswith(suf) and len(token) - len(suf) >= 3:
            out.add(token[: -len(suf)])
    return out


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _WORD_RE.findall(text or "")]


def _index_tokens(text: str) -> set[str]:
    """Tokens + stems, for building an index."""
    out: set[str] = set()
    for t in _tokens(text):
        out |= _stems(t)
    return out


def _expand(terms: list[str]) -> set[str]:
    out: set[str] = set()
    for t in terms:
        for s in _stems(t):
            out.add(s)
            out |= _ALIAS.get(s, set())
    return out


# RFC-0002 lifecycle statuses usable by Company Brain.
USABLE_STATUS = {"approved", "published"}


@dataclass
class Asset:
    id: str
    title: str
    category: str
    path: str
    source_url: str
    valid_from: str
    last_review: str
    body: str
    tags: list[str] = field(default_factory=list)
    # RFC-0002 fields
    type: str = ""
    role: str = ""
    department: str = ""
    summary: str = ""
    status: str = "Published"
    confidence: float = 0.0
    workflow: dict = field(default_factory=dict)  # RFC-0003 structured spec
    _tokens: set[str] = field(default_factory=set)

    def excerpt(self, limit: int = 1800) -> str:
        return self.body[:limit]


class KnowledgeBase:
    def __init__(self, root: Path):
        self.root = root
        self.assets: list[Asset] = []

    def load(self) -> "KnowledgeBase":
        self.assets = []
        for d in KB_DIRS:
            directory = self.root / d
            if not directory.is_dir():
                continue
            for md in sorted(directory.glob("*.md")):
                if md.name.lower() == "readme.md":
                    continue
                post = frontmatter.load(md)
                meta = post.metadata
                try:
                    confidence = float(meta.get("confidence", 0.0) or 0.0)
                except (TypeError, ValueError):
                    confidence = 0.0
                asset = Asset(
                    id=str(meta.get("id", md.stem)),
                    title=str(meta.get("title", md.stem)),
                    category=str(meta.get("category", d)),
                    path=str(md.relative_to(self.root)),
                    source_url=str(meta.get("source_url", "")),
                    valid_from=str(meta.get("valid_from", "")),
                    last_review=str(meta.get("last_review", "")),
                    body=post.content,
                    tags=[str(t) for t in (meta.get("tags") or [])],
                    type=str(meta.get("type", "")),
                    role=str(meta.get("role", "")),
                    department=str(meta.get("department", "")),
                    summary=str(meta.get("summary", "")),
                    status=str(meta.get("status", "Published")),
                    confidence=confidence,
                    workflow=dict(meta.get("workflow") or {}),
                )
                # RFC-0002: only Approved/Published assets are usable by Company Brain.
                if asset.status.lower() not in USABLE_STATUS:
                    continue
                index_text = " ".join(
                    [asset.title, asset.summary, " ".join(asset.tags), asset.category, asset.body]
                )
                asset._tokens = _index_tokens(index_text)
                self.assets.append(asset)
        return self

    def search(self, query: str, top_k: int, min_score: float) -> list[tuple[Asset, float]]:
        q = _expand(_tokens(query))
        if not q:
            return []
        scored: list[tuple[Asset, float]] = []
        for asset in self.assets:
            # Weighted overlap: title/tag hits count double.
            title_tag = _index_tokens(asset.title + " " + " ".join(asset.tags))
            score = 0.0
            for term in q:
                if term in title_tag:
                    score += 2.0
                elif term in asset._tokens:
                    score += 1.0
            if score >= min_score:
                scored.append((asset, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
