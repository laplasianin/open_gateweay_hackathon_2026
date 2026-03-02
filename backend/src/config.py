"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "StageFlow"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/stageflow"
    database_echo: bool = False

    # Nokia Network as Code
    nac_client_id: Optional[str] = None
    nac_client_secret: Optional[str] = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


settings = Settings()

