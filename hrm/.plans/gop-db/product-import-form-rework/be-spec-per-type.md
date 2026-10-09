# BE spec per-type (nguồn: ERP Controller/Model/Blade — agent B + C)

Tài liệu tham chiếu cho Cụm 2/3. Chốt lại nghiệp vụ ERP `warehouse/product_imports` để port BE HRM.

## Cờ dẫn xuất (ERP `ProductImport.blade.php`)
- `is_foreign` = type ∈ {1, 11}
- `has_inland_cost` = type ≠ 3
- `showListedPrice` = type ∈ {4, 9, 13}
- `allocation_all` = type ∈ {11, 15, 2, 16}
- `has_delivery` = warehouse_import.transition_type == 2 (CONG_TY_VAN_CHUYEN)
- `has_rebate_price` = export_request.type == 17 OR borrow_sell WrServiceContract

## 3 biến thể bảng hàng hoá
- **A (foreign / type 11):** cột ngoại tệ + totals sum_price / VAT / sum_price_after_vat.
- **B (VAT / type 2,15,16):** SL / Đơn giá / Thành tiền VND / VAT% / VAT tiền.
- **C (default 3,4,9,14,99):** Giá nhập kho / Thành tiền nhập kho + nhóm showListedPrice (Giá niêm
  yết/Đơn giá bán/…) + nhóm is_settlement + cột Hạn gửi (type 14) + Tài khoản nợ (type 8||10).

## supplier_price theo type (nguồn giá)
- 2/11/15/16 ← `ProductImportRequestDetail.supplier_price` (`?: 0`)
- 3/4/6/7 ← `ProductImportRequestDetail.supplier_price` (trực tiếp) + copy price/rebate/extra/allocated từ payload
- 9/14/99 ← payload `$l['supplier_price']` (nhập tay)
- Update: chỉ overwrite nếu `!price_setted`.

## qty
`qty` = lot source qty, KHÔNG trừ returned_qty (returned_qty cộng vào source trong updateWarehouse SAU khi duyệt).

## currency / exchange_rate
Lấy từ ProductImportRequest CHỈ cho type ∈ {1,2,11,12,13}; còn lại VNĐ / 1.

## canEdit()
status == 3 AND created_by == auth. Nguồn bị KHOÁ khi edit (không chọn lại).

## validateAccountingWarehouse
Mỗi dòng: Σ(acc qty) == row qty, nếu lệch → "Phân bổ số lượng kho kế toán không khớp!".

## AccountingWarehouse::getByCompany()
KHÔNG check quyền. Lọc company_id (mặc định auth company) + status=1 + optional type whereIn.
consignmentIds() từ companies.consignment_warehouse_ids.

## Consignment (kho ký gửi)
CONSIGNMENT_TYPE_IDS import = [14]; consignmentAccOk(awId, type): type gửi (14) CHỈ hiện kho ký
gửi; type khác LOẠI kho ký gửi.

## Bản đồ hạch toán (code dùng 1541, KHÔNG phải 1562)
- type 4-WR: Nợ5112/Có1311 + 33311 + CK5211 + GG5213 + 1561÷632
- type 4-firm: 5212/1311 + 5213 + 1561÷632
- type 9-WR: thêm 157/632 → 1561/157
- type 9-firm: 5212 + 5211/5213 + 157 → 1561
- type 2/15/16: 1541/3311 + 1331 + NCC/nội địa costs → 1561/1541
- type 11: pick_up 1541/1331/3311 → 1561/1541 (BuyContract2)
- type 8/10: account_debt / account_has
- type 3/14/99 (else): CHỈ bốc xếp nếu rent_type==2, KHÔNG hạch toán hàng hoá.

## ImportCost types
QUOC_TE=1 (type 1&11), NOI_DIA=2, NCC=3, HOP_DONG_MUA=4, BOC_XEP=5.

## Nguồn ERP (đường dẫn tuyệt đối)
- Controller: `ERP/TanPhatDev/app/Http/Controllers/Warehouse/ProductImportsController.php` (store 265-994, update 994-1611)
- `ERP/TanPhatDev/app/Model/Warehouse/ImportModel.php` (hằng type 11-74)
- `ERP/TanPhatDev/app/Model/Warehouse/ProductImport.php` (canEdit 833, has_delivery 232, need_allocation 915, getDataCreateDept 2056-2381, updateWarehouse 1225+/returned_qty 1634-1786, syncCosts 922-1182)
- `ERP/TanPhatDev/app/Model/Warehouse/AccountingWarehouse.php` (getByCompany 276-286, consignmentIds 408-418)
- `.../views/partials/classes/warehouse/ProductImportLot.blade.php` (công thức giá từng dòng — SOURCE OF TRUTH)
- `.../views/partials/classes/warehouse/ProductImport.blade.php` (totals/allocation; flags 362/374/430/455)
- `.../app/Model/Warehouse/ImportCost.php` (hằng cost)
- `.../public/js/constant.js` (IMPORT_TYPES 231-244, ALL_IMPORT_TYPES 246-259)
- `.../views/warehouse/partials/consignment_warehouse_js.blade.php` (CONSIGNMENT_TYPE_IDS, consignmentAccOk)
- `.../views/warehouse/product_imports/form.blade.php` (2214 dòng UI)
- Firm: `.../app/Services/Sale/Firm/Contract/FirmContractProductImportService.php`, `FirmContractBorrowSellImportService.php`
