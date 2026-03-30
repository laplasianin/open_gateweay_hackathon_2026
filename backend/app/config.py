from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://stageflow:stageflow@localhost:5432/stageflow"
    nokia_mode: str = "mock"  # "mock" or "real"
    nokia_api_key: str = ""
    nokia_api_secret: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
