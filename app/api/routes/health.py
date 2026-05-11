from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.models.response_models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API health",
    response_description="Basic health information for the running API service.",
)
async def health_check() -> HealthResponse:
    """
    Return a lightweight health status payload.

    This endpoint is useful for local smoke testing, container health probes,
    and production uptime checks.
    """

    return HealthResponse(
        status="ok",
        environment=settings.environment,
        version=settings.app_version,
    )
