import enum

from aiogram.filters.callback_data import CallbackData


class AuthMethod(str, enum.Enum):
    login = "Войти"
    register = "Зарегистрироваться"


class AuthCallback(CallbackData, prefix="auth"):
    method: AuthMethod
