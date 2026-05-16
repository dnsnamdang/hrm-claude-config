# Plan: subjects-list-ui

**Plan chi tiết:** [docs/superpowers/plans/2026-04-25-subjects-list-ui.md](../../docs/superpowers/plans/2026-04-25-subjects-list-ui.md)

## Tasks tổng quát

- [x] Task 1: Fix bug `exportExcel` — `this.formFilter` → `this.filters`
- [x] Task 2: Fix bug `lockItem` / `unlockItem` — `this.getData()` → `this.loadData()`
- [x] Task 3: Fix conflict `getTrainingTypes()` vs computed `trainingTypes`
- [x] Task 4: Fix CSS `::v-deep .data-table tbody tr:hover .row-actions`
- [x] Task 5: Thêm nút lock toggle + 2 method + CSS vào `#cell-status`
- [x] Fix Critical: modal ID `modal-warning-lock-timesheet` + xóa dead code `onEditClick`/`eventHandler`
- [x] Fix UI: status pill dùng global class `tpl-status-*` từ `v2-styles.scss`, xóa local CSS override gây font-size lớn

### Checkpoint — 2026-04-25

Vừa hoàn thành: Toàn bộ 5 task + critical fix + UI polish status pill
Đang làm dở: —
Bước tiếp theo: Manual test trên browser (lock/unlock flow, export excel, hover row actions, status badge)
Blocked: —
