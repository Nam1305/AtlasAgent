"""Liveness and readiness endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from ...config import get_settings
from ...schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok" if settings.gemini_api_key else "degraded",
        version=settings.api_version,
        model=settings.gemini_model,
        api_key_configured=bool(settings.gemini_api_key),
    )
