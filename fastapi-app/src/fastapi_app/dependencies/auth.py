import jwt
from dependency_injector.wiring import Provide
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from typing import Annotated
from configs.app_config import get_settings
from containers.app_container import AppContainer
from dependencies.exceptions import TokenExpired, TokenInvalid, TokenDataLoss
from services import AuthService


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
    except ExpiredSignatureError:
        raise TokenExpired()
    except InvalidTokenError as exc:
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
