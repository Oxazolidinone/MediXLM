# -*- coding: utf-8 -*-
"""
GraphRAGReasoner - Rule-Based RAG on Knowledge Graph.
Uses intent-driven rules with LLM formatting (no knowledge generation).
"""
import time
import re
from typing import Dict, Any, List, Tuple, Optional
from enum import Enum
from .base_reasoner import BaseReasoner, ReasonerResult, ReasonerType


class Intent(Enum):
    """Supported query intents."""
    DEFINITION = "definition"       # "X là gì?"
    OBLIGATION = "obligation"       # "Nghĩa vụ của X?"
    PROCEDURE = "procedure"         # "Thủ tục cho X?"
    CONSEQUENCE = "consequence"     # "Hậu quả của X?"
    AUTHORITY = "authority"         # "Ai có thẩm quyền?"
    GENERAL = "general"             # General questions


class IntentParser:
    """Parse user questions using LLM to determine intent and extract entities."""
    
    # Keep this for reference in prompt
    INTENT_DESCRIPTIONS = {
        Intent.DEFINITION: "Hỏi định nghĩa, khái niệm (X là gì?, nghĩa là gì?)",
        Intent.OBLIGATION: "Hỏi nghĩa vụ, trách nhiệm (X phải làm gì?, nghĩa vụ của X?)",
        Intent.PROCEDURE: "Hỏi thủ tục, quy trình (thủ tục cho X?, làm thế nào?)",
        Intent.CONSEQUENCE: "Hỏi hậu quả, xử phạt, chế tài, hành vi vi phạm (X bị xử lý thế nào?, hành vi vi phạm?)",
        Intent.AUTHORITY: "Hỏi thẩm quyền, cơ quan (ai có thẩm quyền?, cơ quan nào?)",
        Intent.GENERAL: "Câu hỏi chung khác",
    }
    
    def __init__(self, llm_service=None):
        self.llm_service = llm_service
    
    async def parse_with_llm(self, question: str) -> tuple[Intent, Dict[str, Any]]:
        """Parse a question using LLM to extract intent and entities."""
        if not self.llm_service:
            # Fallback to regex
            return self.parse_regex(question)
        
        prompt = f"""Phân tích câu hỏi sau và trích xuất:
1. INTENT: Loại câu hỏi
2. ENTITY: Đối tượng/chủ đề chính

CÂU HỎI: "{question}"

CÁC LOẠI INTENT:
- definition: Hỏi định nghĩa, khái niệm (X là gì?)
- obligation: Hỏi nghĩa vụ, trách nhiệm (X phải làm gì?)
- procedure: Hỏi thủ tục, quy trình (thủ tục cho X?)
- consequence: Hỏi hậu quả, xử phạt, chế tài, HÀNH VI VI PHẠM (bị xử lý thế nào?, hành vi vi phạm?)
- authority: Hỏi thẩm quyền, cơ quan (ai có thẩm quyền?)
- general: Câu hỏi chung khác

TRẢ LỜI THEO FORMAT (chỉ 2 dòng):
INTENT: [tên intent]
ENTITY: [đối tượng chính]"""

        try:
            response = await self.llm_service.generate_response(prompt, temperature=0.0)
            return self._parse_llm_response(response, question)
        except Exception as e:
            print(f"  [IntentParser] LLM error: {e}, fallback to regex")
            return self.parse_regex(question)
    
    def _parse_llm_response(self, response: str, original_question: str) -> tuple[Intent, Dict[str, Any]]:
        """Parse the LLM response to extract intent and entity."""
        lines = response.strip().split('\n')
        
        intent = Intent.GENERAL
        entity = ""
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith("INTENT:"):
                intent_str = line.split(":", 1)[1].strip().lower()
                # Map to Intent enum
                intent_map = {
                    "definition": Intent.DEFINITION,
                    "obligation": Intent.OBLIGATION,
                    "procedure": Intent.PROCEDURE,
                    "consequence": Intent.CONSEQUENCE,
                    "authority": Intent.AUTHORITY,
                    "general": Intent.GENERAL,
                }
                intent = intent_map.get(intent_str, Intent.GENERAL)
            elif line.upper().startswith("ENTITY:"):
                entity = line.split(":", 1)[1].strip()
        
        # Build entities dict based on intent
        entities = {}
        if intent == Intent.DEFINITION:
            entities["term"] = entity
        elif intent == Intent.OBLIGATION:
            entities["subject"] = entity
        elif intent == Intent.PROCEDURE:
            entities["project_type"] = entity
        elif intent == Intent.CONSEQUENCE:
            entities["action"] = entity
        elif intent == Intent.AUTHORITY:
            entities["permission"] = entity
        else:
            entities["query"] = entity or original_question
        
        return intent, entities
    
    def parse_regex(self, question: str) -> tuple[Intent, Dict[str, Any]]:
        """Fallback: Parse using regex patterns."""
        question_clean = re.sub(r'\s+', ' ', question.lower().strip())
        question_clean = re.sub(r'[?.!]+$', '', question_clean)
        
        # Simple keyword matching
        if "là gì" in question_clean or "định nghĩa" in question_clean:
            return Intent.DEFINITION, {"term": question_clean}
        elif "nghĩa vụ" in question_clean or "trách nhiệm" in question_clean or "phải làm" in question_clean:
            return Intent.OBLIGATION, {"subject": question_clean}
        elif "thủ tục" in question_clean or "quy trình" in question_clean:
            return Intent.PROCEDURE, {"project_type": question_clean}
        elif "hậu quả" in question_clean or "xử phạt" in question_clean or "vi phạm" in question_clean or "chế tài" in question_clean:
            return Intent.CONSEQUENCE, {"action": question_clean}
        elif "thẩm quyền" in question_clean or "cơ quan nào" in question_clean or "ai " in question_clean:
            return Intent.AUTHORITY, {"permission": question_clean}
        
        return Intent.GENERAL, {"query": question_clean}


class GraphRAGReasoner(BaseReasoner):
    """
    GraphRAG Reasoner - Rule-Based RAG.
    
    Strategy:
    1. Parse intent and entities from question
    2. Execute intent-specific rule (Cypher query)
    3. Format results with LLM (no knowledge generation)
    
    Best for: All intents, default reasoner
    """
    
    SYSTEM_PROMPT = """Bạn là trợ lý tra cứu Luật Bảo vệ Môi trường Việt Nam 2020.

QUY TẮC BẮT BUỘC:
1. CHỈ sử dụng thông tin trong [DỮ LIỆU] - KHÔNG thêm gì mới.
2. TUYỆT ĐỐI KHÔNG bịa đặt, KHÔNG suy diễn.
3. Nếu không có dữ liệu, trả lời: "Không tìm thấy thông tin."
4. LUÔN trích dẫn điều khoản nếu có.
5. Viết tiếng Việt rõ ràng, mạch lạc."""
    
    def __init__(self, kg_repo, llm_service):
        self.kg_repo = kg_repo
        self.llm_service = llm_service
        self.parser = IntentParser(llm_service)  # Pass LLM for intent extraction
    
    @property
    def name(self) -> str:
        return "GraphRAG"
    
    @property
    def reasoner_type(self) -> ReasonerType:
        return ReasonerType.GRAPHRAG
    
    @property
    def supported_intents(self) -> List[str]:
        return ["dinh_nghia", "nghia_vu", "quyen", "hau_qua", "che_tai", "co_quan", "hanh_vi", "yes_no", "who"]
    
    async def reason(
        self, 
        question: str, 
        intent: str, 
        entity: str,
        context: Dict[str, Any]
    ) -> ReasonerResult:
        start_time = time.time()
        
        if not self.kg_repo or not self.llm_service:
            return self._create_result(
                success=False,
                explanation="KG repo or LLM service not configured",
                execution_time_ms=self._measure_time(start_time)
            )
        
        try:
            # 1. Parse intent using REGEX (no LLM - faster, no timeout)
            parsed_intent, entities = self.parser.parse_regex(question)
            print(f"  [GraphRAG] Parsed Intent: {parsed_intent.value}, Entities: {entities}")
            
            # 2. Execute rule based on intent
            kg_data = await self._execute_rule(parsed_intent, entities, entity)
            
            if not kg_data:
                return self._create_result(
                    success=False,
                    conclusions=[],
                    explanation=f"No data found for '{entity}'",
                    execution_time_ms=self._measure_time(start_time)
                )
            
            # 3. For CONSEQUENCE (hành vi vi phạm), return raw data WITHOUT LLM formatting
            # This prevents LLM from altering the KG content
            if parsed_intent == Intent.CONSEQUENCE:
                formatted = kg_data  # Raw KG data
            else:
                # Other intents: Format with LLM (no generation, only formatting)
                formatted = await self._format_with_llm(question, kg_data)
            
            return self._create_result(
                success=True,
                conclusions=[formatted],
                evidence=kg_data[:5] if isinstance(kg_data, list) else [{"raw": kg_data}],
                confidence=0.8,
                explanation=f"Rule-Based RAG via {parsed_intent.value}",
                execution_time_ms=self._measure_time(start_time),
                metadata={"intent": parsed_intent.value, "entities": entities}
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                explanation=f"GraphRAG error: {str(e)}",
                execution_time_ms=self._measure_time(start_time)
            )
    
    async def _execute_rule(self, intent: Intent, entities: Dict, fallback_entity: str) -> str:
        """Execute the appropriate rule based on intent."""
        
        if intent == Intent.DEFINITION:
            term = entities.get("term") or fallback_entity
            return await self._rule_definition(term)
        
        elif intent == Intent.OBLIGATION:
            subject = entities.get("subject") or fallback_entity
            return await self._rule_obligation(subject)
        
        elif intent == Intent.PROCEDURE:
            project_type = entities.get("project_type") or fallback_entity
            return await self._rule_procedure(project_type)
        
        elif intent == Intent.CONSEQUENCE:
            action = entities.get("action") or fallback_entity
            return await self._rule_consequence(action)
        
        elif intent == Intent.AUTHORITY:
            permission = entities.get("permission") or fallback_entity
            return await self._rule_authority(permission)
        
        else:  # GENERAL
            return await self._rule_general(fallback_entity)
    
    def _get_legal_citation(self, ctx: dict) -> str:
        """Lấy căn cứ pháp lý từ context (outgoing QUY_DINH_TAI)."""
        # Ưu tiên từ relationship QUY_DINH_TAI
        for out in ctx.get('outgoing', []):
            if out.get('type') == 'QUY_DINH_TAI' and out.get('target'):
                return f"Căn cứ vào {out['target']} của Luật BVMT 2020"
        # Fallback từ entity.source
        entity = ctx.get('entity')
        if entity and entity.source:
            return f"Căn cứ vào {entity.source} của Luật BVMT 2020"
        return ""
    
    async def _rule_definition(self, term: str) -> str:
        """Rule: Get definition of a term."""
        results = await self.kg_repo.search_by_name(term)
        if not results:
            fts = await self.kg_repo.search_full_text(term, limit=3)
            results = [n for n, s in fts]
        
        if not results:
            return ""
        
        lines = []
        for node in results[:3]:
            ctx = await self.kg_repo.get_node_full_context(node.id)
            if ctx:
                entity = ctx.get("entity")
                # Nội dung đầy đủ
                content = entity.description or 'Không có mô tả'
                line = f"**{entity.name}**: {content}"
                # Căn cứ pháp lý
                citation = self._get_legal_citation(ctx)
                if citation:
                    line += f"\n  → {citation}"
                lines.append(line)
        
        return "\n\n".join(lines)
    
    async def _rule_obligation(self, subject: str) -> str:
        """Rule: Get obligations of a subject."""
        records = await self.kg_repo.get_obligations(subject)
        
        if not records:
            return ""
        
        lines = []
        for r in records[:15]:
            chu_the = r.get('chu_the', subject)
            nghia_vu = r.get('nghia_vu', '')
            dieu_khoan = r.get('dieu_khoan', '')
            
            line = f"• {chu_the}: {nghia_vu}"
            if dieu_khoan:
                line += f"\n  → Căn cứ vào {dieu_khoan} của Luật BVMT 2020"
            lines.append(line)
        
        return "\n\n".join(lines)
    
    async def _rule_procedure(self, project_type: str) -> str:
        """Rule: Get procedure steps."""
        fts = await self.kg_repo.search_full_text(project_type + " thủ tục", limit=5)
        
        lines = []
        for node, score in fts:
            ctx = await self.kg_repo.get_node_full_context(node.id)
            if ctx:
                entity = ctx.get("entity")
                content = entity.description or ''
                line = f"• {entity.name}: {content}"
                citation = self._get_legal_citation(ctx)
                if citation:
                    line += f"\n  → {citation}"
                lines.append(line)
        
        return "\n\n".join(lines) if lines else ""
    
    async def _rule_consequence(self, action: str) -> str:
        """Rule: Get consequences/violations."""
        records = await self.kg_repo.get_consequences(action)
        
        if not records:
            fts = await self.kg_repo.search_full_text(action + " xử phạt", limit=5)
            lines = []
            for node, score in fts:
                ctx = await self.kg_repo.get_node_full_context(node.id)
                if ctx:
                    entity = ctx.get("entity")
                    line = f"• {entity.name}: {entity.description or ''}"
                    citation = self._get_legal_citation(ctx)
                    if citation:
                        line += f"\n  → {citation}"
                    lines.append(line)
            return "\n\n".join(lines)
        
        lines = []
        for r in records:
            hanh_vi = r.get('hanh_vi', '')
            noi_dung = r.get('noi_dung_hanh_vi', '')
            dieu_khoan = r.get('dieu_khoan', '')
            che_tai = r.get('che_tai', '')
            
            if hanh_vi and noi_dung:
                line = f"• {hanh_vi}: {noi_dung}"
            elif hanh_vi:
                line = f"• {hanh_vi}"
            else:
                continue
            
            if che_tai:
                line += f"\n  [Chế tài: {che_tai}]"
            
            if dieu_khoan:
                line += f"\n  → Căn cứ vào {dieu_khoan} của Luật BVMT 2020"
            
            lines.append(line)
        
        return "\n\n".join(lines)
    
    async def _rule_authority(self, permission: str) -> str:
        """Rule: Get authority information."""
        # Search for related authority nodes
        fts = await self.kg_repo.search_full_text(permission + " thẩm quyền", limit=5)
        
        lines = []
        for node, score in fts:
            ctx = await self.kg_repo.get_node_full_context(node.id)
            if ctx:
                entity = ctx.get("entity")
                lines.append(f"• {entity.name}")
                # Check incoming for who has authority
                for inc in ctx.get("incoming", []):
                    if inc.get("type") in ["CHIU_TRACH_NHIEM", "CO_THAM_QUYEN"]:
                        lines.append(f"  → {inc['source']} có thẩm quyền")
        
        return "\n".join(lines) if lines else ""
    
    async def _rule_general(self, entity: str) -> str:
        """Rule: General search fallback."""
        fts = await self.kg_repo.search_full_text(entity, limit=5)
        
        lines = []
        for node, score in fts:
            ctx = await self.kg_repo.get_node_full_context(node.id)
            if ctx:
                entity_obj = ctx.get("entity")
                lines.append(f"**{entity_obj.name}**: {entity_obj.description or ''}")
                if entity_obj.source:
                    lines.append(f"(Căn cứ: {entity_obj.source})")
        
        return "\n".join(lines) if lines else ""
    
    async def _format_with_llm(self, question: str, kg_data: str) -> str:
        """Format KG data into natural response using LLM (no generation)."""
        if not kg_data:
            return "Không tìm thấy thông tin trong cơ sở tri thức."
        
        prompt = f"""BẠN LÀ TRỢ LÝ VIẾT VĂN PHÁP LUẬT TIẾNG VIỆT.

[CÂU HỎI]
{question}

[DỮ LIỆU TỪ KNOWLEDGE GRAPH]
{kg_data}
[/DỮ LIỆU]

QUY TẮC BẮT BUỘC:
1. PHẢI viết 100% TIẾNG VIỆT - KHÔNG dùng tiếng Anh
2. Mỗi thông tin một dòng, bắt đầu bằng "•"
3. Cuối mỗi dòng PHẢI có căn cứ pháp lý (nếu có trong dữ liệu)
4. KHÔNG thêm thông tin mới, KHÔNG bịa đặt
5. Giữ nguyên TẤT CẢ nội dung, viết lại cho mạch lạc - KHÔNG cắt ngắn
6. KHÔNG tóm tắt, KHÔNG lược bỏ

VIẾT NGAY (TIẾNG VIỆT):"""

        try:
            response = await self.llm_service.generate_response(prompt, temperature=0.0)
            return response.strip()
        except Exception as e:
            # Fallback to raw data
            return f"**Kết quả tra cứu:**\n\n{kg_data}"
