import enum

from aiogram.filters.callback_data import CallbackData


class HabitDetailsAction(str, enum.Enum):
    habit_complete = "✅ Выполнить"
    habit_edit = "⚙ Редактировать"
    habit_delete = "❌ Удалить"


class HabitDetailsActionCallback(CallbackData, prefix="habit_details_action"):
    action: HabitDetailsAction
    habit_id: int


class HabitEditAction(str, enum.Enum):
    habit_title = "Название"
    habit_description = "Описание"
    remind_time = "Время напоминания"
    remind_quantity = "Количество напоминаний"


class HabitEditActionCallback(CallbackData, prefix="habit_edit_action"):
    action: HabitEditAction
    habit_id: int


class HabitIdCallback(CallbackData, prefix="habit_id"):
    habit_id: int


class HabitAddConfirmAction(str, enum.Enum):
    add = "✅ Добавить"
    cancel = "❌ Отменить"


class HabitAddConfirmActionCallback(CallbackData, prefix="habit_add_confirm"):
    action: HabitAddConfirmAction


class HabitMarkCompletedAction(str, enum.Enum):
    mark_completed = "✅ Выполнить"


class HabitMarkCompletedCallback(CallbackData, prefix="habit_mark_completed"):
    action: HabitMarkCompletedAction
    habit_id: int
