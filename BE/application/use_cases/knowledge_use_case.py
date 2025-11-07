"""Knowledge use case."""
from typing import List, Optional, Dict, Any
from uuid import UUID

from infrastructure.services import LLMService
from domain.entities import MedicalKnowledge
from domain.entities.medical_knowledge import KnowledgeType
from domain.repositories import IKnowledgeGraphRepository
from core.exceptions import KnowledgeNotFoundError


class KnowledgeUseCase:
    def __init__( self, knowledge_graph_repository: IKnowledgeGraphRepository, embedding_service: LLMService):
        self.kg_repo = knowledge_graph_repository
        self.embedding_service = embedding_service

    async def add_knowledge(self, name: str, knowledge_type: KnowledgeType, description: Optional[str] = None, properties: Optional[Dict[str, Any]] = None, source: Optional[str] = None) -> MedicalKnowledge:
        knowledge = MedicalKnowledge.create(
            name=name,
            knowledge_type=knowledge_type,
            description=description,
            properties=properties,
            source=source,
        )

        # Generate embeddings
        text_for_embedding = f"{name}. {description or ''}"
        embeddings = await self.embedding_service.generate_embeddings(text_for_embedding)
        knowledge.update_embeddings(embeddings)

        # Save to knowledge graph
        created_knowledge = await self.kg_repo.create_node(knowledge)

        return created_knowledge

    async def link_knowledge(
        self,
        source_id: UUID,
        target_id: UUID,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Create a relationship between two knowledge nodes."""

        # Verify both nodes exist
        source = await self.kg_repo.get_node_by_id(source_id)
        if not source:
            raise KnowledgeNotFoundError(f"Source knowledge {source_id} not found")

        target = await self.kg_repo.get_node_by_id(target_id)
        if not target:
            raise KnowledgeNotFoundError(f"Target knowledge {target_id} not found")

        # Create relationship
        return await self.kg_repo.create_relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties,
        )

    async def search_knowledge(
        self,
        query: str,
        knowledge_type: Optional[KnowledgeType] = None,
        limit: int = 10,
    ) -> List[MedicalKnowledge]:
        """Search for medical knowledge using semantic search."""

        # Generate embeddings for query
        embeddings = await self.embedding_service.generate_embeddings(query)

        # Perform similarity search
        results = await self.kg_repo.similarity_search(
            embeddings=embeddings,
            knowledge_type=knowledge_type,
            limit=limit,
        )

        return results

    async def get_related_knowledge(
        self,
        node_id: UUID,
        relationship_type: Optional[str] = None,
        depth: int = 1,
    ) -> List[MedicalKnowledge]:
        """Get knowledge nodes related to a given node."""

        # Verify node exists
        node = await self.kg_repo.get_node_by_id(node_id)
        if not node:
            raise KnowledgeNotFoundError(f"Knowledge {node_id} not found")

        # Get related nodes
        related = await self.kg_repo.get_related_nodes(
            node_id=node_id,
            relationship_type=relationship_type,
            depth=depth,
        )

        return related

    async def get_knowledge_by_name(
        self,
        name: str,
        knowledge_type: Optional[KnowledgeType] = None,
    ) -> List[MedicalKnowledge]:
        """Search knowledge by name."""
        return await self.kg_repo.search_by_name(name=name, knowledge_type=knowledge_type)
