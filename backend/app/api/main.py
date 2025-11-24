#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from uvicorn import run

from ..core.config import settings
from ..core.logging import configure_logging
from ..utils.health import health_status
from .routes import games, leaderboard, words

configure_logging()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
)

app.include_router(words.router, prefix=settings.api_prefix)
app.include_router(games.router, prefix=settings.api_prefix)
app.include_router(leaderboard.router, prefix=settings.api_prefix)


@app.get("/")
def root() -> ORJSONResponse:
    """Root endpoint."""
    logger.info("Root endpoint called")
    return ORJSONResponse({"message": "Backend is running", "app": settings.app_name})


@app.get("/health")
def health() -> ORJSONResponse:
    """Health check endpoint."""
    logger.debug("Health endpoint called")
    return ORJSONResponse(health_status())


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=2024)
