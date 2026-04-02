"""Модуль схем привычек."""

from datetime import datetime, time
from typing import Optional

from pydantic import ConfigDict, Field, PositiveInt, field_validator


from .base import BaseDtoModel
from .tracking import TrackingRead


class HabitFields:
    """Поля привычки."""

    id: PositiveInt = Field(description="Идентификатор привычки", examples=[1])
    title: str = Field(
        description="Название привычки", max_length=250, examples=["Тренировка"]
    )
    description: str = Field(
        description="Описание привычки", examples=["Пробежать 1 км"]
    )
    remind_time: time = Field(
        description="Время напоминания", examples=[time(hour=10, minute=00)]
    )
    remind_quantity: PositiveInt = Field(
        description="Количество напоминаний", examples=[21]
    )
    completed: bool = Field(description="Статус выполнения привычки", examples=[False])
    created_at: datetime = Field(
        description="Время создания", examples=[datetime.now()]
    )
    user_id: PositiveInt = Field(description="Идентификатор пользователя", examples=[2])


class BaseHabit(BaseDtoModel):
    """Базовая схема привычки."""


class HabitTitleInput(BaseHabit):
    title: str = Field(max_length=250, pattern=r"^[А-ЯЁа-яёA-Za-z0-9 \-:]+$")


class HabitDescriptionInput(BaseHabit):
    description: str = Field(pattern=r"^[А-ЯЁа-яёA-Za-z0-9 \-:]+$")


class HabitRemindTimeInput(BaseHabit):
    remind_time: time = HabitFields.remind_time


class HabitRemindQuantityInput(BaseHabit):
    remind_quantity: PositiveInt = HabitFields.remind_quantity


# Commands
class HabitCreateCommand(BaseHabit):
    """Схема для создания привычки."""

    title: str = HabitFields.title
    description: Optional[str] = HabitFields.description
    remind_time: time = HabitFields.remind_time
    remind_quantity: PositiveInt = HabitFields.remind_quantity
    user_id: PositiveInt = HabitFields.user_id


class HabitUpdateCommand(BaseHabit):
    """Схема для изменения данных привычки."""

    title: Optional[str] = None
    description: Optional[str] = None
    remind_time: Optional[time] = None
    remind_quantity: Optional[PositiveInt] = None
    completed: Optional[bool] = None


class HabitDeleteCommand(BaseHabit):
    """Схема для удаления привычки."""

    id: PositiveInt = HabitFields.id


class HabitJobCreateCommand(BaseHabit):
    """Схема данных для создания задачи планировщику."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    habit_id: PositiveInt = HabitFields.id
    title: str = HabitFields.title
    description: Optional[str] = HabitFields.description
    remind_time: time = HabitFields.remind_time
    remind_quantity: PositiveInt = HabitFields.remind_quantity
    user_id: PositiveInt = HabitFields.user_id


# Queries
class HabitByIdQuery(BaseHabit):
    """Схема для получения привычки по id"""

    id: PositiveInt = HabitFields.id


class HabitByUserIdQuery(BaseHabit):
    """Схема для получения привычки по user_id"""

    user_id: PositiveInt = HabitFields.user_id


# Output
class HabitRead(BaseHabit):
    """Схема для вывода данных привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt = HabitFields.id
    title: str = HabitFields.title
    description: Optional[str] = HabitFields.description
    remind_time: time = HabitFields.remind_time
    remind_quantity: PositiveInt = HabitFields.remind_quantity
    completed: bool = HabitFields.completed
    created_at: datetime = HabitFields.created_at

    tracking: list[TrackingRead]
