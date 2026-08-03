# Task 1 Report — Migration `min_stock` + Product entity

Plan gốc: `docs/superpowers/plans/2026-07-02-warehouse-dashboard.md` (Task 1)

## Trạng thái: DONE

## File đã tạo

- `nhatlinh-api/Modules/Category/Database/Migrations/2026_07_02_000001_add_min_stock_to_products_table.php`
  - Thêm cột `min_stock DECIMAL(18,2) NULL` vào bảng `products`, đặt `->after('status')`, có comment mô tả.
  - Có `down()` để rollback (`dropColumn('min_stock')`).

## File đã sửa

- `nhatlinh-api/Modules/Category/Entities/Product.php`
  - Thêm `'min_stock'` vào mảng `$fillable` (cạnh `'status'`).
  - **Không thêm `$casts`**: file entity này KHÔNG có mảng `$casts` sẵn có (đã đọc toàn bộ file, chỉ có `$fillable`, `$table`, các const `STATUS_*`, `STATUSES`, `PRODUCT_CLASSIFICATIONS`). Theo đúng chỉ dẫn của plan ("trong `$casts` (nếu có) thêm...") và ràng buộc "không phá field khác", không tự tạo thêm mảng `$casts` mới vì đó là thay đổi ngoài phạm vi Task 1 và có thể ảnh hưởng cách các field khác được trả ra (không có cast nào từ trước). Nếu cần ép kiểu `decimal:2` cho `min_stock`, nên xử lý ở Resource layer (Task 2) thay vì thêm cast mới ở đây.

## Xác nhận trước khi viết migration

- Đọc `nhatlinh-api/Modules/Category/Database/Migrations/2026_06_03_000001_create_products_table.php`: bảng `products` **có cột `status`** (`$table->integer('status')->default(1)`) → giữ nguyên `->after('status')` như plan, không cần điều chỉnh.

## Kết quả `php -l`

```
$ php -l Modules/Category/Entities/Product.php
No syntax errors detected in Modules/Category/Entities/Product.php

$ php -l Modules/Category/Database/Migrations/2026_07_02_000001_add_min_stock_to_products_table.php
No syntax errors detected in Modules/Category/Database/Migrations/2026_07_02_000001_add_min_stock_to_products_table.php
```

(Output có kèm warning `PHP Startup: Unable to load dynamic library 'imagick.so'` — không liên quan, do thiếu extension imagick trên máy dev, không ảnh hưởng kết quả lint. Đã lọc bỏ warning này khỏi output trên.)

## Kết quả `php artisan migrate`

```
$ php artisan migrate
Migrating: 2026_07_02_000001_add_min_stock_to_products_table
Migrated:  2026_07_02_000001_add_min_stock_to_products_table (76.81ms)
```

Migrate chạy thành công trên DB dev, không lỗi. (Cùng warning imagick không liên quan như trên, đã lọc.)

## Kết quả tinker verify

```
$ php artisan tinker --execute="echo \Modules\Category\Entities\Product::query()->first()->min_stock ?? 'null';"
null
```

→ Không lỗi "column not found", model đọc được `min_stock` (giá trị `null` vì record hiện có chưa set).

Verify bổ sung — `Schema::getColumnListing('products')` xác nhận cột `min_stock` nằm đúng vị trí ngay sau `status`:

```
[...] status, min_stock, product_classification, supplier_id, default_bom_id, [...]
```

## Nghi ngờ / edge case

- Product entity không có `$casts`, nên `min_stock` trả về kiểu string/numeric-string mặc định của Eloquent khi query trực tiếp (không tự động ép `float`/`decimal:2`). Task 2 (ProductResource) sẽ là nơi kiểm soát định dạng trả ra cho FE — cần lưu ý khi implement Task 2.
- Chưa động tới `ProductRequest`, `ProductResource`, `ProductForm.vue` — đúng phạm vi, các phần này thuộc Task 2 (không làm trong task này).
- Không commit/push git theo đúng yêu cầu.
