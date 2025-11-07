"""Local LLM service using transformers."""
from typing import List, Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
import requests
from core.config import settings
from services.local_embedding_service import LocalEmbeddingService


class LocalLLMService:
    def __init__(self):
        self.api_url = f"{settings.LLM_API_URL}/generate"
        self.timeout = settings.LLM_TIMEOUT
        self.embedding_service = LocalEmbeddingService() 

    def _format_messages(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        """Format multi-turn chat messages into a single prompt."""
        prompt_parts = []
        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}\n")

        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            prompt_parts.append(f"{role}: {content}\n")

        prompt_parts.append("Assistant:")
        return "\n".join(prompt_parts)

    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ):
        """Stream tokens from local vLLM API endpoint."""
        prompt = self._format_messages(messages, system_prompt)
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens or settings.LLM_MAX_TOKENS,
        }

        with requests.post(self.api_url, json=payload, stream=True, timeout=self.timeout) as r:
            for line in r.iter_lines():
                if not line:
                    continue
            decoded = line.decode("utf-8")
            if decoded.startswith("data: "):
                yield decoded.replace("data: ", "")


    async def generate_embeddings(self, text: str):
        return await self.embedding_service.generate_embedding(text)

    async def generate_batch_embeddings(self, texts: List[str]):
        return await self.embedding_service.generate_batch_embeddings(texts)
