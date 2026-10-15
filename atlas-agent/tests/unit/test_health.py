"""Tests for the /health endpoint."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    from app.config import get_settings
    get_settings.cache_clear()
    from app.main import create_app

    return TestClient(create_app())


def test_health_returns_ok_when_key_configured(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["api_key_configured"] is True
    assert "version" in data
    assert "model" in data


def test_health_degraded_when_no_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    from app.config import get_settings
    get_settings.cache_clear()
    from app.main import create_app

    c = TestClient(create_app())
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "degraded"
    assert resp.json()["api_key_configured"] is False
