# application/use_cases/user_use_case.py

## Mục đích
File này chứa business logic cho user management, bao gồm tạo user mới, lấy thông tin user, cập nhật profile. UserUseCase đảm bảo validation business rules (unique username/email) và xử lý errors phù hợp trước khi persist data.

## Chức năng chính

### UserUseCase Class
Quản lý user lifecycle với dependency:
- **user_repository**: IUserRepository interface để truy cập data layer

### create_user(user_data: UserCreateDTO) -> UserResponseDTO
Tạo user mới với validation:
1. **Check username exists**: Kiểm tra username đã tồn tại chưa
2. **Check email exists**: Kiểm tra email đã được sử dụng chưa
3. **Create User entity**: Tạo domain entity từ DTO
4. **Save to repository**: Persist user vào database
5. **Handle IntegrityError**: Catch race condition từ database constraints
6. **Return UserResponseDTO**: Trả về user data

### get_user(user_id: UUID) -> UserResponseDTO
Lấy thông tin user theo ID:
- Raise UserNotFoundError nếu không tìm thấy
- Trả về UserResponseDTO

### get_user_by_username(username: str) -> Optional[UserResponseDTO]
Tìm user theo username:
- Trả về None nếu không tìm thấy (không raise error)
- Useful cho authentication flow

### update_user_profile(user_id, full_name, email) -> UserResponseDTO
Cập nhật profile của user:
1. Get user by ID
2. Update entity với new values
3. Persist changes
4. Return updated UserResponseDTO

## Liên kết với các file khác

### Dependencies (Import)
- **application/dto**: UserCreateDTO, UserResponseDTO
- **domain/entities**: User
- **domain/repositories**: IUserRepository
- **core/exceptions**: UserAlreadyExistsError, UserNotFoundError
- **infrastructure/database/connection**: get_database_session
- **infrastructure/repositories**: UserRepositoryImpl
- **sqlalchemy.exc**: IntegrityError

### Được sử dụng bởi
- **api/v1/endpoints/users.py**: User API endpoints (create, get, update user)
- **api/dependencies.py**: Dependency injection setup

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - User Management System Failure

File này là core của user management. Nếu bị xóa:

- **Không thể tạo user mới**: Registration sẽ không hoạt động
- **Không thể lấy thông tin user**: Profile pages sẽ bị lỗi
- **Không thể update profile**: Users không thể chỉnh sửa thông tin
- **Mất business validation**: Duplicate username/email sẽ không được check
- **User API endpoints hoàn toàn không hoạt động**
- **Chat system bị ảnh hưởng**: Chat cần user_id để tạo conversations

### Cách thay thế
1. **Tạo lại UserUseCase** với cùng interface
2. **Implement lại business rules**:
   - Unique username validation
   - Unique email validation
   - Error handling cho race conditions
3. **Re-implement CRUD operations** với proper error handling
4. **Maintain async/sync pattern** với thread executor
5. **Add transaction management** trong session context

## Technical Notes

### Thread Executor Pattern
Sử dụng `asyncio.run_in_executor()` để chạy sync database operations:
```python
loop = asyncio.get_event_loop()
created_user = await loop.run_in_executor(None, sync_operations)
```

### Session Management
Mỗi operation tạo fresh session với `get_database_session()` context manager:
```python
with get_database_session() as session:
    user_repo = UserRepositoryImpl(session)
    # operations...
```

### Race Condition Handling
Double-check pattern + IntegrityError catch để handle concurrent user creation:
1. Check if user exists (business logic)
2. Try to create user
3. Catch IntegrityError if database constraint violated (race condition)

### Error Hierarchy
- **UserAlreadyExistsError**: Business rule violation (duplicate username/email)
- **UserNotFoundError**: Resource not found
- **IntegrityError**: Database constraint violation (caught và converted to business error)

## Best Practices

### Separation of Concerns
- Use case chứa business logic
- Repository chứa data access logic
- DTO cho data transfer
- Entity cho domain model

### Validation Layers
1. **DTO validation**: Pydantic validates input format (EmailStr, required fields)
2. **Business validation**: Use case checks business rules (uniqueness)
3. **Database validation**: Constraints trong schema là last line of defense

### Error Handling
- Use custom exceptions cho business errors
- Catch và convert infrastructure exceptions
- Return meaningful error messages cho client

## Future Improvements

1. **Add password management**: Hash passwords, change password functionality
2. **Add email verification**: Send verification email sau khi register
3. **Add user roles**: Admin, user, moderator roles
4. **Implement soft delete**: Deactivate instead of hard delete
5. **Add audit logging**: Track user creation, updates
6. **Add pagination**: For listing users (admin feature)
