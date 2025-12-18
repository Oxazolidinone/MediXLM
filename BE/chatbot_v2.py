# -*- coding: utf-8 -*-
"""
Environmental Law Chatbot - UPDATED V3.0 (MULTI-REASONER)
Supports multiple reasoning engines running in parallel.
"""
import asyncio
import os
import sys
import re
import json
import warnings
import logging
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

# Suppress Neo4j deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("neo4j").setLevel(logging.ERROR)


# Add project root to path to import infrastructure modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Local LLM Service
try:
    from infrastructure.services.local_llm_service import LocalLLMService
    from infrastructure.services.env_law_service import EnvLawChatbotService
    from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl
except ImportError:
    # Fallback if running directly from BE folder without package context
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from infrastructure.services.local_llm_service import LocalLLMService
    from infrastructure.services.env_law_service import EnvLawChatbotService
    from infrastructure.repositories.knowledge_graph_repository_impl import KnowledgeGraphRepositoryImpl

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


# =============================================================================
# QUERY FUNCTIONS
# =============================================================================

async def query_nghia_vu(driver, subject: str) -> str:
    """Query obligations using DoiTuong and QuyenNghiaVu."""
    if subject.lower() in ["nhà nước", "nha nuoc"]:
        subject = "Chính phủ"
        
    query = """
    MATCH (d:DoiTuong)-[r:CO_NGHIA_VU]->(q:QuyenNghiaVu)
    WHERE toLower(d.ten) CONTAINS toLower($subject)
    OPTIONAL MATCH (q)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT d.ten AS chu_the,
           q.noi_dung AS nghia_vu,
           q.loai AS loai_nghia_vu,
           dl.ten AS dieu_khoan
    LIMIT 15
    """
    
    query_coquan = """
    MATCH (c:CoQuan)-[r:CHIU_TRACH_NHIEM]->(t:TrachNhiem)
    WHERE toLower(c.ten) CONTAINS toLower($subject)
    OPTIONAL MATCH (t)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT c.ten AS chu_the,
           t.noi_dung AS nghia_vu,
           t.ten AS ten_trach_nhiem,
           "Trách nhiệm" AS loai_nghia_vu,
           dl.ten AS dieu_khoan
    LIMIT 15
    """
    
    lines = []
    seen = set()
    
    async with driver.session() as session:
        res1 = await session.run(query, {"subject": subject})
        rec1 = await res1.data()
        
        res2 = await session.run(query_coquan, {"subject": subject})
        rec2 = await res2.data()
    
    if rec1:
        lines.append(f"--- Nghĩa vụ của {subject} (Đối tượng) ---")
        for r in rec1:
            line = f"• {r['nghia_vu']}"
            if r.get('loai_nghia_vu'):
                line += f" ({r['loai_nghia_vu']})"
            if r.get('dieu_khoan'):
                line += f" [Căn cứ: {r['dieu_khoan']}]"
            if line not in seen:
                lines.append(line)
                seen.add(line)
            
    if rec2:
        if lines: lines.append("")
        lines.append(f"--- Trách nhiệm của {subject} (Cơ quan) ---")
        for r in rec2:
            trach_nhiem = r.get('ten_trach_nhiem', '')
            noi_dung = r.get('nghia_vu', '')
            if len(trach_nhiem) > 50 and trach_nhiem in noi_dung:
                line = f"• {noi_dung}"
            else:
                line = f"• {trach_nhiem}: {noi_dung}"
            if r.get('dieu_khoan'):
                line += f" [Căn cứ: {r['dieu_khoan']}]"
            if line not in seen:
                lines.append(line)
                seen.add(line)
            
    return "\n\n".join(lines) if lines else ""


async def query_quyen(driver, subject: str) -> str:
    """Query rights using DoiTuong and QuyenNghiaVu."""
    query = """
    MATCH (d:DoiTuong)-[r:CO_QUYEN]->(q:QuyenNghiaVu)
    WHERE toLower(d.ten) CONTAINS toLower($subject)
    OPTIONAL MATCH (q)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT d.ten AS chu_the,
           q.noi_dung AS quyen,
           q.loai AS loai_quyen,
           dl.ten AS dieu_khoan
    LIMIT 15
    """
    async with driver.session() as session:
        result = await session.run(query, {"subject": subject})
        records = await result.data()
    
    if not records: return ""
    
    lines = []
    seen = set()
    lines.append(f"--- Quyền của {subject} ---")
    for r in records:
        line = f"• {r['quyen']}"
        if r.get('loai_quyen'):
            line += f" ({r['loai_quyen']})"
        if r.get('dieu_khoan'):
            line += f" [Căn cứ: {r['dieu_khoan']}]"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_co_quan(driver) -> str:
    """Query all CoQuan nodes."""
    query = """
    MATCH (cq:CoQuan)
    RETURN DISTINCT cq.ten AS ten, cq.cap AS cap, cq.mo_ta AS mo_ta
    ORDER BY CASE cq.cap WHEN 'trung_uong' THEN 1 WHEN 'tinh' THEN 2 WHEN 'huyen' THEN 3 WHEN 'xa' THEN 4 ELSE 5 END
    LIMIT 20
    """
    async with driver.session() as session:
        result = await session.run(query, {})
        records = await result.data()
    
    lines = []
    seen = set()
    for r in records:
        cap_vn = {"trung_uong": "Trung ương", "tinh": "Tỉnh", "huyen": "Huyện", "xa": "Xã"}.get(r.get('cap', ''), r.get('cap', 'N/A'))
        line = f"• {r['ten']}"
        if cap_vn != 'N/A': line += f" (Cấp: {cap_vn})"
        if r.get('mo_ta'): line += f"\n  Mô tả: {r['mo_ta']}"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_chu_the(driver) -> str:
    """Query all DoiTuong nodes."""
    query = """
    MATCH (d:DoiTuong)
    RETURN DISTINCT d.ten AS ten
    ORDER BY d.ten
    LIMIT 50
    """
    async with driver.session() as session:
        result = await session.run(query, {})
        records = await result.data()
    
    lines = []
    for r in records:
        lines.append(f"• {r['ten']}")
    return "\n\n".join(lines)


async def query_che_tai(driver) -> str:
    """Query distinct CheTai nodes linked to HanhVi."""
    query = """
    MATCH (h:HanhVi)-[:CO_CHE_TAI]->(ct:CheTai)
    RETURN DISTINCT ct.noi_dung AS che_tai, h.ten as hanh_vi
    LIMIT 20
    """
    async with driver.session() as session:
        result = await session.run(query, {})
        records = await result.data()
    
    lines = []
    for r in records:
        lines.append(f"• {r['che_tai']} (Áp dụng cho: {r['hanh_vi']})")
    return "\n\n".join(lines)


async def query_hanh_vi(driver) -> str:
    """Query all HanhVi nodes."""
    query = """
    MATCH (h:HanhVi)
    OPTIONAL MATCH (h)-[:CO_CHE_TAI]->(ct:CheTai)
    OPTIONAL MATCH (h)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT h.ten AS ten, h.noi_dung AS noi_dung, 
           collect(distinct ct.noi_dung) AS che_tais,
           dl.ten AS dieu_khoan
    LIMIT 20
    """
    async with driver.session() as session:
        result = await session.run(query, {})
        records = await result.data()
    
    lines = []
    for r in records:
        line = f"• {r['ten']}"
        if r.get('noi_dung'): line += f": {r['noi_dung']}"
        che_tais = r.get('che_tais')
        if che_tais:
             cleaned_cts = [c for c in che_tais if c]
             if cleaned_cts: line += f"\n  [Chế tài: {'; '.join(cleaned_cts)}]"
        if r.get('dieu_khoan'): line += f" [Căn cứ: {r['dieu_khoan']}]"
        lines.append(line)
    
    return "\n\n".join(lines)


async def query_hau_qua(driver, action: str) -> str:
    """Query consequences (CheTai) for specific HanhVi."""
    query = """
    MATCH (h:HanhVi)
    WHERE toLower(h.ten) CONTAINS toLower($term)
       OR toLower(h.noi_dung) CONTAINS toLower($term)
    OPTIONAL MATCH (h)-[:CO_CHE_TAI]->(ct:CheTai)
    OPTIONAL MATCH (h)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT h.ten AS hanh_vi, 
           h.noi_dung AS noi_dung_hanh_vi, 
           collect(distinct ct.noi_dung) AS che_tais,
           dl.ten AS dieu_khoan
    LIMIT 10
    """
    
    async with driver.session() as session:
        result = await session.run(query, {"term": action})
        records = await result.data()
    
    if not records:
        return "Không tìm thấy thông tin xử phạt cho hành vi này."
    
    lines = []
    seen = set()
    for r in records:
        line = f"• Hành vi: {r['hanh_vi']}"
        if r.get('noi_dung_hanh_vi'): line += f"\n  Chi tiết: {r['noi_dung_hanh_vi']}"
        che_tais = r.get('che_tais')
        if che_tais:
             cleaned_cts = [c for c in che_tais if c]
             if cleaned_cts: line += f"\n  → Chế tài: {'; '.join(cleaned_cts)}"
        if r.get('dieu_khoan'): line += f" [Căn cứ: {r['dieu_khoan']}]"
        
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_khai_niem(driver, term: str) -> str:
    """Query assignments from KhaiNiem."""
    query = """
    MATCH (k:KhaiNiem)
    WHERE toLower(k.ten) CONTAINS toLower($term)
    OPTIONAL MATCH (k)-[:QUY_DINH_TAI]->(dl:DieuLuat)
    RETURN DISTINCT k.ten AS ten, k.noi_dung AS noi_dung, dl.ten AS dieu_khoan
    LIMIT 5
    """
    async with driver.session() as session:
        result = await session.run(query, {"term": term})
        records = await result.data()
    
    if not records: return ""
    
    lines = []
    seen = set()
    for r in records:
        line = f"• {r['ten']}: {r.get('noi_dung', '')}"
        if r.get('dieu_khoan'): line += f"\n  [Căn cứ: {r['dieu_khoan']}]"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_yes_no(driver, llm_service, question: str, claim: str) -> str:
    """
    Process yes/no question using 2-step LLM approach:
    1. LLM analyzes claim to extract structured info (subject, predicate, relationship_type)
    2. Query KG based on structured info to get evidence
    3. LLM verifies claim based on retrieved evidence
    """
    print(f"  [Debug] Processing yes/no. Claim: '{claim}'")
    
    # === STEP 1: Use LLM to analyze and decompose the claim ===
    analyze_prompt = f"""
Phân tích CÂU HỎI YES/NO sau để trích xuất thông tin tra cứu Knowledge Graph Luật Bảo vệ Môi trường.

CÂU HỎI GỐC: "{question}"
CLAIM (mệnh đề cần xác nhận): "{claim}"

Dựa vào CÂU HỎI GỐC, trích xuất JSON:
1. "subject": Chủ thể/đối tượng/khái niệm chính được hỏi. Nếu hỏi về định nghĩa khái niệm, subject là tên khái niệm đó.
2. "predicate": Thuộc tính/hành động/đặc điểm được hỏi. Nếu không rõ, để trống "".
3. "relationship_type": Loại quan hệ cần kiểm tra:
   - "DINH_NGHIA" (nếu hỏi về định nghĩa, bản chất, so sánh khái niệm. VD: "X là gì?", "X có phải là Y không?")
   - "NGHIA_VU" (nếu hỏi về nghĩa vụ/phải làm gì)
   - "QUYEN" (nếu hỏi về quyền được làm gì)
   - "HANH_VI" (nếu hỏi về hành vi vi phạm)
   - "CHE_TAI" (nếu hỏi về chế tài/xử phạt)
4. "search_terms": 2-3 từ khóa chính từ CÂU HỎI GỐC (không bịa từ khóa không có trong câu hỏi)

CHÚ Ý: Chỉ trích xuất thông tin CÓ TRONG câu hỏi. KHÔNG bịa đặt.

Trả về JSON duy nhất:
{{"subject": "...", "predicate": "...", "relationship_type": "...", "search_terms": [...]}}
"""
    
    try:
        analysis_response = await llm_service.generate_response(analyze_prompt, temperature=0.1)
        # Parse JSON from response
        match = re.search(r'\{.*\}', analysis_response, re.DOTALL)
        if match:
            analysis = json.loads(match.group(0))
            subject = analysis.get("subject", "")
            predicate = analysis.get("predicate", "")
            relationship_type = analysis.get("relationship_type", "NGHIA_VU")
            search_terms = analysis.get("search_terms", [])
            print(f"  [Debug] LLM Analysis: subject='{subject}', predicate='{predicate}', rel='{relationship_type}', terms={search_terms}")
        else:
            print(f"  [Debug] Failed to parse LLM analysis, using fallback")
            subject = claim
            predicate = ""
            relationship_type = "NGHIA_VU"
            search_terms = []
    except Exception as e:
        print(f"  [Debug] LLM analysis error: {e}")
        subject = claim
        predicate = ""
        relationship_type = "NGHIA_VU"
        search_terms = []
    
    # === STEP 2: Query KG based on structured info ===
    kg_data_parts = []
    
    # Build dynamic query based on relationship_type
    if relationship_type == "DINH_NGHIA":
        # Query for concept definition
        query = """
        MATCH (k:KhaiNiem)
        WHERE toLower(k.ten) CONTAINS toLower($subject)
        OPTIONAL MATCH (k)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN DISTINCT k.ten AS entity_name,
               'DINH_NGHIA' AS relationship,
               k.noi_dung AS content,
               dl.ten AS dieu_khoan
        LIMIT 10
        """
    elif relationship_type == "NGHIA_VU":
        query = """
        MATCH (d:DoiTuong)-[r:CO_NGHIA_VU]->(q:QuyenNghiaVu)
        WHERE toLower(d.ten) CONTAINS toLower($subject)
        OPTIONAL MATCH (q)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN DISTINCT d.ten AS entity_name, 
               'NGHIA_VU' AS relationship,
               q.noi_dung AS content, 
               dl.ten AS dieu_khoan
        LIMIT 20
        """
    elif relationship_type == "QUYEN":
        query = """
        MATCH (d:DoiTuong)-[r:CO_QUYEN]->(q:QuyenNghiaVu)
        WHERE toLower(d.ten) CONTAINS toLower($subject)
        OPTIONAL MATCH (q)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN DISTINCT d.ten AS entity_name,
               'QUYEN' AS relationship,
               q.noi_dung AS content,
               dl.ten AS dieu_khoan
        LIMIT 20
        """
    elif relationship_type == "HANH_VI":
        query = """
        MATCH (h:HanhVi)
        WHERE toLower(h.ten) CONTAINS toLower($subject) OR toLower(h.noi_dung) CONTAINS toLower($subject)
        OPTIONAL MATCH (h)-[:CO_CHE_TAI]->(ct:CheTai)
        OPTIONAL MATCH (h)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN DISTINCT h.ten AS entity_name,
               'HANH_VI' AS relationship,
               h.noi_dung AS content,
               collect(distinct ct.noi_dung)[0] AS che_tai,
               dl.ten AS dieu_khoan
        LIMIT 10
        """
    else:  # CHE_TAI or default
        query = """
        MATCH (h:HanhVi)-[:CO_CHE_TAI]->(ct:CheTai)
        WHERE toLower(h.ten) CONTAINS toLower($subject) OR toLower(h.noi_dung) CONTAINS toLower($subject)
        OPTIONAL MATCH (h)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN DISTINCT h.ten AS entity_name,
               'CHE_TAI' AS relationship,
               ct.noi_dung AS content,
               dl.ten AS dieu_khoan
        LIMIT 10
        """
    
    async with driver.session() as session:
        res = await session.run(query, {"subject": subject})
        records = await res.data()
    
    # Filter results by search_terms (predicate matching)
    for r in records:
        content = (r.get('content') or '').lower()
        # Check if content matches any search terms
        matches_predicate = True
        if search_terms:
            matches_predicate = any(term.lower() in content for term in search_terms)
        
        if matches_predicate:
            rel_type = r.get('relationship', '')
            line = f"{r['entity_name']} --[{rel_type}]--> {r.get('content', '')}"
            if r.get('che_tai'): line += f" (Chế tài: {r['che_tai']})"
            if r.get('dieu_khoan'): line += f" [Căn cứ: {r['dieu_khoan']}]"
            kg_data_parts.append(line)
    
    # If no matching results, try broader search
    if not kg_data_parts and records:
        for r in records[:5]:
            rel_type = r.get('relationship', '')
            line = f"{r['entity_name']} --[{rel_type}]--> {r.get('content', '')}"
            if r.get('dieu_khoan'): line += f" [Căn cứ: {r['dieu_khoan']}]"
            kg_data_parts.append(line)
    
    # Also search for relevant concepts using predicate
    if predicate:
        concept_query = """
        MATCH (k:KhaiNiem)
        WHERE toLower(k.ten) CONTAINS toLower($term)
        OPTIONAL MATCH (k)-[:QUY_DINH_TAI]->(dl:DieuLuat)
        RETURN k.ten AS name, k.noi_dung AS description, dl.ten AS dieu_khoan
        LIMIT 3
        """
        async with driver.session() as session:
            res = await session.run(concept_query, {"term": predicate})
            concept_records = await res.data()
        
        for r in concept_records:
            if r.get('description'):
                line = f"Khái niệm '{r['name']}': {r['description'][:200]}"
                if r.get('dieu_khoan'): line += f" [Căn cứ: {r['dieu_khoan']}]"
                kg_data_parts.append(line)
    
    if not kg_data_parts:
        return f"Không tìm thấy thông tin về '{subject}' với '{predicate}' trong cơ sở tri thức."
    
    print(f"  [Debug] Found {len(kg_data_parts)} relevant KG entries")
    
    # === STEP 3: Use LLM to verify claim based on evidence ===
    kg_data = "\n".join(kg_data_parts[:10])
    
    verify_prompt = f"""
Bạn cần XÁC NHẬN hay PHỦ NHẬN một claim dựa vào dữ liệu Knowledge Graph.

CÂU HỎI: "{question}"
CLAIM CẦN KIỂM TRA: "{claim}"

DỮ LIỆU KNOWLEDGE GRAPH:
{kg_data}

QUY TRÌNH SUY LUẬN (BẮT BUỘC):
1. Đọc kỹ CLAIM - xác định ĐIỀU GÌ đang được khẳng định (VD: "X là vi phạm", "X phải làm Y")
2. Đọc kỹ NỘI DUNG trong dữ liệu KG
3. SO SÁNH: Nội dung KG có XÁC NHẬN hay PHỦ NHẬN claim không?
   - Nếu claim nói "X là hành vi vi phạm" nhưng KG định nghĩa X là hành vi tốt/hợp pháp → PHỦ NHẬN
   - Nếu claim nói "X phải làm Y" và KG có nghĩa vụ tương ứng → XÁC NHẬN
4. TRẢ LỜI:
   - "**Có**" nếu KG XÁC NHẬN claim + trích dẫn
   - "**Không**" nếu KG PHỦ NHẬN claim + giải thích tại sao
   - "**Không có thông tin**" nếu KG không liên quan đến claim

LƯU Ý: KHÔNG trả lời "Có" chỉ vì tìm được data. Phải SO SÁNH NỘI DUNG với claim!
"""
    
    try:
        response = await llm_service.generate_response(verify_prompt, temperature=0.1)
        return response.strip()
    except Exception as e:
        return f"**Dữ liệu KG tìm được:**\n" + "\n".join([f"• {line}" for line in kg_data_parts[:8]])


# =============================================================================
# LLM NLU ANALYSIS
# =============================================================================

async def analyze_query_with_llm(llm_service, user_query: str) -> tuple:
    """
    Use Local LLM (Qwen) to analyze the query and extract Intent + Entity.
    """
    prompt = f"""
    Bạn là một trợ lý AI phân tích ý định câu hỏi về Luật Môi trường Việt Nam.
    Hãy phân tích câu hỏi của người dùng và trích xuất 2 thông tin:
    1. INTENT (Ý định): Chọn một trong các loại sau:
       - 'yes_no': Câu hỏi xác nhận đúng/sai có dạng "...có...không?", "...phải...không?", "...được...không?". (VD: "Doanh nghiệp có phải đăng ký môi trường không?", "Xả thải có vi phạm không?", "Cá nhân có quyền khiếu nại không?")
       - 'hanh_vi': Hỏi danh sách các hành vi vi phạm. (VD: "hành vi nào vi phạm", "các hành vi bị cấm", "liệt kê hành vi"...). Lưu ý: Nếu câu hỏi là "hành vi nào...", hãy chọn 'hanh_vi'.
       - 'che_tai': Hỏi về chế tài, hình phạt CỦA MỘT HÀNH VI CỤ THỂ. (VD: "vứt rác bị phạt thế nào", "xả thải xử lý ra sao"). Nếu hỏi chung chung "hành vi nào bị phạt" -> chọn 'hanh_vi'.
       - 'nghia_vu': Hỏi về nghĩa vụ, trách nhiệm.
       - 'quyen': Hỏi về quyền lợi.
       - 'dinh_nghia': Hỏi định nghĩa, khái niệm.
       - 'co_quan': Hỏi danh sách cơ quan.
       - 'hau_qua': Hỏi hậu quả pháp lý cụ thể.
    2. ENTITY (Thực thể): 
       - Nếu intent là 'yes_no': Trích xuất CLAIM (mệnh đề cần xác nhận, VD: "doanh nghiệp phải đăng ký môi trường", "xả thải vi phạm luật")
       - Nếu intent khác: Đối tượng chính trong câu hỏi (bỏ các từ nối như "là gì", "của", "những", "bao gồm"...).

    Câu hỏi: "{user_query}"

    Trả về kết quả dưới dạng JSON duy nhất:
    {{
        "intent": "...",
        "entity": "..."
    }}
    Không giải thích gì thêm. Chỉ trả về JSON.
    """
    
    # Generate response
    response_text = await llm_service.generate_response(prompt, temperature=0.1)
    
    # Clean response to get JSON
    try:
        # Find JSON blob if wrapped in markdown
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data.get("intent", "dinh_nghia"), data.get("entity", "").strip()
        else:
            print(f"[LLM Warning] Could not parse JSON. Raw: {response_text}")
    except Exception as e:
        print(f"[LLM Error] Parse error: {e}")
        
    return "dinh_nghia", user_query # Fallback


# =============================================================================
# MAIN ANSWER FUNCTION
# =============================================================================

async def answer_question(driver, llm_service, question: str) -> str:
    """Process question using LLM NLU and Neo4j via Service Layer."""
    
    # Initialize Repository and Service
    # (In a real app, strict dependency injection would handle this outside, 
    # but for this script we init here to use the shared driver)
    repo = KnowledgeGraphRepositoryImpl(driver)
    service = EnvLawChatbotService(repo, llm_service)
    
    # Delegate logical reasoning and answering to the updated service
    # This ensures the Reasoning Engine (Rules, Chaining) is used.
    print(f"  [ChatbotV2] Delegating to EnvLawChatbotService (Reasoning Engine Enabled)...")
    return await service.answer_question(question)


# =============================================================================
# MAIN PROGRAM
# =============================================================================

async def main():
    print("=" * 60)
    print("CHATBOT LUẬT BVMT 2020 - V3.0 (MULTI-REASONER)")
    print("=" * 60)
    
    # Initialize LLM
    try:
        llm_service = LocalLLMService()
        print("[OK] Đã khởi tạo Local LLM (Qwen)")
    except Exception as e:
        print(f"[LỖI] Không thể khởi tạo LLM: {e}")
        return

    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        await driver.verify_connectivity()
        print("[OK] Đã kết nối Neo4j")
        
    except Exception as e:
        print(f"[LỖI] Neo4j: {e}")
        return
    
    # Initialize Service with Multi-Reasoner
    repo = KnowledgeGraphRepositoryImpl(driver)
    service = EnvLawChatbotService(repo, llm_service)
    
    print("\nSẵn sàng nhận câu hỏi. Các lệnh đặc biệt:")
    print("  'exit'      - Thoát chương trình")
    print("  'compare'   - Bật/tắt chế độ so sánh reasoners")
    print("=" * 60)
    
    compare_mode = False  # Toggle for showing all reasoner outputs
    
    try:
        while True:
            mode_indicator = "[COMPARE] " if compare_mode else ""
            q = input(f"\n{mode_indicator}Câu hỏi: ").strip()
            
            if q.lower() in ['exit', 'quit', 'q']:
                break
            if not q:
                continue
            
            # Toggle compare mode
            if q.lower() == 'compare':
                compare_mode = not compare_mode
                status = "BẬT" if compare_mode else "TẮT"
                print(f"\n[Chế độ so sánh reasoners: {status}]")
                continue
            
            print("\nĐang xử lý...")
            
            if compare_mode:
                # Use multi-reasoner with comparison
                result = await service.answer_with_comparison(q)
                
                # Show comparison report
                print("\n" + result["comparison_report"])
                
                # Show consensus answer
                print("\n" + "=" * 50)
                print(">>> KẾT LUẬN TỔNG HỢP:")
                print(result["consensus_answer"])
            else:
                # Normal mode - use best answer
                answer = await service.answer_question(q)
                print(f"\nTrả lời:\n{answer}")
                
    finally:
        await driver.close()
    
    print("\nTạm biệt!")


if __name__ == "__main__":
    asyncio.run(main())

