# domain/entities/medical_knowledge.py

## Mục đích
File này định nghĩa MedicalKnowledge entity và KnowledgeType enum - domain models đại diện cho medical knowledge trong knowledge graph. MedicalKnowledge entity chứa medical information, embeddings cho semantic search, và metadata về nguồn và độ tin cậy.

## Chức năng chính

### KnowledgeType Enum
Enum phân loại medical knowledge:
- **DISEASE**: Bệnh lý (diabetes, hypertension, etc.)
- **SYMPTOM**: Triệu chứng (fever, cough, pain, etc.)
- **TREATMENT**: Phương pháp điều trị (surgery, therapy, etc.)
- **MEDICATION**: Thuốc men (insulin, aspirin, etc.)
- **PROCEDURE**: Thủ thuật y tế (blood test, MRI, etc.)
- **ANATOMY**: Giải phẫu (heart, liver, etc.)
- **TEST**: Xét nghiệm (blood glucose test, etc.)

### MedicalKnowledge Dataclass
Domain entity với attributes:
- **id** (UUID): Unique knowledge identifier
- **name** (str): Tên của knowledge (e.g., "Diabetes Type 2")
- **knowledge_type** (KnowledgeType): Loại knowledge
- **description** (Optional[str]): Mô tả chi tiết
- **properties** (Dict): Additional properties (symptoms, dosage, etc.)
- **embeddings** (Optional[List[float]]): Vector embeddings cho semantic search
- **created_at** (datetime): Timestamp tạo
- **updated_at** (datetime): Timestamp cập nhật
- **source** (Optional[str]): Nguồn thông tin (WHO, Mayo Clinic, etc.)
- **confidence_score** (float): Độ tin cậy (0.0-1.0, default: 1.0)

### __post_init__()
Auto-initialize optional fields:
- Set created_at, updated_at = datetime.utcnow() nếu None
- Initialize properties = {} nếu None

### create(...) -> MedicalKnowledge
Static factory method tạo knowledge node mới:
- Generate UUID tự động
- Initialize với provided data
- Set default confidence_score = 1.0
- Return new MedicalKnowledge instance

Parameters:
- name, knowledge_type (required)
- description, properties, source, confidence_score (optional)

### update_embeddings(embeddings: List[float])
Update embeddings cho knowledge:
- Set embeddings vector
- Update updated_at timestamp
- Enable semantic search

### update_properties(properties: Dict)
Update properties dict:
- Merge new properties với existing
- Update updated_at timestamp
- Preserve existing properties

## Liên kết với các file khác

### Dependencies (Import)
- **dataclasses**: dataclass - Dataclass decorator
- **datetime**: datetime - Timestamp type
- **enum**: Enum - Enum base class
- **typing**: Optional, Dict, Any, List - Type hints
- **uuid**: UUID, uuid4 - Unique identifiers

### Được sử dụng bởi
- **application/use_cases/knowledge_use_case.py**: Create và manage medical knowledge
- **infrastructure/repositories/knowledge_graph_repository_impl.py**: Persist knowledge trong Neo4j
- **domain/repositories/knowledge_graph_repository.py**: Repository interface
- **domain/entities/__init__.py**: Export entity và enum
- **scripts/seed_medical_knowledge.py**: Seed initial medical data

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Knowledge Graph and RAG System Failure

MedicalKnowledge entity là core của knowledge management. Nếu bị xóa:

- **Knowledge graph hoàn toàn không hoạt động**: Không có model cho medical knowledge
- **RAG system bị mất**: Không thể retrieve relevant medical knowledge
- **Chat quality giảm cực kỳ nghiêm trọng**: Responses không có medical knowledge backing
- **Knowledge use case bị lỗi**: Không thể add/search knowledge
- **Neo4j repository bị lỗi**: Không có entity để convert graph nodes
- **Seeding scripts bị lỗi**: Không thể populate knowledge base
- **Breaking change nghiêm trọng**: Medical knowledge system mất hoàn toàn

### Cách thay thế
1. **Recreate MedicalKnowledge dataclass** với đầy đủ attributes
2. **Recreate KnowledgeType enum** với tất cả medical types
3. **Implement factory method** create()
4. **Implement update methods** update_embeddings, update_properties
5. **Update all imports** trong knowledge-related files

## Technical Notes

### Vector Embeddings
`embeddings: Optional[List[float]]` stores vector representation:
- Generated bởi sentence transformers
- Used cho cosine similarity search
- Dimension: 384 (all-MiniLM-L6-v2 model)
- Enable semantic search: "diabetes symptoms" → finds relevant knowledge

### Knowledge Graph Node
MedicalKnowledge maps to Neo4j node:
```cypher
CREATE (n:MedicalKnowledge {
  id: "uuid",
  name: "Diabetes Type 2",
  knowledge_type: "disease",
  description: "...",
  embeddings: [0.1, 0.2, ...],
  confidence_score: 0.95
})
```

### Confidence Score
Tracks reliability của knowledge:
- **1.0**: Highly reliable (WHO, medical textbooks)
- **0.7-0.9**: Moderately reliable (medical websites)
- **<0.7**: Lower reliability (user-contributed, needs review)

### Properties Flexibility
`properties: Dict[str, Any]` stores type-specific data:
```python
# Disease properties
properties = {
    "icd10_code": "E11",
    "prevalence": "8.5% globally",
    "risk_factors": ["obesity", "age", "genetics"]
}

# Medication properties
properties = {
    "dosage": "500mg twice daily",
    "side_effects": ["nausea", "diarrhea"],
    "contraindications": ["kidney disease"]
}
```

## Domain-Driven Design

### Entity vs Value Object
MedicalKnowledge là entity vì:
- **Has identity**: UUID uniquely identifies knowledge
- **Has lifecycle**: Created, updated, linked to other knowledge
- **Mutable**: Embeddings, properties có thể update

### Aggregate Root
MedicalKnowledge là aggregate root trong knowledge domain:
- Self-contained unit
- May have relationships to other knowledge (edges trong graph)
- Transactional boundary

### Ubiquitous Language
- **Knowledge Type**: Medical domain classification
- **Embeddings**: Technical term for vectors
- **Confidence Score**: Trust level of information
- **Source**: Attribution to medical authorities

## Knowledge Graph Relationships

### Example Relationships
```
(Diabetes:DISEASE) -[:HAS_SYMPTOM]-> (Thirst:SYMPTOM)
(Diabetes:DISEASE) -[:TREATED_BY]-> (Metformin:MEDICATION)
(Metformin:MEDICATION) -[:HAS_SIDE_EFFECT]-> (Nausea:SYMPTOM)
(BloodTest:TEST) -[:DIAGNOSES]-> (Diabetes:DISEASE)
```

### Relationship Types
- HAS_SYMPTOM
- TREATED_BY
- CAUSES
- PREVENTS
- DIAGNOSES
- CONTRAINDICATED_WITH
- INTERACTS_WITH

## Best Practices

### Source Attribution
Always provide source cho medical knowledge:
```python
knowledge = MedicalKnowledge.create(
    name="Aspirin",
    knowledge_type=KnowledgeType.MEDICATION,
    source="WHO Essential Medicines List 2023"
)
```

### Validation
Validate medical knowledge before adding:
```python
def create(cls, name: str, ...):
    if not name or len(name) < 2:
        raise ValueError("Knowledge name too short")
    if confidence_score < 0 or confidence_score > 1:
        raise ValueError("Confidence must be 0-1")
    return MedicalKnowledge(...)
```

### Versioning
Track knowledge updates:
```python
properties = {
    "version": "2.0",
    "last_reviewed": "2024-01-15",
    "reviewer": "Dr. Smith"
}
```

### Multilingual Support
Store translations:
```python
properties = {
    "name_vi": "Tiểu đường type 2",
    "description_vi": "Bệnh tiểu đường..."
}
```

## Future Improvements

1. **Add knowledge versioning**: Track changes over time
2. **Add validation against medical ontologies**: SNOMED CT, ICD-10
3. **Add multilingual support**: Name và description trong nhiều ngôn ngữ
4. **Add knowledge sources tracking**: Multiple sources per knowledge
5. **Add review workflow**: Pending, approved, rejected states
6. **Add knowledge quality score**: Based on source reliability
7. **Add usage analytics**: Track how often knowledge is used
8. **Add knowledge relationships**: As part of entity (not just graph)
9. **Add expiry dates**: Knowledge có thể outdated
10. **Add knowledge hierarchy**: Parent-child relationships
11. **Add knowledge tags**: Additional categorization
12. **Add knowledge images**: Visual representations
