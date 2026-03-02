from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from fastapi_app.exceptions.repositories import EmptyResult
from fastapi_app.models import Habit
from fastapi_app.repositories.base import Repository
from fastapi_app.schemas.habits import (
    HabitByIdQuery,
    HabitByUserIdQuery,
    HabitCreateCommand,
    HabitDeleteCommand,
    HabitRead,
    HabitUpdateCommand,
)


class HabitRepository(Repository):
    """Репозиторий привычек."""

    session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def create(self, cmd: HabitCreateCommand) -> HabitRead:
        """Создает привычку в БД."""
        async with self.session_factory() as session:
            stmt = insert(Habit).values(**cmd.model_dump()).returning(Habit)
            habit_orm = await session.scalar(stmt)
            await session.commit()
            return HabitRead.model_validate(habit_orm)

    async def read(self, query: HabitByIdQuery) -> HabitRead:
        """Получает привычку по id."""
        async with self.session_factory() as session:
            habit_orm = await session.get(
                Habit,
                query.id,
                options=[
                    joinedload(Habit.user),
                    selectinload(Habit.tracking),
                ],
            )
            if not habit_orm:
                raise EmptyResult
            return HabitRead.model_validate(habit_orm)

    async def read_all_by_user_id(
        self,
        query: HabitByUserIdQuery,
        completed: bool,
    ) -> list[HabitRead]:
        """Получает все привычки по user_id.

        :param query: Фильтр по HabitByUserIdQuery.
        :param completed: Фильтр по состоянию выполнения.
        """
        async with self.session_factory() as session:
            stmt = (
                select(Habit)
                .where(
                    Habit.user_id == query.user_id,
                    Habit.completed == completed,
                )
                .options(
                    joinedload(Habit.user),
                    selectinload(Habit.tracking),
                )
            )
            result = await session.scalars(stmt)
            habits_orm = result.all()
            if not habits_orm:
                raise EmptyResult()
            habits_dto = [HabitRead.model_validate(habit) for habit in habits_orm]
            return habits_dto

    async def update(self, cmd: HabitUpdateCommand) -> HabitRead:
        """Обновление данных привычки в БД."""
        async with self.session_factory() as session:
            stmt = (
                update(Habit)
                .where(Habit.id == cmd.id)
                .values(**cmd.model_dump(exclude={"id"}, exclude_none=True))
                .returning(Habit)
            )
            habit_orm = await session.scalar(stmt)
            await session.commit()

            if not habit_orm:
                raise EmptyResult
            return HabitRead.model_validate(habit_orm)

    async def delete(self, cmd: HabitDeleteCommand) -> HabitRead:
        """Удаление привычки из БД."""
        async with self.session_factory() as session:
            stmt = delete(Habit).where(Habit.id == cmd.id).returning(Habit)
            habit_orm = await session.scalar(stmt)
            await session.commit()
            if not habit_orm:
                raise EmptyResult
            return HabitRead.model_validate(habit_orm)
