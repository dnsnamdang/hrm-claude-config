# Sửa gate duyệt Điều chuyển kho (17/11/2026) — @cuong61n

Lỗi: gate đọc `warehouse_accountants` (0 dòng) nên không ai duyệt được. Bảng sống: `accounting_warehouse_accountants (accounting_warehouse_id, accountant_id)`; kho kế toán trỏ kho vật lý qua `accounting_warehouses.warehouse_id` (49/55 kho kế toán có liên kết, 18 kho vật lý có kế toán).

## Đã sửa
- `Modules/Finance/Http/Controllers/V1/WarehouseTransferController.php` `isAccountantOf` (cuối file, ~dòng 414-433): join `accounting_warehouse_accountants` ⨝ `accounting_warehouses` theo `aw.warehouse_id` = kho nguồn. Hàm này là private, chỉ phục vụ `approve` + cờ `is_can_approve` ở `show` (cùng hàm nên cùng sửa).
- `Definitions/Finance/WarehouseTransferDefinition.php`: `approvers()` cùng truy vấn; `watchedTables` thêm `accounting_warehouse_accountants`, `accounting_warehouses` (bỏ `warehouse_accountants`); `version()` 1 → 2; bỏ `gate_blocker`; `seedTest` dùng kế toán thật (không ghi bảng kế toán), `deleteTest` bỏ xoá `warehouse_accountants`.
- Test: helper `accountant()` tạo kho kế toán `TESTWT-*` + pivot đúng bảng; chọn kho vật lý chưa có kế toán thật; ca "rỗng" còn chèn dòng vào bảng cũ để chứng minh không còn được đọc.

## Còn lại (không sửa, báo)
Vẫn đọc `warehouse_accountants` (chỉ thông báo, không phải gate): `ProductImportRequestService.php:796,1978`, `WarehouseImportWriteService.php:1343`; `PhysicalWarehouseService.php:201` còn xoá bảng cũ. Cùng gốc lỗi: thông báo kế toán kho ở các luồng nhập kho không ai nhận.
Lưu ý: kế toán kho vẫn cần mã xem phiếu điều chuyển (hoặc là người lập) mới duyệt được.

## Kiểm
phpunit WarehouseTransfer 5 test / 77 assertion xanh. Đột biến 4/4 bị bắt (bỏ lọc kho, bỏ lọc người, Definition bỏ lọc kho, quay lại bảng cũ). seed-test 6 phiếu → verify 18.120 cặp, 0 chênh lệch → clean-test.
