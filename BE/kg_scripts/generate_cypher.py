
import csv
import os
import re

# Configuration
KG_DIR = r"c:\Users\Luc\MediXLM\BE\kg"
OUTPUT_FILE = r"c:\Users\Luc\MediXLM\BE\kg\import.cypher"

# Files
FILES = {
    "khai_niem": "Mô hình cơ sở tri thức-DA - Khái niệm.csv",
    "quan_he": "Mô hình cơ sở tri thức-DA - Quan hệ giữa các khái niệm.csv",
    "hanh_vi": "Mô hình cơ sở tri thức-DA - Hành vi.csv",
    "phan_loai": "Mô hình cơ sở tri thức-DA - Phân loại dự án đầu tư.csv",
    "quy_trinh": "Mô hình cơ sở tri thức-DA - Quy trình đánh giá ĐTM.csv",
    "quyen_nv": "Mô hình cơ sở tri thức-DA - Quyền Nghĩa vụ.csv",
    "trach_nhiem": "Mô hình cơ sở tri thức-DA - Trách nhiệm Nhà nước.csv"
}

def clean_text(text):
    if not text:
        return ""
    # Remove leading/trailing whitespace and newlines
    text = str(text).strip().replace('\n', ' ').replace('\r', '')
    # Escape quotes for Cypher
    text = text.replace('"', "'") 
    text = text.replace('\\', '\\\\')
    return re.sub(' +', ' ', text)

def generate_id(text):
    if not text:
        return "unknown"
    # Create a simpler ID string
    s = clean_text(text).lower()
    s = re.sub(r'[^a-z0-9àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s]', '', s)
    s = re.sub(r'\s+', '_', s)
    return s[:100]  # Limit length

def write_cypher(f, query):
    f.write(query + ";\n")

def process_khai_niem(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            kn = clean_text(row.get('Khái niệm', ''))
            if not kn: continue
            
            dieu_khoan = clean_text(row.get('Điều khoản ', '')) or clean_text(row.get('Điều khoản', ''))
            noi_dung = clean_text(row.get('Nội dung ', '')) or clean_text(row.get('Nội dung', ''))
            chuong = clean_text(row.get('Chương', ''))
            keyphrase = clean_text(row.get('Keyphrase ', '')) or clean_text(row.get('Keyphrase', ''))

            query = (
                f'MERGE (n:KhaiNiem {{ten: "{kn}"}}) '
                f'ON CREATE SET n.dieu_khoan = "{dieu_khoan}", n.noi_dung = "{noi_dung}", '
                f'n.chuong = "{chuong}", n.keyphrase = "{keyphrase}" '
                f'ON MATCH SET n.dieu_khoan = "{dieu_khoan}", n.noi_dung = "{noi_dung}"'
            )
            write_cypher(f, query)

def process_quan_he(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            kn1 = clean_text(row.get('Khái niệm 1 ', '')) or clean_text(row.get('Khái niệm 1', ''))
            kn2 = clean_text(row.get('Khái niệm 2 ', '')) or clean_text(row.get('Khái niệm 2', ''))
            rel_text = clean_text(row.get('Quan hệ ', '')) or clean_text(row.get('Quan hệ', ''))
            
            if not kn1 or not kn2: continue

            # Normalize relationship type
            rel_type = "LIEN_KET"
            if "bao gồm" in rel_text.lower(): rel_type = "BAO_GOM"
            elif "cơ sở" in rel_text.lower(): rel_type = "CO_SO"
            elif "nguyên nhân" in rel_text.lower() or "gây ra" in rel_text.lower(): rel_type = "GAY_RA"
            elif "tác động" in rel_text.lower(): rel_type = "TAC_DONG"
            elif "hậu quả" in rel_text.lower(): rel_type = "HAU_QUA"
            elif "quy định" in rel_text.lower(): rel_type = "QUY_DINH"
            
            # Use 'LIEN_KET' with a property for the specific Vietnamese text
            query = (
                f'MERGE (a:KhaiNiem {{ten: "{kn1}"}}) '
                f'MERGE (b:KhaiNiem {{ten: "{kn2}"}}) '
                f'MERGE (a)-[:{rel_type} {{mo_ta: "{rel_text}"}}]->(b)'
            )
            write_cypher(f, query)

def process_hanh_vi(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            doi_tuong = clean_text(row.get('Đối tượng ', '')) or clean_text(row.get('Đối tượng', ''))
            hanh_vi = clean_text(row.get('Hành vi ', '')) or clean_text(row.get('Hành vi', ''))
            noi_dung = clean_text(row.get('Nội dung ', '')) or clean_text(row.get('Nội dung', ''))
            che_tai = clean_text(row.get('Chế tài ', '')) or clean_text(row.get('Chế tài', ''))
            lien_ket = clean_text(row.get('Liên kết khái niệm ', '')) or clean_text(row.get('Liên kết khái niệm', ''))

            if not hanh_vi: continue

            # HanhVi Node
            hv_id = generate_id(hanh_vi)
            query_hv = (
                f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}}) '
                f'ON CREATE SET h.noi_dung = "{noi_dung}", h.che_tai = "{che_tai}" '
                f'ON MATCH SET h.noi_dung = "{noi_dung}"'
            )
            write_cypher(f, query_hv)

            # DoiTuong Node & Rel
            if doi_tuong:
                # Split multiple subjects if needed, but for now treat as one entity or comma sep
                for dt in doi_tuong.split(','):
                    dt = dt.strip()
                    if not dt: continue
                    query_dt = (
                        f'MERGE (d:DoiTuong {{ten: "{dt}"}}) '
                        f'MERGE (d)-[:THUC_HIEN]->(h:HanhVi {{ten: "{hanh_vi}"}})'
                    )
                    write_cypher(f, query_dt)
            
            # Link to KhaiNiem
            if lien_ket:
                # Naive split by comma, might need better parsing if names contain commas
                # Some are like "Khái niệm A (Điều X), Khái niệm B"
                # Remove content in parenthesis for matching
                links = [re.sub(r'\(.*?\)', '', k).strip() for k in lien_ket.split(',')]
                for link in links:
                    if not link: continue
                    query_link = (
                        f'MERGE (k:KhaiNiem {{ten: "{link}"}}) '
                        f'MERGE (h:HanhVi {{ten: "{hanh_vi}"}})-[:LIEN_QUAN]->(k)'
                    )
                    write_cypher(f, query_link)

def process_quyen_nv(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            doi_tuong_str = clean_text(row.get('Đối tượng', ''))
            noi_dung = clean_text(row.get('Nội dung', ''))
            pham_vi = clean_text(row.get('Phạm vi', '')) # Quyền/Nghĩa vụ
            lien_ket = clean_text(row.get('Liên kết khái niệm', ''))

            if not doi_tuong_str or not noi_dung: continue

            # Create node for the Content (QuyenNghiaVu)
            # Use hash of content for ID or just a truncated string
            qnv_id = generate_id(noi_dung)[:50]
            
            # Classify type
            label = "Quyen" if "Quyền" in pham_vi else "NghiaVu"
            
            query_qnv = (
                f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) '
                f'SET q.noi_dung = "{noi_dung}", q.loai = "{pham_vi}"'
            )
            write_cypher(f, query_qnv)

            # DoiTuong
            for dt in doi_tuong_str.split(','):
                dt = dt.strip()
                if not dt: continue
                # Simple heuristic mapping for relations
                rel = "CO_QUYEN" if "Quyền" in pham_vi else "CO_NGHIA_VU"
                query_dt = (
                    f'MERGE (d:DoiTuong {{ten: "{dt}"}}) '
                    f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}}) '
                    f'MERGE (d)-[:{rel}]->(q)'
                )
                write_cypher(f, query_dt)

            # Link to concepts
            if lien_ket:
                links = [re.sub(r'\(.*?\)', '', k).strip() for k in lien_ket.split(',')]
                for link in links:
                    if not link: continue
                    query_link = (
                        f'MERGE (k:KhaiNiem {{ten: "{link}"}}) '
                        f'MERGE (q:QuyenNghiaVu {{id: "{qnv_id}"}})-[:DE_CAP]->(k)'
                    )
                    write_cypher(f, query_link)

def process_trach_nhiem(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            co_quan = clean_text(row.get('Cơ quan', ''))
            noi_dung = clean_text(row.get('Nội dung ', ''))
            trach_nhiem = clean_text(row.get('Trách nhiệm ', ''))
            lien_ket = clean_text(row.get('Liên kết khái niệm ', ''))

            if not co_quan: continue

            query_cq = f'MERGE (c:CoQuan {{ten: "{co_quan}"}})'
            write_cypher(f, query_cq)

            if noi_dung:
                tn_id = generate_id(trach_nhiem + "_" + noi_dung)[:50]
                query_tn = (
                    f'MERGE (tn:TrachNhiem {{id: "{tn_id}"}}) '
                    f'SET tn.ten = "{trach_nhiem}", tn.noi_dung = "{noi_dung}" '
                    f'MERGE (c:CoQuan {{ten: "{co_quan}"}})-[:CHIU_TRACH_NHIEM]->(tn)'
                )
                write_cypher(f, query_tn)

                # Link concepts
                if lien_ket:
                     links = [re.sub(r'\(.*?\)', '', k).strip() for k in lien_ket.split(',')]
                     for link in links:
                        if not link: continue
                        write_cypher(f, f'MERGE (k:KhaiNiem {{ten: "{link}"}}) MERGE (tn:TrachNhiem {{id: "{tn_id}"}})-[:QUAN_LY_VE]->(k)')

def process_phan_loai(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nhom = clean_text(row.get('Nhóm Dự án', ''))
            tieu_chi = clean_text(row.get('Tiêu chí', ''))
            muc_do = clean_text(row.get('Mức độ ảnh hưởng môi trường ', ''))
            bat_buoc = clean_text(row.get('Hoạt động Bắt buộc ', ''))

            if not nhom: continue

            query_nhom = (
                f'MERGE (n:NhomDuAn {{ten: "{nhom}"}}) '
                f'SET n.tieu_chi = "{tieu_chi}", n.muc_do_anh_huong = "{muc_do}"'
            )
            write_cypher(f, query_nhom)

            if bat_buoc:
                # Map requirement to concepts like ĐTM, PEIA, Giấy phép
                if "ĐTM" in bat_buoc or "EIA" in bat_buoc:
                    write_cypher(f, f'MERGE (k:KhaiNiem {{ten: "Đánh giá tác động môi trường (EIA/ĐTM)"}}) MERGE (n:NhomDuAn {{ten: "{nhom}"}})-[:YEU_CAU]->(k)')
                if "PEIA" in bat_buoc or "sơ bộ" in bat_buoc.lower():
                    write_cypher(f, f'MERGE (k:KhaiNiem {{ten: "Đánh giá sơ bộ tác động môi trường (PEIA)"}}) MERGE (n:NhomDuAn {{ten: "{nhom}"}})-[:YEU_CAU]->(k)')
                if "Giấy phép" in bat_buoc:
                    write_cypher(f, f'MERGE (k:KhaiNiem {{ten: "Giấy phép môi trường"}}) MERGE (n:NhomDuAn {{ten: "{nhom}"}})-[:YEU_CAU]->(k)')

def process_quy_trinh(filepath, f):
    print(f"Processing {os.path.basename(filepath).encode('ascii', 'replace').decode('ascii')}...")
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            giai_doan = clean_text(row.get('Giai đoạn', ''))
            hoat_dong = clean_text(row.get('Hoạt động Cụ thể', ''))
            doi_tuong = clean_text(row.get('Đối tượng Thực hiện ', ''))
            san_pham = clean_text(row.get('Sản phẩm Đầu ra/Kết quả', ''))

            if not giai_doan: continue
            
            # Stage Node
            gd_id = generate_id(giai_doan)
            write_cypher(f, f'MERGE (g:GiaiDoan {{ten: "{giai_doan}"}})')
            
            # Activity/Step Node
            if hoat_dong:
                hd_id = generate_id(hoat_dong)
                query_hd = (
                    f'MERGE (hd:BuocQuyTrinh {{ten: "{hoat_dong}"}}) '
                    f'MERGE (g:GiaiDoan {{ten: "{giai_doan}"}})-[:BAO_GOM]->(hd)'
                )
                write_cypher(f, query_hd)

                if doi_tuong:
                     write_cypher(f, f'MERGE (dt:DoiTuong {{ten: "{doi_tuong}"}}) MERGE (dt)-[:THUC_HIEN]->(hd)')
                
                if san_pham:
                    # San pham is likely a Concept or a Document
                    sp_clean = san_pham.split('.')[0] # Take first sentence
                    query_sp = (
                        f'MERGE (sp:KetQua {{ten: "{sp_clean}"}}) '
                        f'MERGE (hd)-[:TAO_RA]->(sp)'
                    )
                    write_cypher(f, query_sp)


def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # 1. Khai niem
        process_khai_niem(os.path.join(KG_DIR, FILES["khai_niem"]), f)
        # 2. Quan he
        process_quan_he(os.path.join(KG_DIR, FILES["quan_he"]), f)
        # 3. Hanh vi
        process_hanh_vi(os.path.join(KG_DIR, FILES["hanh_vi"]), f)
        # 4. Trach nghiem
        process_trach_nhiem(os.path.join(KG_DIR, FILES["trach_nhiem"]), f)
        # 5. Quyen Nghia vu
        process_quyen_nv(os.path.join(KG_DIR, FILES["quyen_nv"]), f)
        # 6. Phan loai du an
        process_phan_loai(os.path.join(KG_DIR, FILES["phan_loai"]), f)
        # 7. Quy trinh
        process_quy_trinh(os.path.join(KG_DIR, FILES["quy_trinh"]), f)

    print(f"Done! Cypher script generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
