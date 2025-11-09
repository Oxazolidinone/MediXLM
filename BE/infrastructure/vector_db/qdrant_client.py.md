# infrastructure/vector_db/qdrant_client.py

## Mục đích
File này quản lý Qdrant vector database client cho RAG system. Qdrant stores medical knowledge embeddings và provides fast similarity search. Connects to Qdrant Cloud với API key authentication.

## Chức năng chính

### Global Variable
- **_qdrant_client**: Global QdrantClient instance

### init_qdrant()
Async function initialize Qdrant connection:
- Create QdrantClient với URL và API key
- Check nếu collection exists
- Create collection nếu chưa có với:
  - Vector size: 384 (embedding dimension)
  - Distance metric: COSINE similarity
- Handle errors gracefully (continue nếu unavailable)

### close_qdrant()
Close Qdrant connection (set client to None).

### get_qdrant_client() -> QdrantClient
Get global Qdrant client:
- Return _qdrant_client
- Raise RuntimeError nếu not initialized

## Liên kết với các file khác

### Dependencies
- **qdrant_client**: QdrantClient, models
- **core.config**: settings - Qdrant URL, API key, collection name

### Được sử dụng bởi
- **main.py**: Initialize/close Qdrant
- **infrastructure/services/rag_service.py**: Similarity search
- **scripts/seed_medical_knowledge.py**: Upload embeddings

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Vector Database Access Lost

Nếu bị xóa:
- **RAG system không hoạt động**: Không similarity search
- **Medical knowledge retrieval fails**: Không retrieve relevant knowledge
- **Chat responses không có knowledge context**: Quality giảm nghiêm trọng

### Cách thay thế
Recreate Qdrant client với collection initialization.
