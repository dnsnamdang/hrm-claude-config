# Plan — Bộ lọc danh mục ngân hàng: thêm Tên ngân hàng, đổi Tên viết tắt → Mã ngân hàng

Phụ trách: @khoipv

## Phase 1 — Bộ lọc nâng cao

- [x] FE `hrm-client/pages/master-data/banks/index.vue`: thêm ô lọc "Tên ngân hàng" (`filters.name`)
- [x] FE: đổi ô lọc "Tên viết tắt" (`filters.short_name`) → "Mã ngân hàng" (`filters.code`)
- [x] FE: cập nhật `initialStateForm` + `apiFilters` (bỏ `short_name`, thêm `name`, `code`)
- [x] BE `hrm-api/Modules/MasterData/Services/BankService.php`: bỏ filter `short_name`, thêm filter `name` và `code` (like)
- [x] BE: bọc điều kiện `keyword` trong closure để `orWhere` không phá logic khi kết hợp filter khác
- [ ] Verify trên UI: lọc theo tên, theo mã, kết hợp với trạng thái / tên giao dịch quốc tế

## Ghi chú

- Không màn nào khác gửi tham số `short_name` tới `master-data/banks` → bỏ an toàn.
- Ô tìm nhanh (`keyword`) vẫn tìm theo cả tên + mã như cũ.
