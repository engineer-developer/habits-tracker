import requests
from requests.exceptions import ConnectTimeout
from telebot import TeleBot
from telebot.types import Message

from keyboards import kb_factory
from ..core.config import settings


class RequestToApiWithHeaders(requests.PreparedRequest):
    url = settings.api_url

    def post(self):
        pass


def process_start(message: Message, bot: TeleBot):
    headers = {"telegram_id": str(message.from_user.id)}
    url = settings.api_url + "main/"

    try:
        response = requests.post(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            user_status = response_data.get("user_status", None)

            if user_status and user_status == "is_logged":
                bot.send_message(
                    message.chat.id,
                    f"Приветствую {message.from_user.first_name}",
                    reply_markup=kb_factory.main_menu_kb,
                )
            elif user_status and user_status == "not_logged":
                bot.send_message()

    except ConnectTimeout:
        bot.reply_to(message, "Ошибка соединения. Попробуйте еще раз.")
