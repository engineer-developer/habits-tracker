from http.client import responses
from typing import Optional

import httpx
from httpx import codes

from tg_bot.schemas.auth import TokenDto
from tg_bot.schemas.base import BaseDtoModel
from tg_bot.schemas.users import UserCredentials, UserCreateCommand, UserRead


class ApiService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.base_url = self.client.base_url

    async def _make_request_for_auth(
        self, url: str, body_data: BaseDtoModel
    ) -> Optional[str]:
        """Отправляет запрос для получения access-token."""
        response = await self.client.post(url, json=body_data.model_dump())
        if response.status_code == codes.OK:
            payload = TokenDto.model_validate(response.json())
            token = payload.access_token
            return token

    async def register(self, cmd: UserCreateCommand) -> Optional[str]:
        """Отправляет запрос для регистрации пользователя."""
        url = f"{self.base_url}auth/register"
        return await self._make_request_for_auth(url, cmd)

    async def login(self, credentials: UserCredentials) -> Optional[str]:
        """Отправляет запрос для входа в систему."""
        url = f"{self.base_url}auth/login"
        return await self._make_request_for_auth(url, credentials)

    async def get_user_profile(self, token: str) -> Optional[UserRead]:
        url = f"{self.base_url}users/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.get(url, headers=headers)
        if response.status_code == codes.OK:
            user = UserRead.model_validate(response.json())
            return user
