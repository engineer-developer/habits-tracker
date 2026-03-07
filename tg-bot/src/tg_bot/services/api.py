from datetime import datetime, time
import functools
import json
from typing import Optional, Callable

import httpx
from httpx import HTTPStatusError
from pydantic import ValidationError

from tg_bot.schemas.auth import TokenRead
from tg_bot.schemas.base import BaseDtoModel
from tg_bot.schemas.habits import HabitRead, HabitCreateCommand, HabitByIdQuery
from tg_bot.schemas.tracking import TrackingCreateCommand, TrackingRead
from tg_bot.schemas.users import UserCredentials, UserCreateCommand, UserRead
from tg_bot.configs.loguru_config import logger


def catch_exceptions(func: Callable):
    """Декоратор перехвата исключений."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except HTTPStatusError as exc:
            logger.error(exc)
            return
        except ValidationError as exc:
            logger.error(exc)
            return

    return wrapper


class ApiService:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.base_url = self.client.base_url

    @catch_exceptions
    async def register(self, cmd: UserCreateCommand) -> Optional[str]:
        """Запрос для регистрации пользователя."""
        url = f"{self.base_url}auth/register"
        response = await self.client.post(url=url, json=cmd.model_dump(), timeout=5)
        response.raise_for_status()
        payload = TokenRead.model_validate(response.json())
        return payload.access_token

    @catch_exceptions
    async def login(self, credentials: UserCredentials) -> Optional[str]:
        """Запрос для входа в систему."""
        url = f"{self.base_url}auth/login"
        response = await self.client.post(
            url=url, json=credentials.model_dump(), timeout=5
        )
        response.raise_for_status()
        payload = TokenRead.model_validate(response.json())
        return payload.access_token

    @catch_exceptions
    async def get_user_profile(self, token: str) -> Optional[UserRead]:
        """Запрос на получение данных пользователей."""
        url = f"{self.base_url}users/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.get(url=url, headers=headers, timeout=5)
        response.raise_for_status()
        user = UserRead.model_validate(response.json())
        return user

    @catch_exceptions
    async def habit_add(
        self, token: str, cmd: HabitCreateCommand
    ) -> Optional[HabitRead]:
        """Запрос на добавление новой привычки."""
        url = f"{self.base_url}habits"
        headers = {"Authorization": f"Bearer {token}"}
        cmd.remind_time = cmd.remind_time
        response = await self.client.post(
            url=url,
            headers=headers,
            json=cmd.model_dump(mode="json"),
            timeout=5,
        )
        response.raise_for_status()
        habit = HabitRead.model_validate(response.json())
        return habit

    @catch_exceptions
    async def get_habit_by_id(self, query: HabitByIdQuery) -> Optional[HabitRead]:
        """Запрос на получение данных привычки"""
        url = f"{self.base_url}habits/{query.id}"
        response = await self.client.get(url=url, timeout=5)
        response.raise_for_status()
        habit = HabitRead.model_validate(response.json())
        return habit

    @catch_exceptions
    async def add_tracking_of_habit(
        self, token: str, cmd: TrackingCreateCommand
    ) -> Optional[TrackingRead]:
        """Запрос на добавление отслеживания привычки."""
        url = f"{self.base_url}tracking"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.post(
            url=url,
            headers=headers,
            json=cmd.model_dump(mode="json"),
            timeout=5,
        )
        response.raise_for_status()
        tracking = TrackingRead.model_validate(response.json())
        return tracking
