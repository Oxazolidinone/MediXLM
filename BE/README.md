# MediXLM Backend

Medical AI Chatbot với Knowledge Graph và Self-hosted LLM, được xây dựng theo Clean Architecture.

## Công Nghệ Sử Dụng

### Core Framework
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Databases
- **PostgreSQL** - Primary relational database
- **Redis** - Caching layer
- **Neo4j** - Knowledge Graph (Brain - lưu trữ medical knowledge)
- **Milvus** - Vector database cho semantic search

### AI/ML (Self-hosted)
- **PyTorch** - Deep learning framework
- **Transformers** - HuggingFace transformers library
- **Sentence-Transformers** - Local embedding generation
- **Local LLM**: Microsoft Phi-2 (2.7B parameters) hoặc các model khác

### Các Model Đề Xuất

#### LLM Models (chọn theo RAM có sẵn):
- `microsoft/phi-2` - 2.7B params, ~6GB RAM (đề xuất)
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0` - 1.1B params, ~3GB RAM (nhanh)
- `meta-llama/Llama-2-7b-chat-hf` - 7B params, ~16GB RAM (chất lượng cao)

#### Embedding Models:
- `sentence-transformers/all-MiniLM-L6-v2` - 384 dim (nhanh, đề xuất)
- `sentence-transformers/all-mpnet-base-v2` - 768 dim (chất lượng tốt hơn)

## Kiến Trúc Clean Architecture

```
BE/
├── domain/                 # Domain Layer - Core Business Logic
│   ├── entities/          # User, Conversation, Message, MedicalKnowledge
│   └── repositories/      # Repository interfaces
│
├── application/           # Application Layer - Use Cases
│   ├── use_cases/        # Business logic (functional style)
│   ├── dto/              # Data Transfer Objects
│   └── interfaces/       # Service interfaces
│
├── infrastructure/        # Infrastructure Layer
│   ├── database/         # PostgreSQL
│   ├── cache/            # Redis
│   ├── knowledge_graph/  # Neo4j
│   ├── vector_db/        # Milvus
│   ├── repositories/     # Repository implementations
│   └── services/         # Local LLM & Embedding services
│
├── presentation/          # API Layer
│   └── api/v1/endpoints/ # FastAPI endpoints
│
└── core/                 # Config, Exceptions, Logging
```

## Setup

### Yêu Cầu Hệ Thống

- Python 3.11+
- Docker & Docker Compose
- RAM: Tối thiểu 8GB (16GB recommended)
- GPU (Optional): CUDA-compatible GPU cho tốc độ nhanh hơn

### Cài Đặt Nhanh với Docker

1. Clone repository và cd vào thư mục:
```bash
cd MediXLM
```

2. Tạo file `.env`:
```bash
cp BE/.env.example BE/.env
```

3. (Optional) Chỉnh sửa BE/.env để chọn model phù hợp:
```bash
# Cho máy RAM thấp
LLM_MODEL_NAME=TinyLlama/TinyLlama-1.1B-Chat-v1.0

# Cho máy RAM cao
LLM_MODEL_NAME=microsoft/phi-2
```

4. Start tất cả services:
```bash
make up
# hoặc
docker-compose up -d
```

**Lần đầu chạy sẽ mất 10-20 phút** để download models từ HuggingFace.

5. Kiểm tra logs:
```bash
make logs
# hoặc
docker-compose logs -f backend
```

### Cài Đặt Local Development

1. Tạo virtual environment:
```bash
cd BE
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Cài dependencies:
```bash
pip install -r requirements.txt
```

3. Start infrastructure services (PostgreSQL, Redis, Neo4j, Milvus):
```bash
cd ..
docker-compose up -d postgres redis neo4j etcd minio milvus
```

4. Tạo `.env`:
```bash
cp .env.example .env
```

5. Run backend:
```bash
python main.py
```

## API Endpoints

API Docs: `http://localhost:8000/docs`

### Health
- `GET /health` - Health check

### Chat
- `POST /api/v1/chat/` - Gửi message và nhận AI response
- `GET /api/v1/chat/history/{conversation_id}` - Lấy lịch sử chat

### Users
- `POST /api/v1/users/` - Tạo user
- `GET /api/v1/users/{user_id}` - Lấy thông tin user
- `GET /api/v1/users/username/{username}` - Tìm user theo username

### Knowledge Graph
- `POST /api/v1/knowledge/` - Thêm medical knowledge
- `POST /api/v1/knowledge/relationships` - Tạo relationship
- `POST /api/v1/knowledge/search` - Tìm kiếm knowledge
- `GET /api/v1/knowledge/{node_id}/related` - Lấy related knowledge

## Services Overview

### PostgreSQL
- **Port**: 5432
- **Purpose**: Lưu users, conversations, messages
- **Access**: `psql -h localhost -U postgres -d medixlm`

### Redis
- **Port**: 6379
- **Purpose**: Cache responses, session data
- **Access**: `redis-cli`

### Neo4j (Knowledge Graph - Brain)
- **Port**: 7474 (HTTP), 7687 (Bolt)
- **Purpose**: Lưu medical knowledge và relationships
- **Access**: http://localhost:7474 (user: neo4j, pass: medixlm123)

### Milvus (Vector Database)
- **Port**: 19530 (gRPC), 9091 (HTTP)
- **Purpose**: Vector similarity search cho semantic search
- **Dependencies**: etcd (port 2379), MinIO (port 9000, 9001)

### Backend API
- **Port**: 8000
- **Purpose**: REST API
- **Docs**: http://localhost:8000/docs

## Functional Programming Approach

Code được đơn giản hóa bằng cách sử dụng functional programming thay vì class-based approach:

### Before (Class-based):
```python
class ChatUseCase:
    def __init__(self, repo1, repo2, service1):
        self.repo1 = repo1
        ...

    async def process_message(self, request):
        ...
```

### After (Functional):
```python
async def process_chat_message(
    message: str,
    user_id: UUID,
    conversation_repo,
    kg_repo,
    llm_service,
    ...
):
    ...
```

Lợi ích:
- Code ngắn gọn hơn
- Ít boilerplate
- Dễ test hơn
- Dependencies rõ ràng

## Development Commands

```bash
# Start tất cả services
make up

# Stop services
make down

# Xem logs
make logs

# Clean up (xóa volumes)
make clean

# Format code
make format

# Run tests
make test

# Lint code
make lint
```

## Memory Usage

Dự tính memory usage:

- PostgreSQL: ~200MB
- Redis: ~50MB
- Neo4j: ~2GB
- Milvus (với etcd, MinIO): ~1GB
- Backend với models:
  - microsoft/phi-2: ~6GB
  - TinyLlama: ~3GB
  - all-MiniLM-L6-v2: ~100MB

**Total**: ~9-12GB cho full stack

## Troubleshooting

### Model download quá chậm
Models được download từ HuggingFace. Nếu chậm, có thể:
1. Set HF mirror: `export HF_ENDPOINT=https://hf-mirror.com`
2. Download trước: `huggingface-cli download microsoft/phi-2`

### Out of Memory
- Giảm model size: Dùng TinyLlama thay vì Phi-2
- Giảm workers: Set `WORKERS=1` trong .env
- Tăng swap space

### GPU không được sử dụng
Cài CUDA toolkit và GPU-enabled PyTorch:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Milvus không start
Kiểm tra etcd và MinIO đã chạy:
```bash
docker-compose ps etcd minio
docker-compose logs etcd minio
```

## Production Deployment

Để deploy production:

1. Set `DEBUG=False` trong .env
2. Sử dụng managed services cho databases
3. Set up proper logging và monitoring
4. Sử dụng reverse proxy (nginx)
5. Enable HTTPS
6. Set up CI/CD pipeline
7. Implement rate limiting
8. Use GPU instances cho performance tốt hơn

## Tối Ưu Performance

### CPU-only
- Sử dụng models nhỏ (TinyLlama, MiniLM)
- Tăng batch size cho embedding
- Enable quantization

### With GPU
- Models có thể lớn hơn (Llama-2-7b)
- Sử dụng torch.compile() cho speedup
- Enable mixed precision (FP16)

## License

MIT
