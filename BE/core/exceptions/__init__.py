"""Custom exceptions."""


class MediXLMException(Exception):
    """Base exception for MediXLM."""
    pass


class UserNotFoundError(MediXLMException):
    """User not found exception."""
    pass


class UserAlreadyExistsError(MediXLMException):
    """User already exists exception."""
    pass


class ConversationNotFoundError(MediXLMException):
    """Conversation not found exception."""
    pass


class KnowledgeNotFoundError(MediXLMException):
    """Knowledge node not found exception."""
    pass


class DatabaseError(MediXLMException):
    """Database error exception."""
    pass


class CacheError(MediXLMException):
    """Cache error exception."""
    pass


class LLMServiceError(MediXLMException):
    """LLM service error exception."""
    pass


class EmbeddingServiceError(MediXLMException):
    """Embedding service error exception."""
    pass
