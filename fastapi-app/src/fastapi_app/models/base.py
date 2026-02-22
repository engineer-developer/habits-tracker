"""Модуль базовой ORM модели базы данных."""

from datetime import UTC, datetime
from typing import TypeVar

from sqlalchemy import MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

__all__ = (
    "Model",
    "BaseOrmModel",
    "TimestampMixin",
    "metadata",
)

Model = TypeVar("Model", bound="BaseOrmModel")

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s_%(column_1_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)
custom_registry = registry(metadata=metadata)


class BaseOrmModel(AsyncAttrs, DeclarativeBase):
    """Базовая ORM модель."""

    __abstract__ = True
    registry = custom_registry

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"


class TimestampMixin:
    """Миксин для дополнения ORM модели временем создания."""

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC).replace(tzinfo=None),
        server_default=func.now(),
    )
