# Plan: Progress Manager — Tab Tiến độ

## Trạng thái
- Bắt đầu: 2026-04-02
- Tiến độ: 15/15 task ✅
- Code pushed: ✅

## Phase 1: Cấp Giải pháp (DONE)

### BE — Migration
- [x] Task 1: Migration thêm cột `weight` vào `solution_modules`
- [x] Task 2: Migration thêm cột `weight` vào `tasks`

### BE — API endpoints
- [x] Task 3: Thêm route GET progress + PUT weights
- [x] Task 4: Controller methods `getProgress` + `updateWeights`
- [x] Task 5: Service methods `getProgressData` + `updateProgressWeights`

### FE — Component
- [x] Task 6: Tạo `ProgressTab.vue` (Mode 1: hạng mục, Mode 2: tasks)
- [x] Task 7: Tích hợp tab vào `manager.vue`

### Bugfix
- [x] Task 8: Fix solutionId prop type + apiPutMethod payload key
- [x] Task 9: Fix solutionId null initialization

## Phase 2: Cấp Hạng mục (DONE)

### BE — API
- [x] Task 10: Thêm 2 routes vào `{solutionModule}/manager` group
- [x] Task 11: Controller + Service methods cho module progress

### FE — Refactor + Tích hợp
- [x] Task 12: Refactor ProgressTab.vue — thêm props apiPrefix, canEdit, humanResourceUrl
- [x] Task 13: Cập nhật cấp GP truyền props mới
- [x] Task 14: Tích hợp vào solution-modules/_id/manager.vue
- [x] Task 15: Test cả 2 cấp — 18/18 test cases PASS, fix thêm 1 bug (isPM→canEdit sót)

## Checkpoint

### Checkpoint — 2026-04-02 (Final)
Vừa hoàn thành: Push code lên GitHub
- BE: `origin/progress-manager` trên `DNS-Media/hrm-api`
- FE: `origin/progress-manager` trên `DNS-Media/hrm-client`
Đang làm dở: không
Bước tiếp theo: Tạo PR merge vào `tpe-develop-assign` (nếu cần)
Blocked: không
