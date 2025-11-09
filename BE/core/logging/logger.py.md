# core/logging/logger.py

## Mục đích
File này cung cấp centralized logging configuration cho toàn bộ ứng dụng. Setup logging với proper format, log level từ settings, và output đến stdout để dễ dàng monitor trong Docker và production environments.

## Chức năng chính

### setup_logging()
Configure logging cho application:
- **Log level**: Lấy từ settings.LOG_LEVEL (INFO, DEBUG, WARNING, ERROR)
- **Format**: Timestamp, logger name, level, message
- **Handler**: StreamHandler output đến stdout
- Setup basic config với `logging.basicConfig()`

### get_logger(name: Optional[str] = None) -> logging.Logger
Factory function để tạo logger instances:
- **name**: Logger name (thường là __name__ của module)
- **Return**: Configured logger instance
- Cho phép mỗi module có logger riêng với tên riêng

## Liên kết với các file khác

### Dependencies (Import)
- **logging**: Python standard logging library
- **sys**: System module để access stdout
- **typing**: Optional type hint
- **core.config**: settings - Lấy LOG_LEVEL

### Được sử dụng bởi
Có thể được sử dụng bởi bất kỳ module nào cần logging:
- **Use cases**: Log business logic events
- **Repositories**: Log database operations
- **Services**: Log external service calls
- **API endpoints**: Log requests/responses

## Tác động nếu file này bị xóa

### 🟢 LOW - Logging Configuration Lost

File này chỉ setup logging config, không critical cho core functionality. Nếu bị xóa:

- **Logging vẫn hoạt động**: Python có default logging
- **Mất centralized config**: Mỗi module phải tự setup logging
- **Inconsistent log format**: Logs sẽ không có format thống nhất
- **Debug khó khăn hơn**: Không có structured logs với timestamps
- **Production monitoring khó hơn**: Logs không standardized

### Cách thay thế
1. **Tạo lại logging setup function** với basicConfig
2. **Sử dụng default Python logging** (không khuyến khích)
3. **Implement logging trong mỗi module** riêng lẻ (duplicated code)
4. **Use third-party logging library** như structlog, loguru

## Technical Notes

### Log Format
Current format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
Example output:
```
2024-01-15 10:30:45,123 - api.v1.endpoints.chat - INFO - Processing chat request
```

### Log Levels
- **DEBUG**: Detailed information, typically for diagnosing problems
- **INFO**: Confirmation that things are working as expected
- **WARNING**: Something unexpected happened, but app still works
- **ERROR**: More serious problem, some function failed
- **CRITICAL**: Serious error, program may not continue

### StreamHandler to Stdout
Output đến stdout (không phải file) vì:
- **Docker-friendly**: Docker logs capture stdout
- **Cloud-friendly**: Cloud platforms (AWS, GCP) capture stdout logs
- **Real-time monitoring**: Logs hiển thị ngay trong console

### Logger Naming
Best practice: Sử dụng `__name__` để logger có tên theo module:
```python
logger = get_logger(__name__)  # logger name: "api.v1.endpoints.chat"
```

## Best Practices

### Structured Logging
Consider chuyển sang structured/JSON logging cho production:
```python
{
    "timestamp": "2024-01-15T10:30:45Z",
    "level": "INFO",
    "module": "api.v1.endpoints.chat",
    "message": "Processing chat request",
    "user_id": "123",
    "conversation_id": "456"
}
```

### Log Correlation
Add correlation IDs để track requests across services:
```python
logger.info("Processing request", extra={"request_id": request_id})
```

### Sensitive Data
Never log sensitive information:
- Passwords, tokens, API keys
- Personal health information (PHI)
- Credit card numbers

### Performance
- Use lazy formatting: `logger.debug("Value: %s", expensive_func())` instead of f-strings
- Consider log sampling cho high-traffic endpoints

## Current Limitations

### No File Output
Logs chỉ đến stdout, không save vào files. Cần external tool (Docker, systemd) để persist logs.

### No Rotation
Không có log rotation logic. Nếu output đến file, cần implement rotation.

### No Filtering
Không có advanced filtering based on module, level, etc.

### Simple Format
Format đơn giản, không phải JSON. Khó parse bằng log aggregation tools.

## Future Improvements

1. **Structured logging**: JSON format logs với fields
2. **Log correlation**: Request IDs, trace IDs
3. **Log levels per module**: Different log levels cho different modules
4. **Log sanitization**: Automatically redact sensitive data
5. **Log aggregation integration**: Integrate với ELK, Datadog, Sentry
6. **Performance logging**: Log request duration, database query times
7. **Error tracking**: Integrate với Sentry cho error tracking
8. **Audit logging**: Separate audit trail cho compliance
