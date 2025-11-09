# infrastructure/cache/redis_client.py

## Mục đích
File này quản lý Redis client connection cho caching layer. Provides async Redis client với connection pooling, health checks, và proper lifecycle management. Supports local Redis hoặc cloud Redis (Upstash).

## Chức năng chính

### Global Variable
- **redis_client**: Global async Redis client instance

### init_redis()
Async function initialize Redis connection:
- Create Redis client từ URL (supports rediss:// for TLS)
- Configure connection pool (max_connections=50)
- Set timeouts và keepalive
- Test connection với ping()
- Called during app startup

### close_redis()
Async function đóng Redis connection:
- Close Redis client properly
- Called during app shutdown

### get_redis_client() -> redis.Redis
Get global Redis client instance:
- Return redis_client
- Raise RuntimeError nếu not initialized

## Liên kết với các file khác

### Dependencies
- **redis.asyncio**: Async Redis client
- **core.config**: settings - Redis URL và config

### Được sử dụng bởi
- **main.py**: Initialize/close Redis
- **application/use_cases/chat_use_case.py**: Get Redis client cho caching
- **infrastructure/repositories/cache_repository_impl.py**: Implements cache operations

## Tác động nếu file này bị xóa

### 🟡 HIGH - Caching Layer Lost

Nếu bị xóa:
- **Caching không hoạt động**: Performance hit
- **Cache repository fails**: CacheRepositoryImpl không có client
- **Application vẫn chạy**: Nhưng slower without caching

### Cách thay thế
Recreate Redis client initialization với proper lifecycle management.
