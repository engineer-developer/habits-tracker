"""Модуль загрузки приложения."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from fastapi_app.api.v1 import router as api_v1_router
from fastapi_app.configs.config import get_settings
from fastapi_app.containers.app_container import AppContainer
from fastapi_app.exceptions.base import BaseApiException
from fastapi_app.handlers.handle_exception import (
    handle_http_exception,
    handle_other_exception,
)


def create_app() -> FastAPI:
    """Создает приложение Fastapi."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Жизненный цикл приложения."""
        settings = get_settings()
        container = AppContainer()
        container.config.from_pydantic(settings)
        container.wire(packages=["fastapi_app.api"])
        app.container = container
        app.include_router(api_v1_router)
        app.add_exception_handler(BaseApiException, handle_http_exception)
        app.add_exception_handler(Exception, handle_other_exception)
        yield

    app = FastAPI(
        title="Habit tracker",
        description="Backend app for habit tracking",
        lifespan=lifespan,
    )

    return app
