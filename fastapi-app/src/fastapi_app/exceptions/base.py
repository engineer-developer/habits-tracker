from typing import Optional

from fastapi.exceptions import HTTPException


class BaseApiException(HTTPException):
    """Базовый класс API исключений."""

    status_code = 500
    message = "Base API exception"

    def __init__(
        self,
        message: Optional[str] = None,
    ) -> None:
        if message is not None:
            self.message = message

        super().__init__(status_code=self.status_code, detail=self.message)
