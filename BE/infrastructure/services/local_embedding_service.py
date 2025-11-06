"""Local embedding service using sentence-transformers."""
from typing import List
import torch
from sentence_transformers import SentenceTransformer

from application.interfaces import IEmbeddingService
from core.config import settings


class LocalEmbeddingService(IEmbeddingService):
    """Local embedding service using sentence-transformers."""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL_NAME,
            device=self.device
        )

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text."""
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding.tolist()

    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            batch_size=32,
        )
        return embeddings.tolist()
