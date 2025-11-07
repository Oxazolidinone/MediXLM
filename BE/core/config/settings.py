"""Application settings."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "MediXLM"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database (PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/medixlm"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis Cache (Upstash Cloud)
    REDIS_URL: str = "rediss://default:password@your-redis.upstash.io:6379"
    REDIS_MAX_CONNECTIONS: int = 50

    # Neo4j Knowledge Graph (Aura Cloud)
    NEO4J_URI: str = "neo4j+s://xxxxxxxx.databases.neo4j.io"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # Milvus Vector Database (Cloud)
    MILVUS_URI: str = "https://your-instance.api.gcp-us-west1.zillizcloud.com"
    MILVUS_TOKEN: Optional[str] = None
    MILVUS_COLLECTION_NAME: str = "medical_knowledge"

    # Qdrant Vector Database (Cloud)
    QDRANT_URL = "https://<your-qdrant-endpoint>"
    QDRANT_API_KEY = "<your-api-key>"
    QDRANT_COLLECTION_NAME = "medical_knowledge"
    EMBEDDING_DIMENSION = 384

    # Local LLM (HuggingFace models)
    LLM_MODEL_NAME: str = "microsoft/phi-2"  # Lightweight model
    LLM_MAX_TOKENS: int = 2000

    # Local Embedding Model
    EMBEDDING_MODEL_NAME: str = "intfloat/e5-base-v2"
    EMBEDDING_DIMENSION: int = 384  # all-MiniLM-L6-v2 dimension

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()


settings = get_settings()
