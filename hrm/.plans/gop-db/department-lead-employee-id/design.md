# Trưởng phòng / trưởng bộ phận lệch người sau gộp DB — tóm tắt

> @namdangit · 2026-09-25 · nhánh `fix/department-lead-employee-id` (từ `gop_db`) · spec: `docs/superpowers/specs/gop-db/2026-09-25-department-lead-employee-id-design.md`

## Hiện trạng (đo trên PROD `hrm_erp_gop`, 25/09/2026)
- `departments.department_lead_id` / `parts.part_lead_id`: **ERP hiểu là `employees.id`** (`app/Model/Common/Department.php:32`), **HRM hiểu là `employee_infos.id`**.
- Trước gộp mỗi hệ 1 DB, đồng bộ có dịch id (commit `610839805`). Gộp xong bảng trùng lấy bản ERP → giá trị là `employees.id` → HRM đọc ra người khác.
- Lệch: **75/84 phòng ban** (56 chỉ khác loại id, **19 ERP ghi hẳn người khác**) · **20/25 bộ phận**.
- Triệu chứng: `/human/company-struct` đổi hết trưởng phòng; duyệt làm thêm giờ, thông báo trưởng bộ phận (Issue), CRM sync… dùng nhầm người.

## Quyết định đã chốt (user chọn hướng 1)
| Điểm | Chốt |
|---|---|
| Nghĩa cột trong DB | **`employees.id` (theo ERP)** — ERP không phải sửa |
| HRM | Custom cast `EmployeeIdAsInfoIdCast` trên 6 model Department/Part của HRM: đọc ra `employee_infos.id`, ghi vào đổi ngược → code + FE HRM giữ nguyên hợp đồng cũ |
| Code đọc SQL thô (`DB::table`) | Sửa tay, quy đổi qua helper static của cast |
| Code port từ ERP (hạch toán, BillPayment) | Đã hiểu `employees.id` → KHÔNG đụng |
| Nhân sự chưa có tài khoản `employees` | Không lưu được làm trưởng phòng → báo lỗi 422 |
| 19 phòng lệch hẳn người | Chờ nghiệp vụ chốt, không tự sửa dữ liệu |
