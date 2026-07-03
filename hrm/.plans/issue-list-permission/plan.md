# Plan — Phân quyền màn danh sách Issue

## Phase 1 — Phân quyền danh sách (org-based + vai trò + dự án)

> **Cập nhật thiết kế (user feedback):** Tầng 3 phải xét org của TẤT CẢ người giữ vai trò (không chỉ người tạo).
> Vì watchers/supporters là n-n → dùng bảng phụ `issue_org_units` (issue_id, employee_id, company/department/part)
> snapshot org của 6 vai trò. Không thêm cột org lên bảng `issues`.

### BE
- [x] Migration tạo bảng `issue_org_units` + backfill org từ 6 vai trò (creator/assignee/approver/detected + watchers + supporters)
- [x] `IssueService::syncIssueOrgUnits()`: đồng bộ bảng phụ khi store + update
- [x] `IssueService::index()`: scope quyền — Tầng 1 (6 vai trò) + Tầng 2 (solution/project membership) + Tầng 3 (org qua `issue_org_units`)
- [x] `IssueService::tier3OrgCondition()`: điều kiện org theo quyền cấp cao nhất (cty/phòng ban/bộ phận); "tổng cty" = xem tất cả
- [x] `IssueService::index()`: nhận filter `company_id/department_id/part_id` (khớp nếu bất kỳ vai trò thuộc đơn vị)
- [x] Seeder: thêm 4 quyền group "Quản lý issue" (ids 1099–1102)

### FE
- [x] `index.vue`: thêm `V2BaseCompanyDepartmentFilter` (Công ty → Phòng ban → Bộ phận, ẩn nhân viên) đầu filter-grid
- [x] `index.vue`: `permissions` set trong `created()` qua `hasAPermission`
- [x] `index.vue`: auto-search deep watcher (ignoredFields/oldFilters) + filterStateMixin (key `assign_issues`)
- [x] `index.vue`: `@/assets/scss/v2-styles.scss` (đã có sẵn)

### Verify
- [x] `php -l` các file BE sửa — PASS
- [x] FE parse template (vue-template-compiler/@babel) — PASS
- [ ] User chạy migration + seeder + verify browser theo từng cấp quyền

## Phase 2 — Phân quyền danh sách Task (`/assign/tasks`)

> Mô hình tương tự Issue nhưng: **5 vai trò** (tạo/xử lý/phê duyệt kết quả/duyệt triển khai/theo dõi) +
> **kế thừa Cha↔Con** (vai trò ở task cha thấy task con; vai trò ở task con thấy task cha).
> "Người duyệt triển khai" là vai trò ĐỘNG (có quyền 'Duyệt task' + quản lý phòng của người xử lý) → xử lý trực tiếp trong query, không snapshot.

### BE
- [x] Migration tạo bảng `task_org_units` + backfill org từ created_by/assignee/approver/watchers
- [x] `TaskService::syncTaskOrgUnits()`: đồng bộ khi store + update
- [x] `TaskService::applyPermissionScope()`: Tầng 1 (5 vai trò + Cha→Con + Con→Cha) + Tầng 2 + Tầng 3 + deployment-approver
- [x] `TaskService::tier3OrgCondition()` + `applyOrgFilter()` + `getMySolutionIds`/`getMyProjectIds`
- [x] `TaskService::index()`: nhận filter `company_id/department_id/part_id`
- [x] Seeder: 4 quyền group "Quản lý task" (ids 1103–1106)

### FE
- [x] `tasks/index.vue`: dùng `V2BaseCompanyDepartmentFilter` (đã import sẵn) + set `permissions` trong created()
- [x] `tasks/index.vue`: filterStateMixin (key `assign_tasks`) + org fields trong initialStateForm (deep watcher đã có sẵn)

### Verify (test thật trên DB, rollback)
- [x] Script `hrm-api/scope_permission_test.php` — **17/17 PASS** cả Issue + Task
  - Tầng 1 (vai trò), Tầng 2 (solution member), Tầng 3 (cty/phòng ban/tổng cty), kế thừa Cha↔Con, deployment approver, lọc org, loại trừ khác công ty, sync org_units
- [x] `php -l` PASS, FE SFC parse PASS
- [x] 2 migration đã chạy trên `hrm_prod_local` (issue_org_units, task_org_units)
- [ ] User seed 8 quyền (1099–1106) + verify browser
