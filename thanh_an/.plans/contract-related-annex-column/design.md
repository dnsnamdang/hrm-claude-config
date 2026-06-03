# Design (tóm tắt): Cột "Phụ lục liên quan" — Danh sách hợp đồng

> Người phụ trách: @khoipv | Ngày: 2026-06-02
> Spec chi tiết: `docs/superpowers/specs/2026-06-02-contract-list-related-annex-column-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-06-02-contract-related-annex-column.md`

## Mục tiêu
Thêm cột "Phụ lục liên quan" vào màn `pages/contract/contract/index.vue`, hiển thị mọi mã phụ lục của hợp đồng (mỗi mã một dòng), click → mở chi tiết phụ lục đúng loại.

## Quyết định lớn
- Hiển thị **tất cả trạng thái** phụ lục.
- **Mỗi mã một dòng**, dùng `b-link`.
- Cột **hiển thị mặc định** (ẩn được qua "Tuỳ chỉnh cột").
- **Không** đưa vào Excel.
- Không filter/sort/badge theo phụ lục (YAGNI).

## Cách làm
- BE: relation `Contract::annexes()` → eager load trong `ContractService::index` → expose `annexes` (id/code/annex_type/status) ở `ContractResource`.
- FE: thêm field cột + cell slot render link; build URL từ `ANNEX_TYPE_ROUTE_MAP` (copy từ `contract_annex/approve.vue`): `/contract/{route}/{annex.id}`.
