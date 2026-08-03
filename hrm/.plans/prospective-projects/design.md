# Design — Filter "Nhân viên KD phụ trách" màn Quản lý dự án TKT

## Mục tiêu
Màn `/assign/prospective-projects` (Danh sách dự án tiền khả thi) đang có 2 select nhân viên gây hiểu nhầm. Gộp còn 1 select "Nhân viên KD phụ trách" lọc đúng theo người phụ trách.

## Scope (FE-only, `hrm-client/pages/assign/prospective-projects/index.vue`)
1. **Đổi label**: "Nhân viên kinh doanh" → "Nhân viên KD phụ trách" (label + placeholder).
2. **Bỏ select "Nhân viên" thừa**: `V2BaseCompanyDepartmentFilter` thêm `:disable_employee="true"` (select `employee_id` này BE không dùng).
3. **Select "Nhân viên KD phụ trách" cascade**:
   - Options lọc theo Công ty → Phòng ban → Bộ phận (computed `mainSaleEmployeeOptions` + `mainSaleEmployeeAvailable`, replicate permission-scope + cascade của `V2BaseCompanyDepartmentFilter`, fail-closed `[]` nếu không quyền).
   - `:disabled="!filters.department_id"` — enable khi đã chọn Phòng ban (Bộ phận optional lọc hẹp thêm).
   - Reset `main_sale_employee_id` khi đổi company/department/part (3 watcher).

## Quyết định
- `main_sale_employee_id` = "NV KD phụ trách" (Employee.id). BE `ProspectiveProjectService::index` đã filter `where('main_sale_employee_id', ...)` — **không sửa BE**.
- Điều kiện enable: chọn Phòng ban (chốt với user).
- Không đụng component dùng chung `V2BaseCompanyDepartmentFilter`; mọi thay đổi nằm trong index.vue.

## Trạng thái
CODE DONE 2026-07-13, FE-only, chờ user build + test.
