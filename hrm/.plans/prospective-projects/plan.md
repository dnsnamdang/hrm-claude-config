# Plan — Quản lý dự án TKT (/assign/prospective-projects)

## Fix: Label filter "Nhân viên" → "Nhân viên KD phụ trách" (2026-07-13)

- [x] FE: Đổi label `V2BaseLabel` "Nhân viên kinh doanh" → "Nhân viên KD phụ trách" (index.vue dòng 27)
- [x] FE: Đổi placeholder select `main_sale_employee_id` → "Nhân viên KD phụ trách" (index.vue dòng 32)
- [x] Xác nhận filter BE: `ProspectiveProjectService::index` đã filter `where('main_sale_employee_id', ...)` = đúng NV KD phụ trách (dòng 93-94) → không cần sửa BE

## Fix 2: Gộp 2 select nhân viên → chỉ còn "Nhân viên KD phụ trách" cascade (2026-07-13)

Bối cảnh: màn đang có 2 select — "Nhân viên" (của `V2BaseCompanyDepartmentFilter`, field `employee_id`, không dùng ở BE) và "Nhân viên KD phụ trách" (`main_sale_employee_id`). Gây hiểu nhầm.

- [x] FE: Ẩn select "Nhân viên" thừa → thêm `:disable_employee="true"` cho `V2BaseCompanyDepartmentFilter`
- [x] FE: Select "Nhân viên KD phụ trách" dùng options cascade theo Công ty→Phòng ban→Bộ phận (computed `mainSaleEmployeeOptions` + `mainSaleEmployeeAvailable`, replicate permission-scope + cascade của component)
- [x] FE: `:disabled="!filters.department_id"` — enable khi đã chọn Phòng ban (Bộ phận optional lọc thêm)
- [x] FE: Reset `main_sale_employee_id` khi đổi company/department/part (3 watcher)
- [x] Verify: BE `index()` filter `main_sale_employee_id` không đổi (đã đúng)

### Ghi chú
- `main_sale_employee_id` chính là "NV KD phụ trách" (xác nhận qua comment service dòng 1148). BE đã filter đúng, chỉ label FE gây hiểu nhầm.

### Checkpoint — 2026-07-13
Vừa hoàn thành: Fix 1 (đổi label) + Fix 2 (gộp 2 select nhân viên → 1 select "Nhân viên KD phụ trách" cascade Công ty→Phòng ban→Bộ phận, disable đến khi chọn Phòng ban). FE-only.
Đang làm dở: (không)
Bước tiếp theo: user build FE + test trên UI (chỉ còn 1 select nhân viên; chọn Phòng ban mới enable; lọc dự án theo NV KD phụ trách; đổi Công ty/Phòng ban → reset).
Blocked: (không)
