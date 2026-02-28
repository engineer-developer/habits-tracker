"""Модуль взаимодействия с backend API."""

from abc import ABC, abstractmethod
from typing import Optional

import loguru
import requests
from requests import Response
from requests.exceptions import RequestException

from configs import settings
from schemas.habits import HabitAddDto
from services.logging_service import logger


class SessionStrategy(ABC):
    """Абстрактная стратегия создания сессии."""

    @abstractmethod
    def create_session(self) -> requests.Session:
        pass


class NoAuthSessionStrategy(SessionStrategy):
    """Стратегия создания обычной request сессии."""

    def create_session(self) -> requests.Session:
        """Создание сессии."""
        return requests.Session()


class TokenAuthSessionStrategy(SessionStrategy):
    """Стратегия создания сессии, с jwt токеном в заголовке."""

    def __init__(self, token: str) -> None:
        """Логика инициализации."""
        self.token = token

    def create_session(self) -> requests.Session:
        """Создание сессии."""
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {self.token}"})
        return session


class RequestService:
    """Сервис взаимодействия с бэкэндом."""

    def __init__(self, api_url: str, logger: loguru.logger) -> None:
        """Логика инициализации."""
        self.api_url = api_url
        self.logger = logger
        self._session_strategy = NoAuthSessionStrategy()
        self._requests_session = self._session_strategy.create_session()

    @property
    def strategy(self) -> SessionStrategy:
        """Геттер _session_strategy."""
        return self._session_strategy

    @strategy.setter
    def strategy(self, new_strategy: SessionStrategy) -> None:
        """Сеттер _session_strategy."""
        self._session_strategy = new_strategy
        self._requests_session.close()
        self._requests_session = self._session_strategy.create_session()

    def close_session(self) -> None:
        """Закрываем сессию."""
        self._requests_session.close()

    def get_user_profile(self) -> Response | None:
        """Получаем доступ к личному кабинету пользователя."""
        url = self.api_url + "users/profile/"

        with self._requests_session as req:
            try:
                response = req.get(url)
                return response
            except RequestException as exc:
                self.logger.error(exc)

    def upload_new_habit_data(self, data: HabitAddDto) -> Optional[dict]:
        """Отправка данных новой привычки."""
        url = self.api_url + "habits/"

        with self._requests_session as req:
            try:
                response = req.post(url, json=data.model_dump(mode="json"))
                response.raise_for_status()
                self.logger.debug("Данные привычки успешно отправлены.")
                return response.json()
            except RequestException as exc:
                self.logger.error(exc)
                return None

    def get_all_habits_info(self) -> dict | bool:
        """Получаем данные о всех привычках пользователя."""
        url = self.api_url + "habits/"

        with self._requests_session as req:
            try:
                response = req.get(url)
                response.raise_for_status()
                response_data = response.json()
                self.logger.debug(
                    "Данные о всех привычках пользователя получены: {}",
                    response_data,
                )
                return response_data
            except RequestException as exc:
                self.logger.error(exc)
                return False

    def get_habit_info(self, name: str, job_id: str) -> bool | dict:
        """Получаем данные привычки из бэкэнда."""
        url = self.api_url + f"habits/{name}/reminders/{job_id}/"

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

    def upload_habit_confirm_data(self, data: dict) -> bool:
        """Отправляем данные о выполнении привычки."""
        url = self.api_url + "habits/confirm_completed/"

        with self._requests_session as req:
            try:
                response = req.post(url=url, json=data)
                response.raise_for_status()
                self.logger.debug("Данные о выполнении привычки отправлены.")
                return True
            except RequestException as exc:
                self.logger.error(
                    "Данные о выполнении привычки не отправлены: {}",
                    exc,
                )
                return False
            except TypeError as exc:
                self.logger.error("{}", exc)
                return False


requests_service = RequestService(api_url=settings.api_url, logger=logger)
