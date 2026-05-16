# Design: Phiếu báo có loại NCC chọn phiếu xuất hàng (TanPhatDev)

## Bối cảnh

Phiếu báo có (`bill_income_reports`) loại NCC hiện cho user chọn **hợp đồng mua trực tiếp** ở chi tiết (commit `f7857238ce` ngày 25/4/2026 đã add). Yêu cầu mới: đổi sang chọn **Phiếu xuất hàng** (luồng cũ đã code sẵn từ commit `50f48e1272` 4/4/2023 nhưng không wire vào form sau Apr 25). Sau khi chọn phiếu xuất → hệ thống auto-fill hợp đồng mua tương ứng (read-only). Bỏ search hợp đồng mua trực tiếp.

## Quy tắc

### Schema
- Thêm cột mới `product_export_id` (BIGINT NULL) vào `bill_income_report_details` để lưu phiếu xuất user chọn.
- `objectable_id` / `objectable_type` **vẫn lưu hợp đồng mua** như cũ (cho cả phiếu cũ + phiếu mới).
- Phiếu cũ (`product_export_id = NULL`): chỉ hiển thị, không cần migrate dữ liệu.

### Mapping 3 loại import_request → hợp đồng mua

| Type | Path | Class |
|------|------|-------|
| 1 (`MUA_HANG_NUOC_NGOAI`) | `product_import_request.order_import_request.buy_contract2` (FK `order_import_request_id` → `buy_contract2_id`) | `BuyContract2::class` |
| 2 (`MUA_HANG_TRONG_NUOC`) | `product_import_request.product_arrived_notify.inland_contract` (FK `notify_id` → `inland_buy_contract_id`) | `InlandBuyContract::class` |
| 15 (`MUA_HANG_TRONG_NUOC_TU_DO`) | `product_import_request.inland_product_arrived_new.inland_buy_contract_new` (FK `inland_product_arrived_new_id` → `inland_buy_contract_new_id`) | `InlandBuyContractNew::class` |

### Validation & UX
- Filter modal "Phiếu xuất hàng": chỉ hiện phiếu xuất `type = XUAT_TRA_NCC`, `status = 1`, `product_import_request.supplier_id = supplier`, **`product_import_request.type IN (1, 2, 15)`**.
- Phiếu xuất không thuộc 3 type → backend `getDataForBillIncomeReport` trả `success: false`.
- `product_export_id` cho NCC: **nullable** (không bắt buộc — user vẫn nhập tay được khi không chọn phiếu xuất).
- Money: **không auto-fill**, user nhập tay (giữ giống logic cũ commit 4/4/2023).
- Đổi supplier → `clearData()` xoá luôn `product_export_id` + `product_export_code`.
- Unique check trong `chooseProductExport`: dùng `detail.product_export_id == obj.id` (không phải `object_id`).

## Thay đổi

### Migration
- `database/migrations/2026_04_28_xxxxxx_add_product_export_id_to_bill_income_report_details.php`
  ```sql
  ALTER TABLE bill_income_report_details
    ADD COLUMN product_export_id BIGINT UNSIGNED NULL AFTER objectable_type,
    ADD INDEX idx_product_export (product_export_id);
  ```

### Backend
- `app/Http/Controllers/Warehouse/ProductExportsController.php::getDataForBillIncomeReport($id)` (L1601):
  - Switch theo `product_import_request.type` (3 case 1/2/15) → derive `$contract` + `$contract_class` theo bảng mapping
  - Trả response: `product_export_id, product_export_code, object_id, object_type, object_code, contract_created_by`
  - Type khác / không có hợp đồng → `success: false, message: "Phiếu xuất không có hợp đồng mua tương ứng"`

- `app/Model/Warehouse/ProductExport.php::searchData()` (block `bill_income_report_supplier` L1071):
  - Bổ sung `whereIn('product_import_request.type', [1, 2, 15])` trong subquery `whereHas`

- `app/Http/Controllers/IncomeExpenditure/BillIncomeReportController.php::store/update`:
  - Validation: `details.*.product_export_id => nullable|integer|exists:product_exports,id`

- `app/Model/IncomeExpenditure/BillIncomeReport.php`:
  - `syncDetails()` (L293): thêm `product_export_id` vào `BillIncomeReportDetail::create(...)`
  - `getDataForEdit/Show` (L255+): eager load `productExport` relationship + set `detail->product_export_code` cho FE
  - `saveAccountsDetail()` (L329): khi `detail.product_export_id` có giá trị → set `billable_id = product_export_id, billable_type = ProductExport::class`. `contractable_*` lấy thẳng từ `objectable_*` (đã = hợp đồng mua từ store)

- `app/Model/IncomeExpenditure/BillIncomeReportDetail.php`:
  - Thêm `product_export_id` vào `$fillable`
  - Thêm relationship `productExport()` → `belongsTo(ProductExport::class)`

### Frontend — `resources/views/income_expenditure/bill_income_reports/form.blade.php`

Trong block `ng-if="form.type_supplier"`:
- **Bỏ** search button cột "Hợp đồng mua" (L246-265) → đổi thành label `<% detail.object_code %>`
- **Thêm cột mới "Phiếu xuất hàng"** (giữa NCC và Hợp đồng mua): input disabled hiển thị `detail.product_export_code` + search button → `detail.chooseProductExport()`

`formShow.blade.php`, `forAccounting.blade.php`, `approved.blade.php` — tương tự, read-only 2 cột.

### Frontend — `resources/views/partials/classes/IncomeExpenditure/BillIncomeReportDetail.blade.php`

- `addDetailProductExport()` (L230): set thêm `product_export_id, product_export_code, object_id, object_type, object_code` từ response mới
- `chooseProductExport()` (L294, dòng 324): unique check đổi `detail.object_id == obj.id` → `detail.product_export_id == obj.id`
- `submit_data` (L115): thêm `product_export_id, product_export_code`
- `clearData()` (L134): thêm `product_export_id, product_export_code` vào array clear
- **Xoá** `chooseBuyContract()` (L337-366) + `addBuyContractDetail()` (L368-396) — dead code sau khi bỏ search

## Không thay đổi

- Type customer (`form.type_customer`): giữ nguyên flow chọn hợp đồng + phiếu YCXH (`showModalChooseContract`, `showModalProductExportRequest`)
- Type other: giữ nguyên
- BillIncomeRequest (phiếu báo có yêu cầu): không động
- Pattern filter `searchData?type=bill_income_report_supplier`: chỉ thêm `whereIn type`, không thay đổi cấu trúc
- Phiếu cũ (`product_export_id = NULL`): không migrate dữ liệu, hiển thị nguyên trạng
- Bảng `bill_income_reports` cấp cha: không đổi schema
