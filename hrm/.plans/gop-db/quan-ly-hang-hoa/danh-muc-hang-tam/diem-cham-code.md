# Điểm chạm code Phase 6 — Hàng tạm (khảo sát chỉ đọc 12/10/2026)

> API = `wt-chuyen-doi-hang-hoa/hrm-api` · CLI = `wt-chuyen-doi-hang-hoa/hrm-client` · ERP = `wt-erp-2d1`. Dùng làm căn cứ viết `p6-plan.md`.

## A. Trạng thái hàng × công ty
- `API/Modules/MasterData/Entities/Product/ProductCompany.php:23-47` — mã 1–5, `PRICING_FLOW_STATUSES=[2,5]` (:30), STATUS_TEXT/COLOR, `isLocked` (:62). Thêm 6/7/8 + `TEMP_STATUSES`.
- `ProductService::applyScreen` (:180-216): WAREHOUSE chỉ lọc `products.status<>0` ⇒ **lọt hàng tạm**; COMPANY `IS NOT NULL` ⇒ **lọt 6/7/8**; ENTERING `IN(1,2,5)`; TRADING `=3`. `show()` others_using_count `status is not null` (:168-172).
- `Product.php`: scopes `withCompanyStatus` :365 (pcs) / `withOwnerStatus` :390 (pco); `editableAt` :401 (chỉ chặn 4); `takeableAt` :413 (owner=3); `deletableAt/deleteModeAt` :446-465 (chỉ mã 1).
- Resource đọc `STATUS_TEXT[...] ?? null`: `ProductListResource.php:27,57`, `ProductDetailResource.php:28,42`, `ProductFormResource.php:46`.
- `ProductWriteService`: take :159-215, `takeSkipReason` :218-238, `updateAdmin` :240-250, `update` :252-268, `writeAdmin` :565-607.
- `ProductLifecycleService`: destroy :68-99 (chỉ mã 1), lock :219, `statusPayload` :285.
- `ProductCatalogService` tab Thêm :140-145 (`<>4` ⇒ lọt), `checkProductsAddable` :155-175 (lọt).
- Giá: `InternalPricePolicyService.php:579`, `ProductPriceListService.php:126`, `ProductPriceUpdateService.php:165-185`, `ProductPriceSetWriter::companiesWithStatus` :26-34, `ProductPriceApprovalService.php:489`.
- Luồng giá: `PriceAskingRequestWriter.php` :112 (1→2 gửi), :278 ({2,5}→1 PTKD từ chối), :349 ({2,5}→1 đóng nhóm), :399 `moveProducts`; `PriceCalculateWriter.php` :124,:170,:209,:423; `PriceCalculateFinalizer.php:240` ({2,5}→3).
- YCHG chọn hàng `PriceAskingProductReader.php`: :24 `SELECTABLE_STATUSES=[1,3]`, :42 search, :82-96 `blockReason`, :98 `base()` INNER JOIN brands/manufactures.
- Không lọc pcc (lọt mọi mã kể cả 6/7/8 — có từ trước): `ProductOptionService::itemSearch` :126-134 · `CustomerCare/Services/ServiceService.php:997` · `DeviceErrorController.php:258`.
- FE: `CLI/utils/product-list-screens.js:49-172, 206-217`; `ProductListPage.vue:329,601,870`; `PriceAskingRequestForm.vue:162`; `PriceAskingProductPickerModal.vue:31`.
- Khuôn rà "mã 5": `luong-tinh-gia/t2-plan.md:56-76`; test bất biến `ProductCompanyFoundationTest.php:58-62`.
- ERP: popup chỉ nhận `pcc.status=3` (`SearchController.php:109-122`, gọi :456, :939, :1361, :1747) ⇒ 6/7/8 tự bị loại; cron 14:30 không đọc status ⇒ **ERP không sửa lọc**.

## B. Đường ghi hàng hoá
- Tạo: `POST master-data/products` (`Routes/api.php:405`, 1652) ⇒ `ProductWriteService::store` :71-98 ⇒ `ProductCodeGenerator::generate(?manufactureId, ?barcodeId, ?modelId, ?ignoreId)`; `writeAdmin(..., STATUS_ENTERING_INFO)` đọc `$a['job_cluster_ids']` (không `??`).
- `ProductRequest`: authorize :23-33 (1652 + assertOwner); rules :41-135 (product_type_id required :58, characteristic nullable :59, VAT :109); `adminRules()` :139-152 (`admin.job_cluster_ids required|min:1` :149); withValidator :180-191 (`checkUniqueName` :279-302 Tên×Model×Thương hiệu×Hãng, `checkClusters`).
- Tab Quản trị: `PUT products/{product}/admin-data` (:411, 1652) ⇒ `updateAdmin` ⇒ `assertCanEditAdmin` :128-141; `ProductAdminDataRequest.php` authorize :20-35, `adminKeys` :38-50.
- Xoá: `DELETE products/{product}` (:416) ⇒ `ProductLifecycleService::destroy` ⇒ `hardDelete` :105-170 ⇒ `ProductUsageGuard::FK_COLUMNS` :31-58 có **`price_asking_request_products` (:56)**.
- Sửa: `PUT products/{product}` (:412) ⇒ `assertOwner` :108-121 ⇒ `update` :252-268; `GET {product}/edit` :410.

## C. YCHG / YCTG
- `PriceAskingRequestWriter::save(?id, input{note, product_ids}, send)` :63-124 (lockForUpdate pcc :81; `validateInput` :144-183; `rebuildLines` :186-219 gom brand×manufacture); `ptkdApprove` :223-261 (lockForPtkd :286, nhóm ⇒ chờ XNK, phiếu ⇒ 10, **chưa đổi pcc**); `ptkdReject` :263-284 (phiếu 8, pcc {2,5}→1); `closeGroup` :329-361; `log()` :409-415.
- Gate 1662: `Routes/api.php:296-299` + `PriceAskingAccess::canPtkd` :88-96. Controller `PriceAskingRequestController.php` store :97, update :105, approve :120, reject :127.
- `price_asking_request_approve_histories`: id, price_asking_request_id, group_id, created_by, note, type, timestamps — **không có product_id**.
- YCTG lấy dòng: `PriceCalculateRequestService::skeletonRows` :244-262 (:246 theo group_id); :193 đếm; `PriceCalculateWriter.php:358`.
- FE `CLI/components/sale/price-asking/PriceAskingRequestForm.vue`: nút "Chọn hàng hoá" :57-60, bảng nhóm :65-190 (dòng :149-185, badge :162), footer Duyệt :239-242 / Từ chối :243-246, `save` payload `{note, product_ids, send}` :544-547, PTKD qua `PriceAskingReasonModal` :600-625.

## D. Popup hàng tạm có sẵn
- `CLI/pages/assign/quotations/components/QuotationProductSearchModal.vue` (2230 dòng): props :566-614 (enableReuse, projectId, hideManualCreate…); emit `apply(items, parentRowId, groupId)`; overlay :247-420; tab Tái sử dụng :277-338 ⇒ `GET assign/product-projects?only_temp=1&prospective_project_id=` (:1351), `reuse-children` (:1475); tab thủ công :341-392 (Tên*, 1 ĐVT*, Model, Thương hiệu*, Xuất xứ*, SL, Ghi chú, TSKT — **không Hãng SX/Loại SP/VAT/Đặc tính**); `createProduct` :1545-1600 **không gọi API**, chỉ emit.
- BE `Modules/Assign/Http/Controllers/Api/V1/ProductProjectController.php`: index :58-78, `filterOutNativeErp` :110-125 (ẩn dòng có erp_product_id mà `products.tmp_product_id` NULL), `applyKeyFilters` :235-260 (không lọc quyền xem dự án), `reuseChildren` :334; route `Assign/Routes/api.php:476-486`.
- Mã: `BomListService.php:2336-2340` (`HHB`+id 6 số), `QuotationService.php:2598-2723` (HHBG). Cột `bom_list_products.erp_product_id`, `quotation_product_prices.{bom_list_product_id, erp_product_id, erp_tmp_product_id}`.

## E. FE hàng hoá
- `CLI/components/product/form/ProductForm.vue`: props mode/productId/backUrl :83-87; `editScope full|admin` :100; parentTabs :105-118; stepTabs :134-142; save :254-288 (`PUT {id}/admin-data` | `PUT {id}` | `POST`). `productFormModel.js` (toPayload/toAdminPayload). `ProductFormAdmin.vue` :93-100; `ProductFormCatalogPicker.vue` :82-85; `ProductFormGeneral.vue` (Đặc tính :91-99 không required); `ProductFormPurchase.vue:23` VAT.
- Danh sách: `ProductListPage.vue` (slug :1047, `rowActionsOf` :832-845), khuôn `pages/master-data/products/entering.vue`, registry `utils/product-list-screens.js:49-172`, menu hub `components/subsystem-menu/master-data.js:59-85` (`subItems`).
- Menu "Danh sách hàng tạm": `components/menu-sidebar.js:34-35`; tiêu đề `pages/assign/product-project/index.vue:47`.

## F. Đường cũ cần gỡ (HRM)
- `Modules/Assign/Services/TmpProductSyncService.php`; routes `Assign/Routes/api.php:677-679, 814-822`; controller `QuotationController.php` :734, :756, :778, :825, `buildTmpSyncSummary` :137-145; `QuotationResource.php:105`.
- `QuotationErpSyncService.php` sync gọi `createTmpProducts` :43 (:105-129); `buildPayload` dùng `$tmpProductMap` :171-202; nơi gọi `QuotationService::syncToErpAfterApproval` :4095-4105 (+ :4005, :4055, :4090), `QuotationController.php:1917`.
- FE `ProspectiveProjectQuotationsTab.vue`: banner :3-37, tmpSync :414-445, :518, :655-713; banner hợp đồng :40-80 phụ thuộc `contract.is_synced`.

## G. ERP chặn
- `routes/web.php` :678-692 (`tmp_products`), :694-699 (`my_tmp_products`), :3634-3644 (`sale/tmp_product_requests`); API `routes/api.php:74-77` (`sync-from-hrm`, `approved-status`).
- `ProductMovedToHrm.php` TARGETS :29-50, handle :66-93; view `errors/moved_to_hrm.blade.php:21-23`.
- Menu topmenubar :20, :326, :1525-1532, :2227-2229, :2377-2381; `HomeController.php:548-573`; nút `quotations/form.blade.php:182-183`; partials `partials/tmpProduct/*` include ở quotations/form :720, create :150, edit :114, project_quotations/form_template :701, tmp_product_requests/form :68.
- Test khuôn `tests/Feature/PriceFlowRoutesMovedToHrmTest.php`.

## H. Test
- PHPUnit `API/Modules/MasterData/Tests/Feature/PriceAskingRequestApiTest.php` (trait `Concerns\ActsAsProductUser::actAs`, helper `product($key,$group,$status)`, `create()` :140); `ProductWriteApiTest.php`, `ProductLifecycleApiTest.php`, `ProductCompanyFoundationTest.php` (bất biến tập status). Chạy `cd API && vendor/bin/phpunit Modules/MasterData`.
- e2e `ERP-HRM/HRM/e2e/tests/sale/price-asking-request.spec.ts`; khuôn hàng hoá `wt-chuyen-doi-hang-hoa/e2e/tests/master-data/products-*.spec.ts`.

## Mâu thuẫn spec ↔ code (đưa vào tồn plan)
1. Xoá hàng tạm bị `ProductUsageGuard` chặn khi đã có dòng YCHG (FK), kể cả phiếu Không duyệt; `destroy` chỉ nhận mã 1.
2. `ptkdReject` / `closeGroup` đưa {2,5}→1 — hàng tạm sau PTKD duyệt (đã là 2) khi nhóm đóng không giá ⇒ về 1 hay 6?
3. `ptkdApprove` chưa đổi pcc; nhóm toàn hàng 8 sẽ sang XNK rỗng.
4. Chọn hàng YCHG chỉ nhận [1,3]; hàng 7 sửa ⇒ về 6 cần hook ở `update`.
5. Tạo hàng gắn 1652 + catalog bắt buộc; popup thiếu Hãng SX / Loại SP / VAT / Đặc tính / nhiều ĐVT.
6. Kho + màn company + catalog + itemSearch + CustomerCare để lọt 6/7/8.
7. `filterOutNativeErp` ẩn dòng BOM/báo giá đã gắn mã hàng tạm ⇒ mất khỏi "Hàng tạm dự án".
8. Tái sử dụng không lọc quyền xem dự án, bắt buộc `prospective_project_id`.
9. `approve_histories` không có product_id.
10. Gỡ `createTmpProducts` ảnh hưởng `buildPayload` + điều kiện `contract.is_synced` (lập HĐ ERP).
