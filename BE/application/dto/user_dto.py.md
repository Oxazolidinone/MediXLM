# application/dto/user_dto.py

## Mục đích
File này định nghĩa các Data Transfer Objects (DTO) cho tính năng quản lý người dùng, bao gồm UserCreateDTO cho việc tạo user mới và UserResponseDTO để trả về thông tin user. DTOs này đảm bảo validation email, username và cấu trúc dữ liệu nhất quán.

## Chức năng chính

### UserCreateDTO
- **username** (str): Tên đăng nhập của người dùng (required)
- **email** (EmailStr): Email của người dùng với validation tự động
- **full_name** (Optional[str]): Họ tên đầy đủ (optional)
- Validation: Email format, required fields

### UserResponseDTO
- **id** (UUID): ID duy nhất của người dùng
- **username** (str): Tên đăng nhập
- **email** (str): Địa chỉ email
- **full_name** (Optional[str]): Họ tên đầy đủ
- **created_at** (datetime): Thời gian tạo tài khoản
- **is_active** (bool): Trạng thái hoạt động của tài khoản

## Liên kết với các file khác

### Dependencies (Import)
- **pydantic**: BaseModel, EmailStr - Base class và email validation
- **datetime**: datetime - Kiểu dữ liệu timestamp
- **typing**: Optional - Type hints
- **uuid**: UUID - Kiểu dữ liệu UUID

### Được sử dụng bởi
- **api/v1/endpoints/users.py**: Validate request/response trong user API endpoints
- **application/use_cases/user_use_case.py**: Xử lý business logic cho user operations
- **application/dto/__init__.py**: Export để các module khác import

## Tác động nếu file này bị xóa

### 🟡 HIGH - User Management Broken

File này định nghĩa contract cho toàn bộ user management system. Nếu bị xóa:

- **User API endpoints bị lỗi**: Không thể tạo mới hoặc trả về thông tin user
- **Email validation bị mất**: Không kiểm tra được định dạng email hợp lệ
- **Mất data structure**: Không có cấu trúc chuẩn cho user data
- **Security risk**: Không validate input có thể dẫn đến injection attacks
- **API documentation bị mất**: Swagger/OpenAPI docs cho user endpoints sẽ không có

### Cách thay thế
1. Tạo lại Pydantic models với cùng schema và EmailStr validation
2. Implement manual email validation nếu không dùng Pydantic
3. Sử dụng dataclasses + custom validators (phức tạp hơn)
4. Dùng dict + manual validation (không khuyến khích)

## Best Practices

### Email Validation
- Sử dụng EmailStr của Pydantic để tự động validate email format
- Đảm bảo email uniqueness ở application layer (use case) và database layer

### Password Security
- DTOs hiện tại không có password field (có thể cần thêm AuthDTO riêng)
- Không bao giờ trả về password trong ResponseDTO

### Privacy
- UserResponseDTO không chứa thông tin nhạy cảm (password hash, tokens, etc.)
- Chỉ trả về thông tin cần thiết cho client
