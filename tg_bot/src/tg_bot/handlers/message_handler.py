from telebot import TeleBot
from telebot.types import Message


def echo_all(message: Message, bot: TeleBot):
    bot.reply_to(message, message.text)
