"""Модуль состояний."""

from telebot.states import State, StatesGroup
from telebot.storage import StateRedisStorage

from tg_bot.core.config import settings


class AuthStates(StatesGroup):
    """Состояния аутентификации."""

    wait_password_for_register = State()
    wait_password_for_login = State()


class HabitAddStates(StatesGroup):
    """Состояния добавления привычки."""

    wait_for_habit_name = State()
    wait_for_habit_description = State()
    wait_for_habit_remind_time = State()
    wait_for_habit_remind_quantity = State()



