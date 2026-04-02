from contextlib import AbstractAsyncContextManager
from typing import Callable

from pydantic import PositiveInt
from sqlalchemy import delete, insert, select, update, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, aliased

from fastapi_app.configs.loguru_config import logger
from fastapi_app.exceptions.repositories import EmptyResult
from fastapi_app.models import Habit, Tracking, User
from fastapi_app.repositories.base import Repository
from fastapi_app.schemas.habits import (
    HabitByIdQuery,
    HabitByUserIdQuery,
    HabitCreateCommand,
    HabitDeleteCommand,
    HabitRead,
    HabitUpdateCommand,
    DeletedHabitsIds,
)
from fastapi_app.schemas.users import UserByTelegramIdQuery


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

    async def update(self, habit_id: PositiveInt, cmd: HabitUpdateCommand) -> HabitRead:
        """Обновление данных привычки в БД."""
        async with self.session_factory() as session:
            stmt = (
                update(Habit)
                .where(Habit.id == habit_id)
                .values(**cmd.model_dump(exclude_unset=True))
                .returning(Habit)
            )
            habit_orm = await session.scalar(stmt)
            await session.commit()

            if not habit_orm:
                raise EmptyResult
            return HabitRead.model_validate(habit_orm)

    async def delete(self, habit_id: int) -> HabitRead:
        """Удаление привычки и ее отслеживаний из БД."""
        async with self.session_factory() as session:
            delete_habit_tracking_stmt_cte = (
                delete(Tracking)
                .where(Tracking.habit_id == habit_id)
                .cte("delete_habit_tracking")
            )
            stmt = (
                delete(Habit)
                .where(Habit.id == habit_id)
                .returning(Habit)
                .add_cte(delete_habit_tracking_stmt_cte)
            )
            habit_orm = await session.scalar(stmt)
            await session.commit()
            if not habit_orm:
                raise EmptyResult
            return HabitRead.model_validate(habit_orm)

    async def delete_completed_habits_by_telegram_id(
        self, query: UserByTelegramIdQuery
    ) -> DeletedHabitsIds:
        """Удаление завершенных привычек и их отслеживаний из БД"""
        async with self.session_factory() as session:
            async with session.begin():
                completed_habits_ids_cte = (
                    select(Habit.id)
                    .join(User, User.id == Habit.user_id)
                    .where(
                        User.telegram_id == query.telegram_id,
                        Habit.completed == True,
                    )
                    .cte("completed_habits_ids")
                )
                await session.execute(
                    delete(Tracking).where(
                        Tracking.habit_id.in_(select(completed_habits_ids_cte))
                    )
                )

                delete_completed_habits_stmt = (
                    delete(Habit)
                    .where(Habit.id.in_(select(completed_habits_ids_cte)))
                    .returning(Habit.id)
                )
                logger.debug(delete_completed_habits_stmt)
                result = await session.execute(delete_completed_habits_stmt)
                habits_ids = result.scalars().all()
                deleted_habits_ids = DeletedHabitsIds(habits_ids=list(habits_ids))
                return deleted_habits_ids
