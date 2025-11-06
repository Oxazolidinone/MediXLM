"""Cache repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, Any


class ICacheRepository(ABC):
    """Interface for cache repository."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in cache with optional expiration (in seconds)."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass

    @abstractmethod
    async def clear(self, pattern: Optional[str] = None) -> bool:
        """Clear cache entries matching pattern."""
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment value in cache."""
        pass

    @abstractmethod
    async def get_ttl(self, key: str) -> Optional[int]:
        """Get time to live for a key."""
        pass
