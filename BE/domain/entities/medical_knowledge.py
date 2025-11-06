"""Medical Knowledge entity for Knowledge Graph."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from uuid import UUID, uuid4


class KnowledgeType(str, Enum):
    """Knowledge type enumeration."""
    DISEASE = "disease"
    SYMPTOM = "symptom"
    TREATMENT = "treatment"
    MEDICATION = "medication"
    PROCEDURE = "procedure"
    ANATOMY = "anatomy"
    TEST = "test"


@dataclass
class MedicalKnowledge:
    """Medical Knowledge domain entity for Knowledge Graph nodes."""

    id: UUID
    name: str
    knowledge_type: KnowledgeType
    description: Optional[str] = None
    properties: Dict[str, Any] = None
    embeddings: Optional[List[float]] = None
    created_at: datetime = None
    updated_at: datetime = None
    source: Optional[str] = None
    confidence_score: float = 1.0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.properties is None:
            self.properties = {}

    @staticmethod
    def create(
        name: str,
        knowledge_type: KnowledgeType,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        confidence_score: float = 1.0
    ) -> "MedicalKnowledge":
        """Create a new medical knowledge entity."""
        return MedicalKnowledge(
            id=uuid4(),
            name=name,
            knowledge_type=knowledge_type,
            description=description,
            properties=properties or {},
            source=source,
            confidence_score=confidence_score,
        )

    def update_embeddings(self, embeddings: List[float]):
        """Update embeddings for vector search."""
        self.embeddings = embeddings
        self.updated_at = datetime.utcnow()

    def update_properties(self, properties: Dict[str, Any]):
        """Update knowledge properties."""
        self.properties.update(properties)
        self.updated_at = datetime.utcnow()
