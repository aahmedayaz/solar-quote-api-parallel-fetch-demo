from __future__ import annotations

import asyncio

import httpx

from app.core.config import settings
from app.models.response_models import FinanceOffer


class FinanceServiceError(Exception):
    """Raised when the mock finance API cannot be reached successfully."""


async def build_mock_finance_offer(kwp: float) -> FinanceOffer:
    """
    Create a predictable mock finance response with an artificial delay.

    The delay helps demonstrate that the main endpoint runs the solar and
    finance calls concurrently rather than one after the other.
    """

    await asyncio.sleep(0.3)

    monthly_payment_per_kw = 15.0
    estimated_monthly_payment = round(kwp * monthly_payment_per_kw, 2)

    return FinanceOffer(
        provider="Demo Finance",
        apr_percent=9.9,
        monthly_payment_per_kw=monthly_payment_per_kw,
        estimated_monthly_payment=estimated_monthly_payment,
        term_months=120,
    )


async def fetch_finance_offer_via_api(kwp: float) -> FinanceOffer:
    """
    Call the internal mock finance endpoint through HTTP.

    This keeps the combined quote flow aligned with the requirement that the
    main endpoint fetches data from two APIs in parallel.
    """

    try:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(settings.finance_api_url, params={"kwp": kwp})
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise FinanceServiceError("Finance API request timed out.") from exc
    except httpx.HTTPStatusError as exc:
        raise FinanceServiceError(
            f"Finance API returned HTTP {exc.response.status_code}."
        ) from exc
    except httpx.HTTPError as exc:
        raise FinanceServiceError(str(exc)) from exc

    return FinanceOffer.parse_obj(response.json())
