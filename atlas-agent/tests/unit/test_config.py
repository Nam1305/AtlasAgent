"""Tests for Settings / config loading from environment."""
from __future__ import annotations

import pytest


def test_settings_loads_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "abc")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("MODEL_TEMPERATURE", "0.5")
    monkeypatch.setenv("MODEL_MAX_TOKENS", "256")

    from app.config import get_settings
    get_settings.cache_clear()

    s = get_settings()
    assert s.gemini_api_key == "abc"
    assert s.gemini_model == "gemini-2.5-flash"
    assert s.model_temperature == 0.5
    assert s.model_max_tokens == 256


def test_settings_defaults_when_no_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    from app.config import get_settings
    get_settings.cache_clear()

    s = get_settings()
    assert s.gemini_api_key == ""
    assert s.gemini_model  # some default
    assert 0.0 <= s.model_temperature <= 2.0
