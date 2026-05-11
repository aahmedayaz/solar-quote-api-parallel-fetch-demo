from __future__ import annotations

from fastapi import APIRouter, Query

from app.models.request_models import MockFinanceRequest
from app.models.response_models import FinanceOffer
from app.services.finance_service import build_mock_finance_offer

router = APIRouter(tags=["Finance"])


@router.get(
    "/mock-finance",
    response_model=FinanceOffer,
    summary="Get a mock finance offer",
    response_description="Finance product details for the requested solar system size.",
)
async def get_mock_finance(
    kwp: float = Query(
        4,
        ge=0.5,
        le=100,
        description="System size in kilowatt-peak used to estimate monthly payments.",
        examples=[4, 6.5],
    ),
) -> FinanceOffer:
    """
    Return mock finance product data for the requested system size.

    This endpoint simulates a realistic provider call by waiting for 300
    milliseconds before returning a deterministic finance offer.
    """

    request = MockFinanceRequest(kwp=kwp)
    return await build_mock_finance_offer(request.kwp)
