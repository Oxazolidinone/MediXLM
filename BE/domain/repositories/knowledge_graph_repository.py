"""Knowledge Graph repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple

from domain.entities.env_law_knowledge import EnvLawKnowledge, KnowledgeType


class IKnowledgeGraphRepository(ABC):
    @abstractmethod
    async def get_node_by_id(self, node_id: str) -> Optional[EnvLawKnowledge]:
        pass

    @abstractmethod
    async def search_full_text(self, query: str, limit: int = 10) -> List[Tuple[EnvLawKnowledge, float]]:
        """Search using Full Text Index."""
        pass
        
    @abstractmethod
    async def search_by_name(self, name: str, knowledge_type: Optional[KnowledgeType] = None) -> List[EnvLawKnowledge]:
        pass

    @abstractmethod
    async def get_node_full_context(self, node_id: str) -> Dict[str, Any]:
        """Get node properties and all incoming/outgoing relationships."""
        pass

    @abstractmethod
    async def get_related_nodes(self, node_id: str, relationship_type: Optional[str] = None, depth: int = 1) -> List[EnvLawKnowledge]:
        pass

    # Specific queries for EnvLaw
    @abstractmethod
    async def get_obligations(self, subject: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_rights(self, subject: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_consequences(self, action: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_agencies(self) -> List[EnvLawKnowledge]:
        pass
    
    @abstractmethod
    async def get_all_by_type(self, knowledge_type: KnowledgeType) -> List[EnvLawKnowledge]:
        pass
