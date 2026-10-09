# Plan — Nhập hàng bán trả lại cho HĐ loại 21

> Nhánh `gop_db` · @namdangit · Spec: `docs/superpowers/specs/gop-db/2026-08-25-nhap-ban-tra-lai-hd21-design.md`
> Design: `.plans/gop-db/nhap-ban-tra-lai-hd21/design.md`

## Phase 1 — Nửa trước (lập + validate + duyệt giá phiếu nhập trả lại nguồn loại 21)

### P1.0 — Xác minh trước khi code (đọc lại code thật) ✅ 2026-08-25
- [x] Đọc `ProductImportRequestService::fillFromExportRequest / guardBusinessRules / guardControlBoardStatus / handleAfterSubmit` — nắm chính xác nhánh type 4 hiện tại
- [x] Đọc `ProductExportRequest::searchForImportType` + `dataForSaleReturn` + `SALE_RETURN_EXPORT_TYPES`
- [x] Chốt map status: ERP type14 `[5,13]` = Đã hạch toán / Đã quyết toán. HRM loại 21 KHÔNG có 13 → filter chỉ `status=5`; "đã QT" đọc từ `Contract.status`
- [x] `price_buy_approve` + `amount_price_buy_approve` ĐÃ có trên `product_import_request_details` + xử lý ở `updateSaleReturnPrices` → KHÔNG cần migration cột giá
- [x] `Contract::support_accounting()` = morphOne `SupportAccounting` (bảng **`firm_support_accounting`** số ít); `settlement_contracts` là **polymorphic** (`contractable_id`+`contractable_type`), KHÔNG phải khóa `contract_id`; Contract status DA_QUYET_TOAN=11/DANG_QUYET_TOAN=12; FQN = `Modules\Assign\Entities\Contract\Contract`
- [x] `product_import_requests` CHƯA có `emplement_contract_id/type` (migration cũ chỉ thêm cho `product_imports`); `SOURCE_TABLE_BY_TYPE[BAN_TRA_LAI]=product_export_requests` nên `source_id` map đúng
- [x] Verify DB: flat `product_export_request_details` loại 21 có đủ `qty`/tên/giá/vat NHƯNG `exported_qty=returned_qty=0` (cả tab_products cũng 0) → nhánh 21 đọc flat theo `qty`

### P1.1 — DB ✅
- [x] Migration `add_emplement_contract_to_product_import_requests_table` thêm `emplement_contract_id`(idx) + `emplement_contract_type` + `emplement_contract_code` — đã migrate OK
- [x] ~~price_buy_approve~~ ĐÃ có (P1.0), không cần

### P1.2 — BE: chọn nguồn loại 21 ✅
- [x] Thêm `const XUAT_BAN_HOP_DONG=21` + `STATUS_DA_HACH_TOAN=5` + `HRM_CONTRACT_SETTLED_STATUSES=[11,12]` + `HRM_CONTRACT_CLASS` vào Finance `ProductExportRequest`
- [x] `searchForImportType()` nhánh `BAN_TRA_LAI`: OR thêm `(type=21 AND status=5)`; verify SQL đúng
- [x] KHÔNG thêm filter "phiếu trả treo" ở search (giữ "giống type 14")

### P1.3 — BE: dữ liệu dòng trả ✅
- [x] `dataForSaleReturn()` early-return nhánh 21 → `dataForSaleReturnHrmContract()`: đọc flat details theo `qty` (exported/returned=0); HĐ từ `emplement_contract_id`→`hrm_contracts`, `is_settlement=Contract.status∈[11,12]`; trả `emplement_contract_id/type/code`, null firm/wr. Verify DB phiếu 35676 OK

### P1.4 — BE: validate (mirror type 14) ✅
- [x] `guardBusinessRules()` BAN_TRA_LAI: type=21 → `guardSaleReturnHrmContract()`: HTHT qua tồn tại `firm_support_accounting` (polymorphic FQN Contract); "đã lập quyết toán" qua `settlement_contracts` (polymorphic FQN Contract)
- [x] Chặn SL trả > `qty` khả dụng (dataForSaleReturn keyed by detail_id) — rethrow ValidationException
- [x] `guardControlBoardStatus()`: nhánh 21 tự chạy đúng qua `dataForSaleReturn` is_settlement (không sửa)
- [x] Verify: FE gửi cả source_id + product_export_request_id (form 1651-1652) → guard đọc đúng; HĐ13 sa=true settle=false

### P1.5 — BE: lưu phiếu ✅
- [x] `fillFromExportRequest()` BAN_TRA_LAI: type=21 → set `emplement_contract_id/type/code` (code lấy từ hrm_contracts), giữ `customer_id`, null firm/wr; nhánh ERP cũ giữ nguyên
- [x] `SOURCE_TABLE_BY_TYPE[BAN_TRA_LAI]=product_export_requests` đã đúng cho nguồn 21 (P1.0)

### P1.6 — BE: duyệt giá ✅
- [x] `handleAfterSubmit` type 4: status 10 → BKS notify; còn lại → `CHO_TP_DUYET(12)` notify TP. `price_buy_approve`/`amount` xử lý ở `updateSaleReturnPrices` (đã có). Không cần sửa cho nhánh 21

### P1.7 — FE ✅
- [x] Loại-21 sales TỰ hiện trong `ExportRequestSearchModal` nhờ BE search (không cần sửa FE để chọn được)
- [x] BE `exportRequests` trả thêm `contract_code` (batch hrm_contracts/firm_contracts); modal thêm cột "Số hợp đồng" (chỉ hiện khi có HĐ), colspan động
- [x] Form nhập trả + qty giới hạn dùng lại UI sẵn có (nguồn 21 trả cùng shape products)
- [x] **(2026-08-25) Đổi kiểu ô "Phiếu yêu cầu xuất hàng"**: bỏ input readonly + nút "Chọn" xanh → ô dạng select (`.source-select`) click cả ô mở popup, có × xoá chọn (chỉ khi Tạo + đã chọn), icon 🔍, khoá xám khi Sửa/chưa chọn loại. Thêm method `clearExportRequest()` + guard `isEdit` trong `openExportRequestModal()`; không đụng logic popup/chọn nguồn

### P1.T — Test (verify bằng DB smoke test dữ liệu thật)
- [x] `searchForImportType(BAN_TRA_LAI)` SQL đúng: `((type∈[…] & status∈[5,13]) OR (type=21 & status=5))`
- [x] `dataForSaleReturn(35676)` nhánh 21: 4 dòng theo `qty`, HĐ 13, is_settlement=false, firm/wr null, emplement_contract_id/type/code đúng
- [x] Guard queries HĐ13: `firm_support_accounting` exists=true (qua), `settlement_contracts` exists=false (qua)
- [x] `contract_code` map: PYCXH-35676→HĐ13, PYCXH-3567x→HĐ15 đúng
- [x] Hồi quy: nhánh HĐ ERP đều type-gated `type==21`, code cũ giữ nguyên (early-return/sub-branch)
- [x] **Setup dữ liệu test E2E (2026-08-25)**: bump `PYCXH-35676` (HĐ13, creator emp 13 = namdangit) từ `status=8`→`5` trên `erp_hrm_check` (dev). Verify qua code thật: search trả #35676; `dataForSaleReturn(35676)` → is_settlement=false, HD_CODE=`HĐ_TPE_CTV_NV_26_0001_abc`, firm_id=NULL, 4 dòng (detail 226755-226758, qty=1, giá 610k/260k/240k/150k). `firm_support_accounting` id=21653 (type HRM Contract) tồn tại → guard PASS; `settlement_contracts` HĐ13 chỉ có type FirmContract (ERP) → không chặn.
  - **HOÀN NGUYÊN sau test**: `UPDATE product_export_requests SET status = 8 WHERE id = 35676;`
  - E2E còn lại: user đăng nhập emp13 → lập phiếu nhập "Bán trả lại" → chọn PYCXH-35676 → duyệt giá; test chặn SL vượt + chặn quyết toán (tạm `UPDATE hrm_contracts SET status=11 WHERE id=13` rồi hoàn nguyên về 1)
- [ ] Khung PHPUnit hiện có là unit-thuần (không DB); logic này DB-driven → cân nhắc thêm feature-test khi có seeder dữ liệu loại-21 status 5

### P1.8 — FE: parity cột bảng chi tiết loại 4 (bán trả lại) — 2026-08-25
> User: "form loại bán trả lại, box chi tiết hàng hoá thiếu cột so với ERP". Chốt scope: (1) tách cột gộp "SL có thể nhập" trở lại 3 cột ERP *SL xuất / Đã trả / SL trả*; (2) bộ cột giá đầy đủ CHỈ áp cho loại 4, loại 3/14/99 giữ bảng tối giản như cũ.
- [x] Tách bảng: thêm `<table v-if="isSaleReturn">` riêng cho loại 4, bảng cũ thành `v-else` (loại 3/14/99 KHÔNG đổi)
- [x] Bảng loại 4 mirror ERP `form.blade.php:612-732`: STT · Tên · Model · Mã · Thương hiệu · ĐVT · **SL xuất** (exported_qty) · **Đã trả** (returned_qty) · **SL trả** (qty input) · Giá niêm yết (price) · Đơn giá bán (price_after_extra) · Thành tiền (total_amount_after_extra) · [Chiết khấu nếu hasRebatePrice] · Giảm giá (discount_price) · Đơn giá sau giảm (allocated_price) · Thành tiền sau giảm (total_amount_allocated) · VAT · Tiền VAT (vat_cost_allocated) · Thành tiền sau VAT (total_amount_allocated_after_vat) · [settlement] Đơn giá mua đề xuất (price_buy input, cap = price_after_extra) · Thành tiền mua đề xuất (amount_price_buy)
- [x] Computed mới: `isSaleReturn`, `hasRebatePrice` (từ sourceInfo, mặc định false — nguồn 21 luôn false), `isSourceSettlement` (sourceInfo.is_settlement), `saleReturnColCount`, `saleReturnTotals`
- [x] Method derived per-row (mirror getter ERP `ProductImportRequestDetail`): priceAfterExtra / totalAmountAfterExtra / discountPrice / totalAmountAllocated / vatCostAllocated / totalAmountAllocatedAfterVat / amountPriceBuy + clamp price_buy (`onPriceBuyInput`)
- [x] Dòng tổng: Tổng tiền bán · Tổng giảm giá · Tổng tiền trước thuế · Tiền VAT · Tổng tiền sau thuế (+ Σ amount_price_buy khi settlement); dòng qty=0 làm mờ (`row-disabled`)
- [x] Map thêm `exported_qty`/`returned_qty`/`price_buy` vào `onChooseExportRequest` (tạo) + đủ `price/allocated/extra/rebate/exported/returned/price_buy` vào `loadDetail` (sửa)
- [x] `buildProductsPayload` +`price_buy`/`amount_price_buy`; `unsavedSnapshotSource` +`price_buy` (sửa giá mua đề xuất = bẩn form)
- [x] BE `ProductImportRequestDetailResource` +`extra_price`/`rebate_price` (cần cho cột Đơn giá bán/Giảm giá khi mở Sửa)
- [x] BE `ProductImportRequestService::syncDetails` +`price_buy`/`amount_price_buy` (lưu giá mua đề xuất lúc tạo, mirror ERP submit_data). Verify: `store/update` đọc `$request->input('products')` (KHÔNG `validated()`) → 2 field mới truyền thẳng, không bị strip

### P1.9 — FE: màn Chi tiết bỏ header, đưa status lên topbar — 2026-08-25
> User: "màn chi tiết yêu cầu nhập hàng bỏ cái header đi và cho cái status lên phía trên topbar" — "tương tự chi tiết yêu cầu xuất hàng". Mirror `product-export-requests/_id/index.vue` (buildStatusTitle trong pageTitle, không còn card header).
- [x] Xoá khối `<div class="form-header">` (icon + tiêu đề + status-pill) đầu template
- [x] `pageTitle` computed dùng `buildStatusTitle(...)` để nhét badge trạng thái vào topbar (v-html qua PageTitleMixin). Import STATUSES chỉ có `type` (không hex) → map `status_type`→hex trên FE (success=xanh, danger=đỏ, khác=xám)
- [x] Dọn CSS/method không còn dùng: `statusPillClass`, `.form-header`/`.header-*`/`.status-pill` (nếu không nơi nào khác dùng)

## Phase 2 — Màn Phiếu nhập hàng (ProductImport) HRM — type 4 loại 21
> Design/Spec: `docs/superpowers/specs/gop-db/2026-08-27-product-import-hrm-design.md`
> Khung generic mở rộng mọi loại nhập; đợt này chỉ xử lý type 4 (BAN_TRA_LAI) cho HĐ HRM loại 21. Hai đường vào (A qua kho ERP redirect / B nhập thẳng từ yêu cầu nhập hàng HRM).

**Mục tiêu:** dựng màn Phiếu nhập hàng (`ProductImport`) HRM (chưa từng có bên HRM) — nhập kho thực + cộng dồn returned_qty + hạch toán nhập trả cho HĐ HRM loại 21, khung dispatch-theo-type mở rộng được.

**Ràng buộc chung (Global Constraints — áp cho MỌI task Phase 2):**
- Nhánh `gop_db`. KHÔNG dùng `mysql2`/`DB_CONNECTION_SECOND`. Bảng trùng tên ưu tiên bản ERP; HĐ HRM = `hrm_contracts`.
- KHÔNG tạo bảng mới. Model HRM trỏ bảng ERP sẵn có (`product_imports`, `product_import_details`, `product_import_tabs`, `product_import_tab_products`, `product_import_detail_accountings`, `import_costs`). Header `product_imports` đã có `emplement_contract_id/type/code` + `source_export_id`.
- Cột polymorphic (invoiceable/contractable/billable/objectable, accounting stock log) lưu **FQN của ERP** để ERP đọc lại được — dùng hằng số có sẵn: `AccountDetail::CONTRACTABLE_HRM_CONTRACT` = `Modules\Assign\Entities\Contract\Contract`, `AccountDetail::TYPE_DEPT=1`(Nợ)/`TYPE_HAS=2`(Có); `AccountingStockLog::OBJ_TYPE_*`, `BEGINNING_FQN`.
- Validate: BE rethrow `ValidationException`; FE hiện lỗi inline. Không commit/push git khi chưa được yêu cầu.
- Test = DB smoke test qua tinker trên `erp_hrm_check` (PHPUnit hiện không chạy DB) — `grep DB_ .env` trước mỗi lần tinker.

**Tham chiếu bắt buộc (mirror, KHÔNG bịa API):**
- ERP nguồn port: `ProductImportsController::store` (:266-980), `ProductImport::updateWarehouse` (:1225-1297) / `updateUnitCostPriceOfProducts` (:1199) / returned_qty (:1658-1722) / `generateCode` (:860), `FirmContractProductImportService` (full) + base `FirmContractImportService`.
- HRM mẫu sẵn: `Modules/Assign/Services/ContractParentImportService.php` (đã port `ProductImport::updateWarehouse` nhánh tăng tồn — `AccountingStock`/`AccountingStockLog` ở `Modules/Assign/Entities/Warehouse/`); `Modules/Assign/Services/ProductExportPostingService.php` + `WarehouseExportAccountingService.php` (ảnh gương hạch toán loại 21, cùng bộ TK + cách gọi `AccountDetail::createDataSaveDept`/`saveAccountDetail($accounts,$invId,$invType,$invCode,$meta)`); `Modules/Finance/Services/ProductImportRequestService.php` (mẫu store/update/dispatch nhánh type + FormRequest + Resource + route).
- HĐ HRM: `Modules/Assign/Entities/Contract/Contract.php` (status DA_QUYET_TOAN=11/DANG_QUYET_TOAN=12; `support_accounting` morphOne bảng `firm_support_accounting`; `settlement_contracts` polymorphic). billable = ProductExport (verify FQN P2.0: `Modules/Finance/Entities/Contract/ProductExport.php` vs `Modules/Assign/Entities/Warehouse/ProductExport.php`).
- Hằng số loại nhập + status + TYPE_NAMES: đã khai đủ ở `Modules/Finance/Entities/ProductImportRequest/ProductImportRequest.php` (:57-162) — copy y hệt sang `ProductImport` (BAN_TRA_LAI=4, NHAP_BAN_MUON_TRA_LAI=9, MUON_TRA_LAI=3, …).

---

### P2.0 — Xác minh trước khi code (đọc code thật, không code) ✅ 2026-08-27
- [x] SHOW COLUMNS 6 bảng ProductImport — cột đủ (chi tiết ledger scratchpad). `product_import_details` có supplier_price/price/rebate/extra/allocated/price_buy/amount_price_buy/import_qty/detail_type. `product_import_detail_accountings` có accounting_warehouse_id/qty/import_qty/import_price/account_debt.
- [x] Chốt tally returned_qty loại 21: `hrm_contract_product_prices` KHÔNG có cột tally → tally ở `product_export_request_tab_products` (có emplement_contract_id + exported/returned/warehouse_exported_qty + contract_product_id); `product_export_request_details.returned_qty` có sẵn. **Ruling P2.3b** (ledger): update details + tab_products, BỎ hrm_contract_product_prices. Spec mục 6 đã sửa.
- [x] `product_import_tabs`/`tab_products` chỉ có firm_contract_id (không emplement) — ruling: loại 21 bỏ tab nếu parent không có (details đủ), hoặc lưu emplement vào firm_contract_id.
- [x] billable ProductExport: FQN `App\Model\Warehouse\ProductExport` (Finance & Assign đều bảng product_exports).
- [ ] (giao implementer P2.3/P2.4) đọc `ContractParentImportService`/`WarehouseExportAccountingService`/`ProductExportPostingService` để port API stock + accounting

### P2.1 — Entities (model HRM trỏ bảng ERP, KHÔNG bảng mới)
**Files:** Create `Modules/Finance/Entities/ProductImport/{ProductImport,ProductImportDetail,ProductImportTab,ProductImportTabProduct,ProductImportDetailAccounting}.php`
**Produces:** `ProductImport` (const loại nhập/status/TYPE_NAMES; relations `products`/`tabs`/`accounting`/`costs`/`emplement_contract`; `generateCode()`; `canView/canEdit`); các model chi tiết + quan hệ.
- [ ] `ProductImport extends BaseModel`, `$table='product_imports'`; copy const loại nhập (3/4/9…) + status (DANG_TAO=3, DA_HOAN_THANH=1) + TYPE_NAMES từ `ProductImportRequest`; `$fillable` theo cột P2.0
- [ ] Relations: `products()` hasMany ProductImportDetail(`parent_id`), `tabs()` hasMany ProductImportTab, `accounting()` morphMany AccountDetail(`invoiceable`), `costs()` hasMany ImportCost, `emplement_contract()` belongsTo Contract(`emplement_contract_id`), `product_import_request()`, `warehouse_import()` (đọc bảng ERP)
- [ ] `generateCode()` = `'PNH-'.codeHelper(5,id)` (mirror ERP :860 + `BomList::getNextCode` pattern); `canView()/canEdit()` (status==3 && creator) — cờ quyền fail-closed
- [ ] `ProductImportDetail`/`ProductImportTab`/`ProductImportTabProduct`/`ProductImportDetailAccounting` (`$table`, `$fillable`, quan hệ product/unit, `acc_warehouse`)
- [ ] **Verify:** `tinker` load `ProductImport::with(['products','tabs','costs'])->first()` không lỗi cột/quan hệ

### P2.2 — Service khung `ProductImportService` (dispatch theo type)
**Files:** Create `Modules/Finance/Services/ProductImportService.php`
**Consumes:** entities P2.1. **Produces:** `store(Request):ProductImport`, `update(Request,ProductImport):ProductImport`, `getData(id):array` (create/show), `searchByFilter(Request)`; protected `buildDetailsByType(int $type, $productImport, $parent, array $lots)`, `accumulateReturnedQtyByType(int $type, ProductImport $obj)`, `resolveAccountingService(int $type): ProductImportAccountingService`.
- [ ] `store()`: `DB::transaction` — nạp parent (`is_import_direct` → `ProductImportRequest::findOrFail` guard `canProductImport`; else `WarehouseImport` guard `canApprove`+`checkInventory`); tạo header (copy type/customer/warehouse/emplement_*/sums/is_import_direct/status/accounting_date), `generateCode()`; `syncCosts()` (inland/pickup/contract) + arrange_delivery/executors (port ERP :594 trở về trước); `buildDetailsByType()`; tạo tab từ `parent->tabs`; `parent->approve()`
- [ ] Nếu `status==1`: `$obj->updateWarehouse()` (P2.3a) + `updateUnitCostPriceOfProducts()` + `accumulateReturnedQtyByType()` (P2.3b) + hạch toán bốc xếp nếu có
- [ ] Hạch toán (nếu `canCreateDept`): `resolveAccountingService($type)` → gọi `->build(...)` → `AccountDetail::saveAccountDetail(...)` (P2.4)
- [ ] `buildDetailsByType`: `case BAN_TRA_LAI` nạp dòng từ lots (mirror ERP :633-744: supplier_price/price/rebate/extra/allocated/price_buy/amount_price_buy/qty + `ProductImportDetailAccounting` acc_warehouses :728); `default: throw ValidationException('Loại nhập chưa hỗ trợ')`
- [ ] `resolveAccountingService`: `BAN_TRA_LAI → app(SaleReturnProductImportAccountingService::class)`; `default: throw`
- [ ] `update()` cho phiếu nháp (status 3) — mirror ERP `update` (:982) phạm vi type 4
- [ ] **Verify:** tinker gọi `store()` với payload direct dựng tay từ YCNH type 4 → tạo `ProductImport` + details + tabs, chưa cần duyệt

### P2.3 — Nhập kho thực + cộng dồn returned_qty
**Files:** method trên `ProductImport` (updateWarehouse/updateUnitCostPriceOfProducts) + `ProductImportService::accumulateReturnedQtyByType`
- [ ] **P2.3a `updateWarehouse()`** — mirror ERP :1225-1297 + `ContractParentImportService` (:200-270): mỗi product × acc_warehouse → lock `AccountingStock` (find/create theo `accounting_warehouse_id`+product), ghi `AccountingStockLog` (qty_before/change/qty_after/value_*), `acc_stock->qty +=`, `stock->accounting_qty +=`; nếu không direct: set warehouse_import status; `objectable_type = OBJ_TYPE_PRODUCT_IMPORT_DETAIL_ACCOUNTING`
- [ ] **P2.3a `updateUnitCostPriceOfProducts()`** — mirror ERP :1199 (cập nhật giá vốn đơn vị sản phẩm)
- [ ] **P2.3b `accumulateReturnedQtyByType` case 4** — mirror ERP :1658-1722, đổi HĐ ERP→HRM: `product_export_request_details.returned_qty += qty`; `product_export_request_tab_products.returned_qty += qty` (nếu có dòng tab); dòng SP HĐ loại 21 (đích chốt ở P2.0): `exported_qty -= qty`, `returned_qty += qty`
- [ ] **Verify:** tinker duyệt phiếu (status→1) → `accounting_stock_logs` +1 dòng/sp, `accounting_stocks.qty` tăng đúng, nguồn `returned_qty` cộng đúng

### P2.4 — Hạch toán nhập trả
**Files:** Create `Modules/Finance/Services/ProductImportAccountingService.php` (base) + `SaleReturnProductImportAccountingService.php`
**Consumes:** ProductImport (P2.1) + AccountDetail. **Produces:** base helpers `revenueDeductionAccounting/costAccounting/bonusContractAccounting/vatExtraCostAccounting/commissionAccounting/riskFundAccounting/inlandCostAccounting(&$accounts,...)`; `SaleReturnProductImportAccountingService::build(ProductImport,$not_paying_bill,$group): array [ok,data]`.
- [ ] Base `ProductImportAccountingService` = port `FirmContractImportService`: các helper build `$accounts` qua `AccountDetail::createDataSaveDept($accounts,$number,$value,$type,$refs,$objects,$note)` (mirror `ProductExportPostingService` :340-450 ngược chiều nhập trả)
- [ ] `SaleReturnProductImportAccountingService::build` (mirror `FirmContractProductImportService::getDataProductImportAccounting` + `prepareData`): lấy `contract = emplement_contract` (HRM), `support_accounting` qua `firm_support_accounting`, `settlement` qua `settlement_contracts` + `Contract.status∈[11,12]` && `approved_time<=request.created_at`, `product_export` (billable) truy từ product_export_request
  - Chưa QT: giảm trừ DT (Nợ1311/Có5213 + Có33311 VAT; `not_paying_bill`→bỏ VAT); giá vốn (Nợ1561/Có632 theo `supplier_price*qty`); thưởng(5211/35241) + TNCN(35241/3335) + hoa hồng tháng/quý(6411/35241) + quỹ rủi ro(6411/35241) theo support_accounting; chi phí nội địa
  - Đã QT: Nợ5212/Có1311 (Σamount_price_buy) + 33311 VAT + Có1311(Customer); giá vốn + chi phí nội địa (bỏ thưởng/thuế/quỹ)
- [ ] Ghi sổ trong `store()`: `AccountDetail::saveAccountDetail($data, $obj->id, ProductImport::class(FQN ERP `App\Model\Warehouse\ProductImport`), $obj->code, $meta)` với `$meta` = contractable(Contract HRM)/billable(ProductExport)/company/created_by (mirror `ProductExportPostingService` :80-100)
- [ ] **Verify:** tinker duyệt phiếu → `account_details` (invoiceable=ProductImport, contractable=Contract HRM, billable=ProductExport); ΣNợ=ΣCó lệch 0; đối chiếu 1 phiếu nhập-trả ERP thật nếu có

### P2.5 — Controller + Requests + Transformers + Routes
**Files:** Create `Modules/Finance/Http/Controllers/V1/ProductImportController.php`, `Http/Requests/ProductImport/{ProductImportStoreRequest,ProductImportUpdateRequest}.php`, `Transformers/ProductImportResource/{ProductImportListResource,ProductImportDetailResource}.php`; Modify `Modules/Finance/Routes/api.php` (+group `/product-imports`)
- [ ] Controller (mirror `ProductImportRequestController`): `index`(searchByFilter)/`create`(getData theo `warehouse_import_id`|`product_import_request_id`)/`store`/`show`/`edit`/`update`/`searchData`/`printData`
- [ ] `ProductImportStoreRequest`/`UpdateRequest`: rule mirror ERP `store` (:268-300) — status∈[1,3], lots required, mỗi lot product/unit/detail_type/supplier_price/…, acc_warehouses required_unless qty=0 + tổng SL khớp, parent id required
- [ ] Transformers + route group `/product-imports` (quyền "Kế toán kho" gate trong Entity `searchByFilter`+`canView` như ProductImportRequest)
- [ ] **Verify:** `GET /product-imports/create?product_import_request_id=Y` trả data dòng đúng; `POST /product-imports` tạo phiếu

### P2.6 — FE (Nuxt) `hrm-client/pages/finance/product-imports/`
**Files:** Create `index.vue`, `create.vue`, `_id/index.vue` (+ components nếu cần). Skills bắt buộc đọc: `button-convention`, `modal-popup`, `form-validate`, `unsaved-changes`, `notification-convention`.
- [x] `create.vue` nhận query `warehouse_import_id`|`product_import_request_id` → gọi API nguồn; bảng chi tiết mirror ERP + parity P1.8 + chi phí; nút Lưu (status 3)/Duyệt (status 1); `markFormSaved()`; cờ quyền fail-closed. **Đường A** dùng endpoint mới `warehouse-import-source` (dựng từ lô ERP), đường B dùng API show YCNH sẵn có.
- [x] `index.vue` (searchData list) + `_id/index.vue` + `_id/edit.vue` (show/sửa) đã có
- [ ] **Verify:** mở màn create từ 2 đường vào, nhập + Duyệt chạy end-to-end trên trình duyệt (BE store đã verify tinker; còn chạy tay UI)

### P2.7 — Nút entry (2 đường vào)
- [x] **Đường B (HRM):** ĐÃ CÓ SẴN — `pages/finance/product-import-requests/_id/index.vue` nút "Tạo phiếu nhập hàng" (`goCreateProductImport`, gated `is_can_product_import` = BE canProductImport: status CHO_DUYET && is_import_direct=1 && quyền Kế toán kho) → `router.push('/finance/product-imports/create?product_import_request_id='+id)`
- [x] **Đường A (ERP) — trang chi tiết:** `resources/views/warehouse/warehouse_imports/show.blade.php` — nút "Tạo phiếu nhập hàng" tách nhánh: HĐ HRM → `config('app.HRM_URL_FE')/finance/product-imports/create?warehouse_import_id=X` (target=_blank), ngược lại giữ route ERP nội bộ. Điều kiện HĐ HRM = accessor MỚI `WarehouseImport::getIsHrmContractImportAttribute()` (trace WI→WIR→product_import_request.emplement_contract_id != null) — mirror nút loại 20/21 ở `warehouse_exports/show.blade.php:491`. Verify tinker: WI 8913 (HĐ13)=true→HRM, WI 8912=false→ERP.
- [x] **Đường A (ERP) — menu ⚙️ DANH SÁCH (bổ sung 2026-08-28, bug user báo):** `WarehouseImportsController::searchData` action-column (`:310`) build link `productImport.create` CỨNG → chưa branch HRM. Đây mới là entry point user thực dùng (không phải trang chi tiết). Đã vá: `if ($object->is_hrm_contract_import)` → HRM URL (target=_blank), else route ERP. Mirror y hệt `WarehouseExportsController:163-171`. Gate bằng `is_hrm_contract_import` (KHÔNG dùng type vì type=4 bán trả lại không riêng cho HĐ HRM). Verify: href row 8913 = `http://127.0.0.1:3000/finance/product-imports/create?warehouse_import_id=8913`; lint sạch. (2 action-column khác `:377`,`:1960` không có link tạo PNH → không cần vá.)

### P2.8 — Redesign màn tạo phiếu nhập hàng thành tab (FE-only, 2026-08-28)
- [x] `ProductImportForm.vue` — dọn UI Thông tin chung: (1) xoá 2 câu mô tả dev thừa (hdr-note "SL trả = SL xuất − Đã trả…" trên bảng + callout note-info dài dưới bảng); (2) fix ô chứng từ nguồn trống ở **đường A** — trước chỉ render "Phiếu YC nhập hàng" (=`product_import_request_code`, luôn null ở đường A) → nay `v-if is_import_direct===0` hiện **"Phiếu nhập kho" = `warehouse_import_code`**, else "Phiếu YC nhập hàng"; (3) map `is_import_direct`/`warehouse_import_id` trong `loadForEdit` để nhánh nhãn đúng khi Sửa. Còn hở (chưa yêu cầu): edit resource BE (`ProductImportDetailResource`) chưa trả `warehouse_import_code`/`customer_name`/`warehouse_name` → màn Sửa các ô này vẫn `—`.
- [x] `ProductImportForm.vue` — **Thông tin chung giữ SECTION RIÊNG (luôn hiện)** ở trên; chỉ **Hàng hoá nhập trả lại / Chi phí nội địa / Chi phí bốc xếp** gom vào 1 dải `<b-tabs nav-class="nav-tabs nav-bordered">` (mirror form YCNH `ProductImportRequestForm.vue:330`). Tab "Hàng hoá" active mặc định; 2 tab chi phí `v-if="canViewCostPrice"`; nút "Thêm chi phí" chuyển vào thân tab (căn phải). Nội dung bảng hàng + `CostTable` giữ nguyên, KHÔNG đổi script. Thanh actionbar ngoài tabs. CSS `.pnh-tabs` (::v-deep) đồng bộ `.pir-tabs`.

### P2.T — Test E2E (đường B, erp_hrm_check)
- [ ] `grep DB_ .env` = erp_hrm_check; dùng PYCXH-35676/HĐ13 (emp13=namdangit) → tạo yêu cầu nhập hàng bán trả lại → bấm "Tạo phiếu nhập hàng" → nhập SL trả + phân bổ kho kế toán → Duyệt
- [ ] Verify: `product_imports` (type 4, emplement_contract_id=13, code PNH-…); `accounting_stocks.qty` tăng; `returned_qty` cộng đúng (`product_export_request_details` + dòng SP HĐ); bút toán đúng TK, ΣNợ=ΣCó=0
- [ ] Hoàn nguyên toàn bộ data test

## PENDING
- [ ] Import type 9 (bán mượn trả) cho loại 21 — chờ "phiếu xuất bán hàng mượn" loại 21
  - **Cập nhật 2026-08-25 (QA feature de-nghi-nhap-kho):** `handleAfterSubmit` (:1475) NAY đã bump cả type 9 → CHO_TP_DUYET (trước chỉ type 4). Sửa lại note plan:40 "Không cần sửa cho nhánh 21": chỉ đúng cho *luồng giá loại 21*; còn cổng TP duyệt của type 9 đã bật để khớp ERP :699-701, phòng khi ai tạo tay phiếu type 9 (vẫn nằm trong CREATABLE) — nguồn borrow-sell loại 21 vẫn PENDING như trên.

## Checkpoint — 2026-08-25
Vừa hoàn thành: Phase 1 nửa trước (BE + FE) — lập + validate + duyệt giá phiếu nhập bán trả lại nguồn HĐ HRM loại 21.
- DB: migration `emplement_contract_id/type/code` trên `product_import_requests` (đã migrate)
- Finance `ProductExportRequest`: +const (XUAT_BAN_HOP_DONG, STATUS_DA_HACH_TOAN, HRM_CONTRACT_SETTLED_STATUSES, HRM_CONTRACT_CLASS); `searchForImportType` +nhánh 21; `dataForSaleReturn`→`dataForSaleReturnHrmContract`
- `ProductImportRequestService`: `guardBusinessRules`+`guardSaleReturnHrmContract`; `fillFromExportRequest` nhánh 21
- Controller `exportRequests` +`contract_code`; FE `ExportRequestSearchModal` +cột "Số hợp đồng"
- Verify: DB smoke test dữ liệu thật (phiếu 35676/HĐ13) tất cả nhánh OK; lint sạch
Đang làm dở: (không) — Phase 1 code done
Bước tiếp theo: E2E trên hệ thống chạy khi có 1 lần bán loại 21 hoàn tất hạch toán (status 5); sau đó Phase 2 (nhập kho thực + cộng dồn returned_qty + hạch toán). Type 9 vẫn PENDING.
Blocked: chưa có phiếu xuất loại-21 status=5 trong DB để E2E store()→duyệt TP

## Checkpoint — 2026-08-28
Vừa hoàn thành: **Nối ĐƯỜNG A (nhập trả gián tiếp, `is_import_direct=0`, nguồn Phiếu nhập kho ERP `WarehouseImport` + lô `WarehouseImportLot`) ở tầng BE** — trước đó Phase 2 chỉ chạy đường B (`product_import_request`). Đường A giờ chạy end-to-end cả 2 nhánh status.
- **Entities:** tạo `Modules/Finance/Entities/Contract/WarehouseImportLot.php` (read-only, `$guarded=['*']`); `WarehouseImport.php` +quan hệ `warehouseImportRequest()` (BelongsTo) + `lots()` (HasMany) — CHỈ để đọc, không mở ghi.
- **ProductImportService:** thêm `resolveSourcePir($parent,$isImportDirect)` (đường A truy ngược WarehouseImport→WarehouseImportRequest→ProductImportRequest lấy HĐ HRM) + `sourceProductImportRequest($obj)` (đi ngược từ `warehouse_import_id` khi ghi sổ/cộng dồn). `fillHeader` đọc emplement/firm/customer từ `$sourcePir` (không phải `$parent`); `product_import_request_id` để **NULL** cho đường A (khớp ERP đọc chung bảng). `buildDetailsForSaleReturn` +nhánh đọc lô từ `WarehouseImportLot` (theo parent/product/unit/detail_type) → set `lot_id`. `accumulateReturnedQtySaleReturn` bỏ early-return đường A (guard `warehouse_exported_qty` bên trong vẫn chỉ đường B). `markParentUsed` +nhánh đường A ghi status qua `DB::table()` (WI→7, WIR→7, PIR→9).
- **Thông báo đường A (`notifyParentImportedIndirect`):** bắn 2 thông báo cho người tạo WIR + PIR qua `EmployeeInfoService::sendNotification` (chuông HRM, precedent D9 — KHÔNG ghi bảng `notifications` kiểu ERP). Nội dung chuẩn skill notification-convention: `[PDNNK] Đã duyệt: <b>{mã}</b>. Đã được nhập kho.` + `[NH] Đã duyệt: <b>{mã}</b>. Đã được nhập kho.`, deep-link `/finance/warehouse-import-requests/{id}` + `/finance/product-import-requests/{id}`; map `created_by`(employees)→`employee_info_id`; try/catch+log mỗi người. CỐ Ý bỏ `Redis::publish("ke_toan_only_…")` (board kho ERP, cần accessor `activity_message`).
- **ProductImport::updateWarehouse:** đường A ghi WI status→1 + `handled_time`, WIR→4 qua `DB::table()`; vòng nhập kho thực vẫn chạy (bỏ `return`).
- **HTTP:** `ProductImportStoreRequest` `warehouse_import_id` →`required_if:is_import_direct,0`; dọn docblock "đường A CÒN PARKED" ở Request + `ProductImportController`.
- **Verify (tinker dry-run rollback, `erp_hrm_check`, nguồn PNK-08913→WIR-8538→PIR-12231→HĐ13, emp 34 duyệt):**
  - Nháp (status=3): header đúng (`warehouse_import_id=8913`, `product_import_request_id=NULL`, emplement HĐ13), 2 dòng có `lot_id`, upstream status chưa đổi. ✅
  - Hoàn thành (status=1): WI→1+handled_time, WIR→4, PIR→9; `returned_qty` +1 ở `product_export_request_details` 226755/6 + `product_export_request_tab_products` 178173/4; `warehouse_exported_qty` KHÔNG trừ (đúng đường A); nhập kho thực `accounting_stock_logs` 2 dòng; hạch toán `account_details` 6 dòng scope đúng HĐ13 (contractable=Contract, contract_created_by=13). `billable_id=NULL` đúng vì PER-35676 `is_export_direct=0` (đường-A-export đã park, không có ProductExport). ✅
Đang làm dở: (không) — BE đường A done + verified (gồm cả 2 thông báo WIR/PIR, verify tinker tạo đúng 2 noti info 6, đúng nội dung + deep-link).
Bước tiếp theo: FE đường A — P2.6 `create.vue` nạp theo `warehouse_import_id` + P2.7 nút Blade `warehouse_imports/show.blade.php` (ERP) redirect sang HRM.
Blocked: (để trống)

## Checkpoint — 2026-08-28 (FE đường A)
Vừa hoàn thành: **Nối ĐƯỜNG A ở tầng FE + endpoint nguồn BE** — màn Tạo phiếu nhập hàng HRM giờ nạp được từ CẢ 2 nguồn (query `product_import_request_id`=đường B, `warehouse_import_id`=đường A).
- **BE endpoint nguồn đường A:** `ProductImportService::getWarehouseImportSource($wiId)` — truy ngược WI→WIR→PIR (dùng lại `resolveSourcePir`), dựng header (`is_import_direct=0`, `product_import_request_id=NULL`, `warehouse_import_id/code`, warehouse/customer/emplement_contract, company_id, vat) + `products[]` từ lô ERP (`WarehouseImportLot` theo `parent_id`), enrich giá từ `ProductImportRequestDetail` khớp product/unit/detail_type (đúng cặp `buildDetailsForSaleReturn` dùng lúc store). Giá vốn gate quyền "Xem giá vốn hàng hoá" → null nếu thiếu (mirror đường B). Field `products` trùng tên field resource đường B → FE map chung 1 helper.
- **Controller/Route:** `ProductImportController::warehouseImportSource()` (UNGATED, giá đã gate trong service) + route `GET finance/product-imports/warehouse-import-source`. `accountingWarehouses()` +nhánh `warehouse_import_id` (resolve warehouse/company từ `warehouse_imports`).
- **FE `ProductImportForm.vue`:** header +`warehouse_import_id/code` +`is_import_direct`(=1 mặc định). Tách helper `mapSourceRow(p)` (dùng chung 2 đường). `loadForCreate()` chọn nhánh theo query (ưu tiên `warehouse_import_id`): đường A gọi `warehouse-import-source`, set `is_import_direct=0`; đường B giữ như cũ (set `=1`). `loadAccountingWarehouses()` keyed theo `warehouse_import_id` khi đường A. `buildFormData()` gửi `is_import_direct=0`+`warehouse_import_id` (đường A) / `=1`+`product_import_request_id` (đường B). `buildLotsPayload()` KHÔNG đổi (đã gửi đủ identity product/unit/detail_type/pird + acc_warehouses).
- **FE `create.vue`:** gỡ docblock "đường A CÒN PARKED".
- **Verify:** lint PHP 3 file sạch; `getWarehouseImportSource(8913)` tinker trả header đúng (wi 8913, pir_id=NULL, is_import_direct=0, warehouse=Liên Ninh, customer Đại Nam, emplement PYCXH-35676) + 2 dòng pird 61734/61735 KHỚP CHÍNH XÁC `WarehouseImportLot` (product 3962/3960, unit 44, dt 1) → FE round-trip tìm đúng lô; `supplier_price=null` (emp 34 không quyền giá) = gate đúng, `vat=8.0` từ reqProduct = match được. Store end-to-end đã verify ở checkpoint trên (cùng payload shape).
Đang làm dở: (không) — FE đường A wiring done. Màn `index.vue`/`_id/index.vue`/`_id/edit.vue` đã có sẵn.
Bước tiếp theo: P2.7 — nút entry.
Blocked: (để trống)

## Checkpoint — 2026-08-28 (P2.7 nút entry — HOÀN TẤT Phase 2 code)
Vừa hoàn thành: **Nút entry cả 2 đường vào màn Tạo phiếu nhập hàng.**
- **Đường B (HRM) — ĐÃ CÓ SẴN từ trước:** `pages/finance/product-import-requests/_id/index.vue:365` nút "Tạo phiếu nhập hàng" (`goCreateProductImport`, gated `is_can_product_import`) → `/finance/product-imports/create?product_import_request_id={id}`. Không phải làm gì thêm.
- **Đường A (ERP) — MỚI:** `ERP/…/resources/views/warehouse/warehouse_imports/show.blade.php:405` tách nhánh nút "Tạo phiếu nhập hàng": nếu `$import->is_hrm_contract_import` → `config('app.HRM_URL_FE')/finance/product-imports/create?warehouse_import_id={id}` (target=_blank, mirror nút xuất hàng loại 20/21 ở `warehouse_exports/show.blade.php:491`); ngược lại giữ route ERP nội bộ `productImport.create`.
- **Accessor MỚI** `WarehouseImport::getIsHrmContractImportAttribute()` (ERP model): trace WI → `warehouse_import_request` → `product_import_request` → `emplement_contract_id != null` = HĐ HRM. Chỉ THÊM method mới, không sửa logic chung.
- **Verify:** lint ERP model sạch; tinker qua model thật: WI 8913 (WIR 8538→PIR 12231, HĐ13) `is_hrm_contract_import=true` → nút sang HRM; WI 8912 `=false` → nút ERP nội bộ. `config('app.HRM_URL_FE')` tồn tại (config/app.php:17). PER 35676 type=21 xác nhận nguồn loại 21.
Đang làm dở: (không) — **toàn bộ code Phase 2 (BE+FE, cả đường A & B, nút entry) đã xong + verify tinker.**
Bước tiếp theo: P2.T — E2E chạy tay trên trình duyệt (erp_hrm_check): từ PNK HĐ HRM bấm nút → màn create HRM đường A → nhập phân bổ kho → Duyệt → kiểm tra `product_imports`/`accounting_stocks`/`returned_qty`/bút toán, rồi hoàn nguyên data.
Blocked: (để trống)
