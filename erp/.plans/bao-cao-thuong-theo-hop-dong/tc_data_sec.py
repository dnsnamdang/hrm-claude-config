# -*- coding: utf-8 -*-
"""Section I - IX cho man Bao cao thuong theo hop dong."""
from tc_data_role import MENU, DATA, KT, LOC_T10

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     KT,
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề \"BÁO CÁO THƯỞNG THEO HỢP ĐỒNG\"\n"
     "- Bộ lọc: Phòng ban, Bộ phận, Nhân viên, Từ ngày (bắt buộc), Đến ngày (bắt buộc), Hợp đồng, Khách hàng\n"
     "- Nút Lọc (mờ khi chưa chọn ngày), làm mới, In, Xuất excel (mờ khi bảng chưa có dữ liệu)\n"
     "- Bảng ghi \"Chưa có dữ liệu\", chưa tự lọc"),

    ("002", "Cột của bảng và dòng Tổng cộng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Cột: STT, Hợp đồng, Khách hàng, Phòng ban, Thưởng thực hiện hợp đồng, Thưởng năng suất tháng, "
     "Thưởng năng suất quý, Tiền vận chuyển còn lại, Tổng cộng, Doanh số tiêu chuẩn\n"
     "- Ngay dưới tiêu đề có dòng \"Tổng cộng\""),

    ("003", "Hiển thị dòng hợp đồng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Xem dòng HD-01",
     "—",
     "- STT 1 (chữ đậm), Hợp đồng HD-01 dạng liên kết, Khách hàng \"KH-01 - <tên khách>\", Phòng ban P1\n"
     "- Số tiền có dấu phân cách hàng nghìn; ô bằng 0 hiện \"-\""),

    ("004", "Bấm số hợp đồng hãng mở hợp đồng", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm HD-01",
     "—",
     "- Mở tab mới, trang chi tiết hợp đồng hãng HD-01"),

    ("005", "Bấm số hợp đồng bảo hành sửa chữa", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm BH-02",
     "—",
     "- Mở tab mới, trang chi tiết hợp đồng bảo hành sửa chữa BH-02"),

    ("006", "Đang tải dữ liệu", "P2",
     KT,
     "1. " + LOC_T10 + ", quan sát ngay",
     "—",
     "- Bảng hiện \"Đang tải dữ liệu\"; nút Lọc, In, Xuất excel mờ đến khi xong"),

    ("007", "Khoảng ngày không có thưởng nào", "P1",
     KT + "; không có bút toán thưởng nào trong năm 2020",
     "1. Chọn Từ ngày 01/01/2020, Đến ngày 31/12/2020, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\"; dòng Tổng cộng bằng 0; nút In, Xuất excel mờ"),
]


SEC_II = [
    ("001", "Thiếu Từ ngày hoặc Đến ngày thì không lọc được", "P0",
     KT,
     "1. Chỉ chọn Từ ngày 01/10/2026\n"
     "2. Quan sát nút Lọc",
     "—",
     "- Nút Lọc mờ, không bấm được"),

    ("002", "Bấm sắp xếp cột khi chưa chọn ngày", "P1",
     KT,
     "1. Để trống Từ ngày, Đến ngày\n"
     "2. Bấm tiêu đề cột \"Tổng cộng\"",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\"\n"
     "- Dưới 2 ô ngày ghi \"Bắt buộc chọn\"; bảng không đổi"),

    ("003", "Khoảng ngày lấy theo ngày hạch toán, tính trọn ngày cuối", "P0",
     KT + "; bút toán Năng suất tháng NV-A 700.000 của HD-01 hạch toán 31/10/2026 lúc 17:30, bút toán 450.000 "
     "hạch toán 01/11/2026",
     "1. " + LOC_T10,
     "—",
     "- Có 700.000 của ngày 31/10/2026\n"
     "- Không có số của ngày 01/11/2026"),

    ("004", "Từ ngày sau Đến ngày", "P2",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 31/10/2026, Đến ngày 01/10/2026, bấm Lọc",
     "—",
     "- Mong đợi: báo Từ ngày không được sau Đến ngày\n"
     "- Lưu ý: theo code hiện tại vẫn lọc, bảng ghi \"Chưa có dữ liệu\" - ghi Failed"),

    ("005", "Lọc theo Nhân viên", "P0",
     KT + "\n" + DATA,
     "1. Ô Nhân viên chọn NV-B\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có HD-01; các cột chỉ cộng phần của NV-B: Năng suất tháng 800.000, Tổng 800.000\n"
     "- Dưới HD-01 chỉ có dòng NV-B; không có BH-02"),

    ("006", "Lọc theo Hợp đồng gõ một phần số", "P0",
     KT + "\n" + DATA,
     "1. Ô Hợp đồng gõ \"HD-0\"\n"
     "2. " + LOC_T10,
     "—",
     "- Có HD-01; không có BH-02"),

    ("007", "Lọc theo Khách hàng", "P0",
     KT + "\n" + DATA,
     "1. Bấm nút tìm ở ô Khách hàng, chọn KH-02\n"
     "2. " + LOC_T10,
     "—",
     "- Ô Khách hàng hiện tên KH-02\n"
     "- Chỉ có BH-02"),

    ("008", "Bỏ khách hàng đã chọn", "P1",
     KT + "\n" + DATA,
     "1. Chọn Khách hàng KH-02, bấm Lọc\n"
     "2. Bấm nút x ở ô Khách hàng, bấm Lọc",
     "—",
     "- Ô Khách hàng trống; bảng có lại cả HD-01 và BH-02"),

    ("009", "Lọc theo Phòng ban", "P0",
     KT + "; NV-D phòng P2 có bút toán thưởng HD-05 2.000.000 tháng 10/2026\n" + DATA,
     "1. Ô Phòng ban chọn P2\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có HD-05 (Tổng 2.000.000); không có HD-01, BH-02"),

    ("010", "Lọc Phòng ban xét phòng trên bút toán, không xét phòng trên hợp đồng", "P1",
     KT + "; HD-06 có phòng trên hợp đồng là P1, nhưng bút toán thưởng là của NV-D phòng P2 (2.000.000)",
     "1. Ô Phòng ban chọn P1\n"
     "2. " + LOC_T10 + "\n"
     "3. Đổi Phòng ban sang P2, bấm Lọc",
     "—",
     "- Bước 2: không có HD-06\n"
     "- Bước 3: có HD-06, cột Phòng ban của dòng hợp đồng ghi P1\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ muốn lọc theo phòng trên hợp đồng"),

    ("011", "Lọc theo Bộ phận", "P1",
     KT + "; NV-A thuộc bộ phận BP1, NV-B thuộc BP2\n" + DATA,
     "1. Ô Phòng ban chọn P1, ô Bộ phận chọn BP1\n"
     "2. " + LOC_T10,
     "—",
     "- HD-01 chỉ cộng phần NV-A (Tổng 7.000.000), không có dòng NV-B"),

    ("012", "Lọc theo Công ty (quyền theo tổng công ty)", "P1",
     "TGĐ-1 có quyền theo tổng công ty; HD-09 của TPC có thưởng tháng 10/2026",
     "1. Ô Công ty chọn TPC\n"
     "2. " + LOC_T10,
     "—",
     "- Chỉ có hợp đồng của TPC (có HD-09); không có HD-01, BH-02"),

    ("013", "Nút làm mới", "P1",
     KT + "\n" + DATA,
     "1. Chọn Nhân viên NV-A, Khách hàng KH-01, Hợp đồng \"HD\", " + LOC_T10.lower() + "\n"
     "2. Bấm nút làm mới",
     "—",
     "- Mọi ô lọc trống (kể cả Từ ngày, Đến ngày); nút Lọc mờ\n"
     "- Bảng giữ kết quả cũ đến lần lọc sau"),

    ("014", "Kết hợp nhiều điều kiện lọc", "P1",
     KT + "\n" + DATA,
     "1. Chọn Nhân viên NV-A, Khách hàng KH-02\n"
     "2. " + LOC_T10,
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\" (NV-A không có thưởng ở hợp đồng của KH-02)"),
]


SEC_III = [
    ("001", "Cột Thưởng thực hiện hợp đồng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Xem dòng HD-01",
     "—",
     "- Thưởng thực hiện hợp đồng = 3.000.000"),

    ("002", "Cột năng suất tháng = Có trừ Nợ", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Xem dòng HD-01",
     "—",
     "- Thưởng năng suất tháng = 2.000.000 + 1.000.000 trừ 200.000 = 2.800.000"),

    ("003", "Cột năng suất quý và tiền vận chuyển", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- HD-01: Thưởng năng suất quý 1.500.000, Tiền vận chuyển còn lại 500.000"),

    ("004", "Tổng cộng của dòng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- HD-01 Tổng cộng = 3.000.000 + 2.800.000 + 1.500.000 + 500.000 = 7.800.000\n"
     "- Tổng cộng không cộng Doanh số tiêu chuẩn"),

    ("005", "Phiếu chi trả thưởng không làm giảm số thưởng", "P0",
     KT + "; ngày 20/10/2026 có phiếu chi trả NV-A 2.000.000 thưởng năng suất tháng của HD-01 (ghi Nợ 3351)\n"
     + DATA,
     "1. " + LOC_T10,
     "—",
     "- HD-01 Thưởng năng suất tháng vẫn 2.800.000, NV-A vẫn 2.000.000"),

    ("006", "Ủy nhiệm chi và kết chuyển chi phí phải trả không được tính", "P0",
     KT + "; trong tháng 10/2026 có ủy nhiệm chi trả NV-B 800.000 và phiếu kết chuyển chi phí phải trả của "
     "phòng P1 ghi Nợ 3351 cho HD-01\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Số của HD-01, NV-B không đổi so với khi chưa có 2 phiếu này"),

    ("007", "Bút toán điều chỉnh giảm làm cột âm", "P1",
     KT + "; HD-07 trong tháng 10/2026 chỉ có bút toán điều chỉnh Nợ 3351 năng suất tháng của NV-A 300.000",
     "1. " + LOC_T10,
     "—",
     "- Có HD-07, Thưởng năng suất tháng -300.000, Tổng cộng -300.000"),

    ("008", "Hợp đồng mà các cột bù trừ về 0 thì không hiện", "P1",
     KT + "; HD-08 trong tháng 10/2026 có năng suất tháng Có 500.000 và Nợ 500.000",
     "1. " + LOC_T10,
     "—",
     "- Không có HD-08"),

    ("009", "Bút toán không gắn nhân viên không được tính", "P1",
     KT + "; HD-01 có thêm bút toán 3351 năng suất tháng Có 900.000 không gắn nhân viên\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- HD-01 Thưởng năng suất tháng vẫn 2.800.000"),

    ("010", "Hợp đồng loại khác không có trên báo cáo", "P1",
     KT + "; hợp đồng dự án DA-01 có bút toán 3351 thưởng năng suất tháng NV-A 1.000.000 tháng 10/2026",
     "1. " + LOC_T10,
     "—",
     "- Không có DA-01\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ cần cả hợp đồng loại khác"),

    ("011", "Thưởng thêm không có trên báo cáo", "P1",
     KT + "; HD-01 có bút toán 3351 Thưởng thêm NV-A 1.000.000 tháng 10/2026\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Không có cột Thưởng thêm; HD-01 Tổng cộng vẫn 7.800.000\n"
     "- Lưu ý: ghi để nghiệp vụ quyết có cần cột Thưởng thêm không"),

    ("012", "Bút toán thưởng của hợp đồng bảo hành sửa chữa", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Xem dòng BH-02",
     "—",
     "- Khách hàng \"KH-02 - <tên>\", Phòng ban P1\n"
     "- Thưởng năng suất tháng 1.200.000, Tổng cộng 1.200.000; các cột khác \"-\""),
]


SEC_IV = [
    ("001", "Các dòng nhân viên dưới hợp đồng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Xem các dòng dưới HD-01",
     "—",
     "- Dòng 1.1, 1.2 cho NV-A, NV-B; cột Hợp đồng ghi tên nhân viên, cột Khách hàng trống, cột Phòng ban "
     "ghi phòng của nhân viên"),

    ("002", "Số tiền từng nhân viên", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- NV-A: 3.000.000 / 2.000.000 / 1.500.000 / 500.000, Tổng 7.000.000\n"
     "- NV-B: Năng suất tháng 800.000, Tổng 800.000; các cột khác \"-\""),

    ("003", "Cộng các dòng nhân viên bằng dòng hợp đồng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Cộng từng cột của các dòng nhân viên HD-01",
     "—",
     "- Bằng đúng các cột của dòng HD-01 (Tổng 7.000.000 + 800.000 = 7.800.000)"),

    ("004", "Hợp đồng có rất nhiều bút toán vẫn đủ dòng nhân viên", "P2",
     KT + "; hợp đồng HD-50 có hơn 300 dòng bút toán thưởng trong kỳ, chia cho 6 nhân viên (dữ liệu thử)",
     "1. Lọc khoảng ngày có các bút toán của HD-50\n"
     "2. Đếm các dòng nhân viên của HD-50 và cộng cột Tổng cộng",
     "—",
     "- Mong đợi: đủ 6 nhân viên, cộng các dòng nhân viên bằng dòng HD-50\n"
     "- Lưu ý: theo code hiện tại danh sách nhân viên của hợp đồng bị cắt khi quá dài (khoảng 250 dòng bút "
     "toán trở lên), có thể thiếu nhân viên - ghi Failed. Dữ liệu thật hiện chưa có hợp đồng nào dài như vậy"),

    ("005", "Nhân viên có các cột bù trừ về 0 không có dòng", "P1",
     KT + "; HD-01 có thêm NV-E: năng suất tháng Có 300.000, Nợ 300.000 trong tháng 10/2026\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Dưới HD-01 không có dòng NV-E"),

    ("006", "Phòng ban của dòng nhân viên là phòng hiện tại", "P1",
     KT + "; NV-B chuyển từ P1 sang P3 ngày 05/11/2026\n" + DATA,
     "1. Ngày 17/11/2026 " + LOC_T10.lower(),
     "—",
     "- Dòng NV-B ghi Phòng ban P3 (phòng hiện tại)\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ muốn hiện phòng tại thời điểm hạch toán"),

    ("007", "Thứ tự nhân viên theo cột đang sắp", "P2",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm tiêu đề cột \"Tổng cộng\"",
     "—",
     "- Trong HD-01, NV-B (800.000) đứng trước NV-A (7.000.000)"),
]


SEC_V = [
    ("001", "Doanh số tiêu chuẩn của hợp đồng hãng đã quyết toán", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Dòng HD-01 Doanh số tiêu chuẩn 100.000.000"),

    ("002", "Doanh số tiêu chuẩn từng nhân viên theo tỷ lệ hưởng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- NV-A 60.000.000 (100.000.000 x 60%), NV-B 40.000.000 (x 40%)"),

    ("003", "Doanh số tiêu chuẩn không bị nhân đôi", "P0",
     "KT-1; hợp đồng HĐ_TPE_HN_KD2_25_0135_VXM đã quyết toán, doanh số tiêu chuẩn trên phiếu quyết toán "
     "925.509.958; có thưởng hạch toán ngày 30/09/2025; nhân viên phòng chính hưởng 100%",
     "1. Chọn Từ ngày 01/09/2025, Đến ngày 30/09/2025, ô Hợp đồng gõ \"0135_VXM\", bấm Lọc\n"
     "2. Mở phiếu quyết toán của hợp đồng, so cột Doanh số tiêu chuẩn",
     "—",
     "- Mong đợi: dòng hợp đồng và dòng nhân viên phòng chính đều 925.509.958, khớp phiếu quyết toán\n"
     "- Lưu ý: theo code hiện tại ra 1.851.019.915 (gấp đôi), vì doanh số được cộng cả bản lưu theo phiếu "
     "yêu cầu quyết toán lẫn bản lưu theo phiếu quyết toán - ghi Failed"),

    ("004", "Nhân viên không thuộc phòng chính không có doanh số tiêu chuẩn", "P1",
     KT + "; HD-01 có thêm NV-F thuộc phòng phối hợp, có thưởng năng suất tháng 500.000 tháng 10/2026\n"
     + DATA,
     "1. " + LOC_T10,
     "—",
     "- Dòng NV-F: Năng suất tháng 500.000, Doanh số tiêu chuẩn \"-\""),

    ("005", "Hợp đồng hãng chưa quyết toán", "P0",
     KT + "; HD-03 hợp đồng hãng Có hiệu lực, chưa có quyết toán, NV-A có thưởng năng suất tháng 600.000 "
     "tháng 10/2026",
     "1. " + LOC_T10,
     "—",
     "- Dòng HD-03 và dòng NV-A của HD-03: Doanh số tiêu chuẩn \"-\""),

    ("006", "Hợp đồng bảo hành sửa chữa không có doanh số tiêu chuẩn", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- BH-02 và NV-C: Doanh số tiêu chuẩn \"-\"\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ cần doanh số tiêu chuẩn cho hợp đồng bảo hành sửa chữa"),

    ("007", "Doanh số tiêu chuẩn không theo khoảng ngày", "P1",
     KT + "\n" + DATA + "\nHD-01 có thêm thưởng NV-A tháng 11/2026",
     "1. " + LOC_T10 + "\n"
     "2. Chọn Từ ngày 01/11/2026, Đến ngày 30/11/2026, bấm Lọc",
     "—",
     "- Cả 2 lần, HD-01 Doanh số tiêu chuẩn đều 100.000.000\n"
     "- Lọc cả 01/10 - 30/11/2026 thì HD-01 chỉ hiện 1 dòng, doanh số 100.000.000"),

    ("008", "Lọc Nhân viên thì dòng hợp đồng vẫn lấy doanh số cả hợp đồng", "P1",
     KT + "\n" + DATA,
     "1. Ô Nhân viên chọn NV-B\n"
     "2. " + LOC_T10,
     "—",
     "- Dòng NV-B Doanh số tiêu chuẩn 40.000.000\n"
     "- Mong đợi: dòng HD-01 và dòng Tổng cộng theo phần của NV-B (40.000.000)\n"
     "- Lưu ý: theo code hiện tại dòng HD-01 và Tổng cộng vẫn 100.000.000 - ghi Failed"),

    ("009", "Người không có quyền thấy doanh số cả hợp đồng", "P1",
     "NV-B không có quyền xem báo cáo thưởng theo hợp đồng\n" + DATA,
     "1. Đăng nhập NV-B, " + LOC_T10.lower(),
     "—",
     "- Dòng NV-B Doanh số tiêu chuẩn 40.000.000\n"
     "- Mong đợi: dòng HD-01 không lộ doanh số của người khác\n"
     "- Lưu ý: theo code hiện tại dòng HD-01 và Tổng cộng ghi 100.000.000 - ghi Failed"),
]


SEC_VI = [
    ("001", "Dòng Tổng cộng cộng mọi hợp đồng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Thưởng thực hiện hợp đồng 3.000.000; Năng suất tháng 2.800.000 + 1.200.000 = 4.000.000; Năng suất "
     "quý 1.500.000; Tiền vận chuyển 500.000; Tổng cộng 9.000.000; Doanh số tiêu chuẩn 100.000.000"),

    ("002", "Tổng cộng tính cả hợp đồng ở trang khác", "P0",
     KT + "; tháng 10/2026 có 23 hợp đồng có thưởng",
     "1. " + LOC_T10 + "\n"
     "2. Cộng cột Tổng cộng của 10 hợp đồng trang 1, so với dòng Tổng cộng",
     "—",
     "- Dòng Tổng cộng bằng tổng của cả 23 hợp đồng, lớn hơn tổng trang 1\n"
     "- Sang trang 2, 3 dòng Tổng cộng không đổi"),

    ("003", "Phân trang 10 hợp đồng, STT liên tục", "P0",
     KT + "; tháng 10/2026 có 23 hợp đồng có thưởng",
     "1. " + LOC_T10 + "\n"
     "2. Bấm trang 3",
     "—",
     "- Trang 1 có 10 hợp đồng; trang 3 có 3 hợp đồng, STT 21, 22, 23; dòng nhân viên dạng 21.1, 21.2"),

    ("004", "Sắp mặc định theo số hợp đồng giảm dần", "P1",
     KT + "; có HD-01, HD-03, HD-07 trong tháng 10/2026",
     "1. " + LOC_T10,
     "—",
     "- Thứ tự HD-07, HD-03, HD-01"),

    ("005", "Sắp theo một cột số tiền", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm tiêu đề cột \"Tổng cộng\"\n"
     "3. Bấm lại lần nữa",
     "—",
     "- Bước 2: tăng dần, BH-02 (1.200.000) trước HD-01 (7.800.000), biểu tượng mũi tên lên\n"
     "- Bước 3: giảm dần, HD-01 trước BH-02\n"
     "- Mỗi lần bấm quay về trang 1"),

    ("006", "Các cột sắp xếp được", "P2",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Lần lượt bấm tiêu đề từng cột",
     "—",
     "- Sắp được: Thưởng thực hiện hợp đồng, năng suất tháng, năng suất quý, Tiền vận chuyển còn lại, Tổng "
     "cộng, Doanh số tiêu chuẩn\n"
     "- Bấm STT, Hợp đồng, Khách hàng, Phòng ban không có tác dụng"),

    ("007", "Đổi trang giữ nguyên bộ lọc và thứ tự", "P1",
     KT + "; tháng 10/2026 có 23 hợp đồng",
     "1. Chọn Nhân viên NV-A, " + LOC_T10.lower() + ", sắp theo Tổng cộng\n"
     "2. Bấm trang 2",
     "—",
     "- Trang 2 vẫn theo NV-A và vẫn sắp theo Tổng cộng"),
]


SEC_VII = [
    ("001", "In báo cáo", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm In",
     "—",
     "- Mở tab mới bản in khổ ngang, có tiêu đề công ty\n"
     "- Bảng: STT, Hợp đồng, Khách hàng, Phòng ban, 4 cột thưởng, Tổng cộng, Doanh số tiêu chuẩn; dòng Tổng "
     "cộng đầu bảng = 9.000.000\n"
     "- Có HD-01 với 2 dòng 1.1 NV-A, 1.2 NV-B (mã - tên nhân viên) và BH-02"),

    ("002", "In lấy toàn bộ, không theo trang", "P0",
     KT + "; tháng 10/2026 có 23 hợp đồng",
     "1. " + LOC_T10 + ", đứng ở trang 2\n"
     "2. Bấm In",
     "—",
     "- Bản in có đủ 23 hợp đồng, STT 1 đến 23"),

    ("003", "Xuất excel", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file bao_cao_thuong_theo_hop_dong.xlsx, tiêu đề \"Báo cáo thưởng theo hợp đồng\"\n"
     "- Số liệu khớp màn hình, gồm cả dòng nhân viên và dòng Tổng cộng\n"
     "- Ô số ghi số thô (ví dụ 7800000), ô bằng 0 ghi \"-\""),

    ("004", "In / Excel theo bộ lọc và thứ tự đang chọn", "P0",
     KT + "\n" + DATA,
     "1. Chọn Nhân viên NV-A, " + LOC_T10.lower() + ", sắp theo Tổng cộng tăng dần\n"
     "2. Bấm In, rồi Xuất excel",
     "—",
     "- Cả hai chỉ có số của NV-A và theo đúng thứ tự trên màn"),

    ("005", "Nút In, Xuất excel khi bảng trống", "P1",
     KT,
     "1. Lọc khoảng ngày không có thưởng\n"
     "2. Bấm In, Xuất excel",
     "—",
     "- Hai nút mờ, không mở gì"),

    ("006", "Ký tự & trong tên khách hàng", "P2",
     KT + "; khách KH-01 tên \"Công ty A & B\"",
     "1. " + LOC_T10 + ", bấm In và Xuất excel",
     "—",
     "- Tên khách hiện đúng \"Công ty A & B\", file mở không lỗi"),

    ("007", "Xuất excel khoảng ngày dài", "P2",
     "TGĐ-1 có quyền theo tổng công ty",
     "1. Chọn Từ ngày 01/01/2024, Đến ngày 31/10/2026, bấm Lọc\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải được file trong thời gian chấp nhận được, không báo lỗi hệ thống"),
]


SEC_VIII = [
    ("001", "Đối chiếu với sổ chi tiết TK 3351", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Mở sổ chi tiết TK 3351 tháng 10/2026, lọc HD-01, bỏ phiếu chi, ủy nhiệm chi, kết chuyển chi phí "
     "phải trả, cộng theo từng vụ việc",
     "—",
     "- Từng cột của HD-01 khớp với số Có trừ Nợ của vụ việc tương ứng"),

    ("002", "Đối chiếu với Bảng tổng hợp thu nhập từ bán hàng", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + ", lọc Nhân viên NV-A\n"
     "2. Mở Bảng tổng hợp thu nhập từ bán hàng cùng khoảng ngày, xem dòng NV-A",
     "—",
     "- Năng suất tháng, năng suất quý, Thưởng thực hiện hợp đồng, tiền vận chuyển của NV-A khớp nhau\n"
     "- Tổng của bảng kia có thể lớn hơn đúng bằng phần Thưởng thêm"),

    ("003", "Báo cáo không sửa dữ liệu", "P0",
     KT + "\n" + DATA,
     "1. Lọc, sắp xếp, đổi trang, In, Xuất excel nhiều lần\n"
     "2. Mở lại sổ chi tiết TK 3351 và hợp đồng HD-01",
     "—",
     "- Không có bút toán, trạng thái hay số liệu nào thay đổi"),

    ("004", "Bút toán mới hạch toán hiện sau khi lọc lại", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10 + "\n"
     "2. Kế toán duyệt thêm phiếu thưởng NV-A HD-01 năng suất tháng 300.000 ngày 30/10/2026\n"
     "3. Bấm Lọc lại",
     "—",
     "- Bước 3: HD-01 Năng suất tháng 3.100.000, NV-A 2.300.000"),

    ("005", "Ô Hợp đồng gõ ký tự đặc biệt", "P2",
     KT,
     "1. Ô Hợp đồng gõ \"' OR 1=1 --\"\n"
     "2. " + LOC_T10,
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\", không báo lỗi, không lộ hợp đồng nào"),

    ("006", "Gọi thẳng chức năng với ngày sai định dạng", "P2",
     KT,
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu với Từ ngày \"2026-10-01\"",
     "—",
     "- Mong đợi: báo ngày không hợp lệ\n"
     "- Lưu ý: theo code hiện tại báo lỗi hệ thống - ghi Failed"),
]


SEC_IX = [
    ("001", "Thưởng năng suất tháng ghi nhận lên báo cáo", "P0",
     KT + "; HD-10 hợp đồng hãng mới, NV-A là người thực hiện",
     "1. Kế toán duyệt phiếu năng suất tháng 10/2026 có thưởng NV-A HD-10 1.000.000 (hạch toán 31/10/2026)\n"
     "2. " + LOC_T10,
     "—",
     "- Có HD-10, Năng suất tháng 1.000.000, dòng NV-A 1.000.000"),

    ("002", "Trả thưởng bằng phiếu chi không làm mất số trên báo cáo", "P0",
     KT + "; tiếp TC 001",
     "1. Ngày 05/11/2026 kế toán lập phiếu chi trả NV-A 1.000.000 thưởng HD-10\n"
     "2. " + LOC_T10 + "\n"
     "3. Lọc tháng 11/2026",
     "—",
     "- Bước 2: HD-10 vẫn 1.000.000\n"
     "- Bước 3: không có HD-10 (phiếu chi không được tính)"),

    ("003", "Quyết toán hợp đồng làm hiện doanh số tiêu chuẩn", "P0",
     KT + "; tiếp TC 001, HD-10 chưa quyết toán",
     "1. " + LOC_T10 + ", xem cột Doanh số tiêu chuẩn của HD-10\n"
     "2. Duyệt quyết toán HD-10 với doanh số tiêu chuẩn 50.000.000, NV-A hưởng 100%\n"
     "3. Lọc lại",
     "—",
     "- Bước 1: \"-\"\n"
     "- Bước 3: HD-10 và NV-A đều 50.000.000"),

    ("004", "Điều chỉnh giảm thưởng sau khi đã ghi nhận", "P1",
     KT + "; tiếp TC 001",
     "1. Kế toán lập phiếu kế toán điều chỉnh giảm thưởng năng suất tháng NV-A HD-10 300.000 ngày 31/10/2026\n"
     "2. " + LOC_T10,
     "—",
     "- HD-10 Năng suất tháng 700.000, dòng NV-A 700.000"),

    ("005", "Nhân viên mới thấy thưởng của mình", "P0",
     "NV-A không có quyền xem báo cáo; tiếp TC 001",
     "1. Đăng nhập NV-A, mở màn\n"
     "2. " + LOC_T10,
     "—",
     "- Có HD-10 với đúng số của NV-A; không thấy hợp đồng chỉ có thưởng của người khác"),

    ("006", "Trưởng phòng xem thưởng của phòng theo hợp đồng", "P0",
     "TP-1 có quyền theo phòng ban, phụ trách P1\n" + DATA,
     "1. Đăng nhập TP-1, " + LOC_T10.lower() + "\n"
     "2. Bấm In",
     "—",
     "- Màn và bản in có HD-01 (NV-A, NV-B), BH-02 (NV-C); dòng Tổng cộng 9.000.000"),
]
