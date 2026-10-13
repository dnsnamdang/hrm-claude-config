# Redmine #11585 — Bộ lọc "Người thực hiện" ở mọi màn lịch sử: Tên NV - Mã phòng - Mã NV

- [x] BE: `HistoryPerformerOptions` (nguồn chung SystemLog/Catalog/Setting history) dùng `employeeOptionLabel()`; 10 service lịch sử Finance trả thêm `actor_dept_code`; lịch sử tài khoản NV trả `changed_by_label`
- [x] FE: fallback `SystemInfoSection` + `CustomerHistoryModal`, 3 panel lịch sử Finance (`performerText`), `EmployeeHistoryModal` dùng khuôn chung `employeeOptionText`
