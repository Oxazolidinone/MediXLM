import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Force UTF-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

from infrastructure.database import init_database, close_database
from infrastructure.knowledge_graph import init_neo4j, close_neo4j
from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
from infrastructure.services.local_llm_service import LocalLLMService
from infrastructure.services.env_law_service import EnvLawChatbotService

async def verify_chatbot():
    print("Initializing services (Mock mode)...")
    
    # Mock Repository
    class MockKGRepo:
        pass
        
    try:
        llm_service = LocalLLMService()
        kg_repo = MockKGRepo() # Mock
        chatbot_service = EnvLawChatbotService(kg_repo, llm_service)
        
        test_questions = [
            "Ai phải nộp thuế bảo vệ môi trường?",
            "Doanh nghiệp có phải lập báo cáo đánh giá tác động môi trường không?",
            "Cá nhân có được nhập khẩu vũ khí hạt nhân không?", # Should return NO BASIS
            "Chủ nguồn thải chất thải nguy hại là ai?",
            # Previous regression tests
            "Hành vi xả thải bị phạt thế nào?",
        ]
        
        for q in test_questions:
            print(f"\n--- Testing: {q} ---")
            intent, entity = chatbot_service.detect_intent(q)
            print(f"Detected Intent: {intent}")
            print(f"Detected Entity: {entity}")

    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    asyncio.run(verify_chatbot())
