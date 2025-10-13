"""Модуль обработки сообщений."""

from api_requests.funcs import get_request_session_with_headers
from core.config import Settings
from core.loguru_config import logger
from keyboards.kb_factory import login_kb
from requests import ConnectTimeout, codes
from states.states import AuthStates
from telebot import TeleBot
from telebot.types import Message


def register_message_handlers(bot: TeleBot, settings: Settings) -> None:
    """Функция регистрации обработчиков сообщений."""

    @bot.message_handler(state=AuthStates.wait_password, content_types=["text"])
    def get_password_and_register(message: Message) -> None:
        """Получаем пароль и отправляем запрос на бэкэнд для регистрации."""
        chat_id = message.chat.id
        password = message.text
        logger.debug("Get password: {}", password)

        url = settings.api_url + "auth/register/"
        data = {"telegram_id": message.from_user.id, "password": password}
        request_session = get_request_session_with_headers(
            telegram_id=message.from_user.id
        )

        try:
            response = request_session.post(url=url, json=data)

            if response.status_code == codes.OK:
                bot.send_message(
                    chat_id=chat_id,
                    text="Войдите в личный кабинет.",
                    reply_markup=login_kb,
                )
            else:
                bot.send_message(chat_id=chat_id, text="Не удалось зарегистрироваться.")

        except ConnectTimeout:
            bot.send_message(
                chat_id=chat_id, text="Ошибка соединения. Попробуйте еще раз."
            )
        finally:
            bot.delete_message(chat_id=chat_id, message_id=message.id)
