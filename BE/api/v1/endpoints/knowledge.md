# api/v1/endpoints/knowledge.py

## Mục đích
REST API endpoints cho Medical Knowledge Graph operations. Cung cấp CRUD cho knowledge nodes, tạo relationships, semantic search, và graph traversal trong Neo4j.

## Chức năng chính

### 1. POST /knowledge/ - Thêm Medical Knowledge Node
- **Input**: `KnowledgeCreate` (name, type, description, properties, source)
- **Output**: `KnowledgeResponse` (HTTP 201 Created)
- **Process**:
  1. Validate knowledge type (DISEASE, SYMPTOM, TREATMENT, etc.)
  2. Generate embeddings cho semantic search
  3. Lưu vào Neo4j graph database
  4. Return node với confidence score

### 2. POST /knowledge/relationships - Tạo Relationship giữa Nodes
- **Input**: `RelationshipCreate` (source_id, target_id, relationship_type, properties)
- **Output**: Success message
- **Examples**:
  - "Diabetes" --CAUSES--> "High Blood Sugar"
  - "Aspirin" --TREATS--> "Headache"
  - "Fever" --SYMPTOM_OF--> "Flu"

### 3. POST /knowledge/search - Semantic Search Medical Knowledge
- **Input**: `SearchRequest` (query, knowledge_type optional, limit)
- **Output**: List of `KnowledgeResponse` (ranked by relevance)
- **Process**:
  1. Generate embedding cho query
  2. Vector similarity search trong embeddings
  3. Filter by knowledge_type (nếu có)
  4. Return top-k results

### 4. GET /knowledge/{node_id}/related - Graph Traversal
- **Input**: node_id, relationship_type (optional), depth
- **Output**: List of related knowledge nodes
- **Use cases**:
  - Find all symptoms của một disease
  - Find all treatments cho một condition
  - Explore knowledge graph từ một node

## Knowledge Types (Enum)

```python
class KnowledgeType(Enum):
    DISEASE = "disease"           # Bệnh
    SYMPTOM = "symptom"           # Triệu chứng
    TREATMENT = "treatment"       # Phương pháp điều trị
    MEDICATION = "medication"     # Thuốc
    PROCEDURE = "procedure"       # Thủ thuật y tế
    ANATOMY = "anatomy"           # Giải phẫu
    TEST = "test"                 # Xét nghiệm
```

## Request/Response Models

### KnowledgeCreate (Input)
```python
{
    "name": "Diabetes Type 2",
    "knowledge_type": "disease",
    "description": "Chronic metabolic disorder...",
    "properties": {
        "icd_code": "E11",
        "prevalence": "high",
        "severity": "moderate"
    },
    "source": "WHO Guidelines 2023"
}
```

### RelationshipCreate (Input)
```python
{
    "source_id": "uuid-of-diabetes",
    "target_id": "uuid-of-high-blood-sugar",
    "relationship_type": "CAUSES",
    "properties": {
        "confidence": 0.95,
        "evidence_level": "strong"
    }
}
```

### SearchRequest (Input)
```python
{
    "query": "how to treat headache",
    "knowledge_type": "treatment",  # Optional filter
    "limit": 10
}
```

## Liên kết với các file khác

### Dependencies (Import)
- `application/use_cases/knowledge_use_case.py` - Business logic
- `domain/entities/medical_knowledge.py` - KnowledgeType enum, MedicalKnowledge entity
- `core/exceptions/` - KnowledgeNotFoundError
- `api/dependencies.py` - `get_knowledge_use_case()` dependency injection

### Được sử dụng bởi
- `infrastructure/services/rag_service.py` - Search knowledge cho chat RAG
- Admin panels - Quản lý medical knowledge base
- Data ingestion pipelines - Import medical data
- Knowledge graph visualization tools

### Calls to
- `KnowledgeUseCase.add_knowledge()` - Tạo node mới
- `KnowledgeUseCase.link_knowledge()` - Tạo relationship
- `KnowledgeUseCase.search_knowledge()` - Semantic search
- `KnowledgeUseCase.get_related_knowledge()` - Graph traversal

## Tác động nếu file này bị xóa

### 🟡 HIGH IMPACT - KNOWLEDGE GRAPH MANAGEMENT KHÔNG KHẢ DỤNG

Nếu xóa file này:

1. **Không thêm được medical knowledge**:
   - Không populate knowledge base
   - RAG system không có data để retrieve

2. **Không tạo được relationships**:
   - Knowledge graph không có connections
   - Graph traversal không hoạt động

3. **RAG search bị ảnh hưởng gián tiếp**:
   - `rag_service.py` vẫn hoạt động (direct Qdrant access)
   - Nhưng không thể add/update knowledge qua API

4. **Admin workflows bị block**:
   - Không quản lý được knowledge base
   - Phải edit trực tiếp trong Neo4j

### Workaround
- Data có thể được import trực tiếp vào Neo4j
- RAG vẫn hoạt động với existing data
- Nhưng không có API interface

### Cách thay thế
Cần tạo lại knowledge endpoints với:
- CRUD operations cho nodes
- Relationship management
- Semantic search integration
- Graph traversal logic

## Knowledge Graph Architecture

### Neo4j Schema
```cypher
// Node structure
(:MedicalKnowledge {
    id: UUID,
    name: String,
    knowledge_type: String,
    description: String,
    properties: Map,
    embeddings: [Float],  # 384-dim vector
    confidence_score: Float,
    created_at: DateTime,
    updated_at: DateTime
})

// Relationships
(:Disease)-[:CAUSES]->(:Symptom)
(:Medication)-[:TREATS]->(:Disease)
(:Symptom)-[:SYMPTOM_OF]->(:Disease)
(:Medication)-[:HAS_SIDE_EFFECT]->(:Symptom)
(:Procedure)-[:DIAGNOSES]->(:Disease)
```

### Embedding Integration
1. Text được embed với sentence-transformers (384-dim)
2. Embeddings stored trong Neo4j node properties
3. Similarity search: Cosine distance calculation
4. Cũng sync với Qdrant cho fast vector search

## Semantic Search Flow

### Step 1: Generate Query Embedding
```python
# In KnowledgeUseCase
query_embedding = embedding_service.embed_text(query)
```

### Step 2: Vector Similarity in Neo4j
```cypher
// Cosine similarity calculation
MATCH (k:MedicalKnowledge)
WHERE k.knowledge_type = $type  // Optional filter
WITH k,
     gds.similarity.cosine(k.embeddings, $query_embedding) AS similarity
ORDER BY similarity DESC
LIMIT $limit
RETURN k
```

### Step 3: Return Ranked Results
Sorted by similarity score (highest first)

## Graph Traversal Patterns

### Example 1: Find All Symptoms of Diabetes
```python
GET /knowledge/{diabetes_id}/related?relationship_type=CAUSES&depth=1
```

### Example 2: Multi-hop Traversal
```python
GET /knowledge/{symptom_id}/related?depth=2
# Finds: Symptom -> Disease -> Treatments
```

### Example 3: Bidirectional Traversal
```cypher
MATCH path = (start)-[*1..depth]-(related)
WHERE start.id = $node_id
RETURN DISTINCT related
```

## Error Handling

### 1. Invalid Knowledge Type (400 Bad Request)
```python
try:
    knowledge_type = KnowledgeType(knowledge_data.knowledge_type)
except ValueError as e:
    raise HTTPException(status_code=400, detail=f"Invalid knowledge type: {e}")
```

### 2. Knowledge Not Found (404 Not Found)
```python
except KnowledgeNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
```

### 3. Relationship Creation Failed (500)
```python
if not success:
    raise HTTPException(status_code=500, detail="Failed to create relationship")
```

## Best Practices

### ✅ Current Implementation
- Enum validation cho knowledge types
- Semantic search với embeddings
- Graph traversal với configurable depth
- Flexible properties (JSON/Dict)
- Source attribution
- Confidence scoring

### ⚠️ Missing Features
- **Bulk import**: Chỉ có single node creation
- **Update/Delete**: Không có PATCH/DELETE endpoints
- **Relationship querying**: Không list all relationships
- **Graph analytics**: Không có PageRank, centrality, etc.
- **Version control**: Không track knowledge updates

### 🔧 Potential Improvements
```python
# Bulk import
@router.post("/bulk")
async def bulk_import_knowledge(data: List[KnowledgeCreate]):
    ...

# Update node
@router.patch("/{node_id}")
async def update_knowledge(node_id: UUID, updates: KnowledgeUpdate):
    ...

# Delete node
@router.delete("/{node_id}")
async def delete_knowledge(node_id: UUID):
    ...

# List all relationships
@router.get("/{node_id}/relationships")
async def get_relationships(node_id: UUID):
    ...

# Graph analytics
@router.get("/analytics/centrality")
async def get_important_nodes():
    ...
```

## Integration với RAG System

### Knowledge Graph → Vector DB Flow
1. Knowledge được add qua `/knowledge/` endpoint
2. Embeddings được generate trong `KnowledgeUseCase`
3. Node được save vào Neo4j với embeddings
4. **Parallel**: Data cũng được index vào Qdrant (để fast search)
5. RAG service search Qdrant cho speed
6. Graph traversal từ Neo4j cho reasoning

### Dual Storage Strategy
- **Neo4j**: Graph relationships, complex queries
- **Qdrant**: Fast vector similarity search
- **Sync mechanism**: Needed để keep consistent
