# Bỏ bắt buộc file đính kèm — bảng Tiến độ thực hiện (Báo giá)

**Phụ trách:** @khoipv
**Bắt đầu:** 25/09/2026
**Phạm vi:** chỉ BE, chỉ màn Báo giá (`plan/quotation`)

## Bối cảnh

Tab **Tiến độ thực hiện** của màn Báo giá: thêm dòng nào là bắt buộc dòng đó phải upload file
(`progress_report_attachments.*.name => required`). User yêu cầu bỏ bắt buộc file, **giữ nguyên**
bắt buộc *Ngày thực hiện* + *Nội dung thực hiện*.

FE không chặn phía client — chỉ render lỗi BE trả về → không phải sửa FE, không cần build client.

## Phase 1 — BE

- [x] `Modules/Category/Http/Requests/StoreQuotationRequest.php:51` — `progress_report_attachments.*.name`: `required|max:255` → `nullable|max:255`
- [x] `Modules/Category/Http/Requests/UpdateProgressReportAttachmentsRequest.php:20` — sửa tương tự
- [x] `php -l` 2 file

## Phase 2 — Test UI

- [ ] `plan/quotation/add`: thêm dòng tiến độ chỉ điền Ngày + Nội dung, không upload file → lưu được
- [ ] Màn chi tiết báo giá: nút **Lưu tiến độ** (`updateProgressReportAttachments`) → lưu được dòng không file
- [ ] Bỏ trống Ngày hoặc Nội dung → vẫn báo lỗi bắt buộc (không bị nới lỏng ngoài ý muốn)
- [ ] Kết xuất báo giá (`render`) → không đổi hành vi (rule `.name` vốn đã comment sẵn)

## Quyết định / ghi chú

- `StoreQuotationRequest` phục vụ `QuotationController::store()` + `update()`. `BidPackageController`
  và `ProductUnitPriceController` chỉ `use` thừa chứ **không dùng** → sửa không ảnh hưởng màn khác.
- `RenderQuotationRequest:22` vốn đã comment rule `.name` → không phải sửa.
- GIỮ NGUYÊN rule `$validator->after()` (StoreQuotationRequest:112): khi *Ngày YC hoàn thành <
  Ngày hoàn thành* thì vẫn bắt buộc có **ít nhất 1 dòng** tiến độ — đây là bắt buộc *bảng*, không
  phải bắt buộc *file*.
- `QuotationService::store()/updateProgressReportAttachments()` đã dùng `$item['name'] ?? null`
  → lưu dòng không file an toàn, không cần sửa.
- NGOÀI PHẠM VI: bảng Tiến độ thực hiện ở màn **Hợp đồng** (`pages/contract/contract`) và
  **Gói thầu** (`pages/bid_package`) có cấu trúc tương tự nhưng không đụng tới.

### Checkpoint — 25/09/2026
Vừa hoàn thành: Phase 1 — đổi `progress_report_attachments.*.name` từ `required|max:255` sang
`nullable|max:255` ở `StoreQuotationRequest.php:51` và `UpdateProgressReportAttachmentsRequest.php:20`;
`php -l` sạch cả 2 file. Đã kiểm tra cột `quotation_attachments.name` + `.link` vốn `nullable`
(migration `2025_08_30_083858`, `2025_05_02_225311`) → KHÔNG cần migration.
Đang làm dở: (không)
Bước tiếp theo: Phase 2 — test UI trên màn `plan/quotation/add` + nút "Lưu tiến độ" ở màn chi tiết.
Blocked:
