# Plan — role-permission-history

Người phụ trách: @khoipv

## Phase 1 — Lịch sử phân quyền chức vụ (setting/roles)

### BE
- [x] T1. Migration `role_permission_history` (module Timesheet, PHPDoc up/down) — ĐÃ migrate 2026_07_14_000012
- [x] T2. Entity `Modules\Timesheet\Entities\RolePermissionHistory` (+ user → Human\Employee)
- [x] T3. `RoleService`: buildRoleSnapshot (resolve tên company/permission qua DB, sort ổn định) + logRoleHistory + hook save() (create log 'create'; update chụp snapshot trước mutation → so JSON → log 'update') + roleHistories sort cũ→mới
- [x] T4. `RoleController::histories(Request)` (đọc role_id, responseJson 3-arg) + delete() chụp snapshot trước xóa → log 'delete'
- [x] T5. Route `GET timesheet/roles/histories` đặt TRƯỚC `/{id}`

### FE
- [x] T6. `components/setting/roles/RolePermissionHistoryModal.vue` (full-snapshot: create/delete render snapshot; update diff Tên/Ghi chú/Vị trí cũ→mới + Công ty +/− + Quyền theo công ty +/−; bộ lọc Thao tác/Người/ngày; dot create xanh/update amber/delete đỏ)
- [x] T7. Màn danh sách `roles/index.vue`: dropdown-item "Lịch sử thay đổi" giữa Sửa/Xóa + gắn modal + openHistory(item)
- [x] T8. Màn Sửa `roles/add/_id.vue`: ~~nút light ri-history-line cạnh Lưu~~ → ĐÃ GỠ (2026-07-14, user yêu cầu chỉ hiển thị lịch sử ở màn danh sách). Chỉ còn màn danh sách có nút xem lịch sử.

### Verify
- [x] T9. `php -l` sạch + tinker round-trip THẬT: create→1 log(create, old=null); update đổi tên+quyền→1 log(update diff); no-op update→KHÔNG log thêm; delete→1 log(delete, new=null); roleHistories format/sort/changed_by_name đúng. Dọn sạch role test + logs (TOTAL=0)
- [x] T10. Playwright: chèn 3 log test cho role 29 → màn danh sách dropdown có mục "Lịch sử thay đổi" → mở modal render đủ 3 nhánh (Tạo xanh snapshot / Cập nhật Tên đỏ→xanh + chip +xanh/−đỏ / Xóa đỏ snapshot), header "29 - ...", sort cũ→mới; màn Sửa hiện nút light "Lịch sử thay đổi" giữa Lưu/Quay lại; network GET histories 200 KHÔNG POST store
- [x] T11. Dọn log test (ids 4,5,6 role 29) → TOTAL=0; xóa 2 ảnh screenshot test

### Phase 1.1 — Chi tiết phân quyền theo cây (2026-07-14, inline Opus 4.8)
User yêu cầu: "Chi tiết phân quyền phải chỉ rõ tab công ty nào, phân hệ, phần nào".
- [x] T12. BE `buildRoleSnapshot`: đổi permissions từ `permission_names:[]` phẳng → `items:[{module_type, module, group, name}]` (join permissions lấy type/group/display_name; sort theo phân hệ→phần→tên) + hằng `MODULE_LABELS` (type 1-7)
- [x] T13. FE modal: render CÂY Công ty→Phân hệ→Phần→Quyền cho snapshot (create/delete) + change-tree (update) qua helper groupByModuleGroup/buildChangeTree/buildSnapshotTree; CSS perm-detail/perm-company/perm-module/perm-group
- [x] T14. Verify Playwright: chèn 3 log format mới role 29 → modal render cây đúng (Tạo: chấm công/giao việc chip xanh; Cập nhật: −Bảng chấm công tổng hợp đỏ ở phân hệ chấm công + +Xem bảng lương test xanh ở phân hệ tính lương; Xóa: cây chip đỏ). Dọn log test TOTAL=0.
- [x] T15. ⚠️ PHÁT HIỆN + xử lý phantom write: role 29 bị lưu thật 16:26:21 thêm 3 quyền chấm công (perm 2/32/363) → hỏi user → user chọn "Giữ data, xóa log" → giữ 6 quyền role 29, xóa log phantom. TOTAL=0.

### Checkpoint — 2026-07-14 (inline Opus 4.8)
Vừa hoàn thành: Phase 1 + Phase 1.1 (Chi tiết phân quyền theo cây Công ty→Phân hệ→Phần→Quyền) — CODE DONE + VERIFIED.
Đang làm dở: (không)
Bước tiếp theo: user verify browser bằng mắt (tạo/sửa/xóa 1 chức vụ thật → mở lịch sử) + quyết định merge/commit (chưa git).
Blocked:
