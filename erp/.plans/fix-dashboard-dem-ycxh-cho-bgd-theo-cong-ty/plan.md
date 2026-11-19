# Trang tổng quan: số phiếu YC xuất hàng cần duyệt lệch danh sách

Không Redmine (user gửi ảnh: anh Trần Quang Hưng thấy 1 phiếu cần duyệt, bấm vào không có) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Xử lý: ô "Phiếu yêu cầu xuất hàng cần duyệt" ở trang tổng quan đếm mọi phiếu chờ Ban giám đốc duyệt, còn danh sách `?type=for_approve` chỉ lấy phiếu của công ty đang đăng nhập (sửa phân quyền task #7620 năm 2024, chỗ đếm không sửa theo). Xác nhận bằng dữ liệu prod: PYCXH-45658 thuộc công ty 1, anh Hưng ở công ty 9. Thêm lọc công ty vào chỗ đếm (`HomeController.php` ~1511-1519). Commit `3e713a23de`, đã lên `origin/gop_db`.
