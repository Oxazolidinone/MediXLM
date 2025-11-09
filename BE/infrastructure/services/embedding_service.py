"""Embedding service for RAG using sentence-transformers."""
from typing import List
from sentence_transformers import SentenceTransformer
from core.config import settings


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self, model_name: str = None):
        """Initialize embedding model."""
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        print(f"[EMBEDDING] Loading model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        self.dimension = settings.EMBEDDING_DIMENSION
        print(f"[EMBEDDING] Model loaded. Dimension: {self.dimension}")

    def embed_text(self, text: str) -> List[float]:
        """
        Embed single text string.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=32
        )
        return embeddings.tolist()


# Global instance (singleton pattern)
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """
    Get or create global embedding service instance.

    Returns:
        EmbeddingService instance
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
