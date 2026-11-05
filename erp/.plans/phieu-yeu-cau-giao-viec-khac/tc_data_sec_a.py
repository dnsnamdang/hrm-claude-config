# -*- coding: utf-8 -*-
"""Section I - IV cho man Phieu yeu cau giao viec khac."""
from tc_data_role import MENU, DATA, OPEN_KD1, OPEN_CREATE

LIST = ("KD-1 đã lập:\n"
        "- YC-01: KH-01, HD-01, Chờ giao việc, lập 03/11/2026 09:15\n"
        "- YC-04: KH-02, không hợp đồng, Đang tạo, lập 04/11/2026 14:00")

SEC_I = [
    ("001", "Mở danh sách từ menu", "P0",
     DATA + "\n" + LIST,
     "1. " + OPEN_KD1,
     "—",
     "- Tiêu đề \"Danh sách phiếu yêu cầu giao việc khác\"\n"
     "- Có nút \"Tạo mới\"\n"
     "- Cột: STT, Số phiếu, Số hợp đồng, Khách hàng, Người lập, Ngày lập, Trạng thái, Hành động"),

    ("002", "Thứ tự dòng mới lập lên đầu", "P1",
     LIST,
     "1. " + OPEN_KD1,
     "—",
     "- YC-04 ở dòng 1, YC-01 ở dòng 2"),

    ("003", "Nội dung một dòng có hợp đồng", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Xem dòng YC-01",
     "—",
     "- Số phiếu dạng TPE.YCGVK.2026xxxxxx, bấm mở chi tiết\n"
     "- Số hợp đồng HD-01, bấm mở hợp đồng\n"
     "- Khách hàng \"<mã KH-01>-<tên KH-01>\"\n"
     "- Người lập KD-1, Ngày lập \"03/11/2026 - 09:15\"\n"
     "- Trạng thái \"Chờ giao việc\" màu vàng"),

    ("004", "Dòng không có hợp đồng", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Xem dòng YC-04",
     "—",
     "- Cột Số hợp đồng trống\n"
     "- Trạng thái \"Đang tạo\" màu đỏ"),

    ("005", "Nút hành động của người lập theo trạng thái", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Bấm nút bánh răng ở YC-04, rồi ở YC-01",
     "—",
     "- YC-04: có \"Sửa\", \"Xóa\"\n"
     "- YC-01: không có Sửa, không có Xóa, không có \"Tạo phiếu giao việc\" (KD-1 không thuộc PKT1)"),

    ("006", "Không có nút In, Xuất excel", "P2",
     LIST,
     "1. " + OPEN_KD1,
     "—",
     "- Không có nút In, không có nút Xuất excel"),

    ("007", "Mở form tạo mới", "P0",
     DATA,
     "1. " + OPEN_CREATE,
     "—",
     "- Các ô bắt buộc có dấu đỏ: Khách hàng, Người liên hệ, Thời gian dự kiến, Địa chỉ lắp đặt, Phòng tiếp "
     "nhận xử lý\n"
     "- SĐT, Địa chỉ, Hợp đồng, Phòng QTC, Nhân viên QTC không gõ được\n"
     "- Bảng \"Danh sách cần giao việc\" ghi \"Không có dữ liệu\", có nút \"Thêm dịch vụ\"\n"
     "- Nút: Lưu, Lưu và gửi duyệt, Quay lại"),

    ("008", "Nút Quay lại về danh sách", "P2",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Bấm \"Quay lại\"",
     "—",
     "- Về Danh sách phiếu yêu cầu giao việc khác, không lưu gì"),
]

SEC_II = [
    ("001", "Quyền theo công ty thấy cả phiếu mình lập ở công ty khác", "P1",
     "QL-C có quyền theo công ty, thuộc TPE; trước đây QL-C lập YC-08 khi thuộc TPC (Chờ giao việc)",
     "1. Đăng nhập QL-C, " + MENU,
     "—",
     "- Thấy YC-08 cùng các phiếu của TPE"),

    ("002", "Phòng tiếp nhận không có quyền xem không thấy yêu cầu ở danh sách này", "P1",
     "TP-1 thuộc PKT1, không có quyền xem phiếu yêu cầu giao việc khác; YC-01 phòng tiếp nhận PKT1",
     "1. Đăng nhập TP-1, " + MENU,
     "—",
     "- Không thấy YC-01 ở danh sách này (YC-01 nằm ở Phiếu chờ giao việc, tab Giao việc khác)"),

    ("003", "Phiếu Đang tạo của chính mình vẫn hiện với mọi mức quyền", "P0",
     "QL-T có quyền tổng công ty, tự lập YC-10 Đang tạo",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Thấy YC-10"),

    ("004", "Phiếu Từ chối và Đã giao việc vẫn hiện", "P1",
     "KD-1 có YC-05 Từ chối, YC-06 Đã giao việc",
     "1. " + OPEN_KD1,
     "—",
     "- Thấy YC-05 (Từ chối, màu đỏ), YC-06 (Đã giao việc, màu xanh)"),

    ("005", "Phân trang và STT", "P2",
     "KD-1 có 12 phiếu",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn hiển thị 10 dòng, sang trang 2",
     "—",
     "- Trang 2 có 2 dòng, STT 11 và 12"),
]

SEC_III = [
    ("001", "Lọc Số phiếu yêu cầu theo một phần", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ 6 số cuối của YC-01 vào ô \"Số phiếu yêu cầu\"",
     "—",
     "- Chỉ còn YC-01"),

    ("002", "Lọc Khách hàng", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Khách hàng KH-02",
     "—",
     "- Chỉ còn YC-04"),

    ("003", "Lọc Số hợp đồng gõ đủ số", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ đủ số HD-01 vào ô \"Số hợp đồng\"",
     "—",
     "- Chỉ còn YC-01"),

    ("004", "Lọc Số hợp đồng gõ một phần", "P2",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ 3 ký tự cuối của số HD-01",
     "—",
     "- Mong đợi: ra YC-01\n"
     "- Lưu ý: theo code hiện tại phải gõ đủ số, bảng trống - ghi Failed nếu nghiệp vụ cần tìm một phần"),

    ("005", "Lọc Người lập", "P1",
     "QL-C có quyền theo công ty; YC-01 do KD-1, YC-02 do KD-2 lập",
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Chọn Người lập KD-2",
     "—",
     "- Chỉ còn YC-02"),

    ("006", "Lọc Trạng thái", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Trạng thái \"Chờ giao việc\"",
     "—",
     "- Chỉ còn YC-01"),

    ("007", "Danh sách trạng thái trong ô lọc", "P2",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Mở ô Trạng thái",
     "—",
     "- Có: Đang tạo, Chờ giao việc, Đã giao việc, Từ chối"),

    ("008", "Lọc Từ ngày / Đến ngày", "P0",
     LIST + "\nYC-01 thời gian dự kiến 10/11/2026",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Từ ngày 01/11/2026, Đến ngày 30/11/2026",
     "—",
     "- Mong đợi: ra các phiếu có thời gian dự kiến trong tháng 11/2026\n"
     "- Lưu ý: theo code hiện tại bảng báo lỗi, không ra dòng nào - ghi Failed"),

    ("009", "Lọc Phòng ban với quyền theo công ty", "P1",
     "QL-C có quyền theo công ty; YC-02 do KD-2 (PKD1) lập, YC-03 do nhân viên PKT1 lập",
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Chọn Phòng ban PKD1",
     "—",
     "- Chỉ còn YC-02"),

    ("010", "Lọc Công ty với quyền tổng công ty", "P1",
     "QL-T có quyền tổng công ty; YC-02 (TPE), YC-09 (TPC)",
     "1. Đăng nhập QL-T, " + MENU + "\n"
     "2. Chọn Công ty TPC",
     "—",
     "- Chỉ còn YC-09"),

    ("011", "Kết hợp nhiều ô lọc", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Khách hàng KH-01 và Trạng thái \"Đang tạo\"",
     "—",
     "- Bảng không có dữ liệu"),
]

SEC_IV = [
    ("001", "Chọn khách hàng doanh nghiệp", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Bấm nút tìm ở ô Khách hàng, chọn KH-01",
     "—",
     "- Ô Khách hàng \"<mã KH-01> - <tên KH-01>\"\n"
     "- Địa chỉ \"12 Lê Lợi\"\n"
     "- Người liên hệ, SĐT trống, nút tìm Người liên hệ bấm được\n"
     "- Ô Địa chỉ lắp đặt bấm được"),

    ("002", "Chọn người liên hệ của khách doanh nghiệp", "P0",
     "Đã chọn KH-01",
     "1. Bấm nút tìm ở ô Người liên hệ, chọn Anh Bình",
     "—",
     "- Người liên hệ \"Anh Bình\", SĐT là số của Anh Bình"),

    ("003", "Chọn khách hàng cá nhân", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn khách hàng KH-02",
     "—",
     "- Người liên hệ tự điền \"Chị Hoa\", SĐT là số di động của Chị Hoa\n"
     "- Nút tìm Người liên hệ bị mờ"),

    ("004", "Chọn Địa chỉ lắp đặt", "P0",
     "Đã chọn KH-01, KH-01 có địa chỉ giao hàng \"Kho Bình Dương\"",
     "1. Bấm vào ô Địa chỉ lắp đặt, chọn \"Kho Bình Dương\"",
     "—",
     "- Ô Địa chỉ lắp đặt \"Kho Bình Dương\"\n"
     "- Không gõ tay được vào ô"),

    ("005", "Địa chỉ lắp đặt khóa khi chưa chọn khách", "P1",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Bấm vào ô Địa chỉ lắp đặt",
     "—",
     "- Ô bị mờ, không mở được danh sách địa chỉ"),

    ("006", "Đổi khách hàng sau khi đã chọn người liên hệ và địa chỉ", "P1",
     "Đã chọn KH-01, người liên hệ Anh Bình, Địa chỉ lắp đặt \"Kho Bình Dương\"; KH-03 là doanh nghiệp khác",
     "1. Chọn lại khách hàng KH-03",
     "—",
     "- Mong đợi: Người liên hệ, SĐT, Địa chỉ lắp đặt được xóa để chọn lại theo KH-03\n"
     "- Lưu ý: theo code hiện tại vẫn giữ Anh Bình và \"Kho Bình Dương\" của KH-01, lưu được phiếu KH-03 với "
     "thông tin KH-01 - ghi Failed"),

    ("007", "Chọn Thời gian dự kiến", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn Thời gian dự kiến 10/11/2026",
     "—",
     "- Ô hiện \"10/11/2026\""),

    ("008", "Danh sách Phòng tiếp nhận xử lý", "P1",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Mở ô Phòng tiếp nhận xử lý",
     "—",
     "- Liệt kê các phòng đang hoạt động dạng \"<mã> - <tên>\", có PKT1\n"
     "- Lưu ý: có cả phòng của công ty khác (TPC); nghiệp vụ xác nhận có cho gửi sang công ty khác không"),

    ("009", "Ghi chú tự do", "P2",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Gõ Ghi chú \"Khách cần làm buổi sáng\"",
     "—",
     "- Ô Ghi chú nhận nội dung, không bắt buộc"),
]
