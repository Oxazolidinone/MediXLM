# infrastructure/database/models.py

## Mục đích
File này định nghĩa SQLAlchemy ORM models cho PostgreSQL database schema. Models này map database tables đến Python classes, định nghĩa columns, relationships, và constraints. Đây là database layer trong Clean Architecture.

## Chức năng chính

### Base
Declarative base cho tất cả ORM models.

### UserModel
Database model cho users table:
- **Columns**: id, username, email, full_name, created_at, updated_at, is_active
- **Indexes**: username, email (unique indexes)
- **Relationships**: conversations (one-to-many)
- **Cascade**: Delete user → delete conversations

### ConversationModel
Database model cho conversations table:
- **Columns**: id, user_id (FK), title, created_at, updated_at, is_active
- **Indexes**: user_id
- **Relationships**:
  - user (many-to-one)
  - messages (one-to-many)
- **Cascade**: Delete conversation → delete messages

### MessageModel
Database model cho messages table:
- **Columns**: id, conversation_id (FK), role, content, created_at, message_metadata, tokens_used
- **Indexes**: conversation_id
- **Relationships**: conversation (many-to-one)
- **JSON field**: message_metadata stores arbitrary JSON data

## Liên kết với các file khác

### Dependencies (Import)
- **datetime**: datetime
- **uuid**: uuid4
- **sqlalchemy**: Column types, ForeignKey, relationship
- **sqlalchemy.dialects.postgresql**: UUID type
- **sqlalchemy.orm**: relationship, declarative_base

### Được sử dụng bởi
- **infrastructure/database/connection.py**: Import Base, create tables
- **infrastructure/repositories/user_repository_impl.py**: CRUD operations với UserModel
- **infrastructure/repositories/conversation_repository_impl.py**: CRUD với ConversationModel, MessageModel
- **infrastructure/repositories/sync_conversation_repository.py**: Sync operations

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Database Schema Lost

Models này định nghĩa entire database schema. Nếu bị xóa:

- **Database tables không được tạo**: init_database() fails
- **Repositories không hoạt động**: Không có models để query
- **Complete data persistence failure**: Không save được gì
- **Application hoàn toàn không hoạt động**: No database schema

### Cách thay thế
1. Recreate tất cả models với correct schema
2. Define relationships properly
3. Add indexes cho performance
4. Set up cascading deletes

## Technical Notes

### UUID Primary Keys
Sử dụng UUID thay vì auto-increment integers:
- Distributed-friendly
- No sequential ID guessing
- Better for security

### JSON Column
`message_metadata` sử dụng JSON type:
- Flexible schema cho metadata
- Native PostgreSQL JSON support
- Can query/index JSON fields

### Timestamps
Auto-managed timestamps:
- `default=datetime.utcnow` - Set on creation
- `onupdate=datetime.utcnow` - Update on modification

### Cascade Delete
- Delete User → Delete Conversations → Delete Messages
- Maintains referential integrity
- Prevents orphaned records
