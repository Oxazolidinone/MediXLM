# infrastructure/repositories/user_repository_impl.py

## Mục đích
File này implements IUserRepository interface sử dụng SQLAlchemy ORM. Provides concrete implementation cho user data access operations với PostgreSQL database. Converts giữa UserModel (database) và User entity (domain).

## Chức năng chính

### UserRepositoryImpl Class
Implements IUserRepository với SQLAlchemy Session:

#### __init__(session: Session)
Initialize repository với database session.

#### create(user: User) -> User
Convert User entity → UserModel, insert vào database, flush, convert back to User entity.

#### get_by_id(user_id: UUID) -> Optional[User]
Query UserModel by ID, convert to User entity nếu found.

#### get_by_username(username: str) -> Optional[User]
Query UserModel by username (indexed).

#### get_by_email(email: str) -> Optional[User]
Query UserModel by email (indexed).

#### update(user: User) -> User
Get UserModel by ID, update fields, flush, return updated User entity.

#### delete(user_id: UUID) -> bool
Get UserModel by ID, delete, flush, return success status.

#### _to_entity(model: UserModel) -> User
Static method convert UserModel → User entity.

## Liên kết với các file khác

### Dependencies
- **sqlalchemy**: select - Query builder
- **sqlalchemy.orm**: Session
- **domain.entities**: User
- **domain.repositories**: IUserRepository (interface)
- **infrastructure.database.models**: UserModel

### Được sử dụng bởi
- **application/use_cases/user_use_case.py**: Create repository instance với session
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - User Data Access Lost

Nếu bị xóa:
- **User operations hoàn toàn fail**: Không persist users
- **Registration không hoạt động**: Không tạo được users
- **User lookup fails**: Không get user info
- **Application unusable**: Cần users cho chat

### Cách thay thế
Recreate implementation của IUserRepository với SQLAlchemy operations và entity/model conversion.
