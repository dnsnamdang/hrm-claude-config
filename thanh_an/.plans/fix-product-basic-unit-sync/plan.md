# Fix: Tab thông tin cơ bản hiện sai đơn vị tính (lệch với tab đơn vị chuyển đổi)

@khoipv

## Bối cảnh
- Tab cơ bản hiển thị `products.unit_id` (`DetailProductResource:56-57`), không cho sửa tay (`GeneralComponent.vue:176` `v-if=isShow` + disabled).
- Tab chuyển đổi: "đơn vị tính chính" = cờ `is_usually` (`UnitComponent.vue.vue:89,131`).
- Code đồng bộ `products.unit_id` = đơn vị `is_usually` chỉ mới có từ **12/12/2025** (commit `b9e1acb8`, `ProductService:707-731`). Bản ghi sửa trước mốc này còn giữ unit_id cũ (đơn vị cơ bản).
- Phạm vi: 26 sản phẩm lệch (25 sửa trước 12/12/2025 = data cũ; 1 sửa sau = id 170).

## Task
- [x] Backfill `products.unit_id` = đơn vị `is_usually` cho 26 bản ghi lệch (DB staging — chạy tay)
- [x] Tạo migration data-fix để chạy được trên production: `database/migrations/2026_06_26_100000_backfill_product_unit_id_from_usually_package.php` (idempotent)
- [x] Xác minh product 174 + 170 hiển thị đúng sau backfill
- [x] Truy endpoint "chạm" id 170 sau 12/12/2025 → **lưu giá đơn vị** (`ProductUnitPriceService::store` dòng 149: `Product::...->update(['status'=>ACTIVE])`). Chỉ set status, KHÔNG ghi đè unit_id (không phá dữ liệu, cũng không sửa giá trị cũ). → 170 vẫn là data cũ, không phải lỗi ghi mới.

## Checkpoint — 2026-06-26
Vừa hoàn thành: Backfill 26 bản ghi (`UPDATE products ... SET unit_id = đơn vị is_usually`). 174 & 170 → unit_id=3 (Hộp). Còn lệch: 0.
Đang làm dở: (không)
Bước tiếp theo: Nếu cần triệt để → truy endpoint cập nhật product sau 12/12/2025 vẫn để lệch (id 170) và vá đồng bộ unit_id.
Blocked: (không)
