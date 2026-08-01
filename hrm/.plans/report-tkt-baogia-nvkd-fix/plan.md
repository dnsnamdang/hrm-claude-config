# Plan — Fix báo cáo "Dự án TKT theo PB - NV KD" (Redmine #10819)

Màn: `/assign/report/prospective-projects`
Nguồn: http://quanly.dnsmedia.vn/issues/10819 — @Manh Cuong

## Phase 1 — Nhóm cột BÁO GIÁ đang hiển thị 0

Quyết định: BG hợp lệ = status IN (2 Chờ TP duyệt, 3 Chờ BGĐ duyệt, 4 Đã duyệt, 7 Trúng thầu) — loại 1 Đang tạo, 5 Đóng, 6 Dừng.
Giá trị BG = SUM(total_after_vat) của tất cả BG hợp lệ. Liên kết: `quotations.project_id = prospective_projects.id`.

### BE

- [x] `ProspectiveProjectsReportService::buildQuery` — thêm subquery `quotation_count`, `quotation_value` theo từng dự án
- [x] `groupProjects` — cộng dồn `quote_project_count` / `quotation_count` / `quotation_value` ở cả 3 cấp
- [x] `normalizeGroupedData` — tính `quote_rate` = dự án có BG / tổng dự án
- [x] `calculateSummary` — tổng BG toàn báo cáo
- [x] `ProspectiveProjectsReportResource` — trả 4 field mới ở cả 3 cấp
- [x] Blade `exports/prospective_projects_report.blade.php` — thay số 0 hardcode bằng dữ liệu thật

### FE

- [x] `index.vue::createMetricsFromNode` — map `quoteProjects/quotes/quoteValue/quoteRate` từ API
- [x] `index.vue` — bỏ chặn popup ô Dự án có báo giá / Số lượng báo giá, bỏ chú thích "chưa có dữ liệu backend"
- [x] `print.vue` — hiển thị đúng cột BÁO GIÁ

## Phase 2 — Lọc NVKD ra danh sách rỗng

Giả thuyết: 1 `employee_info` có nhiều dòng `employees` → dropdown lấy `employees.id` của dòng này, dự án lưu dòng khác → lọc ra 0.

- [x] Dựng dữ liệu giả lập trên local (employee_info nhiều dòng employees) để tái hiện
- [x] `applyFilters` + `applyProjectListFilters` — lọc theo mọi `employees.id` cùng `employee_info_id`
- [x] `groupProjects` — gom nhóm NVKD theo `employee_info_id` để không tách 2 dòng trùng tên
- [x] Verify lại bằng script tinker (có/không lọc NVKD)

### Checkpoint — 2026-07-27
Vừa hoàn thành: Phase 1 (nhóm cột BÁO GIÁ lấy dữ liệu thật) + Phase 2 (lọc NVKD quy về employee_info). Code ở repo HRM-tpe, nhánh `tpe` (API + Client).
Đang làm dở: chưa test trên UI thật (mới verify qua tinker + SQL).
Bước tiếp theo: chạy FE/BE dev, mở màn báo cáo kiểm tra nhóm cột BÁO GIÁ + popup, rồi phản hồi Redmine #10819.
Blocked:
