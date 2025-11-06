"""Local LLM service using transformers."""
from typing import List, Dict, Any, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

from application.interfaces import ILLMService
from core.config import settings


class LocalLLMService(ILLMService):
    """Local LLM service using HuggingFace transformers."""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = settings.LLM_MODEL_NAME

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )

        if self.device == "cpu":
            self.model = self.model.to(self.device)

        self.model.eval()

    def _format_messages(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> str:
        """Format messages into prompt string."""
        prompt_parts = []

        if system_prompt:
            prompt_parts.append(f"System: {system_prompt}\n")

        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            prompt_parts.append(f"{role}: {content}\n")

        prompt_parts.append("Assistant:")
        return "\n".join(prompt_parts)

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate response from local LLM."""

        prompt = self._format_messages(messages, system_prompt)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens or settings.LLM_MAX_TOKENS,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the assistant's response
        response = response[len(prompt):].strip()

        return {
            "content": response,
            "tokens_used": len(outputs[0]),
            "model": self.model_name,
            "finish_reason": "stop",
        }

    async def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None,
    ):
        """Generate streaming response from local LLM."""

        prompt = self._format_messages(messages, system_prompt)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_special_tokens=True,
            skip_prompt=True,
        )

        generation_kwargs = {
            **inputs,
            "max_new_tokens": max_tokens or settings.LLM_MAX_TOKENS,
            "temperature": temperature,
            "do_sample": True,
            "top_p": 0.9,
            "pad_token_id": self.tokenizer.eos_token_id,
            "streamer": streamer,
        }

        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for text in streamer:
            yield text
