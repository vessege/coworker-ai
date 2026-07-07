"""Minimal multi-tenant layer (auth + usage metering).

A tenant = a company using CoWorker AI. Requests authenticate with an
`X-API-Key` header that resolves to a tenant; usage is metered against the
tenant's credit limit. Tenants load from a JSON file; in development a fallback
"dev" tenant keeps local demos working without configuration.

This is the MVP foundation for RFC's per-tenant Company Context / Memory /
billing. State is in-memory (resets on restart) — move to Postgres/Redis for
production.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Tenant:
    id: str
    name: str
    api_key: str
    plan: str = "free"
    credit_limit: int = -1  # -1 = unlimited
    used: int = field(default=0)

    def remaining(self) -> int:
        return -1 if self.credit_limit < 0 else max(0, self.credit_limit - self.used)

    def over_limit(self) -> bool:
        return self.credit_limit >= 0 and self.used >= self.credit_limit


class TenantStore:
    def __init__(self, tenants_file: Path, dev_mode: bool, dev_api_key: str):
        self.dev_mode = dev_mode
        self._by_key: dict[str, Tenant] = {}
        if tenants_file.is_file():
            for t in json.loads(tenants_file.read_text()):
                tenant = Tenant(
                    id=t["id"], name=t.get("name", t["id"]), api_key=t["api_key"],
                    plan=t.get("plan", "free"), credit_limit=int(t.get("credit_limit", -1)),
                )
                self._by_key[tenant.api_key] = tenant
        if dev_mode and not self._by_key:
            dev = Tenant(id="dev", name="Development", api_key=dev_api_key,
                         plan="dev", credit_limit=-1)
            self._by_key[dev.api_key] = dev
            self._dev = dev
        else:
            self._dev = None

    def resolve(self, api_key: str | None) -> Tenant | None:
        if api_key and api_key in self._by_key:
            return self._by_key[api_key]
        # In dev mode, allow anonymous access via the dev tenant.
        if self.dev_mode and self._dev is not None:
            return self._dev
        return None

    def record_usage(self, tenant: Tenant, credits: int = 1) -> None:
        tenant.used += credits
