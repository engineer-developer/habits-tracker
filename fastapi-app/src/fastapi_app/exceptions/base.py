from typing import Optional

from fastapi.exceptions import HTTPException


class BaseApiException(HTTPException):
    """Базовый класс API исключений."""

    status_code = 500
    detail = "Base API exception"

    def __init__(
        self,
        status_code: Optional[int] = None,
        detail: Optional[str] = None,
    ):
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)
