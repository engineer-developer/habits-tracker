"""Модуль схем пользователя."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    """Базовая схема пользователя."""

    pass


class UserInSchema(UserSchema):
    """Схема создания пользователя."""

    name: str
    password: str
    telegram_id: int


class UserOutSchema(UserInSchema):
    """Схема вывода информации о пользователе."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
