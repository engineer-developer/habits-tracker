"""Модуль конфигурации приложения."""

__all__ = ("get_settings",)


import enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class _Settings(BaseSettings):
    """Базовые настройки."""

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    if ENV_FILE.exists():
        model_config["env_file"] = BASE_DIR / ".env"


class ApiSettings(BaseModel):
    """Настройки внешнего api."""

    host: Optional[str] = Field(default="127.0.0.1")
    port: Optional[int] = Field(default=8000)

    url: Optional[str] = Field(default=None, init=False)

    @model_validator(mode="after")
    def calculate_url(self):
        self.url = f"http://{self.host}:{self.port}/api"
        return self

class BotSettings(BaseModel):
    """Настройки ТГ бота."""

    token: str


class RedisSettings(BaseModel):
    """Настройки Redis."""

    host: str
    port: int
    db: int


class LoggingLevel(str, enum.Enum):
    """Уровни логирования."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"


class LoggingSettings(BaseModel):
    """Настройки логирования."""

    level: LoggingLevel


class Settings(_Settings):
    """Настройки приложения."""

    api: ApiSettings = Field(validation_alias="APP")
    bot: BotSettings
    redis: RedisSettings
    logging: LoggingSettings


def get_settings() -> Settings:
    """Функция получения экземпляра класса Settings."""
    settings = Settings()
    # print(settings)
    return settings
