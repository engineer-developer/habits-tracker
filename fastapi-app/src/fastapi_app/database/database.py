"""Модуль базы данных."""

from contextlib import asynccontextmanager

import sqlalchemy
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database:
    def __init__(
        self,
        drivername: str,
        username: str,
        password: SecretStr,
        host: str,
        port: int,
        database: str,
    ) -> None:
        url = sqlalchemy.URL.create(
            drivername=drivername,
            username=username,
            password=password.get_secret_value(),
            host=host,
            port=port,
            database=database,
        ).render_as_string(hide_password=False)
        print(url)
        self._engine: AsyncEngine = create_async_engine(url=url, echo=True)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
