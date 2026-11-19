# -*- coding: utf-8 -*-
"""Section I - X cho man Bao cao thuong theo nhan vien."""
from tc_data_role import MENU, DATA, KT, LOC_T10, LOC_T10_11

NVA = "Đăng nhập NV-A (không có quyền, chỉ thấy mình)"
PHU_THUOC = "- Lưu ý: TC này cần lỗi phân quyền (Phân quyền 01) đã được sửa; nếu chưa sửa thì ghi Blocked"

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     KT,
     "1. Đăng nhập KT-1\n"
     "2. " + MENU + "\n"
     "3. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề trang \"Báo cáo thưởng theo nhân viên\"\n"
     "- Bộ lọc: Phòng ban, Bộ phận, Nhân viên, Từ ngày (bắt buộc), Đến ngày (bắt buộc)\n"
     "- Nút Lọc, làm mới, In, Xuất excel\n"
     "- Bảng ghi \"Chưa có dữ liệu\", chưa tự lọc khi mở màn"),

    ("002", "Cột của bảng", "P0",
     DATA,
     "1. " + NVA + ", mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Cột: STT, Nhân viên, Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý, "
     "Tổng cộng\n"
     "- Dòng Tổng cộng nằm ngay dưới dòng tiêu đề"),

    ("003", "Biểu tượng đang tải", "P2",
     DATA,
     "1. " + NVA + ", mở màn\n"
     "2. " + LOC_T10 + ", quan sát ngay",
     "—",
     "- Bảng hiện \"Đang tải dữ liệu\"; nút Lọc mờ và quay đến khi xong"),

    ("004", "Khoảng ngày không có thưởng", "P1",
     DATA,
     "1. " + NVA + ", mở màn\n"
     "2. Chọn Từ ngày 01/01/2024, Đến ngày 31/01/2024, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\"; dòng Tổng cộng trống hoặc 0"),

    ("005", "Số bằng 0 hiện dấu gạch", "P1",
     DATA,
     "1. " + NVA + ", mở màn\n"
     "2. Chọn Từ ngày 05/11/2026, Đến ngày 05/11/2026, bấm Lọc",
     "—",
     "- NV-A: Thưởng thực hiện hợp đồng \"-\", Thưởng năng suất tháng 800.000, Thưởng năng suất quý "
     "\"-\", Tổng cộng 800.000"),
]


SEC_II = [
    ("001", "Thiếu Từ ngày / Đến ngày", "P0",
     KT,
     "1. Mở màn, để trống Từ ngày, Đến ngày, bấm Lọc",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\"\n"
     "- Dưới 2 ô ghi \"Bắt buộc chọn\"; bảng không đổi"),

    ("002", "Chỉ thiếu Đến ngày", "P1",
     KT,
     "1. Chọn Từ ngày 01/10/2026, để trống Đến ngày, bấm Lọc",
     "—",
     "- Báo \"Bắt buộc chọn\" dưới Đến ngày, không lọc"),

    ("003", "Từ ngày sau Đến ngày", "P2",
     DATA,
     "1. " + NVA + "\n"
     "2. Chọn Từ ngày 31/10/2026, Đến ngày 01/10/2026, bấm Lọc",
     "—",
     "- Mong đợi: báo Từ ngày không được sau Đến ngày\n"
     "- Lưu ý: theo code hiện tại không chặn, bảng ra \"Chưa có dữ liệu\" - ghi Failed"),

    ("004", "Lọc trọn ngày Đến ngày", "P0",
     DATA,
     "1. " + NVA + "\n"
     "2. Chọn Từ ngày 01/11/2026, Đến ngày 05/11/2026, bấm Lọc",
     "—",
     "- NV-A có Thưởng năng suất tháng 800.000 (bút toán ngày 05/11/2026 được tính)"),

    ("005", "Khoảng ngày gồm 2 tháng", "P0",
     DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10_11,
     "—",
     "- NV-A: 3.000.000 | 2.300.000 | 1.500.000 | 6.800.000"),

    ("006", "Lọc Nhân viên", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, chọn Nhân viên NV-B\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có PKD1 > NV-B: \"-\" | 1.000.000 | \"-\" | 1.000.000; Tổng cộng 1.000.000\n" + PHU_THUOC),

    ("007", "Lọc Phòng ban", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, chọn Phòng ban PKD2\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có PKD2 > NV-C 4.000.000; Tổng cộng 4.000.000\n" + PHU_THUOC),

    ("008", "Lọc Bộ phận", "P1",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, chọn Phòng ban PKD1, Bộ phận BP1\n"
     "2. " + LOC_T10,
     "—",
     "- Mong đợi: chỉ NV-A (BP1); Tổng cộng 6.000.000\n"
     "- Lưu ý: theo code hiện tại vẫn ra cả NV-B (BP2), vì Bộ phận chỉ dùng để chọn phòng có bộ phận đó - "
     "ghi Failed\n" + PHU_THUOC),

    ("009", "Lọc Công ty (quyền Tổng công ty)", "P1",
     "TGĐ quyền Tổng công ty\n" + DATA,
     "1. Đăng nhập TGĐ, chọn Công ty TPC\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có PKD5 > NV-D 2.500.000\n" + PHU_THUOC),

    ("010", "Đổi Công ty thì danh sách Phòng ban đổi theo", "P2",
     "TGĐ quyền Tổng công ty",
     "1. Chọn Công ty TPE, mở ô Phòng ban\n"
     "2. Đổi Công ty sang TPC, mở lại ô Phòng ban",
     "—",
     "- Lần 1 chỉ phòng của TPE, lần 2 chỉ phòng của TPC; Phòng ban đã chọn trước bị xóa"),

    ("011", "Nút làm mới xóa bộ lọc", "P1",
     KT,
     "1. Chọn Phòng ban PKD1, Nhân viên NV-A, Từ ngày, Đến ngày\n"
     "2. Bấm nút làm mới",
     "—",
     "- Mọi ô lọc về trống; bảng giữ kết quả cũ cho đến khi bấm Lọc lại"),

    ("012", "Lọc lại sau khi đổi ngày", "P1",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Đổi Đến ngày sang 30/11/2026, bấm Lọc",
     "—",
     "- Lần 1 Tổng cộng 6.000.000; lần 2 Tổng cộng 6.800.000"),
]


SEC_III = [
    ("001", "Ba cột lấy theo ba vụ việc trên TK 3351", "P0",
     DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng thực hiện hợp đồng 3.000.000\n"
     "- Thưởng năng suất tháng 1.500.000 (Có 2.000.000 trừ Nợ 500.000)\n"
     "- Thưởng năng suất quý 1.500.000\n"
     "- Tổng cộng 6.000.000"),

    ("002", "Phiếu chi trả thưởng không bị trừ", "P0",
     DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Phiếu chi Nợ 3351 5.000.000 ngày 20/10/2026 không làm giảm số; Tổng cộng vẫn 6.000.000"),

    ("003", "Ủy nhiệm chi trả thưởng không bị trừ", "P0",
     "Thêm: ủy nhiệm chi ngày 25/10/2026 Nợ 3351 Thưởng năng suất quý 1.500.000 cho NV-A, HD-02\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng năng suất quý vẫn 1.500.000"),

    ("004", "Kết chuyển chi phí phải trả không bị trừ", "P0",
     "Thêm: phiếu Kết chuyển chi phí phải trả đến 31/10/2026 đã ghi Nợ 3351 Thưởng thực hiện hợp đồng "
     "3.000.000 cho NV-A, HD-01\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng thực hiện hợp đồng vẫn 3.000.000"),

    ("005", "Bút toán Nợ điều chỉnh từ chứng từ khác được trừ", "P0",
     "Thêm: phiếu kế toán ngày 28/10/2026 Nợ 3351 Thưởng thực hiện hợp đồng 1.000.000 cho NV-A, HD-01\n"
     + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng thực hiện hợp đồng 2.000.000 (3.000.000 trừ 1.000.000); Tổng cộng 5.000.000"),

    ("006", "Bút toán không gắn hợp đồng không được tính", "P0",
     "Thêm: phiếu kế toán ngày 15/10/2026 Có 3351 Thưởng năng suất quý 900.000 cho NV-A, không chọn hợp "
     "đồng\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng năng suất quý vẫn 1.500.000\n"
     "- Lưu ý: nếu nghiệp vụ cần tính cả thưởng không gắn hợp đồng (ví dụ thưởng quý ghi theo nhân viên) "
     "thì ghi Failed"),

    ("007", "Bút toán không gắn nhân viên không được tính", "P1",
     "Thêm: phiếu kế toán ngày 15/10/2026 Có 3351 Thưởng thực hiện hợp đồng 600.000, HD-01, không chọn "
     "nhân viên\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Không có dòng mới; Tổng cộng không đổi\n" + PHU_THUOC),

    ("008", "Vụ việc khác trên 3351 không được tính", "P0",
     "Thêm: bút toán ngày 15/10/2026 Có 3351 vụ việc Tiền vận chuyển 300.000 cho NV-A, HD-01\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Không có cột Tiền vận chuyển; Tổng cộng NV-A vẫn 6.000.000"),

    ("009", "Thưởng ghi trên tài khoản khác 3351 không được tính", "P1",
     "Thêm: bút toán ngày 15/10/2026 Có 3348 vụ việc Thưởng năng suất tháng 450.000 cho NV-A, HD-01\n"
     + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng năng suất tháng vẫn 1.500.000"),

    ("010", "Lọc theo ngày hạch toán của chứng từ", "P0",
     "Thêm: phiếu kế toán lập ngày 01/11/2026, ngày hạch toán 31/10/2026, Có 3351 Thưởng năng suất tháng "
     "200.000 cho NV-A, HD-01\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng năng suất tháng 1.700.000 (tính theo ngày hạch toán 31/10)"),

    ("011", "Có và Nợ bù trừ hết thì nhân viên không hiện", "P1",
     "Thêm NV-F (PKD2): ngày 10/10/2026 Có 3351 Thưởng năng suất tháng 500.000, ngày 20/10/2026 phiếu kế "
     "toán Nợ 500.000, cùng HD-07\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Không có dòng NV-F\n" + PHU_THUOC),

    ("012", "Số âm hiện dấu trừ", "P1",
     "Thêm: phiếu kế toán ngày 28/10/2026 Nợ 3351 Thưởng năng suất quý 2.000.000 cho NV-A, HD-02\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Thưởng năng suất quý -500.000; Tổng cộng 4.000.000"),

    ("013", "Bút toán của phiếu đã hủy / đã xóa không còn tính", "P0",
     "Thêm: phiếu năng suất tháng ghi Có 3351 Thưởng năng suất tháng 700.000 cho NV-A ngày 15/10/2026, "
     "sau đó phiếu bị hủy duyệt và bút toán bị xóa\n" + DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10 + " trước và sau khi hủy",
     "—",
     "- Trước khi hủy: Thưởng năng suất tháng 2.200.000\n"
     "- Sau khi hủy: 1.500.000"),
]


SEC_IV = [
    ("001", "Gom nhân viên theo phòng ban", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Dòng 1 \"PKD1 - tên phòng\" chữ đậm: 3.000.000 | 2.500.000 | 1.500.000 | 7.000.000\n"
     "- Dòng 1.1 NV-A 6.000.000; dòng 1.2 NV-B 1.000.000\n"
     "- Dòng 2 PKD2 4.000.000; dòng 2.1 NV-C\n" + PHU_THUOC),

    ("002", "Nhân viên hiện \"mã - họ tên\"", "P2",
     DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Dòng nhân viên dạng mã NV-A, gạch nối, họ tên NV-A\n"
     "- Tên là liên kết màu xanh"),

    ("003", "Phòng không có nhân viên nào có thưởng thì không hiện", "P1",
     KT + "; phòng PKD3 của TPE không ai có thưởng tháng 10\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Không có dòng PKD3\n" + PHU_THUOC),

    ("004", "Nhân viên thuộc phòng đã ngừng hoạt động", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Mong đợi: thưởng 700.000 của NV-E vẫn được thể hiện (dưới phòng PKD9 hoặc một dòng riêng) và tính "
     "vào Tổng cộng\n"
     "- Lưu ý: theo code hiện tại NV-E mất hẳn, Tổng cộng 11.000.000 thiếu 700.000 - ghi Failed\n"
     + PHU_THUOC),

    ("005", "Nhân viên chuyển phòng trong kỳ", "P1",
     "NV-B chuyển từ PKD1 sang PKD2 ngày 01/11/2026; thưởng tháng 10 ghi khi còn ở PKD1\n" + DATA,
     "1. Đăng nhập KT-1 ngày 17/11/2026\n"
     "2. " + LOC_T10,
     "—",
     "- NV-B hiện dưới PKD2 (phòng hiện tại), thưởng tháng 10 cộng vào PKD2\n"
     "- Lưu ý: nếu nghiệp vụ muốn thưởng theo phòng tại thời điểm ghi nhận thì ghi Failed\n" + PHU_THUOC),

    ("006", "Nhân viên chuyển công ty", "P1",
     "NV-C chuyển từ TPE sang TPC (phòng PKD5) ngày 01/11/2026\n" + DATA,
     "1. Đăng nhập KT-1 (phạm vi Công ty TPE)\n"
     "2. " + LOC_T10,
     "—",
     "- Mong đợi theo nghiệp vụ: thưởng tháng 10 của NV-C vẫn thuộc báo cáo TPE\n"
     "- Lưu ý: theo code hiện tại NV-C chuyển hẳn sang PKD5 của TPC, KT-1 không còn thấy - ghi để nghiệp "
     "vụ quyết\n" + PHU_THUOC),

    ("007", "Thứ tự STT phòng và nhân viên", "P2",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- STT phòng 1, 2; STT nhân viên 1.1, 1.2, 2.1\n" + PHU_THUOC),
]


SEC_V = [
    ("001", "Dòng Tổng cộng trên cùng", "P0",
     DATA,
     "1. " + NVA + "\n"
     "2. " + LOC_T10,
     "—",
     "- Dòng Tổng cộng: 3.000.000 | 1.500.000 | 1.500.000 | 6.000.000 (bằng dòng NV-A)"),

    ("002", "Tổng cộng bằng cộng các phòng", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10,
     "—",
     "- Tổng cộng 7.000.000 | 2.500.000 | 1.500.000 | 11.000.000 (PKD1 + PKD2)\n" + PHU_THUOC),

    ("003", "Phân trang 10 phòng mỗi trang", "P1",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1\n"
     "2. " + LOC_T10 + "\n"
     "3. Bấm sang trang 2",
     "—",
     "- Trang 1 có 10 phòng (STT 1 - 10), trang 2 có 2 phòng (STT 11, 12)\n"
     "- Nhân viên trang 2 đánh số 11.1, 12.1\n" + PHU_THUOC),

    ("004", "Dòng Tổng cộng không đổi khi sang trang", "P0",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1, " + LOC_T10 + "\n"
     "2. Ghi lại dòng Tổng cộng, bấm sang trang 2",
     "—",
     "- Dòng Tổng cộng giữ nguyên, là tổng của cả 12 phòng\n" + PHU_THUOC),

    ("005", "Cộng các phòng của mọi trang khớp Tổng cộng", "P0",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1, " + LOC_T10 + "\n"
     "2. Cộng cột Tổng cộng của các dòng phòng trên trang 1 và trang 2",
     "—",
     "- Kết quả bằng dòng Tổng cộng trên cùng\n" + PHU_THUOC),

    ("006", "Lọc lại thì quay về trang 1", "P2",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1, lọc, sang trang 2\n"
     "2. Bấm Lọc lại",
     "—",
     "- Bảng quay về trang 1\n" + PHU_THUOC),
]


SEC_VI = [
    ("001", "Mở cửa sổ chi tiết theo hợp đồng", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm tên NV-A",
     "—",
     "- Mở cửa sổ \"Chi tiết\": cột STT, Hợp đồng, Khách hàng, Thưởng thực hiện hợp đồng, Thưởng năng suất "
     "tháng, Thưởng năng suất quý, Tổng cộng\n"
     "- Dòng HD-01: 3.000.000 | 2.000.000 | \"-\" | 5.000.000\n"
     "- Dòng HD-02: \"-\" | -500.000 | 1.500.000 | 1.000.000"),

    ("002", "Dòng Tổng cộng của cửa sổ khớp dòng nhân viên", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm tên NV-A",
     "—",
     "- Dòng Tổng cộng trên cùng: 3.000.000 | 1.500.000 | 1.500.000 | 6.000.000, bằng dòng NV-A ở bảng "
     "chính"),

    ("003", "Cửa sổ chi tiết dùng khoảng ngày đang chọn", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10_11 + "\n"
     "2. Bấm tên NV-A",
     "—",
     "- HD-01 Thưởng năng suất tháng 2.800.000 (gồm 800.000 ngày 05/11)"),

    ("004", "Khách hàng hiện \"mã - tên\" theo hợp đồng", "P2",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + ", bấm tên NV-A",
     "—",
     "- Cột Khách hàng của HD-01 hiện mã khách hàng, gạch nối, tên khách hàng của HD-01"),

    ("005", "Ô Tổng cộng cột quý khi thưởng tháng bằng 0", "P1",
     "NV-G (PKD2) chỉ có Thưởng năng suất quý 1.200.000 trên HD-08 trong tháng 10/2026",
     "1. Đăng nhập NV-G, mở màn, " + LOC_T10 + "\n"
     "2. Bấm tên NV-G",
     "—",
     "- Mong đợi: dòng Tổng cộng cột Thưởng năng suất quý 1.200.000\n"
     "- Lưu ý: theo code hiện tại ô này hiện \"-\" vì đang xét theo cột Thưởng năng suất tháng - ghi Failed"),

    ("006", "Đóng cửa sổ chi tiết", "P2",
     DATA,
     "1. " + NVA + ", mở cửa sổ chi tiết NV-A\n"
     "2. Bấm Đóng",
     "—",
     "- Cửa sổ đóng, bảng chính giữ nguyên"),

    ("007", "Cửa sổ chi tiết không bỏ các hợp đồng bù trừ về 0", "P2",
     "Thêm: NV-A HD-09 Có 300.000 và Nợ 300.000 Thưởng năng suất tháng trong tháng 10/2026\n" + DATA,
     "1. " + NVA + ", " + LOC_T10 + ", bấm tên NV-A",
     "—",
     "- Có dòng HD-09 với các cột \"-\", Tổng cộng 0 (cửa sổ liệt kê mọi hợp đồng có bút toán)"),

    ("008", "Đổi khoảng ngày rồi mở lại cửa sổ", "P1",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + ", mở chi tiết NV-A, đóng\n"
     "2. Đổi Đến ngày 30/11/2026 nhưng CHƯA bấm Lọc, bấm lại tên NV-A",
     "—",
     "- Mong đợi: cửa sổ khớp bảng đang hiện (01/10 - 31/10)\n"
     "- Lưu ý: theo code hiện tại cửa sổ lấy ngày đang gõ trên ô lọc (đến 30/11), HD-01 tháng 2.800.000 "
     "lệch bảng 6.000.000 - ghi Failed"),
]


SEC_VII = [
    ("001", "Bấm tên phòng mở báo cáo chi phí bán hàng của phòng", "P1",
     KT + "; KT-1 có quyền xem báo cáo chi phí bán hàng theo hợp đồng\n" + DATA,
     "1. Đăng nhập KT-1, " + LOC_T10 + "\n"
     "2. Bấm tên phòng PKD1",
     "—",
     "- Mở tab mới báo cáo chi phí bán hàng theo hợp đồng, đã điền Công ty TPE, Phòng ban PKD1, 01/10 - "
     "31/10/2026\n" + PHU_THUOC),

    ("002", "Bấm tên phòng khi không có quyền báo cáo chi phí bán hàng", "P2",
     "NV-A không có quyền báo cáo chi phí bán hàng\n" + DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm tên phòng PKD1",
     "—",
     "- Mở tab mới, chỉ thấy số liệu của chính NV-A theo phạm vi quyền của báo cáo đó"),
]


SEC_VIII = [
    ("001", "In báo cáo", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm In",
     "—",
     "- Mở tab bản in khổ ngang, tiêu đề báo cáo thưởng theo nhân viên, kỳ 01/10/2026 - 31/10/2026\n"
     "- Bảng: dòng Tổng cộng 6.000.000; PKD1; 1.1 NV-A 3.000.000 | 1.500.000 | 1.500.000 | 6.000.000"),

    ("002", "Xuất excel", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file \"bao_cao_thuong_theo_nhan_vien.xlsx\"\n"
     "- Số liệu giống bảng trên màn"),

    ("003", "In khi có nhiều trang", "P0",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1, " + LOC_T10 + "\n"
     "2. Đang ở trang 1, bấm In",
     "—",
     "- Mong đợi: bản in đủ 12 phòng, cộng các phòng bằng dòng Tổng cộng\n"
     "- Lưu ý: theo code hiện tại bản in chỉ có 10 phòng của trang 1 nhưng dòng Tổng cộng là của cả 12 "
     "phòng - ghi Failed\n" + PHU_THUOC),

    ("004", "Xuất excel khi đang ở trang 2", "P0",
     KT + "; TPE có 12 phòng có thưởng tháng 10",
     "1. Đăng nhập KT-1, " + LOC_T10 + ", sang trang 2\n"
     "2. Bấm Xuất excel",
     "—",
     "- Mong đợi: file đủ 12 phòng\n"
     "- Lưu ý: theo code hiện tại file chỉ có 2 phòng của trang 2, đánh STT lại từ 1 - ghi Failed\n"
     + PHU_THUOC),

    ("005", "In theo bộ lọc đang chọn", "P1",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, chọn Phòng ban PKD2, " + LOC_T10 + "\n"
     "2. Bấm In",
     "—",
     "- Bản in chỉ có PKD2 > NV-C 4.000.000\n" + PHU_THUOC),

    ("006", "In khi chưa chọn ngày", "P1",
     KT,
     "1. Mở màn, không chọn ngày, bấm In",
     "—",
     "- Mong đợi: báo phải chọn Từ ngày, Đến ngày\n"
     "- Lưu ý: theo code hiện tại bản in mở được, lấy toàn bộ thời gian, kỳ để trống - ghi Failed"),

    ("007", "Số bằng 0 trong bản in", "P2",
     DATA,
     "1. " + NVA + ", chọn 05/11/2026 - 05/11/2026, bấm Lọc\n"
     "2. Bấm In",
     "—",
     "- Thưởng thực hiện hợp đồng và Thưởng năng suất quý hiện \"-\"; Tổng cộng 800.000"),

    ("008", "Tên phòng có ký tự &", "P2",
     "Phòng \"KD Ô tô & Xe máy\" có nhân viên có thưởng tháng 10",
     "1. Đăng nhập người thuộc phòng đó, " + LOC_T10 + "\n"
     "2. Bấm In, bấm Xuất excel",
     "—",
     "- Tên phòng hiện đúng \"KD Ô tô & Xe máy\"; file Excel mở được, không báo lỗi"),
]


SEC_IX = [
    ("001", "Đối chiếu với sổ chi tiết TK 3351", "P0",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Mở sổ chi tiết tài khoản 3351, lọc nhân viên NV-A, 01/10 - 31/10/2026, cộng Có trừ Nợ theo 3 vụ "
     "việc, bỏ phiếu chi / ủy nhiệm chi / kết chuyển",
     "—",
     "- Ba số khớp 3.000.000 | 1.500.000 | 1.500.000"),

    ("002", "Đối chiếu với Bảng tổng hợp thu nhập từ bán hàng", "P1",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Mở Bảng tổng hợp thu nhập từ bán hàng, cùng khoảng ngày",
     "—",
     "- Cột Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, Thưởng năng suất quý của NV-A khớp hai màn"),

    ("003", "Màn chỉ xem, không sửa dữ liệu", "P0",
     DATA,
     "1. " + NVA + ", lọc, mở chi tiết, In, Xuất excel\n"
     "2. Mở lại sổ chi tiết 3351",
     "—",
     "- Không có bút toán nào thay đổi"),

    ("004", "Dữ liệu mới ghi nhận hiện ngay khi lọc lại", "P1",
     DATA,
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Kế toán duyệt thêm phiếu ghi Có 3351 Thưởng năng suất tháng 300.000 cho NV-A ngày 30/10/2026\n"
     "3. Bấm Lọc lại",
     "—",
     "- Thưởng năng suất tháng 1.800.000; Tổng cộng 6.300.000"),

    ("005", "Gọi chức năng lấy dữ liệu với ngày sai định dạng", "P2",
     "—",
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu với Từ ngày \"2026-10-01\"",
     "—",
     "- Mong đợi: báo ngày không hợp lệ\n"
     "- Lưu ý: nếu ra trang lỗi hệ thống thì ghi Failed"),

    ("006", "Thu nhập của người khác không lộ qua cửa sổ chi tiết", "P0",
     "NV-A không có quyền; biết mã nhân viên của NV-C",
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi chức năng chi tiết theo nhân viên với NV-C",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại trả đủ thưởng từng hợp đồng của NV-C - ghi Failed (trùng Phân quyền 06)"),
]


SEC_X = [
    ("001", "Phiếu năng suất tháng được duyệt hiện lên báo cáo", "P0",
     "NV-A có hợp đồng HD-10 đủ điều kiện tính thưởng tháng 10/2026",
     "1. Kế toán lập và duyệt phiếu năng suất tháng 10/2026 có NV-A, HD-10 Thưởng năng suất tháng "
     "1.000.000, ngày hạch toán 31/10/2026\n"
     "2. " + NVA + ", " + LOC_T10 + "\n"
     "3. Bấm tên NV-A",
     "—",
     "- Thưởng năng suất tháng của NV-A tăng 1.000.000\n"
     "- Cửa sổ chi tiết có dòng HD-10 1.000.000"),

    ("002", "Trả thưởng bằng phiếu chi không làm giảm báo cáo", "P0",
     "Tiếp TC 001",
     "1. Kế toán lập phiếu chi trả 1.000.000 thưởng tháng cho NV-A ngày 05/11/2026\n"
     "2. " + NVA + ", chọn 01/10 - 30/11/2026, bấm Lọc",
     "—",
     "- Thưởng năng suất tháng vẫn gồm 1.000.000 của HD-10 (phiếu chi không trừ)"),

    ("003", "Quyết toán hợp đồng ghi thưởng thực hiện hợp đồng", "P0",
     "HD-11 của NV-A quyết toán ngày 20/10/2026, sinh Có 3351 Thưởng thực hiện hợp đồng 2.000.000",
     "1. " + NVA + ", " + LOC_T10 + "\n"
     "2. Bấm tên NV-A",
     "—",
     "- Thưởng thực hiện hợp đồng tăng 2.000.000; chi tiết có dòng HD-11"),

    ("004", "Điều chỉnh giảm thưởng sau khi đã ghi nhận", "P1",
     "Tiếp TC 003",
     "1. Kế toán lập phiếu kế toán ngày 25/10/2026 Nợ 3351 Thưởng thực hiện hợp đồng 500.000 cho NV-A, "
     "HD-11\n"
     "2. " + NVA + ", " + LOC_T10,
     "—",
     "- Thưởng thực hiện hợp đồng HD-11 còn 1.500.000"),

    ("005", "Quản lý xem toàn công ty sau khi ghi nhận thưởng", "P0",
     KT + "\n" + DATA,
     "1. Đăng nhập KT-1, " + LOC_T10 + "\n"
     "2. Bấm tên NV-C, rồi In, rồi Xuất excel",
     "—",
     "- Bảng có PKD1 (7.000.000) và PKD2 (4.000.000), Tổng cộng 11.000.000\n"
     "- Chi tiết NV-C: HD-04 4.000.000\n"
     "- Bản in và file Excel cùng số liệu\n" + PHU_THUOC),
]
