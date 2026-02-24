from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseOrmModel, TimestampMixin

if TYPE_CHECKING:
    from .habits import Habit


class Tracking(TimestampMixin, BaseOrmModel):
    """Модель для отслеживания выполнения привычек."""

    __tablename__ = "tracking"

    execution_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"))

    habit: Mapped["Habit"] = relationship(
        back_populates="tracking",
        lazy="joined",
    )
