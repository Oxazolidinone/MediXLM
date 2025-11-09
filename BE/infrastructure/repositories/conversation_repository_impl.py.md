# infrastructure/repositories/conversation_repository_impl.py

## Mục đích
File này implements IConversationRepository interface với SQLAlchemy ORM. Provides concrete implementation cho conversation và message data access. Handles conversation CRUD, message persistence, và eager/lazy loading của messages.

## Chức năng chính

### ConversationRepositoryImpl Class

#### Conversation Operations
- **create**: Insert ConversationModel vào DB
- **get_by_id**: Query với eager loading messages (selectinload)
- **get_by_user_id**: Get user's conversations với pagination, ordered by updated_at DESC
- **update**: Update conversation fields
- **delete**: Delete conversation (cascade delete messages)

#### Message Operations
- **add_message**: Insert MessageModel vào DB
- **get_messages**: Get conversation messages với pagination, ordered by created_at ASC

#### Helper Methods
- **_to_entity**: Convert ConversationModel → Conversation entity (with messages)
- **_message_to_entity**: Convert MessageModel → Message entity

## Liên kết với các file khác

### Dependencies
- **sqlalchemy**: select
- **sqlalchemy.orm**: Session, selectinload (eager loading)
- **domain.entities**: Conversation, Message, MessageRole
- **domain.repositories**: IConversationRepository
- **infrastructure.database.models**: ConversationModel, MessageModel

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Create repository instance
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Conversation Data Access Lost

Nếu bị xóa:
- **Chat completely fails**: Không persist conversations/messages
- **Conversation history lost**: Không retrieve messages
- **Application unusable**: Chat là core feature

### Cách thay thế
Recreate implementation với SQLAlchemy ORM operations, eager loading, và entity conversion.
