"""FastAPI application factory."""

from collections.abc import Mapping

from fastapi import FastAPI, Response

from statforge_api.health import Check, HealthResponse, check_db, check_s3
from statforge_api.settings import Settings
from statforge_api.version import VersionResponse, current_version


def _default_checks() -> dict[str, Check]:
    settings = Settings()  # type: ignore[call-arg]  # values come from the environment
    return {
        "db": lambda: check_db(settings.database_url),
        "s3": lambda: check_s3(
            settings.s3_endpoint_url, settings.s3_access_key, settings.s3_secret_key
        ),
    }


def create_app(checks: Mapping[str, Check] | None = None) -> FastAPI:
    app = FastAPI(title="StatForge API", version=current_version().version)
    resolved: dict[str, Check] | None = dict(checks) if checks is not None else None

    @app.get("/health", response_model=HealthResponse)
    def health(response: Response) -> HealthResponse:
        nonlocal resolved
        if resolved is None:
            resolved = _default_checks()
        components = {name: check() for name, check in resolved.items()}
        healthy = all(result.status == "ok" for result in components.values())
        response.status_code = 200 if healthy else 503
        return HealthResponse(status="ok" if healthy else "unavailable", components=components)

    @app.get("/api/v1/version", response_model=VersionResponse)
    def api_version() -> VersionResponse:
        return current_version()

    return app


app = create_app()
