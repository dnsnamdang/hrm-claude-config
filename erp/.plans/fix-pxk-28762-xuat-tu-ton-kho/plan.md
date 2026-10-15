# Fix: PXK-28762 không tạo được phiếu xuất (lỗi prepick) → cho xuất từ tồn kho

## Bối cảnh / Root cause (đã xác minh trên prod erp_new)
- Tạo phiếu xuất từ `product_exports/create?warehouse_export_id=28762` báo lỗi
  `ProductExport.php:1427` "Mã hàng: GROZ-MP23R Xuất nhiều hơn lượng prepick hiện có".
- Chỉ **1 dòng** gây lỗi: `warehouse_export_request_details` id=**72058** (request 29047,
  product 4481 GROZ-MP23R) có `export_prepick_qty=1` (ghi 2026-07-03).
- Ngày **2026-07-05 21:25** ai đó chạy `(new \UpdateDB)->resetPrepickDetailQtyCompany4()`
  → reset TẤT CẢ `prepick_details` company_id=4 về 0 (1875 dòng). Giữ của mã này (prepick_detail 46876)
  về 0, nhưng `export_prepick_qty` trên request KHÔNG bị reset → FE vẫn gửi `export_from_prepick=1`,
  BE query prepick_details thấy 0 → guard 1427 throw.
- Kho 4 còn tồn total_qty=19 → xuất 1 từ tồn kho hợp lệ. Chưa có product_export nào cho WE 28762.

## Quyết định (user chọn)
- KHÔNG khôi phục 1874 giữ. Chỉ sửa **riêng phiếu PXK-28762** để xuất từ **tồn kho**, bỏ prepick.

## Fix
- [x] Thêm method `fixPxk28762ExportFromStock()` vào `database/seeds/UpdateDB.php`:
      zero `export_prepick_qty` (và `export_hold_qty`) cho các dòng `parent_id=29047` (chỉ ảnh hưởng
      dòng 72058). FE mở lại create → `export_from_prepick=0`, `export_from_stock=total` → xuất tồn.
- [x] Chạy `(new \UpdateDB)->fixPxk28762ExportFromStock()` trên prod → sửa 1 dòng (72058),
      verify `export_prepick_qty=0`, `export_total_qty=1` giữ nguyên.
- [ ] User mở lại `product_exports/create?warehouse_export_id=28762` → tạo phiếu → xuất kho OK.

### Checkpoint — 2026-07-15
Vừa hoàn thành: điều tra root cause (script reset prepick company 4 làm stale export_prepick_qty) +
thêm & chạy `fixPxk28762ExportFromStock()` trên prod (dòng 72058 prepick 1→0).
Đang làm dở: (không)
Bước tiếp theo: user mở lại create form phiếu PXK-28762 → tạo phiếu xuất → xác nhận xuất từ tồn kho OK.
Blocked:

## Không làm
- Không đụng `prepick_details` / `prepick_logs` (giữ nguyên hiện trạng reset).
- Không sửa guard BE ở `ProductExport.php` (đúng nghiệp vụ, giữ nguyên).
