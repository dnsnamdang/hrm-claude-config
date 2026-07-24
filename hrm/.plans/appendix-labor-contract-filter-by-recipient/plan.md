# Plan — Filter Phụ lục HĐLĐ lọc theo nhân sự (recipient) + cột Phòng ban

## Bối cảnh
Màn `/decision/appendix-labor-contract`: filter Công ty/Phòng ban/Bộ phận đang lọc theo `company_id/department_id/part_id` của bảng `appendix_labor_contracts` = org **người tạo** (auto-set bởi `BaseModel::boot`). Yêu cầu: đổi sang lọc theo org của **nhân sự trong phụ lục** (recipient) — giống màn HĐLĐ (`labor-contract-filter-by-recipient`). Chốt với user: **Phòng ban & Bộ phận lọc + hiển thị theo giá trị MỚI (snapshot) trên phụ lục** (`new_department_id`/`new_part_id`/`new_department_name`); riêng **Công ty** lọc theo org của NV (`employee_id` → `employees` → `employee_infos.company_id`) vì phụ lục không lưu công ty người nhận.

## Phase 1 — Bugfix filter theo recipient

### BE (hrm-api)
- [x] `AppendixLaborContractService::index()`: `department_id` lọc theo `new_department_id`, `part_id` lọc theo `new_part_id`; `company_id` lọc theo `whereIn('employee_id', <subquery employees join employee_infos.company_id>)`. Giữ nguyên `checkPermissionList(...,'appendix_labor_contracts')` (phân quyền theo org người tạo). Cover luôn export/print (dùng chung endpoint index).

### Verify
- [x] Lọc Công ty/Phòng ban/Bộ phận → ra phụ lục có NV thuộc org đó (không theo người tạo) — tinker OK

## Phase 2 — Thêm cột Phòng ban

### BE (hrm-api)
- [x] `AppendixLaborContractResource`: thêm field `department_name` = `new_department_name` (phòng ban mới trên phụ lục).

### FE (hrm-client)
- [x] `index.vue`: thêm cột "Phòng ban" (`department_name`) ngay sau cột Nhân viên.

### Verify
- [ ] Danh sách hiển thị cột Phòng ban đúng vị trí, có dữ liệu (UI)
