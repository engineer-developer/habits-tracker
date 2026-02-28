"""Модуль инициализации сервиса взаимодействия с Redis."""

import datetime
import json
from typing import Optional

import redis

from configs import get_settings

TOKEN_EXPIRED_TIME = datetime.timedelta(minutes=30)
settings = get_settings()


class RedisService:
    """Сервис взаимодействия с redis."""

    def __init__(self, url: str) -> None:
        """логика инициализации."""
        self.url = url
        self._redis_client = redis.from_url(self.url, decode_responses=True)

    def save_user_data(self, user_id: int, key: str, value: str) -> None:
        """Сохранение данных в Redis."""
        self._redis_client.hset(f"user:{user_id}", key, json.dumps(value))

    def load_user_data(self, user_id: int, key: str) -> Optional[str]:
        """Загрузка данных из Redis."""
        data = self._redis_client.hget(f"user:{user_id}", key)
        if data:
            return json.loads(data)
        else:
            return None

    def delete_user_data(self, user_id: int, key: str) -> bool:
        """Удаление данных из Redis."""
        if self.load_user_data(user_id, key):
            self._redis_client.hdel(f"user:{user_id}", key)
            return True
        else:
            return False


redis_service = RedisService(url=settings.redis_url)
