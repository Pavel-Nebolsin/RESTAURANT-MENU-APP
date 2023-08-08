import json
from typing import Any, Callable

import redis
from fastapi.encoders import jsonable_encoder


class Cache:
    def __init__(self, redis_host: str) -> None:
        self.redis_client: redis.StrictRedis = redis.StrictRedis(host=redis_host, port=6379, db=0)

    def get(self, key) -> str | None:
        cached_data = self.redis_client.get(key)
        if cached_data:
            return cached_data.decode('utf-8')
        return None

    def set(self, key: str, value: str) -> None:
        self.redis_client.set(key, value)

    def cached_or_fetch(
            self,
            cache_key: str,
            repository_function: Callable[..., Any],
            *args: Any, **kwargs: Any) -> Any:

        cached_result = self.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        items = repository_function(*args, **kwargs)
        json_compatible_value = jsonable_encoder(items)
        self.set(cache_key, json.dumps(json_compatible_value))
        return items

    def invalidate(self, *args: str) -> None:
        for cache_key in args:
            self.redis_client.delete(cache_key)


cache = Cache('redis')
