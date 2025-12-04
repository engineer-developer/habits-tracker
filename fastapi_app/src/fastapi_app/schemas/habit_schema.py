"""Модуль схем привычек."""

from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.tracking_schema import TrackingOutDto


class HabitBaseDto(BaseModel):
    """Базовая схема привычки."""

    title: str = Field(max_length=250)
    description: Optional[str]


class HabitAddDto(HabitBaseDto):
    """Схема для создания привычки."""

    remind_time: time
    remind_quantity: int = Field(gt=0)


class HabitOutDto(HabitAddDto):
    """Схема для вывода данных привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool
    tracking: list[TrackingOutDto]


class HabitListDto(BaseModel):
    """Схема списка привычек."""

    habits: list[HabitOutDto]


class HabitPatchDto(HabitAddDto):
    """Схема для изменения данных привычки."""

    title: Optional[str] = Field(default=None, max_length=250)
    description: Optional[str] = None
    remind_time: Optional[time] = None
    remind_quantity: Optional[int] = Field(default=None, gt=0)


class HabitExecutionData(BaseModel):
    """Схема данных о выполнении привычки."""

    habit_id: int
    execution_time: datetime


class HabitDeleteInfoDto(BaseModel):
    """Схема данных об удалении привычки."""

    habit_id: int
    status: str = "successful deleted"
