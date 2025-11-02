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
EXPIRE_TIME = settings.access_token_expire_minutes


auth_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login/")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаем jwt-токен."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_TIME)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_access_token(token: Annotated[str, Depends(auth_scheme)]) -> str:
    """Проверяем jwt-токен.

    Возвращаем декодированные данные.

    :return: Данные, ранее помещенные в "sub", в данном проекте значение 'telegram_id'.
    :rtype: String.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug("payload: {}", payload)

        sub_data: str = payload.get("sub")
        if sub_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не содержит данных.",
            )
        logger.debug("sub_data: {}", sub_data)
        return sub_data

    except ExpiredSignatureError:
        logger.error("Срок действия токена истек")
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
