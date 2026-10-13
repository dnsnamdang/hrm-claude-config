# Fix: PXK-29117 chuyển hàng về xuất từ tồn kho (giống PXK-28762)

## Bối cảnh (xác minh trên prod erp_new)
- warehouse_exports id=29117, code PXK-29117 → warehouse_export_request_id=28995, kho 4, công ty 4.
- 3 dòng detail (parent_id=28995): #71926 (prod 20053) prepick0/total2, **#71927 (prod 4397 Máy nén khí piston 3HP) prepick=1/total1** ← cần sửa, #71928 (prod 7893) prepick0/total1.
- Chưa có product_export nào cho WE 29117. Công ty 4 = công ty từng bị reset prepick 2026-07-05 → cùng ca stale export_prepick_qty như 28762.

## Fix
- [x] Thêm `fixPxk29117ExportFromStock()` vào database/seeds/UpdateDB.php (mirror fixPxk28762): zero export_prepick_qty + export_hold_qty các dòng parent_id=28995 (chỉ #71927), giữ export_total_qty.
- [x] Chạy `(new \UpdateDB)->fixPxk29117ExportFromStock()` trên prod → sửa 1 dòng (#71927 prepick 1→0), verify 3/3 dòng prepick=0/hold=0, giữ total. TẤT CẢ xuất từ tồn kho.
- [ ] User mở lại product_exports/create?warehouse_export_id=29117 → tạo phiếu → xuất tồn kho OK.

## Không làm
- Không đụng prepick_details/prepick_logs. Không sửa guard ProductExport.php.
