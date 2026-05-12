# Progress Version Snapshot — Plan

**Spec chi tiết:** `docs/superpowers/specs/2026-04-29-progress-version-snapshot-design.md`
**Implementation plan:** `docs/superpowers/plans/2026-04-29-progress-version-snapshot.md`

## Phase 1 — DB Migration

- [x] Task 1: Migration `add_progress_percent_to_solution_versions`
- [x] Task 2: Migration `add_snapshot_columns_to_solution_module_versions`

## Phase 2 — Backend

- [x] Task 3: `SolutionModuleService::createNewVersion` — snapshot weight + progress version cũ, reset progress_percent về 0
- [x] Task 4: `SolutionService::createNewVersion` — snapshot progress version cũ, reset progress_percent về 0
- [x] Task 5: `SolutionService::getProgressByModules` — filter module theo current solution version

## Phase 3 — Frontend

- [x] Task 6: Màn danh sách giải pháp hiển thị version hiện tại + tiến độ tương ứng
