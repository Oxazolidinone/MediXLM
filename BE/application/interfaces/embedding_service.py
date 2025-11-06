"""Embedding service interface."""
from abc import ABC, abstractmethod
from typing import List


class IEmbeddingService(ABC):
    @abstractmethod
    async def generate_embeddings(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        pass
