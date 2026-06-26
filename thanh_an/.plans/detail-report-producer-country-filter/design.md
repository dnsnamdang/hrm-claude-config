# Lọc Hãng/nước SX — màn detail-report (tóm tắt)

**@khoipv · 2026-06-25**

## Mục tiêu
Thêm bộ lọc **Hãng, nước sản xuất** (dropdown, chọn 1) vào màn
`plan/detail-report` (Báo cáo chi tiết báo giá).

## Quyết định lớn
- 1 trường duy nhất (danh mục `producer_countries` chỉ có `name`).
- Dropdown lấy từ danh mục, bổ sung tham số `all=1` để bỏ lọc `created_by`.
- Lọc qua `whereExists` trên `quotation_tab_products.producer_country = name` (khớp chính xác).
- Export Excel tự hưởng filter (dùng chung endpoint).

## Phạm vi
- BE: `ProducerCountryService::index` (+param `all`), `QuotationController`
  (`applySummaryReportFilters` + `applyDetailReportFilters`).
- FE: `pages/plan/detail-report/index.vue` (Select2 + formFilter + getProducerCountries).
- Không migration.

Spec đầy đủ: `docs/superpowers/specs/2026-06-25-detail-report-producer-country-filter-design.md`
