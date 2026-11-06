# Phiếu yêu cầu chuyển hàng: chi tiết /show + In không xét 4 quyền phạm vi xem (ERP) — @junfoke

Phản ánh 06/11/2026: chị Mỹ Dung đã được cấp quyền xem theo tổng công ty (role 100010, tab công ty 1) mà mở phiếu 6902 vẫn báo không có quyền.

## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Xử lý lỗi code: danh sách lọc theo 4 quyền phạm vi (tổng công ty / công ty / phòng ban / bộ phận), còn `canView()` của màn chi tiết + In chỉ cho Super Admin, người tạo, hoặc `Kế toán kho` cùng công ty phiếu ⇒ thấy phiếu ở danh sách mà mở không được. Sửa `canView()` xét đủ 4 quyền phạm vi như danh sách (`app/Model/Warehouse/ProductTransferRequest.php`), chạy thử DB local: quyền tổng công ty mở được phiếu công ty khác. Commit `ce03b6832f` (gop_db, đã push). Sau deploy người dùng đăng xuất / đăng nhập lại.
