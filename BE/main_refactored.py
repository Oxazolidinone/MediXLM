"""
Main entry point for Environmental Law Chatbot (Refactored Layered Architecture).
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stdin.reconfigure(encoding='utf-8')

from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
from infrastructure.services.env_law_service import EnvLawChatbotService
from infrastructure.services.local_llm_service import LocalLLMService

# Config
load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

async def main():
    print("=" * 60)
    print("CHATBOT LUẬT BVMT 2020 - LAYERED ARCHITECTURE (W/ FTS)")
    print("=" * 60)
    
    driver = None
    try:
        # 1. Initialize Infrastructure
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        await driver.verify_connectivity()
        print("[OK] Connected to Neo4j")
        
        # 2. Dependency Injection
        repo = KnowledgeGraphRepositoryImpl(driver)
        llm_service = LocalLLMService()
        service = EnvLawChatbotService(repo, llm_service)
        
        print("[OK] Service Initialized")
        print("\nSẵn sàng! Nhập 'exit' để thoát.")
        
        # 3. CLI Loop
        while True:
            q = input("\nCâu hỏi: ").strip()
            if q.lower() in ['exit', 'quit', 'q']:
                break
            if not q:
                continue
            
            print("Đang xử lý...")
            answer = await service.answer_question(q)
            print(f"\nTrả lời:\n{answer}")
            
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if driver:
            await driver.close()
            print("\n[INFO] Connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
