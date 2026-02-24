from fastapi import status

from fastapi_app.exceptions.base import BaseApiException


class UserNotFoundException(BaseApiException):
    """Исключение - пользователь не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не зарегистрирован."


class UserAlreadyExistException(BaseApiException):
    """Исключение - пользователь уже существует."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователь уже зарегистрирован."


class UserIsNotActiveException(BaseApiException):
    """Исключение - пользователь не активен."""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователь не активен."


class InvalidPasswordException(BaseApiException):
    """Исключение - неверный пароль."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверные пользователь или пароль."


class DbException(BaseApiException):
    """Ошибка при взаимодействии с базой данных."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Ошибка при взаимодействии с базой данных."
