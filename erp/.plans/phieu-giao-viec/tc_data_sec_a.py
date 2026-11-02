# -*- coding: utf-8 -*-
"""Section I - IV cho man Phieu giao viec."""
from tc_data_role import MENU, DATA, OPEN_TP1, FROM_HD01

PGV = ("Đã có các phiếu do TP-1 lập:\n"
       "- PGV-01 từ HD-01, Chờ thực hiện, dự kiến 05/11/2026 - 06/11/2026, Tổng công 2\n"
       "- PGV-02 từ LD-01, Đang nhập kết quả, dự kiến 10/11/2026 - 12/11/2026\n"
       "- PGV-03 từ YC-01, Đã duyệt kết quả, dự kiến 03/11/2026 - 03/11/2026\n"
       "- PGV-04 từ BH-01, Chờ thực hiện, đã bị Xóa")

SEC_I = [
    ("001", "Mở danh sách phiếu giao việc", "P0",
     PGV,
     "1. " + OPEN_TP1,
     "Tài khoản: TP-1",
     "- Tiêu đề \"Danh sách phiếu giao việc\"\n"
     "- Có PGV-01, PGV-02, PGV-03, mới nhất lên đầu\n"
     "- Có nút In, Xuất excel; không có nút Tạo mới"),

    ("002", "Các cột của bảng", "P1",
     PGV,
     "1. " + OPEN_TP1,
     "—",
     "- Cột: STT, Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Người lập, "
     "Người thực hiện, Thời gian dự kiến, Tổng công định mức, Trạng thái, Hành động"),

    ("003", "Dòng phiếu từ hợp đồng", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Xem dòng PGV-01",
     "—",
     "- Số hợp đồng: HD-01 (bấm mở hợp đồng)\n"
     "- Số phiếu yêu cầu trống\n"
     "- Người yêu cầu: KD-1 kèm SĐT; Người lập: TP-1 kèm SĐT\n"
     "- Thời gian dự kiến 05/11/2026-06/11/2026; Tổng công định mức 2.00; Trạng thái \"Chờ thực hiện\""),

    ("004", "Dòng phiếu từ yêu cầu lắp đặt", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Xem dòng PGV-02",
     "—",
     "- Số hợp đồng: HDH-01 (bấm mở hợp đồng hàng)\n"
     "- Số phiếu yêu cầu: LD-01 (bấm mở yêu cầu lắp đặt)\n"
     "- Trạng thái \"Đang nhập kết quả\""),

    ("005", "Dòng phiếu từ yêu cầu giao việc khác", "P1",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Xem dòng PGV-03",
     "—",
     "- Số hợp đồng trống, Số phiếu yêu cầu: YC-01 (bấm mở)\n"
     "- Người yêu cầu: KD-1\n"
     "- Trạng thái \"Đã duyệt kết quả\""),

    ("006", "Phiếu đã xóa không hiện", "P0",
     PGV,
     "1. " + OPEN_TP1,
     "—",
     "- Không có PGV-04"),

    ("007", "Người thực hiện trống khi chưa có phiếu công tác", "P1",
     PGV + "\nPGV-01 chưa có phiếu công tác",
     "1. " + OPEN_TP1 + "\n"
     "2. Xem cột Người thực hiện ở PGV-01",
     "—",
     "- Ô trống"),

    ("008", "Người thực hiện hiện người trưởng nhóm", "P1",
     "PGV-01 có phiếu công tác gắn KTV-1 và KTV-2, KTV-2 là trưởng nhóm",
     "1. " + OPEN_TP1 + "\n"
     "2. Xem cột Người thực hiện ở PGV-01",
     "—",
     "- Hiện tên KTV-2 kèm SĐT của KTV-2"),

    ("009", "Phân trang", "P2",
     "TP-1 có 25 phiếu giao việc",
     "1. " + OPEN_TP1 + "\n"
     "2. Sang trang 2",
     "—",
     "- STT trang 2 nối tiếp trang 1"),
]

SEC_II = [
    ("001", "Menu Phiếu giao việc được giao chỉ có phiếu giao cho mình", "P0",
     "PGV-01 người thực hiện KTV-1; PGV-02 người thực hiện KTV-2; KTV-1 có thêm quyền \"Xem phiếu giao việc "
     "theo công ty\"",
     "1. Đăng nhập KTV-1\n"
     "2. Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc được giao\"",
     "—",
     "- Chỉ có PGV-01\n"
     "- Không có PGV-02 dù KTV-1 có quyền xem theo công ty"),

    ("002", "Quyền theo công ty vẫn thấy phiếu mình lập ở công ty khác", "P1",
     "QL-C thuộc TPE, có quyền \"Xem phiếu giao việc theo công ty\"; QL-C từng lập PGV-08 khi thuộc TPC",
     "1. Đăng nhập QL-C, " + MENU,
     "—",
     "- Có PGV-08"),

    ("003", "Quyền theo phòng ban dựa vào phòng của người lập lúc tạo", "P1",
     "QL-P phụ trách PKT1; PGV-01 do TP-1 lập khi TP-1 thuộc PKT1; sau đó TP-1 chuyển sang PKT2",
     "1. Đăng nhập QL-P, " + MENU,
     "—",
     "- Vẫn thấy PGV-01"),

    ("004", "Người có quyền Nhập kết quả thực hiện nhưng không có quyền xem", "P1",
     "KTV-3 có quyền \"Nhập kết quả thực hiện\", không là người thực hiện của phiếu nào, không có quyền xem",
     "1. Đăng nhập KTV-3, " + MENU,
     "—",
     "- Bảng không có dữ liệu"),

    ("005", "Super Admin mở chi tiết mọi phiếu", "P2",
     "SA có vai trò Super Admin; PGV-09 của TPC",
     "1. Đăng nhập SA, dán đường dẫn chi tiết PGV-09",
     "—",
     "- Mở được chi tiết"),
]

SEC_III = [
    ("001", "Lọc theo Số phiếu giao việc gõ một phần", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Số phiếu giao việc gõ \"01\"",
     "—",
     "- Chỉ còn PGV-01"),

    ("002", "Lọc theo Số hợp đồng gồm cả hợp đồng hàng", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Số hợp đồng gõ \"HDH-01\"",
     "—",
     "- Ra PGV-02 (phiếu lắp đặt của hợp đồng hàng HDH-01)"),

    ("003", "Lọc theo Số phiếu yêu cầu", "P1",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Số phiếu yêu cầu gõ \"YC-01\"",
     "—",
     "- Chỉ còn PGV-03"),

    ("004", "Lọc theo Khách hàng", "P1",
     PGV + "\nPGV-01 khách KH-A; PGV-02 khách KH-B",
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Khách hàng chọn KH-A",
     "—",
     "- Chỉ còn PGV-01"),

    ("005", "Lọc theo Trạng thái", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Trạng thái chọn \"Đang nhập kết quả\"",
     "—",
     "- Chỉ còn PGV-02\n"
     "- Ô Trạng thái không có lựa chọn Hủy"),

    ("006", "Lọc theo Người lập", "P1",
     "QL-C như TC phân quyền 01; PGV-01 do TP-1 lập, PGV-05 do TP-2 lập",
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Ô Người lập chọn TP-2",
     "—",
     "- Chỉ còn PGV-05"),

    ("007", "Lọc theo Người thực hiện", "P0",
     "PGV-01 người thực hiện KTV-1; PGV-02 người thực hiện KTV-2",
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Người thực hiện chọn KTV-2",
     "—",
     "- Chỉ còn PGV-02"),

    ("008", "Lọc theo Thời gian dự kiến từ / đến ngày", "P0",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Chọn Thời gian dự kiến từ ngày 04/11/2026, đến ngày 06/11/2026",
     "—",
     "- Chỉ còn PGV-01 (05/11 - 06/11)\n"
     "- Không có PGV-03 (bắt đầu 03/11), PGV-02 (kết thúc 12/11)"),

    ("009", "Lọc Người yêu cầu với phiếu lắp đặt / giao việc khác", "P1",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Người yêu cầu chọn KD-1",
     "—",
     "- Mong đợi: ra PGV-01, PGV-02, PGV-03 (cùng người yêu cầu KD-1)\n"
     "- Lưu ý: theo code hiện tại chỉ ra PGV-01 (chỉ tìm theo người lập hợp đồng) - ghi Failed"),

    ("010", "Lọc Phòng ban với phiếu lắp đặt / giao việc khác", "P1",
     "QL-C như TC phân quyền 01\n" + PGV,
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Ô Phòng ban chọn PKT1",
     "—",
     "- Mong đợi: ra cả PGV-01, PGV-02, PGV-03 (phiếu của phòng PKT1)\n"
     "- Lưu ý: theo code hiện tại lọc theo phòng của hợp đồng, PGV-02 và PGV-03 biến mất; chọn PKD (phòng lập "
     "hợp đồng) lại ra PGV-01 - ghi Failed"),

    ("011", "Lọc Bộ phận", "P2",
     "QL-P như TC phân quyền 03; PGV-01 người lập thuộc bộ phận BP-1",
     "1. Đăng nhập QL-P, " + MENU + "\n"
     "2. Ô Bộ phận chọn BP-2",
     "—",
     "- Mong đợi: PGV-01 bị lọc ra\n"
     "- Lưu ý: theo code hiện tại ô Bộ phận không có tác dụng - ghi Failed"),

    ("012", "Lọc Công ty", "P1",
     "QL-T như TC phân quyền 02",
     "1. Đăng nhập QL-T, " + MENU + "\n"
     "2. Ô Công ty chọn TPC",
     "—",
     "- Chỉ còn phiếu của TPC (PGV-09)"),

    ("013", "Kết hợp nhiều bộ lọc", "P2",
     PGV,
     "1. " + OPEN_TP1 + "\n"
     "2. Ô Trạng thái chọn \"Chờ thực hiện\", ô Số hợp đồng gõ \"HD-01\"",
     "—",
     "- Chỉ còn PGV-01"),
]

SEC_IV = [
    ("001", "Mở form tạo phiếu từ hợp đồng", "P0",
     DATA,
     "1. " + FROM_HD01,
     "—",
     "- Thông báo \"Lấy dữ liệu thành công\"\n"
     "- Thông tin khách hàng điền sẵn: Số hợp đồng HD-01 (bấm mở), Khách hàng, Người liên hệ, SĐT, Địa chỉ, "
     "Người yêu cầu KD-1, SĐT, Phòng yêu cầu PKD (đều khóa)\n"
     "- Có mục \"A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG\", \"B - Danh sách vật tư bán thêm\", \"C - CÔNG VIỆC PHỤ\", "
     "\"D - TỔNG HỢP\"\n"
     "- Nút \"Lưu & duyệt\", \"Quay lại\""),

    ("002", "Dịch vụ sửa chữa điền sẵn số còn giao", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Xem bảng \"I - Dịch vụ sửa chữa\"",
     "—",
     "- Dòng M1 serial S1 lỗi E1: SL còn trên hợp đồng 1, SL giao lần này 1, Định mức công 2\n"
     "- Dịch vụ \"Vệ sinh máy\": SL còn 1, SL giao 1"),

    ("003", "Không nhập được SL giao lần này lớn hơn SL còn", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Ô SL giao lần này của \"Vệ sinh máy\" gõ 5",
     "—",
     "- Ô tự về 1 (bằng SL còn trên hợp đồng)"),

    ("004", "Dòng đã giao hết thì khóa ô SL giao", "P1",
     "HD-01 đã có phiếu giao việc PGV-01 giao máy M1, chưa giao \"Vệ sinh máy\"\n" + DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Xem dòng M1",
     "—",
     "- SL còn trên hợp đồng 0, ô SL giao lần này bị khóa\n"
     "- \"Vệ sinh máy\" vẫn nhập được"),

    ("005", "Lưu & duyệt phiếu từ hợp đồng", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Chọn Ngày dự kiến bắt đầu, kết thúc là hôm nay, bấm \"Lưu & duyệt\"",
     "—",
     "- Thông báo \"Tạo phiếu giao việc thành công!\"\n"
     "- Chuyển về danh sách Phiếu giao việc, phiếu mới đầu bảng: số phiếu dạng <mã công ty>.PGV.<năm><6 số>, "
     "Trạng thái \"Chờ thực hiện\", Người lập TP-1"),

    ("006", "Hợp đồng giao hết rời danh sách chờ giao việc", "P0",
     "Vừa lưu phiếu ở TC 005 giao đủ M1, \"Vệ sinh máy\", VT1",
     "1. Đăng nhập TP-1, mở Phiếu chờ giao việc, tab Hợp đồng",
     "—",
     "- Không còn HD-01"),

    ("007", "Giao một phần thì hợp đồng vẫn chờ giao", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Ô SL giao lần này của \"Vệ sinh máy\" gõ 0, chọn ngày dự kiến, bấm \"Lưu & duyệt\"\n"
     "3. Mở lại Phiếu chờ giao việc",
     "—",
     "- Tạo phiếu thành công\n"
     "- HD-01 vẫn ở tab Hợp đồng\n"
     "- Mở form giao tiếp: M1 SL còn 0, \"Vệ sinh máy\" SL còn 1"),

    ("008", "Tổng công định mức của phiếu hợp đồng", "P0",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Xem mục \"D - TỔNG HỢP\" > I. Tổng công định mức",
     "—",
     "- Công chính 2.00, Công phụ 0.00\n"
     "- Tổng công định mức được giao 2.00"),

    ("009", "Đặt SL giao máy sửa chữa bằng 0 thì không tính công", "P1",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Ô SL giao lần này của M1 gõ 0",
     "—",
     "- Công chính 0.00, Tổng công định mức 0.00"),

    ("010", "Vật tư bán thêm", "P1",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Xem \"B - Danh sách vật tư bán thêm\", ô số lượng của VT1 gõ 5",
     "—",
     "- VT1: Số lượng còn trên hợp đồng 3\n"
     "- Ô số lượng tự về 3\n"
     "- Mục \"III. Tổng hợp vật tư phải giao\" có VT1"),

    ("011", "Tạo phiếu từ PL bổ sung", "P0",
     "PL-01: PL bổ sung của HD-01, Có hiệu lực, thêm 1 công sửa M1\n" + DATA,
     "1. Đăng nhập TP-1, mở Phiếu chờ giao việc, tab PL bổ sung, bấm \"Tạo phiếu giao việc\" ở PL-01\n"
     "2. Chọn ngày dự kiến, bấm \"Lưu & duyệt\"",
     "—",
     "- Form có \"Số hợp đồng\" là PL-01, mục \"A - DỊCH VỤ SỬA CHỮA BẢO DƯỠNG\"\n"
     "- Lưu thành công; ở danh sách, Số hợp đồng PL-01 bấm mở PL bổ sung"),

    ("012", "Dịch vụ bảo dưỡng: chỉ dịch vụ có số lượng mới tính công", "P1",
     "HD-03 Có hiệu lực có thiết bị bảo dưỡng TB1 với 2 dịch vụ: DV-A định mức công 1, DV-B định mức công "
     "0,5\n" + DATA,
     "1. Đăng nhập TP-1, mở form tạo phiếu giao việc từ HD-03\n"
     "2. Ở \"II - Danh mục thiết bị cần bảo dưỡng\", DV-B gõ SL 0",
     "—",
     "- Công chính 1.00 (chỉ DV-A)"),

    ("013", "Bấm Quay lại không tạo phiếu", "P2",
     DATA,
     "1. " + FROM_HD01 + "\n"
     "2. Bấm \"Quay lại\"",
     "—",
     "- Về danh sách Phiếu giao việc, không có phiếu mới\n"
     "- HD-01 vẫn chờ giao việc"),
]
