# main.py

## Mục đích
File entry point chính của ứng dụng FastAPI MediXLM Backend. Chịu trách nhiệm khởi tạo toàn bộ hệ thống, quản lý vòng đời ứng dụng (startup/shutdown), cấu hình middleware và đăng ký các API routes.

## Chức năng chính

### 1. Application Lifecycle Management
- **Startup**: Khởi tạo tất cả các kết nối cần thiết (Database, Redis, Neo4j, Qdrant)
- **Shutdown**: Đóng tất cả các kết nối một cách graceful
- **Error Handling**: Xử lý lỗi khởi tạo với logging chi tiết, tiếp tục chạy nếu một số service không khả dụng

### 2. FastAPI Application Configuration
- Cấu hình metadata (title, version, contact, license)
- Định nghĩa OpenAPI documentation endpoints (/docs, /redoc)
- Phân loại API endpoints theo tags (health, chat, knowledge, users)

### 3. CORS Middleware
- Cho phép cross-origin requests từ frontend
- Cấu hình từ settings (origins, credentials, methods, headers)

### 4. API Router Registration
- Đăng ký tất cả API v1 routes với prefix từ settings
- Root endpoint (/) trả về thông tin ứng dụng

### 5. Uvicorn Server Configuration
- Cấu hình host, port, workers từ settings
- Auto-reload trong chế độ DEBUG

## Liên kết với các file khác

### Dependencies (Import)
- `core/config/settings.py` - Cấu hình toàn hệ thống
- `core/logging/logger.py` - Logging setup
- `infrastructure/cache/redis_client.py` - Redis initialization
- `infrastructure/database/connection.py` - Database initialization
- `infrastructure/knowledge_graph/neo4j_client.py` - Neo4j initialization
- `infrastructure/vector_db/qdrant_client.py` - Qdrant initialization
- `api/v1/__init__.py` - API router với tất cả endpoints

### Được sử dụng bởi
- Uvicorn server (khi chạy ứng dụng)
- Deployment scripts
- Testing frameworks

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - HỆ THỐNG SẼ KHÔNG THỂ CHẠY

Nếu xóa file này:

1. **Không có entry point**: Ứng dụng không thể khởi động
2. **Không có lifecycle management**: Các service sẽ không được khởi tạo hoặc đóng đúng cách
3. **Không có API server**: Tất cả endpoints sẽ không thể truy cập
4. **Memory leaks**: Kết nối database/Redis/Neo4j/Qdrant sẽ không được đóng khi shutdown
5. **Không có CORS**: Frontend sẽ không thể gọi API
6. **Không có logging**: Không theo dõi được hoạt động hệ thống
7. **Không có documentation**: Swagger UI (/docs) sẽ không hoạt động

### Cách thay thế
Cần tạo file entry point mới với:
- FastAPI app instance
- Lifespan context manager để khởi tạo/đóng services
- CORS middleware configuration
- API router registration
- Uvicorn server configuration

## Các cấu hình quan trọng

### Lifespan Events
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database() → init_redis() → init_neo4j() → init_qdrant()

    yield  # Application running

    # Shutdown
    close_database() → close_redis() → close_neo4j() → close_qdrant()
```

### Service Initialization Order
1. **Database (PostgreSQL)** - Lưu trữ dữ liệu chính
2. **Redis** - Caching layer
3. **Neo4j** - Knowledge graph
4. **Qdrant** - Vector database cho RAG

### Error Resilience
- Mỗi service initialization được wrap trong try-catch
- Nếu một service fail → log warning và tiếp tục
- Chỉ critical error mới dừng ứng dụng

## Best Practices
- ✅ Sử dụng `asynccontextmanager` cho lifecycle management (thay vì deprecated startup/shutdown events)
- ✅ Graceful error handling cho từng service
- ✅ Logging chi tiết cho debugging
- ✅ CORS configuration từ settings (không hardcode)
- ✅ API versioning với prefix
- ✅ OpenAPI documentation tags
