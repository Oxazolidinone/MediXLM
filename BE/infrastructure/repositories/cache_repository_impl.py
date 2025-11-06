"""Cache repository implementation using Redis."""
import json
from typing import Optional, Any

import redis.asyncio as redis

from domain.repositories import ICacheRepository


class CacheRepositoryImpl(ICacheRepository):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value is None:
            return None

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        try:
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            if expire:
                return await self.redis.setex(key, expire, serialized_value)
            else:
                return await self.redis.set(key, serialized_value)
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        result = await self.redis.delete(key)
        return result > 0

    async def exists(self, key: str) -> bool:
        result = await self.redis.exists(key)
        return result > 0

    async def clear(self, pattern: Optional[str] = None) -> bool:
        try:
            if pattern:
                keys = await self.redis.keys(pattern)
                if keys:
                    await self.redis.delete(*keys)
            else:
                await self.redis.flushdb()
            return True
        except Exception:
            return False

    async def increment(self, key: str, amount: int = 1) -> int:
        return await self.redis.incrby(key, amount)

    async def get_ttl(self, key: str) -> Optional[int]:
        ttl = await self.redis.ttl(key)
        return ttl if ttl > 0 else None
