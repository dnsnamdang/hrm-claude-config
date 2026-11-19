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

## Fix #11892 — Màn Thêm chọn phiếu kiểm kê + nút Lưu và tiếp tục (2026-10-28, @junfoke)

- [x] 28/10/2026 — Bug 1: màn Thêm có ô "Phiếu kiểm kê" (chỉ phiếu Chờ xử lý / Đang xử lý còn hàng thừa chưa nhập điều chỉnh), làm giống phiếu xuất điều chỉnh; ô Kho khoá tới khi chọn phiếu; vào từ chi tiết phiếu kiểm kê thì chọn sẵn như cũ. BE thêm API `source-options`.
- [x] 28/10/2026 — Bug 2: thêm nút "Lưu và tiếp tục" giữa Lưu và Gửi duyệt; lưu xong form làm trống để lập phiếu tiếp.
- [x] 28/10/2026 — Commit `develop`: client `51b04d60e`, api `76c7eb60f` (đã lên origin/develop).
- [ ] Test trọn luồng chọn phiếu → lưu → Lưu và tiếp tục trên dev (local không có phiếu kiểm kê Chờ / Đang xử lý).
