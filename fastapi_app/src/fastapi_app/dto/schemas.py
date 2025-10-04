"""Модуль схем пользователя."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """Базовая схема пользователя."""

    name: str
    telegram_id: int


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
