"""Main application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import setup_logging, get_logger
from infrastructure.cache import init_redis, close_redis
from infrastructure.database import init_database, close_database
from infrastructure.knowledge_graph import init_neo4j, close_neo4j
from infrastructure.vector_db import init_milvus, close_milvus
from presentation.api.v1 import api_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting MediXLM application...")

    try:
        # Initialize database
        logger.info("Initializing database...")
        await init_database()

        # Initialize Redis cache
        logger.info("Initializing Redis cache...")
        await init_redis()

        # Initialize Neo4j knowledge graph
        logger.info("Initializing Neo4j knowledge graph...")
        await init_neo4j()

        # Initialize Milvus vector database
        logger.info("Initializing Milvus vector database...")
        await init_milvus()

        logger.info("MediXLM application started successfully!")

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down MediXLM application...")

    try:
        await close_database()
        await close_redis()
        await close_neo4j()
        await close_milvus()

        logger.info("MediXLM application shutdown successfully!")

    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Medical AI Chatbot with Knowledge Graph",
    lifespan=lifespan,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS,
        reload=settings.DEBUG,
    )
