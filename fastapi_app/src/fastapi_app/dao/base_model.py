"""
Модуль создания базовой модели базы данных.

naming_convention - Шаблон соглашения об именовании.
metadata - Метаданные.
custom_registry - Обобщенный реестр для сопоставления классов.
Model - Базовая модель.
TimeStampMixin - Миксин для дополнения модели временем создания и обновления.
"""

from datetime import UTC, datetime

from sqlalchemy import MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s_%(column_1_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)

custom_registry = registry(metadata=metadata)


class Model(AsyncAttrs, DeclarativeBase):
    """Базовая модель."""

    __abstract__ = True
    registry = custom_registry

    id: Mapped[int] = mapped_column(primary_key=True)


class TimeStampMixin:
    """Миксин для дополнения модели временем создания и обновления."""

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        server_default=func.now(),
        onupdate=func.now(),
    )
