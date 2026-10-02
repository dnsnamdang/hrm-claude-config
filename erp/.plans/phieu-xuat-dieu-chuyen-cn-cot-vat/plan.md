# Plan — Phiếu xuất hàng ĐC chi nhánh: cột %VAT (#11319)

Repo `TanPhatDev`, nhánh `task_11319` (từ `master`). @junfoke.

## Tasks

- [x] T1. Màn chi tiết `show.blade.php`: hiện cột "% VAT" cho `type == 7`, giá trị `product.product.vat_percent`.
- [x] T2. Màn tạo/sửa `form.blade.php`: hiện cột "% VAT" cho `type == 7`, giá trị `product.product.vat_percent`.
- [x] T3. Bản in `getProductTableAttribute()` (ProductExport.php): thêm cột "% VAT" chỉ khi `type == 7`.
- [x] T3b. `WarehouseExport::getDataForProductExport()`: thêm `vat_percent` vào select quan hệ `product` (create form nạp từ phiếu xuất kho — nếu không thêm thì cột %VAT ở màn TẠO sẽ rỗng vì select cũ chỉ có `id, avatar`).
- [x] T4. Verify: `php -l` sạch (ProductExport + WarehouseExport); CRLF/LF giữ nguyên (LF); diff gọn 4 file. **Test browser XONG** (server bản B `artisan serve :8001`, DB local, phiếu **PXH-00717 id=717 type=7**, hàng product 40409 có `products.vat_percent=8.00` nhưng `product_export_details.vat_percent=0.00` — case chứng minh lấy đúng VAT gốc):
  - Chi tiết (show): cột **VAT / %** = **8** ✓
  - Sửa (edit): cột **% VAT** = **8** ✓
  - In phiếu (print): header + cột **% VAT** = **8** ✓
  - Tạo (create): kiểm payload `WarehouseExport::getDataForProductExport(787)` → `product` keys có `vat_percent=8.00` ✓ (trước fix chỉ id,avatar,units)

- [x] T5. Sửa giao diện header cột VAT ở màn chi tiết (`show.blade.php`): với phiếu KHÔNG phải bán hàng (type 4/7) chỉ có 1 cột VAT nhưng header vẫn bị tách 2 dòng "VAT" / "%" → gộp thành 1 ô `rowspan="2"` ghi "% VAT" (giống form.blade). Cột `colspan=2` "VAT" + sub-header "%" / "Số tiền" chỉ còn dùng khi `form.is_sale`. (Chưa verify browser — server local chưa chạy.)

- [x] T6. **Quy tắc VAT theo thời điểm** (yêu cầu bổ sung 2026-09-07, phiếu #815 dev-erp):
  - BE `ProductExportsController@store` + `@update`: với `type == 7`, `product_export_details.vat_percent` **luôn ghi lại theo `products.vat_percent` tại thời điểm lưu** (không tin payload FE). "Lưu & Duyệt" = lưu với `status = 1` → chính là chốt VAT tại thời điểm duyệt (sau duyệt `canEdit()` = false nên không đổi được nữa). Lấy VAT bằng 1 query `pluck` trước vòng lặp, không N+1.
  - Hiển thị: màn **Sửa** (chỉ mở được khi nháp) giữ đọc live `product.product.vat_percent`; màn **Chi tiết** + **bản in** đọc live khi `status == 3`, đọc **snapshot** `product.vat_percent` khi phiếu đã duyệt.
- [x] T8. **Test luồng thật trên local** (PXH-00717, type 7, DB `erp_dev_30_01_26`, server `artisan serve :8001`) — hàng `HN-809F-O90915-ZZD4:01` (product 40409):
  1. Danh mục 8 → **10**, mở màn Sửa → cột % VAT hiện **10** (trước fix hiện số đã lưu) ✓
  2. Bấm **Lưu** (status 3) → `product_export_details.vat_percent` 0 → **10** ✓
  3. Danh mục 10 → **5**, mở lại Sửa → hiện **5**; bấm **Lưu & Duyệt** → detail = **5**, phiếu `status = 1` ✓
  4. Danh mục 5 → **12** (sau khi duyệt) → màn **Chi tiết** vẫn **5**, **bản in** vẫn **5** (VAT chốt tại thời điểm duyệt, không chạy theo danh mục) ✓
  - Gotcha khi test: `update()` gọi `WarehouseExport::canApproveProductExportWhenEdit()` → PXK phải `status = 7` + user có quyền "Kế toán kho" + cùng `company_id`, không thì trả `{"success":false,"message":"Không đủ quyền!"}` (200, không có toast trên UI — phải xem response mới biết).
  - Đã khôi phục dữ liệu test: danh mục về 8, detail về 0, phiếu về `status = 1` / `created_by = 787`, PXK 787 về `status = 1`. **Lưu ý**: bước "Lưu & Duyệt" có chạy side-effect nghiệp vụ (hạch toán/kho/thông báo) trên DB local, không rollback được — chỉ ảnh hưởng snapshot dev.

- [ ] T7. **Backfill dữ liệu cũ** (chờ user quyết): 89 dòng `product_export_details` của phiếu type 7 đang có `vat_percent = 0` (không phân biệt được "0% thật" vì cột không null) → phiếu cũ đã duyệt sẽ hiện VAT = 0 sau khi đổi sang đọc snapshot. Đề xuất chạy 1 lần trước khi deploy:
  `UPDATE product_export_details d JOIN product_exports p ON p.id = d.parent_id JOIN products pr ON pr.id = d.product_id SET d.vat_percent = pr.vat_percent WHERE p.type = 7;`

## Files đã sửa

- `resources/views/warehouse/product_exports/show.blade.php` (header VAT/%, body value, gộp header "% VAT" 1 ô, đọc snapshot khi đã duyệt)
- `app/Http/Controllers/Warehouse/ProductExportsController.php` (store + update: ghi `vat_percent` theo danh mục lúc lưu, chỉ type 7)
- `resources/views/warehouse/product_exports/form.blade.php` (+2 sửa: header, body value)
- `app/Model/Warehouse/ProductExport.php` (`getProductTableAttribute` +cột VAT khi type 7)
- `app/Model/Warehouse/WarehouseExport.php` (`getDataForProductExport` select thêm `vat_percent`)

## Checkpoint

### Checkpoint — 2026-09-05
Vừa hoàn thành: code xong T1–T3b (chi tiết + tạo/sửa + in phiếu), `php -l` sạch, CRLF giữ nguyên, diff 4 file gọn.
Đang làm dở: —
Bước tiếp theo: user test browser (phiếu loại điều chuyển chi nhánh) rồi commit/merge task_11319 → master.
Blocked: chưa có sẵn phiếu type 7 để tự test browser.

### Checkpoint — 2026-09-07
Vừa hoàn thành: T5 — header cột VAT màn chi tiết không còn bị tách 2 dòng khi phiếu type 7 (1 ô "% VAT" rowspan=2).
Đang làm dở: —
Bước tiếp theo: user xem lại màn chi tiết PXH-00814 xác nhận header, rồi commit/merge task_11319.
Blocked:

### Checkpoint — 2026-09-07 (2)
Vừa hoàn thành: T6 — BE ghi VAT theo danh mục mỗi lần lưu (type 7), chi tiết/in đọc snapshot khi phiếu đã duyệt. `php -l` sạch, diff gọn 3 file.
Đang làm dở: —
Bước tiếp theo: user quyết T7 (backfill 89 dòng VAT=0 của phiếu type 7 cũ); test luồng Lưu / Lưu & Duyệt trên dev-erp với phiếu #815.
Blocked: local DB không có phiếu type 7 trạng thái nháp nên chưa test được luồng lưu bằng browser.

### Checkpoint — 2026-09-07 (3)
Vừa hoàn thành: T8 — test đủ luồng Lưu / Lưu & Duyệt / xem chi tiết / in trên local, cả 4 bước đúng kỳ vọng; dữ liệu test đã khôi phục.
Đang làm dở: —
Bước tiếp theo: user quyết T7 (backfill VAT cho 89 dòng phiếu type 7 cũ) rồi commit/merge task_11319.
Blocked: 
