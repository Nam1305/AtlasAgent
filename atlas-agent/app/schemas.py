"""Pydantic schemas for the Atlas Agent API.

These are the public contracts. /chat output is validated against ChatResponse
so a malformed model response becomes a structured error, never a 500.
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ---- Requests ---------------------------------------------------------------


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1, max_length=20_000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1, max_length=64)
    model: str | None = Field(default=None, description="Override the default model")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=8192)


# ---- Responses --------------------------------------------------------------


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatResponse(BaseModel):
    request_id: str
    content: str
    model: str
    finish_reason: str = "stop"
    usage: UsageInfo = Field(default_factory=UsageInfo)


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"] = "ok"
    version: str
    model: str
    api_key_configured: bool


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


# ---- Documents (Week 2 surface; the routes land alongside the ingest
# pipeline). The frontend already speaks this shape. ---------------------


DocumentType = Literal["text", "pdf_text", "pdf_scan", "pdf_mixed"]
IngestStatus = Literal["pending", "processing", "ready", "failed"]


class DocumentItem(BaseModel):
    id: str
    filename: str
    type: DocumentType
    size_bytes: int
    uploaded_at: datetime
    status: IngestStatus
    chunk_count: int | None = None
    error: str | None = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentItem]
    total: int


class DocumentDeleteResponse(BaseModel):
    ok: Literal[True] = True
    id: str
