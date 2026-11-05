# -*- coding: utf-8 -*-
"""Section VIII - XII: trang thai lien quan, xuat Excel, rang buoc, dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_YC, HD, YC1, YC2, KT1, TAO, TIEN_YC1

SEC_VIII = [
    ("001", "Phiếu yêu cầu bị Không duyệt khi đã có phiếu hạch toán Đang tạo", "P0",
     "HT-3 Đang tạo do KT-1 lập từ YC-1; KT-5 bấm Không duyệt YC-1 (YC-1 thành Không duyệt)",
     "1. KT-1 mở Sửa HT-3, bấm \"Lưu & Duyệt\"",
     "—",
     "- Mong đợi: bị chặn, báo phiếu yêu cầu không còn chờ hạch toán\n"
     "- Lưu ý: theo code hiện tại HT-3 duyệt được, bút toán được ghi, YC-1 bị đổi thành Đã hạch toán - ghi "
     "Failed"),

    ("002", "Không lập được phiếu từ phiếu yêu cầu đã Đã hạch toán", "P0",
     "YC-1 đã Đã hạch toán (HT-2)",
     "1. KT-1 mở Chi tiết YC-1",
     "—",
     "- Không có nút \"Hạch toán dịch vụ\""),

    ("003", "Phiếu yêu cầu Đang tạo không lập được phiếu", "P1",
     "YC-7 Đang tạo do NV-1 lập",
     "1. KT-1 dán đường dẫn tạo phiếu kèm YC-7",
     "—",
     "- Báo \"Không thể yêu cầu hạch toán làm dịch vụ cho hợp đồng này\", bảng chi tiết trống"),

    ("004", "Xóa phiếu Đang tạo rồi lập lại", "P1",
     "HT-3 Đang tạo do KT-1 lập từ YC-1",
     "1. KT-1 xóa HT-3\n"
     "2. Mở YC-1, bấm \"Hạch toán dịch vụ\", bấm \"Lưu & Duyệt\"",
     "—",
     "- Tạo được phiếu mới Đã duyệt, YC-1 Đã hạch toán"),

    ("005", "Người lập phiếu yêu cầu không còn sửa, xóa sau khi hạch toán", "P0",
     "YC-1 Đã hạch toán",
     "1. NV-1 mở Hành động của YC-1",
     "—",
     "- Không có Sửa, Xóa"),

    ("006", "Phiếu yêu cầu bị Không duyệt rồi xóa khi phiếu hạch toán còn Đang tạo", "P2",
     "HT-3 Đang tạo từ YC-1; YC-1 bị Không duyệt, NV-1 xóa YC-1",
     "1. KT-1 mở Sửa HT-3",
     "—",
     "- Mong đợi: HT-3 không còn mở sửa được hoặc báo phiếu yêu cầu đã bị xóa\n"
     "- Lưu ý: nếu trang báo lỗi kỹ thuật thì ghi Failed"),
]

SEC_IX = [
    ("001", "Xuất excel danh sách", "P0",
     "KT-1 thấy 3 phiếu trên danh sách",
     "1. Bấm Xuất excel",
     "—",
     "- Tải file danh_sach_hach_toan_lam_dich_vu.xlsx\n"
     "- Tiêu đề \"DANH SÁCH HẠCH TOÁN DỊCH VỤ\", có logo đầu trang\n"
     "- Cột STT, Ngày lập, Mã, Số hợp đồng, Khách hàng, Tổng thanh toán, Người lập, Ngày duyệt, Trạng thái; 3 "
     "dòng"),

    ("002", "Xuất excel theo bộ lọc", "P0",
     "HT-2 của KH-1, HT-7 của KH-2",
     "1. Lọc Khách hàng KH-1, bấm Tìm\n"
     "2. Bấm Xuất excel",
     "—",
     "- File chỉ có HT-2"),

    ("003", "Xuất excel ghi khoảng ngày lọc", "P1",
     "—",
     "1. Chọn Từ ngày 01/11/2026, Đến ngày 05/11/2026, bấm Tìm\n"
     "2. Bấm Xuất excel",
     "—",
     "- Dưới tiêu đề có dòng \"Từ ngày 01/11/2026 đến ngày 05/11/2026\""),

    ("004", "Số liệu dòng trong file khớp màn hình", "P0",
     "HT-2 Đã duyệt lúc 09:30 ngày 05/11/2026",
     "1. Xuất excel, tìm dòng HT-2",
     "—",
     "- Tổng thanh toán 1,980,000; Người lập KT-1; Trạng thái Đã duyệt\n"
     "- Ngày duyệt 05/11/2026 09:30:00"),

    ("005", "Phiếu Đang tạo trong file để trống Ngày duyệt", "P2",
     "HT-3 Đang tạo của KT-1",
     "1. KT-1 xuất excel, tìm dòng HT-3",
     "—",
     "- Cột Ngày duyệt trống, Trạng thái Đang tạo"),

    ("006", "Cộng được cột Tổng thanh toán trong file", "P2",
     "File có 3 phiếu",
     "1. Mở file, dùng hàm cộng trên cột Tổng thanh toán",
     "—",
     "- Mong đợi: ra tổng tiền 3 phiếu\n"
     "- Lưu ý: nếu cột lưu dạng chữ, tổng bằng 0 - ghi Failed"),

    ("007", "File không chứa phiếu ngoài quyền", "P0",
     "KT-2 quyền theo công ty TPE; HT-5 của TPC",
     "1. KT-2 bấm Xuất excel",
     "—",
     "- File không có HT-5"),
]

SEC_X = [
    ("001", "Gọi thẳng chức năng lưu với trạng thái không có trên màn", "P1",
     YC1,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu cho YC-1 với trạng thái là số 3",
     "—",
     "- Mong đợi: bị chặn vì trạng thái không hợp lệ\n"
     "- Lưu ý: theo code hiện tại phiếu được tạo với trạng thái không có tên, không sửa / xóa được - ghi "
     "Failed"),

    ("002", "Gọi thẳng chức năng lưu với phiếu yêu cầu không Chờ duyệt", "P0",
     "YC-1 đã Đã hạch toán",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu cho YC-1",
     "—",
     "- Báo \"Thao tác thất bại\", không tạo phiếu"),

    ("003", "Gọi thẳng chức năng lưu không kèm dòng chi tiết", "P1",
     YC1,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu cho YC-1, bỏ trống cả danh sách gói dịch vụ và "
     "dịch vụ đi kèm",
     "—",
     "- Báo \"Thao tác thất bại\", không tạo phiếu"),

    ("004", "Gọi thẳng chức năng lưu với Tổng thanh toán tự sửa", "P1",
     YC1,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu cho YC-1, Tổng thanh toán 10.000, trạng thái Đã "
     "duyệt",
     "—",
     "- Mong đợi: Tổng thanh toán tính lại theo dòng chi tiết (1.980.000)\n"
     "- Lưu ý: theo code hiện tại danh sách và file excel ghi 10,000 trong khi bút toán vẫn 1.980.000 - ghi "
     "Failed"),

    ("005", "Gọi thẳng chức năng sửa phiếu Đã duyệt", "P0",
     "HT-2 Đã duyệt do KT-1 lập",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng sửa HT-2 với Ghi chú mới",
     "—",
     "- Bị chặn, HT-2 và bút toán không đổi"),

    ("006", "Sửa đổi sang phiếu yêu cầu của hợp đồng khác", "P1",
     "HT-3 Đang tạo do KT-1 lập từ YC-1 (HD-01); KT-1 tự lập YC-8 Chờ duyệt của HD-02",
     "1. KT-1 mở Sửa HT-3, chọn phiếu yêu cầu YC-8, bấm \"Lưu & Duyệt\"\n"
     "2. Xem Số hợp đồng của HT-3 và bút toán",
     "—",
     "- Mong đợi: HT-3 chuyển sang HD-02, công nợ ghi cho khách của HD-02\n"
     "- Lưu ý: theo code hiện tại HT-3 vẫn gắn HD-01, bút toán dùng số tiền của YC-8 nhưng ghi cho khách "
     "HD-01 - ghi Failed"),

    ("007", "Ghi chú dài và có ký tự đặc biệt", "P2",
     YC1,
     "1. " + TAO + "\n"
     "2. Ghi chú 500 ký tự có dấu & < >, bấm Lưu",
     "—",
     "- Lưu thành công, Ghi chú hiện đúng nguyên văn ở Chi tiết"),
]

SEC_XI = [
    ("001", "Hai phiếu hạch toán từ cùng một phiếu yêu cầu", "P0",
     YC1 + "\n" + KT1,
     "1. KT-1 lập HT-3 từ YC-1, bấm Lưu\n"
     "2. KT-1 mở lại YC-1, bấm \"Hạch toán dịch vụ\", bấm Lưu (HT-4)\n"
     "3. Lần lượt mở Sửa HT-3 và HT-4, bấm \"Lưu & Duyệt\"",
     "—",
     "- Mong đợi: bước 2 bị chặn vì YC-1 đã có phiếu hạch toán; hoặc bước 3 chỉ duyệt được 1 phiếu\n"
     "- Lưu ý: theo code hiện tại cả 2 phiếu Đã duyệt, công nợ KH-1 tăng 3.960.000 - ghi Failed"),

    ("002", "Hai tab cùng Lưu & Duyệt một phiếu yêu cầu", "P0",
     YC1 + "\nKT-1 và KT-5 cùng có quyền hạch toán",
     "1. KT-1 và KT-5 cùng mở form hạch toán YC-1\n"
     "2. Bấm \"Lưu & Duyệt\" ở 2 tab gần như cùng lúc",
     "—",
     "- Mong đợi: chỉ 1 phiếu thành công, tab còn lại báo phiếu yêu cầu không còn Chờ duyệt\n"
     "- Lưu ý: nếu có 2 phiếu Đã duyệt và bút toán ghi 2 lần thì ghi Failed"),

    ("003", "Tab mở sẵn bấm Lưu & Duyệt sau khi người khác đã duyệt", "P0",
     YC1,
     "1. KT-1 mở form hạch toán YC-1, để đó\n"
     "2. KT-5 hạch toán YC-1 bằng \"Lưu & Duyệt\"\n"
     "3. KT-1 bấm \"Lưu & Duyệt\"",
     "—",
     "- KT-1 nhận \"Thao tác thất bại\", không tạo phiếu thứ hai"),

    ("004", "Mã phiếu theo công ty người lập", "P1",
     "KT-1 thuộc TPE, KT-6 thuộc TPC cùng lập phiếu",
     "1. Xem mã 2 phiếu vừa lập",
     "—",
     "- Phiếu KT-1 dạng TPE.HTDV.<số>, phiếu KT-6 dạng TPC.HTDV.<số>, số tăng dần"),

    ("005", "Người cùng phòng không thấy phiếu Đang tạo của nhau", "P1",
     "KT-1 và KT-5 cùng phòng, KT-5 có quyền theo phòng ban; HT-3 Đang tạo của KT-1",
     "1. KT-5 mở danh sách",
     "—",
     "- Không có HT-3"),
]

SEC_XII = [
    ("001", "Luồng chuẩn hạch toán dịch vụ đi kèm", "P0",
     HD + "\n" + YC1 + "\n" + KT1,
     "1. " + TAO + ", bấm \"Lưu & Duyệt\"\n"
     "2. Mở Chi tiết phiếu, tab Hạch toán\n"
     "3. Mở YC-1\n"
     "4. Mở báo cáo công nợ KH-1",
     "—",
     "- Phiếu Đã duyệt, " + TIEN_YC1 + "\n"
     "- Bút toán doanh thu, giảm trừ, giá vốn như mục VII\n"
     "- YC-1 Đã hạch toán, NV-1 có thông báo\n"
     "- Dư nợ KH-1 tăng 1.980.000"),

    ("002", "Luồng Lưu nháp, sửa rồi duyệt", "P0",
     HD + "\n" + YC1,
     "1. " + TAO + ", bấm Lưu\n"
     "2. Kiểm tra YC-1 vẫn Chờ duyệt, công nợ chưa đổi\n"
     "3. Mở Sửa phiếu, bấm \"Lưu & Duyệt\"",
     "—",
     "- Sau bước 2: không có bút toán\n"
     "- Sau bước 3: phiếu Đã duyệt, bút toán như mục VII, YC-1 Đã hạch toán"),

    ("003", "Luồng hạch toán phí vận chuyển", "P0",
     HD + "\n" + YC2,
     "1. KT-1 hạch toán YC-2, bấm \"Lưu & Duyệt\"\n"
     "2. Xem tab Hạch toán, mở HD-01",
     "—",
     "- Nợ 1311 540.000 / Có 5113 500.000, Có 33311 40.000\n"
     "- HD-01 không cho lập thêm yêu cầu hạch toán vận chuyển"),

    ("004", "Luồng hạch toán hết hợp đồng rồi xem hạn thanh toán", "P1",
     "HD-01 đã xuất hàng đủ; YC-1 và YC-2 Chờ duyệt",
     "1. KT-1 Lưu & Duyệt phiếu từ YC-1\n"
     "2. KT-1 Lưu & Duyệt phiếu từ YC-2\n"
     "3. Mở HD-01",
     "—",
     "- Sau bước 1: chưa có ngày bàn giao\n"
     "- Sau bước 3: Ngày bàn giao hôm nay, hạn thanh toán = hôm nay cộng số ngày được nợ"),

    ("005", "Luồng phiếu yêu cầu bị trả về", "P1",
     YC1,
     "1. KT-5 bấm Không duyệt YC-1 với lý do \"Sai giá\"\n"
     "2. NV-1 sửa YC-1, gửi lại (Chờ duyệt)\n"
     "3. KT-1 hạch toán YC-1, bấm \"Lưu & Duyệt\"",
     "—",
     "- Sau bước 1: không có nút \"Hạch toán dịch vụ\"\n"
     "- Sau bước 3: phiếu Đã duyệt theo số liệu mới của YC-1"),
]
