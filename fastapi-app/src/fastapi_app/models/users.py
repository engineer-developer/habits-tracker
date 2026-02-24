from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseOrmModel, TimestampMixin

if TYPE_CHECKING:
    from .habits import Habit


class User(TimestampMixin, BaseOrmModel):
    """Модель пользователя."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    habits: Mapped[list["Habit"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )
