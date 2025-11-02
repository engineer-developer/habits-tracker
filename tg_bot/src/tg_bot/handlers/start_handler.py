"""Модуль обработки команд направленных боту."""

import requests
from pydantic import ValidationError
from requests.exceptions import ConnectTimeout
from requests.status_codes import codes
from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from tg_bot.api_requests.request_session_factory import RequestSession
from tg_bot.core.config import Settings
from tg_bot.keyboards import kb_factory
from tg_bot.schemas.user_schema import UserLoginSchema, UserRegisterSchema
from tg_bot.services.logging_services import logger
from tg_bot.services.redis_services import redis_service
from tg_bot.states.states import AuthStates


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Регистрируем обработчики команд."""

    @bot.message_handler(commands=["start"])
    def process_start(message: Message) -> None:
        """Обработчик команды '/start'."""
        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)

        token = redis_service.load_user_data(message.from_user.id, "token")
        if not token:
            logger.debug("Токен аутентификации отсутствует.")
            msg_text = (
                f"Приветствую {message.from_user.first_name}.\n\n"
                f"Вы не аутентифицированы.\n"
                f"Пожалуйста войдите в систему или зарегистрируйтесь."
            )
            bot.reply_to(
                message=message,
                text=msg_text,
                reply_markup=kb_factory.kb_login_or_register(),
            )
            return

        request_session = RequestSession(token=token)
        url = settings.api_url + "users/profile/"
        try:
            response = request_session.get(url)

            if response.status_code == codes.OK:
                logger.debug("Пользователь вошел в профиль.")
                bot.send_message(
                    chat_id=message.chat.id,
                    text="🏠 Добро пожаловать в личный кабинет",
                    reply_markup=kb_factory.kb_profile(),
                )
            elif response.status_code == codes.UNAUTHORIZED:
                logger.debug("Пользователь не аутентифицирован.")
                bot.reply_to(
                    message,
                    f"Приветствую {message.from_user.first_name}.\n\n"
                    f"Вы не аутентифицированы.\n\nПожалуйста войдите в систему "
                    f"или зарегистрируйтесь.",
                    reply_markup=kb_factory.kb_login_or_register(),
                )
            elif (
                response.status_code == codes.NOT_FOUND
                and response.json().get("detail") == "Пользователь не найден."
            ):
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Вы не зарегистрированы.",
                    reply_markup=kb_factory.kb_register(),
                )
            else:
                logger.error("Ошибка: {}: {}", response.status_code, response.text)
                bot.reply_to(message, "Не удалось получить сведения.")

        except ConnectTimeout as exc:
            logger.error("Ошибка соединения: {}", exc)

    @bot.callback_query_handler(func=lambda callback: callback.data == "cb_login")
    def process_login(callback: CallbackQuery) -> None:
        """Функция обработки callback 'cb_login'."""
        bot.set_state(
            user_id=callback.from_user.id,
            state=AuthStates.wait_password_for_login,
            chat_id=callback.message.chat.id,
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Отправьте пароль для входа.",
        )
        bot.answer_callback_query(callback_query_id=callback.id)

    @bot.message_handler(state=AuthStates.wait_password_for_login)
    def get_password_and_login(message: Message) -> None:
        """Получаем пароль и отправляем запрос на бэкэнд для входа в систему."""
        password = message.text

        user_schema = UserLoginSchema(
            username=str(message.from_user.id),
            password=password,
        )
        url = settings.api_url + "auth/login/"

        try:
            response = requests.post(url=url, data=user_schema.model_dump())

            if response.status_code == codes.OK:
                token = response.json().get("access_token")

                redis_service.save_user_data(message.from_user.id, "token", token)
                logger.debug("Пользователь вошел в систему.")

                bot.send_message(
                    chat_id=message.chat.id,
                    text="🏠 Добро пожаловать в личный кабинет",
                    reply_markup=kb_factory.kb_profile(),
                )
            elif (
                response.status_code == codes.NOT_FOUND
                and response.json().get("detail") == "Пользователь не зарегистрирован."
            ):
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Вы не зарегистрированы.",
                    reply_markup=kb_factory.kb_register(),
                )
            elif (
                response.status_code == codes.UNAUTHORIZED
                and response.json().get("detail") == "Неверные пользователь или пароль."
            ):
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Неверный пароль.",
                    reply_markup=kb_factory.kb_login(),
                )
            else:
                logger.error("{}: {}", response.status_code, response.text)
                bot.send_message(
                    chat_id=message.chat.id,
                    text="Не удалось войти.",
                    reply_markup=kb_factory.kb_start(),
                )

        except ValidationError as exc:
            logger.error(exc.errors())
        except ConnectTimeout as exc:
            logger.error(exc)
            bot.send_message(chat_id=message.chat.id, text="Ошибка соединения.")
        finally:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            bot.delete_state(message.from_user.id, message.chat.id)

    @bot.callback_query_handler(func=lambda callback: callback.data == "cb_register")
    def process_register(callback: CallbackQuery) -> None:
        """Функция обработки callback cb_register."""
        bot.set_state(
            user_id=callback.from_user.id,
            state=AuthStates.wait_password_for_register,
            chat_id=callback.message.chat.id,
        )
        bot.send_message(
            chat_id=callback.message.chat.id,
            text="Отправьте пароль для регистрации.",
        )
        bot.answer_callback_query(callback_query_id=callback.id)

    @bot.message_handler(state=AuthStates.wait_password_for_register)
    def get_password_and_register(message: Message) -> None:
        """Получаем пароль и отправляем запрос на бэкэнд для регистрации."""
        password = message.text
        user = message.from_user

        user_schema = UserRegisterSchema(
            password=password,
            telegram_id=user.id,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
        )

        redis_service.delete_user_data(message.from_user.id, "token")

        url = settings.api_url + "auth/register/"
        try:
            response = requests.post(url=url, json=user_schema.model_dump())

            if response.status_code == codes.OK:
                token = response.json().get("access_token")
                redis_service.save_user_data(message.from_user.id, "token", token)

                bot.send_message(
                    chat_id=message.chat.id,
                    text="🏠 Добро пожаловать в личный кабинет",
                    reply_markup=kb_factory.kb_profile(),
                )
                logger.debug("Пользователь вошел в систему.")
            else:
                bot.send_message(chat_id=message.chat.id, text="Ошибка регистрации.")

        except ValidationError as exc:
            logger.error(exc.errors())
        except ConnectTimeout as exc:
            logger.error(exc)
            bot.send_message(chat_id=message.chat.id, text="Ошибка соединения.")
        finally:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
