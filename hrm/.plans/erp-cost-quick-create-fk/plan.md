# Fix lỗi 1452 khi tạo nhanh Dịch vụ/Chi phí ở báo giá

- [x] BE: `ErpCostController::resolveErpEmployeeId()` query `mysql2.employees` theo `employee_info_id` (fallback 1) thay vì `TpEmployee` (đọc employees DB HRM) — id HRM ghi vào `costs.created_by` vi phạm FK sang employees ERP
