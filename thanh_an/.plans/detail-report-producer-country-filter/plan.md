# Plan: Lọc Hãng/nước SX — màn detail-report

**@khoipv · 2026-06-25**

> **Đổi hướng (user chốt):** dùng ô nhập **text** (LIKE) giống "Mã báo giá",
> KHÔNG dùng dropdown danh mục. Đã revert thay đổi ở `ProducerCountryService`.

## Phase 1 — Backend
- [x] `QuotationController::applySummaryReportFilters`: filter `producer_country` LIKE (whereExists)
- [x] `QuotationController::applyDetailReportFilters`: filter `producer_country` LIKE (where trực tiếp)
- [x] Revert `ProducerCountryService::index` (bỏ param `all`)

## Phase 2 — Frontend (`pages/plan/detail-report/index.vue`)
- [x] `formFilter.producer_country` (data + reset)
- [x] Ô `b-form-input` "Hãng, nước sản xuất" sau ô Mã hàng hóa
- [x] Bỏ `producerCountries` + `getProducerCountries()` + lời gọi trong `mounted()`

## Phase 3 — Verify
- [x] PHP lint BE PASS
- [ ] Chạy thử lọc trên UI + kiểm tra export Excel hưởng filter (chờ user verify)

## Phase 4 — Bổ sung lọc Trạng thái
- [x] BE: `applySummaryReportFilters` + `applyDetailReportFilters` filter `quotations.status`
- [x] FE: `statusOptions` (19 trạng thái) + Select2 "Trạng thái" (sau Loại báo giá) + `formFilter.status` (data + reset). PHP lint PASS.

## Fix phát sinh — Trạng thái hiện "-"
- [x] `statusMap` trong `summaryReport` + `exportDetailReport` thiếu 17/18 → báo giá "Gói thầu đã kết xuất" (18) hiện "-". Bổ sung `17 => 'Gói thầu đã bị hủy'`, `18 => 'Gói thầu đã kết xuất'` (đúng nhãn màn quotation/index.vue). PHP lint PASS.

---
### Checkpoint — 2026-06-25
Vừa hoàn thành: đổi sang ô text LIKE — BE 2 chỗ + revert service + FE (b-form-input + formFilter), PHP lint PASS
Đang làm dở: không
Bước tiếp theo: user verify trên UI (lọc + export)
Blocked:
