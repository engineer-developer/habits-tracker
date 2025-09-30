"""Модуль получения настроек из переменных окружения."""

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки сервиса."""

    db_url: PostgresDsn = Field(
        validation_alias="DB_URL",
        default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5004/db",
    )
    db_url: PostgresDsn = Field(validation_alias="DB_URL")
