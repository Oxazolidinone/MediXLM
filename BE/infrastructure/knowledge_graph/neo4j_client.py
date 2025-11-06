from typing import Optional

from neo4j import AsyncGraphDatabase, AsyncDriver

from core.config import settings

# Global Neo4j driver
neo4j_driver: Optional[AsyncDriver] = None


async def init_neo4j():
    """Initialize Neo4j connection to Aura Cloud.

    Connects to Neo4j Aura using neo4j+s:// protocol (secure with TLS).
    Aura automatically manages connection pooling and security.
    """
    global neo4j_driver

    neo4j_driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        max_connection_pool_size=50,  # Aura handles pooling efficiently
        connection_acquisition_timeout=60,  # Cloud connection timeout
        encrypted=True,  # Always encrypted for Aura
    )
    await neo4j_driver.verify_connectivity()


async def close_neo4j():
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()


def get_neo4j_driver() -> AsyncDriver:
    if neo4j_driver is None:
        raise RuntimeError("Neo4j driver not initialized. Call init_neo4j() first.")
    return neo4j_driver
