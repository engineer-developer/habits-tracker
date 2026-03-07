import enum

from aiogram.filters.callback_data import CallbackData


class HabitAction(str, enum.Enum):
    habit_edit = "⚙ Редактировать"
    habit_complete = "✅ Выполнить"


class HabitListCallback(CallbackData, prefix="habit_list"):
    action: HabitAction
    habit_id: int


class HabitAddConfirmAction(str, enum.Enum):
    add = "✅ Добавить"
    cancel = "❌ Отменить"

class HabitAddConfirmCallback(CallbackData, prefix="habit_add_confirm"):
    action: HabitAddConfirmAction


class HabitMarkCompletedAction(str, enum.Enum):
    mark_completed = "✅ Выполнить"


class HabitMarkCompletedCallback(CallbackData, prefix="habit_mark_completed"):
    action: HabitMarkCompletedAction
    habit_id: int
