# application/dto/chat_dto.py

## Mục đích
File này định nghĩa các Data Transfer Objects (DTO) cho tính năng chat, bao gồm ChatRequestDTO để nhận yêu cầu từ client và ChatResponseDTO để trả về kết quả cho client. DTOs này đảm bảo validation và cấu trúc dữ liệu nhất quán giữa API và application layer.

## Chức năng chính

### ChatRequestDTO
- **message** (str): Nội dung tin nhắn từ người dùng
- **conversation_id** (Optional[UUID]): ID của cuộc hội thoại (None nếu tạo mới)
- **user_id** (Optional[UUID]): ID của người dùng
- **context** (Optional[Dict]): Thông tin ngữ cảnh bổ sung

### ChatResponseDTO
- **message** (str): Nội dung phản hồi từ AI
- **conversation_id** (UUID): ID của cuộc hội thoại
- **message_id** (UUID): ID của tin nhắn phản hồi
- **related_knowledge** (Optional[List]): Danh sách kiến thức y tế liên quan
- **tokens_used** (Optional[int]): Số token đã sử dụng
- **confidence_score** (Optional[float]): Độ tin cậy của câu trả lời

## Liên kết với các file khác

### Dependencies (Import)
- **pydantic**: BaseModel - Base class cho DTOs
- **typing**: Optional, List, Dict, Any - Type hints
- **uuid**: UUID - Kiểu dữ liệu UUID

### Được sử dụng bởi
- **api/v1/endpoints/chat.py**: Sử dụng để validate request/response trong API endpoints
- **application/use_cases/chat_use_case.py**: Sử dụng để xử lý logic nghiệp vụ chat
- **application/dto/__init__.py**: Export để các module khác import dễ dàng

## Tác động nếu file này bị xóa

### 🟡 HIGH - Application API Contract Broken

File này định nghĩa contract giữa API layer và Application layer cho tính năng chat. Nếu bị xóa:

- **API endpoints chat sẽ bị lỗi**: Không thể validate và serialize request/response
- **Mất type safety**: Không có cấu trúc dữ liệu chuẩn cho chat operations
- **Breaking change**: Client applications sẽ không biết cấu trúc dữ liệu để gửi/nhận
- **Validation bị mất**: Không kiểm tra được input từ client
- **Documentation tự động bị mất**: FastAPI dựa vào DTOs để tạo OpenAPI/Swagger docs

### Cách thay thế
1. Tạo lại các Pydantic models với cùng schema
2. Sử dụng dict thông thường (không khuyến khích - mất validation)
3. Tạo dataclasses thay thế (mất validation và serialization tự động)
4. Sử dụng TypedDict (chỉ có type hints, không có validation)

## Best Practices

### Validation
- DTOs sử dụng Pydantic để tự động validate dữ liệu đầu vào
- Type hints đảm bảo IDE có thể autocomplete và type checking

### Immutability
- DTOs nên được coi là immutable sau khi tạo
- Chỉ dùng để transfer data, không chứa business logic

### Serialization
- `Config.from_attributes = True` cho phép tạo DTO từ ORM models hoặc entities
- Tự động serialize UUID, datetime thành JSON-compatible format
