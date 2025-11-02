"""Модуль конфигурации приложения."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent


class Settings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        validate_default=False,
    )

    bot_token: str = Field(validation_alias="BOT_TOKEN")
    api_url: str = Field(validation_alias="FASTAPI_API_URL")
    redis_host: str = Field(validation_alias="REDIS_HOST")
    redis_port: int = Field(validation_alias="REDIS_PORT")
    redis_db: int = Field(validation_alias="REDIS_DB")

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings()
