"""Модуль представлений пользователей."""

from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import Depends, status
from fastapi.routing import APIRouter

from fastapi_app.dependencies.auth import get_current_user_telegram_id
from fastapi_app.dependencies.users import DepsUserService
from fastapi_app.schemas.users import UserByTelegramIdQuery, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/profile",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    description="""
    Получаем профиль активного пользователя.
    
    Получаем данные зарегистрированного, аутентифицированного и активного пользователя.
    """,
)
@inject
async def get_user(
    telegram_id: Annotated[int, Depends(get_current_user_telegram_id)],
    user_service: DepsUserService,
) -> UserRead:
    """Получаем профиль активного пользователя."""
    user = await user_service.get_current_active_user(
        query=UserByTelegramIdQuery(telegram_id=telegram_id)
    )
    return user


# @router.get(
#     "",
#     response_model=list[UserRead],
#     status_code=status.HTTP_200_OK,
# )
# @inject
# async def get_all_users(
#     user_service: DepsUserService,
# ) -> list[UserRead]:
#     """Получаем всех пользователей."""
#     users = await user_service.get_all_users()
#     return users


# @router.get(
#     "/active",
#     response_model=list[UserRead],
#     status_code=status.HTTP_200_OK,
# )
# @inject
# async def get_all_active_users(
#     user_service: DepsUserService,
# ) -> list[UserRead]:
#     """Получаем всех активных пользователей."""
#     active_users = await user_service.get_all_active_users()
#     return active_users
