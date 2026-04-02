"""Модуль генерации keyboards."""

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from tg_bot import callbacks
from tg_bot import schemas

button_loging = InlineKeyboardButton(
    text=callbacks.AuthMethod.login.value,
    callback_data=callbacks.AuthCallback(method=callbacks.AuthMethod.login).pack(),
)
button_register = InlineKeyboardButton(
    text=callbacks.AuthMethod.register.value,
    callback_data=callbacks.AuthCallback(method=callbacks.AuthMethod.register).pack(),
)
button_back = InlineKeyboardButton(
    text="🔙 Назад",
    callback_data="back",
)
button_cancel = InlineKeyboardButton(
    text="🚫 Отмена",
    callback_data="cancel",
)
button_clear_completed_habits = InlineKeyboardButton(
    text="🗑 Удалить завершенные",
    callback_data="clear_completed_habits",
)


def kb_back() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой назад."""
    builder = InlineKeyboardBuilder()
    builder.add(button_back)
    return builder.as_markup()


def kb_cancel() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой отмена."""
    builder = InlineKeyboardBuilder()
    builder.add(button_cancel)
    return builder.as_markup()


def kb_back_cancel() -> InlineKeyboardMarkup:
    """Клавиатура с кнопками назад и отмена."""
    builder = InlineKeyboardBuilder()
    builder.add(button_back, button_cancel)
    builder.adjust(2)
    return builder.as_markup()


def kb_login() -> InlineKeyboardMarkup:
    """Клавиатура login."""
    builder = InlineKeyboardBuilder()
    builder.add(button_loging)
    builder.add(button_back, button_cancel)
    builder.adjust(1, 2)
    return builder.as_markup()


def kb_register() -> InlineKeyboardMarkup:
    """Клавиатура register."""
    builder = InlineKeyboardBuilder()
    builder.add(button_register)
    builder.add(button_back, button_cancel)
    builder.adjust(1, 2)
    return builder.as_markup()


def kb_login_or_register() -> InlineKeyboardMarkup:
    """Клавиатура login или register."""
    builder = InlineKeyboardBuilder()
    builder.add(button_loging, button_register)
    return builder.as_markup()


def kb_profile() -> InlineKeyboardMarkup:
    """Клавиатура профиля пользователя."""
    builder = InlineKeyboardBuilder()
    for action in callbacks.ProfileAction:
        builder.button(
            text=action.value,
            callback_data=callbacks.ProfileMenuCallback(action=action),
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def kb_active_habits(habits: list[schemas.HabitRead]) -> InlineKeyboardMarkup:
    """Клавиатура списка привычек."""
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(
            text=f"🔹{habit.title}",
            callback_data=callbacks.HabitIdCallback(habit_id=habit.id),
        )
    builder.add(button_back, button_cancel)
    builder.adjust(1)
    return builder.as_markup()


def kb_completed_habits(habits: list[schemas.HabitRead]) -> InlineKeyboardMarkup:
    """Клавиатура списка привычек."""
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(
            text=f"🔹{habit.title}",
            callback_data=callbacks.HabitIdCallback(habit_id=habit.id),
        )
    builder.add(button_clear_completed_habits, button_back, button_cancel)
    builder.adjust(1)
    return builder.as_markup()


def kb_habit_add_or_cancel() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения добавления привычки или отмены."""
    builder = InlineKeyboardBuilder()
    for action in callbacks.HabitAddConfirmAction:
        builder.button(
            text=action.value,
            callback_data=callbacks.HabitAddConfirmActionCallback(action=action),
        )
    return builder.as_markup()


def kb_confirm_habit_completed(habit_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения выполнения привычки."""
    action = callbacks.HabitMarkCompletedAction.mark_completed
    builder = InlineKeyboardBuilder()
    builder.button(
        text=action.value,
        callback_data=callbacks.HabitMarkCompletedCallback(
            action=action,
            habit_id=habit_id,
        ),
    )
    return builder.as_markup()


def kb_habit_edit_delete_complete(habit_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in callbacks.HabitDetailsAction:
        builder.button(
            text=action.value,
            callback_data=callbacks.HabitDetailsActionCallback(
                action=action,
                habit_id=habit_id,
            ),
        )
    builder.add(button_back)
    builder.adjust(3, 1)
    return builder.as_markup()


def kb_habit_edit_choices(habit_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for action in callbacks.HabitEditAction:
        builder.button(
            text=action.value,
            callback_data=callbacks.HabitEditActionCallback(
                action=action, habit_id=habit_id
            ),
        )
    builder.add(button_back, button_cancel)
    builder.adjust(2)
    return builder.as_markup()
