from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi_app.exceptions.repositories import EmptyResult, EntityAlreadyExist
from fastapi_app.models.users import User
from fastapi_app.repositories.base import Repository
from fastapi_app.schemas.users import (
    UserByIdQuery,
    UserByTelegramIdQuery,
    UserCreateCommand,
    UserRead,
    UserReadWithPassword,
)


class UserRepository(Repository):
    """Репозиторий пользователей."""

    session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def create(self, cmd: UserCreateCommand) -> UserRead:
        """Создает пользователя в БД."""
        user_orm = User(**cmd.model_dump())
        async with self.session_factory() as session:
            session.add(user_orm)
            try:
                await session.commit()
            except IntegrityError:
                raise EntityAlreadyExist("User already exist")
            await session.refresh(user_orm)
            return UserRead.model_validate(user_orm)

    async def read(self, query: UserByIdQuery) -> UserReadWithPassword:
        """Получает пользователя по id."""
        async with self.session_factory() as session:
            user_orm = await session.get(User, query.id)
            if user_orm is None:
                raise EmptyResult("User not found")
            return UserReadWithPassword.model_validate(user_orm)

    async def read_by_telegram_id(
        self,
        query: UserByTelegramIdQuery,
    ) -> UserReadWithPassword:
        """Получаем пользователя по telegram_id."""
        async with self.session_factory() as session:
            stmt = (
                select(User)
                .where(User.telegram_id == query.telegram_id)
                .options(selectinload(User.habits))
            )
            user_orm = await session.scalar(stmt)
            if user_orm is None:
                raise EmptyResult("User not found")
            return UserReadWithPassword.model_validate(user_orm)

    async def read_all(self) -> list[UserRead]:
        async with self.session_factory() as session:
            stmt = select(User)
            result = await session.scalars(stmt)
            users_dto = [UserRead.model_validate(user) for user in result]
            return users_dto
