"""Модуль получения настроек из переменных окружения."""

from typing import Annotated

from fastapi import Depends
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки сервиса."""

    db_url: PostgresDsn = Field(validation_alias="DB_URL")
    secret_key: str = Field(alias="FASTAPI_SECRET_KEY")
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
