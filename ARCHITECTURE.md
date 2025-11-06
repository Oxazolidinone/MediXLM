# MediXLM Architecture Documentation

## Clean Architecture Overview

MediXLM follows **Clean Architecture** principles, organizing code into concentric layers with strict dependency rules.

```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│              (FastAPI Endpoints, Schemas)            │
├─────────────────────────────────────────────────────┤
│                  Application Layer                   │
│            (Use Cases, DTOs, Interfaces)             │
├─────────────────────────────────────────────────────┤
│                    Domain Layer                      │
│          (Entities, Value Objects, Repos)            │
├─────────────────────────────────────────────────────┤
│                 Infrastructure Layer                 │
│    (Database, Cache, KG, Vector DB, Services)        │
└─────────────────────────────────────────────────────┘
```

### Dependency Rule

**Dependencies point inward**: Outer layers depend on inner layers, never the reverse.

- **Domain** has no dependencies
- **Application** depends on Domain
- **Infrastructure** depends on Domain & Application
- **Presentation** depends on Application & Infrastructure (via dependency injection)

## Layer Descriptions

### 1. Domain Layer (Core Business Logic)

**Location**: `BE/domain/`

Contains pure business logic with zero external dependencies.

#### Entities
- `User` - User account entity
- `Conversation` - Chat conversation entity
- `Message` - Individual message entity
- `MedicalKnowledge` - Knowledge graph node entity

#### Repository Interfaces
- `IUserRepository`
- `IConversationRepository`
- `IKnowledgeGraphRepository`
- `ICacheRepository`

**Key Principles**:
- No framework dependencies
- Pure Python with dataclasses
- Business rules and validation
- Repository interfaces (not implementations)

### 2. Application Layer (Use Cases)

**Location**: `BE/application/`

Orchestrates business logic and coordinates data flow.

#### Use Cases
- `ChatUseCase` - Handle chat conversations with AI
- `UserUseCase` - Manage user operations
- `KnowledgeUseCase` - Manage knowledge graph operations

#### DTOs (Data Transfer Objects)
- `ChatRequestDTO`, `ChatResponseDTO`
- `UserCreateDTO`, `UserResponseDTO`
- `ConversationDTO`, `MessageDTO`

#### Service Interfaces
- `ILLMService` - Language model interface
- `IEmbeddingService` - Embedding generation interface

**Key Principles**:
- Implements business workflows
- No database/framework details
- Uses DTOs for data transfer
- Depends only on Domain interfaces

### 3. Infrastructure Layer (External Services)

**Location**: `BE/infrastructure/`

Implements external service integrations.

#### Database (PostgreSQL)
- `connection.py` - SQLAlchemy async engine
- `models.py` - Database models (UserModel, ConversationModel, MessageModel)

#### Cache (Redis)
- `redis_client.py` - Redis connection management
- `CacheRepositoryImpl` - Cache operations implementation

#### Knowledge Graph (Neo4j)
- `neo4j_client.py` - Neo4j driver management
- `KnowledgeGraphRepositoryImpl` - Graph operations

#### Vector Database (Qdrant)
- `qdrant_client.py` - Qdrant connection
- Used for semantic similarity search

#### Services
- `OpenAIService` - LLM service implementation (GPT-4)
- `EmbeddingServiceImpl` - Embedding generation (OpenAI)

#### Repository Implementations
- `UserRepositoryImpl`
- `ConversationRepositoryImpl`
- `KnowledgeGraphRepositoryImpl`
- `CacheRepositoryImpl`

**Key Principles**:
- Implements Domain interfaces
- Contains all external dependencies
- Database models separate from Domain entities
- Can be swapped without affecting business logic

### 4. Presentation Layer (API)

**Location**: `BE/presentation/`

Handles HTTP requests/responses and API contracts.

#### Endpoints
- `health.py` - Health check endpoint
- `chat.py` - Chat endpoints
- `users.py` - User management endpoints
- `knowledge.py` - Knowledge graph endpoints

#### Dependencies
- `dependencies.py` - Dependency injection setup

**Key Principles**:
- FastAPI routers and schemas
- Request/response validation
- Error handling
- Dependency injection

### 5. Core Layer (Cross-Cutting Concerns)

**Location**: `BE/core/`

#### Configuration
- `settings.py` - Application settings (Pydantic)

#### Exceptions
- Custom exception classes
- Error hierarchy

#### Logging
- Logging configuration
- Logger factory

## Data Flow

### Example: Chat Message Flow

```
1. User sends message via HTTP POST
   ↓
2. [Presentation] chat.py endpoint receives request
   ↓
3. [Presentation] Validates input, converts to DTO
   ↓
4. [Application] ChatUseCase.process_message()
   ├─ Get conversation from ConversationRepository
   ├─ Generate embeddings via EmbeddingService
   ├─ Search knowledge graph via KnowledgeGraphRepository
   ├─ Build context and call LLMService
   ├─ Save messages via ConversationRepository
   └─ Cache response via CacheRepository
   ↓
5. [Presentation] Convert response DTO to HTTP response
   ↓
6. Return to user
```

## Technology Stack

### Databases
- **PostgreSQL** - Primary relational database
- **Redis** - Caching layer
- **Neo4j** - Knowledge Graph (medical relationships)
- **Qdrant** - Vector database (semantic search)

### Framework
- **FastAPI** - Async web framework
- **SQLAlchemy 2.0** - Async ORM
- **Pydantic** - Data validation

### AI/ML
- **OpenAI API**
  - GPT-4 Turbo for conversations
  - text-embedding-3-small for embeddings

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Uvicorn** - ASGI server

## Key Features

### 1. Knowledge Graph (Brain)

**Purpose**: Store and query medical knowledge relationships

**Implementation**:
- Neo4j graph database
- Nodes: Diseases, Symptoms, Treatments, Medications
- Relationships: CAUSES, TREATS, DIAGNOSES, etc.
- Graph traversal for related knowledge

**Example**:
```cypher
(Disease:Diabetes)-[:HAS_SYMPTOM]->(Symptom:Fatigue)
(Medication:Metformin)-[:TREATS]->(Disease:Diabetes)
```

### 2. Vector Search

**Purpose**: Semantic similarity search for medical knowledge

**Implementation**:
- Qdrant vector database
- OpenAI embeddings (1536 dimensions)
- Cosine similarity search
- Fast retrieval of relevant medical information

### 3. Caching Strategy

**Purpose**: Improve response time and reduce API costs

**Implementation**:
- Redis in-memory cache
- Cache conversation context
- Cache frequently accessed knowledge
- TTL-based expiration

### 4. Conversation Management

**Purpose**: Maintain chat context and history

**Implementation**:
- PostgreSQL for persistence
- Conversation sessions per user
- Message history with role tracking
- Token usage tracking

## Dependency Injection

Using FastAPI's dependency injection system:

```python
# dependencies.py
def get_chat_use_case(
    conversation_repo: IConversationRepository = Depends(...),
    kg_repo: IKnowledgeGraphRepository = Depends(...),
    cache_repo: ICacheRepository = Depends(...),
    llm_service: ILLMService = Depends(...),
    embedding_service: IEmbeddingService = Depends(...),
) -> ChatUseCase:
    return ChatUseCase(
        conversation_repository=conversation_repo,
        knowledge_graph_repository=kg_repo,
        cache_repository=cache_repo,
        llm_service=llm_service,
        embedding_service=embedding_service,
    )
```

## Benefits of This Architecture

1. **Testability**: Easy to mock interfaces for unit testing
2. **Maintainability**: Clear boundaries and responsibilities
3. **Scalability**: Easy to add new features without breaking existing code
4. **Flexibility**: Easy to swap implementations (e.g., different LLM providers)
5. **Independence**: Business logic independent of frameworks
6. **Team Collaboration**: Different teams can work on different layers

## Future Enhancements

### Potential Additions
- [ ] GraphQL API layer
- [ ] Message queue (RabbitMQ/Kafka) for async processing
- [ ] Elasticsearch for full-text search
- [ ] Authentication & Authorization (OAuth2, JWT)
- [ ] Rate limiting and throttling
- [ ] API versioning strategy
- [ ] Monitoring (Prometheus, Grafana)
- [ ] Distributed tracing (Jaeger)
- [ ] Load balancing
- [ ] Multi-model LLM support (Anthropic, local models)

## Development Guidelines

### Adding a New Feature

1. **Define Domain entities** (if needed)
2. **Create repository interface** in Domain
3. **Implement use case** in Application
4. **Implement repository** in Infrastructure
5. **Create API endpoint** in Presentation
6. **Write tests** for each layer

### Testing Strategy

- **Unit Tests**: Test Domain entities and Application use cases
- **Integration Tests**: Test Infrastructure repositories
- **E2E Tests**: Test API endpoints

### Code Quality

- Use type hints everywhere
- Follow PEP 8 style guide
- Use `black` for formatting
- Use `mypy` for type checking
- Write docstrings for all public methods

## Deployment

### Development
```bash
make dev-setup
make up
```

### Production
- Use environment-specific `.env` files
- Enable HTTPS (reverse proxy)
- Set DEBUG=False
- Use managed database services
- Implement proper logging and monitoring
- Set up CI/CD pipeline
