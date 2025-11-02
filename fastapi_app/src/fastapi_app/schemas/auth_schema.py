"""Модуль схем аутентификации."""

from pydantic import BaseModel, Field


class TokenDto(BaseModel):
    """Схема токена."""

    access_token: str = Field(description="Токен аутентификации")
    token_type: str = Field(description="Тип токена аутентификации")
