// Mini Update for "Chủ nguồn thải chất thải nguy hại" - Article 83, Clause 1 (Full content)
// ID calculated from full text: e3f5b70dd62f

// 1. Define QuyenNghiaVu Node
MERGE (q:QuyenNghiaVu {id: "id_e3f5b70dd62f"}) 
ON CREATE SET q.noi_dung = "- Khai báo khối lượng, loại chất thải nguy hại trong hồ sơ đề nghị cấp giấy phép môi trường hoặc nội dung đăng ký môi trường; - Thực hiện phân định, phân loại, thu gom, lưu giữ riêng và không để lẫn với chất thải không nguy hại, bảo đảm không gây ô nhiễm môi trường; - Tự tái sử dụng, tái chế, xử lý, đồng xử lý, thu hồi năng lượng theo quy định của pháp luật hoặc chuyển giao chất thải nguy hại cho cơ sở có giấy phép môi trường phù hợp để xử lý.", q.loai = "Nghĩa vụ";

// 2. Link DoiTuong: Chủ nguồn thải chất thải nguy hại
MERGE (d:DoiTuong {ten: "Chủ nguồn thải chất thải nguy hại"});
MERGE (d)-[:CO_NGHIA_VU]->(q);

// 3. Link DieuLuat: Điều 83, Khoản 1
MERGE (dl:DieuLuat {id: "id_update_d83k1"}) 
ON CREATE SET dl.ten = "Điều 83, Khoản 1";
MERGE (q)-[:QUY_DINH_TAI]->(dl);

// 4. Link Lien Quan Concepts
MERGE (k1:KhaiNiem {ten: "Chất thải nguy hại"});
MERGE (q)-[:LIEN_QUAN]->(k1);

MERGE (k2:KhaiNiem {ten: "Giấy phép môi trường"});
MERGE (q)-[:LIEN_QUAN]->(k2);

MERGE (k3:KhaiNiem {ten: "Đăng ký môi trường"});
MERGE (q)-[:LIEN_QUAN]->(k3);

MERGE (k4:KhaiNiem {ten: "Ô nhiễm môi trường"});
MERGE (q)-[:LIEN_QUAN]->(k4);

MERGE (k5:KhaiNiem {ten: "Chất thải"});
MERGE (q)-[:LIEN_QUAN]->(k5);

// 5. Link CoQuan (Who receives the report/declaration?)
// Implied: Cơ quan cấp Giấy phép môi trường / Cơ quan nhận Đăng ký môi trường
MERGE (c:CoQuan {ten: "Cơ quan cấp Giấy phép môi trường"});
MERGE (q)-[:THAM_QUYEN_CUA]->(c);
