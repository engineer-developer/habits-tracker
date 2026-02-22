"""Модуль тестов БД."""

import pytest
from conftest import test_engine
from models.users import User
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncConnection

from tests.conftest import Async_session


@pytest.mark.parametrize(
    "table_name",
    ["users", "habits", "reminders", "tracking"],
)
async def test_db_has_tables(table_name: str) -> None:
    """Тест - проверяет, что в БД есть вышеуказанные таблицы."""

    def get_tables(connection: AsyncConnection) -> list[str]:
        """Получаем таблицы с помощью inspector."""
        inspector = inspect(connection)
        return inspector.get_table_names()

    async with test_engine.begin() as conn:
        tables = await conn.run_sync(get_tables)

    assert table_name in tables


async def test_users_in_db() -> None:
    """Тест - проверяем наличие пользователей в БД."""
    users_count = 2
    async with Async_session() as session:
        stmt = select(User)
        res = await session.scalars(stmt)
        users_orm = res.all()
    assert len(users_orm) == users_count
