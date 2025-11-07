"""Test if all services are running."""
import asyncio
import asyncpg
import aioredis
from neo4j import GraphDatabase

async def test_services():
    """Test database connections."""

    # Test PostgreSQL
    try:
        conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/medixlm')
        await conn.close()
        print("✅ PostgreSQL: OK")
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")

    # Test Redis
    try:
        redis = await aioredis.from_url('redis://localhost:6379/0')
        await redis.ping()
        await redis.close()
        print("✅ Redis: OK")
    except Exception as e:
        print(f"❌ Redis: {e}")

    # Test Neo4j
    try:
        driver = GraphDatabase.driver('neo4j://localhost:7687', auth=('neo4j', 'medixlm123'))
        with driver.session() as session:
            session.run('RETURN 1')
        driver.close()
        print("✅ Neo4j: OK")
    except Exception as e:
        print(f"❌ Neo4j: {e}")

if __name__ == "__main__":
    asyncio.run(test_services())
