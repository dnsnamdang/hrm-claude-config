# -*- coding: utf-8 -*-
"""Muc I - III: hien thi, pham vi danh sach, cot du lieu."""

from tc_data_role import MENU, MENU_DG, DATA, OPEN_KTV1, OPEN_KTV2

SEC_I = [
    ("001", "Mở menu Phiếu giao việc được giao", "P0",
     DATA,
     "1. Đăng nhập KTV-1\n"
     "2. " + MENU_DG,
     "Tài khoản: KTV-1",
     "- Mở trang danh sách, có bảng phiếu và dải ô lọc\n"
     "- Có nút In và Xuất excel\n"
     "- Không có nút Tạo mới"),

    ("002", "Tiêu đề trang phân biệt với menu Phiếu giao việc", "P2",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Mong đợi: tiêu đề cho biết đây là phiếu được giao cho mình\n"
     "- Lưu ý: theo code hiện tại tiêu đề là \"Danh sách phiếu giao việc\", giống hệt menu Phiếu giao việc - "
     "ghi Failed"),

    ("003", "Đủ các cột của bảng", "P0",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Cột theo thứ tự: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, "
     "Người lập, Người thực hiện, Thời gian dự kiến, Tổng công định mức, Trạng thái, Hành động"),

    ("004", "Không có ô lọc Công ty, Phòng ban, Bộ phận", "P1",
     "KTV-1 có quyền \"Xem phiếu giao việc theo tổng công ty\"\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Dải ô lọc không có Công ty, Phòng ban, Bộ phận\n"
     "- Ở menu \"Phiếu giao việc\" KTV-1 có các ô này"),

    ("005", "Sắp xếp mới nhất lên đầu", "P1",
     "KTV-1 thực hiện PGV-01 (lập 01/11/2026) và PGV-05 (lập 05/11/2026)\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- PGV-05 nằm trên PGV-01"),

    ("006", "Phân trang và STT liên tục", "P2",
     "KTV-1 thực hiện 25 phiếu giao việc",
     "1. " + OPEN_KTV1 + "\n"
     "2. Sang trang 2",
     "—",
     "- Mặc định 10 dòng mỗi trang\n"
     "- Trang 2 STT nối tiếp từ 11"),

    ("007", "Bộ lọc được nhớ riêng cho menu này", "P2",
     DATA,
     "1. " + OPEN_KTV1 + ", lọc Trạng thái \"Chờ thực hiện\"\n"
     "2. Mở menu \"Phiếu giao việc\", rồi quay lại menu \"Phiếu giao việc được giao\"",
     "—",
     "- Menu \"Phiếu giao việc\" không mang theo bộ lọc vừa chọn\n"
     "- Quay lại menu được giao: ô Trạng thái vẫn là \"Chờ thực hiện\""),

    ("008", "Không có ô đếm phiếu được giao trên trang chủ", "P2",
     DATA,
     "1. Đăng nhập KTV-1, xem trang chủ",
     "—",
     "- Không có ô đếm \"Phiếu giao việc được giao\" / \"chờ nhập kết quả\"\n"
     "- Ghi nhận: nghiệp vụ quyết có cần ô đếm cho kỹ thuật viên không, không ghi Failed"),
]

SEC_II = [
    ("001", "Trưởng nhóm thấy phiếu của nhóm", "P0",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Có PGV-01\n"
     "- Cột Người thực hiện: \"KTV-1 - <SĐT KTV-1>\""),

    ("002", "Thành viên nhóm cũng thấy phiếu", "P0",
     DATA,
     "1. " + OPEN_KTV2,
     "—",
     "- Có PGV-01 và PGV-02\n"
     "- Dòng PGV-01 cột Người thực hiện vẫn là KTV-1 (trưởng nhóm)"),

    ("003", "Thấy phiếu của công ty khác nếu mình là người thực hiện", "P0",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Có PGV-09 (công ty TPC) dù KTV-1 thuộc TPE"),

    ("004", "Hiện cả phiếu đã xong việc", "P0",
     DATA,
     "1. " + OPEN_KTV2,
     "—",
     "- Có PGV-02 trạng thái \"Đã duyệt kết quả\""),

    ("005", "Phiếu có PCT chưa duyệt chưa hiện", "P0",
     "PGV-04 có PCT-04 gồm KTV-1, PCT-04 đang Chờ duyệt bên HRM\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Không có PGV-04\n"
     "- Người thực hiện chỉ được ghi sang ERP khi PCT duyệt"),

    ("006", "PCT được duyệt thì phiếu xuất hiện", "P0",
     "Như TC 005",
     "1. Trưởng phòng duyệt PCT-04 bên HRM\n"
     "2. " + OPEN_KTV1 + " (tải lại trang)",
     "—",
     "- Có PGV-04, Trạng thái \"Chờ thực hiện\"\n"
     "- Bấm nút bánh răng có \"Nhập kết quả\""),

    ("007", "Phiếu chưa có PCT không hiện với ai", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. " + OPEN_KTV2,
     "—",
     "- Không ai thấy PGV-03"),

    ("008", "Sửa PCT đã duyệt bỏ một người", "P0",
     "PCT-01 đã duyệt; PGV-01 còn Chờ thực hiện\n" + DATA,
     "1. Bên HRM sửa PCT-01, bỏ KTV-2 khỏi danh sách người đi, lưu\n"
     "2. " + OPEN_KTV2,
     "—",
     "- Không còn PGV-01\n"
     "- KTV-1 vẫn thấy PGV-01"),

    ("009", "Sửa PCT đã duyệt đổi trưởng nhóm", "P1",
     "Như TC 008, PCT-01 còn KTV-1 và KTV-2",
     "1. Bên HRM sửa PCT-01, đặt KTV-2 làm trưởng nhóm, lưu\n"
     "2. " + OPEN_KTV1,
     "—",
     "- PGV-01 vẫn hiện với KTV-1\n"
     "- Cột Người thực hiện đổi thành KTV-2"),

    ("010", "Xóa PCT thì phiếu rời danh sách", "P0",
     "PCT-01 được phép xóa bên HRM\n" + DATA,
     "1. Bên HRM xóa PCT-01\n"
     "2. " + OPEN_KTV1,
     "—",
     "- Không còn PGV-01\n"
     "- Ở menu \"Phiếu giao việc\", PGV-01 trạng thái \"Chờ thực hiện\", không có \"Nhập kết quả\""),

    ("011", "Phiếu giao việc bị xóa (Hủy) không hiện", "P0",
     "PGV-06 có người thực hiện KTV-1 rồi bị chuyển Hủy\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Không có PGV-06"),

    ("012", "Phiếu duyệt kết quả không nằm trong danh sách", "P1",
     "PGV-02 đã có phiếu duyệt kết quả DKQ-02\n" + DATA,
     "1. " + OPEN_KTV2,
     "—",
     "- Chỉ có dòng PGV-02, không có dòng DKQ-02"),

    ("013", "Phiếu PCT đã duyệt nhưng không có người thực hiện", "P2",
     "PGV-07 có PCT đã duyệt nhưng danh sách người thực hiện trống (dữ liệu thật đang có 3 phiếu như vậy)",
     "1. Đăng nhập TP-1, " + MENU + "\n"
     "2. Bấm nút bánh răng ở PGV-07",
     "—",
     "- Không có \"Nhập kết quả\"\n"
     "- Không ai thấy PGV-07 ở menu \"Phiếu giao việc được giao\"\n"
     "- Ghi nhận: phiếu bị kẹt, nghiệp vụ quyết cách xử lý, không ghi Failed"),
]

SEC_III = [
    ("001", "Số phiếu giao việc mở chi tiết", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm số PGV-01",
     "—",
     "- Mở trang \"Phiếu giao việc PGV-01\" ở chế độ xem"),

    ("002", "Số hợp đồng của phiếu từ hợp đồng", "P1",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Cột Số hợp đồng dòng PGV-01 là HD-01, bấm được\n"
     "- Cột Số phiếu yêu cầu trống"),

    ("003", "Phiếu lắp đặt hiện số hợp đồng hàng và số yêu cầu", "P1",
     DATA,
     "1. " + OPEN_KTV2,
     "—",
     "- Dòng PGV-02: Số hợp đồng HDH-01, Số phiếu yêu cầu LD-01"),

    ("004", "Phiếu giao việc khác chỉ có số yêu cầu", "P2",
     "PGV-08 từ yêu cầu giao việc khác YC-01 (không gắn hợp đồng), người thực hiện KTV-1",
     "1. " + OPEN_KTV1,
     "—",
     "- Dòng PGV-08: Số hợp đồng trống, Số phiếu yêu cầu YC-01"),

    ("005", "Khách hàng hiện mã kèm tên", "P1",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Cột Khách hàng dòng PGV-01: \"<mã KH-1>-<tên KH-1>\""),

    ("006", "Người yêu cầu và Người lập kèm SĐT", "P1",
     "HD-01 do KD-1 lập\n" + DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Người yêu cầu: \"KD-1 - <SĐT KD-1>\"\n"
     "- Người lập: \"TP-1 - <SĐT TP-1>\""),

    ("007", "Nhóm không có trưởng nhóm thì hiện người đầu tiên", "P2",
     "PGV-10 có người thực hiện KTV-2, KTV-1 (ghi theo thứ tự này), không ai là trưởng nhóm",
     "1. " + OPEN_KTV1,
     "—",
     "- Cột Người thực hiện dòng PGV-10 là KTV-2"),

    ("008", "Thời gian dự kiến và Tổng công định mức", "P1",
     DATA,
     "1. " + OPEN_KTV1,
     "—",
     "- Thời gian dự kiến dòng PGV-01: \"10/11/2026-12/11/2026\"\n"
     "- Tổng công định mức: 2.00"),

    ("009", "Tên trạng thái đúng theo vòng đời", "P0",
     "KTV-1 có các phiếu ở trạng thái: Chờ thực hiện, Đang nhập kết quả, Đã nhập kết quả, Đang duyệt kết quả, "
     "Đã duyệt kết quả",
     "1. " + OPEN_KTV1,
     "—",
     "- Cột Trạng thái hiện đúng 5 tên trên, mỗi phiếu một tên"),
]
