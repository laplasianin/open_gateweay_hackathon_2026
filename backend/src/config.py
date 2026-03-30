"""Application configuration."""
from pydantic_settings import BaseSettings
from pydantic import Field
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
    nac_token: Optional[str] = Field(default=None, alias="nac_client_token")

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False
        populate_by_name = True


settings = Settings()

