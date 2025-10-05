"""Модуль модели таблицы базы данных для пользователя."""

from sqlalchemy import (
    BigInteger,
    Boolean,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Model, TimestampMixin


class User(TimestampMixin, Model):
    """Модель пользователя."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
    )

    def __repr__(self):
        return f"<User id-{self.id}>"
