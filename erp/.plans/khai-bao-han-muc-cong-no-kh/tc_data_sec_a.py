# -*- coding: utf-8 -*-
"""Section I (Hien thi), II (Loc), III (Danh sach & phan trang)."""

SEC_I = [
    ("001", "Mở màn từ menu Kế toán", "P0",
     "Tài khoản D có cả 2 quyền, thuộc Công ty 1\n"
     "Hệ thống có 3 công ty, 57 khách hàng",
     "1. Đăng nhập bằng D\n"
     "2. Rê chuột vào menu Kế toán > Kế toán Công nợ\n"
     "3. Ở nhóm Khách hàng, bấm \"Khai báo hạn mức công nợ KH\"",
     "—",
     "- Mở màn tiêu đề \"Khai báo hạn mức công nợ khách hàng\"\n"
     "- Danh sách tự tải ngay, không cần bấm tìm kiếm\n"
     "- Hiện trang 1 với 10 khách hàng"),

    ("002", "Tiêu đề các cột của lưới", "P1",
     "Tài khoản D, mở màn",
     "1. Quan sát dòng tiêu đề bảng",
     "—",
     "- Đúng 9 cột theo thứ tự: STT · Mã khách · Tên khách · MST/CMND · Khai báo theo công ty · Cách tính "
     "lãi · Hạn mức công nợ tính lãi · Hạn mức công nợ xuất hàng · Hành động\n"
     "- Dòng tiêu đề dính trên cùng khi cuộn bảng"),

    ("003", "Bố cục khối dòng của một khách hàng", "P0",
     "KH-001 (Công ty Minh Phát, MST 0101234567) khai báo ở Công ty 1 và Công ty 3",
     "1. Tìm KH-001\n"
     "2. Quan sát khối dòng",
     "Khách hàng: KH-001",
     "- Các ô STT, Mã khách, Tên khách, MST/CMND, Hành động gộp dọc theo cả khối\n"
     "- Dưới dòng đầu có 2 dòng: Công ty 1, Công ty 3\n"
     "- Mỗi dòng công ty có ô chọn Cách tính lãi và 2 ô nhập hạn mức\n"
     "- Cột Hành động có 1 nút Lưu (biểu tượng đĩa mềm), chú thích \"Cập nhật\" khi rê chuột"),

    ("004", "Khách chưa khai báo hiện đủ mọi công ty", "P0",
     "Tài khoản D có cả 2 quyền\n"
     "Hệ thống có 3 công ty\n"
     "KH-NEW chưa có khai báo nào",
     "1. Tìm KH-NEW\n"
     "2. Quan sát các dòng công ty",
     "Khách hàng: KH-NEW",
     "- Hiện 3 dòng: Công ty 1, Công ty 3, Công ty 4\n"
     "- 2 ô hạn mức hiển thị 0\n"
     "- Ô Cách tính lãi chưa được chọn giá trị thật (xem TC_04.007)"),

    ("005", "Khách đã khai báo một phần chỉ hiện công ty đã khai báo", "P0",
     "Tài khoản D (2 quyền, Công ty 1)\n"
     "KH-002 chỉ khai báo ở Công ty 3",
     "1. Tìm KH-002\n"
     "2. Đếm số dòng công ty",
     "Khách hàng: KH-002",
     "- Chỉ hiện 1 dòng Công ty 3 (khóa)\n"
     "- KHÔNG có dòng Công ty 1 để D khai báo\n"
     "- Lưu ý: đây là hạn chế hiện tại, D không thể khai báo cho Công ty 1 với khách này"),

    ("006", "Hiển thị giá trị đã lưu", "P0",
     "KH-001 Công ty 1: Cách tính lãi = Theo thời gian thanh toán; Hạn mức tính lãi = 200000000; Hạn mức "
     "xuất hàng = 500000000",
     "1. Tìm KH-001\n"
     "2. Đọc dòng Công ty 1",
     "—",
     "- Cách tính lãi: \"Theo thời gian thanh toán\"\n"
     "- Hạn mức công nợ tính lãi: 200,000,000\n"
     "- Hạn mức công nợ xuất hàng: 500,000,000\n"
     "- Số căn phải"),

    ("007", "Trạng thái đang tải", "P2",
     "Mạng chậm (giả lập bằng công cụ trình duyệt)",
     "1. Mở màn\n"
     "2. Quan sát bảng khi đang chờ",
     "—",
     "- Bảng hiện dòng \"Đang tải dữ liệu\" kèm biểu tượng xoay\n"
     "- Tải xong dòng này biến mất"),

    ("008", "Trạng thái không có dữ liệu", "P1",
     "Khách hàng X đã bị xóa khỏi danh mục sau khi đã chọn trong ô tìm",
     "1. Chọn khách X trong ô \"Chọn khách hàng\"\n"
     "2. Bấm biểu tượng kính lúp",
     "—",
     "- Bảng hiện dòng \"Chưa có dữ liệu\"\n"
     "- Không hiện thanh phân trang số trang"),

    ("009", "Lỗi kết nối khi tải danh sách", "P2",
     "Ngắt mạng sau khi trang đã mở",
     "1. Bấm biểu tượng kính lúp",
     "—",
     "- Hiện thông báo đỏ \"Đã có lỗi xảy ra\"\n"
     "- Biểu tượng đang tải biến mất, trang không treo"),
]

SEC_II = [
    ("001", "Ô Chọn khách hàng tìm theo mã", "P0",
     "Có khách KH-001",
     "1. Bấm ô \"Chọn khách hàng\"\n"
     "2. Gõ \"KH-001\"\n"
     "3. Quan sát danh sách gợi ý",
     "Từ khóa: KH-001",
     "- Ô hiện chữ gợi ý \"Nhập tên, số điện thoại hoặc mã KH để tìm kiếm.\"\n"
     "- Gợi ý hiện dạng \"KH-001 - Công ty Minh Phát\""),

    ("002", "Tìm theo tên và theo số điện thoại", "P1",
     "KH-001 tên Công ty Minh Phát, SĐT 0912345678",
     "1. Gõ \"Minh Phát\" vào ô, quan sát gợi ý\n"
     "2. Xóa, gõ \"0912345678\", quan sát gợi ý",
     "Từ khóa 1: Minh Phát\nTừ khóa 2: 0912345678",
     "- Cả 2 lần đều ra KH-001\n"
     "- Không tìm được theo MST (ô không hỗ trợ tìm MST)"),

    ("003", "Từ khóa ngắn dưới 3 ký tự chỉ trả tối đa 20 gợi ý", "P2",
     "Có hơn 50 khách chứa chữ \"KH\"",
     "1. Gõ \"KH\" vào ô\n"
     "2. Đếm gợi ý",
     "Từ khóa: KH",
     "- Tối đa 20 gợi ý, khách tạo mới nhất lên đầu\n"
     "- Gõ thêm ký tự thứ 3 thì trả đủ toàn bộ kết quả khớp"),

    ("004", "Lọc theo một khách hàng", "P0",
     "Có 57 khách hàng",
     "1. Chọn KH-001 trong ô \"Chọn khách hàng\"\n"
     "2. Bấm vào biểu tượng kính lúp",
     "Khách hàng: KH-001",
     "- Lưới chỉ còn 1 khối KH-001, STT = 1\n"
     "- Thanh phân trang còn 1 trang"),

    ("005", "Chọn khách hàng không tự lọc", "P1",
     "Đang ở trang 1, chưa lọc",
     "1. Chọn KH-001 trong ô\n"
     "2. Không bấm tìm kiếm, quan sát lưới",
     "—",
     "- Lưới giữ nguyên danh sách cũ\n"
     "- Chỉ lọc khi bấm kính lúp"),

    ("006", "Bấm vào mép nút tìm kiếm (ngoài biểu tượng kính lúp)", "P2",
     "Đã chọn KH-001 trong ô",
     "1. Bấm vào phần viền xanh của nút tìm kiếm, tránh biểu tượng kính lúp",
     "—",
     "- Lưu ý: theo code hiện tại nút chỉ nhận thao tác khi bấm trúng biểu tượng, bấm ở viền KHÔNG lọc\n"
     "- Ghi nhận lỗi giao diện nếu người dùng phản ánh"),

    ("007", "Nút Làm mới xóa điều kiện lọc", "P0",
     "Đang lọc KH-001, đang ở trang 1",
     "1. Bấm biểu tượng làm mới (mũi tên tròn, nút xanh lá)",
     "—",
     "- Ô \"Chọn khách hàng\" trở về trống\n"
     "- Lưới hiện lại toàn bộ khách, về trang 1"),

    ("008", "Xóa chọn bằng dấu x trong ô rồi tìm kiếm", "P1",
     "Đang lọc KH-001",
     "1. Bấm dấu x trong ô \"Chọn khách hàng\"\n"
     "2. Bấm kính lúp",
     "—",
     "- Lưới hiện toàn bộ khách hàng, về trang 1"),

    ("009", "Lọc khi đang đứng ở trang sau", "P1",
     "Đang ở trang 4 của danh sách",
     "1. Chọn KH-001\n"
     "2. Bấm kính lúp",
     "—",
     "- Kết quả đưa về trang 1, hiển thị KH-001, không bị trang trống"),
]

SEC_III = [
    ("001", "Phân trang 10 khách hàng mỗi trang", "P0",
     "Có 57 khách hàng",
     "1. Mở màn, đếm số khối khách ở trang 1\n"
     "2. Bấm số trang 6",
     "—",
     "- Trang 1 có 10 khách\n"
     "- Trang 6 có 7 khách\n"
     "- Thanh phân trang có 6 số trang"),

    ("002", "STT đánh lại từ 1 ở mỗi trang", "P1",
     "Có 57 khách hàng",
     "1. Đọc cột STT ở trang 1\n"
     "2. Chuyển sang trang 2, đọc cột STT",
     "—",
     "- Trang 1: STT 1 > 10\n"
     "- Trang 2: STT vẫn 1 > 10 (KHÔNG phải 11 > 20)\n"
     "- Lưu ý: STT là số thứ tự trong trang, không phải trong toàn danh sách"),

    ("003", "Các nút điều hướng trang", "P1",
     "Có 150 khách hàng (15 trang)",
     "1. Bấm › (trang sau)\n"
     "2. Bấm » (trang cuối)\n"
     "3. Bấm ‹ (trang trước)\n"
     "4. Bấm « (trang đầu)",
     "—",
     "- Lần lượt về trang 2, 15, 14, 1\n"
     "- Thanh số trang hiện tối đa 10 số cùng lúc"),

    ("004", "Danh sách gồm cả khách ngừng hoạt động", "P1",
     "KH-OFF đang ở trạng thái ngừng hoạt động trong danh mục khách hàng",
     "1. Tìm KH-OFF bằng ô Chọn khách hàng, bấm kính lúp",
     "Khách hàng: KH-OFF",
     "- KH-OFF vẫn hiện và khai báo được"),

    ("005", "Danh sách gồm khách của mọi công ty", "P1",
     "Tài khoản C (chỉ Quản lý, Công ty 3)\n"
     "KH-C1 là khách do Công ty 1 phụ trách",
     "1. Tìm KH-C1",
     "—",
     "- KH-C1 vẫn hiện trong danh sách\n"
     "- C thấy dòng Công ty 3 để khai báo cho KH-C1"),

    ("006", "Chuyển trang khi đang sửa dở không cảnh báo", "P1",
     "KH-001 ở trang 1, tài khoản D có quyền sửa",
     "1. Sửa Hạn mức xuất hàng KH-001 thành 700,000,000, KHÔNG bấm Lưu\n"
     "2. Bấm sang trang 2 rồi quay lại trang 1",
     "Hạn mức công nợ xuất hàng: 700,000,000",
     "- Không có hộp thoại cảnh báo\n"
     "- Quay lại trang 1, KH-001 hiện số cũ (số vừa nhập bị mất)"),

    ("007", "Không có chức năng sắp xếp", "P2",
     "Mở màn",
     "1. Bấm vào tiêu đề các cột",
     "—",
     "- Không có biểu tượng sắp xếp, bấm tiêu đề không đổi thứ tự"),
]
