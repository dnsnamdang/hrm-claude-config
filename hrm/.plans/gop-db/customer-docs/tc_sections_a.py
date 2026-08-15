# -*- coding: utf-8 -*-
"""Section I -> V cua testcase man Danh muc khach hang."""

SEC_I = [
    (1, "Mở màn hình từ menu", "P0",
     "Tài khoản có quyền 'Xem tất cả khách hàng'. Hệ thống có 3.451 khách hàng.",
     "1. Đăng nhập\n2. Vào menu Giao việc → Danh mục khách hàng",
     "—",
     "- Tiêu đề trang hiện 'Danh mục khách hàng'\n"
     "- Lưới nạp xong trong vòng 5 giây, không còn vòng quay chờ\n"
     "- Ô 'Hiển thị a–b / N' hiện đúng tổng 3.451"),

    (2, "Kiểm tra đủ các nút trên thanh công cụ", "P0",
     "Tài khoản có đủ quyền Thêm / Sửa / Xóa / Xuất dữ liệu khách hàng.",
     "1. Mở Danh mục khách hàng\n2. Quan sát thanh công cụ phía trên lưới",
     "—",
     "- Có đủ các nút: Tạo mới, Import Excel, Xuất CSV, Xuất Excel, Xuất PDF\n"
     "- Có biểu tượng Tuỳ chỉnh cột ở góc phải thanh công cụ\n"
     "- Có ô tìm kiếm nhanh và nút Bộ lọc nâng cao"),

    (3, "Kiểm tra đủ các cột mặc định của lưới", "P0",
     "Người dùng chưa từng chỉnh cấu hình cột trên màn này.",
     "1. Mở Danh mục khách hàng\n2. Kéo ngang lưới, đọc tên từng tiêu đề cột",
     "—",
     "- Có các cột theo đúng thứ tự: STT, Mã KH, Tên khách hàng, Tên viết tắt, Loại, MST, SĐT, Email, "
     "Nhóm KH, Địa chỉ, Tỉnh/TP, Tên đơn vị, Địa chỉ xuất hóa đơn, Trạng thái, Hành động\n"
     "- ⚠️ Bốn cột Công ty mẹ, Hãng xe, Người tạo, Người sửa (gần nhất) MẶC ĐỊNH ẨN, không thấy trên lưới"),

    (4, "Hiển thị khi không có dữ liệu khớp bộ lọc", "P1",
     "Hệ thống có dữ liệu bình thường.",
     "1. Mở Danh mục khách hàng\n2. Gõ vào ô tìm kiếm một chuỗi chắc chắn không tồn tại\n3. Chờ lưới nạp lại",
     "Từ khóa: zzzkhongtontai999",
     "- Lưới hiện dòng thông báo không có dữ liệu, kèm hình minh họa\n"
     "- Ô 'Hiển thị a–b / N' hiện N = 0\n"
     "- ⚠️ Không hiện lưới trắng trơn, không báo lỗi kỹ thuật"),

    (5, "Hiển thị đúng nhãn 5 loại đối tượng ở cột Loại", "P0",
     "Hệ thống có ít nhất 1 khách hàng cho mỗi loại: Cá nhân, Doanh nghiệp tư nhân, "
     "Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước.",
     "1. Mở Danh mục khách hàng\n2. Lọc lần lượt theo từng giá trị của ô Loại hình tổ chức\n"
     "3. Đọc giá trị cột Loại",
     "—",
     "- Cột Loại hiện đúng chữ tiếng Việt của từng loại, không hiện số hay mã"),

    (6, "Cột Trạng thái phân biệt Hoạt động và Khóa", "P0",
     "Có ít nhất 1 khách hàng đang Hoạt động và 1 khách hàng đã Khóa.",
     "1. Mở Danh mục khách hàng\n2. Tìm cả hai khách hàng trên\n3. Đọc cột Trạng thái",
     "—",
     "- Khách hàng bình thường hiện nhãn Hoạt động\n"
     "- Khách hàng đã khóa hiện nhãn Khóa, màu khác biệt rõ ràng\n"
     "- ⚠️ Cả hai đều nằm trong danh sách, khách hàng Khóa không bị ẩn đi"),

    (7, "Cột SĐT hiển thị nhiều số điện thoại", "P1",
     "Khách hàng KH-G có 3 số điện thoại.",
     "1. Mở Danh mục khách hàng\n2. Tìm KH-G\n3. Đọc cột SĐT",
     "—",
     "- Ba số hiện trong cùng một ô, ngăn nhau bằng dấu phẩy\n"
     "- Không bị cắt mất số nào"),

    (8, "Cột Nhóm KH hiển thị nhiều nhóm", "P1",
     "Khách hàng KH-H thuộc 2 nhóm khách hàng.",
     "1. Mở Danh mục khách hàng\n2. Tìm KH-H\n3. Đọc cột Nhóm KH",
     "—",
     "- Hai tên nhóm hiện trong cùng một ô, ngăn nhau bằng dấu phẩy"),

    (9, "Khách hàng cá nhân tự do không hiện trong danh sách", "P0",
     "Khách hàng cá nhân KH-TD do người khác tạo, chưa ai đăng ký, chưa có báo giá / cuộc họp / dự án "
     "tiềm năng nào. Số điện thoại của KH-TD là 0912345678. Tài khoản đăng nhập có quyền "
     "'Xem tất cả khách hàng của công ty'.",
     "1. Mở Danh mục khách hàng\n2. Gõ tên KH-TD vào ô tìm kiếm\n3. Quan sát kết quả",
     "Tên: (tên của KH-TD)",
     "- KHÔNG có kết quả nào\n"
     "- ⚠️ Đây là quy tắc bảo vệ khách hàng cá nhân, không phải lỗi tìm kiếm"),

    (10, "Tìm đúng trọn vẹn số điện thoại để thấy khách hàng cá nhân tự do", "P0",
     "Tiếp theo trường hợp trên: KH-TD có số điện thoại 0912345678.",
     "1. Ở ô tìm kiếm gõ 0912345678\n2. Chờ lưới nạp lại\n"
     "3. Xóa bớt chữ số cuối, gõ 091234567\n4. Chờ lưới nạp lại",
     "Số đúng: 0912345678 · Số thiếu: 091234567",
     "- Bước 2: KH-TD HIỆN trong danh sách\n"
     "- Bước 4: KH-TD KHÔNG hiện\n"
     "- ⚠️ Chỉ khớp đúng trọn vẹn số mới ra, khớp một phần thì không"),

    (11, "Khách hàng do chính mình tạo luôn nhìn thấy", "P0",
     "Tài khoản T0 không có cấp quyền xem nào. T0 vừa tạo khách hàng KH-MINE.",
     "1. Đăng nhập bằng T0\n2. Mở Danh mục khách hàng\n3. Tìm KH-MINE",
     "Tài khoản: T0",
     "- KH-MINE hiện trong danh sách dù T0 không có cấp quyền xem nào"),

    (12, "Khách hàng tổ chức không bị chặn bởi lớp bảo vệ khách hàng cá nhân", "P1",
     "Khách hàng tổ chức KH-TC do người khác tạo, chưa có báo giá nào, nhưng thuộc phạm vi công ty của "
     "người đăng nhập.",
     "1. Đăng nhập bằng tài khoản có quyền 'Xem tất cả khách hàng của công ty'\n2. Tìm KH-TC",
     "—",
     "- KH-TC hiện bình thường\n"
     "- ⚠️ Quy tắc ẩn 'khách hàng tự do' chỉ áp cho khách hàng CÁ NHÂN"),

    (13, "Tải lại trang giữ nguyên bộ lọc đang áp dụng", "P1",
     "Đã lọc theo Tỉnh/Thành phố = Hà Nội, kết quả 320 khách hàng.",
     "1. Áp dụng bộ lọc trên\n2. Nhấn phím tải lại trang\n3. Chờ lưới nạp xong",
     "Tỉnh/Thành phố: Hà Nội",
     "- Sau khi tải lại, bộ lọc Tỉnh/Thành phố vẫn là Hà Nội\n"
     "- Kết quả vẫn là 320 khách hàng"),

    (14, "Tốc độ nạp danh sách với dữ liệu lớn", "P1",
     "Hệ thống có 3.451 khách hàng, tài khoản có quyền Xem tất cả khách hàng.",
     "1. Mở Danh mục khách hàng, bấm giờ từ lúc bấm menu\n2. Ghi nhận thời gian tới khi lưới hiện dữ liệu",
     "—",
     "- Lưới hiện dữ liệu trong vòng 5 giây\n"
     "- ⚠️ Nếu bật thêm 4 cột ẩn mặc định thì thời gian sẽ tăng, cần đo riêng"),

    (15, "Khách hàng vừa là nhà cung cấp vẫn hiển thị", "P1",
     "Khách hàng KH-NCC được tích 'Là nhà cung cấp'.",
     "1. Mở Danh mục khách hàng\n2. Tìm KH-NCC",
     "—",
     "- KH-NCC hiện bình thường trong danh sách khách hàng\n"
     "- ⚠️ Đối tác vừa là khách hàng vừa là nhà cung cấp chỉ có MỘT bản ghi, không tách đôi"),
]

SEC_II = [
    (1, "Tìm nhanh theo tên khách hàng", "P0",
     "Có khách hàng tên 'Doanh nghiệp Thương mại An Phát'.",
     "1. Mở Danh mục khách hàng\n2. Gõ 'An Phát' vào ô tìm kiếm nhanh\n3. Chờ lưới nạp lại",
     "Từ khóa: An Phát",
     "- Danh sách chỉ còn các khách hàng có tên chứa 'An Phát'\n"
     "- Tổng số bản ghi đổi theo kết quả lọc"),

    (2, "Tìm nhanh theo mã khách hàng", "P0",
     "Có khách hàng mã KH.00125.",
     "1. Gõ KH.00125 vào ô tìm kiếm nhanh\n2. Chờ lưới nạp lại",
     "Từ khóa: KH.00125",
     "- Ra đúng 1 khách hàng có mã KH.00125"),

    (3, "Tìm nhanh theo mã số thuế", "P0",
     "Có khách hàng mã số thuế 0101234567.",
     "1. Gõ 0101234567 vào ô tìm kiếm nhanh\n2. Chờ lưới nạp lại",
     "Từ khóa: 0101234567",
     "- Ra đúng khách hàng có mã số thuế trên"),

    (4, "Tìm nhanh không phân biệt chữ hoa chữ thường", "P1",
     "Có khách hàng tên 'Doanh nghiệp Đại Việt'.",
     "1. Gõ 'đại việt'\n2. Ghi nhận kết quả\n3. Xóa, gõ 'ĐẠI VIỆT'\n4. So sánh kết quả",
     "Từ khóa: đại việt / ĐẠI VIỆT",
     "- Hai lần tìm cho ra CÙNG một tập kết quả"),

    (5, "Tìm nhanh với khoảng trắng thừa đầu cuối", "P2",
     "Có khách hàng tên 'Đại Việt'.",
     "1. Gõ '   Đại Việt   ' (có khoảng trắng thừa hai đầu)\n2. Chờ lưới nạp lại",
     "Từ khóa: '   Đại Việt   '",
     "- Vẫn ra kết quả như khi gõ không có khoảng trắng thừa"),

    (6, "Xóa từ khóa thì danh sách quay về đầy đủ", "P0",
     "Đang tìm với từ khóa cho ra 12 kết quả, tổng ban đầu là 3.451.",
     "1. Xóa hết nội dung ô tìm kiếm\n2. Chờ lưới nạp lại",
     "—",
     "- Tổng số bản ghi quay lại 3.451\n"
     "- Lưới quay về trang 1"),

    (7, "Mở cửa sổ Bộ lọc nâng cao", "P0",
     "Người dùng đang ở màn danh sách.",
     "1. Bấm nút Bộ lọc nâng cao\n2. Đếm số ô lọc hiện ra",
     "—",
     "- Cửa sổ bộ lọc mở ra với 19 tiêu chí\n"
     "- Có các ô: Công ty – Phòng ban – Bộ phận – Nhân viên, Quốc gia, Tỉnh/Thành phố, Mã khách hàng, "
     "MST/SĐT, Tên khách hàng, Số CCCD, Tên đơn vị, Loại hình tổ chức, Trạng thái, "
     "Loại hình hoạt động – Lĩnh vực kinh doanh, Người sửa gần nhất, Khách hàng hãng, Hãng xe, Cấp đại lý"),

    (8, "Lọc theo Loại hình tổ chức = Cá nhân", "P0",
     "Hệ thống có 1.200 khách hàng cá nhân trong phạm vi quyền.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Loại hình tổ chức = Cá nhân\n3. Bấm Tìm kiếm",
     "Loại hình tổ chức: Cá nhân",
     "- Mọi dòng đều có cột Loại = Cá nhân\n"
     "- Tổng số bản ghi đổi đúng theo kết quả lọc"),

    (9, "Lọc theo Trạng thái = Khóa", "P0",
     "Hệ thống có 35 khách hàng đã Khóa.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Trạng thái = Khóa\n3. Bấm Tìm kiếm",
     "Trạng thái: Khóa",
     "- Ra đúng 35 khách hàng, mọi dòng đều có cột Trạng thái = Khóa"),

    (10, "Lọc theo Trạng thái = Hoạt động", "P0",
     "Hệ thống có 3.451 khách hàng, trong đó 35 đã Khóa.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Trạng thái = Hoạt động\n3. Bấm Tìm kiếm",
     "Trạng thái: Hoạt động",
     "- Ra 3.416 khách hàng\n"
     "- ⚠️ Cộng với 35 khách hàng Khóa phải đúng bằng 3.451"),

    (11, "Lọc theo Tỉnh/Thành phố", "P0",
     "Hà Nội có 320 khách hàng.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Tỉnh/Thành phố = Hà Nội\n3. Bấm Tìm kiếm",
     "Tỉnh/Thành phố: Hà Nội",
     "- Ra 320 khách hàng, cột Tỉnh/TP đều là Hà Nội"),

    (12, "Ô Tỉnh/Thành phố phụ thuộc ô Quốc gia", "P0",
     "Danh mục có Việt Nam và một số quốc gia khác.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Quốc gia = Việt Nam\n3. Mở ô Tỉnh/Thành phố, đọc danh sách\n"
     "4. Đổi Quốc gia sang một quốc gia khác\n5. Mở lại ô Tỉnh/Thành phố",
     "Quốc gia: Việt Nam → quốc gia khác",
     "- Bước 3: danh sách chỉ có tỉnh/thành của Việt Nam\n"
     "- Bước 5: ô Tỉnh/Thành phố bị xóa trắng và nạp lại theo quốc gia mới"),

    (13, "Lọc theo Mã khách hàng khớp một phần", "P1",
     "Có nhiều khách hàng mã bắt đầu bằng KH.001.",
     "1. Mở Bộ lọc nâng cao\n2. Nhập Mã khách hàng = KH.001\n3. Bấm Tìm kiếm",
     "Mã khách hàng: KH.001",
     "- Ra tất cả khách hàng có mã chứa KH.001"),

    (14, "Lọc theo MST/SĐT — tìm bằng mã số thuế", "P0",
     "Khách hàng KH-I có mã số thuế 0109876543.",
     "1. Nhập MST/SĐT = 0109876543\n2. Bấm Tìm kiếm",
     "MST/SĐT: 0109876543",
     "- Ra đúng KH-I"),

    (15, "Lọc theo MST/SĐT — tìm bằng số điện thoại", "P0",
     "Khách hàng KH-J có 2 số điện thoại, số thứ hai là 0987654321.",
     "1. Nhập MST/SĐT = 0987654321\n2. Bấm Tìm kiếm",
     "MST/SĐT: 0987654321",
     "- Ra đúng KH-J\n"
     "- ⚠️ Tìm được cả khi số cần tìm nằm ở vị trí thứ hai trong danh sách nhiều số"),

    (16, "Lọc theo Số CCCD", "P1",
     "Khách hàng cá nhân KH-K có số CCCD 001199012345.",
     "1. Nhập Số CCCD = 001199012345\n2. Bấm Tìm kiếm",
     "Số CCCD: 001199012345",
     "- Ra đúng KH-K"),

    (17, "Lọc theo Tên đơn vị", "P1",
     "Khách hàng cá nhân KH-L có Tên đơn vị = 'Gara Minh Long'.",
     "1. Nhập Tên đơn vị = Minh Long\n2. Bấm Tìm kiếm",
     "Tên đơn vị: Minh Long",
     "- Ra các khách hàng có tên đơn vị chứa 'Minh Long'"),

    (18, "Lọc theo Khách hàng hãng = Có", "P1",
     "Hệ thống có 48 khách hàng được tích 'Là khách hãng'.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Khách hàng hãng = Có\n3. Bấm Tìm kiếm",
     "Khách hàng hãng: Có",
     "- Ra 48 khách hàng, tất cả đều có ít nhất một Hãng xe"),

    (19, "Lọc theo Hãng xe", "P1",
     "Hãng xe 'Toyota' gắn với 15 khách hàng.",
     "1. Chọn Hãng xe = Toyota\n2. Bấm Tìm kiếm",
     "Hãng xe: Toyota",
     "- Ra 15 khách hàng, bật cột Hãng xe lên thấy đều chứa Toyota"),

    (20, "Lọc theo Cấp đại lý", "P1",
     "Có các cấp đại lý trong danh mục, cấp 1 gắn với 9 khách hàng.",
     "1. Chọn Cấp đại lý = cấp 1\n2. Bấm Tìm kiếm",
     "Cấp đại lý: 1",
     "- Ra 9 khách hàng, cột Cấp đại lý đều đúng giá trị đã chọn"),

    (21, "Lọc theo cặp Loại hình hoạt động – Lĩnh vực kinh doanh", "P0",
     "Có 22 khách hàng khai loại hình 'Sản xuất' và lĩnh vực 'Cơ khí'.",
     "1. Mở ô Loại hình hoạt động – Lĩnh vực kinh doanh\n2. Chọn cặp Sản xuất – Cơ khí\n3. Bấm Tìm kiếm",
     "Cặp: Sản xuất – Cơ khí",
     "- Ra 22 khách hàng\n"
     "- ⚠️ Chọn theo cặp chứ không chọn rời từng vế"),

    (22, "Lọc theo Công ty – Phòng ban – Bộ phận – Nhân viên", "P0",
     "Nhân viên NV-A đã tạo 17 khách hàng.",
     "1. Mở ô Công ty – Phòng ban – Bộ phận – Nhân viên\n2. Chọn tới cấp nhân viên NV-A\n3. Bấm Tìm kiếm",
     "Nhân viên: NV-A",
     "- Ra 17 khách hàng liên quan tới NV-A"),

    (23, "Lọc theo Người sửa gần nhất", "P1",
     "Nhân viên NV-B là người sửa gần nhất của 6 khách hàng.",
     "1. Chọn Người sửa gần nhất = NV-B\n2. Bấm Tìm kiếm\n3. Bật cột Người sửa (gần nhất)",
     "Người sửa gần nhất: NV-B",
     "- Ra 6 khách hàng, cột Người sửa (gần nhất) đều là NV-B"),

    (24, "Kết hợp nhiều tiêu chí lọc cùng lúc", "P0",
     "Có 4 khách hàng vừa thuộc Hà Nội, vừa là Doanh nghiệp tư nhân, vừa đang Hoạt động.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Tỉnh/Thành phố = Hà Nội, Loại hình tổ chức = Doanh nghiệp tư nhân, "
     "Trạng thái = Hoạt động\n3. Bấm Tìm kiếm",
     "3 tiêu chí như trên",
     "- Ra 4 khách hàng thỏa ĐỒNG THỜI cả ba điều kiện\n"
     "- ⚠️ Các tiêu chí kết hợp theo kiểu 'và', không phải 'hoặc'"),

    (25, "Kết hợp tìm nhanh và bộ lọc nâng cao", "P0",
     "Tỉnh Hà Nội có 320 khách hàng, trong đó 3 khách hàng có tên chứa 'An Phát'.",
     "1. Chọn Tỉnh/Thành phố = Hà Nội, bấm Tìm kiếm\n2. Gõ thêm 'An Phát' vào ô tìm nhanh",
     "Hà Nội + An Phát",
     "- Ra 3 khách hàng thỏa cả hai\n"
     "- ⚠️ Ô tìm nhanh KHÔNG xóa bộ lọc nâng cao đang áp dụng"),

    (26, "Nút Làm mới xóa hết bộ lọc và nạp lại danh sách", "P0",
     "Đang áp dụng 3 tiêu chí lọc, kết quả 4 khách hàng.",
     "1. Bấm nút Làm mới trong cửa sổ bộ lọc\n2. Quan sát các ô lọc và lưới",
     "—",
     "- Tất cả ô lọc trở về rỗng\n"
     "- ⚠️ Lưới PHẢI nạp lại ngay, tổng số bản ghi quay về 3.451 — không được giữ nguyên kết quả cũ"),

    (27, "Số hiển thị trên nút Bộ lọc nâng cao", "P1",
     "Chưa áp dụng bộ lọc nào.",
     "1. Quan sát nút Bộ lọc nâng cao\n2. Chọn 3 tiêu chí, bấm Tìm kiếm\n3. Quan sát lại nút",
     "3 tiêu chí bất kỳ",
     "- Ban đầu nút không hiện số\n"
     "- Sau khi áp dụng, nút hiện số 3\n"
     "- ⚠️ Số này là số TIÊU CHÍ đang có giá trị, không phải số bản ghi"),

    (28, "Đóng cửa sổ bộ lọc mà không bấm Tìm kiếm", "P1",
     "Đang không áp dụng bộ lọc nào.",
     "1. Mở Bộ lọc nâng cao\n2. Chọn Trạng thái = Khóa\n3. Đóng cửa sổ mà KHÔNG bấm Tìm kiếm\n"
     "4. Quan sát lưới",
     "Trạng thái: Khóa",
     "- Lưới KHÔNG đổi, vẫn hiện đủ 3.451 khách hàng"),

    (29, "Lọc ra kết quả rỗng bằng bộ lọc nâng cao", "P1",
     "Không có khách hàng nào vừa ở Cà Mau vừa là Doanh nghiệp tư nhân.",
     "1. Chọn Tỉnh/Thành phố = Cà Mau, Loại hình tổ chức = Doanh nghiệp tư nhân\n2. Bấm Tìm kiếm",
     "Cà Mau + Doanh nghiệp tư nhân",
     "- Lưới hiện thông báo không có dữ liệu\n"
     "- Tổng số bản ghi = 0, không báo lỗi kỹ thuật"),

    (30, "Giữ bộ lọc khi chuyển trang rồi quay lại", "P1",
     "Đang lọc Tỉnh/Thành phố = Hà Nội.",
     "1. Bấm Sửa một khách hàng\n2. Bấm Quay lại danh sách\n3. Quan sát bộ lọc và tổng số bản ghi",
     "Tỉnh/Thành phố: Hà Nội",
     "- Bộ lọc Hà Nội vẫn còn, kết quả vẫn 320 khách hàng"),
]

SEC_III = [
    (1, "Mở cửa sổ Cài đặt bộ lọc", "P0",
     "Người dùng đang ở màn danh sách.",
     "1. Mở Bộ lọc nâng cao\n2. Bấm Cài đặt bộ lọc",
     "—",
     "- Cửa sổ mở ra, liệt kê 15 ô lọc có thể bật/tắt\n"
     "- Mỗi dòng có ô tích chọn và tay nắm để kéo đổi thứ tự"),

    (2, "Bỏ tích một ô lọc thì ô đó biến mất khỏi bộ lọc nâng cao", "P0",
     "Ô lọc 'Cấp đại lý' đang hiện trong bộ lọc nâng cao.",
     "1. Mở Cài đặt bộ lọc\n2. Bỏ tích 'Cấp đại lý'\n3. Bấm Lưu\n4. Mở lại Bộ lọc nâng cao",
     "Bỏ tích: Cấp đại lý",
     "- Ô Cấp đại lý không còn trong cửa sổ bộ lọc\n"
     "- Các ô còn lại giữ nguyên"),

    (3, "Kéo đổi thứ tự các ô lọc", "P1",
     "Ô 'Tên khách hàng' đang ở vị trí thứ 6.",
     "1. Mở Cài đặt bộ lọc\n2. Kéo 'Tên khách hàng' lên vị trí đầu tiên\n3. Bấm Lưu\n"
     "4. Mở lại Bộ lọc nâng cao",
     "—",
     "- Ô Tên khách hàng nằm ở vị trí đầu tiên trong cửa sổ bộ lọc"),

    (4, "Cài đặt bộ lọc được ghi nhớ sau khi tải lại trang", "P0",
     "Vừa bỏ tích 3 ô lọc và lưu.",
     "1. Nhấn phím tải lại trang\n2. Mở Bộ lọc nâng cao\n3. Đăng xuất rồi đăng nhập lại, mở lại bộ lọc",
     "—",
     "- Vẫn chỉ hiện 12 ô lọc như đã cấu hình\n"
     "- Cấu hình không bị mất sau khi đăng nhập lại"),

    (5, "Ẩn ô lọc không làm mất giá trị lọc đang áp dụng", "P0",
     "Đang lọc Trạng thái = Khóa, ra 35 kết quả.",
     "1. Mở Cài đặt bộ lọc, bỏ tích ô Trạng thái, bấm Lưu\n2. Quan sát lưới",
     "Bỏ tích: Trạng thái",
     "- ⚠️ Lưới VẪN chỉ hiện 35 khách hàng đã Khóa — giá trị lọc cũ vẫn còn tác dụng dù ô lọc bị ẩn\n"
     "- Bấm Làm mới mới xóa được giá trị đó"),

    (6, "Bật lại tất cả ô lọc", "P1",
     "Đang tắt 3 ô lọc.",
     "1. Mở Cài đặt bộ lọc\n2. Tích lại cả 3 ô\n3. Bấm Lưu\n4. Mở Bộ lọc nâng cao",
     "—",
     "- Đủ 19 tiêu chí hiện lại như ban đầu"),

    (7, "Mở cửa sổ Tuỳ chỉnh cột", "P0",
     "Người dùng đang ở màn danh sách.",
     "1. Bấm biểu tượng Tuỳ chỉnh cột ở góc phải thanh công cụ",
     "—",
     "- Cửa sổ mở ra, liệt kê đủ 20 cột kèm ô tích\n"
     "- ⚠️ Cột STT và Mã KH bị khóa, ô tích của hai cột này mờ và không bấm được"),

    (8, "Bật một cột đang ẩn", "P0",
     "Cột Công ty mẹ đang ẩn.",
     "1. Mở Tuỳ chỉnh cột\n2. Tích cột Công ty mẹ\n3. Bấm Lưu\n4. Quan sát lưới",
     "Bật: Công ty mẹ",
     "- Cột Công ty mẹ hiện trên lưới, có dữ liệu với khách hàng có công ty mẹ, để trống với khách hàng khác"),

    (9, "Bật cả 4 cột nặng cùng lúc", "P1",
     "Bốn cột Công ty mẹ, Hãng xe, Người tạo, Người sửa (gần nhất) đang ẩn.",
     "1. Mở Tuỳ chỉnh cột, tích cả 4 cột, bấm Lưu\n2. Bấm giờ thời gian nạp lưới",
     "Bật 4 cột",
     "- Cả 4 cột hiện đủ dữ liệu\n"
     "- ⚠️ Thời gian nạp lưới chậm hơn khi ẩn 4 cột này — ghi nhận số đo để đối chiếu"),

    (10, "Tắt một cột đang hiện", "P0",
     "Cột Email đang hiện.",
     "1. Mở Tuỳ chỉnh cột, bỏ tích Email, bấm Lưu",
     "Tắt: Email",
     "- Cột Email biến mất khỏi lưới, các cột khác dồn lại không để khoảng trống"),

    (11, "Không bỏ tích được cột STT và Mã KH", "P0",
     "Đang mở cửa sổ Tuỳ chỉnh cột.",
     "1. Bấm vào ô tích của cột STT\n2. Bấm vào ô tích của cột Mã KH",
     "—",
     "- Cả hai không bỏ tích được, luôn giữ trạng thái đã chọn"),

    (12, "Kéo đổi thứ tự cột", "P1",
     "Cột Email đang đứng sau cột SĐT.",
     "1. Mở Tuỳ chỉnh cột\n2. Kéo Email lên trước SĐT\n3. Bấm Lưu\n4. Quan sát lưới",
     "—",
     "- Trên lưới, cột Email đứng trước cột SĐT"),

    (13, "Cấu hình cột được ghi nhớ theo tài khoản", "P0",
     "Tài khoản A vừa bật cột Công ty mẹ và tắt cột Email.",
     "1. Đăng xuất tài khoản A\n2. Đăng nhập tài khoản B, mở Danh mục khách hàng\n"
     "3. Đăng xuất, đăng nhập lại tài khoản A",
     "—",
     "- Tài khoản B thấy cấu hình cột MẶC ĐỊNH, không bị ảnh hưởng bởi tài khoản A\n"
     "- Tài khoản A quay lại vẫn thấy cấu hình riêng của mình"),

    (14, "Khôi phục cấu hình cột mặc định", "P1",
     "Đang bật 4 cột ẩn và tắt 2 cột mặc định.",
     "1. Mở Tuỳ chỉnh cột\n2. Bấm nút khôi phục mặc định\n3. Bấm Lưu",
     "—",
     "- Lưới quay về đúng cấu hình mặc định ban đầu"),

    (15, "Cột đã tắt vẫn xuất ra file hay không", "P1",
     "Đang tắt cột Email trên lưới. Bộ lọc cho ra 20 khách hàng.",
     "1. Bấm Xuất Excel\n2. Mở file, đọc tiêu đề các cột",
     "—",
     "- Ghi nhận rõ: file xuất theo cấu hình cột đang hiện hay theo danh sách cột cố định\n"
     "- ⚠️ Kết quả phải nhất quán giữa ba định dạng CSV, Excel, PDF"),
]

SEC_IV = [
    (1, "Sắp xếp tăng dần theo Tên khách hàng", "P0",
     "Danh sách đang ở thứ tự mặc định.",
     "1. Bấm vào tiêu đề cột Tên khách hàng\n2. Đọc 5 dòng đầu",
     "—",
     "- Mũi tên sắp xếp hiện trên tiêu đề cột\n"
     "- 5 dòng đầu xếp theo bảng chữ cái tăng dần, đúng thứ tự tiếng Việt có dấu"),

    (2, "Sắp xếp giảm dần theo Tên khách hàng", "P0",
     "Vừa sắp xếp tăng dần theo Tên khách hàng.",
     "1. Bấm lần thứ hai vào tiêu đề cột Tên khách hàng\n2. Đọc 5 dòng đầu",
     "—",
     "- Thứ tự đảo ngược hoàn toàn so với lần trước"),

    (3, "Sắp xếp theo Mã KH", "P1",
     "Danh sách có nhiều mã dạng KH.000xx.",
     "1. Bấm tiêu đề cột Mã KH\n2. Đọc 10 dòng đầu",
     "—",
     "- Mã sắp xếp đúng thứ tự, không bị lẫn lộn giữa mã ngắn và mã dài"),

    (4, "Sắp xếp theo Ngày tạo", "P1",
     "Cột Ngày tạo đang hiện trên lưới.",
     "1. Bấm tiêu đề cột Ngày tạo hai lần để lấy giảm dần\n2. Đọc 5 dòng đầu",
     "—",
     "- Khách hàng tạo gần đây nhất đứng đầu"),

    (5, "Sắp xếp giữ nguyên khi chuyển trang", "P0",
     "Đang sắp xếp giảm dần theo Tên khách hàng.",
     "1. Bấm sang trang 2\n2. Đọc dòng đầu trang 2 và dòng cuối trang 1",
     "—",
     "- Thứ tự nối tiếp liền mạch giữa hai trang, không bị đảo lộn hay lặp bản ghi"),

    (6, "Sắp xếp kết hợp bộ lọc", "P1",
     "Đang lọc Tỉnh/Thành phố = Hà Nội (320 kết quả).",
     "1. Bấm tiêu đề cột Tên khách hàng\n2. Đọc tổng số bản ghi",
     "—",
     "- Tổng vẫn là 320, chỉ đổi thứ tự\n"
     "- ⚠️ Sắp xếp KHÔNG được làm mất bộ lọc"),

    (7, "Cột Hành động không sắp xếp được", "P2",
     "Đang ở màn danh sách.",
     "1. Bấm vào tiêu đề cột Hành động",
     "—",
     "- Không có gì xảy ra, không hiện mũi tên sắp xếp, lưới không nạp lại"),

    (8, "Chuyển trang bằng nút số trang", "P0",
     "Có 3.451 khách hàng, mỗi trang 20 dòng.",
     "1. Bấm số trang 2\n2. Đọc ô 'Hiển thị a–b / N' và cột STT",
     "—",
     "- Ô hiển thị đổi thành 21–40 / 3.451\n"
     "- Số thứ tự dòng đầu trang 2 là 21, không quay về 1"),

    (9, "Chuyển trang bằng nút tiến/lùi", "P1",
     "Đang ở trang 2.",
     "1. Bấm nút lùi một trang\n2. Bấm nút tiến một trang hai lần",
     "—",
     "- Về trang 1 rồi tới trang 3, số thứ tự và ô hiển thị đổi đúng theo"),

    (10, "Nút lùi bị vô hiệu ở trang đầu", "P2",
     "Đang ở trang 1.",
     "1. Quan sát nút lùi và nút về trang đầu",
     "—",
     "- Hai nút bị vô hiệu hóa, bấm không có tác dụng"),

    (11, "Nút tiến bị vô hiệu ở trang cuối", "P2",
     "Đang ở trang cuối cùng.",
     "1. Quan sát nút tiến và nút về trang cuối",
     "—",
     "- Hai nút bị vô hiệu hóa"),

    (12, "Đổi số dòng mỗi trang", "P0",
     "Đang hiển thị 20 dòng mỗi trang, tổng 3.451.",
     "1. Đổi ô số dòng mỗi trang sang 50\n2. Đếm số dòng trên lưới\n3. Đọc ô 'Hiển thị a–b / N'",
     "Số dòng: 50",
     "- Lưới hiện 50 dòng\n"
     "- Ô hiển thị đổi thành 1–50 / 3.451\n"
     "- ⚠️ Sau khi đổi số dòng phải quay về trang 1"),

    (13, "Đổi số dòng mỗi trang khi đang ở trang giữa", "P1",
     "Đang ở trang 5 với 20 dòng mỗi trang.",
     "1. Đổi số dòng mỗi trang sang 100\n2. Đọc ô 'Hiển thị a–b / N'",
     "Số dòng: 100",
     "- Quay về trang 1, ô hiển thị là 1–100 / 3.451\n"
     "- ⚠️ Không được nhảy tới trang 5 rỗng"),

    (14, "Áp dụng bộ lọc khi đang ở trang giữa", "P0",
     "Đang ở trang 7. Bộ lọc mới chỉ cho ra 12 kết quả.",
     "1. Áp dụng bộ lọc cho ra 12 kết quả\n2. Quan sát lưới",
     "—",
     "- ⚠️ Lưới quay về trang 1 và hiện 12 kết quả — không được hiện trang trống"),

    (15, "Số thứ tự liên tục qua các trang", "P0",
     "Đang hiển thị 20 dòng mỗi trang.",
     "1. Ghi lại số thứ tự dòng cuối trang 1\n2. Sang trang 2, đọc số thứ tự dòng đầu",
     "—",
     "- Dòng cuối trang 1 là 20, dòng đầu trang 2 là 21"),

    (16, "Trang cuối có ít dòng hơn", "P1",
     "Bộ lọc cho ra 45 kết quả, hiển thị 20 dòng mỗi trang.",
     "1. Bấm sang trang 3\n2. Đếm số dòng, đọc ô hiển thị",
     "—",
     "- Trang 3 có 5 dòng\n"
     "- Ô hiển thị là 41–45 / 45"),
]
