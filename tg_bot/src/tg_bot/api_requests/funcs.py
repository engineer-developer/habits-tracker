import requests

from core.config import get_settings, Settings

settings: Settings = get_settings()


def make_request_to_api(message, url):
    headers = {"telegram_id": str(message.from_user.id)}
    url = settings.api_url + url

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:


            response_data = response.json()





    except ConnectTimeout:
        bot.reply_to(message, "Ошибка соединения. Попробуйте еще раз.")