# infrastructure/vector_db/milvus_client.py

## Mục đích
File này quản lý Milvus vector database client - alternative cho Qdrant. Milvus stores embeddings và provides similarity search. Connects to Milvus Cloud (Zilliz) với token authentication. Currently unused, Qdrant được sử dụng thay thế.

## Chức năng chính

### Global Variable
- **_collection**: Global Milvus Collection instance

### init_milvus()
Initialize Milvus connection:
- Connect to Milvus Cloud với URI và token
- Create collection nếu chưa có với schema:
  - id (VARCHAR, primary key)
  - embedding (FLOAT_VECTOR, dim=384)
  - text (VARCHAR)
  - metadata (JSON)
- Create IVF_FLAT index cho similarity search
- Load collection vào memory

### close_milvus()
Close Milvus connection:
- Release collection từ memory
- Disconnect from Milvus

### get_milvus_client() -> Collection
Get global Milvus collection instance.

## Liên kết với các file khác

### Dependencies
- **pymilvus**: connections, Collection, FieldSchema, etc.
- **core.config**: settings - Milvus URI, token, collection name

### Được sử dụng bởi
Currently unused. Có thể được sử dụng thay Qdrant nếu cần.

## Tác động nếu file này bị xóa

### 🟢 LOW - Alternative Vector DB Lost

Nếu bị xóa:
- **Không ảnh hưởng**: Currently unused, Qdrant được dùng
- **Mất alternative option**: Không thể switch sang Milvus nếu cần

### Cách thay thế
Keep cho future use hoặc delete nếu không cần.
