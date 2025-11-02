"""Модуль обслуживания привычек."""

from typing import Sequence

from core.loguru_config import logger
from fastapi import HTTPException
from models.app_models import Habit, Reminder
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


async def add_habit_to_db(habit: Habit, session: AsyncSession) -> bool:
    """Добавление привычки в базу данных."""
    session.add(habit)
    try:
        await session.commit()
        return True
    except Exception as exc:
        logger.error(exc)
        raise HTTPException(status_code=400, detail=exc)


async def fetch_habit_by_id(id: int, session: AsyncSession) -> Habit:
    """Извлечение привычки из базы данных по id."""
    stmt = (
        select(Habit)
        .where(Habit.id == id)
        .options(
            joinedload(Habit.user),
            joinedload(Habit.reminder),
            selectinload(Habit.tracking),
        )
    )
    habit = await session.scalar(stmt)
    logger.debug("Получена привычка: {}", habit)
    return habit


async def fetch_habit_by_name_and_user_id(
    name: str, user_id: int, session: AsyncSession
) -> Habit:
    """Извлечение привычки из базы данных по name и user_id."""
    stmt = (
        select(Habit)
        .filter_by(name=name, user_id=user_id)
        .options(
            joinedload(Habit.user),
            joinedload(Habit.reminder),
            selectinload(Habit.tracking),
        )
    )
    habit = await session.scalar(stmt)
    logger.debug("Получена привычка: {}", habit)
    return habit


async def fetch_habit_by_name_and_job_id(
    name: str, job_id: str, session: AsyncSession
) -> Habit:
    """Извлечение привычки из базы данных по name и job_id."""
    stmt = (
        select(Habit)
        .join(Reminder, Reminder.habit_id == Habit.id)
        .filter(
            Reminder.job_id == job_id,
            Habit.name == name,
        )
        .options(
            joinedload(Habit.reminder),
            selectinload(Habit.tracking),
        )
    )
    habit = await session.scalar(stmt)
    logger.debug("Получена привычка: {}", habit)
    return habit


async def delete_habit_by_name_and_user_id(
    name: str, user_id: int, session: AsyncSession
) -> int | None:
    """Удаление привычки из базы данных по name и user_id."""
    stmt = delete(Habit).filter_by(name=name, user_id=user_id).returning(Habit.id)
    res = await session.execute(stmt)
    deleted_habit_id = res.scalar()
    if not deleted_habit_id:
        return None
    await session.commit()
    logger.debug("Удалена привычка c id={}", deleted_habit_id)
    return deleted_habit_id


async def fetch_all_habit_by_user_id(
    user_id: int, session: AsyncSession
) -> Sequence[Habit]:
    """Извлечение всех привычек пользователя."""
    stmt = (
        select(Habit)
        .where(Habit.user_id == user_id)
        .options(
            joinedload(Habit.user),
            joinedload(Habit.reminder),
            selectinload(Habit.tracking),
        )
    )
    res = await session.scalars(stmt)
    habits = res.all()
    logger.debug("Получены привычки: {}", habits)
    return habits
