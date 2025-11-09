# core/prompts.py

## Mục đích
File này quản lý tất cả prompts cho LLM, bao gồm system prompts, emergency prompts, symptom assessment prompts. Provides functions để build prompts với medical knowledge context và format knowledge graph results. Đây là template engine cho LLM interactions.

## Chức năng chính

### PROMPTS_DIR
Path constant đến thư mục chứa prompt templates (prompts/system_prompt.txt).

### load_system_prompt() -> str
Load base system prompt từ file:
- Read từ `prompts/system_prompt.txt`
- Return prompt content as string
- Base prompt định nghĩa AI personality và medical guidelines

### build_chat_prompt(knowledge_context: Optional[str] = None) -> str
Build system prompt cho chat với optional medical knowledge:
- **No knowledge**: Return base system prompt
- **With knowledge**: Append knowledge context section
- Add instruction để use knowledge và recommend professional medical evaluation

### build_emergency_prompt() -> str
Build prompt cho emergency situations:
- Detect emergency symptoms
- Provide immediate action instructions
- List common emergency symptoms
- Emphasize calling emergency services

### build_symptom_assessment_prompt() -> str
Build prompt để assess symptoms:
- Questions về symptom onset, severity, triggers
- Guide user để provide detailed information
- Help determine urgency level (immediate/urgent/monitor)

### format_knowledge_context(knowledge_items: list) -> str
Format knowledge graph results cho LLM prompt:
- **Input**: List of knowledge dicts với name, type, description
- **Output**: Formatted string với bullet points
- Return "No specific medical knowledge found" nếu empty

## Liên kết với các file khác

### Dependencies (Import)
- **pathlib**: Path - File path operations
- **typing**: Optional - Type hints

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: Build prompts cho chat responses
- **api/v1/endpoints/chat.py**: May directly use prompts
- Bất kỳ service nào cần interact với LLM

## Tác động nếu file này bị xóa

### 🔴 CRITICAL - LLM Prompt System Failure

File này cung cấp tất cả prompts cho LLM. Nếu bị xóa:

- **Chat không có system instructions**: AI sẽ không biết cách respond properly
- **Medical knowledge không được inject**: RAG system không hoạt động
- **Emergency detection bị mất**: Không có prompts để handle emergencies
- **Symptom assessment không hoạt động**: Không có guided questions
- **AI personality và guidelines bị mất**: Responses không consistent với medical context
- **Chat quality giảm nghiêm trọng**: No medical-specific instructions

### Cách thay thế
1. **Tạo lại prompt building functions** với cùng interface
2. **Recreate prompt templates** trong prompts/ directory
3. **Implement knowledge context formatting** logic
4. **Add emergency và symptom assessment prompts**
5. **Load base system prompt** từ file hoặc hardcode

## Technical Notes

### Prompt Structure
System prompt structure:
```
[Base System Prompt]

## Relevant Medical Knowledge:
[Knowledge Context]

Use this knowledge to inform your response, but always recommend professional medical evaluation for specific medical advice.
```

### Knowledge Context Format
```
- Diabetes (disease): A chronic metabolic disorder...
- Hypertension (disease): High blood pressure...
- Metformin (medication): First-line treatment for Type 2 diabetes...
```

### Emergency Prompt
Includes:
- Warning emoji (⚠️)
- IMMEDIATE ACTION REQUIRED
- List of emergency symptoms
- Instructions to call 911/112

### File-based Prompt Loading
System prompt load từ file để:
- Dễ edit without code changes
- Version control cho prompts
- Non-technical people có thể edit
- Support multiple languages (future)

## Prompt Engineering Best Practices

### System Prompt Guidelines
- **Clear role definition**: "You are a medical AI assistant..."
- **Safety disclaimers**: "Always recommend professional medical evaluation..."
- **Scope limitations**: Define what AI can and cannot do
- **Tone and style**: Professional, empathetic, clear

### Knowledge Context Integration
- **Relevance**: Only include relevant knowledge
- **Source attribution**: Allow AI to cite sources
- **Limitations**: Remind AI knowledge might not be exhaustive

### Emergency Handling
- **Clear trigger conditions**: Specific symptoms that trigger emergency prompt
- **Action-oriented**: Clear instructions on what to do
- **Time-critical emphasis**: Emphasize urgency

## Current Limitations

### Static Prompts
Prompts hiện tại là static, không dynamic based on user context hoặc conversation history.

### No Multilingual Support
Prompts chỉ có English, không support Vietnamese hay các ngôn ngữ khác.

### No Prompt Versioning
Không track prompt versions, khó A/B test different prompts.

### No Context-Aware Prompting
Không adjust prompts based on user's medical history, previous conversations.

## Future Improvements

1. **Prompt templates**: Use Jinja2 templates cho flexible prompting
2. **Multilingual prompts**: Vietnamese, English, other languages
3. **Context-aware prompting**: Adjust based on user profile, history
4. **Prompt versioning**: Track and A/B test different prompt versions
5. **Dynamic knowledge injection**: Smart selection of most relevant knowledge
6. **Prompt optimization**: Use prompt engineering techniques (Chain-of-Thought, Few-Shot)
7. **Safety layers**: Multiple safety checks trong prompts
8. **Personalization**: Adjust tone based on user preferences
9. **Conversation memory**: Reference previous conversation trong prompts
10. **Domain-specific prompts**: Different prompts cho different medical domains

## Example Usage

```python
# Basic chat prompt
prompt = build_chat_prompt()

# Chat with medical knowledge
knowledge = [
    {"name": "Diabetes", "type": "disease", "description": "..."},
    {"name": "Insulin", "type": "medication", "description": "..."}
]
context = format_knowledge_context(knowledge)
prompt = build_chat_prompt(knowledge_context=context)

# Emergency situation
emergency_prompt = build_emergency_prompt()

# Symptom assessment
assessment_prompt = build_symptom_assessment_prompt()
```
