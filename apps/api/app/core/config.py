from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Reads from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CoWorker AI"
    app_env: str = "development"

    # LLM. Multi-provider routing; default Anthropic (Claude).
    default_model: str = "claude-sonnet-5"
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Self-hosted model (Ollama, OpenAI-compatible /v1 endpoint). Empty ollama_model
    # means no local model is available; set it to the pulled tag (e.g.
    # "qwen2.5:7b-instruct") to enable it in the model selector.
    ollama_base_url: str = "http://127.0.0.1:11434/v1"
    ollama_model: str = ""

    # Knowledge base root. Defaults to the repo root (4 levels up from this file:
    # app/core/config.py -> app -> api -> apps -> repo root).
    kb_root: Path = Path(__file__).resolve().parents[4]

    # Retrieval
    retrieval_top_k: int = 4
    retrieval_min_score: float = 1.0

    # CORS (comma-separated origins allowed to call the API from the browser)
    cors_origins: list[str] = ["http://localhost:3000"]

    # Multi-tenancy / auth
    tenants_file: Path = Path(__file__).resolve().parents[4] / "config" / "tenants.json"
    dev_api_key: str = "dev-key"

    @property
    def dev_mode(self) -> bool:
        return self.app_env != "production"


# Model registry: id -> {provider, label}. The selector shows these; a model is
# "available" only if its provider's API key is configured.
MODELS: dict[str, dict] = {
    "claude-sonnet-5": {"provider": "anthropic", "label": "Claude Sonnet 5"},
    "claude-opus-4-8": {"provider": "anthropic", "label": "Claude Opus 4.8"},
    "claude-haiku-4-5-20251001": {"provider": "anthropic", "label": "Claude Haiku 4.5"},
    "gpt-5.5": {"provider": "openai", "label": "GPT-5.5"},
    "gpt-5": {"provider": "openai", "label": "GPT-5"},
    "qwen2.5:7b-instruct": {"provider": "ollama", "label": "Qwen2.5 7B (lokal, VPS)"},
}


def provider_key(settings: "Settings", provider: str) -> str:
    return {
        "anthropic": settings.anthropic_api_key,
        "openai": settings.openai_api_key,
        "ollama": settings.ollama_model,
    }.get(provider, "")


@lru_cache
def get_settings() -> Settings:
    return Settings()
