# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao thuong theo nhan vien'."""

MENU = "Mở menu Báo cáo bán hàng > mục \"Báo cáo thu nhập\" > bấm \"Báo cáo thưởng theo nhân viên\""

# Du lieu mau dung chung (hom nay 17/11/2026)
DATA = ("Công ty TPE: phòng PKD1 (bộ phận BP1 có NV-A; bộ phận BP2 có NV-B), phòng PKD2 có NV-C. "
        "Công ty TPC: phòng PKD5 có NV-D. Phòng PKD9 của TPE đã ngừng hoạt động, có NV-E.\n"
        "Bút toán TK 3351 có gắn nhân viên và hợp đồng, ngày hạch toán trong tháng 10/2026:\n"
        "- NV-A: HD-01 Thưởng thực hiện hợp đồng Có 3.000.000; HD-01 Thưởng năng suất tháng Có 2.000.000; "
        "HD-02 Thưởng năng suất quý Có 1.500.000; HD-02 Thưởng năng suất tháng Nợ 500.000 (điều chỉnh giảm)\n"
        "- NV-B: HD-03 Thưởng năng suất tháng Có 1.000.000\n"
        "- NV-C: HD-04 Thưởng thực hiện hợp đồng Có 4.000.000\n"
        "- NV-D: HD-05 Thưởng năng suất quý Có 2.500.000\n"
        "- NV-E: HD-06 Thưởng thực hiện hợp đồng Có 700.000\n"
        "- NV-A ngày 05/11/2026: HD-01 Thưởng năng suất tháng Có 800.000\n"
        "- Phiếu chi ngày 20/10/2026 trả thưởng NV-A: Nợ 3351 5.000.000 (không được tính)")

KT = "KT-1 có quyền \"Xem báo cáo thưởng theo nhân viên\" phạm vi Công ty, thuộc TPE"

LOC_T10 = "Chọn Từ ngày 01/10/2026, Đến ngày 31/10/2026, bấm Lọc"
LOC_T10_11 = "Chọn Từ ngày 01/10/2026, Đến ngày 30/11/2026, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo thưởng theo nhân viên: cho biết trong một khoảng ngày, mỗi nhân viên kinh doanh được ghi "
     "nhận bao nhiêu Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý, gom theo "
     "phòng ban.\n"
     "Người dùng làm được: lọc theo công ty, phòng ban, bộ phận, nhân viên, khoảng ngày; bấm tên nhân "
     "viên để xem chi tiết theo từng hợp đồng; bấm tên phòng để mở báo cáo chi phí bán hàng của phòng; "
     "In, Xuất excel. Màn chỉ xem, không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Số liệu lấy từ bút toán tài khoản 3351 (chi phí phải trả ngắn hạn) có gắn nhân viên và gắn hợp "
     "đồng, theo 3 vụ việc: Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý.\n"
     "- Mỗi cột = phát sinh Có trừ phát sinh Nợ của vụ việc đó.\n"
     "- Nhân viên hiện dưới phòng ban HIỆN TẠI trong hồ sơ; phòng ban phải đang hoạt động.\n"
     "- Chỉ hiện nhân viên có ít nhất 1 trong 3 cột khác 0; chỉ hiện phòng có ít nhất 1 nhân viên như vậy.\n"
     "- STT phòng 1, 2, ...; STT nhân viên 1.1, 1.2, ..."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bút toán của phiếu chi, ủy nhiệm chi, kết chuyển chi phí phải trả (là bút toán trả / kết chuyển "
     "thưởng, không phải ghi nhận thưởng).\n"
     "- Bút toán không gắn nhân viên hoặc không gắn hợp đồng.\n"
     "- Các vụ việc khác trên 3351 (thưởng thêm, tiền vận chuyển...): màn này không có cột cho chúng.\n"
     "- Nhân viên có cả 3 cột bằng 0 (ví dụ Có và Nợ bù trừ hết).\n"
     "- Nhân viên thuộc phòng đã ngừng hoạt động hoặc không có phòng (theo code hiện tại bị mất cả ở bảng "
     "lẫn dòng Tổng cộng)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày, Đến ngày là bắt buộc. Lọc theo NGÀY HẠCH TOÁN của chứng từ gốc của bút toán, tính trọn "
     "ngày (từ 00:00 Từ ngày đến 23:59 Đến ngày). Cửa sổ chi tiết dùng cùng khoảng ngày đang chọn trên "
     "màn."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Công ty (quyền tổng công ty), Phòng ban, Bộ phận, Nhân viên, Từ ngày, Đến ngày; nút Lọc, "
     "làm mới, In, Xuất excel.\n"
     "Bảng: STT, Nhân viên, Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý, "
     "Tổng cộng. Dòng Tổng cộng nằm ngay dưới tiêu đề. Dòng phòng ban (chữ đậm, \"mã - tên\") > dòng nhân "
     "viên (\"mã - họ tên\").\n"
     "Cửa sổ Chi tiết: STT, Hợp đồng, Khách hàng, 3 cột thưởng, Tổng cộng; dòng Tổng cộng ở trên cùng."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột của nhân viên = tổng mọi hợp đồng của nhân viên trong kỳ (Có trừ Nợ).\n"
     "- Tổng cộng của nhân viên = 3 cột cộng lại.\n"
     "- Dòng phòng ban = cộng các nhân viên hiện dưới phòng.\n"
     "- Dòng Tổng cộng trên cùng = cộng mọi nhân viên của MỌI trang.\n"
     "Với dữ liệu mẫu, KT-1 lọc 01/10 - 31/10/2026 (nếu quyền đúng): NV-A 3.000.000 | 1.500.000 | "
     "1.500.000 | 6.000.000; NV-B 0 | 1.000.000 | 0 | 1.000.000; PKD1 3.000.000 | 2.500.000 | 1.500.000 | "
     "7.000.000; PKD2 4.000.000 | 0 | 0 | 4.000.000."),

    ("7. Phân quyền cấp",
     "- Quyền \"Xem báo cáo thưởng theo nhân viên\" có 4 phạm vi: Tổng công ty, Công ty, Phòng ban, Bộ "
     "phận; phạm vi quyết định ô lọc hiện ra.\n"
     "- Không có quyền vẫn mở được màn, chỉ thấy thưởng của chính mình.\n"
     "- Theo code hiện tại phần lấy số liệu kiểm 4 tên quyền cũ không còn tồn tại, nên MỌI người (kể cả "
     "phạm vi Tổng công ty) chỉ thấy dòng của chính mình - xem nhóm phân quyền.\n"
     "- Cửa sổ chi tiết không kiểm tra quyền.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang theo PHÒNG BAN, 10 phòng mỗi trang; STT phòng nối tiếp qua các trang.\n"
     "- Số bằng 0 hiện \"-\" (riêng cột Tổng cộng trong bản in hiện 0).\n"
     "- In, Xuất excel: theo code hiện tại chỉ lấy các phòng của TRANG đang xem, còn dòng Tổng cộng là "
     "tổng mọi trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Người có quyền vẫn chỉ thấy mình.\n"
     "- In / Excel chỉ ra trang đang xem nhưng dòng Tổng cộng là của mọi trang.\n"
     "- Nhân viên ở phòng ngừng hoạt động bị mất khỏi báo cáo và khỏi Tổng cộng.\n"
     "- Lọc Bộ phận vẫn ra mọi nhân viên của phòng.\n"
     "- Cửa sổ chi tiết: ô Tổng cộng của cột Thưởng năng suất quý hiện \"-\" khi Thưởng năng suất tháng "
     "bằng 0.\n"
     "- Khác Bảng tổng hợp thu nhập từ bán hàng: màn này không có cột thưởng thêm và tiền vận chuyển."),
]


ROLE_TCS = [
    ("00", "Không có quyền vẫn mở được màn, chỉ thấy thưởng của mình", "P0",
     "NV-A không có quyền \"Xem báo cáo thưởng theo nhân viên\"\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. " + LOC_T10,
     "Tài khoản: NV-A",
     "- Mở được màn, không có ô Công ty, Phòng ban, Bộ phận, Nhân viên\n"
     "- Chỉ có PKD1 > NV-A: 3.000.000 | 1.500.000 | 1.500.000 | 6.000.000\n"
     "- Không có NV-B, NV-C"),

    ("01", "Quyền phạm vi Công ty thấy mọi phòng của công ty", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Phòng ban, Bộ phận, Nhân viên; không có ô Công ty\n"
     "- Mong đợi: PKD1 (NV-A, NV-B) và PKD2 (NV-C); Tổng cộng 11.000.000; không có NV-D của TPC\n"
     "- Lưu ý: theo code hiện tại chỉ hiện dòng của chính KT-1 (hoặc \"Chưa có dữ liệu\" nếu KT-1 không "
     "có thưởng), vì phần lấy số liệu kiểm tên quyền cũ không còn - ghi Failed"),

    ("02", "Quyền phạm vi Tổng công ty thấy mọi công ty", "P0",
     "TGĐ có quyền phạm vi Tổng công ty\n" + DATA,
     "1. Đăng nhập TGĐ, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Công ty\n"
     "- Mong đợi: có PKD1, PKD2 (TPE) và PKD5 - NV-D 2.500.000 (TPC)\n"
     "- Lưu ý: theo code hiện tại chỉ thấy dòng của chính TGĐ - ghi Failed"),

    ("03", "Quyền phạm vi Phòng ban chỉ thấy phòng mình phụ trách", "P0",
     "TP-1 trưởng PKD1, quyền phạm vi Phòng ban\n" + DATA,
     "1. Đăng nhập TP-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có ô Bộ phận, Nhân viên; không có ô Công ty; ô Phòng ban chỉ hiện khi phụ trách từ 2 phòng\n"
     "- Mong đợi: chỉ PKD1 với NV-A, NV-B; không có PKD2\n"
     "- Lưu ý: theo code hiện tại chỉ thấy dòng của chính TP-1 - ghi Failed"),

    ("04", "Quyền phạm vi Bộ phận chỉ thấy bộ phận mình", "P1",
     "TBP-1 thuộc BP1 của PKD1, quyền phạm vi Bộ phận\n" + DATA,
     "1. Đăng nhập TBP-1, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có ô Nhân viên\n"
     "- Mong đợi: chỉ NV-A (BP1), không có NV-B (BP2)\n"
     "- Lưu ý: theo code hiện tại chỉ thấy dòng của chính TBP-1; nếu sửa phần quyền thì phạm vi Bộ phận "
     "lại ra cả phòng PKD1 (đoạn lọc theo bộ phận đang bị tắt) - ghi Failed"),

    ("05", "Người không có quyền chọn nhân viên khác qua đường dẫn", "P0",
     "NV-A không có quyền; NV-C có thưởng\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu báo cáo với nhân viên NV-C, 01/10 - "
     "31/10/2026",
     "—",
     "- Không có dữ liệu của NV-C (\"Chưa có dữ liệu\")"),

    ("06", "Cửa sổ chi tiết gọi thẳng với nhân viên khác", "P0",
     "NV-A không có quyền; NV-C có thưởng HD-04\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi chức năng lấy chi tiết theo nhân viên với nhân viên NV-C, "
     "01/10 - 31/10/2026",
     "—",
     "- Mong đợi: bị chặn, không trả số liệu của NV-C\n"
     "- Lưu ý: theo code hiện tại trả đủ HD-04, khách hàng, Thưởng thực hiện hợp đồng 4.000.000 - ghi "
     "Failed (lộ thu nhập của người khác)"),

    ("07", "Cửa sổ chi tiết gọi thẳng với nhân viên công ty khác", "P1",
     "KT-1 phạm vi Công ty TPE; NV-D thuộc TPC\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. Dùng công cụ kiểm thử API gọi chức năng lấy chi tiết với nhân viên NV-D",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả HD-05, Thưởng năng suất quý 2.500.000 - ghi Failed"),

    ("08", "In / Xuất excel qua đường dẫn khi không có quyền", "P1",
     "NV-A không có quyền\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dán đường dẫn In của báo cáo kèm nhân viên NV-C, 01/10 - 31/10/2026",
     "—",
     "- Bản in không có NV-C; chỉ có dòng của NV-A (nếu khớp lọc)"),
]
