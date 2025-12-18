# -*- coding: utf-8 -*-
"""
Environmental Law Chatbot - UPDATED V2.1
Based on granular Import Schema (Nodes: DieuLuat, CheTai, etc.)
"""
import asyncio
import os
import sys
import re
from neo4j import AsyncGraphDatabase
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


# =============================================================================
# QUERY FUNCTIONS - UPDATED SCHEMA
# =============================================================================

async def query_nghia_vu(driver, subject: str) -> str:
    """
    Query obligations using DoiTuong and QuyenNghiaVu.
    Updated to fetch citation from linked DieuLuat node.
    """
    # Map "nhà nước" to "Chính phủ" or general search
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
    
    # Also check CoQuan -> CHIU_TRACH_NHIEM
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
        # Run both queries
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
            # If ten_trach_nhiem is roughly same as noi_dung, just show one
            if len(trach_nhiem) > 50 and trach_nhiem in noi_dung:
                line = f"• {noi_dung}"
            else:
                line = f"• {trach_nhiem}: {noi_dung}"
                
            if r.get('dieu_khoan'):
                line += f" [Căn cứ: {r['dieu_khoan']}]"
                
            if line not in seen:
                lines.append(line)
                seen.add(line)
            
    if not lines:
        return ""
        
    return "\n\n".join(lines)


async def query_quyen(driver, subject: str) -> str:
    """
    Query rights using DoiTuong and QuyenNghiaVu (CO_QUYEN).
    Updated to fetch citation from linked DieuLuat node.
    """
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
    
    if not records:
        return ""
    
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
    """
    Query all CoQuan nodes.
    """
    query = """
    MATCH (cq:CoQuan)
    RETURN DISTINCT cq.ten AS ten, cq.cap AS cap, cq.mo_ta AS mo_ta
    ORDER BY CASE cq.cap
        WHEN 'trung_uong' THEN 1
        WHEN 'tinh' THEN 2
        WHEN 'huyen' THEN 3
        WHEN 'xa' THEN 4
        ELSE 5 END
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
        if cap_vn != 'N/A':
            line += f" (Cấp: {cap_vn})"
        if r.get('mo_ta'):
            line += f"\n  Mô tả: {r['mo_ta']}"
        
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_chu_the(driver) -> str:
    """
    Query all DoiTuong nodes.
    """
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
    seen = set()
    for r in records:
        line = f"• {r['ten']}"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_che_tai(driver) -> str:
    """
    Query distinct CheTai nodes linked to HanhVi.
    Updated for new schema.
    """
    query = """
    MATCH (h:HanhVi)-[:CO_CHE_TAI]->(ct:CheTai)
    RETURN DISTINCT ct.noi_dung AS che_tai, h.ten as hanh_vi
    LIMIT 20
    """
    async with driver.session() as session:
        result = await session.run(query, {})
        records = await result.data()
    
    lines = []
    seen = set()
    for r in records:
        line = f"• {r['che_tai']} (Áp dụng cho: {r['hanh_vi']})"
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_hanh_vi(driver) -> str:
    """
    Query all HanhVi nodes.
    Updated to fetch linked CheTai and DieuLuat nodes.
    """
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
    seen = set()
    for r in records:
        line = f"• {r['ten']}"
        if r.get('noi_dung'):
            line += f": {r['noi_dung']}"
            
        che_tais = r.get('che_tais')
        if che_tais:
             cleaned_cts = [c for c in che_tais if c]
             if cleaned_cts:
                line += f"\n  [Chế tài: {'; '.join(cleaned_cts)}]"
                
        if r.get('dieu_khoan'):
            line += f" [Căn cứ: {r['dieu_khoan']}]"
        
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_hau_qua(driver, action: str) -> str:
    """
    Query consequences (CheTai) for specific HanhVi.
    Updated for new schema.
    """
    # Clean the input
    clean = action.lower()
    for w in ["trái phép", "vi phạm", "bị phạt", "bị xử lý", "như thế nào", "thì sao", "hậu quả"]:
        clean = clean.replace(w, "").strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    
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
        result = await session.run(query, {"term": clean})
        records = await result.data()
    
    if not records:
        return "Không tìm thấy thông tin xử phạt cho hành vi này."
    
    lines = []
    seen = set()
    for r in records:
        line = f"• Hành vi: {r['hanh_vi']}"
        if r.get('noi_dung_hanh_vi'):
            line += f"\n  Chi tiết: {r['noi_dung_hanh_vi']}"
            
        che_tais = r.get('che_tais')
        if che_tais:
             cleaned_cts = [c for c in che_tais if c]
             if cleaned_cts:
                line += f"\n  → Chế tài: {'; '.join(cleaned_cts)}"
                
        if r.get('dieu_khoan'):
            line += f" [Căn cứ: {r['dieu_khoan']}]"
        
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


async def query_khai_niem(driver, term: str) -> str:
    """
    Query assignments from KhaiNiem.
    Updated to fetch linked DieuLuat.
    """
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
    
    if not records:
        return ""
    
    lines = []
    seen = set()
    for r in records:
        line = f"• {r['ten']}: {r.get('noi_dung', '')}"
        if r.get('dieu_khoan'):
            line += f"\n  [Căn cứ: {r['dieu_khoan']}]"
        
        if line not in seen:
            lines.append(line)
            seen.add(line)
    
    return "\n\n".join(lines)


# =============================================================================
# INTENT DETECTION
# =============================================================================

def detect_intent(question: str) -> tuple:
    """
    Detect user intent and extract entity.
    Returns: (intent, entity, original_question)
    """
    q = question.lower().strip()
    
    # 1. NGHĨA VỤ / TRÁCH NHIỆM
    nghia_vu_patterns = [
        (r"(.+?)\s*có\s*nghĩa\s*vụ", "nghia_vu"),
        (r"(.+?)\s*có\s*trách\s*nhiệm", "nghia_vu"),
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
                return intent, entity, question
    
    # 2. QUYỀN
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
                return intent, entity, question
    
    # 3. HẬU QUẢ / XỬ LÝ
    if any(w in q for w in ["bị xử lý", "bi xu ly", "bị phạt", "bi phat", "hậu quả", "hau qua", "thế nào", "the nao"]):
        clean = q
        for w in ["bị xử lý", "như thế nào", "thì sao", "thế nào", "bị phạt", "bị cấm"]:
            clean = clean.replace(w, "").strip()
        return "hau_qua", clean, question
    
    # 4. DANH SÁCH / LIỆT KÊ
    if "cơ quan" in q:
        return "co_quan", "", question
    if "chủ thể" in q or "đối tượng" in q:
        return "chu_the", "", question
    if "hành vi" in q:
        return "hanh_vi", "", question
    if "chế tài" in q:
        return "che_tai", "", question
        
    # DEFAULT: ĐỊNH NGHĨA
    # Common stop phrases to strip from the end or beginning
    stop_phrases = [
        "là gì", "là sao", "như thế nào", "thế nào",
        "bao gồm những gì", "bao gồm những chất gì", "bao gồm cái gì", "bao gồm gì",
        "gồm những gì", "gồm những chất gì", "gồm cái gì", "gồm gì",
        "những gì", "cái gì", "gì", "?"
    ]
    
    term = q
    for phrase in stop_phrases:
        term = term.replace(phrase, "")
    
    # Also strip "bao gồm" if it's at the start/middle but meant as a connector
    term = term.replace("bao gồm", "").replace("gồm", "").strip()
    
    return "dinh_nghia", term, question


# =============================================================================
# MAIN ANSWER FUNCTION
# =============================================================================

async def answer_question(driver, question: str) -> str:
    """Process question and return answer from Neo4j."""
    intent, entity, original = detect_intent(question)
    
    print(f"  [Debug] Intent: {intent}, Entity: '{entity}'")
    
    result = ""
    
    if intent == "nghia_vu":
        result = await query_nghia_vu(driver, entity)
    elif intent == "quyen":
        result = await query_quyen(driver, entity)
    elif intent == "co_quan":
        result = await query_co_quan(driver)
    elif intent == "chu_the":
        result = await query_chu_the(driver)
    elif intent == "che_tai":
        result = await query_che_tai(driver)
    elif intent == "hanh_vi":
        result = await query_hanh_vi(driver)
    elif intent == "hau_qua":
        result = await query_hau_qua(driver, entity)
    else:  # dinh_nghia
        result = await query_khai_niem(driver, entity)
    
    if result:
        return result
    else:
        return "Không tìm thấy thông tin trong cơ sở tri thức. Vui lòng thử câu hỏi khác."


# =============================================================================
# MAIN PROGRAM
# =============================================================================

async def main():
    print("=" * 60)
    print("CHATBOT LUẬT BVMT 2020 - REBUILT V2 (CLI Update)")
    print("=" * 60)
    
    try:
        driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        await driver.verify_connectivity()
        print("[OK] Đã kết nối Neo4j")
        
    except Exception as e:
        print(f"[LỖI] Neo4j: {e}")
        return
    
    print("\nCâu hỏi mẫu:")
    print("  • Môi trường là gì")
    print("  • Tổ chức có nghĩa vụ gì")
    print("  • Hộ gia đình có quyền gì")
    print("  • Xả thải bị xử lý thế nào")
    print("  • Danh sách đối tượng")
    print("\nNhập 'exit' để thoát")
    print("=" * 60)
    
    try:
        while True:
            q = input("\nCâu hỏi: ").strip()
            if q.lower() in ['exit', 'quit', 'q']:
                break
            if not q:
                continue
            
            print("\nĐang xử lý...")
            answer = await answer_question(driver, q)
            print(f"\nTrả lời:\n{answer}")
    finally:
        await driver.close()
    
    print("\nTạm biệt!")


if __name__ == "__main__":
    asyncio.run(main())
