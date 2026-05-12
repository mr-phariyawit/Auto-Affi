"""Application settings loaded from environment via pydantic-settings.

Secrets MUST come from Vault / SOPS in non-dev environments. .env is for
local dev only and is gitignored.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Top-level config namespace."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="AUTO_AFFI__",
        extra="ignore",
    )

    env: Literal["dev", "staging", "prod"] = "dev"

    anthropic_api_key: SecretStr = Field(default=SecretStr(""))
    kie_api_key: SecretStr = Field(default=SecretStr(""))
    elevenlabs_api_key: SecretStr = Field(default=SecretStr(""))
    shopee_app_id: SecretStr = Field(default=SecretStr(""))
    shopee_secret: SecretStr = Field(default=SecretStr(""))

    postgres_dsn: str = "postgresql+asyncpg://localhost:5432/auto_affi"
    redis_url: str = "redis://localhost:6379/0"
    s3_bucket: str = "auto-affi-dev"

    daily_opus_budget_usd: float = 50.0
    per_video_budget_usd: float = 3.32


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached app settings."""
    return Settings()
