"""Модуль загрузки сервиса Fastapi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from config import Settings, get_settings
from fastapi import Depends, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Настройка параметров приложения.

    :param app: Экземпляр класса Fastapi.
    :return: Асинхронный итератор.
    """
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", name="Get some", description="Get some info")
async def get_some(settings: Settings = Depends(get_settings)) -> dict:
    """
    Тестовая ручка.

    :return: db_url
    """
    db_url = settings.db_url
    return {"DB_URL": db_url, "message": "HI Nick"}
