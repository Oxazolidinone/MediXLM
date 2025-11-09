# domain/repositories/conversation_repository.py

## Mục đích
File này định nghĩa IConversationRepository interface - abstract contract cho conversation và message data access. Interface này định nghĩa operations cho managing conversations và messages mà không phụ thuộc vào database implementation.

## Chức năng chính

### IConversationRepository Interface (ABC)

#### Conversation Operations
- **create(conversation: Conversation) -> Conversation**: Tạo conversation mới
- **get_by_id(conversation_id: UUID) -> Optional[Conversation]**: Lấy conversation theo ID
- **get_by_user_id(user_id: UUID, skip, limit) -> List[Conversation]**: Lấy conversations của user với pagination
- **update(conversation: Conversation) -> Conversation**: Cập nhật conversation
- **delete(conversation_id: UUID) -> bool**: Xóa conversation

#### Message Operations
- **add_message(message: Message) -> Message**: Thêm message vào conversation
- **get_messages(conversation_id: UUID, skip, limit) -> List[Message]**: Lấy messages của conversation với pagination

## Liên kết với các file khác

### Dependencies (Import)
- **abc**: ABC, abstractmethod
- **typing**: List, Optional
- **uuid**: UUID
- **domain.entities**: Conversation, Message

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Depends on interface
- **infrastructure/repositories/conversation_repository_impl.py**: Implements interface
- **infrastructure/repositories/sync_conversation_repository.py**: Sync implementation
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Chat Repository Contract Lost

Interface này là contract cho chat data access. Nếu bị xóa:

- **Chat use case bị lỗi**: Không biết conversation repository contract
- **Message persistence bị mất**: Không có standard interface cho message operations
- **Clean Architecture vi phạm**: Use cases phụ thuộc trực tiếp vào infrastructure
- **Testing impossible**: Không mock được repository
- **Implementation switching bị mất**: Không thể đổi database dễ dàng

### Cách thay thế
Recreate ABC interface với conversation và message operations.
