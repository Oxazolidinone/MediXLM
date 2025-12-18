# KẾ HOẠCH XÂY DỰNG BỘ SUY DIỄN (REASONING ENGINE)
## Knowledge Graph - Luật Bảo vệ Môi trường Việt Nam 2020

---

## PHẦN 1: PHÂN TÍCH YÊU CẦU

### 1.1 Mục tiêu của Bộ Suy diễn

Bộ suy diễn cần hỗ trợ các tác vụ sau:

| STT | Tác vụ | Mô tả | Ví dụ |
|-----|--------|-------|-------|
| 1 | **Xác định nghĩa vụ** | Tìm tất cả nghĩa vụ của một chủ thể | "Chủ dự án Nhóm I cần làm gì?" |
| 2 | **Tra cứu thủ tục** | Xác định thủ tục cần thiết cho một loại dự án | "Dự án khai thác mỏ cần thủ tục gì?" |
| 3 | **Phân tích hậu quả** | Suy luận hậu quả pháp lý của hành vi | "Xả thải không phép bị xử lý thế nào?" |
| 4 | **Kiểm tra tuân thủ** | Kiểm tra một dự án/cơ sở có tuân thủ không | "Cơ sở X đã đủ điều kiện vận hành chưa?" |
| 5 | **Tìm cơ quan thẩm quyền** | Xác định cơ quan có thẩm quyền | "Ai cấp GPMT cho dự án quy mô này?" |
| 6 | **Truy vết căn cứ pháp lý** | Tìm điều khoản luật liên quan | "Căn cứ pháp lý cho yêu cầu ĐTM?" |
| 7 | **Phân tích chuỗi nhân quả** | Suy luận chuỗi nguyên nhân-kết quả | "Ô nhiễm dẫn đến hậu quả gì?" |
| 8 | **Gợi ý biện pháp** | Đề xuất biện pháp khắc phục/tuân thủ | "Làm gì để khắc phục vi phạm?" |

### 1.2 Đặc điểm Knowledge Graph

```
Đặc điểm cấu trúc:
├── 12 Node Labels (Classes)
├── ~60 Relationship Types  
├── ~150 Nodes
├── ~350 Relationships
├── Đồ thị có hướng (Directed Graph)
├── Quan hệ có thuộc tính (dieu_khoan, dieu_kien, thoi_han, ...)
└── Một số quan hệ được đánh dấu suy_luan: true
```

### 1.3 Các loại Suy diễn cần thiết

| Loại | Mô tả | Kỹ thuật |
|------|-------|----------|
| **Deductive** | Suy diễn từ quy tắc chung đến cụ thể | Rule-based, Forward Chaining |
| **Inductive** | Suy luận mẫu từ các trường hợp | Pattern Matching |
| **Abductive** | Suy luận ngược từ kết quả về nguyên nhân | Backward Chaining |
| **Transitive** | Suy luận qua các quan hệ bắc cầu | Graph Traversal |
| **Default** | Suy luận với giả định mặc định | Closed World Assumption |

---

## PHẦN 2: THIẾT KẾ KIẾN TRÚC

### 2.1 Kiến trúc tổng quan

```
┌─────────────────────────────────────────────────────────────────┐
│                     REASONING ENGINE                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Query      │  │   Rule       │  │   Inference  │           │
│  │   Parser     │  │   Engine     │  │   Engine     │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         ▼                 ▼                 ▼                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  REASONING CORE                          │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │    │
│  │  │Forward  │ │Backward │ │Pattern  │ │Graph    │        │    │
│  │  │Chaining │ │Chaining │ │Matching │ │Traversal│        │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              NEO4J KNOWLEDGE GRAPH                       │    │
│  │  (Nodes, Relationships, Properties)                      │    │
│  └─────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Result     │  │   Explain    │  │   Cache      │           │
│  │   Formatter  │  │   Generator  │  │   Manager    │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Các Module chính

#### Module 1: Query Parser
- Phân tích câu hỏi người dùng
- Nhận dạng intent (nghĩa vụ, thủ tục, hậu quả, ...)
- Trích xuất entities (chủ thể, dự án, hành vi, ...)

#### Module 2: Rule Engine
- Quản lý các quy tắc suy diễn
- Kiểm tra điều kiện áp dụng quy tắc
- Thực thi quy tắc

#### Module 3: Inference Engine
- Thực hiện các chiến lược suy diễn
- Kết hợp kết quả từ nhiều nguồn
- Xử lý xung đột và ưu tiên

#### Module 4: Result Formatter
- Định dạng kết quả
- Tạo giải thích (explanation)
- Trích dẫn căn cứ pháp lý

---

## PHẦN 3: ĐỊNH NGHĨA QUY TẮC SUY DIỄN

### 3.1 Quy tắc về Nghĩa vụ (Obligation Rules)

```
RULE OBL_001: Nghĩa vụ PEIA
IF: 
  - Dự án thuộc Nhóm I
THEN:
  - Chủ dự án CO_NGHIA_VU thực hiện PEIA
  - Căn cứ: Điều 29, Khoản 1

RULE OBL_002: Nghĩa vụ ĐTM  
IF:
  - Dự án thuộc Nhóm I OR (Dự án thuộc Nhóm II AND thuộc đối tượng ĐTM)
THEN:
  - Chủ dự án CO_NGHIA_VU lập Báo cáo ĐTM
  - Căn cứ: Điều 28, Khoản 3, 4

RULE OBL_003: Nghĩa vụ GPMT
IF:
  - Dự án thuộc Nhóm I, II, hoặc III
THEN:
  - Chủ dự án CO_NGHIA_VU có GPMT trước vận hành
  - Căn cứ: Điều 39

RULE OBL_004: Nghĩa vụ Đăng ký MT
IF:
  - Dự án thuộc Nhóm IV AND Phát sinh chất thải
THEN:
  - Chủ dự án CO_NGHIA_VU Đăng ký môi trường
  - Căn cứ: Điều 49

RULE OBL_005: Nghĩa vụ phân loại rác
IF:
  - Chủ thể là Hộ gia đình
THEN:
  - CO_NGHIA_VU phân loại CTRSH tại nguồn
  - Thời hạn: 31/12/2024
  - Căn cứ: Điều 75, Khoản 1

RULE OBL_006: Nghĩa vụ kiểm kê KNK
IF:
  - Cơ sở thuộc danh mục phát thải KNK
THEN:
  - CO_NGHIA_VU kiểm kê KNK định kỳ 2 năm
  - Căn cứ: Điều 91, Khoản 7a

RULE OBL_007: Nghĩa vụ tái chế (EPR)
IF:
  - Chủ thể là Nhà sản xuất/nhập khẩu sản phẩm, bao bì
THEN:
  - CO_NGHIA_VU tái chế theo tỷ lệ bắt buộc
  - HOẶC đóng góp tài chính vào Quỹ BVMT
  - Căn cứ: Điều 54

RULE OBL_008: Nghĩa vụ ký quỹ
IF:
  - Hoạt động khai thác khoáng sản OR Nhập khẩu phế liệu
THEN:
  - CO_NGHIA_VU ký quỹ BVMT
  - Căn cứ: Điều 137
```

### 3.2 Quy tắc về Thẩm quyền (Authority Rules)

```
RULE AUTH_001: Thẩm quyền Bộ TN&MT
IF:
  - Dự án thuộc Nhóm I
THEN:
  - Bộ TN&MT CO_THAM_QUYEN thẩm định ĐTM
  - Bộ TN&MT CO_THAM_QUYEN cấp GPMT
  - Căn cứ: Điều 166, Khoản 2

RULE AUTH_002: Thẩm quyền UBND tỉnh
IF:
  - Dự án thuộc Nhóm II
THEN:
  - UBND tỉnh CO_THAM_QUYEN thẩm định ĐTM
  - UBND tỉnh CO_THAM_QUYEN cấp GPMT
  - Căn cứ: Điều 168, Khoản 1b

RULE AUTH_003: Thẩm quyền UBND huyện
IF:
  - Dự án thuộc Nhóm III (theo phân cấp)
THEN:
  - UBND huyện CO_THAM_QUYEN cấp GPMT
  - Căn cứ: Điều 168, Khoản 2b

RULE AUTH_004: Thẩm quyền UBND xã
IF:
  - Dự án thuộc Nhóm IV
THEN:
  - UBND xã CO_THAM_QUYEN tiếp nhận Đăng ký MT
  - Căn cứ: Điều 168, Khoản 3b
```

### 3.3 Quy tắc về Hậu quả (Consequence Rules)

```
RULE CONS_001: Hậu quả vi phạm xả thải
IF:
  - Hành vi: Xả thải không phép OR Xả thải vượt quy chuẩn
THEN:
  - DAN_DEN Xử phạt vi phạm hành chính
  - DAN_DEN Thu hồi GPMT (nếu có)
  - DAN_DEN Truy cứu trách nhiệm hình sự (nếu nghiêm trọng)
  - Căn cứ: Điều 6, Khoản 2, 5

RULE CONS_002: Hậu quả gây ô nhiễm
IF:
  - Hành vi GAY_RA Ô nhiễm môi trường
THEN:
  - PHAI Bồi thường thiệt hại
  - PHAI Khắc phục, phục hồi môi trường
  - Căn cứ: Điều 130, Khoản 2

RULE CONS_003: Hậu quả không có GPMT
IF:
  - Vận hành mà KHÔNG CÓ GPMT
THEN:
  - Hành vi bị cấm theo Điều 6, Khoản 5
  - DAN_DEN Đình chỉ hoạt động
  - DAN_DEN Xử phạt VPHC
  
RULE CONS_004: Hậu quả không phân loại rác
IF:
  - Không phân loại CTRSH đúng quy định
THEN:
  - Bị từ chối thu gom
  - Phải chi trả như rác chưa phân loại
  - Căn cứ: Điều 75, Khoản 1
```

### 3.4 Quy tắc về Chuỗi nhân quả (Causal Chain Rules)

```
RULE CAUSAL_001: Chuỗi ô nhiễm
Chất ô nhiễm vượt ngưỡng 
  -> GAY_RA Ô nhiễm môi trường
  -> DAN_DEN Suy thoái môi trường
  -> DAN_DEN Thiệt hại môi trường
  -> YEU_CAU Bồi thường + Phục hồi

RULE CAUSAL_002: Chuỗi sự cố
Sự cố chất thải
  -> LA_LOAI Sự cố môi trường
  -> GAY_RA Ô nhiễm môi trường
  -> YEU_CAU Ứng phó sự cố
  -> YEU_CAU Phục hồi môi trường

RULE CAUSAL_003: Chuỗi khí hậu
Phát thải KNK
  -> GAY_RA Hiệu ứng nhà kính
  -> DAN_DEN Biến đổi khí hậu
  -> YEU_CAU Ứng phó BĐKH
  -> BAO_GOM Giảm nhẹ phát thải + Thích ứng
```

### 3.5 Quy tắc về Miễn trừ (Exemption Rules)

```
RULE EXEMPT_001: Miễn ĐTM
IF:
  - Dự án là Đầu tư công khẩn cấp
THEN:
  - DUOC_MIEN Đánh giá tác động môi trường
  - Căn cứ: Điều 30, Khoản 2

RULE EXEMPT_002: Miễn GPMT
IF:
  - Dự án là Đầu tư công khẩn cấp
THEN:
  - DUOC_MIEN Giấy phép môi trường
  - Căn cứ: Điều 39, Khoản 3

RULE EXEMPT_003: Miễn phí xử lý rác
IF:
  - Chất thải đã phân loại có khả năng tái chế
THEN:
  - DUOC_MIEN Giá dịch vụ thu gom, vận chuyển, xử lý
  - Căn cứ: Điều 79, Khoản 1c

RULE EXEMPT_004: Miễn bồi thường
IF:
  - Tuân thủ đầy đủ pháp luật BVMT
  - AND Không gây thiệt hại do lỗi của mình
THEN:
  - DUOC_MIEN Bồi thường thiệt hại
  - Căn cứ: Điều 130, Khoản 4
```

### 3.6 Quy tắc về Thời hạn (Deadline Rules)

```
RULE TIME_001: Thời hạn thẩm định ĐTM
IF: Dự án Nhóm I
THEN: Thời hạn thẩm định = 45 ngày

IF: Dự án Nhóm II  
THEN: Thời hạn thẩm định = 30 ngày

RULE TIME_002: Thời hạn cấp GPMT
IF: Thẩm quyền Bộ TN&MT
THEN: Thời hạn = 45 ngày

IF: Thẩm quyền UBND tỉnh
THEN: Thời hạn = 30 ngày

IF: Thẩm quyền UBND huyện
THEN: Thời hạn = 20 ngày

RULE TIME_003: Hiệu lực GPMT
IF: Dự án có ĐTM được phê duyệt
THEN: Hiệu lực GPMT = 10 năm

IF: Dự án không thuộc đối tượng ĐTM
THEN: Hiệu lực GPMT = 7 năm

RULE TIME_004: Lộ trình bắt buộc
- Phân loại CTRSH: Chậm nhất 31/12/2024
- Thị trường các-bon: Vận hành chính thức từ 2028
- EPR: Theo lộ trình Chính phủ quy định
```

---

## PHẦN 4: CHIẾN LƯỢC SUY DIỄN

### 4.1 Forward Chaining (Suy diễn tiến)

**Mục đích:** Từ dữ kiện đã biết, suy ra tất cả kết luận có thể.

**Thuật toán:**
```
1. Khởi tạo Working Memory với các dữ kiện đầu vào
2. REPEAT:
   a. Tìm tất cả quy tắc có điều kiện thỏa mãn
   b. Chọn quy tắc theo độ ưu tiên (conflict resolution)
   c. Thực thi quy tắc, thêm kết luận vào Working Memory
   d. Đánh dấu quy tắc đã thực thi
3. UNTIL không còn quy tắc nào có thể thực thi
4. Trả về Working Memory
```

**Ứng dụng:**
- Xác định tất cả nghĩa vụ của một chủ thể
- Tính toán tất cả hậu quả của một hành vi
- Liệt kê tất cả thủ tục cần thiết

### 4.2 Backward Chaining (Suy diễn lùi)

**Mục đích:** Từ mục tiêu cần chứng minh, tìm ngược về các điều kiện cần.

**Thuật toán:**
```
1. Đặt Goal là kết luận cần chứng minh
2. FUNCTION prove(Goal):
   a. Nếu Goal đã có trong Working Memory -> TRUE
   b. Tìm tất cả quy tắc có kết luận = Goal
   c. FOR EACH quy tắc:
      - FOR EACH điều kiện trong quy tắc:
        - Nếu prove(điều kiện) = FALSE -> thử quy tắc khác
      - Nếu tất cả điều kiện TRUE -> thêm Goal vào WM, return TRUE
   d. Return FALSE
3. Trả về kết quả và đường đi suy luận
```

**Ứng dụng:**
- Kiểm tra một dự án có cần ĐTM không
- Xác định điều kiện để được cấp GPMT
- Truy vết căn cứ pháp lý

### 4.3 Graph Traversal (Duyệt đồ thị)

**Mục đích:** Tìm đường đi và quan hệ trên Knowledge Graph.

**Các thuật toán:**
- **BFS:** Tìm đường ngắn nhất
- **DFS:** Tìm tất cả đường đi
- **Dijkstra:** Tìm đường với trọng số
- **Transitive Closure:** Tìm quan hệ bắc cầu

**Ứng dụng:**
- Tìm chuỗi nhân quả
- Xác định quan hệ gián tiếp
- Phân tích ảnh hưởng lan truyền

### 4.4 Pattern Matching (Đối sánh mẫu)

**Mục đích:** Tìm các cấu trúc con trong đồ thị khớp với mẫu.

**Cypher Patterns:**
```cypher
// Mẫu: Chủ thể -> Nghĩa vụ -> Đối tượng
(s:ChuThe)-[r:CO_NGHIA_VU]->(o:KhaiNiem)

// Mẫu: Hành vi -> Hậu quả -> Chế tài
(h:HanhVi)-[:DAN_DEN*1..3]->(c:CheTai)

// Mẫu: Dự án -> Thủ tục -> Cơ quan
(d:DuAn)-[:YEU_CAU]->(t:KhaiNiem)<-[:CO_THAM_QUYEN]-(cq:CoQuan)
```

---

## PHẦN 5: IMPLEMENTATION PLAN

### 5.1 Công nghệ sử dụng

| Thành phần | Công nghệ | Lý do |
|------------|-----------|-------|
| Knowledge Graph | Neo4j | Native graph database, Cypher query |
| Reasoning Engine | Python | Linh hoạt, nhiều thư viện |
| Rule Engine | Custom + Cypher | Tận dụng Neo4j |
| API | FastAPI | Hiệu năng cao, async |
| Cache | Redis | Caching query results |

### 5.2 Cấu trúc project

```
env_law_reasoner/
├── src/
│   ├── __init__.py
│   ├── config.py              # Cấu hình
│   ├── neo4j_client.py        # Kết nối Neo4j
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── base_rule.py       # Abstract Rule class
│   │   ├── obligation_rules.py
│   │   ├── authority_rules.py
│   │   ├── consequence_rules.py
│   │   ├── exemption_rules.py
│   │   └── time_rules.py
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── forward_chaining.py
│   │   ├── backward_chaining.py
│   │   ├── graph_traversal.py
│   │   └── pattern_matcher.py
│   ├── reasoner.py            # Main Reasoner class
│   ├── query_parser.py        # Parse user queries
│   ├── explainer.py           # Generate explanations
│   └── api.py                 # FastAPI endpoints
├── tests/
│   ├── test_rules.py
│   ├── test_engines.py
│   └── test_reasoner.py
├── examples/
│   └── demo_queries.py
├── requirements.txt
└── README.md
```

### 5.3 Timeline

| Giai đoạn | Thời gian | Công việc |
|-----------|-----------|-----------|
| Phase 1 | 1-2 ngày | Core Infrastructure: Neo4j client, Base classes |
| Phase 2 | 2-3 ngày | Rule Engine: Định nghĩa và implement rules |
| Phase 3 | 2-3 ngày | Inference Engines: Forward/Backward chaining |
| Phase 4 | 1-2 ngày | Graph Traversal & Pattern Matching |
| Phase 5 | 1-2 ngày | Query Parser & Explainer |
| Phase 6 | 1 ngày | API & Integration |
| Phase 7 | 1 ngày | Testing & Documentation |

---

## PHẦN 6: CÁC QUERY MẪU

### 6.1 Nghĩa vụ theo chủ thể
```cypher
// Tìm tất cả nghĩa vụ của Chủ dự án
MATCH (c:ChuThe {ten: 'Chủ dự án đầu tư'})-[r:CO_NGHIA_VU]->(k)
RETURN k.ten AS nghia_vu, r.dieu_khoan AS can_cu, r.dieu_kien AS dieu_kien
```

### 6.2 Thủ tục theo loại dự án
```cypher
// Tìm thủ tục cho Dự án Nhóm I
MATCH (d:DuAn {nhom: 'I'})-[r:YEU_CAU]->(k:KhaiNiem)
RETURN k.ten AS thu_tuc, r.bat_buoc AS bat_buoc, r.dieu_khoan AS can_cu
ORDER BY r.bat_buoc DESC
```

### 6.3 Chuỗi hậu quả
```cypher
// Tìm chuỗi hậu quả từ hành vi vi phạm
MATCH path = (h:HanhVi {trang_thai: 'cam'})-[:DAN_DEN*1..3]->(c:CheTai)
RETURN h.ten AS hanh_vi, 
       [n IN nodes(path) | n.ten] AS chuoi_hau_qua,
       c.ten AS che_tai
```

### 6.4 Cơ quan thẩm quyền
```cypher
// Tìm cơ quan có thẩm quyền cấp GPMT
MATCH (cq:CoQuan)-[r:CO_THAM_QUYEN]->(k:KhaiNiem {ten: 'Giấy phép môi trường'})
RETURN cq.ten AS co_quan, cq.cap AS cap, r.noi_dung AS tham_quyen
ORDER BY cq.cap
```

### 6.5 Kiểm tra tuân thủ
```cypher
// Kiểm tra dự án Nhóm I đã có đủ thủ tục chưa
MATCH (d:DuAn {nhom: 'I'})-[:YEU_CAU]->(req:KhaiNiem)
WHERE req.ten IN ['Đánh giá sơ bộ tác động môi trường', 
                  'Đánh giá tác động môi trường', 
                  'Giấy phép môi trường']
RETURN req.ten AS thu_tuc_can, 
       CASE WHEN req IS NOT NULL THEN 'Bắt buộc' ELSE 'Không' END AS trang_thai
```

---

## PHẦN 7: KẾT LUẬN

Bộ suy diễn được thiết kế với:
- **Quy tắc rõ ràng**: 30+ quy tắc covering nghĩa vụ, thẩm quyền, hậu quả, miễn trừ, thời hạn
- **Nhiều chiến lược suy diễn**: Forward/Backward Chaining, Graph Traversal, Pattern Matching
- **Kiến trúc module**: Dễ mở rộng, bảo trì
- **Giải thích được**: Truy vết căn cứ pháp lý

Bước tiếp theo: Implement code Python cho Reasoning Engine.
