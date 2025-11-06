"""Redis client management for Upstash Cloud."""
import json
from typing import Optional

import redis.asyncio as redis

from core.config import settings

# Global Redis client
redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection to Upstash Cloud.

    Uses REDIS_URL format: rediss://default:password@host:port
    Upstash provides secure Redis with TLS (rediss://)
    """
    global redis_client

    # Connect using URL (supports Upstash format with TLS)
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
        socket_connect_timeout=5,
        socket_keepalive=True,
        health_check_interval=30,
    )

    # Test connection
    await redis_client.ping()


async def close_redis():
    """Close Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()


def get_redis_client() -> redis.Redis:
    """Get Redis client."""
    if redis_client is None:
        raise RuntimeError("Redis client not initialized. Call init_redis() first.")
    return redis_client
