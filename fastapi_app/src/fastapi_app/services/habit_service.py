"""Модуль обслуживания привычек."""

from typing import Sequence, Optional, Any, Coroutine

from core.loguru_config import logger
from fastapi import HTTPException
from models.app_models import Habit
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import DBAPIError


async def add_habit_to_db(
    habit_data: dict, user_id: int, session: AsyncSession
) -> Habit | None:
    """Функция добавления привычки в базу данных."""
    habit = Habit(
        title=habit_data.get("title"),
        description=habit_data.get("description"),
        remind_time=habit_data.get("remind_time"),
        remind_quantity=habit_data.get("remind_quantity"),
        completed=False,
        user_id=user_id,
    )
    session.add(habit)

    try:
        await session.commit()
        return habit
    except DBAPIError as exc:
        logger.error(exc)
        return None


async def fetch_habit_by_id(id: int, session: AsyncSession) -> Habit:
    """Функция извлечения привычки из базы данных по id."""
    stmt = (
        select(Habit)
        .where(Habit.id == id)
        .options(
            joinedload(Habit.user),
            selectinload(Habit.tracking),
        )
    )
    habit = await session.scalar(stmt)
    logger.debug("Получена привычка: {}", habit)
    return habit


async def fetch_all_habit_by_user_id(
    user_id: int,
    session: AsyncSession,
    completed=False,
) -> Sequence[Habit]:
    """Функция извлечения всех привычек пользователя.

    По умолчанию извлекает только незавершенные привычки.
    """
    stmt = (
        select(Habit)
        .filter(
            Habit.user_id == user_id,
            Habit.completed == completed,
        )
        .options(
            joinedload(Habit.user),
            selectinload(Habit.tracking),
        )
    )
    result = await session.scalars(stmt)
    habits = result.all()
    logger.debug("Получены привычки: {}", habits)
    return habits


async def edit_habit(
    id: int, data: dict, session: AsyncSession
) -> [Optional[Habit], bool]:
    """Функция изменения данных привычки."""
    edited: bool = False

    habit = await fetch_habit_by_id(id=id, session=session)
    if not habit:
        return None, edited

    title = data.get("title")
    if title is not None:
        habit.title = title
        edited = True

    description = data.get("description")
    if description is not None:
        habit.description = description
        edited = True

    remind_quantity = data.get("remind_quantity")
    if remind_quantity is not None and remind_quantity > 0:
        habit.remind_quantity = remind_quantity
        edited = True

    remind_time = data.get("remind_time")
    if remind_time is not None:
        habit.remind_time = remind_time
        edited = True

    if edited:
        await session.commit()

    return habit, edited


async def delete_habit(id: int, session: AsyncSession) -> int | None:
    """Функция удаления привычки из базы данных."""
    stmt = delete(Habit).filter(Habit.id == id).returning(Habit.id)
    result = await session.execute(stmt)
    deleted_habit_id = result.scalar()

    if not deleted_habit_id:
        return None

    await session.commit()
    logger.debug("Удалена привычка c id={}", deleted_habit_id)
    return deleted_habit_id
