"""Модуль регистрации обработчиков commands, callbacks, messages."""

from tg_bot.core.config import Settings
from telebot import TeleBot

from tg_bot.handlers import start_handler, habits_handler


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Функция регистрации обработчиков."""
    start_handler.register_handlers(bot, settings)
    habits_handler.register_handlers(bot, settings)
