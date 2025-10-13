from requests import Response, codes
from telebot import TeleBot
from telebot.types import CallbackQuery

from api_requests.funcs import get_request_session_with_headers
from core.config import Settings


def register_callback_handlers(bot: TeleBot, settings: Settings):

    @bot.callback_query_handler(func=lambda callback: callback.data == "cb_register")
    def make_request_for_register(callback: CallbackQuery):
        request_session = get_request_session_with_headers(
            telegram_id=callback.from_user.id
        )
        url = settings.api_url + "register/"
        response: Response = request_session.get(url=url)

        if response.status_code == codes.OK:
            bot.answer_callback_query(callback_query_id=callback.id, text="Успешно зарегистрирован.")

