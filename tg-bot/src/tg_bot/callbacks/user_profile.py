

import enum

from aiogram.filters.callback_data import CallbackData


class ProfileAction(str, enum.Enum):
    add_habit = "➕ Добавить привычку"
    non_completed_habits = "📃 Активные привычки"
    completed_habits = "🏁 Завершенные привычки"


class ProfileMenuCallback(CallbackData, prefix="profile_menu"):
    action: ProfileAction
