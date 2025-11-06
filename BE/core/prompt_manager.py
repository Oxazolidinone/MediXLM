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

    def get_embedding_prompt(self, name: str, description: Optional[str] = None) -> str:
        return self.format_prompt(
            "embedding_generation",
            name=name,
            description=description or ""
        )

    def get_search_prompt(self, query: str, knowledge_type: Optional[str] = None, limit: int = 10) -> str:
        return self.format_prompt(
            "knowledge_search",
            query=query,
            knowledge_type=knowledge_type or "All types",
            limit=limit
        )

    def get_validation_prompt(self, name: str, knowledge_type: str, description: Optional[str] = None, source: Optional[str] = None, properties: Optional[Dict[str, Any]] = None) -> str:
        return self.format_prompt(
            "knowledge_validation",
            name=name,
            knowledge_type=knowledge_type,
            description=description or "N/A",
            source=source or "N/A",
            properties=properties or {}
        )

    def get_relationship_prompt(self, source_name: str, source_id: str, target_name: str, target_id: str, relationship_type: str) -> str:
        return self.format_prompt(
            "relationship_extraction",
            source_name=source_name,
            source_id=source_id,
            target_name=target_name,
            target_id=target_id,
            relationship_type=relationship_type
        )

    def get_related_analysis_prompt(self, node_name: str, node_id: str, relationship_type: Optional[str] = None, depth: int = 1) -> str:
        return self.format_prompt(
            "related_knowledge_analysis",
            node_name=node_name,
            node_id=node_id,
            relationship_type=relationship_type or "All types",
            depth=depth
        )

    def clear_cache(self):
        self.load_prompt.cache_clear()
        self._template_cache.clear()

_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
