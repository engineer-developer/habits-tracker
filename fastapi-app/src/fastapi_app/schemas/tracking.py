"""Модуль схем отслеживаний выполнения привычки."""

from datetime import datetime

from pydantic import ConfigDict, Field

from .base import BaseDtoModel


class TrackingFields:
    """Поля схемы отслеживания выполнения привычки."""

    id: int = Field(description="Идентификатор отслеживания", examples=[1])
    execution_time: datetime = Field(
        description="Время выполнения", examples=[datetime.now()]
    )
    created_at: datetime = Field(
        description="Время создания", examples=[datetime.now()]
    )
    habit_id: int = Field(description="Идентификатор привычки", examples=[11])


class BaseTracking(BaseDtoModel):
    """Базовая схема отслеживания привычки."""


# Commands
class TrackingCreateCommand(BaseTracking):
    """Схема отслеживания привычки."""

    habit_id: int = TrackingFields.habit_id
    execution_time: datetime = TrackingFields.execution_time


# Output
class TrackingRead(BaseTracking):
    """Схема вывода информации об отслеживании привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int = TrackingFields.id
    execution_time: datetime = TrackingFields.execution_time
