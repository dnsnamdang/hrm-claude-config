# Plan: Bộ lọc Ngân hàng thực hiện — Danh sách Hợp đồng

> Người phụ trách: @khoipv | Ngày: 2026-05-22

## Phase 1 — Backend

- [x] Thêm `->when($request->bank_guarantee_id, ...)` vào `ContractService::index()`

## Phase 2 — Frontend

- [x] Thêm `bank_guarantee_id` vào `initialStateForm`
- [x] Thêm `bankGuaranteeOptions: []` vào `data()`
- [x] Thêm method `getBankGuaranteeOptions()` gọi API `human/banks`
- [x] Gọi `getBankGuaranteeOptions()` trong `mounted()`
- [x] Thêm dropdown `Select2` vào filter panel (sau "Số chứng thư bảo lãnh")

## Phase 3 — Verify

- [ ] Test: chọn ngân hàng → danh sách chỉ hiện hợp đồng có bảo lãnh thuộc ngân hàng đó
- [ ] Test: xóa filter → hiện lại tất cả hợp đồng
- [ ] Test: filter kết hợp với các bộ lọc khác
