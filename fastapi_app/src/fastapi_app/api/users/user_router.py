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


@router.get(
    "/",
    name="Get all users",
    description="Получение всех пользователей из БД",
    response_model=UsersListSchema,
)
async def get_all_users(
    session: CommonAsyncSession,
    is_active: Annotated[
        bool,
        Query(
            description="Параметр запроса для получения только активных пользователей"
        ),
    ] = False,
) -> UsersListSchema:
    """Представление для получения всех пользователей.

    :param session: Сессия взаимодействия с БД.
    :param is_active: Параметр запроса для получения только активных пользователей.
    :return: {"users": list[User]}
    """
    users_orm: Sequence[User] = await fetch_all_users(session, is_active=is_active)
    users_sch: list[UserOutSchema] = [
        UserOutSchema.model_validate(user) for user in users_orm
    ]
    return UsersListSchema(users=users_sch)


@router.post(
    "/",
    name="Add user",
    description="Добавление пользователя в БД",
    response_model=UserOutSchema,
    status_code=201,
    responses={400: {"description": "Ошибка добавления пользователя"}},
)
async def add_user(session: CommonAsyncSession, user: UserInSchema) -> UserOutSchema:
    """Представление для добавления нового пользователя.

    :param session: Сессия взаимодействия с БД.
    :param user: Данные пользователя.
    :return: Данные созданного пользователя.
    """
    user_orm: User = User(**user.model_dump())
    user_from_db: User = await add_user_to_db(user=user_orm, session=session)
    if not user_from_db:
        raise HTTPException(status_code=400, detail="Ошибка добавления пользователя")
    return UserOutSchema.model_validate(user_from_db)


@router.get("/profile/", response_model=UserOutSchema, status_code=200)
async def get_profile(
    user: Annotated[User, Depends(get_current_active_user)],
) -> UserOutSchema:
    """Представление для получения профиля пользователя.

    Получаем данные зарегистрированного, аутентифицированного
    и активного пользователя.
    """
    return UserOutSchema.model_validate(user)
