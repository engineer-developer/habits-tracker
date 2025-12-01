"""Модуль определения моделей таблиц базы данных."""

from datetime import datetime, time

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
    CheckConstraint,
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
    __table_args__ = (UniqueConstraint("name", "user_id"),)

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(default="", server_default="")
    completed: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="habits")
    reminder: Mapped["Reminder"] = relationship(back_populates="habit")
    tracking: Mapped[list["Tracking"]] = relationship(back_populates="habit")


class Reminder(TimestampMixin, Model):
    """Модель напоминания."""

    __tablename__ = "reminders"

    remind_time: Mapped[time]
    remind_quantity: Mapped[int]
    job_id: Mapped[str] = mapped_column(unique=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))

    habit: Mapped["Habit"] = relationship(back_populates="reminder")


class Tracking(TimestampMixin, Model):
    """Модель для отслеживания выполненных привычек."""

    __tablename__ = "tracking"

    alert_time: Mapped[datetime]=mapped_column(TIMESTAMP(timezone=True))
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))

    habit: Mapped["Habit"] = relationship(back_populates="tracking")
