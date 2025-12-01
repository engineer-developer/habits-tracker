"""Модуль схем привычек."""

from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.reminder_schema import ReminderOutDto
from schemas.tracking_schema import TrackingOutDto


class HabitDto(BaseModel):
    """Базовая схема привычки."""

    name: str
    description: Optional[str]


class HabitAddDto(BaseModel):
    """Схема для создания привычки."""

    name: str = Field(max_length=100)
    description: str
    remind_time: time
    remind_quantity: int = Field(gt=0)
    job_id: str


class HabitPatchDto(BaseModel):
    """Схема для изменения данных привычки."""

    name: str = Field(max_length=100)
    description: Optional[str] = None
    remind_time: Optional[time] = None
    remind_quantity: Optional[int] = Field(default=None, gt=0)


class HabitCompletedDto(BaseModel):
    """Схема данных о выполнении привычки."""

    name: str = Field(max_length=100)
    alert_time: datetime


class HabitOutDto(BaseModel):
    """Схема для вывода данных привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    completed: bool
    reminder: ReminderOutDto
    tracking: list[TrackingOutDto]


class HabitListDto(BaseModel):
    """Схема списка привычек."""

    habits: list[HabitOutDto]


class HabitDeleteInfoDto(BaseModel):
    """Схема данных об удалении привычки."""

    habit_id: int
    status: str = "successful deleted"
