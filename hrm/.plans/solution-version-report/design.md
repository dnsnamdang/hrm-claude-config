# Design: Báo cáo chỉ số hoàn thành giải pháp theo version (QLDA_BC_10)

## Mục đích
Trang báo cáo theo dõi chỉ số hoàn thành giải pháp theo version, phân cấp Công ty → Phòng GP → Giải pháp → Version. Giúp quản lý theo dõi khối lượng công việc, định mức giờ và hiệu suất.

## Scope

### Bộ lọc
- Công ty, Phòng GP, PM (dùng V2BaseCompanyDepartmentFilter, ẩn bộ phận)
- Khách hàng, Giải pháp, Version (cascade), Thời gian từ/đến

### Bảng dữ liệu
Phân cấp 4 level: Công ty → Phòng GP → Giải pháp → Version
- Dòng tổng "Tổng toàn bộ version" ở đầu bảng
- Expand/collapse theo từng cấp + button "Xem chi tiết" toggle tất cả
- Mặc định chỉ hiện cấp Công ty

### Nhóm cột
1. **THÔNG TIN VERSION** (4 cột): Trạng thái, Ngày bắt đầu làm, Ngày chốt, Số ngày thực hiện
2. **KHỐI LƯỢNG & ĐỊNH MỨC** (5 cột): Số hạng mục, Số nhân sự tham gia, Số task giao, Số giờ được giao (estimated_hours), Số giờ thực tế (SUM task_result_progress_logs.hours)
3. **HIỆU SUẤT** (3 cột): Hiệu suất (%), Task/giờ, Đánh giá (V2BaseBadge: cao ≥100% xanh, trung bình 80-99% vàng, thấp <80% đỏ)

### Popup chi tiết (3 loại)
1. **Chi tiết hạng mục**: Hạng mục, Leader, Giờ giao, Giờ thực tế
2. **Chi tiết nhân sự**: Nhân sự, Vai trò, Giờ tham gia (từ progress logs) — thứ tự: PM → Leader → Thành viên
3. **Tiến độ**: Progress bar + bảng hạng mục với tiến độ %

### Bảng solution_version_members
- Bảng mới lưu snapshot nhân sự theo từng version
- Snapshot khi tạo version mới: PM + Leaders hạng mục + Solution members + Module members
- Loại bỏ duplicate, ưu tiên: PM > Leader > Member
- Seeder backfill cho versions đã tồn tại

### Tính năng khác
- Xuất Excel (FromView pattern, blade template)
- In báo cáo
- Phân trang theo giải pháp
- Loading spinner khi search
- Permission: "Xem báo cáo chỉ số hoàn thành giải pháp theo version"

## Data Structure

### Cách tính các chỉ số
| Chỉ số | Nguồn |
|--------|-------|
| Số hạng mục | COUNT solution_modules WHERE solution_id |
| Số nhân sự | COUNT solution_version_members WHERE solution_version_id |
| Số task giao | COUNT tasks WHERE solution_version_id |
| Số giờ được giao | SUM tasks.estimated_hours WHERE solution_version_id |
| Số giờ thực tế | SUM task_result_progress_logs.hours JOIN tasks WHERE solution_version_id |
| Hiệu suất | estimated_hours / actual_hours × 100 |
| Số ngày thực hiện | end_date - start_date (solution_versions) |
| Ngày chốt | approved_at (solution_versions) |
| Giờ tham gia nhân sự | SUM progress_logs.hours WHERE task.assignee_id = member_id AND task.solution_version_id |
| Trạng thái giải pháp | Trạng thái version cao nhất, text + color từ Solution::STATUSES |

### API endpoints
- `GET /api/v1/assign/report/solution-versions` — data báo cáo + phân trang
- `GET /api/v1/assign/report/solution-versions/export` — xuất Excel
- `GET /api/v1/assign/report/solution-versions/filter-options` — options cho filter
- `GET /api/v1/assign/report/solution-versions/{versionId}/members` — popup nhân sự
- `GET /api/v1/assign/report/solution-versions/{solutionId}/modules` — popup hạng mục

### Tối ưu hiệu năng
- Pre-aggregate bằng leftJoinSub thay vì correlated subqueries
- 4 aggregate subqueries (tasks, progress_logs, members, modules) JOIN 1 lần

## Files

### Backend
- `Modules/Assign/Services/Report/SolutionVersionsReportService.php` — **Tạo mới**: query, group, aggregate, paginate, export
- `Modules/Assign/Http/Controllers/Api/V1/SolutionVersionsReportController.php` — **Tạo mới**: index, export, filterOptions, versionMembers, solutionModules
- `Modules/Assign/Transformers/SolutionVersionsReportResource/SolutionVersionsReportResource.php` — **Tạo mới**
- `Modules/Assign/Routes/api.php` — +route group
- `app/ExcelExport/SolutionVersionsReportExport.php` — **Tạo mới**: FromView export
- `resources/views/exports/solution_versions_report.blade.php` — **Tạo mới**: blade template
- `database/migrations/2026_04_06_100000_create_solution_version_members_table.php` — **Tạo mới**
- `Modules/Assign/Entities/SolutionVersionMember.php` — **Tạo mới**
- `database/seeders/SolutionVersionMembersSeeder.php` — **Tạo mới**
- `Modules/Assign/Services/SolutionService.php` — +method snapshotVersionMembers(), gọi trong createNewVersion()

### Frontend
- `pages/assign/report/solution-versions/index.vue` — **Tạo mới**: trang chính (filter inline, table, modal)
- `pages/assign/report/solution-versions/components/SolutionVersionsTable.vue` — **Tạo mới**: bảng phân cấp
- `pages/assign/report/solution-versions/components/SolutionVersionDetailModal.vue` — **Tạo mới**: popup 3 loại
- `pages/assign/report/solution-versions/components/reportUtils.js` — **Tạo mới**: helpers
