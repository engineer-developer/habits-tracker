from typing import Sequence, Optional

from core.loguru_config import logger
from services.auth.password_handler import get_password_hash
from models.user_model import User
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    """Извлекаем всех активных пользователей из БД"""
    stmt = select(User).where(User.is_active == True)
    result = await session.execute(stmt)
    users = result.scalars().all()
    logger.debug("Got users: {}", users)
    return users


async def fetch_user_by_telegram_id(
    telegram_id: int, session: AsyncSession
) -> Optional[User]:
    """Извлекаем пользователя из БД"""
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.one_or_none()
    return user


async def add_user_to_db(user: User, session: AsyncSession) -> Optional[User]:
    """Добавляем пользователя в базу данных"""
    user_hash_password = await get_password_hash(user.password)
    user.password = user_hash_password
    session.add(user)
    try:
        await session.commit()
        logger.info("Пользователь {} добавлен.", user.first_name)
        return user
    except IntegrityError:
        logger.error("Пользователь уже есть в БД")
    except DatabaseError as exc:
        logger.error("{} - {}", exc.__class__.__name__, exc.args[0])
