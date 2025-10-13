"""Модуль обработки callback."""

from core.config import Settings
from states.states import AuthStates
from telebot import TeleBot
from telebot.types import CallbackQuery


def register_callback_handlers(bot: TeleBot, settings: Settings) -> None:
    """Функция регистрации обработчиков callback."""

    @bot.callback_query_handler(func=lambda callback: callback.data == "cb_register")
    def query_password_for_register(callback: CallbackQuery) -> None:
        """Функция обработки callback cb_register."""
        user_id = callback.from_user.id
        chat_id = callback.message.chat.id
        bot.set_state(user_id=user_id, chat_id=chat_id, state=AuthStates.wait_password)
        bot.send_message(
            chat_id=callback.message.chat.id, text="Отправьте пароль для регистрации."
        )
        bot.answer_callback_query(callback_query_id=callback.id)
