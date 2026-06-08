# Mở rộng Hàng hoá (DM-08 + DM-01) — Tóm tắt

**Ngày:** 2026-06-05 · @manhcuong · Spec: `docs/superpowers/specs/2026-06-05-product-catalog-extend-design.md` · MODULE 1 (DM-08+DM-01)

## Scope
Gộp 2 việc cùng đụng product:
- DM-08: thêm `conversion_rate` (tỷ lệ quy đổi) cho từng ĐVT của sản phẩm (cơ bản=1).
- DM-01: thêm phân loại (mua sẵn/SX) + NCC mặc định (supplier_id) + BOM mặc định (default_bom_id).

## Quyết định
- product_units += conversion_rate (decimal 15,4 default 1).
- products += product_classification (1=mua sẵn,2=SX), supplier_id (FK suppliers), default_bom_id (FK boms).
- FE ProductForm: select phân loại; mua sẵn→chọn NCC; SX→chọn BOM mặc định (từ BOM của product, chỉ khi edit); bảng ĐVT thêm cột quy đổi.
- Migration mới (không sửa migration cũ).
