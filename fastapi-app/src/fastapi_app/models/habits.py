from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseOrmModel, TimestampMixin

if TYPE_CHECKING:
    from .tracking import Tracking
    from .users import User


class Habit(TimestampMixin, BaseOrmModel):
    """Модель привычки."""

    __tablename__ = "habits"

    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(default="", server_default="")
    remind_time: Mapped[time]
    remind_quantity: Mapped[int]
    completed: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(
        back_populates="habits",
        lazy="joined",
    )
    tracking: Mapped[list["Tracking"]] = relationship(
        back_populates="habit",
        lazy="selectin",
    )
