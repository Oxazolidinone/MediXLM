# domain/repositories/knowledge_graph_repository.py

## Mục đích
File này định nghĩa IKnowledgeGraphRepository interface - abstract contract cho knowledge graph operations. Interface này định nghĩa operations cho managing medical knowledge nodes, relationships, và semantic search mà không phụ thuộc vào Neo4j implementation cụ thể.

## Chức năng chính

### IKnowledgeGraphRepository Interface (ABC)

#### Node Operations
- **create_node(knowledge: MedicalKnowledge) -> MedicalKnowledge**: Tạo knowledge node
- **get_node_by_id(node_id: UUID) -> Optional[MedicalKnowledge]**: Lấy node theo ID
- **search_by_name(name, knowledge_type) -> List[MedicalKnowledge]**: Search nodes theo tên
- **update_node(knowledge: MedicalKnowledge) -> MedicalKnowledge**: Update node
- **delete_node(node_id: UUID) -> bool**: Xóa node

#### Relationship Operations
- **create_relationship(source_id, target_id, relationship_type, properties) -> bool**: Tạo relationship giữa nodes

#### Graph Traversal
- **get_related_nodes(node_id, relationship_type, depth) -> List[MedicalKnowledge]**: Traverse graph để find related nodes

#### Semantic Search
- **similarity_search(embeddings, knowledge_type, limit) -> List[MedicalKnowledge]**: Cosine similarity search với embeddings

## Liên kết với các file khác

### Dependencies (Import)
- **abc**: ABC, abstractmethod
- **typing**: List, Optional, Dict, Any
- **uuid**: UUID
- **domain.entities**: MedicalKnowledge
- **domain.entities.medical_knowledge**: KnowledgeType

### Được sử dụng bởi
- **application/use_cases/knowledge_use_case.py**: Depends on interface cho knowledge operations
- **application/use_cases/chat_use_case.py**: Use semantic search cho RAG
- **infrastructure/repositories/knowledge_graph_repository_impl.py**: Implements với Neo4j
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Knowledge Graph Contract Lost

Interface này là contract cho knowledge graph operations. Nếu bị xóa:

- **Knowledge use case bị lỗi**: Không biết knowledge graph contract
- **RAG system bị mất**: Chat không thể retrieve medical knowledge
- **Semantic search impossible**: Không có interface cho similarity search
- **Graph traversal bị mất**: Không explore relationships
- **Clean Architecture vi phạm**: Application phụ thuộc trực tiếp vào Neo4j
- **Testing impossible**: Không mock được graph operations

### Cách thay thế
Recreate ABC interface với node operations, relationships, traversal, và semantic search.
