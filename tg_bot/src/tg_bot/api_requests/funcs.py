"""Модуль для работы с запросами."""


from requests import Session


def get_request_session_with_headers(telegram_id: str | int) -> Session:
    """Получаем сессию запроса с заголовком, содержащим telegram_id."""
    if isinstance(telegram_id, int):
        telegram_id = str(telegram_id)

    session = Session()
    session.headers.update({"telegram_id": telegram_id})
    return session



