from telebot import TeleBot
from telebot.types import BotCommand
from .config import settings


bot = TeleBot(token=settings.bot_token, parse_mode=None)
bot.set_my_commands([BotCommand("start", "Начнем работу")])
