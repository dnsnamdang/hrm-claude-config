# Báo cáo Thị trường – Dự án: panel chi tiết meeting dùng chung + nới quyền xem

Nhánh: `gop_db-report-meeting-drawer` (hrm-api + hrm-client), worktree `websites/wt-report-meeting-drawer` (cổng 8022/3022).
User cho phép code 05/10/2026. Chưa merge gop_db.

## Quyết định đã chốt
- Người có quyền báo cáo mở được chi tiết meeting trong **đúng phạm vi QUYỀN của báo cáo** (không xét trạng thái / kỳ),
  giống 4 báo cáo đã làm trước (meeting theo dự án, meeting theo NV, tổng hợp CSKH tiềm năng, nhu cầu dịch vụ).
- Mọi báo cáo mở panel meeting dùng `components/report/ReportMeetingDetailDrawer.vue` — header cố định
  `linear-gradient(135deg, #0a1c3d, #06b6d4)` (màu đầu popup `V2BaseReportModal`).

## Tasks
- [x] BE: `MeetingByMarketService` + `PotentialCustomerCareService` — thêm `hasReportPermission()`, `applyPermissionFilter()` → public
- [x] BE: `Meeting::canView()` + `canViewByReportScope($report)` dùng chung hàm lọc quyền của báo cáo (1174–1176, 1179–1181)
- [x] BE test: `tests/Feature/ReportMeetingView/MeetingCanViewTest.php` (6 ca, RED → GREEN); hồi quy 4 bộ MeetingByEmployees/Projects/ServiceDemand/PotentialCustomerTracking xanh
- [x] FE: component `ReportMeetingDetailDrawer` + chuyển 6 trang (meeting-by-market, potential-customer-care, potential-customer-tracking, service-demand, meeting-by-projects, meeting-by-employees)
- [x] E2E: `e2e/tests/assign/report-meeting-drawer.spec.ts` (4 ca, xanh trên 3022; đỏ trên code cũ: panel trống 403 + header tím)
- [ ] Merge gop_db (chờ user)

## Ngoài phạm vi
- Panel "Kế hoạch & kết quả làm việc theo NV" là panel ĐẦU VIỆC (dữ liệu sẵn trong dòng, không gọi API meeting), header đã cùng gradient.
- Comment `@deprecated meetingId` trong `WorkItemDetailDrawer.vue` còn nhắc 2 màn cũ dùng `:meeting-id` — nay không còn màn nào, chưa dọn.

### Checkpoint — 2026-10-06 (wrap up)
Vừa hoàn thành: nới Meeting::canView cho 2 báo cáo thị trường (1174–1176, 1179–1181) qua canViewByReportScope + component
dùng chung ReportMeetingDetailDrawer cho 6 báo cáo. Nhánh `gop_db-report-meeting-drawer` (worktree
`websites/wt-report-meeting-drawer`, api 8022 · client 3022): api 007396696, client 1b030dbb1. PHPUnit 6/6 + 4 bộ liên quan
135/135; e2e `e2e/tests/assign/report-meeting-drawer.spec.ts` 4/4 (đỏ trên code cũ).
Đang làm dở: không. Bước tiếp theo: chờ lệnh merge gop_db. Chưa push.
Blocked:
- [x] 06/10: ĐÃ MERGE + PUSH gop_db (api b64c15d07, client fa6df767d)
