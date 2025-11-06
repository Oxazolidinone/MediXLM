"""Prompt manager for loading and formatting prompt templates."""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache


class PromptManager:
    """Manager for loading and formatting prompt templates."""

    def __init__(self, prompts_dir: Optional[Path] = None):
        """Initialize prompt manager.
        
        Args:
            prompts_dir: Directory containing prompt templates.
                        Defaults to BE/prompts directory.
        """
        if prompts_dir is None:
            # Get the BE directory (parent of core)
            be_dir = Path(__file__).parent.parent
            prompts_dir = be_dir / "prompts"
        
        self.prompts_dir = Path(prompts_dir)
        self._template_cache: Dict[str, str] = {}

    @lru_cache(maxsize=32)
    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt template from file.
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
            
        Returns:
            The prompt template as a string
            
        Raises:
            FileNotFoundError: If prompt file doesn't exist
        """
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def format_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """Load and format a prompt template with provided variables.
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
            **kwargs: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
            
        Example:
            >>> pm = PromptManager()
            >>> prompt = pm.format_prompt(
            ...     "embedding_generation",
            ...     name="Diabetes Type 2",
            ...     description="Chronic metabolic disorder"
            ... )
        """
        template = self.load_prompt(prompt_name)
        
        # Replace placeholders with provided values
        # Handle missing values gracefully
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            if placeholder in template:
                # Convert None to empty string
                value_str = str(value) if value is not None else ""
                template = template.replace(placeholder, value_str)
        
        return template

    def get_embedding_prompt(self, name: str, description: Optional[str] = None) -> str:
        """Get formatted prompt for embedding generation.
        
        Args:
            name: Knowledge name
            description: Knowledge description
            
        Returns:
            Formatted embedding prompt
        """
        return self.format_prompt(
            "embedding_generation",
            name=name,
            description=description or ""
        )

    def get_search_prompt(
        self,
        query: str,
        knowledge_type: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Get formatted prompt for knowledge search.
        
        Args:
            query: Search query
            knowledge_type: Optional knowledge type filter
            limit: Maximum results
            
        Returns:
            Formatted search prompt
        """
        return self.format_prompt(
            "knowledge_search",
            query=query,
            knowledge_type=knowledge_type or "All types",
            limit=limit
        )

    def get_validation_prompt(
        self,
        name: str,
        knowledge_type: str,
        description: Optional[str] = None,
        source: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """Get formatted prompt for knowledge validation.
        
        Args:
            name: Knowledge name
            knowledge_type: Type of knowledge
            description: Knowledge description
            source: Source of knowledge
            properties: Additional properties
            
        Returns:
            Formatted validation prompt
        """
        return self.format_prompt(
            "knowledge_validation",
            name=name,
            knowledge_type=knowledge_type,
            description=description or "N/A",
            source=source or "N/A",
            properties=properties or {}
        )

    def get_relationship_prompt(
        self,
        source_name: str,
        source_id: str,
        target_name: str,
        target_id: str,
        relationship_type: str
    ) -> str:
        """Get formatted prompt for relationship extraction.
        
        Args:
            source_name: Source node name
            source_id: Source node ID
            target_name: Target node name
            target_id: Target node ID
            relationship_type: Type of relationship
            
        Returns:
            Formatted relationship prompt
        """
        return self.format_prompt(
            "relationship_extraction",
            source_name=source_name,
            source_id=source_id,
            target_name=target_name,
            target_id=target_id,
            relationship_type=relationship_type
        )

    def get_related_analysis_prompt(
        self,
        node_name: str,
        node_id: str,
        relationship_type: Optional[str] = None,
        depth: int = 1
    ) -> str:
        """Get formatted prompt for related knowledge analysis.
        
        Args:
            node_name: Root node name
            node_id: Root node ID
            relationship_type: Optional relationship filter
            depth: Traversal depth
            
        Returns:
            Formatted analysis prompt
        """
        return self.format_prompt(
            "related_knowledge_analysis",
            node_name=node_name,
            node_id=node_id,
            relationship_type=relationship_type or "All types",
            depth=depth
        )

    def clear_cache(self):
        """Clear the prompt template cache."""
        self.load_prompt.cache_clear()
        self._template_cache.clear()


# Global prompt manager instance
_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """Get or create the global prompt manager instance.
    
    Returns:
        Global PromptManager instance
    """
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
