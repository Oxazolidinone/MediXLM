# infrastructure/repositories/sync_conversation_repository.py

## Mục đích
File này provides synchronous conversation repository implementation, tương tự ConversationRepositoryImpl nhưng không implement interface. Designed để sử dụng trong thread executors với sync SQLAlchemy sessions để tránh greenlet errors.

## Chức năng chính

### SyncConversationRepository Class
Synchronous operations (không inherit từ IConversationRepository):

#### Operations
- **create**: Create conversation synchronously
- **get_by_id**: Get conversation by ID
- **get_by_user_id**: Get user's conversations
- **add_message**: Add message synchronously
- **get_messages**: Get conversation messages

Note: Không có async/await, pure synchronous operations.

## Liên kết với các file khác

### Dependencies
- Same as ConversationRepositoryImpl
- No interface implementation

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Used trong thread executor để avoid greenlet errors

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Chat Use Case Broken

Nếu bị xóa:
- **Chat use case fails**: Depends on this for sync operations
- **Thread executor pattern broken**: Greenlet errors return

### Cách thay thế
Use async repository directly (but may cause greenlet errors) hoặc recreate sync version.
