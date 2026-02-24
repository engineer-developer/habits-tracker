"""Модуль роутов аутентификации."""

from dependency_injector.wiring import inject
from fastapi.routing import APIRouter

from fastapi_app.dependencies.auth import DepsAuthService
from fastapi_app.schemas.auth import TokenDto
from fastapi_app.schemas.users import UserCreateCommand, UserCredentials

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=200,
    response_model=TokenDto,
)
@inject
async def sign_up(
    cmd: UserCreateCommand,
    auth_service: DepsAuthService,
):
    """Роут для регистрации нового пользователя.

    При успешной регистрации пользователя выдается access-token.
    """
    return await auth_service.register_user(cmd)


@router.post(
    "/login",
    status_code=200,
    response_model=TokenDto,
)
@inject
async def sign_in(
    credentials: UserCredentials,
    auth_service: DepsAuthService,
) -> TokenDto:
    """Роут для входа в систему.

    При успешной аутентификации выдается access-token.
    """
    return await auth_service.sign_in(credentials)
