# application/dto/conversation_dto.py

## Mục đích
File này định nghĩa các Data Transfer Objects (DTO) cho conversation (cuộc hội thoại) và message (tin nhắn). MessageDTO đại diện cho từng tin nhắn trong cuộc trò chuyện, còn ConversationDTO chứa metadata của cuộc hội thoại và danh sách tin nhắn.

## Chức năng chính

### MessageDTO
- **id** (UUID): ID duy nhất của tin nhắn
- **conversation_id** (UUID): ID của cuộc hội thoại chứa tin nhắn này
- **role** (str): Vai trò (user, assistant, system)
- **content** (str): Nội dung tin nhắn
- **created_at** (datetime): Thời gian tạo tin nhắn
- **tokens_used** (Optional[int]): Số token LLM đã sử dụng

### ConversationDTO
- **id** (UUID): ID duy nhất của cuộc hội thoại
- **user_id** (UUID): ID của người dùng sở hữu cuộc hội thoại
- **title** (Optional[str]): Tiêu đề cuộc hội thoại
- **created_at** (datetime): Thời gian tạo
- **updated_at** (datetime): Thời gian cập nhật lần cuối
- **is_active** (bool): Trạng thái hoạt động
- **messages** (Optional[List[MessageDTO]]): Danh sách tin nhắn trong cuộc hội thoại

## Liên kết với các file khác

### Dependencies (Import)
- **pydantic**: BaseModel - Base class cho DTOs
- **datetime**: datetime - Kiểu dữ liệu timestamp
- **typing**: Optional, List - Type hints
- **uuid**: UUID - Kiểu dữ liệu UUID

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Sử dụng MessageDTO để trả về lịch sử chat
- **api/v1/endpoints/chat.py**: Serialize conversation history cho API responses
- **application/dto/__init__.py**: Export để các module khác import

## Tác động nếu file này bị xóa

### 🟡 HIGH - Chat History and Conversation Management Broken

File này định nghĩa cấu trúc dữ liệu cho conversation và message history. Nếu bị xóa:

- **Không thể trả về lịch sử chat**: API endpoints cho conversation history sẽ bị lỗi
- **Mất cấu trúc message**: Không có format chuẩn cho tin nhắn
- **Frontend không hiển thị được chat history**: Client không biết cấu trúc dữ liệu
- **Validation bị mất**: Không kiểm tra được role, content của message
- **API documentation bị thiếu**: Swagger docs cho conversation endpoints sẽ không đầy đủ

### Cách thay thế
1. Tạo lại Pydantic models với cùng schema
2. Sử dụng nested dictionaries (mất type safety và validation)
3. Tạo separate DTOs cho Message và Conversation (recommended practice)
4. Sử dụng Entity classes trực tiếp (vi phạm Clean Architecture)

## Best Practices

### Nested DTOs
- ConversationDTO chứa List[MessageDTO] để biểu diễn one-to-many relationship
- Cho phép lazy loading: messages có thể là Optional

### Role Validation
- Role field nên được validate với enum (user/assistant/system)
- Cân nhắc tạo RoleEnum thay vì dùng string

### Pagination
- Với conversations có nhiều messages, cần implement pagination
- Có thể cần thêm MessageListDTO với metadata (total_count, page, etc.)

### Token Tracking
- tokens_used giúp monitor chi phí LLM API
- Quan trọng cho cost optimization và rate limiting
