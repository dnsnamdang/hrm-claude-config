# -*- coding: utf-8 -*-
"""Section I - X cho man Bao cao hang gui."""
from tc_data_role import MENU, DATA, KT, LOC_T11, LOC_T10

SEC_I = [
    ("001", "Bố cục mặc định của màn", "P0",
     KT,
     "1. " + MENU + "\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Tiêu đề \"BÁO CÁO HÀNG GỬI\"\n"
     "- Bộ lọc: Phòng ban, Nhân viên, Khách hàng, Hàng hóa, Kho, Từ ngày (bắt buộc), Đến ngày (bắt buộc)\n"
     "- Nút Lọc, làm mới, In, Xuất excel\n"
     "- Khu Chi tiết ghi \"Chưa có dữ liệu\", chưa tự lọc"),

    ("002", "Cột của bảng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11,
     "—",
     "- Cột: STT, Tên hàng hóa, Mã hàng, ĐVT, SL còn đầu kì, SL gửi, SL đã xuất, SL còn"),

    ("003", "Biểu tượng đang tải", "P2",
     KT,
     "1. " + LOC_T11 + ", quan sát ngay",
     "—",
     "- Bảng hiện \"Đang tải dữ liệu\"; nút Lọc mờ đến khi xong"),

    ("004", "Khoảng ngày không có hàng gửi nào", "P1",
     KT + "; chưa có hàng gửi nào trước 01/01/2025",
     "1. Chọn Từ ngày 01/01/2024, Đến ngày 31/12/2024, bấm Lọc",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\""),
]


SEC_II = [
    ("001", "Thiếu Từ ngày / Đến ngày", "P0",
     KT,
     "1. Để trống Từ ngày, Đến ngày, bấm Lọc",
     "—",
     "- Thông báo \"Chưa chọn đủ điều kiện bắt buộc\"\n"
     "- Dưới 2 ô ghi \"Bắt buộc chọn\"; bảng không đổi"),

    ("002", "Thiếu một trong hai ô ngày", "P1",
     KT,
     "1. Chỉ chọn Từ ngày 01/11/2026, bấm Lọc",
     "—",
     "- Dưới ô Đến ngày ghi \"Bắt buộc chọn\", không lọc"),

    ("003", "Từ ngày sau Đến ngày", "P2",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 30/11/2026, Đến ngày 01/11/2026, bấm Lọc",
     "—",
     "- Mong đợi: báo Từ ngày không được sau Đến ngày\n"
     "- Lưu ý: theo code hiện tại vẫn lọc, SL gửi / SL đã xuất bằng 0 - ghi Failed"),

    ("004", "Lọc theo Nhân viên", "P0",
     KT + "\n" + DATA,
     "1. Ô Nhân viên chọn NV-C\n"
     "2. " + LOC_T11,
     "—",
     "- Chỉ có PKD2 > NV-C > KH-02 > H1: đầu kì 5, gửi 0, xuất 0, còn 5"),

    ("005", "Lọc theo Phòng ban", "P0",
     KT + "\n" + DATA,
     "1. Ô Phòng ban chọn PKD1\n"
     "2. " + LOC_T11,
     "—",
     "- Chỉ có PKD1 > NV-A; không có PKD2"),

    ("006", "Lọc theo Khách hàng", "P0",
     KT + "\n" + DATA,
     "1. Ô Khách hàng chọn KH-02\n"
     "2. " + LOC_T11,
     "—",
     "- Chỉ có nhánh NV-C > KH-02 > H1: đầu kì 5, còn 5\n"
     "- Không có KH-01"),

    ("007", "Lọc theo Hàng hóa", "P0",
     KT + "\n" + DATA,
     "1. Bấm kính lúp ở ô Hàng hóa, chọn H1\n"
     "2. " + LOC_T11,
     "—",
     "- Ô Hàng hóa hiện tên H1\n"
     "- Chỉ có các dòng hàng H1 (NV-A / KH-01, NV-C / KH-02)"),

    ("008", "Lọc theo Kho tách số theo kho", "P0",
     KT + "\n" + DATA,
     "1. Ô Kho chọn K1\n"
     "2. " + LOC_T11 + "\n"
     "3. Đổi Kho sang K2, bấm Lọc",
     "—",
     "- Bước 2: NV-A / KH-01 / H1 = đầu kì 18, gửi 0, xuất 6, còn 12\n"
     "- Bước 3: NV-A / KH-01 / H1 = đầu kì 0, gửi 12, xuất 0, còn 12"),

    ("009", "Không lọc Kho thì cộng gộp các kho", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11,
     "—",
     "- NV-A / KH-01 / H1 chỉ 1 dòng: đầu kì 18, gửi 12, xuất 6, còn 24"),

    ("010", "Chọn Công ty lọc lại danh sách Kho", "P1",
     "TGĐ quyền Tổng công ty; TPE có K1, K2; TPC có K5",
     "1. Ô Công ty chọn TPC, mở ô Kho",
     "—",
     "- Ô Kho chỉ còn K5"),

    ("011", "Nút làm mới", "P1",
     KT + "; đã chọn PKD1, NV-A, KH-01, H1, K1, kỳ 01/11 - 30/11/2026 và đã Lọc",
     "1. Bấm nút làm mới",
     "—",
     "- Mọi ô lọc về trống, kể cả Từ ngày, Đến ngày\n"
     "- Bảng giữ kết quả cũ đến khi bấm Lọc lần nữa"),

    ("012", "Kết hợp nhiều điều kiện", "P1",
     KT + "\n" + DATA,
     "1. Chọn NV-A, KH-01, H1, Kho K2\n"
     "2. " + LOC_T11,
     "—",
     "- Đúng 1 dòng H1: đầu kì 0, gửi 12, xuất 0, còn 12"),
]


SEC_III = [
    ("001", "Số liệu kỳ hiện tại", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11,
     "—",
     "- NV-A / KH-01 / H1: đầu kì 18, gửi 12, đã xuất 6, còn 24\n"
     "- NV-C / KH-02 / H1: đầu kì 5, gửi 0, đã xuất 0, còn 5\n"
     "- Không có NV-A / KH-02 / H2 (đã xuất hết trước kỳ)"),

    ("002", "SL còn = đầu kì + gửi - đã xuất", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Tính lại cột SL còn từng dòng",
     "—",
     "- Mọi dòng: SL còn bằng SL còn đầu kì cộng SL gửi trừ SL đã xuất\n"
     "- Ví dụ NV-A / KH-01 / H1: 18 cộng 12 trừ 6 bằng 24"),

    ("003", "Kỳ tháng 10", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- NV-A / KH-01 / H1: đầu kì 0, gửi 24, xuất 6, còn 18\n"
     "- NV-C / KH-02 / H1: gửi 5, còn 5\n"
     "- Mong đợi: có NV-A / KH-02 / H2 gửi 10, xuất 10, còn 0\n"
     "- Lưu ý: theo code hiện tại không có dòng H2 vì hiện tại H2 đã hết - ghi Failed"),

    ("004", "Kỳ trong quá khứ, hàng đã xuất hết sau kỳ", "P0",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 01/10/2026, Đến ngày 10/10/2026, bấm Lọc",
     "—",
     "- Mong đợi: NV-A / KH-01 / H1 gửi 24, còn 24; NV-A / KH-02 / H2 gửi 10, còn 10\n"
     "- Lưu ý: theo code hiện tại thiếu dòng H2 (bị ẩn vì hiện đã xuất hết) - ghi Failed"),

    ("005", "Hàng gửi sau kỳ hiện thành dòng toàn số 0", "P1",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 01/10/2026, Đến ngày 10/10/2026, bấm Lọc\n"
     "2. Tìm nhánh NV-C",
     "—",
     "- Mong đợi: không có NV-C (gửi ngày 15/10, sau kỳ)\n"
     "- Lưu ý: theo code hiện tại có NV-C / KH-02 / H1 với cả 4 cột bằng 0 - ghi Failed"),

    ("006", "Kỳ trước mọi phát sinh", "P1",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 01/09/2026, Đến ngày 30/09/2026, bấm Lọc",
     "—",
     "- Mong đợi: \"Chưa có dữ liệu\"\n"
     "- Lưu ý: theo code hiện tại hiện các dòng NV-A / KH-01 / H1, NV-C / KH-02 / H1 toàn số 0 - ghi "
     "Failed"),

    ("007", "Phiếu đúng ngày Từ ngày được tính vào SL gửi", "P0",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 03/11/2026, Đến ngày 30/11/2026, bấm Lọc",
     "—",
     "- NV-A / KH-01 / H1: đầu kì 18, gửi 12 (PNH-02 ngày 03/11), xuất 6, còn 24"),

    ("008", "Phiếu đúng ngày Đến ngày được tính", "P0",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 01/11/2026, Đến ngày 10/11/2026, bấm Lọc",
     "—",
     "- NV-A / KH-01 / H1: SL đã xuất 6 (PXH-02 ngày 10/11, tính trọn ngày), còn 24"),

    ("009", "Phiếu ngay trước Từ ngày vào SL còn đầu kì", "P0",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 13/10/2026, Đến ngày 31/10/2026, bấm Lọc",
     "—",
     "- NV-A / KH-01 / H1: đầu kì 18 (24 gửi ngày 05/10 trừ 6 xuất ngày 12/10), gửi 0, xuất 0, còn 18"),

    ("010", "Phiếu nhập gửi chưa hoàn thành chưa được tính", "P0",
     KT + "\n" + DATA + "\n"
     "PNH-05 (nhập gửi H1 = 3 cho KH-01 của NV-A) đang chờ, chưa hoàn thành",
     "1. " + LOC_T11,
     "—",
     "- NV-A / KH-01 / H1 vẫn gửi 12, còn 24 (không cộng 3)"),
]


SEC_IV = [
    ("001", "Phân cấp Phòng > Nhân viên > Khách hàng > Hàng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11,
     "—",
     "- Dòng phòng in đậm, STT 1, 2\n"
     "- Dòng nhân viên STT 1.1, khách hàng STT 1.1.1 dạng \"KH-01 - <tên khách>\", hàng STT 1.1.1.1\n"
     "- Dòng phòng, nhân viên, khách hàng để trống các cột số"),

    ("002", "Nhân viên gửi cho 2 khách", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T10,
     "—",
     "- Mong đợi: dưới NV-A có 2 nhánh riêng KH-01 (H1) và KH-02 (H2)\n"
     "- Lưu ý: theo code hiện tại chỉ có KH-01 vì H2 đã xuất hết (xem TC III.003) - ghi Failed"),

    ("003", "Nhân viên chuyển phòng", "P1",
     KT + "\n" + DATA + "\n"
     "NV-A vừa chuyển từ PKD1 sang PKD2",
     "1. " + LOC_T10,
     "—",
     "- Hàng gửi của NV-A (cả tháng 10) nằm dưới PKD2\n"
     "- Lưu ý: báo cáo xếp theo phòng HIỆN TẠI của nhân viên; ghi Failed nếu nghiệp vụ muốn theo phòng lúc "
     "gửi"),

    ("004", "Đổi ĐVT sang Thùng", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Dòng NV-A / KH-01 / H1 đổi ĐVT sang Thùng",
     "—",
     "- Đầu kì 1.5, gửi 1, đã xuất 0.5, còn 2\n"
     "- Các dòng khác không đổi"),

    ("005", "Đổi ĐVT ra số lẻ dài", "P2",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Dòng NV-C / KH-02 / H1 đổi ĐVT sang Thùng",
     "—",
     "- Mong đợi: đầu kì, còn hiện khoảng 0.42 (làm tròn hợp lý)\n"
     "- Lưu ý: nếu hiện chuỗi số lẻ dài 0.41666666... thì ghi Failed"),

    ("006", "Đổi ĐVT về Cái", "P1",
     KT + "\n" + DATA,
     "1. Làm TC IV.004, rồi đổi lại ĐVT Cái",
     "—",
     "- Trở về đầu kì 18, gửi 12, xuất 6, còn 24"),

    ("007", "Đổi ĐVT mất khi lọc lại", "P2",
     KT + "\n" + DATA,
     "1. Làm TC IV.004, bấm Lọc lại",
     "—",
     "- Dòng H1 trở về ĐVT Cái và số theo Cái"),
]


SEC_V = [
    ("001", "Mở cửa sổ chi tiết từ SL gửi", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Bấm số 12 ở cột SL gửi dòng NV-A / KH-01 / H1",
     "—",
     "- Mở cửa sổ \"Chi tiết hàng gửi nhân viên <mã NV-A> - <tên NV-A>\"\n"
     "- Ô Hàng hóa \"<tên H1> - <mã H1>\", ô Khách hàng \"KH-01 - <tên>\" (không sửa được)\n"
     "- Có ô lọc Phiếu yêu cầu, Phiếu hạch toán, Kho; nút Lọc, In"),

    ("002", "Các dòng phiếu trong kỳ", "P0",
     KT + "\n" + DATA,
     "1. Làm TC V.001, quan sát bảng",
     "—",
     "- Dòng 1: PYCNH-02 / PNH-02, ngày 03/11/2026, kho K2, SL gửi 12, SL xuất 0, SL còn 12\n"
     "- Dòng 2: PYCXH-02 / PXH-02, ngày 10/11/2026, kho K1, SL gửi 0, SL xuất 6, SL còn 12\n"
     "- Cột SL còn đầu kì từng dòng để trống"),

    ("003", "Dòng Tổng cộng của cửa sổ", "P0",
     KT + "\n" + DATA,
     "1. Làm TC V.001, xem dòng Tổng cộng",
     "—",
     "- SL còn đầu kì 18, SL gửi 12, SL xuất 6, SL còn 24 (khớp dòng ở bảng chính)"),

    ("004", "Phiếu đúng ngày Đến ngày có trong cửa sổ", "P0",
     KT + "\n" + DATA,
     "1. Chọn Từ ngày 01/11/2026, Đến ngày 10/11/2026, bấm Lọc\n"
     "2. Bấm SL gửi dòng NV-A / KH-01 / H1",
     "—",
     "- Mong đợi: có cả PXH-02 ngày 10/11; Tổng cộng SL xuất 6, SL còn 24 như bảng chính\n"
     "- Lưu ý: theo code hiện tại thiếu PXH-02 (không tính phiếu của ngày Đến ngày), Tổng cộng SL xuất 0, "
     "SL còn 30 - ghi Failed"),

    ("005", "Bấm mã phiếu mở phiếu gốc", "P1",
     KT + "\n" + DATA,
     "1. Làm TC V.001\n"
     "2. Bấm PYCNH-02, rồi PNH-02, rồi PYCXH-02, rồi PXH-02",
     "—",
     "- Mỗi mã mở tab mới đúng màn chi tiết: phiếu yêu cầu nhập hàng, phiếu nhập hàng, phiếu yêu cầu xuất "
     "hàng, phiếu xuất hàng"),

    ("006", "Lọc theo Phiếu yêu cầu, Phiếu hạch toán", "P1",
     KT + "\n" + DATA,
     "1. Làm TC V.001\n"
     "2. Ô Phiếu yêu cầu gõ \"YCX\", bấm Lọc\n"
     "3. Xóa ô đó, ô Phiếu hạch toán gõ \"PNH-02\", bấm Lọc",
     "—",
     "- Bước 2: chỉ còn dòng PYCXH-02 / PXH-02\n"
     "- Bước 3: chỉ còn dòng PNH-02"),

    ("007", "Lọc theo Kho trong cửa sổ", "P1",
     KT + "\n" + DATA,
     "1. Làm TC V.001\n"
     "2. Ô Kho chọn K2, bấm Lọc",
     "—",
     "- Chỉ còn dòng PNH-02 ở K2\n"
     "- Tổng cộng SL gửi 12, SL xuất 0"),

    ("008", "Ô lọc cửa sổ giữ lại khi mở hàng khác", "P2",
     KT + "\n" + DATA,
     "1. Làm TC V.006 bước 3 (ô Phiếu hạch toán = PNH-02), đóng cửa sổ\n"
     "2. Bấm SL gửi dòng NV-C / KH-02 / H1",
     "—",
     "- Mong đợi: các ô lọc của cửa sổ về trống\n"
     "- Lưu ý: theo code hiện tại ô Phiếu hạch toán vẫn là PNH-02 nên bảng trống - ghi Failed"),

    ("009", "Cửa sổ khi đã đổi ĐVT", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Đổi ĐVT dòng NV-A / KH-01 / H1 sang Thùng, bấm SL gửi (1)",
     "—",
     "- Các dòng: PNH-02 gửi 1, còn 1; PXH-02 xuất 0.5, còn 1\n"
     "- Mong đợi: Tổng cộng đầu kì 1.5, gửi 1, xuất 0.5, còn 2\n"
     "- Lưu ý: theo code hiện tại Tổng cộng SL gửi 12, SL xuất 6 (vẫn theo Cái) - ghi Failed"),

    ("010", "Phân trang cửa sổ và STT", "P2",
     KT + "; NV-A / KH-01 / H1 có 13 phiếu trong kỳ; bảng chính đang ở trang 2",
     "1. Ở trang 2 bảng chính, bấm SL gửi dòng NV-A / KH-01 / H1\n"
     "2. Sang trang 2 của cửa sổ",
     "—",
     "- Mong đợi: trang 1 STT 1 đến 10, trang 2 STT 11 đến 13\n"
     "- Lưu ý: theo code hiện tại STT lấy theo trang của bảng chính (trang 1 cửa sổ bắt đầu từ 11) - ghi "
     "Failed"),

    ("011", "In từ cửa sổ chi tiết", "P1",
     KT + "\n" + DATA,
     "1. Làm TC V.001, bấm In",
     "—",
     "- Tab mới mẫu in ngang, có tên nhân viên \"<mã> - <tên NV-A>\"\n"
     "- Bảng có 2 dòng PNH-02, PXH-02 và dòng Tổng cộng 18 / 12 / 6 / 24"),

    ("012", "Cửa sổ khi chưa có phiếu trong kỳ", "P1",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Bấm số 0 ở SL gửi dòng NV-C / KH-02 / H1",
     "—",
     "- Bảng ghi \"Chưa có dữ liệu\"\n"
     "- Tổng cộng: đầu kì 5, gửi 0, xuất 0, còn 5"),
]


SEC_VI = [
    ("001", "Mỗi trang 10 phòng ban", "P1",
     KT + "; có hàng gửi ở 12 phòng ban",
     "1. Lọc kỳ có đủ 12 phòng",
     "—",
     "- Trang 1 có 10 phòng ban, trang 2 có 2 phòng\n"
     "- Số trang tính theo phòng ban, không theo số dòng hàng"),

    ("002", "STT phòng ban ở trang 2", "P2",
     KT + "; có hàng gửi ở 12 phòng ban",
     "1. Lọc, sang trang 2",
     "—",
     "- Mong đợi: phòng đầu trang 2 có STT 11\n"
     "- Lưu ý: theo code hiện tại STT bắt đầu lại từ 1 - ghi Failed"),

    ("003", "Đổi trang giữ bộ lọc", "P1",
     KT + "; đang lọc theo khách KH-01, kết quả có 2 trang",
     "1. Sang trang 2",
     "—",
     "- Trang 2 vẫn chỉ có khách KH-01, cùng khoảng ngày"),
]


SEC_VII = [
    ("001", "In báo cáo", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Bấm In",
     "—",
     "- Tab mới mẫu in ngang, có tiêu đề công ty\n"
     "- Bảng STT, Tên hàng, Mã hàng, ĐVT, SL còn đầu kì, SL gửi, SL xuất, SL còn; cùng phân cấp và số như "
     "màn (18 / 12 / 6 / 24)"),

    ("002", "Xuất excel", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file bao_cao_hang_gui.xlsx, tiêu đề \"Báo cáo hàng gửi\"\n"
     "- Số liệu giống bản In"),

    ("003", "In / Excel lấy đủ mọi trang", "P0",
     KT + "; có hàng gửi ở 12 phòng ban",
     "1. Lọc, đang ở trang 1, bấm In",
     "—",
     "- Bản in có đủ 12 phòng ban"),

    ("004", "In / Excel theo bộ lọc đang chọn", "P0",
     KT + "\n" + DATA,
     "1. Chọn Nhân viên NV-C, kỳ 01/11 - 30/11/2026\n"
     "2. Bấm In, rồi Xuất excel",
     "—",
     "- Chỉ có NV-C / KH-02 / H1 đầu kì 5, còn 5"),

    ("005", "In khi chưa chọn ngày", "P1",
     KT,
     "1. Để trống Từ ngày, Đến ngày, bấm In",
     "—",
     "- Mong đợi: báo cần chọn Từ ngày, Đến ngày\n"
     "- Lưu ý: theo code hiện tại tab mới ra trang lỗi hệ thống - ghi Failed"),

    ("006", "Xuất excel khi chưa chọn ngày", "P1",
     KT,
     "1. Để trống Từ ngày, Đến ngày, bấm Xuất excel",
     "—",
     "- Mong đợi: báo cần chọn ngày\n"
     "- Lưu ý: theo code hiện tại ra trang lỗi hệ thống, không có file - ghi Failed"),

    ("007", "In không theo ĐVT đang chọn", "P2",
     KT + "\n" + DATA,
     "1. Làm TC IV.004 (H1 đang hiện Thùng), bấm In",
     "—",
     "- Bản in H1 theo Cái: 18 / 12 / 6 / 24\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu in theo ĐVT đang chọn"),

    ("008", "In khi chưa bấm Lọc", "P2",
     KT + "\n" + DATA,
     "1. Chọn kỳ 01/11 - 30/11/2026 nhưng không bấm Lọc, bấm In",
     "—",
     "- Bản in vẫn theo các ô lọc đang chọn (có NV-A, NV-C)"),

    ("009", "In với hàng có tên chứa ký tự &", "P2",
     KT + "; khách KH-03 tên \"A & B\" có hàng gửi",
     "1. Lọc kỳ có KH-03, bấm In",
     "—",
     "- Tên khách hiện đúng \"A & B\", bản in không vỡ bố cục"),
]


SEC_VIII = [
    ("001", "Phiếu nhập gửi hoàn thành làm tăng hàng gửi", "P0",
     KT + "\n" + DATA,
     "1. NV-A lập phiếu yêu cầu nhập hàng loại gửi cho KH-01, H1 = 2, kho K1\n"
     "2. Thủ kho, kế toán hoàn thành phiếu nhập hàng tương ứng hôm nay\n"
     "3. Mở báo cáo, " + LOC_T11,
     "—",
     "- NV-A / KH-01 / H1: SL gửi 14, còn 26\n"
     "- Cửa sổ chi tiết có thêm dòng phiếu nhập mới"),

    ("002", "Hàng gửi ghi cho người lập phiếu yêu cầu", "P0",
     KT + "\n" + DATA,
     "1. NV-B lập phiếu yêu cầu nhập hàng gửi cho KH-01, H1 = 2; NV-A không liên quan\n"
     "2. Hoàn thành phiếu nhập hàng, mở báo cáo kỳ tháng 11",
     "—",
     "- Có nhánh mới NV-B > KH-01 > H1 gửi 2\n"
     "- Dòng NV-A / KH-01 / H1 không đổi"),

    ("003", "Phiếu xuất hàng xuất từ hàng gửi làm giảm", "P0",
     KT + "\n" + DATA,
     "1. NV-A lập phiếu yêu cầu xuất hàng cho KH-01, H1 = 4, chọn xuất từ hàng gửi, kho K1\n"
     "2. Kế toán hạch toán phiếu xuất hàng hôm nay\n"
     "3. Mở báo cáo, " + LOC_T11,
     "—",
     "- NV-A / KH-01 / H1: SL đã xuất 10, còn 20"),

    ("004", "Xuất hàng thường không trừ hàng gửi", "P0",
     KT + "\n" + DATA,
     "1. NV-A xuất H1 = 4 cho KH-01 nhưng KHÔNG chọn xuất từ hàng gửi, hạch toán xong\n"
     "2. Mở báo cáo kỳ tháng 11",
     "—",
     "- NV-A / KH-01 / H1 vẫn xuất 6, còn 24"),

    ("005", "Xuất vượt hàng gửi bị chặn", "P0",
     KT + "\n" + DATA + "\n"
     "Hiện K1 còn 12 H1 gửi của NV-A / KH-01",
     "1. Hạch toán phiếu xuất hàng xuất từ hàng gửi H1 = 15 tại K1",
     "—",
     "- Thông báo \"Xuất nhiều hơn tồn hold.\", phiếu không hạch toán\n"
     "- Báo cáo không đổi"),

    ("006", "Xuất từ hàng gửi sai kho không trừ kho khác", "P1",
     KT + "\n" + DATA,
     "1. NV-A xuất từ hàng gửi H1 = 12 tại K2, hạch toán xong\n"
     "2. Lọc kỳ tháng 11, lần lượt chọn Kho K1, K2",
     "—",
     "- Lọc K1: NV-A / KH-01 / H1 vẫn còn 12\n"
     "- Lọc K2: không còn dòng NV-A / KH-01 / H1 (K2 đã hết)\n"
     "- Không lọc Kho: đầu kì 18, gửi 12, xuất 18, còn 12"),
]


SEC_IX = [
    ("001", "Đối chiếu bảng chính với cửa sổ chi tiết", "P0",
     KT + "\n" + DATA,
     "1. " + LOC_T11 + "\n"
     "2. Với từng dòng hàng, mở cửa sổ chi tiết, so dòng Tổng cộng",
     "—",
     "- Tổng cộng SL gửi, SL xuất, SL còn của cửa sổ bằng số ở bảng chính\n"
     "- Lưu ý: nếu lệch do phiếu ngày Đến ngày, xem TC V.004"),

    ("002", "Đối chiếu SL còn với kỳ kế tiếp", "P0",
     KT + "\n" + DATA,
     "1. Lọc kỳ 01/10 - 31/10/2026, ghi SL còn NV-A / KH-01 / H1\n"
     "2. Lọc kỳ 01/11 - 30/11/2026, xem SL còn đầu kì cùng dòng",
     "—",
     "- SL còn tháng 10 (18) bằng SL còn đầu kì tháng 11 (18)"),

    ("003", "Phát sinh mới khi đang xem", "P1",
     KT + "\n" + DATA,
     "1. Lọc kỳ tháng 11\n"
     "2. Người khác hạch toán phiếu xuất từ hàng gửi H1 = 2 cho KH-01\n"
     "3. Không bấm gì, rồi bấm Lọc lại",
     "—",
     "- Bước 3 trước khi Lọc: số cũ\n"
     "- Sau khi Lọc: SL đã xuất 8, còn 22"),

    ("004", "Ngày nhập ký tự lạ khi gọi thẳng chức năng", "P0",
     KT,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy dữ liệu báo cáo, ô Từ ngày là \"2026-11-01\" "
     "kèm dấu nháy đơn và một đoạn chữ phía sau",
     "—",
     "- Mong đợi: bị từ chối, báo ngày không hợp lệ\n"
     "- Lưu ý: theo code hiện tại đoạn chữ được đưa thẳng vào câu tra cứu dữ liệu và vẫn chạy - ghi Failed "
     "(lỗi an toàn dữ liệu)"),

    ("005", "Gọi thẳng chức năng lọc thiếu ngày", "P2",
     KT,
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy dữ liệu báo cáo không gửi Từ ngày, Đến ngày",
     "—",
     "- Mong đợi: báo thiếu ngày\n"
     "- Lưu ý: ghi Failed nếu trả về dữ liệu với số liệu lạ"),
]


SEC_X = [
    ("001", "Vòng đời một lô hàng gửi", "P0",
     KT + "; khách KH-05 chưa có hàng gửi",
     "1. NV-A lập yêu cầu nhập hàng gửi H1 = 10 cho KH-05 tại K1, hoàn thành phiếu nhập\n"
     "2. Báo cáo kỳ tháng 11: kiểm tra\n"
     "3. NV-A xuất từ hàng gửi 4, hạch toán; kiểm tra\n"
     "4. NV-A xuất nốt 6, hạch toán; kiểm tra",
     "—",
     "- Bước 2: NV-A / KH-05 / H1 gửi 10, còn 10\n"
     "- Bước 3: xuất 4, còn 6\n"
     "- Bước 4 (mong đợi): gửi 10, xuất 10, còn 0\n"
     "- Lưu ý: theo code hiện tại bước 4 dòng KH-05 biến mất khỏi kỳ tháng 11 - ghi Failed"),

    ("002", "Người không quyền và kế toán xem cùng lô", "P0",
     KT + "\n" + DATA,
     "1. NV-A (không quyền) lọc kỳ tháng 11\n"
     "2. KT-1 lọc cùng kỳ, chọn Nhân viên NV-A",
     "—",
     "- 2 bảng giống nhau: NV-A / KH-01 / H1 đầu kì 18, gửi 12, xuất 6, còn 24"),

    ("003", "Báo cáo, cửa sổ chi tiết, bản in khớp nhau", "P0",
     KT + "\n" + DATA,
     "1. Lọc kỳ 01/11 - 30/11/2026\n"
     "2. Mở cửa sổ chi tiết NV-A / KH-01 / H1, bấm In trong cửa sổ\n"
     "3. Bấm In và Xuất excel ở màn chính",
     "—",
     "- Cùng số 18 / 12 / 6 / 24 ở màn, cửa sổ, bản in cửa sổ, bản in và file excel"),
]
