# Plan — Trường "Tiến trình" cho QĐ cử đi đào tạo

@manhcuong · Design: `.plans/assign-training-progress/design.md` · Spec: `docs/superpowers/specs/2026-07-15-assign-training-progress-design.md`

## Phase 1 — Entity

### BE
- [x] `AssignTraining.php`: thêm relation `trainingContracts()` hasMany(TrainingContract, 'assign_training_id')
- [x] `AssignTraining.php`: thêm hằng `PROGRESS_NOT_CREATED=1` / `PROGRESS_INCOMPLETE=2` / `PROGRESS_COMPLETED=3` + mảng `PROGRESS_TEXT`

## Phase 2 — Query + Resource

### BE
- [x] `AssignTrainingService::index()`: thêm `withCount(['assignTrainingStudents as students_count', 'trainingContracts as training_contracts_count' => count distinct student_id])`
- [x] `AssignTrainingService::index()`: thêm filter `training_progress` bằng correlated subquery trong `whereRaw` (KHÔNG dùng alias withCount — MySQL không cho trong WHERE)
- [x] `AssignTrainingResource`: thêm `training_progress` + `training_progress_name`; `count_students` chuyển dùng `students_count` (fallback query nếu thiếu)
- [x] Verify `php -l` sạch 3 file BE

## Phase 3 — FE

### FE
- [x] `index.vue`: thêm field `training_progress` label "Tiến trình" ngay sau `count_students` + slot render badge
- [x] `index.vue`: thêm `listProgress` + `getProgressClass` **LOCAL** (KHÔNG sửa `pages/decision/mixins/common.js` — verify mixin chung 0 dòng liên quan)
- [x] FIX badge: `badge-secondary` KHÔNG tồn tại trong theme (0 chỗ dùng toàn dự án) → render nền TRẮNG vô hình; đổi 'Chưa tạo' sang `badge-info` (theme chỉ có info/warning/success/danger)
- [x] `index.vue`: thêm droplist lọc "Tiến trình" (Select2 + allowClear) trong tìm kiếm nâng cao

## Phase 4 — Verify

- [x] Tinker: công thức đúng 3 ca thật (AT#4=Chưa tạo, AT#1/AT#3=Đã hoàn thành)
- [x] Tinker + transaction rollback: ca "Chưa hoàn thành" (xoá 1 HĐĐT của AT#3 → 2/3), data nguyên vẹn sau rollback
- [x] Tinker: ca QĐ 0 học viên → Chưa tạo
- [x] Đếm query (`DB::listen`): `withCount` gộp, không N+1; so sánh trước/sau
- [x] Tinker/API: filter mỗi giá trị trả đúng tập QĐ; không truyền filter → trả đủ
- [x] Playwright: cột "Tiến trình" render đúng badge + màu, droplist lọc hoạt động, 0 lỗi console
- [x] Kiểm tra `export()` không vỡ (đi qua index())

## Phase 5 — Chuyển vị trí cột + Export Excel (user yêu cầu)

### FE
- [x] `index.vue`: chuyển field `training_progress` từ sau `count_students` → **ngay trước `status`** (Trạng thái)

### BE
- [x] `exports/assign_training.blade.php`: thêm `<td>Tiến trình</td>` vào thead + `{{$item['training_progress_name'] ?? ''}}` vào tbody, ngay trước Trạng thái
- [x] `exports/assign_training.blade.php`: bảng 12→13 cột → nới colspan (tiêu đề/dòng trống/ngày: 12→13; đệm khối chữ ký: 11→12) — không nới thì layout Excel lệch
- [x] Verify thead 13 `<td>` == tbody 13 `<td>`

### Verify
- [x] Playwright: cột "Tiến trình" (11) NGAY TRƯỚC "Trạng thái" (12), thứ tự `Người duyệt -> Tiến trình -> Trạng thái`
- [x] Playwright: badge có màu thật (Chưa tạo bg=rgb(55,205,230) info, Đã hoàn thành bg=rgb(26,188,156) success)
- [x] Playwright: lọc "Chưa tạo" → chỉ còn QĐ chưa tạo
- [x] Playwright: bấm nút "Xuất excel" thật → tải `danh_sach_quyet_dinh_cu_di_dao_tao.xls` (82944 bytes)
- [x] Đọc lại CHÍNH file tải về bằng PhpSpreadsheet: 13 cột, "Tiến trình" ở vị trí 11 ngay trước "Trạng thái", giá trị đúng từng dòng (Đã hoàn thành / Đã hoàn thành / Chưa tạo)
- [x] Ghi nhận: export là `.xls` (BIFF/OLE2) KHÔNG phải `.xlsx` → không đọc bằng zipfile được

### Checkpoint — 2026-07-15
Vừa hoàn thành: Toàn bộ Phase 1-4. 4 file (3 BE + 1 FE), verify pass hết.
Đang làm dở: (không)
Bước tiếp theo: User hard-refresh màn /decision/assign-training kiểm tra cột Tiến trình + bộ lọc.
Blocked: (không)
