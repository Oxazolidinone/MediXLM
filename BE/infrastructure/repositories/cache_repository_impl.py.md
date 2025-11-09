# infrastructure/repositories/cache_repository_impl.py

## Mục đích
File này implements ICacheRepository interface với Redis async client. Provides concrete implementation cho caching operations với JSON serialization/deserialization, TTL support, và pattern-based clearing.

## Chức năng chính

### CacheRepositoryImpl Class

#### Basic Operations
- **get**: Get value từ Redis, deserialize JSON
- **set**: Serialize value to JSON, set với optional TTL (setex)
- **delete**: Delete key, return success
- **exists**: Check key exists

#### Advanced Operations
- **clear**: Clear all keys hoặc keys matching pattern
- **increment**: Atomic counter increment
- **get_ttl**: Get remaining TTL của key

#### JSON Handling
Auto serialize/deserialize JSON:
- Serialize non-string values to JSON
- Deserialize JSON to Python objects
- Handle decode errors gracefully

## Liên kết với các file khác

### Dependencies
- **json**: JSON serialization
- **redis.asyncio**: Async Redis client
- **domain.repositories**: ICacheRepository interface

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Cache responses và knowledge
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🟡 HIGH - Caching Implementation Lost

Nếu bị xóa:
- **Caching không hoạt động**: Performance degradation
- **Cache use case code fails**: Depends on this implementation

### Cách thay thế
Recreate implementation với Redis operations và JSON handling.
