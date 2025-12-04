"""Модуль схем отслеживаний выполнения привычки."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrackingBaseDto(BaseModel):
    """Схема отслеживания привычки."""

    habit_id: int
    alert_time: datetime


class TrackingOutDto(BaseModel):
    """Схема вывода информации об отслеживании привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    alert_time: datetime
