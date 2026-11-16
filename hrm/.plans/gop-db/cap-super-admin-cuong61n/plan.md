# Cấp Super Admin cho tài khoản cuong61n@gmail.com trên PROD (không có số Redmine) — @cuong61n

## Task
- [x] 16/11/2026 — Cấp quyền Super Admin TPE cho tài khoản `cuong61n@gmail.com` (employees.id 1349, Nguyễn Mạnh Cường, công ty 1 = TPE) trên PROD HRM (hrm.eteksofts.com, DB `hrm_erp_gop`).
  - Nghiệp vụ: tài khoản vừa tạo hôm nay, chưa có vai trò nào → cho đủ quyền quản trị như tài khoản chính namdangit.
  - Kỹ thuật: INSERT 2 dòng vào `employee_has_roles` (company_id=1): role 18 `TPE_Super admin (DNS DÙNG)` + role 100002 `TPE_Super Admin` — đúng 2 vai trò Super Admin TPE mà namdangit đang giữ. Không đụng bảng/quyền khác.
  - Đã kiểm: SELECT lại thấy đủ 2 dòng. Chưa đăng nhập thử bằng tài khoản này.
  - Gỡ lại: `DELETE FROM employee_has_roles WHERE employee_id=1349 AND role_id IN (18,100002);`
  - Trạng thái: đã ghi thẳng vào DB prod ngày 16/11/2026.
