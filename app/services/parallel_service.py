from __future__ import annotations

import asyncio

from app.models.request_models import SolarQuoteRequest
from app.models.response_models import (
    FinanceOffer,
    LocationInfo,
    SolarData,
    SolarQuoteResponse,
    SystemInfo,
)
from app.services.finance_service import FinanceServiceError, fetch_finance_offer_via_api
from app.services.solar_service import SolarServiceError, fetch_solar_estimate


def _build_location_payload(request: SolarQuoteRequest) -> LocationInfo:
    return LocationInfo(lat=request.lat, lon=request.lon)


def _build_system_payload(request: SolarQuoteRequest) -> SystemInfo:
    return SystemInfo(
        kwp=request.kwp,
        tilt_degrees=request.tilt,
        azimuth_degrees=request.azimuth,
    )


async def fetch_parallel_quote(request: SolarQuoteRequest) -> SolarQuoteResponse:
    """
    Fetch solar and finance data at the same time using ``asyncio.gather``.

    Each request is allowed to fail independently so the endpoint can return a
    partial response instead of failing the entire quote.
    """

    solar_result, finance_result = await asyncio.gather(
        fetch_solar_estimate(request),
        fetch_finance_offer_via_api(request.kwp),
        return_exceptions=True,
    )

    status = "success"

    if isinstance(solar_result, Exception):
        status = "partial_error"
        solar_payload = SolarData(
            today_production_wh=None,
            today_production_kwh=None,
            api_source="forecast.solar",
            error=f"Solar API failed: {solar_result}",
        )
    else:
        solar_payload = solar_result

    if isinstance(finance_result, Exception):
        status = "partial_error"
        finance_payload = FinanceOffer(
            error=f"Finance API failed: {finance_result}",
        )
    else:
        finance_payload = finance_result

    if isinstance(solar_result, SolarServiceError) and isinstance(
        finance_result, FinanceServiceError
    ):
        status = "partial_error"

    return SolarQuoteResponse(
        status=status,
        location=_build_location_payload(request),
        system=_build_system_payload(request),
        solar=solar_payload,
        finance=finance_payload,
    )
