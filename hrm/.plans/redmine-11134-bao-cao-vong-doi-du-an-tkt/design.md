# Redmine #11134 — Báo cáo vòng đời dự án TKT

Người phụ trách: @khoipv — Nhánh: `fix-bug-11092026` (hrm-api + hrm-client)

## Mục tiêu

Màn **Báo cáo → `/assign/report/prospective-projects`**:

1. Đổi tên báo cáo: "Báo cáo tổng hợp dự án TKT theo Phòng ban - Nhân viên KD" → **"Báo cáo vòng đời dự án TKT"**
   (tiêu đề trang, tab trình duyệt, menu sidebar, trang in, file Excel, tên hiển thị của quyền).
2. Đổi nhãn:
   - "Giai đoạn dự án" → **"Giai đoạn dự án khách hàng"** (bộ lọc + cột popup danh sách)
   - "Tiến trình nội bộ" → **"Tiến trình dự án"** (bộ lọc + cột "Cơ cấu tiến trình" + popup)
3. Thêm cột **"Cơ cấu giai đoạn dự án"** trong nhóm cột `DỰ ÁN TKT`, ngay sau "Cơ cấu tiến trình".

## Quyết định đã chốt (hỏi user 11/09/2026)

- Ticket viết "Trạng thái dự án" theo tên cũ; màn đang hiển thị "Tiến trình nội bộ" → đổi chỗ này thành
  "Tiến trình dự án".
- Cột mới hiển thị **giống "Cơ cấu tiến trình"**: nút + icon biểu đồ, bấm mở popup thống kê số dự án theo
  từng giai đoạn kèm %.
- Quyền: chỉ đổi `display_name` (chỗ hiển thị ở màn Phân quyền), **GIỮ NGUYÊN `name`** vì `name` là khoá
  `isCurrentEmployeeHasPermission()` / `hasAPermission()` — đổi `name` mà DB prod chưa update sẽ khiến
  toàn bộ user mất quyền xem báo cáo (fail-closed).

## Phạm vi kỹ thuật

**BE (`hrm-api`)**
- `Modules/Assign/Services/Report/ProspectiveProjectsReportService.php`: thêm chiều cơ cấu
  `project_phase_counts` (company / phòng ban / NVKD / tổng) — cùng khuôn với scope/industry/application.
- `Modules/Assign/Transformers/ProspectiveProjectsReportResource/ProspectiveProjectsReportResource.php`:
  trả thêm `project_phase_count` + `project_phase_counts` ở cả 3 cấp và ở summary.
- `resources/views/exports/prospective_projects_report.blade.php`: đổi tiêu đề.
- `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`: đổi `display_name` 3 quyền 1054–1056.

**FE (`hrm-client`)**
- `pages/assign/report/prospective-projects/index.vue`: tiêu đề + nhãn popup + dựng dữ liệu `phase`.
- `.../components/ProspectiveProjectsTable.vue`: thêm cột + đổi nhãn.
- `.../components/ProspectiveProjectsFilter.vue`, `.../components/ProspectiveListModal.vue`: đổi nhãn.
- `pages/assign/report/prospective-projects/print.vue`: đổi tiêu đề bản in.
- `components/menu-sidebar.js`: đổi nhãn menu.

## Không đổi

- Excel + bản in KHÔNG thêm cột mới (2 nơi này vốn không có cột "Cơ cấu tiến trình" — cơ cấu chỉ xem qua popup).
- `name` của permission, id quyền, route, tên key API cũ (`scope_*`, `industry_*`).
