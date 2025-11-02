"""Модуль обработки паролей."""
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


async def get_password_hash(password: str) -> str:
    """Получаем хешированный пароль.

    :param password: Открытый пароль, который необходимо захэшировать.
    :return: Хешированный пароль.
    """
    return password_hash.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяем совпадает ли переданный открытый пароль и хэшированный пароль.

    :param plain_password: Открытый пароль.
    :param hashed_password: Хэшированный пароль.
    :return: Логическое значение True или False.
    """
    return password_hash.verify(plain_password, hashed_password)
