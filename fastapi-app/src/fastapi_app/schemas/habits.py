"""Модуль схем привычек."""

from datetime import datetime, time
from typing import Optional

from pydantic import ConfigDict, Field, PositiveInt

from .base import BaseDtoModel
from .tracking import TrackingOutDto


class HabitFields:
    """Поля привычки."""

    id: int = Field(description="Идентификатор привычки", examples=[1])
    title: str = Field(description="Название привычки", max_length=250)
    description: str = Field(description="Описание привычки")
    remind_time: time = Field(description="Время напоминания")
    remind_quantity: PositiveInt = Field(description="Количество напоминаний")
    completed: bool = Field(description="Статус выполнения привычки")
    created_at: datetime = Field(description="Время создания")
    execution_time: datetime = Field(description="Дата и время выполнения")


class BaseHabit(BaseDtoModel):
    """Базовая схема привычки."""


class HabitCreateCommand(BaseHabit):
    """Схема для создания привычки."""

    title: str = HabitFields.title
    description: Optional[str] = HabitFields.description
    remind_time: time = HabitFields.remind_time
    remind_quantity: int = HabitFields.remind_quantity


class HabitRead(BaseHabit):
    """Схема для вывода данных привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int = HabitFields.id
    title: str = HabitFields.title
    description: Optional[str] = HabitFields.description
    remind_time: time = HabitFields.remind_time
    remind_quantity: int = HabitFields.remind_quantity
    completed: bool = HabitFields.completed
    created_at: datetime = HabitFields.created_at

    tracking: list[Optional[TrackingOutDto]]


class HabitPatchCommand(BaseHabit):
    """Схема для изменения данных привычки."""

    title: Optional[str] = Field(default=None, max_length=250)
    description: Optional[str] = None
    remind_time: Optional[time] = None
    remind_quantity: Optional[int] = Field(default=None, gt=0)


class HabitExecutionData(BaseDtoModel):
    """Схема данных о выполнении привычки."""

    habit_id: int
    execution_time: datetime
