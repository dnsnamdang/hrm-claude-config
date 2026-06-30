# Task P5 FE — Yêu cầu xuất hàng (cha-con) + payload phiếu xuất kho

## STATUS: DONE

## Định vị màn

### Màn TẠO YÊU CẦU XUẤT HÀNG (rút SL từ HĐ hãng)
- Blade: `resources/views/warehouse/product_export_requests/create.blade.php`
  - Gọi `getDataForWarehouseExport` tại dòng 126, 155, 176 (`/admin/sale/firm-contracts/{id}/getDataForWarehouseExport`)
  - type 14 = xuất bán HĐ hàng, type 15 = xuất KM HĐ hàng
- Form (UI): `resources/views/warehouse/product_export_requests/form.blade.php`
  - Bảng **flat list** `form.products`: dòng 626-651 (ô SL ở 651, `ng-disabled="form.firm_contract.id"` → KHÓA cho HĐ hãng)
  - Bảng **theo tab** `tab.products`: dòng 740-820 (ô SL đề nghị ở dòng 804, EDIT được — đây là surface nhập liệu thực tế cho HĐ hãng)
- JS controller logic: `resources/views/warehouse/product_export_requests/formJs.blade.php`
- Class JS dòng SP:
  - Flat list: `resources/views/partials/classes/warehouse/ProductExportRequestDetail.blade.php` (class `ProductExportRequestDetail`)
  - Theo tab: `resources/views/partials/classes/warehouse/ProductExportRequestTabProduct.blade.php` (class `ProductExportRequestTabProduct`) ← màn HĐ hãng nhập SL ở đây
  - Tab: `ProductExportRequestTab.blade.php`; Root: `ProductExportRequest.blade.php`

### Màn TẠO PHIẾU XUẤT KHO
Có 2 dòng phiếu xuất kho:
1. **WarehouseExport** (đề nghị xuất kho): `resources/views/warehouse/warehouse_exports/create.blade.php`
   - Lấy data: `/admin/warehouse/warehouse_export_requests/{id}/getDataForWarehouseExport` (dòng 651)
   - Class: `WarehouseExportTabProduct.blade.php`, `WarehouseExportTab.blade.php`, `WarehouseExport.blade.php`
2. **ProductExport** (xuất kho thực): `resources/views/warehouse/product_exports/create.blade.php`
   - Lấy data: `/admin/warehouse/product_export_requests/{id}/getDataForProductExport` (dòng 175) HOẶC `/admin/warehouse/warehouse_exports/{id}/getDataForProductExport` (dòng 103)
   - Class: `ProductExportTabProduct.blade.php`, `ProductExportTab.blade.php`, `ProductExport.blade.php`

## Cơ chế max/qty hiện tại

- BE `FirmContractProductExportService::formatWarehouseExportData` đặt mỗi product **theo tab** (`parent.tabs[].products[]`):
  `qty` = số lượng CÒN ĐƯỢC XUẤT (cha-con aware: childAwareRemaining − joinExportingQty), kèm
  `firm_contract_tab_product_id`, `child_parent_id`, `child_ratio`, `contract_qty`, `exporting_qty`
  (dòng 371-376 service). Product thô của tab còn có `quantity`, `exported_qty`.
- Flat top-level `products` (feed `response.data.products`, dòng 119-168 service) KHÔNG cha-con aware và
  KHÔNG có fctp_id — nhưng với HĐ hãng ô flat bị disabled, và `qty` của flat list được tính bằng cách
  cộng dồn từ `tab_products` (getter `ProductExportRequestDetail.qty` dòng 37-42) → giá trị cuối vẫn đúng.
- Trước sửa: `ProductExportRequestTabProduct` setter `qty` chặn max bằng công thức CŨ
  `contract_qty - exported_qty - exporting_qty` (sai với cha-con).

## Chỗ sửa

### TASK 5.3 — chặn max theo `qty` cha-con BE trả
File: `resources/views/partials/classes/warehouse/ProductExportRequestTabProduct.blade.php`
- `after()` (dòng ~7-12): lưu `this.max_export_qty = Number(form.qty)` — chính là SL còn được xuất BE trả.
- Thêm getter `max_allowed_qty`: ưu tiên `max_export_qty` (cha-con aware), fallback công thức cũ nếu BE
  không gửi (legacy-safe).
- Setter `qty`: clamp về `this.max_allowed_qty` thay vì công thức cũ.
→ Ô nhập SL đề nghị tự kẹp về trần cha-con; không thể vượt → chặn submit hiệu quả.
  Lỗi BE quỹ vẫn hiện inline tại `errors['products.'+$index+'.qty']` (form.blade dòng 805-807).

### TASK 5.3 — payload yêu cầu xuất có fctp_id: ĐÃ CÓ SẴN
- `ProductExportRequestTabProduct.submit_data` đã có `firm_contract_tab_product_id` (dòng 104, không sửa).
- Root `ProductExportRequest.submit_data` gửi `tabs: this.tabs.map(val => val.submit_data)` (dòng 879).
- BE `ProductExportRequestsController::store` validate quỹ cha-con đọc đúng từ
  `$request->tabs[].products[].firm_contract_tab_product_id` (dòng 615-649). → KHỚP, không cần sửa thêm.

### TASK 5.5 — payload phiếu xuất kho có fctp_id: ĐÃ CÓ SẴN (BE serve + FE submit đều đủ)
FE submit_data đã có `firm_contract_tab_product_id`:
- `WarehouseExportTabProduct.submit_data` (dòng 56)
- `ProductExportTabProduct.submit_data`
BE serve cho màn phiếu xuất kho đều trả field này (cột đã có trong DB):
- `WarehouseExportRequest::getDataForWarehouseExport` → tab products select `warehouse_export_request_tab_products.*` (model dòng 304)
- `ProductExportRequest::getDataForProductExport` → tab products select `product_export_request_tab_products.*` (model dòng 1174)
- `WarehouseExport::getDataForProductExport` → eager load `'tabs.products'` full cột (model dòng 381)
Migration cột: 2022_10_25 (request_tab_products), 2026_06_20_100003 (product_export_request_tab_products),
2026_06_20_100004 (product_export_tab_products + warehouse_export_tab_products). → Đủ 4 bảng.

## php -l
- `resources/views/partials/classes/warehouse/ProductExportRequestTabProduct.blade.php`: No syntax errors detected.

## File sửa
- resources/views/partials/classes/warehouse/ProductExportRequestTabProduct.blade.php (1 file duy nhất)

## Concern
- Flat list `ProductExportRequestDetail` setter `qty` (dòng 50-51) vẫn dùng công thức cũ — KHÔNG sửa vì với
  HĐ hãng ô này bị disabled và giá trị derive từ tab_products. Nếu sau này có flow HĐ hãng cho phép nhập
  trực tiếp trên flat list thì cần xem lại.
- `max_export_qty` lấy từ `form.qty` BE trả. Nếu BE đổi tên field "còn được xuất" sang tên khác (vd
  `remaining_qty`) thì FE phải cập nhật theo.
