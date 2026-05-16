# Fix quy đổi giá khi thay đổi đơn vị tính

**Người phụ trách:** @khoipv
**Ngày tạo:** 2026-05-12

## Mô tả

Khi thay đổi đơn vị tính của hàng hóa (VD: Can → Lít), các trường giá (price, price_before_vat, price_pre_contract, price_bid_package) không được quy đổi theo hệ số `conversion_factor`. Cần fix ở cả gói thầu và hợp đồng.

## Nguyên nhân

- Hàm `updatePrice` chỉ lookup `price_min`, `price_max`, `price_cost` từ mảng `prices` theo `unit_id` mới — không quy đổi `price`, `price_before_vat`, etc.
- Mảng `units` khi addProduct chỉ lưu `{id, text}` — thiếu `coefficient` (hệ số quy đổi).

## Tasks

### Phase 1 — Gói thầu (`bid_package/components/ProductComponent.vue`)

- [x] Thêm `coefficient` vào mapping `units` từ `packageInformations` (2 chỗ addProduct)
- [x] Thêm hàm `onUnitChange`: tính ratio = newCoefficient / oldCoefficient, nhân vào price, price_before_vat, price_pre_contract, price_bid_package
- [x] Đổi `@input` trên select đơn vị từ `updatePrice` → `onUnitChange`
- [x] Thêm `_prev_unit_id` trong watcher `formSubmit` để biết unit cũ

### Phase 1b — Phân quyền bảng hàng hóa gói thầu

- [x] Sửa `GeneralComponent.vue` truyền `:isShow="isShow && !formSubmit.can_handle"` cho `ProductComponent`
- [x] Trang detail (`_id/index.vue`): chỉ cho thao tác khi `can_handle = true`
- [x] Trang add: luôn cho thao tác (không ảnh hưởng)

### Phase 2 — Hợp đồng (`contract/components/ProductComponent.vue`)

- [x] Thêm `coefficient` vào mapping `units` từ `packageInformations` (3 chỗ)
- [x] Thêm hàm `onUnitChange` tương tự gói thầu (dùng `price` và `amount` thay vì `price_bid_package` và `amount_bid_package`)
- [x] Đổi `@input` trên select đơn vị từ `updatePrice` → `onUnitChange`
- [x] Thêm `_prev_unit_id` trong watcher `formSubmit`

### Phase 3 — Kiểm tra

- [x] Test gói thầu: đổi đơn vị → giá quy đổi đúng
- [x] Test hợp đồng: đổi đơn vị → giá quy đổi đúng
- [x] Test trang add gói thầu: bảng hàng hóa luôn thao tác được
- [x] Test trang detail gói thầu: bảng hàng hóa chỉ thao tác khi can_handle

### Checkpoint — 2026-05-12
Hoàn thành tất cả tasks. Đã test OK.
