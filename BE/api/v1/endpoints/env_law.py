"""Environmental Law chatbot API endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from infrastructure.knowledge_graph import get_neo4j_driver
from infrastructure.services.ollama_service import OllamaService
from infrastructure.services.cache_service import get_cache_service
from infrastructure.cache import get_redis_client
from domain.reasoner.kg_reasoner import KGReasoner


router = APIRouter(prefix="/env-law", tags=["env-law"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    question: str
    stream: bool = False


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    answer: str
    success: bool = True
    error: str | None = None
    cached: bool = False


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer questions about Environmental Protection Law 2020.
    
    This endpoint queries the Neo4j Knowledge Graph and uses Ollama Qwen
    to format responses. All knowledge comes from the KG - no hallucination.
    Results are cached in Redis for faster subsequent responses.
    
    Args:
        request: ChatRequest with question and optional stream flag
        
    Returns:
        ChatResponse with formatted answer
    """
    try:
        driver = get_neo4j_driver()
        ollama = OllamaService()
        cache_service = get_cache_service()
        reasoner = KGReasoner(driver, ollama, cache_service)
        
        # Check if answer is cached (for response metadata)
        cached_answer = await cache_service.get_cached_answer(request.question)
        is_cached = cached_answer is not None
        
        if request.stream:
            # Return streaming response
            async def generate():
                async for chunk in reasoner.answer_stream(request.question):
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        
        # Non-streaming response
        answer = await reasoner.answer(request.question)
        return ChatResponse(answer=answer, cached=is_cached)
        
    except RuntimeError as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Service unavailable: {str(e)}"
        )
    except Exception as e:
        return ChatResponse(
            answer="",
            success=False,
            error=f"Lỗi xử lý câu hỏi: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Check health of env-law service including Redis cache."""
    result = {
        "status": "healthy",
        "neo4j": "unknown",
        "ollama": "unknown",
        "redis": "unknown"
    }
    
    try:
        # Check Neo4j
        driver = get_neo4j_driver()
        async with driver.session() as session:
            await session.run("RETURN 1 as test")
        result["neo4j"] = "connected"
    except Exception as e:
        result["neo4j"] = f"error: {str(e)}"
        result["status"] = "degraded"
    
    try:
        # Check Ollama
        ollama = OllamaService()
        ollama_ok = await ollama.health_check()
        result["ollama"] = "connected" if ollama_ok else "disconnected"
        if not ollama_ok:
            result["status"] = "degraded"
    except Exception as e:
        result["ollama"] = f"error: {str(e)}"
        result["status"] = "degraded"
    
    try:
        # Check Redis
        redis = get_redis_client()
        await redis.ping()
        result["redis"] = "connected"
        
        # Get cache stats
        cache_service = get_cache_service()
        cache_stats = await cache_service.get_stats()
        result["cache_stats"] = cache_stats
    except RuntimeError:
        result["redis"] = "not initialized"
    except Exception as e:
        result["redis"] = f"error: {str(e)}"
        result["status"] = "degraded"
    
    return result


@router.delete("/cache")
async def clear_cache():
    """Clear all cached answers (admin endpoint)."""
    try:
        cache_service = get_cache_service()
        await cache_service.clear_all()
        return {"status": "success", "message": "Cache cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )
