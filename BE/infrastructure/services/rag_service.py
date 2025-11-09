"""RAG (Retrieval-Augmented Generation) service."""
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from core.config import settings
from .embedding_service import get_embedding_service


class RAGService:
    """Service for retrieving relevant knowledge from vector database."""

    def __init__(self, qdrant_client: QdrantClient):
        """
        Initialize RAG service.

        Args:
            qdrant_client: QdrantClient instance
        """
        self.qdrant = qdrant_client
        self.embedding_service = get_embedding_service()
        self.collection_name = settings.QDRANT_COLLECTION_NAME

    def search_knowledge(
        self,
        query: str,
        limit: int = 3,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant knowledge in vector database.

        Args:
            query: Search query text
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of relevant knowledge with scores
        """
        try:
            print(f"[RAG] Searching for: '{query[:50]}...'")

            # Embed the query
            query_vector = self.embedding_service.embed_text(query)
            print(f"[RAG] Query embedded (dim: {len(query_vector)})")

            # Search in Qdrant
            results = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True
            )

            print(f"[RAG] Found {len(results)} relevant documents")

            # Extract and format results
            knowledge_list = []
            for hit in results:
                knowledge_list.append({
                    "text": hit.payload.get("text", ""),
                    "source": hit.payload.get("source", "Unknown"),
                    "score": hit.score,
                    "metadata": hit.payload.get("metadata", {})
                })

            return knowledge_list

        except Exception as e:
            print(f"[RAG] Search error: {e}")
            # Return empty list on error - chat will continue without RAG
            return []

    def format_knowledge_context(self, knowledge_list: List[Dict]) -> str:
        """
        Format retrieved knowledge for LLM context.

        Args:
            knowledge_list: List of knowledge items from search

        Returns:
            Formatted string to include in system prompt
        """
        if not knowledge_list:
            return ""

        context_parts = ["\n\n=== Relevant Medical Knowledge ==="]

        for i, k in enumerate(knowledge_list, 1):
            score = k.get('score', 0)
            text = k.get('text', '')
            source = k.get('source', 'Unknown')

            context_parts.append(
                f"\n[{i}] (Relevance: {score:.2f})\n{text}\nSource: {source}"
            )

        context_parts.append("\n=== End of Knowledge ===\n")
        context_parts.append(
            "Please use the above medical knowledge to provide accurate, "
            "evidence-based answers. If the knowledge is relevant, cite it in your response."
        )

        return "\n".join(context_parts)

    def get_context_for_chat(
        self,
        user_message: str,
        max_results: int = 3
    ) -> Dict[str, Any]:
        """
        Get RAG context for chat response.

        Args:
            user_message: User's question/message
            max_results: Maximum knowledge items to retrieve

        Returns:
            Dictionary with knowledge and formatted context
        """
        knowledge = self.search_knowledge(user_message, limit=max_results)
        formatted_context = self.format_knowledge_context(knowledge)

        return {
            "knowledge": knowledge,
            "context": formatted_context,
            "has_knowledge": len(knowledge) > 0
        }
