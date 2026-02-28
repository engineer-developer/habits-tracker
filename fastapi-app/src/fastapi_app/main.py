"""Модуль загрузки приложения."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from fastapi_app.api.v1 import router as api_v1_router
from fastapi_app.configs.config import Settings
from fastapi_app.containers.app_container import AppContainer


def create_app() -> FastAPI:
    """Создаем приложение Fastapi."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Жизненный цикл приложения."""
        # выполняем при запуске Fastapi
        yield
        # выполняем после остановки Fastapi

    container = AppContainer()
    container.config.from_pydantic(Settings())
    container.wire(packages=["fastapi_app.api"])

    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(api_v1_router)
    return app
