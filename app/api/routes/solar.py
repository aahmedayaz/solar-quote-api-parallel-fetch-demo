from __future__ import annotations

from fastapi import APIRouter, Query

from app.models.request_models import SolarQuoteRequest
from app.models.response_models import SolarQuoteResponse
from app.services.parallel_service import fetch_parallel_quote

router = APIRouter(tags=["Solar Quote"])


@router.get(
    "/solar-quote",
    response_model=SolarQuoteResponse,
    summary="Get a combined solar production and finance quote",
    response_description="Combined payload containing solar production and finance data.",
)
async def get_solar_quote(
    lat: float = Query(
        ...,
        ge=-90,
        le=90,
        description="Latitude coordinate for the installation site (for example, 51.5 for London).",
        examples=[51.5],
    ),
    lon: float = Query(
        ...,
        ge=-180,
        le=180,
        description="Longitude coordinate for the installation site (for example, -0.1 for London).",
        examples=[-0.1],
    ),
    tilt: int = Query(
        35,
        ge=0,
        le=90,
        description="Solar panel tilt angle in degrees from horizontal.",
        examples=[35],
    ),
    azimuth: int = Query(
        0,
        ge=-180,
        le=180,
        description="Panel azimuth where 0=South, -90=East, and 90=West.",
        examples=[0],
    ),
    kwp: float = Query(
        4,
        ge=0.5,
        le=100,
        description="System size in kilowatt-peak.",
        examples=[4],
    ),
) -> SolarQuoteResponse:
    """
    Get a combined solar production estimate and finance offer.

    This endpoint runs two API calls in parallel using ``asyncio.gather``:
    Forecast.Solar for real production data and the internal ``/mock-finance``
    endpoint for a demo finance product. If one call fails, the response still
    includes whatever data was retrieved successfully.
    """

    request = SolarQuoteRequest(
        lat=lat,
        lon=lon,
        tilt=tilt,
        azimuth=azimuth,
        kwp=kwp,
    )
    return await fetch_parallel_quote(request)
