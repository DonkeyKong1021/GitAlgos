import functools
import pickle
from typing import Any, Callable, Optional

import redis

from app.settings import settings


_client: Optional[redis.Redis] = None


def get_client() -> Optional[redis.Redis]:
    global _client
    if _client is None:
        try:
            _client = redis.from_url(settings.redis_url)
        except redis.RedisError:
            _client = None
    return _client


def cache(ttl: int = 30):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"cache:{func.__name__}:{args}:{kwargs}"
            client = get_client()
            if client:
                try:
                    cached = client.get(key)
                    if cached:
                        return pickle.loads(cached)
                except redis.RedisError:
                    pass
            result = func(*args, **kwargs)
            if client:
                try:
                    client.setex(key, ttl, pickle.dumps(result))
                except redis.RedisError:
                    pass
            return result

        return wrapper

    return decorator
