from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from fastapi_app.configs.loguru_config import logger
from fastapi_app.exceptions.base import BaseApiException


async def handle_http_exception(
    request: Request, exc: BaseApiException
) -> JSONResponse:
    """Обработка API исключений."""
    logger.error(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def handle_other_exception(request: Request, exc: Exception) -> JSONResponse:
    """Обработка не обработанных исключений."""
    logger.error(repr(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": repr(exc)},
    )
