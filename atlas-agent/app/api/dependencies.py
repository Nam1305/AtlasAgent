"""Shared FastAPI dependencies."""
from __future__ import annotations

import uuid

from fastapi import Request


def get_request_id(request: Request) -> str:
    """Return the request id, generating one if the client did not send one."""
    return request.headers.get("X-Request-ID") or str(uuid.uuid4())
