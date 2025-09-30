"""
Менеджер базы данных.

async_engine - асинхронный движок
AsyncSessionMaker - класс для создания асинхронных сессий
"""

from typing import Annotated, AsyncIterator

from config import Settings, get_settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

CommonSettings = Annotated[Settings, Depends(get_settings)]


def get_async_engine(settings: CommonSettings) -> AsyncEngine:
    """
    Получаем асинхронный движок.

    :param settings: Настройки приложения.
    :type settings: CommonSettings
    :return: Асинхронный движок.
    :rtype: AsyncEngine
    """
    a_engine = create_async_engine(url=settings.db_url.unicode_string())
    a_engine.execution_options(isolation_level="SERIALIZABLE")
    return a_engine


async_engine = Depends(get_async_engine)
AsyncSessionMaker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """
    Получаем асинхронную сессию.

    :return: Асинхронная сессия.
    :rtype: AsyncSession
    """
    async with AsyncSessionMaker() as session:
        yield session


async def get_engine_connection() -> AsyncIterator[AsyncConnection]:
    """
    Получаем асинхронное подключение.

    :return: Асинхронное подключение.
    :rtype: AsyncConnection
    """
    async with async_engine.begin() as connection:
        yield connection
