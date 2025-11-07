from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.logging import setup_logging, get_logger
from infrastructure.cache import init_redis, close_redis
from infrastructure.database import init_database, close_database
from infrastructure.knowledge_graph import init_neo4j, close_neo4j
from infrastructure.vector_db import init_milvus, close_milvus
from infrastructure.vector_db import init_qdrant, close_qdrant
from api.v1 import api_router

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting MediXLM application...")
    try:
        await init_database()
        await init_redis()
        await init_neo4j()
        await init_qdrant()

        logger.info("MediXLM application started successfully!")

    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

    yield
    logger.info("Shutting down MediXLM application...")

    try:
        await close_database()
        await close_redis()
        await close_neo4j()
        await close_qdrant()

        logger.info("MediXLM application shutdown successfully!")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "MediXLM Team",
        "email": "support@medixlm.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://medixlm.com/terms",
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and system status endpoints",
        },
        {
            "name": "chat",
            "description": "Chat operations including message processing and conversation history",
        },
        {
            "name": "knowledge",
            "description": "Medical knowledge graph operations including CRUD, search, and relationships",
        },
        {
            "name": "users",
            "description": "User management operations",
        },
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

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
