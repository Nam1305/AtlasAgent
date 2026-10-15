"""Model gateway.

A single chokepoint between the app and the LLM provider. Every request goes
through `complete()` which:
  - validates inputs
  - calls the provider
  - normalises the response into a known shape (ChatResponse)
  - turns any provider error into a structured `ModelGatewayError`

The rest of the app never imports httpx or the provider SDK directly.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any

import httpx

from .config import Settings, get_settings
from .schemas import ChatMessage, ChatResponse, UsageInfo

logger = logging.getLogger(__name__)

GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class ModelGatewayError(RuntimeError):
    """Raised when the upstream model call fails for a known, structured reason."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _messages_to_prompt(messages: list[ChatMessage]) -> tuple[str, str | None]:
    """Collapse the message list into (single prompt, system instruction).

    Gemini's generateContent API takes a systemInstruction and a list of
    contents. For the simple Week 0 chatbot we fold everything into one
    user turn and keep the system prompt separate.
    """
    system_parts: list[str] = []
    user_parts: list[str] = []
    for m in messages:
        if m.role == "system":
            system_parts.append(m.content)
        elif m.role == "user":
            user_parts.append(f"User: {m.content}")
        else:
            user_parts.append(f"Assistant: {m.content}")
    system = "\n".join(system_parts) if system_parts else None
    prompt = "\n".join(user_parts) or "Hello"
    return prompt, system


async def complete(
    messages: list[ChatMessage],
    *,
    settings: Settings | None = None,
    model_override: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    request_id: str | None = None,
) -> ChatResponse:
    """Call the model and return a validated ChatResponse.

    Raises ModelGatewayError with a stable `code` so the API layer can map it
    to an HTTP status without leaking provider internals.
    """
    settings = settings or get_settings()
    request_id = request_id or str(uuid.uuid4())
    model = model_override or settings.gemini_model
    temperature = temperature if temperature is not None else settings.model_temperature
    max_tokens = max_tokens or settings.model_max_tokens

    if not settings.gemini_api_key:
        raise ModelGatewayError(
            code="model_api_key_missing",
            message="GEMINI_API_KEY is not configured on the server",
        )

    prompt, system = _messages_to_prompt(messages)

    body: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}

    url = f"{GEMINI_ENDPOINT.format(model=model)}?key={settings.gemini_api_key}"

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            resp = await client.post(url, json=body)
    except httpx.TimeoutException as exc:
        logger.warning("model_timeout request_id=%s model=%s", request_id, model)
        raise ModelGatewayError(
            code="model_timeout", message="Model request timed out"
        ) from exc
    except httpx.HTTPError as exc:
        logger.warning("model_network_error request_id=%s err=%s", request_id, exc)
        raise ModelGatewayError(
            code="model_network_error", message="Could not reach the model provider"
        ) from exc

    if resp.status_code != 200:
        # Log the provider's text but don't echo it to the client.
        logger.warning(
            "model_non_200 request_id=%s status=%s body=%s",
            request_id,
            resp.status_code,
            resp.text[:300],
        )
        raise ModelGatewayError(
            code="model_upstream_error",
            message=f"Model provider returned status {resp.status_code}",
        )

    data = resp.json()
    try:
        candidate = data["candidates"][0]
        text = candidate["content"]["parts"][0]["text"]
        finish = candidate.get("finishReason", "stop")
    except (KeyError, IndexError, TypeError) as exc:
        logger.warning("model_bad_shape request_id=%s data=%s", request_id, str(data)[:300])
        raise ModelGatewayError(
            code="model_bad_response", message="Model response had an unexpected shape"
        ) from exc

    usage_meta = data.get("usageMetadata", {}) or {}
    usage = UsageInfo(
        prompt_tokens=int(usage_meta.get("promptTokenCount", 0)),
        completion_tokens=int(usage_meta.get("candidatesTokenCount", 0)),
        total_tokens=int(usage_meta.get("totalTokenCount", 0)),
    )

    return ChatResponse(
        request_id=request_id,
        content=text,
        model=model,
        finish_reason=str(finish).lower(),
        usage=usage,
    )
