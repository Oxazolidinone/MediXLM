# infrastructure/services/rag_service.py

## Mục đích
File này implements RAG (Retrieval-Augmented Generation) service - core component kết hợp semantic search với LLM generation. RAGService retrieves relevant medical knowledge từ Qdrant vector database dựa trên user query, format knowledge thành context cho LLM prompts. Đây là bridge giữa knowledge base và chat system.

## Chức năng chính

### RAGService Class

#### __init__(qdrant_client: QdrantClient)
Initialize RAG service:
- Store Qdrant client reference
- Get global embedding service instance
- Store collection name từ settings

#### search_knowledge(query, limit, score_threshold) -> List[Dict]
Search relevant knowledge trong vector database:
1. **Embed query**: Generate embedding vector cho search query
2. **Similarity search**: Query Qdrant với cosine similarity
3. **Filter by score**: Only return results above threshold (default 0.5)
4. **Extract results**: Format results với text, source, score, metadata
5. **Error handling**: Return empty list on errors (graceful degradation)

Returns list of knowledge items:
```python
{
    "text": "Medical knowledge text...",
    "source": "WHO Guidelines 2023",
    "score": 0.87,
    "metadata": {...}
}
```

#### format_knowledge_context(knowledge_list) -> str
Format retrieved knowledge cho LLM prompt:
- Return empty string nếu no knowledge
- Create structured context với headers
- Number each knowledge item
- Include relevance score
- Add source attribution
- Add instruction để cite sources

Output format:
```
=== Relevant Medical Knowledge ===

[1] (Relevance: 0.87)
[Knowledge text]
Source: WHO Guidelines

[2] (Relevance: 0.75)
[Knowledge text]
Source: Mayo Clinic

=== End of Knowledge ===
Please use the above medical knowledge...
```

#### get_context_for_chat(user_message, max_results) -> Dict
High-level method cho chat integration:
1. Search knowledge based on user message
2. Format knowledge into context string
3. Return dict với:
   - `knowledge`: Raw knowledge list
   - `context`: Formatted context string
   - `has_knowledge`: Boolean flag

## Liên kết với các file khác

### Dependencies
- **qdrant_client**: QdrantClient - Vector database client
- **core.config**: settings - Collection name
- **.embedding_service**: get_embedding_service - Get embeddings

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Retrieve knowledge context cho chat responses (currently commented out)
- **api/v1/endpoints/chat.py**: May directly use RAG service

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - RAG System Completely Lost

Nếu bị xóa:
- **RAG không hoạt động**: Chat responses không có medical knowledge context
- **Semantic search lost**: Không retrieve relevant knowledge
- **Chat quality giảm cực kỳ nghiêm trọng**: Responses based on LLM knowledge only, không grounded in medical facts
- **Source attribution impossible**: Không cite medical sources
- **Core value proposition lost**: MediXLM differentiator là medical knowledge integration

### Cách thay thế
1. Recreate RAGService với Qdrant search
2. Implement alternative với different vector DB
3. Use external RAG services (LlamaIndex, LangChain)

## Technical Notes

### Semantic Search Flow
```
User Query → Embedding → Vector Search → Top K Results → Format Context → LLM Prompt
```

### Score Threshold
- **High threshold (>0.7)**: Only very relevant knowledge
- **Medium threshold (0.5-0.7)**: Moderately relevant
- **Low threshold (<0.5)**: May include less relevant knowledge

Default 0.5 balances precision và recall.

### Error Handling
Graceful degradation on errors:
- Vector DB unavailable → Return empty list
- Embedding fails → Return empty list
- Chat continues without RAG context

### Context Size
Limited to `max_results` (default 3) để:
- Avoid overwhelming LLM context
- Reduce token usage
- Focus on most relevant knowledge

## RAG Best Practices

### Query Optimization
Transform user query để better search:
```python
# User: "I have fever"
# Optimized: "fever symptoms causes treatment"
```

### Reranking
Consider adding reranking step:
1. Initial broad search (get 10 results)
2. Rerank với cross-encoder model
3. Return top 3 results

### Hybrid Search
Combine vector search với keyword search:
- Vector search: Semantic similarity
- Keyword search: Exact matches
- Combine scores

### Knowledge Freshness
Track knowledge update dates:
- Prefer recent knowledge
- Flag outdated information

## Future Improvements

1. **Query expansion**: Expand user query với synonyms, related terms
2. **Reranking**: Add cross-encoder reranking cho better results
3. **Hybrid search**: Combine semantic + keyword search
4. **Metadata filtering**: Filter by knowledge type, source, date
5. **Context compression**: Summarize knowledge nếu too long
6. **Multi-hop retrieval**: Follow knowledge graph relationships
7. **Feedback loop**: Learn từ user feedback on results
8. **A/B testing**: Test different retrieval strategies
9. **Knowledge caching**: Cache frequently retrieved knowledge
10. **Multilingual search**: Support Vietnamese queries

## Integration Example

```python
# In chat use case
rag_service = RAGService(qdrant_client)
context_data = rag_service.get_context_for_chat(
    user_message="What are diabetes symptoms?",
    max_results=3
)

if context_data["has_knowledge"]:
    system_prompt = base_prompt + context_data["context"]
    response = llm.generate(system_prompt, messages)
else:
    # No relevant knowledge found
    response = llm.generate(base_prompt, messages)
```
