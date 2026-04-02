from typing import AsyncGenerator, AsyncIterator, Any, Generator

import pytest
from fastapi_app.configs.config import get_settings
from fastapi_app.database.database import Database
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from fastapi_app.main import create_app
from fastapi_app.models.users import User
from fastapi_app.models.base import BaseOrmModel
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from source_data.users import users_list

settings = get_settings()
prod_db_url = settings.db.dsn.render_as_string()
test_db_url = prod_db_url.rsplit(sep="/", maxsplit=1)[0] + "/test_db"


test_engine = create_async_engine(
    url=test_db_url,
    poolclass=NullPool,
    echo=False,
)
Async_session = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)
BaseOrmModel.metadata.bind = test_engine


# async def override_get_async_session() -> AsyncIterator[AsyncSession]:
#     """Получаем асинхронную сессию."""
#     async with Async_session() as session:
#         yield session


@pytest.fixture(scope="session")
async def users(request) -> list[User]:
    """Получаем список пользователей."""
    users = [User(**row) for row in users_list]
    return users


@pytest.fixture(autouse=True, scope="session")
async def prepare_database(users) -> AsyncGenerator[None, Any]:
    """Подготовка БД."""
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.drop_all)
        await conn.run_sync(BaseOrmModel.metadata.create_all)

    async with Async_session() as session:
        session.add_all(users)
        await session.commit()

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.drop_all)


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """Инициализируем тестовое приложение."""
    _app: FastAPI = create_app()

    # Переопределение зависимостей
    # _app.dependency_overrides[get_async_session] = override_get_async_session
    yield _app


@pytest.fixture(scope="session")
async def async_client(app) -> AsyncIterator[AsyncClient]:
    """Create async client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest.fixture(scope="session")
async def jwt_token(async_client: AsyncClient, users: list[User]):
    url = "api/auth/login/"
    data = {
        "username": 1,
        "password": "123",
    }
    response = await async_client.post(url=url, data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        raise Exception("Failed to get token.")
