# Plan: Lưu và duyệt — Giải pháp không có hạng mục

## Trạng thái
- Bắt đầu: 2026-04-07
- Tiến độ: 2/2 task ✅

## Phase 1: Thêm nhánh "Lưu và duyệt" khi has_modules = false (DONE)

### FE — Button logic
- [x] Task 1: Sửa `nextStatus` + `submitButtonText` trong `edit.vue` — khi CHO_PM_DUYET + has_modules=false → button "Lưu và duyệt", next status = DANG_TRIEN_KHAI

### BE — Cho phép transition + set start_date
- [x] Task 2: Uncomment logic set `start_date` trong `SolutionService.php` khi chuyển sang DANG_TRIEN_KHAI (cover cả case có/không hạng mục)

## Checkpoint

### Checkpoint — 2026-04-07
Vừa hoàn thành: Implement xong cả FE + BE
- FE: `hrm-client/pages/assign/solutions/_id/edit.vue` — sửa computed nextStatus + submitButtonText
- BE: `hrm-api/Modules/Assign/Services/SolutionService.php` — uncomment đoạn set start_date
Đang làm dở: không
Bước tiếp theo: Test thủ công 2 case (có hạng mục / không hạng mục)
Blocked: không
