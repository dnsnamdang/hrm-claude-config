# Đổi tồn kho popup searchProduct sang tồn có thể bán

## Mục tiêu
Cột `in_stock` trên popup searchProduct hiển thị tồn có thể bán (trừ prepick + hold + YCXK chưa xuất) thay vì tồn sổ sách.

## Scope
- 1 file BE: `SearchController::searchProduct()` — thay subquery tồn kho + thêm join hold + YCXK
- FE: không sửa

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-06-search-product-sellable-stock-design.md`
