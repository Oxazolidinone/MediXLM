# infrastructure/services/local_llm_service.py

## Mục đích
File này implements local LLM service sử dụng HuggingFace Transformers. Provides text generation với streaming support và embedding generation. Uses local models (microsoft/phi-2) để avoid API costs và ensure privacy. Currently partially implemented, some methods reference non-existent model attributes.

## Chức năng chính

### LocalLLMService Class

#### __init__()
Initialize LLM service:
- Detect device (CUDA/CPU)
- Load tokenizer từ HuggingFace
- Load model (AutoModelForCausalLM) với appropriate dtype
- Set model to eval mode

#### _format_messages(messages, system_prompt) -> str
Format conversation messages thành prompt string:
- Add system prompt nếu provided
- Format messages với role prefixes (User:, Assistant:)
- Prepare cho model input

#### generate_streaming_response(messages, temperature, max_tokens, system_prompt)
Generate streaming LLM response:
- Format messages thành prompt
- Tokenize input
- Use TextIteratorStreamer cho streaming output
- Run generation trong separate thread
- Yield tokens as they're generated

#### generate_embeddings(text: str) -> List[float]
Generate embeddings cho text (currently broken - calls self.model.encode which doesn't exist for CausalLM).

#### generate_batch_embeddings(texts: List[str]) -> List[List[float]]
Generate embeddings cho batch of texts (also broken).

## Liên kết với các file khác

### Dependencies
- **torch**: PyTorch framework
- **transformers**: AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
- **threading**: Thread cho streaming
- **core.config**: settings - Model configuration

### Được sử dụng bởi
- **application/use_cases/chat_use_case.py**: LLM inference (currently disabled)
- **api/dependencies.py**: Dependency injection

## Tác động nếu file này bị xóa

### 🟡 HIGH - Local LLM Service Lost

Nếu bị xóa:
- **Local LLM không hoạt động**: Phải dùng external API (Ollama, OpenAI)
- **Chat responses bị ảnh hưởng**: Currently disabled trong use case, so minimal immediate impact
- **Privacy option lost**: Không option để run completely local

### Cách thay thế
1. Use Ollama service instead (already configured)
2. Use cloud LLM APIs (OpenAI, Anthropic)
3. Recreate với proper model loading

## Technical Notes

### Issues
- **Embedding methods broken**: CausalLM models không có .encode() method. Cần SentenceTransformer model cho embeddings.
- **Currently unused**: Chat use case không call LLM service (disabled cho debugging)

### Model Choice
- **phi-2**: Small efficient model (2.7B parameters)
- Lightweight enough cho CPU inference
- Good cho testing và development

### Streaming Implementation
Uses thread-based streaming:
- TextIteratorStreamer collects generated tokens
- Model.generate runs trong separate thread
- Main thread yields tokens as available

## Future Improvements

1. **Fix embedding methods**: Use separate embedding model hoặc remove methods
2. **Add error handling**: Handle model loading errors, OOM errors
3. **Add batching**: Batch multiple requests cho efficiency
4. **Add caching**: Cache common responses
5. **Integrate with chat use case**: Re-enable LLM calls
6. **Support multiple models**: Allow switching models dynamically
7. **Add quantization**: Use 4-bit/8-bit quantization cho memory efficiency
