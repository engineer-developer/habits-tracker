"""Модуль схем аутентификации."""

from pydantic import Field

from .base import BaseDtoModel


class TokenRead(BaseDtoModel):
    """Схема токена доступа."""

    access_token: str = Field(
        description="Токен аутентификации",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdC"
            "I6MTUxNjIzOTAyMn0."
            "KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
        ],
    )


