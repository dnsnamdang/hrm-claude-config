# Phân quyền hàng loạt — Plan

**Owner:** @dnsnamdang
**Spec:** [docs/superpowers/specs/2026-05-27-bulk-permission-design.md](../../docs/superpowers/specs/2026-05-27-bulk-permission-design.md)

---

## Phase 1 — Backend (Module Timesheet)

### BE

- [x] Tạo `Modules/Timesheet/Services/BulkPermissionService.php` (extend TimesheetService)
- [x] Implement `resolveAffectedEmployeesQuery` + `baseAffectedEmployeesQuery` (refactor để tách excluded)
- [x] Implement `preview(request)` — paginate + sub-filter + tab + totals
- [x] Implement `apply(request)` — chunk 100, transaction, raw insert/delete `employee_has_permissions` (KHÔNG có company_id — schema chưa hỗ trợ, quyết định 2026-05-27)
- [x] `BulkPermissionPreviewRequest`
- [x] `BulkPermissionApplyRequest` + custom rule "phải có ít nhất 1 đối tượng"
- [x] `BulkPermissionController` (3 method)
- [x] `BulkPermissionEmployeesExport` + blade `bulk_permission_employees.blade.php` + method `exportEmployees` trong service
- [x] 3 routes `/timesheet/bulk-permissions/*` với middleware `checkPermission:Quản lý phân quyền`
- [x] ~~Verify index trên model_has_permissions~~ (skip)
- [ ] Test thủ công Postman: preview combo filter, apply grant + revoke, export

---

## Phase 2 — Frontend (hrm-client)

### FE

- [x] Button "Phân quyền hàng loạt" trên `pages/timesheet/setting/roles/index.vue` (check `hasAPermission`)
- [x] `components/timesheet/setting/roles/BulkPermissionModal.vue` — modal xl, state + watchers + debounced fetch
- [x] `BulkPermissionFilter.vue` — radio grant/revoke + 5 multiselect (group/dept/part/cv/cd) + NV bổ sung + permission + dependency cascade + "Tất cả" + validate inline
- [x] `BulkPermissionEmployeeList.vue` — sub-filter + 3 tab chip + b-table tick all/page indeterminate + pagination + refresh + export
- [x] `BulkPermissionBanner.vue` — alert warning + clear loại trừ
- [x] Footer 3 button (Áp dụng / Áp dụng và làm tiếp / Hủy) + validate + reset form khi continueAfter
- [x] Export Excel qua `$axios` blob

---

## Phase 3 — Test E2E

### Test thủ công

- [ ] Preview: chọn từng combo (chỉ Khối, chỉ PB, Khối+CV, …) → DS NV đúng
- [ ] NV bổ sung: chỉ hiện NV không thuộc filter chính
- [ ] Excluded persist khi paging (page 1 → 2 → 1 vẫn nhớ tick)
- [ ] Excluded persist khi đổi sub-filter
- [ ] Excluded persist khi đổi objectFilter, banner hiện, click "Xóa loại trừ" → clear
- [ ] Header tick-all chỉ ảnh hưởng trang hiện tại + indeterminate khi mix
- [ ] Apply grant: NV có Role A,B,C + apply D,E → kết quả A,B,C,D,E (kiểm tra DB `model_has_permissions`)
- [ ] Apply revoke: NV có permission trực tiếp D,E + revoke D → còn E
- [ ] Apply revoke quyền đến từ Role: NV vẫn còn quyền sau revoke (vì Role không bị đụng)
- [ ] Áp dụng và làm tiếp: form reset đầy đủ
- [ ] Export Excel: cột Nguồn đúng (Theo bộ lọc / Bổ sung / Loại trừ)
- [ ] Validate: thiếu đối tượng → inline error; thiếu quyền → inline error
- [ ] Permission middleware: tài khoản không có "Quản lý phân quyền" → 403
- [ ] Scope company: admin company A, thử apply cho NV company B → reject

---

### Checkpoint — 2026-05-27
Vừa hoàn thành: Brainstorming + spec + plan + verify schema DB
Đang làm dở: Chưa code
Bước tiếp theo: Dispatch task 1 — tạo BulkPermissionService
Blocked: Không.

### Checkpoint — 2026-05-28
Vừa hoàn thành: TOÀN BỘ Phase 1 BE (8 task: service + 2 request + controller + export + routes) + TOÀN BỘ Phase 2 FE (4 task: modal + filter + employee-list + banner + footer/export).
Files BE: BulkPermissionService, BulkPermissionController, BulkPermissionPreviewRequest, BulkPermissionApplyRequest, BulkPermissionEmployeesExport + blade, route group `/timesheet/bulk-permissions`.
Files FE: pages/timesheet/setting/roles/index.vue (sửa thêm button), components/timesheet/setting/roles/{BulkPermissionModal, BulkPermissionFilter, BulkPermissionEmployeeList, BulkPermissionBanner}.vue.
Test BE: PHP syntax pass tất cả, autoload OK, SQL query verify đúng cú pháp + chạy thật DB không lỗi schema. Test FE thủ công chưa làm.
Quyết định kiến trúc:
- Bỏ scope company khỏi `employee_has_permissions` (schema chưa có cột) → permission trực tiếp NV là global.
- "Chức danh" = bảng `titles`, "Chức vụ" cột `employee_work_position_id`, "Khối" = `groups` qua `departments.group_id`.
- Lịch sử phân quyền (#10455) defer.
Bước tiếp theo: Phase 3 — test thủ công 13 case trên trình duyệt (cần chạy hrm-client + hrm-api dev).
Blocked: Không.
