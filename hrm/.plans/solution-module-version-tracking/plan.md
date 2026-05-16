# Plan: Liên kết solution_module_versions với solution_versions

## Trạng thái
- Bắt đầu: 2026-04-07
- Tiến độ: 6/6 task ✅

## Phase 1: Migration + Model (DONE)

### BE — Migration
- [x] Task 1: Migration thêm cột `solution_version_id` vào `solution_module_versions`
- [x] Task 2: Migration thêm cột `solution_module_id` + `solution_module_version_id` vào `solution_version_members`

### BE — Model
- [x] Task 3: Thêm relationship `solutionVersion()` vào `SolutionModuleVersion.php`

## Phase 2: Gán giá trị khi tạo/snapshot (DONE)

### BE — Service
- [x] Task 4: `SolutionService.php` — khi tạo module version đầu tiên, gán `solution_version_id`
- [x] Task 5: `SolutionModuleService.php` — khi tạo version mới cho module, gán `solution_version_id`
- [x] Task 6: `SolutionService.php` — snapshotVersionMembers gán `solution_module_id` + `solution_module_version_id` cho Leaders và Module Members

## Checkpoint

### Checkpoint — 2026-04-07
Vừa hoàn thành: 6/6 task
- Migration 1: `2026_04_07_100000_add_solution_version_id_to_solution_module_versions_table.php`
- Migration 2: `2026_04_07_110000_add_module_columns_to_solution_version_members_table.php`
- Model: `SolutionModuleVersion` thêm relationship `solutionVersion()`
- SolutionService: syncModules gán `solution_version_id`, snapshotVersionMembers gán `solution_module_id` + `solution_module_version_id`
- SolutionModuleService: createNewVersion gán `solution_version_id`
Đang làm dở: không
Bước tiếp theo: Chạy migration + test
Blocked: không
