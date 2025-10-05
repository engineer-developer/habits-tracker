"""Модуль схемы валидации и сериализации пользователя."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    """Базовая схема пользователя."""

    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    telegram_id: int = Field(gt=0)


class UserInSchema(UserSchema):
    """Схема создания пользователя."""

    password: str


class UserOutSchema(UserSchema):
    """Схема вывода информации о пользователе."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UsersListSchema(BaseModel):
    """Схема для списка пользователей."""

    users: list[UserOutSchema]
