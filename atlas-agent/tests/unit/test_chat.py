"""Tests for the /chat endpoint (using a stubbed model gateway)."""
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


def test_chat_returns_valid_response_schema(client: TestClient, monkeypatch) -> None:
    from app.schemas import ChatResponse, UsageInfo
    from app.api.routes import chat as chat_route

    async def fake_complete(messages, **kwargs):
        return ChatResponse(
            request_id=kwargs.get("request_id", "rid"),
            content="hello back",
            model="gemini-2.5-flash",
            finish_reason="stop",
            usage=UsageInfo(prompt_tokens=4, completion_tokens=2, total_tokens=6),
        )

    monkeypatch.setattr(chat_route, "complete", fake_complete)

    resp = client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "hi"}]},
        headers={"X-Request-ID": "abc-123"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["content"] == "hello back"
    assert body["model"] == "gemini-2.5-flash"
    assert body["request_id"] == "abc-123"
    assert body["usage"]["total_tokens"] == 6


def test_chat_rejects_empty_messages(client: TestClient) -> None:
    resp = client.post("/chat", json={"messages": []})
    assert resp.status_code == 422


def test_chat_returns_structured_error_on_model_failure(
    client: TestClient, monkeypatch
) -> None:
    from app.model_gateway import ModelGatewayError
    from app.api.routes import chat as chat_route

    async def fake_complete(messages, **kwargs):
        raise ModelGatewayError(code="model_timeout", message="timeout")

    monkeypatch.setattr(chat_route, "complete", fake_complete)

    resp = client.post(
        "/chat", json={"messages": [{"role": "user", "content": "hi"}]}
    )
    assert resp.status_code == 504
    body = resp.json()
    assert "detail" in body
    assert body["detail"]["error"]["code"] == "model_timeout"


def test_chat_missing_api_key_returns_503(client: TestClient, monkeypatch) -> None:
    from app.model_gateway import ModelGatewayError
    from app.api.routes import chat as chat_route

    async def fake_complete(messages, **kwargs):
        raise ModelGatewayError(code="model_api_key_missing", message="no key")

    monkeypatch.setattr(chat_route, "complete", fake_complete)

    resp = client.post(
        "/chat", json={"messages": [{"role": "user", "content": "hi"}]}
    )
    assert resp.status_code == 503
    assert resp.json()["detail"]["error"]["code"] == "model_api_key_missing"
