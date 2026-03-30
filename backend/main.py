"""Application entry point."""
import uvicorn
from src.app import app
from src.config import settings


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info",
    )
