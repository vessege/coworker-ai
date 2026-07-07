"""1C:Enterprise integration (read-only, OData standard interface).

1C 8.3+ publishes a standard OData endpoint (…/odata/standard.odata/). Each
tenant configures its own base URL + credentials; `sync` pulls the configured
entities, renders them as readable bilingual summaries, and stores them in the
tenant's DocumentStore — so /ask grounds answers in live 1C data with zero
extra retrieval machinery.

Read-only by design (Phase 3 writes back). The HTTP fetcher is injectable so
tests run against a mock 1C.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

# Default entities to sync: (odata entity, human name, row renderer)
DEFAULT_ENTITIES = ["Catalog_Контрагенты", "Document_РеализацияТоваровУслуг"]

ENTITY_LABELS = {
    "Catalog_Контрагенты": "1C Kontragentlar / Counterparties",
    "Document_РеализацияТоваровУслуг": "1C Sotuvlar (realizatsiya) / Sales documents",
}


@dataclass
class OneCConfig:
    base_url: str
    username: str = ""
    password: str = ""
    entities: list[str] = field(default_factory=lambda: list(DEFAULT_ENTITIES))
    last_sync: str = ""
    last_error: str = ""


def _http_fetch(cfg: OneCConfig, entity: str) -> list[dict]:
    """Real fetcher: GET {base}/odata/standard.odata/{entity}?$format=json."""
    import httpx

    url = f"{cfg.base_url.rstrip('/')}/odata/standard.odata/{entity}"
    auth = (cfg.username, cfg.password) if cfg.username else None
    r = httpx.get(url, params={"$format": "json", "$top": "500"},
                  auth=auth, timeout=20)
    r.raise_for_status()
    return r.json().get("value", [])


def render_entity(entity: str, rows: list[dict]) -> str:
    """Render 1C rows as a readable markdown doc for retrieval/grounding."""
    label = ENTITY_LABELS.get(entity, entity)
    lines = [f"# {label}", f"Manba: 1C OData ({entity}) · yozuvlar: {len(rows)}", ""]
    for r in rows[:200]:
        if entity == "Catalog_Контрагенты":
            lines.append(
                f"- Kontragent: {r.get('Description','?')} | STIR (INN): {r.get('ИНН','—')}"
                f" | Kod: {r.get('Code','—')}"
            )
        elif entity == "Document_РеализацияТоваровУслуг":
            lines.append(
                f"- Sotuv hujjati №{r.get('Number','?')} | Sana: {r.get('Date','?')}"
                f" | Kontragent: {r.get('Контрагент','—')} | Summa: {r.get('СуммаДокумента','—')} so'm"
            )
        else:
            lines.append(f"- {r}")
    return "\n".join(lines)


class OneCIntegration:
    def __init__(self, fetcher: Callable[[OneCConfig, str], list[dict]] | None = None):
        self._configs: dict[str, OneCConfig] = {}  # tenant_id -> config
        self._fetch = fetcher or _http_fetch

    def configure(self, tenant_id: str, base_url: str, username: str = "",
                  password: str = "", entities: list[str] | None = None) -> OneCConfig:
        cfg = OneCConfig(base_url=base_url, username=username, password=password)
        if entities:
            cfg.entities = entities
        self._configs[tenant_id] = cfg
        return cfg

    def status(self, tenant_id: str) -> dict:
        cfg = self._configs.get(tenant_id)
        if cfg is None:
            return {"configured": False}
        return {"configured": True, "base_url": cfg.base_url,
                "entities": cfg.entities, "last_sync": cfg.last_sync,
                "last_error": cfg.last_error}

    def sync(self, tenant_id: str, doc_store) -> dict:
        """Pull entities and (re)load them into the tenant's DocumentStore."""
        cfg = self._configs.get(tenant_id)
        if cfg is None:
            raise ValueError("1C is not configured for this tenant")
        synced, errors = [], []
        for entity in cfg.entities:
            try:
                rows = self._fetch(cfg, entity)
                doc = doc_store.add(tenant_id, f"1c-{entity}.md",
                                    render_entity(entity, rows))
                synced.append({"entity": entity, "rows": len(rows), "doc": doc.id})
            except Exception as e:  # keep syncing other entities
                errors.append({"entity": entity, "error": str(e)})
        cfg.last_sync = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        cfg.last_error = "; ".join(e["error"] for e in errors) if errors else ""
        return {"synced": synced, "errors": errors, "last_sync": cfg.last_sync}
