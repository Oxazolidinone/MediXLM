# infrastructure/knowledge_graph/neo4j_client.py

## Mục đích
File này quản lý Neo4j graph database connection cho knowledge graph. Provides async Neo4j driver với connection pooling và lifecycle management. Connects to local Neo4j Docker container.

## Chức năng chính

### Global Variable
- **neo4j_driver**: Global async Neo4j driver instance

### init_neo4j()
Async function initialize Neo4j connection:
- Create AsyncGraphDatabase driver
- Configure connection pool (max_connection_pool_size=50)
- Set timeout (60s)
- encrypted=False (local Docker không cần TLS)
- Verify connectivity với verify_connectivity()
- Continue even nếu Neo4j unavailable

### close_neo4j()
Async function đóng Neo4j driver:
- Close driver properly
- Release all connections

### get_neo4j_driver() -> AsyncDriver
Get global Neo4j driver instance:
- Return neo4j_driver
- Raise RuntimeError nếu not initialized

## Liên kết với các file khác

### Dependencies
- **neo4j**: AsyncGraphDatabase, AsyncDriver
- **core.config**: settings - Neo4j URI và credentials

### Được sử dụng bởi
- **main.py**: Initialize/close Neo4j
- **infrastructure/repositories/knowledge_graph_repository_impl.py**: Execute Cypher queries

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Knowledge Graph Access Lost

Nếu bị xóa:
- **Knowledge graph không hoạt động**: Không access Neo4j
- **RAG system fails**: Không retrieve medical knowledge
- **Chat quality giảm nghiêm trọng**: No knowledge context

### Cách thay thế
Recreate Neo4j driver initialization với proper configuration.
