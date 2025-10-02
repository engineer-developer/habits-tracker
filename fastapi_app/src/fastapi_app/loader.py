"""Модуль загрузки сервиса Fastapi."""

from asyncio import get_running_loop
from contextlib import asynccontextmanager
from typing import AsyncIterator

from alembic_utils import upgrade_to_head
from app_cfg.config import CommonSettings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncIterator[None]:
    """Настройка параметров приложения.

    :param app: Экземпляр класса Fastapi.
    :return: Асинхронный итератор.
    """
    # Применение миграций alembic
    loop = get_running_loop()
    loop.run_in_executor(None, upgrade_to_head)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", name="Get some", description="Get some info")
async def get_some(settings: CommonSettings) -> dict:
    """Тестовая ручка.

    :return: db_url
    """
    db_url = settings.db_url
    return {"DB_URL": db_url, "message": "HI Nick"}
