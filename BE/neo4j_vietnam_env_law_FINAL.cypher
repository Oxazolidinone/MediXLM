// =============================================================================
// KNOWLEDGE GRAPH - LUẬT BẢO VỆ MÔI TRƯỜNG VIỆT NAM 2020
// Neo4j Cypher Import Script - PART 1: Schema + Nodes
// =============================================================================

// PHẦN 1: TẠO CONSTRAINTS VÀ INDEXES
CREATE CONSTRAINT khainem_id IF NOT EXISTS FOR (k:KhaiNiem) REQUIRE k.id IS UNIQUE;
CREATE CONSTRAINT chuthe_id IF NOT EXISTS FOR (c:ChuThe) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT hanhvi_id IF NOT EXISTS FOR (h:HanhVi) REQUIRE h.id IS UNIQUE;
CREATE CONSTRAINT duan_id IF NOT EXISTS FOR (d:DuAn) REQUIRE d.id IS UNIQUE;
CREATE CONSTRAINT thutuc_id IF NOT EXISTS FOR (t:ThuTuc) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT giaidoan_id IF NOT EXISTS FOR (g:GiaiDoan) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT coquan_id IF NOT EXISTS FOR (cq:CoQuan) REQUIRE cq.id IS UNIQUE;
CREATE CONSTRAINT vanban_id IF NOT EXISTS FOR (v:VanBan) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT chetai_id IF NOT EXISTS FOR (ct:CheTai) REQUIRE ct.id IS UNIQUE;
CREATE CONSTRAINT yeuto_id IF NOT EXISTS FOR (y:YeuToNhayCam) REQUIRE y.id IS UNIQUE;

CREATE INDEX khainem_ten IF NOT EXISTS FOR (k:KhaiNiem) ON (k.ten);
CREATE INDEX chuthe_ten IF NOT EXISTS FOR (c:ChuThe) ON (c.ten);
CREATE INDEX coquan_ten IF NOT EXISTS FOR (cq:CoQuan) ON (cq.ten);
CREATE INDEX hanhvi_ten IF NOT EXISTS FOR (h:HanhVi) ON (h.ten);

// =============================================================================
// PHẦN 2: TẠO CÁC KHÁI NIỆM (54 khái niệm)
// =============================================================================

CREATE (:KhaiNiem {id:'KN001',ten:'Môi trường',dieu_khoan:'Điều 3, Khoản 1',chuong:'I',noi_dung:'Bao gồm các yếu tố vật chất tự nhiên và nhân tạo quan hệ mật thiết với nhau, bao quanh con người, có ảnh hưởng đến đời sống, kinh tế, xã hội, sự tồn tại, phát triển của con người, sinh vật và tự nhiên.',keyphrase:'yếu tố vật chất, tự nhiên, nhân tạo'});
CREATE (:KhaiNiem {id:'KN002',ten:'Hoạt động bảo vệ môi trường',dieu_khoan:'Điều 3, Khoản 2',chuong:'I',noi_dung:'Hoạt động phòng ngừa, hạn chế tác động xấu đến môi trường; ứng phó sự cố môi trường; khắc phục ô nhiễm, suy thoái môi trường',keyphrase:'phòng ngừa, ứng phó sự cố, khắc phục ô nhiễm'});
CREATE (:KhaiNiem {id:'KN003',ten:'Thành phần môi trường',dieu_khoan:'Điều 3, Khoản 3',chuong:'I',noi_dung:'Yếu tố vật chất tạo thành môi trường gồm đất, nước, không khí, sinh vật, âm thanh, ánh sáng',keyphrase:'đất, nước, không khí, sinh vật'});
CREATE (:KhaiNiem {id:'KN004',ten:'Quy hoạch bảo vệ môi trường quốc gia',dieu_khoan:'Điều 3, Khoản 4',chuong:'I',noi_dung:'Việc sắp xếp, định hướng phân bố không gian phân vùng quản lý chất lượng môi trường',keyphrase:'phân vùng, quản lý chất lượng'});
CREATE (:KhaiNiem {id:'KN005',ten:'Đánh giá môi trường chiến lược',dieu_khoan:'Điều 3, Khoản 5',chuong:'I',noi_dung:'Quá trình nhận dạng, dự báo xu hướng của các vấn đề môi trường chính',keyphrase:'nhận dạng, dự báo xu hướng'});
CREATE (:KhaiNiem {id:'KN006',ten:'Đánh giá sơ bộ tác động môi trường',viet_tat:'PEIA',dieu_khoan:'Điều 3, Khoản 6',chuong:'I',noi_dung:'Việc xem xét, nhận dạng các vấn đề môi trường chính của dự án đầu tư trong giai đoạn nghiên cứu tiền khả thi',keyphrase:'nghiên cứu tiền khả thi'});
CREATE (:KhaiNiem {id:'KN007',ten:'Đánh giá tác động môi trường',viet_tat:'ĐTM',dieu_khoan:'Điều 3, Khoản 7',chuong:'I',noi_dung:'Quá trình phân tích, đánh giá, nhận dạng, dự báo tác động đến môi trường của dự án đầu tư và đưa ra biện pháp giảm thiểu',keyphrase:'phân tích, đánh giá, dự báo tác động'});
CREATE (:KhaiNiem {id:'KN008',ten:'Giấy phép môi trường',viet_tat:'GPMT',dieu_khoan:'Điều 3, Khoản 8',chuong:'I',noi_dung:'Văn bản do cơ quan quản lý nhà nước có thẩm quyền cấp cho tổ chức, cá nhân được phép xả chất thải ra môi trường',keyphrase:'văn bản cấp phép, xả chất thải'});
CREATE (:KhaiNiem {id:'KN009',ten:'Đăng ký môi trường',dieu_khoan:'Điều 3, Khoản 9',chuong:'I',noi_dung:'Việc chủ dự án đầu tư, cơ sở thực hiện đăng ký với cơ quan quản lý nhà nước các nội dung liên quan đến xả chất thải',keyphrase:'đăng ký với cơ quan nhà nước'});
CREATE (:KhaiNiem {id:'KN010',ten:'Quy chuẩn kỹ thuật môi trường',viet_tat:'QCKTMT',dieu_khoan:'Điều 3, Khoản 10',chuong:'I',noi_dung:'Quy định bắt buộc áp dụng mức giới hạn của thông số về chất lượng môi trường, hàm lượng của chất ô nhiễm',keyphrase:'bắt buộc áp dụng, mức giới hạn'});
CREATE (:KhaiNiem {id:'KN011',ten:'Tiêu chuẩn môi trường',dieu_khoan:'Điều 3, Khoản 11',chuong:'I',noi_dung:'Quy định tự nguyện áp dụng mức giới hạn của thông số về chất lượng môi trường',keyphrase:'tự nguyện áp dụng'});
CREATE (:KhaiNiem {id:'KN012',ten:'Ô nhiễm môi trường',dieu_khoan:'Điều 3, Khoản 12',chuong:'I',noi_dung:'Sự biến đổi tính chất vật lý, hóa học, sinh học của thành phần môi trường không phù hợp với quy chuẩn kỹ thuật môi trường',keyphrase:'biến đổi tính chất, không phù hợp quy chuẩn'});
CREATE (:KhaiNiem {id:'KN013',ten:'Suy thoái môi trường',dieu_khoan:'Điều 3, Khoản 13',chuong:'I',noi_dung:'Sự suy giảm về chất lượng, số lượng của thành phần môi trường',keyphrase:'suy giảm chất lượng, số lượng'});
CREATE (:KhaiNiem {id:'KN014',ten:'Sự cố môi trường',dieu_khoan:'Điều 3, Khoản 14',chuong:'I',noi_dung:'Sự cố xảy ra trong quá trình hoạt động của con người hoặc do biến đổi bất thường của tự nhiên, gây ô nhiễm, suy thoái môi trường nghiêm trọng',keyphrase:'sự cố, biến đổi bất thường'});
CREATE (:KhaiNiem {id:'KN015',ten:'Chất ô nhiễm',dieu_khoan:'Điều 3, Khoản 15',chuong:'I',noi_dung:'Chất hóa học hoặc tác nhân vật lý, sinh học mà khi xuất hiện trong môi trường vượt mức cho phép sẽ gây ô nhiễm',keyphrase:'vượt mức cho phép'});
CREATE (:KhaiNiem {id:'KN016',ten:'Chất ô nhiễm khó phân hủy',dieu_khoan:'Điều 3, Khoản 16',chuong:'I',noi_dung:'Chất ô nhiễm có độc tính cao, khó phân hủy, có khả năng tích lũy sinh học và lan truyền',keyphrase:'độc tính cao, khó phân hủy'});
CREATE (:KhaiNiem {id:'KN017',ten:'Chất ô nhiễm hữu cơ khó phân hủy',viet_tat:'POPs',dieu_khoan:'Điều 3, Khoản 17',chuong:'I',noi_dung:'Chất ô nhiễm khó phân hủy được quy định trong Công ước Stockholm',keyphrase:'Công ước Stockholm'});
CREATE (:KhaiNiem {id:'KN018',ten:'Chất thải',dieu_khoan:'Điều 3, Khoản 18',chuong:'I',noi_dung:'Vật chất ở thể rắn, lỏng, khí hoặc ở dạng khác được thải ra từ hoạt động sản xuất, kinh doanh, dịch vụ, sinh hoạt',keyphrase:'rắn, lỏng, khí'});
CREATE (:KhaiNiem {id:'KN019',ten:'Chất thải rắn',dieu_khoan:'Điều 3, Khoản 19',chuong:'I',noi_dung:'Chất thải ở thể rắn hoặc bùn thải',keyphrase:'thể rắn, bùn thải'});
CREATE (:KhaiNiem {id:'KN020',ten:'Chất thải nguy hại',viet_tat:'CTNH',dieu_khoan:'Điều 3, Khoản 20',chuong:'I',noi_dung:'Chất thải chứa yếu tố độc hại, phóng xạ, lây nhiễm, dễ cháy, dễ nổ, gây ăn mòn',keyphrase:'độc hại, phóng xạ, lây nhiễm'});
CREATE (:KhaiNiem {id:'KN021',ten:'Đồng xử lý chất thải',dieu_khoan:'Điều 3, Khoản 21',chuong:'I',noi_dung:'Việc kết hợp một quá trình sản xuất sẵn có để tái chế, xử lý, thu hồi năng lượng từ chất thải',keyphrase:'kết hợp sản xuất, tái chế'});
CREATE (:KhaiNiem {id:'KN022',ten:'Kiểm soát ô nhiễm',dieu_khoan:'Điều 3, Khoản 22',chuong:'I',noi_dung:'Quá trình phòng ngừa, phát hiện, ngăn chặn và xử lý ô nhiễm',keyphrase:'phòng ngừa, phát hiện, ngăn chặn'});
CREATE (:KhaiNiem {id:'KN023',ten:'Khả năng chịu tải của môi trường',dieu_khoan:'Điều 3, Khoản 23',chuong:'I',noi_dung:'Giới hạn chịu đựng của môi trường đối với các nhân tố tác động để môi trường có thể tự phục hồi',keyphrase:'giới hạn chịu đựng, tự phục hồi'});
CREATE (:KhaiNiem {id:'KN024',ten:'Hạ tầng kỹ thuật bảo vệ môi trường',dieu_khoan:'Điều 3, Khoản 24',chuong:'I',noi_dung:'Hệ thống thu gom, lưu giữ, vận chuyển, xử lý chất thải, quan trắc môi trường',keyphrase:'thu gom, xử lý chất thải'});
CREATE (:KhaiNiem {id:'KN025',ten:'Quan trắc môi trường',dieu_khoan:'Điều 3, Khoản 25',chuong:'I',noi_dung:'Việc theo dõi liên tục, định kỳ, đột xuất, có hệ thống về thành phần môi trường, các nhân tố tác động',keyphrase:'theo dõi liên tục, định kỳ'});
CREATE (:KhaiNiem {id:'KN026',ten:'Vận hành thử nghiệm công trình xử lý chất thải',dieu_khoan:'Điều 3, Khoản 26',chuong:'I',noi_dung:'Việc vận hành nhằm kiểm tra, đánh giá hiệu quả và sự phù hợp với yêu cầu về bảo vệ môi trường',keyphrase:'kiểm tra, đánh giá hiệu quả'});
CREATE (:KhaiNiem {id:'KN027',ten:'Phế liệu',dieu_khoan:'Điều 3, Khoản 27',chuong:'I',noi_dung:'Vật liệu được thu hồi, phân loại, lựa chọn từ những vật liệu, sản phẩm loại ra để sử dụng làm nguyên liệu cho sản xuất khác',keyphrase:'thu hồi, phân loại, nguyên liệu'});
CREATE (:KhaiNiem {id:'KN028',ten:'Cộng đồng dân cư',dieu_khoan:'Điều 3, Khoản 28',chuong:'I',noi_dung:'Cộng đồng người sinh sống trên cùng địa bàn thôn, ấp, bản, làng, buôn, tổ dân phố',keyphrase:'cộng đồng người, cùng địa bàn'});
CREATE (:KhaiNiem {id:'KN029',ten:'Khí nhà kính',viet_tat:'GHG',dieu_khoan:'Điều 3, Khoản 29',chuong:'I',noi_dung:'Loại khí trong khí quyển gây hiệu ứng nhà kính',keyphrase:'khí, hiệu ứng nhà kính'});
CREATE (:KhaiNiem {id:'KN030',ten:'Hiệu ứng nhà kính',dieu_khoan:'Điều 3, Khoản 30',chuong:'I',noi_dung:'Hiện tượng năng lượng bức xạ của Mặt Trời được hấp thụ trong khí quyển, chuyển hóa thành nhiệt lượng gây nóng lên toàn cầu',keyphrase:'bức xạ, nóng lên toàn cầu'});
CREATE (:KhaiNiem {id:'KN031',ten:'Giảm nhẹ phát thải khí nhà kính',dieu_khoan:'Điều 3, Khoản 31',chuong:'I',noi_dung:'Hoạt động nhằm giảm nhẹ mức độ hoặc cường độ phát thải khí nhà kính, tăng cường hấp thụ',keyphrase:'giảm cường độ phát thải'});
CREATE (:KhaiNiem {id:'KN032',ten:'Ứng phó với biến đổi khí hậu',dieu_khoan:'Điều 3, Khoản 32',chuong:'I',noi_dung:'Hoạt động của con người nhằm thích ứng với biến đổi khí hậu và giảm nhẹ phát thải khí nhà kính',keyphrase:'thích ứng, giảm nhẹ phát thải'});
CREATE (:KhaiNiem {id:'KN033',ten:'Hạn ngạch phát thải khí nhà kính',dieu_khoan:'Điều 3, Khoản 33',chuong:'I',noi_dung:'Lượng khí nhà kính được phép phát thải trong một khoảng thời gian xác định, tính theo tấn CO2',keyphrase:'lượng KNK được phép, tấn CO2'});
CREATE (:KhaiNiem {id:'KN034',ten:'Tầng ô-dôn',dieu_khoan:'Điều 3, Khoản 34',chuong:'I',noi_dung:'Một lớp trong tầng bình lưu của Trái Đất, có tác dụng bảo vệ Trái Đất khỏi các bức xạ cực tím có hại',keyphrase:'tầng bình lưu, bức xạ cực tím'});
CREATE (:KhaiNiem {id:'KN035',ten:'Tín chỉ các-bon',dieu_khoan:'Điều 3, Khoản 35',chuong:'I',noi_dung:'Chứng nhận có thể giao dịch thương mại và thể hiện quyền phát thải một tấn CO2',keyphrase:'giao dịch thương mại, quyền phát thải'});
CREATE (:KhaiNiem {id:'KN036',ten:'Kỹ thuật hiện có tốt nhất',viet_tat:'BAT',dieu_khoan:'Điều 3, Khoản 36',chuong:'I',noi_dung:'Giải pháp kỹ thuật tốt nhất được lựa chọn bảo đảm hiệu quả trong phòng ngừa, kiểm soát ô nhiễm',keyphrase:'giải pháp kỹ thuật tốt nhất'});
CREATE (:KhaiNiem {id:'KN037',ten:'Khu sản xuất kinh doanh dịch vụ tập trung',dieu_khoan:'Điều 3, Khoản 37',chuong:'I',noi_dung:'Gồm khu công nghiệp, khu chế xuất, khu công nghệ cao và khu chức năng sản xuất công nghiệp của khu kinh tế',keyphrase:'khu công nghiệp, khu chế xuất'});
CREATE (:KhaiNiem {id:'KN038',ten:'Chủ dự án đầu tư',dieu_khoan:'Điều 3, Khoản 38',chuong:'I',noi_dung:'Chủ đầu tư hoặc nhà đầu tư của dự án theo quy định của pháp luật về đầu tư',keyphrase:'chủ đầu tư, nhà đầu tư'});
CREATE (:KhaiNiem {id:'KN039',ten:'Khu vực ô nhiễm môi trường đất',dieu_khoan:'Điều 16, Khoản 1',chuong:'II',noi_dung:'Khu vực đất có chất ô nhiễm vượt mức cho phép theo quy chuẩn kỹ thuật môi trường',keyphrase:'đất ô nhiễm, vượt mức cho phép'});
CREATE (:KhaiNiem {id:'KN040',ten:'Kiểm toán môi trường',dieu_khoan:'Điều 74, Khoản 1',chuong:'VI',noi_dung:'Việc xem xét, đánh giá có hệ thống, toàn diện hiệu quả quản lý môi trường, kiểm soát ô nhiễm của cơ sở',keyphrase:'đánh giá hệ thống, hiệu quả quản lý'});
CREATE (:KhaiNiem {id:'KN041',ten:'Sự cố chất thải',dieu_khoan:'Điều 121, Khoản 6',chuong:'X',noi_dung:'Sự cố do rò rỉ, tràn đổ, phát tán chất thải',keyphrase:'rò rỉ, tràn đổ, phát tán'});
CREATE (:KhaiNiem {id:'KN042',ten:'Thiệt hại do ô nhiễm suy thoái môi trường',dieu_khoan:'Điều 130, Khoản 1',chuong:'X',noi_dung:'Bao gồm suy giảm chức năng, tính hữu ích của môi trường; thiệt hại về tính mạng, sức khỏe, tài sản',keyphrase:'suy giảm chức năng, thiệt hại'});
CREATE (:KhaiNiem {id:'KN043',ten:'Chi trả dịch vụ hệ sinh thái tự nhiên',dieu_khoan:'Điều 138, Khoản 1',chuong:'XI',noi_dung:'Việc tổ chức, cá nhân sử dụng dịch vụ hệ sinh thái tự nhiên trả tiền cho tổ chức, cá nhân cung ứng',keyphrase:'trả tiền dịch vụ hệ sinh thái'});
CREATE (:KhaiNiem {id:'KN044',ten:'Thị trường các-bon trong nước',dieu_khoan:'Điều 139, Khoản 1',chuong:'XI',noi_dung:'Gồm các hoạt động trao đổi hạn ngạch phát thải khí nhà kính và tín chỉ các-bon',keyphrase:'trao đổi hạn ngạch, tín chỉ các-bon'});
CREATE (:KhaiNiem {id:'KN045',ten:'Kinh tế tuần hoàn',dieu_khoan:'Điều 142, Khoản 1',chuong:'XI',noi_dung:'Mô hình kinh tế nhằm giảm khai thác nguyên liệu, vật liệu, kéo dài vòng đời sản phẩm, hạn chế chất thải phát sinh',keyphrase:'giảm khai thác, kéo dài vòng đời'});
CREATE (:KhaiNiem {id:'KN046',ten:'Công nghiệp môi trường',dieu_khoan:'Điều 143, Khoản 1',chuong:'XI',noi_dung:'Ngành kinh tế cung cấp công nghệ, thiết bị và sản phẩm phục vụ yêu cầu về bảo vệ môi trường',keyphrase:'cung cấp công nghệ, thiết bị BVMT'});
CREATE (:KhaiNiem {id:'KN047',ten:'Dịch vụ môi trường',dieu_khoan:'Điều 144, Khoản 1',chuong:'XI',noi_dung:'Ngành kinh tế cung cấp dịch vụ đo lường, kiểm soát, hạn chế, phòng ngừa và giảm thiểu ô nhiễm',keyphrase:'đo lường, kiểm soát, giảm thiểu'});
CREATE (:KhaiNiem {id:'KN048',ten:'Sản phẩm dịch vụ thân thiện môi trường',dieu_khoan:'Điều 145, Khoản 1',chuong:'XI',noi_dung:'Sản phẩm, dịch vụ được tạo ra từ nguyên liệu, công nghệ thân thiện môi trường, giảm tác động tiêu cực',keyphrase:'thân thiện môi trường'});
CREATE (:KhaiNiem {id:'KN049',ten:'Nhãn sinh thái Việt Nam',dieu_khoan:'Điều 145, Khoản 2',chuong:'XI',noi_dung:'Nhãn được cơ quan có thẩm quyền của Việt Nam chứng nhận cho sản phẩm, dịch vụ thân thiện môi trường',keyphrase:'nhãn chứng nhận'});
CREATE (:KhaiNiem {id:'KN050',ten:'Mua sắm xanh',dieu_khoan:'Điều 146, Khoản 1',chuong:'XI',noi_dung:'Việc mua sắm các sản phẩm, dịch vụ thân thiện môi trường được chứng nhận Nhãn sinh thái Việt Nam',keyphrase:'mua sắm sản phẩm thân thiện'});
CREATE (:KhaiNiem {id:'KN051',ten:'Vốn tự nhiên',dieu_khoan:'Điều 147, Khoản 1',chuong:'XI',noi_dung:'Các nguồn tài nguyên thiên nhiên, gồm đất, nước, rừng, nguồn lợi thủy sản, khoáng sản và dịch vụ hệ sinh thái',keyphrase:'tài nguyên thiên nhiên'});
CREATE (:KhaiNiem {id:'KN052',ten:'Tín dụng xanh',dieu_khoan:'Điều 149, Khoản 1',chuong:'XI',noi_dung:'Tín dụng được cấp cho dự án đầu tư sử dụng hiệu quả tài nguyên thiên nhiên; ứng phó với biến đổi khí hậu',keyphrase:'tín dụng cho ứng phó BĐKH'});
CREATE (:KhaiNiem {id:'KN053',ten:'Trái phiếu xanh',dieu_khoan:'Điều 150, Khoản 1',chuong:'XI',noi_dung:'Trái phiếu do Chính phủ, chính quyền địa phương, doanh nghiệp phát hành để huy động vốn cho hoạt động bảo vệ môi trường',keyphrase:'trái phiếu huy động vốn BVMT'});
CREATE (:KhaiNiem {id:'KN054',ten:'Quỹ Bảo vệ môi trường',dieu_khoan:'Điều 151, Khoản 1',chuong:'XI',noi_dung:'Tổ chức tài chính nhà nước thành lập ở trung ương, tỉnh để cho vay ưu đãi, nhận ký quỹ, tài trợ hoạt động BVMT',keyphrase:'tổ chức tài chính, cho vay ưu đãi'});

// =============================================================================
// PHẦN 3: TẠO CÁC CHỦ THỂ (12 chủ thể)
// =============================================================================

CREATE (:ChuThe {id:'CT001',ten:'Tổ chức',loai:'phap_nhan',mo_ta:'Pháp nhân hoạt động trên lãnh thổ Việt Nam'});
CREATE (:ChuThe {id:'CT002',ten:'Cá nhân',loai:'the_nhan',mo_ta:'Cá nhân hoạt động trên lãnh thổ Việt Nam'});
CREATE (:ChuThe {id:'CT003',ten:'Chủ dự án đầu tư',loai:'phap_nhan',mo_ta:'Chủ đầu tư hoặc nhà đầu tư của dự án'});
CREATE (:ChuThe {id:'CT004',ten:'Cơ sở sản xuất kinh doanh',loai:'phap_nhan',mo_ta:'Cơ sở sản xuất, kinh doanh, dịch vụ'});
CREATE (:ChuThe {id:'CT005',ten:'Hộ gia đình',loai:'ho_gia_dinh',mo_ta:'Hộ gia đình sinh sống trên lãnh thổ Việt Nam'});
CREATE (:ChuThe {id:'CT006',ten:'Cộng đồng dân cư',loai:'cong_dong',mo_ta:'Cộng đồng người sinh sống trên cùng địa bàn'});
CREATE (:ChuThe {id:'CT007',ten:'Cán bộ công chức',loai:'ca_nhan',mo_ta:'Cán bộ, công chức nhà nước'});
CREATE (:ChuThe {id:'CT008',ten:'Chủ nguồn thải CTNH',loai:'phap_nhan',mo_ta:'Chủ nguồn thải chất thải nguy hại'});
CREATE (:ChuThe {id:'CT009',ten:'Cơ sở xử lý CTNH',loai:'phap_nhan',mo_ta:'Cơ sở thực hiện dịch vụ xử lý chất thải nguy hại'});
CREATE (:ChuThe {id:'CT010',ten:'Nhà sản xuất nhập khẩu',loai:'phap_nhan',mo_ta:'Tổ chức, cá nhân sản xuất, nhập khẩu sản phẩm, bao bì'});
CREATE (:ChuThe {id:'CT011',ten:'Cơ sở phát thải KNK',loai:'phap_nhan',mo_ta:'Cơ sở phát thải khí nhà kính thuộc danh mục kiểm kê'});
CREATE (:ChuThe {id:'CT012',ten:'Tổ chức tín dụng',loai:'phap_nhan',mo_ta:'Tổ chức tín dụng, chi nhánh ngân hàng nước ngoài'});

// =============================================================================
// PHẦN 4: TẠO CÁC CƠ QUAN NHÀ NƯỚC (8 cơ quan)
// =============================================================================

CREATE (:CoQuan {id:'CQ001',ten:'Chính phủ',cap:'trung_uong',mo_ta:'Cơ quan hành pháp cao nhất',tham_quyen:'Quản lý thống nhất về BVMT trong phạm vi cả nước'});
CREATE (:CoQuan {id:'CQ002',ten:'Bộ Tài nguyên và Môi trường',viet_tat:'BTNMT',cap:'trung_uong',mo_ta:'Cơ quan quản lý nhà nước về môi trường',tham_quyen:'Thẩm định ĐTM, cấp GPMT, quản lý chất thải, quan trắc môi trường'});
CREATE (:CoQuan {id:'CQ003',ten:'Bộ Quốc phòng',cap:'trung_uong',mo_ta:'Cơ quan quản lý nhà nước về quốc phòng',tham_quyen:'BVMT trong lĩnh vực quốc phòng, ứng phó sự cố môi trường'});
CREATE (:CoQuan {id:'CQ004',ten:'Bộ Công an',cap:'trung_uong',mo_ta:'Cơ quan quản lý nhà nước về an ninh',tham_quyen:'BVMT trong lĩnh vực an ninh'});
CREATE (:CoQuan {id:'CQ005',ten:'UBND cấp tỉnh',cap:'tinh',mo_ta:'Ủy ban nhân dân cấp tỉnh/thành phố trực thuộc TW',tham_quyen:'Thẩm định ĐTM, cấp GPMT theo thẩm quyền'});
CREATE (:CoQuan {id:'CQ006',ten:'UBND cấp huyện',cap:'huyen',mo_ta:'Ủy ban nhân dân cấp huyện/quận/thị xã',tham_quyen:'Cấp GPMT theo thẩm quyền, kiểm tra thanh tra'});
CREATE (:CoQuan {id:'CQ007',ten:'UBND cấp xã',cap:'xa',mo_ta:'Ủy ban nhân dân cấp xã/phường/thị trấn',tham_quyen:'Tiếp nhận đăng ký môi trường, kiểm soát nguồn ô nhiễm'});
CREATE (:CoQuan {id:'CQ008',ten:'Quỹ Bảo vệ môi trường Việt Nam',cap:'trung_uong',mo_ta:'Tổ chức tài chính nhà nước về môi trường',tham_quyen:'Cho vay ưu đãi, nhận ký quỹ, tài trợ hoạt động BVMT'});
// =============================================================================
// KNOWLEDGE GRAPH - LUẬT BẢO VỆ MÔI TRƯỜNG VIỆT NAM 2020
// Neo4j Cypher Import Script - PHẦN 2: RELATIONSHIPS
// =============================================================================

// Tiếp tục từ phần Yếu tố nhạy cảm
CREATE (yn002:YeuToNhayCam {id: 'YN002', ten: 'Nguồn nước cấp sinh hoạt', mo_ta: 'Nguồn nước phục vụ cấp nước sinh hoạt'});
CREATE (yn003:YeuToNhayCam {id: 'YN003', ten: 'Khu bảo tồn thiên nhiên', mo_ta: 'Khu vực được bảo tồn thiên nhiên theo quy định'});
CREATE (yn004:YeuToNhayCam {id: 'YN004', ten: 'Các loại rừng', mo_ta: 'Rừng đặc dụng, rừng phòng hộ, rừng sản xuất'});
CREATE (yn005:YeuToNhayCam {id: 'YN005', ten: 'Đất trồng lúa nước từ 02 vụ', mo_ta: 'Đất trồng lúa nước từ 02 vụ trở lên'});
CREATE (yn006:YeuToNhayCam {id: 'YN006', ten: 'Vùng đất ngập nước quan trọng', mo_ta: 'Vùng đất ngập nước có tầm quan trọng quốc gia, quốc tế'});
CREATE (yn007:YeuToNhayCam {id: 'YN007', ten: 'Di dân tái định cư', mo_ta: 'Yêu cầu di dân, tái định cư quy mô lớn'});

// =============================================================================
// PHẦN 8: TẠO CÁC GIAI ĐOẠN QUY TRÌNH ĐTM (GiaiDoan)
// =============================================================================

CREATE (gd001:GiaiDoan {id: 'GD001', ten: 'Phân loại dự án', thu_tu: 1, mo_ta: 'Phân loại dự án đầu tư (Nhóm I, II, III, IV) để xác định thủ tục môi trường', dieu_khoan: 'Điều 28'});
CREATE (gd002:GiaiDoan {id: 'GD002', ten: 'Đánh giá sơ bộ tác động môi trường', viet_tat: 'PEIA', thu_tu: 2, mo_ta: 'Đánh giá sự phù hợp địa điểm với chiến lược/quy hoạch BVMT trong giai đoạn nghiên cứu tiền khả thi', dieu_khoan: 'Điều 29', san_pham: 'Nội dung PEIA trong hồ sơ đề nghị chấp thuận chủ trương đầu tư'});
CREATE (gd003:GiaiDoan {id: 'GD003', ten: 'Lập Báo cáo ĐTM', thu_tu: 3, mo_ta: 'Phân tích, đánh giá sự phù hợp quy hoạch, công nghệ, hiện trạng, dự báo tác động, biện pháp giảm thiểu', dieu_khoan: 'Điều 31, 32', san_pham: 'Báo cáo đánh giá tác động môi trường (EIAR)'});
CREATE (gd004:GiaiDoan {id: 'GD004', ten: 'Tham vấn', thu_tu: 4, mo_ta: 'Tham vấn ý kiến các đối tượng chịu tác động trực tiếp và cơ quan liên quan', dieu_khoan: 'Điều 33', san_pham: 'Kết quả tham vấn thể hiện trong báo cáo ĐTM'});
CREATE (gd005:GiaiDoan {id: 'GD005', ten: 'Thẩm định Báo cáo ĐTM', thu_tu: 5, mo_ta: 'Tổ chức thẩm định báo cáo ĐTM, Hội đồng thẩm định tối thiểu 07 thành viên', dieu_khoan: 'Điều 34', thoi_han: '45 ngày (Nhóm I), 30 ngày (Nhóm II)', san_pham: 'Thông báo kết quả thẩm định'});
CREATE (gd006:GiaiDoan {id: 'GD006', ten: 'Phê duyệt kết quả thẩm định', thu_tu: 6, mo_ta: 'Ra quyết định phê duyệt kết quả thẩm định báo cáo ĐTM', dieu_khoan: 'Điều 34, 36', thoi_han: '20 ngày kể từ ngày nhận báo cáo ĐTM đã chỉnh sửa', san_pham: 'Quyết định phê duyệt kết quả thẩm định báo cáo ĐTM'});
CREATE (gd007:GiaiDoan {id: 'GD007', ten: 'Thực hiện sau phê duyệt', thu_tu: 7, mo_ta: 'Điều chỉnh dự án phù hợp với yêu cầu BVMT, công khai báo cáo ĐTM đã phê duyệt', dieu_khoan: 'Điều 37', san_pham: 'Dự án đã điều chỉnh, báo cáo ĐTM được công khai'});

// =============================================================================
// PHẦN 9: TẠO CÁC THỦ TỤC HÀNH CHÍNH (ThuTuc)
// =============================================================================

CREATE (tt001:ThuTuc {id: 'TT001', ten: 'Thẩm định ĐTM cấp Bộ', mo_ta: 'Thẩm định báo cáo ĐTM thuộc thẩm quyền Bộ TN&MT', thoi_han: '45 ngày', co_quan: 'Bộ Tài nguyên và Môi trường'});
CREATE (tt002:ThuTuc {id: 'TT002', ten: 'Thẩm định ĐTM cấp tỉnh', mo_ta: 'Thẩm định báo cáo ĐTM thuộc thẩm quyền UBND cấp tỉnh', thoi_han: '30 ngày', co_quan: 'UBND cấp tỉnh'});
CREATE (tt003:ThuTuc {id: 'TT003', ten: 'Cấp Giấy phép môi trường cấp Bộ', mo_ta: 'Cấp GPMT thuộc thẩm quyền Bộ TN&MT', thoi_han: '45 ngày', co_quan: 'Bộ Tài nguyên và Môi trường'});
CREATE (tt004:ThuTuc {id: 'TT004', ten: 'Cấp Giấy phép môi trường cấp tỉnh', mo_ta: 'Cấp GPMT thuộc thẩm quyền UBND cấp tỉnh', thoi_han: '30 ngày', co_quan: 'UBND cấp tỉnh'});
CREATE (tt005:ThuTuc {id: 'TT005', ten: 'Cấp Giấy phép môi trường cấp huyện', mo_ta: 'Cấp GPMT thuộc thẩm quyền UBND cấp huyện', thoi_han: '20 ngày', co_quan: 'UBND cấp huyện'});
CREATE (tt006:ThuTuc {id: 'TT006', ten: 'Đăng ký môi trường', mo_ta: 'Đăng ký môi trường với UBND cấp xã', co_quan: 'UBND cấp xã'});

// =============================================================================
// PHẦN 10: TẠO CÁC CHẾ TÀI (CheTai)
// =============================================================================

CREATE (cht001:CheTai {id: 'CHT001', ten: 'Xử lý theo Luật BVMT', loai: 'hanh_chinh', mo_ta: 'Bị xử lý theo quy định của Luật này và quy định khác của pháp luật có liên quan'});
CREATE (cht002:CheTai {id: 'CHT002', ten: 'Xử phạt vi phạm hành chính', loai: 'hanh_chinh', mo_ta: 'Bị xử phạt vi phạm hành chính theo quy định'});
CREATE (cht003:CheTai {id: 'CHT003', ten: 'Truy cứu trách nhiệm hình sự', loai: 'hinh_su', mo_ta: 'Bị truy cứu trách nhiệm hình sự theo quy định của pháp luật'});
CREATE (cht004:CheTai {id: 'CHT004', ten: 'Bồi thường thiệt hại', loai: 'dan_su', mo_ta: 'Phải bồi thường toàn bộ thiệt hại và chi trả chi phí xác định thiệt hại'});
CREATE (cht005:CheTai {id: 'CHT005', ten: 'Thu hồi giấy phép môi trường', loai: 'hanh_chinh', mo_ta: 'Bị tước quyền sử dụng hoặc thu hồi Giấy phép môi trường'});
CREATE (cht006:CheTai {id: 'CHT006', ten: 'Xử lý kỷ luật', loai: 'ky_luat', mo_ta: 'Bị xử lý kỷ luật đối với cán bộ, công chức'});

// =============================================================================
// PHẦN 11: TẠO CÁC VĂN BẢN (VanBan)
// =============================================================================

CREATE (vb001:VanBan {id: 'VB001', ten: 'Báo cáo đánh giá tác động môi trường', loai: 'bao_cao', viet_tat: 'Báo cáo ĐTM'});
CREATE (vb002:VanBan {id: 'VB002', ten: 'Quyết định phê duyệt kết quả thẩm định ĐTM', loai: 'quyet_dinh'});
CREATE (vb003:VanBan {id: 'VB003', ten: 'Giấy phép môi trường', loai: 'giay_phep', viet_tat: 'GPMT'});
CREATE (vb004:VanBan {id: 'VB004', ten: 'Đăng ký môi trường', loai: 'dang_ky'});

// =============================================================================
// PHẦN 12: TẠO CÁC QUAN HỆ (RELATIONSHIPS)
// =============================================================================

// --- 12.1 QUAN HỆ CẤU TRÚC KHÁI NIỆM ---

// Môi trường BAO_GOM Thành phần môi trường
MATCH (a:KhaiNiem {id: 'KN001'}), (b:KhaiNiem {id: 'KN003'})
CREATE (a)-[:BAO_GOM {dieu_khoan: 'Điều 3, Khoản 1'}]->(b);

// Chất thải -> các loại chất thải
MATCH (a:KhaiNiem {id: 'KN018'}), (b:KhaiNiem {id: 'KN019'})
CREATE (a)-[:BAO_GOM]->(b);

MATCH (a:KhaiNiem {id: 'KN018'}), (b:KhaiNiem {id: 'KN020'})
CREATE (a)-[:BAO_GOM]->(b);

// Chất ô nhiễm -> các loại
MATCH (a:KhaiNiem {id: 'KN015'}), (b:KhaiNiem {id: 'KN016'})
CREATE (b)-[:LA_LOAI]->(a);

MATCH (a:KhaiNiem {id: 'KN016'}), (b:KhaiNiem {id: 'KN017'})
CREATE (b)-[:LA_LOAI]->(a);

// Ứng phó BĐKH bao gồm Giảm nhẹ phát thải
MATCH (a:KhaiNiem {id: 'KN032'}), (b:KhaiNiem {id: 'KN031'})
CREATE (a)-[:BAO_GOM {dieu_khoan: 'Điều 3, Khoản 32'}]->(b);

// Khí nhà kính gây Hiệu ứng nhà kính
MATCH (a:KhaiNiem {id: 'KN029'}), (b:KhaiNiem {id: 'KN030'})
CREATE (a)-[:GAY_RA {dieu_khoan: 'Điều 3, Khoản 29'}]->(b);

// --- 12.2 QUAN HỆ NHÂN QUẢ ---

// Sự cố môi trường GAY_RA Ô nhiễm/Suy thoái
MATCH (a:KhaiNiem {id: 'KN014'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:GAY_RA {dieu_khoan: 'Điều 3, Khoản 14'}]->(b);

MATCH (a:KhaiNiem {id: 'KN014'}), (b:KhaiNiem {id: 'KN013'})
CREATE (a)-[:GAY_RA {dieu_khoan: 'Điều 3, Khoản 14'}]->(b);

// Sự cố chất thải LA_LOAI Sự cố môi trường
MATCH (a:KhaiNiem {id: 'KN041'}), (b:KhaiNiem {id: 'KN014'})
CREATE (a)-[:LA_LOAI {dieu_khoan: 'Điều 121, Khoản 6'}]->(b);

// Ô nhiễm DAN_DEN Thiệt hại
MATCH (a:KhaiNiem {id: 'KN012'}), (b:KhaiNiem {id: 'KN042'})
CREATE (a)-[:DAN_DEN {dieu_khoan: 'Điều 130, Khoản 1'}]->(b);

// Suy thoái DAN_DEN Thiệt hại
MATCH (a:KhaiNiem {id: 'KN013'}), (b:KhaiNiem {id: 'KN042'})
CREATE (a)-[:DAN_DEN {dieu_khoan: 'Điều 130, Khoản 1'}]->(b);

// Ô nhiễm DANH_GIA_THEO Quy chuẩn
MATCH (a:KhaiNiem {id: 'KN012'}), (b:KhaiNiem {id: 'KN010'})
CREATE (a)-[:DANH_GIA_THEO {dieu_khoan: 'Điều 3, Khoản 12'}]->(b);

// Hoạt động BVMT PHONG_NGUA Ô nhiễm
MATCH (a:KhaiNiem {id: 'KN002'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:PHONG_NGUA {dieu_khoan: 'Điều 3, Khoản 2'}]->(b);

// Hoạt động BVMT PHONG_NGUA Suy thoái
MATCH (a:KhaiNiem {id: 'KN002'}), (b:KhaiNiem {id: 'KN013'})
CREATE (a)-[:PHONG_NGUA {dieu_khoan: 'Điều 3, Khoản 2'}]->(b);

// Kiểm soát ô nhiễm PHONG_NGUA Ô nhiễm
MATCH (a:KhaiNiem {id: 'KN022'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:PHONG_NGUA {dieu_khoan: 'Điều 3, Khoản 22'}]->(b);

// --- 12.3 QUAN HỆ ĐÁNH GIÁ MÔI TRƯỜNG ---

// ĐMC là cơ sở để lập Quy hoạch
MATCH (a:KhaiNiem {id: 'KN005'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:CO_SO_DE_LAP {dieu_khoan: 'Điều 22, Khoản 1'}]->(b);

// ĐTM là cơ sở để cấp GPMT
MATCH (a:KhaiNiem {id: 'KN007'}), (b:KhaiNiem {id: 'KN008'})
CREATE (a)-[:CAN_CU_DE_CAP {dieu_khoan: 'Điều 36, Khoản 1; Điều 42, Khoản 1b'}]->(b);

// GPMT phải có trước Vận hành thử nghiệm
MATCH (a:KhaiNiem {id: 'KN008'}), (b:KhaiNiem {id: 'KN026'})
CREATE (a)-[:TRUOC_KHI {dieu_khoan: 'Điều 42, Khoản 2a', bat_buoc: true}]->(b);

// GPMT và Đăng ký môi trường - quan hệ thay thế
MATCH (a:KhaiNiem {id: 'KN008'}), (b:KhaiNiem {id: 'KN009'})
CREATE (a)-[:THAY_THE {dieu_khoan: 'Điều 39, Khoản 1; Điều 49, Khoản 1', ghi_chu: 'GPMT cho đối tượng lớn, Đăng ký MT cho đối tượng nhỏ'}]->(b);

// --- 12.4 QUAN HỆ CHỦ THỂ - HÀNH VI BỊ CẤM ---

// Tổ chức bị cấm các hành vi
MATCH (c:ChuThe {id: 'CT001'}), (h:HanhVi) WHERE h.trang_thai = 'cam' AND h.id IN ['HV001','HV002','HV003','HV004','HV006','HV007','HV009','HV010','HV011','HV012','HV013']
CREATE (c)-[:BI_CAM]->(h);

// Cá nhân bị cấm các hành vi
MATCH (c:ChuThe {id: 'CT002'}), (h:HanhVi) WHERE h.trang_thai = 'cam' AND h.id IN ['HV001','HV002','HV003','HV004','HV009','HV010','HV011','HV012','HV013']
CREATE (c)-[:BI_CAM]->(h);

// Chủ dự án bị cấm
MATCH (c:ChuThe {id: 'CT003'}), (h:HanhVi {id: 'HV005'})
CREATE (c)-[:BI_CAM {dieu_khoan: 'Điều 6, Khoản 5'}]->(h);

MATCH (c:ChuThe {id: 'CT003'}), (h:HanhVi {id: 'HV008'})
CREATE (c)-[:BI_CAM {dieu_khoan: 'Điều 6, Khoản 8'}]->(h);

// Cán bộ công chức bị cấm lợi dụng chức vụ
MATCH (c:ChuThe {id: 'CT007'}), (h:HanhVi {id: 'HV014'})
CREATE (c)-[:BI_CAM {dieu_khoan: 'Điều 6, Khoản 14'}]->(h);

// --- 12.5 QUAN HỆ HÀNH VI - CHẾ TÀI ---

// Các hành vi bị cấm DAN_DEN chế tài chung
MATCH (h:HanhVi {trang_thai: 'cam'}), (ct:CheTai {id: 'CHT001'})
CREATE (h)-[:DAN_DEN]->(ct);

// Cán bộ lợi dụng chức vụ -> chế tài đặc biệt
MATCH (h:HanhVi {id: 'HV014'}), (ct:CheTai {id: 'CHT006'})
CREATE (h)-[:DAN_DEN {dieu_khoan: 'Điều 6, Khoản 14'}]->(ct);

MATCH (h:HanhVi {id: 'HV014'}), (ct:CheTai {id: 'CHT003'})
CREATE (h)-[:DAN_DEN {dieu_khoan: 'Điều 6, Khoản 14'}]->(ct);

// --- 12.6 QUAN HỆ DỰ ÁN - THỦ TỤC YÊU CẦU ---

// Dự án Nhóm I YEU_CAU các thủ tục
MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN006'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, dieu_khoan: 'Điều 29, Khoản 1'}]->(k);

MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN007'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, dieu_khoan: 'Điều 28, Khoản 3'}]->(k);

MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN008'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, dieu_khoan: 'Điều 39'}]->(k);

// Dự án Nhóm II YEU_CAU
MATCH (d:DuAn {id: 'DA002'}), (k:KhaiNiem {id: 'KN007'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, ghi_chu: 'Một số đối tượng theo Điều 28 Khoản 4c,d,đ,e', dieu_khoan: 'Điều 28, Khoản 4'}]->(k);

MATCH (d:DuAn {id: 'DA002'}), (k:KhaiNiem {id: 'KN008'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, dieu_khoan: 'Điều 39'}]->(k);

// Dự án Nhóm III YEU_CAU
MATCH (d:DuAn {id: 'DA003'}), (k:KhaiNiem {id: 'KN008'})
CREATE (d)-[:YEU_CAU {bat_buoc: true, ghi_chu: 'Khi vận hành chính thức', dieu_khoan: 'Điều 39'}]->(k);

// Dự án Nhóm IV YEU_CAU
MATCH (d:DuAn {id: 'DA004'}), (k:KhaiNiem {id: 'KN009'})
CREATE (d)-[:YEU_CAU {bat_buoc: false, ghi_chu: 'Nếu phát sinh chất thải', dieu_khoan: 'Điều 49'}]->(k);

// --- 12.7 QUAN HỆ DỰ ÁN - YẾU TỐ NHẠY CẢM ---

MATCH (d:DuAn {nhom: 'I'}), (y:YeuToNhayCam)
CREATE (d)-[:LIEN_QUAN_YEU_TO]->(y);

// --- 12.8 QUAN HỆ QUY TRÌNH ĐTM ---

// Các giai đoạn theo thứ tự
MATCH (g1:GiaiDoan {id: 'GD001'}), (g2:GiaiDoan {id: 'GD002'})
CREATE (g1)-[:TRUOC_KHI]->(g2);

MATCH (g2:GiaiDoan {id: 'GD002'}), (g3:GiaiDoan {id: 'GD003'})
CREATE (g2)-[:TRUOC_KHI]->(g3);

MATCH (g3:GiaiDoan {id: 'GD003'}), (g4:GiaiDoan {id: 'GD004'})
CREATE (g3)-[:TRUOC_KHI]->(g4);

MATCH (g4:GiaiDoan {id: 'GD004'}), (g5:GiaiDoan {id: 'GD005'})
CREATE (g4)-[:TRUOC_KHI]->(g5);

MATCH (g5:GiaiDoan {id: 'GD005'}), (g6:GiaiDoan {id: 'GD006'})
CREATE (g5)-[:TRUOC_KHI]->(g6);

MATCH (g6:GiaiDoan {id: 'GD006'}), (g7:GiaiDoan {id: 'GD007'})
CREATE (g6)-[:TRUOC_KHI]->(g7);

// --- 12.9 QUAN HỆ CƠ QUAN - THẨM QUYỀN ---

// Bộ TN&MT có thẩm quyền
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN007'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Thẩm định ĐTM Nhóm I', dieu_khoan: 'Điều 166, Khoản 2'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN008'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Cấp GPMT theo thẩm quyền Bộ', dieu_khoan: 'Điều 166, Khoản 2'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN010'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Ban hành QCKT quốc gia', dieu_khoan: 'Điều 166, Khoản 1'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN025'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Quản lý mạng lưới quan trắc quốc gia', dieu_khoan: 'Điều 166, Khoản 4'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN018'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Quản lý chất thải', dieu_khoan: 'Điều 166, Khoản 3'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN033'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Phân bổ hạn ngạch KNK', dieu_khoan: 'Điều 139, Khoản 10'}]->(k);

MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN044'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Vận hành thị trường các-bon', dieu_khoan: 'Điều 139, Khoản 10'}]->(k);

// UBND cấp tỉnh có thẩm quyền
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN007'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Thẩm định ĐTM Nhóm II', dieu_khoan: 'Điều 168, Khoản 1b'}]->(k);

MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN008'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Cấp GPMT theo thẩm quyền tỉnh', dieu_khoan: 'Điều 168, Khoản 1b'}]->(k);

MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN019'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Quản lý chất thải rắn sinh hoạt', dieu_khoan: 'Điều 79, Khoản 6'}]->(k);

MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN010'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Ban hành QCKT địa phương', dieu_khoan: 'Điều 102, Khoản 5'}]->(k);

// UBND cấp huyện có thẩm quyền
MATCH (cq:CoQuan {id: 'CQ006'}), (k:KhaiNiem {id: 'KN008'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Cấp GPMT theo thẩm quyền huyện', dieu_khoan: 'Điều 168, Khoản 2b'}]->(k);

// UBND cấp xã có thẩm quyền
MATCH (cq:CoQuan {id: 'CQ007'}), (k:KhaiNiem {id: 'KN009'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Tiếp nhận đăng ký môi trường', dieu_khoan: 'Điều 168, Khoản 3b'}]->(k);

MATCH (cq:CoQuan {id: 'CQ007'}), (k:KhaiNiem {id: 'KN022'})
CREATE (cq)-[:CO_THAM_QUYEN {noi_dung: 'Kiểm soát nguồn ô nhiễm', dieu_khoan: 'Điều 168, Khoản 3b'}]->(k);

// --- 12.10 QUAN HỆ CHỦ THỂ - NGHĨA VỤ ---

// Chủ dự án Nhóm I phải thực hiện PEIA
MATCH (ct:ChuThe {id: 'CT003'}), (k:KhaiNiem {id: 'KN006'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phải thực hiện đánh giá sơ bộ tác động môi trường', dieu_khoan: 'Điều 29, Khoản 1', dieu_kien: 'Dự án thuộc Nhóm I', thoi_diem: 'Giai đoạn nghiên cứu tiền khả thi'}]->(k);

// Chủ dự án phải có GPMT trước vận hành
MATCH (ct:ChuThe {id: 'CT003'}), (k:KhaiNiem {id: 'KN008'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phải có Giấy phép môi trường trước khi vận hành thử nghiệm', dieu_khoan: 'Điều 42, Khoản 2a', dieu_kien: 'Dự án thuộc đối tượng ĐTM'}]->(k);

// Hộ gia đình phải phân loại rác
MATCH (ct:ChuThe {id: 'CT005'}), (k:KhaiNiem {id: 'KN019'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phải phân loại chất thải rắn sinh hoạt tại nguồn', dieu_khoan: 'Điều 60, Khoản 1a; Điều 75, Khoản 1', thoi_han: 'Chậm nhất ngày 31/12/2024'}]->(k);

// Cơ sở phát thải KNK phải kiểm kê
MATCH (ct:ChuThe {id: 'CT011'}), (k:KhaiNiem {id: 'KN029'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Tổ chức thực hiện kiểm kê khí nhà kính', dieu_khoan: 'Điều 91, Khoản 7a', dinh_ky: '02 năm một lần'}]->(k);

// Nhà sản xuất phải tái chế (EPR)
MATCH (ct:ChuThe {id: 'CT010'}), (k:KhaiNiem {id: 'KN045'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phải thực hiện tái chế theo tỷ lệ và quy cách bắt buộc', dieu_khoan: 'Điều 54, Khoản 1', ghi_chu: 'Trách nhiệm mở rộng của nhà sản xuất (EPR)'}]->(k);

// Chủ nguồn thải CTNH phải phân loại
MATCH (ct:ChuThe {id: 'CT008'}), (k:KhaiNiem {id: 'KN020'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phân định, phân loại, thu gom, lưu giữ riêng chất thải nguy hại', dieu_khoan: 'Điều 83, Khoản 1b'}]->(k);

// Cơ sở xử lý CTNH phải có GPMT
MATCH (ct:ChuThe {id: 'CT009'}), (k:KhaiNiem {id: 'KN008'})
CREATE (ct)-[:CO_NGHIA_VU {noi_dung: 'Phải có giấy phép môi trường', dieu_khoan: 'Điều 84, Khoản 3d'}]->(k);

// --- 12.11 QUAN HỆ CHỦ THỂ - QUYỀN ---

// Cộng đồng có quyền giám sát
MATCH (ct:ChuThe {id: 'CT006'}), (k:KhaiNiem {id: 'KN014'})
CREATE (ct)-[:CO_QUYEN {noi_dung: 'Được thông báo về nguy cơ sự cố và tham gia giám sát', dieu_khoan: 'Điều 129, Khoản 1'}]->(k);

// Cộng đồng có quyền yêu cầu thông tin
MATCH (ct:ChuThe {id: 'CT006'}), (k:KhaiNiem {id: 'KN025'})
CREATE (ct)-[:CO_QUYEN {noi_dung: 'Yêu cầu cung cấp thông tin về môi trường', dieu_khoan: 'Điều 159, Khoản 1'}]->(k);

// Cơ sở phát thải có quyền trao đổi các-bon
MATCH (ct:ChuThe {id: 'CT011'}), (k:KhaiNiem {id: 'KN035'})
CREATE (ct)-[:CO_QUYEN {noi_dung: 'Được phân bổ hạn ngạch và trao đổi tín chỉ các-bon', dieu_khoan: 'Điều 139, Khoản 2, 5'}]->(k);

// --- 12.12 QUAN HỆ KINH TẾ MÔI TRƯỜNG ---

// Kinh tế tuần hoàn giúp giảm chất thải
MATCH (a:KhaiNiem {id: 'KN045'}), (b:KhaiNiem {id: 'KN018'})
CREATE (a)-[:GIAM_THIEU {dieu_khoan: 'Điều 142, Khoản 1'}]->(b);

// Tín dụng xanh hỗ trợ ứng phó BĐKH
MATCH (a:KhaiNiem {id: 'KN052'}), (b:KhaiNiem {id: 'KN032'})
CREATE (a)-[:HO_TRO {dieu_khoan: 'Điều 149, Khoản 1'}]->(b);

// Trái phiếu xanh huy động vốn cho BVMT
MATCH (a:KhaiNiem {id: 'KN053'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:HUY_DONG_VON_CHO {dieu_khoan: 'Điều 150, Khoản 1'}]->(b);

// Thị trường các-bon giao dịch hạn ngạch và tín chỉ
MATCH (a:KhaiNiem {id: 'KN044'}), (b:KhaiNiem {id: 'KN033'})
CREATE (a)-[:GIAO_DICH {dieu_khoan: 'Điều 139, Khoản 1'}]->(b);

MATCH (a:KhaiNiem {id: 'KN044'}), (b:KhaiNiem {id: 'KN035'})
CREATE (a)-[:GIAO_DICH {dieu_khoan: 'Điều 139, Khoản 1'}]->(b);

// Nhãn sinh thái chứng nhận sản phẩm thân thiện
MATCH (a:KhaiNiem {id: 'KN049'}), (b:KhaiNiem {id: 'KN048'})
CREATE (a)-[:CHUNG_NHAN {dieu_khoan: 'Điều 145, Khoản 2'}]->(b);

// Mua sắm xanh ưu tiên sản phẩm thân thiện
MATCH (a:KhaiNiem {id: 'KN050'}), (b:KhaiNiem {id: 'KN048'})
CREATE (a)-[:UU_TIEN {dieu_khoan: 'Điều 146, Khoản 1'}]->(b);

// Quỹ BVMT hỗ trợ hoạt động BVMT
MATCH (a:KhaiNiem {id: 'KN054'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:HO_TRO_TAI_CHINH {dieu_khoan: 'Điều 151, Khoản 1'}]->(b);

// Vốn tự nhiên bao gồm dịch vụ hệ sinh thái
MATCH (a:KhaiNiem {id: 'KN051'}), (b:KhaiNiem {id: 'KN043'})
CREATE (a)-[:BAO_GOM {dieu_khoan: 'Điều 147, Khoản 1'}]->(b);

// --- 12.13 QUAN HỆ CƠ QUAN - TRÁCH NHIỆM ---

// Chính phủ quản lý thống nhất
MATCH (cq:CoQuan {id: 'CQ001'}), (k:KhaiNiem {id: 'KN002'})
CREATE (cq)-[:QUAN_LY_THONG_NHAT {dieu_khoan: 'Điều 165, Khoản 1'}]->(k);

// Bộ TN&MT xây dựng quy hoạch
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN004'})
CREATE (cq)-[:XAY_DUNG {dieu_khoan: 'Điều 166, Khoản 1'}]->(k);

// UBND cấp tỉnh chịu trách nhiệm về ô nhiễm
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN012'})
CREATE (cq)-[:CHIU_TRACH_NHIEM {noi_dung: 'Chịu trách nhiệm trước Chính phủ về việc để xảy ra ô nhiễm', dieu_khoan: 'Điều 168, Khoản 1d'}]->(k);

// UBND cấp huyện chịu trách nhiệm
MATCH (cq:CoQuan {id: 'CQ006'}), (k:KhaiNiem {id: 'KN012'})
CREATE (cq)-[:CHIU_TRACH_NHIEM {noi_dung: 'Chịu trách nhiệm trước UBND cấp tỉnh về việc để xảy ra ô nhiễm', dieu_khoan: 'Điều 168, Khoản 2c'}]->(k);

// UBND cấp xã hướng dẫn phân loại rác
MATCH (cq:CoQuan {id: 'CQ007'}), (k:KhaiNiem {id: 'KN019'})
CREATE (cq)-[:HUONG_DAN {noi_dung: 'Hướng dẫn hộ gia đình, cá nhân phân loại và chuyển giao chất thải', dieu_khoan: 'Điều 77, Khoản 7c'}]->(k);

// --- 12.14 QUAN HỆ THỦ TỤC - CƠ QUAN ---

MATCH (t:ThuTuc {id: 'TT001'}), (cq:CoQuan {id: 'CQ002'})
CREATE (cq)-[:THUC_HIEN]->(t);

MATCH (t:ThuTuc {id: 'TT002'}), (cq:CoQuan {id: 'CQ005'})
CREATE (cq)-[:THUC_HIEN]->(t);

MATCH (t:ThuTuc {id: 'TT003'}), (cq:CoQuan {id: 'CQ002'})
CREATE (cq)-[:THUC_HIEN]->(t);

MATCH (t:ThuTuc {id: 'TT004'}), (cq:CoQuan {id: 'CQ005'})
CREATE (cq)-[:THUC_HIEN]->(t);

MATCH (t:ThuTuc {id: 'TT005'}), (cq:CoQuan {id: 'CQ006'})
CREATE (cq)-[:THUC_HIEN]->(t);

MATCH (t:ThuTuc {id: 'TT006'}), (cq:CoQuan {id: 'CQ007'})
CREATE (cq)-[:THUC_HIEN]->(t);

// --- 12.15 QUAN HỆ VĂN BẢN ---

// Báo cáo ĐTM là sản phẩm của giai đoạn lập ĐTM
MATCH (g:GiaiDoan {id: 'GD003'}), (v:VanBan {id: 'VB001'})
CREATE (g)-[:TAO_RA]->(v);

// Quyết định phê duyệt là căn cứ cấp GPMT
MATCH (v:VanBan {id: 'VB002'}), (v2:VanBan {id: 'VB003'})
CREATE (v)-[:CAN_CU_DE_CAP {dieu_khoan: 'Điều 36, Khoản 1'}]->(v2);

// Giai đoạn phê duyệt tạo ra Quyết định
MATCH (g:GiaiDoan {id: 'GD006'}), (v:VanBan {id: 'VB002'})
CREATE (g)-[:TAO_RA]->(v);

// =============================================================================
// PHẦN 13: CÁC TRUY VẤN MẪU (SAMPLE QUERIES)
// =============================================================================

// --- Query 1: Tìm tất cả nghĩa vụ của Chủ dự án đầu tư ---
// MATCH (ct:ChuThe {ten: 'Chủ dự án đầu tư'})-[r:CO_NGHIA_VU]->(k:KhaiNiem)
// RETURN ct.ten AS chu_the, r.noi_dung AS nghia_vu, k.ten AS doi_tuong, r.dieu_khoan AS can_cu;

// --- Query 2: Tìm thủ tục cần thiết cho dự án Nhóm I ---
// MATCH (d:DuAn {nhom: 'I'})-[r:YEU_CAU]->(k:KhaiNiem)
// RETURN d.ten AS du_an, k.ten AS thu_tuc, r.bat_buoc AS bat_buoc, r.dieu_khoan AS can_cu;

// --- Query 3: Tìm hành vi bị cấm và chế tài tương ứng ---
// MATCH (h:HanhVi {trang_thai: 'cam'})-[r:DAN_DEN]->(ct:CheTai)
// RETURN h.ten AS hanh_vi, h.dieu_khoan AS can_cu, ct.ten AS che_tai, ct.loai AS loai_che_tai;

// --- Query 4: Tìm cơ quan có thẩm quyền về Giấy phép môi trường ---
// MATCH (cq:CoQuan)-[r:CO_THAM_QUYEN]->(k:KhaiNiem {ten: 'Giấy phép môi trường'})
// RETURN cq.ten AS co_quan, cq.cap AS cap, r.noi_dung AS tham_quyen;

// --- Query 5: Tìm quy trình ĐTM theo thứ tự ---
// MATCH (g:GiaiDoan)
// RETURN g.ten AS giai_doan, g.thu_tu AS thu_tu, g.mo_ta AS mo_ta, g.thoi_han AS thoi_han
// ORDER BY g.thu_tu;

// --- Query 6: Tìm quan hệ giữa các khái niệm về chất thải ---
// MATCH (k1:KhaiNiem)-[r]->(k2:KhaiNiem)
// WHERE k1.ten CONTAINS 'Chất thải' OR k2.ten CONTAINS 'Chất thải'
// RETURN k1.ten AS khai_niem_1, type(r) AS quan_he, k2.ten AS khai_niem_2;

// --- Query 7: Tìm yếu tố nhạy cảm ảnh hưởng đến phân loại dự án ---
// MATCH (d:DuAn)-[r:LIEN_QUAN_YEU_TO]->(y:YeuToNhayCam)
// RETURN d.ten AS du_an, d.nhom AS nhom, collect(y.ten) AS yeu_to_nhay_cam;

// --- Query 8: Tìm đường đi từ hành vi vi phạm đến chế tài ---
// MATCH path = (ct:ChuThe)-[:BI_CAM]->(h:HanhVi)-[:DAN_DEN]->(cht:CheTai)
// RETURN ct.ten AS chu_the, h.ten AS hanh_vi, cht.ten AS che_tai;

// --- Query 9: Tìm tất cả quan hệ của Giấy phép môi trường ---
// MATCH (n)-[r]-(k:KhaiNiem {ten: 'Giấy phép môi trường'})
// RETURN labels(n)[0] AS loai_node, n.ten AS ten, type(r) AS quan_he, r.dieu_khoan AS can_cu;

// --- Query 10: Thống kê số lượng nodes theo loại ---
// MATCH (n)
// RETURN labels(n)[0] AS loai, count(n) AS so_luong
// ORDER BY so_luong DESC;

// --- Query 11: Tìm chuỗi quan hệ: Dự án -> Thủ tục -> Cơ quan thẩm quyền ---
// MATCH (d:DuAn)-[:YEU_CAU]->(k:KhaiNiem)<-[:CO_THAM_QUYEN]-(cq:CoQuan)
// RETURN d.ten AS du_an, k.ten AS thu_tuc, cq.ten AS co_quan_tham_quyen;

// --- Query 12: Tìm tất cả quyền của cộng đồng dân cư ---
// MATCH (ct:ChuThe {ten: 'Cộng đồng dân cư'})-[r:CO_QUYEN]->(k:KhaiNiem)
// RETURN r.noi_dung AS quyen, k.ten AS doi_tuong, r.dieu_khoan AS can_cu;

// --- Query 13: Phân tích quan hệ kinh tế môi trường ---
// MATCH (k1:KhaiNiem)-[r]->(k2:KhaiNiem)
// WHERE k1.chuong = 'XI' OR k2.chuong = 'XI'
// RETURN k1.ten, type(r), k2.ten, r.dieu_khoan;

// =============================================================================
// END OF SCRIPT
// =============================================================================
// =============================================================================
// KNOWLEDGE GRAPH - LUẬT BẢO VỆ MÔI TRƯỜNG VIỆT NAM 2020
// PHẦN MỞ RỘNG: CÁC MỐI QUAN HỆ SUY LUẬN
// =============================================================================

// =============================================================================
// PHẦN A: BỔ SUNG THÊM NODES MỚI
// =============================================================================

// --- A1: Thêm các Chủ thể cụ thể hơn ---
CREATE (ct013:ChuThe {id: 'CT013', ten: 'Bệnh viện cơ sở y tế', loai: 'phap_nhan', mo_ta: 'Bệnh viện, cơ sở y tế có phát sinh chất thải y tế lây nhiễm'});
CREATE (ct014:ChuThe {id: 'CT014', ten: 'Cơ sở khai thác khoáng sản', loai: 'phap_nhan', mo_ta: 'Tổ chức thăm dò, khai thác, chế biến khoáng sản'});
CREATE (ct015:ChuThe {id: 'CT015', ten: 'Chủ đầu tư hạ tầng KCN', loai: 'phap_nhan', mo_ta: 'Chủ đầu tư xây dựng, kinh doanh hạ tầng khu công nghiệp, cụm công nghiệp'});
CREATE (ct016:ChuThe {id: 'CT016', ten: 'Tổ chức chính trị xã hội', loai: 'to_chuc', mo_ta: 'Tổ chức chính trị - xã hội, tổ chức xã hội - nghề nghiệp'});
CREATE (ct017:ChuThe {id: 'CT017', ten: 'Bên gây thiệt hại môi trường', loai: 'phap_nhan', mo_ta: 'Tổ chức, cá nhân gây ô nhiễm môi trường, thiệt hại về môi trường'});

// --- A2: Thêm các Hành vi được phép/bắt buộc ---
CREATE (hv015:HanhVi {id: 'HV015', ten: 'Phân loại chất thải tại nguồn', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 75, Khoản 1', mo_ta: 'Phân loại chất thải rắn sinh hoạt tại nguồn thành các loại theo quy định'});
CREATE (hv016:HanhVi {id: 'HV016', ten: 'Chi trả dịch vụ thu gom xử lý chất thải', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 79, Khoản 1b', mo_ta: 'Chi trả giá dịch vụ thu gom, vận chuyển và xử lý chất thải theo khối lượng hoặc thể tích'});
CREATE (hv017:HanhVi {id: 'HV017', ten: 'Kiểm kê khí nhà kính', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 91, Khoản 7a', mo_ta: 'Tổ chức thực hiện kiểm kê khí nhà kính định kỳ 02 năm một lần'});
CREATE (hv018:HanhVi {id: 'HV018', ten: 'Ký quỹ bảo vệ môi trường', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 137, Khoản 2c', mo_ta: 'Ký quỹ trước khi nhập khẩu phế liệu hoặc khai thác khoáng sản'});
CREATE (hv019:HanhVi {id: 'HV019', ten: 'Quan trắc môi trường tự động', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 111, Khoản 1', mo_ta: 'Quan trắc nước thải, khí thải tự động, liên tục và truyền dữ liệu'});
CREATE (hv020:HanhVi {id: 'HV020', ten: 'Công khai thông tin môi trường', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 47, Khoản 2đ', mo_ta: 'Công khai Giấy phép môi trường và báo cáo ĐTM đã được phê duyệt'});
CREATE (hv021:HanhVi {id: 'HV021', ten: 'Tái chế sản phẩm bao bì', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 54, Khoản 1', mo_ta: 'Thực hiện tái chế theo tỷ lệ và quy cách tái chế bắt buộc (EPR)'});
CREATE (hv022:HanhVi {id: 'HV022', ten: 'Phục hồi môi trường sau sự cố', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 126, Khoản 1', mo_ta: 'Thực hiện phục hồi môi trường sau sự cố môi trường'});
CREATE (hv023:HanhVi {id: 'HV023', ten: 'Bồi thường thiệt hại môi trường', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 130, Khoản 2', mo_ta: 'Bồi thường toàn bộ thiệt hại và chi trả chi phí xác định thiệt hại'});
CREATE (hv024:HanhVi {id: 'HV024', ten: 'Áp dụng kỹ thuật hiện có tốt nhất', trang_thai: 'bat_buoc', dieu_khoan: 'Điều 105, Khoản 1', mo_ta: 'Nghiên cứu, áp dụng BAT theo lộ trình'});

// --- A3: Thêm các Khái niệm bổ sung ---
CREATE (kn055:KhaiNiem {id: 'KN055', ten: 'Chất thải y tế lây nhiễm', dieu_khoan: 'Điều 62, Khoản 1', chuong: 'V', noi_dung: 'Chất thải y tế có chứa mầm bệnh có khả năng lây nhiễm', keyphrase: 'chất thải y tế, lây nhiễm, mầm bệnh'});
CREATE (kn056:KhaiNiem {id: 'KN056', ten: 'Trách nhiệm mở rộng của nhà sản xuất', viet_tat: 'EPR', dieu_khoan: 'Điều 54, Khoản 1', chuong: 'V', noi_dung: 'Trách nhiệm của nhà sản xuất, nhập khẩu trong việc thu hồi, tái chế sản phẩm, bao bì', keyphrase: 'trách nhiệm nhà sản xuất, tái chế, thu hồi'});
CREATE (kn057:KhaiNiem {id: 'KN057', ten: 'Phục hồi môi trường', dieu_khoan: 'Điều 126, Khoản 1', chuong: 'X', noi_dung: 'Các hoạt động khắc phục, cải tạo để đưa môi trường về trạng thái ban đầu hoặc mức chấp nhận được', keyphrase: 'khắc phục, cải tạo, phục hồi'});
CREATE (kn058:KhaiNiem {id: 'KN058', ten: 'Chất làm suy giảm tầng ô-dôn', viet_tat: 'ODS', dieu_khoan: 'Điều 92, Khoản 1', chuong: 'VII', noi_dung: 'Các chất được quy định trong Nghị định thư Montreal có khả năng làm suy giảm tầng ô-dôn', keyphrase: 'ODS, Montreal, suy giảm ô-dôn'});

// =============================================================================
// PHẦN B: QUAN HỆ GIỮA CÁC KHÁI NIỆM (SUY LUẬN TỪ NỘI DUNG)
// =============================================================================

// --- B1: Quan hệ phân cấp/bao hàm khái niệm ---

// Chất thải y tế là loại chất thải nguy hại
MATCH (a:KhaiNiem {id: 'KN055'}), (b:KhaiNiem {id: 'KN020'})
CREATE (a)-[:LA_LOAI {suy_luan: true, giai_thich: 'Chất thải y tế lây nhiễm có đặc tính nguy hại theo Điều 3 Khoản 20'}]->(b);

// Chất làm suy giảm ô-dôn liên quan đến khí nhà kính
MATCH (a:KhaiNiem {id: 'KN058'}), (b:KhaiNiem {id: 'KN029'})
CREATE (a)-[:LIEN_QUAN {suy_luan: true, giai_thich: 'Nhiều ODS cũng là khí nhà kính mạnh'}]->(b);

// EPR thuộc về Kinh tế tuần hoàn
MATCH (a:KhaiNiem {id: 'KN056'}), (b:KhaiNiem {id: 'KN045'})
CREATE (a)-[:THANH_PHAN_CUA {suy_luan: true, giai_thich: 'EPR là công cụ thúc đẩy kinh tế tuần hoàn'}]->(b);

// Phục hồi môi trường là hoạt động BVMT
MATCH (a:KhaiNiem {id: 'KN057'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:LA_LOAI {suy_luan: true, giai_thich: 'Phục hồi môi trường thuộc hoạt động khắc phục trong BVMT'}]->(b);

// --- B2: Quan hệ nhân quả mở rộng ---

// Chất ô nhiễm vượt ngưỡng -> Ô nhiễm môi trường
MATCH (a:KhaiNiem {id: 'KN015'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:GAY_RA_KHI_VUOT_NGUONG {suy_luan: true, dieu_khoan: 'Điều 3, Khoản 15', giai_thich: 'Khi xuất hiện trong môi trường vượt mức cho phép sẽ gây ô nhiễm'}]->(b);

// Khí nhà kính -> Biến đổi khí hậu (ngầm định)
MATCH (a:KhaiNiem {id: 'KN029'}), (b:KhaiNiem {id: 'KN032'})
CREATE (a)-[:GAY_RA {suy_luan: true, giai_thich: 'Khí nhà kính gây hiệu ứng nhà kính dẫn đến biến đổi khí hậu'}]->(b);

// Kinh tế tuần hoàn -> Giảm khí nhà kính
MATCH (a:KhaiNiem {id: 'KN045'}), (b:KhaiNiem {id: 'KN031'})
CREATE (a)-[:HO_TRO {suy_luan: true, giai_thich: 'Giảm khai thác, kéo dài vòng đời sản phẩm giúp giảm phát thải'}]->(b);

// Thiệt hại môi trường -> cần Phục hồi
MATCH (a:KhaiNiem {id: 'KN042'}), (b:KhaiNiem {id: 'KN057'})
CREATE (a)-[:YEU_CAU {suy_luan: true, giai_thich: 'Thiệt hại môi trường đòi hỏi phải phục hồi môi trường'}]->(b);

// ODS -> Suy giảm tầng ô-dôn
MATCH (a:KhaiNiem {id: 'KN058'}), (b:KhaiNiem {id: 'KN034'})
CREATE (a)-[:GAY_SUY_GIAM {suy_luan: true, dieu_khoan: 'Điều 92, Khoản 1'}]->(b);

// --- B3: Quan hệ tiền đề - hậu quả (prerequisite) ---

// Không có GPMT -> Không được vận hành
MATCH (a:KhaiNiem {id: 'KN008'}), (b:HanhVi {id: 'HV005'})
CREATE (a)-[:THIEU_SE_VI_PHAM {suy_luan: true, dieu_khoan: 'Điều 6, Khoản 5', giai_thich: 'Thiếu GPMT khi vận hành là hành vi bị cấm'}]->(b);

// Quan trắc môi trường -> Phát hiện ô nhiễm
MATCH (a:KhaiNiem {id: 'KN025'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:PHAT_HIEN {suy_luan: true, giai_thich: 'Quan trắc giúp theo dõi và phát hiện ô nhiễm môi trường'}]->(b);

// ĐTM -> Dự báo tác động
MATCH (a:KhaiNiem {id: 'KN007'}), (b:KhaiNiem {id: 'KN014'})
CREATE (a)-[:DU_BAO {suy_luan: true, giai_thich: 'ĐTM dự báo các tác động có thể dẫn đến sự cố môi trường'}]->(b);

// --- B4: Quan hệ công cụ - mục tiêu ---

// Quy chuẩn kỹ thuật -> Kiểm soát ô nhiễm
MATCH (a:KhaiNiem {id: 'KN010'}), (b:KhaiNiem {id: 'KN022'})
CREATE (a)-[:CONG_CU_CHO {suy_luan: true, giai_thich: 'QCKTMT là công cụ để kiểm soát ô nhiễm'}]->(b);

// BAT -> Giảm thiểu tác động
MATCH (a:KhaiNiem {id: 'KN036'}), (b:KhaiNiem {id: 'KN012'})
CREATE (a)-[:GIAM_THIEU {suy_luan: true, dieu_khoan: 'Điều 3, Khoản 36', giai_thich: 'BAT giúp phòng ngừa, kiểm soát ô nhiễm'}]->(b);

// Kiểm toán môi trường -> Đánh giá hiệu quả quản lý
MATCH (a:KhaiNiem {id: 'KN040'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:DANH_GIA {suy_luan: true, dieu_khoan: 'Điều 74, Khoản 1', giai_thich: 'Kiểm toán đánh giá hiệu quả hoạt động BVMT'}]->(b);

// =============================================================================
// PHẦN C: QUAN HỆ CHỦ THỂ - HÀNH VI CHI TIẾT
// =============================================================================

// --- C1: Nghĩa vụ của Hộ gia đình ---

// Hộ gia đình phải phân loại rác
MATCH (c:ChuThe {id: 'CT005'}), (h:HanhVi {id: 'HV015'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 75, Khoản 1', thoi_han: '31/12/2024', mo_ta: 'Phân loại chất thải rắn sinh hoạt tại nguồn'}]->(h);

// Hộ gia đình phải chi trả dịch vụ
MATCH (c:ChuThe {id: 'CT005'}), (h:HanhVi {id: 'HV016'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 79, Khoản 1b', mo_ta: 'Chi trả theo khối lượng hoặc thể tích đã phân loại'}]->(h);

// --- C2: Nghĩa vụ của Cơ sở phát thải KNK ---

// Cơ sở phát thải KNK phải kiểm kê
MATCH (c:ChuThe {id: 'CT011'}), (h:HanhVi {id: 'HV017'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 91, Khoản 7a', dinh_ky: '02 năm', han_nop: 'trước 01/12'}]->(h);

// --- C3: Nghĩa vụ của Nhà sản xuất nhập khẩu ---

// NSX phải tái chế (EPR)
MATCH (c:ChuThe {id: 'CT010'}), (h:HanhVi {id: 'HV021'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 54, Khoản 1', mo_ta: 'Tái chế theo tỷ lệ bắt buộc hoặc đóng góp tài chính vào Quỹ BVMT'}]->(h);

// NSX nhập phế liệu phải ký quỹ
MATCH (c:ChuThe {id: 'CT010'}), (h:HanhVi {id: 'HV018'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 71, Khoản 2c; Điều 137', thoi_diem: 'Trước khi dỡ hàng xuống cảng'}]->(h);

// --- C4: Nghĩa vụ của Chủ dự án ---

// Chủ dự án phải quan trắc tự động
MATCH (c:ChuThe {id: 'CT003'}), (h:HanhVi {id: 'HV019'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 111, Khoản 1', dieu_kien: 'Lưu lượng xả thải trung bình/lớn', mo_ta: 'Quan trắc và truyền dữ liệu đến cơ quan chuyên môn cấp tỉnh'}]->(h);

// Chủ dự án phải công khai thông tin
MATCH (c:ChuThe {id: 'CT003'}), (h:HanhVi {id: 'HV020'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 47, Khoản 2đ; Điều 37, Khoản 5', mo_ta: 'Công khai trừ bí mật nhà nước, doanh nghiệp'}]->(h);

// Chủ dự án phải áp dụng BAT
MATCH (c:ChuThe {id: 'CT003'}), (h:HanhVi {id: 'HV024'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 105, Khoản 1', dieu_kien: 'Thuộc loại hình có nguy cơ gây ô nhiễm', mo_ta: 'Theo lộ trình do Chính phủ quy định'}]->(h);

// --- C5: Trách nhiệm khi gây thiệt hại ---

// Bên gây thiệt hại phải bồi thường
MATCH (c:ChuThe {id: 'CT017'}), (h:HanhVi {id: 'HV023'})
CREATE (c)-[:CO_TRACH_NHIEM {dieu_khoan: 'Điều 130, Khoản 2', mo_ta: 'Bồi thường toàn bộ thiệt hại và chi trả chi phí xác định thiệt hại'}]->(h);

// Bên gây thiệt hại phải phục hồi môi trường
MATCH (c:ChuThe {id: 'CT017'}), (h:HanhVi {id: 'HV022'})
CREATE (c)-[:CO_TRACH_NHIEM {dieu_khoan: 'Điều 126, Khoản 1', mo_ta: 'Phục hồi môi trường trong phạm vi cơ sở'}]->(h);

// --- C6: Nghĩa vụ đặc thù ngành ---

// Bệnh viện phải xử lý chất thải y tế
MATCH (c:ChuThe {id: 'CT013'}), (k:KhaiNiem {id: 'KN055'})
CREATE (c)-[:CO_NGHIA_VU_XU_LY {dieu_khoan: 'Điều 62, Khoản 1', mo_ta: 'Xử lý nước thải y tế, phân loại CTNH, ưu tiên công nghệ không đốt'}]->(k);

// Cơ sở khai thác khoáng sản phải ký quỹ
MATCH (c:ChuThe {id: 'CT014'}), (h:HanhVi {id: 'HV018'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 67, Khoản 1', thoi_diem: 'Trước khi khai thác'}]->(h);

// Cơ sở khai thác khoáng sản phải phục hồi
MATCH (c:ChuThe {id: 'CT014'}), (h:HanhVi {id: 'HV022'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 67, Khoản 1', mo_ta: 'Cải tạo, phục hồi môi trường sau khai thác'}]->(h);

// =============================================================================
// PHẦN D: QUAN HỆ CHỦ THỂ - QUYỀN LỢI
// =============================================================================

// --- D1: Quyền miễn trừ ---

// Hộ gia đình phân loại tốt được miễn phí
MATCH (c:ChuThe {id: 'CT005'}), (h:HanhVi {id: 'HV016'})
CREATE (c)-[:DUOC_MIEN {dieu_khoan: 'Điều 79, Khoản 1c', dieu_kien: 'Chất thải có khả năng tái chế đã được phân loại riêng', mo_ta: 'Miễn chi trả giá dịch vụ'}]->(h);

// Dự án khẩn cấp được miễn GPMT
MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN008'})
CREATE (d)-[:DUOC_MIEN {dieu_khoan: 'Điều 39, Khoản 3', dieu_kien: 'Dự án đầu tư công khẩn cấp'}]->(k);

// --- D2: Quyền của Cộng đồng ---

// Cộng đồng có quyền yêu cầu thông tin
MATCH (c:ChuThe {id: 'CT006'}), (h:HanhVi {id: 'HV020'})
CREATE (c)-[:CO_QUYEN_YEU_CAU {dieu_khoan: 'Điều 159, Khoản 1', mo_ta: 'Yêu cầu cung cấp thông tin môi trường, tìm hiểu thực tế'}]->(h);

// Cộng đồng có quyền giám sát
MATCH (c:ChuThe {id: 'CT006'}), (k:KhaiNiem {id: 'KN002'})
CREATE (c)-[:CO_QUYEN_GIAM_SAT {dieu_khoan: 'Điều 158, Khoản 2d; Điều 129, Khoản 1', mo_ta: 'Tham gia giám sát hoạt động BVMT'}]->(k);

// --- D3: Quyền của Cơ sở phát thải KNK ---

// Được trao đổi hạn ngạch và tín chỉ
MATCH (c:ChuThe {id: 'CT011'}), (k:KhaiNiem {id: 'KN044'})
CREATE (c)-[:CO_QUYEN_THAM_GIA {dieu_khoan: 'Điều 139, Khoản 2, 5', mo_ta: 'Được phân bổ hạn ngạch và trao đổi trên thị trường các-bon'}]->(k);

// --- D4: Quyền của Tổ chức chính trị xã hội ---

// Được tham gia kiểm tra
MATCH (c:ChuThe {id: 'CT016'}), (k:KhaiNiem {id: 'KN022'})
CREATE (c)-[:CO_QUYEN_THAM_GIA {dieu_khoan: 'Điều 158, Khoản 2d', mo_ta: 'Tham gia hoạt động kiểm tra, giám sát về BVMT'}]->(k);

// =============================================================================
// PHẦN E: QUAN HỆ CƠ QUAN - TRÁCH NHIỆM CHI TIẾT
// =============================================================================

// --- E1: Bộ TN&MT ---

// Tổ chức thị trường các-bon
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN044'})
CREATE (cq)-[:TO_CHUC_VAN_HANH {dieu_khoan: 'Điều 139, Khoản 10', mo_ta: 'Tổ chức phân bổ hạn ngạch và vận hành thị trường'}]->(k);

// Quản lý ODS
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN058'})
CREATE (cq)-[:QUAN_LY {dieu_khoan: 'Điều 92', mo_ta: 'Quản lý, kiểm soát chất làm suy giảm tầng ô-dôn'}]->(k);

// Xây dựng lộ trình BAT
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN036'})
CREATE (cq)-[:XAY_DUNG_LO_TRINH {dieu_khoan: 'Điều 105, Khoản 1', mo_ta: 'Ban hành hướng dẫn kỹ thuật về BAT'}]->(k);

// Kiểm kê vốn tự nhiên
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN051'})
CREATE (cq)-[:KIEM_KE_DANH_GIA {dieu_khoan: 'Điều 147, Khoản 4', mo_ta: 'Kiểm kê, đánh giá vốn tự nhiên'}]->(k);

// --- E2: UBND cấp tỉnh ---

// Quy định giá dịch vụ xử lý chất thải
MATCH (cq:CoQuan {id: 'CQ005'}), (h:HanhVi {id: 'HV016'})
CREATE (cq)-[:QUY_DINH_GIA {dieu_khoan: 'Điều 79, Khoản 1', mo_ta: 'Ban hành đơn giá dịch vụ thu gom, vận chuyển, xử lý chất thải'}]->(h);

// Ban hành QCKT địa phương
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN010'})
CREATE (cq)-[:BAN_HANH_DIA_PHUONG {dieu_khoan: 'Điều 102, Khoản 5', dieu_kien: 'Nghiêm ngặt hơn QCKT quốc gia', thoi_han: '02 năm kể từ ngày ban hành QCKT quốc gia'}]->(k);

// Yêu cầu di dời cơ sở ô nhiễm
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN012'})
CREATE (cq)-[:YEU_CAU_DI_DOI {dieu_khoan: 'Điều 53, Khoản 2', dieu_kien: 'Cơ sở có nguy cơ gây ô nhiễm trong khu dân cư'}]->(k);

// --- E3: UBND cấp xã ---

// Hướng dẫn phân loại rác
MATCH (cq:CoQuan {id: 'CQ007'}), (h:HanhVi {id: 'HV015'})
CREATE (cq)-[:HUONG_DAN {dieu_khoan: 'Điều 77, Khoản 7c', mo_ta: 'Hướng dẫn hộ gia đình phân loại và chuyển giao chất thải'}]->(h);

// --- E4: Quỹ BVMT ---

// Nhận ký quỹ
MATCH (cq:CoQuan {id: 'CQ008'}), (h:HanhVi {id: 'HV018'})
CREATE (cq)-[:NHAN_KY_QUY {dieu_khoan: 'Điều 137, Khoản 2c', mo_ta: 'Nhận ký quỹ từ cơ sở nhập khẩu phế liệu, khai thác khoáng sản'}]->(h);

// Nhận đóng góp EPR
MATCH (cq:CoQuan {id: 'CQ008'}), (k:KhaiNiem {id: 'KN056'})
CREATE (cq)-[:NHAN_DONG_GOP {dieu_khoan: 'Điều 54, Khoản 2b', mo_ta: 'Nhận đóng góp tài chính từ nhà sản xuất, nhập khẩu để hỗ trợ tái chế'}]->(k);

// =============================================================================
// PHẦN F: QUAN HỆ LOGIC VỀ HẬU QUẢ PHÁP LÝ
// =============================================================================

// --- F1: Vi phạm -> Chế tài ---

// Không phân loại rác -> Bị từ chối thu gom
MATCH (h:HanhVi {id: 'HV015'}), (ct:CheTai {id: 'CHT002'})
CREATE (h)-[:KHONG_THUC_HIEN_SE {dieu_khoan: 'Điều 75, Khoản 1', hau_qua: 'Cơ sở thu gom có quyền từ chối', suy_luan: true}]->(ct);

// Không kiểm kê KNK -> Bị kiểm tra
MATCH (h:HanhVi {id: 'HV017'}), (ct:CheTai {id: 'CHT002'})
CREATE (h)-[:KHONG_THUC_HIEN_SE {dieu_khoan: 'Điều 91, Khoản 7a', hau_qua: 'Bị kiểm tra việc tuân thủ', suy_luan: true}]->(ct);

// Vi phạm GPMT -> Thu hồi GPMT
MATCH (h:HanhVi {id: 'HV005'}), (ct:CheTai {id: 'CHT005'})
CREATE (h)-[:DAN_DEN {dieu_khoan: 'Điều 47, Khoản 2a', suy_luan: true}]->(ct);

// Gây thiệt hại -> Phải bồi thường
MATCH (k:KhaiNiem {id: 'KN042'}), (ct:CheTai {id: 'CHT004'})
CREATE (k)-[:YEU_CAU {dieu_khoan: 'Điều 130, Khoản 2', suy_luan: true}]->(ct);

// --- F2: Quan hệ chứng minh pháp lý ---

// Bên gây thiệt hại phải chứng minh nhân quả
MATCH (ct:ChuThe {id: 'CT017'}), (k:KhaiNiem {id: 'KN042'})
CREATE (ct)-[:CO_NGHIA_VU_CHUNG_MINH {dieu_khoan: 'Điều 133, Khoản 2', mo_ta: 'Chứng minh mối quan hệ nhân quả giữa hành vi vi phạm và thiệt hại'}]->(k);

// =============================================================================
// PHẦN G: QUAN HỆ VỀ LỘ TRÌNH ÁP DỤNG
// =============================================================================

// --- G1: Lộ trình phân loại rác ---
CREATE (lt001:LoTrinh {id: 'LT001', ten: 'Lộ trình phân loại CTRSH tại nguồn', thoi_han: '31/12/2024', dieu_khoan: 'Điều 75, Khoản 1'});

MATCH (lt:LoTrinh {id: 'LT001'}), (h:HanhVi {id: 'HV015'})
CREATE (lt)-[:AP_DUNG_CHO]->(h);

// --- G2: Lộ trình thị trường các-bon ---
CREATE (lt002:LoTrinh {id: 'LT002', ten: 'Lộ trình thị trường các-bon trong nước', giai_doan_1: '2025-2027: Thí điểm', giai_doan_2: '2028 trở đi: Vận hành chính thức', dieu_khoan: 'Điều 139'});

MATCH (lt:LoTrinh {id: 'LT002'}), (k:KhaiNiem {id: 'KN044'})
CREATE (lt)-[:AP_DUNG_CHO]->(k);

// --- G3: Lộ trình EPR ---
CREATE (lt003:LoTrinh {id: 'LT003', ten: 'Lộ trình trách nhiệm mở rộng của nhà sản xuất', mo_ta: 'Theo lộ trình do Chính phủ quy định', dieu_khoan: 'Điều 54'});

MATCH (lt:LoTrinh {id: 'LT003'}), (k:KhaiNiem {id: 'KN056'})
CREATE (lt)-[:AP_DUNG_CHO]->(k);

// =============================================================================
// PHẦN H: QUAN HỆ KINH TẾ MÔI TRƯỜNG MỞ RỘNG
// =============================================================================

// --- H1: Chuỗi giá trị tín chỉ các-bon ---

// Giảm phát thải -> Tạo tín chỉ
MATCH (a:KhaiNiem {id: 'KN031'}), (b:KhaiNiem {id: 'KN035'})
CREATE (a)-[:TAO_RA {suy_luan: true, giai_thich: 'Hoạt động giảm nhẹ phát thải KNK có thể tạo ra tín chỉ các-bon'}]->(b);

// Tín chỉ -> Thị trường -> Thu nhập
MATCH (a:KhaiNiem {id: 'KN035'}), (b:KhaiNiem {id: 'KN044'})
CREATE (a)-[:GIAO_DICH_TREN {dieu_khoan: 'Điều 139, Khoản 6'}]->(b);

// --- H2: Chuỗi EPR ---

// Sản phẩm -> Chất thải -> Tái chế -> Kinh tế tuần hoàn
MATCH (a:KhaiNiem {id: 'KN056'}), (b:KhaiNiem {id: 'KN018'})
CREATE (a)-[:QUAN_LY {suy_luan: true, giai_thich: 'EPR quản lý vòng đời sản phẩm đến giai đoạn thải bỏ'}]->(b);

MATCH (a:KhaiNiem {id: 'KN056'}), (b:KhaiNiem {id: 'KN045'})
CREATE (a)-[:THUC_DAY {suy_luan: true, giai_thich: 'EPR thúc đẩy tái chế, tái sử dụng theo mô hình kinh tế tuần hoàn'}]->(b);

// --- H3: Dịch vụ hệ sinh thái ---

// Vốn tự nhiên -> Dịch vụ hệ sinh thái -> Chi trả
MATCH (a:KhaiNiem {id: 'KN051'}), (b:KhaiNiem {id: 'KN043'})
CREATE (a)-[:CUNG_CAP {suy_luan: true, dieu_khoan: 'Điều 147, Khoản 1', giai_thich: 'Vốn tự nhiên cung cấp dịch vụ hệ sinh thái'}]->(b);

// --- H4: Công cụ tài chính xanh ---

// Tín dụng xanh -> Dự án BVMT
MATCH (a:KhaiNiem {id: 'KN052'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:TAI_TRO {dieu_khoan: 'Điều 149, Khoản 1', giai_thich: 'Tín dụng xanh cho vay ưu đãi cho dự án BVMT'}]->(b);

// Trái phiếu xanh -> Dự án BVMT
MATCH (a:KhaiNiem {id: 'KN053'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:HUY_DONG_VON {dieu_khoan: 'Điều 150, Khoản 1', giai_thich: 'Trái phiếu xanh huy động vốn cho hoạt động BVMT'}]->(b);

// Quỹ BVMT -> Hỗ trợ tài chính
MATCH (a:KhaiNiem {id: 'KN054'}), (b:KhaiNiem {id: 'KN057'})
CREATE (a)-[:HO_TRO {suy_luan: true, giai_thich: 'Quỹ BVMT hỗ trợ tài chính cho phục hồi môi trường'}]->(b);

// =============================================================================
// PHẦN I: QUAN HỆ ĐA CHIỀU GIỮA CÁC NHÓM DỰ ÁN
// =============================================================================

// --- I1: Quan hệ giữa các nhóm dự án ---

// Nhóm I > Nhóm II > Nhóm III > Nhóm IV (về mức độ yêu cầu)
MATCH (a:DuAn {id: 'DA001'}), (b:DuAn {id: 'DA002'})
CREATE (a)-[:YEU_CAU_CAO_HON {giai_thich: 'Nhóm I có yêu cầu BVMT cao hơn Nhóm II'}]->(b);

MATCH (a:DuAn {id: 'DA002'}), (b:DuAn {id: 'DA003'})
CREATE (a)-[:YEU_CAU_CAO_HON {giai_thich: 'Nhóm II có yêu cầu BVMT cao hơn Nhóm III'}]->(b);

MATCH (a:DuAn {id: 'DA003'}), (b:DuAn {id: 'DA004'})
CREATE (a)-[:YEU_CAU_CAO_HON {giai_thich: 'Nhóm III có yêu cầu BVMT cao hơn Nhóm IV'}]->(b);

// --- I2: Điều kiện chuyển nhóm ---

// Có yếu tố nhạy cảm -> Tăng nhóm
MATCH (yn:YeuToNhayCam), (d:DuAn {nhom: 'II'})
CREATE (yn)-[:LAM_TANG_NHOM {giai_thich: 'Yếu tố nhạy cảm có thể làm dự án Nhóm II chuyển thành Nhóm I', suy_luan: true}]->(d);

// =============================================================================
// PHẦN J: QUERY MẪU CHO CÁC QUAN HỆ MỚI
// =============================================================================

// --- Query 1: Tìm tất cả quan hệ suy luận ---
// MATCH ()-[r]-() WHERE r.suy_luan = true
// RETURN type(r) AS quan_he, r.giai_thich AS giai_thich, count(*) AS so_luong
// ORDER BY so_luong DESC;

// --- Query 2: Tìm chuỗi nhân quả: Hành vi -> Hậu quả -> Chế tài ---
// MATCH path = (h:HanhVi)-[:KHONG_THUC_HIEN_SE|DAN_DEN*1..2]->(ct:CheTai)
// RETURN h.ten AS hanh_vi, [r IN relationships(path) | type(r)] AS quan_he, ct.ten AS che_tai;

// --- Query 3: Tìm nghĩa vụ theo lộ trình ---
// MATCH (lt:LoTrinh)-[:AP_DUNG_CHO]->(target)
// RETURN lt.ten, lt.thoi_han, labels(target)[0], target.ten;

// --- Query 4: Phân tích chuỗi giá trị kinh tế xanh ---
// MATCH path = (start:KhaiNiem)-[:TAO_RA|GIAO_DICH|GIAO_DICH_TREN|HO_TRO|TAI_TRO*1..3]->(end:KhaiNiem)
// WHERE start.chuong = 'XI'
// RETURN [n IN nodes(path) | n.ten] AS chuoi_gia_tri;

// --- Query 5: Tìm quan hệ công cụ - mục tiêu ---
// MATCH (tool:KhaiNiem)-[r:CONG_CU_CHO|GIAM_THIEU|PHONG_NGUA]->(target:KhaiNiem)
// RETURN tool.ten AS cong_cu, type(r) AS quan_he, target.ten AS muc_tieu;

// --- Query 6: Tìm tất cả nghĩa vụ của một chủ thể cụ thể ---
// MATCH (ct:ChuThe {ten: 'Hộ gia đình'})-[r:CO_NGHIA_VU]->(h)
// RETURN r.mo_ta AS nghia_vu, r.dieu_khoan AS can_cu, r.thoi_han AS thoi_han;

// =============================================================================
// KẾT THÚC FILE MỞ RỘNG
// =============================================================================
// =============================================================================
// KNOWLEDGE GRAPH - LUẬT BẢO VỆ MÔI TRƯỜNG VIỆT NAM 2020
// PHẦN BỔ SUNG: CÁC QUAN HỆ CÒN THIẾU
// =============================================================================

// =============================================================================
// PHẦN A: BỔ SUNG NODES CÒN THIẾU
// =============================================================================

// --- A1: Khái niệm còn thiếu từ file quan hệ ---
CREATE (kn059:KhaiNiem {id: 'KN059', ten: 'Chiến lược bảo vệ môi trường quốc gia', dieu_khoan: 'Điều 22, Khoản 1', chuong: 'II', noi_dung: 'Chiến lược bảo vệ môi trường quốc gia là cơ sở để lập quy hoạch bảo vệ môi trường quốc gia'});
CREATE (kn060:KhaiNiem {id: 'KN060', ten: 'Xả nước thải khí thải', dieu_khoan: 'Điều 72, Khoản 2a,3', chuong: 'VI', noi_dung: 'Hoạt động xả nước thải, khí thải ra môi trường phải đạt quy chuẩn kỹ thuật môi trường'});
CREATE (kn061:KhaiNiem {id: 'KN061', ten: 'Chất thải có khả năng tái sử dụng tái chế', dieu_khoan: 'Điều 75, Khoản 1a', chuong: 'V', noi_dung: 'Chất thải rắn sinh hoạt được phân loại có khả năng tái sử dụng, tái chế'});
CREATE (kn062:KhaiNiem {id: 'KN062', ten: 'Chất thải rắn công nghiệp thông thường', dieu_khoan: 'Điều 81, Khoản 1', chuong: 'V', noi_dung: 'Chất thải rắn phát sinh từ hoạt động sản xuất công nghiệp không có đặc tính nguy hại'});
CREATE (kn063:KhaiNiem {id: 'KN063', ten: 'Giá dịch vụ xử lý chất thải rắn sinh hoạt', dieu_khoan: 'Điều 79, Khoản 1', chuong: 'V', noi_dung: 'Giá dịch vụ thu gom, vận chuyển và xử lý chất thải rắn sinh hoạt do UBND cấp tỉnh quy định'});
CREATE (kn064:KhaiNiem {id: 'KN064', ten: 'Nguồn thải vào môi trường nước mặt', dieu_khoan: 'Điều 9, Khoản 1', chuong: 'II', noi_dung: 'Các nguồn xả thải vào môi trường nước mặt phải được kiểm soát theo khả năng chịu tải'});
CREATE (kn065:KhaiNiem {id: 'KN065', ten: 'Hệ thống xử lý chất thải', dieu_khoan: 'Điều 132, Khoản 1a', chuong: 'XII', noi_dung: 'Hệ thống xử lý nước thải, khí thải, chất thải rắn, chất thải nguy hại'});
CREATE (kn066:KhaiNiem {id: 'KN066', ten: 'Chi phí ứng phó sự cố môi trường', dieu_khoan: 'Điều 128, Khoản 1', chuong: 'X', noi_dung: 'Chi phí tổ chức ứng phó sự cố môi trường, phục hồi môi trường'});
CREATE (kn067:KhaiNiem {id: 'KN067', ten: 'Suy giảm chức năng tính hữu ích của môi trường', dieu_khoan: 'Điều 130, Khoản 1a', chuong: 'X', noi_dung: 'Thành phần thiệt hại do ô nhiễm, suy thoái môi trường'});
CREATE (kn068:KhaiNiem {id: 'KN068', ten: 'Di sản thiên nhiên', dieu_khoan: 'Điều 20, Khoản 1', chuong: 'II', noi_dung: 'Di sản thiên nhiên được bảo vệ theo quy định của pháp luật'});
CREATE (kn069:KhaiNiem {id: 'KN069', ten: 'Hệ thống thông tin cơ sở dữ liệu môi trường', dieu_khoan: 'Điều 115, Khoản 2', chuong: 'IX', noi_dung: 'Cơ sở dữ liệu môi trường là tập hợp thông tin về môi trường được xây dựng, cập nhật'});
CREATE (kn070:KhaiNiem {id: 'KN070', ten: 'Chủ quyền an ninh lợi ích quốc gia', dieu_khoan: 'Điều 4, Khoản 7', chuong: 'I', noi_dung: 'Hoạt động BVMT không được gây phương hại đến chủ quyền, an ninh và lợi ích quốc gia'});
CREATE (kn071:KhaiNiem {id: 'KN071', ten: 'Thông tin về môi trường', dieu_khoan: 'Điều 114, Khoản 1', chuong: 'IX', noi_dung: 'Thông tin về môi trường bao gồm số liệu, dữ liệu về môi trường'});
CREATE (kn072:KhaiNiem {id: 'KN072', ten: 'Mối quan hệ nhân quả với thiệt hại', dieu_khoan: 'Điều 133, Khoản 2', chuong: 'X', noi_dung: 'Mối quan hệ nhân quả giữa hành vi vi phạm và thiệt hại môi trường'});
CREATE (kn073:KhaiNiem {id: 'KN073', ten: 'Hành vi vi phạm pháp luật về môi trường', dieu_khoan: 'Điều 133, Khoản 2', chuong: 'X', noi_dung: 'Hành vi vi phạm quy định pháp luật về bảo vệ môi trường'});

// --- A2: Văn bản/Báo cáo còn thiếu ---
CREATE (vb005:VanBan {id: 'VB005', ten: 'Báo cáo công tác bảo vệ môi trường', loai: 'bao_cao', dieu_khoan: 'Điều 118'});
CREATE (vb006:VanBan {id: 'VB006', ten: 'Quy chuẩn kỹ thuật môi trường địa phương', loai: 'quy_chuan', dieu_khoan: 'Điều 102, Khoản 5'});

// =============================================================================
// PHẦN B: CÁC QUAN HỆ TỪ FILE QUAN HỆ KHÁI NIỆM (47 quan hệ)
// =============================================================================

// --- B1: Quan hệ 2 - Chiến lược là cơ sở để lập Quy hoạch ---
MATCH (a:KhaiNiem {id: 'KN059'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:CO_SO_DE_LAP {dieu_khoan: 'Điều 22, Khoản 1; Điều 23, Khoản 1'}]->(b);

// --- B2: Quan hệ 3 - Ô nhiễm được đánh giá theo Quy chuẩn (đã có, bỏ qua) ---

// --- B3: Quan hệ 4 - Ứng phó BĐKH bao gồm Giảm nhẹ phát thải (đã có, bỏ qua) ---

// --- B4: Quan hệ 5 - Xả thải phải đạt Quy chuẩn ---
MATCH (a:KhaiNiem {id: 'KN060'}), (b:KhaiNiem {id: 'KN010'})
CREATE (a)-[:PHAI_DAT {dieu_khoan: 'Điều 72, Khoản 2a, 3', mo_ta: 'Xả nước thải, khí thải phải đạt quy chuẩn kỹ thuật môi trường'}]->(b);

// --- B5: Quan hệ 6 - GPMT và Đăng ký MT (quan hệ hành chính thay thế) (đã có) ---

// --- B6: Quan hệ 7 - Sự cố MT gây Ô nhiễm/Suy thoái (đã có) ---

// --- B7: Quan hệ 8 - Dự án khẩn cấp được miễn ĐTM ---
MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN007'})
CREATE (d)-[:DUOC_MIEN_TRU {dieu_khoan: 'Điều 30, Khoản 2', dieu_kien: 'Dự án đầu tư công khẩn cấp'}]->(k);

// --- B8: Quan hệ 9 - QĐ phê duyệt ĐTM căn cứ cấp GPMT (đã có) ---

// --- B9: Quan hệ 10 - GPMT trước Vận hành thử nghiệm (đã có) ---

// --- B10: Quan hệ 11 - Chất thải rắn SH phân loại thành Chất thải tái chế ---
MATCH (a:KhaiNiem {id: 'KN019'}), (b:KhaiNiem {id: 'KN061'})
CREATE (a)-[:PHAN_LOAI_THANH {dieu_khoan: 'Điều 75, Khoản 1'}]->(b);

// --- B11: Quan hệ 12 - Chất thải rắn CN phân loại với Chất thải nguy hại ---
MATCH (a:KhaiNiem {id: 'KN062'}), (b:KhaiNiem {id: 'KN020'})
CREATE (a)-[:PHAN_LOAI_RIENG_VOI {dieu_khoan: 'Điều 81, Khoản 3', mo_ta: 'Phải phân loại riêng với chất thải nguy hại'}]->(b);

// --- B12: Quan hệ 13 - Giá dịch vụ chi trả theo Khối lượng/thể tích ---
MATCH (a:KhaiNiem {id: 'KN063'}), (b:KhaiNiem {id: 'KN019'})
CREATE (a)-[:TINH_THEO {dieu_khoan: 'Điều 79, Khoản 1b', mo_ta: 'Tính theo khối lượng hoặc thể tích chất thải đã phân loại'}]->(b);

// --- B13: Quan hệ 14 - Gây thiệt hại phải bồi thường Thiệt hại MT (đã có phần nào) ---
MATCH (ct:ChuThe {id: 'CT017'}), (k:KhaiNiem {id: 'KN042'})
CREATE (ct)-[:PHAI_BOI_THUONG {dieu_khoan: 'Điều 130, Khoản 2', mo_ta: 'Bồi thường toàn bộ thiệt hại'}]->(k);

// --- B14: Quan hệ 15 - Trách nhiệm chứng minh nhân quả ---
MATCH (a:KhaiNiem {id: 'KN073'}), (b:KhaiNiem {id: 'KN072'})
CREATE (a)-[:PHAI_CHUNG_MINH {dieu_khoan: 'Điều 133, Khoản 2', mo_ta: 'Bên gây thiệt hại phải chứng minh mối quan hệ nhân quả'}]->(b);

// --- B15: Quan hệ 16 - Nguồn thải kiểm soát theo Khả năng chịu tải ---
MATCH (a:KhaiNiem {id: 'KN064'}), (b:KhaiNiem {id: 'KN023'})
CREATE (a)-[:KIEM_SOAT_THEO {dieu_khoan: 'Điều 9, Khoản 2', mo_ta: 'Kiểm soát nguồn thải theo khả năng chịu tải của môi trường'}]->(b);

// --- B16: Quan hệ 17 - Hạ tầng BVMT bao gồm Hệ thống xử lý chất thải ---
MATCH (a:KhaiNiem {id: 'KN024'}), (b:KhaiNiem {id: 'KN065'})
CREATE (a)-[:BAO_GOM {dieu_khoan: 'Điều 3, Khoản 24; Điều 132, Khoản 1'}]->(b);

// --- B17: Quan hệ 18 - Dự án Nhóm I yêu cầu PEIA (đã có) ---

// --- B18: Quan hệ 19 - Chất thải tái chế được miễn chi trả ---
MATCH (a:KhaiNiem {id: 'KN061'}), (b:KhaiNiem {id: 'KN063'})
CREATE (a)-[:DUOC_MIEN {dieu_khoan: 'Điều 79, Khoản 1c', mo_ta: 'Miễn chi trả giá dịch vụ thu gom, vận chuyển và xử lý'}]->(b);

// --- B19: Quan hệ 20 - Hạn ngạch KNK và Tín chỉ các-bon (cơ chế kinh tế) ---
MATCH (a:KhaiNiem {id: 'KN033'}), (b:KhaiNiem {id: 'KN035'})
CREATE (a)-[:CO_THE_TRAO_DOI_VOI {dieu_khoan: 'Điều 139, Khoản 1', mo_ta: 'Cơ chế kinh tế trao đổi hạn ngạch và tín chỉ'}]->(b);

// --- B20: Quan hệ 21 - Kinh tế tuần hoàn khuyến khích giảm khai thác, kéo dài vòng đời ---
MATCH (a:KhaiNiem {id: 'KN045'}), (b:KhaiNiem {id: 'KN027'})
CREATE (a)-[:KHUYEN_KHICH_SU_DUNG {dieu_khoan: 'Điều 142, Khoản 1', mo_ta: 'Khuyến khích tái sử dụng phế liệu'}]->(b);

// --- B21: Quan hệ 22 - Tiêu chuẩn MT là cơ sở cho Quy chuẩn MT ---
MATCH (a:KhaiNiem {id: 'KN011'}), (b:KhaiNiem {id: 'KN010'})
CREATE (a)-[:CO_SO_XAY_DUNG {dieu_khoan: 'Điều 103, Khoản 2', mo_ta: 'Tiêu chuẩn môi trường là cơ sở để xây dựng quy chuẩn'}]->(b);

// --- B22: Quan hệ 23 - Khai thác khoáng sản/Nhập khẩu phế liệu phải Ký quỹ ---
MATCH (c:ChuThe {id: 'CT014'}), (k:KhaiNiem {id: 'KN054'})
CREATE (c)-[:PHAI_KY_QUY_TAI {dieu_khoan: 'Điều 137, Khoản 1, 2', mo_ta: 'Ký quỹ tại Quỹ BVMT'}]->(k);

// --- B23: Quan hệ 24 - Hoạt động BVMT không được gây phương hại chủ quyền ---
MATCH (a:KhaiNiem {id: 'KN002'}), (b:KhaiNiem {id: 'KN070'})
CREATE (a)-[:KHONG_DUOC_GAY_PHUONG_HAI {dieu_khoan: 'Điều 4, Khoản 7'}]->(b);

// --- B24: Quan hệ 25 - Khu vực ô nhiễm đất là tiền đề của Ô nhiễm MT ---
MATCH (a:KhaiNiem {id: 'KN012'}), (b:KhaiNiem {id: 'KN039'})
CREATE (a)-[:HINH_THANH {dieu_khoan: 'Điều 16, Khoản 1', mo_ta: 'Ô nhiễm môi trường hình thành khu vực ô nhiễm đất'}]->(b);

// --- B25: Quan hệ 26 - Kiểm toán MT đánh giá Kiểm soát ô nhiễm (đã có phần nào) ---
MATCH (a:KhaiNiem {id: 'KN040'}), (b:KhaiNiem {id: 'KN022'})
CREATE (a)-[:DANH_GIA_HIEU_QUA {dieu_khoan: 'Điều 74, Khoản 1', mo_ta: 'Kiểm toán MT đánh giá hiệu quả kiểm soát ô nhiễm'}]->(b);

// --- B26: Quan hệ 27 - Sự cố chất thải là loại Sự cố MT (đã có) ---

// --- B27: Quan hệ 28 - Sự cố MT yêu cầu Chi phí ứng phó/Phục hồi ---
MATCH (a:KhaiNiem {id: 'KN014'}), (b:KhaiNiem {id: 'KN066'})
CREATE (a)-[:YEU_CAU_CHI_TRA {dieu_khoan: 'Điều 128, Khoản 1', mo_ta: 'Tổ chức, cá nhân gây ra sự cố MT phải chi trả chi phí ứng phó'}]->(b);

MATCH (a:KhaiNiem {id: 'KN014'}), (b:KhaiNiem {id: 'KN057'})
CREATE (a)-[:YEU_CAU {dieu_khoan: 'Điều 126, Khoản 1', mo_ta: 'Sự cố MT yêu cầu phục hồi môi trường'}]->(b);

// --- B28: Quan hệ 29 - Thiệt hại MT bao gồm Suy giảm chức năng ---
MATCH (a:KhaiNiem {id: 'KN042'}), (b:KhaiNiem {id: 'KN067'})
CREATE (a)-[:BAO_GOM {dieu_khoan: 'Điều 130, Khoản 1a'}]->(b);

// --- B29: Quan hệ 30 - Chi trả dịch vụ HSTT để Bảo vệ, duy trì HSTT ---
MATCH (a:KhaiNiem {id: 'KN043'}), (b:KhaiNiem {id: 'KN051'})
CREATE (a)-[:BAO_VE_DUY_TRI {dieu_khoan: 'Điều 138, Khoản 1; Điều 147, Khoản 2', mo_ta: 'Chi trả dịch vụ HSTT để bảo vệ, duy trì và phát triển hệ sinh thái tự nhiên'}]->(b);

// --- B30: Quan hệ 31 - Thị trường các-bon bao gồm Hạn ngạch và Tín chỉ (đã có phần nào) ---

// --- B31: Quan hệ 32 - Quy chuẩn địa phương căn cứ Quy chuẩn quốc gia ---
MATCH (a:VanBan {id: 'VB006'}), (b:KhaiNiem {id: 'KN010'})
CREATE (a)-[:CAN_CU {dieu_khoan: 'Điều 102, Khoản 5', mo_ta: 'QCKTMT địa phương ban hành trong 02 năm kể từ ngày ban hành QCKTMT quốc gia'}]->(b);

// --- B32: Quan hệ 33 - Tín dụng xanh cho Ứng phó BĐKH (đã có phần nào) ---
MATCH (a:KhaiNiem {id: 'KN052'}), (b:KhaiNiem {id: 'KN018'})
CREATE (a)-[:TAI_TRO_CHO {dieu_khoan: 'Điều 149, Khoản 1', mo_ta: 'Tín dụng xanh cho dự án quản lý chất thải'}]->(b);

// --- B33: Quan hệ 34 - Trái phiếu xanh cho Dự án lợi ích MT ---
MATCH (a:KhaiNiem {id: 'KN053'}), (b:KhaiNiem {id: 'KN007'})
CREATE (a)-[:HUY_DONG_VON_CHO {dieu_khoan: 'Điều 150, Khoản 1', mo_ta: 'Trái phiếu xanh huy động vốn cho dự án mang lại lợi ích về môi trường'}]->(b);

// --- B34: Quan hệ 35 - Sản phẩm thân thiện MT được chứng nhận Nhãn sinh thái ---
MATCH (a:KhaiNiem {id: 'KN048'}), (b:KhaiNiem {id: 'KN049'})
CREATE (a)-[:DUOC_CHUNG_NHAN {dieu_khoan: 'Điều 145, Khoản 2'}]->(b);

// --- B35: Quan hệ 36 - Mua sắm xanh ưu tiên Sản phẩm thân thiện MT (đã có) ---

// --- B36: Quan hệ 37 - Công nghiệp MT cung cấp Công nghệ thiết bị BVMT ---
MATCH (a:KhaiNiem {id: 'KN046'}), (b:KhaiNiem {id: 'KN024'})
CREATE (a)-[:CUNG_CAP {dieu_khoan: 'Điều 143, Khoản 1', mo_ta: 'Công nghiệp MT cung cấp công nghệ, thiết bị phục vụ BVMT'}]->(b);

// --- B37: Quan hệ 38 - Vốn tự nhiên bao gồm Dịch vụ HSTT (đã có) ---

// --- B38: Quan hệ 39 - Ký quỹ BVMT tại Quỹ BVMT ---
MATCH (a:KhaiNiem {id: 'KN054'}), (h:HanhVi {id: 'HV018'})
CREATE (a)-[:NHAN {dieu_khoan: 'Điều 137, Khoản 4', mo_ta: 'Quỹ BVMT nhận ký quỹ BVMT'}]->(h);

// --- B39: Quan hệ 40 - Quỹ BVMT hỗ trợ Hoạt động BVMT (đã có) ---

// --- B40: Quan hệ 41 - Nhà sản xuất phải Tái chế ---
MATCH (c:ChuThe {id: 'CT010'}), (k:KhaiNiem {id: 'KN021'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 54, Khoản 1', mo_ta: 'Phải thực hiện tái chế theo tỷ lệ bắt buộc'}]->(k);

// --- B41: Quan hệ 42 - BAT dùng cho Phòng ngừa, kiểm soát ô nhiễm (đã có phần nào) ---

// --- B42: Quan hệ 43 - Cơ sở xử lý CTNH phải có GPMT ---
MATCH (c:ChuThe {id: 'CT009'}), (k:KhaiNiem {id: 'KN008'})
CREATE (c)-[:PHAI_CO {dieu_khoan: 'Điều 84, Khoản 3d', mo_ta: 'Cơ sở xử lý CTNH phải có giấy phép môi trường'}]->(k);

// --- B43: Quan hệ 44 - Đồng xử lý chất thải được khuyến khích ---
MATCH (a:KhaiNiem {id: 'KN021'}), (b:KhaiNiem {id: 'KN019'})
CREATE (a)-[:DUOC_KHUYEN_KHICH_CHO {dieu_khoan: 'Điều 78, Khoản 1; Điều 84, Khoản 2', mo_ta: 'Nhà nước khuyến khích đồng xử lý chất thải'}]->(b);

MATCH (a:KhaiNiem {id: 'KN021'}), (b:KhaiNiem {id: 'KN020'})
CREATE (a)-[:DUOC_KHUYEN_KHICH_CHO {dieu_khoan: 'Điều 84, Khoản 2'}]->(b);

// --- B44: Quan hệ 45 - ĐTM đánh giá tác động đến Di sản thiên nhiên ---
MATCH (a:KhaiNiem {id: 'KN007'}), (b:KhaiNiem {id: 'KN068'})
CREATE (a)-[:DANH_GIA_TAC_DONG_DEN {dieu_khoan: 'Điều 32, Khoản 1đ', mo_ta: 'ĐTM đánh giá tác động đến đa dạng sinh học, di sản thiên nhiên'}]->(b);

// --- B45: Quan hệ 46 - Thông tin MT là cơ sở dữ liệu MT ---
MATCH (a:KhaiNiem {id: 'KN071'}), (b:KhaiNiem {id: 'KN069'})
CREATE (a)-[:TAP_HOP_THANH {dieu_khoan: 'Điều 115, Khoản 2a', mo_ta: 'Cơ sở dữ liệu MT là tập hợp thông tin về MT'}]->(b);

// --- B46: Quan hệ 47 - Dự án khẩn cấp được miễn GPMT ---
MATCH (d:DuAn {id: 'DA001'}), (k:KhaiNiem {id: 'KN008'})
CREATE (d)-[:DUOC_MIEN_TRU_2 {dieu_khoan: 'Điều 39, Khoản 3', dieu_kien: 'Dự án đầu tư công khẩn cấp'}]->(k);

// =============================================================================
// PHẦN C: TRÁCH NHIỆM NHÀ NƯỚC CHI TIẾT (25 trách nhiệm)
// =============================================================================

// --- C1: Chính phủ - Quản lý thống nhất (đã có) ---

// --- C2: Chính phủ - Định hướng chính sách và ứng phó ---
MATCH (cq:CoQuan {id: 'CQ001'}), (k:KhaiNiem {id: 'KN012'})
CREATE (cq)-[:CHI_DAO_GIAI_QUYET {dieu_khoan: 'Điều 165, Khoản 2', mo_ta: 'Chỉ đạo tập trung giải quyết, khắc phục tình trạng ô nhiễm'}]->(k);

MATCH (cq:CoQuan {id: 'CQ001'}), (k:KhaiNiem {id: 'KN014'})
CREATE (cq)-[:CHI_DAO_KIEM_SOAT {dieu_khoan: 'Điều 165, Khoản 2', mo_ta: 'Chỉ đạo kiểm soát sự cố môi trường'}]->(k);

// --- C3: Chính phủ - Báo cáo Quốc hội ---
MATCH (cq:CoQuan {id: 'CQ001'}), (v:VanBan {id: 'VB005'})
CREATE (cq)-[:BAO_CAO_HANG_NAM {dieu_khoan: 'Điều 165, Khoản 4', mo_ta: 'Hằng năm, báo cáo Quốc hội về công tác BVMT'}]->(v);

// --- C4-7: Bộ TN&MT - Các trách nhiệm (đã có phần lớn) ---

// Bổ sung: Bộ TN&MT - Quản lý nước mặt
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN023'})
CREATE (cq)-[:DANH_GIA {dieu_khoan: 'Điều 8, Khoản 2b', mo_ta: 'Đánh giá khả năng chịu tải của môi trường nước mặt đối với sông, hồ liên tỉnh'}]->(k);

// Bổ sung: Bộ TN&MT - Quản lý chất ô nhiễm khó phân hủy
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN016'})
CREATE (cq)-[:QUAN_LY {dieu_khoan: 'Điều 69, Khoản 2b', mo_ta: 'Hướng dẫn và tổ chức thực hiện quản lý chất ô nhiễm khó phân hủy'}]->(k);

// Bổ sung: Bộ TN&MT - Giảm nhẹ phát thải KNK
MATCH (cq:CoQuan {id: 'CQ002'}), (k:KhaiNiem {id: 'KN031'})
CREATE (cq)-[:GIAM_SAT_DANH_GIA {dieu_khoan: 'Điều 166, Khoản 9', mo_ta: 'Triển khai hệ thống giám sát, đánh giá hoạt động giảm nhẹ phát thải KNK'}]->(k);

// --- C8-9: Bộ Quốc phòng / Công an ---
MATCH (cq:CoQuan {id: 'CQ003'}), (k:KhaiNiem {id: 'KN014'})
CREATE (cq)-[:UNG_PHO {dieu_khoan: 'Điều 167, Khoản 1', mo_ta: 'Xây dựng, tổ chức lực lượng, phương tiện tham gia ứng phó sự cố MT'}]->(k);

MATCH (cq:CoQuan {id: 'CQ004'}), (k:KhaiNiem {id: 'KN014'})
CREATE (cq)-[:UNG_PHO {dieu_khoan: 'Điều 167, Khoản 2', mo_ta: 'Tham gia ứng phó, khắc phục sự cố MT trong lĩnh vực an ninh'}]->(k);

// --- C10-13: UBND cấp tỉnh ---

// Bổ sung: UBND tỉnh - Chịu trách nhiệm ô nhiễm (đã có phần nào)

// Bổ sung: UBND tỉnh - Quy định giá dịch vụ rác
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN063'})
CREATE (cq)-[:QUY_DINH {dieu_khoan: 'Điều 79, Khoản 6', mo_ta: 'Quy định giá cụ thể đối với dịch vụ thu gom, vận chuyển, xử lý CTRSH'}]->(k);

// Bổ sung: UBND tỉnh - Xử lý ô nhiễm đất
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN039'})
CREATE (cq)-[:XU_LY {dieu_khoan: 'Điều 19, Khoản 3b', mo_ta: 'Xử lý khu vực ô nhiễm môi trường đất do lịch sử để lại'}]->(k);

// Bổ sung: UBND tỉnh - Bố trí kinh phí
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN002'})
CREATE (cq)-[:BO_TRI_KINH_PHI {dieu_khoan: 'Điều 168, Khoản 1i', mo_ta: 'Trình HĐND bố trí kinh phí thực hiện nhiệm vụ BVMT'}]->(k);

// Bổ sung: UBND tỉnh - Quản lý cụm công nghiệp
MATCH (cq:CoQuan {id: 'CQ005'}), (k:KhaiNiem {id: 'KN037'})
CREATE (cq)-[:QUAN_LY {dieu_khoan: 'Điều 52, Khoản 6c', mo_ta: 'Ban hành lộ trình di dời dân cư ra khỏi cụm công nghiệp'}]->(k);

// --- C14-16: UBND cấp huyện ---

// Bổ sung: UBND huyện - Thanh tra kiểm tra
MATCH (cq:CoQuan {id: 'CQ006'}), (k:KhaiNiem {id: 'KN002'})
CREATE (cq)-[:THANH_TRA_KIEM_TRA {dieu_khoan: 'Điều 168, Khoản 2e', mo_ta: 'Tổ chức kiểm tra, thanh tra về BVMT trên địa bàn'}]->(k);

// --- C17-20: UBND cấp xã (đã có phần lớn) ---

// Bổ sung: UBND xã - Kiểm tra vi phạm CTRSH
MATCH (cq:CoQuan {id: 'CQ007'}), (k:KhaiNiem {id: 'KN019'})
CREATE (cq)-[:KIEM_TRA_XU_LY {dieu_khoan: 'Điều 77, Khoản 7a', mo_ta: 'Kiểm tra, xử lý vi phạm về thu gom, vận chuyển CTRSH'}]->(k);

// Bổ sung: UBND xã - Giáo dục cộng đồng
MATCH (cq:CoQuan {id: 'CQ007'}), (c:ChuThe {id: 'CT006'})
CREATE (cq)-[:VAN_DONG_GIAO_DUC {dieu_khoan: 'Điều 168, Khoản 3d', mo_ta: 'Vận động, hướng dẫn cộng đồng dân cư bảo vệ môi trường'}]->(c);

// =============================================================================
// PHẦN D: BỔ SUNG QUAN HỆ QUYỀN VÀ NGHĨA VỤ CÒN THIẾU
// =============================================================================

// --- D1: Mọi cơ quan, tổ chức, cá nhân - Quyền và Nghĩa vụ BVMT ---
MATCH (c:ChuThe {id: 'CT001'}), (k:KhaiNiem {id: 'KN002'})
CREATE (c)-[:CO_QUYEN_VA_NGHIA_VU {dieu_khoan: 'Điều 4, Khoản 1; Điều 1', mo_ta: 'BVMT là quyền, nghĩa vụ và trách nhiệm của mọi đối tượng'}]->(k);

MATCH (c:ChuThe {id: 'CT002'}), (k:KhaiNiem {id: 'KN002'})
CREATE (c)-[:CO_QUYEN_VA_NGHIA_VU {dieu_khoan: 'Điều 4, Khoản 1; Điều 1'}]->(k);

MATCH (c:ChuThe {id: 'CT005'}), (k:KhaiNiem {id: 'KN002'})
CREATE (c)-[:CO_QUYEN_VA_NGHIA_VU {dieu_khoan: 'Điều 4, Khoản 1; Điều 1'}]->(k);

MATCH (c:ChuThe {id: 'CT006'}), (k:KhaiNiem {id: 'KN002'})
CREATE (c)-[:CO_QUYEN_VA_NGHIA_VU {dieu_khoan: 'Điều 4, Khoản 1; Điều 1'}]->(k);

// --- D2: Tổ chức tín dụng - Khuyến khích tín dụng xanh ---
MATCH (c:ChuThe {id: 'CT012'}), (k:KhaiNiem {id: 'KN052'})
CREATE (c)-[:DUOC_KHUYEN_KHICH {dieu_khoan: 'Điều 149, Khoản 3', mo_ta: 'Khuyến khích cho vay ưu đãi đối với dự án tín dụng xanh'}]->(k);

// --- D3: Cơ sở SX KD DV - Nghĩa vụ giảm thiểu bụi, khí thải ---
MATCH (c:ChuThe {id: 'CT004'}), (k:KhaiNiem {id: 'KN060'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 12, Khoản 1', mo_ta: 'Giảm thiểu và xử lý bụi, khí thải tác động xấu đến môi trường'}]->(k);

// --- D4: Hộ gia đình - Xử lý nước thải tại chỗ ---
MATCH (c:ChuThe {id: 'CT005'}), (k:KhaiNiem {id: 'KN065'})
CREATE (c)-[:CO_NGHIA_VU {dieu_khoan: 'Điều 60, Khoản 1e', dieu_kien: 'Ở đô thị, khu dân cư tập trung khi xây mới/cải tạo', mo_ta: 'Xây lắp công trình, thiết bị xử lý nước thải tại chỗ'}]->(k);

// --- D5: Hộ gia đình - Không gây ô nhiễm tiếng ồn, khí thải ---
MATCH (c:ChuThe {id: 'CT005'}), (k:KhaiNiem {id: 'KN012'})
CREATE (c)-[:KHONG_DUOC_GAY_RA {dieu_khoan: 'Điều 60, Khoản 1c', mo_ta: 'Không được gây ô nhiễm tiếng ồn, độ rung, khí thải'}]->(k);

// --- D6: Cơ sở có nguy cơ - Khoảng cách an toàn ---
MATCH (c:ChuThe {id: 'CT004'}), (c2:ChuThe {id: 'CT006'})
CREATE (c)-[:PHAI_DAM_BAO_KHOANG_CACH {dieu_khoan: 'Điều 53, Khoản 2', mo_ta: 'Phải có khoảng cách an toàn đối với cộng đồng dân cư'}]->(c2);

// --- D7: Đại diện cộng đồng - Quyền yêu cầu thông tin ---
MATCH (c:ChuThe {id: 'CT006'}), (k:KhaiNiem {id: 'KN071'})
CREATE (c)-[:CO_QUYEN_YEU_CAU {dieu_khoan: 'Điều 159, Khoản 1', mo_ta: 'Yêu cầu chủ dự án, cơ sở cung cấp thông tin về môi trường'}]->(k);

// --- D8: Chủ dự án - Điều chỉnh dự án theo kết quả thẩm định ---
MATCH (c:ChuThe {id: 'CT003'}), (k:KhaiNiem {id: 'KN007'})
CREATE (c)-[:PHAI_DIEU_CHINH_THEO {dieu_khoan: 'Điều 37, Khoản 1', mo_ta: 'Điều chỉnh, bổ sung nội dung dự án cho phù hợp với kết quả thẩm định ĐTM'}]->(k);

// --- D9: Chủ dự án - Miễn bồi thường khi tuân thủ ---
MATCH (c:ChuThe {id: 'CT003'}), (k:KhaiNiem {id: 'KN042'})
CREATE (c)-[:DUOC_MIEN_BOI_THUONG {dieu_khoan: 'Điều 130, Khoản 4', dieu_kien: 'Tuân thủ đầy đủ pháp luật BVMT', mo_ta: 'Không phải bồi thường nếu không gây thiệt hại do tuân thủ đầy đủ pháp luật'}]->(k);

// =============================================================================
// PHẦN E: THỐNG KÊ VÀ QUERY
// =============================================================================

// --- Query: Đếm tổng số quan hệ theo loại ---
// MATCH ()-[r]->()
// RETURN type(r) AS quan_he, count(*) AS so_luong
// ORDER BY so_luong DESC;

// --- Query: Tìm tất cả quan hệ của một cơ quan cụ thể ---
// MATCH (cq:CoQuan {ten: 'UBND cấp tỉnh'})-[r]->(target)
// RETURN type(r) AS quan_he, target.ten AS doi_tuong, r.mo_ta AS mo_ta;

// --- Query: Tìm chuỗi quan hệ kinh tế môi trường ---
// MATCH path = (start)-[:TAI_TRO|TAI_TRO_CHO|HUY_DONG_VON_CHO|HO_TRO*1..3]->(end)
// WHERE 'KhaiNiem' IN labels(start) AND start.chuong = 'XI'
// RETURN [n IN nodes(path) | n.ten] AS chuoi;

// =============================================================================
// KẾT THÚC FILE BỔ SUNG
// =============================================================================
// =============================================================================
// KNOWLEDGE GRAPH - LUẬT BẢO VỆ MÔI TRƯỜNG VIỆT NAM 2020
// BỔ SUNG TỪ GOOGLE SHEETS "QA Environment"
// =============================================================================

// =============================================================================
// PHẦN A: NODES MỚI TỪ GOOGLE SHEETS (Chưa có trong KG hiện tại)
// =============================================================================

// --- A1: Khái niệm Cốt lõi - Bổ sung ---

// (Hầu hết đã có, bổ sung ID mới theo naming convention của GSheet)

// --- A2: Công cụ Quản lý & Pháp lý - Bổ sung ---

CREATE (kn074:KhaiNiem {
  id: 'KN074', 
  id_gsheet: 'KếHoạchQLCLMTNước',
  ten: 'Kế hoạch quản lý chất lượng môi trường nước mặt', 
  dieu_khoan: 'Điều 9', 
  chuong: 'II', 
  noi_dung: 'Kế hoạch quản lý chất lượng môi trường nước mặt đối với sông, hồ liên tỉnh và nội tỉnh',
  keyphrase: 'kế hoạch, quản lý chất lượng, nước mặt, sông hồ'
});

CREATE (kn075:KhaiNiem {
  id: 'KN075', 
  id_gsheet: 'KếHoạchQLCLMTKhôngKhí',
  ten: 'Kế hoạch quản lý chất lượng môi trường không khí', 
  dieu_khoan: 'Điều 13', 
  chuong: 'II', 
  noi_dung: 'Kế hoạch quản lý chất lượng môi trường không khí cấp quốc gia và cấp tỉnh',
  keyphrase: 'kế hoạch, quản lý chất lượng, không khí'
});

CREATE (kn076:KhaiNiem {
  id: 'KN076', 
  id_gsheet: 'Phí/ThuếBVMT',
  ten: 'Chính sách thuế phí bảo vệ môi trường', 
  dieu_khoan: 'Điều 136', 
  chuong: 'XI', 
  noi_dung: 'Thuế bảo vệ môi trường, phí bảo vệ môi trường theo quy định của pháp luật về thuế, phí',
  keyphrase: 'thuế, phí, bảo vệ môi trường'
});

CREATE (kn077:KhaiNiem {
  id: 'KN077', 
  id_gsheet: 'NướcThải',
  ten: 'Nước thải', 
  dieu_khoan: 'Điều 72, Khoản 2', 
  chuong: 'VI', 
  noi_dung: 'Nước thải từ hoạt động sản xuất, kinh doanh, dịch vụ, sinh hoạt',
  keyphrase: 'nước thải, xả thải'
});

CREATE (kn078:KhaiNiem {
  id: 'KN078', 
  id_gsheet: 'KhíThải',
  ten: 'Khí thải', 
  dieu_khoan: 'Điều 72, Khoản 3', 
  chuong: 'VI', 
  noi_dung: 'Khí thải từ hoạt động sản xuất, kinh doanh, dịch vụ',
  keyphrase: 'khí thải, xả khí'
});

CREATE (kn079:KhaiNiem {
  id: 'KN079', 
  id_gsheet: 'Bụi',
  ten: 'Bụi', 
  dieu_khoan: 'Điều 88', 
  chuong: 'VI', 
  noi_dung: 'Bụi từ hoạt động giao thông vận tải, xây dựng, sản xuất',
  keyphrase: 'bụi, ô nhiễm không khí'
});

CREATE (kn080:KhaiNiem {
  id: 'KN080', 
  id_gsheet: 'PhânVùngMT',
  ten: 'Phân vùng môi trường', 
  dieu_khoan: 'Điều 23, Khoản 4', 
  chuong: 'II', 
  noi_dung: 'Phân vùng môi trường trong quy hoạch bảo vệ môi trường quốc gia',
  keyphrase: 'phân vùng, quy hoạch môi trường'
});

CREATE (kn081:KhaiNiem {
  id: 'KN081', 
  id_gsheet: 'KhoảngCáchAnToàn',
  ten: 'Khoảng cách an toàn về môi trường', 
  dieu_khoan: 'Điều 53, Khoản 2', 
  chuong: 'IV', 
  noi_dung: 'Khoảng cách an toàn về môi trường đối với khu dân cư, công trình văn hóa, di tích lịch sử',
  keyphrase: 'khoảng cách an toàn, khu dân cư'
});

CREATE (kn082:KhaiNiem {
  id: 'KN082', 
  id_gsheet: 'BồiThườngTH',
  ten: 'Bồi thường thiệt hại về môi trường', 
  dieu_khoan: 'Điều 133', 
  chuong: 'X', 
  noi_dung: 'Việc bồi thường thiệt hại về môi trường được thực hiện theo quy định của pháp luật dân sự',
  keyphrase: 'bồi thường, thiệt hại, dân sự'
});

CREATE (kn083:KhaiNiem {
  id: 'KN083', 
  id_gsheet: 'HD_TáiChế',
  ten: 'Hoạt động tái chế sản phẩm bao bì', 
  dieu_khoan: 'Điều 54, Khoản 1', 
  chuong: 'V', 
  noi_dung: 'Trách nhiệm tái chế của nhà sản xuất, nhập khẩu theo tỷ lệ và quy cách bắt buộc',
  keyphrase: 'tái chế, sản phẩm, bao bì, EPR'
});

// --- A3: Chủ thể & Khu vực - Bổ sung ---

CREATE (ct018:ChuThe {
  id: 'CT018', 
  id_gsheet: 'BanQLKhuTT',
  ten: 'Ban quản lý khu sản xuất kinh doanh dịch vụ tập trung', 
  loai: 'phap_nhan', 
  dieu_khoan: 'Điều 50, 51',
  mo_ta: 'Ban quản lý các khu công nghiệp, khu chế xuất, khu công nghệ cao'
});

CREATE (ct019:ChuThe {
  id: 'CT019', 
  id_gsheet: 'HộiĐồngTĐ',
  ten: 'Hội đồng thẩm định', 
  loai: 'to_chuc', 
  dieu_khoan: 'Điều 34, Khoản 3',
  mo_ta: 'Hội đồng thẩm định báo cáo ĐTM, tối thiểu 07 thành viên'
});

CREATE (ct020:ChuThe {
  id: 'CT020', 
  id_gsheet: 'CơQuanThủyLợi',
  ten: 'Cơ quan nhà nước quản lý công trình thủy lợi', 
  loai: 'co_quan', 
  dieu_khoan: 'Điều 34, Khoản 3d',
  mo_ta: 'Cơ quan quản lý công trình thủy lợi tham gia Hội đồng thẩm định'
});

// --- A4: Khu vực đặc thù ---

CREATE (kv001:KhuVuc {
  id: 'KV001', 
  id_gsheet: 'KhuKinhTế',
  ten: 'Khu kinh tế', 
  loai: 'khu_kinh_te', 
  dieu_khoan: 'Điều 50',
  mo_ta: 'Khu kinh tế được thành lập theo quy định của pháp luật'
});

CREATE (kv002:KhuVuc {
  id: 'KV002', 
  id_gsheet: 'CCN',
  ten: 'Cụm công nghiệp', 
  loai: 'cum_cong_nghiep', 
  dieu_khoan: 'Điều 52',
  mo_ta: 'Cụm công nghiệp theo quy định của pháp luật về quản lý cụm công nghiệp'
});

// =============================================================================
// PHẦN B: MAPPING ID GSHEET VỚI KG HIỆN TẠI
// =============================================================================

// Cập nhật ID GSheet cho các nodes đã có
// (Chạy sau khi có nodes trong DB)

// MATCH (k:KhaiNiem {id: 'KN001'}) SET k.id_gsheet = 'MôiTrường';
// MATCH (k:KhaiNiem {id: 'KN003'}) SET k.id_gsheet = 'ThànhPhầnMT';
// MATCH (k:KhaiNiem {id: 'KN002'}) SET k.id_gsheet = 'HD_BVMT';
// ... và tiếp tục cho các nodes khác

// =============================================================================
// PHẦN C: QUAN HỆ MỚI SUY LUẬN TỪ CẤU TRÚC GSHEET
// =============================================================================

// --- C1: Quan hệ trong nhóm A - Khái niệm Cốt lõi ---

// Môi trường bao gồm Thành phần MT (đã có)
// Ô nhiễm/Suy thoái là trạng thái tiêu cực của MT
MATCH (a:KhaiNiem {id: 'KN001'}), (b:KhaiNiem {id: 'KN012'})
CREATE (b)-[:TRANG_THAI_TIEU_CUC_CUA {suy_luan: true}]->(a);

MATCH (a:KhaiNiem {id: 'KN001'}), (b:KhaiNiem {id: 'KN013'})
CREATE (b)-[:TRANG_THAI_TIEU_CUC_CUA {suy_luan: true}]->(a);

// Khả năng chịu tải là thuộc tính của Môi trường
MATCH (a:KhaiNiem {id: 'KN023'}), (b:KhaiNiem {id: 'KN001'})
CREATE (a)-[:THUOC_TINH_CUA {suy_luan: true}]->(b);

// BAT hỗ trợ Kiểm soát ô nhiễm
MATCH (a:KhaiNiem {id: 'KN036'}), (b:KhaiNiem {id: 'KN022'})
CREATE (a)-[:HO_TRO {dieu_khoan: 'Điều 3, Khoản 36', suy_luan: true}]->(b);

// Phục hồi MT là hoạt động sau Sự cố/Suy thoái
MATCH (a:KhaiNiem {id: 'KN057'}), (b:KhaiNiem {id: 'KN014'})
CREATE (a)-[:THUC_HIEN_SAU {dieu_khoan: 'Điều 126', suy_luan: true}]->(b);

MATCH (a:KhaiNiem {id: 'KN057'}), (b:KhaiNiem {id: 'KN013'})
CREATE (a)-[:THUC_HIEN_SAU {suy_luan: true}]->(b);

// Di sản thiên nhiên là thành phần cần bảo vệ của MT
MATCH (a:KhaiNiem {id: 'KN068'}), (b:KhaiNiem {id: 'KN001'})
CREATE (a)-[:THANH_PHAN_CAN_BAO_VE_CUA {dieu_khoan: 'Điều 20', suy_luan: true}]->(b);

// --- C2: Quan hệ trong nhóm B - Công cụ Quản lý ---

// GPMT và Đăng ký MT là công cụ cấp phép thay thế nhau (đã có)

// ĐTM là cơ sở để cấp GPMT (đã có)

// PEIA là bước đầu của ĐTM
MATCH (a:KhaiNiem {id: 'KN006'}), (b:KhaiNiem {id: 'KN007'})
CREATE (a)-[:BUOC_DAU_CUA {dieu_khoan: 'Điều 29', suy_luan: true}]->(b);

// ĐMCL (SEA) là cơ sở cho Quy hoạch BVMT
MATCH (a:KhaiNiem {id: 'KN005'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:CO_SO_CHO {dieu_khoan: 'Điều 22, 23', suy_luan: true}]->(b);

// QCKTMT là chuẩn bắt buộc, TCMT là tự nguyện
MATCH (a:KhaiNiem {id: 'KN010'}), (b:KhaiNiem {id: 'KN011'})
CREATE (a)-[:BAT_BUOC_HON {dieu_khoan: 'Điều 3, Khoản 10, 11', suy_luan: true}]->(b);

// Quan trắc MT cung cấp dữ liệu cho Kiểm soát ô nhiễm
MATCH (a:KhaiNiem {id: 'KN025'}), (b:KhaiNiem {id: 'KN022'})
CREATE (a)-[:CUNG_CAP_DU_LIEU_CHO {suy_luan: true}]->(b);

// Kế hoạch QLCL nước mặt thuộc về Quy hoạch BVMT
MATCH (a:KhaiNiem {id: 'KN074'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:THANH_PHAN_CUA {dieu_khoan: 'Điều 9', suy_luan: true}]->(b);

// Kế hoạch QLCL không khí thuộc về Quy hoạch BVMT
MATCH (a:KhaiNiem {id: 'KN075'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:THANH_PHAN_CUA {dieu_khoan: 'Điều 13', suy_luan: true}]->(b);

// Kiểm toán MT đánh giá hiệu quả Hoạt động BVMT
MATCH (a:KhaiNiem {id: 'KN040'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:DANH_GIA_HIEU_QUA {dieu_khoan: 'Điều 74', suy_luan: true}]->(b);

// Thuế/phí BVMT là công cụ kinh tế của Hoạt động BVMT
MATCH (a:KhaiNiem {id: 'KN076'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:CONG_CU_KINH_TE_CUA {dieu_khoan: 'Điều 136', suy_luan: true}]->(b);

// --- C3: Quan hệ trong nhóm C - Chủ thể ---

// Các cấp QLNN có phân cấp thẩm quyền
MATCH (a:CoQuan {id: 'CQ001'}), (b:CoQuan {id: 'CQ002'})
CREATE (a)-[:CAP_TREN_CUA {suy_luan: true}]->(b);

MATCH (a:CoQuan {id: 'CQ002'}), (b:CoQuan {id: 'CQ005'})
CREATE (a)-[:HUONG_DAN {suy_luan: true}]->(b);

MATCH (a:CoQuan {id: 'CQ005'}), (b:CoQuan {id: 'CQ006'})
CREATE (a)-[:CAP_TREN_CUA {suy_luan: true}]->(b);

MATCH (a:CoQuan {id: 'CQ006'}), (b:CoQuan {id: 'CQ007'})
CREATE (a)-[:CAP_TREN_CUA {suy_luan: true}]->(b);

// Chủ dự án vận hành Cơ sở SXKD
MATCH (c:ChuThe {id: 'CT003'}), (c2:ChuThe {id: 'CT004'})
CREATE (c)-[:VAN_HANH {suy_luan: true}]->(c2);

// Ban quản lý KCN quản lý Khu SXKD tập trung
MATCH (c:ChuThe {id: 'CT018'}), (k:KhaiNiem {id: 'KN037'})
CREATE (c)-[:QUAN_LY {dieu_khoan: 'Điều 50, 51'}]->(k);

// Hội đồng thẩm định thẩm định ĐTM
MATCH (c:ChuThe {id: 'CT019'}), (k:KhaiNiem {id: 'KN007'})
CREATE (c)-[:THAM_DINH {dieu_khoan: 'Điều 34, Khoản 3'}]->(k);

// Cơ quan thủy lợi tham gia Hội đồng thẩm định
MATCH (c:ChuThe {id: 'CT020'}), (c2:ChuThe {id: 'CT019'})
CREATE (c)-[:THAM_GIA {dieu_khoan: 'Điều 34, Khoản 3d', dieu_kien: 'Dự án xả thải vào công trình thủy lợi'}]->(c2);

// Cộng đồng dân cư có quyền giám sát Chủ dự án
MATCH (c:ChuThe {id: 'CT006'}), (c2:ChuThe {id: 'CT003'})
CREATE (c)-[:CO_QUYEN_GIAM_SAT {dieu_khoan: 'Điều 159'}]->(c2);

// --- C4: Quan hệ trong nhóm D - Chất thải ---

// Phân loại chất thải theo cấu trúc
MATCH (a:KhaiNiem {id: 'KN018'}), (b:KhaiNiem {id: 'KN019'})
CREATE (a)-[:PHAN_LOAI_THANH {mo_ta: 'Theo thể vật chất'}]->(b);

MATCH (a:KhaiNiem {id: 'KN018'}), (b:KhaiNiem {id: 'KN077'})
CREATE (a)-[:PHAN_LOAI_THANH {mo_ta: 'Nước thải'}]->(b);

MATCH (a:KhaiNiem {id: 'KN018'}), (b:KhaiNiem {id: 'KN078'})
CREATE (a)-[:PHAN_LOAI_THANH {mo_ta: 'Khí thải'}]->(b);

// CTR phân loại thành CTRSH, CTNH, CTCNTT
MATCH (a:KhaiNiem {id: 'KN019'}), (b:KhaiNiem {id: 'KN020'})
CREATE (b)-[:LA_LOAI_CUA]->(a);

MATCH (a:KhaiNiem {id: 'KN019'}), (b:KhaiNiem {id: 'KN062'})
CREATE (b)-[:LA_LOAI_CUA]->(a);

// CTRSH là loại CTR
MATCH (a:KhaiNiem {id: 'KN019'}), (b:KhaiNiem)
WHERE b.ten = 'Chất thải rắn sinh hoạt' OR b.id = 'KN019'
CREATE (b)-[:LA_LOAI_CUA]->(a);

// Bụi là dạng khí thải/ô nhiễm không khí
MATCH (a:KhaiNiem {id: 'KN079'}), (b:KhaiNiem {id: 'KN078'})
CREATE (a)-[:LIEN_QUAN_DEN]->(b);

// Phế liệu NK là nguồn tiềm ẩn CTNH
MATCH (a:KhaiNiem {id: 'KN027'}), (b:KhaiNiem {id: 'KN020'})
CREATE (a)-[:CO_THE_CHUA {suy_luan: true, dieu_khoan: 'Điều 70, 71'}]->(b);

// Chất ô nhiễm khó phân hủy là loại Chất ô nhiễm
MATCH (a:KhaiNiem {id: 'KN016'}), (b:KhaiNiem {id: 'KN015'})
CREATE (a)-[:LA_LOAI_CUA]->(b);

// KNK gây hiệu ứng nhà kính -> BĐKH (đã có)

// ODS gây suy giảm tầng ô-dôn (đã có)

// Vận hành thử nghiệm CTXL trước Vận hành chính thức
MATCH (a:KhaiNiem {id: 'KN026'}), (b:KhaiNiem {id: 'KN008'})
CREATE (a)-[:SAU_KHI_CO {dieu_khoan: 'Điều 42, Khoản 2a'}]->(b);

// Đồng xử lý CT là phương pháp xử lý
MATCH (a:KhaiNiem {id: 'KN021'}), (b:KhaiNiem {id: 'KN018'})
CREATE (a)-[:PHUONG_PHAP_XU_LY {dieu_khoan: 'Điều 3, Khoản 21'}]->(b);

// Sự cố chất thải là loại Sự cố MT (đã có)

// --- C5: Quan hệ trong nhóm E - Chính sách & Tài chính ---

// Kinh tế tuần hoàn giảm Chất thải (đã có)

// Tín dụng xanh hỗ trợ Hoạt động BVMT
MATCH (a:KhaiNiem {id: 'KN052'}), (b:KhaiNiem {id: 'KN002'})
CREATE (a)-[:HO_TRO_TAI_CHINH {dieu_khoan: 'Điều 149'}]->(b);

// Trái phiếu xanh huy động vốn cho BVMT (đã có)

// Vốn tự nhiên cung cấp Dịch vụ HSTT (đã có)

// Chi trả DVHSTT bảo vệ Vốn tự nhiên
MATCH (a:KhaiNiem {id: 'KN043'}), (b:KhaiNiem {id: 'KN051'})
CREATE (a)-[:BAO_VE {dieu_khoan: 'Điều 138'}]->(b);

// Quỹ BVMT nhận Ký quỹ BVMT
MATCH (a:KhaiNiem {id: 'KN054'}), (h:HanhVi {id: 'HV018'})
CREATE (a)-[:NHAN_2 {dieu_khoan: 'Điều 137, Khoản 4'}]->(h);

// Thị trường Carbon giao dịch Hạn ngạch KNK và Tín chỉ Carbon (đã có)

// Sản phẩm thân thiện MT được chứng nhận Nhãn sinh thái (đã có)

// Mua sắm xanh ưu tiên SP thân thiện MT (đã có)

// Giá dịch vụ CTRSH tính theo khối lượng (đã có)

// Thiệt hại MT yêu cầu Bồi thường
MATCH (a:KhaiNiem {id: 'KN042'}), (b:KhaiNiem {id: 'KN082'})
CREATE (a)-[:YEU_CAU {dieu_khoan: 'Điều 130, 133'}]->(b);

// Hoạt động tái chế là trách nhiệm của Nhà sản xuất (EPR)
MATCH (a:KhaiNiem {id: 'KN083'}), (c:ChuThe {id: 'CT010'})
CREATE (c)-[:CO_TRACH_NHIEM {dieu_khoan: 'Điều 54'}]->(a);

// Phân vùng MT là nội dung của Quy hoạch BVMT
MATCH (a:KhaiNiem {id: 'KN080'}), (b:KhaiNiem {id: 'KN004'})
CREATE (a)-[:NOI_DUNG_CUA {dieu_khoan: 'Điều 23, Khoản 4'}]->(b);

// Khoảng cách an toàn bảo vệ Cộng đồng dân cư
MATCH (a:KhaiNiem {id: 'KN081'}), (c:ChuThe {id: 'CT006'})
CREATE (a)-[:BAO_VE {dieu_khoan: 'Điều 53, Khoản 2'}]->(c);

// =============================================================================
// PHẦN D: QUAN HỆ CHÉO GIỮA CÁC NHÓM
// =============================================================================

// --- D1: Công cụ áp dụng cho Chủ thể ---

// GPMT cấp cho Chủ dự án và Cơ sở SXKD
MATCH (k:KhaiNiem {id: 'KN008'}), (c:ChuThe {id: 'CT003'})
CREATE (k)-[:CAP_CHO {dieu_khoan: 'Điều 39'}]->(c);

MATCH (k:KhaiNiem {id: 'KN008'}), (c:ChuThe {id: 'CT004'})
CREATE (k)-[:CAP_CHO]->(c);

// Đăng ký MT áp dụng cho Hộ gia đình, CSSX nhỏ
MATCH (k:KhaiNiem {id: 'KN009'}), (c:ChuThe {id: 'CT005'})
CREATE (k)-[:AP_DUNG_CHO {dieu_khoan: 'Điều 49'}]->(c);

// ĐTM bắt buộc cho Dự án đầu tư (đã có)

// Quan trắc MT thực hiện bởi CQQLNN và Chủ dự án
MATCH (k:KhaiNiem {id: 'KN025'}), (c:CoQuan {id: 'CQ002'})
CREATE (c)-[:TO_CHUC_THUC_HIEN {dieu_khoan: 'Điều 166, Khoản 4'}]->(k);

MATCH (k:KhaiNiem {id: 'KN025'}), (c:ChuThe {id: 'CT003'})
CREATE (c)-[:PHAI_THUC_HIEN {dieu_khoan: 'Điều 111'}]->(k);

// --- D2: Chất thải phát sinh từ Chủ thể ---

// Cơ sở SXKD phát sinh Chất thải
MATCH (c:ChuThe {id: 'CT004'}), (k:KhaiNiem {id: 'KN018'})
CREATE (c)-[:PHAT_SINH]->(k);

// Hộ gia đình phát sinh CTRSH
MATCH (c:ChuThe {id: 'CT005'}), (k:KhaiNiem {id: 'KN019'})
CREATE (c)-[:PHAT_SINH {dieu_khoan: 'Điều 75'}]->(k);

// Khu SXKD tập trung phát sinh nhiều loại chất thải
MATCH (k:KhaiNiem {id: 'KN037'}), (ct:KhaiNiem {id: 'KN018'})
CREATE (k)-[:PHAT_SINH]->(ct);

// --- D3: Công cụ kinh tế áp dụng cho Chất thải ---

// Thuế/phí BVMT áp dụng cho Chất thải
MATCH (k:KhaiNiem {id: 'KN076'}), (ct:KhaiNiem {id: 'KN018'})
CREATE (k)-[:AP_DUNG_CHO {dieu_khoan: 'Điều 136'}]->(ct);

// Kinh tế tuần hoàn giảm khai thác nguyên liệu, giảm chất thải
MATCH (k:KhaiNiem {id: 'KN045'}), (ct:KhaiNiem {id: 'KN018'})
CREATE (k)-[:GIAM {dieu_khoan: 'Điều 142'}]->(ct);

// --- D4: Khu vực và Quản lý ---

// Khu kinh tế có Ban quản lý
MATCH (kv:KhuVuc {id: 'KV001'}), (c:ChuThe {id: 'CT018'})
CREATE (c)-[:QUAN_LY]->(kv);

// Cụm công nghiệp do UBND tỉnh quản lý
MATCH (kv:KhuVuc {id: 'KV002'}), (cq:CoQuan {id: 'CQ005'})
CREATE (cq)-[:QUAN_LY {dieu_khoan: 'Điều 52'}]->(kv);

// --- D5: Sự cố và Ứng phó ---

// Sự cố MT gây Thiệt hại MT
MATCH (a:KhaiNiem {id: 'KN014'}), (b:KhaiNiem {id: 'KN042'})
CREATE (a)-[:GAY_RA {suy_luan: true}]->(b);

// Thiệt hại MT yêu cầu Phục hồi MT
MATCH (a:KhaiNiem {id: 'KN042'}), (b:KhaiNiem {id: 'KN057'})
CREATE (a)-[:YEU_CAU {suy_luan: true}]->(b);

// Bồi thường thiệt hại liên quan đến Thiệt hại MT
MATCH (a:KhaiNiem {id: 'KN082'}), (b:KhaiNiem {id: 'KN042'})
CREATE (a)-[:AP_DUNG_CHO]->(b);

// =============================================================================
// PHẦN E: QUAN HỆ ĐẶC BIỆT - CHUỖI GIÁ TRỊ VÀ QUY TRÌNH
// =============================================================================

// --- E1: Chuỗi quy trình ĐTM (đã có GiaiDoan, bổ sung quan hệ) ---

// Dự án -> PEIA -> ĐTM -> Thẩm định -> GPMT -> Vận hành
MATCH (d:DuAn {nhom: 'I'}), (p:KhaiNiem {id: 'KN006'})
CREATE (d)-[:BAT_DAU_VOI]->(p);

// --- E2: Chuỗi quản lý chất thải ---

// Phát sinh -> Phân loại -> Thu gom -> Vận chuyển -> Xử lý/Tái chế
CREATE (quy001:QuyTrinh {id: 'QT001', ten: 'Quy trình quản lý chất thải', mo_ta: 'Từ phát sinh đến xử lý cuối cùng'});

// --- E3: Chuỗi kinh tế các-bon ---

// Kiểm kê KNK -> Phân bổ hạn ngạch -> Giao dịch thị trường -> Giảm phát thải
CREATE (quy002:QuyTrinh {id: 'QT002', ten: 'Quy trình quản lý các-bon', mo_ta: 'Từ kiểm kê đến giao dịch thị trường'});

// --- E4: Chuỗi EPR ---

// Sản xuất -> Tiêu dùng -> Thải bỏ -> Thu hồi -> Tái chế
CREATE (quy003:QuyTrinh {id: 'QT003', ten: 'Trách nhiệm mở rộng của nhà sản xuất', dieu_khoan: 'Điều 54', mo_ta: 'Vòng đời sản phẩm từ sản xuất đến tái chế'});

// =============================================================================
// PHẦN F: QUERY MẪU CHO CẤU TRÚC MỚI
// =============================================================================

// --- Query 1: Tìm tất cả nodes theo nhóm GSheet ---
// MATCH (n)
// WHERE n.id_gsheet IS NOT NULL
// RETURN n.id_gsheet, n.ten, labels(n)[0] AS loai
// ORDER BY n.id_gsheet;

// --- Query 2: Tìm quan hệ giữa các nhóm ---
// MATCH (a)-[r]->(b)
// WHERE labels(a)[0] <> labels(b)[0]
// RETURN labels(a)[0] AS nhom_1, type(r) AS quan_he, labels(b)[0] AS nhom_2, count(*) AS so_luong
// ORDER BY so_luong DESC;

// --- Query 3: Phân tích chuỗi giá trị từ Dự án đến Vận hành ---
// MATCH path = (d:DuAn)-[*1..5]->(k:KhaiNiem)
// WHERE k.ten CONTAINS 'Vận hành'
// RETURN [n IN nodes(path) | n.ten] AS chuoi;

// --- Query 4: Tìm tất cả công cụ quản lý ---
// MATCH (k:KhaiNiem)
// WHERE k.chuong IN ['II', 'III', 'IV'] OR k.id_gsheet STARTS WITH 'Kế' OR k.id_gsheet STARTS WITH 'Quy'
// RETURN k.ten, k.dieu_khoan;

// --- Query 5: Phân tích quan hệ chủ thể - nghĩa vụ ---
// MATCH (c:ChuThe)-[r:CO_NGHIA_VU|PHAI_THUC_HIEN|CO_TRACH_NHIEM]->(target)
// RETURN c.ten AS chu_the, type(r) AS loai_quan_he, target.ten AS doi_tuong, r.dieu_khoan AS can_cu;

// =============================================================================
// KẾT THÚC FILE BỔ SUNG TỪ GSHEET
// =============================================================================
