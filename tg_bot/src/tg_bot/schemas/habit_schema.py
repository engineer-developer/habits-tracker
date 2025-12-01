"""Модуль схем для валидации и сериализации данных о привычке."""

import datetime

from pydantic import BaseModel, Field


class HabitBaseDto(BaseModel):
    """Базовая схема привычки."""

    name: str = Field(max_length=100)
    description: str


class HabitAddDto(HabitBaseDto):
    """Схема для создания привычки."""

    remind_time: datetime.time
    remind_quantity: int = Field(gt=0)
    job_id: str


class HabitDataDto(HabitAddDto):
    """Схема данных о привычке."""

    user_id: int
    chat_id: int


