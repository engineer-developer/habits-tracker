import enum

from aiogram.filters.callback_data import CallbackData


class HabitAction(str, enum.Enum):
    habit_complete = "✅ Выполнить"
    habit_edit = "⚙ Редактировать"
    habit_stat = "📃 Статистика"
    habit_delete = "❌ Удалить"

class HabitDetailsCallback(CallbackData, prefix="habit_details"):
    action: HabitAction
    habit_id: int


class HabitListCallback(CallbackData, prefix="habit_list"):
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


# class HabitsListCallback(CallbackData, prefix="habit")
