# domain/repositories/user_repository.py

## Mục đích
File này định nghĩa IUserRepository interface - abstract contract cho user data access. Interface này định nghĩa các operations cần thiết cho user management mà không phụ thuộc vào implementation cụ thể (SQLAlchemy, MongoDB, etc.). Đây là core của Dependency Inversion Principle trong Clean Architecture.

## Chức năng chính

### IUserRepository Interface (ABC)
Abstract base class định nghĩa user repository contract:

#### create(user: User) -> User
Tạo user mới trong database và return created user.

#### get_by_id(user_id: UUID) -> Optional[User]
Lấy user theo ID, return None nếu không tìm thấy.

#### get_by_username(username: str) -> Optional[User]
Lấy user theo username, return None nếu không tìm thấy.

#### get_by_email(email: str) -> Optional[User]
Lấy user theo email, return None nếu không tìm thấy.

#### update(user: User) -> User
Cập nhật user và return updated user.

#### delete(user_id: UUID) -> bool
Xóa user, return True nếu thành công.

## Liên kết với các file khác

### Dependencies (Import)
- **abc**: ABC, abstractmethod - Abstract base class support
- **typing**: Optional - Type hints
- **uuid**: UUID - UUID type
- **domain.entities**: User - User entity

### Được sử dụng bởi
- **application/use_cases/user_use_case.py**: Depends on interface, không phụ thuộc implementation
- **infrastructure/repositories/user_repository_impl.py**: Implements interface với SQLAlchemy
- **api/dependencies.py**: Dependency injection setup

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - Repository Pattern Broken

Interface này là foundation của repository pattern. Nếu bị xóa:

- **Use cases bị lỗi**: UserUseCase không biết user repository contract
- **Dependency injection bị mất**: Không thể inject repository implementations
- **Clean Architecture vi phạm**: Application layer phụ thuộc trực tiếp vào infrastructure
- **Testability bị mất**: Không thể mock repository cho unit tests
- **Flexibility bị mất**: Không thể switch database implementations dễ dàng

### Cách thay thế
1. Recreate ABC interface với tất cả abstract methods
2. Use cases depend on interface
3. Infrastructure implements interface
4. Dependency injection binds interface to implementation
