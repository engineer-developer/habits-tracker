"""Модуль генерации keyboards."""

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_kb(text: str, callback_data: str) -> InlineKeyboardMarkup:
    """Получаем стартовую клавиатуру."""
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=text, callback_data=callback_data)
    markup.add(button)
    return markup


kb_personal_account = get_start_kb(
    text="Личный кабинет",
    callback_data="cb_personal_account",
)
kb_login = get_start_kb(
    text="Войти",
    callback_data="cb_login",
)
kb_register = get_start_kb(
    text="Зарегистрироваться",
    callback_data="cb_register",
)
