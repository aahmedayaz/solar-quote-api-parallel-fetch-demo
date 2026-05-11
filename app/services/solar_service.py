from __future__ import annotations

from datetime import date

import httpx

from app.core.config import settings
from app.models.request_models import SolarQuoteRequest
from app.models.response_models import SolarData


class SolarServiceError(Exception):
    """Raised when the Forecast.Solar request cannot produce usable data."""


def _pick_production_value(watt_hours_day: dict[str, float | int]) -> int:
    today_key = date.today().isoformat()

    if today_key in watt_hours_day:
        return int(round(watt_hours_day[today_key]))

    first_available_value = next(iter(watt_hours_day.values()), None)
    if first_available_value is None:
        raise SolarServiceError("Solar API returned an empty production payload.")

    return int(round(first_available_value))


async def fetch_solar_estimate(request: SolarQuoteRequest) -> SolarData:
    """
    Fetch solar production data from Forecast.Solar for a given system setup.

    Raises:
        SolarServiceError: When the external API request fails or the response
            shape is missing the expected production fields.
    """

    endpoint = (
        f"{settings.solar_api_base_url}/estimate/"
        f"{request.lat}/{request.lon}/{request.tilt}/{request.azimuth}/{request.kwp}"
    )

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise SolarServiceError("Connection timeout.") from exc
    except httpx.HTTPStatusError as exc:
        raise SolarServiceError(
            f"Upstream service returned HTTP {exc.response.status_code}."
        ) from exc
    except httpx.HTTPError as exc:
        raise SolarServiceError(str(exc)) from exc

    payload = response.json()
    watt_hours_day = payload.get("result", {}).get("watt_hours_day")

    if not isinstance(watt_hours_day, dict) or not watt_hours_day:
        raise SolarServiceError("Solar API returned no daily production data.")

    today_production_wh = _pick_production_value(watt_hours_day)

    return SolarData(
        today_production_wh=today_production_wh,
        today_production_kwh=round(today_production_wh / 1000, 2),
        api_source="forecast.solar",
    )
