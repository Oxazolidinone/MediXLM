# domain/repositories/cache_repository.py

## Mục đích
File này định nghĩa ICacheRepository interface - abstract contract cho caching operations. Interface này định nghĩa standard cache operations (get, set, delete, etc.) mà không phụ thuộc vào Redis implementation cụ thể.

## Chức năng chính

### ICacheRepository Interface (ABC)

#### Basic Operations
- **get(key: str) -> Optional[Any]**: Lấy value từ cache
- **set(key, value, expire) -> bool**: Set value vào cache với optional TTL
- **delete(key: str) -> bool**: Xóa key từ cache
- **exists(key: str) -> bool**: Check nếu key tồn tại

#### Advanced Operations
- **clear(pattern: Optional[str] = None) -> bool**: Clear cache (tất cả hoặc theo pattern)
- **increment(key: str, amount: int = 1) -> int**: Atomic increment counter
- **get_ttl(key: str) -> Optional[int]**: Lấy remaining TTL của key

## Liên kết với các file khác

### Dependencies (Import)
- **abc**: ABC, abstractmethod
- **typing**: Optional, Any

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Cache chat responses và knowledge
- **infrastructure/repositories/cache_repository_impl.py**: Implements với Redis
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🟡 HIGH - Caching Contract Lost

Interface này là contract cho caching operations. Nếu bị xóa:

- **Cache use bị mất**: Chat use case không thể cache responses
- **Performance degradation**: Mất caching layer
- **Clean Architecture vi phạm**: Application phụ thuộc trực tiếp vào Redis
- **Testing khó khăn**: Không mock được cache
- **Implementation switching impossible**: Không thể đổi cache backend

### Cách thay thế
Recreate ABC interface với basic và advanced cache operations.

## Best Practices

### Key Naming
Use prefixes cho different data types:
- `user:{user_id}` - User data
- `conv:{conversation_id}` - Conversation data
- `knowledge:{query_hash}` - Cached knowledge search results

### TTL Strategy
- Short TTL (minutes): Frequently changing data
- Medium TTL (hours): Relatively stable data
- Long TTL (days): Static reference data
