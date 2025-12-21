# Chatbot Hỏi Đáp Luật Môi Trường

Hệ thống chatbot hỏi đáp về Luật Bảo vệ Môi trường 2020 sử dụng Knowledge Graph và Multi-Reasoner AI.

## 🚀 Khởi động nhanh

### Windows
```batch
start.bat
```

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

## 📋 Yêu cầu hệ thống

### Phần mềm cần cài đặt:
- **Python 3.10+** với pip
- **Node.js 18+** với npm
- **Docker Desktop** (cho Redis)
- **Neo4j Desktop** hoặc Neo4j Docker
- **Ollama** (cho LLM)

### Các model LLM cần tải:
```bash
ollama pull qwen2.5:7b
```

## 🛠️ Cài đặt thủ công

### 1. Clone repository
```bash
git clone <repository-url>
cd Project_Chatbot_hoi_dap_luat_moi_truong
```

### 2. Cài đặt Backend
```bash
cd MediXLM/BE

# Tạo môi trường ảo (khuyến nghị)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file cấu hình
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Chỉnh sửa .env với thông tin Neo4j của bạn
```

### 3. Cài đặt Frontend
```bash
cd FE

# Cài đặt dependencies
npm install

# Tạo file cấu hình
copy env.example .env.local  # Windows
cp env.example .env.local    # macOS/Linux
```

### 4. Khởi động Redis
```bash
docker run -d --name redis-cache -p 6379:6379 redis
```

### 5. Khởi động Neo4j
- Mở Neo4j Desktop và start database
- Hoặc dùng Docker: `docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j`

### 6. Import Knowledge Graph
- Mở Neo4j Browser: http://localhost:7474
- Chạy file `MediXLM/BE/kg/import_new.cypher`

### 7. Khởi động Backend
```bash
cd MediXLM/BE
python -m uvicorn main_standalone:app --reload --host 0.0.0.0 --port 8000
```

### 8. Khởi động Frontend
```bash
cd FE
npm run dev
```

### 9. Truy cập ứng dụng
- **Chatbot**: http://localhost:3000/chatbot
- **Admin**: http://localhost:3000/admin
- **API Docs**: http://localhost:8000/docs

## 🐳 Chạy với Docker Compose

```bash
# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

## 📁 Cấu trúc dự án

```
Project_Chatbot_hoi_dap_luat_moi_truong/
├── FE/                          # Next.js Frontend
│   ├── app/
│   │   ├── chatbot/            # Trang chatbot
│   │   └── admin/              # Trang quản trị
│   ├── components/             # React components
│   └── env.example             # Mẫu cấu hình
│
├── MediXLM/BE/                  # FastAPI Backend
│   ├── core/reasoning/         # Multi-Reasoner Engine
│   ├── infrastructure/
│   │   └── services/
│   │       ├── env_law_service.py
│   │       └── redis_cache_service.py
│   ├── kg/                     # Knowledge Graph files
│   ├── main_standalone.py      # API Server
│   ├── requirements.txt
│   └── .env.example            # Mẫu cấu hình
│
├── docker-compose.yml          # Docker Compose config
├── start.bat                   # Windows startup script
├── start.sh                    # macOS/Linux startup script
└── README.md
```

## 🔧 Cấu hình

### Backend (.env)
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

REDIS_HOST=localhost
REDIS_PORT=6379

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🌟 Tính năng

- ✅ **Chatbot AI** hỏi đáp Luật Môi trường
- ✅ **Multi-Reasoner Engine** với nhiều chiến lược suy luận
- ✅ **Knowledge Graph** dựa trên Neo4j
- ✅ **Redis Caching** tăng tốc độ phản hồi 22x
- ✅ **Admin Dashboard** quản lý nodes
- ✅ **Visualization** hiển thị quá trình suy luận

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. Neo4j đang chạy và có dữ liệu
2. Ollama đang chạy với model qwen2.5:7b
3. Redis đang chạy (optional)
4. Các port 3000, 8000, 7687, 6379 không bị chiếm
