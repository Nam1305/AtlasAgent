"""Document management endpoints.

The full ingest pipeline (PDF parsing, OCR, chunking, vector store) lands
in Week 2. This Week 1 stub exposes the routes the frontend already talks
to and keeps an in-memory list so the UI can be exercised end-to-end.

Persistence: in-memory only. Re-deploying the server drops the list.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ...schemas import (
    DocumentDeleteResponse,
    DocumentItem,
    DocumentListResponse,
    ErrorDetail,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Module-level store: a single list shared by all requests.
_STORE: list[DocumentItem] = []


def _detect_type(filename: str) -> DocumentItem.model_fields["type"].annotation:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        # The real detector inspects the text layer; this is a placeholder.
        return "pdf_text"
    return "text"


@router.get(
    "/documents",
    response_model=DocumentListResponse,
    summary="List all ingested documents",
)
async def list_documents() -> DocumentListResponse:
    return DocumentListResponse(documents=list(_STORE), total=len(_STORE))


@router.post(
    "/documents",
    response_model=DocumentItem,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document for ingestion (Week 2: real pipeline)",
    responses={413: {"description": "File too large"}},
)
async def upload_document(file: UploadFile = File(...)) -> DocumentItem:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": ErrorDetail(code="missing_filename", message="filename is required").model_dump()},
        )
    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:  # 50 MB cap for the stub
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"error": ErrorDetail(code="file_too_large", message="Max upload size is 50 MB").model_dump()},
        )

    item = DocumentItem(
        id=str(uuid.uuid4()),
        filename=file.filename,
        type=_detect_type(file.filename),  # type: ignore[arg-type]
        size_bytes=len(contents),
        uploaded_at=datetime.now(timezone.utc),
        status="pending",
    )
    _STORE.append(item)
    logger.info(
        "document_uploaded id=%s filename=%s size=%d", item.id, item.filename, item.size_bytes
    )
    return item


@router.delete(
    "/documents/{doc_id}",
    response_model=DocumentDeleteResponse,
    responses={404: {"description": "Not found"}},
)
async def delete_document(doc_id: str) -> DocumentDeleteResponse:
    for i, d in enumerate(_STORE):
        if d.id == doc_id:
            _STORE.pop(i)
            return DocumentDeleteResponse(id=doc_id)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": ErrorDetail(code="not_found", message=f"document {doc_id} not found").model_dump()},
    )
