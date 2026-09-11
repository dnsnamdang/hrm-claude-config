# Plan — Báo cáo meeting theo dự án (bỏ cấp Công ty/Phòng ban/Bộ phận)

Nhánh: `tpe` (API :8005, Client :3005) · Người phụ trách: @namdangit

## Yêu cầu
- Bảng báo cáo bỏ 2 cấp Công ty / Phòng ban (và Bộ phận), chỉ còn **Dự án → Meeting**
- Phân quyền xem còn 2 mức: **Theo tổng công ty** / **Theo công ty**
- Bộ lọc: giữ ô **Công ty**, bỏ ô Phòng ban + Bộ phận
- Không có quyền nào → giữ nguyên: chỉ thấy dự án mình tạo / mình là NVKD chính

## Phase 1 — BE
- [x] `MeetingByProjectsService::applyPermissionFilter` bỏ nhánh quyền phòng ban
- [x] `getFilteredQuery` bỏ lọc `department_id` / `part_id`
- [x] `getData` gom phẳng theo dự án (bỏ 2 vòng group công ty/phòng ban + 2 vòng recalc participants)
- [x] `MeetingByProjectsResource` đổi sang field cấp dự án
- [x] Blade `exports/meeting_by_projects_report.blade.php` bỏ dòng Công ty / Phòng
- [x] `PermissionsTableSeeder` xoá quyền id 1062 (theo phòng ban)

## Phase 2 — FE
- [x] `index.vue`: bộ lọc chỉ còn Công ty (`disable_department/part/employee`), bỏ `department_id`/`part_id` khỏi filters
- [x] `index.vue`: cờ quyền fail-closed (bỏ `|| true`), expand/collapse theo cấp dự án
- [x] `MeetingByProjectsTable.vue`: bảng 2 cấp Dự án → Meeting
- [x] `print.vue`: bản in 2 cấp

## Phase 3 — Fix UI
- [x] `components/TopProjectsChart.vue`: bảng "Chi tiết theo biểu đồ" bỏ `.sticky-top` của Bootstrap (z-index 1020 > topbar 1001 nên header bảng nổi đè header trang) → class riêng `.chart-detail-head` z-index 2; khung cuộn đổi `max-h-[380px]` (class Tailwind không tồn tại trong project) → `.chart-detail-scroll` max-height 380px

### Checkpoint — 2026-09-07
Vừa hoàn thành: toàn bộ Phase 1 (BE) + Phase 2 (FE)
Đang làm dở: chưa chạy thử trên trình duyệt (chờ user xác nhận có test không)
Bước tiếp theo: test màn /assign/report/meeting-by-projects, cân nhắc xoá bản ghi quyền id 1062 còn trong DB dev
Blocked:
