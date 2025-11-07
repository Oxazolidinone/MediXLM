from typing import List
import requests
from core.config import settings


class LocalEmbeddingService:
    def __init__(self):
        self.api_url = f"{settings.EMBEDDING_API_URL}/embeddings"
        self.timeout = settings.LLM_TIMEOUT

    async def generate_embedding(self, text: str) -> List[float]:
        """Call vLLM embedding endpoint for a single text."""
        payload = {"input": text}
        response = requests.post(self.api_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Batch version."""
        payload = {"input": texts}
        response = requests.post(self.api_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]
