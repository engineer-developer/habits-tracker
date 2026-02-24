from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional, Type

from fastapi_app.models import User
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.repositories.base import Repository
from fastapi_app.exceptions.repositories import EntityAlreadyExist, EmptyResult


class UserRepository(Repository):
    """Репозиторий пользователей."""

    session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create(self, user: User) -> User:
        """Create User."""
        async with self.session_factory() as session:
            session.add(user)
            try:
                await session.commit()
            except IntegrityError:
                raise EntityAlreadyExist()
            await session.refresh(user)
            return user

    async def read(self, id: int) -> Optional[Type[User]]:
        """Get user by id."""
        async with self.session_factory() as session:
            user = await session.get(User, id)
            if user is None:
                raise EmptyResult("User not found")
            return user

    async def read_by_telegram_id(self, telegram_id: int) -> User:
        """Получаем пользователя по telegram_id."""
        async with self.session_factory() as session:
            stmt = (
                select(User)
                .where(User.telegram_id == telegram_id)
                # TODO: add habits JOIN
                # .options(selectinload(User.habits))
            )
            user = await session.scalar(stmt)
            if user is None:
                raise EmptyResult("User not found")
            return user

    async def read_all(self) -> list[User]:
        async with self.session_factory() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def update(self, cmd) -> User:
        pass

    async def delete(self, id: int) -> User:
        async with self.session_factory() as session:
            stmt = delete(User).filter_by(id=id).returning(User)
            res = await session.scalar(stmt)
            return res
