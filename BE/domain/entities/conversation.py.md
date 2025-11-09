# domain/entities/conversation.py

## Mục đích
File này định nghĩa Conversation entity - domain model đại diện cho cuộc hội thoại giữa user và AI assistant. Conversation entity quản lý conversation lifecycle và chứa collection của Messages. Đây là aggregate root cho conversation-message aggregate.

## Chức năng chính

### Conversation Dataclass
Domain entity với attributes:
- **id** (UUID): Unique conversation identifier
- **user_id** (UUID): ID của user sở hữu conversation
- **title** (Optional[str]): Tiêu đề conversation
- **created_at** (datetime): Thời gian tạo
- **updated_at** (datetime): Thời gian cập nhật lần cuối
- **is_active** (bool): Trạng thái hoạt động (default: True)
- **messages** (List[Message]): Collection of messages trong conversation

### __post_init__()
Auto-initialize timestamps:
- Set created_at = datetime.utcnow() nếu None
- Set updated_at = datetime.utcnow() nếu None

### create(user_id, title) -> Conversation
Static factory method tạo Conversation mới:
- Generate UUID tự động
- Auto-generate title nếu không provided: "Conversation YYYY-MM-DD HH:MM"
- Initialize empty messages list
- Return new Conversation instance

### add_message(message: Message)
Thêm message vào conversation:
- Append message vào messages list
- Auto-update updated_at timestamp
- Maintains conversation state

### update_title(title: str)
Update conversation title:
- Set new title
- Update updated_at timestamp

### close()
Close/deactivate conversation:
- Set is_active = False
- Update updated_at timestamp

## Liên kết với các file khác

### Dependencies (Import)
- **dataclasses**: dataclass, field - Dataclass decorators
- **datetime**: datetime - Timestamp type
- **typing**: Optional, List - Type hints
- **uuid**: UUID, uuid4 - Unique identifiers
- **.message**: Message - Message entity import

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Create và manage conversations
- **infrastructure/repositories/conversation_repository_impl.py**: Persist Conversation entities
- **infrastructure/repositories/sync_conversation_repository.py**: Sync version của repository
- **domain/entities/__init__.py**: Export entity
- **application/dto/conversation_dto.py**: Convert to/from DTOs

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Conversation Management Failure

Conversation entity là core của chat system. Nếu bị xóa:

- **Chat system ngừng hoạt động**: Không có model cho conversations
- **Message grouping bị mất**: Messages không được organize vào conversations
- **Conversation lifecycle management bị mất**: Không có methods để manage conversation state
- **Repositories bị lỗi**: Không có entity để convert database models
- **Use cases bị lỗi**: Chat use case không thể tạo/quản lý conversations
- **Breaking change nghiêm trọng**: Core chat functionality mất

### Cách thay thế
1. **Recreate Conversation dataclass** với cùng attributes và methods
2. **Import Message entity** properly
3. **Implement lifecycle methods**: add_message, update_title, close
4. **Maintain relationship** với User và Messages

## Technical Notes

### Aggregate Root
Conversation là aggregate root trong DDD:
- **Root entity**: Conversation
- **Child entities**: Messages
- **Consistency boundary**: All messages belong to one conversation
- **Transactional boundary**: Load/save conversation with messages together

### One-to-Many Relationship
Conversation has many Messages:
```python
messages: List[Message] = field(default_factory=list)
```
- Uses `field(default_factory=list)` để avoid mutable default argument
- Messages được manage qua add_message() method

### Auto-Generated Title
Default title với timestamp:
```python
title = title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
```
- Readable title cho users
- Includes timestamp để distinguish conversations

### Lifecycle State
`is_active` flag tracks conversation state:
- **True**: Conversation đang active, có thể add messages
- **False**: Conversation đã closed, archived

## Domain-Driven Design

### Entity Identity
Conversation identity defined by UUID:
- Unique across all conversations
- Immutable after creation
- Used cho database lookups

### Aggregate Pattern
```
Conversation (Aggregate Root)
  └── Messages (Child Entities)
```
- Conversation controls access to Messages
- External code không directly modify Messages
- All changes go through Conversation methods

### Invariants
Business rules maintained by entity:
- `updated_at` always updated when conversation changes
- Messages chỉ added qua add_message() method
- Title không thể empty (auto-generated)

## Best Practices

### Lazy Loading Messages
Messages có thể lazy-loaded:
```python
messages: Optional[List[Message]] = None
```
- Don't load all messages by default
- Load when needed (on-demand)
- Better performance cho list views

### Pagination
Với conversations có nhiều messages, consider pagination:
```python
def get_recent_messages(self, limit: int = 10) -> List[Message]:
    return self.messages[-limit:]
```

### Domain Events
Consider emitting events:
```python
def add_message(self, message: Message):
    self.messages.append(message)
    self.updated_at = datetime.utcnow()
    self.add_domain_event(MessageAddedEvent(self.id, message.id))
```

### Validation
Add business rule validation:
```python
def add_message(self, message: Message):
    if not self.is_active:
        raise ValueError("Cannot add message to closed conversation")
    if message.conversation_id != self.id:
        raise ValueError("Message belongs to different conversation")
    self.messages.append(message)
```

## Future Improvements

1. **Add message count**: Track total message count
2. **Add participants**: Support multi-user conversations
3. **Add conversation type**: One-on-one, group, channel
4. **Add tags**: Categorize conversations
5. **Add summary**: Auto-generate conversation summary
6. **Add sentiment**: Track conversation sentiment
7. **Add priority**: High/medium/low priority conversations
8. **Add scheduled close**: Auto-close after inactivity period
9. **Add archival**: Archive old conversations
10. **Add sharing**: Share conversations with other users
11. **Add encryption**: End-to-end encrypted conversations
12. **Add voice mode**: Voice conversation support
