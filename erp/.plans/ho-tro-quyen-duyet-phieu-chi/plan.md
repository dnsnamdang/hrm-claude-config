# Hỗ trợ: phân quyền kế toán thanh toán — không thấy nút duyệt phiếu chi

Không Redmine (user nhờ check, ảnh phiếu chi `bill_payments/1674`) · @junfoke · ERP `TanPhatDev` — không sửa code

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Hỗ trợ check: nút Duyệt/Hủy phiếu chi phụ thuộc trạng thái + quyền (`income_expenditure/bill_payments/show.blade.php:19-35`): Chờ KT trưởng duyệt → cần "Kế toán trưởng duyệt phiếu chi"; Chờ chi tiền → cần "Thủ quỹ duyệt phiếu chi". Phiếu EG.PC1126.00001 đang Chờ chi tiền nên chị Hải Yến (chỉ có quyền KT trưởng) không thấy nút là đúng; chị Thu Huyền thấy vì có quyền thủ quỹ. Giải thích thêm các phiếu ở menu Quản lý tiền (đang tiếp tục trong phiên).

- [x] 04/11/2026 — Hỗ trợ check (tiếp): 6 màn menu Kế toán › Quản lý tiền **không chặn quyền vào trang**, chỉ chặn từng thao tác (`routes/web.php:6494-6642`): Phiếu thu / chi / UNC tạo-sửa cần "Kế toán thanh toán", duyệt cần "Thủ quỹ duyệt phiếu thu/chi" (phiếu chi thêm bước "Kế toán trưởng duyệt phiếu chi"); **Phiếu báo có dùng quyền riêng "Quản lý phiếu báo có"**; Đề nghị thu tiền ai cũng tạo, tab "Chờ kế toán xử lý" cần "Kế toán thanh toán"; Đề nghị thanh toán theo cấu hình duyệt. Thiếu quyền xem (`Xem tất cả phiếu thu/chi của công ty / tổng công ty`) thì vào được nhưng danh sách gần như trống → người dùng tưởng "không vào được".
