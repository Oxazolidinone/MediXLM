"""Main KG Reasoner - Orchestrates intent parsing, rule execution, and response formatting."""
from typing import Dict, Any, Optional, AsyncGenerator
from neo4j import AsyncDriver

from .intent_parser import IntentParser, Intent
from .rules import (
    BaseRule,
    DefinitionRule,
    ObligationRule,
    ProcedureRule,
    ConsequenceRule,
    AuthorityRule,
)
from infrastructure.services.ollama_service import OllamaService


class KGReasoner:
    """Main reasoner that orchestrates KG queries and LLM formatting."""
    
    # System prompt for Ollama - strictly prevents hallucination
    SYSTEM_PROMPT = """Bạn là trợ lý tra cứu Luật Bảo vệ Môi trường Việt Nam 2020.

QUY TẮC BẮT BUỘC:
1. CHỈ sử dụng thông tin được cung cấp trong phần [DỮ LIỆU] bên dưới.
2. TUYỆT ĐỐI KHÔNG suy diễn, KHÔNG bịa đặt, KHÔNG thêm thông tin ngoài dữ liệu.
3. Nếu [DỮ LIỆU] trống hoặc không liên quan, trả lời: "Không tìm thấy thông tin trong cơ sở tri thức."
4. LUÔN trích dẫn điều khoản cụ thể nếu có trong dữ liệu.
5. Trả lời bằng tiếng Việt, rõ ràng, mạch lạc.
6. Sử dụng định dạng markdown với bullet points khi liệt kê.

Hãy trả lời câu hỏi dựa HOÀN TOÀN trên dữ liệu được cung cấp."""
    
    def __init__(self, driver: AsyncDriver, ollama_service: Optional[OllamaService] = None):
        """Initialize the reasoner.
        
        Args:
            driver: Neo4j async driver
            ollama_service: Optional Ollama service for LLM formatting
        """
        self.driver = driver
        self.ollama = ollama_service or OllamaService()
        self.parser = IntentParser()
        
        # Initialize rules
        self.rules: Dict[Intent, BaseRule] = {
            Intent.DEFINITION: DefinitionRule(driver),
            Intent.OBLIGATION: ObligationRule(driver),
            Intent.PROCEDURE: ProcedureRule(driver),
            Intent.CONSEQUENCE: ConsequenceRule(driver),
            Intent.AUTHORITY: AuthorityRule(driver),
        }
    
    async def answer(self, question: str) -> str:
        """Answer a question about Environmental Law 2020.
        
        Args:
            question: User's question in Vietnamese
            
        Returns:
            Formatted answer string
        """
        # Parse intent and entities
        intent, entities = self.parser.parse(question)
        
        # Execute appropriate rule(s)
        kg_data = await self._execute_rules(intent, entities)
        
        # If no data found and intent is general, try definition search
        if not kg_data and intent == Intent.GENERAL:
            entities["term"] = entities.get("query", question)
            kg_data = await self.rules[Intent.DEFINITION].execute(entities)
            if kg_data:
                kg_data = self.rules[Intent.DEFINITION].format_results(kg_data)
        
        # Format response with Ollama
        response = await self._format_with_llm(question, kg_data)
        
        return response
    
    async def answer_stream(self, question: str) -> AsyncGenerator[str, None]:
        """Stream answer for a question.
        
        Args:
            question: User's question in Vietnamese
            
        Yields:
            Token chunks of the answer
        """
        # Parse intent and entities
        intent, entities = self.parser.parse(question)
        
        # Execute appropriate rule(s)
        kg_data = await self._execute_rules(intent, entities)
        
        # If no data found and intent is general, try definition search
        if not kg_data and intent == Intent.GENERAL:
            entities["term"] = entities.get("query", question)
            kg_data = await self.rules[Intent.DEFINITION].execute(entities)
            if kg_data:
                kg_data = self.rules[Intent.DEFINITION].format_results(kg_data)
        
        # Stream response with Ollama
        prompt = self._build_prompt(question, kg_data)
        async for chunk in self.ollama.generate_stream(
            prompt=prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3,
        ):
            yield chunk
    
    async def _execute_rules(self, intent: Intent, entities: Dict[str, Any]) -> str:
        """Execute rules based on intent and format results.
        
        Args:
            intent: Detected intent
            entities: Extracted entities
            
        Returns:
            Formatted KG data string
        """
        if intent in self.rules:
            rule = self.rules[intent]
            results = await rule.execute(entities)
            return rule.format_results(results)
        
        # For general intent, try multiple rules
        all_results = []
        
        # Try definition first
        if "query" in entities or "term" in entities:
            term = entities.get("term") or entities.get("query", "")
            results = await self.rules[Intent.DEFINITION].execute({"term": term})
            if results:
                all_results.append(self.rules[Intent.DEFINITION].format_results(results))
        
        return "\n\n".join(all_results) if all_results else ""
    
    async def _format_with_llm(self, question: str, kg_data: str) -> str:
        """Format KG data into a natural response using Ollama.
        
        Args:
            question: Original user question
            kg_data: Formatted data from KG
            
        Returns:
            LLM-formatted response
        """
        prompt = self._build_prompt(question, kg_data)
        
        try:
            response = await self.ollama.generate(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.3,
                max_tokens=1024,
            )
            return response.strip()
        except Exception as e:
            # Fallback to raw KG data if Ollama fails
            if kg_data:
                return f"**Kết quả tra cứu:**\n\n{kg_data}"
            return f"Không thể kết nối với dịch vụ LLM. Lỗi: {str(e)}"
    
    def _build_prompt(self, question: str, kg_data: str) -> str:
        """Build the prompt for LLM.
        
        Args:
            question: User's question
            kg_data: Formatted KG data
            
        Returns:
            Complete prompt string
        """
        if not kg_data:
            kg_data = "(Không có dữ liệu từ cơ sở tri thức)"
        
        return f"""[CÂU HỎI]
{question}

[DỮ LIỆU]
{kg_data}
[/DỮ LIỆU]

Hãy trả lời câu hỏi trên dựa hoàn toàn vào dữ liệu được cung cấp. Nếu dữ liệu trống hoặc không liên quan, hãy nói rõ là không tìm thấy thông tin."""
