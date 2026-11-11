# -*- coding: utf-8 -*-
"""Section I - VIII cho man Bang tong hop thu nhap tu ban hang."""
from tc_data_role import MENU, DATA, KY

KT1 = "KT-1 (TPE, quyền xem phạm vi Công ty)\n" + DATA

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     "KT-1 thuộc TPE có quyền xem phạm vi Công ty",
     "1. Đăng nhập KT-1\n"
     "2. " + MENU,
     "—",
     "- Tiêu đề trang \"Bảng tổng hợp thu nhập từ bán hàng\"\n"
     "- Bộ lọc: Phòng ban, Bộ phận, Nhân viên, Năm (mặc định năm hiện tại), Kì quyết toán (trống), Từ "
     "ngày, Đến ngày (bị khóa), Xuất hóa đơn = Tất cả\n"
     "- Nút Lọc, làm mới, In, Xuất excel\n"
     "- Bảng ghi \"Chưa có dữ liệu\", màn không tự lọc"),

    ("002", "Tiêu đề các cột", "P1",
     "KT-1 đã mở màn",
     "1. Quan sát dòng tiêu đề bảng",
     "—",
     "- 13 cột: STT, Nhân viên, DS tính thưởng năng suất tháng, DS tiêu chuẩn tính thưởng năng suất quý, "
     "Thưởng năng suất tháng, Thưởng năng suất quý, Tổng thưởng năng suất tính lũy tiến, Thưởng thêm, "
     "Thưởng thực hiện hợp đồng, Tiền vận chuyển, Tổng thu nhập từ bán hàng, Lãi quá hạn, Thưởng năng suất "
     "bị trừ quá hạn\n"
     "- Không có cột % Lũy tiến"),

    ("003", "Lọc lần đầu theo kỳ", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- Dòng Tổng cộng dưới tiêu đề\n"
     "- Dòng phòng KD1 (STT 1) in đậm, dưới là NV-A (1.1), NV-B (1.2)\n"
     "- Dòng phòng KD2 (STT 2), dưới là NV-C (2.1)"),

    ("004", "Biểu tượng đang tải", "P2",
     KT1,
     "1. Bấm Lọc, quan sát ngay",
     "—",
     "- Nút Lọc quay vòng và mờ; bảng hiện \"Đang tải dữ liệu\""),

    ("005", "Kỳ không có dữ liệu", "P1",
     "Kì 1 năm 2026 không có bút toán thưởng nào trong phạm vi KT-1",
     "1. Chọn Năm 2026, Kì 1, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\"; dòng Tổng cộng hiện \"-\" ở mọi cột"),

    ("006", "Cố định cột STT và Nhân viên khi cuộn ngang", "P2",
     KT1,
     "1. " + KY + "\n"
     "2. Cuộn bảng sang phải",
     "—",
     "- Cột STT và Nhân viên đứng yên, các cột tiền cuộn"),
]


SEC_II = [
    ("001", "Chọn Năm mà chưa chọn Kì", "P0",
     "KT-1 mở màn, Năm mặc định 2026",
     "1. Không chọn Kì, bấm Lọc",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\"\n"
     "- Dưới ô Kì quyết toán ghi \"Bắt buộc chọn\"; bảng không đổi"),

    ("002", "Chọn Kì tự điền Từ ngày, Đến ngày", "P0",
     "Cấu hình kỳ của TPE năm 2026: Kì 3 từ 01/07/2026 đến 30/09/2026",
     "1. Chọn Năm 2026, Kì 3",
     "—",
     "- Từ ngày 01/07/2026, Đến ngày 30/09/2026, hai ô bị khóa không sửa được"),

    ("003", "Danh sách Kì theo cấu hình của công ty", "P1",
     "Cấu hình kỳ của TPE năm 2026 có 4 kì",
     "1. Chọn Năm 2026, mở ô Kì quyết toán",
     "—",
     "- Có \"Chọn kì\", Kì 1, Kì 2, Kì 3, Kì 4"),

    ("004", "Năm chưa cấu hình kỳ", "P1",
     "TPE chưa cấu hình kỳ cho năm 2027",
     "1. Chọn Năm 2027, mở ô Kì quyết toán",
     "—",
     "- Chỉ có \"Chọn kì\"; bấm Lọc báo \"Chưa chọn đủ điều kiện bắt buộc\""),

    ("005", "Bỏ Năm để nhập khoảng ngày tự do", "P0",
     KT1,
     "1. Ở ô Năm chọn \"Chọn năm\"\n"
     "2. Nhập Từ ngày 01/07/2026, Đến ngày 31/07/2026, bấm Lọc",
     "—",
     "- Từ ngày, Đến ngày mở khóa, nhập được\n"
     "- Bảng chỉ tính bút toán có ngày hạch toán trong tháng 7/2026"),

    ("006", "Bỏ Năm mà không nhập ngày", "P0",
     "KT-1 đã chọn \"Chọn năm\"",
     "1. Để trống Từ ngày, Đến ngày, bấm Lọc",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\"\n"
     "- Dưới Từ ngày và Đến ngày ghi \"Bắt buộc chọn\""),

    ("007", "Bút toán ngày cuối kỳ được tính", "P0",
     "NV-C có thêm Thưởng năng suất quý 1.000.000 ở chứng từ hạch toán ngày 30/09/2026",
     "1. " + KY,
     "—",
     "- Thưởng năng suất quý của NV-C là 9.000.000 (gồm cả khoản ngày 30/09/2026)"),

    ("008", "Bút toán ngoài kỳ không được tính", "P0",
     "NV-C có Thưởng năng suất quý 1.000.000 hạch toán ngày 01/10/2026\n" + DATA,
     "1. " + KY,
     "—",
     "- Thưởng năng suất quý của NV-C vẫn là 8.000.000"),

    ("009", "Đổi Năm sau khi đã chọn Kì", "P1",
     "KT-1 đã chọn Năm 2026, Kì 3",
     "1. Đổi Năm sang 2025 (năm 2025 cũng có Kì 3), không chọn lại Kì\n"
     "2. Bấm Lọc",
     "—",
     "- Mong đợi: Kì bị xóa và yêu cầu chọn lại, hoặc Từ ngày / Đến ngày tự lấy theo Kì 3 năm 2025\n"
     "- Lưu ý: theo code hiện tại ô Kì vẫn hiện Kì 3, Từ ngày / Đến ngày bị xóa, Lọc ra bảng trống không "
     "báo gì - ghi Failed"),

    ("010", "In sau khi đổi Năm mà chưa chọn lại Kì", "P1",
     "KT-1 đã chọn Năm 2026, Kì 3, rồi đổi Năm sang 2025",
     "1. Bấm In",
     "—",
     "- Mong đợi: báo cần chọn Kì, hoặc in đúng Kì 3 năm 2025\n"
     "- Lưu ý: theo code hiện tại trang in báo lỗi hệ thống vì ngày trống - ghi Failed"),

    ("011", "Từ ngày sau Đến ngày", "P2",
     "KT-1 đã chọn \"Chọn năm\"",
     "1. Nhập Từ ngày 30/09/2026, Đến ngày 01/07/2026, bấm Lọc",
     "—",
     "- Mong đợi: báo Từ ngày phải trước Đến ngày\n"
     "- Lưu ý: theo code hiện tại không chặn, bảng trống - ghi Failed nếu nghiệp vụ yêu cầu chặn"),

    ("012", "Nút làm mới xóa hết bộ lọc", "P1",
     "KT-1 đã chọn Phòng ban KD1, Năm 2026, Kì 3, Xuất hóa đơn",
     "1. Bấm nút làm mới",
     "—",
     "- Phòng ban, Bộ phận, Nhân viên, Năm, Kì, Từ ngày, Đến ngày, Xuất hóa đơn đều trống\n"
     "- Từ ngày, Đến ngày mở khóa; bảng chưa lọc lại"),
]


SEC_III = [
    ("001", "Lọc theo Phòng ban", "P0",
     KT1,
     "1. Chọn Phòng ban KD2, Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Chỉ có phòng KD2 với NV-C\n"
     "- Tổng cộng: Thưởng năng suất quý 8.000.000, Tổng thu nhập 8.000.000"),

    ("002", "Lọc theo Nhân viên", "P0",
     KT1,
     "1. Chọn Nhân viên NV-B, Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Chỉ có KD1 với NV-B; Thưởng năng suất tháng 5.000.000"),

    ("003", "Lọc theo Bộ phận", "P1",
     "NV-A thuộc bộ phận BP1, NV-B thuộc BP2 (cùng KD1)\n" + DATA,
     "1. Chọn Phòng ban KD1, Bộ phận BP1, Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Chỉ có NV-A"),

    ("004", "Chọn Phòng ban thì Bộ phận, Nhân viên lọc theo phòng", "P1",
     KT1,
     "1. Chọn Phòng ban KD2\n"
     "2. Mở ô Nhân viên",
     "—",
     "- Ô Nhân viên chỉ có nhân viên của KD2"),

    ("005", "Lọc Xuất hóa đơn", "P0",
     KT1,
     "1. Chọn Xuất hóa đơn = \"Xuất hóa đơn\", Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- NV-A Thưởng năng suất tháng 10.000.000 (chỉ HD-01, không có HD-02)\n"
     "- NV-A Tổng thu nhập 21.000.000"),

    ("006", "Lọc Không xuất hóa đơn", "P0",
     KT1,
     "1. Chọn Xuất hóa đơn = \"Không xuất hóa đơn\", Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Chỉ có NV-A với Thưởng năng suất tháng 4.000.000 (HD-02)\n"
     "- Không có NV-B, NV-C nếu HD-01, HD-03 đều có xuất hóa đơn"),

    ("007", "Hợp đồng chưa ghi xuất hóa đơn tính vào nhóm Không xuất hóa đơn", "P1",
     "HD-06 để trống thông tin xuất hóa đơn; NV-B có Thưởng năng suất tháng 1.000.000 ở HD-06",
     "1. Chọn Xuất hóa đơn = \"Không xuất hóa đơn\", Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- NV-B có Thưởng năng suất tháng 1.000.000 (HD-06)"),

    ("008", "Quyền tổng công ty lọc theo Công ty", "P1",
     "KT-2 có quyền phạm vi Tổng công ty; TPC có NV-D",
     "1. Chọn Công ty TPC, Năm 2026, Kì 3, bấm Lọc",
     "—",
     "- Chỉ có nhân viên của TPC; ô Phòng ban chỉ còn phòng của TPC"),

    ("009", "Mở màn bằng đường dẫn có sẵn bộ lọc", "P2",
     KT1,
     "1. Mở màn bằng đường dẫn kèm tham số Phòng ban KD1, Năm 2026, Kì 3\n"
     "2. Bấm Lọc",
     "—",
     "- Các ô lọc tự điền theo đường dẫn; bảng chỉ có KD1"),
]


SEC_IV = [
    ("001", "Thưởng năng suất tháng cộng qua các hợp đồng", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Xem dòng NV-A",
     "—",
     "- Thưởng năng suất tháng 14.000.000 (HD-01 10.000.000 + HD-02 4.000.000)"),

    ("002", "Ghi Nợ điều chỉnh được trừ ra", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Xem dòng NV-B",
     "—",
     "- Thưởng năng suất tháng 5.000.000 (6.000.000 trừ 1.000.000)"),

    ("003", "Đúng cột theo vụ việc", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Xem dòng NV-A",
     "—",
     "- Thưởng năng suất quý 5.000.000; Thưởng thêm 2.000.000; Thưởng thực hiện hợp đồng 3.000.000; Tiền "
     "vận chuyển 1.000.000"),

    ("004", "Tổng thưởng năng suất tính lũy tiến", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- NV-A 19.000.000 (14.000.000 + 5.000.000); NV-B 5.000.000; NV-C 8.000.000"),

    ("005", "Tổng thu nhập từ bán hàng", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- NV-A 25.000.000 (19.000.000 + 2.000.000 + 3.000.000 + 1.000.000)\n"
     "- Không cộng Lãi quá hạn 500.000"),

    ("006", "DS tiêu chuẩn lấy từ phiếu quyết toán", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- NV-A: DS tính thưởng năng suất tháng 200.000.000, DS tiêu chuẩn quý 200.000.000\n"
     "- NV-B: 100.000.000 ở cả hai cột"),

    ("007", "Hợp đồng chưa quyết toán không có DS tiêu chuẩn", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- NV-C hiện \"-\" ở hai cột DS (HD-03 chưa quyết toán)\n"
     "- NV-A vẫn là 200.000.000 (HD-02 chưa quyết toán không cộng thêm)"),

    ("008", "Lãi quá hạn và thưởng bị trừ quá hạn", "P1",
     KT1,
     "1. " + KY,
     "—",
     "- NV-A Lãi quá hạn 500.000; NV-B, NV-C hiện \"-\""),

    ("009", "Phiếu chi không làm giảm thu nhập", "P0",
     "Trong kỳ kế toán lập phiếu chi trả 10.000.000 Thưởng năng suất tháng cho NV-A (ghi Nợ 3351)\n" + DATA,
     "1. " + KY,
     "—",
     "- NV-A Thưởng năng suất tháng vẫn 14.000.000"),

    ("010", "Phiếu kết chuyển chi phí phải trả không làm giảm thu nhập", "P0",
     "Trong kỳ có phiếu kết chuyển chi phí phải trả ghi Nợ 3351 cho NV-A 5.000.000\n" + DATA,
     "1. " + KY,
     "—",
     "- Số của NV-A không đổi"),

    ("011", "Bút toán không gắn hợp đồng không được tính", "P1",
     "Phiếu kế toán ghi Có 3351 Thưởng năng suất tháng 3.000.000 cho NV-C, không chọn hợp đồng\n" + DATA,
     "1. " + KY,
     "—",
     "- NV-C không có Thưởng năng suất tháng"),

    ("012", "Thưởng thêm từ phiếu năng suất quý phiên bản mới", "P1",
     "Phiếu quyết toán năng suất quý (phiên bản mới) đã hạch toán Thưởng thêm 4.000.000 cho NV-C trong kỳ, "
     "bút toán ghi theo nhân viên, không gắn hợp đồng\n" + DATA,
     "1. " + KY,
     "—",
     "- Mong đợi: NV-C Thưởng thêm 4.000.000, Tổng thu nhập 12.000.000\n"
     "- Lưu ý: theo code hiện tại Thưởng thêm vẫn \"-\" vì chỉ lấy bút toán gắn hợp đồng - ghi Failed"),

    ("013", "Hợp đồng bảo hành sửa chữa được tính như hợp đồng hãng", "P1",
     KT1,
     "1. " + KY + "\n"
     "2. Bấm NV-A mở chi tiết",
     "—",
     "- Có 2 dòng HD-01 và HD-02; HD-02 Thưởng năng suất tháng 4.000.000"),

    ("014", "Số âm khi ghi Nợ lớn hơn ghi Có", "P2",
     "NV-B có Thưởng thực hiện hợp đồng ghi Nợ 2.000.000, không có ghi Có trong kỳ",
     "1. " + KY,
     "—",
     "- NV-B Thưởng thực hiện hợp đồng -2.000.000; Tổng thu nhập giảm tương ứng"),

    ("015", "Lãi quá hạn của trưởng phòng", "P1",
     "QT-01 có phần lãi quá hạn của trưởng phòng KD1 là 300.000; NV-B có bút toán thưởng HD-01 nhưng không "
     "có dòng nhân viên trên QT-01",
     "1. " + KY,
     "—",
     "- Mong đợi: 300.000 chỉ tính cho trưởng phòng KD1\n"
     "- Lưu ý: theo code hiện tại nhân viên không có dòng trên phiếu quyết toán cũng nhận 300.000, cộng "
     "nhiều lần ở dòng phòng - ghi Failed nếu nghiệp vụ xác nhận"),
]


SEC_V = [
    ("001", "Dòng Tổng cộng tính trên mọi trang", "P0",
     "KT-1, trong kỳ có 25 nhân viên có thưởng (3 trang)",
     "1. " + KY + "\n"
     "2. Ghi số Tổng cộng, chuyển sang trang 2, 3",
     "—",
     "- Tổng cộng giống nhau ở mọi trang và bằng tổng của cả 25 nhân viên"),

    ("002", "Dòng phòng bằng tổng các nhân viên của phòng", "P0",
     KT1,
     "1. " + KY,
     "—",
     "- KD1: Thưởng năng suất tháng 19.000.000, quý 5.000.000, Tổng thưởng lũy tiến 24.000.000, Tổng thu "
     "nhập 30.000.000, DS tiêu chuẩn 300.000.000\n"
     "- KD2: Tổng thu nhập 8.000.000\n"
     "- Tổng cộng 38.000.000"),

    ("003", "Phòng có nhân viên nằm ở 2 trang", "P0",
     "Phòng KD1 có 13 nhân viên có thưởng trong kỳ, tổng thu nhập cả phòng 93,40 triệu; 10 nhân viên đầu "
     "cộng 87,96 triệu, 3 nhân viên sau cộng 5,44 triệu (số đối chiếu từ Phòng Thiết bị ô tô 2 quý 3/2025)",
     "1. " + KY + "\n"
     "2. Xem dòng KD1 ở trang 1, chuyển sang trang 2",
     "—",
     "- Mong đợi: dòng KD1 hiện 93,40 triệu và không lặp lại ở trang 2\n"
     "- Lưu ý: theo code hiện tại trang 1 hiện KD1 87,96 triệu, trang 2 lại có dòng KD1 5,44 triệu - ghi "
     "Failed"),

    ("004", "STT phòng và nhân viên liên tục qua trang", "P1",
     "KD1 có 13 nhân viên (STT 1), KD2 có 2 nhân viên",
     "1. " + KY + "\n"
     "2. Sang trang 2",
     "—",
     "- Nhân viên đầu trang 2 là 1.11; dòng KD2 có STT 2, nhân viên 2.1, 2.2"),

    ("005", "Phân trang 10 nhân viên", "P1",
     "KT-1, trong kỳ có 25 nhân viên",
     "1. " + KY,
     "—",
     "- Trang 1 có 10 dòng nhân viên; thanh phân trang có 3 trang"),

    ("006", "Thứ tự hiển thị", "P2",
     KT1,
     "1. " + KY,
     "—",
     "- Phòng xếp theo thứ tự phòng trong hệ thống; nhân viên trong phòng xếp theo thứ tự tạo nhân viên"),

    ("007", "Ô bằng 0 hiện gạch ngang", "P2",
     KT1,
     "1. " + KY + "\n"
     "2. Xem dòng NV-C",
     "—",
     "- Các cột Thưởng tháng, Thưởng thêm, Thưởng thực hiện hợp đồng, Tiền vận chuyển hiện \"-\""),

    ("008", "Nhân viên chuyển phòng trong kỳ", "P2",
     "NV-B chuyển từ KD1 sang KD2 ngày 15/08/2026; có Thưởng năng suất tháng ở cả hai phòng",
     "1. " + KY,
     "—",
     "- Mong đợi theo nghiệp vụ: số tách theo từng phòng\n"
     "- Lưu ý: theo code hiện tại NV-B chỉ hiện dưới một phòng với tổng của cả hai - ghi Failed nếu "
     "nghiệp vụ yêu cầu tách"),
]


SEC_VI = [
    ("001", "Mở chi tiết hợp đồng của nhân viên", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Bấm tên NV-A",
     "—",
     "- Cửa sổ \"Chi tiết hợp đồng của NV-A\"\n"
     "- 2 dòng HD-01, HD-02 với cột Hợp đồng, Khách hàng, Số quyết toán, Ngày bàn giao, Ngày thanh toán "
     "và các cột tiền"),

    ("002", "Số liệu chi tiết từng hợp đồng", "P0",
     KT1,
     "1. Mở chi tiết NV-A",
     "—",
     "- HD-01: tháng 10.000.000, quý 5.000.000, tính lũy tiến 15.000.000, Thưởng thêm 2.000.000, Thưởng "
     "thực hiện hợp đồng 3.000.000, Tiền vận chuyển 1.000.000, Tổng thu nhập 21.000.000, Số quyết toán "
     "QT-01, DS tiêu chuẩn 200.000.000, Lãi quá hạn 500.000\n"
     "- HD-02: tháng 4.000.000, Tổng thu nhập 4.000.000, Số quyết toán trống, DS tiêu chuẩn \"-\""),

    ("003", "Tổng cộng chi tiết khớp dòng nhân viên", "P0",
     KT1,
     "1. Mở chi tiết NV-A, xem dòng Tổng cộng",
     "—",
     "- Tổng thu nhập 25.000.000, đúng bằng dòng NV-A ở bảng chính"),

    ("004", "Chi tiết dùng cùng kỳ và bộ lọc của bảng chính", "P0",
     "KT-1 đã lọc Xuất hóa đơn = \"Xuất hóa đơn\", kỳ 3/2026\n" + DATA,
     "1. Mở chi tiết NV-A",
     "—",
     "- Chỉ có HD-01, không có HD-02"),

    ("005", "Lọc chi tiết theo Hợp đồng", "P1",
     KT1,
     "1. Mở chi tiết NV-A\n"
     "2. Gõ \"HD-02\" vào ô Hợp đồng, bấm Lọc",
     "—",
     "- Chỉ còn HD-02; Tổng cộng 4.000.000"),

    ("006", "Lọc chi tiết theo một phần số hợp đồng", "P2",
     KT1,
     "1. Mở chi tiết NV-A, gõ \"01\" vào ô Hợp đồng, bấm Lọc",
     "—",
     "- Còn HD-01"),

    ("007", "Lọc chi tiết theo Khách hàng", "P1",
     "HD-01 của khách KH-01, HD-02 của KH-02\n" + DATA,
     "1. Mở chi tiết NV-A, chọn Khách hàng KH-02, bấm Lọc",
     "—",
     "- Chỉ còn HD-02"),

    ("008", "Làm mới bộ lọc chi tiết", "P2",
     "Đang lọc chi tiết NV-A theo HD-02",
     "1. Bấm nút làm mới trong cửa sổ, bấm Lọc",
     "—",
     "- Ô Hợp đồng, Khách hàng trống; lại có HD-01, HD-02"),

    ("009", "Bấm số hợp đồng mở hợp đồng", "P1",
     KT1,
     "1. Mở chi tiết NV-A\n"
     "2. Bấm HD-01, rồi bấm HD-02",
     "—",
     "- HD-01 mở màn chi tiết hợp đồng hãng ở tab mới\n"
     "- HD-02 mở màn chi tiết hợp đồng bảo hành sửa chữa ở tab mới"),

    ("010", "Bấm số quyết toán mở phiếu quyết toán", "P1",
     KT1,
     "1. Mở chi tiết NV-A, bấm QT-01",
     "—",
     "- Mở phiếu quyết toán hợp đồng QT-01 ở tab mới"),

    ("011", "Phân trang chi tiết", "P2",
     "NV-A có 15 hợp đồng có thưởng trong kỳ",
     "1. Mở chi tiết NV-A, sang trang 2",
     "—",
     "- Trang 1 có 10 hợp đồng STT 1-10; trang 2 có 5 hợp đồng STT 11-15\n"
     "- Tổng cộng không đổi giữa hai trang"),

    ("012", "Mở chi tiết nhân viên khác làm mới cửa sổ", "P2",
     "Vừa xem chi tiết NV-A",
     "1. Đóng cửa sổ, bấm NV-C",
     "—",
     "- Tiêu đề đổi thành NV-C; chỉ có HD-03, không còn dòng của NV-A"),

    ("013", "Ngày bàn giao, Ngày thanh toán theo phiếu quyết toán", "P2",
     "QT-01 ngày bàn giao 15/07/2026, ngày thanh toán cuối 20/08/2026",
     "1. Mở chi tiết NV-A",
     "—",
     "- HD-01 Ngày bàn giao 15/07/2026, Ngày thanh toán 20/08/2026; HD-02 trống"),

    ("014", "Tên cột DS tháng ở chi tiết khác bảng chính", "P2",
     KT1,
     "1. So tên cột thứ 3 của bảng chính với cột DS tháng ở cửa sổ chi tiết",
     "—",
     "- Mong đợi: cùng một tên\n"
     "- Lưu ý: bảng chính ghi \"DS tính thưởng năng suất tháng\", chi tiết ghi \"DS tiêu chuẩn tính "
     "thưởng năng suất tháng\" - ghi Failed nếu cần thống nhất"),
]


SEC_VII = [
    ("001", "In bảng tổng hợp", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Bấm In",
     "—",
     "- Mở tab mới khổ ngang, tiêu đề công ty, kỳ 01/07/2026 - 30/09/2026\n"
     "- Bảng 13 cột như màn, KD1, KD2 và 3 nhân viên; Tổng cộng 38.000.000"),

    ("002", "In lấy toàn bộ, không theo trang", "P0",
     "KT-1, trong kỳ có 25 nhân viên (3 trang)",
     "1. Đang ở trang 1, bấm In",
     "—",
     "- Bản in có đủ 25 nhân viên\n"
     "- Dòng phòng trên bản in là tổng đầy đủ của phòng"),

    ("003", "In khi chưa đủ điều kiện", "P1",
     "KT-1 có Năm 2026, chưa chọn Kì",
     "1. Bấm In",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\", không mở tab"),

    ("004", "Xuất excel bảng tổng hợp", "P0",
     KT1,
     "1. " + KY + "\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file \"Bang_tong_hop_thu_nhap_tu_ban_hang.xlsx\"\n"
     "- Tiêu đề \"Bảng tổng hợp thu nhập từ bán hàng\", 13 cột, số liệu như màn"),

    ("005", "Excel giữ bộ lọc", "P0",
     "KT-1 lọc Phòng ban KD2, kỳ 3/2026",
     "1. Bấm Xuất excel",
     "—",
     "- File chỉ có KD2 và NV-C"),

    ("006", "Excel số liệu dạng số", "P2",
     KT1,
     "1. Xuất excel, mở file, chọn ô Tổng thu nhập của NV-A",
     "—",
     "- Ô là số 25000000 tính tổng được, không phải chữ"),

    ("007", "In chi tiết nhân viên", "P0",
     KT1,
     "1. Mở chi tiết NV-A, bấm In trong cửa sổ",
     "—",
     "- Tab mới có tên \"<mã NV-A>-<TÊN NV-A>\" viết hoa, kỳ 01/07/2026 - 30/09/2026\n"
     "- Bảng HD-01, HD-02 và Tổng cộng 25.000.000"),

    ("008", "Xuất excel chi tiết nhân viên", "P0",
     KT1,
     "1. Mở chi tiết NV-A, bấm Xuất excel trong cửa sổ",
     "—",
     "- Tải file \"Bang_tong_hop_thu_nhap_tu_ban_hang_chi_tiet_nhan_vien.xlsx\" có HD-01, HD-02"),

    ("009", "In chi tiết giữ bộ lọc Hợp đồng", "P1",
     "Đang lọc chi tiết NV-A theo HD-02",
     "1. Bấm In trong cửa sổ",
     "—",
     "- Bản in chỉ có HD-02"),

    ("010", "In tôn trọng phạm vi quyền", "P0",
     "NV-A không có quyền xem\n" + DATA,
     "1. Đăng nhập NV-A, " + KY + ", bấm In",
     "—",
     "- Bản in chỉ có NV-A"),

    ("011", "Bỏ Năm, In theo khoảng ngày", "P1",
     "KT-1 chọn \"Chọn năm\", Từ ngày 01/07/2026, Đến ngày 31/07/2026",
     "1. Bấm Lọc rồi In",
     "—",
     "- Bản in ghi kỳ từ 01/07/2026 đến 31/07/2026, số khớp màn"),
]


SEC_VIII = [
    ("001", "Đối chiếu tổng thu nhập với sổ chi tiết TK 3351", "P0",
     KT1,
     "1. " + KY + ", ghi Tổng cộng từng cột thưởng\n"
     "2. Mở sổ chi tiết TK 3351 cùng kỳ, cộng phát sinh Có trừ Nợ theo từng vụ việc (bỏ phiếu chi, ủy "
     "nhiệm chi, kết chuyển chi phí phải trả, bút toán không gắn hợp đồng)",
     "—",
     "- Từng cột khớp số trên sổ"),

    ("002", "Hạch toán thêm thưởng thì báo cáo tăng", "P0",
     KT1,
     "1. Lọc kỳ 3/2026, ghi số NV-C\n"
     "2. Duyệt một phiếu hạch toán ghi Có 3351 Thưởng năng suất quý 2.000.000 cho NV-C ở HD-03, ngày "
     "10/08/2026\n"
     "3. Bấm Lọc lại",
     "—",
     "- NV-C Thưởng năng suất quý 10.000.000; KD2 và Tổng cộng tăng 2.000.000"),

    ("003", "Quyết toán hợp đồng thì DS tiêu chuẩn xuất hiện", "P0",
     KT1,
     "1. Lọc kỳ 3/2026: NV-C DS tiêu chuẩn \"-\"\n"
     "2. Duyệt phiếu quyết toán HD-03 với DS tiêu chuẩn NV-C 80.000.000\n"
     "3. Bấm Lọc lại",
     "—",
     "- NV-C DS tính thưởng năng suất tháng và DS tiêu chuẩn quý 80.000.000"),

    ("004", "Chi trả thưởng không làm đổi báo cáo", "P1",
     KT1,
     "1. Lọc kỳ 3/2026, ghi số NV-A\n"
     "2. Kế toán lập phiếu chi trả thưởng tháng cho NV-A\n"
     "3. Lọc lại",
     "—",
     "- Số NV-A không đổi"),

    ("005", "Hai người xem cùng lúc theo quyền khác nhau", "P1",
     "KT-1 phạm vi Công ty; TP-1 phạm vi Phòng ban quản lý KD1\n" + DATA,
     "1. KT-1 và TP-1 cùng lọc kỳ 3/2026",
     "—",
     "- KT-1 thấy Tổng cộng 38.000.000; TP-1 thấy 30.000.000"),

    ("006", "Luồng đầu - cuối: từ hạch toán tới in báo cáo", "P0",
     KT1,
     "1. Duyệt quyết toán HD-01, hạch toán thưởng tháng, quý, thưởng thêm, thưởng thực hiện hợp đồng, tiền "
     "vận chuyển cho NV-A trong kỳ 3/2026\n"
     "2. Mở báo cáo, " + KY + "\n"
     "3. Bấm NV-A xem chi tiết, In chi tiết\n"
     "4. Đóng cửa sổ, Xuất excel bảng tổng hợp",
     "—",
     "- Dòng NV-A đủ các cột như dữ liệu mẫu, Tổng thu nhập 25.000.000\n"
     "- Chi tiết, bản in chi tiết và file Excel cùng số"),
]
