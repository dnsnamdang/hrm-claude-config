# Plan — Giữ nguyên tên file gốc khi upload (@khoipv)

## Bối cảnh

Màn `timesheet/request-payment-working-fee/add`: tên file đính kèm sau khi lưu bị đổi khác lúc upload.

**Root cause** — `hrm-thanhan-api/app/Helper/CmcS3Helper.php:56-60`:
```php
$filename = $file->getClientOriginalName();           // "Đề nghị thanh toán.pdf"
$name = Str::slug(str_replace("/", "", $filename));   // → "de-nghi-thanh-toan-pdf"  (slug cả extension)
$extension = pathinfo($filename, PATHINFO_EXTENSION); // → "pdf"
$destinationFileName = $name . '-' . time() . '-' . $this->randomString(4);
$destinationFile = $destinationFileName . '.' . $extension;
// → "de-nghi-thanh-toan-pdf-1752633600-x8Kq.pdf"
```
Tên bị biến đổi 3 chỗ: (1) slug bỏ dấu tiếng Việt, (2) slug nuốt extension thành `-pdf`, (3) nối `-{timestamp}-{random4}`.

`timestamp + random` đang là cơ chế chống trùng key S3 → không được bỏ thẳng, phải chuyển sang path thư mục.

## Quyết định (đã chốt với user)

1. **Sửa hàm chung** `CmcS3Helper::putFile()`, áp dụng toàn hệ thống (không tạo method riêng cho 1 màn).
2. **Giữ nguyên 100% tên gốc** kể cả dấu tiếng Việt + khoảng trắng. Chống trùng chuyển vào folder: `{folder}/{timestamp}-{random4}/{Tên gốc}.pdf`.
3. **FE**: tách `fileNameFromUrl()` (đang copy-paste ở 27 file) thành helper chung có `decodeURIComponent`, thay toàn bộ bản copy bằng import.
   - Đặt trong `utils/helpers.js` có sẵn (không tạo `utils/file.js` mới) — đúng convention repo: `export const` + import `@/utils/helpers`.

## Phạm vi ảnh hưởng

**BE** — `putFile()` được gọi từ 3 nơi:
- `Modules/Human/Http/Controllers/Api/V1/FileController.php:33` (`putFiles`) — endpoint `files/upload`, dùng chung TẤT CẢ màn upload
- `Modules/Timesheet/Http/Controllers/Api/V1/TimekeeperController.php:462` (`putFiles`)
- `app/Http/Controllers/Api/V1/ExcelTemplateController.php:150` (`putFile`)

Data cũ lưu URL đầy đủ trong DB → không bị ảnh hưởng bởi đổi format key.

**FE** — 27 file × 52 occurrence chứa bản copy `fileNameFromUrl()`.

## Task

### Phase 1 — BE
- [x] Sửa `CmcS3Helper::putFile()`: giữ tên gốc, timestamp+random vào path thư mục
- [ ] `putFileProduct()` — CÙNG bug (slug nuốt extension + nối timestamp/random). CHƯA sửa: ngoài scope, ảnh hưởng ảnh sản phẩm + đặt tên thumbnail/large. Cần quyết định riêng.

### Phase 2 — FE helper
- [x] Thêm `export const fileNameFromUrl` vào `utils/helpers.js` (có `decodeURIComponent` + try/catch, guard null)
- [x] Sửa 27 file:
  - 13 file: method là **code chết** (định nghĩa, không ai gọi) → xóa hẳn
  - 8 file script-only: xóa method, import helper, đổi `this.`/`self.` → gọi trực tiếp
  - 4 file dùng trong template: giữ key `fileNameFromUrl,` (shorthand ES6 trỏ vào import) để template + `this.` vẫn chạy
  - 2 file fallback riêng (`BaseUploadFileProduct` → `''`, `BaseUploadFileSelfNotification` → `url`): wrapper mỏng giữ nguyên semantics

### Phase 3 — Verify
- [x] Parse 27/27 file .vue (vue-template-compiler + @babel/parser) → không lỗi cú pháp
- [x] `php -l CmcS3Helper.php` sạch; mô phỏng đặt tên đúng; path traversal `../../etc/passwd` → `passwd`
- [x] Unit test `fileNameFromUrl` 6 case PASS (tên có dấu, ASCII, **URL format cũ**, null, không phải URL, `%` lỗi không crash)
- [x] Rủi ro dấu phẩy: `ObjectURL = @metadata.effectiveUri` (percent-encoded) → `,` thành `%2C`, KHÔNG phá `join(', ')` ở Training/JobAssignmentNote. Màn công tác phí dùng `json_encode` nên vốn đã an toàn.
- [ ] **CHƯA chạy end-to-end**: upload thật lên S3 qua app đang chạy (cần Laravel + Nuxt + S3 thật)
- [ ] Regression thực tế: các màn upload khác (jobassignment, training, company, timekeeper)
- [ ] File cũ (URL format cũ) vẫn hiển thị + tải được

## Checkpoint

### Checkpoint — 2026-07-16
Vừa hoàn thành: code xong BE (1 file) + FE (28 file: helper + 27 file dùng). Verify tĩnh đầy đủ.
Đang làm dở: không
Bước tiếp theo: user chạy app test upload file tên tiếng Việt ở `timesheet/request-payment-working-fee/add`
Blocked: end-to-end S3 chưa chạy — cần app chạy thật. `putFileProduct()` còn cùng bug, chờ quyết định.
