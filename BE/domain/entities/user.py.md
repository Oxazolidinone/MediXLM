# domain/entities/user.py

## Mục đích
File này định nghĩa User entity - domain model đại diện cho người dùng trong hệ thống. User entity chứa business logic cho user operations như tạo user, update profile, deactivate account. Đây là pure domain object, không phụ thuộc vào infrastructure.

## Chức năng chính

### User Dataclass
Domain entity với attributes:
- **id** (UUID): Unique identifier
- **username** (str): Tên đăng nhập duy nhất
- **email** (str): Email address
- **full_name** (Optional[str]): Họ tên đầy đủ
- **created_at** (datetime): Thời gian tạo account
- **updated_at** (datetime): Thời gian cập nhật lần cuối
- **is_active** (bool): Trạng thái hoạt động (default: True)

### __post_init__()
Auto-initialize timestamps:
- Set created_at = datetime.utcnow() nếu None
- Set updated_at = datetime.utcnow() nếu None

### create(username, email, full_name) -> User
Static factory method tạo User entity mới:
- Generate UUID tự động
- Initialize với provided data
- Set timestamps automatically
- Return new User instance

### update_profile(full_name, email)
Update user profile information:
- Update full_name nếu provided
- Update email nếu provided
- Auto-update updated_at timestamp

### deactivate()
Deactivate user account:
- Set is_active = False
- Update updated_at timestamp

## Liên kết với các file khác

### Dependencies (Import)
- **dataclasses**: dataclass - Decorator cho data classes
- **datetime**: datetime - Timestamp type
- **typing**: Optional - Type hints
- **uuid**: UUID, uuid4 - Unique identifiers

### Được sử dụng bởi
- **application/use_cases/user_use_case.py**: Business logic cho user operations
- **infrastructure/repositories/user_repository_impl.py**: Persist User entities
- **domain/entities/__init__.py**: Export để các modules khác import
- **application/dto/user_dto.py**: Convert between Entity và DTO

## Tác động nếu file này bị xóa

### 🟡 HIGH - User Domain Model Lost

User entity là core domain model cho user management. Nếu bị xóa:

- **Mất domain model**: Không có representation của User trong domain layer
- **User use case bị lỗi**: Use cases không biết User structure
- **Repository implementation bị lỗi**: Không có entity để convert từ/đến database models
- **Business logic bị mất**: update_profile, deactivate methods bị mất
- **Clean Architecture vi phạm**: Application layer phụ thuộc trực tiếp vào infrastructure models

### Cách thay thế
1. **Recreate User dataclass** với cùng attributes và methods
2. **Use database model trực tiếp**: Vi phạm Clean Architecture (không khuyến khích)
3. **Use DTOs everywhere**: Mất domain logic layer (không khuyến khích)
4. **Create new domain model**: Implement lại với cùng interface

## Technical Notes

### Dataclass vs Regular Class
Sử dụng @dataclass vì:
- **Auto __init__**: Không cần viết constructor
- **Auto __repr__**: String representation tự động
- **Auto __eq__**: Equality comparison based on fields
- **Immutability option**: Có thể set frozen=True nếu cần

### Factory Method Pattern
`create()` là static factory method:
- **Encapsulation**: Hide UUID generation logic
- **Consistency**: Ensure proper initialization
- **Convenience**: Cleaner than calling constructor directly

### Business Logic trong Entity
Entity chứa business logic methods:
- **update_profile()**: Encapsulate update logic
- **deactivate()**: Encapsulate deactivation logic
- **Automatic timestamp updates**: Business rule enforcement

### UTC Timestamps
Sử dụng `datetime.utcnow()` thay vì `datetime.now()`:
- **Timezone-agnostic**: Avoid timezone issues
- **Database best practice**: Store UTC, convert to local on display
- **Consistency**: All timestamps trong same timezone

## Domain-Driven Design Principles

### Entity Characteristics
- **Identity**: User có unique ID (UUID)
- **Lifecycle**: User can be created, updated, deactivated
- **Business Logic**: Methods encapsulate business rules
- **Persistence Ignorance**: Không biết về database implementation

### Aggregates
User có thể là aggregate root:
- **User** (root)
- **Conversations** (child entities)
- **Messages** (child entities through Conversation)

### Value Objects
Email, username có thể là value objects trong thiết kế nghiêm ngặt hơn.

## Best Practices

### Immutability
Consider making entities immutable (frozen=True) và use methods return new instances:
```python
@dataclass(frozen=True)
class User:
    def with_updated_email(self, email: str) -> User:
        return User(..., email=email, updated_at=datetime.utcnow())
```

### Validation
Add validation trong entity:
```python
def __post_init__(self):
    if not self.username or len(self.username) < 3:
        raise ValueError("Username must be at least 3 characters")
```

### Domain Events
Consider thêm domain events:
```python
def deactivate(self):
    self.is_active = False
    self.updated_at = datetime.utcnow()
    self.add_domain_event(UserDeactivatedEvent(self.id))
```

## Future Improvements

1. **Add validation**: Validate username format, email format trong entity
2. **Add domain events**: Emit events cho user lifecycle changes
3. **Add value objects**: Email, Username as value objects
4. **Add password field**: Hash password handling
5. **Add roles**: User roles (admin, user, moderator)
6. **Add preferences**: User preferences, settings
7. **Add activation flow**: Email verification, activation tokens
8. **Add audit trail**: Track who created/updated user
9. **Add soft delete**: Deleted_at timestamp thay vì hard delete
10. **Add user statistics**: Login count, last login, etc.
