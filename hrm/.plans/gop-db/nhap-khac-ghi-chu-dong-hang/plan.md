# Plan — #11908 Luồng nhập hàng loại "Nhập khác" (99): cột Ghi chú từng dòng hàng

**Người phụ trách:** @junfoke — 2026-10-28
Issue: http://quanly.dnsmedia.vn/issues/11908

## Ngày 28/10/2026 (@junfoke) — khảo sát

- [x] 28/10/2026 — Đọc issue (không có ảnh): YCNH loại Nhập khác có ô Ghi chú từng dòng — sửa được, không bắt buộc, nhận chữ / số / ký tự đặc biệt, placeholder "Mã số SX,.."; cùng phiếu, cùng mặt hàng mà trùng ghi chú → lỗi tại ô + toast "Nội dung ghi chú trùng nhau". ĐNNK, Phiếu dự kiến, PNK, PNH chỉ xem. Áp cho tạo / sửa / xem.
- [x] 28/10/2026 — Kiểm code `develop` (worktree gop-db): chưa có cột ghi chú ở `product_import_request_details`, `warehouse_import_request_details`, `warehouse_import_lot_details` (+ bảng `tmp_` của phiếu dự kiến), `product_import_details` → cần migration. Màn HRM đã port đủ 4 phiếu.
- [ ] Chờ user chốt các điểm đã hỏi → làm BE (migration + validate trùng) + FE 5 phiếu.

## Checkpoint — 2026-10-28

- **Vừa hoàn thành:** khảo sát issue + code.
- **Bước tiếp theo:** user chốt → triển khai.
- **Blocked:** chờ user chốt.
