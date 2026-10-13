# Redmine #11583 — Phiếu xử lý yêu cầu: lưu xong quay về danh sách kèm `?type=all`

## Phase 1
### FE
- [x] WarrantyRepairHandleRequestForm: Lưu / Gửi / Xoá / lỗi lập phiếu / nút Quay lại đều về `/customer-care/warranty-repair-handle-requests?type=all` (khớp link menu)
- [x] Test Playwright: lập phiếu từ màn Yêu cầu KTSC-BH → về đúng URL, dọn phiếu thử

### Checkpoint — 2026-10-07
Vừa hoàn thành: sửa + test Playwright (Quay lại / Lưu nháp / Xoá đều về `?type=all`), đã dọn phiếu thử
Đang làm dở: —
Bước tiếp theo: commit khi user yêu cầu
Blocked:
