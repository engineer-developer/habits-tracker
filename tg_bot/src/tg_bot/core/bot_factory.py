"""Модуль инициализации бота."""

from states.states import state_storage
from telebot import TeleBot
from telebot.types import BotCommand

from core.config import get_settings

settings = get_settings()

bot = TeleBot(token=settings.bot_token, state_storage=state_storage)
bot.set_my_commands([BotCommand("start", "Начнем работу")])
