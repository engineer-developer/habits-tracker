"""Модуль тестов api views."""

from fastapi import status
from httpx import AsyncClient


async def test_can_not_access_without_auth(async_client: AsyncClient) -> None:
    """Тест - клиент не может получить доступ без аутентификации."""
    url = "/api/users/profile/"
    response = await async_client.get(url=url, timeout=5)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Not authenticated"


async def test_can_access_with_auth(jwt_token: str, async_client: AsyncClient) -> None:
    """Тест - аутентифицированный клиент может получить доступ."""
    url = "/api/users/profile/"
    headers = async_client.headers.copy()
    headers.update(
        {"Authorization": f"Bearer {jwt_token}"},
    )
    response = await async_client.get(url=url, headers=headers, timeout=5)
    assert response.status_code == status.HTTP_200_OK
