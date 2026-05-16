# Plan: Báo cáo chỉ số hoàn thành giải pháp theo version (QLDA_BC_10)

## Trạng thái
- Bắt đầu: 2026-04-06
- Tiến độ: 15/15 task ✅

## Phase 1: Backend — Service + Controller + Route (DONE)

- [x] Task 1: Tạo SolutionVersionsReportService (query, group, aggregate, paginate)
  - buildQuery(): JOIN solution_versions + solutions + companies + departments + employees + prospective_projects
  - Pre-aggregate: leftJoinSub cho tasks, progress_logs, members, modules (tối ưu hiệu năng)
  - groupVersions(): phân cấp Company → Dept → Solution → Version, cộng tổng dồn
  - calculateSummary(): total_versions, avg_days, efficiency
  - paginateHierarchical(): phân trang theo solution
  - getFilterOptions(): companies, departments, employees, customers, solutions
  - getExportData(): lấy tất cả data không phân trang

- [x] Task 2: Tạo Controller + Transformer + Route
  - SolutionVersionsReportController extends ApiController
  - Methods: index(), export(), filterOptions(), versionMembers(), solutionModules()
  - SolutionVersionsReportResource extends ApiResource
  - Routes: GET /, /export, /filter-options, /{versionId}/members, /{solutionId}/modules

## Phase 2: Frontend — Components (DONE)

- [x] Task 3: reportUtils.js (formatNumber, formatHours, formatDateVN, formatPercent, getEffLabel, getVersionStatusClass)
- [x] Task 4: SolutionVersionsTable.vue (bảng phân cấp 4 level, expand/collapse, scroll sync, pagination, loading)
- [x] Task 5: SolutionVersionDetailModal.vue (popup 3 loại: modules, members, progress)
- [x] Task 6: index.vue (trang chính: filter inline dùng V2BaseFilterPanel + V2BaseCompanyDepartmentFilter, table, modal)

## Phase 3: Bảng solution_version_members (DONE)

- [x] Task 7: Migration tạo bảng solution_version_members
- [x] Task 8: Model SolutionVersionMember
- [x] Task 9: SolutionService — method snapshotVersionMembers() + gọi trong createNewVersion()
  - Snapshot: PM + Leaders hạng mục + Solution members + Module members
  - Loại bỏ duplicate, ưu tiên PM > Leader > Member
- [x] Task 10: SolutionVersionMembersSeeder — backfill cho versions đã tồn tại

## Phase 4: Popup chi tiết (DONE)

- [x] Task 11: API versionMembers() — query solution_version_members + leftJoinSub progress_logs cho giờ tham gia
  - Thứ tự: PM → Leader hạng mục → Thành viên (CASE WHEN ORDER BY)
- [x] Task 12: API solutionModules() — query solution_modules + leftJoinSub tasks + progress_logs

## Phase 5: Xuất Excel (DONE)

- [x] Task 13: SolutionVersionsReportExport (FromView pattern)
- [x] Task 14: Blade template solution_versions_report.blade.php
  - Title center, width các cột, format date DD/MM/YYYY
  - Phân cấp: Công ty (xanh) → Phòng (xanh nhạt) → Giải pháp (xám) → Version (trắng)
  - Hiện trạng thái + ngày bắt đầu + ngày chốt cho dòng giải pháp
- [x] Task 15: Frontend exportExcel() dùng $axios.get + responseType arraybuffer + download file

### Checkpoint — 2026-04-07 (2)
Vừa hoàn thành: Fix null pointer bug sendReviewProfileNotification, viết 53 test cases (test-cases.md)
Đang làm dở: không
Bước tiếp theo: Chạy test cases trên UI thực tế, fix bugs nếu có
Blocked:

## Các fix/cải tiến sau khi deploy

- Fix PHP 7.4 syntax (nullsafe operator ?-> → ternary)
- Fix SQL: customers.fullname (không có cột name), xóa deleted_at IS NULL (các bảng không có soft delete)
- Sửa tiếng Việt không dấu trong Table + Modal components
- Dùng V2BaseBadge cho trạng thái version + đánh giá hiệu suất (thay vì status-pill/eff-pill CSS)
- Tối ưu query: correlated subqueries → pre-aggregate leftJoinSub
- Giờ thực tế lấy từ SUM(task_result_progress_logs.hours) thay vì tasks.actual_hours
- Dòng tổng "Tổng toàn bộ version" ở đầu bảng
- Loading spinner trong table khi search
- Pagination UI giống V2BaseDataTable
- Button Xem chi tiết / Xuất Excel / In báo cáo
- Filter dùng V2BaseCompanyDepartmentFilter (ẩn bộ phận) thay vì select thủ công
- Gộp filter vào index.vue, xóa SolutionVersionsFilter.vue
