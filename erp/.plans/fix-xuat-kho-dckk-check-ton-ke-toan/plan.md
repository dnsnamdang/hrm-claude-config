# Fix: Xuất kho ĐCKK phải check tồn kế toán

## Bối cảnh
Phiếu **xuất kho điều chỉnh kiểm kê** (`warehouse_inventory_export`) hiện chỉ thao tác tồn **vật lý** (position + import_lot theo kiểm kê), KHÔNG check tồn kế toán. Hệ quả: phiếu tạo/duyệt xuất kho được, nhưng đến bước **xuất hàng** (`inventory_export`) mới bị chặn vì `in_stock` kế toán = 0 (do prepick giữ chỗ toàn công ty).

Ví dụ thực tế: PXKĐCKK-00034, product 13735, kho SG (wh 4), 1 tồn KT SG01 bị prepick #52146 (NV 583 → KH 23848) → `available = 1 − 1(prepick) − 0(hold) = 0`.

## Yêu cầu
Thêm check tồn kế toán vào bước **xuất kho ĐCKK** (`store` + `update`) để chặn sớm, dùng đúng công thức bước xuất hàng (`InventoryExportsController::validateAccountingWarehouse` → `Product::getAccountingStockDetail`, so `in_stock < qty`). KHÔNG sửa hàm dùng chung `getAccountingStockDetail`, chỉ gọi lại.

## Map kho vật lý → kho kế toán
`AccountingWarehouse` lọc theo `warehouse_id == kho vật lý && company_id == import_lot.company_id` (giống filter FE bước xuất hàng). VD wh 4 + cty 4 → [7, 8].

## Tasks
- [x] Thêm method `validateAccountingStock($details, $warehouse_id)` trong `WarehouseInventoryExportsController` — mỗi dòng: map acc warehouse theo `warehouse_id + import_lot.company_id`, gọi `getAccountingStockDetail(product_id, acc_ids, {unit_id, employee_id, company_id})`, nếu `in_stock < qty` → trả lỗi kèm mã hàng + SL được xuất.
- [x] Gọi check trong `store()` (trước `DB::beginTransaction`)
- [x] Gọi check trong `update()` (trước `DB::beginTransaction`)
- [x] Thêm `use` imports: `App\Product`, `App\Model\Warehouse\AccountingWarehouse`, `App\Model\Warehouse\WarehouseImportLot`
- [x] Verify mapping bằng data thật phiếu #34 (product 13735, lô 29360 → cty 4 → acc_ids [7,8], in_stock=0 < qty=1 → chặn đúng)
- [ ] Test trên UI: tạo lại phiếu ĐCKK product bị prepick → phải bị chặn ngay ở bước xuất kho (user test)

### Checkpoint — 2026-07-31
Vừa hoàn thành: BE validateAccountingStock (store + update) + imports, php -l sạch, verify mapping bằng data prod
Đang làm dở: (không)
Bước tiếp theo: user test trên UI; cân nhắc thêm cột "SL được xuất" trên form xuất kho nếu muốn hiện trực quan
Blocked:
