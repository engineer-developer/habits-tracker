"""Модуль операций с пользователями."""

from core.loguru_config import logger
from fastapi import Depends
from models.app_models import User
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all_users(
    session: AsyncSession, is_active: bool = False
) -> Sequence[User]:
    """Извлекаем всех пользователей из БД.

    :param session: Сессия подключения к БД.
    :param is_active: Флаг получения только активных пользователей.
    :return: Список пользователей.
    """
    if is_active:
        stmt = select(User).where(User.is_active)
    else:
        stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()
    logger.debug("Получены пользователи: {}", users)
    return users


async def fetch_user_by_telegram_id(
    telegram_id: int, session: AsyncSession
) -> Optional[User]:
    """Извлекаем пользователя из БД по telegram_id."""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar()
    if user:
        logger.debug("Получен пользователь {}", user)
        return user


async def add_user_to_db(user: User, session: AsyncSession) -> Optional[User]:
    """Добавляем пользователя в базу данных"""
    user_hash_password = await get_password_hash(user.password)
    user.password = user_hash_password
    session.add(user)
    try:
        await session.commit()
        logger.info("Пользователь {} добавлен.", user)
        return user
    except IntegrityError:
        logger.error("Пользователь уже есть в БД.")
    except DatabaseError as exc:
        logger.error("{} - {}", exc.__class__.__name__, exc.args[0])
