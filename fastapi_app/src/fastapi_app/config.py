"""Модуль получения настроек из переменных окружения."""

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки сервиса."""

    db_url: PostgresDsn = Field(validation_alias="DB_URL")
