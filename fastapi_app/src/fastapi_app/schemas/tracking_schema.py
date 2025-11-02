"""Модуль схем отслеживаний выполнения привычки."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrackingCreateDto(BaseModel):
    """Схема создания отслеживания привычки."""

    alert_time: datetime
    habit_id: int


class TrackingOutDto(BaseModel):
    """Схема вывода информации об отслеживании привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    alert_time: datetime
