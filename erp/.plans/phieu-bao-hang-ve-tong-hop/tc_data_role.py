# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Tong hop phieu bao hang ve'
(menu Kinh doanh > Thong bao > Phieu bao hang ve)."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn \"Tổng hợp phiếu báo hàng về\" gom phiếu báo hàng về của cả 3 luồng mua hàng vào một chỗ để "
     "bộ phận kinh doanh / kho theo dõi hàng sắp về. Màn có 3 tab:\n"
     "- Nhập khẩu: phiếu báo hàng về của luồng mua hàng nhập khẩu (theo Invoice).\n"
     "- Trong nước: phiếu báo hàng về của luồng mua trong nước theo hãng.\n"
     "- Mua ngoài: phiếu báo hàng về của luồng mua ngoài (hợp đồng mua ngoài / phụ lục).\n"
     "Người dùng làm được: xem danh sách từng tab, lọc, bấm Mã để mở chi tiết phiếu, bấm Hợp đồng / "
     "Invoice để mở chứng từ gốc. Riêng tab Nhập khẩu có thêm menu hành động: In, Xuất Excel, Xóa.\n"
     "Màn KHÔNG có chức năng tạo phiếu - phiếu được lập ở màn của từng luồng mua hàng."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có 2 trạng thái, dùng chung cho cả 3 tab:\n"
     "- \"Đã gửi\" (nhãn ĐỎ): phiếu vừa lập xong, đã gửi thông báo, chưa lập yêu cầu nhập hàng.\n"
     "- \"Đã yêu cầu nhập hàng\" (nhãn XANH): đã lập yêu cầu nhập hàng từ phiếu.\n"
     "Phạm vi từng tab:\n"
     "- Tab Nhập khẩu: theo 3 quyền xem ở mục 7. Không có quyền nào thì thấy phiếu do chính mình lập + "
     "phiếu có hàng thuộc hãng / nhà sản xuất mà mình đang được phân công phụ trách mua (phân công còn "
     "hiệu lực, trong công ty mình).\n"
     "- Tab Trong nước: MỌI phiếu của mọi người, mọi công ty.\n"
     "- Tab Mua ngoài: MỌI phiếu của mọi người, mọi công ty."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Tab Nhập khẩu: phiếu ở trạng thái \"Đã yêu cầu nhập hàng\" của NGƯỜI KHÁC luôn bị ẩn, kể cả với "
     "người có quyền xem theo tổng công ty; phiếu \"Đã yêu cầu nhập hàng\" của chính mình vẫn hiện.\n"
     "- Tab Trong nước và Mua ngoài: KHÔNG có cột Hành động (không In, không Xuất Excel, không Tạo yêu "
     "cầu nhập hàng tại màn này).\n"
     "- Tab Nhập khẩu: mục Xóa chỉ hiện khi phiếu ở \"Đã gửi\" VÀ người đăng nhập là người lập.\n"
     "- Tab Trong nước: KHÔNG có ô Từ ngày / Đến ngày.\n"
     "- Tab Nhập khẩu và Trong nước: KHÔNG có ô Công ty / Phòng ban.\n"
     "- Màn không có nút Tạo mới, không có Xuất Excel danh sách, không có Import."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- Tab Nhập khẩu và Mua ngoài có ô \"Từ ngày\" / \"Đến ngày\" lọc theo NGÀY TẠO phiếu (cột Ngày tạo). "
     "Hai đầu mút tính trọn ngày: phiếu tạo trong chính ngày điền ở Đến ngày vẫn được lấy.\n"
     "- Tab Trong nước: không có lọc thời gian.\n"
     "- Không lọc theo ngày dự kiến hàng về."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Mỗi tab là một danh sách phẳng, mỗi dòng 1 phiếu.\n"
     "- Mã phiếu dạng \"PBHV-\" + 5 chữ số. Lưu ý: 3 luồng đánh số RIÊNG nên có thể có 2 phiếu cùng mã ở "
     "2 tab khác nhau - khi trao đổi phải nói rõ tab.\n"
     "- Tab Nhập khẩu: Hợp đồng và Nhà cung cấp lấy từ Invoice của phiếu.\n"
     "- Tab Mua ngoài: Hợp đồng là hợp đồng mua ngoài hoặc phụ lục hợp đồng; cột Nhà cung cấp hiển thị "
     "dạng \"<Mã hợp đồng / phụ lục> - <Tên nhà cung cấp>\".\n"
     "- Cột Kho để trống nếu phiếu không gắn kho."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Không cộng dồn: mỗi phiếu 1 dòng.\n"
     "- Tab Nhập khẩu: một phiếu thỏa nhiều điều kiện phạm vi (vừa do mình lập, vừa có hàng nhiều hãng "
     "mình phụ trách) vẫn chỉ hiện 1 dòng.\n"
     "- Mặc định sắp xếp phiếu mới tạo lên đầu ở cả 3 tab."),

    ("7. Phân quyền cấp",
     "Màn không có quyền riêng: mục menu luôn hiện, mọi tài khoản mở được.\n"
     "Tab Nhập khẩu dùng 3 quyền xem (ưu tiên từ trên xuống, có quyền trên thì bỏ qua quyền dưới):\n"
     "- \"Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty\": mọi phiếu.\n"
     "- \"Xem phiếu báo hàng về mua nhập khẩu theo công ty\": phiếu thuộc công ty của mình.\n"
     "- \"Xem phiếu báo hàng về mua nhập khẩu theo phòng ban\": phiếu thuộc các phòng ban mình được "
     "phân công quản lý (trong công ty mình).\n"
     "- Không có quyền nào: phiếu mình lập + phiếu có hàng thuộc hãng mình phụ trách mua.\n"
     "Tab Trong nước và Mua ngoài KHÔNG áp quyền xem nào (các quyền \"Xem phiếu báo hàng về mua trong "
     "nước theo tổng công ty / theo công ty / theo phòng ban\" KHÔNG có tác dụng ở màn này).\n"
     "Tab Mua ngoài luôn hiện ô lọc Công ty và Phòng ban cho mọi người."),

    ("8. Cách tính các ô thống kê",
     "Không có ô thống kê.\n"
     "- Dòng \"Hiển thị a đến b của N mục\" dưới mỗi bảng: N là tổng phiếu khớp phạm vi + bộ lọc của tab "
     "đó.\n"
     "- Cột STT đánh liên tục qua các trang (trang 2 bắt đầu từ 11).\n"
     "- Cột Ngày tạo dạng ngày/tháng/năm."),

    ("9. Ghi chú đọc bảng",
     "- Mỗi tab có khối Bộ lọc, phân trang và ô chọn số dòng riêng; mặc định 10 dòng/trang.\n"
     "- Hệ thống ghi nhớ bộ lọc của từng tab khi mở lại màn trên cùng trình duyệt.\n"
     "- Bẫy 1: tab Nhập khẩu, ô lọc \"Nhà cung cấp\" đang liệt kê TÊN KHO chứ không phải nhà cung cấp.\n"
     "- Bẫy 2: tab Nhập khẩu có ô lọc mang chữ gợi ý \"all_barcodes\" (lọc theo mã vạch hàng).\n"
     "- Bẫy 3: tab Nhập khẩu ẩn phiếu \"Đã yêu cầu nhập hàng\" của người khác - số phiếu ở tab này sẽ ít "
     "hơn ở màn Danh sách báo hàng về của luồng Nhập khẩu.\n"
     "- Bẫy 4: tab Trong nước / Mua ngoài không giới hạn theo quyền - ai cũng thấy hết.\n"
     "- Bẫy 5: Xóa phiếu ở tab Nhập khẩu xong trang chuyển sang trang trắng, phải tự quay lại màn.\n"
     "- Bẫy 6: ô lọc Hợp đồng ở tab Mua ngoài chỉ tìm theo mã hợp đồng mua ngoài, KHÔNG tìm theo mã phụ "
     "lục.\n"
     "- Nhóm TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),
]

ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem nào - tab Nhập khẩu", "P0",
     "NV-A không có 3 quyền xem phiếu báo hàng về mua nhập khẩu\n"
     "NV-A lập 3 phiếu nhập khẩu (2 Đã gửi, 1 Đã yêu cầu nhập hàng)\n"
     "NV-A đang được phân công phụ trách mua hãng H1; có 2 phiếu của người khác chứa hàng hãng H1, trạng "
     "thái Đã gửi\n"
     "Hệ thống có tổng 550 phiếu nhập khẩu",
     "1. Đăng nhập NV-A\n"
     "2. Vào menu Kinh doanh > Thông báo > bấm \"Phiếu báo hàng về\"\n"
     "3. Ở tab Nhập khẩu, đọc tổng số dòng",
     "Tài khoản: NV-A",
     "- Màn mở được, tiêu đề \"Tổng hợp phiếu báo hàng về\", tab Nhập khẩu đang chọn\n"
     "- Tổng = 5 (3 phiếu của mình + 2 phiếu có hàng hãng H1)\n"
     "- Không thấy phiếu nào khác"),

    ("01", "Quyền xem theo tổng công ty - tab Nhập khẩu", "P0",
     "Tài khoản B có quyền \"Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty\"\n"
     "Hệ thống có 19 phiếu Đã gửi (nhiều công ty) và 531 phiếu Đã yêu cầu nhập hàng, B không lập phiếu nào",
     "1. Đăng nhập B, mở màn\n"
     "2. Ở tab Nhập khẩu đọc tổng\n"
     "3. Lọc Trạng thái = Đã yêu cầu nhập hàng",
     "Quyền: Xem phiếu báo hàng về mua nhập khẩu theo tổng công ty",
     "- Bước 2: tổng = 19, gồm phiếu của mọi công ty\n"
     "- Bước 3: không có dòng nào\n"
     "- Lưu ý: phiếu Đã yêu cầu nhập hàng của người khác luôn bị ẩn ở tab này"),

    ("02", "Quyền xem theo công ty - tab Nhập khẩu", "P0",
     "Tài khoản C có quyền \"Xem phiếu báo hàng về mua nhập khẩu theo công ty\", thuộc Công ty 1\n"
     "Công ty 1 có 12 phiếu Đã gửi; Công ty 3 có 7 phiếu Đã gửi",
     "1. Đăng nhập C, mở màn, ở tab Nhập khẩu đọc tổng",
     "Quyền: theo công ty",
     "- Tổng = 12\n"
     "- Không có phiếu của Công ty 3"),

    ("03", "Quyền xem theo phòng ban - tab Nhập khẩu", "P0",
     "Tài khoản D có quyền \"Xem phiếu báo hàng về mua nhập khẩu theo phòng ban\", được phân công quản lý "
     "phòng MH1 và MH2; 2 phòng có 6 phiếu Đã gửi",
     "1. Đăng nhập D, mở màn, ở tab Nhập khẩu đọc tổng",
     "Quyền: theo phòng ban",
     "- Tổng = 6, chỉ phiếu thuộc MH1, MH2\n"
     "- Lưu ý: chỉ tính phòng ban được phân công quản lý, không tự tính phòng ban của bản thân nếu không "
     "được phân công"),

    ("04", "Có nhiều quyền: quyền cao nhất được áp dụng", "P1",
     "Tài khoản E có cả quyền theo công ty và theo phòng ban",
     "1. Đăng nhập E, mở tab Nhập khẩu, đọc tổng",
     "—",
     "- Kết quả giống như chỉ có quyền theo công ty"),

    ("05", "Quyền xem phiếu trong nước không có tác dụng ở tab Trong nước", "P0",
     "Tài khoản F KHÔNG có quyền xem phiếu báo hàng về mua trong nước nào\n"
     "Hệ thống có 20 phiếu trong nước của nhiều người, nhiều công ty",
     "1. Đăng nhập F, mở màn\n"
     "2. Bấm tab Trong nước, đọc tổng",
     "—",
     "- Tổng = 20 (thấy mọi phiếu)\n"
     "- Lưu ý: tab này không giới hạn theo quyền - ghi nhận nếu nghiệp vụ yêu cầu giới hạn"),

    ("06", "Tab Mua ngoài không giới hạn theo quyền", "P0",
     "Tài khoản F không có quyền nào\n"
     "Hệ thống có 747 phiếu mua ngoài của nhiều công ty",
     "1. Đăng nhập F, bấm tab Mua ngoài, đọc tổng\n"
     "2. Bấm Bộ lọc, quan sát các ô",
     "—",
     "- Tổng = 747\n"
     "- Khối lọc có ô Công ty và Phòng ban dù F không có quyền xem theo cấp nào"),

    ("07", "Gọi thẳng chức năng Xóa phiếu nhập khẩu của người khác", "P0",
     "Tài khoản F (không phải người lập) và phiếu PBHV-00010 tab Nhập khẩu do NV-A lập, trạng thái Đã gửi",
     "1. Đăng nhập F\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa phiếu PBHV-00010, bỏ qua giao diện\n"
     "3. Đăng nhập NV-A, mở tab Nhập khẩu",
     "Phiếu: PBHV-00010",
     "- Kỳ vọng nghiệp vụ: hệ thống từ chối, phiếu vẫn còn\n"
     "- Lưu ý: chức năng Xóa hiện không tự kiểm tra người lập / trạng thái - nếu phiếu bị xóa thì ghi "
     "nhận lỗ hổng phân quyền"),

    ("08", "Gọi thẳng chức năng Xóa phiếu đã yêu cầu nhập hàng", "P1",
     "Phiếu PBHV-00020 tab Nhập khẩu do NV-A lập, trạng thái Đã yêu cầu nhập hàng",
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa phiếu PBHV-00020",
     "—",
     "- Kỳ vọng nghiệp vụ: hệ thống từ chối vì phiếu đã lập yêu cầu nhập hàng\n"
     "- Ghi nhận lỗi nếu phiếu bị xóa"),
]
