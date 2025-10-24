"""Модуль представлений пользователей."""

from typing import Annotated, Sequence

from core.database import CommonAsyncSession
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Query
from fastapi.routing import APIRouter
from models.app_models import User
from schemas.user_schema import UserInSchema, UserOutSchema, UsersListSchema
from services.user_service import add_user_to_db, fetch_all_users

from api.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile/", response_model=UserOutSchema, status_code=200)
async def get_profile(
    user: Annotated[User, Depends(get_current_active_user)],
) -> UserOutSchema:
    """Представление для получения профиля пользователя.

    Получаем данные зарегистрированного, аутентифицированного
    и активного пользователя.
    """
    return UserOutSchema.model_validate(user)
