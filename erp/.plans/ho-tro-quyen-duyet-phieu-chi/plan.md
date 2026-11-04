# Hỗ trợ: phân quyền kế toán thanh toán — không thấy nút duyệt phiếu chi

Không Redmine (user nhờ check, ảnh phiếu chi `bill_payments/1674`) · @junfoke · ERP `TanPhatDev` — không sửa code

## Ngày 04/11/2026 (@junfoke)
- [x] 04/11/2026 — Hỗ trợ check: nút Duyệt/Hủy phiếu chi phụ thuộc trạng thái + quyền (`income_expenditure/bill_payments/show.blade.php:19-35`): Chờ KT trưởng duyệt → cần "Kế toán trưởng duyệt phiếu chi"; Chờ chi tiền → cần "Thủ quỹ duyệt phiếu chi". Phiếu EG.PC1126.00001 đang Chờ chi tiền nên chị Hải Yến (chỉ có quyền KT trưởng) không thấy nút là đúng; chị Thu Huyền thấy vì có quyền thủ quỹ. Giải thích thêm các phiếu ở menu Quản lý tiền (đang tiếp tục trong phiên).
