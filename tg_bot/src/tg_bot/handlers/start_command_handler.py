"""Модуль обработки команд направленных боту."""

from dataclasses import dataclass
from typing import Optional

from api_requests.funcs import get_request_session_with_headers
from core.config import Settings
from core.loguru_config import logger
from keyboards import kb_factory
from requests import Response
from requests.exceptions import ConnectTimeout, ConnectionError
from requests.status_codes import codes
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, Message


@dataclass
class Answer:
    """Класс ответа"""

    text: str
    keyboard: InlineKeyboardMarkup

@dataclass
class AnswerProcessor:
    """Класс подготовки ответа."""

def register_command_handlers(bot: TeleBot, settings: Settings) -> None:
    handlers: dict[str, Callable] | None = None

    def __post_init__(self) -> None:
        """Инициализируем словарь после создания экземпляра."""
        if self.handlers is None:
            self.handlers = {
                "not_registered": self._handle_not_registered,
                "not_logged_in": self._handle_not_logged_in,
                "logged": self._handle_logged,
            }

    def prepare_answer(self, user_status: str) -> Answer:
        """Выбор метода обработки на основе статуса пользователя."""
        handler = self.handlers.get(user_status, self._handle_unknown)
        answer: Answer = handler()
        return answer

    def _handle_not_registered(self) -> Answer:
        return Answer("Пожалуйста зарегистрируйтесь.", kb_factory.kb_register)

    def _handle_not_logged_in(self) -> Answer:
        return Answer("Войдите в систему.", kb_factory.kb_login)

    def _handle_logged(self) -> Answer:
        return Answer("Войдите в личный кабинет.", kb_factory.kb_personal_account)

    def _handle_unknown(self) -> Answer:
        logger.error("Не найден обработчик для полученного статуса пользователя.")
        return Answer("Непредвиденная ошибка.", None)


    """Регистрируем обработчики команд."""

    @bot.message_handler(commands=["start"])
    def process_start(message: Message) -> None:
        """Обработчик команды "start".

        Направляет http-запрос на бэкэнд для аутентификации пользователя.
        """
        request_session = get_request_session_with_headers(
            telegram_id=message.from_user.id
        )
        url = settings.api_url + "auth/"

        try:
            response = request_session.get(url)

            if response.status_code == codes.OK:
                user_status = get_user_status(response=response)
                answer = prepare_answer(user_status=user_status)
                msg: Message = bot.send_message(
                    message.chat.id,
                    f"Приветствую {message.from_user.first_name}.\n" + answer.text,
                    reply_markup=answer.keyboard,
                )
                logger.debug("Бот отправил сообщение с id {}.", msg.message_id)
            else:
                logger.error("Ответ с кодом {}", response.status_code)
                bot.reply_to(message, "Не удалось получить сведения.")

        except ConnectTimeout as exc:
            logger.error("Ошибка соединения: {}", exc)
        except ConnectionError as exc:
            logger.error("Невозможно установить соединение - {}.", exc.__class__.__name__)


    def get_user_status(response: Response) -> Optional[str]:
        """Получаем статус пользователя из http-ответа."""
        response_data = response.json()
        # TODO: сделать user_status объектом класса с валидацией.
        user_status = response_data.get("user_status")
        logger.debug("user status: {}", user_status)
        return user_status

    def prepare_answer(user_status: str | None) -> Answer:
        """Возвращаем ответ с текстом сообщения и клавиатурой.

        Возвращаемые значения зависят от user_status.
        """
        if user_status and user_status == "not registered":
            answer_text = "Пожалуйста зарегистрируйтесь."
            answer_keyboard = kb_factory.register_kb

        elif user_status and user_status == "not logged in":
            answer_text = "Войдите в систему."
            answer_keyboard = kb_factory.login_kb

        elif user_status and user_status == "logged":
            answer_text = "Войдите в личный кабинет."
            answer_keyboard = kb_factory.personal_account_kb

        else:
            answer_text = "Непредвиденная ошибка."
            answer_keyboard = None

        answer = Answer(answer_text, answer_keyboard)
        logger.debug("answer: {}", answer.text)
        return answer
