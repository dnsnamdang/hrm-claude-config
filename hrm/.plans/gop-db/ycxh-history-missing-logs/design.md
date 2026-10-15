# YCXH — Bổ sung lịch sử còn thiếu (Redmine #11388) — Design

> Nhánh: `gop_db` · Phụ trách: @namdangit · Nguồn: Redmine #11388
> "[ERP => HRM] Yêu cầu xuất hàng: Thiếu chức năng Lịch sử Ngoài danh sách và Xem chi tiết"
> Tester Nguyễn Minh Hằng bật lại "Code xong chờ test" với 2 phản hồi:
> 1. **Tick/Bỏ tick "Xuất thẳng" không thấy ghi lịch sử.**
> 2. **Thay đổi file đính kèm không thấy ghi lịch sử.**

Màn: `finance/product-export-requests` (bảng `product_export_requests`). Lịch sử đã dựng sẵn
(trait `LogsCatalogHistory` + `CatalogHistoryService`, popup danh sách + mục Lịch sử chi tiết).
Chỉ 2 hành động dưới đây chưa sinh log — đã trace ra ROOT CAUSE, không phải lỗi hiển thị.

## Root cause (đã trace, không đoán)

### Case #1 — "Xuất thẳng" (`is_export_direct`)
`is_export_direct` ĐÃ nằm trong `catalogColumns()` nên nếu giá trị đổi thì tự có log. Nhưng với
**loại nhập tay (6 ĐC nội bộ, 12 hàng gửi, 18 sản xuất, 99 khác)** cờ này **không bao giờ được ghi**:
- FE `showExportDirect` = mọi loại trừ 3 (mượn) / 15 (KM hãng) → checkbox HIỆN + payload GỬI
  `is_export_direct` cho cả loại nhập tay (ProductExportRequestForm.vue:996, 1650).
- BE `createManual()` **không** có `is_export_direct` trong mảng `fill()` → tạo mới luôn = 0.
- BE `updateFromRequest()` nhánh `!$isContractType` (loại nhập tay) **không** gán `$req->is_export_direct`
  → sửa xong DB vẫn giữ nguyên → `logCatalogUpdate` diff ra "không đổi" → **không log**.
- Loại HĐ (20/21) và loại 7 (điều chuyển) thì BE CÓ gán (`updateFromRequest` nhánh contract:771-772,
  `updateTransfer`:549) nên vẫn log bình thường → chỉ loại nhập tay dính.

→ Đây vừa là lỗi **mất dữ liệu** (bấm xuất thẳng loại nhập tay không lưu) vừa là lỗi **thiếu log**.

**Fix:** persist `is_export_direct` (và gỡ kho khi xuất thẳng, mirror nhánh contract) ở `createManual()`
+ nhánh `!$isContractType` của `updateFromRequest()`. Không đụng `catalogColumns` (đã có sẵn).

### Case #2 — File đính kèm (bảng `files`)
Đính kèm YCXH lưu ở bảng chung `files` (`table='product_export_requests'`), KHÔNG phải cột trên
phiếu. Toàn bộ đường ghi/xoá file **không** sinh log:
- Thêm khi lưu: `persistAttachmentUrls()` (controller, gọi SAU `create/update`) — chỉ tạo bản ghi `files`.
- Xoá tức thì: endpoint `deleteFile` (`DELETE /{id}/files?file_url=`) — AttachmentSection gọi ngay khi
  bấm xoá (không đợi lưu phiếu).
- `attachment_rows` chưa có trong `catalogColumns()` cũng chưa có trong `CatalogHistoryService::TABLES`.

**Fix (theo mẫu bill-payment — skill entity-history §3b, khoá dạng BẢNG):**
- `CatalogHistoryService::TABLES['product_export_requests']` thêm `'attachment_rows' => 'Tệp đính kèm'`.
- Service: thêm `attachment_rows` vào `catalogColumns()` + `catalogDisplay()`; thêm `attachmentRows($model)`
  đọc từ `$model->files()` → `['__key'=>file_path, '__name'=>file_name, 'Tệp'=>file_name]`.
- **Gộp việc ghi file vào chính luồng create/update của service** (đọc `attachment_urls` sẵn có trong
  `$data`): tạo mới → file vào ngay dòng "Tạo mới"; thêm khi sửa → gộp vào dòng "Thay đổi thông tin".
  Bỏ 2 lời gọi `persistAttachmentUrls` ở controller store/update.
- Xoá tức thì (`deleteFile`/`deleteAttachment`/`uploadAttachments` — các endpoint rời): snapshot TRƯỚC
  + `logCatalogUpdate` SAU (helper public `attachmentHistorySnapshot()` / `logAttachmentChanged()`).
  Xoá là request riêng nên là dòng log riêng — không tránh được, và đồng nhất add/remove.

## Ràng buộc
- Không tạo bảng mới; dùng chung `catalog_histories` (giống các phiếu Finance).
- `attachment_rows`/`details_rows` là khoá ẢO — TUYỆT ĐỐI không gán lên model trước `save()`.
- Verify FE bằng Playwright trước khi báo xong (thêm/xoá file + tick xuất thẳng loại nhập tay).
