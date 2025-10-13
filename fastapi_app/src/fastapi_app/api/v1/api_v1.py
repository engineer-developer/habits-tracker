from core.loguru_config import logger
from fastapi.routing import APIRouter
from api.v1.user_router import router as users_router

API_VERSION = "0.1.0"

router = APIRouter(prefix="/api/v1", )

router.include_router(users_router)


@router.get(
    "/version/",
    name="Get api version",
    description="Get current api version",
    tags=["API"],
)
async def get_api_version():
    logger.debug("Api version: {}", API_VERSION)
    return {"api_version": API_VERSION}
