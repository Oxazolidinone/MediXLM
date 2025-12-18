"""Environmental Law chatbot API endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from infrastructure.knowledge_graph import get_neo4j_driver
from infrastructure.services.ollama_service import OllamaService
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


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Answer questions about Environmental Protection Law 2020.
    
    This endpoint queries the Neo4j Knowledge Graph and uses Ollama Qwen
    to format responses. All knowledge comes from the KG - no hallucination.
    
    Args:
        request: ChatRequest with question and optional stream flag
        
    Returns:
        ChatResponse with formatted answer
    """
    try:
        driver = get_neo4j_driver()
        ollama = OllamaService()
        reasoner = KGReasoner(driver, ollama)
        
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
        return ChatResponse(answer=answer)
        
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
    """Check health of env-law service."""
    try:
        driver = get_neo4j_driver()
        ollama = OllamaService()
        ollama_ok = await ollama.health_check()
        
        # Quick Neo4j check
        async with driver.session() as session:
            result = await session.run("RETURN 1 as test")
            await result.single()
        
        return {
            "status": "healthy",
            "neo4j": "connected",
            "ollama": "connected" if ollama_ok else "disconnected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
