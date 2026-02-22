"""Модуль загрузки приложения."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from api import api_v1_router
from fastapi import FastAPI
import uvicorn
from containers.app_container import AppContainer
from configs.app_config import get_settings, Settings

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
    container.wire(packages=["api"])

    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(api_v1_router)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app")
