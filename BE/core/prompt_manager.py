import os
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache


class PromptManager:
    def __init__(self, prompts_dir: Optional[Path] = None):
        if prompts_dir is None:
            be_dir = Path(__file__).parent.parent
            prompts_dir = be_dir / "prompts"
        
        self.prompts_dir = Path(prompts_dir)
        self._template_cache: Dict[str, str] = {}

    @lru_cache(maxsize=32)
    def load_prompt(self, prompt_name: str) -> str:
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def format_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        template = self.load_prompt(prompt_name)
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            if placeholder in template:
                value_str = str(value) if value is not None else ""
                template = template.replace(placeholder, value_str)
        
        return template

    def clear_cache(self):
        self.load_prompt.cache_clear()
        self._template_cache.clear()

_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
