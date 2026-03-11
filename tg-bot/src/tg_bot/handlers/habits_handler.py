"""Модуль обработки сообщений и callbacks о привычках."""

import datetime

from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from configs import get_settings
from keyboards import kb_factory
from keyboards.kb_factory import kb_habit_add_or_cancel, kb_habits_list
from schemas.habits import HabitDataDto
from services.logging_service import logger
from services.message_service import send_notice
from services.notify_service import habit_notify_service
from services.redis_service import redis_service
from services.request_service import requests_service, TokenAuthSessionStrategy
from states.states import HabitAddStates


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Регистрируем обработчики команд."""

    @bot.callback_query_handler(
        func=lambda callback: callback.data == "menu_habits_list"
    )
    def get_all_habits(callback: CallbackQuery) -> None:
        """Обработчик callback для получения всех привычек пользователя."""
        token = redis_service.load_user_data(user_id=callback.from_user.id, key="token")
        requests_service.strategy = TokenAuthSessionStrategy(token=token)
        habits_info: list[dict] = requests_service.get_all_habits_info()
        if habits_info:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text="Вырабатываем привычки:",
                reply_markup=kb_habits_list(habits_info),
            )
        else:
            bot.send_message(
                chat_id=callback.message.chat.id,
                text="Пока нет привычек для привития.",
            )

