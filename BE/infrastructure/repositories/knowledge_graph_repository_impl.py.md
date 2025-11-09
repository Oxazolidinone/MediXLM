# infrastructure/repositories/knowledge_graph_repository_impl.py

## Mục đích
File này implements IKnowledgeGraphRepository interface với Neo4j driver. Provides concrete implementation cho knowledge graph operations bao gồm node CRUD, relationship management, graph traversal, và semantic similarity search sử dụng Cypher queries.

## Chức năng chính

### KnowledgeGraphRepositoryImpl Class

#### Node Operations
- **create_node**: CREATE node trong Neo4j với tất cả properties và embeddings
- **get_node_by_id**: MATCH node by UUID
- **search_by_name**: MATCH nodes WHERE name CONTAINS search string
- **update_node**: SET node properties
- **delete_node**: DETACH DELETE node (removes relationships too)

#### Relationship Operations
- **create_relationship**: CREATE relationship giữa 2 nodes với dynamic relationship type và properties

#### Graph Traversal
- **get_related_nodes**: Traverse graph với configurable depth và relationship type filter

#### Semantic Search
- **similarity_search**: Use gds.similarity.cosine để find similar nodes based on embeddings

#### Helper Methods
- **_to_entity**: Convert Neo4j node → MedicalKnowledge entity

## Liên kết với các file khác

### Dependencies
- **neo4j**: AsyncDriver - Neo4j async driver
- **domain.entities**: MedicalKnowledge
- **domain.entities.medical_knowledge**: KnowledgeType
- **domain.repositories**: IKnowledgeGraphRepository

### Được sử dụng bởi
- **application/use_cases/knowledge_use_case.py**: All knowledge graph operations
- **application/use_cases/chat_use_case.py**: Retrieve knowledge cho RAG
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Knowledge Graph Access Completely Lost

Nếu bị xóa:
- **Knowledge graph hoàn toàn không hoạt động**: Không access Neo4j
- **RAG system fails**: Không retrieve medical knowledge
- **Knowledge management impossible**: Không add/update knowledge
- **Chat quality giảm nghiêm trọng**: No medical knowledge context

### Cách thay thế
Recreate implementation với Cypher queries cho all graph operations, traversal, và similarity search.

## Technical Notes

### Cypher Queries
File này chứa nhiều complex Cypher queries:
- Pattern matching: `MATCH (n:MedicalKnowledge {id: $id})`
- Relationship creation: `CREATE (source)-[r:TREATS]->(target)`
- Graph traversal: `MATCH (n)-[*1..2]-(related)`
- Similarity search: `gds.similarity.cosine(n.embeddings, $embeddings)`

### Dynamic Relationship Types
Relationships được create với dynamic types:
```python
query = "CREATE (source)-[r:%s]->(target)" % relationship_type
```

### Embedding Storage
Embeddings (List[float]) stored directly trong Neo4j properties, used cho similarity search.
