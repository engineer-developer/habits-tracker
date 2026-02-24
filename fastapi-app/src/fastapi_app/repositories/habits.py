from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import Habit

from fastapi_app.repositories.base import Repository


class HabitRepository(Repository):
    """Репозиторий привычек."""

    session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create(self, cmd) -> Habit:
        pass

    async def read(self, query) -> Habit:
        pass

    async def read_all(self) -> list[Habit]:
        pass

    async def update(self, cmd) -> Habit:
        pass

    async def delete(self, cmd) -> Habit:
        pass
