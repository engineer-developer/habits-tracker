# ruff: noqa

from fastapi import APIRouter

from configs.loguru_config import logger
from .auth import router as auth_router
# from .habits import router as habits_router
from .users import router as users_router


API_VERSION = "1.0.0"
router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(users_router)
# router.include_router(habits_router)


@router.get(
    "",
    description="Index",
    tags=["API"],
)
async def index() -> dict:
    """Главная страница."""
    return {"status": "ok"}


@router.get(
    "/version",
    name="Get api version",
    description="Get current api version",
    tags=["API"],
)
async def get_api_version() -> dict:
    """Получаем версию api."""
    logger.debug("Api version: {}", API_VERSION)
    return {"api_version": API_VERSION}
