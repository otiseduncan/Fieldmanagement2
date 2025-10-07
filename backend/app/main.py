from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import routes_auth, routes_clients, routes_jobs, routes_reports, routes_users
from app.core.config import settings
from app.core.logging_config import configure_logging

configure_logging()

app = FastAPI(
    title=settings.project_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    routes_auth.router,
    prefix=f"{settings.api_v1_prefix}/auth",
    tags=["auth"],
)
app.include_router(
    routes_users.router,
    prefix=f"{settings.api_v1_prefix}/users",
    tags=["users"],
)
app.include_router(
    routes_jobs.router,
    prefix=f"{settings.api_v1_prefix}/jobs",
    tags=["jobs"],
)
app.include_router(
    routes_clients.router,
    prefix=f"{settings.api_v1_prefix}/clients",
    tags=["clients"],
)
app.include_router(
    routes_reports.router,
    prefix=f"{settings.api_v1_prefix}/reports",
    tags=["reports"],
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Simple health check used by load balancers and monitoring."""
    return {"status": "ok"}
