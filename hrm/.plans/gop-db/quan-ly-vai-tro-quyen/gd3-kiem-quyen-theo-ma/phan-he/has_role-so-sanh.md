# Task 8.18 — mốc trước/sau (Super Admin + hasRole)

Route: `has_role-routes.json` (3 route ERP phiếu nhập hàng điều chỉnh kiểm kê: index, searchData type=all, show × 7 id)
× 5 tài khoản (13 Super Admin + đủ mã · 196 Super Admin + GĐ + Kế toán · 901 cty 4 · 207 · 630 không mã) = 15 ô.

- Trước: chụp 2 lần, `diff` 0 ô (mốc ổn định). Chụp khi `InventoryImport::canView()` còn vế `hasRole('Admin Role')`.
- Sau: **15/15 ô khớp**. Không có ô lệch: rehearsal không ai giữ Vai trò "Admin Role".

Các chỗ khác đã sửa không có đường HTTP để chụp:
- `server_node/server.js` (socket): kiểm bằng node gọi thẳng `checkPermission` (Super Admin không quyền ⇒ false).
- FE `costPricePermission.js`, dashboard Đào tạo, 6 computed `isAdmin` chết: hrm-api không đổi. Đo bằng Playwright
  (xem task-8.18-report.md). Trên rehearsal, nhánh Vai trò ở FE vốn đã không chạy vì `roles[].name` mang tiền tố công ty.
