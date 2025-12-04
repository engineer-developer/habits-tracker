"""Модуль схем валидации и сериализации пользователя."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBaseDto(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int = Field(gt=0, description="Telegram ID пользователя")


class UserExtendDto(UserBaseDto):
    """Расширенная схема пользователя."""

    first_name: str = Field(description="Имя пользователя")
    last_name: Optional[str] = Field(default=None, description="Фамилия пользователя")
    username: Optional[str] = Field(default=None, description="Username пользователя")


class UserCredentialsDto(UserBaseDto):
    """Схема аутентификации пользователя."""

    password: str = Field(description="Пароль")


class UserAddDto(UserExtendDto):
    """Схема добавления пользователя."""

    password: str = Field(description="Пароль")


class UserOutDto(UserExtendDto):
    """Схема вывода информации о пользователе."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="ID")
    is_active: bool = Field(description="Пользователь активен")
    created_at: datetime = Field(description="Время создания")


class UsersListDto(BaseModel):
    """Схема для списка пользователей."""

    users: list[UserOutDto] = Field(description="Список пользователей")
