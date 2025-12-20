"""Cache service for Environmental Law Chatbot.

Provides caching functionality for KG query results to improve response times
for repeated questions.
"""
import hashlib
import json
from typing import Optional, Any

from infrastructure.cache import get_redis_client
from core.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """Cache service for chatbot responses."""
    
    # Cache key prefixes
    PREFIX_ANSWER = "envlaw:answer:"
    PREFIX_KG_QUERY = "envlaw:kg:"
    PREFIX_INTENT = "envlaw:intent:"
    
    # TTL settings (in seconds)
    TTL_ANSWER = 3600  # 1 hour for full answers
    TTL_KG_QUERY = 1800  # 30 minutes for KG query results
    TTL_INTENT = 7200  # 2 hours for intent parsing (stable)
    
    def __init__(self):
        """Initialize cache service with Redis client."""
        self._redis = None
    
    @property
    def redis(self):
        """Lazy load Redis client."""
        if self._redis is None:
            try:
                self._redis = get_redis_client()
            except RuntimeError:
                logger.warning("Redis not initialized, caching disabled")
                return None
        return self._redis
    
    def _hash_key(self, text: str) -> str:
        """Create a hash key from text."""
        return hashlib.md5(text.lower().strip().encode('utf-8')).hexdigest()
    
    async def get_cached_answer(self, question: str) -> Optional[str]:
        """Get cached answer for a question.
        
        Args:
            question: The user's question
            
        Returns:
            Cached answer string or None if not found
        """
        if not self.redis:
            return None
            
        try:
            key = f"{self.PREFIX_ANSWER}{self._hash_key(question)}"
            cached = await self.redis.get(key)
            if cached:
                logger.info(f"Cache HIT for question: {question[:50]}...")
                return cached
            logger.debug(f"Cache MISS for question: {question[:50]}...")
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set_cached_answer(
        self, 
        question: str, 
        answer: str, 
        ttl: Optional[int] = None
    ) -> bool:
        """Cache an answer for a question.
        
        Args:
            question: The user's question
            answer: The answer to cache
            ttl: Time-to-live in seconds (default: TTL_ANSWER)
            
        Returns:
            True if cached successfully
        """
        if not self.redis:
            return False
            
        try:
            key = f"{self.PREFIX_ANSWER}{self._hash_key(question)}"
            ttl = ttl or self.TTL_ANSWER
            await self.redis.setex(key, ttl, answer)
            logger.info(f"Cached answer for: {question[:50]}... (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def get_cached_kg_result(
        self, 
        query_type: str, 
        entity: str
    ) -> Optional[dict]:
        """Get cached KG query result.
        
        Args:
            query_type: Type of query (e.g., "definition", "obligation")
            entity: The entity being queried
            
        Returns:
            Cached result dict or None
        """
        if not self.redis:
            return None
            
        try:
            key = f"{self.PREFIX_KG_QUERY}{query_type}:{self._hash_key(entity)}"
            cached = await self.redis.get(key)
            if cached:
                return json.loads(cached)
            return None
        except Exception as e:
            logger.error(f"Cache get KG error: {e}")
            return None
    
    async def set_cached_kg_result(
        self, 
        query_type: str, 
        entity: str, 
        result: dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Cache a KG query result.
        
        Args:
            query_type: Type of query
            entity: The entity being queried
            result: Result dict to cache
            ttl: Time-to-live in seconds
            
        Returns:
            True if cached successfully
        """
        if not self.redis:
            return False
            
        try:
            key = f"{self.PREFIX_KG_QUERY}{query_type}:{self._hash_key(entity)}"
            ttl = ttl or self.TTL_KG_QUERY
            await self.redis.setex(key, ttl, json.dumps(result, ensure_ascii=False))
            return True
        except Exception as e:
            logger.error(f"Cache set KG error: {e}")
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache keys matching a pattern.
        
        Args:
            pattern: Redis key pattern (e.g., "envlaw:answer:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.redis:
            return 0
            
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                deleted = await self.redis.delete(*keys)
                logger.info(f"Invalidated {deleted} cache keys matching: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Cache invalidate error: {e}")
            return 0
    
    async def clear_all(self) -> bool:
        """Clear all envlaw cache entries.
        
        Returns:
            True if cleared successfully
        """
        try:
            deleted = await self.invalidate_pattern("envlaw:*")
            logger.info(f"Cleared all envlaw cache: {deleted} keys")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    async def get_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Dict with cache stats
        """
        if not self.redis:
            return {"status": "disabled"}
            
        try:
            answer_keys = await self.redis.keys(f"{self.PREFIX_ANSWER}*")
            kg_keys = await self.redis.keys(f"{self.PREFIX_KG_QUERY}*")
            
            return {
                "status": "enabled",
                "answer_cache_count": len(answer_keys),
                "kg_cache_count": len(kg_keys),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


# Singleton instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """Get cache service singleton."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
