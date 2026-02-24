from typing import Annotated

import jwt
from dependency_injector.wiring import Provide
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from fastapi_app.configs.config import get_settings
from fastapi_app.containers.app_container import AppContainer
from fastapi_app.exceptions.auth import (
    TokenDataLoss,
    TokenExpired,
    TokenInvalid,
)
from fastapi_app.services.auth import AuthService

auth_schema = HTTPBearer()
settings = get_settings()


async def get_jwt_payload(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(auth_schema),
    ],
) -> dict | HTTPException:
    """Получаем payload из jwt-токена."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.secret_key.get_secret_value(),
            algorithms=[settings.auth.algorithm],
        )
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.InvalidTokenError as exc:
        raise TokenInvalid(detail=str(exc))

    sub = payload.get("sub")
    if sub is None:
        raise TokenDataLoss()

    return payload


async def get_current_user_telegram_id(
    payload: Annotated[dict, Depends(get_jwt_payload)],
) -> int:
    """Получаем telegram_id из sub payload jwt."""
    telegram_id = payload.get("sub")
    if isinstance(telegram_id, str) and telegram_id.isdigit():
        telegram_id = int(telegram_id)
    return telegram_id


DepsCurrentUserTelegramId = Annotated[int, Depends(get_current_user_telegram_id)]
DepsAuthService = Annotated[AuthService, Depends(Provide[AppContainer.auth_service])]
