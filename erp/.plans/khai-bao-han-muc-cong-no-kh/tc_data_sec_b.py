# -*- coding: utf-8 -*-
"""Section IV (Khai bao / Luu), V, VI, VII (khong ap dung - kiem tra vang mat)."""

SEC_IV = [
    ("001", "Khai báo hạn mức cho khách chưa có khai báo", "P0",
     "Tài khoản C (chỉ Quản lý, Công ty 3)\n"
     "KH-NEW chưa có khai báo",
     "1. Tìm KH-NEW\n"
     "2. Dòng Công ty 3: chọn Cách tính lãi\n"
     "3. Nhập 2 ô hạn mức\n"
     "4. Bấm nút Lưu (đĩa mềm)\n"
     "5. Tải lại trang, tìm KH-NEW",
     "Cách tính lãi: Theo vượt hạn mức công nợ\n"
     "Hạn mức công nợ tính lãi: 100000000\n"
     "Hạn mức công nợ xuất hàng: 300000000",
     "- Biểu tượng nút Lưu chuyển sang xoay trong lúc lưu\n"
     "- Hiện thông báo xanh \"Cập nhật thành công!\"\n"
     "- Sau tải lại: Theo vượt hạn mức công nợ · 100,000,000 · 300,000,000"),

    ("002", "Sửa hạn mức đã có", "P0",
     "Tài khoản D (2 quyền, Công ty 1)\n"
     "KH-001 Công ty 1: Hạn mức xuất hàng 500,000,000",
     "1. Tìm KH-001\n"
     "2. Sửa Hạn mức công nợ xuất hàng dòng Công ty 1\n"
     "3. Bấm Lưu, tải lại trang",
     "Hạn mức công nợ xuất hàng: 800,000,000",
     "- Thông báo \"Cập nhật thành công!\"\n"
     "- Sau tải lại hiện 800,000,000"),

    ("003", "Đổi Cách tính lãi", "P0",
     "KH-001 Công ty 1: Theo vượt hạn mức công nợ",
     "1. Chọn lại \"Theo thời gian thanh toán\"\n"
     "2. Bấm Lưu, tải lại trang",
     "Cách tính lãi: Theo thời gian thanh toán",
     "- Thông báo thành công\n"
     "- Sau tải lại ô hiện \"Theo thời gian thanh toán\""),

    ("004", "Lưu khi có cả 2 quyền giữ nguyên dòng công ty khác", "P0",
     "Tài khoản D (2 quyền, Công ty 1)\n"
     "KH-001: Công ty 1 = 500,000,000; Công ty 3 = 300,000,000; Công ty 4 = 200,000,000 (hạn mức xuất hàng)",
     "1. Sửa dòng Công ty 1 thành 600,000,000\n"
     "2. Bấm Lưu\n"
     "3. Tải lại trang",
     "Công ty 1 - Hạn mức công nợ xuất hàng: 600,000,000",
     "- Công ty 1 = 600,000,000\n"
     "- Công ty 3 = 300,000,000 và Công ty 4 = 200,000,000 giữ nguyên"),

    ("005", "Lưu bởi người CHỈ có quyền Quản lý làm mất khai báo công ty khác", "P0",
     "Tài khoản C (chỉ Quản lý, Công ty 3)\n"
     "KH-001: Công ty 1 = 500,000,000; Công ty 3 = 300,000,000",
     "1. Đăng nhập C, tìm KH-001 (chỉ thấy dòng Công ty 3)\n"
     "2. Sửa Công ty 3 thành 350,000,000, bấm Lưu\n"
     "3. Đăng nhập tài khoản D (2 quyền), tìm KH-001",
     "Công ty 3 - Hạn mức công nợ xuất hàng: 350,000,000",
     "- Kỳ vọng nghiệp vụ: Công ty 1 vẫn còn 500,000,000\n"
     "- Lưu ý: theo code hiện tại dòng Công ty 1 BỊ XÓA, D chỉ còn thấy Công ty 3 = 350,000,000 - "
     "ghi nhận lỗi mất dữ liệu nếu xảy ra"),

    ("006", "Lưu riêng từng khách hàng", "P0",
     "Trang 1 có KH-001 và KH-002, tài khoản D",
     "1. Sửa hạn mức cả KH-001 và KH-002\n"
     "2. Chỉ bấm Lưu ở KH-001\n"
     "3. Tải lại trang",
     "KH-001: 600,000,000\nKH-002: 900,000,000",
     "- KH-001 hiện 600,000,000\n"
     "- KH-002 vẫn số cũ (chưa được lưu)\n"
     "- Nút Lưu chỉ lưu đúng khách hàng của khối đó"),

    ("007", "Ô Cách tính lãi của khách mới không bấm chọn", "P0",
     "Tài khoản C, KH-NEW2 chưa có khai báo",
     "1. Tìm KH-NEW2, quan sát ô Cách tính lãi dòng Công ty 3\n"
     "2. Không bấm chọn ô này, chỉ nhập Hạn mức tính lãi 100,000,000\n"
     "3. Bấm Lưu, tải lại trang\n"
     "4. Lập Phiếu tính lãi, chọn khách KH-NEW2",
     "Hạn mức công nợ tính lãi: 100,000,000",
     "- Ô Cách tính lãi có thể hiển thị sẵn chữ của lựa chọn đầu\n"
     "- Sau tải lại ô Cách tính lãi trống\n"
     "- Phiếu tính lãi báo vàng \"Khách hàng chưa cấu hình cách tính lãi!\"\n"
     "- Lưu ý: người dùng PHẢI bấm chọn Cách tính lãi thì giá trị mới được lưu"),

    ("008", "Xóa trắng ô hạn mức rồi Lưu", "P1",
     "KH-001 Công ty 1: Hạn mức tính lãi 200,000,000",
     "1. Xóa hết số trong ô Hạn mức công nợ tính lãi\n"
     "2. Bấm Lưu, tải lại trang",
     "Hạn mức công nợ tính lãi: (để trống)",
     "- Thông báo thành công\n"
     "- Sau tải lại ô hiện 0\n"
     "- Hạn mức để trống/0 nghĩa là KHÔNG giới hạn ở các chứng từ dùng tới"),

    ("009", "Tự định dạng dấu phẩy khi gõ", "P1",
     "Tài khoản D, dòng Công ty 1 của KH-001",
     "1. Gõ 1500000000 vào ô Hạn mức công nợ xuất hàng\n"
     "2. Quan sát ô",
     "1500000000",
     "- Ô tự hiển thị 1,500,000,000 ngay khi gõ"),

    ("010", "Nhiều lần bấm Lưu liên tiếp", "P2",
     "Tài khoản D, KH-001",
     "1. Sửa hạn mức\n"
     "2. Bấm Lưu 3 lần thật nhanh\n"
     "3. Tải lại trang",
     "—",
     "- Không sinh khai báo trùng: mỗi công ty vẫn chỉ 1 dòng\n"
     "- Số liệu bằng số vừa nhập"),

    ("011", "Biểu tượng đang lưu hiển thị ở mọi khách hàng", "P2",
     "Trang 1 có 10 khách",
     "1. Bấm Lưu ở KH-001 khi mạng chậm\n"
     "2. Quan sát cột Hành động của các khách khác",
     "—",
     "- Lưu ý: tất cả nút Lưu trên trang cùng chuyển sang biểu tượng xoay cho tới khi lưu xong "
     "(hành vi hiện tại, không phải chỉ riêng KH-001)"),

    ("012", "Lưu thất bại do lỗi hệ thống", "P1",
     "Giả lập lỗi cơ sở dữ liệu khi lưu (môi trường kiểm thử)",
     "1. Sửa hạn mức KH-001, bấm Lưu\n"
     "2. Tải lại trang",
     "—",
     "- Hiện thông báo vàng \"Cập nhật thất bại!\"\n"
     "- Sau tải lại số liệu cũ còn nguyên (không bị xóa mất khai báo cũ)"),

    ("013", "Lỗi kết nối khi Lưu", "P2",
     "Ngắt mạng sau khi mở trang",
     "1. Bấm Lưu",
     "—",
     "- Hiện thông báo đỏ \"Đã có lỗi xảy ra\"\n"
     "- Nút Lưu trở lại biểu tượng đĩa mềm"),
]

SEC_V = [
    ("001", "Màn không có thao tác trạng thái", "P2",
     "Tài khoản D, mở màn",
     "1. Quan sát cột Hành động và thanh công cụ",
     "—",
     "- Chỉ có nút Lưu, không có Khóa/Mở khóa, Duyệt hay Gửi duyệt\n"
     "- Khai báo có hiệu lực ngay sau khi Lưu"),
]

SEC_VI = [
    ("001", "Màn không có chức năng Xóa khai báo", "P2",
     "Tài khoản D, KH-001 có khai báo Công ty 1",
     "1. Quan sát cột Hành động\n"
     "2. Muốn bỏ hạn mức: xóa trắng 2 ô, bấm Lưu",
     "—",
     "- Không có nút Xóa\n"
     "- Bỏ hạn mức bằng cách để trống/0 (xem TC_04.008); dòng công ty vẫn còn trên lưới"),
]

SEC_VII = [
    ("001", "Màn không có In và Xuất Excel", "P2",
     "Tài khoản D, mở màn",
     "1. Tìm các nút In / Xuất Excel / Nhập Excel",
     "—",
     "- Không có nút nào\n"
     "- Muốn xem tổng hợp dùng màn Báo cáo hạn mức công nợ khách hàng"),
]
