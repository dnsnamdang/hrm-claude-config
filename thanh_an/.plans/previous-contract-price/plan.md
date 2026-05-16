# Giá bán HĐ trước — Plan

**Người phụ trách:** @khoipv
**Trạng thái:** Đã implement, chờ test
**Plan chi tiết:** `docs/superpowers/plans/2026-05-13-previous-contract-price.md`

## Phase 1 — BE: Migration + Service + API (Task 1-4)

- [x] Task 1: Migration thêm cột `price_pre_contract` cho 3 bảng
- [x] Task 2: Thêm `price_pre_contract` vào fillable 3 model
- [x] Task 3: Tạo `ProductPriceService` — logic tìm giá HĐ trước
- [x] Task 4: Tạo API endpoint `POST /products/previous-contract-price`

## Phase 2 — BE: Tích hợp sync (Task 5-7)

- [x] Task 5: Tích hợp vào QuotationService::syncGroups()
- [x] Task 6: Tích hợp vào BidPackageService::syncProducts()
- [x] Task 7: Tích hợp vào ContractService::syncGroups()

## Phase 3 — FE: Gọi API khi đổi KH (Task 8-11)

- [x] Task 8: Tạo helper method `fetchPreviousContractPrices`
- [x] Task 9: Gọi API khi đổi KH ở màn Quotation
- [x] Task 10: Gọi API khi đổi KH ở màn BidPackage
- [x] Task 11: Gọi API khi đổi KH ở màn Contract

## Phase 4 — Test (Task 12)

- [ ] Task 12: Test thủ công end-to-end (3 màn + export + edge cases)

### Checkpoint — 2026-05-13
Vừa hoàn thành: Tất cả task implement (1-11)
Đang làm dở: Chờ chạy migration + test thủ công
Bước tiếp theo: Chạy `php artisan migrate`, test trên browser
Blocked: (không có)
