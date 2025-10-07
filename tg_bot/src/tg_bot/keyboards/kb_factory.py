from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_start_kb(text: str, callback: str) -> InlineKeyboardMarkup:
    """Получаем стартовую клавиатуру."""
    markup = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=text, callback=callback)
    markup.add(button)
    return markup


main_menu_kb = get_start_kb("Главное меню", "cb_main_menu")
login_kb = get_start_kb("Войти", "cb_login")
register_kb = get_start_kb("Зарегистрироваться", "cb_register")
