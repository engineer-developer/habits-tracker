from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader


auth_header_key = APIKeyHeader(name="telegram_id")


async def get_auth_key(auth_key: Annotated[str, Depends(auth_header_key)]) -> int:
    """Получаем значение ключа аутентификации."""
    return int(auth_key)
