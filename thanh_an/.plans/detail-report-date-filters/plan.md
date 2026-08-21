# Lọc ngày tiếp nhận & kết chuyển ra ngoài — plan/detail-report (@khoipv)

**Goal:** Thêm lọc "Ngày tiếp nhận" và "Ngày kết chuyển" ra thanh header (giống sale/report-project-contract), đổi các button sang icon-only.

## Tasks
- [x] BE `QuotationController@applySummaryReportFilters`: thêm lọc
  - `received_from/to` trên received_date (CASE: project_id → projects.assigned_at, else quotations.created_at) — dùng subquery độc lập vì stats không join projects
  - `rendered_from/to` trên quotations.rendered_at
- [x] FE: import + đăng ký DatePicker
- [x] FE: thêm date-filter-bar (Ngày tiếp nhận + Ngày kết chuyển) ra header, `@change=searchAndSave` + nút reset icon
- [x] FE: đổi button Xuất excel / Tùy chỉnh cột / Bộ lọc sang icon-only + tooltip
- [x] FE: thêm 4 field formFilter + reset()
- [x] FE: CSS date-filter-bar/filter-label/btn-icon-only; header-action-row → space-between; xóa .btn-export min-width
- [ ] Verify browser: lọc đúng, KPI (stats) cập nhật theo, export tôn trọng filter

## Tasks — bid_package/detail-report (thêm lọc Thời điểm mời thầu & đóng thầu)
- [x] BE `BidPackageController@applyBidPackageSummaryReportFilters` (helper dùng chung list + stats): thêm lọc
  - `bid_opening_from/to` trên `bid_packages.bid_opening_time`
  - `bid_closing_from/to` trên `bid_packages.bid_closing_time`
  - Cột trực tiếp trên bảng gốc `bid_packages` → dùng chung cho cả summaryReport & summaryReportStats
- [x] FE: import + đăng ký DatePicker
- [x] FE: date-filter-bar (Thời điểm mời thầu + Thời điểm đóng thầu) ra header, `@change=searchAndSave` + nút reset icon
- [x] FE: đổi button Xuất excel / Tùy chỉnh cột / Bộ lọc sang icon-only + tooltip
- [x] FE: thêm 4 field formFilter + reset() (bid_opening_from/to, bid_closing_from/to)
- [x] FE: CSS date-filter-bar/filter-label/btn-icon-only; header-action-row → space-between; xóa .btn-export min-width
- [ ] Verify browser: lọc đúng, KPI (stats) cập nhật theo, export tôn trọng filter
