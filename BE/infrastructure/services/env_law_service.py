"""Environmental Law Chatbot Service with Multi-Reasoner Support."""
import re
import json
from typing import Tuple, Dict, Any, Optional

from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
from domain.entities.env_law_knowledge import KnowledgeType
from infrastructure.services.local_llm_service import LocalLLMService
from core.reasoning import (
    RuleEngine, QueryParser, Fact,
    ForwardChainingEngine, BackwardChainingEngine, GraphTraversalEngine,
    PEIARule, DTMRule, GPMTRule,
    BoTNMTAuthorityRule, ProvinceAuthorityRule,
    IllegalDischargeRule, NoLicenseRule,
    PollutionChainRule,
    ExemptDTMRule,
    TimeDTMRule,
    # NEW: Multi-Reasoner System
    ForwardChainingReasoner,
    BackwardChainingReasoner,
    GraphTraversalReasoner,
    OntologyReasoner,
    HybridReasoner,
    GraphRAGReasoner,
    ReasonerOrchestrator,
    ReasonerComparator,
)

class EnvLawChatbotService:
    def __init__(self, kg_repo: KnowledgeGraphRepositoryImpl, llm_service: LocalLLMService):
        self.kg_repo = kg_repo
        self.llm_service = llm_service
        self._init_reasoning_engine()
        self._init_multi_reasoner()

    def _init_reasoning_engine(self):
        """Initialize the Rule-Based Reasoning Engine."""
        self.query_parser = QueryParser()
        self.rule_engine = RuleEngine()
        
        # Register Strategies
        self.rule_engine.register_strategy("forward", ForwardChainingEngine())
        self.rule_engine.register_strategy("traversal", GraphTraversalEngine(self.kg_repo.driver))
        self.rule_engine.register_strategy("backward", BackwardChainingEngine())
        
        # Register Rules from all domains
        rules = [
            PEIARule(), DTMRule(), GPMTRule(),
            BoTNMTAuthorityRule(), ProvinceAuthorityRule(),
            IllegalDischargeRule(), NoLicenseRule(),
            PollutionChainRule(),
            ExemptDTMRule(),
            TimeDTMRule()
        ]
        for r in rules:
            self.rule_engine.add_rule(r)

    def _init_multi_reasoner(self):
        """Initialize the Multi-Reasoner System (EnvLawReasoner)."""
        self.reasoners = [
            ForwardChainingReasoner(self.rule_engine, self.query_parser),
            BackwardChainingReasoner(self.rule_engine, self.query_parser),
            GraphTraversalReasoner(self.kg_repo.driver),
            OntologyReasoner(self.kg_repo.driver),
            HybridReasoner(self.kg_repo, self.llm_service, self.rule_engine),
            GraphRAGReasoner(self.kg_repo, self.llm_service),
        ]
        self.orchestrator = ReasonerOrchestrator(self.reasoners)
        self.comparator = ReasonerComparator()
        print(f"  [EnvLawReasoner] Initialized {len(self.reasoners)} reasoners: {[r.name for r in self.reasoners]}")

    async def _resolve_entity_via_fts(self, entity: str) -> str:
        """
        Use Full Text Search to find the canonical name of an entity.
        This standardizes input for the Reasoning Engine (e.g. 'xả bậy' -> 'Xả thải trái phép').
        """
        # Clean term
        clean_entity = re.sub(r'[^\w\s]', '', entity).strip()
        if not clean_entity: return entity
        
        # Search Index
        # We look for HanhVi, DoiTuong, KhaiNiem primarily for reasoning
        query = f"{clean_entity}*"
        results = await self.kg_repo.search_full_text(query, limit=1)
        
        if results:
            node, score = results[0]
            # Heuristic: If high confidence (score > 1.0) or reasonable length match
            if score > 0.8:
                print(f"  [Reasoning] FTS Resolved '{entity}' -> '{node.name}' (Score: {score:.2f})")
                return node.name
        
        return entity

    async def _try_reasoning_for_intent(self, intent: str, entity: str) -> str:
        """
        Targeted reasoning for specific intent. 
        Returns formatted answer if successful, else "".
        """
        try:
            # 0. Canonicalize Entity using FTS (Global Requirement)
            resolved_entity = await self._resolve_entity_via_fts(entity)
            
            # 1. Create Facts from Intent
            facts = self.query_parser.create_facts_from_intent(intent, resolved_entity)
            if not facts: return ""
            print(f"  [Reasoning] Intent='{intent}' -> Facts: {facts}")

            derived_facts = []
            
            # 2. Select Strategy based on Intent
            if intent == "nghia_vu":
                 # Obligations -> strict Forward Chaining
                 derived_facts = self.rule_engine.infer("forward", facts)
                 
            elif intent == "hau_qua" or intent == "che_tai":
                 # Consequences -> Forward Rule + Graph Traversal
                 derived_facts = self.rule_engine.infer("forward", facts)
                 traversal_facts = await self.rule_engine.ainfer("traversal", facts)
                 derived_facts.extend(traversal_facts)
                 
            elif intent == "thoi_han":
                 # Deadlines -> Forward Chaining
                 derived_facts = self.rule_engine.infer("forward", facts)
                 
            elif intent == "yes_no":
                 # Hypothesis Testing -> Backward Chaining
                 # (Not fully wired in this simplified version, using Rules to check)
                 derived_facts = self.rule_engine.infer("forward", facts)

            # 3. Filter & Format Results
            results = []
            seen = set()
            for f in derived_facts:
                if f in facts: continue
                if f.name in ["obligation", "authority", "consequence", "exemption", "deadline"]:
                    key = f"{f.name}:{f.value}"
                    if key not in seen:
                        results.append(f)
                        seen.add(key)
            
            if not results: return ""

            # Format strictly
            lines = [f"*** KẾT QUẢ SUY DIỄN ({intent.upper()}) ***"]
            groups = {}
            for f in results:
                if f.name not in groups: groups[f.name] = []
                groups[f.name].append(f)
                
            labels = {
                "obligation": "NGHĨA VỤ/TRÁCH NHIỆM",
                "authority": "THẨM QUYỀN",
                "consequence": "HẬU QUẢ/CHẾ TÀI", 
                "exemption": "MIỄN TRỪ",
                "deadline": "THỜI HẠN"
            }
            for type_name, fact_list in groups.items():
                header = labels.get(type_name, type_name.upper())
                lines.append(f"\n[{header}]")
                for f in fact_list:
                    line = f"- {f.value}"
                    if f.metadata and f.metadata.get("source"):
                        line += f" (Căn cứ: {f.metadata['source']})"
                    lines.append(line)
            
            lines.append("\n(Kết quả từ luật quy định)")
            return "\n".join(lines)

        except Exception as e:
            print(f"Reasoning Error: {e}")
            return ""

    def detect_intent(self, question: str) -> Tuple[str, str]:
        """
        Detect user intent and extract entity.
        Returns: (intent, entity)
        """
        q = question.lower().strip()
        
        # Manual overrides for problematic triggers (e.g. Nhà nước có trách nhiệm gì)
        if ("trách nhiệm" in q or "nghĩa vụ" in q) and ("nhà nước" in q or "chính phủ" in q):
            return "nghia_vu", "Chính phủ"

        # 0. WHO / AGENCY - "Ai", "Cơ quan nào", "Đối tượng nào" - CHECK FIRST
        who_patterns = [
            (r"^(?:ai|cơ quan nào|đối tượng nào|tổ chức nào)\s*(.+)", "who"),
            (r"(.+?)\s*(?:là ai|là cơ quan nào|thuộc về ai)", "who"),
            (r"(?:cơ quan|đơn vị|tổ chức)\s*nào\s*(.+)", "who"),
        ]
        for pattern, intent in who_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                # For "who" questions, the entity is often the action they are asking about
                # e.g., "Ai phải nộp thuế?" -> entity = "phải nộp thuế"
                entity = match.group(1).strip()
                # Clean up entity
                entity = re.sub(r"\?$", "", entity).strip()
                return intent, entity

        # 0.5. YES/NO - confirmation questions (HIGHEST PRIORITY after overrides)
        # Pattern: "...có...không?" - Must check before other patterns
        yes_no_patterns = [
            (r"(.+?)\s*có\s*(?:phải|cần|bắt buộc)\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            (r"(.+?)\s*có\s*(?:được|quyền)\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            (r"(.+?)\s*có\s*vi\s*phạm\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            (r"(.+?)\s*(?:là|thuộc)\s*(.+?)\s*(?:không|phải không)", "yes_no"),
            (r"(.+?)\s*có\s*nghĩa\s*vụ\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            (r"(.+?)\s*có\s*trách\s*nhiệm\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            (r"liệu\s*(.+?)\s*có\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            # THÊM: "có bị xử phạt không", "có bị cấm không"
            (r"(.+?)\s*có\s*bị\s*(.+?)\s*(?:không|chăng)", "yes_no"),
            # THÊM: General "có...không?" với bất kỳ verb
            (r"(.+?)\s*có\s*(.+?)\s*(?:không|chăng)\s*\??\s*$", "yes_no"),
        ]
        for pattern, intent in yes_no_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                # Extract claim: combine both groups
                g1 = match.group(1).strip() if match.group(1) else ""
                g2 = match.group(2).strip() if match.group(2) else ""
                # Clean up claim
                claim = f"{g1} {g2}".strip()
                for w in ["có", "không", "phải", "là", "thì", "được", "liệu"]:
                    claim = re.sub(rf"^\s*{w}\s*", "", claim, flags=re.IGNORECASE)
                    claim = re.sub(rf"\s*{w}\s*$", "", claim, flags=re.IGNORECASE)
                if claim and len(claim) > 2:
                    return intent, claim
        
        # 1. NGHĨA VỤ / TRÁCH NHIỆM - obligations/responsibilities
        # Cần phân biệt: trách nhiệm cơ quan nhà nước vs nghĩa vụ tổ chức/cá nhân
        
        # Keywords để nhận diện cơ quan nhà nước
        co_quan_keywords = ["bộ", "ubnd", "ủy ban", "chính phủ", "thủ tướng", "quốc hội", 
                           "sở", "cục", "vụ", "ban quản lý", "cơ quan", "tn&mt", "tnmt", 
                           "tài nguyên", "môi trường", "quốc phòng", "công an"]
        
        # Check nếu entity là cơ quan nhà nước
        def is_co_quan_nha_nuoc(entity_text: str) -> bool:
            entity_lower = entity_text.lower()
            return any(kw in entity_lower for kw in co_quan_keywords)
        
        # Patterns cho cả nghĩa vụ và trách nhiệm
        obligation_patterns = [
            # "X có nghĩa vụ gì"
            (r"(.+?)\s*có\s*(?:những\s*)?nghĩa\s*vụ\s*(?:gì|nào|như thế nào)?", "nghia_vu"),
            # "X có trách nhiệm gì" - tùy entity sẽ quyết định nghia_vu hay trach_nhiem
            (r"(.+?)\s*có\s*(?:những\s*)?trách\s*nhiệm\s*(?:gì|nào|như thế nào)?", "trach_nhiem_check"),
            # "nghĩa vụ của X"
            (r"(?:các\s*)?nghĩa\s*vụ\s*(?:của\s*)?(.+?)(?:\s*là\s*gì\s*\??)?$", "nghia_vu"),
            # "trách nhiệm của X"
            (r"(?:các\s*)?trách\s*nhiệm\s*(?:của\s*)?(.+?)(?:\s*là\s*gì\s*\??)?$", "trach_nhiem_check"),
            # "X phải làm gì"
            (r"(.+?)\s*(?:phải|cần)\s*làm\s*(?:những\s*)?gì", "nghia_vu"),
            # "những nghĩa vụ/trách nhiệm của X"
            (r"những\s*nghĩa\s*vụ\s*(?:của\s*)?(.+)", "nghia_vu"),
            (r"những\s*trách\s*nhiệm\s*(?:của\s*)?(.+)", "trach_nhiem_check"),
        ]
        
        for pattern, intent_type in obligation_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                # Cleanup "là gì?"
                entity = re.sub(r"\s*là\s*gì\s*\??$", "", entity, flags=re.IGNORECASE).strip()
                # Normalize entity
                for w in ["có", "gì", "của", "phải", "làm", "những", "trách", "nhiệm", "nghĩa", "vụ", 
                          "như thế nào", "là", "các", "nào", "?", "cần"]:
                    entity = re.sub(rf"^\s*{w}\s*", "", entity, flags=re.IGNORECASE).strip()
                    entity = re.sub(rf"\s*{w}\s*$", "", entity, flags=re.IGNORECASE).strip()
                
                if entity and len(entity) > 1:
                    # Quyết định intent dựa trên entity
                    if intent_type == "trach_nhiem_check":
                        # Nếu là cơ quan nhà nước -> trach_nhiem
                        if is_co_quan_nha_nuoc(entity):
                            return "trach_nhiem", entity
                        else:
                            return "nghia_vu", entity
                    return intent_type, entity
        
        # 2. QUYỀN - rights
        # Bao quát: "X có quyền gì", "quyền của X", "quyền X là gì"
        quyen_patterns = [
            (r"(.+?)\s*có\s*(?:những\s*)?quyền\s*(?:gì|nào|như thế nào)?", "quyen"),
            (r"(?:các\s*)?quyền\s*(?:của\s*)?(.+?)(?:\s*là\s*gì\s*\??)?$", "quyen"),
            (r"những\s*quyền\s*(?:của\s*)?(.+)", "quyen"),
        ]
        for pattern, intent in quyen_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                # Cleanup mạnh: loại bỏ "là gì?" trước
                entity = re.sub(r"\s*là\s*gì\s*\??$", "", entity, flags=re.IGNORECASE).strip()
                for w in ["có", "gì", "của", "những", "quyền", "như thế nào", "là", "các", "nào", "?"]:
                    entity = re.sub(rf"^\s*{w}\s*", "", entity, flags=re.IGNORECASE).strip()
                    entity = re.sub(rf"\s*{w}\s*$", "", entity, flags=re.IGNORECASE).strip()
                if entity and len(entity) > 1:
                    return intent, entity
        
        # 3. CƠ QUAN - agencies
        if any(w in q for w in ["cơ quan", "co quan", "bộ", "ubnd", "ủy ban"]):
            return "co_quan", ""
        
        # 4. CHỦ THỂ - subjects
        if any(w in q for w in ["chủ thể", "chu the", "đối tượng", "doi tuong"]):
            return "chu_the", ""
        
        # 5. CHẾ TÀI - penalties
        if any(w in q for w in ["chế tài", "che tai", "xử phạt", "xu phat", "hình phạt"]):
            return "che_tai", ""
        
        # 6. HÀNH VI - actions
        if any(w in q for w in ["hành vi", "hanh vi", "bị cấm", "bi cam", "nghiêm cấm"]):
            # Extract the specific behavior if present
            clean_q = q
            for w in ["hành vi", "hanh vi", "bị cấm", "bi cam", "nghiêm cấm", "là gì", "như thế nào"]:
                clean_q = clean_q.replace(w, " ")
            entity = re.sub(r"\s+", " ", clean_q).strip()
            return "hanh_vi", entity
        
        # 7. QUY TRÌNH / GIAI ĐOẠN - process
        if any(w in q for w in ["quy trình", "quy trinh", "giai đoạn", "giai doan", "các bước", "cac buoc"]):
            return "giai_doan", ""
        
        # 8. THỦ TỤC - procedures
        if any(w in q for w in ["thủ tục", "thu tuc"]):
            return "thu_tuc", ""
        
        # 9. THẨM QUYỀN - authority
        if any(w in q for w in ["thẩm quyền", "tham quyen", "ai có thẩm quyền", "ai cấp"]):
            # Extract what they're asking about
            match = re.search(r"(?:thẩm quyền|tham quyen)\s*(?:về\s*)?(.+)", q)
            entity = match.group(1).strip() if match else ""
            return "tham_quyen", entity
        
        # 10. ĐỊNH NGHĨA - CHECK BEFORE hau_qua to avoid "thế nào" conflict
        dinh_nghia_patterns = [
            r"(.+?)\s*(?:được\s*hiểu|là\s*gì|có\s*nghĩa\s*là\s*gì|nghĩa\s*là\s*gì|là\s*thế\s*nào|được\s*định\s*nghĩa)",
            r"(?:khái\s*niệm|định\s*nghĩa)\s*(?:về\s*|của\s*)?(.+)",
            r"(.+?)\s*là\s*sao",
        ]
        for pattern in dinh_nghia_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                term = match.group(1).strip()
                # Clean up
                for w in ["là", "gì", "được", "hiểu", "như", "thế", "nào", "?"]:
                    term = re.sub(rf"^\s*{w}\s*", "", term, flags=re.IGNORECASE)
                    term = re.sub(rf"\s*{w}\s*$", "", term, flags=re.IGNORECASE)
                if term and len(term) > 1:
                    return "dinh_nghia", term
        
        # 11. HẬU QUẢ - consequences (AFTER dinh_nghia check)
        if any(w in q for w in ["bị xử lý", "bi xu ly", "bị phạt", "bi phat", "hậu quả", "hau qua"]):
            # Extract the action - NO "thế nào" here to avoid conflict
            clean = q
            for w in ["bị xử lý", "như thế nào", "thì sao", "bị phạt"]:
                clean = clean.replace(w, "").strip()
            return "hau_qua", clean
        
        # DEFAULT: ĐỊNH NGHĨA - definitions
        term = q
        # Remove common definition query patterns
        patterns_to_remove = [
            r"có\s+nghĩa\s+là\s+gì", 
            r"nghĩa\s+là\s+gì", 
            r"là\s+gì", 
            r"là\s+thế\s+nào",
            r"là\s+sao",
            r"\?",
            r"ý\s+nghĩa\s+của",
            r"định\s+nghĩa"
        ]
        for pattern in patterns_to_remove:
            term = re.sub(pattern, " ", term, flags=re.IGNORECASE)
            
        term = re.sub(r"\s+", " ", term).strip()
        return "dinh_nghia", term

    async def answer_question(self, question: str) -> str:
        """Process question and return answer from Repository."""
        
        # 0. DELETED Global Pre-check
        # reasoning_result = await self._try_answer_with_reasoning(question)

        intent, entity = self.detect_intent(question)
        print(f"  [Service] Detected Intent: {intent}, Entity: '{entity}'")
        
        try:
            if intent == "yes_no":
                # Handle yes/no confirmation questions
                return await self.answer_yes_no_question(question, entity)
            
            elif intent == "who":
                # Handle who questions
                return await self.answer_who_question(question, entity)

            elif intent == "nghia_vu":
                # Split composite entities (e.g., "tổ chức, cá nhân")
                sub_entities = [e.strip() for e in re.split(r',| và ', entity) if e.strip()]
                all_records = []
                
                for sub_e in sub_entities:
                    # 1. Try Reasoning First
                    reasoner_ans = await self._try_reasoning_for_intent(intent, sub_e)
                    if reasoner_ans:
                        all_records.append({"reasoner_raw": reasoner_ans})
                        continue

                    records = await self.kg_repo.get_obligations(sub_e)
                    all_records.extend(records)
                
                if not all_records: 
                    # Fallback to GraphRAG if strict rule failed
                    return await self.answer_general_question(question)
                
                # Deduplicate based on content
                seen = set()
                unique_records = []
                for r in all_records:
                    key = f"{r.get('chu_the')}-{r.get('nghia_vu')}"
                    if key not in seen:
                        seen.add(key)
                        unique_records.append(r)

                lines = []
                for r in unique_records:
                    if "reasoner_raw" in r:
                         lines.append(r["reasoner_raw"])
                         continue
                    
                    # Build output line
                    chu_the = r.get('chu_the', '')
                    nghia_vu = r.get('nghia_vu', '')
                    dieu_khoan = r.get('dieu_khoan', '')
                    
                    line = f"• {chu_the}: {nghia_vu}"
                    
                    # Add legal citation - BẮT BUỘC hiển thị nếu có
                    if dieu_khoan:
                        line += f"\n  → Căn cứ vào {dieu_khoan} của Luật BVMT 2020"
                    
                    lines.append(line)
                return "\n\n".join(lines)

            elif intent == "trach_nhiem":
                # Trách nhiệm của cơ quan nhà nước (Bộ, UBND, Chính phủ...)
                records = await self.kg_repo.get_responsibilities(entity)
                if not records: 
                    return f"Không tìm thấy trách nhiệm của '{entity}' trong cơ sở tri thức."
                
                lines = [f"**Trách nhiệm của {entity}:**\n"]
                for r in records:
                    co_quan = r.get('co_quan', '')
                    trach_nhiem = r.get('trach_nhiem', '')
                    ten_tn = r.get('ten_trach_nhiem', '')
                    dieu_khoan = r.get('dieu_khoan', '')
                    
                    # Format content
                    if ten_tn and trach_nhiem:
                        line = f"• **{ten_tn}**: {trach_nhiem}"
                    elif trach_nhiem:
                        line = f"• {trach_nhiem}"
                    else:
                        continue
                    
                    # Add legal citation
                    if dieu_khoan:
                        line += f"\n  → Căn cứ vào {dieu_khoan} của Luật BVMT 2020"
                    
                    lines.append(line)
                
                return "\n\n".join(lines) if len(lines) > 1 else f"Không tìm thấy trách nhiệm cụ thể của '{entity}'."

            elif intent == "quyen":
                records = await self.kg_repo.get_rights(entity)
                if not records: return await self.answer_general_question(question)
                lines = []
                for r in records:
                    line = f"• {r['chu_the']}: {r['quyen']}"
                    if r.get('dieu_khoan'):
                        line += f"\n  → Căn cứ vào {r['dieu_khoan']} của Luật BVMT 2020"
                    lines.append(line)
                return "\n\n".join(lines)
            
            elif intent == "co_quan":
                nodes = await self.kg_repo.get_agencies()
                if not nodes: return await self.answer_general_question(question)
                lines = []
                for n in nodes:
                    line = f"• **{n.name}**"
                    if n.properties.get('cap'):
                        line += f" ({n.properties.get('cap')})"
                    if n.description:
                        line += f"\n  {n.description[:150]}..." if len(n.description) > 150 else f"\n  {n.description}"
                    if n.source:
                        line += f"\n  → Căn cứ: {n.source}"
                    lines.append(line)
                return "\n\n".join(lines) if lines else await self.answer_general_question(question)
            
            elif intent == "chu_the":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.DOI_TUONG)
                if not nodes: return await self.answer_general_question(question)
                lines = []
                for n in nodes:
                    line = f"• **{n.name}**"
                    if n.description:
                        line += f": {n.description[:100]}..." if len(n.description) > 100 else f": {n.description}"
                    if n.source:
                        line += f"\n  → Căn cứ: {n.source}"
                    lines.append(line)
                return "\n\n".join(lines) if lines else await self.answer_general_question(question)
            
            elif intent == "che_tai":
                # Lấy chế tài từ HanhVi có CO_CHE_TAI relationship
                records = await self.kg_repo.get_consequences("")
                if not records: return await self.answer_general_question(question)
                lines = []
                seen_che_tai = set()
                for r in records:
                    che_tai = r.get('che_tai', '')
                    if che_tai and che_tai not in seen_che_tai:
                        seen_che_tai.add(che_tai)
                        line = f"• {che_tai}"
                        if r.get('dieu_khoan'):
                            line += f"\n  → Căn cứ: {r['dieu_khoan']}"
                        lines.append(line)
                return "\n\n".join(lines) if lines else await self.answer_general_question(question)
                
            elif intent == "hanh_vi":
                # Dùng get_consequences để lấy tất cả hành vi vi phạm từ KG
                records = await self.kg_repo.get_consequences(entity or "vi phạm")
                
                if records:
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
                    
                    if lines:
                        return "\n\n".join(lines)
                
                # Fallback nếu không có data
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.HANH_VI)
                if not nodes: 
                    return "Không tìm thấy thông tin về hành vi vi phạm trong cơ sở tri thức."
                return "\n".join([f"• {n.name}" for n in nodes])
            
            elif intent == "giai_doan":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.GIAI_DOAN)
                if not nodes: return await self.answer_general_question(question)
                nodes.sort(key=lambda x: x.properties.get('thu_tu', '99'))
                lines = []
                for n in nodes:
                    line = f"{n.properties.get('thu_tu', '?')}. **{n.name}**"
                    if n.description:
                        line += f"\n   {n.description[:150]}..." if len(n.description) > 150 else f"\n   {n.description}"
                    if n.source:
                        line += f"\n   → Căn cứ: {n.source}"
                    lines.append(line)
                return "\n\n".join(lines) if lines else await self.answer_general_question(question)
                
            elif intent == "thu_tuc":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.BUOC_QUY_TRINH)
                if not nodes: return await self.answer_general_question(question)
                lines = []
                for n in nodes:
                    line = f"• **{n.name}**"
                    if n.properties.get('co_quan'):
                        line += f" (Cơ quan: {n.properties.get('co_quan')})"
                    if n.description:
                        line += f"\n  {n.description[:150]}..." if len(n.description) > 150 else f"\n  {n.description}"
                    if n.source:
                        line += f"\n  → Căn cứ: {n.source}"
                    lines.append(line)
                return "\n\n".join(lines) if lines else await self.answer_general_question(question)

            elif intent == "hau_qua":
                # 1. Reasoning Check (Forward + Traversal)
                reasoner_ans = await self._try_reasoning_for_intent(intent, entity)
                if reasoner_ans: return reasoner_ans
                
                records = await self.kg_repo.get_consequences(entity)
                if not records: return await self.answer_general_question(question)
                lines = []
                for r in records:
                    line = f"• Hành vi: {r['hanh_vi']}\n  → Chế tài: {r['che_tai']}"
                    if r.get('hau_qua'): line += f"\n  → Hậu quả: {r['hau_qua']}"
                    lines.append(line)
                return "\n\n".join(lines)
                
            elif intent == "dinh_nghia":
                # =========================================================
                # ĐỊNH NGHĨA - Format đơn giản, rõ ràng, có căn cứ pháp lý
                # =========================================================
                
                # 1. Tìm entity
                fts_results = await self.kg_repo.search_full_text(entity, limit=3)
                std_results = await self.kg_repo.search_by_name(entity)
                
                def normalize(s): return s.lower().strip()
                candidates = std_results + [n for n, score in fts_results]
                
                exact_matches = [n for n in candidates if normalize(n.name) == normalize(entity)]
                if not exact_matches and std_results:
                    std_results.sort(key=lambda x: len(x.name))
                    best = std_results[0]
                    if len(best.name) <= len(entity) * 2.5:
                        exact_matches = [best]
                
                if not exact_matches:
                    return await self.answer_general_question(question)
                
                # 2. Lấy entity chính
                exact_matches.sort(key=lambda x: len(x.name))
                main_entity = exact_matches[0]
                context = await self.kg_repo.get_node_full_context(main_entity.id)
                
                if not context:
                    return await self.answer_general_question(question)
                
                entity_obj = context['entity']
                
                # 3. Build output
                lines = []
                
                # --- PHẦN ĐỊNH NGHĨA ---
                def_content = entity_obj.description or "Chưa có mô tả chi tiết."
                lines.append(f"**{entity_obj.name}**")
                lines.append(f"{def_content}")
                
                # Căn cứ pháp lý từ node properties
                if entity_obj.source:
                    lines.append(f"\n📜 **Căn cứ pháp lý:** {entity_obj.source}")
                else:
                    # Tìm từ outgoing QUY_DINH_TAI relationship
                    for out in context.get('outgoing', []):
                        if out.get('type') == 'QUY_DINH_TAI' and out.get('target'):
                            lines.append(f"\n📜 **Căn cứ pháp lý:** {out['target']}")
                            break
                
                # --- PHẦN THÔNG TIN LIÊN QUAN ---
                # Chỉ hiển thị relationships có ý nghĩa
                related = []
                
                for out in context.get('outgoing', []):
                    target = out.get('target')
                    rel_type = out.get('type', '')
                    target_desc = out.get('target_desc', '')
                    
                    if not target or rel_type == 'QUY_DINH_TAI':
                        continue  # Đã hiển thị ở phần căn cứ
                    
                    # Format theo relationship type
                    if rel_type == 'BAO_GOM':
                        related.append(f"• {entity_obj.name} bao gồm: {target}")
                    elif rel_type == 'LA_LOAI' or rel_type == 'THUOC':
                        related.append(f"• {entity_obj.name} thuộc loại: {target}")
                    elif rel_type == 'LIEN_QUAN':
                        if target_desc:
                            related.append(f"• Liên quan: {target_desc}")
                        else:
                            related.append(f"• Liên quan đến: {target}")
                    elif rel_type == 'GAY_RA' or rel_type == 'TAC_DONG':
                        related.append(f"• Tác động: {target}")
                    else:
                        # Format mặc định có ý nghĩa
                        if target_desc:
                            related.append(f"• {target_desc}")
                        else:
                            related.append(f"• {target}")
                
                for inc in context.get('incoming', []):
                    source = inc.get('source')
                    rel_type = inc.get('type', '')
                    source_desc = inc.get('source_desc', '')
                    
                    if not source:
                        continue
                    
                    # Format theo relationship type
                    if rel_type == 'CO_NGHIA_VU':
                        if source_desc:
                            related.append(f"• Nghĩa vụ liên quan: {source_desc}")
                        else:
                            related.append(f"• {source} có nghĩa vụ liên quan")
                    elif rel_type == 'CO_QUYEN':
                        if source_desc:
                            related.append(f"• Quyền liên quan: {source_desc}")
                    elif rel_type == 'QUAN_LY_VE':
                        related.append(f"• Được quản lý bởi: {source}")
                    elif rel_type == 'LIEN_QUAN' or rel_type == 'DE_CAP':
                        if source_desc:
                            related.append(f"• {source_desc}")
                
                # Hiển thị thông tin liên quan (không trùng lặp)
                if related:
                    lines.append("\n---\n**📋 Thông tin liên quan:**")
                    seen = set()
                    for r in related[:10]:
                        if r not in seen:
                            lines.append(r)
                            seen.add(r)
                
                return "\n".join(lines)

            elif intent == "tham_quyen":
                # Simplified for this pass
                return "Chức năng tra cứu thẩm quyền chi tiết đang được cập nhật trong kiến trúc mới."

            else:
                 # Fallback to General GraphRAG
                 return await self.answer_general_question(question)

        except Exception as e:
            return f"Lỗi hệ thống: {str(e)}"

    async def answer_yes_no_question(self, question: str, claim: str) -> str:
        """
        Process yes/no using STRICT comparison approach:
        1. Extract subject & predicate.
        2. Retrieve Subject info (Definition) FIRST.
        3. Retrieve relevant relationships (Obligation/Right/Behavior).
        4. Strict comparison: If KG doesn't have the relationship -> "No basis".
        """
        print(f"  [Service] Processing yes/no (STRICT). Claim: '{claim}'")
        
        # === STEP 1: Analyze Claim ===
        # (Reusing existing analysis logic or simplifying to exact subject extraction)
        # For strict logic, we trust the analysis but fallback to FTS on the claim if needed.
        analyze_prompt = f"""
Phân tích CÂU HỎI YES/NO:
Câu hỏi: "{question}"
Claim: "{claim}"

Trích xuất JSON:
1. "subject": Đối tượng/Khái niệm CHÍNH (VD: "Doanh nghiệp", "Phế liệu").
2. "predicate": Hành động/Thuộc tính (VD: "lập báo cáo đtm", "nhập khẩu").
3. "relationship_type": "NGHIA_VU", "QUYEN", "HANH_VI", "DINH_NGHIA".

JSON:
"""
        try:
            analysis_response = await self.llm_service.generate_response(analyze_prompt, temperature=0.0)
            match = re.search(r'\{.*\}', analysis_response, re.DOTALL)
            if match:
                analysis = json.loads(match.group(0))
                subject = analysis.get("subject", claim)
                predicate = analysis.get("predicate", "")
                relationship_type = analysis.get("relationship_type", "NGHIA_VU")
            else:
                subject, predicate, relationship_type = claim, "", "NGHIA_VU"
        except:
            subject, predicate, relationship_type = claim, "", "NGHIA_VU"

        print(f"  [Service] Analysis: Subj='{subject}', Pred='{predicate}'")

        # === STEP 2: Retrieve Entity Info (First Priority) ===
        # Always try to find and describe the Subject first.
        entity_info = ""
        entity_node = None
        
        fts_sub = await self.kg_repo.search_full_text(subject, limit=1)
        if fts_sub:
            entity_node, _ = fts_sub[0]
            entity_info = f"Về **{entity_node.name}**"
            if entity_node.description:
                entity_info += f": {entity_node.description}"
            entity_info += "."
        else:
            entity_info = f"Hiện chưa có định nghĩa cụ thể về **{subject}** trong dữ liệu."

        # === STEP 3: Retrieve Evidence (Rights/Obligations/Actions) ===
        kg_evidence = []
        
        # Search specifically for the relationship implied
        if relationship_type == "NGHIA_VU":
            records = await self.kg_repo.get_obligations(subject)
            for r in records:
                # Filter moderately by predicate to avoid dumping 100 obligations
                if not predicate or predicate.lower() in r['nghia_vu'].lower():
                    kg_evidence.append(f"- Có nghĩa vụ: {r['nghia_vu']} [Căn cứ: {r.get('dieu_khoan', '')}]")
        
        elif relationship_type == "QUYEN":
            records = await self.kg_repo.get_rights(subject)
            for r in records:
                if not predicate or predicate.lower() in r['quyen'].lower():
                    kg_evidence.append(f"- Có quyền: {r['quyen']} [Căn cứ: {r.get('dieu_khoan', '')}]")

        elif relationship_type == "HANH_VI" or relationship_type == "CHE_TAI":
             # Lấy thông tin về hành vi vi phạm và chế tài
             records = await self.kg_repo.get_consequences(subject)
             for r in records:
                 hanh_vi = r.get('hanh_vi', '')
                 noi_dung = r.get('noi_dung_hanh_vi', '')
                 che_tai = r.get('che_tai', '')
                 dieu_khoan = r.get('dieu_khoan', '')
                 
                 if hanh_vi:
                     evidence_line = f"- Hành vi: {hanh_vi}"
                     if noi_dung:
                         evidence_line += f" - {noi_dung}"
                     if che_tai:
                         evidence_line += f" [Chế tài: {che_tai}]"
                     if dieu_khoan:
                         evidence_line += f" [Căn cứ: {dieu_khoan}]"
                     kg_evidence.append(evidence_line)

        # If strict specific search failed, try broader FTS on predicate + subject
        if not kg_evidence and predicate:
            broad_query = f"{subject} {predicate}"
            fts_broad = await self.kg_repo.search_full_text(broad_query, limit=3)
            for node, _ in fts_broad:
                # Get context of this node to see if it links to Subject
                context = await self.kg_repo.get_node_full_context(node.id)
                if context:
                     for inc in context.get('incoming', []):
                         kg_evidence.append(f"- {inc['source']} --[{inc['type']}]--> {node.name}")

        # === STEP 4: Strict Verification Prompt ===
        evidence_str = "\n".join(kg_evidence[:10])
        
        verify_prompt = f"""
Bạn là chuyên gia pháp lý nghiêm túc.
Hãy trả lời câu hỏi Yes/No dựa CHỈ VÀO dữ liệu cung cấp.

THÔNG TIN ĐỐI TƯỢNG:
{entity_info}

DỮ LIỆU CHỨNG MINH (Evidence):
{evidence_str}

CÂU HỎI: "{question}"
CLAIM: "{claim}"

YÊU CẦU XỬ LÝ:
1. **Bước 1**: Trình bày thông tin đối tượng trước (Copy phần "Thông tin đối tượng").
2. **Bước 2**: So khớp CLAIM với EVIDENCE.
   - Nếu Evidence có chứa nội dung khẳng định Claim (VD: Claim "phải báo cáo" và Evidence có "nghĩa vụ báo cáo") -> KẾT LUẬN: **CÓ**.
   - Nếu Evidence có nội dung ngược lại -> KẾT LUẬN: **KHÔNG**.
   - Nếu Evidence TRỐNG hoặc KHÔNG LIÊN QUAN đến hành động trong Claim -> KẾT LUẬN: **KHÔNG CÓ CƠ SỞ**.

3. **Bước 3**: Trả lời cuối cùng.
   - Nếu CÓ/KHÔNG: "Câu trả lời là: [Có/Không]. Vì theo [Điều khoản/Nội dung evidence]..."
   - Nếu KHÔNG CÓ CƠ SỞ: "Câu trả lời là: Hiện tại không có cơ sở pháp lý/thông tin nào trong hệ thống đề cập đến việc [Subject] [Predicate]."

TUYỆT ĐỐI KHÔNG SỬ DỤNG KIẾN THỨC NGOÀI. KHÔNG BỊA ĐẶT.
"""
        
        try:
            response = await self.llm_service.generate_response(verify_prompt, temperature=0.0)
            return response.strip()
        except Exception as e:
            return f"{entity_info}\n\nLỗi xử lý: {e}"

    async def answer_who_question(self, question: str, entity: str) -> str:
        """
        Process who questions:
        1. Extract the action/obligation/attribute from the question using LLM if needed
        2. Query KG for subjects (DoiTuong, CoQuan) that match
        """
        print(f"  [Service] Processing who question: '{question}'")
        
        # 1. Use LLM to extract the core 'action' to search for
        extract_prompt = f"""
Trích xuất HÀNH ĐỘNG hoặc TRÁCH NHIỆM chính từ câu hỏi "Who" (Ai/Cơ quan nào...):
Câu hỏi: "{question}"

Yêu cầu:
- Loại bỏ các từ hỏi (Ai, cơ quan nào, đối tượng nào, là gì, ...)
- Giữ lại nội dung cốt lõi (VD: "phải nộp thuế Bvmt", "chịu trách nhiệm quản lý nhà nước", "được phép nhập khẩu phế liệu")
- Trả về cụm từ ngắn gọn nhất để tìm kiếm.

Trả về (chỉ cụm từ):
"""
        try:
            search_query = await self.llm_service.generate_response(extract_prompt, temperature=0.0)
            search_query = search_query.strip().replace('"', '').replace("'", "")
            print(f"  [Service] Extracted search query: '{search_query}'")
        except:
            search_query = entity if entity else question

        if not search_query:
            return await self.answer_general_question(question)

        # 2. Search for subjects having this obligation/right
        # We can use GraphRAG approach but focused on finding the SUBJECT
        
        # We will use FTS to find nodes related to the action, then look for incoming relationships from Subjects
        # But standard GraphRAG might be better here because "Who" often implies a complex query
        
        # Let's try a specific Cypher query if it's about Obligation/Right
        
        results = []
        
        # Try finding relationships pointing to a node matching the search query
        # This is hard without exact matching. 
        # Strategy: Use GraphRAG to get context, then ask LLM to identify the "Who".
        
        fts_results = await self.kg_repo.search_full_text(search_query, limit=5)
        
        candidates = []
        for node, score in fts_results:
            # Get incoming relationships (Entity -> [Action/Concept])
            # We want to find who has this Action/Concept
            context = await self.kg_repo.get_node_full_context(node.id)
            if context:
                # Lấy căn cứ pháp lý từ outgoing QUY_DINH_TAI
                dieu_khoan = ""
                for out in context.get('outgoing', []):
                    if out.get('type') == 'QUY_DINH_TAI' and out.get('target'):
                        dieu_khoan = out['target']
                        break
                if not dieu_khoan and node.source:
                    dieu_khoan = node.source
                    
                # Check incoming
                for inc in context.get('incoming', []):
                    # We are looking for Subject -> [CO_NGHIA_VU/CO_QUYEN/CHIU_TRACH_NHIEM] -> Node
                    if inc['type'] in ['CO_NGHIA_VU', 'CO_QUYEN', 'CHIU_TRACH_NHIEM', 'THUC_HIEN']:
                        desc = node.description[:50] if node.description else ""
                        line = f"{inc['source']} --[{inc['type']}]--> {node.name} ({desc}...)"
                        if dieu_khoan:
                            line += f" [Căn cứ: {dieu_khoan}]"
                        candidates.append(line)

                # Check outgoing (e.g. Agency -> [CHIU_TRACH_NHIEM] -> Responsibility)
                # If the matched node IS the Subject
                node_type = node.knowledge_type.value if node.knowledge_type else ""
                if node_type in ['DoiTuong', 'CoQuan']:
                    line = f"{node.name} (Matched term directly)"
                    if dieu_khoan:
                        line += f" [Căn cứ: {dieu_khoan}]"
                    candidates.append(line)

        if not candidates:
             # Fallback: Just ask LLM with general context
             return await self.answer_general_question(question)
              
        # Dùng LLM để VIẾT CÂU VĂN từ dữ liệu KG (KHÔNG sinh tri thức mới)
        raw_data = "\n".join(set(candidates))
        
        format_prompt = f"""BẠN LÀ TRỢ LÝ VIẾT VĂN PHÁP LUẬT TIẾNG VIỆT.

CÂU HỎI: {question}

DỮ LIỆU TỪ KNOWLEDGE GRAPH:
{raw_data}

QUY TẮC BẮT BUỘC:
1. PHẢI viết 100% TIẾNG VIỆT
2. Mỗi chủ thể một dòng, bắt đầu bằng "•"
3. Cuối mỗi dòng PHẢI có căn cứ pháp lý nếu có trong dữ liệu (Căn cứ: Điều X, Khoản Y)
4. KHÔNG thêm thông tin mới, KHÔNG bịa đặt

VIẾT NGAY (TIẾNG VIỆT):"""

        try:
            formatted = await self.llm_service.generate_response(format_prompt, temperature=0.0)
            return formatted.strip()
        except Exception as e:
            # Fallback: hiển thị raw
            lines = [f"**Kết quả tra cứu: {search_query}**\n"]
            for c in set(candidates):
                lines.append(f"• {c}")
            return "\n".join(lines)


    async def answer_general_question(self, question: str) -> str:
        """
        Fallback GraphRAG: 
        1. Search for key terms in the question using FTS.
        2. Get context of the best matching node.
        3. Ask LLM to answer based on that context.
        """
        print(f"  [Service] Fallback to GraphRAG for: '{question}'")
        
        # 1. Extract potential keywords (simple approach: remove common words)
        # In a real system, use an LLM to extract keywords, but here we try FTS on the phrase
        # Remove 'là gì', 'như thế nào', 'ra sao', 'có', 'không'
        stop_words = ["là gì", "như thế nào", "ra sao", "có", "không", "của", "những", "các", "bị", "được", "tại", "trong", "về"]
        search_term = question
        for sw in stop_words:
            search_term = search_term.replace(sw, " ")
        search_term = re.sub(r'\s+', ' ', search_term).strip()
        
        if not search_term: return "Vui lòng đặt câu hỏi cụ thể hơn."

        # 2. FTS Search
        fts_results = await self.kg_repo.search_full_text(search_term, limit=1)
        if not fts_results:
            return "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở tri thức."
            
        best_node, score = fts_results[0]
        print(f"  [Service] GraphRAG matched node: {best_node.name} (Score: {score})")
        
        # 3. Get Context
        context = await self.kg_repo.get_node_full_context(best_node.id)
        if not context:
            return f"Tìm thấy '{best_node.name}' nhưng không có thông tin chi tiết."
            
        # 4. Formatter for LLM
        entity_obj = context['entity']
        raw_relations = []
        
        # Add main node info
        raw_relations.append(f"Chủ đề: {entity_obj.name}")
        if entity_obj.description: raw_relations.append(f"Mô tả: {entity_obj.description}")
        
        # Add relations - SORTED for determinism (handle None values)
        outgoing_list = sorted(context.get('outgoing', []), key=lambda x: x.get('target') or "")
        incoming_list = sorted(context.get('incoming', []), key=lambda x: x.get('source') or "")

        for out in outgoing_list:
            desc = out.get('target_desc', '')
            detail = f"{best_node.name} --({out['type']})--> {out['target']}"
            if desc: detail += f" (Nội dung: {desc[:100]}...)"
            if out.get('props', {}).get('dieu_khoan'): detail += f" [Căn cứ: {out['props']['dieu_khoan']}]"
            raw_relations.append(detail)
            
        for inc in incoming_list:
            desc = inc.get('source_desc', '')
            detail = f"{inc['source']} --({inc['type']})--> {best_node.name}"
            if desc: detail += f" (Nội dung: {desc[:100]}...)"
            if inc.get('props', {}).get('dieu_khoan'): detail += f" [Căn cứ: {inc['props']['dieu_khoan']}]"
            raw_relations.append(detail)
            
        # 5. Dùng LLM để VIẾT CÂU VĂN từ dữ liệu KG (KHÔNG sinh tri thức mới)
        raw_data = "\n".join(raw_relations[:15])
        
        format_prompt = f"""VIẾT BẰNG TIẾNG VIỆT. KHÔNG DÙNG TIẾNG ANH.

Chủ đề: {best_node.name}
Mô tả: {entity_obj.description or 'Không có'}
Căn cứ: {entity_obj.source or 'Không có'}

Các mối quan hệ:
{raw_data}

YÊU CẦU: Viết thành đoạn văn TIẾNG VIỆT.
- Chỉ dùng thông tin có sẵn
- Không thêm gì mới
- Viết thành câu văn mạch lạc

TRẢ LỜI TIẾNG VIỆT:"""

        try:
            formatted = await self.llm_service.generate_response(format_prompt, temperature=0.0)
            return formatted.strip()
        except Exception as e:
            # Fallback: hiển thị raw
            lines = []
            lines.append(f"**{best_node.name}**")
            if entity_obj.description:
                lines.append(f"\n{entity_obj.description}")
            if entity_obj.source:
                lines.append(f"\n📜 Căn cứ: {entity_obj.source}")
            if raw_relations:
                lines.append("\n---")
                for r in raw_relations[:15]:
                    lines.append(f"• {r}")
            return "\n".join(lines)

    async def answer_with_graphrag(self, question: str) -> str:
        """
        Use GraphRAG reasoner as default for answering questions.
        This provides community-based retrieval + LLM synthesis (format only).
        """
        intent, entity = self.detect_intent(question)
        print(f"  [GraphRAG] Intent: {intent}, Entity: '{entity}'")
        
        # Find GraphRAG reasoner
        graphrag = None
        for r in self.reasoners:
            if r.name == "GraphRAG":
                graphrag = r
                break
        
        if not graphrag:
            return await self.answer_general_question(question)
        
        try:
            # Run GraphRAG reasoner
            result = await graphrag.reason(question, intent, entity, {})
            
            if result.success and result.conclusions:
                raw_data = "\n".join(result.conclusions)
                
                # Kiểm tra intent từ metadata của reasoner
                parsed_intent = result.metadata.get("intent", "") if result.metadata else ""
                
                # Với CONSEQUENCE hoặc hanh_vi: trả về raw data KHÔNG qua LLM
                # vì data đã có căn cứ pháp lý, LLM hay bỏ mất khi format
                if intent == "hanh_vi" or parsed_intent == "consequence":
                    return raw_data
                
                # Các intent khác: Format với LLM
                format_prompt = f"""BẠN LÀ TRỢ LÝ VIẾT VĂN PHÁP LUẬT TIẾNG VIỆT.

CÂU HỎI: {question}

DỮ LIỆU TỪ KNOWLEDGE GRAPH:
{raw_data}

QUY TẮC BẮT BUỘC:
1. PHẢI viết 100% TIẾNG VIỆT - KHÔNG dùng tiếng Anh
2. Mỗi thông tin một dòng, bắt đầu bằng "•"
3. Cuối mỗi dòng PHẢI COPY NGUYÊN VĂN căn cứ pháp lý (Căn cứ: Điều X, Khoản Y)
4. KHÔNG thêm thông tin mới, KHÔNG bịa đặt
5. Giữ nguyên TẤT CẢ nội dung - KHÔNG cắt ngắn, KHÔNG lược bỏ

VIẾT NGAY (TIẾNG VIỆT):"""

                formatted = await self.llm_service.generate_response(format_prompt, temperature=0.0)
                return formatted.strip()
            else:
                return await self.answer_general_question(question)
                
        except Exception as e:
            print(f"  [GraphRAG] Error: {e}")
            return await self.answer_general_question(question)

    # =========================================================================
    # MULTI-REASONER METHODS
    # =========================================================================
    
    async def answer_with_comparison(self, question: str) -> Dict[str, Any]:
        """
        Process question using ALL reasoners in parallel with comparison.
        Returns both the best answer and a comparison report.
        
        Use this for debugging, research, or when you want to see
        how different reasoning strategies perform on the same question.
        """
        intent, entity = self.detect_intent(question)
        print(f"  [MultiReasoner] Intent: {intent}, Entity: '{entity}'")
        
        # Run all reasoners in parallel
        results = await self.orchestrator.reason_all(
            question=question,
            intent=intent,
            entity=entity,
            context={}
        )
        
        # Generate comparison report
        report = self.comparator.compare(results)
        
        # Select best answer
        best_result = self.comparator.select_best(results)
        
        # Get raw consensus answer
        consensus = self.comparator.get_consensus_answer(results)
        
        # Get polished answer using LLM (fluent Vietnamese)
        polished = await self.comparator.get_polished_answer(
            results, question, self.llm_service
        )
        
        return {
            "question": question,
            "intent": intent,
            "entity": entity,
            "best_answer": best_result.conclusions if best_result else [],
            "best_reasoner": best_result.reasoner_name if best_result else None,
            "confidence": best_result.confidence if best_result else 0.0,
            "consensus_answer": polished,  # Use polished version
            "raw_answer": consensus,  # Keep raw for reference
            "comparison_report": report.comparison_text,
            "all_results": {name: res.to_dict() for name, res in results.items()},
            "agreement_score": report.agreement_score,
            "conflicts": report.conflicts
        }

    async def answer_with_all_reasoners(self, question: str) -> str:
        """
        Wrapper that returns formatted text output from multi-reasoner.
        Use this as alternative to answer_question() for detailed output.
        """
        result = await self.answer_with_comparison(question)
        
        lines = []
        lines.append(f"**Câu hỏi:** {question}")
        lines.append(f"**Intent:** {result['intent']} | **Entity:** {result['entity']}")
        lines.append("")
        lines.append(result['comparison_report'])
        lines.append("")
        lines.append("=" * 50)
        lines.append("**KẾT LUẬN TỔNG HỢP (đã được viết mạch lạc):**")
        lines.append(result['consensus_answer'])
        
        return "\n".join(lines)


