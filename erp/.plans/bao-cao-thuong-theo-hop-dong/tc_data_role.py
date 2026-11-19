# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao thuong theo hop dong'."""

MENU = "Mở menu Báo cáo > mục \"Báo cáo thu nhập\" > bấm \"Báo cáo thưởng theo hợp đồng\""

Q_TCT = "\"Xem báo cáo thưởng theo hợp đồng theo tổng công ty\""
Q_CT = "\"Xem báo cáo thưởng theo hợp đồng theo công ty\""
Q_PB = "\"Xem báo cáo thưởng theo hợp đồng theo phòng ban\""
Q_BP = "\"Xem báo cáo thưởng theo hợp đồng theo bộ phận\""

KT = "KT-1 thuộc TPE, có quyền " + Q_CT

# Du lieu mau dung chung (but toan TK 3351 trong thang 10/2026)
DATA = ("HD-01: hợp đồng hãng của khách KH-01, phòng P1 (phòng trên hợp đồng), đã quyết toán; doanh số tiêu "
        "chuẩn trên quyết toán 100.000.000; tỷ lệ hưởng NV-A 60%, NV-B 40%.\n"
        "BH-02: hợp đồng bảo hành sửa chữa của khách KH-02, phòng P1.\n"
        "Bút toán TK 3351 hạch toán trong tháng 10/2026:\n"
        "- HD-01, NV-A: Thưởng thực hiện hợp đồng Có 3.000.000; Năng suất tháng Có 2.000.000; Năng suất quý "
        "Có 1.500.000; Tiền vận chuyển Có 500.000\n"
        "- HD-01, NV-B: Năng suất tháng Có 1.000.000, Nợ 200.000 (điều chỉnh)\n"
        "- BH-02, NV-C: Năng suất tháng Có 1.200.000\n"
        "NV-A, NV-B, NV-C thuộc phòng P1 của TPE")

LOC_T10 = "Chọn Từ ngày 01/10/2026, Đến ngày 31/10/2026, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo thưởng theo hợp đồng: cho biết trong một khoảng ngày, mỗi HỢP ĐỒNG đã ghi nhận bao nhiêu tiền "
     "thưởng cho kinh doanh (thưởng thực hiện hợp đồng, thưởng năng suất tháng, thưởng năng suất quý, tiền "
     "vận chuyển còn lại), chia tiếp cho từng nhân viên được hưởng, kèm doanh số tiêu chuẩn.\n"
     "Người dùng làm được: lọc theo công ty, phòng ban, bộ phận, nhân viên, khoảng ngày, số hợp đồng, khách "
     "hàng; sắp xếp theo các cột số tiền; bấm số hợp đồng để mở hợp đồng; In; Xuất excel. Màn chỉ xem, "
     "không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mỗi dòng chính là 1 hợp đồng hãng hoặc 1 hợp đồng bảo hành sửa chữa có bút toán TK 3351 gắn hợp đồng "
     "và gắn nhân viên, ngày hạch toán trong khoảng ngày, và ít nhất một cột thưởng khác 0.\n"
     "- Dưới mỗi hợp đồng là các dòng nhân viên có bút toán của hợp đồng đó (STT dạng 1.1, 1.2).\n"
     "- Mỗi cột = phát sinh Có trừ phát sinh Nợ của TK 3351 theo đúng vụ việc của cột.\n"
     "- Sắp mặc định theo số hợp đồng giảm dần, 10 hợp đồng mỗi trang."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán của phiếu chi, ủy nhiệm chi và kết chuyển chi phí phải trả (không làm giảm số thưởng).\n"
     "- Bút toán không gắn hợp đồng hoặc không gắn nhân viên.\n"
     "- Hợp đồng loại khác ngoài hợp đồng hãng và hợp đồng bảo hành sửa chữa.\n"
     "- Hợp đồng mà mọi cột thưởng đều bằng 0 trong kỳ; nhân viên mà mọi cột của mình bằng 0.\n"
     "- Thưởng thêm không có cột trên báo cáo này."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày, Đến ngày bắt buộc (nút Lọc mờ khi thiếu một trong hai). Lọc theo NGÀY HẠCH TOÁN của bút "
     "toán, tính trọn ngày Đến ngày. Doanh số tiêu chuẩn KHÔNG phụ thuộc khoảng ngày (lấy theo quyết toán "
     "hợp đồng)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Công ty (chỉ quyền theo tổng công ty), Phòng ban, Bộ phận, Nhân viên (hiện theo quyền), Từ ngày, "
     "Đến ngày, Hợp đồng (gõ một phần số), Khách hàng (chọn qua nút tìm, có nút x để bỏ); nút Lọc, làm mới, "
     "In, Xuất excel.\n"
     "Bảng: STT, Hợp đồng (bấm mở hợp đồng), Khách hàng (mã - tên), Phòng ban, Thưởng thực hiện hợp đồng, "
     "Thưởng năng suất tháng, Thưởng năng suất quý, Tiền vận chuyển còn lại, Tổng cộng, Doanh số tiêu chuẩn; "
     "dòng Tổng cộng ngay dưới tiêu đề.\n"
     "Dòng nhân viên: Hợp đồng ghi tên nhân viên, Khách hàng để trống, Phòng ban là phòng HIỆN TẠI của nhân "
     "viên."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tổng cộng của dòng = Thưởng thực hiện hợp đồng + Năng suất tháng + Năng suất quý + Tiền vận chuyển còn "
     "lại (không cộng Doanh số tiêu chuẩn).\n"
     "- Dòng hợp đồng = tổng các dòng nhân viên của hợp đồng đó.\n"
     "- Doanh số tiêu chuẩn: dòng hợp đồng hãng = doanh số tiêu chuẩn trên quyết toán hợp đồng; dòng nhân "
     "viên = doanh số đó nhân tỷ lệ hưởng của nhân viên (chỉ khi hợp đồng Đã quyết toán); hợp đồng bảo hành "
     "sửa chữa luôn \"-\".\n"
     "Với dữ liệu mẫu: HD-01 = 3.000.000 / 2.800.000 / 1.500.000 / 500.000, Tổng 7.800.000, DS 100.000.000; "
     "NV-A Tổng 7.000.000, DS 60.000.000; NV-B Tổng 800.000, DS 40.000.000; BH-02 Năng suất tháng 1.200.000."),

    ("7. Phân quyền cấp",
     "- 4 quyền: " + Q_TCT + ", " + Q_CT + ", " + Q_PB + ", " + Q_BP + ".\n"
     "- Không có quyền nào vẫn mở được màn, chỉ thấy số tiền của chính mình.\n"
     "- Theo công ty: bút toán của công ty mình (và của chính mình). Theo phòng ban: bút toán thuộc các phòng "
     "mình phụ trách. Theo bộ phận: bút toán thuộc bộ phận của mình.\n"
     "- Phạm vi xét theo phòng ban / bộ phận ghi trên BÚT TOÁN, không theo phòng trên hợp đồng.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Dòng Tổng cộng cộng MỌI hợp đồng khớp bộ lọc (kể cả các trang khác).\n"
     "- STT hợp đồng liên tục qua các trang.\n"
     "- In và Xuất excel lấy toàn bộ hợp đồng (không phân trang), giữ thứ tự đang sắp; file Excel ghi số "
     "thô, không có dấu phân cách."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Doanh số tiêu chuẩn của dòng hợp đồng luôn là doanh số của CẢ hợp đồng, không theo khoảng ngày, không "
     "theo nhân viên đang lọc.\n"
     "- Lọc Phòng ban xét phòng ghi trên bút toán; cột Phòng ban của dòng hợp đồng lại là phòng trên hợp "
     "đồng, nên hai giá trị có thể khác nhau.\n"
     "- Doanh số tiêu chuẩn đang bị nhân đôi ở hầu hết hợp đồng đã quyết toán (cộng 2 bản lưu của cùng "
     "hợp đồng).\n"
     "- Không có cột Thưởng thêm nên Tổng cộng có thể nhỏ hơn Bảng tổng hợp thu nhập từ bán hàng."),
]


ROLE_TCS = [
    ("00", "Không có quyền vẫn mở được màn, chỉ thấy số của mình", "P0",
     "NV-A không có quyền nào trong 4 quyền xem báo cáo thưởng theo hợp đồng\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. " + LOC_T10,
     "Tài khoản: NV-A",
     "- Màn mở bình thường, không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Chỉ có HD-01, các cột là số của NV-A: 3.000.000 / 2.000.000 / 1.500.000 / 500.000, Tổng 7.000.000\n"
     "- Dưới HD-01 chỉ có dòng NV-A; không có BH-02"),

    ("01", "Quyền theo công ty thấy mọi hợp đồng của công ty", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty\n"
     "- Có HD-01 (Tổng 7.800.000, 2 dòng NV-A, NV-B) và BH-02 (Tổng 1.200.000, dòng NV-C)"),

    ("02", "Quyền theo công ty không thấy công ty khác", "P0",
     KT + "; hợp đồng HD-09 của TPC có bút toán thưởng NV-T (thuộc TPC) 5.000.000 trong tháng 10/2026",
     "1. KT-1 " + LOC_T10.lower(),
     "—",
     "- Không có HD-09; dòng Tổng cộng không cộng 5.000.000 của TPC"),

    ("03", "Quyền theo tổng công ty thấy mọi công ty và có ô Công ty", "P0",
     "TGĐ-1 có quyền " + Q_TCT + "; dữ liệu như TC 02",
     "1. Đăng nhập TGĐ-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Công ty\n"
     "- Có cả HD-01, BH-02 của TPE và HD-09 của TPC"),

    ("04", "Quyền theo phòng ban chỉ thấy bút toán phòng mình phụ trách", "P0",
     "TP-1 có quyền " + Q_PB + ", phụ trách phòng P1; NV-D phòng P2 có bút toán thưởng HD-05 2.000.000 "
     "trong tháng 10/2026\n" + DATA,
     "1. Đăng nhập TP-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có HD-01, BH-02; không có HD-05\n"
     "- Không có ô Công ty; không có ô Phòng ban (chỉ phụ trách 1 phòng); có ô Bộ phận, Nhân viên"),

    ("05", "Trưởng phòng phụ trách nhiều phòng có ô Phòng ban", "P1",
     "TP-2 có quyền " + Q_PB + ", phụ trách P1 và P2",
     "1. Đăng nhập TP-2, mở màn",
     "—",
     "- Có ô Phòng ban để chọn P1 hoặc P2"),

    ("06", "Quyền theo bộ phận chỉ thấy bút toán bộ phận mình", "P1",
     "TN-1 có quyền " + Q_BP + ", thuộc bộ phận BP1 của P1; NV-A thuộc BP1, NV-B thuộc BP2\n" + DATA,
     "1. Đăng nhập TN-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có ô Nhân viên (không có Công ty, Phòng ban, Bộ phận)\n"
     "- HD-01 chỉ cộng phần của NV-A (Tổng 7.000.000), không có dòng NV-B"),

    ("07", "Gọi thẳng chức năng lấy dữ liệu khi không có quyền", "P1",
     "NV-B không có quyền xem báo cáo thưởng theo hợp đồng\n" + DATA,
     "1. Đăng nhập NV-B\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu báo cáo tháng 10/2026, kèm Công ty TPE "
     "và Nhân viên NV-A",
     "—",
     "- Không trả về số của NV-A; chỉ có số của chính NV-B (HD-01 Năng suất tháng 800.000) hoặc trống"),

    ("08", "In / Xuất excel qua đường dẫn khi không có quyền", "P1",
     "NV-B không có quyền; KT-1 đã copy đường dẫn Xuất excel tháng 10/2026",
     "1. Đăng nhập NV-B, dán đường dẫn Xuất excel\n"
     "2. Dán đường dẫn In",
     "—",
     "- File và bản in chỉ có số của NV-B, không có số của người khác"),
]
