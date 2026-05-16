# Fix quy đổi giá khi thay đổi đơn vị tính

## Mục tiêu

Khi user đổi đơn vị tính của hàng hóa trong gói thầu/hợp đồng, tất cả trường giá phải được quy đổi theo tỷ lệ `conversion_factor`.

## Scope

- Gói thầu: `bid_package/components/ProductComponent.vue`
- Hợp đồng: `contract/components/ProductComponent.vue`
- Phân quyền: `bid_package/components/GeneralComponent.vue`

## Giải pháp

- Lưu `coefficient` (từ `conversion_factor`) vào mảng `units` của mỗi product
- Thêm hàm `onUnitChange`: tính `ratio = new_coefficient / old_coefficient`, nhân vào các trường giá
- Dùng `_prev_unit_id` để track unit cũ trước khi đổi

Spec chi tiết: `docs/superpowers/specs/2026-05-12-fix-unit-price-conversion-design.md`
