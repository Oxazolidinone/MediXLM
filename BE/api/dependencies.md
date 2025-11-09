# api/dependencies.py

## Mục đích
File Dependency Injection cho FastAPI endpoints. Cung cấp các factory functions để tạo instances của repositories, services, và use cases. Đảm bảo clean architecture và loose coupling giữa các layers.

## Chức năng chính

### 1. Database Session Management
- `get_db_session()`: Generator cung cấp SQLAlchemy session với context management
- Tự động đóng session sau khi request hoàn thành
- Thread-safe và connection pooling

### 2. Repository Providers
- `get_user_repository()`: Tạo UserRepositoryImpl với DB session
- `get_conversation_repository()`: Tạo ConversationRepositoryImpl với DB session
- `get_knowledge_graph_repository()`: Tạo KnowledgeGraphRepositoryImpl với Neo4j driver
- `get_cache_repository()`: Tạo CacheRepositoryImpl với Redis client

### 3. Service Providers (Singleton Pattern)
- `get_llm_service()`: Singleton instance của LocalLLMService
- `get_embedding_service()`: Reuse LLM service cho embedding generation
- Global variable `_llm_service` để cache instance

### 4. Use Case Providers
- `get_chat_use_case()`: Inject tất cả dependencies cho ChatUseCase
- `get_user_use_case()`: Inject UserRepository cho UserUseCase
- `get_knowledge_use_case()`: Inject KG repository và embedding service

## Liên kết với các file khác

### Dependencies (Import)
- `infrastructure/database/connection.py` - Database session factory
- `infrastructure/cache/redis_client.py` - Redis client instance
- `infrastructure/knowledge_graph/neo4j_client.py` - Neo4j driver
- `infrastructure/repositories/` - Repository implementations
  - `user_repository_impl.py`
  - `conversation_repository_impl.py`
  - `knowledge_graph_repository_impl.py`
  - `cache_repository_impl.py`
- `infrastructure/services/local_llm_service.py` - LLM service
- `application/use_cases/` - Use case classes
  - `chat_use_case.py`
  - `user_use_case.py`
  - `knowledge_use_case.py`
- `domain/repositories/` - Repository interfaces (ABC)

### Được sử dụng bởi
- `api/v1/endpoints/chat.py` - Depends(get_chat_use_case)
- `api/v1/endpoints/users.py` - Depends(get_user_use_case)
- `api/v1/endpoints/knowledge.py` - Depends(get_knowledge_use_case)

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - API ENDPOINTS SẼ KHÔNG HOẠT ĐỘNG

Nếu xóa file này:

1. **Không có dependency injection**: Tất cả endpoints sẽ fail vì không tạo được dependencies
2. **Tight coupling**: Endpoints sẽ phải tự tạo instances, vi phạm clean architecture
3. **Memory leaks**: Không quản lý được lifecycle của database sessions
4. **Resource exhaustion**: LLM service sẽ được load nhiều lần thay vì singleton
5. **Database connection leaks**: Sessions không được đóng đúng cách
6. **Testing khó khăn**: Không thể mock dependencies cho unit tests
7. **Code duplication**: Mỗi endpoint phải duplicate code khởi tạo dependencies

### Cách thay thế
Cần tạo file dependency injection mới với:
- Database session generators
- Repository factory functions
- Service singleton management
- Use case providers với dependency wiring

## Design Patterns

### 1. Dependency Injection Pattern
```python
# FastAPI tự động inject dependencies
def get_user_use_case(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> UserUseCase:
    return UserUseCase(user_repository=user_repo)
```

### 2. Singleton Pattern (Services)
```python
_llm_service = None  # Global cache

def get_llm_service() -> LocalLLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LocalLLMService()  # Load model once
    return _llm_service
```

### 3. Factory Pattern (Repositories)
```python
def get_user_repository(session: Session = Depends(get_db_session)):
    return UserRepositoryImpl(session)  # New instance per request
```

### 4. Context Manager Pattern (Database Session)
```python
def get_db_session() -> Generator[Session, None, None]:
    with get_database_session() as session:
        yield session  # Auto-close after use
```

## Dependency Graph

```
Endpoints
    ↓ Depends()
Use Cases (get_chat_use_case, get_user_use_case, get_knowledge_use_case)
    ↓ Depends()
Repositories (get_user_repository, get_conversation_repository, etc.)
    ↓ Depends()
Infrastructure Clients (get_db_session, get_neo4j_driver, get_redis_client)
```

## Best Practices

### ✅ Advantages
- **Testability**: Dễ dàng mock dependencies cho unit tests
- **Separation of Concerns**: Endpoints không biết về implementation details
- **Resource Management**: Auto cleanup với context managers
- **Performance**: Singleton pattern cho heavy services (LLM)
- **Type Safety**: Type hints cho tất cả dependencies

### ⚠️ Lưu ý
- **Singleton services**: LLM service được cache globally (cẩn thận với thread safety)
- **Per-request repositories**: Mỗi request có DB session riêng (tránh shared state)
- **Lazy initialization**: Services chỉ load khi cần (graceful degradation)
- **Error handling**: Nếu service init fail, exception sẽ bubble up đến endpoint

## Lifecycle Management

### Request Lifecycle
1. FastAPI nhận request
2. Resolve dependencies theo thứ tự (bottom-up)
3. Execute endpoint function
4. Auto cleanup (generators với yield)
5. Response trả về client

### Singleton Lifecycle
- `_llm_service`: Load lần đầu tiên khi được gọi
- Tồn tại suốt lifetime của application
- Không được cleanup (model vẫn trong memory)

### Per-Request Lifecycle
- Database session: Mới cho mỗi request
- Repositories: Mới cho mỗi request
- Use cases: Mới cho mỗi request
