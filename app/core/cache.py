from typing import Any, Protocol

import json
from redis.asyncio import Redis

class CacheBackend(Protocol):
    async def get(self, key: str) -> Any | None:
        ...
        
    async def set(self, key: str, value: Any, ttl: int) -> None:
        ...
        
    async def delete(self, key: str) -> None:
        ...
        
    async def delete_by_prefix(self, prefix: str) -> None:
        ...
        
class RedisCacheBackend(CacheBackend):
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def get(self, key: str) -> Any | None:
        raw_value = await self.redis.get(key)
        if raw_value is None:
            return None
        return json.loads(raw_value)
    
    async def set(self, key: str, value: Any, ttl: int) -> None:
        raw_value = json.dumps(value, default=str)
        await self.redis.set(key, raw_value, ex=ttl)
        
    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_by_prefix(self, prefix: str) -> None:
        keys = []

        async for key in self.redis.scan_iter(f'{prefix}*'):
            keys.append(key)

        if keys:
            await self.redis.delete(*keys)
            
class InMemoryCacheBackend(CacheBackend):
    def __init__(self):
        self.storage: dict[str, Any] = {}

    async def get(self, key: str) -> Any | None:
        return self.storage.get(key)

    async def set(self, key: str, value: Any, ttl: int) -> None:
        self.storage[key] = value

    async def delete(self, key: str) -> None:
        self.storage.pop(key, None)

    async def delete_by_prefix(self, prefix: str) -> None:
        keys_to_delete = [
            key
            for key in self.storage
            if key.startswith(prefix)
        ]

        for key in keys_to_delete:
            self.storage.pop(key, None)