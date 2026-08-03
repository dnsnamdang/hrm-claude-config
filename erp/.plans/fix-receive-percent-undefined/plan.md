# Fix: Undefined property receive_percent (getReceivePercent)

## Bug
`getReceivePercent` đọc `$commission->receive_percent`/`->from_day` từ JSON `conditions_commissions` (quy chế hoa hồng) không guard → dòng config dở (thiếu receive_percent) làm văng Undefined property. Báo ở FirmSettlementContractService:1564 (userId 787).

Lặp 3 bản: FirmSettlementContractService:1553, SettlementContractService:1473, WrSettlementContractService:1842.

## Fix
Lọc bỏ dòng thiếu from_day/receive_percent trước usort+loop (mirror `?? 0` đã có ở DepartmentsController). Hành vi dữ liệu hợp lệ không đổi.

## Tasks
- [x] Sửa 3 bản getReceivePercent (master) — array_filter bỏ dòng thiếu from_day/receive_percent trước usort+loop. +6 dòng/file.
- [x] php -l 3 file → sạch
- [ ] User verify lại luồng quyết toán trên quy chế lỗi (chưa commit)

### Checkpoint — 2026-06-29
Code xong 3 bản, php -l sạch, **chưa commit** (chờ user). Bước tiếp: user mở lại luồng quyết toán hãng (userId 787 / quy chế lỗi) xác nhận hết văng.
