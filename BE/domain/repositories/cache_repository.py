"""Cache repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, Any


class ICacheRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def clear(self, pattern: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        pass

    @abstractmethod
    async def get_ttl(self, key: str) -> Optional[int]:
        pass
