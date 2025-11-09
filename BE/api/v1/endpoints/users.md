# api/v1/endpoints/users.py

## Mục đích
REST API endpoints cho user management. Cung cấp CRUD operations cho users bao gồm create, get by ID, và get by username.

## Chức năng chính

### 1. POST /users/ - Tạo User Mới
- **Input**: `UserCreate` (username, email, full_name optional)
- **Output**: `UserResponse` (HTTP 201 Created)
- **Validation**: Email format validation với EmailStr
- **Error Handling**:
  - 400 Bad Request nếu username/email đã tồn tại
  - Handle IntegrityError từ database constraints

### 2. GET /users/{user_id} - Lấy User theo ID
- **Input**: user_id (UUID)
- **Output**: `UserResponse`
- **Error Handling**: 404 Not Found nếu user không tồn tại

### 3. GET /users/username/{username} - Lấy User theo Username
- **Input**: username (string)
- **Output**: `UserResponse`
- **Error Handling**: 404 Not Found nếu username không tồn tại

## Request/Response Models

### UserCreate (Input)
```python
{
    "username": str,         # Required
    "email": EmailStr,       # Required, validated
    "full_name": str | None  # Optional
}
```

### UserResponse (Output)
```python
{
    "id": UUID,
    "username": str,
    "email": str,
    "full_name": str | None,
    "created_at": str,       # ISO 8601 format
    "is_active": bool
}
```

## Liên kết với các file khác

### Dependencies (Import)
- `application/use_cases/user_use_case.py` - Business logic layer
- `application/dto/user_dto.py` - UserCreateDTO, UserResponseDTO
- `core/exceptions/` - UserAlreadyExistsError, UserNotFoundError
- `api/dependencies.py` - `get_user_use_case()` dependency injection

### Được sử dụng bởi
- Frontend user registration/profile pages
- `api/v1/endpoints/chat.py` - Cần user_id để tạo conversations
- Admin panels
- Authentication flows (nếu có)

### Calls to
- `UserUseCase.create_user()` - Tạo user mới
- `UserUseCase.get_user()` - Lấy user theo ID
- `UserUseCase.get_user_by_username()` - Lấy user theo username

## Tác động nếu file này bị xóa

### 🟡 HIGH IMPACT - USER MANAGEMENT KHÔNG HOẠT ĐỘNG

Nếu xóa file này:

1. **Không tạo được users**:
   - Không thể onboard users mới
   - Chat endpoint sẽ fail vì cần valid user_id

2. **Không lấy được user info**:
   - Profile pages không hoạt động
   - Không hiển thị được user details

3. **Conversation attribution bị ảnh hưởng**:
   - Conversations cần user_id
   - Không biết ai là owner của conversation

4. **Authentication integration bị block**:
   - Nếu thêm auth sau này, không có endpoint để verify users

### Workaround
- Users có thể được tạo trực tiếp trong database
- Nhưng không có API interface cho frontend

### Cách thay thế
Cần tạo lại user endpoints với:
- Create user với validation
- Get user by ID và username
- Error handling cho duplicates và not found

## Error Handling Strategy

### 1. Duplicate User (400 Bad Request)
```python
try:
    response = await user_use_case.create_user(dto)
except UserAlreadyExistsError as e:
    raise HTTPException(status_code=400, detail=str(e))
except IntegrityError:
    raise HTTPException(status_code=400, detail="User already exists")
```

**Dual handling**: Business exception + Database constraint violation

### 2. User Not Found (404 Not Found)
```python
try:
    response = await user_use_case.get_user(user_id)
except UserNotFoundError as e:
    raise HTTPException(status_code=404, detail=str(e))
```

### 3. Generic Errors (500 Internal Server Error)
```python
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

## Validation Layers

### Layer 1: Pydantic Model Validation
```python
class UserCreate(BaseModel):
    username: str         # Auto-validate: not empty
    email: EmailStr       # Auto-validate: valid email format
    full_name: Optional[str] = None
```

### Layer 2: Business Logic Validation (UserUseCase)
- Check username uniqueness
- Check email uniqueness
- Validate business rules

### Layer 3: Database Constraints
- UNIQUE constraint on username
- UNIQUE constraint on email
- NOT NULL constraints

## Response Format Transformation

### DTO → Pydantic Response
```python
# UserResponseDTO from use case
response = await user_use_case.create_user(dto)

# Transform to Pydantic model
return UserResponse(
    id=response.id,
    username=response.username,
    email=response.email,
    full_name=response.full_name,
    created_at=response.created_at.isoformat(),  # DateTime → ISO string
    is_active=response.is_active,
)
```

**Why double models?**
- `UserCreate/UserResponse`: API layer (Pydantic for OpenAPI docs)
- `UserCreateDTO/UserResponseDTO`: Application layer (business logic)
- Separation of concerns: API contracts vs business models

## Best Practices

### ✅ Current Implementation
- RESTful endpoint design
- Proper HTTP status codes (201, 404, 400, 500)
- Email validation với EmailStr
- Dependency injection cho use cases
- Comprehensive error handling
- Type hints everywhere

### ⚠️ Missing Features
- **Authentication**: Không có authentication/authorization
- **Pagination**: Get all users endpoint không có
- **Update user**: Chỉ có create và read, không có update/delete
- **Password management**: Không có password field (nếu cần auth)
- **Rate limiting**: Không có protection chống spam

### 🔧 Potential Improvements
```python
# Update user profile
@router.patch("/{user_id}")
async def update_user(user_id: UUID, updates: UserUpdate):
    ...

# List users with pagination
@router.get("/")
async def list_users(skip: int = 0, limit: int = 100):
    ...

# Deactivate user
@router.delete("/{user_id}")
async def deactivate_user(user_id: UUID):
    ...
```

## Security Considerations

### ⚠️ Current Security Issues
1. **No authentication**: Anyone có thể tạo users
2. **No authorization**: Anyone có thể xem bất kỳ user nào
3. **No rate limiting**: Vulnerable to spam/DoS
4. **Username enumeration**: `/username/{username}` reveals user existence

### 🔒 Recommendations
- Add JWT authentication
- Add role-based access control
- Add rate limiting middleware
- Add CAPTCHA cho user creation
- Hash emails trong logs (GDPR compliance)
