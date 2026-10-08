# Báo cáo Thị trường – Dự án: panel chi tiết meeting dùng chung + nới quyền xem — tóm tắt

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-05-report-meeting-drawer-design.md` · Plan: `plan.md` cùng thư mục.

## Mục tiêu
- Người CHỈ có quyền báo cáo mở được panel chi tiết meeting từ mọi báo cáo Thị trường – Dự án (trước đó 2 báo cáo trả 403,
  panel trống): Kết quả meeting theo thị trường, Kết quả CSKH tiềm năng.
- 6 báo cáo dùng chung 1 panel `components/report/ReportMeetingDetailDrawer.vue`, header gradient của popup báo cáo.

## Quyết định đã chốt (user 05/10/2026)
- Phạm vi nới = đúng phạm vi QUYỀN của báo cáo (tổng công ty / công ty / phòng ban), không xét trạng thái / kỳ — như 4 báo cáo
  đã làm trước. Chỉ là quyền XEM.
- BE: `Meeting::canViewByReportScope($report)` dùng chung `hasReportPermission()` + `applyPermissionFilter()` (public) của
  `MeetingByMarketService` / `PotentialCustomerCareService`; không quyền báo cáo → false (luật cũ phủ người tạo / chủ trì / thành phần).
- Ngoài phạm vi: panel đầu việc của báo cáo kế hoạch & kết quả làm việc (không gọi API meeting).
