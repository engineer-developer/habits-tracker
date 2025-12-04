"""Модуль реализации API."""

from core.loguru_config import logger
from fastapi.routing import APIRouter

from api.auth.auth_router import router as auth_router
from api.habits.habits_router import router as habits_router
from api.users.user_router import router as users_router

API_VERSION = "1.0.0"


router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(habits_router)


@router.get(
    "/version/",
    name="Get api version",
    description="Get current api version",
    tags=["API"],
)
async def get_api_version() -> dict:
    """Получаем версию api."""
    logger.debug("Api version: {}", API_VERSION)
    return {"api_version": API_VERSION}
