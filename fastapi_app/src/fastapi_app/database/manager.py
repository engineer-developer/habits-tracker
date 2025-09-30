from typing import Annotated, AsyncIterator

from fastapi import Depends

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    AsyncConnection,
)
from config import get_settings, Settings

CommonSettings = Annotated[Settings, Depends(get_settings)]


def get_async_engine(settings: CommonSettings) -> AsyncEngine:
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
    async with AsyncSessionMaker() as session:
        yield session


async def get_engine_connection() -> AsyncIterator[AsyncConnection]:
    async with async_engine.begin() as connection:
        yield connection
