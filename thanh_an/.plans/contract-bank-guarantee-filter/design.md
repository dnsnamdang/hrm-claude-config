# Bộ lọc Ngân hàng thực hiện — Danh sách Hợp đồng

> Spec chi tiết: `docs/superpowers/specs/2026-05-22-contract-bank-guarantee-filter-design.md`

## Mục tiêu

Thêm bộ lọc "Ngân hàng thực hiện" vào trang danh sách hợp đồng để tìm nhanh hợp đồng có bảo lãnh thuộc ngân hàng đã chọn.

## Scope

- Thêm 1 dropdown `Select2` single-select vào filter panel (sau ô "Số chứng thư bảo lãnh")
- Backend: thêm `whereHas('guarantees')` filter theo `bank_guarantee_id`
- Dùng API banks có sẵn (`GET /api/human/banks`), không cần migration

## Quyết định chính

- **Cách tiếp cận:** `whereHas('guarantees')` — theo đúng pattern filter `certificate_number` đã có
- **Single-select** — chọn 1 ngân hàng tại 1 thời điểm
- **Vị trí UI:** Ngay sau ô "Số chứng thư bảo lãnh"

## Thay đổi

| File | Thay đổi |
|------|----------|
| `hrm-thanhan-client/pages/contract/contract/index.vue` | Thêm field, dropdown, method load banks |
| `hrm-thanhan-api/Modules/Category/Services/ContractService.php` | Thêm 1 block `->when()` |
