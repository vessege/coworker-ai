"""Request dependencies: tenant authentication + credit enforcement."""

from __future__ import annotations

from fastapi import Header, HTTPException

from app.core.config import get_settings
from app.core.tenancy import Tenant, TenantStore

_settings = get_settings()
_store = TenantStore(_settings.tenants_file, _settings.dev_mode, _settings.dev_api_key)


def get_store() -> TenantStore:
    return _store


def require_tenant(x_api_key: str | None = Header(default=None)) -> Tenant:
    tenant = _store.resolve(x_api_key)
    if tenant is None:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    if tenant.over_limit():
        raise HTTPException(status_code=429, detail="Credit limit reached")
    return tenant
