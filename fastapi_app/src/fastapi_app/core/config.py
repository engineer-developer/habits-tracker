"""Модуль получения настроек из переменных окружения."""

from pathlib import Path
from typing import Annotated

from fastapi import Depends
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent.parent


class Settings(BaseSettings):
    """Настройки сервиса."""

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    db_url: PostgresDsn = Field(validation_alias="DB_URL")
    secret_key: str = Field(validation_alias="FASTAPI_SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


def get_settings() -> Settings:
    """Функция получения экземпляра класса Settings.

    :return: Экземпляр настроек.
    """
    settings = Settings()
    return settings


# Аннотация для получения экземпляра настроек
CommonSettings = Annotated[Settings, Depends(get_settings)]
