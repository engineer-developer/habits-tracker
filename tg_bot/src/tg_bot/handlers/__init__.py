"""Модуль регистрации обработчиков commands, callbacks, messages."""

from core.config import Settings
from telebot import TeleBot

from handlers.callback_handlers import register_callback_handlers
from handlers.command_handlers import register_command_handlers
from handlers.message_handlers import register_message_handlers


def register_handlers(bot: TeleBot, settings: Settings) -> None:
    """Функция регистрации обработчиков."""
    register_command_handlers(bot, settings)
    register_callback_handlers(bot, settings)
    register_message_handlers(bot, settings)
