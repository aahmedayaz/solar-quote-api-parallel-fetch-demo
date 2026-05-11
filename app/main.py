from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.finance import router as finance_router
from app.api.routes.health import router as health_router
from app.api.routes.solar import router as solar_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "FastAPI demo service that fetches real solar production data and "
        "mock finance data in parallel, then returns a combined quote."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(health_router)
app.include_router(finance_router)
app.include_router(solar_router)


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {"message": "Visit /docs for the interactive API documentation."}
