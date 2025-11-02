"""Модуль схем напоминаний."""

from datetime import time

from pydantic import BaseModel, ConfigDict


class ReminderOutDto(BaseModel):
    """Схема вывода данных о напоминании."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    remind_time: time
    remind_quantity: int
    job_id: str
