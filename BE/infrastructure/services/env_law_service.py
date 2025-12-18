"""Environmental Law Chatbot Service."""
import re
from typing import Tuple

from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
from domain.entities.env_law_knowledge import KnowledgeType
from infrastructure.services.local_llm_service import LocalLLMService

class EnvLawChatbotService:
    def __init__(self, kg_repo: KnowledgeGraphRepositoryImpl, llm_service: LocalLLMService):
        self.kg_repo = kg_repo
        self.llm_service = llm_service

    def detect_intent(self, question: str) -> Tuple[str, str]:
        """
        Detect user intent and extract entity.
        Returns: (intent, entity)
        """
        q = question.lower().strip()
        
        # Manual overrides for problematic triggers (e.g. Nhà nước có trách nhiệm gì)
        if ("trách nhiệm" in q or "nghĩa vụ" in q) and ("nhà nước" in q or "chính phủ" in q):
            return "nghia_vu", "Chính phủ"
        
        # 1. NGHĨA VỤ / TRÁCH NHIỆM - obligations
        nghia_vu_patterns = [
            (r"(.+?)\s*có\s*nghĩa\s*vụ", "nghia_vu"),
            (r"(.+?)\s*có\s*trách\s*nhiệm", "nghia_vu"),
            (r"(.+?)\s*phải\s*làm\s*gì", "nghia_vu"),
            (r"nghĩa\s*vụ\s*(?:của\s*)?(.+)", "nghia_vu"),
            (r"trách\s*nhiệm\s*(?:của\s*)?(.+)", "nghia_vu"),
        ]
        for pattern, intent in nghia_vu_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                for w in ["có", "gì", "của", "phải", "làm", "những", "trách", "nhiệm", "nghĩa", "vụ"]:
                    entity = re.sub(rf"\s*{w}\s*$", "", entity, flags=re.IGNORECASE).strip()
                if entity and len(entity) > 1:
                    return intent, entity
        
        # 2. QUYỀN - rights
        quyen_patterns = [
            (r"(.+?)\s*có\s*quyền", "quyen"),
            (r"quyền\s*(?:của\s*)?(.+)", "quyen"),
        ]
        for pattern, intent in quyen_patterns:
            match = re.search(pattern, q, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                for w in ["có", "gì", "của", "những"]:
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
        
        # 10. HẬU QUẢ - consequences
        if any(w in q for w in ["bị xử lý", "bi xu ly", "bị phạt", "bi phat", "hậu quả", "hau qua", "thế nào", "the nao"]):
            # Extract the action
            clean = q
            for w in ["bị xử lý", "như thế nào", "thì sao", "thế nào", "bị phạt"]:
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
        intent, entity = self.detect_intent(question)
        print(f"  [Service] Detected Intent: {intent}, Entity: '{entity}'")
        
        try:
            if intent == "nghia_vu":
                # Split composite entities (e.g., "tổ chức, cá nhân")
                sub_entities = [e.strip() for e in re.split(r',| và ', entity) if e.strip()]
                all_records = []
                
                for sub_e in sub_entities:
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
                    prefix = "• Trách nhiệm (Cơ quan): " if r.get('source_type') == 'trach_nhiem_co_quan' else "• Nghĩa vụ (Chủ thể): "
                    line = f"{prefix}{r.get('chu_the')}: {r['nghia_vu']}"
                    if r.get('chi_tiet') and r['chi_tiet'] != r.get('doi_tuong'):
                        line += f"\n  Chi tiết: {r['chi_tiet']}"
                    if r.get('dieu_kien'):
                        line += f"\n  Điều kiện: {r['dieu_kien']}"
                    if r.get('dieu_khoan'):
                        line += f" [{r['dieu_khoan']}]"
                    lines.append(line)
                return "\n\n".join(lines)

            elif intent == "quyen":
                records = await self.kg_repo.get_rights(entity)
                if not records: return await self.answer_general_question(question)
                lines = []
                for r in records:
                    line = f"• {r['chu_the']}: {r['quyen']}"
                    if r.get('dieu_khoan'): line += f" [{r['dieu_khoan']}]"
                    lines.append(line)
                return "\n\n".join(lines)
            
            elif intent == "co_quan":
                nodes = await self.kg_repo.get_agencies()
                if not nodes: return await self.answer_general_question(question)
                return "\n".join([f"• {n.name} ({n.properties.get('cap', '')})" for n in nodes])
            
            elif intent == "chu_the":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.CHU_THE)
                if not nodes: return await self.answer_general_question(question)
                return "\n".join([f"• {n.name}" for n in nodes])
            
            elif intent == "che_tai":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.CHE_TAI)
                if not nodes: return await self.answer_general_question(question)
                return "\n".join([f"• {n.name} ({n.properties.get('loai', '')})" for n in nodes])
                
            elif intent == "hanh_vi":
                 if entity:
                     # If user specifies a behavior, use GraphRAG to find details
                     return await self.answer_general_question(question)
                 
                 nodes = await self.kg_repo.get_all_by_type(KnowledgeType.HANH_VI)
                 if not nodes: return await self.answer_general_question(question)
                 # Simpler listing for generic call
                 return "\n".join([f"• {n.name} ({n.properties.get('trang_thai', '')})" for n in nodes])
            
            elif intent == "giai_doan":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.GIAI_DOAN)
                if not nodes: return await self.answer_general_question(question)
                nodes.sort(key=lambda x: x.properties.get('thu_tu', '99'))
                return "\n".join([f"{n.properties.get('thu_tu', '?')}. {n.name}" for n in nodes])
                
            elif intent == "thu_tuc":
                nodes = await self.kg_repo.get_all_by_type(KnowledgeType.THU_TUC)
                if not nodes: return await self.answer_general_question(question)
                return "\n".join([f"• {n.name} (CQ: {n.properties.get('co_quan', 'N/A')})" for n in nodes])

            elif intent == "hau_qua":
                records = await self.kg_repo.get_consequences(entity)
                if not records: return await self.answer_general_question(question)
                lines = []
                for r in records:
                    line = f"• Hành vi: {r['hanh_vi']}\n  → Chế tài: {r['che_tai']}"
                    if r.get('hau_qua'): line += f"\n  → Hậu quả: {r['hau_qua']}"
                    lines.append(line)
                return "\n\n".join(lines)
                
            elif intent == "dinh_nghia":
                # Use FTS first as requested!
                fts_results = await self.kg_repo.search_full_text(entity, limit=3)
                
                # Also standard search fallback
                std_results = await self.kg_repo.search_by_name(entity)
                
                # Merge logic: exact match > score > loose match
                # Check for exact matches in standard results
                exact_matches = [n for n in std_results if n.name.lower() == entity.lower()]
                
                final_results = []
                seen_ids = set()
                
                # Priority 1: Exact matches
                if exact_matches:
                    best_match = exact_matches[0]
                    context = await self.kg_repo.get_node_full_context(best_match.id)
                    
                    if context:
                        entity_obj = context['entity']
                        lines = []
                        line = f"• {entity_obj.name}"
                        if entity_obj.knowledge_type: line += f" ({entity_obj.knowledge_type.value})"
                        if entity_obj.description: line += f": {entity_obj.description}"
                        if entity_obj.source: line += f"\n  [Căn cứ: {entity_obj.source}]"
                        lines.append(line)
                        
                        # Prepare context for LLM
                        # SORTING to ensure deterministic output
                        outgoing_list = sorted(context.get('outgoing', []), key=lambda x: x['target'])
                        incoming_list = sorted(context.get('incoming', []), key=lambda x: x['source'])
                        
                        raw_relations = []
                        for out in outgoing_list:
                            desc = out.get('target_desc', '')
                            detail = f"Mối quan hệ: {best_match.name} --({out['type']})--> {out['target']}"
                            if desc:
                                # Truncate desc to avoid token limit overflow if necessary
                                detail += f" (Nội dung của {out['target']}: {desc[:200]}...)"
                            if out.get('props', {}).get('dieu_khoan'): detail += f" (Căn cứ: {out['props']['dieu_khoan']})"
                            raw_relations.append(detail)
                            
                        for inc in incoming_list:
                            desc = inc.get('source_desc', '')
                            detail = f"Mối quan hệ: {inc['source']} --({inc['type']})--> {best_match.name}"
                            if desc:
                                detail += f" (Nội dung của {inc['source']}: {desc[:200]}...)"
                            if inc.get('props', {}).get('dieu_khoan'): detail += f" (Căn cứ: {inc['props']['dieu_khoan']})"
                            raw_relations.append(detail)
                        
                        if raw_relations:
                            # Call LLM to format
                            llm_prompt = f"""
                            Bạn là trợ lý pháp luật AI.
                            Nhiệm vụ: Dựa vào dữ liệu Graph dưới đây, hãy viết lại danh sách "Thông tin liên quan" cho "{best_match.name}".
                            
                            Dữ liệu Graph:
                            {chr(10).join(raw_relations[:15])}
                            
                            Yêu cầu bắt buộc:
                            1. Chỉ xuất ra danh sách gạch đầu dòng (-). KHÔNG viết mở bài/kết bài. KHÔNG lặp lại dữ liệu thô.
                            2. Mỗi dòng là một câu văn tự nhiên theo cấu trúc: 
                               "[Node Chính] [Mối quan hệ diễn giải thành lời] [Node Liên Quan] (nội dung tóm tắt của nó...)"
                            3. Ví dụ: 
                               - Môi trường bao gồm Thành phần môi trường (là các yếu tố vật chất tự nhiên và nhân tạo...).
                               - Môi trường bị ảnh hưởng tiêu cực bởi Ô nhiễm môi trường (là sự biến đổi tính chất vật lý...).
                            4. Giữ nguyên ý nghĩa của mối quan hệ (A là con của B, A tác động B...).
                            5. Tuyệt đối KHÔNG bịa đặt. Nếu không có mô tả thì chỉ nêu mối quan hệ.
                            """
                            
                            try:
                                print(f"  [Service] Sending {len(raw_relations)} relations to LLM for formatting...")
                                llm_response = await self.llm_service.generate_response(llm_prompt, temperature=0.0)
                                lines.append("\n" + llm_response)
                            except Exception as e:
                                lines.append(f"\n[Lỗi LLM: {e}] - Hiển thị dữ liệu thô:")
                                lines.extend(raw_relations[:10])
                            
                        return "\n\n".join(lines)

                # Priority 2: If no exact match found, use GraphRAG
                if not final_results:
                     # This converts "approximate topic search" into a full GraphRAG answer
                     # which satisfies the need to see relationships for fuzzy queries.
                     return await self.answer_general_question(question)

                # This part is unreachable if we return above, but keeping structure clean if mixed logic needed later.
                # Since we return above, we don't need the listing logic anymore for this case.
                return await self.answer_general_question(question)

            elif intent == "tham_quyen":
                # Simplified for this pass
                return "Chức năng tra cứu thẩm quyền chi tiết đang được cập nhật trong kiến trúc mới."

            else:
                 # Fallback to General GraphRAG
                 return await self.answer_general_question(question)

        except Exception as e:
            return f"Lỗi hệ thống: {str(e)}"

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
        
        # Add relations - SORTED for determinism
        outgoing_list = sorted(context.get('outgoing', []), key=lambda x: x['target'])
        incoming_list = sorted(context.get('incoming', []), key=lambda x: x['source'])

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
            
        # 5. Ask LLM
        llm_prompt = f"""
        Bạn là trợ lý pháp luật. Hãy trả lời câu hỏi của người dùng DỰA TRÊN dữ liệu Graph được cung cấp dưới đây.
        
        Câu hỏi: "{question}"
        
        Dữ liệu Graph liên quan:
        {chr(10).join(raw_relations[:20])}
        
        Yêu cầu:
        1. Trả lời trực tiếp vào câu hỏi.
        2. Dẫn chứng điều khoản (nếu có trong dữ liệu).
        3. Nếu dữ liệu không đủ để trả lời, hãy nói "Dựa trên dữ liệu hiện có, tôi chỉ tìm thấy thông tin về {best_node.name} như sau..." và tóm tắt thông tin đó.
        4. KHÔNG bịa đặt.
        """
        
        try:
            return await self.llm_service.generate_response(llm_prompt, temperature=0.0)
        except Exception as e:
            return f"Lỗi khi tạo câu trả lời: {str(e)}"
