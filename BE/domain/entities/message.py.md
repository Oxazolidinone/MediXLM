# domain/entities/message.py

## Mục đích
File này định nghĩa Message entity và MessageRole enum - domain models đại diện cho tin nhắn trong conversation. Message entity chứa content, role (user/assistant/system), metadata và token tracking. Đây là child entity trong Conversation aggregate.

## Chức năng chính

### MessageRole Enum
Enum định nghĩa các vai trò trong conversation:
- **USER**: Tin nhắn từ người dùng
- **ASSISTANT**: Tin nhắn từ AI assistant
- **SYSTEM**: Tin nhắn hệ thống (instructions, notifications)

Inherits từ `str` và `Enum` để serializable và có string value.

### Message Dataclass
Domain entity với attributes:
- **id** (UUID): Unique message identifier
- **conversation_id** (UUID): ID của conversation chứa message
- **role** (MessageRole): Vai trò của message sender
- **content** (str): Nội dung tin nhắn
- **created_at** (datetime): Timestamp khi message được tạo
- **metadata** (Optional[Dict]): Additional data (knowledge sources, confidence, etc.)
- **tokens_used** (Optional[int]): Number of LLM tokens used

### __post_init__()
Auto-initialize optional fields:
- Set created_at = datetime.utcnow() nếu None
- Initialize metadata = {} nếu None

### create(...) -> Message
Static factory method tạo Message mới:
- Generate UUID tự động
- Initialize với provided data
- Set default metadata = {}
- Return new Message instance

Parameters:
- conversation_id, role, content (required)
- metadata, tokens_used (optional)

### add_metadata(key: str, value: Any)
Add metadata entry vào message:
- Initialize metadata dict nếu None
- Set key-value pair
- Useful cho storing additional context

## Liên kết với các file khác

### Dependencies (Import)
- **dataclasses**: dataclass - Dataclass decorator
- **datetime**: datetime - Timestamp type
- **enum**: Enum - Enum base class
- **typing**: Optional, Dict, Any - Type hints
- **uuid**: UUID, uuid4 - Unique identifiers

### Được sử dụng bởi
- **domain/entities/conversation.py**: Conversation chứa List[Message]
- **application/use_cases/chat_use_case.py**: Create user và assistant messages
- **infrastructure/repositories/conversation_repository_impl.py**: Persist messages
- **infrastructure/repositories/sync_conversation_repository.py**: Sync repo operations
- **domain/entities/__init__.py**: Export entity và enum
- **application/dto/conversation_dto.py**: Convert to MessageDTO

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Message System Complete Failure

Message entity là fundamental building block của chat system. Nếu bị xóa:

- **Chat hoàn toàn không hoạt động**: Không có cách represent messages
- **Conversation entity bị lỗi**: Conversation.messages không có type
- **Chat use case bị lỗi**: Không thể create user/assistant messages
- **Repositories bị lỗi**: Không có entity để convert database models
- **MessageRole enum bị mất**: Không validate role values
- **Breaking change cực kỳ nghiêm trọng**: Core chat functionality mất hoàn toàn

### Cách thay thế
1. **Recreate Message dataclass** với đầy đủ attributes
2. **Recreate MessageRole enum** với USER, ASSISTANT, SYSTEM
3. **Implement factory method** create()
4. **Implement metadata management** add_metadata()
5. **Update all imports** trong project

## Technical Notes

### String Enum
`MessageRole(str, Enum)` pattern:
- **Serializable**: Can be converted to JSON as string
- **Type-safe**: IDE autocomplete và type checking
- **Database-friendly**: Store as VARCHAR in database
- **API-friendly**: Return as string trong API responses

### Metadata Flexibility
Metadata dict cho phép store arbitrary data:
```python
message.add_metadata("knowledge_sources", ["source1", "source2"])
message.add_metadata("confidence_score", 0.95)
message.add_metadata("response_time_ms", 1500)
```

### Token Tracking
`tokens_used` field tracks LLM token consumption:
- Important cho cost monitoring
- Help với rate limiting
- Analytics về token usage per conversation

### Immutable After Creation
Messages thường không được edit sau khi tạo:
- Preserve conversation history integrity
- Audit trail purposes
- Simplify conflict resolution

## Domain-Driven Design

### Value Object Candidate
Message có thể được coi là value object instead of entity:
- **Identity không quan trọng**: Message ID chỉ dùng để reference
- **Immutable**: Messages không được edit
- **Replaceable**: Có thể recreate message với cùng content

Tuy nhiên, current implementation là entity vì có UUID identity.

### Part of Aggregate
Message là child entity trong Conversation aggregate:
```
Conversation (Root)
  └── Message (Child)
```
- Messages không tồn tại independent của Conversation
- Accessed qua Conversation
- Lifecycle tied to Conversation

## Best Practices

### Role Validation
Always validate role:
```python
if role not in MessageRole:
    raise ValueError(f"Invalid role: {role}")
```

### Content Sanitization
Sanitize content để avoid injection attacks:
```python
def create(cls, content: str, ...):
    sanitized_content = sanitize_html(content)
    return Message(..., content=sanitized_content)
```

### Metadata Schema
Define schema cho common metadata fields:
```python
METADATA_SCHEMA = {
    "knowledge_sources": List[str],
    "confidence_score": float,
    "response_time_ms": int,
    "model_version": str
}
```

### Timestamp Precision
Use high-precision timestamps cho message ordering:
```python
created_at = datetime.utcnow()  # microsecond precision
```

## Message Types & Roles

### USER Role
- Represents user input/questions
- Always from human user
- Triggers AI response generation

### ASSISTANT Role
- Represents AI-generated responses
- From LLM service
- Should cite sources when using RAG

### SYSTEM Role
- System instructions, notifications
- Not shown to users (usually)
- Control conversation flow
- Example: "System: Conversation started", "System: Knowledge base updated"

## Future Improvements

1. **Add edit history**: Track message edits với timestamps
2. **Add reactions**: Thumbs up/down, emoji reactions
3. **Add attachments**: Support images, files, audio
4. **Add mentions**: @user mentions trong messages
5. **Add threading**: Reply to specific messages
6. **Add message status**: Sent, delivered, read, failed
7. **Add streaming support**: Track streaming message state
8. **Add message types**: Text, image, audio, video, code
9. **Add formatting**: Rich text formatting support
10. **Add translation**: Auto-translate messages
11. **Add sentiment**: Sentiment analysis score
12. **Add embeddings**: Store message embeddings cho semantic search
