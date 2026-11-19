# -*- coding: utf-8 -*-
"""Section V - VII cho man Ket chuyen chi phi phai tra."""
from tc_data_role import MENU, DATA, OPEN_KT1, NEW_KT1, HEAD

SAVE = "bấm \"Lưu và duyệt\""

SEC_V = [
    ("001", "Lưu khi chưa có dòng chi tiết", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", " + SAVE,
     "—",
     "- Cảnh báo \"Tạo kết chuyển thất bại!\"\n"
     "- Dưới bảng Chi tiết báo \"Bắt buộc phải nhập\"\n"
     "- Không tạo phiếu"),

    ("002", "Lưu khi dòng chưa chọn vụ việc", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", bấm dấu +, " + SAVE,
     "—",
     "- Cảnh báo \"Tạo kết chuyển thất bại!\"\n"
     "- Dưới ô Mã vụ việc dòng 1 báo \"Bắt buộc phải nhập\""),

    ("003", "Lưu khi chưa chọn Tính đến ngày", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Phòng ban PKD1, không chọn Tính đến ngày, " + SAVE,
     "—",
     "- Cảnh báo \"Tạo kết chuyển thất bại!\"\n"
     "- Dưới ô Tính đến ngày, Ngày hạch toán báo \"Bắt buộc phải nhập\""),

    ("004", "Lưu khi chưa chọn Phòng ban", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Tính đến ngày 31/10/2026, " + SAVE,
     "—",
     "- Dưới ô Phòng ban báo \"Bắt buộc phải nhập\", không tạo phiếu"),

    ("005", "Lưu với vụ việc có số tiền 0", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TNSQ (Số tiền 0)\n"
     "3. " + SAVE,
     "—",
     "- Cảnh báo \"Số tiền kết chuyển phải khác 0\"\n"
     "- Không tạo phiếu"),

    ("006", "Một dòng 0 lẫn với dòng có tiền", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD (18.000.000) và dòng TNSQ (0)\n"
     "3. " + SAVE,
     "—",
     "- Cảnh báo \"Số tiền kết chuyển phải khác 0\", không tạo phiếu\n"
     "- Xóa dòng TNSQ rồi lưu lại thì thành công"),

    ("007", "Tính đến ngày là ngày tương lai", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Năm 2026, Tính đến ngày 30/11/2026, Phòng ban PKD1, thêm dòng TTHHD\n"
     "3. " + SAVE,
     "—",
     "- Cảnh báo \"Ngày đến không được chọn ngày tương lai\", không tạo phiếu"),

    ("008", "Tính đến ngày khác Năm đã chọn", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Năm 2026, Tính đến ngày 31/12/2025, Phòng ban PKD1, thêm dòng TTHHD\n"
     "3. " + SAVE,
     "—",
     "- Cảnh báo \"Ngày đến không trùng với năm được chọn\", không tạo phiếu"),

    ("009", "Tính đến ngày hôm nay được chấp nhận", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. Chọn Năm 2026, Tính đến ngày 06/11/2026, Phòng ban PKD1, thêm dòng TTHHD\n"
     "3. " + SAVE,
     "—",
     "- Số tiền 20,000,000 (gồm cả 2.000.000 ngày 03/11/2026)\n"
     "- Thông báo \"Tạo kết chuyển thành công!\""),

    ("010", "Hai dòng trùng vụ việc khi lưu", "P1",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", dòng 1 TTHHD, dòng 2 cũng chọn TTHHD (bỏ qua cảnh báo)\n"
     "3. " + SAVE,
     "—",
     "- Cảnh báo \"Tạo kết chuyển thất bại!\"\n"
     "- Dưới ô Mã vụ việc báo \"Không được nhập trùng\", không tạo phiếu"),

    ("011", "Ghi chú không bắt buộc", "P2",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD, để trống Ghi chú, " + SAVE,
     "—",
     "- Tạo phiếu thành công"),

    ("012", "Ghi chú có ký tự đặc biệt", "P2",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD, Ghi chú \"KC quý 3 <PKD1> & 'TPE'\", " + SAVE + "\n"
     "3. Mở chi tiết phiếu vừa tạo",
     "—",
     "- Ghi chú hiện nguyên văn, không vỡ giao diện"),
]

SEC_VI = [
    ("001", "Lưu và duyệt thành công", "P0",
     DATA,
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", Ghi chú \"KC tháng 10\"\n"
     "3. Thêm dòng TTHHD (18.000.000) và dòng TVC (-500.000)\n"
     "4. " + SAVE,
     "—",
     "- Thông báo \"Tạo kết chuyển thành công!\", về màn danh sách\n"
     "- Phiếu mới ở đầu: Số phiếu TPE.KCCPPT2026.<số kế tiếp>, Đến ngày 31/10/2026, Ngày hạch toán "
     "31/10/2026, Phòng ban PKD1, Số tiền kết chuyển 17,500,000, Người tạo KT-1"),

    ("002", "Bút toán Nợ 3351 theo từng hợp đồng", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. Mở sổ chi tiết tài khoản 3351, lọc theo số phiếu vừa tạo",
     "—",
     "- Nợ 3351 10.000.000 (HĐ-01, NV-K1, vụ việc TTHHD)\n"
     "- Nợ 3351 5.000.000 (HĐ-02, NV-K1, TTHHD)\n"
     "- Nợ 3351 3.000.000 (HĐ-03, NV-K2, TTHHD)\n"
     "- Ngày hạch toán 31/10/2026"),

    ("003", "Bút toán Có 33481 gộp theo nhân viên", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. Mở sổ chi tiết tài khoản 33481, lọc theo số phiếu vừa tạo",
     "—",
     "- Có 33481 15.000.000 (NV-K1, TTHHD)\n"
     "- Có 33481 3.000.000 (NV-K2, TTHHD)"),

    ("004", "Vụ việc số âm ghi ngược chiều", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. Xem bút toán vụ việc TVC của phiếu vừa tạo",
     "—",
     "- Có 3351 500.000 (HĐ-01, NV-K1, TVC)\n"
     "- Nợ 33481 500.000 (NV-K1, TVC)"),

    ("005", "Tổng Nợ bằng tổng Có", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. Cộng toàn bộ bút toán của phiếu",
     "—",
     "- Tổng Nợ = tổng Có = 18.500.000"),

    ("006", "Số dư 3351 về 0 sau kết chuyển", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD",
     "—",
     "- Số tiền 0 (đã kết chuyển hết)\n"
     "- Bấm lưu thì báo \"Số tiền kết chuyển phải khác 0\""),

    ("007", "Phát sinh mới sau kết chuyển được kết chuyển bổ sung", "P0",
     DATA + "\nVừa lưu phiếu như VI.001; sau đó ghi thêm HĐ-02 TTHHD Có 3351 1.200.000 ngày 30/10/2026",
     "1. " + NEW_KT1 + "\n"
     "2. " + HEAD + ", thêm dòng TTHHD, " + SAVE,
     "—",
     "- Số tiền 1,200,000\n"
     "- Phiếu mới chỉ ghi Nợ 3351 / Có 33481 1.200.000 cho HĐ-02, NV-K1"),

    ("008", "Bút toán ghi theo công ty của phòng ban", "P1",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. Xem bút toán của phiếu vừa tạo",
     "—",
     "- Phòng ban nhân viên trên bút toán là PKD1, công ty nhân viên là TPE"),

    ("009", "Số phiếu tăng dần trong năm", "P1",
     DATA + "\nPhiếu kết chuyển năm 2026 mới nhất của TPE là TPE.KCCPPT2026.00055",
     "1. KT-1 tạo phiếu kết chuyển năm 2026 thành công",
     "—",
     "- Số phiếu TPE.KCCPPT2026.00056"),

    ("010", "Số phiếu theo năm đã chọn", "P2",
     DATA + "\nPhiếu kết chuyển năm 2025 mới nhất của TPE là TPE.KCCPPT2025.00041",
     "1. KT-1 tạo phiếu Năm 2025, Tính đến ngày 31/12/2025, có số tiền khác 0",
     "—",
     "- Số phiếu TPE.KCCPPT2025.00042"),

    ("011", "Phiếu kết chuyển không làm đổi báo cáo thưởng kinh doanh", "P1",
     DATA + "\nGhi lại số thưởng của HĐ-01 trên báo cáo thưởng kinh doanh theo hợp đồng; sau đó lưu phiếu "
     "như VI.001",
     "1. Mở lại báo cáo thưởng kinh doanh theo hợp đồng, xem HĐ-01",
     "—",
     "- Số thưởng của HĐ-01 không đổi so với trước khi kết chuyển"),

    ("012", "Bút toán được ghi sau khi lưu vài giây", "P1",
     DATA,
     "1. KT-1 tạo phiếu như VI.001\n"
     "2. Mở ngay sổ chi tiết 3351, sau đó tải lại sau ít giây",
     "—",
     "- Sau ít giây có đủ bút toán như VI.002 - VI.004\n"
     "- Lưu ý: bút toán ghi chạy nền; nếu chạy nền ngừng, phiếu vẫn báo thành công mà không có bút toán, "
     "màn không cho biết - ghi Failed nếu sau vài phút vẫn chưa có"),

    ("013", "Số tiền trên phiếu khớp với bút toán", "P0",
     DATA + "\nVừa lưu phiếu như VI.001",
     "1. So Số tiền kết chuyển trên danh sách với tổng Nợ 3351 trừ Có 3351 của phiếu",
     "—",
     "- Cùng bằng 17.500.000"),
]

SEC_VII = [
    ("001", "Xem chi tiết phiếu", "P0",
     DATA + "\nKC-03: PKD1, 31/10/2026, TTHHD 18.000.000, TVC -500.000, Ghi chú \"KC tháng 10\"",
     "1. " + OPEN_KT1 + "\n"
     "2. Bấm số phiếu KC-03",
     "—",
     "- Tiêu đề \"Chi tiết kết chuyển chi phí phải trả\"\n"
     "- Số phiếu, Năm 2026, Tính đến ngày 31/10/2026, Ngày hạch toán 31/10/2026, Phòng ban PKD1, Xuất hóa "
     "đơn Có, Ghi chú \"KC tháng 10\"\n"
     "- Chi tiết: dòng 1 TTHHD / 3351 / 33481 / 18,000,000; dòng 2 TVC / 3351 / 33481 / -500,000"),

    ("002", "Các ô ở chi tiết không sửa được", "P1",
     DATA + "\nKC-03 như VII.001",
     "1. Mở chi tiết KC-03\n"
     "2. Thử sửa Năm, Tính đến ngày, Phòng ban, Mã vụ việc",
     "—",
     "- Các ô đều khóa\n"
     "- Không có nút thêm / xóa dòng"),

    ("003", "Ô Ghi chú ở chi tiết", "P2",
     DATA + "\nKC-03 như VII.001",
     "1. Mở chi tiết KC-03\n"
     "2. Gõ thêm vào ô Ghi chú",
     "—",
     "- Mong đợi: ô Ghi chú khóa như các ô khác\n"
     "- Lưu ý: theo code hiện tại gõ được nhưng không có nút lưu, tải lại thì mất - ghi Failed"),

    ("004", "Tên vụ việc hiện đúng", "P1",
     DATA + "\nKC-03 như VII.001",
     "1. Mở chi tiết KC-03",
     "—",
     "- Cột Mã vụ việc hiện \"Thưởng thực hiện hợp đồng\", \"Tiền vận chuyển\""),

    ("005", "Phiếu cũ không xuất hóa đơn", "P2",
     "Có phiếu cũ KC-00 lưu với Xuất hóa đơn = Không",
     "1. Mở chi tiết KC-00",
     "—",
     "- Xuất hóa đơn = Không, Tài khoản có từng dòng là 33483"),

    ("006", "Chi tiết không có nút In, Sửa, Xóa", "P2",
     DATA + "\nKC-03 như VII.001",
     "1. Mở chi tiết KC-03",
     "—",
     "- Không có nút In, Sửa, Xóa, Duyệt"),
]
