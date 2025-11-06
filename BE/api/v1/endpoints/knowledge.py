"""Knowledge Graph endpoints."""
from typing import Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.use_cases import KnowledgeUseCase
from domain.entities.medical_knowledge import KnowledgeType
from core.exceptions import KnowledgeNotFoundError
from presentation.api.dependencies import get_knowledge_use_case

router = APIRouter()


class KnowledgeCreate(BaseModel):
    name: str
    knowledge_type: str
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    source: Optional[str] = None


class KnowledgeResponse(BaseModel):
    id: UUID
    name: str
    knowledge_type: str
    description: Optional[str]
    properties: Optional[Dict[str, Any]]
    confidence_score: float


class RelationshipCreate(BaseModel):
    source_id: UUID
    target_id: UUID
    relationship_type: str
    properties: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    query: str
    knowledge_type: Optional[str] = None
    limit: int = 10


@router.post("/", response_model=KnowledgeResponse, status_code=status.HTTP_201_CREATED)
async def add_knowledge(
    knowledge_data: KnowledgeCreate,
    knowledge_use_case: KnowledgeUseCase = Depends(get_knowledge_use_case),
):
    """Add new medical knowledge to the graph."""
    try:
        knowledge_type = KnowledgeType(knowledge_data.knowledge_type)

        result = await knowledge_use_case.add_knowledge(
            name=knowledge_data.name,
            knowledge_type=knowledge_type,
            description=knowledge_data.description,
            properties=knowledge_data.properties,
            source=knowledge_data.source,
        )

        return KnowledgeResponse(
            id=result.id,
            name=result.name,
            knowledge_type=result.knowledge_type.value,
            description=result.description,
            properties=result.properties,
            confidence_score=result.confidence_score,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid knowledge type: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/relationships", status_code=status.HTTP_201_CREATED)
async def create_relationship(
    relationship_data: RelationshipCreate,
    knowledge_use_case: KnowledgeUseCase = Depends(get_knowledge_use_case),
):
    """Create a relationship between two knowledge nodes."""
    try:
        success = await knowledge_use_case.link_knowledge(
            source_id=relationship_data.source_id,
            target_id=relationship_data.target_id,
            relationship_type=relationship_data.relationship_type,
            properties=relationship_data.properties,
        )

        if success:
            return {"message": "Relationship created successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create relationship",
            )

    except KnowledgeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/search", response_model=list[KnowledgeResponse])
async def search_knowledge(
    search_request: SearchRequest,
    knowledge_use_case: KnowledgeUseCase = Depends(get_knowledge_use_case),
):
    """Search for medical knowledge using semantic search."""
    try:
        knowledge_type = (
            KnowledgeType(search_request.knowledge_type)
            if search_request.knowledge_type
            else None
        )

        results = await knowledge_use_case.search_knowledge(
            query=search_request.query,
            knowledge_type=knowledge_type,
            limit=search_request.limit,
        )

        return [
            KnowledgeResponse(
                id=k.id,
                name=k.name,
                knowledge_type=k.knowledge_type.value,
                description=k.description,
                properties=k.properties,
                confidence_score=k.confidence_score,
            )
            for k in results
        ]

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid knowledge type: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{node_id}/related", response_model=list[KnowledgeResponse])
async def get_related_knowledge(
    node_id: UUID,
    relationship_type: Optional[str] = None,
    depth: int = 1,
    knowledge_use_case: KnowledgeUseCase = Depends(get_knowledge_use_case),
):
    """Get knowledge nodes related to a given node."""
    try:
        results = await knowledge_use_case.get_related_knowledge(
            node_id=node_id,
            relationship_type=relationship_type,
            depth=depth,
        )

        return [
            KnowledgeResponse(
                id=k.id,
                name=k.name,
                knowledge_type=k.knowledge_type.value,
                description=k.description,
                properties=k.properties,
                confidence_score=k.confidence_score,
            )
            for k in results
        ]

    except KnowledgeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
