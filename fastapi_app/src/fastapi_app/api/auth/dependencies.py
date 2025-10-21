"""Модуль зависимостей аутентификации."""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from starlette import status

from api.auth.token_handler import verify_access_token
from core.database import CommonAsyncSession
from models.app_models import User
from services.user_service import fetch_user_by_telegram_id


async def get_current_user(
    token_data: Annotated[dict, Depends(verify_access_token)],
    session: CommonAsyncSession,
) -> Optional[User]:
    """Получаем текущего пользователя.

    :param token_data: Данные из токена аутентификации, получаемые через зависимость.
    :param session: Асинхронная сессия взаимодействия с БД.
    :return: User - пользователь на основе данных из токена.
    :rtype: User.
    :raise 400: Не найден telegram_id.
    :raise 404: Пользователь не найден.
    """
    telegram_id = token_data.get("telegram_id")

    if telegram_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Не найден telegram_id."
        )
    if isinstance(telegram_id, str) and telegram_id.isdigit():
        telegram_id = int(telegram_id)

    user = await fetch_user_by_telegram_id(
        telegram_id=telegram_id,
        session=session,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден."
        )
    return user
