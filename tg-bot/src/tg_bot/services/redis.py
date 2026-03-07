from typing import Optional

from redis.asyncio import client


class RedisService:
    def __init__(self, client: client.Redis) -> None:
        self.client = client

    async def save_token(self, telegram_id: int, value: str) -> None:
        """Сохраняем token в БД Redis."""
        await self.client.hset(
            name=f"user:{telegram_id}",
            key="token",
            value=value,
        )

    async def get_token(self, telegram_id: int) -> Optional[str]:
        """Получаем token из БД Redis."""
        return await self.client.hget(
            name=f"user:{telegram_id}",
            key="token",
        )
