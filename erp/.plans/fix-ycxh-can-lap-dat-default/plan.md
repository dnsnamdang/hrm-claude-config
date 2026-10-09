# Plan — Fix "Cần lắp đặt" YCXH mặc định rỗng + cảnh báo inline

Issue 9661. Branch: `fix-ycxh-can-lap-dat-default` (từ master). Verify: `php -l` + `view:clear` + browser.

## Tasks
- [x] T1: FE default rỗng — `resources/views/partials/classes/warehouse/ProductExportRequest.blade.php:44` đổi `this.need_repair = false` → không set (null) cho form mới.
- [x] T2: FE chặn submit + inline — `resources/views/warehouse/product_export_requests/create.blade.php` `$scope.submit`: guard type==14 & need_repair chưa chọn → set `errors['need_repair']` + toastr + return.
- [x] T3: FE clear lỗi — `form.blade.php` 2 radio need_repair thêm `ng-change` xóa `errors['need_repair']`.
- [x] T4: BE defense — `ProductExportRequestsController::store()` block type==14 thêm `'need_repair' => 'required'` + message.
- [x] T5: `php -l` controller + `php artisan view:clear` + đối chiếu grep.

## Checkpoint
(mới tạo — sẽ cập nhật khi xong)

### Checkpoint — 2026-07-04
Vừa hoàn thành: T1-T5 code xong (FE default rỗng + guard submit + clear lỗi + BE required). Nhánh `fix-ycxh-can-lap-dat-default` (từ master), 4 file sửa, CHƯA commit.
- ProductExportRequest.blade.php:46 (default null)
- create.blade.php:413-419 (guard submit type14)
- form.blade.php:41,47 (ng-change clear)
- ProductExportRequestsController.php:418 (rule) + 508 (message)
php -l sạch, view:clear OK.
Bước tiếp theo: chờ user duyệt → commit; test browser (tạo type 14: không chọn→chặn+inline; chọn Có/Không→OK; lưu nháp cũng chặn nếu trống).
Blocked: (không)
