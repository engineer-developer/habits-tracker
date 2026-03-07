"""Модуль схем валидации и сериализации пользователя."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field, SecretStr

from .base import BaseDtoModel
from .habits import HabitRead


class UserFields:
    """Поля схемы пользователя."""

    id: int = Field(description="Идентификатор пользователя", examples=[1])
    telegram_id: int = Field(
        description="Telegram ID пользователя", examples=[123456789]
    )
    first_name: str = Field(description="Имя пользователя", examples=["first_name"])
    last_name: str = Field(description="Фамилия пользователя", examples=["last_name"])
    username: str = Field(description="Username пользователя", examples=["username"])
    password: SecretStr = Field(
        description="Пароль пользователя", examples=["password"]
    )
    is_active: bool = Field(
        description="Состояние активности пользователя", examples=[True]
    )
    created_at: datetime = Field(description="Время создания")


class BaseUser(BaseDtoModel):
    """Базовая схема пользователя."""


# Commands
class UserCredentials(BaseUser):
    """Схема данных аутентификации."""

    telegram_id: int = UserFields.telegram_id
    password: str = UserFields.password


class UserCreateCommand(BaseUser):
    """Схема создания пользователя."""

    telegram_id: int = UserFields.telegram_id
    first_name: str = UserFields.first_name
    last_name: Optional[str] = UserFields.last_name
    username: Optional[str] = UserFields.username
    password: str = UserFields.password


# Queries
class UserByIdQuery(BaseUser):
    """Схема запроса пользователя по id"""

    id: int = UserFields.id


class UserByTelegramIdQuery(BaseUser):
    """Схема запроса пользователя по telegram_id"""

    telegram_id: int = UserFields.telegram_id


# Output
class UserRead(BaseUser):
    """Получаем ответ с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int = UserFields.id
    telegram_id: int = UserFields.telegram_id
    first_name: str = UserFields.first_name
    last_name: Optional[str] = UserFields.last_name
    username: Optional[str] = UserFields.username
    is_active: bool = UserFields.is_active
    created_at: datetime = UserFields.created_at

    habits: list[Optional[HabitRead]]


class UserReadWithPassword(UserRead):
    """Получаем данные пользователя."""

    password: SecretStr = UserFields.password
