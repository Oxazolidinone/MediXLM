"""Dependency injection for API endpoints."""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from application.use_cases import ChatUseCase, UserUseCase, KnowledgeUseCase
from domain.repositories import (
    IConversationRepository,
    IUserRepository,
    IKnowledgeGraphRepository,
    ICacheRepository,
)
from infrastructure.cache.redis_client import get_redis_client
from infrastructure.database.connection import get_database_session, get_sync_session
from infrastructure.knowledge_graph.neo4j_client import get_neo4j_driver
from infrastructure.repositories import (
    ConversationRepositoryImpl,
    UserRepositoryImpl,
    KnowledgeGraphRepositoryImpl,
    CacheRepositoryImpl,
)
from infrastructure.services import LocalLLMService


# Database session dependency
def get_db_session() -> Generator[Session, None, None]:
    """Get database session."""
    with get_database_session() as session:
        yield session


# Repository dependencies
def get_user_repository(
    session: Session = Depends(get_db_session),
) -> IUserRepository:
    """Get user repository."""
    return UserRepositoryImpl(session)


def get_conversation_repository(
    session: Session = Depends(get_db_session),
) -> IConversationRepository:
    """Get conversation repository."""
    return ConversationRepositoryImpl(session)


def get_knowledge_graph_repository() -> IKnowledgeGraphRepository:
    """Get knowledge graph repository."""
    driver = get_neo4j_driver()
    return KnowledgeGraphRepositoryImpl(driver)


def get_cache_repository() -> ICacheRepository:
    """Get cache repository."""
    redis = get_redis_client()
    return CacheRepositoryImpl(redis)


# Service dependencies (singleton instances)
_llm_service = None


def get_llm_service() -> LocalLLMService:
    """Get LLM service (singleton)."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LocalLLMService()
    return _llm_service


def get_embedding_service() -> LocalLLMService:
    """Get embedding service (singleton)."""
    # Reuse LLM service for embeddings
    return get_llm_service()


# Use case dependencies
def get_chat_use_case(
    conversation_repo: IConversationRepository = Depends(get_conversation_repository),
    kg_repo: IKnowledgeGraphRepository = Depends(get_knowledge_graph_repository),
    cache_repo: ICacheRepository = Depends(get_cache_repository),
    llm_service: LocalLLMService = Depends(get_llm_service),
    embedding_service: LocalLLMService = Depends(get_embedding_service),
) -> ChatUseCase:
    """Get chat use case."""
    return ChatUseCase(
        conversation_repository=conversation_repo,
        knowledge_graph_repository=kg_repo,
        cache_repository=cache_repo,
        llm_service=llm_service,
        embedding_service=embedding_service,
    )


def get_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> UserUseCase:
    """Get user use case."""
    return UserUseCase(user_repository=user_repo)


def get_knowledge_use_case(
    kg_repo: IKnowledgeGraphRepository = Depends(get_knowledge_graph_repository),
    embedding_service: LocalLLMService = Depends(get_embedding_service),
) -> KnowledgeUseCase:
    """Get knowledge use case."""
    return KnowledgeUseCase(
        knowledge_graph_repository=kg_repo,
        embedding_service=embedding_service,
    )
