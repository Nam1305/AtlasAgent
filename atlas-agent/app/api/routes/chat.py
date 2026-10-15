"""POST /chat — single-turn (or multi-turn) chat completion.

Errors from the model gateway are caught here and returned as structured
`ErrorResponse` payloads so the server never 500s on a bad model output.
"""
from __future__ import annotations

import logging
import time

from fastapi import APIRouter, Depends, HTTPException, status

from ...api.dependencies import get_request_id
from ...config import get_settings
from ...model_gateway import ModelGatewayError, complete
from ...schemas import ChatRequest, ChatResponse, ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        504: {"model": ErrorResponse},
    },
)
async def chat(
    payload: ChatRequest,
    request_id: str = Depends(get_request_id),
) -> ChatResponse:
    settings = get_settings()

    # Defensive size check (Pydantic already enforces per-message, but the
    # total request can still be large).
    total = sum(len(m.content) for m in payload.messages)
    if total > settings.max_request_chars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "request_too_large",
                    "message": f"Total request size {total} exceeds {settings.max_request_chars}",
                    "request_id": request_id,
                }
            },
        )

    start = time.perf_counter()
    try:
        response = await complete(
            payload.messages,
            settings=settings,
            model_override=payload.model,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
            request_id=request_id,
        )
    except ModelGatewayError as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.warning(
            "chat_model_error request_id=%s code=%s latency_ms=%.1f",
            request_id,
            exc.code,
            elapsed_ms,
        )
        http_status = {
            "model_api_key_missing": status.HTTP_503_SERVICE_UNAVAILABLE,
            "model_timeout": status.HTTP_504_GATEWAY_TIMEOUT,
            "model_network_error": status.HTTP_502_BAD_GATEWAY,
            "model_upstream_error": status.HTTP_502_BAD_GATEWAY,
            "model_bad_response": status.HTTP_502_BAD_GATEWAY,
        }.get(exc.code, status.HTTP_502_BAD_GATEWAY)
        raise HTTPException(
            status_code=http_status,
            detail={
                "error": ErrorDetail(
                    code=exc.code, message=exc.message, request_id=request_id
                ).model_dump()
            },
        ) from exc

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "chat_ok request_id=%s model=%s latency_ms=%.1f tokens=%d",
        request_id,
        response.model,
        elapsed_ms,
        response.usage.total_tokens,
    )
    return response
