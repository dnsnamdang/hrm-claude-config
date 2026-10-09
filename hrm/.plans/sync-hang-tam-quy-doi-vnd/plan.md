# Sync hàng tạm HRM→ERP: quy đổi giá về VND khi báo giá ngoại tệ

## Vấn đề
Báo giá HRM có `currency_id` + `exchange_rate` (ngoại tệ). Giá dòng `estimated_price`/`quoted_price` nhập theo loại tiền báo giá (có thể ngoại tệ), chưa quy VND. `TmpProductSyncService` gửi giá thô sang ERP (không kèm currency/tỷ giá) → ERP hiểu là VND → sai khi báo giá ngoại tệ.

## Fix (user chốt: phương án A — quy đổi VND khi sync)
- [x] `TmpProductSyncService.php`: `$rate = $quotation->exchange_rate ?: 1;` (mặc định 1 nếu null/0 để không phá báo giá VND); gửi `estimated_price = estimated_price * $rate`, `quoted_price = quoted_price * $rate`.
- [ ] User test: sync 1 báo giá ngoại tệ → giá ERP = giá × tỷ giá (VND).

## Giả định cần user xác nhận
- `exchange_rate` là tỷ giá "1 ngoại tệ = X VND" (VND = giá × exchange_rate). Báo giá VND có `exchange_rate = 1`.

## File
- `hrm-api/Modules/Assign/Services/TmpProductSyncService.php`
