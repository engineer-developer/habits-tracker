"""Модуль представлений пользователей."""

from controllers.users.operations import add_user_to_db, fetch_all_users
from dao.models import User
from database.manager import CommonAsyncSession
from dto.schemas import UserInSchema, UserOutSchema, UsersListSchema
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    name="Get all users",
    description="Get all users from database",
    response_model=UsersListSchema,
    responses={404: {"description": "Users not found"}},
)
async def get_all_users(session: CommonAsyncSession) -> UsersListSchema:
    """Точка получения всех активных пользователей."""
    users_orm = await fetch_all_users(session)
    users_sch = [UserOutSchema.model_validate(user) for user in users_orm]
    return UsersListSchema(users=users_sch)


@router.post(
    "",
    name="Add user",
    description="Add user to database",
    response_model=UserOutSchema,
    status_code=201,
    responses={
        403: {
            "description": "Ошибка уникальности пользователя",
            "content": {"application/json": {"example": {"detail": "string"}}},
        }
    },
)
async def add_user(user: UserInSchema, session: CommonAsyncSession) -> UserOutSchema:
    """Точка добавления пользователя."""
    user_orm = User(**user.model_dump())
    user_from_db = await add_user_to_db(user=user_orm, session=session)

    if user_from_db and isinstance(user_from_db, User):
        return UserOutSchema.model_validate(user_from_db)
    elif user_from_db and isinstance(user_from_db, IntegrityError):
        raise HTTPException(
            status_code=403,
            detail=f"Пользователь с telegram_id {user.telegram_id} уже есть.",
        )
    else:
        raise HTTPException(status_code=400, detail="Bad request")
