# Fix — Báo cáo plan-department-by-employee: trưởng phòng xem không ra dữ liệu

## Bối cảnh
`/admin/reports/plan-department-by-employee`. NV Trần Ngọc Duy (emp 35, quyền trưởng phòng), phòng 5 (Thiết bị ô tô 2), tháng 1-6/2026 → không hiện dòng nào.

## Điều tra (production)
- Duy quản lý đúng phòng 5 (EmployeeManageDepartment [5,53]) → **scope phân quyền OK**.
- Có kế hoạch đã duyệt cho phòng 5 năm 2026 → **dữ liệu tồn tại**.
- Plan-side query giống hệt dù có/không chọn công ty (3011 dòng) → **KHÔNG phải do chọn công ty**.

## Root cause
`PlanImplementSaleByEmployee`: sau `getProcessSales(...)`, gán `$de['employee'] = $eml_after_ary` rồi `array_map(..., $de['employee'])`. Trong một số kỳ dữ liệu, giá trị này là `null` → **`array_map(): Expected parameter 2 to be an array, null given`** → cả report throw → controller trả rỗng → user thấy trắng. (Reproduce impersonate Duy: year 2024/2025 crash; 2026 tình cờ không null nên ra 1 dòng — production 2026 nhiều khả năng dính null.)

## Fix
- [x] Guard mọi chỗ dùng `array_map`/`foreach` trên kết quả `getProcessSales` (ép về mảng nếu null) ở cả 3 path:
  - `getPlanDepartmentReportSearchData` (path A, is_company): ~716/721, 742/745, 762.
  - `getPlanDepartmentReportSearchDataByDepartment` (path B, trưởng phòng): ~972/973, 990, 996.
  - `getPlanDepartmentReportSearchDataByEmployee` (path C): ~1170/1176.
  - `$salesPlanEmpl->toArray()` guard null.
- [x] Verify (impersonate Duy, prod DB): 3 path × year 2024/2025/2026 → hết crash, ra dòng; 2023 = 0 (đúng).
- [ ] User test lại trên browser (deploy code) — hết crash, hiện dữ liệu phòng 5.

## File
- `app/Services/Reports/PlanImplementSaleByEmployee.php`

## Lưu ý
Fix crash là defensive — không đổi logic dữ liệu. `php -l` sạch. CHƯA commit.

## Nguyên nhân THẬT vụ "chọn phòng → trắng" (FE, khác bug crash)
Backend trả đủ (1 dòng phòng + 19 NV). View `plan_department_sub.blade.php`:
- Dòng cấp phòng ban gắn `ng-if="!form.department_id"` → chọn phòng cụ thể là ẩn.
- Dòng nhân viên gắn `ng-if="... && form.expand"` → chỉ hiện khi tích "chi tiết theo nhân viên".
→ Chọn phòng + không tích expand = trắng.

## Fix FE (hướng B — cải tiến theo góp ý user: auto-tick thay vì sửa ng-if)
- [x] (Đã revert cách sửa 7 ng-if trong `plan_department_sub.blade.php` — giữ nguyên logic render gốc.)
- [x] `index.blade.php` controller: thêm `$scope.$watch('form.department_id', fn => if(id) form.expand=true)` → chọn phòng ban cụ thể thì tự tích "Xem chi tiết theo nhân viên", nhân viên hiện bằng logic cũ. Không đụng partial dùng chung `onChangeDepartment`.
- [ ] User Ctrl+F5 test: chọn phòng → checkbox tự tick + nhân viên hiện.

Files: `resources/views/reports/sale_plan_by_employee/index.blade.php` (+ service crash-guard `PlanImplementSaleByEmployee.php`).
