# -*- coding: utf-8 -*-
"""Section VI (Xoa) va VII (In & Xuat Excel)."""

SEC_VI = [
    ("001", "Xóa phiếu nháp từ danh sách", "P0",
     "Phiếu T trạng thái Đang tạo do chính người đăng nhập lập, 2 dòng chi tiết",
     "1. Mở menu hành động dòng phiếu T, bấm Xóa\n"
     "2. Đọc hộp thoại\n"
     "3. Bấm Xác nhận\n"
     "4. Quan sát danh sách",
     "Phiếu T",
     "- Hộp thoại tiêu đề \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\"\n"
     "- Bấm Xác nhận: thông báo xanh \"Xóa phiếu đề nghị thanh toán thành công!\"\n"
     "- Phiếu T biến mất khỏi danh sách, tổng giảm 1"),

    ("002", "Hủy hộp thoại xác nhận xóa", "P0",
     "Phiếu T trạng thái Đang tạo",
     "1. Bấm Xóa ở dòng phiếu T\n"
     "2. Bấm nút Hủy\n"
     "3. Quan sát danh sách",
     "—",
     "- Hộp thoại đóng\n"
     "- Phiếu T còn nguyên, tổng không đổi"),

    ("003", "Xóa phiếu từ màn chi tiết", "P0",
     "Phiếu U trạng thái Không duyệt do chính người đăng nhập lập",
     "1. Mở chi tiết phiếu U\n"
     "2. Bấm nút Xóa ở hàng nút dưới cùng\n"
     "3. Đọc hộp thoại, bấm Xác nhận",
     "Phiếu U",
     "- Hộp thoại tiêu đề \"Xác nhận!\", nội dung \"Bạn chắc chắn muốn thực hiện hành động này?\"\n"
     "- Sau khi xác nhận: thông báo thành công, chuyển về màn danh sách chế độ Tất cả\n"
     "- Phiếu U không còn trong danh sách"),

    ("004", "Menu không có nút Xóa với phiếu đang trong dây chuyền duyệt", "P0",
     "4 phiếu do chính người đăng nhập lập, lần lượt ở Chờ TP duyệt, Chờ kế toán công nợ duyệt, Chờ "
     "tạo phiếu chi, Duyệt phiếu chi",
     "1. Mở menu hành động của từng phiếu\n"
     "2. Mở màn chi tiết từng phiếu, quan sát hàng nút",
     "4 trạng thái",
     "- Cả 4 phiếu đều KHÔNG có mục Xóa và không có mục Sửa ở cả 2 chỗ\n"
     "- Chỉ còn In và Xuất Excel"),

    ("005", "Không xóa được phiếu của người khác qua giao diện", "P0",
     "Phiếu W trạng thái Không duyệt do NV-B lập; đăng nhập bằng C có quyền xem theo công ty",
     "1. Tìm phiếu W, mở menu hành động\n"
     "2. Mở màn chi tiết phiếu W, quan sát hàng nút",
     "—",
     "- Không có mục Xóa ở cả 2 chỗ\n"
     "- ⚠️ Nhưng vẫn xóa được bằng đường dẫn trực tiếp — xem TC_06.006"),

    ("006", "Xóa được phiếu bất kỳ bằng đường dẫn trực tiếp", "P0",
     "Phiếu trạng thái Duyệt phiếu chi do người khác lập; đã sao lưu dữ liệu trước khi test",
     "1. Lấy đường dẫn xóa (thay số phiếu vào đường dẫn xóa của một phiếu nháp của mình)\n"
     "2. Dán vào thanh địa chỉ\n"
     "3. Kiểm tra phiếu còn hay mất",
     "—",
     "- ⚠️ Hiện trạng: phiếu BỊ XÓA, hệ thống báo xóa thành công dù không đúng người lập và không đúng "
     "trạng thái. LỖ HỔNG, ghi nhận Failed\n"
     "- Kỳ vọng đúng: từ chối và giữ nguyên phiếu\n"
     "- Khôi phục dữ liệu ngay sau khi test"),

    ("007", "Xóa phiếu không xóa theo dòng chi tiết", "P0",
     "Phiếu V trạng thái Đang tạo, có 3 dòng chi tiết gắn 3 hợp đồng khác nhau",
     "1. Ghi lại mã 3 hợp đồng của phiếu V\n"
     "2. Xóa phiếu V\n"
     "3. Tạo phiếu mới cùng loại chi, chọn lại đúng 3 hợp đồng đó\n"
     "4. Nhờ đội kỹ thuật đối chiếu xem các dòng chi tiết của phiếu V còn tồn tại hay không",
     "3 dòng chi tiết",
     "- Xóa phiếu thành công, phiếu không còn trên danh sách\n"
     "- 3 hợp đồng chọn lại được bình thường\n"
     "- ⚠️ Hiện trạng: các dòng chi tiết của phiếu đã xóa VẪN nằm lại trong hệ thống (không bị xóa "
     "theo). Ghi nhận Failed — dữ liệu rác này có thể làm sai các báo cáo cộng dồn theo dòng chi tiết\n"
     "- Kỳ vọng đúng: xóa phiếu thì xóa cả dòng chi tiết"),

    ("008", "Xóa phiếu xong quay lại đúng chỗ", "P2",
     "Đang ở trang 2 của danh sách, lọc Trạng thái = Đang tạo",
     "1. Xóa 1 phiếu ở trang 2 bằng menu hành động\n"
     "2. Quan sát trang hiện ra sau khi xóa\n"
     "3. Lặp lại nhưng xóa từ màn chi tiết",
     "—",
     "- Xóa từ danh sách: quay lại màn danh sách kèm thông báo xanh; ghi nhận trang và bộ lọc có được "
     "giữ hay không\n"
     "- Xóa từ màn chi tiết: chuyển về màn danh sách chế độ Tất cả"),
]

SEC_VII = [
    ("001", "In phiếu từ menu hành động mở tab mới", "P0",
     "Danh sách đang có phiếu",
     "1. Mở menu hành động của một dòng, bấm In\n"
     "2. Quan sát trình duyệt",
     "—",
     "- Mở TAB MỚI, tab danh sách vẫn còn nguyên\n"
     "- Tab mới hiện bản in của đúng phiếu đó, khổ giấy NGANG"),

    ("002", "Nội dung khối đầu bản in", "P0",
     "Phiếu Chi trả lại khách hàng, VND, đã qua vài cấp duyệt",
     "1. Mở bản in\n"
     "2. Đọc từ trên xuống",
     "—",
     "- Trên cùng là phần đầu trang của công ty người lập\n"
     "- Có Số phiếu, Ngày lập, Người đề nghị, Phòng ban, Lý do chi\n"
     "- Mọi thông tin khớp với màn chi tiết"),

    ("003", "Ba mẫu in theo loại chi và hình thức thanh toán", "P0",
     "3 phiếu: (a) Chi trả nhà cung cấp - TM; (b) Chi trả nhà cung cấp - CK; (c) Chi trả lại khách "
     "hàng - TM",
     "1. Mở bản in của lần lượt 3 phiếu\n"
     "2. So bố cục, tiêu đề và các khối thông tin",
     "3 tổ hợp",
     "- (a) dùng mẫu chi trả nhà cung cấp bằng tiền mặt\n"
     "- (b) dùng mẫu chi trả nhà cung cấp bằng chuyển khoản, có khối thông tin tài khoản ngân hàng\n"
     "- (c) dùng mẫu chung của phiếu đề nghị thanh toán\n"
     "- Không tổ hợp nào báo lỗi thiếu mẫu in"),

    ("004", "Bản in phiếu chuyển khoản hiện thông tin ngân hàng", "P0",
     "Phiếu Chi trả nhà cung cấp - CK, nhà cung cấp trong nước, đã điền đủ số tài khoản, tên tài khoản, "
     "ngân hàng, chi nhánh, tỉnh thành",
     "1. Mở bản in\n"
     "2. Đối chiếu từng ô thông tin ngân hàng với màn chi tiết",
     "—",
     "- Bản in hiện đủ Số tài khoản, Tên tài khoản, Ngân hàng, Chi nhánh, Tỉnh/Thành phố\n"
     "- Số tài khoản in đúng, không bị cắt bớt chữ số"),

    ("005", "Bản in phiếu chuyển khoản quốc tế", "P1",
     "Phiếu Chi trả nhà cung cấp - CK, nhà cung cấp NƯỚC NGOÀI, đã điền mã định danh ngân hàng và ô Phí",
     "1. Mở bản in\n"
     "2. Tìm các dòng thông tin chuyển tiền quốc tế và dòng Phí",
     "—",
     "- Bản in có mã định danh ngân hàng, địa chỉ ngân hàng và thông tin ngân hàng trung gian nếu có\n"
     "- Dòng Phí in đúng lựa chọn đã chọn trên form"),

    ("006", "Bảng chi tiết và số tiền trên bản in", "P0",
     "Phiếu đang ở Chờ tạo phiếu chi; người lập đề nghị 15.000.000, kế toán trưởng duyệt còn 10.000.000",
     "1. Mở bản in\n"
     "2. Đọc bảng chi tiết và dòng tổng",
     "—",
     "- Bảng hiện đủ số dòng chi tiết\n"
     "- ⚠️ Kiểm kỹ bản in đang lấy số của cấp nào: ghi lại con số thực tế và đối chiếu với màn chi "
     "tiết. Nếu bản in lấy số đề nghị ban đầu trong khi phiếu đã duyệt xuống 10.000.000 thì ghi nhận "
     "và báo lại nghiệp vụ\n"
     "- Có dòng tổng cộng và phần đọc số thành chữ"),

    ("007", "Số tiền còn nợ trên bản in được tính lại", "P1",
     "Phiếu lập từ tháng trước, Số tiền còn nợ lúc lập 25.000.000; hợp đồng đã được chi thêm 10.000.000",
     "1. Mở bản in của phiếu đó\n"
     "2. Đọc cột Số tiền còn nợ",
     "—",
     "- Hiện 15.000.000, không phải 25.000.000\n"
     "- ⚠️ Đúng thiết kế (mục 8), không ghi Failed"),

    ("008", "Xuất Excel từ menu hành động", "P0",
     "Danh sách đang có phiếu",
     "1. Mở menu hành động của một dòng, bấm Xuất Excel\n"
     "2. Chờ tệp tải về, mở tệp",
     "—",
     "- Tệp tải về có tên dạng phieu_de_nghi_thanh_toan_<mã phiếu>.xlsx\n"
     "- Mở được bằng Excel, không báo hỏng tệp\n"
     "- Nội dung khớp với bản in: thông tin chung, bảng chi tiết, dòng tổng"),

    ("009", "Xuất Excel từ màn chi tiết", "P1",
     "Đang mở màn chi tiết một phiếu",
     "1. Bấm nút Xuất Excel ở hàng nút dưới cùng",
     "—",
     "- Tệp tải về đúng phiếu đang xem\n"
     "- Màn chi tiết vẫn còn, không bị chuyển trang"),

    ("010", "In và Xuất Excel phiếu ở mọi trạng thái", "P1",
     "5 phiếu ở 5 trạng thái khác nhau, gồm cả Đang tạo và Không duyệt",
     "1. Với mỗi phiếu, bấm In rồi bấm Xuất Excel",
     "5 trạng thái",
     "- Cả 5 phiếu đều in được và xuất được, không trạng thái nào bị chặn\n"
     "- Bản in của phiếu Không duyệt hiển thị được nội dung Ghi chú không duyệt"),

    ("011", "In phiếu có dòng chi tiết thiếu hợp đồng", "P2",
     "Phiếu cũ có dòng chi tiết trỏ tới hợp đồng đã bị xóa hoặc loại hợp đồng không xác định",
     "1. Mở bản in của phiếu đó",
     "—",
     "- Bản in VẪN hiện ra, không trắng trang và không báo lỗi\n"
     "- Dòng đó hiện số tiền còn nợ bằng 0 và ô hợp đồng để trống"),
]
