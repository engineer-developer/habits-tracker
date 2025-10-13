"""Модуль генерации keyboards."""

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_kb(text: str, callback_data: str) -> InlineKeyboardMarkup:
    """Получаем стартовую клавиатуру."""
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=text, callback_data=callback_data)
    markup.add(button)
    return markup


personal_account_kb = get_start_kb("Личный кабинет", "cb_personal_account")
login_kb = get_start_kb("Войти", "cb_login")
register_kb = get_start_kb("Зарегистрироваться", "cb_register")
