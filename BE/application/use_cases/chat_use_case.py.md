# application/use_cases/chat_use_case.py

## Mục đích
File này chứa business logic chính cho tính năng chat của hệ thống. ChatUseCase xử lý toàn bộ flow từ nhận tin nhắn người dùng, truy vấn knowledge graph, gọi LLM, đến lưu trữ conversation vào database. Đây là core use case orchestrating nhiều services và repositories.

## Chức năng chính

### ChatUseCase Class
Orchestrates chat flow với các dependencies:
- **conversation_repository**: Quản lý conversations và messages
- **knowledge_graph_repository**: Truy vấn medical knowledge graph
- **cache_repository**: Cache responses và knowledge
- **llm_service**: Gọi Local LLM để generate responses
- **embedding_service**: Generate embeddings cho semantic search

### process_message(request: ChatRequestDTO) -> ChatResponseDTO
Xử lý tin nhắn từ user với flow:
1. **Get or create conversation**: Lấy conversation hiện có hoặc tạo mới
2. **Save user message**: Lưu tin nhắn của user vào database
3. **Get conversation history**: Lấy 4 tin nhắn gần nhất để làm context
4. **Knowledge retrieval** (commented out): Tìm kiếm medical knowledge liên quan
5. **Generate response**: Gọi LLM để tạo câu trả lời
6. **Save assistant message**: Lưu phản hồi của AI vào database
7. **Return response**: Trả về ChatResponseDTO

### get_conversation_history(conversation_id, skip, limit) -> List[MessageDTO]
Lấy lịch sử chat của một conversation với pagination.

### Helper Methods
- **_build_knowledge_context**: Format knowledge graph results cho prompt
- **_build_conversation_history**: Format messages history cho LLM
- **_build_system_prompt**: Tạo system prompt với knowledge context

## Liên kết với các file khác

### Dependencies (Import)
- **application/dto**: ChatRequestDTO, ChatResponseDTO, MessageDTO
- **infrastructure/services**: LLMService
- **domain/entities**: Conversation, Message, MessageRole
- **domain/repositories**: IConversationRepository, IKnowledgeGraphRepository, ICacheRepository
- **core/exceptions**: ConversationNotFoundError
- **core/prompts**: build_chat_prompt, format_knowledge_context
- **infrastructure/database/connection**: get_sync_session
- **infrastructure/repositories/sync_conversation_repository**: SyncConversationRepository
- **infrastructure/cache/redis_client**: get_redis_client

### Được sử dụng bởi
- **api/v1/endpoints/chat.py**: Chat API endpoints sử dụng use case này
- **api/dependencies.py**: Dependency injection setup

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Complete Chat System Failure

Đây là file QUAN TRỌNG NHẤT của chat system. Nếu bị xóa:

- **Toàn bộ tính năng chat ngừng hoạt động**: API chat endpoints sẽ không có business logic
- **Không thể xử lý tin nhắn**: Users không thể chat với AI assistant
- **Mất orchestration logic**: Không có code điều phối giữa repositories, LLM, và knowledge graph
- **Breaking change nghiêm trọng**: Ứng dụng mất chức năng core nhất
- **Data flow bị đứt**: Không có layer kết nối API và infrastructure

### Cách thay thế
1. **Tạo lại use case** với cùng interface và dependencies
2. **Implement lại toàn bộ business logic**:
   - Conversation management
   - Message persistence
   - LLM integration
   - Knowledge retrieval
   - Error handling
3. **Maintain dependency injection** với các repositories và services
4. **Keep async/sync handling** cho database operations

## Technical Notes

### Threading for Synchronous Database Operations
Use case này sử dụng `loop.run_in_executor()` để chạy synchronous database operations trong thread pool, tránh blocking async event loop:

```python
loop = asyncio.get_event_loop()
result = await loop.run_in_executor(None, sync_db_operations)
```

### Greenlet Compatibility
Code hiện tại sử dụng synchronous SQLAlchemy session trong thread để tránh greenlet spawn errors với async SQLAlchemy.

### LLM Integration Currently Disabled
LLM call đang bị comment out và thay bằng placeholder response để debug database issues:
```python
response_text = "Test response - LLM disabled for debugging"
```

### Transaction Management
Database operations được wrap trong try-finally block với commit/rollback logic trong `get_sync_session()`.

## Future Improvements

1. **Re-enable LLM integration**: Uncomment LLM service calls
2. **Add RAG (Retrieval-Augmented Generation)**: Implement knowledge retrieval
3. **Implement caching**: Cache frequent queries và responses
4. **Add streaming responses**: Stream LLM output cho better UX
5. **Error recovery**: Better error handling và retry logic
6. **Performance optimization**: Optimize database queries và LLM calls
