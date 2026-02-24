from fastapi import status

from fastapi_app.exceptions.base import BaseApiException


class TokenExpired(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек."


class TokenInvalid(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не валидный токен."


class TokenDataLoss(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не содержит данных."
