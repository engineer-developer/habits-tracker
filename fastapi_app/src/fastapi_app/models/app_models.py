"""Модуль определения моделей таблиц базы данных."""

from datetime import datetime, time

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base_model import Model, TimestampMixin


class User(TimestampMixin, Model):
    """Модель пользователя."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    habits: Mapped[list["Habit"]] = relationship(back_populates="user")


class Habit(TimestampMixin, Model):
    """Модель привычки."""

    __tablename__ = "habits"

    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(default="", server_default="")
    remind_time: Mapped[time]
    remind_quantity: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")
    tracking: Mapped[list["Tracking"]] = relationship(back_populates="habit")




class Tracking(TimestampMixin, Model):
    """Модель для отслеживания выполнения привычек."""

    __tablename__ = "tracking"

    execution_time: Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True))
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))

    habit: Mapped["Habit"] = relationship(back_populates="tracking")
