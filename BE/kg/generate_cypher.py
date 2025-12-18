import csv
import os
import re
import sys
import hashlib

# Configuration
INPUT_DIR = r"C:\Users\Luc\MediXLM\BE\kg"
OUTPUT_FILE = os.path.join(INPUT_DIR, "import_new.cypher")

# Files Map
FILES = {
    "hanh_vi": "Mô hình cơ sở tri thức-DA - Hành vi.csv",
    "khai_niem": "Mô hình cơ sở tri thức-DA - Khái niệm.csv",
    "du_an": "Mô hình cơ sở tri thức-DA - Phân loại dự án đầu tư.csv",
    "quan_he": "Mô hình cơ sở tri thức-DA - Quan hệ giữa các khái niệm.csv",
    "dtm": "Mô hình cơ sở tri thức-DA - Quy trình đánh giá ĐTM.csv",
    "quyen_nghia_vu": "Mô hình cơ sở tri thức-DA - Quyền Nghĩa vụ.csv",
    "trach_nhiem_nn": "Mô hình cơ sở tri thức-DA - Trách nhiệm Nhà nước.csv"
}

def clean_text(text):
    if not text: return ""
    # Remove surrounding quotes, extra spaces
    cleaned = text.strip()
    # Should escape quotes for Cypher string
    cleaned = cleaned.replace('"', "'").replace('\\', '\\\\')
    return cleaned

def generate_id(text):
    """Generate a deterministic ID based on text content."""
    if not text: return "unknown"
    hash_object = hashlib.md5(text.strip().lower().encode('utf-8'))
    return "id_" + hash_object.hexdigest()[:12]

def parse_csv(filename):
    path = os.path.join(INPUT_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: File not found {path}")
        return []
    
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return []
            
        # Normalize headers: lower, strip
        headers = [h.strip().lower() for h in headers]
        
        data = []
        for row in reader:
            item = {}
            for i, val in enumerate(row):
                if i < len(headers):
                    item[headers[i]] = val
            data.append(item)
        return data

def get_col(row, *aliases):
    for alias in aliases:
        target = alias.lower()
        # Direct match
        if target in row:
            return clean_text(row[target])
        # Fuzzy match keys
        for k in row.keys():
            if target in k:
                return clean_text(row[k])
    return ""

def split_list(text):
    if not text: return []
    # Normalize separators
    text = text.replace(';', ',').replace('\n', ',')
    parts = text.split(',')
    return [p.strip() for p in parts if p.strip()]

def main():
    cypher_params = [] 
    
    # Helper to add unique calls only? No, we just append sequential commands.
    # To fix "ConstraintValidationFailed", we follow the pattern:
    # MERGE (a:Label {id: x}) ON CREATE SET ...
    # MERGE (b:Label {id: y}) ON CREATE SET ...
    # MERGE (a)-[:REL]->(b)
    
    # 1. KHÁI NIỆM (Concepts)
    print("Processing Khai Niem...")
    data = parse_csv(FILES["khai_niem"])
    for row in data:
        ten = get_col(row, 'Khái niệm', 'concept')
        if not ten: continue
        
        dieu_khoan = get_col(row, 'Điều khoản')
        noi_dung = get_col(row, 'Nội dung')
        chuong = get_col(row, 'Chương')
        keyphrase = get_col(row, 'Keyphrase')
        
        # Concept Node
        cypher_params.append(f'MERGE (n:KhaiNiem {{ten: "{ten}"}}) ' \
                             f'ON CREATE SET n.noi_dung = "{noi_dung}", n.keyphrase = "{keyphrase}" ' \
                             f'ON MATCH SET n.noi_dung = "{noi_dung}";')
        
        # Link to DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (n:KhaiNiem {{ten: "{ten}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (n)-[:QUY_DINH_TAI]->(dl);')
            
            # Link DieuLuat -> Chuong
            if chuong:
                ch_id = generate_id(chuong)
                cypher_params.append(f'MERGE (ch:Chuong {{id: "{ch_id}"}}) ON CREATE SET ch.ten = "{chuong}";')
                cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (ch:Chuong {{id: "{ch_id}"}}) MERGE (dl)-[:THUOC_CHUONG]->(ch);')

    # 2. HÀNH VI (Behaviors)
    print("Processing Hanh Vi...")
    data = parse_csv(FILES["hanh_vi"])
    for row in data:
        hanh_vi = get_col(row, 'Hành vi', 'hanh vi')
        if not hanh_vi: continue
        
        doi_tuong_str = get_col(row, 'Đối tượng', 'doi tuong')
        noi_dung = get_col(row, 'Nội dung')
        dieu_khoan = get_col(row, 'Điều khoản')
        lien_ket = get_col(row, 'Liên kết khái niệm')
        che_tai = get_col(row, 'Chế tài')
        
        hv_id = generate_id(hanh_vi) # Optional: Use ID or Name. User used Name key previously.
        # But 'ten' is unique key for MERGE usually.
        
        # HanhVi Node
        cypher_params.append(f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) ' \
                             f'ON CREATE SET h.noi_dung = "{noi_dung}" ' \
                             f'ON MATCH SET h.noi_dung = "{noi_dung}";')
        
        # DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (h)-[:QUY_DINH_TAI]->(dl);')
            
        # DoiTuong -> HanhVi
        for dt in split_list(doi_tuong_str):
            cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}});')
            cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}}) MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) MERGE (d)-[:THUC_HIEN]->(h);')
            
        # HanhVi -> KhaiNiem
        for c in split_list(lien_ket):
            c_clean = re.sub(r'\(.*?\)', '', c).strip()
            if c_clean:
                cypher_params.append(f'MERGE (k:KhaiNiem {{ten: "{c_clean}"}});')
                cypher_params.append(f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) MERGE (k:KhaiNiem {{ten: "{c_clean}"}}) MERGE (h)-[:LIEN_QUAN]->(k);')
                
        # HanhVi -> CheTai
        if che_tai:
            ct_id = generate_id(che_tai)
            cypher_params.append(f'MERGE (ct:CheTai {{id: "{ct_id}"}}) ON CREATE SET ct.noi_dung = "{che_tai}";')
            cypher_params.append(f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) MERGE (ct:CheTai {{id: "{ct_id}"}}) MERGE (h)-[:CO_CHE_TAI]->(ct);')

    # 3. PHÂN LOẠI DỰ ÁN
    print("Processing Du An...")
    data = parse_csv(FILES["du_an"])
    for row in data:
        nhom = get_col(row, 'Nhóm Dự án')
        tieu_chi = get_col(row, 'Tiêu chí')
        muc_do = get_col(row, 'Mức độ ảnh hưởng')
        dieu_khoan = get_col(row, 'Điều khoản')
        bat_buoc = get_col(row, 'Hoạt động Bắt buộc')
        nhay_cam = get_col(row, 'Yếu tố Nhạy cảm')
        keyphrase = get_col(row, 'Keyphrase')
        
        if not nhom: continue
        
        # NhomDuAn Node
        cypher_params.append(f'MERGE (nda:NhomDuAn {{ten: "{nhom}"}}) ' \
                             f'ON CREATE SET nda.muc_do = "{muc_do}", nda.keyphrase = "{keyphrase}" ' \
                             f'ON MATCH SET nda.muc_do = "{muc_do}";')
                             
        # DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (nda:NhomDuAn {{ten: "{nhom}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (nda)-[:QUY_DINH_TAI]->(dl);')
            
        # TieuChi Node (Split?)
        # TieuChi often long text, treat as single description or check splitting?
        # Assuming single block for now unless semicolon
        for tc in split_list(tieu_chi):
             tc_id = generate_id(tc)
             cypher_params.append(f'MERGE (t:TieuChi {{id: "{tc_id}"}}) ON CREATE SET t.noi_dung = "{tc}";')
             cypher_params.append(f'MERGE (nda:NhomDuAn {{ten: "{nhom}"}}) MERGE (t:TieuChi {{id: "{tc_id}"}}) MERGE (nda)-[:CO_TIEU_CHI]->(t);')
             
        # HoatDong Bat Buoc
        for hd in split_list(bat_buoc):
             hd_id = generate_id(hd)
             cypher_params.append(f'MERGE (act:HoatDong {{id: "{hd_id}"}}) ON CREATE SET act.ten = "{hd}";')
             cypher_params.append(f'MERGE (nda:NhomDuAn {{ten: "{nhom}"}}) MERGE (act:HoatDong {{id: "{hd_id}"}}) MERGE (nda)-[:YEU_CAU_THUC_HIEN]->(act);')
             
        # YeuTo NhayCam
        for yt in split_list(nhay_cam):
             yt_id = generate_id(yt)
             cypher_params.append(f'MERGE (y:YeuToNhayCam {{id: "{yt_id}"}}) ON CREATE SET y.ten = "{yt}";')
             cypher_params.append(f'MERGE (nda:NhomDuAn {{ten: "{nhom}"}}) MERGE (y:YeuToNhayCam {{id: "{yt_id}"}}) MERGE (nda)-[:LIEN_QUAN_DEN]->(y);')

    # 4. QUAN HỆ KHÁI NIỆM
    print("Processing Quan He...")
    data = parse_csv(FILES["quan_he"])
    for row in data:
        kn1 = get_col(row, 'Khái niệm 1')
        kn2 = get_col(row, 'Khái niệm 2')
        rel_text = get_col(row, 'Quan hệ')
        dk = get_col(row, 'Quan hệ được quy định tại')
        
        if not kn1 or not kn2: continue
        
        rel_cypher = "LIEN_KET"
        if "Bao gồm" in rel_text or "Gồm" in rel_text: rel_cypher = "BAO_GOM"
        elif "Cơ sở" in rel_text: rel_cypher = "CO_SO"
        elif "Tác động" in rel_text: rel_cypher = "TAC_DONG"
        elif "Hậu quả" in rel_text: rel_cypher = "HAU_QUA"
        
        cypher_params.append(f'MERGE (a:KhaiNiem {{ten: "{kn1}"}});')
        cypher_params.append(f'MERGE (b:KhaiNiem {{ten: "{kn2}"}});')
        cypher_params.append(f'MERGE (a)-[:{rel_cypher} {{mo_ta: "{rel_text}"}}]->(b);')
        
        # Note: If relationship has source citation, we can't easily Attach to Edge in pure Cypher without an intermediate node or edge property.
        # Edge property is best.
        if dk:
             # Just add property to edge? Update it.
             # Need MATCH to update edge property
             cypher_params.append(f'MATCH (a:KhaiNiem {{ten: "{kn1}"}})-[r:{rel_cypher}]->(b:KhaiNiem {{ten: "{kn2}"}}) SET r.dieu_khoan = "{dk}";')

    # 5. QUY TRÌNH ĐTM
    print("Processing DTM...")
    data = parse_csv(FILES["dtm"])
    for row in data:
        giai_doan = get_col(row, 'Giai đoạn')
        hoat_dong = get_col(row, 'Hoạt động Cụ thể')
        doi_tuong = get_col(row, 'Đối tượng Thực hiện')
        dieu_khoan = get_col(row, 'Điều khoản Liên quan')
        san_pham = get_col(row, 'Sản phẩm Đầu ra')
        thoi_han = get_col(row, 'Thời hạn Pháp lý')
        yeu_cau = get_col(row, 'Yêu cầu, Tiêu chí')
        
        if not hoat_dong: continue
        hd_id = generate_id(hoat_dong)
        
        # HoatDong Node
        cypher_params.append(f'MERGE (hd:HoatDong {{id: "{hd_id}"}}) ' \
                             f'ON CREATE SET hd.ten = "{hoat_dong}", hd.thoi_han = "{thoi_han}", hd.yeu_cau = "{yeu_cau}" ' \
                             f'ON MATCH SET hd.thoi_han = "{thoi_han}";')
                             
        # GiaiDoan Link
        if giai_doan:
             cypher_params.append(f'MERGE (g:GiaiDoan {{ten: "{giai_doan}"}});')
             cypher_params.append(f'MERGE (g:GiaiDoan {{ten: "{giai_doan}"}}) MERGE (hd:HoatDong {{id: "{hd_id}"}}) MERGE (g)-[:BAO_GOM]->(hd);')
        
        # DoiTuong Link
        for dt in split_list(doi_tuong):
             cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}});')
             cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}}) MERGE (hd:HoatDong {{id: "{hd_id}"}}) MERGE (d)-[:THUC_HIEN]->(hd);')
             
        # SanPham Output
        for sp in split_list(san_pham):
             sp_id = generate_id(sp)
             cypher_params.append(f'MERGE (p:SanPham {{id: "{sp_id}"}}) ON CREATE SET p.ten = "{sp}";')
             cypher_params.append(f'MERGE (hd:HoatDong {{id: "{hd_id}"}}) MERGE (p:SanPham {{id: "{sp_id}"}}) MERGE (hd)-[:TAO_RA]->(p);')

        # DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (hd:HoatDong {{id: "{hd_id}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (hd)-[:QUY_DINH_TAI]->(dl);')

    # 6. QUYỀN NGHĨA VỤ
    print("Processing Quyen Nghia Vu...")
    data = parse_csv(FILES["quyen_nghia_vu"])
    for row in data:
        doi_tuong = get_col(row, 'Đối tượng')
        noi_dung = get_col(row, 'Nội dung')
        dieu_khoan = get_col(row, 'Điều khoản')
        co_quan = get_col(row, 'Cơ quan Thẩm quyền')
        hau_qua = get_col(row, 'Hậu quả Pháp lý')
        lien_ket = get_col(row, 'Liên kết khái niệm')
        
        if not noi_dung: continue
        qnv_id = generate_id(noi_dung)
        
        loai = "Nghĩa vụ"
        rel_type = "CO_NGHIA_VU"
        if "được" in noi_dung.lower() or "quyền" in noi_dung.lower():
            loai = "Quyền"
            rel_type = "CO_QUYEN"
            
        # QuyenNghiaVu Node
        cypher_params.append(f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) ' \
                             f'ON CREATE SET q.noi_dung = "{noi_dung}", q.loai = "{loai}";')
                             
        # DoiTuong Link
        for dt in split_list(doi_tuong):
            cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}});')
            cypher_params.append(f'MERGE (d:DoiTuong {{ten: "{dt}"}}) MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) MERGE (d)-[:{rel_type}]->(q);')
            
        # CoQuan Tham Quyen
        for cq in split_list(co_quan):
             cypher_params.append(f'MERGE (c:CoQuan {{ten: "{cq}"}});')
             cypher_params.append(f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) MERGE (c:CoQuan {{ten: "{cq}"}}) MERGE (q)-[:THAM_QUYEN_CUA]->(c);')
             
        # HauQua Phap Ly
        if hau_qua:
             hq_id = generate_id(hau_qua)
             cypher_params.append(f'MERGE (hq:HauQuaPhapLy {{id: "{hq_id}"}}) ON CREATE SET hq.noi_dung = "{hau_qua}";')
             cypher_params.append(f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) MERGE (hq:HauQuaPhapLy {{id: "{hq_id}"}}) MERGE (q)-[:GAY_HAU_QUA]->(hq);')
             
        # DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (q)-[:QUY_DINH_TAI]->(dl);')

        # Lien Ket Concept
        for c in split_list(lien_ket):
            c_clean = re.sub(r'\(.*?\)', '', c).strip()
            if c_clean:
                cypher_params.append(f'MERGE (k:KhaiNiem {{ten: "{c_clean}"}});')
                cypher_params.append(f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) MERGE (k:KhaiNiem {{ten: "{c_clean}"}}) MERGE (q)-[:LIEN_QUAN]->(k);')

    # 7. TRÁCH NHIỆM NHÀ NƯỚC
    print("Processing Trach Nhiem...")
    data = parse_csv(FILES["trach_nhiem_nn"])
    for row in data:
        co_quan = get_col(row, 'Cơ quan')
        trach_nhiem = get_col(row, 'Trách nhiệm')
        noi_dung = get_col(row, 'Nội dung')
        dieu_khoan = get_col(row, 'Điều khoản')
        lien_ket = get_col(row, 'Liên kết khái niệm')
        
        if not trach_nhiem: continue
        tn_id = generate_id(trach_nhiem + co_quan + noi_dung)
        
        # CoQuan
        cypher_params.append(f'MERGE (c:CoQuan {{ten: "{co_quan}"}});')
        
        # TrachNhiem Node
        cypher_params.append(f'MERGE (tn:TrachNhiem {{id: "{tn_id}"}}) ' \
                             f'ON CREATE SET tn.ten = "{trach_nhiem}", tn.noi_dung = "{noi_dung}";')
                             
        # Link CoQuan -> TrachNhiem
        cypher_params.append(f'MERGE (c:CoQuan {{ten: "{co_quan}"}}) MERGE (tn:TrachNhiem {{id: "{tn_id}"}}) MERGE (c)-[:CHIU_TRACH_NHIEM]->(tn);')
        
        # DieuLuat
        if dieu_khoan:
            dl_id = generate_id(dieu_khoan)
            cypher_params.append(f'MERGE (dl:DieuLuat {{id: "{dl_id}"}}) ON CREATE SET dl.ten = "{dieu_khoan}";')
            cypher_params.append(f'MERGE (tn:TrachNhiem {{id: "{tn_id}"}}) MERGE (dl:DieuLuat {{id: "{dl_id}"}}) MERGE (tn)-[:QUY_DINH_TAI]->(dl);')
            
        # Concepts
        for c in split_list(lien_ket):
            c_clean = re.sub(r'\(.*?\)', '', c).strip()
            if c_clean:
                 cypher_params.append(f'MERGE (k:KhaiNiem {{ten: "{c_clean}"}});')
                 cypher_params.append(f'MERGE (tn:TrachNhiem {{id: "{tn_id}"}}) MERGE (k:KhaiNiem {{ten: "{c_clean}"}}) MERGE (tn)-[:QUAN_LY_VE]->(k);')

    # Write output
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(cypher_params))
        print(f"Generated {len(cypher_params)} Cypher commands.")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()
