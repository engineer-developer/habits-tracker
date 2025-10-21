"""Модуль загрузки сервиса Fastapi."""

from asyncio import get_running_loop
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from alembic_utils import upgrade_to_head
from api.api_router import router as api_router
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
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
