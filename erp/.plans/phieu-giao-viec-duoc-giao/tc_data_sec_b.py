# -*- coding: utf-8 -*-
"""Muc IV - VI: bo loc, hanh dong tren dong, ban giao sang phieu nhap ket qua."""

from tc_data_role import MENU, MENU_DG, DATA, OPEN_KTV1, OPEN_KTV2

SEC_IV = [
    ("001", "Lọc theo Số phiếu giao việc (gõ một phần)", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu giao việc gõ \"01\", bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-01"),

    ("002", "Lọc theo Số hợp đồng", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số hợp đồng gõ \"HD-01\", bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-01"),

    ("003", "Lọc Số hợp đồng ra phiếu lắp đặt theo hợp đồng hàng", "P1",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Ô Số hợp đồng gõ \"HDH-01\", bấm Tìm kiếm",
     "—",
     "- Có PGV-02"),

    ("004", "Lọc theo Số phiếu yêu cầu", "P2",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Ô Số phiếu yêu cầu gõ \"LD-01\", bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-02"),

    ("005", "Lọc theo Khách hàng", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Khách hàng chọn KH-1, bấm Tìm kiếm",
     "—",
     "- Chỉ có các phiếu của KH-1, có PGV-01"),

    ("006", "Lọc Người yêu cầu với phiếu lắp đặt", "P2",
     "LD-01 do KD-1 lập\n" + DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Ô Người yêu cầu chọn KD-1, bấm Tìm kiếm",
     "—",
     "- Mong đợi: có PGV-02\n"
     "- Lưu ý: theo code hiện tại không có PGV-02 vì lọc này chỉ xét hợp đồng / phiếu bảo hành (đã ghi ở bộ "
     "Phiếu giao việc) - ghi Failed"),

    ("007", "Lọc theo Trạng thái", "P0",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Ô Trạng thái chọn \"Chờ thực hiện\", bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-01, không có PGV-02 (Đã duyệt kết quả)"),

    ("008", "Danh sách trạng thái trong ô lọc", "P2",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Mở ô Trạng thái",
     "—",
     "- Có: Chờ thực hiện, Đang nhập kết quả, Đã nhập kết quả, Đang duyệt kết quả, Đã duyệt kết quả, Chờ BKS "
     "duyệt kết quả, Đang đề nghị thanh toán, Đã thanh toán\n"
     "- Không có Hủy"),

    ("009", "Lọc theo Người lập", "P2",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Người lập chọn TP-1, bấm Tìm kiếm",
     "—",
     "- Có PGV-01; không có PGV-09 (người lập khác)"),

    ("010", "Lọc Người thực hiện là người khác trong nhóm", "P1",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Người thực hiện chọn KTV-2, bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-01 (phiếu chung nhóm KTV-1 và KTV-2)\n"
     "- Không có PGV-02 (của KTV-2 nhưng KTV-1 không thực hiện)"),

    ("011", "Lọc Thời gian dự kiến từ / đến ngày", "P1",
     "PGV-01 dự kiến 10/11 - 12/11/2026; PGV-09 dự kiến 20/11 - 22/11/2026\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Chọn Thời gian dự kiến từ ngày 09/11/2026, đến ngày 15/11/2026, bấm Tìm kiếm",
     "—",
     "- Chỉ có PGV-01"),

    ("012", "Làm mới bộ lọc", "P2",
     "Như TC 011, đang lọc",
     "1. Bấm nút làm mới",
     "—",
     "- Các ô lọc trống, bảng hiện lại PGV-01 và PGV-09"),

    ("013", "Lọc không ra phiếu ngoài phạm vi", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu giao việc gõ \"03\", bấm Tìm kiếm",
     "—",
     "- Bảng trống (PGV-03 không giao cho KTV-1)"),
]

SEC_V = [
    ("001", "Nhập kết quả khi đủ điều kiện", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Có \"Nhập kết quả\"\n"
     "- Không có \"Xem phiếu nhập kết quả\", \"Xem phiếu duyệt kết quả\", \"Xóa\""),

    ("002", "Thành viên nhóm cũng có Nhập kết quả", "P0",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Có \"Nhập kết quả\""),

    ("003", "Phiếu đã có phiếu nhập kết quả thì không có Nhập kết quả", "P0",
     "KTV-1 đã lưu phiếu nhập kết quả NKQ-01 cho PGV-01\n" + DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Nhập kết quả\"\n"
     "- Có \"Xem phiếu nhập kết quả\""),

    ("004", "Phiếu ở trạng thái khác Chờ thực hiện", "P1",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-02 (Đã duyệt kết quả)",
     "—",
     "- Không có \"Nhập kết quả\"\n"
     "- Có \"Xem phiếu nhập kết quả\" và \"Xem phiếu duyệt kết quả\""),

    ("005", "Phiếu duyệt kết quả đang tạo chưa có nút xem", "P1",
     "PGV-01 đã có phiếu duyệt kết quả DKQ-01 đang ở bước lưu nháp (Đang tạo)\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Xem phiếu duyệt kết quả\""),

    ("006", "Xem phiếu nhập kết quả của chính mình", "P0",
     "KTV-1 đã Lưu & Gửi duyệt NKQ-01 cho PGV-01\n" + DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01, chọn \"Xem phiếu nhập kết quả\"",
     "—",
     "- Mở chi tiết NKQ-01"),

    ("007", "Thành viên nhóm xem phiếu nhập kết quả do trưởng nhóm lập", "P1",
     "Như TC 006; KTV-2 không có quyền xem phiếu nhập kết quả",
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-01, chọn \"Xem phiếu nhập kết quả\"",
     "—",
     "- Mong đợi: mở được NKQ-01 vì KTV-2 là người thực hiện của phiếu\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy (phiếu nhập kết quả chỉ cho người lập và người có "
     "quyền xem) - ghi Failed"),

    ("008", "Xem phiếu duyệt kết quả", "P1",
     DATA,
     "1. " + OPEN_KTV2 + "\n"
     "2. Bấm nút bánh răng ở PGV-02, chọn \"Xem phiếu duyệt kết quả\"",
     "—",
     "- Mở chi tiết phiếu duyệt kết quả của PGV-02"),

    ("009", "PCT đã duyệt nhưng phiếu không có người thực hiện thì không nhập được", "P2",
     "PGV-07 như TC II.013; KTV-1 có quyền \"Nhập kết quả thực hiện\"",
     "1. Đăng nhập KTV-1, " + MENU + "\n"
     "2. Bấm nút bánh răng ở PGV-07",
     "—",
     "- Không có \"Nhập kết quả\""),
]

SEC_VI = [
    ("001", "Bấm Nhập kết quả mở form điền sẵn", "P0",
     DATA,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01, chọn \"Nhập kết quả\"",
     "—",
     "- Mở form nhập kết quả của PGV-01: số phiếu giao việc, khách hàng KH-1, hợp đồng HD-01, người yêu cầu "
     "điền sẵn"),

    ("002", "Lưu nháp kết quả đổi trạng thái trên danh sách", "P0",
     "Như TC 001",
     "1. Trên form, bấm \"Lưu\"\n"
     "2. " + OPEN_KTV1,
     "—",
     "- PGV-01 trạng thái \"Đang nhập kết quả\"\n"
     "- Nút bánh răng: không còn \"Nhập kết quả\", có \"Xem phiếu nhập kết quả\""),

    ("003", "Gửi duyệt kết quả", "P0",
     "PGV-01 đang có NKQ-01 Đang tạo",
     "1. Mở NKQ-01, Sửa, bấm \"Lưu & Gửi duyệt\"\n"
     "2. " + OPEN_KTV1,
     "—",
     "- PGV-01 trạng thái \"Đã nhập kết quả\""),

    ("004", "Kết quả bị Không duyệt", "P1",
     "NKQ-01 Chờ duyệt kết quả; người duyệt bấm \"Không duyệt kết quả\" có lý do",
     "1. " + OPEN_KTV1,
     "—",
     "- PGV-01 vẫn \"Đã nhập kết quả\" (ghi nhận theo code, nghiệp vụ quyết, không ghi Failed)\n"
     "- Không có \"Nhập kết quả\" (phiếu nhập kết quả đã có, sửa lại ở menu Phiếu nhập kết quả)"),

    ("005", "Xóa phiếu nhập kết quả trả lại nút Nhập kết quả", "P0",
     "NKQ-01 Đang tạo, KTV-1 xóa NKQ-01",
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- PGV-01 trạng thái \"Chờ thực hiện\"\n"
     "- Có lại \"Nhập kết quả\", không còn \"Xem phiếu nhập kết quả\""),

    ("006", "Kết quả được duyệt", "P0",
     "NKQ-01 đã gửi; người duyệt lập và duyệt xong phiếu duyệt kết quả DKQ-01",
     "1. " + OPEN_KTV1,
     "—",
     "- PGV-01 trạng thái \"Đã duyệt kết quả\"\n"
     "- Có \"Xem phiếu duyệt kết quả\""),

    ("007", "Dán đường dẫn form nhập kết quả của phiếu không giao cho mình", "P1",
     "KTV-3 không thuộc nhóm PGV-01, không có quyền \"Nhập kết quả thực hiện\"\n" + DATA,
     "1. Đăng nhập KTV-3, dán đường dẫn form nhập kết quả của PGV-01",
     "—",
     "- Mong đợi: ra trang không tìm thấy hoặc báo không có quyền\n"
     "- Lưu ý: theo code hiện tại mở được form, lưu thành công (đã ghi ở bộ Phiếu nhập kết quả) - ghi Failed"),

    ("008", "Dán đường dẫn form nhập kết quả khi PCT chưa duyệt", "P1",
     "PGV-04 có PCT-04 đang Chờ duyệt\n" + DATA,
     "1. Đăng nhập KTV-1, dán đường dẫn form nhập kết quả của PGV-04\n"
     "2. Nhập đủ thông tin, bấm \"Lưu\"",
     "—",
     "- Không lưu được, thông báo \"Chỉ được nhập kết quả khi phiếu công tác (PCT) đã được duyệt\""),

    ("009", "Hai người trong nhóm cùng mở form, người sau lưu", "P1",
     "KTV-1 và KTV-2 cùng mở form nhập kết quả của PGV-01 ở 2 máy\n" + DATA,
     "1. KTV-1 bấm \"Lưu\"\n"
     "2. KTV-2 bấm \"Lưu\"",
     "—",
     "- KTV-2 nhận thông báo \"Phiếu giao việc này đã có phiếu nhập kết quả, không thể tạo thêm. Vui lòng mở "
     "phiếu kết quả đã có để chỉnh sửa.\"\n"
     "- PGV-01 chỉ có 1 phiếu nhập kết quả"),
]
