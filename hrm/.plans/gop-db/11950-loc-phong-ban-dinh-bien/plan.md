# Lọc theo phòng ban định biên — DS ban hành/thay đổi định biên (#11950) — @cuong61n

Redmine: http://quanly.dnsmedia.vn/issues/11950 · Màn: Quyết định → Ban hành/thay đổi định biên (`/decision/manpower-planning`)
Yêu cầu: bộ lọc thêm "Phòng ban định biên" — droplist chọn nhiều, lấy DM phòng ban mọi trạng thái (phòng đã khoá đánh dấu 🔒), chỉ hiện QĐ chứa ĐỦ TẤT CẢ phòng đã chọn.
Nhánh: `gop_db` (prod chạy gop_db) — worktree `worktrees/gop_db-api` + `worktrees/gop_db-client`, chưa commit.

## Phase 1 — Thêm bộ lọc

### BE (hrm-api)
- [x] 30/10/2026 Lọc `manpower_department_ids` (chuỗi `1,2,3`) trong `ManpowerPlanningService::index` — mỗi phòng 1 `whereExists` trên `manpower_departments` ⇒ QĐ phải chứa đủ mọi phòng (AND). Xuất Excel + In dùng chung `index` nên tự áp lọc.
- [x] 30/10/2026 Endpoint `GET decision/manpower-planning/filter-departments`: phòng ban công ty hiện tại (hoặc `company_id`), MỌI trạng thái, `is_locked = status != 1`.
- [x] 30/10/2026 Migration index `(manpower_planning_id, department_id)` trên `manpower_departments` (`2026_10_30_000001_...`) — đã chạy local.
- [x] 30/10/2026 Kiểm tinker DB local: 1 phòng (5 → QĐ 4,5; 42 → 5) · nhiều phòng (5,36 → 4,5; 5,36,42 → 5; 5,999 → rỗng) · không lọc → đủ 5 QĐ · options 39 phòng, 14 khoá. ĐẠT.

### FE (hrm-client)
- [x] 30/10/2026 `pages/decision/manpower-planning/index.vue`: thêm Select2 chọn nhiều "Chọn phòng ban định biên" (cùng kiểu Select2 các ô lọc khác của màn), 🔒 qua `withLockedOptionMarker`; danh mục chỉ tải khi mở Bộ lọc lần đầu; truyền tham số vào danh sách, Xuất Excel, In; nút làm mới xoá lựa chọn.
- [x] 30/10/2026 User chê ô Select2 multiple xấu, viền lệch màu → đổi sang component chung `components/CheckboxMultiSelect.vue` (copy pattern bộ lọc Cấp bậc/Chức vụ `pages/human/employee_info/index.vue:155`); option map `{id, name, is_locked}`.
- [x] 30/10/2026 Bổ sung 🔒 cho `CheckboxMultiSelect` (user đồng ý sửa component chung): `displayName()` gắn `LOCKED_OPTION_PREFIX` ở chip + dòng chọn khi option có `is_locked`; 11 màn đang dùng không truyền cờ nên không đổi.
- [x] 30/10/2026 Chỉnh cao ô lọc bằng các ô khác (chỉ màn này): đo Playwright các ô select2/ô ngày của bộ lọc = 35.6px, `CheckboxMultiSelect` mặc định 32px → scoped `.manpower-department-filter ::v-deep .csp-control { min-height: 35.6px }`.
- [x] 30/10/2026 Test UI cổng 3002 (gop_db-client → API 8003): ô rỗng cao 35.6px = các ô khác · danh sách 39 phòng, 14 có 🔒 · chọn 3 phòng (gồm phòng khoá MAR) → chip có 🔒, 0 bản ghi (đúng, không QĐ nào đủ 3) · bỏ MAR còn HN_QTTT + HN_KD2 → 2 bản ghi (đúng QĐ 4,5). Ghi chú: có chip thì ô giãn (2 chip = 56px) vì tên phòng dài, mỗi chip 1 dòng — hành vi sẵn của CheckboxMultiSelect.
- [ ] Chưa test Xuất Excel / In theo lọc.
- [ ] Commit + push `gop_db`, deploy (nhớ `php artisan migrate` + `route:cache` trên PROD).

### Checkpoint — 30/10/2026
Vừa hoàn thành: BE + FE bộ lọc phòng ban định biên, test BE bằng tinker đạt.
Đang làm dở: —
Bước tiếp theo: test UI → commit/push gop_db → deploy.
Blocked:
