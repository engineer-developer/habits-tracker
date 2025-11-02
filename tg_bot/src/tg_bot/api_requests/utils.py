"""Модуль запросов к бэкэнду."""

from pydantic import ValidationError
from requests import RequestException

from tg_bot.api_requests.request_session_factory import RequestSession
from tg_bot.core.config import settings
from tg_bot.services.logging_services import logger





# def get_habit_info(user_id: int, name: str) -> bool | dict:
#     """Получаем данные привычки из бэкэнда."""
#     token = load_user_data(user_id, "token")
#
#     if not token:
#         logger.error("Токен не найден.")
#         raise KeyError("Token not found.")
#
#     req_session = RequestSession(token=token)
#     url = settings.api_url + f"habits/{name}/"
#
#     try:
#         response = req_session.get(url=url)
#         response.raise_for_status()
#         logger.debug("Данные привычки получены.")
#         data: dict = response.json()
#         return data
#     except RequestException as exc:
#         logger.error(exc)
#         return False
