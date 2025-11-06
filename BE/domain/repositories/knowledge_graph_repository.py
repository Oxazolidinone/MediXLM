"""Knowledge Graph repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from domain.entities import MedicalKnowledge
from domain.entities.medical_knowledge import KnowledgeType


class IKnowledgeGraphRepository(ABC):
    """Interface for Knowledge Graph repository."""

    @abstractmethod
    async def create_node(self, knowledge: MedicalKnowledge) -> MedicalKnowledge:
        """Create a new knowledge node."""
        pass

    @abstractmethod
    async def get_node_by_id(self, node_id: UUID) -> Optional[MedicalKnowledge]:
        """Get knowledge node by ID."""
        pass

    @abstractmethod
    async def search_by_name(self, name: str, knowledge_type: Optional[KnowledgeType] = None) -> List[MedicalKnowledge]:
        """Search knowledge nodes by name."""
        pass

    @abstractmethod
    async def create_relationship(
        self,
        source_id: UUID,
        target_id: UUID,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create relationship between two knowledge nodes."""
        pass

    @abstractmethod
    async def get_related_nodes(
        self,
        node_id: UUID,
        relationship_type: Optional[str] = None,
        depth: int = 1
    ) -> List[MedicalKnowledge]:
        """Get related knowledge nodes."""
        pass

    @abstractmethod
    async def similarity_search(
        self,
        embeddings: List[float],
        knowledge_type: Optional[KnowledgeType] = None,
        limit: int = 10
    ) -> List[MedicalKnowledge]:
        """Perform vector similarity search."""
        pass

    @abstractmethod
    async def update_node(self, knowledge: MedicalKnowledge) -> MedicalKnowledge:
        """Update knowledge node."""
        pass

    @abstractmethod
    async def delete_node(self, node_id: UUID) -> bool:
        """Delete knowledge node."""
        pass
