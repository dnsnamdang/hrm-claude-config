• Logic hệ thống/UI/UX:

Tại tab Báo giá trong màn hình chi tiết dự án tiền khả thi, đối với báo giá được đánh dấu ""Trúng thầu"":
Trường hợp 1: Nếu báo giá chỉ chứa hàng hóa chuẩn lấy từ Core ERP (không chứa hàng tạm), hệ thống KHÔNG hiển thị nút ""Gửi duyệt hàng tạm"".
Trường hợp 2: Nếu báo giá có chứa hàng tạm, hệ thống hiển thị nút ""Gửi duyệt hàng tạm"".
Khi người dùng click nút ""Gửi duyệt hàng tạm"":
Bước 1 (Tại hệ thống QLDA): Báo giá được đánh dấu/chuyển trạng thái đồng bộ hàng hóa thành ""Đang đồng bộ sang ERP"". Hệ thống đóng gói toàn bộ thông tin của các dòng ""Hàng tạm"" trong báo giá để gửi qua ERP.
Bước 2 (Tại hệ thống ERP): ERP tự động khởi tạo một phiếu ""Yêu cầu duyệt hàng tạm"" ở trạng thái ""Đang tạo"".
Hệ thống ERP tự động điền các trường dữ liệu theo bảng ánh xạ thông tin (mapping) nhận được từ QLDA.
Phân quyền: Phiếu ""Yêu cầu duyệt hàng tạm"" trên ERP chỉ mở quyền chỉnh sửa/duyệt cho các tài khoản người dùng thuộc bộ phận có thẩm quyền xét duyệt.
Bắn thông báo: Hệ thống ERP tự động gửi một thông báo (Notification) đến những người có thẩm quyền phê duyệt với nội dung: ""Có yêu cầu duyệt hàng tạm mới từ Dự án X"" (với X là tên dự án).
• Yêu cầu dữ liệu/Database:

Thêm trường trạng thái đồng bộ hàng tạm trên báo giá (Đang đồng bộ sang ERP, Đã đồng bộ).
• Điều kiện nghiệm thu/Acceptance Criteria:

AC 1: Truy cập tab Báo giá của dự án tiền khả thi có báo giá được đánh dấu ""Trúng thầu"" nhưng chỉ có hàng hóa ERP -> Xác nhận nút ""Gửi duyệt hàng tạm"" không hiển thị.
AC 2: Truy cập tab Báo giá có báo giá ""Trúng thầu"" chứa hàng hóa tạm -> Xác nhận nút ""Gửi duyệt hàng tạm"" hiển thị.
AC 3: Click ""Gửi duyệt hàng tạm"" -> Xác nhận trạng thái đồng bộ hàng hóa trên QLDA chuyển thành ""Đang đồng bộ sang ERP"".
AC 4: Kiểm tra trên hệ thống ERP -> Xác nhận sinh ra một phiếu ""Yêu cầu duyệt hàng tạm"" ở trạng thái ""Đang tạo"" với các thông tin được ánh xạ đầy đủ và chính xác từ QLDA.
AC 5: Kiểm tra phân quyền trên ERP -> Chỉ các user thuộc bộ phận có thẩm quyền mới có quyền sửa/duyệt phiếu.
AC 6: Kiểm tra thông báo trên ERP -> Người có thẩm quyền nhận được thông báo ""Có yêu cầu duyệt hàng tạm mới từ Dự án X""."