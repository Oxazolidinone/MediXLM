"""Neo4j client management for Knowledge Graph."""
from typing import Optional

from neo4j import AsyncGraphDatabase, AsyncDriver

from core.config import settings

# Global Neo4j driver
neo4j_driver: Optional[AsyncDriver] = None


async def init_neo4j():
    """Initialize Neo4j connection."""
    global neo4j_driver

    neo4j_driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        max_connection_pool_size=settings.NEO4J_MAX_POOL_SIZE,
    )

    # Verify connection
    await neo4j_driver.verify_connectivity()


async def close_neo4j():
    """Close Neo4j connection."""
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()


def get_neo4j_driver() -> AsyncDriver:
    """Get Neo4j driver."""
    if neo4j_driver is None:
        raise RuntimeError("Neo4j driver not initialized. Call init_neo4j() first.")
    return neo4j_driver
