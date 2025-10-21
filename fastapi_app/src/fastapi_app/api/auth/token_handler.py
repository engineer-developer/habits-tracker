"""Модуль создания и проверки jwt-токенов."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from core.config import get_settings
from core.loguru_config import logger
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


auth_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login/")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаем jwt-токен."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_access_token(token: Annotated[str, Depends(auth_scheme)]) -> dict:
    """Проверяем jwt-токен.

    Возвращаем декодированные данные.

    :return: sub_data
    :rtype: dict
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub_data: dict = payload.get("sub")
        if sub_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не содержит данных.",
            )
        return sub_data

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Срок действия токена истек.",
        )
    except InvalidTokenError as exc:
        logger.error(exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не валидный токен.",
        )
