# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao ton kho theo vi tri'."""

MENU = "Mở menu Kho > mục \"Báo cáo kho\" > bấm \"Báo cáo tồn kho theo vị trí\""

# Du lieu mau dung chung
K1 = ("Kho K1 (công ty thuê kho TPE, TPC): nhà N1 > dãy D1 > khoang KH1 gồm vị trí P1, P2; vị trí tự do P3.\n"
      "Tồn hiện tại:\n"
      "- P1: H1 của TPE lô L01 = 20, lô L02 = 6; H4 của TPE lô L07 = 5\n"
      "- P2: H1 của TPE lô L01 = 4\n"
      "- P3: H1 của TPC lô L03 = 12")

LOC = "Chọn Tồn theo công ty TPE, Kho K1, Tính đến ngày hôm nay, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo tồn kho theo vị trí: cho biết tại MỘT kho, tính đến một ngày, mỗi VỊ TRÍ đang chứa những "
     "hàng nào, của công ty thuê kho nào, lô nào, bao nhiêu. Dùng để thủ kho đi soát kệ, kiểm kê theo vị "
     "trí.\n"
     "Người dùng làm được: lọc theo kho, công ty thuê kho, Nhà / Dãy / Khoang / Vị trí, nhóm / tính chất / "
     "loại hàng, thương hiệu, hãng sản xuất, hàng hóa, hợp đồng; đổi đơn vị tính từng hàng; Xuất Excel đầy "
     "đủ hoặc ngắn gọn. Màn chỉ xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mỗi dòng chính là 1 VỊ TRÍ có hàng tồn lớn hơn 0 tại kho đã chọn, tính tới hết ngày ở ô \"Tính đến "
     "ngày\"; sắp theo tên vị trí, 20 vị trí mỗi trang.\n"
     "- Trong vị trí: từng hàng > từng Công ty thuê kho > từng lô còn số lượng lớn hơn 0.\n"
     "- Cột Nhà Kho: mã nhà chứa vị trí; vị trí tự do hiện \"-\".\n"
     "- Lô nhập từ phiếu có hợp đồng: kèm \"Hợp đồng: <số>\" và khách hàng, ngày đặt / trả hàng.\n"
     "- Dòng \"Tổng cộng\" cuối bảng = tổng tồn của MỌI vị trí khớp bộ lọc (kể cả các trang khác)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Vị trí không có hàng hoặc chỉ có hàng tồn bằng 0 / âm.\n"
     "- Lô đã hết hàng tại vị trí.\n"
     "- Công ty thuê kho bị bỏ chọn.\n"
     "- Không có nút In (đã ẩn)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Chỉ có 1 ô \"Tính đến ngày\" (bắt buộc, mặc định hôm nay): mọi số (SL tồn vị trí, SL lô, Cộng) đều "
     "tính tới hết ngày này theo thời điểm ghi nhận nhập / xuất / điều chuyển vào kho."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Tính đến ngày, Nhóm hàng hóa, Tính chất, Loại hàng hóa, Thương hiệu, Hãng sản xuất, Hàng hóa, "
     "Hợp đồng, Tồn theo công ty, Kho (chọn 1, bắt buộc), Công ty thuê kho (tự chọn hết theo kho), 4 khung "
     "Nhà > Dãy > Khoang > Vị trí (Vị trí tự do và Vị trí thuộc khoang).\n"
     "Bảng: STT (theo vị trí), Nhà Kho, Vị trí, Tên hàng hóa, Model, Mã hàng, Thương hiệu, ĐVT (chọn được), "
     "SL tồn (của cả vị trí), Chi tiết tồn theo từng công ty gồm Công ty, Lô (kèm hợp đồng), SL, Cộng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL tồn của vị trí = tổng mọi hàng, mọi công ty trong vị trí đó.\n"
     "- Cộng của công ty = tổng SL các lô của hàng đó, công ty đó trong vị trí.\n"
     "- Đổi ĐVT của một hàng: SL lô và Cộng của hàng đó chia cho hệ số (2 số lẻ); SL tồn của vị trí không "
     "đổi.\n"
     "Với dữ liệu mẫu K1: P1 = 31, P2 = 4, P3 = 12, Tổng cộng 47."),

    ("7. Phân quyền cấp",
     "- Mở màn và Xuất Excel cần một trong 3 quyền: \"Xem báo cáo tồn kho theo tổng công ty\", \"... theo "
     "công ty\", \"... theo kho\"; không có thì ra trang không tìm thấy.\n"
     "- Quyền theo tổng công ty: ô Tồn theo công ty có mọi công ty; quyền khác chỉ có công ty mình.\n"
     "- Quyền theo kho hiện được xem mọi kho của công ty.\n"
     "- Chức năng lấy dữ liệu khi bấm Lọc KHÔNG kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang 20 vị trí, STT liên tục.\n"
     "- Xuất Excel: dưới 5 vị trí thì tải file ngay; từ 5 vị trí trở lên thì báo \"Danh sách hàng sẽ được "
     "xuất file sau ít phút!.\" và hệ thống tạo file chạy nền, mỗi file tối đa 40 vị trí; người dùng tải ở "
     "menu tài khoản > \"Download File\" (không có email, không có thông báo)."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lọc Loại hàng hóa có thể không ra kết quả nào (cách lọc khác các báo cáo tồn kho khác).\n"
     "- Xuất Excel từ 5 vị trí trở lên không tải ngay, không báo khi xong; file nằm ở \"Download File\", "
     "chia nhiều file.\n"
     "- Bấm nút làm mới thì ô Kho không còn kho nào để chọn.\n"
     "- Hợp đồng để trống ngày đặt / trả hàng thì hiện ngày hôm nay.\n"
     "- Khác Báo cáo tồn kho chi tiết theo mặt hàng: ở đây số Lô cũng tính lùi theo Tính đến ngày."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem báo cáo tồn kho thì không mở được màn", "P0",
     "NV-A không có quyền nào trong 3 quyền xem báo cáo tồn kho",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy"),

    ("01", "Quyền theo công ty mở được màn", "P0",
     "TK-1 có quyền \"Xem báo cáo tồn kho theo công ty\", thuộc TPE",
     "1. Đăng nhập TK-1, mở màn từ menu",
     "—",
     "- Tiêu đề báo cáo tồn kho theo vị trí, Tính đến ngày hôm nay, Tồn theo công ty TPE (chỉ có TPE)\n"
     "- Ô Kho trống, nút Lọc mờ\n"
     "- Khu Chi tiết ghi \"Chưa có dữ liệu\""),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "TK-2 có quyền \"Xem báo cáo tồn kho theo tổng công ty\"",
     "1. Đăng nhập TK-2, mở ô Tồn theo công ty",
     "—",
     "- Liệt kê mọi công ty, mặc định chọn công ty của TK-2"),

    ("03", "Quyền theo kho chỉ nên thấy kho được phân", "P1",
     "TK-3 có quyền \"Xem báo cáo tồn kho theo kho\", thuộc TPE, chỉ được phân K1; TPE có K1, K2",
     "1. Đăng nhập TK-3, mở ô Kho",
     "—",
     "- Mong đợi: chỉ có K1\n"
     "- Lưu ý: nếu có cả K2 thì ghi Failed"),

    ("04", "Gọi thẳng chức năng lấy dữ liệu khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu báo cáo với kho K1",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả về đủ tồn theo vị trí - ghi Failed"),

    ("05", "Xuất Excel qua đường dẫn khi không có quyền", "P1",
     "NV-A không có quyền xem báo cáo tồn kho; có sẵn đường dẫn Xuất Excel",
     "1. Đăng nhập NV-A, dán đường dẫn",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "File xuất nền chỉ người xuất thấy", "P1",
     "TK-1 vừa xuất Excel nền thành công; TK-2 là người khác",
     "1. TK-2 mở menu tài khoản > \"Download File\"",
     "—",
     "- Không thấy file của TK-1"),
]
