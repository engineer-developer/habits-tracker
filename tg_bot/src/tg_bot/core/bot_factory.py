"""Модуль инициализации бота."""

from telebot import StateMemoryStorage, TeleBot
from telebot.types import BotCommand

from core.config import get_settings

settings = get_settings()
storage = StateMemoryStorage()


bot = TeleBot(token=settings.bot_token, state_storage=storage)
bot.set_my_commands([BotCommand("start", "Начнем работу")])
