"""Модуль генерации keyboards."""

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from tg_bot.callbacks.auth import AuthCallback, AuthMethod

loging_button = InlineKeyboardButton(
    text=AuthMethod.login.value,
    callback_data=AuthCallback(method=AuthMethod.login).pack(),
)
register_button = InlineKeyboardButton(
    text=AuthMethod.register.value,
    callback_data=AuthCallback(method=AuthMethod.register).pack(),
)


def kb_login() -> InlineKeyboardBuilder:
    """Получаем login клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(loging_button)
    return builder


def kb_register() -> InlineKeyboardBuilder:
    """Получаем register клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(register_button)
    return builder


def kb_login_or_register() -> InlineKeyboardBuilder:
    """Получаем login or register клавиатуру."""
    builder = InlineKeyboardBuilder()
    builder.add(
        loging_button,
        register_button,
    )
    return builder


def kb_profile() -> InlineKeyboardMarkup:
    """Клавиатура профиля пользователя."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.row(
        InlineKeyboardButton(
            text="➕ Список привычек",
            callback_data="menu_habits_list",
        ),
        InlineKeyboardButton(
            text="➕ Добавить привычку",
            callback_data="menu_add_habit",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text="⚙ Редактировать",
            callback_data="menu_edit_habit",
        ),
        InlineKeyboardButton(
            text="❌ Удалить",
            callback_data="menu_remove_habit",
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text="✅ Выполнить",
            callback_data="menu_mark_habit_complete",
        ),
        InlineKeyboardButton(
            text="📊 Статистика",
            callback_data="menu_habit_stat",
        ),
    )
    return keyboard


def kb_habits_list(habits: list[dict]):
    """Клавиатура списка привычек."""
    keyboard = InlineKeyboardMarkup(row_width=3)
    for habit in habits:
        keyboard.add(
            InlineKeyboardButton(
                text=f"🔹{habit.get('name')}",
                callback_data=f"habits:view:{habit.get('id')}",
            ),
            InlineKeyboardButton(
                text="✅ Выполнено",
                callback_data=f"habits:edit:{habit.get('id')}",
            ),
            InlineKeyboardButton(
                text="⚙ Изменить",
                callback_data=f"habits:edit:{habit.get('id')}",
            ),
        )
    return keyboard


def kb_habit_add_or_cancel():
    """Клавиатура подтверждения добавления привычки или отмены."""
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="✅ Добавить", callback_data="cb_confirm_add_habit"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cb_cancel_add_habit"),
    )
    return keyboard


def kb_confirm_habit_completed(habit_name):
    """Клавиатура подтверждения выполнения привычки."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Подтвердить выполнение",
            callback_data=f"cb_confirm_habit_done:{habit_name}",
        ),
    )
    return keyboard
