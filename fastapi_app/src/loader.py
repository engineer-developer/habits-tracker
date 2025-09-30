"""Модуль загрузки сервиса Fastapi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Настройка параметров приложения.

    :param app: Экземпляр класса Fastapi.
    :return: Асинхронный генератор.
    """
    settings = Settings()
    app.state.settings = settings

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", name="Get some", description="Get some info")
async def get_some() -> dict:
    """
    Тестовая ручка.

    :return: db_url
    """
    db_url = app.state.settings.db_url
    return {"DB_URL": db_url}
