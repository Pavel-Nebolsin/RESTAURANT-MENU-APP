import json
from typing import Any, Callable

import aioredis
from fastapi import BackgroundTasks
from fastapi.encoders import jsonable_encoder

from config import REDIS_HOST, REDIS_PORT


class Cache:
    def __init__(self, redis_host: str, redis_port: str) -> None:
        self.redis_client: aioredis.Redis = aioredis.from_url(f'redis://{redis_host}:{redis_port}')

    async def get(self, key: str) -> str | None:
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return cached_data.decode('utf-8')
        return None

    async def set(self, key: str, value: str) -> None:
        await self.redis_client.set(key, value)

    async def cached_or_fetch(
            self,
            cache_key: str,
            repository_function: Callable[..., Any],
            *args: Any, **kwargs: Any) -> Any:

        cached_result = await self.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        items = await repository_function(*args, **kwargs)
        json_compatible_value = jsonable_encoder(items)
        await self.set(cache_key, json.dumps(json_compatible_value))
        return items

    async def invalidate(self, *args: str) -> None:
        await self.redis_client.delete(*args)
        background_tasks = BackgroundTasks()
        background_tasks.add_task(self.background_invalidation, *args)

    async def background_invalidation(self, *args):
        await self.redis_client.delete(*args)


cache = Cache(REDIS_HOST, REDIS_PORT)
