# Task 4 — WhDashboardService — Report

## File tạo
- `nhatlinh-api/Modules/Warehouse/Services/WhDashboardService.php`

## Xác minh entity thật (trước khi transcribe)
- Namespace/entity đúng như plan giả định:
  - `Modules\Warehouse\Entities\{Inventory, StockMovement, WhReceipt, WhIssue, WhTransfer}`
  - `Modules\Category\Entities\{Product, Warehouse}`
- `stock_movements`: cột `movement_date` (cast `date:Y-m-d`), `type` (const `TYPE_RECEIPT=1`, `TYPE_ISSUE=2`, `TYPE_TRANSFER_IN=3`, `TYPE_TRANSFER_OUT=4`, `TYPE_ADJUST=5`), `quantity` (dấu ±, xác nhận qua cách `WhReportService::stockCard()` dùng `$qty > 0 ? in : out`) — dùng `StockMovement::TYPE_RECEIPT`/`TYPE_ISSUE` thay cho magic number 1/2 cho rõ nghĩa.
- `WhReceipt`/`WhIssue`/`WhTransfer` đều có `STATUS_PENDING = 2` — khớp plan.
- `Warehouse` **có cột `status`** (`STATUS_ACTIVE = 1`) → theo hướng dẫn plan, đổi `warehouse_count` thành `Warehouse::where('status', Warehouse::STATUS_ACTIVE)->count()` (đếm kho đang hoạt động, không đếm toàn bộ).
- ĐVT cơ bản: `Product` đã có sẵn accessor `getBaseUnitNameAttribute()` (dùng `productUnits->firstWhere('is_base_unit', 1)->unit->name`), và `WhReportService` cũng dùng pattern eager-load `product.productUnits.unit` + `$p->base_unit_name`. → Dùng lại accessor có sẵn (`$p->base_unit_name`) thay vì tự viết lại logic lấy đơn vị thủ công như code mẫu trong plan (đỡ trùng lặp, đúng nguyên tắc "ưu tiên helper có sẵn"). Eager-load `productUnits.unit` (không filter `is_base_unit` ở query, để accessor tự lọc) trong `topProducts()` và `lowStock()`.
- `min_stock`: migration `2026_07_02_000001_add_min_stock_to_products_table` đã chạy (`php artisan migrate:status` → Yes), `Product::$fillable` đã có `min_stock` từ trước (Task 1/2 coi như đã hoàn tất ngoài phạm vi task này).

## Điều chỉnh logic so với code mẫu trong plan
- **`movementByTime()`**: code mẫu trong plan dùng `->pluck(DB::raw('CONCAT(in_qty, "|", out_qty)'), 'bucket')` để gộp in/out thành 1 chuỗi rồi tách — cách này **không hoạt động đúng** vì cột `CONCAT(...)` đó không được `SELECT`, nên Laravel `pluck()` không tìm được property tương ứng trên stdClass row (chỉ có `bucket`, `in_qty`, `out_qty`). Đã thay bằng `->get()->keyBy('bucket')` rồi đọc `$row->in_qty` / `$row->out_qty` trực tiếp — an toàn và đã verify bằng tinker cho ra đúng số liệu thật (xem log bên dưới, bucket `2026` ra `in_qty=70` khớp dữ liệu seed).
- Còn lại (kpis, bucketLabel, windowStart, groupExpr, topProducts, lowStock, stockByWarehouse) transcribe gần như nguyên văn code trong plan, chỉ đổi phần base_unit như trên.

## Output `php -l`
```
No syntax errors detected in Modules/Warehouse/Services/WhDashboardService.php
```
(có warning `imagick.so` không load được — môi trường local, không liên quan file này)

## Output tinker smoke test (tóm tắt)
- `granularity=month`: `KEYS: kpis,movement_by_time,top_export,top_import,low_stock,stock_by_warehouse` — đủ 6 khoá.
  - `kpis`: `{"pending_receipts":3,"pending_issues":6,"pending_transfers":0,"warehouse_count":11,"product_in_stock_count":3,"out_of_stock_count":2}` — toàn số nguyên.
  - `movement_by_time.buckets`: 12 mốc liền mạch `2025-08 … 2026-07` (label `YYYY-MM`).
  - `top_import`: 3 dòng, resolve đúng `product_code/product_name/base_unit` (vd `TBTH.0001 / Bàn học sinh đơn BHS-01 / Cái`, `quantity=50`).
  - `top_export`: rỗng — vì DB dev **không có movement type=2** (0 bản ghi), không phải lỗi.
  - `low_stock`: rỗng — vì DB dev chưa có sản phẩm có `min_stock` bị vi phạm (tồn hiện tại chưa < min_stock), không phải lỗi.
  - `stock_by_warehouse`: 6 dòng.
- `granularity=week`: 12 mốc, label ISO tuần `2026-W16 … 2026-W27` — khớp định dạng `GGGG-[W]WW`.
- `granularity=quarter`: 8 mốc, `2024-Q4 … 2026-Q3` — liền mạch.
- `granularity=year`: 5 mốc, `2022 … 2026`; verify riêng bucket `2026` ra `in_qty=70, out_qty=0` khớp 7 movement type=1 đã seed trong khoảng `2026-06-29 → 2026-07-01` (chứng minh mapping `keyBy('bucket')` hoạt động đúng, không chỉ toàn 0 do bug).
- Không có lỗi SQL ở cả 4 granularity.

## Concerns
- `top_export`/`low_stock` rỗng trong môi trường dev hiện tại là do **thiếu dữ liệu seed** (0 movement type=2, chưa có sản phẩm dưới ngưỡng min_stock), không phải lỗi service — cần dữ liệu thật hơn để verify trực quan ở FE (Task 7) sau này.
- Lệch duy nhất so với code mẫu trong plan: cách gộp `in_qty`/`out_qty` theo bucket (đã sửa lỗi `pluck(DB::raw(CONCAT...))`) và cách lấy `base_unit` (dùng accessor `base_unit_name` có sẵn thay vì tự viết). Không có lệch về entity/namespace/tên cột nào khác so với plan.
- `warehouse_count` đếm theo `status=STATUS_ACTIVE(1)` (kho đang hoạt động) — nếu sau này muốn đếm cả kho khoá thì cần đổi lại theo yêu cầu nghiệp vụ.
