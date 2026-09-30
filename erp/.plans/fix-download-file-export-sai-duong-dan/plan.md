# Plan — Fix màn Download File không hiện file export

Repo `TanPhatDev`, nhánh `master`. @junfoke

## Phase 1 — Sửa đường dẫn đọc file (BE)

- [x] `ProductsController::downloadFile()` — `public_path('storage/product_export/...')` →
      `storage_path('app/public/product_export/...')`, tương tự `stock_export`
- [x] `ProductsController::downloadFile()` — thêm key `url` (route tải) vào mảng file trả về view
- [x] `ProductsController::downloadZip()` — 2 chỗ `public_path` → `storage_path`
- [x] `ProductsController::downloadStockZipByDate()` — 1 chỗ `public_path` → `storage_path`
- [x] `ProductTemplatesController::downloadFile()` — sửa cùng pattern (code chết, chưa có route)

## Phase 2 — Route tải file qua PHP

- [x] Thêm method `ProductsController::downloadExportFile(Request $request)`:
      ghép cứng `Auth::id()`, validate `file` theo `/^[A-Za-z0-9_\-]+\.xlsx$/` + `basename()`,
      validate `date` (stock_export) tương tự, `abort(404)` mọi trường hợp lệch → chặn path traversal
- [x] Đăng ký route `product.downloadExportFile` trong `routes/web.php` (group prefix `products`)

## Phase 3 — View

- [x] `products/exports/list.blade.php` — `asset($file['path'])` → `$file['url']` (2 chỗ: bảng sản
      phẩm + chi tiết file tồn kho)
- [x] `product_templates/exports/list.blade.php` — sửa cùng

## Phase 4 — Verify

- [x] `php -l` sạch toàn bộ file sửa
- [x] `git diff --stat` — số dòng đổi phải nhỏ, không phá CRLF (5 file đều đang CRLF)
- [ ] Test browser: user có file export → màn `download-file` hiện danh sách, bấm Tải xuống ra đúng file
- [ ] Test bảo mật: đổi tham số `file` thành `../../../.env` → phải trả 404
- [ ] Test user khác không thấy/không tải được file của user 27

## Checkpoint — 2026-09-08

Vừa hoàn thành: Phase 1-3 code xong (5 file), `php -l` sạch 3 file PHP, `git diff --stat` = 48+/9-,
CRLF nguyên vẹn cả 5 file (CR count == LF count).
Đang làm dở: Phase 4 — chưa verify runtime.
Bước tiếp theo: user test browser trên server đã deploy (màn `/admin/products/download-file` bằng
tài khoản có file export, ví dụ `thunth@etekpower.vn`), + test 404 khi truyền `file=../../../.env`.
Blocked: **không chạy được `php artisan route:list` trên local** — nhánh `master` không boot do lỗi
có sẵn `ProductExportRequest::CHO_DUYET_NHAP` (đã ghi trong STATUS, không liên quan đợt sửa này).
CHƯA commit.
