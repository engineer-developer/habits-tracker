"""Менеджер базы данных.

async_engine - асинхронный движок
AsyncSessionMaker - класс для создания асинхронных сессий
"""

from typing import Annotated, AsyncIterator

from core.config import get_settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

settings = get_settings()

# Создаем асинхронный движок
async_engine: AsyncEngine = create_async_engine(
    url=settings.db_url.unicode_string(),
    echo=True,
)
async_engine.execution_options(isolation_level="SERIALIZABLE")

# Создаем фабрику асинхронных сессий
AsyncSessionMaker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """Получаем асинхронную сессию.

    :return: Асинхронная сессия.
    :rtype: AsyncSession
    """
    async with AsyncSessionMaker() as session:
        yield session


async def get_engine_connection() -> AsyncIterator[AsyncConnection]:
    """Получаем асинхронное подключение.

    :return: Асинхронное подключение.
    :rtype: AsyncConnection
    """
    async with async_engine.begin() as connection:
        yield connection


CommonAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
CommonAsyncConnection = Annotated[AsyncConnection, Depends(get_engine_connection)]
