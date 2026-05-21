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

## Phase 5 — Bugfix: Import Excel thiếu coefficient (Task 13-14)

- [x] Task 13: Thêm `coefficient` vào `units` trong `ProductQuotationImport.php`
- [x] Task 14: Thêm `coefficient` vào `units` trong `ProductContractImport.php`
  - Lưu ý: `ProductBidPackageImport.php` đã có sẵn, không cần sửa
- [x] Task 15: Thêm `_prev_unit_id` vào `handleImportSuccess` — 3 màn Quotation, BidPackage, Contract
  - Quotation: 2 block (nhóm tồn tại + nhóm mới)
  - BidPackage: 1 block (chỉ tạo nhóm mới)
  - Contract: 2 block (nhóm tồn tại + nhóm mới)
- [x] Task 16: Thêm `_prev_unit_id` vào `addProduct` — 3 màn Quotation, BidPackage, Contract
  - Mỗi màn có 2 block: duplicate + normal

### Checkpoint — 2026-05-21
Vừa hoàn thành: Fix 3 bug liên quan quy đổi giá bán HĐ trước khi đổi đơn vị — đã test OK
Đang làm dở: (không có)
Bước tiếp theo: Done — chờ merge
Blocked: (không có)
