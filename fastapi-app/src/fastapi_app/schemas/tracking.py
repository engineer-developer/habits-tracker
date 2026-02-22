"""Модуль схем отслеживаний выполнения привычки."""

from datetime import datetime

from pydantic import ConfigDict

from .base import BaseDtoModel


class TrackingBaseDto(BaseDtoModel):
    """Схема отслеживания привычки."""

    habit_id: int
    alert_time: datetime


class TrackingOutDto(BaseDtoModel):
    """Схема вывода информации об отслеживании привычки."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    alert_time: datetime
