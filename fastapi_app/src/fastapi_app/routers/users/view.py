from fastapi import HTTPException
from fastapi.responses import JSONResponse
"""Модуль представлений пользователей."""

from controllers.users.operations import add_user_to_db, fetch_all_users
from database.manager import CommonAsyncSession
from dto.schemas import UserInSchema, UserOutSchema, UsersListSchema
from fastapi.routing import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "",
    name="Get all users",
    description="Get all users from database",
    response_class=JSONResponse,
    responses={400: {"description": "No content"}},
    response_model=UsersListSchema,
    responses={404: {"description": "Users not found"}},
)
async def get_all_users(session: CommonAsyncSession) -> UsersListSchema:
    """Точка получения всех активных пользователей."""
    users_orm = await fetch_all_users(session)
    users_sch = [UserOutSchema.model_validate(user) for user in users_orm]
    return UsersListSchema(users=users_sch)


)
async def get_all_users():
    # users_dao = fetch_users_from_db()
    users = [
        {"name": "Bob"},
        {"name": "Jack"},
        {"name": "Piter"},
    ]
    content = {"users": users}
    if content:
        return JSONResponse(content)
    else:
        raise HTTPException(400, "No content")
