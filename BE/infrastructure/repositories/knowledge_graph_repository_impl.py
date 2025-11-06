"""Knowledge Graph repository implementation using Neo4j."""
from typing import List, Optional, Dict, Any
from uuid import UUID

from neo4j import AsyncDriver

from domain.entities import MedicalKnowledge
from domain.entities.medical_knowledge import KnowledgeType
from domain.repositories import IKnowledgeGraphRepository


class KnowledgeGraphRepositoryImpl(IKnowledgeGraphRepository):
    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    async def create_node(self, knowledge: MedicalKnowledge) -> MedicalKnowledge:
        query = """
        CREATE (n:MedicalKnowledge {
            id: $id,
            name: $name,
            knowledge_type: $knowledge_type,
            description: $description,
            properties: $properties,
            embeddings: $embeddings,
            created_at: datetime($created_at),
            updated_at: datetime($updated_at),
            source: $source,
            confidence_score: $confidence_score
        })
        RETURN n
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                id=str(knowledge.id),
                name=knowledge.name,
                knowledge_type=knowledge.knowledge_type.value,
                description=knowledge.description,
                properties=knowledge.properties,
                embeddings=knowledge.embeddings,
                created_at=knowledge.created_at.isoformat(),
                updated_at=knowledge.updated_at.isoformat(),
                source=knowledge.source,
                confidence_score=knowledge.confidence_score,
            )
            await result.consume()

        return knowledge

    async def get_node_by_id(self, node_id: UUID) -> Optional[MedicalKnowledge]:
        query = """
        MATCH (n:MedicalKnowledge {id: $id})
        RETURN n
        """

        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            record = await result.single()

            if record:
                return self._to_entity(record["n"])
            return None

    async def search_by_name(self, name: str, knowledge_type: Optional[KnowledgeType] = None) -> List[MedicalKnowledge]:    
        if knowledge_type:
            query = """
            MATCH (n:MedicalKnowledge)
            WHERE n.name CONTAINS $name AND n.knowledge_type = $knowledge_type
            RETURN n
            LIMIT 20
            """
            params = {"name": name, "knowledge_type": knowledge_type.value}
        else:
            query = """
            MATCH (n:MedicalKnowledge)
            WHERE n.name CONTAINS $name
            RETURN n
            LIMIT 20
            """
            params = {"name": name}

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            records = await result.values()

            return [self._to_entity(record[0]) for record in records]

    async def create_relationship(self, source_id: UUID, target_id: UUID, relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> bool:
        query = """
        MATCH (source:MedicalKnowledge {id: $source_id})
        MATCH (target:MedicalKnowledge {id: $target_id})
        CREATE (source)-[r:%s $properties]->(target)
        RETURN r
        """ % relationship_type

        async with self.driver.session() as session:
            result = await session.run(
                query,
                source_id=str(source_id),
                target_id=str(target_id),
                properties=properties or {},
            )
            record = await result.single()
            return record is not None

    async def get_related_nodes(self, node_id: UUID, relationship_type: Optional[str] = None, depth: int = 1) -> List[MedicalKnowledge]:
        if relationship_type:
            query = """
            MATCH (n:MedicalKnowledge {id: $id})-[r:%s*1..%d]-(related:MedicalKnowledge)
            RETURN DISTINCT related
            """ % (relationship_type, depth)
        else:
            query = """
            MATCH (n:MedicalKnowledge {id: $id})-[*1..%d]-(related:MedicalKnowledge)
            RETURN DISTINCT related
            """ % depth

        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            records = await result.values()

            return [self._to_entity(record[0]) for record in records]

    async def similarity_search(self, embeddings: List[float], knowledge_type: Optional[KnowledgeType] = None, limit: int = 10) -> List[MedicalKnowledge]:
        if knowledge_type:
            query = """
            MATCH (n:MedicalKnowledge {knowledge_type: $knowledge_type})
            WHERE n.embeddings IS NOT NULL
            RETURN n, gds.similarity.cosine(n.embeddings, $embeddings) AS score
            ORDER BY score DESC
            LIMIT $limit
            """
            params = {
                "embeddings": embeddings,
                "knowledge_type": knowledge_type.value,
                "limit": limit,
            }
        else:
            query = """
            MATCH (n:MedicalKnowledge)
            WHERE n.embeddings IS NOT NULL
            RETURN n, gds.similarity.cosine(n.embeddings, $embeddings) AS score
            ORDER BY score DESC
            LIMIT $limit
            """
            params = {"embeddings": embeddings, "limit": limit}

        async with self.driver.session() as session:
            result = await session.run(query, **params)
            records = await result.values()

            return [self._to_entity(record[0]) for record in records]

    async def update_node(self, knowledge: MedicalKnowledge) -> MedicalKnowledge:
        query = """
        MATCH (n:MedicalKnowledge {id: $id})
        SET n.name = $name,
            n.knowledge_type = $knowledge_type,
            n.description = $description,
            n.properties = $properties,
            n.embeddings = $embeddings,
            n.updated_at = datetime($updated_at),
            n.source = $source,
            n.confidence_score = $confidence_score
        RETURN n
        """

        async with self.driver.session() as session:
            result = await session.run(
                query,
                id=str(knowledge.id),
                name=knowledge.name,
                knowledge_type=knowledge.knowledge_type.value,
                description=knowledge.description,
                properties=knowledge.properties,
                embeddings=knowledge.embeddings,
                updated_at=knowledge.updated_at.isoformat(),
                source=knowledge.source,
                confidence_score=knowledge.confidence_score,
            )
            await result.consume()

        return knowledge

    async def delete_node(self, node_id: UUID) -> bool:
        query = """
        MATCH (n:MedicalKnowledge {id: $id})
        DETACH DELETE n
        RETURN count(n) as deleted
        """

        async with self.driver.session() as session:
            result = await session.run(query, id=str(node_id))
            record = await result.single()
            return record["deleted"] > 0 if record else False

    @staticmethod
    def _to_entity(node) -> MedicalKnowledge:
        from datetime import datetime

        return MedicalKnowledge(
            id=UUID(node["id"]),
            name=node["name"],
            knowledge_type=KnowledgeType(node["knowledge_type"]),
            description=node.get("description"),
            properties=node.get("properties", {}),
            embeddings=node.get("embeddings"),
            created_at=datetime.fromisoformat(node["created_at"])
            if isinstance(node["created_at"], str)
            else node["created_at"],
            updated_at=datetime.fromisoformat(node["updated_at"])
            if isinstance(node["updated_at"], str)
            else node["updated_at"],
            source=node.get("source"),
            confidence_score=node.get("confidence_score", 1.0),
        )
