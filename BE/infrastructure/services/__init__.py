"""Infrastructure services."""
from .local_llm_service import LocalLLMService

# Alias for backward compatibility
LLMService = LocalLLMService

__all__ = ["LocalLLMService", "LLMService"]
