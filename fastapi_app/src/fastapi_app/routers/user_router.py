"""Модуль представлений пользователей."""

from typing import Sequence

from core.database import CommonAsyncSession
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from models.user_model import User
from schemas.user_schema import UserInSchema, UserOutSchema, UsersListSchema
from services.user_service import add_user_to_db, fetch_all_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    name="Get all users",
    description="Get all users from database",
    response_model=UsersListSchema,
    responses={404: {"description": "Users not found"}},
)
async def get_all_users(session: CommonAsyncSession) -> UsersListSchema:
    """Представление для получения всех активных пользователей."""
    users_orm: Sequence[User] = await fetch_all_users(session)
    users_sch: list[UserOutSchema] = [
        UserOutSchema.model_validate(user) for user in users_orm
    ]
    return UsersListSchema(users=users_sch)


@router.post(
    "/",
    name="Add user",
    description="Add user to database",
    response_model=UserOutSchema,
    status_code=201,
    responses={400: {"description": "Ошибка добавления пользователя"}},
)
async def add_user(user: UserInSchema, session: CommonAsyncSession) -> UserOutSchema:
    """Представление для добавления нового пользователя."""
    user_orm: User = User(**user.model_dump())
    user_from_db: User = await add_user_to_db(user=user_orm, session=session)

    if not user_from_db:
        raise HTTPException(status_code=400, detail="Ошибка добавления пользователя")

    return UserOutSchema.model_validate(user_from_db)
