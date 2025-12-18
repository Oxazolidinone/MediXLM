
import asyncio
import os
import json
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv
from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
from domain.entities.env_law_knowledge import KnowledgeType

# Load env from BE/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))

async def test_rebuild():
    print(f"Connecting to {URI}...")
    driver = AsyncGraphDatabase.driver(URI, auth=AUTH)
    repo = KnowledgeGraphRepositoryImpl(driver)
    
    try:
        print("\n--- Testing get_obligations('Tổ chức') ---")
        obs = await repo.get_obligations("Tổ chức")
        print(f"Found {len(obs)} obligations.")
        if obs:
            print(json.dumps(obs[0], ensure_ascii=False, indent=2))
            
        print("\n--- Testing get_consequences('xả thải') ---")
        cons = await repo.get_consequences("xả thải")
        print(f"Found {len(cons)} consequences.")
        if cons:
            print(json.dumps(cons[0], ensure_ascii=False, indent=2))
            
        print("\n--- Testing search_full_text('môi trường') ---")
        # Note: 'môi trường' might match many concepts
        results = await repo.search_full_text("môi trường", limit=3)
        print(f"Found {len(results)} results.")
        for entity, score in results:
            print(f"- [{entity.knowledge_type.value}] {entity.name} (Score: {score:.2f})")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await driver.close()

if __name__ == "__main__":
    asyncio.run(test_rebuild())
