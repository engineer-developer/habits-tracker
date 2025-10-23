"""Модуль схемы валидации и сериализации пользователя."""

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class UserBaseSchema(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int = Field(gt=0)


class UserExtendSchema(UserBaseSchema):
    """Расширенная схема пользователя."""

    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class UserCredentials(UserBaseSchema):
    """Схема аутентификации пользователя."""

    password: str


class UserInSchema(UserExtendSchema):
    """Схема добавления пользователя."""

    password: str


class UserOutSchema(UserExtendSchema):
    """Схема вывода информации о пользователе."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UsersListSchema(BaseModel):
    """Схема для списка пользователей."""

    users: list[UserOutSchema]

