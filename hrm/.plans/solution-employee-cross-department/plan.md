# Plan — solution-employee-cross-department

Spec: `docs/superpowers/specs/2026-05-20-solution-employee-cross-department-design.md`
Design: `.plans/solution-employee-cross-department/design.md`

## Phase 1 — Mở rộng dropdown FE

### BE
- [x] Verify `/users/auth/user-profile` payload — `AuthNewController:168-186` đã filter sẵn `company_id` + `status=1`. KHÔNG cần sửa BE store.

### FE
- [x] Tạo helper `utils/assign/employee-options.js` với `getAllEmployeeOptions(store)`
- [x] `SolutionForm.vue`: bỏ filter phòng trong `populateInternalMembers()`, dùng helper; gỡ re-populate ở watcher `solution.department_id`; gỡ prop `:department-id`
- [x] `ModulesTab.vue`: gỡ `activeDepartmentId`, `leaderOptions`/`memberOptions` dùng helper; gỡ prop `departmentId`
- [x] `RequestSolutionReceiveModal.vue`: bỏ filter `department_id == receive_dept`, dùng helper (giữ telephone qua employeeMap)
- [x] `InfoTab.vue`: `pmSelectOptions` dùng helper (đây mới là PM dropdown thực tế ở màn add — phát hiện sau khi user báo)
- [x] `manager/HumanResourceTab.vue`: gỡ `pmDepartmentId` + `sameDeptEmployeesOptions`, `availableMembersOptions` lấy toàn nhân sự (chỉ trừ những người đã gán vào module)
- [x] `solution-modules/_id/components/HumanResourceTab.vue`: gỡ `leaderDepartmentId` + `sameDeptEmployeesOptions`, `availableMembersOptions` lấy toàn nhân sự (phát hiện khi rà soát regression)

## Phase 2 — Phân quyền BE xem Solution

### BE
- [x] `SolutionService::index()`: bọc `checkPermissionList` + OR clauses `pm_id` / modules.leader_id / members.member_id / modules.members.member_id
- [x] Rà soát: `show()` (SolutionController:96) không có permission check → leader/member chỉ cần thấy trong list là mở chi tiết được. Chỉ sửa `index()`.
- [ ] Benchmark `pluck('id')` nếu dataset lớn (TODO khi deploy)

## Phase 3 — Test thủ công

- [ ] TC1: PM phòng khác phòng tiếp nhận
- [ ] TC2: Leader module phòng khác + nhận notification
- [ ] TC3: Member phòng khác + thấy solution trong danh sách
- [ ] TC4: Không hiện nhân sự đã nghỉ
- [ ] TC5: Không hiện nhân sự công ty khác
- [ ] TC6: Đổi phòng tiếp nhận không reset PM/Leader/Member
- [ ] TC7: Modal Tiếp nhận chọn PM phòng khác
- [ ] TC8: Leader phòng khác thấy solution trong danh sách
- [ ] TC9: Member phòng khác thấy solution trong danh sách
- [ ] TC10: Notification → mở được chi tiết
- [ ] TC11: User không liên quan + không quyền → không thấy (no leak)
- [ ] TC12: Regression báo cáo

## Checkpoints

### Checkpoint — 2026-05-20
Vừa hoàn thành: brainstorming + spec + design + plan
Đang làm dở: chưa bắt đầu code
Bước tiếp theo: verify payload BE → bắt đầu Phase 1 BE rồi FE
Blocked: không

## Phase 4 — Cột Phòng ban trong bảng phân công nhân sự (2026-05-21)

### BE
- [x] Migration `2026_05_21_000001_add_department_id_to_solution_module_members_table.php`: thêm cột `department_id` nullable + index
- [x] `SolutionService::syncModuleMembers`: lưu `department_id` từ request
- [x] `SolutionService::syncMembers` (cho solution_members — bảng đã có sẵn cột department_id): lưu `department_id` từ request
- [x] `SolutionService::getAll`: thêm `department_id` vào eager-load select cho `modules.members` VÀ `members`
- [x] `DetailSolutionResource`: trả về `department_id` cho cả staff cấp module + staff cấp solution

### FE
- [x] Helper `employee-options.js`: thêm `getEmployeeOptionsByDepartment`, `getActiveDepartmentOptions`, `getEmployeeDepartmentId`
- [x] `ModulesTab.vue`:
  - Thêm cột "Phòng ban" trước cột "Nhân sự" trong bảng staff
  - Computed `departmentOptions`
  - `getMemberOptionsForModule(module, row, idx)` filter theo `row.department_id` nếu có
  - `onStaffDepartmentChange(row)`: clear member_id nếu không thuộc phòng mới
  - `onStaffMemberChange(row)`: auto-set `row.department_id` từ phòng nhân viên
  - `addStaffRow`: init `department_id: null`
  - Watcher modelValue: backfill `department_id` cho dữ liệu cũ
  - Sửa colspan empty state
- [x] `InfoTab.vue` (bảng phân công khi solution KHÔNG có hạng mục):
  - Áp dụng cùng logic như ModulesTab (cột Phòng ban + filter + auto-fill + backfill)

### Test
- [ ] Chạy migration
- [ ] Tạo solution mới: chọn phòng ban trước → list nhân sự filter đúng
- [ ] Chọn nhân sự trước → phòng ban tự fill
- [ ] Đổi phòng ban khi đã chọn nhân sự khác phòng → member_id bị clear
- [ ] Edit solution cũ (legacy data): phòng ban auto-fill từ phòng của member
- [ ] Save → reload → phòng ban giữ đúng từ DB

### Checkpoint — 2026-05-20 (code DONE)
Vừa hoàn thành: Phase 1 FE (4 file) + Phase 2 BE (1 file).
- FE: tạo `utils/assign/employee-options.js`, sửa `SolutionForm.vue`, `ModulesTab.vue`, `RequestSolutionReceiveModal.vue` — toàn bộ dropdown PM/Leader/Member lấy toàn nhân sự công ty (API user-profile đã filter sẵn company_id + status=1).
- BE: `SolutionService::index()` mở rộng permission scope bằng OR clauses `pm_id` / modules.leader_id / members.member_id / modules.members.member_id.
- Phát hiện quan trọng: `AuthNewController:168-186` đã filter sẵn → không cần thêm field vào store, không cần filter lại ở FE.
Bước tiếp theo: test thủ công 12 TC (Phase 3).
Blocked: không
