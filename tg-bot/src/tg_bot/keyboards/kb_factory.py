"""Модуль генерации keyboards."""

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardBuilder
)

from tg_bot.callbacks.auth import AuthCallback, AuthMethod
from tg_bot.callbacks.habits import (
    HabitListCallback,
    HabitAction,
    HabitAddConfirmCallback,
    HabitAddConfirmAction,
    HabitMarkCompletedCallback,
    HabitMarkCompletedAction,
)
from tg_bot.callbacks.user_profile import ProfileAction, ProfileMenuCallback
from tg_bot.schemas.habits import HabitRead


loging_button = InlineKeyboardButton(
    text=AuthMethod.login.value,
    callback_data=AuthCallback(method=AuthMethod.login).pack(),
)
register_button = InlineKeyboardButton(
    text=AuthMethod.register.value,
    callback_data=AuthCallback(method=AuthMethod.register).pack(),
)


def kb_login() -> InlineKeyboardMarkup:
    """Получаем login клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(loging_button)
    return builder.as_markup()


def kb_register() -> InlineKeyboardMarkup:
    """Получаем register клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(register_button)
    return builder.as_markup()


def kb_login_or_register() -> InlineKeyboardMarkup:
    """Получаем login or register клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(
        loging_button,
        register_button,
    )
    return builder.as_markup()


def kb_profile() -> InlineKeyboardMarkup:
    """Клавиатура профиля пользователя."""
    builder = InlineKeyboardBuilder()
    for action in ProfileAction:
        builder.button(
            text=action.value,
            callback_data=ProfileMenuCallback(action=action),
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def kb_habits_list(habits: list[HabitRead]) -> InlineKeyboardMarkup:
    """Клавиатура списка привычек."""
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.button(
            text=f"🔹{habit.title}", callback_data="test"
        )
    builder.adjust(1)
    return builder.as_markup()


def kb_habit_add_or_cancel() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения добавления привычки или отмены."""
    builder = InlineKeyboardBuilder()
    for action in HabitAddConfirmAction:
        builder.button(
            text=action.value,
            callback_data=HabitAddConfirmCallback(action=action),
        )
    return builder.as_markup()


def kb_confirm_habit_completed(habit_id) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения выполнения привычки."""
    action = HabitMarkCompletedAction.mark_completed
    builder = InlineKeyboardBuilder()
    builder.button(
        text=action.value,
        callback_data=HabitMarkCompletedCallback(
            action=action,
            habit_id=habit_id,
        ),
    )
    return builder.as_markup()
