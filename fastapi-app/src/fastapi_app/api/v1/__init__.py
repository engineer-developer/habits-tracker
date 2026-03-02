# ruff: noqa

from fastapi import APIRouter

from fastapi_app.api.v1.auth import router as auth_router
from fastapi_app.api.v1.habits import router as habits_router
from fastapi_app.api.v1.users import router as users_router
from fastapi_app.api.v1.tracking import router as tracking_router


API_VERSION = "1.0.0"


router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(habits_router)
router.include_router(tracking_router)


@router.get(
    "",
    description="Index",
    tags=["API"],
)
async def index() -> dict:
    """Роут API V1."""
    return {
        "status": "ok",
        "version": API_VERSION,
    }
