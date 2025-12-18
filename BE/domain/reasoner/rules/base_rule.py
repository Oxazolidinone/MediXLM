"""Base rule class for KG reasoning."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from neo4j import AsyncDriver


class BaseRule(ABC):
    """Abstract base class for all reasoning rules."""
    
    def __init__(self, driver: AsyncDriver):
        self.driver = driver
    
    @property
    @abstractmethod
    def rule_name(self) -> str:
        """Name of this rule."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this rule does."""
        pass
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the rule and return results.
        
        Args:
            params: Parameters for the query (extracted entities, etc.)
            
        Returns:
            List of result dictionaries from Neo4j
        """
        pass
    
    @abstractmethod
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format raw results into readable text for LLM context.
        
        Args:
            results: Raw results from Neo4j query
            
        Returns:
            Formatted text string
        """
        pass
    
    async def _run_query(self, query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Helper to run a Cypher query.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        async with self.driver.session() as session:
            result = await session.run(query, params)
            records = await result.data()
            return records
