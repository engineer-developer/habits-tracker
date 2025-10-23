"""Модуль операций с пользователями."""

from typing import Optional, Sequence

from api.auth.password_handler import get_password_hash
from core.loguru_config import logger
from models.app_models import User
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all_users(
    session: AsyncSession,
    is_active: bool = False,
) -> Sequence[User]:
    """Извлекаем всех пользователей из БД.

    :param session: Сессия подключения к БД.
    :param is_active: Флаг получения только активных пользователей.
    :return: Список пользователей.
    """
    stmt = select(User)

    if is_active:
        stmt = stmt.where(User.is_active)

    result = await session.execute(stmt)
    users = result.scalars().all()
    logger.debug("Получены пользователи: {}", users)
    return users


async def fetch_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int,
) -> Optional[User]:
    """Получаем пользователя из БД по telegram_id."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        logger.debug("Получен пользователь {}", user)
    return user


async def add_user_to_db(
    session: AsyncSession,
    user: User,
) -> Optional[User]:
    """Добавляем пользователя в базу данных."""
    user_hashed_password = await get_password_hash(user.password)
    user.password = user_hashed_password
    session.add(user)
    try:
        await session.commit()
        logger.info("Пользователь {} добавлен.", user)
        return user
    except IntegrityError:
        logger.error("Пользователь уже есть в БД.")
    except DatabaseError as exc:
        logger.error("{} - {}", exc.__class__.__name__, exc.args[0])
