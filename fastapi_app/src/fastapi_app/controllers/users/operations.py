from typing import Sequence

from app_logging.logger import logger
from dao.models import User
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession


async def add_user(session: AsyncSession, user: User):
async def fetch_all_users(session: AsyncSession) -> Sequence[User]:
    """Извлекаем всех активных пользователей из БД"""
    stmt = select(User).where(User.is_active == True)
    result = await session.execute(stmt)
    users = result.scalars().all()
    logger.debug("Got users: {}", users)
    return users


    session.add(user)
    try:
        await session.commit()
        return user
    except DatabaseError as exc:
        return exc



async def fetch_all_users(session: AsyncSession):
    stmt = select(User).where(User.is_active==True)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users
