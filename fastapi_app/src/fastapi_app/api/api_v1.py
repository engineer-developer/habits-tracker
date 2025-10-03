from fastapi.routing import APIRouter

from app_cfg.config import CommonSettings
from app_logging.logger import logger
from routers.users.view import router as users_router


API_VERSION = "0.1.0"

router = APIRouter(prefix="/api", )

router.include_router(users_router)


@router.get("/version", name="Get api version", description="Get current api version", tags=["API"])
async def get_api_version():
    logger.debug("Api version: {}", API_VERSION)
    return {"api_version": API_VERSION}

@router.get("", name="Get some", description="Get some info", tags=["API"])
async def get_some(settings: CommonSettings) -> dict:
    """Тестовая ручка.

    :return: db_url
    """
    db_url = settings.db_url
    return {"DB_URL": db_url, "message": "HI Nick"}