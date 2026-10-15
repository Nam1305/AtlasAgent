"""Application configuration loaded from environment variables."""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings are loaded from .env / environment, never hard-coded in code."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Gemini / model
    gemini_api_key: str = Field(default="", description="Gemini API key")
    gemini_model: str = Field(default="gemini-2.5-flash", description="Default Gemini model")
    model_temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    model_max_tokens: int = Field(default=1024, ge=1, le=8192)

    # API
    api_title: str = "Atlas Agent API"
    api_version: str = "0.1.0"
    log_level: str = "INFO"

    # Safety
    max_request_chars: int = 8000
    request_timeout_seconds: float = 30.0


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    We never log the API key. If the key is missing we still return a Settings
    object so /health works; /chat surfaces a structured error instead.
    """
    return Settings()
