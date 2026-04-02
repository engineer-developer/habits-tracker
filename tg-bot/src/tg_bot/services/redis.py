from typing import Optional

from redis.asyncio import client

from tg_bot.configs.loguru_config import logger


class RedisService:
    """Сервис взаимодействия с Redis."""

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
        token = await self.client.hget(
            name=f"user:{telegram_id}",
            key="token",
        )
        if not token:
            logger.error("Токен не найден.")
            return None

        return token
