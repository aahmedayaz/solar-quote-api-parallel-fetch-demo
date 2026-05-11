from __future__ import annotations

from pydantic import BaseModel, Field


class SolarQuoteRequest(BaseModel):
    """Validated query parameters for the combined solar quote endpoint."""

    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude coordinate (e.g., 51.5 for London).",
    )
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude coordinate (e.g., -0.1 for London).",
    )
    tilt: int = Field(
        35,
        ge=0,
        le=90,
        description="Solar panel tilt angle in degrees from horizontal.",
    )
    azimuth: int = Field(
        0,
        ge=-180,
        le=180,
        description="Panel azimuth where 0=South, -90=East, and 90=West.",
    )
    kwp: float = Field(
        4,
        ge=0.5,
        le=100,
        description="System size in kilowatt-peak.",
    )

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "lat": 51.5,
                "lon": -0.1,
                "tilt": 35,
                "azimuth": 0,
                "kwp": 4,
            }
        }


class MockFinanceRequest(BaseModel):
    """Validated request parameters for the mock finance endpoint."""

    kwp: float = Field(
        4,
        ge=0.5,
        le=100,
        description="System size in kilowatt-peak used to estimate financing costs.",
    )

    class Config:
        extra = "forbid"
        schema_extra = {"example": {"kwp": 4}}
