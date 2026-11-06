# -*- coding: utf-8 -*-
"""Section I - IV cho man Ket chuyen chi phi phai tra."""
from tc_data_role import MENU, DATA, OPEN_KT1, NEW_KT1, HEAD

LIST = (DATA + "\nĐã có các phiếu của TPE:\n"
        "- KC-01: TPE.KCCPPT2026.00050, PKD1, đến 30/09/2026, 20.000.000, KT-1 tạo 05/10/2026\n"
        "- KC-02: TPE.KCCPPT2026.00051, PKD2, đến 30/09/2026, 8.000.000, KT-3 tạo 06/10/2026\n"
        "- KC-03: TPE.KCCPPT2026.00052, PKD1, đến 31/10/2026, 17.500.000, KT-1 tạo 05/11/2026")

SEC_I = [
    ("001", "Mở màn danh sách", "P0",
     LIST,
     "1. " + OPEN_KT1,
     "—",
     "- Tiêu đề \"Kết chuyển chi phí phải trả\"\n"
     "- Bảng có cột: STT, Số phiếu, Đến ngày, Ngày hạch toán, Phòng ban, Số tiền kết chuyển, Người tạo, "
     "Ngày tạo\n"
     "- Có nút \"Thêm mới\""),

    ("002", "Thứ tự mặc định mới nhất lên đầu", "P1",
     LIST,
     "1. " + OPEN_KT1,
     "—",
     "- Thứ tự: KC-03, KC-02, KC-01"),

    ("003", "Định dạng ngày và số tiền", "P1",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Xem dòng KC-03",
     "—",
     "- Đến ngày 31/10/2026, Ngày hạch toán 31/10/2026, Ngày tạo 05/11/2026\n"
     "- Số tiền kết chuyển 17,500,000"),

    ("004", "Số tiền kết chuyển âm hiển thị đúng dấu", "P2",
     DATA + "\nKC-04: PKD2, chỉ có vụ việc TVC âm 426.000",
     "1. " + OPEN_KT1,
     "—",
     "- Dòng KC-04 Số tiền kết chuyển -426,000"),

    ("005", "Bấm số phiếu mở chi tiết", "P0",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Bấm TPE.KCCPPT2026.00052",
     "—",
     "- Mở màn \"Chi tiết kết chuyển chi phí phải trả\" của KC-03"),

    ("006", "Phân trang và STT liên tục", "P2",
     "Có 25 phiếu trong phạm vi xem của KT-1",
     "1. " + OPEN_KT1 + "\n"
     "2. Sang trang 2",
     "—",
     "- STT trang 2 nối tiếp trang 1, tổng số bản ghi 25"),

    ("007", "Sắp xếp theo cột Số tiền kết chuyển", "P2",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Bấm tiêu đề cột Số tiền kết chuyển",
     "—",
     "- Bảng sắp theo số tiền: KC-02, KC-03, KC-01"),

    ("008", "Danh sách không có nút In, Xuất excel, Sửa, Xóa", "P2",
     LIST,
     "1. " + OPEN_KT1,
     "—",
     "- Không có nút In, Xuất excel\n"
     "- Không có thao tác Sửa / Xóa trên dòng"),
]

SEC_II = [
    ("001", "Lọc theo Số phiếu (một phần)", "P0",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Ô Số phiếu gõ \"00052\"",
     "—",
     "- Chỉ còn KC-03"),

    ("002", "Lọc theo Người lập", "P1",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Ô Người lập chọn KT-3",
     "—",
     "- Chỉ còn KC-02"),

    ("003", "Lọc theo Phòng ban", "P0",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Ô Phòng ban chọn PKD1",
     "—",
     "- Còn KC-01, KC-03"),

    ("004", "Lọc theo Từ ngày (ngày tạo)", "P1",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Chọn Từ ngày 06/10/2026",
     "—",
     "- Còn KC-02, KC-03"),

    ("005", "Lọc Đến ngày gồm cả phiếu tạo trong ngày cuối", "P1",
     LIST + "\nKC-02 tạo lúc 14:30 ngày 06/10/2026",
     "1. " + OPEN_KT1 + "\n"
     "2. Chọn Từ ngày 06/10/2026, Đến ngày 06/10/2026",
     "—",
     "- Mong đợi: có KC-02\n"
     "- Lưu ý: theo code hiện tại so với đầu ngày nên không ra KC-02 - ghi Failed"),

    ("006", "Lọc Số tiền từ / Số tiền đến", "P1",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Số tiền từ 10.000.000, Số tiền đến 18.000.000",
     "—",
     "- Mong đợi: chỉ còn KC-03\n"
     "- Lưu ý: theo code hiện tại ô này không có tác dụng, vẫn ra cả 3 phiếu - ghi Failed"),

    ("007", "Lọc theo Vụ việc", "P1",
     LIST + "\nKC-02 chỉ có dòng vụ việc TNSQ",
     "1. " + OPEN_KT1 + "\n"
     "2. Ô Vụ việc chọn TNSQ",
     "—",
     "- Mong đợi: chỉ còn KC-02\n"
     "- Lưu ý: theo code hiện tại ô này không có tác dụng - ghi Failed"),

    ("008", "Kết hợp nhiều điều kiện lọc", "P2",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Phòng ban PKD1, Người lập KT-1, Từ ngày 01/11/2026",
     "—",
     "- Chỉ còn KC-03"),

    ("009", "Không có kết quả phù hợp", "P2",
     LIST,
     "1. " + OPEN_KT1 + "\n"
     "2. Ô Số phiếu gõ \"ZZZ\"",
     "—",
     "- Bảng báo không có dữ liệu"),

    ("010", "Phòng đã ngừng hoạt động mất khỏi danh sách của quyền theo công ty", "P2",
     LIST + "\nPKD2 vừa chuyển trạng thái ngừng hoạt động",
     "1. " + OPEN_KT1,
     "—",
     "- Mong đợi: vẫn thấy KC-02 (phiếu đã ghi sổ)\n"
     "- Lưu ý: theo code hiện tại KC-02 không còn hiện (trừ khi KT-1 là người tạo) - ghi Failed nếu nghiệp "
     "vụ cần xem"),
]

SEC_III = [
    ("001", "Mở form tạo mới", "P0",
     DATA,
     "1. " + NEW_KT1,
     "—",
     "- Tiêu đề \"Tạo kết chuyển chi phí phải trả\"\n"
     "- Năm = 2026, Tính đến ngày trống, Ngày hạch toán trống và không sửa được\n"
     "- Bảng Chi tiết \"Không có dữ liệu\"\n"
     "- Có nút \"Lưu và duyệt\", \"Hủy\"\n"
     "- Không có ô Xuất hóa đơn"),

    ("002", "Danh sách Năm", "P2",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Mở ô Năm",
     "—",
     "- Có từ Năm 2025 đến Năm 2036\n"
     "- Không có Năm 2024"),

    ("003", "Ngày hạch toán tự theo Tính đến ngày", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Tính đến ngày 31/10/2026",
     "—",
     "- Ngày hạch toán tự hiện 31/10/2026"),

    ("004", "Ô Phòng ban chỉ có phòng công ty mình", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Mở ô Phòng ban",
     "—",
     "- Có PKD1, PKD2; không có PKD9"),

    ("005", "Thêm dòng khi chưa chọn Năm", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Bỏ chọn Năm, bấm dấu + ở bảng Chi tiết",
     "—",
     "- Cảnh báo \"Chưa chọn năm\", không thêm dòng"),

    ("006", "Thêm dòng khi chưa chọn Tính đến ngày", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Bấm dấu + ở bảng Chi tiết",
     "—",
     "- Cảnh báo \"Chưa chọn tính đến ngày\", không thêm dòng"),

    ("007", "Thêm dòng khi chưa chọn Phòng ban", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Tính đến ngày 31/10/2026, bấm dấu +",
     "—",
     "- Cảnh báo \"Chưa chọn phòng ban\", không thêm dòng"),

    ("008", "Thêm dòng khi đã chọn đủ thông tin chung", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + "\n"
     "3. Bấm dấu +",
     "—",
     "- Thêm dòng STT 1: Mã vụ việc trống, Tài khoản nợ 3351, Tài khoản có 33481, Số tiền trống\n"
     "- Dòng 1 không có nút xóa"),

    ("009", "Dòng thứ hai có nút xóa", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", bấm dấu + hai lần\n"
     "3. Bấm nút xóa ở dòng 2",
     "—",
     "- Dòng 2 có nút xóa, bấm thì dòng 2 biến mất, còn dòng 1"),

    ("010", "Đổi Phòng ban xóa hết chi tiết", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD (18.000.000)\n"
     "3. Đổi Phòng ban sang PKD2",
     "—",
     "- Bảng Chi tiết về \"Không có dữ liệu\""),

    ("011", "Đổi Tính đến ngày xóa hết chi tiết", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD\n"
     "3. Đổi Tính đến ngày sang 30/09/2026",
     "—",
     "- Bảng Chi tiết về \"Không có dữ liệu\"\n"
     "- Ngày hạch toán đổi thành 30/09/2026"),

    ("012", "Đổi Năm xóa hết chi tiết", "P2",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD\n"
     "3. Đổi Năm sang 2025",
     "—",
     "- Bảng Chi tiết về \"Không có dữ liệu\""),

    ("013", "Bấm Hủy quay lại danh sách", "P2",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", bấm \"Hủy\"",
     "—",
     "- Về màn danh sách, không có phiếu mới"),

    ("014", "Nhãn ô ngày ở form", "P2",
     DATA,
     "1. " + NEW_KT1,
     "—",
     "- Mong đợi: nhãn \"Tính đến ngày\"\n"
     "- Lưu ý: theo code hiện tại ghi \"Tình đến ngày\" - ghi Failed"),
]

SEC_IV = [
    ("001", "Chọn vụ việc TTHHD tính đúng số tiền", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", bấm dấu +\n"
     "3. Mã vụ việc chọn TTHHD",
     "—",
     "- Thông báo \"Thêm thành công\"\n"
     "- Số tiền 18,000,000 (HĐ-01 10.000.000 + HĐ-02 5.000.000 + HĐ-03 3.000.000)"),

    ("002", "Không tính bút toán sau Tính đến ngày", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Số tiền 18,000,000, không gồm 2.000.000 của HĐ-01 ngày 03/11/2026"),

    ("003", "Tính đến ngày lùi lại thì số tiền giảm theo", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Năm 2026, Tính đến ngày 30/09/2026, Phòng ban PKD1, thêm dòng TTHHD",
     "—",
     "- Số tiền 10,000,000 (chỉ HĐ-01 ngày 15/09/2026)"),

    ("004", "Không tính bút toán của năm khác", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Không gồm 7.000.000 của HĐ-05 ngày 20/12/2025"),

    ("005", "Không tính hợp đồng không xuất hóa đơn", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Không gồm 1.000.000 của HĐ-06"),

    ("006", "Không tính nhân viên phòng khác", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Không gồm 9.000.000 của HĐ-07 (NV-K3, PKD2)"),

    ("007", "Chọn PKD2 thì ra số của PKD2", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Năm 2026, Tính đến ngày 31/10/2026, Phòng ban PKD2, thêm dòng TTHHD",
     "—",
     "- Số tiền 9,000,000"),

    ("008", "Vụ việc có số dư Nợ ra số âm", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TVC",
     "—",
     "- Số tiền -500,000"),

    ("009", "Vụ việc không có số dư ra 0", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TNSQ",
     "—",
     "- Số tiền 0"),

    ("010", "Phần đã kết chuyển kỳ trước được trừ", "P0",
     DATA + "\nĐã có KC-01: PKD1, đến 30/09/2026, TTHHD 10.000.000, bút toán đã ghi",
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Số tiền 8,000,000 (18.000.000 trừ 10.000.000 đã kết chuyển)"),

    ("011", "Chọn trùng vụ việc ở dòng thứ hai", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", dòng 1 chọn TTHHD\n"
     "3. Bấm dấu +, dòng 2 cũng chọn TTHHD",
     "—",
     "- Cảnh báo \"Vụ việc đã được chọn!\"\n"
     "- Dòng 2 không có Số tiền"),

    ("012", "Danh sách vụ việc chỉ gồm vụ việc đang dùng", "P2",
     DATA + "\nVụ việc cũ X1 đã ngừng sử dụng",
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", bấm dấu +, mở ô Mã vụ việc",
     "—",
     "- Không có X1; có TTHHD, TNSQ, TVC..."),

    ("013", "Đổi vụ việc trên cùng dòng thì tính lại", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", dòng 1 chọn TTHHD\n"
     "3. Đổi dòng 1 sang TVC",
     "—",
     "- Số tiền đổi từ 18,000,000 thành -500,000"),

    ("014", "Bút toán thiếu nhân viên hoặc thiếu hợp đồng không được tính", "P1",
     DATA + "\nThêm bút toán Có 3351 TTHHD 600.000 ngày 01/10/2026 của PKD1 nhưng không gắn hợp đồng",
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Số tiền vẫn 18,000,000"),
]
