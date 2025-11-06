"""Application service interfaces."""
from .llm_service import ILLMService
from .embedding_service import IEmbeddingService

__all__ = ["ILLMService", "IEmbeddingService"]
