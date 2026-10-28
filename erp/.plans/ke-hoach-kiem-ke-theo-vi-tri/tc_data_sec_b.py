# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua / xem chi tiet."""

KHO = ("Kho K1 có: nhà N1 (dãy D1 > khoang KG1 > vị trí P1, P2, P3), nhà N2 (dãy D2 > khoang KG2 > vị "
       "trí P4); vị trí tự do PT1 không thuộc khoang")

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "Tài khoản bất kỳ",
     "1. Mở màn từ menu, bấm nút Tạo mới\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Khối \"Thông tin chung\": ô Ngày kiểm kê = ngày hôm nay, bị khóa; ô \"Kho vật lý\" hiện chữ "
     "\"Chọn kho kiểm\"\n"
     "- 4 khung Nhà, Dãy, Khoang, Vị trí đều có dấu (*), mỗi khung có ô tìm và ô tích \"Chọn hết\"\n"
     "- Nút \"Lấy vị trí\" ở cuối khối\n"
     "- Khối \"Chi tiết\" có 2 tab: \"Vị trí (*)\" và \"Hội đồng kiểm kê (*)\"; tab Vị trí hiện \"Chưa có "
     "dữ liệu\", tab Hội đồng hiện \"Chưa có thành viên\"\n"
     "- Cuối trang: Lưu, Lưu & Gửi, Quay lại"),

    ("002", "Ô Kho vật lý chỉ chọn được 1 kho", "P0",
     "Hệ thống có kho K1 (mã K1, tên Kho Hà Nội) và K2",
     "1. Mở ô Kho vật lý, chọn K1\n"
     "2. Mở lại, chọn K2",
     "Kho vật lý: K1 rồi K2",
     "- Lựa chọn hiển thị dạng \"mã - tên\", ví dụ \"K1 - Kho Hà Nội\"\n"
     "- Chọn K2 thì thay thế K1, không chọn được cùng lúc 2 kho"),

    ("003", "Chọn kho thì khung Nhà và vị trí tự do hiện ra", "P0",
     KHO,
     "1. Chọn Kho vật lý = K1\n"
     "2. Quan sát khung Nhà và khung Vị trí",
     "Kho vật lý: K1",
     "- Khung Nhà: tiêu đề \"K1 - Kho Hà Nội\" kèm ô \"chọn hết\", bên dưới là N1, N2\n"
     "- Khung Vị trí: dưới tên kho có sẵn PT1 (vị trí tự do)"),

    ("004", "Tích Nhà thì khung Dãy hiện dãy của nhà đó", "P0",
     KHO,
     "1. Chọn kho K1, tích nhà N1",
     "Nhà: N1",
     "- Khung Dãy: nhóm \"mã - tên N1\" với dãy D1\n"
     "- Không có D2"),

    ("005", "Tích Dãy, Khoang thì khung Vị trí hiện vị trí theo nhóm", "P0",
     KHO,
     "1. Tích N1 > D1 > KG1\n"
     "2. Quan sát khung Khoang và khung Vị trí",
     "—",
     "- Khung Khoang: nhóm ghi \"N1 | D1\" có KG1\n"
     "- Khung Vị trí: nhóm ghi \"N1 | D1 | KG1\" có P1, P2, P3, kèm ô \"chọn hết\""),

    ("006", "Chọn hết ở đầu khung Nhà", "P1",
     KHO,
     "1. Chọn kho K1\n"
     "2. Tích \"Chọn hết\" ở đầu khung Nhà\n"
     "3. Bỏ tích lại",
     "—",
     "- Bước 2: N1, N2 đều được tích, khung Dãy hiện D1, D2\n"
     "- Bước 3: N1, N2 bỏ tích, khung Dãy trống"),

    ("007", "Chọn hết theo từng nhóm và chọn hết toàn khung Vị trí", "P1",
     KHO,
     "1. Tích N1, N2 > D1, D2 > KG1, KG2\n"
     "2. Tích \"chọn hết\" của nhóm KG1\n"
     "3. Tích \"Chọn hết\" ở đầu khung Vị trí",
     "—",
     "- Bước 2: P1, P2, P3 được tích, P4 và PT1 chưa\n"
     "- Bước 3: P1 đến P4 và PT1 đều được tích"),

    ("008", "Bỏ tích cấp trên thì cấp dưới bị bỏ theo", "P0",
     KHO,
     "1. Tích N1 > D1 > KG1 > P1, P2\n"
     "2. Bỏ tích N1",
     "—",
     "- D1, KG1 biến mất khỏi khung Dãy, Khoang\n"
     "- P1, P2 không còn được tích; PT1 (vị trí tự do) giữ nguyên trạng thái"),

    ("009", "Đổi kho thì phạm vi của kho cũ bị bỏ", "P0",
     KHO + "\nKho K2 có nhà N9",
     "1. Chọn K1, tích N1, PT1\n"
     "2. Đổi Kho vật lý sang K2",
     "Kho vật lý: K1 rồi K2",
     "- Khung Nhà chỉ còn N9, N1 không còn được tích\n"
     "- PT1 không còn trong khung Vị trí"),

    ("010", "Ô tìm nhà theo tên hoặc mã", "P2",
     KHO,
     "1. Chọn K1\n"
     "2. Gõ \"N2\" vào ô \"tên hoặc mã nhà\"",
     "Tìm nhà: N2",
     "- Khung Nhà chỉ còn N2\n"
     "- Xóa chữ đã gõ thì N1, N2 hiện lại"),

    ("011", "Ô tìm dãy không làm mất dãy đã tích", "P1",
     "Kho K1, nhà N1 có dãy D1, D3, D5; đã tích D1",
     "1. Gõ \"D\" vào ô \"tên hoặc mã dãy\"\n"
     "2. Quan sát dấu tích của D1",
     "Tìm dãy: D",
     "- Mong đợi: D1 vẫn được tích\n"
     "- Lưu ý: code hiện tại có nguy cơ bỏ tích các dãy đã chọn khi kết quả tìm có từ 2 dãy trở lên "
     "(tương tự ở ô tìm khoang) — nếu mất tích thì ghi Failed"),

    ("012", "Bấm Lấy vị trí khi chưa tích vị trí nào", "P0",
     "Đã chọn kho K1, tích N1, chưa tích vị trí",
     "1. Bấm \"Lấy vị trí\"",
     "—",
     "- Hiện cảnh báo vàng \"Chưa chọn đủ thông tin vị trí!\"\n"
     "- Bảng chi tiết không đổi"),

    ("013", "Lấy vị trí hiện tồn chi tiết theo hàng, công ty, lô", "P0",
     "Vị trí P1 có hàng HH-0091 (ĐVT Cái) tồn 30: công ty TPE lô L01 = 10, lô L02 = 15; công ty ENE "
     "lô L07 = 5",
     "1. Tích P1, bấm \"Lấy vị trí\"\n"
     "2. Đọc tab Vị trí",
     "Vị trí: P1",
     "- Hiện thông báo xanh \"Thành công\"\n"
     "- Bảng có cột: STT, Nhà Kho, Vị trí, Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, và nhóm "
     "\"Chi tiết tồn theo công ty\" gồm Công ty, Lô, SL, Cộng\n"
     "- Nhà Kho = mã nhà N1, Vị trí = P1, SL tồn = 30\n"
     "- Công ty TPE: L01 = 10, L02 = 15, Cộng = 25\n"
     "- Công ty ENE: L07 = 5, Cộng = 5"),

    ("014", "Vị trí không có tồn bị loại khỏi bảng", "P0",
     "P2 có tồn, P3 trống (tồn 0)",
     "1. Tích P2, P3, bấm \"Lấy vị trí\"\n"
     "2. Bỏ tích P2, chỉ giữ P3, bấm \"Lấy vị trí\" lại",
     "—",
     "- Bước 1: bảng chỉ có P2\n"
     "- Bước 2: bảng hiện \"Chưa có dữ liệu\""),

    ("015", "Lô đã hết tồn không hiện", "P1",
     "Vị trí P1 có hàng HH-0091: lô L01 = 10, lô L03 = 0",
     "1. Tích P1, bấm \"Lấy vị trí\"",
     "—",
     "- Chỉ có lô L01, KHÔNG có dòng lô L03"),

    ("016", "Thêm thành viên Hội đồng kiểm kê", "P0",
     "Nhân viên NV-K (phòng KHO) có 2 vai trò: Thủ kho, Kế toán kho",
     "1. Mở tab \"Hội đồng kiểm kê\", bấm dấu + ở góc phải tiêu đề bảng\n"
     "2. Ở ô \"Chọn thành viên\" gõ tìm NV-K, chọn\n"
     "3. Mở ô Chức vụ",
     "Thành viên: NV-K",
     "- Thêm 1 dòng, STT = 1\n"
     "- Lựa chọn thành viên dạng \"Họ tên - mã phòng ban\", ví dụ \"Nguyễn Văn K - KHO\"\n"
     "- Chức vụ TỰ ĐIỀN vai trò đầu tiên của NV-K\n"
     "- Ô Chức vụ chỉ có 2 lựa chọn: Thủ kho, Kế toán kho"),

    ("017", "Danh sách thành viên gồm nhân viên mọi công ty", "P2",
     "Hệ thống có nhân viên đang làm của công ty 1 và công ty 3; NV-Q đã nghỉ việc",
     "1. Mở ô \"Chọn thành viên\", tìm nhân viên công ty khác, tìm NV-Q",
     "—",
     "- Tìm được nhân viên của công ty khác\n"
     "- KHÔNG tìm được NV-Q (đã nghỉ)"),

    ("018", "Bớt thành viên", "P1",
     "Tab Hội đồng có 3 dòng",
     "1. Bấm dấu - (đỏ) ở dòng 2",
     "—",
     "- Còn 2 dòng, STT đánh lại 1, 2\n"
     "- Bớt hết thì hiện \"Chưa có thành viên\""),

    ("019", "Bấm Lưu tạo kế hoạch nháp", "P0",
     "NV-A thuộc công ty mã TPE\n"
     "Đã chọn K1, tích P1, Lấy vị trí, thêm 2 thành viên",
     "1. Bấm \"Lưu\"\n"
     "2. Tìm kế hoạch vừa tạo trên danh sách",
     "—",
     "- Thông báo xanh \"Tạo thành công\", tự về danh sách lối vào menu\n"
     "- Kế hoạch mới ở đầu bảng, Số phiếu dạng TPE-KHKKVT-<5 chữ số>\n"
     "- Ngày kiểm kê = hôm nay, Kho = K1, Trạng thái = Đang tạo (đỏ), Người lập = NV-A"),

    ("020", "Bấm Lưu & Gửi chuyển thẳng sang Đang kiểm", "P0",
     "Như TC_04.019",
     "1. Bấm \"Lưu & Gửi\"",
     "—",
     "- Thông báo \"Tạo thành công\", về danh sách\n"
     "- Trạng thái = Đang kiểm (vàng)\n"
     "- Menu bánh răng của người lập không còn Sửa, Xóa"),

    ("021", "Lưu & Gửi gửi thông báo đúng người", "P0",
     "NV-A thuộc công ty 1, lập kế hoạch kho K1\n"
     "TK1: công ty 1, quyền Lập phiếu, thủ kho K1\n"
     "TK3: công ty 1, thủ kho K1, KHÔNG có quyền Lập phiếu\n"
     "TK4: công ty 3, quyền Lập phiếu, thủ kho K1\n"
     "TK2: công ty 1, quyền Lập phiếu, thủ kho K2",
     "1. NV-A bấm \"Lưu & Gửi\"\n"
     "2. Lần lượt đăng nhập TK1, TK2, TK3, TK4, xem chuông thông báo",
     "—",
     "- CHỈ TK1 nhận \"Bạn có 1 phiếu kế hoạch kiểm kê kho cần duyệt\"\n"
     "- Bấm thông báo mở đúng màn Chi tiết kế hoạch\n"
     "- TK2, TK3, TK4 không nhận"),

    ("022", "Bấm Lưu không gửi thông báo", "P1",
     "Như TC_04.021",
     "1. NV-A bấm \"Lưu\"\n"
     "2. Đăng nhập TK1 xem chuông thông báo",
     "—",
     "- TK1 KHÔNG nhận thông báo nào"),

    ("023", "Chi tiết hiện đúng số liệu đã chụp lúc lưu", "P0",
     "Kế hoạch KH-9 lưu khi P1 có HH-0091 tồn 30\n"
     "Sau đó kho xuất 5 cái HH-0091 khỏi P1 (tồn còn 25)",
     "1. Mở Chi tiết KH-9",
     "—",
     "- SL tồn vẫn = 30, các lô giữ số cũ\n"
     "- Tồn thay đổi sau khi lưu KHÔNG làm đổi kế hoạch"),

    ("024", "Mở Sửa thì hệ thống tự lấy lại tồn hiện tại", "P0",
     "Kế hoạch KH-10 Đang tạo, lưu khi P1 tồn 30; nay P1 tồn 25",
     "1. NV-A bấm bánh răng > Sửa trên KH-10\n"
     "2. Quan sát phần phạm vi và bảng chi tiết",
     "—",
     "- Tiêu đề trang: \"Kế hoạch kiểm kê theo vị trí: <Số phiếu>\"\n"
     "- Kho, nhà, dãy, khoang, vị trí đã tích được giữ nguyên\n"
     "- Bảng chi tiết tự tải lại, SL tồn = 25 (tồn hiện tại)\n"
     "- Lưu ý: đúng thiết kế, không ghi Failed"),

    ("025", "Sửa kế hoạch nháp rồi bấm Lưu", "P0",
     "KH-10 Đang tạo có 2 thành viên",
     "1. Mở Sửa KH-10, thêm 1 thành viên, tích thêm P2, bấm \"Lấy vị trí\"\n"
     "2. Bấm \"Lưu\"\n"
     "3. Mở Chi tiết KH-10",
     "—",
     "- Thông báo \"Tạo thành công\" (Lưu ý: nhãn chưa đổi thành \"Cập nhật\", ghi nhận)\n"
     "- Số phiếu giữ nguyên, trạng thái vẫn Đang tạo\n"
     "- Chi tiết có 3 thành viên, có thêm P2"),

    ("026", "Sửa kế hoạch nháp rồi bấm Lưu & Gửi", "P0",
     "KH-10 Đang tạo, kho K1; TK1 là thủ kho K1 có quyền Lập phiếu",
     "1. Mở Sửa KH-10, bấm \"Lưu & Gửi\"\n"
     "2. Đăng nhập TK1",
     "—",
     "- KH-10 chuyển Đang kiểm\n"
     "- TK1 nhận \"Bạn có 1 phiếu kế hoạch kiểm kê kho cần duyệt\""),

    ("027", "Quay lại không lưu dữ liệu", "P2",
     "Đang ở màn Tạo mới, đã chọn kho và Lấy vị trí",
     "1. Bấm \"Quay lại\"",
     "—",
     "- Về danh sách, KHÔNG có kế hoạch mới nào được tạo"),

    ("028", "Bấm Lưu liên tiếp không sinh 2 kế hoạch", "P1",
     "Dữ liệu hợp lệ như TC_04.019",
     "1. Bấm \"Lưu\" 2 lần thật nhanh",
     "—",
     "- Sau lần bấm đầu, 2 nút Lưu và Lưu & Gửi bị khóa, có biểu tượng quay\n"
     "- Chỉ 1 kế hoạch được tạo"),

    ("029", "Tiền tố Số phiếu theo công ty người lập, không theo công ty của kho", "P1",
     "NV-E thuộc công ty mã ENE, lập kế hoạch cho kho K1 của công ty TPE",
     "1. NV-E tạo và Lưu kế hoạch",
     "—",
     "- Số phiếu bắt đầu bằng ENE-KHKKVT-"),

    ("030", "Kế hoạch có nhiều vị trí, có vị trí tự do", "P1",
     KHO + "\nP1, P4, PT1 đều có tồn",
     "1. Chọn K1, tích N1, N2 > D1, D2 > KG1, KG2 > P1, P4, và PT1\n"
     "2. Bấm \"Lấy vị trí\", thêm thành viên, bấm \"Lưu\"\n"
     "3. Mở Chi tiết",
     "—",
     "- Bảng có 3 vị trí P1, P4, PT1, STT 1 đến 3\n"
     "- Cột Nhà Kho của PT1 để trống (vị trí tự do không thuộc nhà)"),
]
