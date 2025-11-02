"""Модуль инициализации бота."""

from tg_bot.core.config import settings
from telebot import TeleBot, custom_filters
from telebot.types import BotCommand

from tg_bot.states.states import redis_storage


bot = TeleBot(token=settings.bot_token, state_storage=redis_storage)
bot.set_my_commands([BotCommand("start", "Начнем работу")])
bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))
