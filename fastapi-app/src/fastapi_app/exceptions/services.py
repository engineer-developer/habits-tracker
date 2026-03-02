from fastapi import status

from fastapi_app.exceptions.base import BaseApiException


class UserNotFoundException(BaseApiException):
    """Исключение - пользователь не найден."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Пользователь не зарегистрирован."


class UserAlreadyExistException(BaseApiException):
    """Исключение - пользователь уже существует."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Пользователь уже зарегистрирован."


class UserIsNotActiveException(BaseApiException):
    """Исключение - пользователь не активен."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Пользователь не активен."


class HabitNotFoundException(BaseApiException):
    """Исключение - привычка не найдена."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Привычки не найдено."


class HabitAlreadyExistException(BaseApiException):
    """Исключение - привычка уже существует."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Привычка уже существует."


class InvalidPasswordException(BaseApiException):
    """Исключение - неверный пароль."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Неверные пользователь или пароль."


class DbException(BaseApiException):
    """Ошибка при взаимодействии с базой данных."""

    status_code = status.HTTP_409_CONFLICT
    message = "Ошибка при взаимодействии с базой данных."
