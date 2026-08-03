# Plan — employee-permission-history

Người phụ trách: @khoipv

## Phase 1 — Lịch sử phân quyền người dùng (setting/employees)

### BE
- [x] T1. Migration `employee_permission_history` (module Timesheet, PHPDoc up/down) — ĐÃ migrate 2026_07_14_000011
- [x] T2. Entity `Modules\Timesheet\Entities\EmployeePermissionHistory` (+ user → Employee)
- [x] T3. `EmployeeService`: buildPermissionSnapshot (resolve tên roles/company/department/part, sort) + logPermissionHistory (full-snapshot diff) + hook storeRole (chụp trước mutation, log sau) + permissionHistories sort cũ→mới
- [x] T4. `EmployeeController::histories(Request)` (đọc employee_id, responseJson 3-arg)
- [x] T5. Route `GET timesheet/employees/histories` đặt TRƯỚC `/{id}`

### FE
- [x] T6. `components/setting/employee-permission/EmployeePermissionHistoryModal.vue` (full-snapshot diff: roles chip +xanh/−đỏ, all_department Có/Không, manager thêm/bỏ; bộ lọc Người/ngày)
- [x] T7. Màn Sửa `_id/index.vue`: nút light ri-history-line cạnh Lưu/Quay lại + gắn modal
- [x] T8. Màn danh sách `index.vue`: dropdown-item "Lịch sử thay đổi" cạnh "Sửa" + gắn modal

### Verify
- [x] T9. `php -l` sạch + tinker Part A (buildPermissionSnapshot resolve tên đúng; logPermissionHistory fake-old→insert, old==current→không insert) + Part B round-trip storeRole THẬT emp 1367 (lưu y hệt→0 log; thêm role→1 log diff đúng; khôi phục→snapshot == trước test) + permissionHistories format/sort
- [x] T10. Playwright: màn Sửa nút→modal render đủ nhánh (roles chip +xanh/−đỏ, all_department Không→Có, manager thêm/bỏ Công ty›Phòng ban—Bộ phận), GET histories 200 KHÔNG POST; màn danh sách dropdown có mục + mở modal đúng nhân viên; route /histories không nuốt /{id}; 0 lỗi console (trừ warning `items` có sẵn không liên quan)
- [x] T11. Dọn log test bằng tinker (remaining=0), KHÔNG mutate quyền thật (round-trip khôi phục)

### Checkpoint — 2026-07-14 15:52 (inline Opus 4.8)
Vừa hoàn thành: toàn bộ Phase 1 — CODE DONE + VERIFIED (tinker + Playwright).
Đang làm dở: (không)
Bước tiếp theo: user verify browser bằng mắt (đổi quyền 1 user thật → mở lịch sử) + quyết định merge/commit (chưa git).
Blocked:
