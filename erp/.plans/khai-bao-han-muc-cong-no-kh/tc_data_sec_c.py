# -*- coding: utf-8 -*-
"""Section VIII (Rang buoc), IX (Co lap & dong thoi), X (Luong dau-cuoi)."""

SEC_VIII = [
    ("001", "Hạn mức vượt giới hạn số nguyên", "P0",
     "Tài khoản D, KH-001 dòng Công ty 1",
     "1. Nhập Hạn mức công nợ xuất hàng 3,000,000,000\n"
     "2. Bấm Lưu, tải lại trang",
     "Hạn mức công nợ xuất hàng: 3000000000",
     "- Hệ thống báo \"Cập nhật thành công!\"\n"
     "- Lưu ý: sau tải lại hiện 2,147,483,647 (số tối đa lưu được), KHÔNG phải 3,000,000,000\n"
     "- Kỳ vọng nghiệp vụ: phải báo lỗi hoặc lưu đúng số - ghi nhận lỗi nếu xảy ra"),

    ("002", "Hạn mức đúng bằng giới hạn", "P1",
     "Tài khoản D",
     "1. Nhập 2147483647, bấm Lưu, tải lại",
     "2147483647",
     "- Hiện 2,147,483,647"),

    ("003", "Nhập số thập phân", "P1",
     "Tài khoản D",
     "1. Nhập 1000000.6 vào Hạn mức công nợ tính lãi\n"
     "2. Bấm Lưu, tải lại",
     "1000000.6",
     "- Ô hiển thị số đã làm tròn\n"
     "- Sau tải lại hiện 1,000,001 (số nguyên)"),

    ("004", "Nhập số âm", "P1",
     "Tài khoản D",
     "1. Nhập -5000000 vào Hạn mức công nợ xuất hàng\n"
     "2. Bấm Lưu, tải lại",
     "-5000000",
     "- Lưu ý: hệ thống KHÔNG chặn số âm, lưu thành -5,000,000\n"
     "- Kỳ vọng nghiệp vụ: không cho nhập hạn mức âm - ghi nhận nếu xảy ra"),

    ("005", "Nhập chữ vào ô hạn mức", "P1",
     "Tài khoản D, KH-001 Công ty 1 đang 500,000,000",
     "1. Xóa ô, gõ \"abc\"\n"
     "2. Bấm Lưu, tải lại",
     "abc",
     "- Ô hiển thị 0 ngay khi gõ\n"
     "- Sau Lưu và tải lại hạn mức là 0 (không còn 500,000,000)"),

    ("006", "Nhập số 0", "P1",
     "Tài khoản D",
     "1. Nhập 0 vào cả 2 ô hạn mức\n"
     "2. Bấm Lưu",
     "0",
     "- Lưu thành công, ô hiển thị 0\n"
     "- Hạn mức 0 không chặn Phiếu yêu cầu xuất hàng (xem TC_10.003)"),

    ("007", "Dán số có dấu chấm ngăn cách kiểu Việt Nam", "P1",
     "Tài khoản D",
     "1. Dán \"500.000.000\" vào ô Hạn mức công nợ xuất hàng\n"
     "2. Quan sát ô",
     "500.000.000",
     "- Lưu ý: dấu chấm được hiểu là dấu thập phân, ô hiển thị 500 chứ không phải 500,000,000\n"
     "- Người dùng phải nhập số liền hoặc dùng dấu phẩy"),

    ("008", "Không bắt buộc nhập bất kỳ ô nào", "P2",
     "KH-NEW3 chưa khai báo, tài khoản C",
     "1. Không nhập gì, bấm Lưu\n"
     "2. Tải lại",
     "—",
     "- Báo \"Cập nhật thành công!\"\n"
     "- Dòng Công ty 3 vẫn hiện, 2 ô hạn mức = 0, Cách tính lãi trống"),
]

SEC_IX = [
    ("001", "Hai kế toán khác công ty cùng sửa một khách", "P0",
     "D (2 quyền, Công ty 1) và E (2 quyền, Công ty 3) cùng mở KH-001\n"
     "KH-001: Công ty 1 = 500,000,000; Công ty 3 = 300,000,000",
     "1. E sửa Công ty 3 thành 450,000,000, bấm Lưu\n"
     "2. D (KHÔNG tải lại trang) sửa Công ty 1 thành 600,000,000, bấm Lưu\n"
     "3. Tải lại trang, đọc KH-001",
     "E: Công ty 3 = 450,000,000\nD: Công ty 1 = 600,000,000",
     "- Kỳ vọng nghiệp vụ: Công ty 1 = 600,000,000 và Công ty 3 = 450,000,000\n"
     "- Lưu ý: theo code hiện tại Công ty 3 bị ghi đè về 300,000,000 (số cũ trên màn của D) - ghi "
     "nhận lỗi ghi đè chéo nếu xảy ra"),

    ("002", "Hai người cùng công ty cùng sửa", "P1",
     "D1 và D2 cùng có quyền Quản lý, cùng Công ty 1, cùng mở KH-001",
     "1. D1 lưu 600,000,000\n"
     "2. D2 lưu 700,000,000\n"
     "3. Tải lại trang",
     "—",
     "- Kết quả là 700,000,000 (người lưu sau thắng)\n"
     "- Không có cảnh báo dữ liệu đã bị người khác thay đổi"),

    ("003", "Phiếu yêu cầu xuất hàng chỉ dùng hạn mức công ty người lập", "P0",
     "KH-001: Công ty 1 hạn mức xuất hàng 100,000,000; Công ty 3 không khai báo\n"
     "NV-S thuộc Công ty 3 có hợp đồng với KH-001",
     "1. NV-S lập Phiếu yêu cầu xuất hàng cho KH-001 tổng 500,000,000, bấm gửi duyệt",
     "Tổng tiền sau thuế: 500,000,000",
     "- Không có hộp thoại vượt hạn mức\n"
     "- Hạn mức của Công ty 1 không áp cho người lập thuộc Công ty 3"),

    ("004", "Đổi công ty người dùng thì phạm vi dòng đổi theo", "P1",
     "C (chỉ Quản lý) đang thuộc Công ty 3, được chuyển sang Công ty 4",
     "1. Đăng nhập lại C, mở màn, tìm KH-001",
     "—",
     "- Chỉ thấy và sửa dòng Công ty 4"),
]

SEC_X = [
    ("001", "Khai báo hạn mức xuất hàng rồi lập Phiếu yêu cầu xuất hàng vượt hạn mức", "P0",
     "D (Công ty 1) khai báo KH-001 Công ty 1: Hạn mức công nợ xuất hàng 200,000,000\n"
     "NV-S thuộc Công ty 1; công nợ của KH-001 trên các hợp đồng do NV-S lập đang là 150,000,000",
     "1. D lưu hạn mức như tiền điều kiện\n"
     "2. NV-S vào Khởi tạo > Hàng hóa > Phiếu Yêu cầu xuất hàng, lập phiếu cho KH-001 tổng sau thuế "
     "80,000,000\n"
     "3. Bấm gửi duyệt",
     "Tổng tiền sau thuế: 80,000,000",
     "- 150,000,000 + 80,000,000 = 230,000,000 > 200,000,000\n"
     "- Hiện hộp thoại \"Xác nhận!\" nội dung \"Yêu cầu vượt hạn mức công nợ xuất hàng cho khách hàng "
     "(200,000,000 VNĐ)\"\n"
     "- Bấm Đồng ý: phiếu được gửi sang luồng duyệt vượt hạn mức công nợ"),

    ("002", "Phiếu yêu cầu xuất hàng trong hạn mức", "P0",
     "Như TC_10.001 nhưng phiếu tổng sau thuế 40,000,000",
     "1. NV-S gửi duyệt phiếu",
     "Tổng tiền sau thuế: 40,000,000",
     "- 150,000,000 + 40,000,000 = 190,000,000 <= 200,000,000\n"
     "- Không hiện hộp thoại vượt hạn mức, phiếu gửi duyệt bình thường"),

    ("003", "Hạn mức 0 hoặc trống không chặn", "P0",
     "KH-001 Công ty 1: Hạn mức công nợ xuất hàng để trống",
     "1. NV-S gửi duyệt phiếu 1,000,000,000 cho KH-001",
     "—",
     "- Không hiện hộp thoại vượt hạn mức"),

    ("004", "Công nợ chỉ tính trên hợp đồng do chính người lập phiếu tạo", "P1",
     "KH-001 Công ty 1 hạn mức 200,000,000\n"
     "Công nợ KH-001 trên hợp đồng của NV-S = 50,000,000; trên hợp đồng của NV-T = 300,000,000",
     "1. NV-S gửi duyệt phiếu 100,000,000 cho KH-001",
     "—",
     "- 50,000,000 + 100,000,000 = 150,000,000 <= 200,000,000 nên KHÔNG cảnh báo\n"
     "- Công nợ trên hợp đồng của NV-T không được cộng"),

    ("005", "Sửa hạn mức có hiệu lực ngay với phiếu gửi duyệt sau đó", "P1",
     "Như TC_10.001, phiếu vừa bị cảnh báo, NV-S bấm Hủy ở hộp thoại",
     "1. D nâng hạn mức Công ty 1 lên 300,000,000, bấm Lưu\n"
     "2. NV-S bấm gửi duyệt lại phiếu",
     "Hạn mức công nợ xuất hàng: 300,000,000",
     "- Không còn hộp thoại vượt hạn mức, phiếu gửi duyệt bình thường"),

    ("006", "Phiếu yêu cầu xuất hàng mượn không kiểm tra hạn mức", "P1",
     "KH-001 Công ty 1 hạn mức xuất hàng 100,000,000; công nợ đã 150,000,000",
     "1. NV-S lập Phiếu Yêu cầu xuất hàng mượn cho KH-001, gửi duyệt",
     "—",
     "- Lưu ý: theo code hiện tại màn xuất hàng mượn KHÔNG cảnh báo vượt hạn mức dù đã khai báo\n"
     "- Ghi nhận nếu nghiệp vụ yêu cầu phải cảnh báo"),

    ("007", "Phiếu tính lãi lấy cách tính lãi và hạn mức tính lãi", "P0",
     "KH-001 Công ty 1: Theo vượt hạn mức công nợ; Hạn mức tính lãi 200,000,000\n"
     "Người lập thuộc Công ty 1",
     "1. Vào Kế toán > Kế toán Công nợ > Phiếu tính lãi, tạo phiếu\n"
     "2. Chọn khách hàng KH-001",
     "Khách hàng: KH-001",
     "- Thông báo \"Thêm khách hàng thành công!\"\n"
     "- Ô Cách tính lãi hiện \"Theo vượt hạn mức công nợ\"\n"
     "- Hạn mức tính lãi lấy 200,000,000"),

    ("008", "Phiếu tính lãi với khách chưa khai báo cách tính lãi ở công ty mình", "P0",
     "KH-002 chỉ khai báo ở Công ty 3; người lập thuộc Công ty 1",
     "1. Tạo Phiếu tính lãi, chọn KH-002",
     "Khách hàng: KH-002",
     "- Báo vàng \"Khách hàng chưa cấu hình cách tính lãi!\"\n"
     "- Không điền khách vào phiếu"),

    ("009", "Báo cáo hạn mức công nợ khách hàng hiển thị số đã khai báo", "P1",
     "KH-001 Công ty 1: Hạn mức tính lãi 200,000,000; Hạn mức xuất hàng 500,000,000\n"
     "KH-NEW3 Công ty 1: cả 2 hạn mức = 0",
     "1. Người thuộc Công ty 1 vào Kế toán > Kế toán Công nợ > Báo cáo hạn mức công nợ khách hàng\n"
     "2. Tìm KH-001 và KH-NEW3",
     "—",
     "- KH-001: cột Hạn mức tính lãi 200,000,000; cột Hạn mức được nợ 500,000,000\n"
     "- KH-NEW3 KHÔNG có trên báo cáo (cả 2 hạn mức bằng 0)\n"
     "- Khai báo của công ty khác không hiện trên báo cáo của Công ty 1"),
]
