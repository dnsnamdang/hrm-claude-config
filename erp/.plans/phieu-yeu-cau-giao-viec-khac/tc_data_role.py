# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu yeu cau giao viec khac'."""

MENU = "Mở menu Khởi tạo > mục \"Lắp đặt - BH -SC\" > bấm \"Phiếu yêu cầu giao việc khác\""
MENU_CHO = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu chờ giao việc\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng PKD1 (kinh doanh), PKT1 (kỹ thuật); công ty TPC có phòng PKD9.\n"
        "Tài khoản:\n"
        "- KD-1: nhân viên PKD1, người lập yêu cầu, không có quyền xem phiếu yêu cầu giao việc khác\n"
        "- KD-2: nhân viên PKD1 khác, không có quyền xem\n"
        "- TP-1: trưởng PKT1, có quyền \"Tạo phiếu giao việc\"\n"
        "- KTV-1: kỹ thuật viên PKT1, không có quyền \"Tạo phiếu giao việc\"\n"
        "Khách hàng:\n"
        "- KH-01: doanh nghiệp, địa chỉ \"12 Lê Lợi\", người liên hệ Anh Bình\n"
        "- KH-02: cá nhân Chị Hoa\n"
        "Hợp đồng HD-01 của KH-01: Có hiệu lực, do KD-1 lập, có dịch vụ tính doanh thu \"Vệ sinh máy\" và "
        "\"Bảo trì định kỳ\"; phụ lục bổ sung PL-01 có dịch vụ \"Hướng dẫn sử dụng\"")

OPEN_KD1 = "Đăng nhập KD-1, " + MENU
OPEN_CREATE = "Đăng nhập KD-1, " + MENU + ", bấm \"Tạo mới\""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu yêu cầu giao việc khác: nhân viên (thường là kinh doanh) gửi yêu cầu cho một phòng kỹ thuật làm "
     "các việc không thuộc sửa chữa, bảo hành, lắp đặt (ví dụ khảo sát, vệ sinh, hướng dẫn sử dụng).\n"
     "Người dùng làm được:\n"
     "- Tạo phiếu: chọn khách hàng, người liên hệ, địa chỉ lắp đặt, thời gian dự kiến, phòng tiếp nhận xử lý; "
     "chọn hợp đồng (lấy sẵn dịch vụ) hoặc tự thêm dịch vụ.\n"
     "- Lưu (Đang tạo) hoặc \"Lưu và gửi duyệt\" (Chờ giao việc).\n"
     "- Sửa phiếu Đang tạo, xóa phiếu Đang tạo / Từ chối.\n"
     "- Phòng tiếp nhận: \"Tạo phiếu giao việc\" hoặc \"Không duyệt\".\n"
     "Không có nút In, không có Xuất excel."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách \"Phiếu yêu cầu giao việc khác\": phiếu trong phạm vi quyền xem, mới lập lên đầu.\n"
     "- Phiếu Đang tạo chỉ người lập thấy.\n"
     "- Số phiếu: <mã công ty người lập>.YCGVK.<năm><6 chữ số>, ví dụ TPE.YCGVK.2026000812.\n"
     "- Cột Khách hàng: \"<mã> - <tên>\"; cột Số hợp đồng bấm mở hợp đồng.\n"
     "- Bảng \"Danh sách cần giao việc\": các dịch vụ, mỗi dòng có ô tích \"cần giao\"."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của người khác (kể cả với quyền tổng công ty).\n"
     "- Phiếu ngoài phạm vi quyền xem.\n"
     "- Phiếu đã xóa (xóa hẳn, không lưu vết).\n"
     "- Ô chọn hợp đồng chỉ có hợp đồng Có hiệu lực, loại Hợp đồng / Hợp đồng dự án / Hợp đồng nguyên tắc / Đơn "
     "hàng nguyên tắc, của khách hàng đã chọn, do chính người đăng nhập lập.\n"
     "- Danh sách dịch vụ tự thêm chỉ có dịch vụ tính doanh thu."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Ô Từ ngày / Đến ngày trên danh sách được thiết kế để lọc theo thời gian dự kiến của phiếu.\n"
     "Lưu ý: theo code hiện tại lọc theo cột không có trong dữ liệu của phiếu, chọn ngày thì bảng báo lỗi."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Số phiếu yêu cầu, Khách hàng, Số hợp đồng, Người lập, Trạng thái, Từ ngày / Đến ngày, Công ty / "
     "Phòng ban (theo quyền xem).\n"
     "Bảng: STT, Số phiếu, Số hợp đồng, Khách hàng, Người lập, Ngày lập, Trạng thái, Hành động (Tạo phiếu giao "
     "việc / Sửa / Xóa).\n"
     "Form: Khách hàng, Người liên hệ, SĐT, Địa chỉ, Hợp đồng, Thời gian dự kiến, Địa chỉ lắp đặt, Ghi chú, Phòng "
     "tiếp nhận xử lý, Phòng QTC, Nhân viên QTC (lấy từ hợp đồng, chỉ xem); bảng Danh sách cần giao việc; khung "
     "Ghi chú duyệt.\n"
     "Trạng thái: Đang tạo, Chờ giao việc, Đã giao việc, Từ chối."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Chọn hợp đồng: bảng dịch vụ được thay bằng dịch vụ tính doanh thu của hợp đồng và của các phụ lục bổ sung; "
     "khi đã có hợp đồng thì không thêm / bỏ dòng được, chỉ bỏ tích \"cần giao\".\n"
     "- Mỗi hợp đồng chỉ được lập 1 phiếu yêu cầu: chọn hợp đồng đã có phiếu thì không lấy được dịch vụ.\n"
     "- Tạo phiếu giao việc từ yêu cầu: yêu cầu sang Đã giao việc; xóa phiếu giao việc đó thì yêu cầu về Chờ "
     "giao việc."),

    ("7. Phân quyền cấp",
     "- Mở danh sách, tạo phiếu: mọi tài khoản đăng nhập.\n"
     "- Không có quyền xem: chỉ thấy phiếu mình lập.\n"
     "- \"Xem phiếu yêu cầu giao việc khác theo công ty\": phiếu của công ty mình.\n"
     "- \"... theo phòng ban\": phiếu do nhân viên các phòng mình phụ trách lập.\n"
     "- \"... theo tổng công ty\": mọi công ty.\n"
     "- Sửa: người lập, phiếu Đang tạo. Xóa: người lập, phiếu Đang tạo hoặc Từ chối.\n"
     "- \"Tạo phiếu giao việc\" / \"Không duyệt\": người thuộc phòng tiếp nhận, phiếu Chờ giao việc.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Màn không có ô tổng; phân trang theo bảng chung, STT liên tục.\n"
     "- Khi phiếu sang Chờ giao việc: người thuộc phòng tiếp nhận có quyền \"Tạo phiếu giao việc\" nhận thông "
     "báo, bấm mở chi tiết phiếu."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Chọn hợp đồng đã có phiếu yêu cầu: không báo gì, ô Hợp đồng vẫn nhận, lưu được phiếu thứ hai.\n"
     "- Đổi khách hàng: hợp đồng, người liên hệ, địa chỉ lắp đặt của khách cũ vẫn giữ.\n"
     "- Bỏ tích \"cần giao\" không có tác dụng: dòng đó vẫn sang phiếu giao việc.\n"
     "- Chọn Từ ngày / Đến ngày thì bảng báo lỗi.\n"
     "- Không duyệt: không thông báo cho người lập; chức năng không kiểm tra quyền và trạng thái.\n"
     "- Sau khi giao việc, phòng tiếp nhận không mở được chi tiết yêu cầu nếu không có quyền xem."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem vẫn mở được danh sách, chỉ thấy phiếu mình lập", "P0",
     DATA + "\nYC-01 do KD-1 lập (Chờ giao việc), YC-02 do KD-2 lập (Chờ giao việc)",
     "1. Đăng nhập KD-1\n"
     "2. " + MENU,
     "Tài khoản: KD-1",
     "- Mở trang \"Danh sách phiếu yêu cầu giao việc khác\"\n"
     "- Thấy YC-01, không thấy YC-02\n"
     "- Không có ô lọc Công ty, Phòng ban"),

    ("01", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "QL-C có quyền \"Xem phiếu yêu cầu giao việc khác theo công ty\", thuộc TPE; YC-02 của TPE (Chờ giao việc), "
     "YC-09 của TPC (Chờ giao việc)",
     "1. Đăng nhập QL-C, " + MENU,
     "—",
     "- Thấy YC-02, không thấy YC-09\n"
     "- Có ô lọc Phòng ban, không có ô Công ty"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "QL-T có quyền \"Xem phiếu yêu cầu giao việc khác theo tổng công ty\"; YC-02 (TPE), YC-09 (TPC)",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Thấy cả YC-02 và YC-09\n"
     "- Có ô lọc Công ty và Phòng ban"),

    ("03", "Quyền theo phòng ban thấy phiếu của phòng mình phụ trách", "P0",
     "TP-KD có quyền \"Xem phiếu yêu cầu giao việc khác theo phòng ban\", phụ trách PKD1; YC-02 do KD-2 (PKD1) "
     "lập; YC-03 do nhân viên PKT1 lập",
     "1. Đăng nhập TP-KD, " + MENU,
     "—",
     "- Thấy YC-02, không thấy YC-03"),

    ("04", "Phiếu Đang tạo của người khác không hiện kể cả với quyền tổng công ty", "P0",
     "QL-T có quyền theo tổng công ty; YC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Không thấy YC-04"),

    ("05", "Mở chi tiết phiếu ngoài phạm vi qua đường dẫn", "P0",
     "KD-2 không có quyền xem; YC-01 do KD-1 lập, PKD1 không phải phòng tiếp nhận",
     "1. Đăng nhập KD-2, dán đường dẫn chi tiết YC-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "Gọi thẳng chức năng Không duyệt khi không thuộc phòng tiếp nhận", "P1",
     "KD-2 không thuộc PKT1; YC-01 Chờ giao việc, phòng tiếp nhận PKT1",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt YC-01 với ghi chú \"test\"",
     "—",
     "- Mong đợi: bị chặn, YC-01 vẫn Chờ giao việc\n"
     "- Lưu ý: theo code hiện tại YC-01 chuyển Từ chối - ghi Failed"),

    ("07", "Gọi thẳng chức năng Sửa phiếu của người khác", "P1",
     "YC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập KD-2, dùng công cụ kiểm thử API gọi chức năng lưu sửa YC-04",
     "—",
     "- Thông báo \"Không có quyền!\", YC-04 không đổi"),

    ("08", "Gọi thẳng chức năng Xóa phiếu của người khác", "P1",
     "YC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập KD-2, dán đường dẫn xóa YC-04",
     "—",
     "- Thông báo \"Không có quyền\", YC-04 vẫn còn"),
]
