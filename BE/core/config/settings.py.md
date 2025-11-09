# core/config/settings.py

## Mục đích
File này là configuration center của toàn bộ ứng dụng, định nghĩa tất cả settings từ database URLs, service endpoints, đến model configurations. Sử dụng Pydantic Settings để load config từ environment variables và .env file với type safety và validation.

## Chức năng chính

### Settings Class
Centralized configuration với các nhóm settings:

#### Application Settings
- **APP_NAME**: "MediXLM"
- **APP_VERSION**: "1.0.0"
- **DEBUG**: Debug mode flag
- **API_V1_PREFIX**: "/api/v1"

#### Server Settings
- **HOST**: Server bind address
- **PORT**: Server port (8000)
- **WORKERS**: Number of worker processes (4)

#### Database Settings (PostgreSQL)
- **DATABASE_URL**: Connection string (synchronous psycopg2)
- **DATABASE_POOL_SIZE**: 20
- **DATABASE_MAX_OVERFLOW**: 10

#### Redis Cache Settings
- **REDIS_URL**: Redis connection URL
- **REDIS_MAX_CONNECTIONS**: 50

#### Neo4j Knowledge Graph Settings
- **NEO4J_URI**: Neo4j bolt connection
- **NEO4J_USER**, **NEO4J_PASSWORD**: Credentials

#### Milvus Vector Database Settings
- **MILVUS_URI**: Cloud Milvus endpoint
- **MILVUS_TOKEN**: Authentication token
- **MILVUS_COLLECTION_NAME**: Collection name

#### Qdrant Vector Database Settings
- **QDRANT_URL**: Qdrant cloud URL
- **QDRANT_API_KEY**: API key
- **QDRANT_COLLECTION_NAME**: Collection name

#### Ollama LLM Settings
- **OLLAMA_HOST**: Local Ollama server
- **OLLAMA_MODEL**: "qwen2.5:7b"
- **OLLAMA_TIMEOUT**: 120 seconds

#### Local LLM Settings
- **LLM_MODEL_NAME**: "microsoft/phi-2"
- **LLM_MAX_TOKENS**: 2000

#### Embedding Model Settings
- **EMBEDDING_MODEL_NAME**: "sentence-transformers/all-MiniLM-L6-v2"
- **EMBEDDING_DIMENSION**: 384

#### CORS Settings
- **CORS_ORIGINS**: Allowed origins list
- **CORS_ALLOW_CREDENTIALS**: True
- **CORS_ALLOW_METHODS**, **CORS_ALLOW_HEADERS**: ["*"]

#### Logging Settings
- **LOG_LEVEL**: "INFO"
- **LOG_FORMAT**: "json"

### get_settings() -> Settings
Factory function với `@lru_cache()` decorator để return singleton Settings instance.

### settings: Settings
Global settings instance được export để các modules khác import.

## Liên kết với các file khác

### Dependencies (Import)
- **pydantic_settings**: BaseSettings - Base class cho settings
- **typing**: Optional - Type hints
- **functools**: lru_cache - Caching decorator

### Được sử dụng bởi (rất nhiều files)
- **main.py**: Application startup configuration
- **infrastructure/database/connection.py**: Database connection
- **infrastructure/cache/redis_client.py**: Redis connection
- **infrastructure/knowledge_graph/neo4j_client.py**: Neo4j connection
- **infrastructure/vector_db/qdrant_client.py**: Qdrant connection
- **infrastructure/vector_db/milvus_client.py**: Milvus connection
- **infrastructure/services/local_llm_service.py**: LLM configuration
- **infrastructure/services/embedding_service.py**: Embedding model config
- **core/logging/logger.py**: Logging configuration
- Hầu hết các files trong project đều import settings

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Complete Application Failure

File này là ĐIỂM TRUNG TÂM của configuration. Nếu bị xóa:

- **Application không thể start**: Không có database URLs, service endpoints
- **Không kết nối được bất kỳ service nào**: Database, Redis, Neo4j, Qdrant, Milvus
- **LLM services không hoạt động**: Không có model names và endpoints
- **CORS sẽ bị lỗi**: Frontend không thể connect với backend
- **Logging không hoạt động đúng**: Không có log level config
- **Toàn bộ infrastructure layer sụp đổ**: Tất cả clients cần settings để initialize

### Cách thay thế
1. **Tạo lại Settings class** với Pydantic BaseSettings
2. **Define lại TẤT CẢ configuration fields** với đúng types và defaults
3. **Setup environment variable loading** từ .env file
4. **Implement lru_cache** cho settings factory function
5. **Update tất cả imports** trong project để dùng new settings

## Technical Notes

### Pydantic Settings
Sử dụng pydantic_settings để:
- Auto-load từ .env file
- Type validation cho config values
- Case-sensitive environment variables
- Provide default values

### LRU Cache
`@lru_cache()` decorator ensures Settings chỉ được instantiate một lần:
```python
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### Environment Variables
Settings có thể được override bằng environment variables:
```bash
export DATABASE_URL="postgresql://..."
export OLLAMA_MODEL="llama2:13b"
```

### Config Hierarchy
1. Environment variables (highest priority)
2. .env file values
3. Default values trong Settings class (lowest priority)

## Configuration Strategy

### Local vs Cloud Services
- **Local Docker**: PostgreSQL, Redis, Neo4j
- **Cloud Services**: Qdrant, Milvus (có thể chuyển về local)
- **Local LLM**: Ollama cho development, có thể switch sang cloud LLMs

### Database Driver Choice
Sử dụng synchronous psycopg2 driver thay vì asyncpg để tránh greenlet issues:
```python
DATABASE_URL = "postgresql://..." # psycopg2
# Not: "postgresql+asyncpg://..."  # asyncpg would cause greenlet errors
```

### Model Selection
- **LLM**: Qwen 2.5 7B (balanced performance/size)
- **Embedding**: all-MiniLM-L6-v2 (fast, 384 dimensions)

## Best Practices

### Security
- **NEVER commit .env file** với sensitive credentials
- Use environment variables cho production
- Rotate API keys và passwords regularly

### Validation
- Add validators cho URLs, ports, paths
- Validate model names exist before loading
- Check service connectivity on startup

### Documentation
- Document mỗi config field với clear comments
- Provide example .env.example file
- Document required vs optional configs

## Future Improvements

1. **Add config validation**: Validate URLs, check service availability
2. **Environment-specific configs**: Dev, staging, production configs
3. **Secrets management**: Use secret management service (Vault, AWS Secrets Manager)
4. **Config versioning**: Track config changes
5. **Dynamic config reload**: Reload config without restart
6. **Config validation on startup**: Test all connections before serving requests
