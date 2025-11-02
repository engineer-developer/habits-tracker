"""Модуль представлений пользователей."""

from typing import Annotated

from fastapi.params import Depends
from fastapi.routing import APIRouter
from models.app_models import User
from schemas.user_schema import UserOutDto

from api.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile/", response_model=UserOutDto, status_code=200)
async def get_profile(
    user: Annotated[User, Depends(get_current_active_user)],
) -> UserOutDto:
    """Представление для получения профиля пользователя.

    Получаем данные зарегистрированного, аутентифицированного
    и активного пользователя.
    """
    return UserOutDto.model_validate(user)
