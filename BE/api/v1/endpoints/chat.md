# api/v1/endpoints/chat.py

## Mục đích
REST API endpoints cho chat functionality. Xử lý chat messages với RAG (Retrieval-Augmented Generation), quản lý conversation history, và tích hợp với Qdrant vector database để tìm medical knowledge liên quan.

## Chức năng chính

### 1. POST /chat/ - Send Message và Nhận AI Response
- **Input**: `ChatRequest` (message, conversation_id optional, user_id)
- **Output**: `ChatResponse` (AI response, conversation_id, message_id)
- **Workflow**:
  1. Tạo hoặc lấy existing conversation
  2. Lưu user message vào database
  3. RAG: Search medical knowledge trong Qdrant
  4. Build prompt với knowledge context
  5. Generate response với Ollama LLM
  6. Lưu assistant message vào database
  7. Return response

### 2. POST /chat/test-simple - Test Endpoint
- Test endpoint không cần database
- Trả về mock response
- Dùng để verify API availability

### 3. GET /chat/history/{conversation_id} - Lấy Conversation History
- **Input**: conversation_id, skip, limit
- **Output**: List of messages (user + assistant)
- Pagination support

### 4. GET /chat/test-qdrant - Test Qdrant Connection
- Kiểm tra kết nối Qdrant
- Hiển thị collection info
- Sample 3 documents đầu tiên
- Debug tool để verify RAG setup

## Kiến trúc đặc biệt

### Thread Executor Pattern (Tránh Greenlet Error)
```python
def sync_chat_handler():
    # Synchronous code in thread
    session = get_sync_session()
    # ... process chat ...
    session.commit()
    session.close()

# Run in thread pool
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(None, sync_chat_handler)
```

**Lý do**: Tránh greenlet spawn error khi mix async/sync SQLAlchemy operations

## Liên kết với các file khác

### Dependencies (Import)
- `application/use_cases/chat_use_case.py` - Business logic (chỉ dùng cho history endpoint)
- `application/dto/chat_dto.py` - Data Transfer Objects
- `infrastructure/database/connection.py` - `get_sync_session()` cho sync operations
- `infrastructure/repositories/sync_conversation_repository.py` - Sync DB operations
- `infrastructure/services/rag_service.py` - RAG search và formatting
- `infrastructure/vector_db/qdrant_client.py` - Vector similarity search
- `domain/entities/` - Conversation, Message, MessageRole
- `core/config/settings.py` - Ollama model config
- `api/dependencies.py` - Dependency injection (chỉ cho history endpoint)

### External Services
- **Ollama**: LLM inference (localhost:11434)
- **Qdrant**: Vector similarity search (cloud)
- **PostgreSQL**: Conversation storage (localhost:5433)

### Được sử dụng bởi
- Frontend chat interface
- Mobile apps
- API consumers

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - CHAT FUNCTIONALITY HOÀN TOÀN KHÔNG HOẠT ĐỘNG

Nếu xóa file này:

1. **Không có chat API**: Users không thể chat với AI
2. **Không có conversation management**: Không tạo/quản lý được conversations
3. **RAG không hoạt động**: Không retrieve medical knowledge
4. **Mất history**: Không xem được conversation history
5. **Debug khó khăn**: Mất test endpoints (test-simple, test-qdrant)
6. **Core feature down**: Chat là core feature của ứng dụng

### Business Impact
- **100% loss of main functionality**
- Users không thể sử dụng hệ thống
- Medical consultation không khả dụng

### Cách thay thế
Cần tạo lại chat endpoints với:
- Message handling logic
- RAG integration
- Ollama LLM integration
- Database persistence
- Thread executor pattern (critical!)

## RAG Pipeline Detail

### Step 1: User Message Processing
```python
user_message = Message.create(
    conversation_id=conversation_id,
    role=MessageRole.USER,
    content=request.message,
)
sync_conv_repo.add_message(user_message)
```

### Step 2: RAG Search (Vector Similarity)
```python
rag_service = RAGService(qdrant)
rag_result = rag_service.get_context_for_chat(request.message, max_results=3)

# rag_result = {
#     "has_knowledge": True/False,
#     "context": "formatted knowledge text",
#     "knowledge": [list of relevant docs]
# }
```

### Step 3: Build Enhanced Prompt
```python
system_prompt = "You are MediXLM, a medical AI assistant..."
if rag_context:
    system_prompt += rag_context  # Inject knowledge
```

### Step 4: LLM Generation
```python
response = ollama.chat(
    model=settings.OLLAMA_MODEL,  # qwen2.5:7b
    messages=[
        {"role": "system", "content": system_prompt},
        *conversation_history,
        {"role": "user", "content": request.message}
    ],
    options={"temperature": 0.7, "num_predict": 500}
)
```

### Step 5: Save Response
```python
assistant_message = Message.create(
    conversation_id=conversation_id,
    role=MessageRole.ASSISTANT,
    content=response_text,
)
sync_conv_repo.add_message(assistant_message)
session.commit()
```

## Error Handling

### Graceful Degradation
1. **RAG fails**: Continue without knowledge context
   ```python
   except Exception as rag_error:
       print(f"RAG failed: {rag_error}, continuing without RAG")
   ```

2. **LLM fails**: Return fallback message
   ```python
   except Exception as llm_error:
       response_text = "I apologize, but I'm having trouble..."
   ```

3. **Database fails**: Raise HTTPException 500

### Logging Strategy
- Print statements for debugging (sync context)
- Step-by-step logging: `[SYNC] 1. Creating session...`
- Full traceback on errors

## Performance Considerations

### Thread Pool Execution
- **Pros**: Tránh greenlet error, stable
- **Cons**: Blocking operation trong thread
- **Trade-off**: Chấp nhận blocking để tránh async/sync conflicts

### Database Session Management
```python
try:
    session = get_sync_session()
    # ... operations ...
    session.commit()
finally:
    session.close()  # Always cleanup
```

### RAG Performance
- Limit 3 results (configurable)
- Vector search O(log n) với HNSW index
- Embedding cache trong Qdrant

## Best Practices

### ✅ Current Implementation
- Thread executor cho sync operations
- Graceful error handling với fallbacks
- Detailed logging cho debugging
- RAG integration với Qdrant
- Conversation history context

### ⚠️ Known Issues
- Không sử dụng dependency injection cho main chat endpoint (để tránh greenlet)
- Print statements thay vì proper logging
- Hardcoded prompt trong code (nên dùng prompt_manager)
- Không có rate limiting
- Không có authentication/authorization

### 🔧 Potential Improvements
- Implement streaming responses
- Add conversation title auto-generation
- Cache embeddings cho repeated queries
- Add message editing/deletion
- Implement conversation forking
