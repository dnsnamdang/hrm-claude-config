# YCXH — Bổ sung lịch sử còn thiếu (Redmine #11388) — Plan

Nguồn: Redmine #11388 (YCXH thiếu ghi lịch sử: xuất thẳng + file đính kèm). Nhánh `gop_db`.
Xem `design.md` cùng thư mục cho root cause đã trace.

## Phase 1 — BE (hrm-api)

### Case #1 — persist `is_export_direct` cho loại nhập tay
- [x] `ProductExportRequestService::createManual()` — thêm `is_export_direct` vào `fill()` + gỡ kho khi xuất thẳng.
- [x] `ProductExportRequestService::updateFromRequest()` nhánh `!$isContractType` — gán `is_export_direct` + gỡ kho khi xuất thẳng (mirror nhánh contract).

### Case #2 — lịch sử file đính kèm (khoá dạng BẢNG)
- [x] `CatalogHistoryService::TABLES['product_export_requests']` thêm `'attachment_rows' => 'Tệp đính kèm'`.
- [x] `ProductExportRequestService`: `catalogColumns()` thêm `attachment_rows`; `catalogDisplay()` xử lý `attachment_rows`.
- [x] `ProductExportRequestService::attachmentRows($model)` — đọc từ `$model->files()`.
- [x] `ProductExportRequestService`: gộp ghi file vào create/update (đọc `$data['attachment_urls']`), snapshot + set virtual trước khi log.
- [x] Public `attachmentHistorySnapshot()` / `logAttachmentChanged()` cho các endpoint rời.
- [x] Controller: bỏ 2 lời gọi `persistAttachmentUrls` ở store/update (đã chuyển vào service); thêm log ở `deleteFile` / `deleteAttachment` / `uploadAttachments`; gỡ method controller cũ.
- [x] `deleteCompletely()` snapshot xoá gồm cả `attachment_rows`.
- [x] `php -l` sạch các file BE.

## Phase 2 — Verify
- [x] Playwright: sửa YCXH loại nhập tay → tick/bỏ tick Xuất thẳng → lưu → lịch sử có dòng "Xuất thẳng: Không → Có".
- [x] Playwright: thêm/xoá file đính kèm → lịch sử có dòng "Tệp đính kèm" thêm/xoá.
- [x] Kiểm cả 2 nơi: popup Lịch sử (danh sách) + mục Lịch sử (chi tiết).

## Checkpoint

**2026-09-23 — Verify PASS (Playwright MCP, DB erp_hrm_check local).** Test trên PYCXH-35448 (loại 99 "Xuất khác" = nhập tay), tài khoản DNS Admin.

- **Case #1 — Xuất thẳng:** tick "Xuất thẳng" + lưu → DB `is_export_direct` 0→1, `warehouse_id` 2→NULL (gỡ kho đúng như nhánh contract). `catalog_histories` sinh dòng "Kho xuất: Liên Ninh → (trống)" + "Xuất thẳng: Không → Có". Xác nhận vừa **fix mất dữ liệu** vừa **có log**.
- **Case #2 — File đính kèm:** thêm 1 file PDF → log "Tệp đính kèm thêm mới: …pdf"; xoá file đó → log "Tệp đính kèm đã xóa: …pdf". Khoá dạng BẢNG (`attachment_rows`) hiển thị đúng.
- **Cả 2 nơi hiển thị OK:** popup "Lịch sử thay đổi" ở màn danh sách + mục "Lịch sử" ở màn chi tiết — cả hai render đủ 3 dòng giống nhau.

**Đã dọn test data trên local:** revert PYCXH-35448 (`created_by` 13→311, `is_export_direct`→0, `warehouse_id`→2, `updated_at` gốc); khôi phục dòng chi tiết SP 7318 (qty 0) bị luồng re-save chi tiết làm rớt khi lưu form; xoá `catalog_histories` #4/#5/#6; xoá file test trên đĩa. *(Lưu ý: object S3 test-dinhkem-…pdf trên cloud CMC không xoá được từ đây — rác vô hại.)*

**Chưa commit** — chờ user duyệt (ràng buộc plan).
