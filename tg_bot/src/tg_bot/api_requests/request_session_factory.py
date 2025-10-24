"""Модуль для работы с запросами."""

from requests import Session


def get_request_session(token: str | int) -> Session:
    """Получаем сессию запроса с заголовком Authorization, содержащим jwt-токен."""
    if isinstance(token, int):
        token = str(token)

    session = Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session
