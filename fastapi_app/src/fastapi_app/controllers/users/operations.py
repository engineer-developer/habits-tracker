from typing import Sequence

from app_logging.logger import logger
from controllers.auth.password_handler import get_password_hash
from dao.models import User
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    """Извлекаем всех активных пользователей из БД"""
    stmt = select(User).where(User.is_active == True)
    result = await session.execute(stmt)
    users = result.scalars().all()
    logger.debug("Got users: {}", users)
    return users


async def add_user_to_db(user: User, session: AsyncSession):
    """Добавляем пользователя в базу данных"""
    user_hash_password = await get_password_hash(user.password)
    user.password = user_hash_password
    session.add(user)
    try:
        await session.commit()
        logger.info("User {} added.", user.name)
        return user
    except DatabaseError as exc:
        logger.error("{} - {}", exc.__class__.__name__, exc.args[0])
        return exc
