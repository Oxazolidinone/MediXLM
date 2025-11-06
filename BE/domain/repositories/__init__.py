"""Repository interfaces (Domain layer)."""
from .conversation_repository import IConversationRepository
from .user_repository import IUserRepository
from .knowledge_graph_repository import IKnowledgeGraphRepository
from .cache_repository import ICacheRepository

__all__ = [
    "IConversationRepository",
    "IUserRepository",
    "IKnowledgeGraphRepository",
    "ICacheRepository",
]
