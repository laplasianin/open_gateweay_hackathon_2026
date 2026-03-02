"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import network_as_code as nac

from src.config import settings
from src.logging_config import configure_logging, get_logger
from src.models import HealthCheckResponse, ErrorResponse
from src.database.init import init_database
from src.routes import roles_router, users_router, auth_router

# Configure logging
configure_logging()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    @app.on_event("startup")
    def on_startup():
        """
        FastAPI startup event handler.
        Initializes database connection and creates tables.
        """
        logger.info("application_startup")

        # Initialize database and create tables
        init_database()
        logger.info("database_ready")

    @app.get("/healthcheck", response_model=HealthCheckResponse)
    async def healthcheck() -> HealthCheckResponse:
        """
        Health check endpoint.
        
        Returns application status, version, and database connectivity.
        """
        logger.info("healthcheck_request")

        return HealthCheckResponse(
            status="healthy",
            version=settings.app_version,
            timestamp=datetime.utcnow(),
            database="connected",
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        logger.error(
            "unhandled_exception",
            error=str(exc),
            path=request.url.path,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc) if settings.debug else None,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    # Include API routers
    app.include_router(auth_router)
    app.include_router(roles_router)
    app.include_router(users_router)

    return app


# Create app instance for uvicorn
app = create_app()

