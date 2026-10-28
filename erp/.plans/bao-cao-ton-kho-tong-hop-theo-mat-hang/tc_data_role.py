# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao ton kho tong hop theo mat hang'."""

MENU = "Mở menu Kho > mục \"Báo cáo kho\" > bấm \"Báo cáo tồn kho tổng hợp theo mặt hàng\""

# Du lieu mau dung chung
H1 = ("Công ty TPE có kho K1 (công ty thuê kho TPE, TPC) và kho K2 (công ty thuê kho TPE).\n"
      "Hàng H1 (ĐVT Cái, thêm ĐVT Thùng hệ số 12) đang tồn: K1 của TPE = 30, K1 của TPC = 12, K2 của TPE = 8\n"
      "Hàng H2 đã xuất hết (tồn 0)")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo tồn kho tổng hợp theo mặt hàng: cho biết tính đến một ngày, mỗi mặt hàng còn tồn bao "
     "nhiêu trên một hoặc nhiều kho, cộng gộp các kho; người có quyền xem theo tổng công ty thấy thêm cột "
     "chi tiết theo từng Công ty thuê kho.\n"
     "Người dùng làm được: lọc theo kho (hoặc xem toàn bộ kho), công ty thuê kho, nhóm / tính chất / loại "
     "hàng, thương hiệu, hãng sản xuất, hàng hóa, hợp đồng; đổi đơn vị tính từng hàng; Xuất Excel đầy đủ "
     "hoặc ngắn gọn. Màn chỉ xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mặt hàng có tổng tồn khác 0 trên các kho đã chọn, chỉ tính phần tồn của các Công ty thuê kho đang "
     "chọn, tới hết ngày ở ô \"Tính đến ngày\".\n"
     "- Mặc định tích \"Xem toàn bộ kho\": chọn sẵn mọi kho của công ty ở ô Tồn theo công ty.\n"
     "- Cột Chi tiết: mỗi Công ty thuê kho 1 cột (mã công ty, rê chuột hiện tên), số là tổng tồn của công "
     "ty đó trên các kho đã chọn; bằng 0 hiện \"-\". Chỉ hiện với quyền xem theo tổng công ty.\n"
     "- Sắp theo tên hàng A đến Z, 20 hàng mỗi trang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Hàng có tổng tồn bằng 0.\n"
     "- Kho không thuộc công ty đang chọn ở ô Tồn theo công ty.\n"
     "- Công ty thuê kho bị bỏ chọn.\n"
     "- Không có nút In (đã ẩn)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Chỉ có 1 ô \"Tính đến ngày\" (bắt buộc, mặc định hôm nay): tồn tính tới hết ngày này theo thời điểm "
     "ghi nhận nhập / xuất vào kho."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Tính đến ngày, Nhóm hàng hóa, Tính chất hàng hóa, Loại hàng hóa, Thương hiệu, Hãng sản xuất, "
     "Hàng hóa (có nút x), Hợp đồng, Tồn theo công ty, ô tích \"Xem toàn bộ kho\", Kho (chọn nhiều, bắt "
     "buộc), Công ty thuê kho (tự chọn hết theo kho); nút Xuất excel, Lọc, làm mới.\n"
     "Bảng: STT, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT (chọn được), SL tồn, Chi tiết theo Công "
     "ty thuê kho."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL tồn = tổng các cột Chi tiết (gồm cả số âm).\n"
     "- Mỗi cột Chi tiết cộng gộp mọi kho đã chọn của cùng một công ty thuê kho.\n"
     "- Đổi ĐVT: số chia cho hệ số; cột Chi tiết giữ 2 chữ số lẻ, SL tồn làm tròn số nguyên. ĐVT đã đổi được "
     "giữ khi lọc lại và khi xuất Excel.\n"
     "Với dữ liệu mẫu H1, chọn K1 và K2: SL tồn 50, cột TPE 38, cột TPC 12."),

    ("7. Phân quyền cấp",
     "- Mở màn và Xuất Excel cần một trong 3 quyền: \"Xem báo cáo tồn kho theo tổng công ty\", \"... theo "
     "công ty\", \"... theo kho\"; không có thì ra trang không tìm thấy.\n"
     "- Quyền theo tổng công ty: ô Tồn theo công ty có mọi công ty và bảng có cột Chi tiết theo công ty "
     "thuê kho.\n"
     "- Quyền theo kho hiện được xem mọi kho của công ty như quyền theo công ty.\n"
     "- Chức năng lấy dữ liệu khi bấm Lọc KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang 20 hàng, STT liên tục.\n"
     "- Xuất Excel: dưới 500 hàng thì tải ngay; từ 500 hàng thì gửi email, báo \"Báo cáo tồn kho tổng hợp "
     "sẽ gửi về mail của bạn trong ít phút!\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- File Excel đầy đủ có cột Chi tiết theo công ty thuê kho kể cả khi người xuất KHÔNG có quyền tổng "
     "công ty (trên màn bị ẩn).\n"
     "- SL tồn làm tròn số nguyên khi đổi ĐVT (50 Cái hiện 4 Thùng thay vì 4,17), trong khi cột Chi tiết "
     "hiện 2 số lẻ nên tổng các cột không khớp SL tồn.\n"
     "- Nút làm mới đảo trạng thái ô \"Xem toàn bộ kho\" (đang tích thành bỏ tích và ngược lại).\n"
     "- Gọi thẳng chức năng lấy dữ liệu không cần quyền."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem báo cáo tồn kho thì không mở được màn", "P0",
     "NV-A không có quyền nào trong 3 quyền xem báo cáo tồn kho",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy"),

    ("01", "Quyền theo công ty mở được màn, không có cột Chi tiết", "P0",
     "KT-1 có quyền \"Xem báo cáo tồn kho theo công ty\", thuộc TPE\n" + H1,
     "1. Đăng nhập KT-1, mở màn từ menu\n"
     "2. Bấm Lọc",
     "—",
     "- Ô Tồn theo công ty chỉ có TPE\n"
     "- Bảng có H1 SL tồn 50 nhưng KHÔNG có nhóm cột Chi tiết"),

    ("02", "Quyền theo tổng công ty thấy cột Chi tiết", "P0",
     "KT-2 có quyền \"Xem báo cáo tồn kho theo tổng công ty\"\n" + H1,
     "1. Đăng nhập KT-2, chọn Tồn theo công ty TPE, bấm Lọc",
     "—",
     "- Ô Tồn theo công ty có mọi công ty\n"
     "- Nhóm cột Chi tiết có cột TPE = 38, TPC = 12 cho H1"),

    ("03", "Quyền theo kho chỉ nên thấy kho được phân", "P1",
     "TK-3 có quyền \"Xem báo cáo tồn kho theo kho\", thuộc TPE, chỉ được phân K1",
     "1. Đăng nhập TK-3, mở ô Kho",
     "—",
     "- Mong đợi: chỉ có K1\n"
     "- Lưu ý: nếu có cả K2 (đã chọn sẵn) thì ghi Failed"),

    ("04", "Gọi thẳng chức năng lấy dữ liệu khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu báo cáo với kho K1",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả về đủ số liệu - ghi Failed"),

    ("05", "Excel đầy đủ lộ cột Chi tiết khi không có quyền tổng công ty", "P1",
     "KT-1 chỉ có quyền theo công ty\n" + H1,
     "1. KT-1 lọc, Xuất excel đầy đủ",
     "—",
     "- Theo code hiện tại: file có cột TPE, TPC dù trên màn bị ẩn\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu file giống quyền xem trên màn"),

    ("06", "Xuất Excel qua đường dẫn khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho; có sẵn đường dẫn Xuất Excel",
     "1. Đăng nhập NV-A, dán đường dẫn",
     "—",
     "- Ra trang không tìm thấy"),
]
