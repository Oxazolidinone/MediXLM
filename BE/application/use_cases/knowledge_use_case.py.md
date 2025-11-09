# application/use_cases/knowledge_use_case.py

## Mục đích
File này chứa business logic cho knowledge graph management, bao gồm thêm medical knowledge, tạo relationships giữa các nodes, tìm kiếm knowledge bằng semantic search và graph traversal. Đây là use case quan trọng cho RAG (Retrieval-Augmented Generation) system.

## Chức năng chính

### KnowledgeUseCase Class
Quản lý medical knowledge graph với dependencies:
- **knowledge_graph_repository**: Truy cập Neo4j knowledge graph
- **embedding_service**: Generate embeddings cho semantic search

### add_knowledge(...) -> MedicalKnowledge
Thêm medical knowledge mới vào knowledge graph:
1. **Create MedicalKnowledge entity** từ input parameters
2. **Generate embeddings** cho name và description
3. **Update entity với embeddings**
4. **Save to knowledge graph** (Neo4j)
5. **Return created knowledge**

Parameters:
- name, knowledge_type (disease/symptom/treatment/etc.)
- description, properties, source

### link_knowledge(source_id, target_id, relationship_type, properties) -> bool
Tạo relationship giữa 2 knowledge nodes:
1. **Verify source node exists**
2. **Verify target node exists**
3. **Create relationship** trong Neo4j graph
4. **Return success status**

Relationship types có thể là: "CAUSES", "TREATS", "SYMPTOM_OF", etc.

### search_knowledge(query, knowledge_type, limit) -> List[MedicalKnowledge]
Semantic search medical knowledge:
1. **Generate embeddings** cho query string
2. **Perform similarity search** trong knowledge graph
3. **Filter by knowledge_type** nếu được chỉ định
4. **Return top N results** sorted by similarity score

### get_related_knowledge(node_id, relationship_type, depth) -> List[MedicalKnowledge]
Graph traversal để tìm related knowledge:
1. **Verify node exists**
2. **Traverse graph** theo relationships
3. **Return related nodes** trong khoảng depth cho phép

### get_knowledge_by_name(name, knowledge_type) -> List[MedicalKnowledge]
Tìm kiếm knowledge theo tên (exact/partial match).

## Liên kết với các file khác

### Dependencies (Import)
- **infrastructure/services**: LLMService (for embedding_service)
- **domain/entities**: MedicalKnowledge
- **domain/entities.medical_knowledge**: KnowledgeType enum
- **domain/repositories**: IKnowledgeGraphRepository
- **core/exceptions**: KnowledgeNotFoundError

### Được sử dụng bởi
- **api/v1/endpoints/knowledge.py**: Knowledge API endpoints
- **application/use_cases/chat_use_case.py**: Retrieve relevant knowledge cho chat (RAG)
- **scripts/seed_medical_knowledge.py**: Seed initial medical data
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Knowledge Graph and RAG System Failure

File này là core của knowledge management và RAG system. Nếu bị xóa:

- **RAG không hoạt động**: Chat sẽ không có medical knowledge context
- **Không thể thêm medical knowledge**: Admin không thể populate knowledge base
- **Semantic search bị mất**: Không tìm kiếm được knowledge relevant
- **Knowledge graph traversal bị mất**: Không explore được relationships
- **Chat quality giảm nghiêm trọng**: AI responses không có medical knowledge backing
- **Knowledge API endpoints hoàn toàn không hoạt động**

### Cách thay thế
1. **Tạo lại KnowledgeUseCase** với cùng interface
2. **Implement lại các operations**:
   - Knowledge creation với embedding generation
   - Relationship management
   - Semantic search logic
   - Graph traversal logic
3. **Integrate với embedding service** để generate vectors
4. **Maintain error handling** cho missing nodes

## Technical Notes

### Embedding Generation
Use case này orchestrate việc generate embeddings và save vào knowledge graph:
```python
text_for_embedding = f"{name}. {description or ''}"
embeddings = await self.embedding_service.generate_embeddings(text_for_embedding)
knowledge.update_embeddings(embeddings)
```

### Knowledge Types
Sử dụng KnowledgeType enum để classify medical knowledge:
- DISEASE: Bệnh
- SYMPTOM: Triệu chứng
- TREATMENT: Phương pháp điều trị
- MEDICATION: Thuốc
- PROCEDURE: Thủ thuật
- ANATOMY: Giải phẫu
- TEST: Xét nghiệm

### Graph Relationships
Relationships trong Neo4j graph có thể có properties:
```python
create_relationship(
    source_id=disease_id,
    target_id=symptom_id,
    relationship_type="HAS_SYMPTOM",
    properties={"frequency": "common", "severity": "moderate"}
)
```

### Semantic Search
Similarity search sử dụng cosine similarity giữa embeddings:
1. Embed query text
2. Compare với embeddings của tất cả knowledge nodes
3. Return top K nodes với highest similarity scores

## Integration with RAG

### How RAG Uses This Use Case

1. **User asks question** trong chat
2. **Chat use case calls** `search_knowledge(user_question)`
3. **Relevant medical knowledge được retrieve**
4. **Knowledge được format** thành context cho LLM prompt
5. **LLM generates response** dựa trên retrieved knowledge

### Benefits
- **Factual accuracy**: Responses grounded in medical knowledge
- **Source attribution**: Có thể cite nguồn medical knowledge
- **Up-to-date information**: Knowledge có thể được update independently
- **Explainability**: Biết được response dựa trên knowledge nào

## Best Practices

### Knowledge Quality
- Validate source của medical knowledge
- Maintain confidence_score để track reliability
- Regular updates để keep knowledge current

### Embedding Strategy
- Combine name + description để tạo rich embeddings
- Consider multilingual embeddings nếu support nhiều ngôn ngữ

### Graph Design
- Use meaningful relationship types
- Add properties to relationships để enrich context
- Design graph schema carefully cho optimal traversal

## Future Improvements

1. **Batch operations**: Add/update multiple knowledge nodes at once
2. **Knowledge versioning**: Track changes to medical knowledge
3. **Knowledge validation**: Validate against medical ontologies (SNOMED, ICD-10)
4. **Auto-relationship extraction**: Extract relationships từ medical texts
5. **Knowledge graph visualization**: API endpoints để visualize graph
6. **Confidence scoring**: Track và update confidence scores based on usage
