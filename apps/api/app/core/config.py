from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Reads from environment / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CoWorker AI"
    app_env: str = "development"

    # LLM. Default provider is Anthropic (Claude); pluggable.
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-5"
    anthropic_api_key: str = ""

    # Knowledge base root. Defaults to the repo root (4 levels up from this file:
    # app/core/config.py -> app -> api -> apps -> repo root).
    kb_root: Path = Path(__file__).resolve().parents[4]

    # Retrieval
    retrieval_top_k: int = 4
    retrieval_min_score: float = 1.0

    # CORS (comma-separated origins allowed to call the API from the browser)
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
