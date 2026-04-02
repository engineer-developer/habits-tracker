import functools
from typing import Any, Callable, Coroutine, Optional

import httpx
from httpx import HTTPStatusError
from pydantic import ValidationError
from pydantic.v1 import PositiveInt

from tg_bot import schemas
from tg_bot.configs.loguru_config import logger
from tg_bot.schemas import HabitRead


def catch_exceptions(func: Callable):
    """Декоратор перехвата исключений."""

    @functools.wraps(func)
    async def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as exc:
            logger.error(exc)
            return None
        except ValidationError as exc:
            logger.error(exc)
            return None

    return wrapper


class ApiService:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.base_url = self.client.base_url

    @catch_exceptions
    async def register(self, cmd: schemas.UserCreateCommand) -> Optional[str]:
        """Запрос для регистрации пользователя."""
        url = f"{self.base_url}auth/register"
        response = await self.client.post(url=url, json=cmd.model_dump(), timeout=5)
        response.raise_for_status()
        payload = schemas.TokenRead.model_validate(response.json())
        return payload.access_token

    @catch_exceptions
    async def login(self, credentials: schemas.UserCredentials) -> Optional[str]:
        """Запрос для входа в систему."""
        url = f"{self.base_url}auth/login"
        response = await self.client.post(
            url=url, json=credentials.model_dump(), timeout=5
        )
        response.raise_for_status()
        payload = schemas.TokenRead.model_validate(response.json())
        return payload.access_token

    @catch_exceptions
    async def get_user_profile(self, token: str) -> Optional[schemas.UserRead]:
        """Запрос на получение данных пользователей."""
        url = f"{self.base_url}users/profile"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.get(url=url, headers=headers, timeout=5)
        response.raise_for_status()
        user = schemas.UserRead.model_validate(response.json())

        if not user:
            logger.error("Данные пользователя не получены.")
            return None

        return user

    @catch_exceptions
    async def create_habit(
        self, token: str, cmd: schemas.HabitCreateCommand
    ) -> Optional[schemas.HabitRead]:
        """Запрос на добавление новой привычки."""
        url = f"{self.base_url}habits"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.post(
            url=url,
            headers=headers,
            json=cmd.model_dump(mode="json"),
            timeout=5,
        )
        response.raise_for_status()
        habit = schemas.HabitRead.model_validate(response.json())
        if not habit:
            return None
        return habit

    @catch_exceptions
    async def get_habit_by_id(
        self, query: schemas.HabitByIdQuery
    ) -> Optional[schemas.HabitRead]:
        """Запрос на получение данных привычки"""
        url = f"{self.base_url}habits/{query.id}"
        response = await self.client.get(url=url, timeout=5)
        response.raise_for_status()
        habit = schemas.HabitRead.model_validate(response.json())
        if not habit:
            logger.error(f"Привычки с id={query.id} не найдено")
            return None
        return habit

    @catch_exceptions
    async def add_tracking_of_habit(
        self, token: str, cmd: schemas.TrackingCreateCommand
    ) -> Optional[schemas.TrackingRead]:
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
        tracking = schemas.TrackingRead.model_validate(response.json())
        return tracking

    @catch_exceptions
    async def get_habits(
        self, token: str, completed: bool = False
    ) -> Optional[list[HabitRead]]:
        """Получает привычки.

        :param token: Токен аутентификации.
        :param completed: Статус завершенности привычки.
        """
        url = f"{self.base_url}habits"
        params = dict(completed=completed)
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.get(
            url=url, params=params, headers=headers, timeout=5
        )
        response.raise_for_status()
        habits = [schemas.HabitRead.model_validate(habit) for habit in response.json()]
        return habits

    async def get_non_completed_habits(self, token: str) -> Optional[list[HabitRead]]:
        """Получает активные привычки."""
        return await self.get_habits(token=token, completed=False)

    async def get_completed_habits(self, token: str) -> Optional[list[HabitRead]]:
        """Получает завершенные привычки."""
        return await self.get_habits(token=token, completed=True)

    @catch_exceptions
    async def update_habit(
        self,
        token: str,
        habit_id: PositiveInt,
        cmd: schemas.HabitUpdateCommand,
    ) -> Optional[HabitRead]:
        url = f"{self.base_url}habits/{habit_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.patch(
            url=url,
            headers=headers,
            json=cmd.model_dump(exclude_unset=True, mode="json"),
            timeout=5,
        )
        response.raise_for_status()
        habit = schemas.HabitRead.model_validate(response.json())
        return habit

    @catch_exceptions
    async def delete_habit(
        self, token: str, cmd: schemas.HabitDeleteCommand
    ) -> Optional[HabitRead]:
        url = f"{self.base_url}habits/{cmd.id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.delete(
            url=url,
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()
        habit = HabitRead.model_validate(response.json())
        if not habit:
            return None
        return habit

    @catch_exceptions
    async def delete_completed_habits(self, token: str) -> None:
        url = f"{self.base_url}habits/completed"
        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.delete(
            url=url,
            headers=headers,
            timeout=5,
        )
        response.raise_for_status()
        result = response.json()
        deleted_habits_ids = result.get("habits_ids")
        logger.debug(f"Удалено завершенных привычек: {len(deleted_habits_ids)}")
