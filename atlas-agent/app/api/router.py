"""Aggregate router for the HTTP API."""
from fastapi import APIRouter

from .routes.chat import router as chat_router
from .routes.documents import router as documents_router
from .routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(documents_router, tags=["documents"])
