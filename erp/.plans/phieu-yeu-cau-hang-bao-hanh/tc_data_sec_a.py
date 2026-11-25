# -*- coding: utf-8 -*-
"""Section I - IV cho man Phieu yeu cau hang bao hanh."""
from tc_data_role import MENU, MENU_2, DATA, OPEN_KD1, OPEN_CREATE

LIST = ("KD-1 đã lập:\n"
        "- PYC-01: BR-A / HSX-A, Chờ duyệt, tạo 20/11/2026\n"
        "- PYC-03: BR-A / HSX-A, Đã gửi NCC, tạo 05/11/2026, Ngày duyệt 06/11/2026 09:30, Người duyệt MH-1\n"
        "- PYC-04: BR-A / HSX-A, Đang tạo, tạo 24/11/2026")

SEC_I = [
    ("001", "Mở danh sách từ menu Khởi tạo", "P0",
     DATA + "\n" + LIST,
     "1. " + OPEN_KD1,
     "—",
     "- Tiêu đề trang \"Yêu cầu hãng bảo hành\"\n"
     "- Có nút Tạo mới, In, Xuất Excel\n"
     "- Cột: STT, Số phiếu, Thương hiệu, Hãng sản xuất, Ngày tạo, Ngày duyệt, Người yêu cầu, Phòng yêu cầu, "
     "Người duyệt, Trạng thái, Hành động"),

    ("002", "Mở danh sách từ menu Mua hàng", "P1",
     LIST,
     "1. Đăng nhập KD-1, " + MENU_2,
     "—",
     "- Mở cùng danh sách như menu Khởi tạo\n"
     "- Mong đợi: tên menu \"Phiếu yêu cầu hãng bảo hành\"\n"
     "- Lưu ý: menu đang ghi \"Phiếu cầu hãng bảo hành\" (thiếu chữ \"yêu\") - ghi Failed"),

    ("003", "Thứ tự dòng mới tạo lên đầu", "P1",
     LIST,
     "1. " + OPEN_KD1,
     "—",
     "- Thứ tự: PYC-04, PYC-01, PYC-03"),

    ("004", "Nội dung một dòng đã gửi NCC", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Xem dòng PYC-03",
     "—",
     "- Số phiếu dạng PYCHBH-xxxxx, bấm mở chi tiết\n"
     "- Thương hiệu BR-A, Hãng sản xuất HSX-A\n"
     "- Ngày tạo 05/11/2026, Ngày duyệt \"06/11/2026 09:30\"\n"
     "- Người yêu cầu KD-1, Phòng yêu cầu PKD1, Người duyệt MH-1\n"
     "- Trạng thái \"Đã gửi NCC\" màu xanh"),

    ("005", "Rê chuột vào Người duyệt", "P2",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Rê chuột vào tên MH-1 ở dòng PYC-03",
     "—",
     "- Hiện khung Mail và Số điện thoại của MH-1"),

    ("006", "Dòng chưa có người duyệt", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Xem dòng PYC-01",
     "—",
     "- Cột Người duyệt, Ngày duyệt trống\n"
     "- Trạng thái \"Chờ duyệt\" màu đỏ"),

    ("007", "Menu Hành động của người lập theo trạng thái", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Mở menu Hành động của PYC-04, PYC-01, PYC-03",
     "—",
     "- PYC-04 (Đang tạo): In, Xuất Excel, Sửa, Xóa\n"
     "- PYC-01, PYC-03: chỉ In, Xuất Excel"),

    ("008", "Mở form Tạo mới", "P0",
     DATA,
     "1. " + OPEN_CREATE,
     "—",
     "- Ô Thương hiệu, Hãng sản xuất trống; Công ty mặc định TPE\n"
     "- Người yêu cầu KD-1, Phòng yêu cầu PKD1\n"
     "- Bảng hàng ghi \"Chưa có hàng hóa\", nút + chọn hàng bị mờ khi chưa chọn Thương hiệu\n"
     "- Có nút Lưu, Lưu & Gửi, Quay lại"),
]

SEC_II = [
    ("001", "Người lập thấy phiếu mình lập ở mọi trạng thái", "P0",
     LIST,
     "1. " + OPEN_KD1,
     "—",
     "- Thấy PYC-04 (Đang tạo), PYC-01, PYC-03"),

    ("002", "Người được ghi là Người duyệt thấy phiếu", "P1",
     "MH-9 không phụ trách BR-A nữa (đã chuyển phân công); trước đó MH-9 lập thư yêu cầu cho PYC-03 nên là Người "
     "duyệt",
     "1. Đăng nhập MH-9, " + MENU,
     "—",
     "- Thấy PYC-03"),

    ("003", "Người mua hàng không thấy phiếu Đang tạo", "P0",
     LIST,
     "1. Đăng nhập MH-1, " + MENU,
     "—",
     "- Thấy PYC-01, PYC-03; không thấy PYC-04"),

    ("004", "Ô chờ duyệt trên trang chủ của người mua hàng", "P0",
     LIST + "\nPYC-05 do KD-2 lập, BR-A / HSX-A, Chờ duyệt",
     "1. Đăng nhập MH-1, mở trang chủ\n"
     "2. Bấm ô \"Phiếu yêu cầu hãng bảo hành chờ duyệt\"",
     "—",
     "- Ô hiện 2\n"
     "- Mở danh sách chỉ gồm PYC-01, PYC-05"),

    ("005", "Ô chờ duyệt không tính phiếu đã xử lý", "P1",
     LIST,
     "1. MH-1 Không duyệt PYC-01\n"
     "2. Tải lại trang chủ",
     "—",
     "- Ô chờ duyệt giảm 1"),

    ("006", "Danh sách chờ duyệt không có phiếu người khác phụ trách", "P1",
     "PYC-02 (BR-B) Chờ duyệt, MH-1 không phụ trách BR-B",
     "1. Đăng nhập MH-1, bấm ô chờ duyệt trên trang chủ",
     "—",
     "- Không có PYC-02"),

    ("007", "Người mua hàng phụ trách 2 cặp thương hiệu - hãng khác nhau", "P2",
     "MH-1 phụ trách BR-A / HSX-A và BR-B / HSX-B tại TPE; PYC-06 Chờ duyệt có BR-A / HSX-B",
     "1. Đăng nhập MH-1, bấm ô chờ duyệt trên trang chủ\n"
     "2. Bấm PYC-06",
     "—",
     "- Mong đợi: không có PYC-06 trong danh sách chờ duyệt (không ai phụ trách cặp BR-A / HSX-B)\n"
     "- Lưu ý: theo code hiện tại PYC-06 có trong danh sách nhưng mở ra không có nút duyệt (danh sách lọc "
     "thương hiệu và hãng tách rời) - ghi Failed"),

    ("008", "Người mua hàng có thêm quyền xem theo công ty", "P2",
     "MH-1 có thêm quyền \"Xem ... - theo công ty\" (TPE); PYC-09 do nhân viên TPC lập, Công ty gửi TPE, BR-A / "
     "HSX-A, Chờ duyệt",
     "1. Đăng nhập MH-1, " + MENU,
     "—",
     "- Mong đợi: thấy PYC-09 (MH-1 là người mua hàng phụ trách)\n"
     "- Lưu ý: theo code hiện tại không thấy ở menu này vì chỉ lọc theo công ty của người lập; vẫn thấy ở danh "
     "sách chờ duyệt - ghi Failed"),
]

SEC_III = [
    ("001", "Lọc Mã phiếu theo một phần", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ số đuôi của PYC-03 vào ô Mã phiếu",
     "—",
     "- Chỉ còn PYC-03"),

    ("002", "Lọc Thương hiệu", "P1",
     LIST + "\nPYC-07 do KD-1 lập, BR-B, Chờ duyệt",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Thương hiệu BR-B",
     "—",
     "- Chỉ còn PYC-07"),

    ("003", "Lọc Hãng sản xuất", "P1",
     LIST + "\nPYC-07 do KD-1 lập, HSX-B",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Hãng sản xuất HSX-A",
     "—",
     "- Còn PYC-04, PYC-01, PYC-03"),

    ("004", "Lọc Trạng thái", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Trạng thái \"Đã gửi NCC\"",
     "—",
     "- Chỉ còn PYC-03\n"
     "- Ô Trạng thái liệt kê đủ 7 trạng thái"),

    ("005", "Lọc Người nhận", "P1",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Người nhận MH-1",
     "—",
     "- Chỉ còn PYC-03 (phiếu đã có Người duyệt MH-1)"),

    ("006", "Lọc theo mã hoặc tên hàng", "P1",
     LIST + "\nPYC-01 có hàng H1; PYC-03 có hàng H2",
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ tên H2 vào ô \"Nhập mã hoặc tên hàng hóa...\"",
     "—",
     "- Chỉ còn PYC-03"),

    ("007", "Lọc Model và Code đặt hàng", "P2",
     LIST + "\nH1 model M-100, code đặt hàng C-111",
     "1. " + OPEN_KD1 + "\n"
     "2. Gõ \"M-100\" vào ô Model\n"
     "3. Xóa ô Model, gõ \"C-111\" vào ô Code đặt hàng",
     "—",
     "- Cả hai lần chỉ còn PYC-01"),

    ("008", "Lọc Khách hàng", "P1",
     LIST + "\nPYC-01 dòng H1 của KH-01; PYC-03 hàng tồn kho",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Khách hàng KH-01",
     "—",
     "- Chỉ còn PYC-01"),

    ("009", "Lọc Từ ngày / Đến ngày tính trọn ngày cuối", "P0",
     LIST,
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Từ ngày 20/11/2026, Đến ngày 24/11/2026",
     "—",
     "- Còn PYC-04 (tạo 24/11) và PYC-01 (20/11), không có PYC-03"),

    ("010", "Lọc Phòng ban với quyền theo công ty", "P1",
     "QL-C có quyền theo công ty TPE; PYC-01 do KD-1 (PKD1) lập; PYC-08 do nhân viên PKD2 lập (Chờ duyệt)",
     "1. Đăng nhập QL-C, " + MENU + "\n"
     "2. Chọn Phòng ban PKD2",
     "—",
     "- Chỉ còn PYC-08"),

    ("011", "Ô Phòng ban ở thanh lọc chính lọc theo phòng của phiếu", "P2",
     "PYC-01 do KD-1 lập khi còn ở PKD1; sau đó KD-1 chuyển sang PKD2",
     "1. " + OPEN_KD1 + "\n"
     "2. Chọn Phòng ban PKD1",
     "—",
     "- Vẫn có PYC-01 (phòng ghi trên phiếu lúc lập)\n"
     "- Cột Phòng yêu cầu vẫn là PKD1"),
]

SEC_IV = [
    ("001", "Chọn Thương hiệu, Hãng sản xuất tự điền Người nhận đơn", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn Thương hiệu BR-A, Hãng sản xuất HSX-A",
     "—",
     "- Người nhận đơn và Người mua hàng tự hiện MH-1\n"
     "- Hai ô này không sửa được"),

    ("002", "Đổi Công ty gửi lấy lại người mua hàng", "P1",
     DATA + "\nTại TPC, BR-A / HSX-A phân công MH-7",
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-A, HSX-A\n"
     "3. Đổi Công ty sang TPC",
     "—",
     "- Người nhận đơn, Người mua hàng đổi thành MH-7"),

    ("003", "Thương hiệu chưa phân công người mua hàng", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-B, HSX-B",
     "—",
     "- Người nhận đơn, Người mua hàng trống"),

    ("004", "Đổi Thương hiệu xóa bảng hàng", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-A, HSX-A, thêm H1, H2\n"
     "3. Đổi Thương hiệu sang BR-B",
     "—",
     "- Bảng hàng về \"Chưa có hàng hóa\""),

    ("005", "Đổi Hãng sản xuất xóa bảng hàng", "P1",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-A, HSX-A, thêm H1\n"
     "3. Đổi Hãng sản xuất sang HSX-C",
     "—",
     "- Bảng hàng về \"Chưa có hàng hóa\""),

    ("006", "Ô tìm hàng chỉ nhận hàng cùng thương hiệu", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-A, HSX-A, bấm nút + ở cột Hàng hóa\n"
     "3. Chọn H3 (BR-B)",
     "—",
     "- Báo \"Hàng hóa không cùng thương hiệu!\", H3 không được thêm"),

    ("007", "Thêm hàng thành công", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Chọn BR-A, HSX-A, bấm + và chọn H1",
     "—",
     "- Báo \"Thêm thành công\"\n"
     "- Dòng H1 hiện tên, Model, Code đặt hàng, Mã hàng, ĐVT Cái\n"
     "- Có ô Số serial, Nội dung cần bảo hành, ô tích Hàng tồn trong kho, Khách hàng, Hợp đồng, File đính kèm"),

    ("008", "Ghi chú dòng hàng", "P2",
     DATA,
     "1. " + OPEN_CREATE + ", chọn BR-A / HSX-A, thêm H1\n"
     "2. Bấm \"Ghi chú\" dưới tên hàng, gõ \"Máy kêu to\", bấm ra ngoài",
     "—",
     "- Nút hiện \"Máy kêu to\""),

    ("009", "Bỏ một dòng hàng", "P1",
     DATA,
     "1. " + OPEN_CREATE + ", chọn BR-A / HSX-A, thêm H1, H2\n"
     "2. Bấm dấu trừ ở dòng H1",
     "—",
     "- Chỉ còn dòng H2, STT đánh lại từ 1"),
]
