# Dữ liệu tạo thêm để chụp ảnh — Báo cáo phát triển khách hàng theo NVKD

DB: `local_hrm_erp` (gop_db-api local).

| Bảng | Bản ghi | Lý do |
|---|---|---|
| `role_has_permissions` | `(permission_id=1087, role_id=18, company_id=1)` | Gán quyền "Xem báo cáo phát triển khách hàng theo tổng công ty" cho vai trò "Super admin" (công ty 1) của tài khoản chụp DNS Admin. Trước đó tài khoản này không có quyền V1 nên nhóm "Kết quả chăm sóc trong kỳ" toàn 0. |

Gỡ lại nếu cần: `DELETE FROM role_has_permissions WHERE permission_id=1087 AND role_id=18 AND company_id=1;`

Không tạo khách hàng / dự án TKT mới: ảnh dùng dữ liệu có sẵn kỳ Tháng 7/2026 (khách hàng tổ chức tạo trong
tháng 7 + 145 dự án TKT tạo trong tháng 7), kỳ này được chọn trên bộ lọc lúc chụp.
