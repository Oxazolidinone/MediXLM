# infrastructure/services/embedding_service.py

## Mục đích
File này implements embedding service sử dụng SentenceTransformers. Provides text embedding generation cho semantic search trong RAG system. Uses all-MiniLM-L6-v2 model (384 dimensions) - lightweight và fast model cho production use.

## Chức năng chính

### EmbeddingService Class

#### __init__(model_name: str = None)
Initialize embedding service:
- Load model name từ settings hoặc parameter
- Load SentenceTransformer model
- Print loading info và dimension
- Store dimension (384)

#### embed_text(text: str) -> List[float]
Embed single text string:
- Encode text với model
- Convert numpy array to Python list
- Return embedding vector (384 floats)

#### embed_batch(texts: List[str]) -> List[List[float]]
Embed multiple texts efficiently:
- Batch encoding với batch_size=32
- No progress bar (show_progress_bar=False)
- Convert to list of lists
- Return embeddings

### Global Singleton

#### get_embedding_service() -> EmbeddingService
Get or create global embedding service instance:
- Lazy initialization on first call
- Return cached instance on subsequent calls
- Ensure only one model loaded trong memory

## Liên kết với các file khác

### Dependencies
- **sentence_transformers**: SentenceTransformer - Embedding model
- **core.config**: settings - Model name và dimension

### Được sử dụng bởi
- **infrastructure/services/rag_service.py**: Embed queries cho similarity search
- **application/use_cases/knowledge_use_case.py**: Generate embeddings cho medical knowledge
- **scripts/seed_medical_knowledge.py**: Embed medical documents

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Embedding Generation Lost

Nếu bị xóa:
- **RAG system hoàn toàn không hoạt động**: Không embed queries
- **Knowledge search fails**: Không similarity search without embeddings
- **Cannot add medical knowledge**: Need embeddings để store trong vector DB
- **Chat quality giảm nghiêm trọng**: No semantic search capability

### Cách thay thế
1. Recreate với SentenceTransformer model
2. Use OpenAI embeddings API (costs money)
3. Use other embedding services (Cohere, etc.)

## Technical Notes

### Model Choice: all-MiniLM-L6-v2
- **Fast**: Optimized cho inference speed
- **Lightweight**: Small model size (~90MB)
- **Good quality**: Balances speed và quality
- **384 dimensions**: Smaller than larger models (e.g., 768, 1536)
- **Widely used**: Battle-tested trong production

### Singleton Pattern
Global instance ensures:
- Model loaded once (expensive operation)
- Shared across all services
- Memory efficient

### Batch Processing
Batch encoding significantly faster than loop:
```python
# Slow
embeddings = [embed_text(text) for text in texts]

# Fast
embeddings = embed_batch(texts)
```

## Best Practices

### Normalization
SentenceTransformer automatically normalizes embeddings cho cosine similarity.

### Caching
Consider caching embeddings cho frequently-used queries:
```python
cache_key = f"embed:{hash(text)}"
cached = cache.get(cache_key)
if not cached:
    cached = embed_text(text)
    cache.set(cache_key, cached)
```

### GPU Acceleration
Model automatically uses GPU nếu available, CPU fallback.

## Future Improvements

1. **Add caching**: Cache embeddings cho common queries
2. **Support multiple models**: Allow switching embedding models
3. **Add multilingual model**: Support Vietnamese embeddings
4. **Async interface**: Async embed methods
5. **Batch optimization**: Tune batch size cho optimal performance
6. **Model quantization**: Reduce model size với quantization
7. **Dimension reduction**: PCA/UMAP để reduce dimensions nếu needed
