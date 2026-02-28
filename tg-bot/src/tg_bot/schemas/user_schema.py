"""Модуль схемы валидации и сериализации пользователя."""

from typing import Optional

from pydantic import BaseModel, Field



class UserLoginSchema(BaseModel):
    """Схема аутентификации пользователя."""

    telegram_id: int
    password: str



class UserRegisterSchema(BaseModel):
    """Схема регистрации пользователя."""

    password: str

# TODO: Удалить старые схемы

class UserIdSchema(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int = Field(gt=0)


class UserExtendSchema(UserIdSchema):
    """Расширенная схема пользователя."""

    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None






