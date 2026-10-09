# Task 3 — Report: Entity cha `BorrowSellRequest` + hợp nhất & repoint type-9

## File tạo/sửa/xoá
- **Tạo**: `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` — entity cha, namespace `Modules\Finance\Entities\BorrowSellRequest`, `use ChecksEmployeePermission`, dùng lại 5 child entity Task 2 (`BorrowSellRequestProduct`, `BorrowSellRequestProductDetail`, `BorrowSellRequestTab`, `BorrowSellRequestTabProduct`, `BorrowSellRequestTabProductDetail`) + `product_export_requests()` belongsToMany tới `ProductImportRequest\ProductExportRequest`.
- **Sửa**: `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php` — thêm method `currentManagedDepartmentIds()` cạnh `currentCompanyId()` (file đã sẵn `use Illuminate\Support\Facades\DB;` ở đầu, không cần thêm).
- **Sửa**: `Modules/Finance/Services/ProductImportRequestService.php` dòng 11 — đổi `use Modules\Finance\Entities\ProductImportRequest\BorrowSellRequest;` → `use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;`. Call site dùng `BorrowSellRequest::dataForImport()` / `::searchForPicker()` (dòng ~1022/1574/1597) GIỮ NGUYÊN, không đụng.
- **Xoá**: `Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php` (entity read-only cũ).
- `composer dump-autoload -o` đã chạy, "Generated optimized autoload files containing 12317 classes".

## Xác nhận theo ràng buộc bắt buộc
- Employee relation dùng `Modules\Human\Entities\Employee` (đúng như entity cũ, KHÔNG dùng Timesheet).
- `boot()` chỉ set `created_by`, `company_id`, `department_id` trong `creating`; `updated_by` trong `updating`. KHÔNG có `part_id` (cột không tồn tại trên bảng `borrow_sell_requests`).
- Entity `extends Model` trần, KHÔNG set `$connection`, KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`.
- KHÔNG viết `searchByFilter`.

## Đối chiếu brief vs file cũ (2 helper)
Đã đọc nguyên văn `Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php` trước khi xoá. `searchForPicker()` và `dataForImport()` trong brief khớp 100% logic file cũ (chỉ khác: file cũ có thêm 1-2 dòng comment giải thích nghiệp vụ mà brief lược bớt, và class cũ không `use ChecksEmployeePermission`/không có boot()/gates — vì nó chỉ là entity read-only). Không có chênh lệch về tên cột, điều kiện where, hay logic tính toán. Đã dán ĐÚNG NGUYÊN VĂN theo brief (đối chiếu khớp file thật) vào entity mới.

## Output verify (a-d)

### a) Không còn tham chiếu namespace cũ
```
OK: no old refs
```

### b) php lint 3 file đụng tới
```
No syntax errors detected in Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php
No syntax errors detected in Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
No syntax errors detected in Modules/Finance/Services/ProductImportRequestService.php
```

### c) Entity mới load + generateCode format
```
code=PYCXBHM-00001 status=1 dept=77
```

### d) Hồi quy type-9 — 2 helper chạy qua class mới
```
dataForImport products=3 is_settlement=false
picker count=4245
```
(`picker count` chạy không lỗi qua `searchForPicker(request())`; số 4245 vì `count()` trên query builder Laravel bỏ qua `limit()` — không phải bug, chỉ xác nhận query chạy được và có dữ liệu khớp điều kiện.)

## STATUS: DONE
- Verify c: entity mới load được, `generateCode()` format đúng `PYCXBHM-00001`, không exception dù không có `auth()`.
- Verify d: cả 2 helper type-9 (`dataForImport`, `searchForPicker`) chạy qua class mới không lỗi, trả dữ liệu hợp lệ.
- Concerns: không có — không phát hiện chênh lệch logic giữa brief và file cũ.
