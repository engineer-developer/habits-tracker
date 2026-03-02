from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi_app.exceptions.repositories import EmptyResult
from fastapi_app.models import Tracking
from fastapi_app.repositories.base import Repository
from fastapi_app.schemas.tracking import TrackingCreateCommand, TrackingRead


class TrackingRepository(Repository):
    """Репозиторий отслеживаний привычек."""

    session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]

    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def create(self, cmd: TrackingCreateCommand) -> TrackingRead:
        """Создает отслеживание привычки в БД."""
        async with self.session_factory() as session:
            stmt = (
                insert(Tracking)
                .values(**cmd.model_dump())
                .execution_options(populate_existing=True)
                .options(joinedload(Tracking.habit))
                .returning(Tracking)
            )
            tracking_orm = await session.scalar(stmt)
            await session.commit()
            return TrackingRead.model_validate(tracking_orm)

    async def read_all_by_habit_id(self, habit_id: int) -> list[TrackingRead]:
        """Получает все отслеживания по habit_id."""
        async with self.session_factory() as session:
            stmt = (
                select(Tracking)
                .where(Tracking.habit_id == habit_id)
                .options(
                    joinedload(Tracking.habit),
                )
            )
            result = await session.scalars(stmt)
            tracking_orm = result.all()
            if not tracking_orm:
                raise EmptyResult
            habits_dto = [TrackingRead.model_validate(habit) for habit in tracking_orm]
            return habits_dto

    async def read_all(self) -> list[TrackingRead]:
        """Получает все отслеживания."""
        async with self.session_factory() as session:
            stmt = select(Tracking)
            result = await session.scalars(stmt)
            tracking_orm = result.all()
            return [TrackingRead.model_validate(elem) for elem in tracking_orm]
