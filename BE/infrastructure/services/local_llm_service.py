"""Local LLM service using transformers."""
from typing import List, Dict, Any, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
import requests
from core.config import settings
from .local_embedding_service import LocalEmbeddingService


class LocalLLMService:
    def __init__(self):
        self.api_url = f"{settings.OLLAMA_API_URL}/generate"
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

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.5) -> str:
        """Generate a response using the local Ollama Qwen model."""
        url = f"{settings.OLLAMA_API_URL}/api/generate"
        
        # Construct the payload for Ollama
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"System: {system_prompt}\nUser: {prompt}\nAssistant:"
            
        payload = {
            "model": "qwen2.5:1.5b", # Ensure this matches user's model
            "prompt": full_prompt,
            "stream": False,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 1024
            }
        }
        
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "").strip()
        except Exception as e:
            print(f"[LLM Error] {e}")
            return f"Error creating response: {str(e)}"

    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ):
        pass # Not used currently
