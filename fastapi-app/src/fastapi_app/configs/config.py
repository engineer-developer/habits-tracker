"""Модуль получения настроек из переменных окружения."""

from pathlib import Path
from typing import Optional, Self

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

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


class DatabaseSettings(BaseModel):
    """Настройки базы данных."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: str
    passw: SecretStr
    host: str = Field(default="0.0.0.0")
    port: int
    name: str

    dsn: Optional[URL] = Field(default=None, init=False)

    @model_validator(mode="after")
    def calculate_dsn(self) -> Self:
        """DSN базы данных."""
        self.dsn = URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.passw.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )
        return self


class AuthSettings(BaseModel):
    """Настройки аутентификации."""

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


class Settings(_Settings):
    """Настройки сервиса."""

    db: DatabaseSettings
    auth: AuthSettings


def get_settings() -> Settings:
    """Функция получения экземпляра класса Settings."""
    settings = Settings()
    return settings
