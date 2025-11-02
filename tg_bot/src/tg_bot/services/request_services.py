"""Модуль взаимодействия с backend API."""

from dataclasses import dataclass
from typing import Optional

import loguru
from requests import Session
from requests.exceptions import RequestException

from tg_bot.core.config import settings
from tg_bot.schemas.habit_schema import HabitAddDto
from tg_bot.services.logging_services import logger
from tg_bot.services.redis_services import RedisService, redis_service


@dataclass
class RequestSession(Session):
    """Класс requests сессии, с возможностью добавлению jwt-токена в заголовок."""

    token: Optional[str] = None

    def __post_init__(self) -> None:
        """Логика инициализации."""
        super().__init__()
        if self.token:
            self.headers.update({"Authorization": f"Bearer {self.token}"})


@dataclass
class RequestService:
    """Сервис взаимодействия с бэкэндом."""

    api_url: str
    logger: loguru.logger
    redis_service: RedisService
    _requests_session: Optional[RequestSession] = None

    def __post_init__(self):
        """Логика инициализации."""
        self._requests_session = RequestSession()

    def set_token_to_session(self, token: str = None) -> None:
        """Добавляем auth токен в заголовок requests сессии."""
        if token:
            self._requests_session = RequestSession(token=token)
        else:
            self._requests_session = RequestSession()

    def upload_new_habit_data(self, data: HabitAddDto) -> bool:
        """Отправка данных новой привычки."""
        url = self.api_url + "habits/"

        with self._requests_session as req:
            try:
                resp = req.post(url, json=data.model_dump(mode="json"))
                resp.raise_for_status()
                self.logger.debug("Данные привычки успешно отправлены.")
                return True
            except RequestException as exc:
                self.logger.error(exc)
                return False

    def get_all_habits_info(self) -> dict | bool:
        """Получаем данные о всех привычках пользователя."""
        url = self.api_url + "habits/"

        with self._requests_session as req:
            try:
                resp = req.get(url)
                resp.raise_for_status()
                response_data = resp.json()
                self.logger.debug(
                    "Данные о всех привычках пользователя получены: {}", response_data
                )
                return response_data
            except RequestException as exc:
                self.logger.error(exc)
                return False

    def get_habit_info(self, name: str, job_id: str) -> bool | dict:
        """Получаем данные привычки из бэкэнда."""
        url = self.api_url + f"habits/{name}/reminders/{job_id}/"

        self.set_token_to_session(token=None)

        with self._requests_session as req:
            try:
                response = req.get(url=url)
                response.raise_for_status()
                data: dict = response.json()
                self.logger.debug("Данные привычки получены.")
                return data
            except RequestException as exc:
                self.logger.error("Данные о привычке не получены: {}", exc)
                return False


requests_service = RequestService(
    api_url=settings.api_url,
    logger=logger,
    redis_service=redis_service,
)
