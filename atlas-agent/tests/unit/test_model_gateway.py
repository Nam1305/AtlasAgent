"""Tests for the model gateway: input shaping, error handling, response parsing."""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_complete_raises_when_api_key_missing(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "")
    from app.config import get_settings
    get_settings.cache_clear()
    from app.model_gateway import complete, ModelGatewayError
    from app.schemas import ChatMessage

    with pytest.raises(ModelGatewayError) as exc:
        await complete([ChatMessage(role="user", content="hi")])
    assert exc.value.code == "model_api_key_missing"


@pytest.mark.asyncio
async def test_complete_handles_upstream_non_200(monkeypatch) -> None:
    """A 400 from Gemini should become a structured model_upstream_error."""
    import httpx

    monkeypatch.setenv("GEMINI_API_KEY", "test")
    from app.config import get_settings
    get_settings.cache_clear()
    from app.model_gateway import complete, ModelGatewayError
    from app.schemas import ChatMessage

    class FakeAsyncClient:
        def __init__(self, *a, **kw): ...
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, json):
            req = httpx.Request("POST", url, json=json)
            return httpx.Response(400, text="bad request", request=req)

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    with pytest.raises(ModelGatewayError) as exc:
        await complete([ChatMessage(role="user", content="hi")])
    assert exc.value.code == "model_upstream_error"


@pytest.mark.asyncio
async def test_complete_parses_successful_response(monkeypatch) -> None:
    import httpx
    import json as _json

    monkeypatch.setenv("GEMINI_API_KEY", "test")
    from app.config import get_settings
    get_settings.cache_clear()
    from app.model_gateway import complete
    from app.schemas import ChatMessage

    payload = {
        "candidates": [
            {"content": {"parts": [{"text": "hello"}]}, "finishReason": "STOP"}
        ],
        "usageMetadata": {
            "promptTokenCount": 3,
            "candidatesTokenCount": 2,
            "totalTokenCount": 5,
        },
    }

    class FakeAsyncClient:
        def __init__(self, *a, **kw): ...
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, json):
            req = httpx.Request("POST", url)
            return httpx.Response(200, text=_json.dumps(payload), request=req)

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    resp = await complete([ChatMessage(role="user", content="hi")])
    assert resp.content == "hello"
    assert resp.finish_reason == "stop"
    assert resp.usage.total_tokens == 5
