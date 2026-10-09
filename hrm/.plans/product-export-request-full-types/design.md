# Design — Màn Tạo YCXH: đủ 14 loại như ERP + 2 loại mới 20/21 (HRM)

Redmine #11383 — "Lấy đúng giá trị Loại yêu cầu y hệt với erp" + thêm 2 loại xuất mới 20, 21 theo HRM.

## 1. Mục tiêu (đã chốt với user)

- Dropdown "Loại yêu cầu" ở màn `finance/product-export-requests/create` **giống hệt ERP** về giá trị + nhãn.
- **Port trọn luồng TẠO cho 6 loại còn thiếu** (14, 15, 4, 16, 17, 19), không chỉ hiện tên trong dropdown.
- Giữ 2 loại HRM riêng: 20 (Xuất sản xuất hợp đồng), 21 (Xuất bán hợp đồng).

Scope này user đã xác nhận 2 lần (AskUserQuestion): "Thêm đủ + port luồng tạo" → "Port trọn 6 loại ngay".

## 2. Danh sách loại + nhãn chuẩn (nguồn: ERP `public/js/constant.js` EXPORT_TYPES + `ExportModel::TYPES`)

Thứ tự dropdown đích (đã chốt trong preview): `14, 15, 3, 4, 6, 7, 12, 16, 17, 18, 19, 99` **+ 20, 21**

| id | Nhãn chuẩn ERP | HRM hiện có? | Cơ chế tạo |
|----|----------------|--------------|------------|
| 14 | Xuất bán hàng | filter only | Nguồn: HĐ hãng (firm_contract), chọn tab + VAT, auto-load dòng |
| 15 | Xuất khuyến mại | filter only | Nguồn: HĐ hãng (combo KM), kho KM, giá = 0 |
| 3  | Xuất mượn | ✅ creatable | Nhập tay + ngày mượn |
| 4  | Xuất trả nhà cung cấp | filter only | Nguồn: Phiếu đề nghị nhập kho (product_import_request) |
| 6  | Xuất điều chuyển kho nội bộ | ✅ creatable | Nhập tay + kho nhập |
| 7  | Xuất điều chuyển kho chi nhánh | ✅ creatable | Phiếu chuyển kho chi nhánh |
| 12 | Xuất hàng gửi | ✅ creatable | Nhập tay + khách hàng |
| 16 | Xuất bán bảo hành | filter only | Nguồn: HĐ SC-BH (wr_service_contract, items.type=0) |
| 17 | Xuất bán SC - BD | filter only | Nguồn: HĐ SC-BH (wr_service_contract, items.type=1) |
| 18 | Xuất sản xuất | ✅ creatable | Nhập tay + kho |
| 19 | Xuất thực hiện hợp đồng | ❌ | Nhập tay + đính HĐ (attach only, KHÔNG auto-load dòng) |
| 99 | Xuất khác | ✅ creatable | Nhập tay |
| 20 | Xuất sản xuất hợp đồng | ✅ creatable (HRM) | HĐ HRM (hrm_contract) — đã có |
| 21 | Xuất bán hợp đồng | ✅ creatable (HRM) | HĐ HRM (hrm_contract) — đã có |

**Nhãn cần sửa trong `TYPE_NAMES`** (Assign Entity): 14 "Xuất bán hãng"→"Xuất bán hàng"; 15 "Xuất khuyến mại hãng"→"Xuất khuyến mại"; 4 "Xuất trả NCC"→"Xuất trả nhà cung cấp"; 17 "Xuất bán SC-BD"→"Xuất bán SC - BD". (đối chiếu lại từng nhãn với constant.js khi code)

## 3. Độ sẵn sàng DB — ĐÃ VERIFY (erp_hrm_check, gop_db)

**KHÔNG cần migration.** Đã kiểm tra trực tiếp DB:

- `product_export_requests` (cha) đã có đủ: `firm_contract_id, firm_tab_vat_percent, wr_service_contract_id, product_import_request_id, need_repair, promo_warehouse_id, emplement_contract_id/type`.
- `product_export_request_tab_products` (dòng cấu trúc cha-con) có: `firm_contract_tab_id, firm_contract_tab_product_id, firm_contract_tab_combo_product_id, vat_percent, need_export, qty, contract_qty, exported_qty, returned_qty, emplement_contract_id/type, contract_product_id`.
- `product_export_request_details` (dòng phẳng, có giá) có: `rebate_price, allocated_price, price, extra_price, vat_percent, wr_service_contract_item_id, firm_contract_tab_product_id, inland_cost, total_amount`. (Thiếu `product_import_request_detail_id`, `supplier_price` — không cần: type 4 dùng `product_import_request_id` ở cha + `allocated_price`/`inland_cost` ở dòng.)
- Bảng nguồn ERP đều có sẵn: `firm_contracts, firm_contract_tabs, firm_contract_tab_products, firm_contract_combo_group_option_products, wr_service_contracts, wr_service_contract_items, product_import_requests`.

## 4. Mẫu ghi dòng hàng (đã có, mirror ERP) — dùng lại cho mọi loại nguồn

Luồng 20/21 hiện tại (`ProductExportRequestService::writeContractLines`) **ghi kép**:
1. `product_export_request_tab_products` — cấu trúc, khoá nguồn (contract_product_id / firm_contract_tab_*), qty/contract_qty/vat.
2. `product_export_request_details` — dòng phẳng có giá (price/extra_price/allocated_price/total_amount/vat) mà downstream (đề nghị + phiếu xuất kho) đọc trực tiếp.

→ Mọi loại nguồn mới (14/15/16/17/4) theo đúng khuôn ghi kép này. `rebate_price` ghi vào details khi có (17, 15=0).

## 5. Chi tiết từng loại

### 5.1 Type 19 — Xuất thực hiện hợp đồng (NHẸ NHẤT, làm trước)
- FE: biến thể **nhập tay** (như 18/99) + đính HĐ qua `ContractSearchModal` (đang trỏ `assign/contracts` = HĐ HRM). Đính `emplement_contract_id` (read-only KH), **KHÔNG auto-load dòng hàng** (user tự chọn SP).
- BE: `rulesForType(19)` = nhập tay + `emplement_contract_id` nullable/exists; service nhánh manual + set emplement_contract.
- ⚠️ Verify khi code: ERP type 19 attach loại HĐ nào (emplement) và có auto-load không — đối chiếu `form.blade.php` has_parent + `create.blade.php` getParentInfo.

### 5.2 Type 4 — Xuất trả nhà cung cấp
- Nguồn: `product_import_requests`. HRM có model `Modules/Finance/Entities/ProductImportRequest` + list endpoint `GET finance/product-import-requests` (tái dùng làm modal chọn).
- BE cần dựng:
  - `canSupplierReturn($id)` (port ERP: is_complete + đúng người tạo + loại mua + status=5 + không có YCXH type-4 pending).
  - `getDataForSupplierReturn($id)` (port ERP `ProductImportRequest::getDataForReturn`): trả dòng `imported_qty > returned_qty`, qty mặc định = imported_qty−returned_qty, allocated_price = supplier_price, inland_cost, vat_percent, supplier (customers.is_supplier=1, derive lúc hiển thị).
  - `rulesForType(4)`: `product_import_request_id required|exists`; re-check canSupplierReturn khi store; ghi `product_import_request_id` ở cha (supplier KHÔNG lưu, derive).
- FE: modal chọn phiếu ĐNNK + cột SL trả / allocated_price / inland_cost / vat.

### 5.3 Types 16/17 — Xuất bán bảo hành / SC-BD (nguồn HĐ SC-BH)
- Nguồn: `wr_service_contract_items` (cột `type`: 0=bảo hành→loại 16, 1=SC-BD→loại 17).
- HRM có: model đầy đủ `Modules/CustomerCare/.../WrServiceContract`, list endpoint `GET .../wr-service-contracts`, và `BorrowSellRequestSourceService::loadWrService()` (đã port nhánh **type=1** + tính `rebate_price = price_after_extra*sale_percent/100`) → tái dùng cho 17, thêm nhánh **type=0** cho 16 (không rebate/vat, contract_qty=qty).
- Khác biệt 16 vs 17: **17 CÓ delivery** (transition_type required) + rebate/vat/annex/root_qty; **16 KHÔNG delivery**, không rebate/vat.
- BE cần: port `canProductExport()` (HĐ SC-BH đủ điều kiện xuất); search + load endpoint trong Assign; store require `wr_service_contract_id` cho **17** (không cho 16), ghi field cho cả 2, snapshot KH từ HĐ.
- ⚠️ **Thêm 17 vào `HAS_DELIVERY_TYPE_IDS`** (16 để ngoài) — khớp ERP.

### 5.4 Types 14/15 — Xuất bán hàng / Khuyến mại (nguồn HĐ hãng)
- Nguồn: 14 = `firm_contract_tab_products` (theo tab + VAT); 15 = `firm_contract_combo_group_option_products` (combo KM, giá=0).
- HRM có: `BorrowSellRequestSourceService::loadFirm()` (port nhánh type=0 → tái dùng cho 14, gồm `firmExportingQty` in-flight + logic cha-con), logic kho KM `promo_warehouse_ids` (StockService/AccountingStockService). **Chưa có** nhánh combo KM cho 15.
- BE cần:
  - Search endpoint HĐ hãng trong Assign (bê `PrepickExportContractService::searchContracts`).
  - Load endpoint kiểu `getDataForWarehouseExport`: bước 1 trả `vat_percent_options` + tabs; bước 2 (có tab_ids + vat) trả dòng. 14 = loadFirm; 15 = viết nhánh combo KM.
  - `rulesForType(14)`: `firm_contract_id, firm_tab_vat_percent, tabs.*.firm_contract_tab_id, tabs.*.products.*, need_repair` (chỉ 14). `rulesForType(15)`: `firm_contract_id, promo_warehouse_id`.
  - Store: ghi `firm_contract_id/firm_tab_vat_percent/need_repair/promo_warehouse_id`, snapshot KH, guard `canProductExport`(14)/`canProductExportPromotion`(15), ghi dòng vào tab_products (firm_contract_tab_id) + details (giá; 15 giá 0).
  - Endpoint `getPromoWarehouse` (kho KM) cho FE loại 15.
- FE: modal chọn HĐ hãng → bước chọn tab/VAT → bảng có giá (14 có, 15=0) + ô "Cần lắp đặt" (14) + select kho KM (15).

## 6. Điểm chặn / khác biệt cần chú ý
1. **`canProductExport` (SC-BH) + `canProductExportPromotion` (HĐ hãng) + `canSupplierReturn` (ĐNNK) chưa port** → phải viết. Đây là guard nghiệp vụ, không được bỏ (nếu bỏ, user tạo phiếu cho HĐ chưa đủ điều kiện).
2. **HAS_DELIVERY**: ERP → 17 có delivery, 16 không. HRM hiện thiếu 17. Phải thêm 17.
3. **need_repair required** chỉ cho 14 (đã có cột + xử lý ở luồng khác, nhưng chưa ràng buộc theo loại 14).
4. **Type 19 auto-load hay không** — verify ERP trước khi code (mục 5.1).
5. **In-flight qty** (join_exporting_qty / firmExportingQty): loadFirm đã port; loadWrService cần kiểm nhánh type=0; type 4 dùng returned_qty. Không được bỏ để tránh xuất quá SL.
