from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class LocationInfo(BaseModel):
    """Geographic coordinates for the quote request."""

    lat: float = Field(..., description="Latitude coordinate.")
    lon: float = Field(..., description="Longitude coordinate.")


class SystemInfo(BaseModel):
    """Solar system configuration used to calculate the quote."""

    kwp: float = Field(..., description="System size in kilowatt-peak.")
    tilt_degrees: int = Field(..., description="Solar panel tilt angle in degrees.")
    azimuth_degrees: int = Field(..., description="Solar panel azimuth angle in degrees.")


class SolarData(BaseModel):
    """Solar production details returned from Forecast.Solar."""

    today_production_wh: int | None = Field(
        default=None,
        description="Estimated daily production in watt-hours.",
    )
    today_production_kwh: float | None = Field(
        default=None,
        description="Estimated daily production in kilowatt-hours.",
    )
    api_source: str | None = Field(
        default="forecast.solar",
        description="Source of the solar production estimate.",
    )
    error: str | None = Field(
        default=None,
        description="Error details when the solar API call fails.",
    )


class FinanceOffer(BaseModel):
    """Finance product details used in the combined quote."""

    provider: str | None = Field(
        default=None,
        description="Finance provider name.",
    )
    apr_percent: float | None = Field(
        default=None,
        description="Annual percentage rate offered by the finance provider.",
    )
    monthly_payment_per_kw: float | None = Field(
        default=None,
        description="Monthly payment amount per installed kilowatt-peak.",
    )
    estimated_monthly_payment: float | None = Field(
        default=None,
        description="Estimated monthly payment for the requested system size.",
    )
    term_months: int | None = Field(
        default=None,
        description="Length of the finance agreement in months.",
    )
    error: str | None = Field(
        default=None,
        description="Error details when the finance API call fails.",
    )


class SolarQuoteResponse(BaseModel):
    """Combined response returned by the main solar quote endpoint."""

    status: Literal["success", "partial_error"] = Field(
        ...,
        description="Overall result status for the combined request.",
    )
    location: LocationInfo | None = Field(
        default=None,
        description="Location used to request the quote.",
    )
    system: SystemInfo | None = Field(
        default=None,
        description="Solar system settings used for the estimate.",
    )
    solar: SolarData | None = Field(
        default=None,
        description="Solar production estimate or solar API error payload.",
    )
    finance: FinanceOffer | None = Field(
        default=None,
        description="Finance offer or finance API error payload.",
    )

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "location": {"lat": 51.5, "lon": -0.1},
                "system": {
                    "kwp": 4,
                    "tilt_degrees": 35,
                    "azimuth_degrees": 0,
                },
                "solar": {
                    "today_production_wh": 12500,
                    "today_production_kwh": 12.5,
                    "api_source": "forecast.solar",
                },
                "finance": {
                    "provider": "Demo Finance",
                    "apr_percent": 9.9,
                    "monthly_payment_per_kw": 15,
                    "estimated_monthly_payment": 60,
                    "term_months": 120,
                },
            }
        }


class HealthResponse(BaseModel):
    """Health-check payload for service monitoring."""

    status: str = Field(..., description="Health state of the API.")
    environment: str = Field(..., description="Current runtime environment.")
    version: str = Field(..., description="Application version.")
