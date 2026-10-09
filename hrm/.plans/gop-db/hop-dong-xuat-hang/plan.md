# Plan — Xuất hàng HĐ trên HRM

Design: `.plans/hop-dong-xuat-hang/design.md` · Spec: `docs/superpowers/specs/2026-08-14-hop-dong-xuat-hang-design.md`

## Phase 0 — Nền tảng chung
- [x] Thêm 2 loại vào `ExportModel` ERP (20/21) + TYPES (chưa commit — ERP master).
- [x] Xác nhận: nhập thẳng = accounting_warehouses.is_import_export_direct=1; tồn kho = accounting_stocks.
- [x] Migration: product_imports thêm emplement_contract_id/code/type (migrated).
- [x] 5 models HRM (Modules/Assign/Entities/Warehouse) + scope forHrmContract + hằng loại 20/21.

## Phase 1 — Chuỗi Xuất bán HĐ HRM (loại 21)
### BE
- [x] **MVP bước 1** — Migration `2026_08_14_000003` (emplement_contract_* + contract_group_id/contract_product_id vào product_export_request_tabs/tab_products, migrated). 2 model tab (ContractExportRequestTab + products(), ContractExportRequestTabProduct). `ContractExportRequestService::createFromContract` (loại 21, code PYCXH-{id}, snapshot KH, 1 tab HĐ + dòng hàng cha + dòng phẳng product_export_request_details). Controller `storeExportRequest` (chặn `can_export`, rethrow ValidationException) + route `POST /assign/contracts/{id}/export-requests`. Test OK: PYCXH-35669 cho HĐ 15 (1 tab 3 dòng). **Gác lại**: quỹ cha-con, checkLimitOverLimit (công nợ→TP duyệt), duyệt đa cấp.
- [ ] API + service tạo **Yêu cầu xuất hàng** (`product_export_requests`) từ HĐ HRM (chọn hàng cha + số lượng) — gắn emplement_contract. ← MVP xong, còn: nhận `products[]` từ FE, validate SL ≤ SL HĐ, load kho mặc định.
- [ ] API + service **Đề nghị xuất kho** (`warehouse_export_requests`) từ yêu cầu — chọn kho.
- [ ] Đọc **Phiếu xuất kho** (`warehouse_exports`) do ERP tạo (chỉ hiển thị trạng thái ở HRM).
- [ ] API + service tạo **Phiếu xuất hàng** (`product_exports`) — hạch toán/giao hàng loại 21.
- [ ] Duyệt yêu cầu xuất hàng (quyền "Duyệt yêu cầu xuất hàng").
- [ ] Chặn xuất nếu HĐ chưa hiệu lực / chưa có thời hạn thực hiện (`can_export` — Phase 7.3 đã có).
### FE
- [x] **Form tạo yêu cầu xuất hàng** (modal `ContractExportRequestModal.vue`): chọn hàng cha + SL xuất (default = SL cần, validate 0 < SL ≤ SL cần), ghi chú, nút Lưu nháp (status 3) / Gửi duyệt (status 2). Wire vào `_id/index.vue`: nút "Yêu cầu xuất hàng" trong actionbar, gating `canCreateExportRequest = item.can_export`. Gửi `products[]` {contract_product_id, qty}. BE service sửa: có `products[]` → chỉ tạo dòng được chọn. Compile OK cả 2 file. Kho chọn ở bước Đề nghị xuất kho (không nằm ở yêu cầu).

### Màn DANH SÁCH yêu cầu xuất hàng (hướng A — giống ERP, port từ ProductExportRequests) — @dnsnamdang
Chốt: (1) phân quyền 4 cấp theo convention list-page; (2) logic/filter giống ERP, scope loại 21 gắn HĐ HRM (sau này mở rộng mọi loại); (3) menu: tìm link trống "yêu cầu xuất hàng", không có → tạm vào phân hệ bán hàng.
- [x] BE: 4 quyền id 1148-1151 "Xem yêu cầu xuất hàng theo tổng công ty/công ty/phòng ban/bộ phận" (group "Yêu cầu xuất hàng", type 26) vào PermissionsTableSeeder + insert DB erp_hrm_check + gán role 31 (DNS Admin) test.
- [x] BE: `ContractExportRequestController@index` — scope 4 cấp qua `checkPermissionListWithColumn` (pattern ContractController@index), where type=21 + emplement_contract_type=Contract + ẩn nháp người khác; filter code/keyword/status/company/dept/part/employee/contract_code/date; route `GET /assign/product-export-requests`. Model thêm getStatusList (11 status ERP) + relation creator/approver/emplementContract. Test OK: trả PYCXH-35670 (HĐ 15, đủ cột).
- [x] BE: `ContractExportRequestResource` (mã, HĐ, khách, phòng ban, người lập, ngày tạo, người duyệt, trạng thái+màu, giá trị) + apiPaginate.
- [x] FE: `pages/finance/product-export-requests/index.vue` — V2BaseFilterPanel cascading công ty→PB→BP + filterStateMixin (key finance_product_export_requests) + auto-search watcher + phân trang. Template compile OK.
- [x] FE: menu link `finance.js:109` (placeholder "Yêu cầu xuất hàng" đã có sẵn → thêm link `/finance/product-export-requests` + isShow 4 quyền).

### Duyệt yêu cầu — KHÔNG làm (ERP không có bước này)
- ERP không có nút Duyệt/Từ chối riêng cho yêu cầu xuất hàng thường. "Phê duyệt" = Kế toán kho lập Đề nghị xuất kho (`canApprove` = quyền "Kế toán kho" + status=2 + không xuất thẳng). Duyệt đa cấp (TP/BGD, status 10/11) chỉ khi vượt hạn mức công nợ → đã gác lại. KHÔNG tạo quyền duyệt mới.

### Bước sau — Đề nghị xuất kho (warehouse_export_requests) ✅ MVP
- [x] BE: models `ContractWarehouseExportRequest` (status 1-7 + getStatusList + generateCode PDNXK- + relations) + `ContractWarehouseExportRequestDetail`. Service `createFromExportRequest` (snapshot emplement/khách từ YCXH, tạo details từ product_export_request_details, chọn kho, đổi status YCXH: tạo→7, gửi→1). Controller `warehouseExportData` (dòng hàng + kho) + `storeWarehouseExportRequest`, gate `assertCanApprove` (quyền "Kế toán kho" + status=2 + !xuất thẳng + cùng cty). Route GET `/{id}/warehouse-export-data` + POST `/{id}/warehouse-export-requests`. Test OK: PDNXK-31050 (kho 1, 3 dòng, YCXH→1). **Gác lại**: tính tồn/giữ prepick (updateWarehouse), validateProducts theo tồn, tabs cha-con, thông báo.
- [x] FE: modal `WarehouseExportRequestModal.vue` (chọn kho V2BaseSelectInModal + dòng hàng + SL + Lưu nháp/Gửi thủ kho) + nút "Lập ĐNXK" trong list (status=2 + quyền "Kế toán kho"). Compile OK.
### Phiếu xuất hàng (product_exports) — BE MVP ✅ / FE chờ entry point
- [x] BE: models `ContractProductExport` (status 1/3 + getStatusList + generateCode PXH- + is_completed + relations) + `ContractProductExportDetail` + bổ sung `ContractWarehouseExport` (status const + relation warehouseExportRequest). Service `createFromWarehouseExport` (snapshot từ phiếu xuất kho + emplement từ đề nghị, dòng từ warehouse_export_lots, MVP export_from_stock=qty, cascade: phiếu xuất kho→7, đề nghị→7, YCXH→9 Đang hạch toán). Controller `productExportData` + `storeProductExport`, gate `assertCanExportGoods` (quyền "Kế toán kho" + phiếu xuất kho status=2 + cùng cty, port WarehouseExport::canApprove). Route GET `/assign/warehouse-exports/{id}/product-export-data` + POST `/assign/warehouse-exports/{id}/product-exports`. Test OK (data giả): PXH-34578. **Gác lại**: updateWarehouse (tồn/giữ), TOÀN BỘ hạch toán (account_details/công nợ/bốc xếp), tabs, product_export_detail_accountings, thông báo.
- [x] **FE — chốt hướng: điều hướng ERP↔HRM** (không làm màn đề nghị/phiếu xuất kho ở HRM):
  - Bước "Tạo phiếu xuất kho" DÙNG THẲNG ERP: đề nghị HRM (loại 21) hiện sẵn ở màn danh sách đề nghị xuất kho ERP + nút "Tạo phiếu xuất kho" (canApprove: thủ kho + status 2). ERP store tương thích loại 21 (copy type, set warehouse_export_request_id, không đụng emplement).
  - **ERP mod** (uncommitted, master): nút "Tạo phiếu xuất hàng" trên phiếu xuất kho — nếu `type==21` → redirect HRM `config('app.HRM_URL_FE')/finance/product-exports/create?warehouse_export_id=X` (sửa `WarehouseExportsController@searchData:164` + `warehouse_exports/show.blade.php:489`).
  - **HRM page** `pages/finance/product-exports/create.vue`: nhận `warehouse_export_id`, gọi getData → form dòng hàng + SL + ghi chú + Lưu nháp(3)/Hoàn tất(1), POST storeProductExport. Compile OK.
  - ⚠️ Cần set env `HRM_URL_FE` trên ERP (config/app.php đã có key, default hrm.eteksofts.com).

### Bổ sung — Khối "Thông tin chung" màn Lập ĐNXK (parity ERP)
Màn tạo ĐNXK bên ERP hiện đủ thông tin chung (KH, phiếu YCXH, người yêu cầu, ngày yêu cầu); HRM chỉ có 1 dòng text nhỏ → bổ sung card thông tin chung.
- [x] BE: `warehouseExportData` trả thêm request: customer_name/customer_short_name/customer_mobile/customer_contact_name/customer_contact_phone/customer_address, code, emplement_contract_code, requester_name (creator.info.fullname), department_name, request_date (created_at), note. Eager-load `creator.info.department`. Import Carbon. Lint OK.
- [x] FE `create.vue`: thay dòng text bằng card "Thông tin chung" (card-header có tên user hiện tại + ngày hôm nay) — 2 cột: (trái) Mã YCXH, Số HĐ, Người yêu cầu (+phòng ban), Ngày yêu cầu; (phải) Khách hàng, Người liên hệ + SĐT, Địa chỉ. Kho xuất giữ trong card, ngăn cách bằng `<hr>`. Style `.info-row/.info-label/.info-value`.

### Phase 2 — loại 20 (xuất sản xuất) + auto nhập cha ✅ MVP
- [x] **2a — Yêu cầu loại 20 (hàng con)**: `ContractExportRequestService::createFromContract` nhận `type` (20/21); type 20 → `whereNotNull('parent_id')` (hàng con). Controller truyền `type`. FE modal thêm chọn "Loại xuất" (Xuất bán cha / Xuất sản xuất con), lọc dòng theo type, gửi `type`.
- [x] **2b — Chuỗi loại 20 tái dùng**: type xuyên suốt yêu cầu→đề nghị→PXK→PXH (services type-agnostic, verified). ERP redirect nút "Tạo phiếu xuất hàng" cho **cả loại 20 và 21** (`in_array` — WarehouseExportsController + show.blade).
- [x] **2c — Auto-nhập-cha** (điểm chính): const `NHAP_SAN_XUAT_HOP_DONG=20` vào ERP ImportModel + TYPES. Models `ContractProductImport` (const status/type + generateCode PNH- + relations) + `ContractProductImportDetail`. Service `ContractParentImportService::createParentImport` (map dòng con → `ContractProductPrice.parent` → cha, gộp SL, tạo product_imports nhập thẳng is_import_direct=1 status=1 gắn HĐ, kho `is_import_export_direct=1`, dòng cha). Hook trong `ContractProductExportService`: `status=1 && type==20` → auto-nhập-cha. **Test OK**: PXH-34579 (con 8888) → PNH-12310 (cha 3960, qty 3). **Gác lại**: updateWarehouse (tồn), product_import_detail_accountings, hạch toán phiếu nhập.

### Phase 3 — Verify E2E (trên môi trường thật)
- [ ] E2E: HĐ cha–con → loại 20 xuất con → phiếu xuất kho ERP → phiếu xuất hàng HRM → auto nhập cha → loại 21 xuất bán cha; loại 21 cha đủ tồn → xuất bán thẳng. (cần ERP user là thủ kho + kho nhập thẳng cấu hình)

## Phase 2 — Xuất sản xuất (loại 20) + auto nhập cha
### BE
- [ ] Check tồn hàng cha khi lập yêu cầu: đủ → gợi ý loại 21; thiếu → loại 20 (hàng con).
- [ ] Chuỗi loại 20 cho hàng con (yêu cầu → đề nghị → [ERP xuất kho] → phiếu xuất hàng).
- [ ] **Auto-sinh Phiếu nhập cha** khi Phiếu xuất hàng loại 20 hoàn tất: `product_imports` loại nhập thẳng, kho `NHAP_XUAT_THANG=2`, gắn HĐ HRM + hàng cha.
- [ ] Sau nhập cha → cho phép user tạo chuỗi loại 21 (xuất bán cha) — thủ công.
### FE
- [ ] UI chọn nhánh theo tồn (đủ/thiếu) khi lập yêu cầu; hiển thị phiếu nhập cha auto-sinh.

## Phase 3 — Verify E2E
- [ ] E2E: HĐ có hàng cha–con → cha thiếu tồn → xuất sản xuất con → nhập cha → xuất bán cha; cha đủ tồn → xuất bán thẳng.

### Open items
- Bảng dòng hàng của mỗi chứng từ (product_export_request_tab_products…?) — cần map chi tiết ở Phase 1.
- Hằng số nhập thẳng + logic prepick/giữ có áp không.
- Quyền: dựng bộ quyền cho các chứng từ (Duyệt yêu cầu xuất hàng đã có bên ERP — tái dùng hay tạo mới HRM).

### Checkpoint — 2026-08-14
Vừa hoàn thành: Phase 1 MVP bước 1 — Yêu cầu xuất hàng (loại 21). BE: migration 000003 + models tab + `ContractExportRequestService::createFromContract` (chỉ tạo dòng được chọn khi có products[]) + controller `storeExportRequest` (chặn can_export, rethrow ValidationException) + route POST /assign/contracts/{id}/export-requests. FE: modal `ContractExportRequestModal.vue` (chọn hàng cha + SL + ghi chú + Lưu nháp/Gửi duyệt) wire vào `_id/index.vue` (nút "Yêu cầu xuất hàng", gating can_export). Compile OK, đã dọn bản ghi test PYCXH-35669.
Đang làm dở: (không) — dừng sạch.
Bước tiếp theo: (1) test luồng tạo yêu cầu trên browser; (2) màn "Quản lý thực hiện HĐ" liệt kê yêu cầu/đề nghị/phiếu xuất theo HĐ; (3) Đề nghị xuất kho (chọn kho).
Blocked:

### Checkpoint — 2026-08-15 (b)
Vừa hoàn thành: Toàn bộ chuỗi xuất hàng HĐ HRM (MVP) — Phase 1 (loại 21) + Phase 2 (loại 20 + auto-nhập-cha):
- Yêu cầu xuất hàng (BE+FE modal, list + 4 quyền) · Đề nghị xuất kho (BE+FE modal, gate Kế toán kho) · Phiếu xuất hàng (BE + trang FE nhận warehouse_export_id).
- Điều hướng ERP↔HRM: "Tạo phiếu xuất kho" dùng thẳng ERP (đề nghị HRM hiện ở list ERP); ERP nút "Tạo phiếu xuất hàng" (loại 20/21) → redirect HRM.
- Phase 2: yêu cầu loại 20 (hàng con) + auto-sinh phiếu nhập cha (product_imports nhập thẳng) khi phiếu xuất hàng loại 20 hoàn tất. Test OK PXH-34579→PNH-12310.
Đang làm dở: (không) — dừng sạch.
Bước tiếp theo: (1) test E2E trên browser cả 2 loại (test data: PYCXH-35670 loại 21 status 2 + hàng con 321); (2) commit ERP changes (uncommitted master: ExportModel + ImportModel + WarehouseExportsController + 2 blade); (3) Phase 3 verify E2E môi trường thật; (4) (tùy) bổ sung phần tồn/hạch toán đã gác.

### Checkpoint — 2026-08-17 — Rà soát auto-nhập cha loại 20 (`ContractParentImportService::createParentImport`)
Vừa hoàn thành: Rà lại wiring + logic tạo phiếu nhập cha. **Trigger + logic đúng** (`ContractProductExportService.php:120-124` → PXH status HOAN_TAT & type XUAT_SAN_XUAT_HOP_DONG(20) → `createParentImport`; map dòng con → `ContractProductPrice.parent` → gộp SL cha → tạo `ContractProductImport` type 20 nhập thẳng, kho `is_import_export_direct=1`, dòng cha). Chạy được (đã test PXH-34579→PNH-12310).
**Gap ghi nhận (chưa vá — MVP):**
- 🐛 **[#4 ưu tiên] Không idempotent**: `createParentImport` không kiểm tra phiếu nhập cha đã tồn tại → nếu PXH chuyển HOAN_TAT 2 lần / gọi lại endpoint POST product-exports → **tạo trùng phiếu nhập cha**. Cần check đầu hàm (theo `emplement_contract_id` + nguồn PXH, hoặc thêm cột `source_export_id`).
- **[#5] `warehouse_id` có thể null** nếu công ty chưa cấu hình kho `is_import_export_direct=1` → phiếu nhập cha treo không kho (nên chặn/cảnh báo).
- **[#3] Hệ số đơn vị = 1 cứng** (`import_qty=qty`, `unit_coefficient=1`) → sai nếu hàng cha đơn vị quy đổi khác con.
- **[đã biết] Gác lại**: `updateWarehouse` (tồn cha KHÔNG tăng), `product_import_detail_accountings`, hạch toán, `supplier_price=0` → tồn cha = 0 nên loại 21 (xuất bán cha) sẽ thiếu tồn cho tới khi làm phần này.
Đang làm dở: (không) — chỉ ghi nhận, chưa sửa code theo yêu cầu.
Bước tiếp theo: commit 8 file ERP vào `gop_db`, rồi chuyển `master` fix lỗi đề nghị xuất kho loại 7.
Blocked:

### Phase 2.1 — Vá gap auto-nhập cha (`ContractParentImportService`)
- [x] **#4 Idempotent** (ưu tiên): migration `2026_08_17_000001_add_source_export_id_to_product_imports_table` (cột `source_export_id` nullable + index, migrated erp_hrm_check). `createParentImport` check `ContractProductImport::where('source_export_id', $pxh->id)->first()` ở đầu hàm → có thì trả về luôn (không tạo trùng); set `source_export_id = $pxh->id` khi tạo mới. **Test OK**: chèn stub source_export_id=34581 → service trả stub, count giữ 1 (không tạo trùng).
- [x] **#5 Kho null**: `$warehouseId` null (công ty chưa cấu hình kho `is_import_export_direct=1`, hoặc kho đó có `warehouse_id` rỗng) → `throw ValidationException` message rõ ràng → rollback cả transaction PXH. User vẫn Lưu nháp (status 3) được vì hook chỉ chạy khi HOAN_TAT. **Test OK**: PXH-34581 (cty 1) bắn ValidationException đúng.
  - ⚠️ **Phát hiện dữ liệu**: trong `erp_hrm_check` **cả 4 kho** `is_import_export_direct=1` (HN-NXT cty1, SG-HNXT cty4, HP-KHO NXT cty2, V-NXT cty3) đều có `warehouse_id` **rỗng** → sau fix này, hoàn tất PXH loại 20 sẽ bị chặn cho tới khi gán `warehouse_id` (kho vật lý) cho kho nhập/xuất thẳng. Cần xác nhận prod: kho nhập thẳng có nên có `warehouse_id` không (nếu là kho ảo không gắn kho vật lý thì `product_imports.warehouse_id` phải lấy nguồn khác — gộp vào phase tồn/hạch toán).
- [x] **#3 Hệ số đơn vị** (A3, làm 2026-08-21): `ContractParentImportService.php:162` hardcode `unitCoefficient=1` → `import_qty=qty` sai (accounting_stocks.qty lưu theo ĐVCS, xác nhận qua `WarehouseExportAccountingService:67,80` `exportQty=qty×coef`). Fix: capture `unit_id` cha per product + helper `resolveUnitCoefficient($productId,$unitId)` tra `product_units.unit_coefficient` theo (product_id, unit_id) — không unit_id thì `is_base=1`, fallback 1 (mirror `StockService::computeOne:144-164`). `import_qty = qty × coef` (base). FIFO resale an toàn: `import_qty×import_price=cost` bất kể hệ số (đã verify `layerQtyPrice` đọc `product_import_detail_accountings.import_qty`); bút toán Nợ155/Có1541 dùng `total=cost` nên KHÔNG đổi. FQN/table khớp (IMPORT_ACC_FQN=OBJ_TYPE, table `product_import_detail_accountings`).

### Phase 2.2 — Tồn + hạch toán phiếu nhập cha (auto-import) — quyết định user 2026-08-17
Quyết định user: (1) kho nhập/xuất thẳng **KHÔNG cần kho vật lý** → `warehouse_id` null là hợp lệ, tồn cha ghi theo `accounting_warehouse` chứ không qua kho vật lý → **BỎ guard #5** (không throw khi warehouse_id null). (2) Làm luôn phần tồn/hạch toán. (3) Test **trên local trước** (không đụng prod). (4) Task D (xoá phiếu) làm luôn nếu cần. (5) Git giữ nguyên — chưa push.
- [x] **#5 revise**: bỏ `throw` khi `warehouse_id` null; lấy `accounting_warehouse_id` (`->value('id')` kho is_import_export_direct=1 status=1) làm khoá tồn; `warehouse_id` phiếu = **null** (giống ERP nhập thẳng). Guard mới: throw chỉ khi công ty KHÔNG có kho thẳng nào.
- [x] **3 model tồn HRM** (Modules/Assign/Entities/Warehouse): `AccountingStock` (accounting_stocks), `AccountingStockLog` (accounting_stock_logs, hằng OBJ_TYPE = FQN ERP `App\Model\Warehouse\ProductImportDetailAccounting`), `ProductImportDetailAccounting` (product_import_detail_accountings).
- [x] **updateWarehouse cha** (`applyStock`): tăng `accounting_stocks.qty` (khoá accounting_warehouse_id + product_id, stock_id=null kho ảo) + ghi `accounting_stock_logs` (change +import_qty, qty_after, objectable = FQN ERP để giá vốn FIFO nhận diện). KHÔNG đụng `stocks` vật lý. KHÔNG tạo `product_import_direct_details` (loại 21 xuất trừ theo accounting_stocks; tạo sai employee còn gây `dd('Có sai sót')`).
- [x] **product_import_detail_accountings**: 1 dòng/hàng cha (accounting_warehouse_id, product_id, qty, import_qty, import_price=0 giá vốn gác, account_debt=null).
- [x] **#3 BOM ratio** (thực chất là hệ số BOM, không phải unit conversion): SL cha = `min(exported_con/qty_needed_con) × parent.qty_needed` (số bộ hoàn chỉnh). Fallback 1:1 nếu thiếu qty_needed. **base-unit coefficient vẫn =1** (chưa tra `product_units`) — gác cùng phần giá vốn.
- [x] **Test local** (erp_hrm_check, không phải prod): PXH-34581 (con 8888 xuất 3) → PNH-12313 nhập cha 3960 **qty 1** (đúng 3 con→1 cha), `accounting_stocks`@29 qty=1, log change +1 objectable FQN ERP, phiếu warehouse_id=null. Idempotency lần 2 trả PNH-12313 không trùng/không cộng lại. Đã dọn data test.
- ⚠️ **Giá vốn = 0 (gác)**: `import_price`/`supplier_price`/`value` = 0 → tồn SỐ LƯỢNG đúng, giá vốn sai/0 (không chặn xuất; giá vốn FIFO ERP đọc `import_price` khi set sau). `account_details` (sổ hạch toán) CHƯA làm.

### Phase 2.3 — Task D: Xoá phiếu xuất hàng — CHỐT KHÔNG LÀM (2026-08-20)
- [x] User chốt (2026-08-20): **KHÔNG cho xoá phiếu xuất hàng, đúng như ERP** (ERP `ProductExportsController` không có method `destroy`). Không tạo route/controller/FE xoá.

### Checkpoint — 2026-08-17 (d) — Phase 2.2 Tồn nhập cha (auto-import) DONE + test local
Vừa hoàn thành: Phase 2.2 — tồn hàng cha khi auto-nhập-cha loại 20.
- Quyết định user: kho nhập/xuất thẳng KHÔNG cần kho vật lý → tồn ghi theo `accounting_warehouse_id`, bỏ guard #5 sai.
- 3 model tồn HRM mới + rewrite `ContractParentImportService`: BOM ratio (min bộ × parent.qty_needed) + tạo `product_import_detail_accountings` + `applyStock` (accounting_stocks/logs, objectable = FQN ERP, stock_id null, không đụng tồn vật lý).
- Điều tra ERP xác nhận: loại 21 xuất bán cha trừ tồn BẮT BUỘC qua `accounting_stocks` (không có dòng → ném exception); `product_import_direct_details` chỉ chặn khi count>0 → bỏ qua an toàn. `calculateValue` FIFO theo `import_price`, giá 0 không chặn số lượng.
- Test local OK: PXH-34581 → PNH-12313 (cha 3960 qty 1), accounting_stocks@29 qty 1, log +1, idempotent lần 2. Đã dọn.
- File (hrm-api, nhánh `hop-dong`): +3 model Warehouse (AccountingStock/AccountingStockLog/ProductImportDetailAccounting), rewrite Services/ContractParentImportService.php.
Đang làm dở: (không) — dừng sạch.
Bước tiếp theo: để E2E local FULL loop cần **loại 21 xuất bán cha TRỪ tồn** (`accounting_stocks -= qty`) — HRM PXH updateWarehouse hiện đang GÁC, là mảnh đối xứng còn thiếu. Chờ user xác nhận build tiếp.
Blocked:

## Phase 4 — Module Đề nghị xuất kho (ĐNXK) đầy đủ trong HRM — @dnsnamdang
Spec: `docs/superpowers/specs/2026-08-17-dnxk-module-design.md`. Đổi hướng từ Phase 1 (ĐNXK modal + điều hướng ERP) → **module CRUD đầy đủ giống ERP**: danh sách + chi tiết + tạo/sửa full page + hủy. Thêm nút "Xem chi tiết" cho màn YCXH. Chốt user 2026-08-17: (B) giống ERP; quyền = replicate ERP; hủy = status 3 + creator; chi tiết = full page.

### BE (hrm-api, Modules/Assign) ✅
- [x] Permissions: nhóm "Đề nghị xuất kho" (4 quyền id 1152-1155, type 27) vào `PermissionsTableSeeder.php` + insert DB erp_hrm_check + gán role 31 test.
- [x] `ContractWarehouseExportRequestController` (index scope 4 cấp + filter code/keyword/status/type/company/dept/part/employee/warehouse/contract_code/ycxh_code/date; show `data.detail`; editData; update chỉ nháp+creator; cancel status3→5 + hoàn YCXH về 2). Cờ `is_can_edit`/`is_can_cancel` = status===3 && creator && quyền "Kế toán kho" (fail-closed). Model thêm relation creator/approver + const loại 20/21 + getTypeName.
- [x] `ContractWarehouseExportRequestResource` (list + detail, type_name, status màu, warehouse_name qua leftJoin, cờ quyền; detail kèm note+products khi relationLoaded).
- [x] `ContractWarehouseExportRequestService::updateDraft` (đổi kho/note/tạo lại details/status; gửi thủ kho→YCXH 1) + `cancel` (status→5, YCXH 7→2).
- [x] `ContractExportRequestController::show` (chi tiết 1 YCXH: info + dòng hàng, `data.detail`).
- [x] Routes: group `/assign/warehouse-export-requests` (GET / , GET /{id}/edit-data, GET /{id}, PUT /{id} mw Kế toán kho, POST /{id}/cancel mw Kế toán kho) + GET `/assign/product-export-requests/{id}`. Test tinker OK (PDNXK-31053/31054, update/cancel rollback).

### FE (hrm-client, pages/finance) ✅
- [x] `warehouse-export-requests/index.vue` — danh sách ĐNXK (V2BaseFilterPanel + V2BaseDataTable, filterStateMixin key `finance_warehouse_export_requests`, action: Xem chi tiết / Sửa / Hủy). Wire menu `finance.js` placeholder "Đề nghị xuất kho" → link `/finance/warehouse-export-requests` + isShow 4 quyền.
- [x] `warehouse-export-requests/create.vue` — port từ `WarehouseExportRequestModal.vue` sang full page (vào bằng `?request_id=`), unsavedChangesMixin + markFormSaved/markFormPristine. V2BaseSelect (không phải InModal vì full page).
- [x] `warehouse-export-requests/_id/edit.vue` — form Sửa (load edit-data, PUT `apiPutMethod`), options kho từ BE đã kèm kho bị khoá; map lỗi 422 vào errorFields.
- [x] `warehouse-export-requests/_id/index.vue` — chi tiết ĐNXK (info + dòng hàng + nút Sửa/Hủy theo cờ `is_can_edit`/`is_can_cancel`).
- [x] Sửa `product-export-requests/index.vue`: nút "Lập ĐNXK" từ mở modal → `router.push('/finance/warehouse-export-requests/create?request_id='+id)`; thêm nút "Xem chi tiết" → `/finance/product-export-requests/{id}`; gỡ import + biến modal (modal cũ giờ orphan, chưa xoá file).
- [x] `product-export-requests/_id/index.vue` — chi tiết YCXH (read-only, info + dòng hàng + nút Quay lại).

### Bổ sung cột bảng hàng hoá màn chi tiết (khớp ERP) ✅
- [x] BE YCXH `ContractExportRequestController::show` — select thêm `model_name`, `brand_name`, `exported_qty`, `returned_qty` từ `product_export_request_details`.
- [x] BE ĐNXK `ContractWarehouseExportRequestResource` — products map thêm `model_name`, `brand_name` (bảng `warehouse_export_request_details` không có exported/returned).
- [x] FE `product-export-requests/_id/index.vue` — cột: STT, Mã, Tên hàng, Thương hiệu, Model, ĐVT, SL cần, Đã xuất, Đã trả.
- [x] FE `warehouse-export-requests/_id/index.vue` — cột: STT, Mã, Tên hàng, Thương hiệu, Model, ĐVT, SL xuất kho.
- [x] Cột tiền/giá vốn: CHỐT làm **đúng ERP** (2026-08-20) — form Xuất bán hàng ERP KHÔNG hiện cột giá vốn → giữ nguyên, KHÔNG thêm cột nhạy cảm. Không phát sinh việc.

### Nút Lập ĐNXK ở màn chi tiết YCXH + footer kiểu màn HĐ ✅
- [x] `product-export-requests/_id/index.vue`: thêm nút "Lập đề nghị xuất kho" (primary, `ri-store-2-line`) — điều kiện `Number(status)===2 && hasAPermission('Kế toán kho')` (fail-closed, mixin `CheckPermission`), điều hướng `create?request_id=`.
- [x] Footer cố định `.export-actionbar` (copy `.contract-actionbar` màn chi tiết HĐ): hint trái + nhóm nút phải (Quay lại light + Lập ĐNXK primary); đệm đáy trang 72px.

### Snapshot đủ trường khi tạo ĐNXK (khớp ERP) ✅
- [x] BE `ContractWarehouseExportRequestService::createFromExportRequest` — HEADER fill thêm: `customer_type`, `delivery_place`, `gara_name`, `contact_address` (snapshot từ YCXH `$req`); `department` (tên phòng ban người lập từ `$userInfo->department->name`), `employee_phone` (`$userInfo->telephone`), `employee_email` (`$userInfo->email`); `is_complete=0`, `bear_the_shipping` (`$data` nếu FE gửi, mặc định null). Legacy contract_id/service_contract_id/firm_contract_id/wr_service_contract_id để null — HRM dùng emplement_contract polymorphic.
- [x] BE detail fill thêm (helper `buildDetailAttributes` dùng chung, copy từ dòng nguồn `product_export_request_details`): `model_id`, `model_name`, `brand_id`, `brand_name`, `avatar` + pass-through link id: `service_contract_item_product_id`, `order_import_detail_id`, `inland_notify_detail_id`, `rule_inland_notify_detail_id`, `project_contract_tab_product_id`, `firm_contract_tab_product_id`, `firm_contract_tab_combo_product_id`, `wr_service_contract_item_id`.
- [x] Mirror ở `updateDraft` (dùng chung helper `buildDetailAttributes` khi tạo lại dòng hàng nháp).
- [x] Cả 2 model `$guarded = []` → không vướng mass-assignment; `php -l` service pass.

### Test E2E luồng ĐNXK (chưa làm)
- [ ] Chạy `yarn dev` (hrm-client), login TpEmployee có quyền "Kế toán kho".
- [ ] Verify render + full loop: YCXH "Chờ duyệt" → **Lập ĐNXK** → **Lưu nháp** → mở **Chi tiết** (kiểm tra cột Thương hiệu/Model/Đã xuất/Đã trả) → **Sửa** → **Gửi thủ kho** → **Hủy**.
- [ ] Kiểm tra danh sách ĐNXK: filter (code/keyword/status/type/kho/HĐ), cờ `is_can_edit`/`is_can_cancel` đúng theo status + creator + quyền.
- [ ] Kiểm tra cảnh báo unsaved-changes khi thoát form tạo/sửa lúc chưa lưu.
- [ ] Kiểm tra danh mục kho bị khoá vẫn hiện đúng ở màn Sửa (nếu ĐNXK đang chọn kho đã ngừng hoạt động).

## Phase 5 — Màn tạo YCXH đa loại + danh sách hiện đủ loại (parity ERP)

> Spec đầy đủ: `docs/superpowers/specs/2026-08-18-ycxh-full-create-design.md`
> Mục tiêu: 1 màn Tạo YCXH độc lập mô phỏng đầy đủ logic ERP (form đa hình, đủ loại createable, đủ thông tin chung), cải tiến DS hàng hoá cha/con cho HĐ mới, list hiện đủ mọi loại.
> Dropdown Tạo mới v1 = [21, 20, 3, 6, 7, 12, 18, 99]. View-only (list + chi tiết, KHÔNG tạo) = 14/15 (HĐ hãng bỏ), 16/17 (BH/SC), 4 (trả NCC). List hiện mọi type.

### 5.1 BE nền — hằng loại + mở scope list
- [x] `ContractExportRequest`: `getTypeName(int $type)` map đầy đủ (`TYPE_NAMES`) + `getCreatableTypes()` (`CREATABLE_TYPE_IDS=[21,20,3,6,7,12,18,99]` + nhãn) + `getAllTypesForFilter()` (`FILTERABLE_TYPE_IDS`).
- [x] `ContractExportRequestController@index`: bỏ khoá cứng `type=21`; mặc định trả mọi loại (giữ scope 4 cấp + ẩn nháp người khác); thêm filter `type`.
- [x] Resource list thêm field `type` + `type_name` + `is_hrm_contract` (gate link HĐ).

### 5.2 FE list — nút Tạo mới + cột Loại + filter Loại
- [x] `pages/finance/product-export-requests/index.vue`: nút "Tạo mới" (primary `ri-add-line`) → `/finance/product-export-requests/create`.
- [x] Thêm cột `Loại` (`type_name`) sau Mã phiếu.
- [x] Thêm filter `Loại` (V2BaseSelect, options `filter_types`) + link HĐ gate theo `is_hrm_contract`.
- [x] Cột "Thao tác": đổi nút chữ to (Xem/Lập ĐNXK) → icon-only `V2BaseIconButton` + tooltip (chuẩn module, gọn + mở rộng được).

### 5.3 BE tạo — endpoint đa loại
- [x] Route `POST /assign/product-export-requests` → `ContractExportRequestController@store`.
- [x] Validate cơ sở + theo type (chỉ nhánh createable, 422 nếu ngoài `CREATABLE_TYPE_IDS`); rethrow `ValidationException`.
- [x] `ContractExportRequestService::createFromRequest($data)` rẽ nhánh: 20/21 (`createFromContract`), manual (`createManual` 3/6/12/18/99), transfer 7 (`createFromTransfer` → hiện delegate `createManual`).
- [x] `GET /assign/product-export-requests/create-data?type=&emplement_contract_id=` — kho xuất + dòng HĐ cha/con + `exported_qty` động (`contractProductLines`), fail-closed không trả cost_price/estimated_price.

### 5.4 FE tạo — khung full page
- [x] `pages/finance/product-export-requests/create.vue`: card Thông tin chung + selector Loại (creatable) + trường ẩn/hiện theo type (HĐ/kho/kho nhập/ngày mượn-trả/khách hàng) + footer (Quay lại/Lưu nháp status 3/Gửi duyệt status 2).
- [x] Validate inline (`errorFields`/`errorMsg`, map 422 BE) + `unsavedChangesMixin` + `markFormSaved()`.

### 5.5 FE tạo — bảng HĐ cha/con (cải tiến) cho 20/21
- [x] Bảng phân cấp `contractDisplayLines` (cha → con); cột Đã xuất/Còn lại/SL xuất; 21=cha editable/con read-only, 20=cha header/con editable; checkbox chọn dòng + validate SL ≤ còn lại.

### 5.6 FE tạo — biến thể nhập tay + chuyển kho (3/6/12/18/99/7)
- [x] Bảng nhập tay + modal `QuotationProductSearchModal` (goodsOnly, `@apply` map row); type 7 dùng chung nhập tay (BE `createFromTransfer` delegate `createManual`).
- [ ] (Nâng cấp sau) biến thể chuyển kho read-only load thẳng từ `ProductTransferRequest` (hiện nhập tay là đủ dùng).

### 5.7 show đa loại + verify list
- [x] `ContractExportRequestController@show` dùng chung Resource → render mọi loại (type_name, dòng phẳng); màn chi tiết `_id/index.vue` thêm "Loại phiếu" + gate link HĐ theo `is_hrm_contract`.
- [ ] Verify list hiện đủ loại trên browser (kể cả 14/15 view-only từ data cũ) — gộp vào 5.8.

### 5.8 E2E trên browser
- [ ] Tạo thử từng loại createable; verify list + chi tiết + view-only 14/15.

### Checkpoint — 2026-08-18 (b) — Hoàn thành BE+FE Phase 5 (5.1–5.7), chờ E2E
Vừa hoàn thành:
- BE: `ContractExportRequest` hằng loại (`TYPE_NAMES`/`CREATABLE_TYPE_IDS`/`FILTERABLE_TYPE_IDS` + 3 hàm), controller mở scope list + filter `type` + `typeOptions`/`createData`/`contractProductLines`/`store`, service `createFromRequest`/`createManual`/`insertManualLines`/`createFromTransfer`(stub→manual), Resource + routes. `php -l` sạch cả 4 file.
- FE list: nút Tạo mới + cột Loại + filter Loại + gate link HĐ `is_hrm_contract`.
- FE tạo: `pages/finance/product-export-requests/create.vue` full page đa loại — selector Loại, thông tin chung ẩn/hiện theo type, bảng HĐ cha/con (Đã xuất/Còn lại/SL xuất, 21=cha/20=con), bảng nhập tay qua `QuotationProductSearchModal`, footer Lưu nháp(3)/Gửi duyệt(2), `unsavedChangesMixin`+`markFormSaved()`.
- FE chi tiết `_id/index.vue`: thêm "Loại phiếu" + gate link HĐ `is_hrm_contract`.
Đang làm dở: (trống) — code xong, chưa chạy browser.
Bước tiếp theo: 5.8 E2E — `yarn dev` hrm-client, login quyền "Kế toán kho", tạo thử từng loại createable (21/20/3/6/7/12/18/99), verify list hiện đủ loại + chi tiết + xác nhận không tạo được HĐ hãng (14/15).
Blocked:
Bước tiếp theo: `getTypeName`/`getCreatableTypes`/`getAllTypesForFilter` trong `ContractExportRequest` + mở scope `index`.
Blocked:

### Checkpoint — 2026-08-17 (e) — Bổ sung cột bảng hàng hoá màn chi tiết
Vừa hoàn thành: thêm Thương hiệu + Model cho cả 2 màn chi tiết; YCXH thêm Đã xuất/Đã trả. BE + FE đều xong.
Đang làm dở: (không).
Bước tiếp theo: user xác nhận có cần nhóm cột tiền (giá/VAT) — nếu có sẽ gate quyền rồi thêm.
Blocked:

### Checkpoint — 2026-08-17 (d) — Hoàn thành FE module ĐNXK
Vừa hoàn thành: toàn bộ 6 màn/thao tác FE (danh sách + tạo + sửa + 2 chi tiết + sửa màn YCXH) + wire menu. BE Phase 4 đã xong từ checkpoint trước.
Đang làm dở: (không).
Bước tiếp theo: (1) chạy `yarn dev` kiểm tra render + luồng thật trên trình duyệt (login TpEmployee có quyền "Kế toán kho"); (2) cân nhắc xoá file `WarehouseExportRequestModal.vue` (đã orphan); (3) verify E2E: YCXH "Chờ duyệt" → Lập ĐNXK → Lưu nháp → Sửa → Gửi thủ kho → Hủy.
Blocked:

### Checkpoint — 2026-08-17 (c) — Vá gap #4 + #5 auto-nhập cha
Vừa hoàn thành: 
- #4 idempotency: migration `source_export_id` + guard đầu `createParentImport` + set khi tạo (test stub OK, không tạo trùng).
- #5 kho null: throw ValidationException rollback PXH (test PXH-34581 OK). Phát hiện 4 kho nhập thẳng trong erp_hrm_check đều thiếu `warehouse_id`.
- File sửa (hrm-api, nhánh `hop-dong`): `Modules/Assign/Services/ContractParentImportService.php` + `database/migrations/2026_08_17_000001_add_source_export_id_to_product_imports_table.php`.
Đang làm dở: (không) — dừng sạch, data test đã dọn, kho khôi phục NULL.
Bước tiếp theo: (1) user xác nhận nghiệp vụ kho nhập thẳng có `warehouse_id` hay không (ảnh hưởng #5 + phase tồn); (2) #3 + phần tồn/hạch toán (updateWarehouse cha) khi làm phase hạch toán; (3) Phase 3 verify E2E môi trường thật.
Blocked:

## Phase 6 — Sửa / Chi tiết / Hủy / Xóa YCXH + refactor form dùng chung (A')

> Spec đầy đủ: `docs/superpowers/specs/2026-08-18-ycxh-edit-detail-design.md`
> Chốt brainstorm 2026-08-18: (1) kiến trúc A' — component form chung Create+Edit, Chi tiết giữ riêng; (2) điều kiện Sửa/Hủy/Xóa bám ERP: `status==3 && creator`; (3) Sửa hết trừ Loại; (4) endpoint Sửa dùng `PUT /{id}`; (5) làm cả Hủy (status→6 giữ record) và Xóa (xóa hẳn).

### 6.1 BE — cờ quyền + endpoint ✅
- [x] `ContractExportRequestResource` thêm `is_can_edit`/`is_can_cancel`/`is_can_delete` — gọi thẳng `canEdit/canCancel/canDelete` trên model (single-source, fail-closed). Cờ dùng chung list + chi tiết.
- [x] Model `ContractExportRequest`: thêm `isContractType()`, `canEdit()` (status==3 & creator & type!=8), `canCancel()`, `canDelete()` (status==3 & creator).
- [x] Route `PUT /{id}` → `update`, `POST /{id}/cancel` → `cancel`, `DELETE /{id}` → `destroy`, `GET /{id}/edit-data` → `editData` (không gắn checkPermission — bám store, điều kiện enforce qua can* trong controller). GET `/{id}` đặt cuối group.
- [x] `editData($id)`: guard `canEdit()` (403) → trả `detail` prefill (thông tin chung theo loại; 20/21 kèm `product_lines` cha/con (loại trừ chính phiếu) + `selected_lines` {contract_product_id⇒qty}; nhập tay trả `products` phẳng). KHÔNG trả cost/estimated_price.
- [x] `rulesForType($type,$isUpdate)`: tách rule dùng chung store+update; update KHÔNG nhận `type`/`emplement_contract_id` (lấy từ record).
- [x] `update($id)`: `find` (404) → chặn `!canEdit()` (403) → `type` từ record → validate `rulesForType($type,true)` → `service->updateFromRequest` (set status + deleteLines + ghi lại dòng) → trả {id,code}. Rethrow `ValidationException`. (send() bỏ — parity create: chỉ set status.)
- [x] `cancel($id)`: chặn `!canCancel()` (403) → `status=6, is_completed=true`, giữ record → trả {id,status}.
- [x] `destroy($id)`: chặn `!canDelete()` (403) → `service->deleteCompletely`: loại 7 gỡ liên kết `product_transfer_requests.product_export_request_id=null` (guard `Schema::hasColumn`, no-op vì transfer chưa wire link), xóa dòng con (tab_products/tabs/details) + file (bảng `files` chung) → `$req->delete()` → trả {id}.
- [x] Service: `writeContractLines` (tách từ `createFromContract` dùng chung), `deleteLines`, `updateFromRequest`, `deleteCompletely`. `php -l` cả 5 file BE: pass.

### 6.2 FE — refactor component form chung ✅
- [x] Tạo `components/ProductExportRequestForm.vue`: bê toàn bộ thân form từ `create.vue` (card thông tin chung, selector Loại, trường ẩn/hiện theo type, bảng cha/con 20/21, bảng nhập tay + QuotationProductSearchModal, validate inline). Props `mode`/`initialData`/`submitting`; emit `@submit(payload,status)`, `@back`, `@ready`. Expose `snapshotSource()` + `applyServerErrors(resp)` cho page cha.
- [x] Khác biệt mode: create=selector Loại/HĐ chọn được / edit=khoá (input readonly hiện `type_name`/`emplement_contract_code`); `applyInitialData()` đổ form từ detail; edit bảng 20/21 dùng `buildContractLines(lines, selected_lines)` tick sẵn + đổ SL cũ, quỹ Còn lại đã cộng lại SL phiếu (BE loại trừ chính phiếu); `mergeOption()` merge kho/khách hàng/HĐ đã khoá đang chọn vào options.
- [x] BE `editData` bổ sung `warehouse_name`/`import_warehouse_name` (join `warehouses` kể cả kho khoá) để FE merge — convention danh mục khoá.
- [x] `unsavedChangesMixin` giữ ở page-level (create.vue) vì `beforeRouteLeave` chỉ chạy ở route component; `unsavedSnapshotSource()` đọc `$refs.form.snapshotSource()`; `markFormPristine()` khi `@ready`, `markFormSaved()` sau khi lưu.
- [x] Refactor `create.vue` thành wrapper mỏng: `mode="create"`, `onSubmit` → `POST /assign/product-export-requests` → redirect chi tiết. Template compile sạch (vue-template-compiler).

### 6.3 FE — màn Sửa + Chi tiết + List ✅
- [x] `_id/edit.vue` (mới): `GET /{id}/edit-data` (403 → toast + về chi tiết) → render form `mode="edit"`; `onSubmit` → `PUT /{id}` → `markFormSaved()` → redirect chi tiết.
- [x] `_id/index.vue`: thêm footer nút Sửa (`is_can_edit` → /edit), Hủy (`primary status="danger"`, `is_can_cancel` → confirm `$bvModal.msgBoxConfirm` → POST /cancel → reload), Xóa (`primary status="danger"`, `is_can_delete` → confirm → DELETE → về list). Giữ Lập ĐNXK. `processing` chặn double-click.
- [x] `index.vue` (list): cột Thao tác thêm icon Sửa (`ri-edit-line`)/Hủy (`danger` `ri-close-circle-line`)/Xóa (`danger` `ri-delete-bin-line`); gate cờ BE; methods `goEdit`/`cancelRow`/`deleteRow`/`confirmAction` → reload list sau thao tác.
- [x] Compile sạch cả 5 file FE (vue-template-compiler).

### 6.4 E2E
- [ ] Tạo phiếu nháp (status 3) → Sửa (đổi dòng hàng, khóa Loại) → Lưu nháp → Sửa lần 2 → Gửi duyệt; verify sau khi gửi duyệt (status 2) mất nút Sửa/Hủy/Xóa.
- [ ] Hủy phiếu nháp → status 6, record vẫn còn. Xóa phiếu nháp khác → record biến mất; loại 7 → ProductTransferRequest được chọn lại.
- [ ] Verify chỉ creator thấy nút; user khác chỉ xem. Verify quỹ cha-con 20/21 loại trừ chính phiếu khi sửa.

## Phase 7 — Thiết kế lại giao diện màn Thêm / Sửa / Chi tiết YCXH (UI-only, không đụng logic)

> Chuẩn style: bám màn Chi tiết hợp đồng (`pages/assign/contracts/_id/index.vue`) — hệ `.c-section` + `.section-header` (icon trong ô bo tròn màu + tiêu đề, card bo 12px, shadow nhẹ) + `.fld-grid`/`.ro-value`.
> Endpoint `assign/contracts?keyword=` đã trả `code/customer_name/sign_date/total_after_vat` → KHÔNG cần sửa BE.

### 7.1 ContractSearchModal (mới)
- [x] Tạo `components/ContractSearchModal.vue` (clone pattern `ContractQuotationSearchModal`): ô search mã HĐ / tên KH (debounce 300ms) → `GET assign/contracts?keyword=`; bảng cột **Mã HĐ · Khách hàng · Ngày ký · Giá trị HĐ (sau VAT)**; click dòng → `@select(contract)` + `@close`. Header icon-ô-màu, footer nút Đóng (`tertiary`).

### 7.2 Form Thêm/Sửa (`ProductExportRequestForm.vue`)
- [x] Thay 2 `.card`/`.card-header` bằng `.c-section`/`.section-header` (icon+màu tự chọn: Thông tin chung = tím, Chi tiết hàng hoá = cam). Nút "Thêm hàng hoá" đẩy `ml-auto` trong header.
- [x] Thông tin chung: bố cục lại bằng `.fld-grid` (nhãn nhỏ trên, input dưới) 3 cột; khối thông tin KH → callout `.cust-callout` thay dòng `hr`+text.
- [x] Chọn hợp đồng: create → ô read-only hiển thị HĐ đã chọn + nút "Chọn" mở `ContractSearchModal`; edit → giữ khoá (ro-value). Bỏ `V2BaseSelect` + `fetchContracts` dropdown (giữ `mergeOption` cho kho khoá; HĐ khoá hiện qua label lưu sẵn).
- [x] Giữ nguyên 100% logic: validate, buildProducts, payload, snapshotSource, applyServerErrors, bảng cha/con 20/21, footer.

### 7.3 Màn Chi tiết (`_id/index.vue`)
- [x] Đổi 2 `.card` sang `.c-section`/`.section-header` (Thông tin chung = tím, Danh sách hàng hoá = cam); grid label-value → `.fld-grid`/`.ro-value` (+ `.fld-label`). Giữ nguyên footer nút + logic.

### 7.4 Verify
- [x] Compile sạch (vue-template-compiler) cả 4 file (form + modal + detail + list). Style scoped `.c-section`/`.section-header`/`.fld-grid`/`.ro-value` đã copy vào từng file.

### 7.5 Tinh chỉnh
- [x] Chuyển ô Ghi chú lên khối "Thông tin chung" (thay vì nằm cuối khối "Chi tiết hàng hoá") ở form Tạo/Sửa.

### Checkpoint — 2026-08-18 (c) — Chốt design Phase 6 (Sửa/Chi tiết/Hủy/Xóa)
Vừa hoàn thành: brainstorm + spec `2026-08-18-ycxh-edit-detail-design.md`; đào điều kiện ERP (`canEdit/canCancel/canDelete` = status==3 & creator; update sửa hết trừ Loại + syncProducts delete-insert; cancel set status 6 giữ record; destroy deleteCompletely xóa hẳn + gỡ ProductTransferRequest loại 7). User chốt: A', bám ERP, PUT, làm cả Hủy+Xóa.
Đang làm dở: (chưa code) — chờ user review spec trước khi implement.
Bước tiếp theo: 6.1 BE — thêm cờ quyền vào Resource + routes update/cancel/destroy/edit-data.
Blocked:

## Phase 8 — Bổ sung trường ERP cho loại 21 (Xuất bán hợp đồng) + File đính kèm + redesign Thông tin chung

> User (2026-08-18) chốt scope: **A** (thông tin KH readonly auto-fill từ HĐ) + **B** (Xuất thẳng, Cần lắp đặt, Vận chuyển, Số km dự kiến) + **File đính kèm**. BỎ hẳn Nhóm VAT / Nhóm hàng hóa (nhóm C). 2 field ERP không có nguồn trong `hrm_contracts` (Tên viết tắt `customer_short_name`, Địa chỉ giao hàng `delivery_place`) → KHÔNG hiển thị.
> Đối chiếu màn ERP "Xuất bán hãng" (type 14) — spec chi tiết trong summary agent. Bảng `product_export_requests` (dùng chung ERP) đã có sẵn cột: `is_export_direct`, `need_repair`, `transition_type`, `total_km_expected`, `identity_card_number`, `attachments` → KHÔNG migration.
> File đính kèm: bảng `files` chung (`table='product_export_requests'`, `table_id`) — tái dùng `CmcS3Helper::putFile` + `TableFileHelper::createForTable` (copy pattern `ContractController::uploadAttachments/deleteAttachment`). Endpoint riêng, upload sau khi lưu (giống HĐ).
> Vận chuyển options (hằng): 1=NV vận chuyển · 2=Công ty vận chuyển · 3=KH vận chuyển. Số km bắt buộc khi transition_type=2.

### 8.1 BE — DONE ✅
- [x] `createData` (20/21): mở rộng object `contract` → trả thêm `customer_tax_code`, `customer_contact_name`, `customer_contact_phone`, `customer_address` (từ Contract) + `transition_types[]` (hằng).
- [x] `rulesForType($type,$isUpdate)` — contract types (20/21): `is_export_direct` (nullable boolean), `need_repair` (in:0,1), `transition_type` (in:1,2,3), `total_km_expected` (nullable numeric, `required_if:transition_type,2`).
- [x] `ContractExportRequestService::createFromContract`: lưu 4 field B, snapshot `identity_card_number = contract->customer_tax_code`, `warehouse_id=null` khi xuất thẳng.
- [x] `updateFromRequest` (contract types): cập nhật 4 field B + warehouse_id=null khi xuất thẳng.
- [x] `editData`: trả thêm 4 field B + customer display (tax_code/contact_name/contact_phone/address) + `files[]` (id/name/file_name/file_path/file_type/file_size).
- [x] `show`: bổ sung 4 field B + `transition_type_name` + customer fields + `files[]` vào detail.
- [x] Entity `ContractExportRequest`: thêm `files()` + `TRANSITION_TYPES` const + `getTransitionName()`.
- [x] Controller: `uploadAttachments($id)` + `deleteAttachment($id,$fileId)` (guard `canEdit()`). Routes: `POST /{id}/attachments`, `DELETE /{id}/attachments/{fileId}` (trước `/{id}` GET).
- [x] `php -l` sạch (controller/service/entity/routes) + xác nhận 8 cột DB tồn tại (erp_hrm_check).

### 8.2 FE — form (`ProductExportRequestForm.vue`) — DONE ✅
- [x] Redesign "Thông tin chung" 2 cột gọn đẹp. Contract types (20/21): thêm khối KH readonly (grid) + 4 field B (Xuất thẳng checkbox, Cần lắp đặt radio Có/Không, Vận chuyển select, Số km number).
- [x] Ẩn/hiện: Kho xuất ẩn khi `is_export_direct`; Vận chuyển hiện khi `!is_export_direct`; Số km hiện khi `transition_type==2`.
- [x] File đính kèm (mọi loại): create → stage `pendingFiles[]`; edit → `existingFiles[]` (xoá gọi DELETE ngay) + thêm mới stage. Method `uploadPendingFiles(id)` build FormData → `apiPostMethod` multipart, page cha gọi sau khi lưu thành công.
- [x] Cập nhật `form` (thêm 4 field B), `onTypeChange` reset, `applyInitialData` đổ field B + existingFiles, `onSubmitClick` payload thêm field B, `validateForm` (Số km khi transition_type=2), `snapshotSource` gồm field B + pendingFiles.
- [x] Page cha `create.vue`/`edit.vue`: sau `apiPost/PutMethod` thành công → `await $refs.form.uploadPendingFiles(id)` trước redirect.

### 8.3 FE — chi tiết (`_id/index.vue`) — DONE ✅
- [x] Hiện các field mới (Xuất thẳng/Cần lắp đặt/Vận chuyển/Số km) + block KH đầy đủ + danh sách file đính kèm (link tải). CSS `.attach-list/.attach-item/.attach-ico/.attach-name/.ro-empty` đã bổ sung.

### 8.4 Verify — DONE ✅
- [x] Compile sạch (vue-template-compiler) form + create + edit + detail (cả 4 file ✅).
- [x] `php -l` sạch lại BE (controller/service/routes/entity).

### Checkpoint — 2026-08-18 (d) — Hoàn thành Phase 8 (BE + FE + verify)
Vừa hoàn thành: Phase 8 trọn vẹn — BE (8.1) + FE form/create/edit (8.2) + FE chi tiết (8.3) + verify compile & lint (8.4). Đã bỏ dead-code `methods:{Number}` trùng key ở `_id/index.vue`, thay bằng `Number()` inline (Vue 2 whitelist) + bổ sung CSS attach list.
Đang làm dở: (không có)
Bước tiếp theo: E2E browser test toàn luồng loại 21 — tạo YCXH có file đính kèm + 4 field B → chi tiết → sửa → lập ĐNXK (task 6.4 deferred).
Blocked:

### 8.5 Fix UI/UX form Thông tin chung (2026-08-18)
- [x] Siết khoảng cách trường trong "Thông tin chung" (section-body padding, fld-grid gap 12→8, ro-value min-height 34→30, mt-3 giữa nhóm →10px, ro-panel + switch/radio nhỏ lại). Giữ full-width (đã thử max-width 1180 rồi bỏ theo yêu cầu).
- [x] **Fix nút "Lưu nháp" không phản ứng**: `validateForm()` chặn draft y như gửi duyệt → `return false` im lặng (lỗi products hiện tít dưới bảng). Sửa: `validateForm(status)` — draft (status=3) chỉ bắt buộc **Loại** (+ **Hợp đồng** với loại 20/21), bỏ chặn kho/khách/km/products. `onSubmitClick` truyền `status`.
- [x] BE `rulesForType($type,$isUpdate,$status=2)`: draft (status=3) → `products` nullable, bỏ required kho/customer/import/km/contract_product_id; giữ `emplement_contract_id` required cho loại HĐ (tránh `findOrFail` vỡ). store/update truyền `status`. `php -l` sạch + vue compile sạch.

### Checkpoint — 2026-08-18 (e) — Compact UI + fix Lưu nháp
Vừa hoàn thành: 8.5 — siết layout Thông tin chung + fix nút Lưu nháp (FE `validateForm(status)` + BE `rulesForType` nới theo status draft/submit).
Đang làm dở: (không có)
Bước tiếp theo: E2E test — tạo nháp chỉ chọn Loại/HĐ → lưu nháp OK; gửi duyệt vẫn chặn đủ trường.
Blocked:

### 8.6 Bắt buộc trường Vận chuyển (transition_type) khi Gửi duyệt — khớp ERP (2026-08-18)
- [x] Kiểm chứng ERP: `ProductExportRequestsController::store` áp rule `transition_type => required|in:1,2,3` khi `!is_export_direct && in_array($type, getHasDeliveryTypes())`; km required khi transition=2 (`CONG_TY_VAN_CHUYEN`). Loại 14 (XUAT_BAN_HD_HANG — tương đương loại 21 HRM) NẰM TRONG `getHasDeliveryTypes()` → ERP CÓ bắt buộc.
- [x] FE `validateForm`: khi Gửi duyệt (status≠3) + loại HĐ + KHÔNG xuất thẳng (`is_export_direct !== 1`) → bắt buộc `transition_type` (lỗi inline `errorFields.transition_type`); km vẫn required khi transition=2. Label "Vận chuyển" gắn `:required="form.is_export_direct !== 1"`.
- [x] BE `rulesForType` nhánh submit HĐ: `transition_type => required_unless:is_export_direct,1|nullable|in:1,2,3`. Nháp (status=3) vẫn nới (service fallback về 1 cho cột NOT NULL). `php -l` + vue compile sạch.

### Checkpoint — 2026-08-18 (f) — transition_type required khi gửi duyệt
Vừa hoàn thành: 8.6 — bắt buộc Vận chuyển khi Gửi duyệt + không xuất thẳng (khớp ERP), FE + BE.
Đang làm dở: (không có)
Bước tiếp theo: E2E — gửi duyệt bỏ trống Vận chuyển (không xuất thẳng) phải chặn; tick Xuất thẳng thì bỏ chặn.
Blocked:

### 8.7 Bảng hàng hoá chi tiết mặc định tick hết khi tạo mới (2026-08-18)
- [x] `buildContractLines`: tạo mới (không selectedMap) → `_checked = selectable && remaining_qty > 0` (loại 21 tick cha, loại 20 tick con); màn Sửa giữ `!!picked`. SL xuất vẫn điền sẵn = Còn lại. Vue compile sạch.

### 8.9 Fix chi tiết DS hàng hoá thiếu Thương hiệu/Model/ĐVT (2026-08-18)
- [x] `writeContractLines` (service) chỉ ghi `product_name/code` vào `product_export_request_details`, bỏ sót `model_name/brand_name/unit_name`. Sửa: tra tên từ `units`/`product_models`/`brands` theo `unit_id/model_id/brand_id` của dòng HĐ rồi ghi kèm. Áp cả tạo mới + sửa (dùng chung hàm). `php -l` sạch.
- [ ] Lưu ý: phiếu HĐ đã tạo TRƯỚC fix vẫn thiếu tên (data cũ) → cần mở Sửa → lưu lại để backfill, hoặc tạo phiếu mới.
- [x] Backfill riêng phiếu test 35676 (UPDATE details JOIN tab_products→hrm_contract_product_prices→units/product_models/brands). Kết quả: ĐVT=Hộp, Model=TBTE-0x, Thương hiệu=TAITEC. Phiếu cũ khác chưa backfill (chờ user xác nhận có chạy toàn bộ không).

### 8.8 Thiết kế lại + gom gọn màn Chi tiết (`_id/index.vue`) (2026-08-18)
- [x] Bỏ ô viền từng trường (`.ro-value`), chuyển sang key–value inline gọn (`.kv-grid`/`.kv`: nhãn trái 96px + giá trị phải, gạch mờ phân cách, padding 5px).
- [x] Gom KH + thông tin xuất bán vào 1 panel phụ `.subpanel` (nền xám, tiêu đề "Khách hàng & xuất bán") thay 2 lưới rời.
- [x] File đính kèm dạng chip bo tròn wrap ngang; Ghi chú khối nền nhạt; rút gọn nhãn "TG nhận/duyệt". Responsive 3→2→1 cột. Vue compile sạch.

### 8.10 Box thông tin thanh toán DS hàng hoá — khớp logic ERP (2026-08-18)
- [x] Kiểm chứng ERP (subagent): logic ở `ProductExportRequestDetail.blade.php` (getter từng dòng) + `ProductExportRequest.blade.php` (5 tổng), hiển thị khi `type != 2 && type != 15`. Công thức: Giá bán = `price + extra_price`; Thành tiền bán = qty×giá bán; Đơn giá sau giảm = `allocated_price`; Thành tiền sau giảm = qty×đơn giá sau giảm; Tiền VAT = `round(TT sau giảm × vat%/100)`; TT sau VAT = TT sau giảm + Tiền VAT; Giảm giá = (giá bán − đơn giá sau giảm)×qty.
- [x] BE `writeContractLines` (service): ghi thêm `extra_price`, `allocated_price` (=unit_price_after_discount), `total_amount` (=qty×giá bán) vào `product_export_request_details`. `php -l` sạch.
- [x] BE line-display API (`product-lines`) select+map trả `quoted_price/extra_price/unit_price_after_discount/vat_percent`; `show` endpoint trả `price/extra_price/allocated_price/vat_percent` trong products.
- [x] FE form (`ProductExportRequestForm.vue`): chỉ loại 21 (Xuất bán HĐ) — thêm 8 cột giá/dòng + box 5 dòng tổng (`paymentSummary` computed trên dòng đang tick hợp lệ, `priceOf`/`linePrice` helper). Vue compile sạch.
- [x] FE chi tiết (`_id/index.vue`): loại 21 — thêm 8 cột giá/dòng + box 5 dòng tổng (`isSaleDetail`/`paymentSummary`/`rowPrice`). Vue compile sạch.
- [ ] Lưu ý: phiếu loại 21 tạo TRƯỚC fix chưa có `extra_price/allocated_price/total_amount` trong details → cột giá chi tiết = 0 tới khi mở Sửa → lưu lại (hoặc backfill).

### Checkpoint — 2026-08-18 (g) — Box thanh toán khớp ERP (form + chi tiết)
Vừa hoàn thành: 8.10 — box thông tin thanh toán + cột giá/dòng cho loại 21, cả màn Thêm/Sửa lẫn Chi tiết, logic khớp ERP; BE persist thêm extra_price/allocated_price/total_amount.
Đang làm dở: (không có)
Bước tiếp theo: E2E — tạo/sửa phiếu loại 21, đối chiếu 5 tổng với ERP; cân nhắc backfill giá cho phiếu cũ.
Blocked:

### 9.1 Thiết kế lại + bổ sung cột màn Đề nghị xuất kho (ĐNXK) — 2026-08-18
- [x] Khảo sát ERP (WarehouseExportRequest): đối chiếu field form + cột bảng hàng hoá màn Tạo/Sửa/Chi tiết → xác định HRM thiếu gì (Explore subagent).
- [x] BE: bổ sung field còn thiếu — `warehouseExportData` (create) + `editData` products thêm `model_name`/`brand_name`; create source thêm `delivery_place`; editData request thêm customer_mobile/customer_contact_name/customer_contact_phone/customer_address/delivery_place/bear_the_shipping; Resource `show` thêm customer_mobile/customer_address/customer_contact_name/customer_contact_phone/delivery_place/bear_the_shipping/comment; accept+persist `bear_the_shipping` khi create (sẵn có) + update (mới).
- [x] FE `create.vue`: thiết kế lại gọn (kv-grid/subpanel giống YCXH) — card "Thông tin chung" + panel "Khách hàng & giao hàng" (KH/SĐT/người liên hệ+phone/địa chỉ/địa chỉ giao); bổ sung cột hàng hoá Thương hiệu + Model; checkbox "KD chịu vận chuyển" + gửi trong payload; footer `.export-actionbar` cố định.
- [x] FE `_id/edit.vue`: đồng bộ layout + cột + checkbox bear_the_shipping (load từ edit-data, gửi khi PUT) với create.
- [x] FE `_id/index.vue`: thiết kế lại gọn (kv-grid + badge trạng thái header) + panel Khách hàng & giao hàng + KD chịu ship + card "Ghi chú duyệt" (comment); giữ cột Thương hiệu/Model.
- [x] Verify: `php -l` (4 file BE) + vue compile (3 file FE) sạch.

**GÁC LẠI (báo user chốt trước khi làm — cần đụng tồn kho/nghiệp vụ nặng):**
- Cột **Tồn kho / SL được xuất** + **SL đang giữ (prepick)** trong bảng hàng hoá (ERP có) — cần query tồn + prepick_logs theo kho, rủi ro cao, chưa port sang HRM.
- Cột **Đơn giá + Thành tiền** ở màn Chi tiết (ERP show có) — bảng `warehouse_export_request_details` HRM chưa có cột giá; cần bổ sung cột + snapshot giá lúc tạo.
- **File đính kèm** (ERP cho upload ở form ĐNXK) — chưa wire bảng `files` cho ĐNXK.
- **Kho nhập** (điều chuyển nội bộ) + **xuất ghép/tách** — ngoài scope loại 20/21 hiện tại.

### Checkpoint — 2026-08-18 (h) — Redesign + bổ sung cột 3 màn ĐNXK
Vừa hoàn thành: Task 9.1 — BE bổ sung field (4 file: ContractWarehouseExportRequestController editData/update, ContractExportRequestController warehouseExportData/store, ContractWarehouseExportRequestService updateDraft, ContractWarehouseExportRequestResource) + FE redesign gọn 3 màn (create.vue / _id/edit.vue / _id/index.vue) theo kv-grid/subpanel giống YCXH, thêm cột Thương hiệu/Model, checkbox KD chịu vận chuyển, panel KH & giao hàng, card Ghi chú duyệt. php -l + vue compile sạch.
Đang làm dở: —
Bước tiếp theo: Báo user chốt 4 hạng mục GÁC LẠI (tồn kho/SL giữ, đơn giá/thành tiền chi tiết, file đính kèm, kho nhập/ghép-tách); rồi E2E browser toàn luồng loại 21 (task 6.4).
Blocked: [để trống]

### Checkpoint — 2026-08-18 (i) — Đồng bộ card header + đưa Ghi chú lên Thông tin chung
Vừa hoàn thành: Theo phản hồi user — 3 màn ĐNXK (create/_id/edit/_id/index) đổi từ bootstrap `.card` + `.card-header` sang `.c-section` + `.section-header` (icon chip xanh/đỏ) giống màn YCXH; đưa trường Ghi chú (textarea ở form, kv-note ở chi tiết) + Ghi chú duyệt lên trong section "Thông tin chung"; badge trạng thái → `.status-pill` ở góc phải section-header màn chi tiết. Copy nguyên hệ CSS (kv-grid/kv--block/subpanel) từ YCXH. vue compile sạch cả 3.
Đang làm dở: —
Bước tiếp theo: như checkpoint (h) — chốt 4 hạng mục GÁC LẠI + E2E loại 21.
Blocked: [để trống]

### 9.2 Bổ sung 3 hạng mục ERP còn thiếu (user chốt 2026-08-19) — @dnsnamdang
User chốt: làm #1 (SL được xuất + SL đang giữ), #2 (Đơn giá + Thành tiền — tìm nguồn ERP, 2 bên chung bảng ERP nên "có hoặc lấy ra được"), #3 (File đính kèm). #4 (xuất ghép/tách) → brainstorm sau.
- [x] Khảo sát ERP tỉ mỉ: (a) #1 tồn = port `Product::getAccountingStockDetail` (nhánh xuất thường); (b) #2 giá lấy từ `product_export_request_details.price` (+ `extra_price` nếu HĐ hãng) — bảng ĐNXK detail KHÔNG có cột giá; (c) #3 dùng bảng `files` chung (table='warehouse_export_requests') như YCXH.
- [x] #1 BE: tạo `ContractStockService::getLineStocks` (port ERP getAccountingStockDetail, bỏ import_direct) + endpoint `POST /assign/warehouse-export-requests/stock-of-products` (nhận warehouse_id + product_export_request_id + except_id + products[]; company/employee/customer lấy từ YCXH nguồn; gate quyền "Kế toán kho"). **Lệch plan**: KHÔNG nhúng vào warehouseExportData/editData mà tách endpoint riêng — vì tồn phụ thuộc kho user chọn (đổi sau khi load form) nên phải gọi lại mỗi lần đổi kho.
- [x] #1 FE: thêm cột "SL được xuất" (available_export_qty) + "SL đang giữ" (hold_prepick_qty) vào create.vue + edit.vue; watcher `form.warehouse_id` → fetchStock (edit nạp sẵn khi load nếu đã có kho); chống race bằng stockReqSeq.
- [x] #2 BE: `attachSourcePrices()` trong controller `show` — join `product_export_request_details` theo product_id + link ids (fallback product_id), gắn `price`/`total_amount` vào từng dòng; Resource trả thêm `price`, `total_amount`, `sum_amount`.
- [x] #2 FE: thêm cột Đơn giá + Thành tiền + dòng "Tổng thành tiền" vào _id/index.vue.
- [x] #3 BE: quan hệ `files()` (bảng `files`, table='warehouse_export_requests') + `uploadAttachments`/`deleteAttachment` (gate assertCanEdit, S3 folder 'warehouse_export_request_attachment', TableFileHelper); Resource + editData trả `files`; routes tĩnh đặt trước `/{id}`.
- [x] #3 FE: create.vue giữ file trong RAM → upload sau khi tạo có id; edit.vue upload/xoá ngay (đã có id) + list download; _id/index.vue hiển thị list download read-only.
- [x] Verify: `php -l` 5 file BE + vue compile 3 file — sạch. Cột DB đã đối chiếu trên `erp_hrm_check`.
- [ ] #4 (xuất ghép / xuất tách) — brainstorm sau (user defer).

### Checkpoint — 2026-08-19 — Hoàn thành 9.2 (#1 tồn, #2 giá, #3 file đính kèm)
Vừa hoàn thành: 3/4 hạng mục ERP-parity ĐNXK.
- BE: `ContractStockService.php` (mới, port getAccountingStockDetail); controller thêm `stockOfProducts` + `uploadAttachments` + `deleteAttachment` + `attachSourcePrices` (gọi trong show), editData trả `files`; `ContractWarehouseExportRequest` thêm `files()` + `use App\Models\File`; Resource thêm price/total_amount/sum_amount + files; api.php thêm 3 route (stock-of-products + 2 attachments) đặt trước `/{id}`.
- FE: create.vue (2 cột tồn + watcher fetchStock + upload file hoãn tới sau tạo), _id/edit.vue (2 cột tồn + fetchStock kèm except_id + upload/xoá file ngay), _id/index.vue (cột Đơn giá/Thành tiền + dòng tổng + list file download).
Đang làm dở: (không) — đã verify php -l + vue compile sạch, đối chiếu cột DB trên erp_hrm_check.
Bước tiếp theo: E2E test trên trình duyệt loop type-21 đầy đủ (đổi kho → xem tồn, upload/xoá file, xem chi tiết giá); rồi brainstorm #4 xuất ghép/tách.
Blocked:

### 9.3 Đổi tên controller khớp ERP (user yêu cầu 2026-08-19) — @dnsnamdang
User: "đang đặt tên controller là contractexportrequest… muốn đổi thành như erp là productexportrequestcontroller, warehouseexportrequestcontroller, productexportcontroller". ERP tách 3 controller trong `Warehouse/` (ProductExportRequests = YCXH, WarehouseExportRequests = ĐNXK, ProductExports = Phiếu xuất hàng) → HRM đang gộp 3 nghiệp vụ vào 2 controller, tách lại cho khớp.
- [x] `ProductExportRequestController` (đổi tên `ContractExportRequestController`): giữ YCXH (index/typeOptions/createData/store/editData/update/cancel/destroy/show/uploadAttachments/deleteAttachment); GỠ 6 method + import thừa (ContractProductExport, ContractWarehouseExport, ContractProductExportService, ContractWarehouseExportRequestService).
- [x] `WarehouseExportRequestController` (đổi tên `ContractWarehouseExportRequestController`): giữ ĐNXK; NHẬN THÊM `warehouseExportData` + `storeWarehouseExportRequest` + `assertCanApprove` (từ controller cũ) + import Carbon.
- [x] `ProductExportController` (MỚI): `productExportData` + `storeProductExport` + `assertCanExportGoods`.
- [x] `api.php`: đổi 2 import cũ → 3 import mới; route `/{id}/warehouse-export-data` + `/{id}/warehouse-export-requests` trỏ WarehouseExportRequestController; route warehouse-exports (`product-export-data` + `product-exports`) trỏ ProductExportController; còn lại ProductExportRequestController. URL route GIỮ NGUYÊN (FE không đổi).
- [x] Cập nhật 2 comment tham chiếu trong `PermissionsTableSeeder.php`.
- [x] Verify: `php -l` 5 file sạch; grep không còn tên class cũ. Entity/Service/Resource GIỮ tên `Contract*` (user chỉ yêu cầu đổi controller).

### Checkpoint — 2026-08-19 (b) — Tách/đổi tên 3 controller khớp ERP
Vừa hoàn thành: Đổi tên + tách export controller theo ERP. 2 controller cũ (`ContractExportRequestController`, `ContractWarehouseExportRequestController`) → 3 controller mới (`ProductExportRequestController`, `WarehouseExportRequestController`, `ProductExportController`). Route URL không đổi nên FE không cần sửa. php -l 5 file sạch, không còn tham chiếu tên cũ.
Đang làm dở: (không).
Bước tiếp theo: E2E test loop type-21 (task 6.4) + brainstorm #4 xuất ghép/tách.
Blocked:

### 9.4 Đồng bộ HẾT Entity/Service/Resource khớp ERP (user: "đồng bộ hết" 2026-08-19) — @dnsnamdang
Sau khi đổi tên controller (9.3), user yêu cầu bỏ luôn tiền tố `Contract` ở toàn bộ Entity/Service/Transformer trong luồng xuất hàng cho khớp ERP. GIỮ NGUYÊN entity HĐ thật (`Contract`), `ContractController`, `ContractParentImportService`, `ContractProductImport*` (nghiệp vụ nhập, không đụng).
- [x] Kiểm tra an toàn: mọi Entity đều khai `protected $table` tường minh → đổi tên class KHÔNG đổi binding bảng DB; không có class-string morph lưu DB (chỉ `emplement_contract_type => Contract::class` trỏ HĐ thật, không đổi); không trùng tên đích.
- [x] Đổi tên 14 class (file + tên class), longest-first tránh collision chuỗi con:
  - Entities/Warehouse (8): `ContractExportRequest`→`ProductExportRequest`, `ContractExportRequestTab`→`ProductExportRequestTab`, `ContractExportRequestTabProduct`→`ProductExportRequestTabProduct`, `ContractWarehouseExportRequest`→`WarehouseExportRequest`, `ContractWarehouseExportRequestDetail`→`WarehouseExportRequestDetail`, `ContractWarehouseExport`→`WarehouseExport`, `ContractProductExport`→`ProductExport`, `ContractProductExportDetail`→`ProductExportDetail`.
  - Services (4): `ContractExportRequestService`→`ProductExportRequestService`, `ContractWarehouseExportRequestService`→`WarehouseExportRequestService`, `ContractProductExportService`→`ProductExportService`, `ContractStockService`→`StockService`.
  - Transformers (2): `ContractExportRequestResource`→`ProductExportRequestResource`, `ContractWarehouseExportRequestResource`→`WarehouseExportRequestResource`.
- [x] Thay tham chiếu trên 19 file (14 file trên + 5 tham chiếu: 3 controller export, `ContractController`, `ContractParentImportService`) — 180 occurrence, chỉ trong `Modules/Assign`.
- [x] Verify: `php -l` 19 file sạch; tên class khớp filename (PSR-4) 14/14; grep toàn `hrm-api` (app/Modules/config/routes/database) không còn tham chiếu tên cũ.

### 9.5 Fix hiện 2 bảng chi tiết hàng hoá cùng lúc (user báo 2026-08-19) — @dnsnamdang
Triệu chứng: màn Tạo YCXH loại HĐ (20/21) hiện ĐỒNG THỜI bảng dòng hàng HĐ + bảng "Thêm hàng hoá" nhập tay.
- [x] Truy nguyên: KHÔNG phải regression do đổi tên BE (smoke test tinker: mọi class đổi tên nạp OK, bind đúng bảng, `contractProductLines(13)` trả đủ 4 dòng; log BE sạch; composer classmap sạch). Bug template FE có sẵn ở `pages/finance/product-export-requests/components/ProductExportRequestForm.vue`.
- [x] Nguyên nhân: `v-else` của bảng nhập tay (dòng 344) ghép nhầm với `v-if` của pay-box (`isSaleType && contractDisplayLines.length`, dòng 324) thay vì với `isContractType`. Hệ quả: loại 21 mà HĐ 0 dòng phù hợp → pay-box ẩn → bảng nhập tay bật kèm; loại 20 (isSaleType=false) → bảng nhập tay luôn bật.
- [x] Sửa: đổi `v-else` → `v-if="isManualType"` (MANUAL_TYPES=[3,6,7,12,18,99]) → bảng nhập tay chỉ hiện đúng loại nhập tay; pay-box `v-if` đứng độc lập.

### Checkpoint — 2026-08-19 (c) — Đồng bộ hết Entity/Service/Resource khớp ERP
Vừa hoàn thành: Bỏ tiền tố `Contract` khỏi 14 class luồng xuất hàng (8 Entity + 4 Service + 2 Resource), cập nhật tham chiếu trên 19 file trong Modules/Assign. An toàn vì mọi Entity khai `$table` tường minh (không đổi bảng DB), không có morph lưu DB. Giữ nguyên `Contract` (HĐ thật), `ContractController`, `ContractParentImportService`, `ContractProductImport*`. php -l 19 file sạch, PSR-4 khớp, grep repo sạch.
Đang làm dở: (không).
Bước tiếp theo: E2E test loop type-21 (task 6.4) + brainstorm #4 xuất ghép/tách.
Blocked:

### 9.6 Fix màn chi tiết YCXH: nhãn "SL cần" sai + giải thích "thành tiền sau giảm/VAT" = 0 (user báo 2026-08-19) — @dnsnamdang
Trên `/finance/product-export-requests/35676` user hỏi: (Q1) sao "thành tiền sau giảm" và "thành tiền sau VAT" đều = 0; (Q2) "SL yêu cầu xuất" đâu, chỉ thấy "SL cần / đã xuất / đã trả" — "SL yêu cầu xuất" có phải "SL cần" không.
- [x] Q1 truy nguyên: KHÔNG phải lỗi code — dữ liệu cũ (stale). Cả 4 dòng detail của 35676 có `allocated_price = null` trong `product_export_request_details`. FE `priceOf` (_id/index.vue): thành tiền sau giảm = SL × allocated_price → null ⇒ 0. Phiếu lưu TRƯỚC khi sửa code ghi allocated_price. Code hiện tại `ProductExportRequestService::writeContractLines` (dòng 296 `'allocated_price' => $allocatedPrice` lấy từ `unit_price_after_discount` HĐ) đã ghi đúng → YCXH type-21 tạo mới sẽ hiện đúng. 35676 là phiếu type-21 HRM duy nhất, bản cũ.
- [x] Q2: user chốt GIỮ nhãn "SL cần" như ERP → giữ nguyên header dòng 94 `_id/index.vue` = "SL cần" (cell render row.qty = SL yêu cầu xuất, đúng như ERP hiển thị).
- [x] Backfill `allocated_price` cho riêng phiếu 35676 (user yêu cầu fake data để hiện giá): match `product_export_request_details.product_id` → `hrm_contract_product_prices.erp_product_id` (contract_id=13), set allocated_price = unit_price_after_discount. Updated 4 dòng (610k/260k/240k/150k). Verify sau VAT 8%: 658.8k/280.8k/259.2k/162k. Chỉ đụng parent_id=35676, KHÔNG chạm data lịch sử ERP.

### Checkpoint — 2026-08-19 (d) — Fix nhãn SL + chẩn đoán stale allocated_price
Vừa hoàn thành: (Q2) đổi nhãn cột "SL cần" → "SL yêu cầu xuất" ở `_id/index.vue` (dòng 94) vì cell render row.qty = SL yêu cầu xuất. (Q1) xác nhận thành tiền sau giảm/VAT = 0 do stale data — phiếu 35676 có allocated_price=null (lưu trước khi sửa code), code hiện tại đã ghi đúng nên phiếu mới sẽ hiển thị đúng.
Đang làm dở: (không).
Bước tiếp theo: chờ user quyết có backfill 35676 không; E2E test loop type-21 (task 6.4) + brainstorm #4 xuất ghép/tách.
Blocked:

### 9.7 Validate tồn kế toán khi Gửi thủ kho ở bước Đề nghị xuất kho (user báo 2026-08-19) — @dnsnamdang
User: "ko validate ĐNXK khi gửi thủ kho à, SL được xuất = 0 vẫn pass. ERP validate ở bước ĐNXK đủ tồn kế toán mới cho xuất". Trước đây task 9.2 GÁC LẠI validateProducts. Giờ bổ sung.
- ERP `WarehouseExportRequest::validateProducts` (model, dòng 617): nhánh xuất thường (không ghép/tách) → mỗi SP so `qty > available` với `available = in_stock − in_promotion_stock` (getAccountingStockDetail). Fail → "Kho không đủ số lượng…". Gọi ở store TRƯỚC syncProducts.
- [x] BE: thêm `assertEnoughStock()` + `collectSelectedLines()` trong `WarehouseExportRequestService`, dùng `StockService::getLineStocks` (available_export_qty = in_stock−in_promotion_stock). Gọi trong `createFromExportRequest` (except=null) + `updateDraft` (except=dnxk id) — CHỈ khi status=2 (gửi thủ kho), KHÔNG chặn Lưu nháp (status=3). Gộp SL theo product_id trước khi so. Thiếu tồn → throw `\Exception` (business message, KHÔNG dùng ValidationException) → controller catch `Exception` → `responseJson($msg,422)` → FE đọc `data.message` hiện toast + errorMsg. Chọn Exception vì lỗi thiếu tồn là business rule (ERP trả message), ValidationException lại bị framework nuốt message thành "The given data was invalid.".
- [x] Verify: php -l sạch; tinker reflection test: SL 1 > tồn 0 → ĐÃ CHẶN "Kho không đủ số lượng để xuất: … (cần 1, được xuất 0)…"; kho rỗng → "Vui lòng chọn kho xuất."; getLineStocks phiếu 35676 tại kho Cát Bà = 0 đúng.
- Lưu ý: FE hiện chỉ chặn client-side SL ≤ SL yêu cầu (qtyValid), CHƯA chặn SL ≤ SL được xuất → BE là chốt chặn (khớp ERP). Có thể thêm guard FE sau (dựa cột available_export_qty đã có) nếu muốn báo sớm.

### Checkpoint — 2026-08-19 (e) — Validate tồn kế toán khi Gửi thủ kho (ĐNXK)
Vừa hoàn thành: Bổ sung validate đủ tồn ở bước Đề nghị xuất kho khi Gửi thủ kho (status=2), port ERP `validateProducts` nhánh xuất thường. `WarehouseExportRequestService`: +`collectSelectedLines()` (refactor lọc dòng dùng chung create/update), +`assertEnoughStock()` (gộp SL/SP, so available_export_qty từ StockService, thiếu → \Exception 422). Lưu nháp không bị chặn. php -l sạch + tinker test pass.
Đang làm dở: (không).
Bước tiếp theo: E2E trên trình duyệt: tạo ĐNXK từ YCXH type-21, chọn kho tồn=0 → Gửi thủ kho phải báo "Kho không đủ số lượng…"; chọn kho đủ tồn → pass. Cân nhắc thêm guard FE. Rồi brainstorm #4 xuất ghép/tách.
Blocked:

### 9.8 Fake tồn kế toán để duyệt ĐNXK PDNXK-31055 thành phiếu xuất (user báo 2026-08-19) — @dnsnamdang
User: "sửa lại cho tôi duyệt đề nghị xuất kho lại cho phiếu xuất khi này PDNXK-31055". Sau khi bổ sung validate 9.7, phiếu PDNXK-31055 (status=2, kho vật lý 2, 4 SP pid 3962/3960/3959/3958, mỗi SP qty=1, unit 44) không duyệt được vì tồn kế toán tại kho 2 = 0.
- Chẩn đoán: kho 2 có 2 accounting_warehouse — aw 1 "Liên Ninh - Hàng bán" (non-promo, direct=0), aw 2 "Liên Ninh - Hàng khuyến mại" (promo, trong `promo_warehouse_ids=["2","4"]`). Cả 2 đều KHÔNG có `accounting_stocks`/`stocks` cho 4 SP → available=0.
- `stocks` là bản ghi vị trí THEO TỪNG SP (warehouse_id+product_id) → không tái dùng stock_id có sẵn (của SP khác). Phải tạo `stocks` + `accounting_stocks` cho từng SP.
- [x] Fake data (tinker, transaction): mỗi SP tạo 1 `stocks` (warehouse_id=2, total_qty=100, accounting_qty=100) + 1 `accounting_stocks` (aw_id=1 non-promo, stock_id trỏ stocks vừa tạo, qty=100 base, created_by=13). Kết quả: stock_id 14860–14863, accounting_stock_id 21829–21832.
- [x] Chọn aw_id=1 (KHÔNG phải aw 2) để tồn KHÔNG bị coi là khuyến mại (in_promotion=0), nếu không `available = in_stock − in_promotion = 0`.
- [x] Verify `StockService::getLineStocks` tại kho 2: pid 3962/3960 available=10, pid 3959/3958 available=6.67 — đều ≥ qty=1 → validate lúc duyệt pass. Base qty=100 / coeff(10|15) ra số đơn vị này.
- Lưu ý: chỉ fake đúng 4 SP tại kho 2, không đụng tồn SP/kho khác. accounting_stocks không có unique index nên insert an toàn.

### Checkpoint — 2026-08-19 (f) — Fake tồn để duyệt PDNXK-31055
Vừa hoàn thành: Tạo `stocks` + `accounting_stocks` (aw 1 non-promo, qty=100 base) cho 4 SP của PDNXK-31055 tại kho vật lý 2. Verify getLineStocks: available 6.67–10 ≥ 1 → duyệt ĐNXK → phiếu xuất kho không còn bị chặn tồn.
Đang làm dở: (không).
Bước tiếp theo: User duyệt PDNXK-31055 trên UI → xác nhận sinh phiếu xuất kho. Rồi E2E full loop type-21 + brainstorm #4 xuất ghép/tách.
Blocked:

### 9.9 Deep-link nhảy app HRM↔ERP tại 2 bước tạo phiếu (user báo 2026-08-19) — @dnsnamdang
User: "bấm nút tạo phiếu xuất kho bên HRM → nhảy giao diện tạo sang ERP; tương tự phiếu xuất hàng bấm bên ERP → nhảy sang HRM. Tạo xong đang ở đâu thì ở đó, không cần nút quay lại."
Bối cảnh: DB gộp `erp_hrm_check` → ID + bảng `employees`/`warehouse_stockers` dùng chung (map employee ERP↔HRM đã thống nhất, `auth()->id()` = employees.id trong module đã port). Không dựng lại màn, chỉ deep-link `window.location`.
Hạ tầng có sẵn: HRM client expose `tp_url` (URL ERP) qua publicRuntimeConfig; ERP có `HRM_URL_FE` trong config/app.php.
Quyết định: **phương án B** — bê nguyên điều kiện ERP `canApprove` (`isWarehouseStocker(warehouse_id) && status==2 && type != 5`). Thủ kho check qua `warehouse_stockers.stocker_id == auth()->id()` (+ Super Admin bypass = mọi kho).

**Chiều 1 — HRM ĐNXK → ERP tạo phiếu xuất kho:**
- [x] BE: `WarehouseExportRequestResource::canCreateWarehouseExport($status)` + cờ `is_can_create_warehouse_export` (chỉ trả ở nhánh chi tiết `relationLoaded('products')`) = `status==STATUS_CHO_DUYET(2) && type != 5 && (Super Admin || warehouse_stockers có (stocker_id=auth()->id(), warehouse_id=$this->warehouse_id))`. `php -l` sạch.
- [x] FE: `pages/finance/warehouse-export-requests/_id/index.vue` — nút "Tạo phiếu xuất kho" (`v-if="detail.is_can_create_warehouse_export"`, primary, icon `ri-add-line` theo button-convention) + method `goCreateWarehouseExport()` → `window.open($config.tp_url + '/admin/warehouse/warehouse_exports/create?warehouse_export_request_id=' + id, '_blank')` (mở tab mới, đồng nhất chiều 2).

**Chiều 2 — ERP phiếu xuất kho → HRM lập phiếu xuất hàng:**
- [x] ERP: `resources/views/warehouse/warehouse_exports/show.blade.php` (dòng 489-498) — nút "Tạo phiếu xuất hàng": `in_array($export->type, [XUAT_BAN_HOP_DONG, XUAT_SAN_XUAT_HOP_DONG])` → href = `rtrim(config('app.HRM_URL_FE'),'/') . '/finance/product-exports/create?warehouse_export_id=' . $export->id` (target _blank); ngược lại giữ `productExport.create` nội bộ. HRM landing `product-exports/create.vue?warehouse_export_id={id}` đã có sẵn. **Đã hoàn tất.**

Lưu ý test: thủ kho kho 2 = emp 311/321/334/336/477/724/313/320/1050. Đăng nhập HRM bằng 1 trong số đó (hoặc Super Admin) mới thấy nút trên PDNXK-31055 (emp 13 lập nhưng là thủ kho kho 19). Auth ERP qua SSO khi hạ cánh.
- [x] **Fix Super Admin check (2026-08-19):** BE cũ dùng `\App\Models\Employee::find($id)->roles` → spatie relation bị scope theo `company_id` nên trả `[]`, Super Admin không bao giờ pass. Sửa: tra thẳng pivot `employee_has_roles` (join `roles`, `whereRaw LOWER(name)='super admin'`, key `employee_id = auth()->id()`). DNS Admin (emp 13) có role Super Admin (role_id 100002) → auto-pass MỌI kho. `php -l` sạch. Đã gỡ row `warehouse_stockers` id=96 (workaround thừa). → **Tài khoản test lập phiếu xuất kho = DNS Admin (namdangit@gmail.com, emp 13).**
- Lưu ý deploy: BE (Resource PHP) chỉ cần server API chạy đúng codebase này (không cần build); FE cần rebuild `hrm-client` (Nuxt) để nút "Tạo phiếu xuất kho" xuất hiện trên `192.168.120.152:8001`.
- [x] **Nút "Tạo phiếu xuất kho" ở màn danh sách (2026-08-19):** BE chuyển cờ `is_can_create_warehouse_export` ra `$data` gốc (trả cả list lẫn chi tiết). FE `warehouse-export-requests/index.vue` — thêm `V2BaseIconButton` (icon `ri-add-line`, title "Tạo phiếu xuất kho", `v-if="item.is_can_create_warehouse_export"`) vào cột Thao tác (sau nút Xem) + method `goCreateWarehouseExport(item)` mở tab ERP.
- [x] **Fix URL deep-link lấy nhầm domain HRM (2026-08-19):** `tp_url` khai báo trong `nuxt.config.js` block `env:` (không phải `publicRuntimeConfig`) → `this.$config.tp_url` = undefined → URL thành tương đối, dính domain HRM (8001). Sửa cả 2 file dùng `process.env.tp_url` (+ trim trailing slash + toast lỗi nếu chưa cấu hình). **Deploy: kiểm tra biến `TP_URL` trên `.env` của server FE 192.168.120.152 phải trỏ đúng ERP dùng chung DB `erp_hrm_check` (mặc định .env local đang là `http://qttt.tanphat.com` = ERP prod, KHÔNG phải bản gộp).**

### 9.10 Fake tồn vị trí + lô để tạo được phiếu xuất kho PDNXK-31055 (user báo 2026-08-19) — @dnsnamdang
User: "những hàng hoá đó không có tồn vị trí, ko có lô nhỉ. có thể fake dữ liệu giúp tôi không". Sau 9.8 (fake tồn kế toán) đã duyệt được ĐNXK, nhưng màn ERP tạo phiếu xuất kho cần chọn Vị trí + Lô cho từng dòng — 4 SP (3962/3960/3959/3958) chưa có `stock_positions`/`stock_position_of_companies`/`stock_position_details`/`warehouse_import_lots` nên ô Vị trí/Lô trống, Tồn=0.
- Chuỗi tồn vật lý ERP: `positions` → `stock_positions`(stock_id,product_id,position_id,qty base) → `stock_position_of_companies`(spoc: qty>0, company_id — điều kiện xuất) → `stock_position_details`(link tới `import_lot_id`, qty>0, company_id) → `warehouse_import_lots`(lô, qty>0, company_id).
- `Position::searchWithProduct(type=export)`: join spoc, cần `spoc.qty>0` + `spoc.company_id == request.company_id`. Position hiển thị = floor(qty/unit_coefficient đơn vị xuất).
- `getLotsInPosition`: join `stock_position_details`↔`warehouse_import_lots`, cần `spd.qty>0` + `wil.company_id == request.company_id`.
- [x] Fake (tinker, transaction) mỗi SP tại vị trí 3549 (LN-N1-D1-K1-T1, kho 2, có space): 1 `warehouse_import_lots` (tồn đầu kho: parent_id=null, type=2, unit_id=40 "Cái" coeff=1, qty/remain/import/request=100, company_id=1, model_id lấy từ `products.model_id` — NOT NULL, lot_number="TONDAUKHO-{id}-{pid}-40") + 1 `stock_positions`(stock_id tái dùng 14860-14863, qty=100 base) + 1 `stock_position_of_companies`(qty=100, company_id=1) + 1 `stock_position_details`(import_lot_id, qty=100, company_id=1). Kết quả: lot 38617-38620, sp 22758-22761.
- [x] Verify `searchProductPosition`/`getLotsInPosition` trả vị trí 3549 + lô cho 4 SP (available Hộp = floor(100/coeff) = 10 hoặc 6). **Phát hiện nguyên nhân gốc**: 4 SP vốn có lô ở vị trí 4620 nhưng KHÔNG có `stock_position_of_companies` theo company → export query (spoc.qty>0 + company_id) trả rỗng ⇒ màn ERP báo tồn vị trí=0. Fake spoc+chuỗi ở 3549 vá đúng mắt xích.

- [x] **Fix lưu phiếu xuất kho lỗi `brand_id cannot be null` (warehouse_export_lots):** 4 dòng `warehouse_export_request_details` của PDNXK-31055 (id 77383-77386) do HRM tạo có `brand_id=NULL` (chỉ có brand_name), `model_id=0`. Controller `WarehouseExportsController::update` (dòng 1090) copy `$product->brand_id` → NULL vào `warehouse_export_lots` (cột NOT NULL) → fail. Backfill từ `products`: brand_id=280, model_id=68/66/65/64. (Đúng gotcha đã ghi memory "PDNXK model_name+brand_id NULL chặn tạo/xuất phiếu".)

- [x] **Fix `updateWarehouse()` lỗi `No query results for StockOfCompany`:** `WarehouseExport::updateWarehouse` (dòng 742) trừ tồn cấp công ty bằng `StockOfCompany::where(stock_id, company_id)->firstOrFail()` — company_id lấy từ `WarehouseExportLot->parent->company_id` = `warehouse_exports(30296).company_id = 1`. 4 stock (14860-14863) chưa có bản ghi `stock_of_companies`. Tạo 4 dòng (stock_id, product_id, company_id=1, qty=100) → soc 15852-15855. Đã đọc hết `updateWarehouse` + `send()`: các mắt xích còn lại (StockPosition/Detail/OfCompany company 1) đều đã fake ở 9.10, phần sau chỉ insert log + đổi status + Redis.

### Checkpoint — 2026-08-19 (g) — Fake tồn vị trí + lô PDNXK-31055
Vừa hoàn thành: Fake chuỗi tồn vật lý (warehouse_import_lots → stock_positions → stock_position_of_companies → stock_position_details) cho 4 SP tại vị trí 3549 kho 2, company 1, qty 100 base. Verify 2 query ERP đều trả vị trí + lô. Nguyên nhân gốc tồn=0: thiếu spoc theo company (lô cũ ở 4620 không có spoc).
Đang làm dở: (không).
Bước tiếp theo: User vào màn ERP tạo phiếu xuất kho PDNXK-31055 → chọn vị trí "LN-N1-D1-K1-T1" + lô TONDAUKHO cho từng dòng → lưu phiếu. Rồi E2E full loop type-21 + brainstorm #4 xuất ghép/tách.
Blocked:

### 9.11 Danh sách phiếu xuất kho ERP không hiện tên loại 20/21 (user báo 2026-08-19) — @dnsnamdang
User: "danh sách phiếu xuất kho erp thiếu loại mới 20,21 nên đang lỗi ko hiện loại".
- Chẩn đoán: các màn list warehouse (`warehouse_exports`, `product_exports`, `warehouse_export_requests`, `product_export_requests` + bản `forAccounting/forManager/all`) render cột Loại + dropdown filter bằng JS global `ALL_EXPORT_TYPES` (`public/js/constant.js:193`). Mảng này = `...EXPORT_TYPES` + {9 ghép, 10 tách} → KHÔNG có 20/21. `findType(ALL_EXPORT_TYPES, 20/21)` trả undefined → cột trống; các blade dùng `.name` (không `?.`) như forAccounting/forManager/all còn văng lỗi JS. (Model `ExportModel::TYPES` PHP đã có 20/21 từ trước — chỉ thiếu ở JS.)
- [x] Thêm `{id:20,"Xuất sản xuất theo hợp đồng"}`, `{id:21,"Xuất bán hợp đồng"}` vào `ALL_EXPORT_TYPES` (constant.js). CỐ Ý không thêm vào `EXPORT_TYPES` (dùng cho dropdown tạo tay YCXH + `product_export_request_types`) để 20/21 chỉ hiển thị/lọc, không tạo tay được.
- Lưu ý deploy: `constant.js` là static asset → user cần hard refresh (Ctrl/Cmd+Shift+R) hoặc bump version cache để thấy thay đổi.

### Checkpoint — 2026-08-19 (h) — Map tên loại 20/21 ở list ERP
Vừa hoàn thành: Thêm loại 20/21 vào `ALL_EXPORT_TYPES` (constant.js) → cột Loại + filter ở mọi màn list xuất kho/YCXH hiển thị đúng tên, hết lỗi JS ở bản forAccounting/forManager/all. Không đụng EXPORT_TYPES (giữ 20/21 không tạo tay được).
Đang làm dở: (không).
Bước tiếp theo: User hard refresh trình duyệt → kiểm tra list phiếu xuất kho hiện đúng "Xuất bán hợp đồng"/"Xuất sản xuất theo hợp đồng". Rồi E2E full loop type-21.
Blocked:

### 9.12 Form "Lập phiếu xuất hàng" (product-exports/create) restyle giống form YCXH (user báo 2026-08-19) — @dnsnamdang
User: "phiếu xuất hàng form tạo giao diện sửa lại giống form của yêu cầu xuất hàng". Form đích `pages/finance/product-exports/create.vue` (Lập phiếu xuất hàng, tạo từ phiếu xuất kho ERP) đang là bản UI đơn giản; form mẫu `pages/finance/warehouse-export-requests/create.vue` (Lập ĐNXK từ YCXH) có card badge icon + kv-grid "Thông tin chung" + subpanel "Khách hàng & giao hàng" + footer cố định.
- [x] BE: `ProductExportController::productExportData` — enrich payload `warehouse_export` thêm snapshot KH từ chính `$we` (warehouse_exports có sẵn customer_mobile/contact/address/delivery_place) + warehouse_name (join `warehouses`) + export_request_code (`$req->code`) + request_date (`$we->created_at` → d/m/Y H:i). `php -l` sạch.
- [x] FE: rewrite template + scss `product-exports/create.vue` theo form YCXH — section card badge icon, kv-grid "Thông tin chung" (Mã PXK, ĐNXK, số HĐ, kho xuất, ngày lập), subpanel "Khách hàng & giao hàng", ghi chú kv--block, bảng er-table, footer `export-actionbar` cố định (Quay lại + Lưu nháp + Hoàn tất). Giữ done-state/loading/loadError. Kho xuất readonly (kv), không thêm cột tồn/brand/model (BE lots không trả).
- [x] FE: thêm `unsavedChangesMixin` (markFormPristine sau fetch, markFormSaved sau submit) — tuân CLAUDE.md màn form phải cảnh báo thoát khi chưa lưu.

### Checkpoint — 2026-08-19 (i) — Restyle form Lập phiếu xuất hàng
Vừa hoàn thành: BE enrich `productExportData` (snapshot KH + warehouse_name + ĐNXK code + ngày lập); FE rewrite `product-exports/create.vue` giống form YCXH (card badge icon, kv-grid + subpanel KH&giao hàng, er-table, footer cố định) + gắn unsavedChangesMixin.
Đang làm dở: (không).
Bước tiếp theo: Rebuild/restart FE (nay `localhost:3000`) → mở lại luồng từ ERP PXK "Tạo phiếu xuất hàng" → kiểm tra giao diện mới. Rồi E2E full loop type-21.
Blocked:

### 9.13 Bảng chi tiết hàng hoá — port kho kế toán + cột giá (scope A) (user báo 2026-08-19) — @dnsnamdang
User: "bên erp cho chọn kho kế toán được xuất nữa cơ mà màn. bảng chi tiết hàng hoá thiếu nhiều logic quá" (+3 screenshot ERP form Xuất bán hàng). Chốt scope **A** (port đầy đủ): 1 dòng hàng → N kho kế toán, cột giá bán/VAT, tách tồn/giữ readonly, lưu bảng con.
Quyết định: (1) Lưu nháp (status 3) KHÔNG bắt Σ khớp; chỉ Hoàn tất (status 1) mới validate Σ acc = SL thực xuất. (2) Cột giá hiện cả loại 20 & 21. (3) Chỉ 1 bảng Hàng hoá — không tab Nhóm-N (HĐ mới không dùng firm-contract tabs). (4) Tab Bốc xếp/Vận chuyển/Hạch toán bổ sung sau. (5) KHÔNG có cột giá vốn (đúng ERP form này) → không phát sinh dữ liệu nhạy cảm.
Hiện trạng đã verify trên `erp_hrm_check`: bảng con `product_export_detail_accounting` ĐÃ CÓ (đủ cột) → không cần migration. Nguồn tồn/giữ: `StockService::computeOne` (đã có, mirror getAccountingStockDetail). Nguồn giá: `product_export_request_details` (parent_id=product_export_request_id + product_id) có price/extra_price/allocated_price/vat_percent.

- [x] BE: `StockService` thêm method public `accountingStockOfProduct($accWhId, $productId, $unitId, $ctx)` bọc `computeOne` với accWarehouseIds=[1 kho] (không sửa logic cũ).
- [x] BE: entity `ProductExportDetailAccounting` (table `product_export_detail_accounting`, guarded=[]).
- [x] BE: `ProductExportController::productExportData` enrich mỗi lot thêm price/extra_price/allocated_price/vat_percent (join PERD) + top-level `accounting_warehouses` (lọc warehouse_id+company+status=1).
- [x] BE: route + method `POST accounting-stock-of-product` → tồn/giữ theo 1 kho kế toán.
- [x] BE: `storeProductExport` validate payload products[].acc_warehouses; `ProductExportService.createFromWarehouseExport` viết lại — đổ giá vào ProductExportDetail + tạo ProductExportDetailAccounting con + validate Σ (chỉ khi Hoàn tất) + tổng hợp sum_amount/allocated/vat vào phiếu.
- [x] FE: `product-exports/create.vue` bảng chi tiết — cột giá (niêm yết/bán/thành tiền/sau giảm/VAT/sau VAT) readonly + sub-row kho kế toán (dropdown + SL xuất + tồn/giữ readonly + Thêm/Xoá kho) + ràng buộc Σ=SL thực xuất, không trùng kho, SL≤tồn. Footer tổng tiền.

### Checkpoint — 2026-08-19
Vừa hoàn thành: Task 9.13 scope A đầy đủ — BE (4 file: ProductExportDetailAccounting entity, StockService.accountingStockOfProduct, ProductExportController enrich + endpoint accounting-stock-of-product, ProductExportService viết lại lưu bảng con + giá + tổng tiền) đã `php -l` sạch; FE `product-exports/create.vue` viết lại: cột giá readonly (niêm yết/bán/thành tiền/sau giảm/%VAT/tiền VAT/sau VAT), sub-row kho kế toán (dropdown accounting_warehouses + SL xuất + SL được xuất/từ tồn/từ giữ readonly + Thêm/Xoá kho), validate Hoàn tất Σ=SL thực xuất + không trùng kho + SL≤được xuất, Lưu nháp bỏ qua, footer tổng tiền.
Đang làm dở: (chưa test E2E trên trình duyệt)
Bước tiếp theo: Test loại 21 end-to-end (tạo YCXH → ĐNXK → phiếu xuất kho → mở form lập phiếu xuất hàng, chọn kho kế toán, Hoàn tất) để verify tồn/giữ + lưu bảng con đúng.
Blocked:

### 9.14 FE — kho kế toán CÙNG HÀNG với dòng hàng (giống ERP) (user báo 2026-08-19)
User gửi ảnh ERP: toàn bộ là 1 bảng phẳng, cột Kho kế toán / SL xuất / Từ SL tồn / Từ SL giữ nằm CÙNG HÀNG với dòng hàng, không phải panel con bên dưới. Nhiều kho → cột hàng hoá `rowspan`, mỗi kho 1 dòng con.
- [x] FE: gộp bảng — bỏ acc-panel sub-row, đưa cột kho kế toán vào chung `<tr>` dòng hàng; dùng `rowspan` cho cột hàng hoá khi 1 dòng có nhiều kho; badge "đã phân bổ x/y" ngay dưới SL thực xuất; nút +Thêm/xoá kho ở cột cuối.

### 9.15 Hạch toán phiếu xuất hàng — NGHIÊN CỨU + BRAINSTORM (user chốt 2026-08-19, code hôm sau)
Scope A: port hạch toán xuất hàng từ ERP sang HRM (account_details + trừ tồn/prepick + công nợ). Hôm nay chỉ research ERP + brainstorm, mai code.
- [x] Research: đọc ERP `ProductExportsController@store` + service hạch toán — map luồng tạo `account_details`, trừ tồn/prepick, công nợ, jobs, config theo loại phiếu. Kết quả + spec → `docs/superpowers/specs/2026-08-19-hop-dong-xuat-hang-hach-toan-design.md`.
- [x] Brainstorm: user trả lời đủ 4 câu (2026-08-20). Chốt design → spec §3bis.
  - Loại 21: doanh thu Nợ131/Có511+3331 (bê nguyên khuôn bán hàng ERP) + giá vốn Nợ632/**Có155** (đổi từ 1561).
  - Loại 20: giá vốn Nợ**1541**/Có**1561** (không doanh thu). Phiếu nhập cha auto: Nợ**155**/Có**1541**.
  - TK hardcode (tra accounts.identify_number, danh mục chung). Làm FULL 1 đợt bám sát ERP.
  - DB erp_hrm_check verify xong: đủ 11 bảng + TK (131/id21,155/id45,511/id181,632/id213,1541/id44,1561/id49,3331/id101).

#### 9.15 — CODE (bám sát ERP, hạch toán khi Hoàn tất status=1)
- [x] 9.15.1 Research ERP xong: reference = **hạch toán bán hàng theo hãng** (`FirmContractProductExportService` + cha `FirmContractExportService`, 8 cụm) + `updateWarehouse` + `getDataCreateDept` (loại 20 mẫu XUAT_HANG_KM) + `calculateExportPrice` + `AccountDetail::createDataSaveDept/saveAccountDetail`. **PHÁT HIỆN: HRM thiếu toàn bộ hạ tầng GHI sổ** (chi tiết spec §3ter).
- [ ] **P1** Hạ tầng ghi sổ (đặt theo MENU HRM: `Modules/Finance/Entities/Account/`, cạnh `Account` đã có).
  - **Rà menu (2026-08-20):** HRM đã có sẵn nhiều hơn tưởng → KHÔNG cần port model mỏng. `Account` có ở `Finance`. Đọc tồn/prepick/hold (`StockService`) + nhập cha (`ContractParentImportService`) đã ghi accounting_stocks bằng `DB::table()` thô → P2/P4 theo đúng kiểu đó, KHÔNG tạo Eloquent Prepick/Hold/Stock.
  - Chỉ THIẾU: `AccountDetail` + `AccountDetailRef` → tạo ở `Modules/Finance/Entities/Account/` với `createDataSaveDept`(bê nguyên map) + `saveAccountDetail` (mở rộng: set THẲNG cột dẫn xuất vì HRM lưu FQN ERP không morphTo được).
  - Quy ước FQN chốt (theo DB): `invoiceable_type='App\Model\Warehouse\ProductExport'` (ERP), `contractable_type='Modules\Assign\Entities\Contract\Contract'` (HRM). `invoiceable_code` NOT NULL → set thẳng (PXH code).
  - ✅ P1 XONG (2026-08-20): tạo `AccountDetail.php`+`AccountDetailRef.php` ở Finance, lint sạch, smoke-test insert+refs trong tx rollback OK (FQN đúng, đủ NOT NULL). `createDataSaveDept` dùng key field thô; `saveAccountDetail($accounts,$invId,$invType,$invCode,$meta)`.
- [x] **P2** ✅ (2026-08-20) `WarehouseExportAccountingService`: updateWarehouse (trừ accounting_stocks+log, prepick FIFO expire_date, hold, stocks.accounting_qty) + calculateExportPrice + fifoValue (port getValueDetails/calculateValue raw DB). **Cost engine khớp ERP TUYỆT ĐỐI 6 ca thật** (value_before/after tới từng đồng). Lint sạch. Trừ kho test end-to-end ở P6.
- [x] **P3** ✅ (2026-08-20) `Modules/Assign/Services/ProductExportPostingService.php`: port ĐỦ 8 cụm ERP cho loại 21, giá vốn dư **Có 155** (thay 1561). Thêm quan hệ `Contract::support_accounting` (morphOne, cùng-DB OK) + `SupportAccounting::department_main`. Tra org (dept lead / part lead / company) qua `DB::table` memoize — KHÔNG morphTo cross-DB. `objectable_type`→cột obj_* bằng suffix FQN. gross/gross_vat/sale_invoice tính thẳng từ chi tiết (đúng ĐN ERP). **TEST: sinh 28 vế, Σ Nợ = Σ Có (lệch 0)** trên HTHT thật HĐ 15; ghi thật 24 dòng + 26 ref trong tx rollback, mọi cột dẫn xuất đúng (155 Có product, FQN HRM, mã phiếu, org, work, date_acc).
- [x] **P4a** ✅ (2026-08-20) Posting loại 20 (Nợ**1541**/Có**1561**) — `costAccountingProduction` trong cùng service. TEST: 2 vế cân đối (lệch 0).
- [x] **P4b** ✅ (2026-08-20) Phiếu nhập cha auto (Nợ155/Có1541): `ContractParentImportService` thread giá vốn thật per-parent-product (import_price=cost/import_qty, total=cost trên detail + accounting), value stock log cộng dồn, gọi `postParentImportAccounting` trong transaction. Test tinker (rollback): Nợ155=2.100.000/Có1541=2.100.000 lệch 0, FQN ProductImport, contract 15, mã phiếu gán đúng.
- [x] **P5** ✅ (2026-08-20) Wire finalize (status=1) trong `ProductExportService::createFromWarehouseExport`: khi Hoàn tất → (1) `WarehouseExportAccountingService::updateWarehouse` trừ tồn/prepick/hold + ghi đè export_price=giá vốn FIFO, (2) `$pxh->load('products')`, (3) `ProductExportPostingService::postAccounting` ghi sổ (loại 21: 8 cụm; loại 20: giá vốn Nợ1541/Có1561), (4) loại 20 → `createParentImport` (tự hạch toán Nợ155/Có1541). Idempotent guard trong từng service. Lint sạch. **DebtRemindersJob HOÃN**: cần model `ContractStateDelivery` (mốc thanh toán gắn SL bàn giao) — HRM CHƯA có; là nhắc nợ downstream, không phải bút toán → tách feature riêng. Bốc xếp (arrange_delivery) cũng hoãn (đã gác từ P1).
- [x] **P6 — Accuracy gate** ✅ (2026-08-20) Đối chiếu code posting với phiếu bán-hãng ERP THẬT (PXH id=4, HĐ 71, DB gộp): dựng lại đúng input (p3996 qty11 coef100 price664300 alloc540000 vat10 giá vốn248.75) → 3 cụm lõi tái tạo CHÍNH XÁC TỪNG ĐỒNG: Nợ1311=8.038.030, Có5111=7.307.300(work15), Có33311=730.730, Nợ5213=1.367.300(work16), Nợ33311=136.730, Có1311=1.504.030, Nợ632/Có155=273.625 (155 thay 1561 đúng thiết kế). Công thức khớp ERP: gross=Σ(price+extra)×qty; giảm trừ=gross−Σ(alloc×qty); VAT 10% mỗi vế; giá vốn=export_price×qty×coef. Cụm thưởng/HH của HĐ test (có HTHT) balance ΣNợ=ΣCó lệch 0. **Cost engine** đã khớp 6 ca thật tới đồng (P2).
- [x] **P6b — E2E kho** ✅ (2026-08-20) Dựng bộ data mới đầy đủ (warehouse + accounting_warehouse 0/1 + stocks + accounting_stocks + layer nhập đầu kỳ giá 200/ĐVCS + YCXH + đề nghị + phiếu xuất kho + lot + BOM cha-con) trong tx rollback, auth giả Employee 13. Chạy trọn `createFromWarehouseExport(status=1)`:
  - **Loại 21** (p3996 qty11 coef100 price664300 alloc540000 vat10): export_price ghi đè 664300→**200** (FIFO); tồn kế toán + tồn vật lý 2000→**900**; log xuất vb400000/va180000→giá vốn **220000**; account_details **22 dòng ΣNợ=ΣCó lệch 0**, cụm lõi khớp ERP (1311=8.038.030, 5111=7.307.300 emp13 work15, 33311=730.730, 5213=1.367.300 emp13 work16, 1311co=1.504.030), giá vốn **Nợ632/Có155=220.000**.
  - **Loại 20**: **Nợ1541/Có1561=220.000** (không doanh thu); phiếu nhập cha auto (PNH id, status1) detail cha 3960 qty11 **import_price 20.000 total 220.000**; **Nợ155/Có1541=220.000**. Vòng khép giá vốn đóng (1541 net=0).

### Checkpoint — 2026-08-20
Vừa hoàn thành: P4b + P5 (wire finalize) + P6 accuracy gate (khớp ERP PXH4 từng đồng) + P6b E2E kho (loại 20 & 21 chạy trọn, trừ tồn + FIFO + hạch toán cân đối).
Đang làm dở: (không)
Bước tiếp theo: DebtRemindersJob (cần model ContractStateDelivery — tách feature) + hạch toán bốc xếp (arrange_delivery) nếu cần; FE nút Hoàn tất phiếu xuất hàng.
Blocked: (không)

### Checkpoint — 2026-08-19 (cuối ngày, tạm dừng chờ mai)
Vừa hoàn thành: Task 9.13/9.14 (tạo phiếu + phân bổ kho kế toán, FE bảng phẳng giống ERP) xong. Task 9.15: NGHIÊN CỨU hạch toán xuất hàng ERP xong — đã map đầy đủ luồng (updateWarehouse trừ tồn/prepick/giá vốn BQGQ, account_details getDataCreateDept, DebtRemindersJob) vào spec `docs/superpowers/specs/2026-08-19-hop-dong-xuat-hang-hach-toan-design.md`.
PHÁT HIỆN CHÍNH: loại 20/21 là loại MỚI cho HRM, ERP CHƯA có mẫu bút toán → phải tự thiết kế.
Đang làm dở: Brainstorm — đã hỏi user Câu 1 (bản chất hạch toán 20 vs 21: khuôn "bán hàng" 131/511/632/3331 hay khuôn "nội bộ" account_debt/account_has do user chọn). User bảo "nhớ lại mai hỏi lại".
Bước tiếp theo (MAI): Hỏi lại user Câu 1 → 4 (nội dung đầy đủ ở spec §3): (1) bản chất bút toán 20/21, (2) TK hardcode hay user chọn, (3) phạm vi port đợt này, (4) verify bảng DB erp_hrm_check + cột account_debt/account_has. Chốt xong mới code.
Blocked: Chờ user trả lời brainstorm.

### 9.16 Tính năng đã hoãn (làm tiếp sau P6b) — thứ tự A3 → A2 → A1
- [x] **A3** Sửa hệ số đơn vị phiếu nhập cha (loại 20). Root cause: `ContractParentImportService` line 162 hardcode `$unitCoefficient = 1`. Fix: gom `unit_id` cha khi aggregate (`$unitByParentProduct`), thêm helper `resolveUnitCoefficient(product_id, unit_id)` tra `product_units` (unit_id → is_base fallback), `importQty = qty × coef`. Test 2 biến thể (coef 1 vs 200): total giá vốn BẤT BIẾN 2.100.000, Nợ155/Có1541 cân đối, accounting_stocks.qty theo ĐVCS. Lint sạch. (2026-08-20)

#### A2 — Hạch toán bốc xếp / chi phí vận chuyển (arrange_delivery). CHỐT: làm cả 2 hình thức, KHÔNG phân quyền, 1 tab optional trong luồng xuất, bám sát ERP.
**Nguồn ERP** (đã map kỹ 2026-08-21): tab `#boc_xep` trong `warehouse/product_exports/form.blade.php` (dòng 496-685); class JS `WarehouseExportArrangeDelivery`+`WarehouseExportExecutor`; validate `ProductExportsController@store` dòng 366-406; lưu entity dòng 652-695; hạch toán dòng 868-971 (2 nhánh rent_type). Bảng đã có sẵn trong `erp_hrm_check`: `arrange_goods`, `product_import_export_arrange_deliveries`, `product_import_export_arrange_delivery_executors` (chưa có entity HRM).
**Khác ERP (chốt):** bỏ cơ chế "existsArrange" (WarehouseImportExportArrangeDelivery cấp đề nghị) — HRM tab luôn optional; required phụ chỉ theo account/rent_type khi user đã nhập. FQN contractable bốc xếp = WarehouseExport (`App\Model\Warehouse\WarehouseExport`) như ERP (arg 4,5 saveAccountDetail).
- [x] **A2.1 BE Entities** (`Modules/Assign/Entities/Warehouse/`): `ArrangeGood` (bảng `arrange_goods`, đơn giá), `ProductImportExportArrangeDelivery` (fillable theo ERP), `ProductImportExportArrangeDeliveryExecutor`. Quan hệ delivery hasMany executors. KHÔNG hrm_ prefix (bảng ERP đơn bản).
- [x] **A2.2 BE Lưu** trong `ProductExportService::createFromWarehouseExport`: sau khi tạo `$pxh` + details, nếu `$data['arrange_delivery']['rent_type']` → tạo `ProductImportExportArrangeDelivery` (fill + parent_id=pxh->id, type=2/export, request_id=product_export_request_id, account_name/work_name/cost_debt_name tra danh mục, rent_type_name, arrange_type_name từ ArrangeGood) + loop executors. Chạy cho CẢ nháp lẫn hoàn tất (mirror ERP entity-save).
- [x] **A2.3 BE Validate** (request store): khi có `arrange_delivery` → rent_type/arrange_type/account required, weight numeric >0; account prefix 642 → cost_debt required; 154 → work required; rent_type=1 → executors array min1 + Σemployee_price == total_money; rent_type=2 → supplier_id required; mỗi executor employee_price numeric >0. Rethrow ValidationException.
- [x] **A2.4 BE Hạch toán** — method mới `ProductExportPostingService::postArrangeDeliveryAccounting(ProductExport $pxh)`: đọc delivery+executors đã lưu; idempotent guard (account_details invoiceable=pxh + contractable_type=WarehouseExport tồn tại → skip); group = max(group) hiện tại của pxh + 1; 2 nhánh:
  - **rent_type=2 (Thuê ngoài):** Nợ account = total_money ref[3311] {cost_debt_id, work_id, group}; nếu vat: total_cost += total_money×vat/100, Nợ 1331 = total_money×vat/100 ref[3311] {group}, Có 3311 = total_cost ref[account,1311] {supplier_id, group}; else Có 3311 = total_cost ref[account] {supplier_id, group}.
  - **rent_type=1 (Công ty):** Nợ account = total_money ref[33481] {cost_debt_id, work_id, group}; foreach executor Có 33481 = employee_price ref[account] {work_id, employee_id, group}.
  - saveAccountDetail(invoiceable=ProductExport, meta.contractable = WarehouseExport(id/code) — KHÔNG dùng HĐ HRM). Gọi sau `postAccounting` khi finalize (bước 2.5 trong wire).
- [x] **A2.5 BE Wire**: trong finalize block `ProductExportService` (sau postAccounting, trước createParentImport) gọi `postArrangeDeliveryAccounting`, throw ValidationException nếu lỗi.
- [x] **A2.6 FE Tab "Bốc xếp"** (`pages/finance/product-exports/create.vue`): thêm 1 khối card "Bốc xếp / vận chuyển" (tuỳ chọn, không phân quyền — theo yêu cầu "1 tab thêm vào luồng"). Trường is_weight/is_time (radio loại trừ), rent_type (''/1/2), supplier (V2BaseSelectRemote, disabled khi rent_type=1), arrange_type (native select từ arrangeGoods nhúng sẵn), weight, price (computed từ ArrangeGood theo is_weight/rent_type, readonly), total_money (computed price×weight, readonly), vat + vat_price/after_total_money (computed readonly), account TK nợ (V2BaseSelectRemote lọc local, default 6428 khi chọn rent_type), cost_debt + work (V2BaseSelectRemote remote + nút "+" quick-add qua b-modal), bảng executors (khi rent_type=1): V2BaseSelectRemote chọn NV + employee_price, tổng phải = total_money (hiện cảnh báo đỏ). Gửi `arrange_delivery{}` + `executors[]` trong submit; validate FE chỉ khi Hoàn tất (`validateArrange`), snapshot vào unsaved-changes.
- [x] **A2.7 FE Endpoints dropdown**: arrange_goods nhúng vào response `product-export-data` (scope company của phiếu, status=1) — không tạo endpoint rời (giống ERP @json). accounts `finance/accounts/getAll` (load 1 lần, lọc local; value=identify_number), works `finance/works?keyword=` + POST quick-add, cost-debts `finance/cost-debts?keyword=` + POST quick-add, suppliers `assign/customers/manager/suppliers?keyword=` ({id,name}), employees `assign/tasks/employees` (load 1 lần, lọc local). Dùng V2BaseSelectRemote (select trong tab, không modal).
- [x] **A2.8 Test** tinker (rollback): rent_type=2 có/không vat (cân đối ΣNợ=ΣCó, contractable=WarehouseExport); rent_type=1 nhiều executor (Σ khớp total_money, 33481 net=0); idempotent; group nối tiếp sau cụm chính.

#### A1 — DebtRemindersJob (nhắc nợ theo mốc bàn giao) — LÀM CUỐI, cần model `ContractStateDelivery` (HRM chưa có). Tách nhánh nghiên cứu riêng.

### 9.17 Màn DANH SÁCH phiếu xuất hàng (PXH loại 20/21) — CHỐT: bám ERP nhưng chỉ Xem+In, phân 4 cấp, KHÔNG xoá/sửa (user 2026-08-20)
Trước đây chỉ có `create.vue`, thiếu hẳn màn danh sách. User: "làm như bên erp, có xem chi tiết, in ... câu 1 ko cho xoá, câu 2 phân 4 cấp".
**Khác ERP (chốt):** (1) BỎ chức năng xoá/sửa — dropdown thao tác chỉ **Xem chi tiết + In**; (2) phân quyền **4 cấp** (tổng cty/cty/phòng ban/bộ phận + fallback created_by) giống màn anh em HRM, KHÔNG dùng 3 cấp như ERP.
- [x] **L1 BE Permission**: thêm 4 quyền id 1156-1159 type 28 group "Phiếu xuất hàng" (tổng cty/cty/phòng ban/bộ phận) vào `PermissionsTableSeeder.php` (sau nhóm Đề nghị xuất kho id 1155). Tên khớp gate controller.
- [x] **L2 BE Entity** `ProductExport`: thêm const `XUAT_SAN_XUAT_HOP_DONG=20`/`XUAT_BAN_HOP_DONG=21`, static `getTypeName()`, quan hệ `creator()` belongsTo Employee (created_by), `use Employee`.
- [x] **L3 BE Resource** `ProductExportResource` (mới): map list (code, type_name, warehouse_export_code, product_export_request_code, emplement_contract_id/code, customer_*, warehouse_name, creator_name, department_name, status/status_name/status_color, accounting_date, created_at) + detail (note, sum_amount, products[] từ snapshot lot). KHÔNG có is_can_edit/is_can_delete (chỉ xem+in).
- [x] **L4 BE Controller** `ProductExportController`: `scopedQuery()` dùng `checkPermissionListWithColumn` 4 cấp trên `product_exports.created_by` + lọc type∈{20,21} + emplement_contract_type=Contract + ẩn nháp người khác (status≠3 OR created_by=self); `index()` (leftJoin warehouses/warehouse_exports/product_export_requests, filter code/keyword/status/type/company/department/part/employee/warehouse/contract_code/product_export_request_code/start-end_date, sort code|status|created_at, apiPaginate Resource); `show()` (with creator.info.department+products, attachLotSnapshot, trả detail); `attachLotSnapshot()` join warehouse_export_lots theo lot_id lấy snapshot (code/product_name/model_name/brand_name/unit_name), fallback products+units.
- [x] **L5 BE Route**: group `/assign/product-exports` GET `/` (index) + `/{id}` (show), đặt trước group warehouse-exports.
- [x] **L6 FE Menu** `finance.js`: thêm link `/finance/product-exports` + isShow theo 4 quyền "Xem phiếu xuất hàng theo ...".
- [x] **L7 FE List** `pages/finance/product-exports/index.vue` (mới): V2BaseFilterPanel + V2BaseCompanyDepartmentFilter (4 cấp) + V2BaseDataTable; cột STT/Mã/Loại/Phiếu xuất kho/Số HĐ/Khách hàng/Người lập/Ngày lập/Trạng thái/Thao tác; filter keyword+loại+trạng thái(1/3)+cty→PB→BP+người lập+số HĐ+mã YCXH+ngày; thao tác **Xem chi tiết (goDetail) + In (goPrint mở tab)**; filterStateMixin key `finance_product_exports`.
- [x] **L8 FE Detail** `pages/finance/product-exports/_id/index.vue` (mới): 3 khối (Thông tin chung / Khách hàng & giao hàng / Danh sách hàng hoá) + thanh action cố định chỉ **Quay lại + In phiếu** (KHÔNG sửa/huỷ).
- [x] **L9 FE Print** `pages/finance/product-exports/_id/print.vue` (mới): `id="content"`, logo absolute URL, tiêu đề "PHIẾU XUẤT HÀNG", 2 cột info (KH + HĐ/PXK/kho/người lập/ngày), bảng hàng có colgroup+viền, tổng + số tiền bằng chữ, 3 ô ký; `$printContent({styles, pageMargin})` nhúng lại viền bảng vào options.styles.
- [x] **L10 Test** BE integration (`test_pxh_list.php`, tx rollback trên erp_hrm_check): INDEX trả 1 dòng đủ trường (type_name/emplement_contract_code/customer_name/warehouse_name/creator_name/status_name/status_color, KHÔNG có is_can_edit); SHOW trả sum_amount + products (snapshot code/name/qty/price/total/vat) — PASS. Fallback quyền (permissions[4]=true → created_by) hoạt động; thêm fallback units-table cho unit_name khi thiếu lot.

### 9.18 Bỏ gate quyền ở MENU 3 màn xuất hàng (user chốt 2026-08-21)
Yêu cầu: menu Phiếu xuất hàng / Yêu cầu xuất hàng / Đề nghị xuất kho hiện cho MỌI user (bỏ `isShow`); không có quyền vẫn vào được nhưng **chỉ thấy phiếu mình tạo**.
Điều tra root cause "không thấy menu": hệ quyền **2 guard song song** — `web` (gốc ERP, gán role web) vs `api` (HRM auth thực dùng). Menu FE (`getAllPermissions` lọc guard api) + gate BE (`$employee->roles` = role api) chỉ đọc quyền api. Quyền PXH api (1156-1159) chưa vào DB + chưa gán role api nào → `isShow` lọc mất menu. (3 bản web 100918-100920 gán role web nên HRM không thấy.)
- [x] **M1** Xác minh BE 3 màn đã có fallback `created_by`: cả `ProductExportController`, `ProductExportRequestController`, `WarehouseExportRequestController` đều `checkPermissionListWithColumn([..4 cấp.., true], TABLE, 'created_by')` — phần tử [4]=true = không quyền chỉ thấy phiếu mình tạo. Route index cả 3 KHÔNG có middleware `checkPermission` → bỏ menu gate an toàn (không 403, không màn trống).
- [x] **M2** `finance.js`: bỏ `isShow` khỏi 3 item (Yêu cầu xuất hàng, Đề nghị xuất kho, Phiếu xuất hàng). `Topbar.showMenuChild`: `if(!names) return true` → không isShow = luôn hiện. Giữ nguyên quyền api 1156-1159 trong seeder để admin vẫn có thể cấp quyền xem rộng (tổng cty/cty/PB/BP) về sau — không bắt buộc để truy cập cơ bản.
- [x] **M3** Cấp quyền api "xem full theo tổng công ty" cho **namdangit** (employee id 13, employee_info 6, current_company_role=1, role api 18 "Super admin"). Cơ chế role của app = pivot tuỳ biến `employee_has_roles` (KHÔNG phải `model_has_roles` mặc định — rỗng). Đã INSERT permissions api 1156-1159 (group "Phiếu xuất hàng", type 28) + `role_has_permissions` (1156-1159 → role 18, company_id=1) trực tiếp trên `erp_hrm_check`, `php artisan cache:clear`. Verify tinker (auth emp13): gate BE `isCurrentEmployeeHasPermission(tổng cty)=TRUE` → scopedQuery[0] trả toàn bộ phiếu; FE `getAllPermissions` trả đủ 4 quyền PXH → is_all_company=true.

### Checkpoint — 2026-08-21 (bỏ gate quyền menu 3 màn xuất hàng)
Vừa hoàn thành: **9.18** — bỏ `isShow` 3 item menu (finance.js). Root cause "không thấy menu" = hệ 2 guard: HRM auth chỉ đọc quyền guard `api`, mà quyền PXH api chưa tạo/gán → menu bị lọc. BE 3 màn đã sẵn fallback `created_by` + route index không middleware → bỏ menu gate là đủ, user không quyền vẫn vào & thấy phiếu mình tạo.
Đang làm dở: (không)
Bước tiếp theo: (tuỳ user) M3 cấp quyền api để test xem-rộng; hoặc build/QA FE.
Blocked: (không)

### Checkpoint — 2026-08-21 (màn danh sách PXH)
Vừa hoàn thành: **9.17 — màn danh sách phiếu xuất hàng** (trước chỉ có create.vue). BE: 4 quyền id 1156-1159, ProductExport (const 20/21 + getTypeName + creator), ProductExportResource, ProductExportController (scopedQuery 4 cấp + index + show + attachLotSnapshot), route group /assign/product-exports. FE: menu finance.js, index.vue (list), _id/index.vue (detail), _id/print.vue (in). Chốt user: chỉ **Xem + In**, KHÔNG xoá/sửa; phân **4 cấp** quyền. BE test integration PASS (INDEX+SHOW). FE chưa build-verify.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) — build/QA FE màn danh sách; hoặc A1 DebtRemindersJob (cần model ContractStateDelivery, tách feature).
Blocked: (không)

### Checkpoint — 2026-08-21 (test full luồng lần 2, gồm feature mới A2/A3)
Vừa hoàn thành: **Test tích hợp E2E lần 2** — chạy thật `ProductExportService::createFromWarehouseExport(status=1)` trên `erp_hrm_check` (transaction rollback, fake toàn bộ dữ liệu). 2 harness ở scratchpad: `full_flow_test.php` (loại 21) + `full_flow_test_20.php` (loại 20).
- **Loại 21 + bốc xếp Công ty (rent_type=1, 2 executor)**: trừ tồn FIFO 2000→900 ✓; giá vốn export_price=200 (A3 hệ số coef=100 đúng) ✓; 8 cụm hạch toán chính khớp P6b tới từng đồng (Nợ1311=8.038.030, Có5111=7.307.300, Có33311=730.730, Nợ5213=1.367.300, Có1311=1.504.030, Nợ632/Có155=220.000, +35241/5211/6411 bonus/hoa hồng/quỹ rủi ro), ΣNợ=ΣCó=10.516.828 ✓; cụm bốc xếp group=15 NỐI TIẾP sau cụm chính (max 14): Nợ6428=1.5tr / Có33481 emp13=600k+emp14=900k, cân đối; tổng phiếu ΣNợ=ΣCó=12.016.828 lệch=0.
- **Loại 20 + nhập cha + bốc xếp Thuê ngoài+VAT (rent_type=2)**: xuất con 8888 (BOM HĐ15 price 321, qty_needed=3) trừ tồn 100→97 ✓, export_price=200 ✓; cụm chính giá vốn SX Nợ1541/Có1561=600 ✓; cụm bốc xếp Nợ6428=1tr + Nợ1331=100k / Có3311=1.1tr (supplier_id) cân đối ✓; **nhập cha tự sinh** PNH: dòng cha 3960 qty=1 import_qty=1 import_price=600 total=600, tồn cha 3960=1, BT Nợ155/Có1541=600 cân đối ✓; A3 resolveUnitCoefficient chạy đúng.
KẾT LUẬN: Luồng xuất hàng loại 20 & 21 + feature mới A2 (bốc xếp cả 2 hình thức) + A3 (hệ số đơn vị) hoạt động end-to-end, mọi bút toán cân đối, khớp số liệu chuẩn P6b.
Đang làm dở: (không)
Bước tiếp theo: A1 DebtRemindersJob (cần model ContractStateDelivery — tách feature, chờ user).
Blocked: (không)

### 9.19 Màn danh sách PXH hiện MỌI loại phiếu xuất (parity ERP — user chốt 2026-08-21)
Yêu cầu: "phiếu xuất hàng hiện tất cả theo db đang có cho tôi ko filter riêng loại như bên erp đang làm".
Root cause "chỉ thấy 2 phiếu mình tạo" (không phải bug quyền): `scopedQuery` khoá cứng `type IN (20,21) AND emplement_contract_type=Contract` → chỉ 2 dòng khớp trong DB (đều created_by=13). ~30k dòng còn lại là legacy ERP (type 3-99, contract_type NULL) bị lọc mất. Quyền tổng cty của namdangit đã đúng (verify gate=TRUE) nhưng dữ liệu bị thu hẹp bởi type filter.
- [x] **P1 BE Entity** `ProductExport`: mở rộng `TYPE_NAMES` đủ 1-99 (khớp `ProductExportRequest::TYPE_NAMES`), thêm `getAllTypesForFilter()` (id+name toàn bộ loại) để cấp cho filter FE. `getTypeName()` fallback null nếu id lạ.
- [x] **P2 BE Controller** `ProductExportController::scopedQuery()`: **BỎ** filter `type IN (20,21)` + `emplement_contract_type=Contract`. Giữ nguyên: phân quyền 4 cấp trên `created_by` + ẩn nháp người khác (`status != 3 OR created_by=self`). Lọc theo loại giờ do user chọn qua filter `type` trong `index()` (đã có sẵn). Thêm method `typeOptions()` trả `filter_types`.
- [x] **P3 BE Route**: thêm `GET /assign/product-exports/type-options` ĐẶT TRƯỚC `/{id}` (tránh bị nuốt path).
- [x] **P4 FE** `pages/finance/product-exports/index.vue`: `typeOptions` từ static [20,21] → `[]` nạp động qua `fetchTypeOptions()` (gọi `assign/product-exports/type-options`) trong `mounted`, map id→value/name→label.
- [x] **P5 Test** tinker trên `erp_hrm_check` (auth emp13, quyền tổng cty): scopedQuery (sau khi bỏ type filter) trả **34.435 phiếu** (trước = 2); `getTypeName` resolve đúng loại 14/99/20/21; 3 dòng mới nhất id 34581(t20)/34580(t21)/34577(t14) đủ loại. `php -l` cả ProductExport.php + ProductExportController.php PASS.

### Checkpoint — 2026-08-21 (PXH hiện mọi loại — parity ERP)
Vừa hoàn thành: **9.19** — bỏ filter cứng loại 20/21 + emplement_contract_type ở `scopedQuery`; màn danh sách PXH giờ hiện toàn bộ `product_exports` trong DB đúng như ERP. Filter loại chuyển sang nạp động từ endpoint mới `/type-options` (toàn bộ loại 1-99), user tự chọn để lọc. Verify: emp13 (quyền tổng cty) thấy 34.435 phiếu thay vì 2, type_name đúng cho mọi loại.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) build/QA FE màn danh sách (chưa build-verify); hoặc A1 DebtRemindersJob (tách feature).
Blocked: (không)

### 9.20 Bỏ label trạng thái ở 2 màn chi tiết + link "Phiếu xuất kho" nhảy sang danh sách ERP (user chốt 2026-08-21)
Yêu cầu: "cái label trạng thái này ở màn chi tiết phiếu xuất hàng và chi tiết đề nghị xuất kho thì bỏ đi. Gắn link danh sách phiếu xuất kho nhảy sang danh sách bên erp".
- [x] **U1 FE** `product-exports/_id/index.vue`: bỏ `<span class="status-pill">` (label trạng thái ở header "Thông tin chung") + xoá CSS `.status-pill` không dùng.
- [x] **U2 FE** `warehouse-export-requests/_id/index.vue`: bỏ `<span class="status-pill">` + xoá CSS `.status-pill`.
- [x] **U3 FE** `product-exports/_id/index.vue`: field "Phiếu xuất kho" (`warehouse_export_code`) → link mở tab mới sang danh sách phiếu xuất kho ERP `${TP_URL}/admin/warehouse/warehouse_exports` (method `goErpWarehouseExportList`, dùng `process.env.tp_url` như pattern `goCreateWarehouseExport` sẵn có). Không có code → hiện "—", không link.
Ghi chú: ERP list là DataTables server-side (global search `search[value]`), KHÔNG lọc qua URL query → chỉ link tới danh sách như user yêu cầu, không deep-link record. `buildStatusTitle` (tiêu đề tab trình duyệt) giữ nguyên — không phải label hiển thị trên màn.

### Checkpoint — 2026-08-21 (bỏ label trạng thái + link PXK sang ERP)
Vừa hoàn thành: **9.20** — 2 màn chi tiết (PXH + ĐNXK) bỏ pill trạng thái ở header "Thông tin chung"; màn PXH field "Phiếu xuất kho" thành link mở danh sách phiếu xuất kho bên ERP (tab mới).
Đang làm dở: (không)
Bước tiếp theo: (chờ user) build/QA FE.
Blocked: (không)

### 9.21 Bảng "Danh sách hàng hoá" màn chi tiết PXH hiện đủ cột như ERP (user chốt 2026-08-21)
Yêu cầu: "danh sách hàng hoá ở màn chi tiết phiếu xuất hàng hiện thiếu thông tin. Hãy hiện như erp" (3 screenshot bảng chi tiết ERP: giá niêm yết/đơn giá bán/thành tiền bán/đơn giá sau giảm/thành tiền sau giảm/VAT %/số tiền/thành tiền sau VAT/đơn giá vốn/thành tiền vốn/SL đề nghị/SL thực xuất/chi tiết xuất tồn-giữ/kho kế toán + tổng cuối bảng).
Hiện trạng: bảng HRM chỉ 9 cột cơ bản (STT, Mã, Tên, Thương hiệu, Model, ĐVT, SL xuất, Đơn giá, Thành tiền) + 1 dòng tổng. Thiếu toàn bộ khối giá bán/VAT/giá vốn/chi tiết xuất/kho kế toán mà ERP show.
Công thức ERP (JS ProductExportLot getters + ProductExport getters):
- Đơn giá bán `price_after_extra` = price + extra_price; Thành tiền bán = *qty
- Đơn giá sau giảm = allocated_price; Thành tiền sau giảm = allocated_price*qty
- VAT tiền `vat_cost_allocated` = total_amount_allocated*vat%/100; Thành tiền sau VAT = total_amount_allocated + VAT tiền
- Đơn giá vốn = export_price*unit_coefficient (chỉ khi status==1 = đã finalize giá vốn FIFO); Thành tiền vốn = export_price*unit_coefficient*qty
- Cờ loại: is_sale ∈ [1,11,13,14,16,17]; showAllocatedPrice ∈ [1,4,11,13,14,16,17]; chi tiết xuất ẩn khi is_export_direct
- [x] **B1 BE Entity** `ProductExportDetail`: thêm relation `acc_warehouses()` → hasMany `ProductExportDetailAccounting` (product_export_detail_id).
- [x] **B2 BE Controller** `ProductExportController::show`: eager load `products.acc_warehouses`; batch nạp tên kho kế toán (accounting_warehouses) gắn `accounting_warehouse_name` vào từng dòng acc (trong `attachLotSnapshot`).
- [x] **B3 BE Resource** `ProductExportResource`: thêm cờ header `is_sale/show_allocated/is_export_direct/show_cost/can_view_cost_price`; per-line thêm listed_price, extra_price, sale_price, sale_amount, allocated_price, allocated_amount, vat_amount, amount_after_vat, request_qty, unit_coefficient, export_from_stock, export_from_hold, cost_price, cost_amount (2 cột vốn GATE `Xem giá vốn hàng hoá` + status==1 → null nếu không quyền/chưa finalize), acc_warehouses[{name,qty,from_stock,from_hold}]. Giữ `price`/`total_amount` cũ để tương thích.
- [x] **B4 FE** `product-exports/_id/index.vue`: dựng lại bảng theo cột ERP (ẩn/hiện theo cờ is_sale/show_allocated/show_cost/is_export_direct), acc kho kế toán = sub-row rowspan (mỗi SP 1 `<tbody>`); thay dòng tổng đơn bằng khối `.goods-totals` (Tổng tiền bán/giảm giá/trước thuế/VAT/sau thuế + Tổng tiền vốn) — tính FE từ dòng hàng (computed `totals`), chỉ hiện khi is_sale/show_cost. `php -l` 3 file BE PASS.
Ghi chú thiết kế: tổng đặt ở **khối card phải** dưới bảng (không nhồi vào footer table) — tránh colspan mong manh khi cột động, thông tin y hệt ERP. Bỏ cột "ĐV cơ bản/SL theo ĐV cơ bản" (edge is_export_base_unit hiếm). Giá vốn = giá nhạy cảm → BE trả null khi thiếu quyền (không chỉ ẩn FE).

### Checkpoint — 2026-08-21 (bảng hàng hoá PXH đủ cột như ERP)
Vừa hoàn thành: **9.21** — bảng "Danh sách hàng hoá" màn chi tiết PXH port đủ cột ERP: khối giá bán (niêm yết/bán/sau giảm), VAT (%/tiền/sau VAT), giá vốn (đơn giá vốn/thành tiền vốn — gate quyền + status=1), SL đề nghị/thực xuất, chi tiết xuất tồn/giữ, kho kế toán (sub-row). Tổng cuối bảng dạng card phải. BE: relation acc_warehouses + Resource enrich + gate `Xem giá vốn hàng hoá`.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) build/QA FE trên phiếu loại bán (is_sale) đã finalize để soi cột giá vốn + sub-row kho kế toán; kiểm cả phiếu legacy không phải loại bán.
Blocked: (không)

### 9.22 Fix bug bảng hàng hoá PXH không hiện thông số (phiếu 34580, loại 21) — user báo 2026-08-21
Yêu cầu: "sao phiếu này chả hiện thông số gì vậy" (phiếu 34580, type 21 "Hoàn tất") — bảng hàng hoá gần như trống sau khi làm 9.21.
Điều tra (evidence từ DB `erp_hrm_check`): 3 nguyên nhân —
1. **Bug code — thiếu loại 21 trong cờ is_sale/show_allocated**: 9.21 port nguyên list ERP `[1,11,13,14,16,17]` nhưng loại 21 (XUAT_BAN_HOP_DONG = xuất bán theo HĐ, riêng HRM) không có trong ERP → toàn bộ cột giá bán/VAT bị ẩn với chính loại bán của HRM.
2. **Bug code — fallback snapshot dùng `??` không bắt chuỗi rỗng**: `warehouse_export_lots.unit_name` (và có thể code/product_name) lưu `''` → `$lot->unit_name ?? fallback` trả `''` (vì `''` không null) nên KHÔNG rơi về bảng units → ĐVT hiện "—".
3. **Điều kiện dữ liệu (KHÔNG phải bug)**: phiếu 34580/34581 tạo TRƯỚC khi có logic sync giá → `price/allocated_price/vat_percent/export_price` NULL và không có dòng `product_export_detail_accounting` → cột tiền = 0, không sub-row kho kế toán. Giá thật nằm ở YCXH cha (product_export_request_details, parent 35672). Phiếu tạo mới bằng `ProductExportService` hiện tại sẽ có đủ.
- [x] **F1 BE Resource** `ProductExportResource`: thêm `21` vào `$isSale` (`[1,11,13,14,16,17,21]`) và `$showAllocated` (`[1,4,11,13,14,16,17,21]`) + comment giải thích loại 20 (SX nội bộ, chỉ giá vốn) vs 21 (bán).
- [x] **F2 BE Controller** `ProductExportController::attachLotSnapshot`: thêm closure `$pick($value,$fallback)` coi `''`/whitespace là thiếu → dùng cho display_code/product_name/model_name/brand_name/unit_name thay cho `??`. `php -l` 2 file PASS.
- [x] **F3 Data (user chọn (b) — backfill)**: backfill giá test cho phiếu 34580 trên `erp_hrm_check`, mô phỏng đúng công thức `ProductExportService` (không bịa số). 3 dòng PED (89085/89086/89087) set price/vat_percent từ YCXH 35672 (matched product_id), `allocated_price = price` (không giảm giá → đơn giá sau giảm = đơn giá bán), `export_price = allocated`. Tạo 3 dòng `product_export_detail_accounting` (acc_warehouse_id=3 "Phan Trọng Tuệ - Hàng bán", xuất toàn bộ từ tồn). Verify khớp: prod3960 giá niêm yết 35.6tr → sau VAT 8% = 38.448tr; prod7579 85k×10 → 918k; prod3959 43.3k → 46.764k; ĐVT fallback OK (lot.unit_name='' → units: Bộ/Lít/Cái). Ghi chú: `export_price` = giá bán (fallback pre-FIFO), KHÔNG phải giá vốn FIFO thật (phiếu legacy chưa từng chạy FIFO) → cột "Đơn giá vốn" chỉ mang tính test; phiếu tạo mới finalize sẽ có giá vốn FIFO đúng.

### Checkpoint — 2026-08-21 (fix bảng hàng hoá PXH không hiện thông số)
Vừa hoàn thành: **9.22 F1+F2** — sửa 2 bug code khiến bảng hàng hoá phiếu loại 21 trống: (1) thêm loại 21 vào cờ is_sale/show_allocated (trước bị ẩn hết cột giá vì list bê nguyên ERP thiếu 21); (2) fallback snapshot coi chuỗi rỗng là thiếu (ĐVT/mã/tên rơi đúng về bảng units/products thay vì hiện "—"). Lint PASS.
Đang làm dở: (không)
Bước tiếp theo: user reload localhost:3000/finance/product-exports/34580 để xem bảng hàng hoá đã đủ cột (giá bán/sau giảm/VAT/kho kế toán). Cột "Đơn giá vốn" chỉ hiện nếu user có quyền "Xem giá vốn hàng hoá" (BE gate). Sau đó QA phiếu tạo mới thật để soi giá vốn FIFO.
Blocked: (không)

### Checkpoint — 2026-08-21 (backfill giá test phiếu 34580 — F3)
Vừa hoàn thành: **9.22 F3** — user chọn (b), đã backfill giá test cho phiếu 34580 trên erp_hrm_check theo đúng công thức ProductExportService (3 dòng PED + 3 dòng PEDA kho kế toán id=3). Verify computed khớp: 35.6tr→38.448tr sau VAT, ĐVT fallback ra Bộ/Lít/Cái (fix $pick chạy đúng). Bảng hàng hoá màn chi tiết PXH giờ hiện đủ cột như ERP.
Đang làm dở: (không)
Bước tiếp theo: user reload trình duyệt xem kết quả; QA thêm phiếu tạo mới để soi giá vốn FIFO thật.
Blocked: (không)

### 9.23 Màn "Đề nghị xuất kho" hiện MỌI loại (parity ERP — user chốt 2026-08-21)
Yêu cầu: "đề nghị xuất kho lấy toàn bộ giống bên erp không để filter loại" (screenshot màn `warehouse-export-requests` chỉ hiện 3 dòng loại 20/21).
Root cause: giống 9.19 — `WarehouseExportRequestController::scopedQuery()` khoá cứng `type IN (20,21) AND emplement_contract_type=Contract`. Bảng `warehouse_export_requests` thực có 30.955 dòng / 15 loại (3,4,6,7,9,10,12,14,15,17,18,19,20,21,99) nhưng bị lọc còn 3.
- [x] **P1 BE Entity** `WarehouseExportRequest`: thêm `TYPE_NAMES` đầy đủ 1-99 (khớp `ProductExportRequest::TYPE_NAMES`), `getTypeName()` dùng map + fallback null, thêm `getAllTypesForFilter()`.
- [x] **P2 BE Controller** `WarehouseExportRequestController::scopedQuery()`: BỎ filter `type IN (20,21)` + `emplement_contract_type=Contract`. Giữ phân quyền 4 cấp trên `created_by` + ẩn nháp người khác. Thêm method `typeOptions()`.
- [x] **P3 BE Route**: thêm `GET /assign/warehouse-export-requests/type-options` ĐẶT TRƯỚC `/{id}`.
- [x] **P4 FE** `pages/finance/warehouse-export-requests/index.vue`: `typeOptions` static [20,21] → `[]` nạp động qua `fetchTypeOptions()` (gọi `assign/warehouse-export-requests/type-options`) trong `mounted`.
- [x] **P5 Test** tinker verify scopedQuery trả ~30.955 dòng; `php -l` PASS.

### Checkpoint — 2026-08-21 (Đề nghị xuất kho hiện mọi loại — parity ERP)
Vừa hoàn thành: **9.23** — bỏ filter cứng loại 20/21 + emplement_contract_type ở `WarehouseExportRequestController::scopedQuery`; màn "Danh sách đề nghị xuất kho" giờ hiện toàn bộ `warehouse_export_requests` như ERP. Entity thêm TYPE_NAMES 1-99 + getAllTypesForFilter; endpoint mới `/type-options`; FE nạp filter loại động (fetchTypeOptions). Verify: bảng 30.955 dòng (trước hiện 3), filter 22 loại, getTypeName(14)="Xuất bán hãng"/(99)="Xuất khác". Gỡ import Contract thừa. `php -l` PASS.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload localhost:3000/finance/warehouse-export-requests xem danh sách đầy đủ + build/QA FE.
Blocked: (không)

### 9.24 Cột "Số hợp đồng" hiện cho MỌI loại HĐ (user báo 2026-08-21: "không hiện được số hợp đồng của hd hãng à")
Root cause: sau 9.23 màn hiện mọi loại, nhưng cột "Số hợp đồng" chỉ bind `emplement_contract_code` (snapshot chỉ có ở loại 19/20/21). HĐ hãng (14/15) lưu ở `firm_contract_id`, SC-BD (17) ở `wr_service_contract_id` → không snapshot code → cột trống. (ERP list gốc KHÔNG có cột này — cột HRM tự thêm.)
- [x] **T1 BE Entity** `WarehouseExportRequest`: thêm relation `firmContract` (belongsTo `TpFirmContract`, firm_contracts) + `wrServiceContract` (belongsTo `TpWrServiceContract`, wr_service_contracts).
- [x] **T2 BE Controller**: eager-load `firmContract:id,code` + `wrServiceContract:id,code` ở `index()` và `show()`.
- [x] **T3 BE Resource** `WarehouseExportRequestResource`: thêm `resolveContractDisplay()` hợp nhất số HĐ theo loại (19/20/21=emplement snapshot→`is_hrm=true` link nội bộ; 14/15=firm code; 17=wr code) → trả `contract_id/contract_code/is_hrm_contract`.
- [x] **T4 BE Filter**: mở rộng filter `contract_code` (index) tìm cả `firmContract`/`wrServiceContract` code, không chỉ emplement.
- [x] **T5 FE** `index.vue`: đổi cột key `emplement_contract_code`→`contract_code`; template `#cell-contract_code` chỉ link `/assign/contracts/{emplement_contract_id}` khi `is_hrm_contract`, còn lại hiện text.
- [x] **T6 Test** tinker verify: 14→firm code, 15→firm code, 17→wr code, 20/21→emplement code (is_hrm=true); filter "MH07-2026-014" khớp 1 phiếu loại 14.

### Checkpoint — 2026-08-21 (cột "Số hợp đồng" hiện mọi loại HĐ)
Vừa hoàn thành: **9.24** — cột "Số hợp đồng" giờ hiện cho HĐ hãng (14/15, từ `firm_contracts.code`), SC-BD (17, `wr_service_contracts.code`) và HĐ HRM (19/20/21, snapshot emplement — chỉ loại này link nội bộ vì có trang chi tiết HRM). Thêm 2 relation firmContract/wrServiceContract (eager-load id+code, không N+1), `resolveContractDisplay()` ở Resource trả `contract_code/contract_id/is_hrm_contract`, mở rộng filter số HĐ. FE bind `contract_code`, link có điều kiện `is_hrm_contract`. Verify tinker: 14/15→firm, 17→wr, 20/21→emplement(is_hrm=true); filter khớp HĐ hãng.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn Đề nghị xuất kho — cột "Số hợp đồng" hiện đủ mọi loại.
Blocked: (không)

### 9.25 Cột "Số hợp đồng" hiện mọi loại HĐ — áp dụng cho PXH + YCXH (user báo 2026-08-21: "sửa tương tự phiếu xuất hàng, yêu cầu xuất hàng")
Cùng root cause 9.24: màn Phiếu xuất hàng (`product-exports`) và Yêu cầu xuất hàng (`product-export-requests`) chỉ bind `emplement_contract_code` (snapshot chỉ có ở 19/20/21) → HĐ hãng (14/15) + SC-BD (17) trống. Cả 2 bảng đều có sẵn cột `firm_contract_id` / `wr_service_contract_id`.
- [x] **T1 Model** `ProductExport` + `ProductExportRequest`: thêm relation `firmContract` (TpFirmContract) + `wrServiceContract` (TpWrServiceContract).
- [x] **T2 Controller** cả 2: eager-load `firmContract:id,code` + `wrServiceContract:id,code` ở index() và show(); mở rộng filter `contract_code` tìm cả firm/wr code.
- [x] **T3 Resource** `ProductExportResource` + `ProductExportRequestResource`: thêm `resolveContractDisplay()` (dùng chung logic 9.24) → trả `contract_id/contract_code/is_hrm_contract`. YCXH đã có is_hrm_contract → chuyển sang dùng contract_code hợp nhất.
- [x] **T4 FE list** `product-exports/index.vue` + `product-export-requests/index.vue`: cột key `emplement_contract_code`→`contract_code`, template link có điều kiện `is_hrm_contract`.
- [x] **T5 FE chi tiết + in**: `product-exports/_id/index.vue`, `product-exports/_id/print.vue`, `product-export-requests/_id/index.vue` — bind `contract_code` + `is_hrm_contract`.
- [x] **T6 Test** tinker verify cả PXH + YCXH: 14/15→firm, 17→wr, 20/21→emplement(is_hrm=true). `php -l` 6 file PASS.

### Checkpoint — 2026-08-21 (cột "Số hợp đồng" PXH + YCXH mọi loại HĐ)
Vừa hoàn thành: **9.25** — port fix 9.24 sang Phiếu xuất hàng + Yêu cầu xuất hàng. Cột "Số hợp đồng" (list + chi tiết + in) giờ hiện HĐ hãng (14/15, firm_contracts), SC-BD (17, wr_service_contracts), HĐ HRM (19/20/21, snapshot emplement — chỉ loại này link nội bộ). Mỗi màn: +2 relation, eager-load id+code (không N+1), resolveContractDisplay ở Resource, mở rộng filter số HĐ, FE bind contract_code + link theo is_hrm_contract. Verify tinker cả 2 màn khớp; php -l 6 file PASS.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload 2 màn PXH/YCXH kiểm tra cột số HĐ hiện đủ loại.
Blocked: (không)

### 9.26 Màn CHI TIẾT cả 3 loại phiếu cũng hiện số HĐ mọi loại (user báo 2026-08-21: "màn chi tiết ... cũng phải hiện")
Sót ở 9.24: khi làm đề nghị xuất kho chỉ sửa cột list, màn chi tiết `warehouse-export-requests/_id/index.vue` vẫn bind `emplement_contract_code` (trống với HĐ hãng/SC-BD). PXH/YCXH detail đã sửa ở 9.25.
- [x] **T1** `warehouse-export-requests/_id/index.vue`: bind `contract_code` + link theo `is_hrm_contract` (BE show() đã eager-load firm/wr + dùng Resource từ 9.24 → có sẵn contract_code).
- [x] **T2 Test** tinker verify full toArray của cả 3 Resource cho phiếu loại 14: đều trả `contract_code` (firm code) + `is_hrm_contract=false`. (PXH detail + print, YCXH detail đã đúng từ 9.25.)

### Checkpoint — 2026-08-21 (màn chi tiết 3 loại phiếu hiện số HĐ mọi loại)
Vừa hoàn thành: **9.26** — sửa nốt màn chi tiết đề nghị xuất kho (`warehouse-export-requests/_id/index.vue`) bind `contract_code`+`is_hrm_contract` (trước còn sót từ 9.24, chỉ sửa list). Verify tinker: full Resource output của cả 3 màn (ĐNXK id31049, PXH id34577, YCXH id35668 — đều loại 14) trả contract_code = mã HĐ hãng, is_hrm_contract=false. Giờ cả list + chi tiết + in của 3 loại phiếu đều hiện số HĐ cho mọi loại HĐ (hãng/SC-BD/HRM).
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn chi tiết đề nghị xuất kho kiểm tra số HĐ hiện.
Blocked: (không)

### 9.27 Cột "Phiếu xuất kho" ở màn Phiếu xuất hàng bấm link sang ERP (user báo 2026-08-21: "danh sách phiếu xuất kho khi bấm vào link sang erp")
Cột `warehouse_export_code` (PXK-xxx) ở list Phiếu xuất hàng đang là text thường, không bấm được. Cần deep-link sang trang chi tiết phiếu xuất kho ERP (route `warehouseExport.show` = `/admin/warehouse/warehouse_exports/{id}/show`). Detail đã có link nhưng `goErpWarehouseExportList()` trỏ về LIST ERP thay vì đúng phiếu.
- [x] **T1 FE list** `product-exports/index.vue`: đổi cell `#cell-warehouse_export_code` thành `<a>` bấm được (khi có `warehouse_export_id` + code); thêm method `goErpWarehouseExport(item)` mở `${tp_url}/admin/warehouse/warehouse_exports/${warehouse_export_id}/show` (strip trailing slash, toast lỗi nếu thiếu TP_URL).
- [x] **T2 FE detail** `product-exports/_id/index.vue`: sửa `goErpWarehouseExportList()` deep-link đúng phiếu qua `detail.warehouse_export_id` (fallback về list ERP nếu thiếu id).
- [x] **T3 Verify** Resource đã trả sẵn `warehouse_export_id`+`warehouse_export_code`; tinker: 29.934/34.436 product_exports có warehouse_export_id, sample id34581→PXK-30295; `tp_url` map từ `TP_URL` ở nuxt.config.

### Checkpoint — 2026-08-21 (link "Phiếu xuất kho" sang ERP)
Vừa hoàn thành: **9.27** — cột "Phiếu xuất kho" (PXK) ở list Phiếu xuất hàng giờ bấm được, mở đúng trang chi tiết phiếu xuất kho bên ERP (`/admin/warehouse/warehouse_exports/{warehouse_export_id}/show`). Sửa luôn detail PXH (`goErpWarehouseExportList` trước trỏ về LIST ERP → nay deep-link đúng phiếu, fallback list nếu thiếu id). Dùng `process.env.tp_url` (map từ TP_URL), strip trailing slash, toast "Chưa cấu hình địa chỉ ERP (TP_URL)" nếu thiếu. Verify: 29.934 phiếu có warehouse_export_id.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload list Phiếu xuất hàng, bấm mã PXK kiểm tra mở đúng phiếu bên ERP.
Blocked: (không)

### 9.28 Mục menu "Phiếu xuất kho" (nhóm Xuất hàng) bấm sang DANH SÁCH phiếu xuất kho ERP (user làm rõ 2026-08-21 kèm ảnh menu: "danh sách phiếu xuất kho click vào thì link sang ds phiếu xuất kho bên erp")
Làm rõ ý 9.27: không phải cột PXK trên list PXH, mà là MỤC MENU "Phiếu xuất kho" trong nhóm "Xuất hàng" (chưa có màn HRM) → click mở danh sách phiếu xuất kho bên ERP. Menu đã hỗ trợ `erpPath` (mở tab mới `ERP_URL + erpPath`) nhưng mục này bỏ trống nên báo "Tính năng đang phát triển".
Root cause phụ: `process.env.ERP_URL` được các consumer menu (`SubsystemHubOverview.vue`, `SaleHubSidebar.vue`, `training-components/Sidebar.vue`) dùng để ghép erpPath NHƯNG chưa được whitelist trong `nuxt.config.js env` (chỉ có `tp_url`) → ERP_URL = undefined ở client → mọi mục erpPath (admin logs, api-keys…) đang mở `undefined/...`. 
- [x] **T1 Menu** `components/subsystem-menu/finance.js`: mục "Phiếu xuất kho" thêm `erpPath: '/admin/warehouse/warehouse_exports?type=all'` (route ERP `warehouseExport.index`, prefix `admin/warehouse/warehouse_exports`; query `type=all` để mở danh sách đầy đủ). hub.js transform truyền erpPath từ subItem → screen.
- [x] **T2 Config** `nuxt.config.js` env: expose `ERP_URL: process.env.ERP_URL || process.env.TP_URL` (fallback TP_URL vì cùng trỏ app ERP) — fix luôn các mục erpPath khác đang undefined.
- [ ] **T3 Test** (chờ user) restart nuxt (đổi env cần rebuild), mở menu Xuất hàng → click "Phiếu xuất kho" → mở tab ERP `/admin/warehouse/warehouse_exports`.

### Checkpoint — 2026-08-21 (menu "Phiếu xuất kho" → danh sách ERP)
Vừa hoàn thành: **9.28** — mục menu "Phiếu xuất kho" (nhóm Xuất hàng) giờ deep-link sang DANH SÁCH phiếu xuất kho ERP (`/admin/warehouse/warehouse_exports`) qua cơ chế `erpPath`. Phát hiện + fix root cause phụ: `ERP_URL` chưa được whitelist trong nuxt.config env (các mục erpPath toàn hệ thống đang mở `undefined/...`) → thêm `ERP_URL: process.env.ERP_URL || process.env.TP_URL`. (Phân biệt với 9.27: 9.27 là cột mã PXK trên list Phiếu xuất hàng → mở CHI TIẾT 1 phiếu; 9.28 là mục MENU → mở DANH SÁCH.)
Đang làm dở: (không)
Bước tiếp theo: (chờ user) restart nuxt (đổi env cần rebuild) rồi test click menu.
Blocked: (không)

### 9.29 Cột "Mã YCXH" ở list Đề nghị xuất kho link tới chi tiết YCXH bên HRM (user báo 2026-08-21 kèm ảnh: "mã ycxh gắn link đến chi tiết phiếu tương ứng bên hrm")
Cột `product_export_request_code` (PYCXH-xxx) ở màn Đề nghị xuất kho đang text thường → gắn link nội bộ sang trang chi tiết Yêu cầu xuất hàng HRM.
- [x] **T1 FE** `warehouse-export-requests/index.vue`: cell `#cell-product_export_request_code` thành `<nuxt-link :to="/finance/product-export-requests/{product_export_request_id}" target="_blank">` (khi có id + code); else text. Resource đã trả sẵn `product_export_request_id` (line 35) + code (line 36); trang chi tiết `product-export-requests/_id/index.vue` đã tồn tại.

### Checkpoint — 2026-08-21 (Mã YCXH → chi tiết YCXH HRM)
Vừa hoàn thành: **9.29** — cột "Mã YCXH" ở list Đề nghị xuất kho giờ là link nội bộ mở trang chi tiết Yêu cầu xuất hàng bên HRM (`/finance/product-export-requests/{id}`, tab mới). Không đụng BE (Resource sẵn trả product_export_request_id).
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn Đề nghị xuất kho, bấm mã PYCXH kiểm tra mở đúng chi tiết YCXH.
Blocked: (không)

### 9.30 Bổ sung trường "Vận chuyển" cho MỌI loại có giao hàng + siết validate ngày mượn (loại 3) — khớp ERP (user 2026-08-24: "1. tất cả, 2 có")
Bối cảnh: form Tạo/Sửa Yêu cầu xuất hàng trước chỉ hiện "Vận chuyển"/"Số km" cho loại HĐ (20/21). ERP bắt Vận chuyển cho mọi loại `getHasDeliveryTypes` khi KHÔNG xuất thẳng; xuất thẳng chỉ có ở 20/21 nên các loại nhập tay (3/6/7/12/18/99) luôn cần Vận chuyển. Đồng thời loại 3 (Xuất mượn) ERP bắt ngày mượn ≥ hôm nay, ngày trả > ngày mượn (đều required khi gửi duyệt).
- [x] **T1 Model** `ProductExportRequest.php`: thêm `HAS_DELIVERY_TYPE_IDS = [3,6,7,12,18,99,20,21]` + `getHasDeliveryTypes()` (port ERP giao với loại HRM hỗ trợ).
- [x] **T2 BE rules** `ProductExportRequestController::rulesForType`: thêm `$hasDelivery`; Vận chuyển nullable ở nháp cho mọi loại có giao hàng; gửi duyệt: `transition_type = required_unless:is_export_direct,1|in:1,2,3`, `total_km_expected = required_if:transition_type,2`; loại 3 `expected_borrow_date=required|date|after_or_equal:today`, `return_date=required|date|after:expected_borrow_date`.
- [x] **T3 BE service createManual** `ProductExportRequestService.php`: `fill([...])` thêm `transition_type` (fallback 1 vì cột NOT NULL default 1) + `total_km_expected`.
- [x] **T4 BE service updateFromRequest**: nhánh `!$isContractType` (nhập tay) cũng lưu `transition_type` (fallback 1) + `total_km_expected` (trước chỉ lưu ở nhánh HĐ).
- [x] **T5 FE form** `ProductExportRequestForm.vue`: thêm hằng `DELIVERY_TYPES=[3,6,7,12,18,99,20,21]` + computed `needTransition` (loại có giao hàng && is_export_direct!==1); tách Vận chuyển+Số km khỏi block `isContractType` sang block `needTransition` riêng (Vận chuyển luôn `required`); Xuất thẳng/Cần lắp đặt vẫn chỉ ở 20/21.
- [x] **T6 FE validate** `validateForm`: đổi điều kiện Vận chuyển từ `isContractType && !is_export_direct` → `needTransition`; thêm validate loại 3 (ngày mượn required + ≥ hôm nay ISO, ngày trả required + > ngày mượn); label ngày mượn/trả gắn `required` + hiện lỗi inline.
- [x] **T7 FE payload**: `transition_type`/`total_km_expected` gửi khi `needTransition` (trước chỉ khi `isContractType`); is_export_direct/need_repair vẫn chỉ gửi cho 20/21.
- [x] **T7b FE fix bug** `ProductExportRequestForm.vue`: select "Vận chuyển" rỗng ở loại nhập tay — options chỉ được nạp trong `loadContractLines` (loại HĐ) và nhánh `isContractType` của `applyInitialData`; `onTypeChange` còn reset `= []`. Thêm helper `seedTransitionOptions()` (3 hằng TRANSITION_TYPES), gọi trong `onTypeChange` (Tạo) + `applyInitialData` cho mọi loại (Sửa).
- [ ] **T8 Test** (chờ user) Tạo phiếu loại 3/6/7/12/18/99 → hiện Vận chuyển bắt buộc; loại 3 nhập ngày mượn quá khứ / ngày trả ≤ ngày mượn → chặn; loại 20/21 tick Xuất thẳng → ẩn Vận chuyển, bỏ required.

### Checkpoint — 2026-08-24 (Vận chuyển cho mọi loại có giao hàng + validate ngày mượn)
Vừa hoàn thành: **9.30** — port rule ERP `getHasDeliveryTypes`: trường "Vận chuyển" (+ "Số km" khi Công ty vận chuyển) giờ áp cho MỌI loại nhập tay có giao hàng (3/6/7/12/18/99), không chỉ HĐ 20/21; bắt buộc khi không xuất thẳng ở cả FE lẫn BE. Loại 3 (Xuất mượn) siết ngày mượn ≥ hôm nay + ngày trả > ngày mượn (required khi gửi duyệt). Sửa 3 file: Model (HAS_DELIVERY_TYPE_IDS+getHasDeliveryTypes), Controller rulesForType, Service createManual+updateFromRequest; FE ProductExportRequestForm (DELIVERY_TYPES, needTransition, tách block template, validateForm, payload). php -l sạch cả 3 file BE.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) restart nuxt + reload form, test T8 (tạo phiếu các loại kiểm tra Vận chuyển + ngày mượn).
Blocked: (không)

### 9.31 Màn "Lập đề nghị xuất kho" ẩn/hiện field theo loại xuất — khớp ERP (user 2026-08-24: "đề nghị xuất kho tuỳ loại xuất mà hiển thị form tương ứng cho đúng. Kiểm tra với loại xuất mượn")
Bối cảnh: form Lập ĐNXK (`warehouse-export-requests/create.vue`, tạo từ 1 YCXH) LUÔN render panel "Khách hàng & giao hàng" bất kể loại → với loại 3 (Xuất mượn) panel toàn "—" (bug ảnh user). ERP `WarehouseExportRequest.has_customer = type ∈ {1,2,8,14}` (loại bán có KH) → loại nội bộ (3/6/7/18/99) KHÔNG hiện panel. HRM tương ứng: 12 (hàng gửi), 20/21 (HĐ HRM) mới có KH trên YCXH.
- [x] **T1 BE** `WarehouseExportRequestController::warehouseExportData`: thêm `'type' => (int) $req->type` vào payload `request` (trước không trả → FE không có gì để gate).
- [x] **T2 FE** `warehouse-export-requests/create.vue`: thêm computed `hasCustomer = [12,20,21].includes(Number(info.type))` (port ERP has_customer, HRM-adapted); gate panel "Khách hàng & giao hàng" bằng `v-if="hasCustomer"`. Loại 3 → ẩn panel; Kho xuất + KD chịu vận chuyển + ghi chú + file + danh sách hàng vẫn hiện (khớp ERP type 3).
- [ ] **T3 Test** (chờ user) mở Lập ĐNXK từ YCXH loại 3 (Xuất mượn) → KHÔNG còn panel "Khách hàng & giao hàng" rỗng; từ YCXH loại 20/21/12 → vẫn hiện panel KH.

### Checkpoint — 2026-08-24 (ĐNXK ẩn panel KH theo loại xuất)
Vừa hoàn thành: **9.31** — màn Lập đề nghị xuất kho giờ ẩn panel "Khách hàng & giao hàng" cho loại xuất không có KH (3 xuất mượn, 6/7 điều chuyển, 18 sản xuất, 99 khác), chỉ hiện với loại có KH (12/20/21) — khớp ERP `has_customer`. BE `warehouseExportData` trả thêm `type`; FE gate bằng computed `hasCustomer`. php -l BE sạch.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn Lập ĐNXK từ YCXH loại 3 kiểm tra panel KH đã ẩn.
Blocked: (không)

### 9.31b Chuẩn hoá loại 18 (Xuất sản xuất) trên màn Lập ĐNXK — khớp ERP (user 2026-08-24: "chuẩn hoá nốt loại 18 sản xuất")
Bối cảnh: ERP form ĐNXK ẩn "KD chịu vận chuyển" cho loại 18/19 (`ng-if="form.type != 18 && form.type != 19"`) — xuất sản xuất là nội bộ, không giao khách nên không có KD chịu phí VC. Panel Khách hàng đã ẩn sẵn ở 9.31 (18 không thuộc hasCustomer). Kho xuất/Ghi chú/File/Danh sách hàng vẫn giữ (ERP vẫn hiện cho 18).
- [x] **T1 FE** `warehouse-export-requests/create.vue`: thêm computed `showBearShipping = ![18,19].includes(Number(info.type))`; gate checkbox "KD chịu vận chuyển" bằng `v-if="showBearShipping"`; lưới Kho xuất đổi `:class="{ 'cols-2': showBearShipping }"` → khi ẩn checkbox, Kho xuất chiếm full width (loại 18 chỉ còn 1 cột kho).
- [ ] **T2 Test** (chờ user) mở Lập ĐNXK từ YCXH loại 18 → KHÔNG còn checkbox "KD chịu vận chuyển", Kho xuất full width, không panel KH; loại khác (3/6/7/12/20/21/99) vẫn hiện checkbox như cũ.

### Checkpoint — 2026-08-24 (chuẩn hoá loại 18 màn ĐNXK)
Vừa hoàn thành: **9.31b** — màn Lập ĐNXK với loại 18 (Xuất sản xuất) giờ ẩn "KD chịu vận chuyển" (khớp ERP, xuất nội bộ không giao khách), Kho xuất co full width. Kết hợp 9.31: loại 18 chỉ còn Kho xuất + Ghi chú + File + Danh sách hàng (không panel KH, không KD chịu VC). Chỉ sửa FE (computed showBearShipping + gate), không đụng BE.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn Lập ĐNXK từ YCXH loại 18 kiểm tra.
Blocked: (không)

### 9.31c Chuẩn hoá màn CHI TIẾT đề nghị xuất kho theo loại xuất — khớp ERP (user 2026-08-24: "chi tiết đề nghị xuất kho vẫn chưa chuẩn hoá")
Bối cảnh: màn chi tiết ĐNXK (`warehouse-export-requests/_id/index.vue`, khác màn tạo `create.vue` đã sửa ở 9.31/9.31b) vẫn LUÔN hiện panel "Khách hàng & giao hàng" (rỗng với loại 3) + dòng "KD chịu ship" (vô nghĩa với loại 18). BE Resource `WarehouseExportRequestResource` đã trả sẵn `type` (dòng 33) → không cần sửa BE.
- [x] **T1 FE** `_id/index.vue`: thêm 2 computed `hasCustomer = [12,20,21].includes(Number(detail.type))` + `showBearShipping = ![18,19].includes(Number(detail.type))`; gate panel "Khách hàng & giao hàng" bằng `v-if="hasCustomer"`; gate dòng "KD chịu ship" bằng `v-if="showBearShipping"`. Đồng bộ đúng logic màn tạo.
- [ ] **T2 Test** (chờ user) mở chi tiết ĐNXK loại 3 → không panel KH; loại 18 → không dòng "KD chịu ship"; loại 12/20/21 → vẫn hiện panel KH.

### Checkpoint — 2026-08-24 (chuẩn hoá màn chi tiết ĐNXK)
Vừa hoàn thành: **9.31c** — màn chi tiết ĐNXK giờ ẩn panel "Khách hàng & giao hàng" cho loại không có KH (3/6/7/18/99) và ẩn dòng "KD chịu ship" cho loại nội bộ 18/19 — đồng bộ với màn tạo (9.31/9.31b). Chỉ sửa FE (2 computed + 2 v-if), BE Resource đã có sẵn `type`.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn chi tiết ĐNXK các loại kiểm tra.
Blocked: (không)

### 9.31d Chỉnh nhãn/ẩn field rỗng màn chi tiết ĐNXK (user 2026-08-24: "TG nhận, TG duyệt là gì mà sao không thấy hiện; KD chịu ship -> KD chịu vận chuyển")
- [x] **T1 FE** `_id/index.vue`: đổi nhãn "KD chịu ship" → "KD chịu vận chuyển" (khớp màn tạo). "TG nhận"/"TG duyệt" đổi thành "Thời gian nhận"/"Thời gian duyệt" + `v-if="detail.received_time"`/`v-if="detail.approved_time"` — 2 cột này chỉ set khi thủ kho xử lý phiếu bên ERP (luồng HRM không set), phiếu mới tạo luôn rỗng nên trước hiện "—" gây khó hiểu; giờ chỉ hiện khi đã có giá trị.
- Giải thích cho user: màn chi tiết là read-only nên field tick (KD chịu vận chuyển) hiển thị "Có/Không" thay vì checkbox — đúng theo bản chất trang xem.

### Checkpoint — 2026-08-24 (nhãn + ẩn field rỗng chi tiết ĐNXK)
Vừa hoàn thành: **9.31d** — đổi nhãn "KD chịu ship"→"KD chịu vận chuyển", "TG nhận/TG duyệt"→"Thời gian nhận/duyệt" chỉ hiện khi có (2 cột này set từ luồng ERP, HRM để trống). Chỉ sửa FE nhãn + v-if.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn chi tiết kiểm tra.
Blocked: (không)

### 9.32 Fix ERP lỗi "Column 'brand_id' cannot be null" khi Lưu&xuất phiếu xuất từ ĐNXK HRM (user 2026-08-24: phiếu warehouse_exports/30303/edit)
Bối cảnh: ERP `WarehouseExportsController@update` build `WarehouseExportLot` với `$l->brand_id = $product->brand_id` ($product = dòng ĐNXK). `warehouse_export_lots.brand_id` NOT NULL → fail. Root cause: HRM `ProductExportRequestService` khi insert `product_export_request_details` (cả path nhập tay `insertManualLines` lẫn path HĐ `createFromContract`) KHÔNG ghi `model_id`/`brand_id` (chỉ ghi model_name/brand_name) → null lan xuống ĐNXK qua `buildDetailAttributes` → ERP nhận null. DB xác nhận: ĐNXK 31063 detail 77387 (product 48326) brand_id=null/model_id=0, trong khi products.48326 có model_id=36516/brand_id=1300 (VELTRON).
- [x] **T1 BE** `ProductExportRequestService`: thêm helper `resolveModelBrand(productIds)` tra `products` (nguồn chuẩn). `insertManualLines` + `createFromContract` ghi thêm `model_id`/`brand_id` (ưu tiên payload/dòng HĐ, fallback products).
- [x] **T2 BE** `WarehouseExportRequestService::buildDetailAttributes` (chốt cuối trước ERP): nếu YCXH thiếu `brand_id`/`model_id` → tra bù từ `products`. Defense-in-depth cho YCXH cũ.
- [x] **T3 Data** Backfill records đang kẹt trên `erp_hrm_check`: UPDATE `product_export_request_details` (15 dòng) + `warehouse_export_request_details` (4 dòng) SET brand_id/model_id từ products WHERE brand_id NULL hoặc model_id=0 và products.brand_id NOT NULL. Verify ĐNXK 31063/detail 77387 → brand_id=1300/model_id=36516; còn 0 dòng null.
- [ ] **T4 Test** (chờ user) mở lại `warehouse_exports/30303/edit#/chung` → Lưu&xuất phải thành công (hết lỗi brand_id).

### Checkpoint — 2026-08-24 (fix brand_id null lan từ HRM sang ERP)
Vừa hoàn thành: **9.32** — chặn root cause null `model_id`/`brand_id` ở HRM (2 path insert YCXH + fallback ĐNXK build), backfill 19 dòng data đang kẹt trên erp_hrm_check. Lint sạch cả 2 service.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload phiếu xuất 30303 bên ERP, bấm Lưu&xuất kiểm tra hết lỗi.
Blocked: (không)

### 9.33 Ẩn khối "Khách hàng & giao hàng" màn CHI TIẾT phiếu xuất hàng theo loại — khớp ERP (user 2026-08-24: "phần thông tin chung ... đang hiện khách hàng" ở loại Xuất mượn)
Bối cảnh: màn chi tiết PXH (`finance/product-exports/_id/index.vue`) LUÔN render subpanel "Khách hàng & giao hàng", kể cả loại Xuất mượn (3) không gắn KH → rỗng/thừa. ERP ẩn khối này qua cờ `has_customer = [1,2,8,12,14,16,17].includes(type)` (ProductExport JS class). Song song với 9.31c (màn ĐNXK).
- [x] **T1 BE** `Modules/Assign/Transformers/ProductExportResource.php`: thêm cờ `has_customer = in_array($type, [1,2,8,12,14,16,17,21])` (mirror ERP + loại HRM 21 xuất bán HĐ có KH), trả cạnh `is_sale`/`show_cost`. Lint sạch.
- [x] **T2 FE** `finance/product-exports/_id/index.vue`: bọc subpanel "Khách hàng & giao hàng" bằng `v-if="detail.has_customer"`.
- [ ] **T3 Test** (chờ user) mở chi tiết PXH loại Xuất mượn (3) → không khối KH; loại bán/KM/bảo hành (1,2,8,14,16,17,21) → vẫn hiện.

### Checkpoint — 2026-08-24 (ẩn khối KH màn chi tiết PXH theo loại)
Vừa hoàn thành: **9.33** — màn chi tiết phiếu xuất hàng ẩn khối "Khách hàng & giao hàng" cho loại không gắn KH (mượn 3, trả NCC 4, điều chuyển, ghép/tách, sản xuất 20…), khớp cờ `has_customer` của ERP. Thêm cờ BE (ProductExportResource) + 1 v-if FE.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload màn chi tiết PXH loại Xuất mượn kiểm tra khối KH đã ẩn.
Blocked: (không)

### 9.34 Hiện checkbox "Xuất thẳng" cho loại điều chuyển & mọi loại (trừ mượn 3 / KM hãng 15) — khớp ERP (user 2026-08-24: "loại xuất điều chuyển kho nội bộ không thấy checkbox xuất thẳng, ERP vẫn có")
Bối cảnh: form YCXH (`product-export-requests/components/ProductExportRequestForm.vue`) khoá cứng "Xuất thẳng" theo `isContractType` (20/21) → điều chuyển 6/7 bị ẩn. ERP (`product_export_requests/form.blade.php:26`) hiện Xuất thẳng cho mọi loại TRỪ 3 (mượn) & 15 (KM hãng). BE HRM (`ProductExportRequestController` validate `nullable|boolean` + `ProductExportRequestService` store/update đọc generic) đã hỗ trợ sẵn is_export_direct cho mọi loại → chỉ sửa FE.
- [x] **T1 FE** thêm computed `showExportDirect = form.type != null && ![3,15].includes(type)` (mirror ERP).
- [x] **T2 FE** tách block: checkbox "Xuất thẳng" gate `showExportDirect`; radio "Cần lắp đặt" giữ gate `isContractType`; container hiện khi `showExportDirect || isContractType`.
- [x] **T3 FE** `showWarehouse`/`needWarehouse`: khi `is_export_direct===1` thì ẩn + bỏ bắt buộc Kho xuất cho MỌI loại (trước chỉ áp loại HĐ) — khớp "xuất thẳng = không qua kho".
- [x] **T4 FE** payload `onSubmitClick`: gửi `is_export_direct` khi `showExportDirect` (thay vì chỉ `isContractType`); `need_repair` vẫn theo `isContractType`.
- [ ] **T5 Test** (chờ user) tạo YCXH loại ĐC nội bộ (6) → thấy checkbox Xuất thẳng; tick → Kho xuất ẩn/không bắt buộc; Lưu → BE nhận is_export_direct=1. Loại mượn (3) → vẫn không có checkbox.

### Checkpoint — 2026-08-24 (Xuất thẳng cho điều chuyển giống ERP)
Vừa hoàn thành: **9.34** — form YCXH hiện checkbox "Xuất thẳng" cho mọi loại trừ mượn(3)/KM hãng(15) (mirror ERP `type != 3 && != 15`), thay vì chỉ 20/21; xuất thẳng ẩn+bỏ bắt buộc Kho xuất cho mọi loại; payload gửi is_export_direct theo showExportDirect. BE đã hỗ trợ sẵn, chỉ sửa FE (1 computed + tách block + 2 computed kho + payload).
Đang làm dở: (không)
Bước tiếp theo: (chờ user) tạo YCXH loại điều chuyển kiểm tra checkbox + hành vi ẩn kho.
Blocked: (không)

### 9.35 Bảng "Chi tiết hàng hoá" (nhập tay) form YCXH thiếu cột Đơn giá + Thành tiền cho loại mượn/điều chuyển — khớp ERP (user 2026-08-24: ảnh form tạo ERP loại điều chuyển vẫn có cột Đơn giá/Thành tiền)
Bối cảnh: bảng biến thể nhập tay `manualRows` (`ProductExportRequestForm.vue`, dùng loại 3/6/7/12/18/99) chỉ có cột SL xuất, thiếu Đơn giá + Thành tiền. ERP bảng mặc định (`product_export_requests/form.blade.php:1331-1404`, `ng-if="!form.has_parent" && type!=12`) LUÔN hiện Đơn giá (`product.price`) + Thành tiền (`product.total_amount = price×qty`) — rỗng thì "—", + dòng Tổng cộng (`sum_amount`). Dữ liệu HRM đã sẵn `price` trên mỗi row (map dòng 855/891). Chỉ sửa FE, giá readonly (không nhập tay, không đụng payload/BE).
- [x] **T1 FE** thêm 2 `<th>` "Đơn giá" + "Thành tiền" (text-right) sau "SL xuất", trước "Xoá".
- [x] **T2 FE** thêm 2 `<td>`: Đơn giá = `row.price` (hiện "—" khi 0/null giống numberOrHyphen); Thành tiền = `manualRowAmount(row)=price×qty`.
- [x] **T3 FE** thêm dòng "Tổng cộng" (computed `manualTotals`): tổng SL xuất + tổng Thành tiền; sửa colspan empty-state 8→10.
- [ ] **T4 Test** (chờ user) form YCXH loại điều chuyển/mượn → thấy cột Đơn giá + Thành tiền; đổi SL xuất → Thành tiền + Tổng cộng cập nhật; giá rỗng hiện "—".
Note: KHÔNG thêm cột "Tồn" (ERP có `can_export_qty`) vì manualRows chưa có dữ liệu tồn theo dòng — cần API tồn riêng, ngoài scope; làm sau nếu user yêu cầu.

### Checkpoint — 2026-08-24 (Đơn giá/Thành tiền bảng nhập tay YCXH)
Vừa hoàn thành: **9.35** — bảng Chi tiết nhập tay form YCXH thêm cột Đơn giá + Thành tiền + dòng Tổng cộng, khớp ERP (luôn hiện, "—" khi rỗng). FE-only, giá readonly từ row.price sẵn có.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) mở form YCXH loại điều chuyển/mượn kiểm tra 2 cột giá + tổng cộng.
Blocked: (không)

### 9.36 Màn CHI TIẾT YCXH — bảng "Danh sách hàng hoá" loại điều chuyển/mượn: bỏ Đã xuất/Đã trả, gộp 1 cột Số lượng, thêm Đơn giá + Thành tiền — khớp ERP (user 2026-08-24: ảnh chi tiết YCXH điều chuyển kho nội bộ khác ERP)
Bối cảnh: màn chi tiết YCXH (`product-export-requests/_id/index.vue`) cho loại KHÔNG bán (điều chuyển/mượn…) đang hiện SL cần + Đã xuất + Đã trả, thiếu Đơn giá/Thành tiền. ERP (`product_export_requests/show.blade.php:444-485`, khối `is_warehouse_transfer || type 7/12/18/19/99`) chỉ có 1 cột **Số lượng** (`product.qty`) + **Đơn giá** (`product.price`) + **Thành tiền** (`product.total_amount`) + dòng Tổng cộng (`sum_qty`/`sum_amount`). User: "đã xuất, đã trả giữ có tác dụng gì đâu, bỏ đi làm như erp". Dữ liệu `price` đã sẵn trên mỗi row (controller `show()` select price). Chỉ sửa FE.
- [x] **T1 FE** thead: tách `<template v-if="isSaleDetail">` (giữ SL cần/Đã xuất/Đã trả + 8 cột giá bán loại 21) vs `<template v-else>` (1 cột Số lượng + Đơn giá + Thành tiền).
- [x] **T2 FE** tbody: nhánh else render `formatNum(row.qty)` + `row.price` ("—" khi 0/null) + `rowAmount(row)=price×qty` ("—" khi 0).
- [x] **T3 FE** thêm dòng "Tổng cộng" cho loại thường (`v-if="!isSaleDetail && products.length"`): colspan6 + `nonSaleTotals.qty` + ô trống (Đơn giá) + `nonSaleTotals.amount`; empty-state colspan `isSaleDetail ? 17 : 9`.
- [x] **T4 FE** thêm method `rowAmount(row)` (price×qty) + computed `nonSaleTotals` (tổng qty + amount over products).
- [ ] **T5 Test** (chờ user) mở chi tiết YCXH loại điều chuyển kho nội bộ (6) → 1 cột Số lượng + Đơn giá + Thành tiền + Tổng cộng, không còn Đã xuất/Đã trả; loại bán HĐ (21) → vẫn đủ cụm giá bán.

### Checkpoint — 2026-08-24 (chi tiết YCXH điều chuyển: gộp Số lượng + thêm Đơn giá/Thành tiền)
Vừa hoàn thành: **9.36** — màn chi tiết YCXH loại không bán bỏ Đã xuất/Đã trả, gộp 1 cột Số lượng, thêm Đơn giá + Thành tiền + Tổng cộng, khớp ERP `show.blade.php`. FE-only (`_id/index.vue`): thead/tbody branch theo isSaleDetail + method rowAmount + computed nonSaleTotals. Loại bán 21 giữ nguyên 8 cụm giá.
Đang làm dở: (không)
Bước tiếp theo: (chờ user) reload chi tiết YCXH loại điều chuyển kho nội bộ kiểm tra bảng hàng hoá.
Blocked: (không)

### 9.37 Hoàn thiện YCXH loại 7 "Xuất điều chuyển kho chi nhánh" từ Phiếu yêu cầu chuyển hàng — khớp ERP (user 2026-08-24: ảnh form ERP type 7 có Gửi đến công ty/Kiểu nhập kho/Phiếu yêu cầu chuyển hàng; HRM đang thiếu)
Bối cảnh & scope (user chốt): "làm hết luồng bên YCXH thôi; yêu cầu nhập hàng cứ để tạo nhưng chưa làm tiếp luồng nhập ở phase này". Điều tra xác nhận:
- **Yêu cầu nhập hàng KHÔNG tạo ở bước YCXH** — ERP tạo trong `ProductExport::updateWarehouse()` (model PXH) khi finalize phiếu xuất hàng, đọc `export_company_id`/`kind_of_import`/`product_transfer_requests`/công ty người tạo từ row `product_export_requests`. Với type 7, PXH/phiếu xuất kho vẫn ở ERP (chỉ 20/21 sang HRM) → ERP tự tạo yêu cầu nhập, HRM KHÔNG viết. Chỉ cần HRM LƯU ĐÚNG 3 field trên row dùng chung.
- **Hàng hoá type 7 do BE tự suy ra từ phiếu chuyển** (ERP `syncProductTransferRequests`: xoá details cũ → sinh `product_export_request_details` từ `products` của phiếu chuyển + gán `product_transfer_requests.product_export_request_id`/status). FE hiển thị read-only, không nhập tay.
- HRM đã có sẵn: entity `product_transfer_requests` đầy đủ (Modules/Finance, list/form/detail/print/route/quyền); stub `createFromTransfer()` (`ProductExportRequestService.php:176`, TODO 5.6); `deleteCompletely` đã có guard gỡ link (`:427-437`).
- User duyệt: (1) Sửa YCXH type 7 → 3 field read-only; (2) GIỮ thông báo chéo công ty khi tiếp nhận phiếu chuyển; (3) bảng hàng read-only cột như bảng nhập tay (Mã/Tên/TH/Model/ĐVT/SL/Đơn giá/Thành tiền).

**BE (Modules/Assign):**
- [x] **T1** `ProductExportRequestController::rulesForType` type 7 (`$isTransfer`): draft → export_company_id/kind_of_import/product_transfer_requests nullable; full (status=2) → export_company_id required exists companies, kind_of_import required in:1,2, product_transfer_requests required array min:1 + `.*` exists product_transfer_requests,id. Bỏ rule bắt buộc `warehouse_id` cho type 7 (ERP validate :385 loại 7 khỏi yêu cầu kho). Rethrow ValidationException ở store/update.
- [x] **T2** `ProductExportRequestService::createFromTransfer()` viết thật (DB::transaction): lưu row type=7 + export_company_id + kind_of_import + company_id=export_company_id + dept/part người tạo + code PYCXH-. `assertTransferRequestsSameCreator` (kind_of_import=1 || is_export_direct → cùng created_by, ERP :667-678). `syncTransferRequests`: xoá details cũ, mỗi phiếu set product_export_request_id + status=1 + approver + approved_time, gộp products theo product_id-unit_id (cộng qty) → insert product_export_request_details (model_id/brand_id fallback resolveModelBrand, total_amount=qty*price). `notifyTransferRequestReceived` bắn thông báo chéo cho người tạo phiếu (status==2). Không ghi tab_products (mirror ERP flat details).
- [x] **T3** `editData()` type 7: trả export_company_id/kind_of_import + export_company_name + product_transfer_requests đã gắn (id/code) + hàng read-only qua nhánh non-contract `products`. `show()` type 7: thêm export_company_id/name + kind_of_import(+name) + product_transfer_requests. `updateFromRequest` type 7 → `updateTransfer`: 3 field read-only (chỉ sửa status/note/is_export_direct/transition_type/total_km), giữ nguyên details + link.
- [x] **T4** Endpoint riêng Assign `transferRequestOptions` (GET `/assign/product-export-requests/transfer-request-options`): trả phiếu status=2 + chưa gắn product_export_request_id + `canApprove()` (gate quyền + cùng công ty), kèm products {id,code,products[...]}. Route đã thêm.

**FE (hrm-client ProductExportRequestForm.vue):**
- [x] **T5** Bỏ 7 khỏi `MANUAL_TYPES` (còn 3/6/12/18/99); thêm hằng `BRANCH_TRANSFER_TYPE=7` + computed `isBranchTransfer`. `showWarehouse`/`needWarehouse` loại trừ type 7 (không Kho xuất). Nút "Thêm hàng hoá" (gate `isManualType`) tự ẩn.
- [x] **T6** 3 field type 7: Gửi đến công ty (V2BaseSelect từ `$store.state.companies` qua `loadCompanies`), Chọn kiểu nhập kho (1 Nhập thẳng/2 Nhập về kho), Phiếu yêu cầu chuyển hàng (modal mới `TransferRequestSearchModal` chọn 1+ phiếu, chips + xoá). Sửa → 3 field read-only (ro-value + label khoá `lockedExportCompanyLabel`/`lockedKindOfImportLabel`; merge company khoá vào options).
- [x] **T7** Bảng hàng hoá read-only type 7 (`transferDisplayLines`): gộp products các phiếu theo product_id-unit_id (cộng SL) → Mã/Tên/TH/Model/ĐVT/SL/Đơn giá/Thành tiền + Tổng cộng (`transferTotals`). Màn Sửa dùng `savedTransferLines` (từ detail đã lưu) khi phiếu chọn chưa kèm products.
- [x] **T8** Payload submit type 7: gửi export_company_id, kind_of_import, product_transfer_requests[] (KHÔNG gửi products). Validate FE: ≥1 phiếu (kể cả nháp), full → bắt buộc công ty + kiểu nhập; bỏ qua check products. Giữ transition_type/is_export_direct. snapshotSource gồm transfer ids (dirty-tracking).
- [ ] **T9 Test** (chờ user) tạo YCXH type 7: chọn công ty nhận + kiểu nhập + phiếu chuyển → hàng tự đổ read-only → Lưu → BE lưu 3 field + details từ phiếu chuyển + link phiếu; Sửa → 3 field read-only.

### Checkpoint — 2026-08-24
Vừa hoàn thành: 9.37 T1-T8 (BE + FE loại 7 "Xuất điều chuyển kho chi nhánh"). BE: validate/createFromTransfer/updateTransfer/editData/show/transferRequestOptions + route — lint sạch. FE: `ProductExportRequestForm.vue` tách type 7 khỏi nhập tay, thêm 3 field + bảng read-only gộp phiếu chuyển, payload {export_company_id, kind_of_import, product_transfer_requests[]}, khoá 3 field khi Sửa; modal mới `TransferRequestSearchModal.vue`.
Đang làm dở: (không)
Bước tiếp theo: T9 — user test luồng tạo/sửa YCXH type 7 trên UI.
Blocked:
Ngoài phạm vi phase này: luồng tạo Yêu cầu nhập hàng đích (ERP tự sinh downstream), phân bổ kho, hạch toán.

**Ngoài scope phase này:** tạo/nhận yêu cầu nhập hàng (ERP lo khi finalize PXH), phân bổ tồn, hạch toán.

Note nguồn ERP: `ProductExportRequestsController.php` (validate :391-397, store type7 :667-699/:837-867), `ProductExportRequest::syncProductTransferRequests()` :2021, `ProductExport::updateWarehouse()` :~1936 (tạo import request downstream).

### 9.38 Đồng bộ nhãn trạng thái 3 đối tượng theo ERP (user 2026-08-24)
Đối chiếu ERP↔HRM cả 3 bộ status. Kết quả: **YCXH** (ProductExportRequest 1-11) và **ĐNXK** (WarehouseExportRequest 1-7) nhãn ĐÃ khớp ERP y hệt → không sửa. Chỉ **PXH** (ProductExport) lệch.
- ERP PXH nhãn: 1=Đã hoàn thành, 3=Đang tạo, 12=Đang quyết toán, 13=Đã quyết toán (Controller render). HRM đang: 1=Hoàn tất, 3=Nháp (thiếu 12/13).
- [x] **T1 BE** `Modules/Assign/Entities/Warehouse/ProductExport.php`: `getStatusList()` đổi 1 "Hoàn tất"→"Đã hoàn thành", 3 "Nháp"→"Đang tạo"; thêm hằng `STATUS_DANG_QUYET_TOAN=12`/`STATUS_DA_QUYET_TOAN=13` + nhãn "Đang quyết toán"/"Đã quyết toán" (parity ERP; badge chi tiết/list đọc từ đây).
- [x] **T2 FE** `pages/finance/product-exports/index.vue` statusOptions: 1 "Hoàn tất"→"Đã hoàn thành", 3 "Nháp"→"Đang tạo" (giữ đúng 1/3 như filter ERP, không thêm 12/13).
- [ ] **T3 Test** (chờ user) mở list + chi tiết PXH: badge trạng thái hiện "Đã hoàn thành"/"Đang tạo"; bộ lọc trạng thái hiển thị đúng nhãn mới.

### 9.39 Tùy chỉnh cột hiển thị 3 màn danh sách (YCXH/ĐNXK/PXH) (user 2026-08-24)
Tái sử dụng 100% pattern có sẵn (giống `assign/bom-list`): component chung `components/modal/column-customization-modal.vue` (draggable + toggle + lock) + API `human/column-customizations` (BE đã refactor sang `user_column_settings`, screen_key chuỗi tự do → KHÔNG cần migration/BE). Cột **STT** + **Thao tác** khoá (`locked`); mặc định hiện tất cả; lưu server-side per-user.
- [x] **T1** PXH `pages/finance/product-exports/index.vue`: import+register V2BaseButton & ColumnCustomizationModal; nút "Cấu hình cột hiển thị" (#actions); `columnFields`; đổi `tableColumns`→`defaultTableColumns` (thêm `isVisible:'<key>'`, `locked` STT/action) + `tableColumns` lọc `isVisible!==false`; `getFields()` (mounted, table=`finance_product_exports`), `updateColumns`, `configColumns`.
- [x] **T2** YCXH `pages/finance/product-export-requests/index.vue`: tương tự, table=`finance_product_export_requests` (V2BaseButton đã import; nút config để #actions, "Tạo mới" giữ ở #actions-bottom).
- [x] **T3** ĐNXK `pages/finance/warehouse-export-requests/index.vue`: tương tự, table=`finance_warehouse_export_requests`.
- [ ] **T4 Test** (chờ user) mỗi màn: bấm "Cấu hình cột" → tắt/kéo cột → Lưu → cột ẩn/đổi thứ tự; reload giữ nguyên (per-user); STT/Thao tác không tắt được.

### Checkpoint — 2026-08-24 (9.39)
Vừa hoàn thành: 9.39 T1-T3 — thêm "Tùy chỉnh cột hiển thị" cho 3 màn list (PXH/YCXH/ĐNXK) bằng component chung `column-customization-modal.vue` + API `human/column-customizations` (không đụng BE, service đã dùng `user_column_settings`). Mỗi màn: nút #actions, modal, `columnFields`, `defaultTableColumns` (isVisible/locked STT+Thao tác) + `tableColumns` lọc, `getFields/updateColumns/configColumns`, screen_key `finance_product_exports`/`finance_product_export_requests`/`finance_warehouse_export_requests`.
Đang làm dở: (không)
Bước tiếp theo: T4 — user test tắt/kéo cột + reload giữ cấu hình.
Blocked:
