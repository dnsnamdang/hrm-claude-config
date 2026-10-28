# Phụ lục — kiểm kê chỗ dùng Nhóm hàng hoá (`groups` / `products.group_id`), 16/10/2026

Khảo sát chỉ đọc trên worktree `wt-chuyen-doi-hang-hoa` (hrm-api/hrm-client, nhánh `feat/chuyen-doi-hang-hoa`) và
`wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi`). Số dòng đo trên `hrm_erp_giacty`. Số dòng code có thể lệch khi nhánh đổi — tra lại trước khi sửa.

## 1. DB
**FK trỏ `groups` (13):** `attribute_groups` 2.434 · `contract_products` 32 · `contract_promotions` 0 · `firm_contract_promotions` 4.091 ·
`firm_quotation_promotions` 2.061 · `handover_acceptance_record_products` 0 · `product_group_classifies` 1.019 · `products` 45.890 ·
`project_contract_products` 0 · `quotation_products` 155 · `root_contract_products` 0 · `service_has_products` 4.896 · `tmp_products` 1.957
(+ `project_contract_customer_infos` theo agent ERP).

**Không FK nhưng là nhóm hàng:** `product_templates.group_id` 29.813 (100% id nhóm) · `assign_benefit_rate_has_groups` 0 ·
`benefit_rate_has_group_products` 0 · `device_error_has_group_product` 0 · `contract_rows.product_groups` (JSON, 8 dòng `[null]`) ·
`productables` morph `App\Model\Product\Group` **3.968** · `pi_*` 0.
**Không phải nhóm hàng (cùng tên cột):** `companies/departments/department_*.group_id` (Khối), `leave_types.group_id`, `supplier_has_groups` (→ customer_groups).

**Thuộc tính trên `groups`:** `vat_percent_tax_rate_id` 879 nhóm · `long_stock_days` 751 · `must_serial` 0 · `rate_liquidation` 0 (hàng có riêng 1.251) · `checksheet_id` 0.

## 2. ERP (`wt-erp-2d1`)
Màn Nhóm hàng đã khoá `productMovedToHrm:stopped-generic` (`routes/web.php:107-120`), chỉ còn `groups.searchData` (select2 màn Dịch vụ, Lỗi thiết bị).
Tạo/sửa hàng, mẫu hàng, hàng tạm cũng đã khoá (`web.php:512-695`).

| Khu | Vị trí | Dùng | Loại |
|---|---|---|---|
| Model | `app/Model/Product/Group.php:21-27,193-210` | đổi VAT nhóm ⇒ job ghi VAT mọi hàng của nhóm | ghi |
| | `Group.php:29-130` | đồng bộ CRM `product.category` | ghi |
| | `Group.php:132-160` | quan hệ attribute_groups, products, tmp_products, canDelete | quan hệ |
| | `BaseProduct.php:65`, `Product.php:862,900`, `ProductTemplate.php:875` | `group()`, `groupsUse()` (productables) | quan hệ |
| CRUD/import | `Sale/GroupsController.php:116-300`, `ExcelImports/GroupsImport.php:76-85`, `Services/ProductInfo/SyncCategoryInfoService.php:171-179` | CRUD, import, pi_groups→groups | ghi (đã khoá) |
| Thuế | `Jobs/UpdateProductOrGroupTaxValueJob.php:49`, `Common/TaxRatesController.php:202`, `Model/Product/TaxRate.php:36` | đổi thuế suất dội xuống nhóm; chặn xoá thuế suất | ghi/luật |
| CRM/Cost | `Product.php:239`, `Accounting/Cost.php:70,163`, `Services/CRM/CRMImportProductToCrm.php:49,138` | `categ_id` CRM theo nhóm; Cost tra nhóm THEO TÊN | luật |
| VAT dự phòng | `Common/SearchController.php:894,1701,2054` | `groups.vat_percent` khi hàng trống VAT | luật giá |
| Thanh lý | `Product.php:1412,1482`, `ProductTemplate.php:1197`, `ProductInfo.php:743`, `SearchController.php:900,1289,1707,2060` | `rate_liquidation` dự phòng | luật giá |
| | `Model/Sale/LiquidationQuotation.php:51`, `CostFixingQuotation.php:51` | form sửa GHI ĐÈ tỷ lệ dòng bằng tỷ lệ nhóm | luật giá |
| Serial | `BaseProduct.php:99-104` (dùng ở `Customercare/HandoverAcceptanceRecordsController.php:506,515`), `Requests/CustomerCare/HandoverAcceptanceRecordStoreRequest.php:62-90`, `…UpdateRequest.php:71-99` | `must_serial` — bắt serial, số serial = SL | luật |
| Tồn lâu | `Product.php:6822-6874`, `ProductTemplate.php:6359,6392`, `ProductInfo.php:3466,3499` | `DATEDIFF > g.long_stock_days`; hàng không nhóm rơi khỏi báo cáo | báo cáo |
| Checksheet | `Model/Tech/Checksheet.php:74-77,97-105`, `Tech/ChecksheetController.php:74,137,214` | checksheet gắn nhóm; 1 checksheet/nhóm | luật/ghi |
| In tem cũ | `ProductTemplatesController.php:514-620`, `Product2Controller.php:311-417`, `ProductInfoController.php:307-413` | barcode/ingredient/warning/user_manual | hiển thị (đường đang chạy đã dùng `Product::barcodeInfoOf` → product_types) |
| Hệ số công | `Model/Common/BenefitRateHasGroupProducts.php:19-27` (dùng ở `Model/Customers/WrAssignTask.php:936`), `Common/BenefitRateController.php:32-122`, `BenefitRates.php:28-33` | hệ số công lắp đặt theo nhóm | luật/ghi |
| Số thợ | `Customercare/AssemblyRequestController.php:465-486`, `WrAssignTask.php:1932-1939`, `Common/ConfigsController.php:22,75-115`, `Models/ContractRow.php:11` | `contract_rows.product_groups` (có khoá `product_natures` song song) | luật |
| Chụp chứng từ | `FirmQuotation.php:626,682`, `FirmContract.php:1491`, `Contract.php:2566,2620,2660`, `ContractAdditionAnnex.php:192,385,424` | chép `product.group_id` sang dòng KM/HĐ | ghi |
| Dịch vụ | `Sale/ServiceController.php:156-163`, `Requests/ServiceStoreRequest.php:35` | `service_has_products.group_id` (N100 đã nullable) | ghi/hiển thị |
| Lỗi thiết bị | `Model/Sale/DeviceErrorGroup.php:16-68`, `DeviceError.php:207,294`, `DeviceErrorGroupController.php:126-224` | phân loại lỗi theo nhóm | luật/lọc |
| Phụ kiện tương thích | `SearchController.php:730-735,944-956` | productables(Group) | luật |
| Báo cáo BH | `Services/Reports/WarrantyRepairService.php:33,69` | tên nhóm | hiển thị |
| Lọc kho | `Product.php:1996-2075,3093-4272` (~10 truy vấn `p.group_id`), catalog `Product.php:2054-2070`, `SearchController.php:621-654,1040-1067` | lọc | lọc |
| **INNER JOIN** | `Services/OrderReports/StockTransferReportService.php:301,355,2335,2389`, `Model/Warehouse/ProductExportDetail.php:266`, `MarketCommodity*ReportService` (~30 join `g.name = $type`) | hàng không nhóm biến mất | báo cáo |
| LEFT JOIN | `ProductExportRequest.php:3539-3567`, `CustomerCareReportService.php:290-337`, `SummarySaleReportService.php:589,966`, `SaleProductReportService.php:134-136,250,402`, `PurchaseInvoice.php:977`, `OrderSummary2.php:1229`, `ProductConfirmWarrantyService.php:151`, `ChangeImportPriceService.php:164`, `StockPosition.php:66-79` | hiển thị | hiển thị |
| Khác | `Api/HrmProductSearchController.php:330`, `Jobs/ProductSettingMailJob.php:183`, `Console/Commands/ExportLargeProductList.php`, `ExcelExports/RevenueByProduct.php` | feed/xuất | hiển thị |
| Blade | ~111 view (`warehouse_reports/*`, `orders/reports/stock_transfer`, `benefit_rates`, `device_error*`, `services`, `common/configs/edit`) | ô lọc/chọn nhóm | lọc |

`product_types` HRM có `serial_required`, `vat_percent_tax_rate_id`, `long_stock_days`, `ingredient`, `warning`, `user_manual`,
`barcode_template_type`; **không có `rate_liquidation`, `checksheet_id`**; thuộc tính theo loại ở `product_type_attributes`.

## 3. HRM (`wt-chuyen-doi-hang-hoa`)
Model nhóm hàng: `Modules/Assign/Entities/TpGroupProduct.php:11`, `Modules/Human/Entities/TpGroupProduct.php:11`
(`app/Models/Group.php`, `Modules/Human/Entities/Group.php` là `hrm_groups` — KHÁC). `products.group_id` fillable `Modules/MasterData/Entities/Product/Product.php:98`.

| Khu | Vị trí | Dùng | Loại |
|---|---|---|---|
| Hệ số (CSKH) | `Modules/CustomerCare/Entities/BenefitRate/BenefitRate.php:44`, `Services/BenefitRateService.php:335`, `Http/Requests/BenefitRate/BenefitRateRequest.php:57-82` (exists:groups + chặn 1 nhóm 2 hệ số), `Transformers/BenefitRateResource/BenefitRateResource.php:25`; FE `pages/admin/benefit-rates/index.vue:79,231,244`, `components/BenefitRateModal.vue:52` | `benefit_rate_has_group_products` | luật/ghi |
| Hệ số (Assign) | `Modules/Assign/Entities/AssignBenefitRateHasGroup.php:24`, `AssignBenefitRateConfig.php:27-36`, `Http/Controllers/Api/V1/AssignConfigBenefitRateController.php:53,91-179,198`, `Services/AssignConfigBenefitRateService.php:38`, route `Modules/Assign/Routes/api.php:1163`; FE `pages/assign/settings/benefit_rate/BenefitRateForm.vue:53-179`, `index.vue:212` | `assign_benefit_rate_has_groups` | luật/ghi |
| Gói dịch vụ | `Modules/CustomerCare/Entities/Service/Service.php:93`, `Services/ServiceService.php:1486-1498` (điền từ products.group_id), `Http/Requests/Service/ServiceRequest.php:59-70,142` (exists:groups), `ServiceService.php:612-739` (nhóm dòng ĐÃ theo product_type_id), `ServiceService.php:1045,1055` (option catalog theo groups + product_group_classifies), `ServiceImportService.php:683` | `service_has_products.group_id` | ghi/lọc |
| Lỗi thiết bị | `Modules/CustomerCare/Services/DeviceErrorService.php:197,999`, `Exports/DeviceErrorExport.php:175,547-551`; FE `pages/customer-care/device-errors/index.vue:419,471,634` | lọc + cột | lọc/hiển thị |
| Thiết bị KH | `Modules/Assign/Services/CustomerManagerService.php:385-453,489,529,641-750`, route `api.php:181`; FE `components/assign-components/customer/manager/EquipmentTab.vue:12,19,645` | gom/lọc theo nhóm | lọc |
| Catalog BOM | `Modules/Assign/Services/ErpProductSourceInfoService.php:13,65-78`, `Http/Controllers/Api/V1/BomListController.php:397,442-443`; ghi chú `Modules/MasterData/Entities/BusinessCatalog/Chapter.php:16` | product_group_classifies → Lĩnh vực/Chương | hiển thị |
| **Nhóm máy** | `Modules/MasterData/Entities/Product/Productable.php:37` (TYPE_GROUP), `Product.php:340`, `Http/Requests/Product/ProductRequest.php:148-149`, `Services/Product/ProductWriteService.php:444`, `Transformers/Product/ProductFormResource.php:98,140`, `ProductDetailResource.php:200`, `Services/Product/ProductOptionService.php:93,491`, picker `Services/Product/ProductPickerService.php:401-412`; FE `components/product/form/ProductFormMachines.vue:8-87`, `productFormModel.js:18,86`, `components/product/detail/ProductTabMachines.vue:9,51` | productables morph Group | ghi/luật |
| Công khoán | `Modules/MasterData/Support/RegulationTabRegistry.php:190`, `Services/RegulationConfigService.php:544,2099` | `contract_rows.product_groups` | luật |
| Tra tồn | `Modules/Finance/Services/SellableStockReportService.php:452-453`; FE `pages/lookup/stock-companies/index.vue:483,534` | lọc | lọc |
| Dự án SP | `Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php:430` (route `api.php:487`), `Services/ProductProjectService.php:60-61` | dropdown/lọc | lọc |
| Tìm hàng ERP | `Modules/Assign/Services/ErpProductSearchService.php:34` | group_id, group_id_use | hiển thị |
| Thuế | `Modules/MasterData/Services/ProductCatalog/TaxRateService.php:87-104` (+ test `TaxRatePropagationTest.php:47-68`) | dội VAT xuống groups | ghi |
| Sync | `app/Console/Commands/CompanySyncErp.php:171` | `DB::table('groups')` — kiểm lại có phải nhóm hàng | ? |
| Test fixture | `ServiceAppliedProductTypeTest.php:94`, `ProductPickerSearchTest.php:161`, `ProductWriteApiTest.php:293`, `ProductWriteHardeningTest.php:172` | groups | test |
