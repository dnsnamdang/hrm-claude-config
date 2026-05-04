# Plan: Phiếu báo có loại NCC chọn phiếu xuất hàng (TanPhatDev)

## Trạng thái
- Bắt đầu: 2026-04-28
- Tiến độ: ✅ Hoàn thành 2026-04-29 (12 task code + migration + 7 case manual test)

## Phase 1: Backend

### Migration
- [x] Task 1: `database/migrations/2026_04_28_000001_add_product_export_id_to_bill_income_report_details.php` — thêm `product_export_id BIGINT NULL` + index `idx_product_export`

### ProductExport.php
- [x] Task 2: Block `bill_income_report_supplier` (L1071-1081): bổ sung `whereIn('type', [MUA_HANG_NUOC_NGOAI, MUA_HANG_TRONG_NUOC, MUA_HANG_TRONG_NUOC_TU_DO])` trong subquery `whereHas('product_export_request.product_import_request')`

### ProductExportsController.php
- [x] Task 3: Refactor `getDataForBillIncomeReport($id)` — switch 3 case (1→`order_import_request->buy_contract2`/BuyContract2, 2→`product_arrived_notify->inland_contract`/InlandBuyContract, 15→`inland_product_arrived_new->inland_buy_contract_new`/InlandBuyContractNew). Trả `product_export_id, product_export_code, object_id, object_type, object_code, contract_created_by`. Type khác hoặc contract null → `success: false`. Thêm import `BuyContract2`.

### BillIncomeReportDetail.php (model)
- [x] Task 4: Thêm `product_export_id` vào `$fillable`. Thêm relationship `productExport()` → `belongsTo(ProductExport::class)`. Import `App\Model\Warehouse\ProductExport`.

### BillIncomeReport.php (model)
- [x] Task 5: `syncDetails()` — thêm `'product_export_id' => $detail['product_export_id'] ?? null` vào `BillIncomeReportDetail::create([...])`
- [x] Task 6: `saveAccountsDetail()` — bỏ block legacy derive contractable từ `objectable_type == ProductExport::class`. Thay bằng: nếu `$detail->product_export_id` → set `billable_id/billable_type = ProductExport`. `contractable_*` mặc định lấy từ `objectable_*`.
- [x] Task 7: `getDataForEdit()` — eager load `details.productExport` (chỉ lấy id, code). Set `$detail->product_export_code = $detail->productExport->code ?? null`.

### Request
- [x] Task 8: `BillIncomeReportStoreRequest` + `BillIncomeReportUpdateRequest` — thêm rule `'details.*.product_export_id' => 'nullable|integer|exists:product_exports,id'` + 2 message tiếng Việt

## Phase 2: Frontend

### BillIncomeReportDetail.blade.php (JS class)
- [x] Task 9: 
  - `addDetailProductExport()`: set thêm `product_export_id, product_export_code, object_id, object_code` từ response mới
  - `chooseProductExport()` unique check: đổi `detail.object_id == obj.id` → `detail.product_export_id == obj.id`
  - `submit_data`: thêm `product_export_id, product_export_code`
  - `clearData()`: mở rộng array
  - **Xoá** `chooseBuyContract` + `addBuyContractDetail` dead code

### form.blade.php
- [x] Task 10: Cột "Hợp đồng mua" của type_supplier → đổi search button thành label `<% detail.object_code %>` (tách thành 2 td riêng cho `type_customer` và `type_supplier` để dễ render)
- [x] Task 11: Thêm cột "Phiếu xuất hàng" (chỉ `type_supplier`) trước cột Hợp đồng mua: input disabled + button `chooseProductExport()`. Sửa Tổng cộng row thêm 1 td empty cho supplier.

### formShow.blade.php
- [x] Task 12: Tách object_code thành 2 td (type_customer giữ checkbox debt_begin; type_supplier hiển thị product_export_code rồi object_code). Thêm cột header "Phiếu xuất hàng". Sửa Tổng cộng. forAccounting/approved là list view → không cần sửa.

## Phase 3: Manual test

- [x] Task 13: Manual test 7 case:
  1. Tạo phiếu báo có NCC, chọn supplier → chọn phiếu xuất type 1 (NUOC_NGOAI) → kiểm `object_code` = mã `BuyContract2`, `product_export_code` = mã phiếu xuất
  2. Tương tự type 2 (TRONG_NUOC) → `InlandBuyContract`
  3. Tương tự type 15 (TRONG_NUOC_TU_DO) → `InlandBuyContractNew`
  4. Đổi supplier sau khi đã chọn phiếu xuất → cả `product_export_*` và `object_*` clear sạch
  5. Edit phiếu cũ (`product_export_id = NULL`): hiển thị nguyên hợp đồng mua, ô Phiếu xuất hàng trống, save lại bình thường
  6. Type customer + type other: 0 ảnh hưởng (cột mới chỉ xuất hiện cho type_supplier)
  7. Kiểm `account_details` sau khi save: `contractable_id/type` = HĐ mua, `billable_id/type` = phiếu xuất. Phiếu cũ giữ nguyên `billable_*` cũ.

## Checkpoint

### Checkpoint — 2026-04-28 (fix-1)
Fix bug user phát hiện sau lần test đầu: **form chi tiết của type_supplier lệch cột so với header**. Nguyên nhân:
1. Td "Phiếu YCXH" (line 284) thiếu `ng-if="form.type_customer"` → render cả supplier (thừa 1 cell)
2. Tổng cộng row dùng nhóm ng-if quá rộng (`cust||sup||other` cho 2 td liên tục) → đếm sai số cell cho từng type

Đã rewrite tổng cộng row dùng ng-if precise theo từng cột:
```
<td colspan="4">Tổng cộng</td>
<td ng-if="cust||sup||other"></td>     // Tên KH/NCC
<td ng-if="cust"></td>                  // Số HĐ
<td ng-if="cust"></td>                  // YCXH
<td ng-if="sup"></td>                   // Phiếu xuất
<td ng-if="sup"></td>                   // HĐ mua
<td ng-if="cust||sup"></td>             // NVKD
<td>money</td>
<td ng-if="foreign">money_ex</td>
<td>Diễn giải</td>
```
→ Counts khớp: customer 10, supplier 10, other 7 (excluding action). Tags balanced.

### Checkpoint — 2026-04-28
Vừa hoàn thành: 12/12 task code (8 BE + 4 FE). Tất cả file pass `php -l`. 

**Backend (8 file modified, 1 new):**
- Migration mới: `2026_04_28_000001_add_product_export_id_to_bill_income_report_details.php`
- `app/Model/Warehouse/ProductExport.php` — filter searchData
- `app/Http/Controllers/Warehouse/ProductExportsController.php` — refactor `getDataForBillIncomeReport` 3 case + import BuyContract2
- `app/Model/IncomeExpenditure/BillIncomeReportDetail.php` — fillable + productExport relationship + import
- `app/Model/IncomeExpenditure/BillIncomeReport.php` — syncDetails + saveAccountsDetail + getDataForEdit
- `app/Http/Requests/IncomeExpenditure/BillIncomeReports/BillIncomeReportStoreRequest.php` + `UpdateRequest.php` — validation

**Frontend (3 file modified):**
- `partials/classes/IncomeExpenditure/BillIncomeReportDetail.blade.php` — JS class extend addDetailProductExport, sửa unique check, submit_data, clearData. Xoá `chooseBuyContract` + `addBuyContractDetail` dead code.
- `income_expenditure/bill_income_reports/form.blade.php` — thêm cột "Phiếu xuất hàng", bỏ search HĐ mua, sửa Tổng cộng
- `income_expenditure/bill_income_reports/formShow.blade.php` — thêm cột "Phiếu xuất hàng" read-only, sửa Tổng cộng

Đang làm dở: chờ user chạy migration + manual test.
Bước tiếp theo: User `php artisan migrate` → test 7 case → báo lại.
Blocked: không.

### Checkpoint — 2026-04-29
Vừa hoàn thành: ✅ Migration chạy + 7 case manual test pass. Đóng feature.
Đang làm dở: không
Bước tiếp theo: không
Blocked: không
