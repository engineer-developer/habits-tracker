"""Модуль состояний."""

from aiogram.fsm.state import StatesGroup, State


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
