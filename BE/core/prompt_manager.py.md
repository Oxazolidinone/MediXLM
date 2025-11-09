# core/prompt_manager.py

## Mục đích
File này cung cấp PromptManager class để quản lý prompt templates từ files, với caching và template formatting capabilities. Đây là advanced version của prompts.py, cho phép load multiple prompt templates và format chúng với dynamic variables.

## Chức năng chính

### PromptManager Class
Quản lý prompt templates với features:
- **prompts_dir**: Directory chứa prompt template files
- **_template_cache**: Dict để cache loaded templates
- **@lru_cache** trên load_prompt method để optimize performance

### __init__(prompts_dir: Optional[Path] = None)
Initialize PromptManager:
- **Default prompts_dir**: `{project_root}/prompts/`
- Auto-detect prompts directory từ file location
- Initialize empty template cache

### load_prompt(prompt_name: str) -> str
Load prompt template từ file với caching:
- **Path**: `prompts/{prompt_name}.txt`
- **Caching**: LRU cache với maxsize=32
- **Error handling**: Raise FileNotFoundError nếu template không tồn tại
- Return raw template string

### format_prompt(prompt_name: str, **kwargs: Any) -> str
Load và format prompt template với variables:
- Load template từ file (cached)
- Replace placeholders `{variable_name}` với values từ kwargs
- Handle None values (replace với empty string)
- Return formatted prompt string

### clear_cache()
Clear tất cả cached templates:
- Clear LRU cache của load_prompt
- Clear _template_cache dict

### get_prompt_manager() -> PromptManager
Singleton factory function:
- Return global _prompt_manager instance
- Lazy initialization: Create on first call
- Ensure single instance across application

## Liên kết với các file khác

### Dependencies (Import)
- **os**: Operating system interface
- **pathlib**: Path - File path operations
- **typing**: Dict, Any, Optional - Type hints
- **functools**: lru_cache - Caching decorator

### Được sử dụng bởi
- **Application use cases**: Format prompts với dynamic data
- **LLM services**: Get formatted prompts cho LLM calls
- **Chat system**: Build conversation-specific prompts

## Tác động nếu file này bị xóa

### 🟢 LOW - Advanced Prompt Management Lost

File này là optional enhancement cho prompt management. Nếu bị xóa:

- **Basic prompts vẫn hoạt động**: core/prompts.py vẫn còn
- **Mất template formatting**: Không format prompts với variables
- **Mất caching**: Performance hit khi load prompts nhiều lần
- **Mất centralized prompt management**: Khó manage multiple prompt templates
- **Code duplication**: Phải manually load và format prompts

### Cách thay thế
1. **Use core/prompts.py**: Basic prompt functions vẫn available
2. **Manual file reading**: Read prompt files directly với open()
3. **Hardcode prompts**: Embed prompts trong code (không khuyến khích)
4. **Use template engine**: Jinja2, Mako cho advanced templating
5. **Recreate PromptManager**: Implement lại với cùng interface

## Technical Notes

### Template Placeholder Format
Templates sử dụng `{variable_name}` syntax:
```
Hello {user_name}, you asked about {topic}.
Based on your symptoms: {symptoms}, I recommend...
```

### Formatting Example
```python
manager = get_prompt_manager()
prompt = manager.format_prompt(
    "medical_advice",
    user_name="John",
    topic="diabetes",
    symptoms="increased thirst, frequent urination"
)
```

### LRU Cache Benefits
- **Performance**: Avoid repeated file I/O
- **Memory efficient**: LRU eviction policy (maxsize=32)
- **Thread-safe**: functools.lru_cache is thread-safe

### Singleton Pattern
Global _prompt_manager ensures:
- Single instance across application
- Shared cache across all callers
- Consistent configuration

## Comparison với core/prompts.py

### core/prompts.py
- **Simple**: Basic functions để build prompts
- **Hardcoded logic**: Specific functions cho specific prompts
- **Limited flexibility**: Không support custom templates

### core/prompt_manager.py
- **Flexible**: Generic template loading và formatting
- **File-based**: Templates trong files, dễ edit
- **Cacheable**: Automatic caching cho performance
- **Extensible**: Easy thêm new templates

## Best Practices

### Template Organization
- Một file per prompt type: `medical_advice.txt`, `emergency.txt`, etc.
- Clear naming convention cho template files
- Document required variables trong template comments

### Template Variables
- Use descriptive variable names: `{user_name}`, `{symptoms}`, `{medical_history}`
- Document required vs optional variables
- Provide defaults cho optional variables

### Error Handling
- Validate template exists before formatting
- Handle missing variables gracefully
- Log template loading errors

### Performance
- Leverage LRU cache cho frequently-used templates
- Clear cache nếu templates được updated
- Monitor cache hit rate

## Current Limitations

### Simple String Replacement
Chỉ support simple `{variable}` replacement, không có:
- Conditional logic (if/else)
- Loops (for)
- Filters (uppercase, truncate, etc.)
- Template inheritance

### No Template Validation
Không validate:
- Required variables present
- Variable types correct
- Template syntax valid

### No Hot Reload
Templates chỉ load once và cached. Code changes cần clear cache hoặc restart.

## Future Improvements

1. **Use Jinja2**: Full-featured template engine với logic, filters, inheritance
2. **Template validation**: Validate required variables, syntax
3. **Hot reload**: Auto-reload templates khi files change
4. **Version control**: Track template versions trong database
5. **A/B testing**: Support multiple template versions
6. **Multilingual templates**: Load templates based on user language
7. **Template preview**: API endpoint để preview formatted templates
8. **Template analytics**: Track which templates perform best
9. **Dynamic template loading**: Load templates từ database instead of files
10. **Template composition**: Compose complex prompts từ smaller templates

## Example Usage

```python
# Get singleton manager
manager = get_prompt_manager()

# Load raw template
template = manager.load_prompt("medical_advice")

# Format template với variables
formatted = manager.format_prompt(
    "medical_advice",
    user_name="John Doe",
    symptoms="fever, cough",
    duration="3 days",
    medical_history="diabetes"
)

# Clear cache after updating templates
manager.clear_cache()
```
