from pydantic import BaseModel, Field
import datetime

class HabitAddDto(BaseModel):
    """Схема для создания привычки."""

    name: str = Field(max_length=100)
    description: str
    remind_time: datetime.time
    remind_quantity: int = Field(gt=0)
    job_id: str


class HabitJobDataDto(HabitAddDto):
    """Схема для создания задания о напоминании."""

    user_id: int
    chat_id: int


class HabitData(HabitJobDataDto):
    """Данные о привычке."""
    pass
