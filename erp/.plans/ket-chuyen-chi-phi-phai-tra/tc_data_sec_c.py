# -*- coding: utf-8 -*-
"""Section VIII - X cho man Ket chuyen chi phi phai tra."""
from tc_data_role import MENU, DATA, OPEN_KT1, NEW_KT1, HEAD

SAVE = "bấm \"Lưu và duyệt\""

SEC_VIII = [
    ("001", "Sửa phiếu đã lưu qua đường dẫn", "P1",
     DATA + "\nKC-03 đã lưu",
     "1. Đăng nhập KT-1\n"
     "2. Dán đường dẫn sửa của KC-03",
     "—",
     "- Mong đợi: có cách điều chỉnh phiếu (hoặc báo rõ không cho sửa)\n"
     "- Lưu ý: theo code hiện tại đường dẫn không có chức năng xử lý, ra trang lỗi - ghi Failed"),

    ("002", "Xóa phiếu lập sai", "P0",
     DATA + "\nKT-1 lập nhầm KC-05 cho PKD2 thay vì PKD1, bút toán đã ghi",
     "1. Đăng nhập KT-1\n"
     "2. Tìm cách xóa KC-05 (danh sách, chi tiết, đường dẫn xóa)",
     "—",
     "- Mong đợi: xóa được phiếu và các bút toán của phiếu, số dư 3351 của PKD2 trở lại như trước\n"
     "- Lưu ý: theo code hiện tại không có nút xóa, đường dẫn xóa ra trang lỗi; phiếu lập sai không gỡ "
     "được - ghi Failed"),

    ("003", "Lập sai Tính đến ngày thì chỉ kết chuyển bổ sung được", "P1",
     DATA + "\nKT-1 lập nhầm KC-06: PKD1, đến 30/09/2026 (đúng ra 31/10/2026), TTHHD 10.000.000",
     "1. KT-1 lập phiếu mới PKD1, đến 31/10/2026, dòng TTHHD",
     "—",
     "- Số tiền 8,000,000 (phần còn lại)\n"
     "- Lưu thành công; tổng hai phiếu bằng 18.000.000"),

    ("004", "Kết chuyển vào kỳ đã khóa sổ", "P1",
     DATA + "\nKế toán đã chốt số liệu hết tháng 09/2026",
     "1. KT-1 lập phiếu Năm 2026, Tính đến ngày 31/08/2026, PKD1, dòng TTHHD có số tiền khác 0\n"
     "2. " + SAVE,
     "—",
     "- Mong đợi theo nghiệp vụ: chặn ghi sổ vào kỳ đã chốt\n"
     "- Lưu ý: theo code hiện tại không có kiểm tra kỳ, phiếu lưu được với Ngày hạch toán 31/08/2026 - "
     "để nghiệp vụ quyết"),

    ("005", "Kết chuyển hợp đồng không xuất hóa đơn", "P2",
     DATA,
     "1. KT-1 cần kết chuyển 1.000.000 của HĐ-06 (không xuất hóa đơn) sang 33483",
     "—",
     "- Mong đợi theo nghiệp vụ: có cách kết chuyển 1.000.000 của HĐ-06 sang 33483\n"
     "- Lưu ý: theo code hiện tại form không có ô Xuất hóa đơn, phiếu luôn lưu là Có nên không kết chuyển "
     "được HĐ-06 - để nghiệp vụ quyết"),
]

SEC_IX = [
    ("001", "Lưu lại form mở từ trước sau khi đã kết chuyển", "P0",
     DATA + "\nKT-1 mở tab 1 form tạo, chọn PKD1, 31/10/2026, dòng TTHHD 18.000.000 (chưa lưu)",
     "1. KT-1 mở tab 2, lập và lưu phiếu PKD1, 31/10/2026, TTHHD 18.000.000\n"
     "2. Quay lại tab 1, " + SAVE,
     "—",
     "- Mong đợi: báo đã kết chuyển hết, không tạo phiếu thứ hai\n"
     "- Lưu ý: theo code hiện tại tab 1 lưu thành công, danh sách có 2 phiếu cùng 18.000.000 nhưng phiếu "
     "thứ hai không có bút toán nào (đã gặp ở dữ liệu thật: TPE.KCCPPT2025.00010 trùng 00008, "
     "492.706.613) - ghi Failed"),

    ("002", "Hai kế toán cùng kết chuyển một phòng, một kỳ", "P0",
     DATA + "\nKT-1 và KT-3 cùng mở form, cùng chọn PKD1, 31/10/2026, dòng TTHHD 18.000.000",
     "1. KT-1 và KT-3 cùng bấm \"Lưu và duyệt\" gần như cùng lúc",
     "—",
     "- Mong đợi: chỉ một phiếu được tạo, người sau được báo đã kết chuyển\n"
     "- Bút toán không bị ghi 2 lần (tổng Nợ 3351 vụ việc TTHHD của PKD1 tới 31/10/2026 vẫn 18.000.000)\n"
     "- Lưu ý: theo code hiện tại cả hai phiếu đều tạo, danh sách hiện 2 phiếu 18.000.000 (bút toán chỉ "
     "ghi 1 lần) - ghi Failed"),

    ("003", "Số dư thay đổi giữa lúc chọn vụ việc và lúc lưu", "P1",
     DATA + "\nKT-1 đang mở form PKD1, 31/10/2026, dòng TTHHD 18.000.000",
     "1. Trong lúc đó, ghi thêm HĐ-02 TTHHD Có 3351 1.200.000 ngày 30/10/2026\n"
     "2. KT-1 " + SAVE,
     "—",
     "- Mong đợi: số tiền trên phiếu khớp với bút toán\n"
     "- Lưu ý: theo code hiện tại phiếu ghi 18.000.000 nhưng bút toán ghi 19.200.000 - ghi Failed"),

    ("004", "Gọi thẳng chức năng lưu với số tiền tự đặt", "P0",
     DATA,
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu: PKD1, 31/10/2026, TTHHD, số tiền 50.000.000",
     "—",
     "- Mong đợi: số tiền được tính lại hoặc bị từ chối\n"
     "- Lưu ý: theo code hiện tại phiếu ghi 50.000.000 trên danh sách, còn bút toán chỉ 18.000.000 - ghi "
     "Failed"),

    ("005", "Gọi thẳng chức năng lưu với phòng của công ty khác", "P1",
     DATA,
     "1. KT-1 dùng công cụ kiểm thử API gọi chức năng lưu với Phòng ban PKD9 (TPHP)",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: theo code hiện tại lưu được, Số phiếu mang mã TPE, bút toán ghi cho PKD9 - ghi Failed"),

    ("006", "Gọi thẳng chức năng lưu với Xuất hóa đơn = Không", "P2",
     DATA,
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu PKD1, 31/10/2026, TTHHD, Xuất hóa đơn = Không",
     "—",
     "- Phiếu lưu với Xuất hóa đơn Không; bút toán lấy hợp đồng không xuất hóa đơn (HĐ-06 1.000.000) và "
     "ghi Có 33483\n"
     "- Số tiền trên phiếu là số gửi lên"),

    ("007", "Bấm Lưu và duyệt nhiều lần liên tiếp", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD\n"
     "3. Bấm \"Lưu và duyệt\" liên tiếp 3 lần thật nhanh",
     "—",
     "- Nút bị khóa trong lúc lưu, chỉ tạo 1 phiếu"),
]

SEC_X = [
    ("001", "Kết chuyển cuối tháng cho một phòng", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + "\n"
     "3. Thêm dòng TTHHD, TVC; " + SAVE + "\n"
     "4. Mở chi tiết phiếu vừa tạo, xem bút toán",
     "—",
     "- Danh sách có phiếu 17.500.000\n"
     "- Chi tiết đủ 2 dòng\n"
     "- Bút toán như VI.002 - VI.004"),

    ("002", "Kết chuyển nhiều kỳ liên tiếp", "P0",
     DATA,
     "1. KT-1 lập phiếu PKD1, đến 30/09/2026, TTHHD\n"
     "2. KT-1 lập phiếu PKD1, đến 31/10/2026, TTHHD",
     "—",
     "- Phiếu 1: 10.000.000\n"
     "- Phiếu 2: 8.000.000\n"
     "- Sau đó số dư TTHHD của PKD1 tới 31/10/2026 bằng 0"),

    ("003", "Kết chuyển nhiều phòng trong cùng kỳ", "P1",
     DATA,
     "1. KT-1 lập phiếu PKD1, 31/10/2026, TTHHD\n"
     "2. KT-1 lập phiếu PKD2, 31/10/2026, TTHHD",
     "—",
     "- Phiếu PKD1 18.000.000, phiếu PKD2 9.000.000\n"
     "- Lọc Phòng ban ở danh sách tách đúng từng phiếu"),

    ("004", "Người xem tổng công ty kiểm tra phiếu của các công ty", "P1",
     DATA + "\nĐã có phiếu của TPE (PKD1) và TPHP (PKD9)",
     "1. Đăng nhập KT-2, " + MENU + "\n"
     "2. Mở chi tiết từng phiếu",
     "—",
     "- Thấy và mở được phiếu của cả hai công ty\n"
     "- Không có nút Thêm mới"),

    ("005", "Kết chuyển đầu năm mới không lấy số năm cũ", "P1",
     DATA + "\nĐầu năm 2027, còn số dư TTHHD năm 2026 chưa kết chuyển của PKD1 là 600.000",
     "1. KT-1 lập phiếu Năm 2027, Tính đến ngày 31/01/2027, PKD1, dòng TTHHD",
     "—",
     "- Số tiền chỉ gồm phát sinh năm 2027, không có 600.000 của năm 2026\n"
     "- Muốn kết chuyển 600.000 phải lập phiếu Năm 2026"),
]
