import enum

from aiogram.filters.callback_data import CallbackData


class ProfileAction(str, enum.Enum):
    habits_list = "📃 Список привычек"
    habit_add = "➕ Добавить привычку"
    habit_edit = "⚙ Редактировать"
    habit_delete = "❌ Удалить"
    habit_complete = "✅ Выполнить"
    habit_stat = "📊 Статистика"


class ProfileMenuCallback(CallbackData, prefix="profile_menu"):
    action: ProfileAction
