"""Модуль схем для валидации и сериализации данных о привычке."""

import datetime

from pydantic import BaseModel, Field


class HabitBaseDto(BaseModel):
    """Базовая схема привычки."""

    title: str = Field(max_length=250)
    description: str


class HabitAddDto(HabitBaseDto):
    """Схема для создания привычки."""

    remind_time: datetime.time
    remind_quantity: int = Field(gt=0)


class HabitDataDto(HabitAddDto):
    """Схема данных о привычке."""

    user_id: int
    chat_id: int

