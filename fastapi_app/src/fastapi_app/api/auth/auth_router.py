"""Модуль представлений аутентификации."""

from typing import Optional

from core.database import CommonAsyncSession
from core.loguru_config import logger
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from models.app_models import User
from pydantic import ValidationError
from schemas.auth_schema import Token
from schemas.user_schema import UserInSchema
from services.user_service import add_user_to_db, fetch_user_by_telegram_id

from api.auth.password_handler import verify_password
from api.auth.token_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/", response_model=Token)
async def login(
    session: CommonAsyncSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Представление аутентификации пользователя.

    Представляет собой реализацию входа пользователя в систему.

    form_data принимает 'username' и 'password' переданные в body
    в виде 'application/x-www-form-urlencoded'
    и выдает jwt-токен для последующей аутентификации.

    OAuth2PasswordRequestForm требует обязательного указания 'username' и 'password'.
    При взаимодействии с telegram ботом 'username' = 'user.id'.
    """
    telegram_id = form_data.username
    password = form_data.password

    if not telegram_id.isdigit():
        logger.error("'username' должен содержать только цифры.")
        raise HTTPException(403, "'username' должен содержать только цифры.")

    user: User = await fetch_user_by_telegram_id(
        session=session, telegram_id=int(telegram_id)
    )
    if not user:
        logger.error("Пользователь не найден.")
        raise HTTPException(404, "Пользователь не зарегистрирован.")

    is_valid_password = await verify_password(
        plain_password=password, hashed_password=user.password
    )
    if not is_valid_password:
        logger.error("Неверный пароль.")
        raise HTTPException(401, "Неверные пользователь или пароль.")

    data = {"sub": str(user.telegram_id)}
    jwt_token = create_access_token(data=data)
    access_token = Token(access_token=jwt_token, token_type="Bearer")
    return access_token


@router.post("/register/", status_code=200, response_model=Token)
async def register_user(user: UserInSchema, session: CommonAsyncSession) -> Token:
    """Представление регистрации пользователя."""
    user_orm = await fetch_user_by_telegram_id(
        session=session, telegram_id=user.telegram_id
    )
    if user_orm:
        raise HTTPException(403, "Такой пользователь уже зарегистрирован.")

    try:
        user_orm = User(**user.model_dump())
    except ValidationError as exc:
        logger.error(exc.errors())
        raise HTTPException(status_code=400, detail="Ошибка добавления пользователя.")

    user_from_db: Optional[User] = await add_user_to_db(session=session, user=user_orm)
    if not user_from_db:
        raise HTTPException(status_code=400, detail="Ошибка добавления пользователя.")

    data = {"sub": str(user_from_db.telegram_id)}
    jwt_token = create_access_token(data=data)
    access_token = Token(access_token=jwt_token, token_type="Bearer")
    return access_token
