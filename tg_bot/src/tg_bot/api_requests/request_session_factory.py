"""Модуль для работы с запросами."""

from requests import Session


class RequestSession(Session):
    """Класс сессии requests с заголовком Authorization, содержащим jwt-токен."""

    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.headers.update({"Authorization": f"Bearer {self.token}"})
