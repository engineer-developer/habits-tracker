"""Модуль инициализации сервиса взаимодействия с Redis."""

import datetime
import json
from dataclasses import dataclass
from typing import Optional

import redis

from tg_bot.core.config import settings

TOKEN_EXPIRED_TIME = datetime.timedelta(minutes=30)


@dataclass
class RedisService:
    """Сервис взаимодействия с redis."""

    url: str
    redis_client: Optional[redis.Redis] = None

    def __post_init__(self) -> None:
        """логика инициализации."""
        if not self.redis_client:
            self.redis_client = redis.from_url(self.url, decode_responses=True)

    def save_user_data(self, user_id: int, key: str, value: str) -> None:
        """Сохранение данных в Redis."""
        self.redis_client.hset(f"user:{user_id}", key, json.dumps(value))

    def load_user_data(self, user_id: int, key: str):
        """Загрузка данных из Redis."""
        data = self.redis_client.hget(f"user:{user_id}", key)
        return json.loads(data) if data else None

    def delete_user_data(self, user_id: int, key: str) -> bool:
        """Удаление данных из Redis."""
        if self.load_user_data(user_id, key):
            self.redis_client.hdel(f"user:{user_id}", key)
            return True
        else:
            return False


redis_service = RedisService(url=settings.redis_url)
