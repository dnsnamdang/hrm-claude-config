# Design (tóm tắt) — Quản lý Bảng giá

> Spec đầy đủ: `docs/superpowers/specs/2026-06-26-price-tier-management-design.md`

## Mục tiêu
Thay cơ chế cột giá cứng (`price_p3/p5/p7/p10`) bằng **danh mục Bảng giá động**. User chỉ nhập **P0 (NET)** cho hàng hoá; các cấp giá còn lại tự tính & lưu snapshot theo % cấu hình.

## Quyết định chung
- Công thức: `Giá cấp = P0 × (1 + percent/100)`.
- **Snapshot** giá cấp vào `product_unit_prices` lúc lưu hàng hoá (không tính live).
- Đổi % KHÔNG tự đổi hàng cũ → có **nút "Tính lại" hàng loạt** trên danh mục.
- Danh mục **dùng chung** (không phân quyền cấp). Mã `BG.XXXX`.
- Lịch sử: chỉ track danh mục bảng giá (name/percent).

## Phạm vi
- **Trong scope**: danh mục Bảng giá (CRUD + lịch sử + tính lại), đổi cấu trúc giá product, FE form hàng hoá cột động.
- **Ngoài scope**: auto-fill giá vào Báo giá, lịch sử giá P0, phân quyền cấp.

## DB
- `price_tiers` (code, name, percent, status).
- `price_tier_histories` (action, old/new name/percent, changed_by).
- `product_units`: drop `price_p3/p5/p7/p10`, giữ `price_p0`.
- `product_unit_prices` (product_unit_id, price_tier_id, percent, price) — snapshot.

## Permission
- `1113 Quản lý danh mục bảng giá`, `1114 Xem danh mục bảng giá` (group "Danh mục chung", type 8).

## Phase
1. Danh mục Bảng giá CRUD + lịch sử + permission.
2. Đổi cấu trúc giá product (migration + snapshot + Service + Resource + FE form động + seeder).
3. Nút tính lại hàng loạt.
