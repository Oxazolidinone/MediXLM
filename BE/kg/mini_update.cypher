// Mini Update for "Chủ nguồn thải chất thải nguy hại" - Row 62 from CSV
// ID calculated from content: 8f9f13a3a29f

// 1. Define QuyenNghiaVu Node
MERGE (q:QuyenNghiaVu {id: "id_8f9f13a3a29f"}) 
ON CREATE SET q.noi_dung = "- Chủ nguồn thải chất thải nguy hại có phương tiện, thiết bị phù hợp đáp ứng yêu cầu kỹ thuật, quy trình quản lý theo quy định của pháp luật về bảo vệ môi trường; - Cơ sở được cấp giấy phép môi trường có chức năng xử lý chất thải nguy hại phù hợp với loại chất thải cần vận chuyển.", q.loai = "Quyền";

// 2. Link DoiTuong 1: Chủ nguồn thải chất thải nguy hại
MERGE (d1:DoiTuong {ten: "Chủ nguồn thải chất thải nguy hại"});
MERGE (d1)-[:CO_QUYEN]->(q);

// 3. Link DoiTuong 2: Cơ sở thực hiện dịch vụ xử lý chất thải nguy hại
MERGE (d2:DoiTuong {ten: "Cơ sở thực hiện dịch vụ xử lý chất thải nguy hại"});
MERGE (d2)-[:CO_QUYEN]->(q);

// 4. Link DieuLuat: Điều 83, Khoản 4
MERGE (dl:DieuLuat {id: "id_mini_update_d83k4"}) 
ON CREATE SET dl.ten = "Điều 83, Khoản 4";
MERGE (q)-[:QUY_DINH_TAI]->(dl);

// 5. Link HauQuaPhapLy
MERGE (hq:HauQuaPhapLy {id: "id_mini_update_hq83"}) 
ON CREATE SET hq.noi_dung = "Bị xử phạt vi phạm hành chính hoặc truy cứu trách nhiệm hình sự nếu vận chuyển trái phép";
MERGE (q)-[:GAY_HAU_QUA]->(hq);

// 6. Link CoQuan Tham Quyen
MERGE (c:CoQuan {ten: "Cơ quan cấp Giấy phép môi trường (Bộ TN&MT/UBND cấp tỉnh)"});
MERGE (q)-[:THAM_QUYEN_CUA]->(c);

// 7. Link Concepts (Lien Ket)
MERGE (k1:KhaiNiem {ten: "Chất thải nguy hại"});
MERGE (q)-[:LIEN_QUAN]->(k1);

MERGE (k2:KhaiNiem {ten: "Giấy phép môi trường"});
MERGE (q)-[:LIEN_QUAN]->(k2);

MERGE (k3:KhaiNiem {ten: "Chủ nguồn thải"});
MERGE (q)-[:LIEN_QUAN]->(k3);
