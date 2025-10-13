from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from models.app_models import User
from services.user_service import fetch_user_by_telegram_id
from schemas.user_schema import UserOutSchema


router = APIRouter(prefix="/auth")


@router.get("/")
async def auth(user: Annotated[User, Depends(fetch_user_by_telegram_id)]):
    """Представление для аутентификации пользователя."""
    if not user:
        user_status = "not registered"
    elif user and not user.is_active:
        user_status = "not logged in"
    elif user and user.is_active:
        user_status = "logged"
    else:
        user_status = "unknown"

    return {"user_status": user_status}