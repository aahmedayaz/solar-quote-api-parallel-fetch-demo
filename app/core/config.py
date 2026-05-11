from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    app_name: str = "Solar Quote API - Parallel Fetch Demo"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
    solar_api_base_url: str = os.getenv(
        "SOLAR_API_BASE_URL",
        "https://api.forecast.solar",
    ).rstrip("/")
    internal_api_host: str = os.getenv("INTERNAL_API_HOST", "127.0.0.1")
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    cors_allow_origins_raw: str = os.getenv("CORS_ALLOW_ORIGINS", "*")

    @property
    def finance_api_url(self) -> str:
        return os.getenv(
            "FINANCE_API_URL",
            f"http://{self.internal_api_host}:{self.api_port}/mock-finance",
        )

    @property
    def enable_cors(self) -> bool:
        default_enabled = self.environment.lower() == "production"
        return _get_bool_env("ENABLE_CORS", default_enabled)

    @property
    def cors_allow_origins(self) -> list[str]:
        if self.cors_allow_origins_raw.strip() == "*":
            return ["*"]
        return [
            origin.strip()
            for origin in self.cors_allow_origins_raw.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
