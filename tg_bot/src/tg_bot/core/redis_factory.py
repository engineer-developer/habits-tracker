import json

import redis
from tg_bot.core.config import settings

#
# redis_client = redis.from_url(settings.redis_url, decode_responses=True)
#
#
# def save_user_data(user_id, key, value):
#     """Сохранение данных в Redis."""
#     redis_client.hset(f"user:{user_id}", key, json.dumps(value))
#
# def load_user_data(user_id, key):
#     """Загрузка данных из Redis."""
#     data = redis_client.hget(f"user:{user_id}", key)
#     return json.loads(data) if data else None
#
# def delete_user_data(user_id, key):
#     """Удаление данных из Redis."""
#     if load_user_data(user_id, key):
#         redis_client.hdel(f"user:{user_id}", key)