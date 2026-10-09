# Fix — Validate xuất kho vượt SL: báo cụ thể hàng nào

## Bối cảnh
URL: `admin/warehouse/warehouse_exports/{id}/edit`. Khi số lượng xuất vượt số lượng có thể xuất, hệ thống báo chung chung "Số lượng xuất vượt quá số lượng có thể xuất!" — không biết hàng nào.

## Root cause
`WarehouseExportsController::validateLots()` dòng 1960: trả message cố định, không kèm tên hàng/lô/vị trí. Method này dùng chung cho store (381), update (857), reExport (1595).

## Fix
- [x] Tại vòng lặp check `$qty > $stock->qty` (1948-1962): lấy tên hàng (`Product::find($ids[0])->name`), số lô (`warehouse_import_lots.lot_number`), vị trí (`Position::find($ids[1])->name`), ghép vào message: `Hàng "X" (lô ..., vị trí ...): số lượng xuất (a) vượt quá số lượng có thể xuất (b)!`. Mẫu tham chiếu `PrepickTransfer2Controller:391`.
- [ ] User test trên edit phiếu 28558.

## File
- `app/Http/Controllers/Warehouse/WarehouseExportsController.php` (validateLots ~1948-1962)
