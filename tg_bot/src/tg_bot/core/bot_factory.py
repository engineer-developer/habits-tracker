"""Модуль инициализации бота."""

from telebot import TeleBot, custom_filters
from telebot.storage import StateRedisStorage
from telebot.types import BotCommand

from tg_bot.core.config import settings


redis_storage = StateRedisStorage(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
)

bot = TeleBot(token=settings.bot_token, state_storage=redis_storage)
bot.set_my_commands([BotCommand("start", "Профиль пользователя")])
bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot))
