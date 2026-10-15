"""FastAPI application entry point."""
from __future__ import annotations

import logging

from fastapi import FastAPI

from .api.router import api_router
from .config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    app = FastAPI(title=settings.api_title, version=settings.api_version)
    app.include_router(api_router)
    return app


app = create_app()
