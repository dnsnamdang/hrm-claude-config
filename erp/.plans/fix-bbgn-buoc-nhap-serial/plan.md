# Fix: Biên bản giao nhận hàng hóa — hàng buộc serial vẫn cho lưu khi thiếu serial

## Bối cảnh
`admin/accounting/handover_acceptance_product_records` (controller `Sale/HandoverAcceptanceProductRecordsController`). Hàng có tính chất **buộc nhập serial** (product_type NGOÀI cấu hình `serial_product_types` = "Hàng không bắt buộc Serial") vẫn lưu được khi chưa nhập serial. VD BBGN.00030 / mã BT3D--T4DT135H.

## Root cause (reproduce được)
`validateSerialRequirements`: `if ($handoverQty <= 0 || ...) continue;` → khi **SL bàn giao trống** (=0) thì bỏ qua cả dòng → hàng buộc serial né validation. Chỉ chặn đúng khi SL bàn giao > 0.

## Fix (đã chốt phương án A)
- [x] Hàng buộc serial: **không bỏ qua khi SL bàn giao trống**; yêu cầu **SL bàn giao > 0 VÀ đủ serial theo SL bàn giao**.
- [x] Message: `"[Mã hàng] - [Tên hàng] buộc nhập serial."`
- [x] Verify reflection 4 ca: buộc+SL0 chặn, buộc+SL2 thiếu serial chặn, buộc+SL2 đủ pass, không buộc pass.
- [x] php -l sạch; config test khôi phục.

## Nhánh
- task_10533 (đang test local) → commit + push.
- develop_01 (dev-erp chạy) → cherry-pick + push. Method validateSerialRequirements giống hệt.
