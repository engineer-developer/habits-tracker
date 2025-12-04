"""Модуль схемы валидации и сериализации пользователя."""

from typing import Optional

from pydantic import BaseModel, Field


class UserIdSchema(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int = Field(gt=0)


class UserExtendSchema(UserIdSchema):
    """Расширенная схема пользователя."""

    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class UserRegisterSchema(UserExtendSchema):
    """Схема регистрации пользователя."""

    password: str


class UserLoginSchema(BaseModel):
    """Схема аутентификации пользователя."""

    username: str
    password: str
