# Phiếu nhập kho điều chỉnh kiểm kê — Plan

Người phụ trách: @khoipv
Màn: `hrm-client/pages/warehouse/inventory-imports/` · BE: `Modules/Finance` (`WarehouseInventoryImportController`, `InventoryImport/WarehouseInventoryImportWriteService`)

## Fix #11856 — Chưa validate dung lượng file đính kèm (2026-10-26)

- [x] BE: thay rule `mimes:` bằng closure kiểm ĐUÔI file (`WarehouseInventoryImportWriteService::attachmentFileRule()`), dùng cho cả endpoint `upload-files` lẫn lưu phiếu — `mimes` đoán theo nội dung nên file .pdf đúng đuôi bị báo "Chỉ nhận file…" và che lỗi dung lượng
- [x] BE: thêm message `attachments.*.uploaded` = "Dung lượng tối đa 20MB" (file vượt giới hạn PHP)

### Checkpoint — 2026-10-26
Vừa hoàn thành: fix #11856; kiểm qua HTTP kernel: pdf 21MB → "Dung lượng tối đa 20MB", .txt → "Chỉ nhận file pdf, png, jpg, jpeg", pdf giả 10MB → qua rule
Đang làm dở: —
Bước tiếp theo: deploy dev (dev đang chạy bản trước #11841, vẫn hiện 15MB) rồi QA test lại
Blocked:
