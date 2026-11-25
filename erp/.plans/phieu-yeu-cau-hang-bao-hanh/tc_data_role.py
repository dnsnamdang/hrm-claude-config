# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu yeu cau hang bao hanh'."""

MENU = "Mở menu Khởi tạo > mục \"Hỏi hàng – đặt hàng – Khiêu nại\" > bấm \"Phiếu Yêu cầu hãng bảo hành\""
MENU_2 = "Mở menu Mua hàng > mục \"Hãng bảo hành\" > bấm \"Phiếu cầu hãng bảo hành\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng PKD1, PKD2; công ty TPC có phòng PKD9.\n"
        "Thương hiệu / hãng sản xuất:\n"
        "- BR-A (hãng HSX-A): tại TPE đã phân công người mua hàng MH-1\n"
        "- BR-B (hãng HSX-B): tại TPE chưa phân công người mua hàng\n"
        "Hàng hóa: H1, H2 thuộc BR-A / HSX-A (ĐVT Cái); H3 thuộc BR-B / HSX-B; H5 thuộc BR-A nhưng hãng HSX-C.\n"
        "Tài khoản:\n"
        "- KD-1, KD-2: nhân viên PKD1, không có quyền xem phiếu yêu cầu hãng bảo hành\n"
        "- MH-1: người mua hàng phụ trách BR-A / HSX-A tại TPE\n"
        "Khách hàng KH-01 có hợp đồng HD-01 (có hàng H1, bàn giao 10/09/2026) và HD-02 (không có H1)")

OPEN_KD1 = "Đăng nhập KD-1, " + MENU
OPEN_CREATE = "Đăng nhập KD-1, " + MENU + ", bấm \"Tạo mới\""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu yêu cầu hãng bảo hành: nhân viên kinh doanh đề nghị bộ phận mua hàng gửi hàng lỗi (của khách hoặc "
     "hàng tồn trong kho) sang hãng / nhà cung cấp để bảo hành.\n"
     "Người dùng làm được:\n"
     "- Tạo phiếu: chọn Thương hiệu, Hãng sản xuất, Công ty gửi; hệ thống tự điền Người nhận đơn / Người mua "
     "hàng theo phân công phụ trách thương hiệu.\n"
     "- Thêm hàng cần bảo hành: serial, nội dung lỗi, hàng tồn trong kho hoặc của khách (kèm hợp đồng), hàng "
     "bảo hành thay thế, khoản bảo hành bằng tiền, file đính kèm.\n"
     "- Lưu (Đang tạo) hoặc \"Lưu & Gửi\" (Chờ duyệt).\n"
     "- Người mua hàng: \"Không duyệt\" hoặc \"Lập thư yêu cầu\" (sang màn Thư yêu cầu bảo hành).\n"
     "- In, Xuất Excel từng phiếu và danh sách."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách (menu \"Phiếu Yêu cầu hãng bảo hành\"): phiếu trong phạm vi quyền xem, mới lập lên đầu.\n"
     "- Không có quyền xem: phiếu mình lập, phiếu mình là người duyệt, phiếu thuộc thương hiệu và hãng sản xuất "
     "mình phụ trách mua hàng.\n"
     "- Phiếu Đang tạo chỉ người lập thấy.\n"
     "- Số phiếu: PYCHBH-<5 chữ số>, ví dụ PYCHBH-00102.\n"
     "- Danh sách chờ duyệt (ô trên trang chủ): phiếu Chờ duyệt của thương hiệu / hãng mình phụ trách."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của người khác (kể cả với quyền tổng công ty).\n"
     "- Phiếu ngoài phạm vi quyền xem.\n"
     "- Phiếu đã xóa (xóa hẳn cùng các dòng hàng).\n"
     "- Ô tìm hàng chỉ nhận hàng cùng thương hiệu với phiếu.\n"
     "- Ô chọn hợp đồng chỉ nhận hợp đồng có hàng đang bảo hành."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô Từ ngày / Đến ngày lọc theo Ngày tạo phiếu, tính trọn ngày Đến ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Mã phiếu, Người nhận, Thương hiệu, Phòng ban, Hãng sản xuất, Mã / tên hàng, Model, Code đặt hàng, "
     "Khách hàng, Trạng thái, Từ ngày / Đến ngày, Công ty / Phòng ban (theo quyền xem).\n"
     "Bảng: STT, Số phiếu, Thương hiệu, Hãng sản xuất, Ngày tạo, Ngày duyệt, Người yêu cầu, Phòng yêu cầu, Người "
     "duyệt, Trạng thái, Hành động (In / Xuất Excel / Sửa / Xóa / Duyệt).\n"
     "Form: Thương hiệu, Hãng sản xuất, Công ty, Người nhận đơn, Người mua hàng, Người yêu cầu, Phòng yêu cầu, "
     "Ghi chú; bảng hàng: Hàng hóa, Số serial, Nội dung cần bảo hành, Hàng tồn trong kho, Khách hàng, Hợp đồng, "
     "File đính kèm; dưới mỗi hàng: \"Bảo hành bằng hàng\" (hàng, SL) và \"Bảo hành bằng tiền\" (tên, giá trị).\n"
     "Trạng thái: Đang tạo, Chờ duyệt, Đang gửi NCC, Đã gửi NCC, Không duyệt, Đã xác nhận BH, Hoàn thành."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một hàng không được lặp cùng một serial trong phiếu.\n"
     "- Mọi hàng phải cùng thương hiệu với phiếu.\n"
     "- Đổi Thương hiệu hoặc Hãng sản xuất: bảng hàng bị xóa trắng.\n"
     "- Lập thư yêu cầu: thư lưu nháp thì phiếu sang Đang gửi NCC; thư gửi NCC thì phiếu sang Đã gửi NCC và "
     "có Ngày duyệt; phiếu xác nhận bảo hành lưu xong thì phiếu sang Đã xác nhận BH."),

    ("7. Phân quyền cấp",
     "- Mở danh sách, tạo phiếu: mọi tài khoản đăng nhập.\n"
     "- \"Xem phiếu yêu cầu hãng bảo hành - theo tổng công ty / công ty / phòng ban / bộ phận\": mở rộng danh "
     "sách theo phạm vi.\n"
     "- Sửa, Xóa: người lập, phiếu Đang tạo hoặc Không duyệt.\n"
     "- Không duyệt, Lập thư yêu cầu: người mua hàng đang được phân công cho Công ty gửi + Thương hiệu + Hãng "
     "sản xuất của phiếu, phiếu Chờ duyệt.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Phiếu yêu cầu hãng bảo hành chờ duyệt\" trên trang chủ: số phiếu Chờ duyệt thuộc thương hiệu và "
     "hãng mình phụ trách tại công ty mình.\n"
     "- Phân trang theo bảng chung, STT liên tục.\n"
     "- Lưu & Gửi: người mua hàng nhận thông báo \"Bạn có một yêu cầu hãng bảo hành cần duyệt từ <người lập>\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Xuất Excel từng phiếu không kiểm tra quyền xem: ai đăng nhập cũng tải được phiếu bất kỳ qua đường dẫn.\n"
     "- Không duyệt nhận trạng thái do trình duyệt gửi lên: gọi thẳng chức năng đặt được phiếu sang trạng thái "
     "bất kỳ.\n"
     "- Xóa thư yêu cầu nháp: phiếu kẹt ở Đang gửi NCC, không ai lập lại thư hay sửa phiếu được.\n"
     "- Quyền xem theo phòng ban / bộ phận: thấy phiếu ở danh sách nhưng mở ra trang không tìm thấy.\n"
     "- Thương hiệu / hãng chưa phân công người mua hàng: bấm Lưu (kể cả lưu nháp) bị chặn ở ô Người nhận đơn.\n"
     "- Hai dòng cùng một hàng không nhập serial bị báo \"có serial trùng nhau\".\n"
     "- Trạng thái Hoàn thành không bao giờ được gán."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem vẫn mở được danh sách, chỉ thấy phiếu liên quan", "P0",
     DATA + "\nPYC-01 do KD-1 lập (Chờ duyệt, BR-A), PYC-02 do KD-2 lập (Chờ duyệt, BR-B)",
     "1. Đăng nhập KD-1\n"
     "2. " + MENU,
     "Tài khoản: KD-1",
     "- Mở trang \"Yêu cầu hãng bảo hành\"\n"
     "- Thấy PYC-01, không thấy PYC-02\n"
     "- Không có ô lọc Công ty, Phòng ban"),

    ("01", "Người mua hàng thấy phiếu của thương hiệu mình phụ trách", "P0",
     "MH-1 không có quyền xem; PYC-01 (BR-A / HSX-A, Chờ duyệt) do KD-1 lập; PYC-02 (BR-B) do KD-2 lập",
     "1. Đăng nhập MH-1, " + MENU,
     "—",
     "- Thấy PYC-01, không thấy PYC-02"),

    ("02", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "QL-C có quyền \"Xem phiếu yêu cầu hãng bảo hành - theo công ty\", thuộc TPE; PYC-01 của TPE, PYC-09 do "
     "nhân viên TPC lập (cả hai Chờ duyệt)",
     "1. Đăng nhập QL-C, " + MENU,
     "—",
     "- Thấy PYC-01, không thấy PYC-09\n"
     "- Bấm PYC-01 mở được chi tiết"),

    ("03", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "QL-T có quyền \"Xem phiếu yêu cầu hãng bảo hành - theo tổng công ty\"; PYC-01 (TPE), PYC-09 (TPC)",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Thấy cả PYC-01 và PYC-09\n"
     "- Có ô lọc Công ty và Phòng ban"),

    ("04", "Quyền theo phòng ban mở được chi tiết phiếu thấy trên danh sách", "P0",
     "TP-1 có quyền \"Xem phiếu yêu cầu hãng bảo hành - theo phòng ban\", phụ trách PKD1; PYC-01 do KD-1 (PKD1) "
     "lập; TP-1 không phụ trách mua hàng BR-A",
     "1. Đăng nhập TP-1, " + MENU + "\n"
     "2. Bấm số phiếu PYC-01",
     "—",
     "- Danh sách có PYC-01\n"
     "- Mong đợi: mở được chi tiết PYC-01\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy (quyền theo phòng ban / bộ phận không được xét khi "
     "mở chi tiết) - ghi Failed"),

    ("05", "Phiếu Đang tạo của người khác không hiện kể cả với quyền tổng công ty", "P0",
     "QL-T có quyền theo tổng công ty; PYC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Không thấy PYC-04"),

    ("06", "Mở chi tiết phiếu ngoài phạm vi qua đường dẫn", "P0",
     "KD-2 không có quyền xem, không phụ trách mua hàng; PYC-01 do KD-1 lập",
     "1. Đăng nhập KD-2, dán đường dẫn chi tiết PYC-01\n"
     "2. Dán đường dẫn In PYC-01",
     "—",
     "- Cả hai ra trang không tìm thấy"),

    ("07", "Người không phải người mua hàng không có nút duyệt", "P0",
     "KD-2 có quyền \"Xem ... - theo công ty\"; PYC-01 Chờ duyệt (BR-A / HSX-A, phụ trách MH-1)",
     "1. Đăng nhập KD-2, mở chi tiết PYC-01\n"
     "2. Mở menu Hành động của PYC-01 trên danh sách",
     "—",
     "- Không có khung Ghi chú duyệt, không có nút \"Không duyệt\", \"Lập thư yêu cầu\"\n"
     "- Menu Hành động không có \"Duyệt\""),

    ("08", "Gọi thẳng chức năng Không duyệt khi không phải người mua hàng", "P1",
     "KD-2 không phụ trách mua hàng BR-A; PYC-01 Chờ duyệt",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt PYC-01 với ghi chú \"test\"",
     "—",
     "- Báo \"Bạn không có quyền!\", PYC-01 vẫn Chờ duyệt"),
]
