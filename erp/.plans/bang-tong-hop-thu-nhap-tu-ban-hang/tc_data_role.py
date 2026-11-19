# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bang tong hop thu nhap tu ban hang'."""

MENU = "Mở menu Báo cáo > mục \"Báo cáo thu nhập\" > bấm \"Bảng tổng hợp thu nhập từ bán hàng\""

# Du lieu mau dung chung
DATA = ("Công ty TPE, kỳ quyết toán Năm 2026 Kì 3 (01/07/2026 - 30/09/2026). Phòng KD1 có NV-A, NV-B; "
        "phòng KD2 có NV-C.\n"
        "Số dư TK 3351 (Có trừ Nợ) ghi sổ trong kỳ:\n"
        "- NV-A, HD-01 (hợp đồng hãng, có xuất hóa đơn): Thưởng năng suất tháng 10.000.000; Thưởng năng "
        "suất quý 5.000.000; Thưởng thêm 2.000.000; Thưởng thực hiện hợp đồng 3.000.000; Tiền vận chuyển "
        "1.000.000\n"
        "- NV-A, HD-02 (hợp đồng bảo hành sửa chữa, không xuất hóa đơn): Thưởng năng suất tháng 4.000.000\n"
        "- NV-B, HD-01: Thưởng năng suất tháng ghi Có 6.000.000, ghi Nợ điều chỉnh 1.000.000\n"
        "- NV-C, HD-03: Thưởng năng suất quý 8.000.000\n"
        "HD-01 đã quyết toán QT-01: DS tiêu chuẩn NV-A 200.000.000, NV-B 100.000.000; lãi quá hạn NV-A "
        "500.000. HD-02, HD-03 chưa quyết toán.")

KY = "Chọn Năm 2026, Kì 3, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Bảng tổng hợp thu nhập từ bán hàng: cho biết trong một kỳ, mỗi nhân viên kinh doanh (gom theo phòng "
     "ban) được ghi nhận bao nhiêu tiền thưởng năng suất tháng, quý, thưởng thêm, thưởng thực hiện hợp đồng, "
     "tiền vận chuyển, cùng doanh số tiêu chuẩn, lãi quá hạn, thưởng bị trừ quá hạn.\n"
     "Người dùng làm được: chọn kỳ quyết toán hoặc khoảng ngày, lọc công ty / phòng ban / bộ phận / nhân "
     "viên / xuất hóa đơn; bấm tên nhân viên xem chi tiết theo từng hợp đồng; In, Xuất excel bảng tổng hợp "
     "và bảng chi tiết nhân viên. Màn chỉ xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Lấy bút toán TK 3351 (Chi phí phải trả ngắn hạn) có gắn nhân viên và gắn hợp đồng (hợp đồng hãng "
     "hoặc hợp đồng bảo hành sửa chữa), ngày hạch toán của chứng từ nằm trong kỳ.\n"
     "- Mỗi cột thưởng = số ghi Có trừ số ghi Nợ của đúng vụ việc: Thưởng năng suất tháng, Thưởng năng "
     "suất quý, Thưởng thêm, Thưởng thực hiện hợp đồng, Tiền vận chuyển.\n"
     "- Bảng gom theo phòng ban của nhân viên trên bút toán: dòng phòng (in đậm) rồi các dòng nhân viên."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán của phiếu chi, ủy nhiệm chi, phiếu kết chuyển chi phí phải trả (phần chi trả, kết chuyển) "
     "không được tính.\n"
     "- Bút toán không gắn hợp đồng hoặc không gắn nhân viên không được tính.\n"
     "- Nhân viên ngoài phạm vi quyền xem."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- Chọn Năm thì phải chọn Kì quyết toán; Từ ngày, Đến ngày tự lấy theo kỳ cấu hình của công ty và bị "
     "khóa. Mặc định Năm = năm hiện tại, Kì trống.\n"
     "- Bỏ Năm (chọn \"Chọn năm\") thì nhập Từ ngày, Đến ngày (bắt buộc).\n"
     "- Kỳ lọc theo ngày hạch toán của chứng từ sinh bút toán. DS tiêu chuẩn, lãi quá hạn lấy từ phiếu "
     "quyết toán hợp đồng, không phụ thuộc ngày."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Công ty, Phòng ban, Bộ phận, Nhân viên (hiện theo quyền), Năm, Kì quyết toán, Từ ngày, Đến "
     "ngày, Xuất hóa đơn (Tất cả / Xuất hóa đơn / Không xuất hóa đơn); nút Lọc, làm mới, In, Xuất excel.\n"
     "Bảng: STT, Nhân viên, DS tính thưởng năng suất tháng, DS tiêu chuẩn tính thưởng năng suất quý, Thưởng "
     "năng suất tháng, Thưởng năng suất quý, Tổng thưởng năng suất tính lũy tiến, Thưởng thêm, Thưởng thực "
     "hiện hợp đồng, Tiền vận chuyển, Tổng thu nhập từ bán hàng, Lãi quá hạn, Thưởng năng suất bị trừ quá "
     "hạn. Dòng Tổng cộng ngay dưới tiêu đề.\n"
     "Cửa sổ chi tiết nhân viên: lọc Hợp đồng, Khách hàng; cột Hợp đồng (bấm mở), Khách hàng, Số quyết toán "
     "(bấm mở), Ngày bàn giao, Ngày thanh toán và các cột tiền như bảng chính."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng thưởng năng suất tính lũy tiến = Thưởng năng suất tháng + quý.\n"
     "- Tổng thu nhập từ bán hàng = tháng + quý + Thưởng thêm + Thưởng thực hiện hợp đồng + Tiền vận "
     "chuyển (không gồm Lãi quá hạn, Thưởng bị trừ quá hạn).\n"
     "- DS tiêu chuẩn tháng và quý cùng lấy doanh số của nhân viên trên phiếu quyết toán hợp đồng; hợp đồng "
     "chưa quyết toán hiện \"-\".\n"
     "Với dữ liệu mẫu: NV-A tháng 14.000.000, quý 5.000.000, tổng thu nhập 25.000.000, DS tiêu chuẩn "
     "200.000.000, lãi quá hạn 500.000; NV-B tháng 5.000.000; NV-C quý 8.000.000; KD1 tổng thu nhập "
     "30.000.000; Tổng cộng 38.000.000."),

    ("7. Phân quyền cấp",
     "Quyền \"Xem báo cáo tổng thu nhập từ bán hàng\" có 4 phạm vi:\n"
     "- Tổng công ty: mọi công ty, có ô Công ty.\n"
     "- Công ty: nhân viên cùng công ty.\n"
     "- Phòng ban: các phòng mình quản lý.\n"
     "- Bộ phận: bộ phận của mình.\n"
     "Phạm vi nào cũng luôn thấy số của chính mình. Không có quyền vẫn mở được màn (menu không ẩn) nhưng "
     "chỉ thấy số của chính mình."),

    ("8. Cách tính các ô thống kê",
     "- Dòng Tổng cộng = tổng của mọi nhân viên khớp bộ lọc (kể cả trang khác).\n"
     "- Dòng phòng ban = tổng các nhân viên của phòng đang hiện trên trang.\n"
     "- STT phòng 1, 2...; STT nhân viên 1.1, 1.2...\n"
     "- Phân trang 10 nhân viên mỗi trang; cửa sổ chi tiết 10 hợp đồng mỗi trang.\n"
     "- In / Xuất excel lấy toàn bộ, không phân trang. Ô bằng 0 hiện \"-\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Phòng có nhân viên nằm ở 2 trang thì dòng phòng ở mỗi trang chỉ cộng nhân viên trên trang đó, phòng "
     "lặp lại ở trang sau (đã đối chiếu dữ liệu thật quý 3/2025: Phòng Thiết bị ô tô 2 hiện 87,96 triệu ở "
     "trang 1 và 5,44 triệu ở trang 2, đúng phải là 93,40 triệu).\n"
     "- Đổi Năm khi đã chọn Kì: Kì vẫn hiện nhưng Từ ngày / Đến ngày bị xóa, Lọc ra bảng trống, In báo lỗi.\n"
     "- Thưởng thêm từ phiếu năng suất quý phiên bản mới (ghi theo nhân viên, không gắn hợp đồng) không "
     "được cộng.\n"
     "- Nhân viên chuyển phòng trong kỳ chỉ hiện dưới một phòng.\n"
     "- Lãi quá hạn của trưởng phòng có thể bị gán cho cả nhân viên không có dòng trên phiếu quyết toán."),
]


ROLE_TCS = [
    ("00", "Không có quyền vẫn mở được màn, chỉ thấy số của mình", "P0",
     "NV-A không có quyền \"Xem báo cáo tổng thu nhập từ bán hàng\"\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. " + KY,
     "Tài khoản: NV-A",
     "- Mở được màn, không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Bảng chỉ có phòng KD1 với 1 dòng NV-A, Tổng cộng 25.000.000\n"
     "- Không thấy NV-B, NV-C"),

    ("01", "Quyền theo công ty thấy mọi nhân viên của công ty", "P0",
     "KT-1 thuộc TPE có quyền xem phạm vi Công ty\n" + DATA,
     "1. Đăng nhập KT-1, mở màn\n"
     "2. " + KY,
     "—",
     "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty\n"
     "- Bảng có KD1 (NV-A, NV-B) và KD2 (NV-C); Tổng cộng 38.000.000"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "KT-2 có quyền xem phạm vi Tổng công ty; TPC có NV-D có thưởng trong kỳ",
     "1. Đăng nhập KT-2, mở màn\n"
     "2. Không chọn Công ty, chọn Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Có ô Công ty\n"
     "- Bảng có cả nhân viên TPE và NV-D của TPC"),

    ("03", "Quyền theo phòng ban chỉ thấy phòng mình quản lý", "P0",
     "TP-1 có quyền xem phạm vi Phòng ban, quản lý KD1; TP-1 không có thưởng\n" + DATA,
     "1. Đăng nhập TP-1, mở màn\n"
     "2. " + KY,
     "—",
     "- Chỉ có phòng KD1 với NV-A, NV-B\n"
     "- Không có KD2, NV-C"),

    ("04", "Quyền theo phòng ban luôn thấy số của chính mình", "P1",
     "TP-2 quản lý KD2, bản thân TP-2 thuộc KD3 và có Thưởng năng suất tháng 2.000.000 ở HD-05",
     "1. Đăng nhập TP-2, " + KY,
     "—",
     "- Có KD2 (NV-C) và dòng của chính TP-2 dưới KD3"),

    ("05", "Quyền theo bộ phận chỉ thấy bộ phận mình", "P1",
     "NV-B có quyền xem phạm vi Bộ phận; NV-A cùng bộ phận BP1 với NV-B; NV-C khác bộ phận\n" + DATA,
     "1. Đăng nhập NV-B, " + KY,
     "—",
     "- Thấy NV-A, NV-B; không thấy NV-C\n"
     "- Chỉ có ô Nhân viên, không có ô Phòng ban, Bộ phận"),

    ("06", "Quyền theo công ty chọn công ty khác qua đường dẫn", "P1",
     "KT-1 thuộc TPE có quyền phạm vi Công ty",
     "1. Đăng nhập KT-1\n"
     "2. Mở màn bằng đường dẫn có thêm tham số công ty là TPC, bấm Lọc kỳ 3/2026",
     "—",
     "- Bảng trống hoặc chỉ có số của chính KT-1, không hiện nhân viên TPC"),

    ("07", "Mở chi tiết nhân viên ngoài phạm vi qua đường dẫn", "P1",
     "NV-A không có quyền xem\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. Mở thẳng đường dẫn In chi tiết nhân viên với nhân viên là NV-C, kỳ 01/07/2026 - 30/09/2026",
     "—",
     "- Bản in có tên NV-C nhưng bảng không có hợp đồng nào, các tổng bằng \"-\""),
]
