# Plan — task-assignee-all-company

## Phase 1: FE mở Người thực hiện (CreateTaskModal.vue)

- [x] Thêm data `companyEmployees` + fetch `GET assign/tasks/employees` trong `loadSelectOptions()` (map id/name/code/dept)
- [x] Đổi computed `assigneeOptionsForModule` → `assigneeOptions`: trả về companyEmployees (fallback peopleOptions), append assignee đang chọn nếu ngoài list (form + children)
- [x] Cập nhật 3 chỗ template dùng list assignee (task cha dòng ~149, add-row task con ~484, list task con ~590)
- [x] Bỏ điều kiện disable `(selectedSolutionHasModules && !form.solution_module_id)` ở picker Người thực hiện
- [x] Bỏ reset `assignee_id` trong `handleSolutionChange` + `handleSolutionModuleChange`; đổi check reset approver sang `approverOptionsForSolution`

## Phase 2: BE fix báo cáo version giải pháp (SolutionVersionsReportService.php)

- [x] `getVersionMembers()`: append assignee của task trong version không nằm trong snapshot (role "Thành viên", module_name gộp, giờ từ progress logs)
- [x] `buildQuery()`: `member_count` += COUNT(DISTINCT assignee ngoài snapshot) per version

## Phase 3: Verify

- [x] php -l file BE sửa — sạch
- [x] Tinker: version 1 có assignee 126 ngoài snapshot (snapshot=0) → getVersionMembers trả 1 người (Đỗ Văn Quảng, 3h), member_count=1 qua getReportData (trước fix = 0). DB dev không có version nào có snapshot member nên nhánh snapshot chỉ verify bằng code (query gốc giữ nguyên)
- [x] Playwright (token-inject namdangit): popup Thêm mới Task ở /assign/tasks — picker Người thực hiện enabled ngay khi chưa chọn giải pháp/hạng mục, dropdown hiện NV toàn công ty (Tên (mã NV) + mã phòng ban); BE endpoint trả 389 NV hoạt động công ty 1

## Phase 4: Fix option thiếu thông tin (feedback user 2026-07-04)

- [x] BE `TaskController::getEmployeesByCompany`: bổ sung select `name` (CONCAT mã phòng ban - fullname như Employee::getAll), `department_name`, `email`, `personal_telephone` + filter `departments.cooperation_type != 2` (khớp filter store module assign); giữ nguyên field cũ (additive)
- [x] FE `loadCompanyEmployees()`: map lại giống peopleOptions (name || fullname, dept=department_name, email, phone=personal_telephone)
- [x] Verify: php -l sạch; curl endpoint trả đủ field; Playwright screenshot option hiện "HN_QTTT - DNS Admin (11910245)" + SĐT + email + tên phòng ban đầy đủ — giống format cũ

### Checkpoint — 2026-07-04
Vừa hoàn thành: Phase 4 (option Người thực hiện hiển thị đủ thông tin như trước)
Đang làm dở: không
Bước tiếp theo: user verify browser bằng mắt (tạo task chọn NV ngoài staff giải pháp → lưu → check báo cáo /assign/report/solution-versions)
Blocked: không

