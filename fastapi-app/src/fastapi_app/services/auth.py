from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pydantic import SecretStr

from fastapi_app.exceptions.services import InvalidPasswordException
from fastapi_app.schemas.auth import TokenDto
from fastapi_app.schemas.users import UserCreateCommand, UserCredentials
from fastapi_app.services.users import UserService

password_hash = PasswordHash.recommended()


class AuthService:
    """Сервис аутентификации."""

    def __init__(
        self,
        secret_key: SecretStr,
        algorithm: str,
        access_token_expire_minutes: int,
        user_service: UserService,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.user_service = user_service

    async def get_password_hash(self, password: str) -> str:
        """Получаем хэшированный пароль."""
        return password_hash.hash(password)

    async def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """Проверяем совпадает ли переданный открытый пароль и хэшированный пароль."""
        return password_hash.verify(plain_password, hashed_password)

    async def create_jwt_token(self, data: dict, expires_delta: timedelta) -> str:
        """Создаем jwt токен."""
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        payload = data.copy()
        payload.update({"exp": expire})
        jwt_token = jwt.encode(
            payload=payload,
            key=self.secret_key.get_secret_value(),
            algorithm=self.algorithm,
        )
        return jwt_token

    async def register_user(self, cmd: UserCreateCommand) -> TokenDto:
        """Метод регистрации пользователя."""
        hashed_password = await self.get_password_hash(cmd.password)
        cmd.password = hashed_password
        await self.user_service.add_user(cmd)

        payload = {"sub": str(cmd.telegram_id)}
        access_token = await self.create_jwt_token(
            data=payload,
            expires_delta=timedelta(minutes=self.access_token_expire_minutes),
        )
        return TokenDto(access_token=access_token)

    async def sign_in(
        self,
        credentials: UserCredentials,
    ):
        """Метод входа в систему."""
        user = await self.user_service.get_current_active_user_with_password(
            credentials.telegram_id
        )

        isvalid_password = await self.verify_password(
            credentials.password.get_secret_value(),
            user.password.get_secret_value(),
        )
        if not isvalid_password:
            raise InvalidPasswordException()

        payload = {"sub": str(credentials.telegram_id)}
        access_token = await self.create_jwt_token(
            data=payload,
            expires_delta=timedelta(minutes=self.access_token_expire_minutes),
        )
        return TokenDto(access_token=access_token)
