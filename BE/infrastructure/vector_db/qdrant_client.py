# core/qdrant_client.py

from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from core.config import settings


_qdrant_client: Optional[QdrantClient] = None


async def init_qdrant():
    """Initialize Qdrant cloud connection."""
    global _qdrant_client

    _qdrant_client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

    collection_name = settings.QDRANT_COLLECTION_NAME

    collections = [c.name for c in _qdrant_client.get_collections().collections]
    if collection_name not in collections:
        # Create new collection
        _qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=settings.EMBEDDING_DIMENSION,
                distance=models.Distance.COSINE
            )
        )


async def close_qdrant():
    """Close Qdrant connection."""
    global _qdrant_client
    if _qdrant_client:
        _qdrant_client = None


def get_qdrant_client() -> QdrantClient:
    """Return the Qdrant client."""
    if _qdrant_client is None:
        raise RuntimeError("Qdrant not initialized. Call init_qdrant() first.")
    return _qdrant_client
