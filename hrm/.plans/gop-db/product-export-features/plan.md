# Plan — Bổ sung chức năng màn Phiếu xuất hàng (finance/product-exports)

Phụ trách: @namdangit · Nhánh: gop_db

## Bối cảnh
Màn `finance/product-exports` (Phiếu xuất hàng) hiện thiếu một số chức năng so với màn
tham chiếu ĐNXK (`warehouse-export-requests`). Sau khi rà (2026-10-09):

- **Cài đặt bộ lọc**: ĐÃ CÓ sẵn (V2BaseSmartFilterPanel) — không cần làm.
- **Xuất Excel toàn bộ danh sách**: THIẾU → làm (bê pattern ĐNXK).
- **Lịch sử (list + chi tiết)**: THIẾU cả FE lẫn BE ghi log → làm (tham khảo màn khác).
- **Tạo mới**: giữ CẢ 2 luồng — luồng sinh-từ-ĐNXK (hiện có) + thêm nút "Tạo mới" lập trực tiếp.

## Phase 1 — Xuất Excel toàn bộ danh sách ✅ XONG (2026-10-09)
- [x] BE: thêm endpoint `GET assign/product-exports/export-rows` (phân trang 2000/trần 5000, trả JSON `{headings, widths, rows, total, page, limit}`)
      - `ProductExportController::exportRows()` thay cho `export()`/`exportFilterText()` cũ (lấy-tất-cả-1-lần)
      - `EXPORT_COLUMNS` (8 cột: code, type_name, warehouse_export_code, contract_code, customer_name, creator_name, created_at, status_name) — BE quyết `headings`/`widths`, FE chỉ gửi `fields` (theo thứ tự user tick, BE tôn trọng thứ tự)
      - dùng lại `buildListQuery()` + `ProductExportResource` từng dòng; total qua `getCountForPagination()`
      - route đặt TRƯỚC `/{id}` để không bị nuốt path (Routes/api.php)
- [x] FE: nút "Xuất Excel" + popup chọn trường (ExportFieldsModal) → `exportExcel()` gọi `utils/export/listExportFile.js`
      - `exportExcel()` lặp trang qua `exportListFile({endpoint:'assign/product-exports/export-rows', filters, fields, ...})`, hiện dòng tiến độ `exportProgress`
      - `components/export-excel.js` rút còn danh mục trường (`PRODUCT_EXPORT_EXPORT_COLUMNS` + `productExportExportFields()`), bỏ builder ExcelJS cũ
- [x] Verify Playwright — ca KHÔNG lọc (34436 dòng, ca trước đây 500/CORS): 18 trang `export-rows?page=1..18&limit=2000` đều `200`, letterhead `200`, file `danh-sach-phieu-xuat-hang-2026-10-09.xlsx` build + tải về OK. BE page 1 = 1166ms, peak 83MB (<512M).

> Root cause 500 cũ: `->get()` toàn bộ 34436 dòng + eager load + Resource từng dòng → cạn 512M → PHP Fatal error (try/catch không bắt được), response Fatal thiếu CORS header nên trình duyệt báo nhầm thành lỗi CORS. Cùng lỗi với sibling `ProductImportRequest` trong module Finance — fix theo đúng chuẩn `list-page` mục 14c.

## Phase 2 — Lịch sử ✅ XONG (2026-10-09)
- [x] BE: ghi `catalog_histories` cho product_exports (mirror WER qua trait `LogsCatalogHistory`)
      - `ProductExportService`: `use LogsCatalogHistory` + `catalogTable()='product_exports'`
      - `catalogColumns()` = type, emplement_contract_code, customer_name, warehouse_id, note, **details_rows** (KHÔNG status, KHÔNG bear_the_shipping — theo skill §3a)
      - `catalogDisplay()`: type→`getTypeName()`, warehouse_id→tên kho; `details_rows` trả nguyên mảng (check TRƯỚC nhánh null để `[]` không bị nulled)
      - `detailRows()`: JOIN products+units (bảng `product_export_details` KHÔNG có cột tên — khác WER), `__key=product_id|unit_id`, cột: Mã hàng / ĐVT / Số lượng
      - product-exports CHỈ có luồng create (`createFromWarehouseExport`) → gán `details_rows` + `logCatalogCreate()` ngay trước `return $pxh->fresh()`
      - `CatalogHistoryService::TABLES` thêm entry `product_exports` (nhãn cột tiếng Việt)
      - Verify tinker PXH-34590 (trong transaction, rollBack): detailRows + snapshot (type→"Xuất mượn", warehouse→"Liên Ninh") + getLogs 1 dòng action=create "Tạo mới" actor="DNS Admin", changes=[] (đúng thiết kế `changesOf()` cho create)
- [x] FE list (`index.vue`): nút "Lịch sử" (ri-history-line) + `CatalogHistoryModal`, `goHistory()` → `open('product_exports', id, code)`
- [x] FE chi tiết (`_id/index.vue`): `<SystemInfoSection entity-type="product_exports" :entity-id="id" endpoint-base="catalog-histories">` đặt trước action-bar
- [x] Verify Playwright: list popup mở, `catalog-histories/product_exports/34590` + `/filter-options` đều **200**; chi tiết block render đúng vị trí, mở rộng (Làm mới/Thu gọn), cùng empty state "Chưa có lịch sử thao tác nào." (PXH cũ chưa có log — đúng kỳ vọng). Console errors chỉ là socket.io :8891 + menu-settings 400 có sẵn, không liên quan.

### Checkpoint — 2026-10-09
Vừa hoàn thành: Phase 2 (Lịch sử) — BE ghi log + FE list popup + FE chi tiết block, verify Playwright cả 2 nơi.
Đang làm dở: (không có)
Bước tiếp theo: Phase 3 — chốt thiết kế nút "Tạo mới" với user; báo teammate erp-hrm-44 trước khi đụng form.
Blocked: Phase 3 chờ user chốt thiết kế.

## Phase 3 — Tạo mới (dual-source: Phiếu xuất kho + YCXH) ✅ ĐÃ CHỐT THIẾT KẾ (2026-10-09)

### Chốt thiết kế
- **Bản chất**: form tạo PXH GIỮ NGUYÊN, chỉ khác cách truyền id nguồn vào form.
  - Luồng 1 — tự chọn trên form: nút "Tạo mới" → vào form, ô search chọn **Phiếu xuất kho** HOẶC **YCXH**.
  - Luồng 2 — đi từ phiếu nguồn: deep-link kèm `warehouse_export_id` (sẵn có) hoặc `product_export_request_id` (mới).
- **Template mirror 1-1**: màn `product-imports` đã làm y hệt (dual-source import kho + YCNH, cờ `is_import_direct`). Bê sang.
- **ERP đối chiếu**: ERP form có sẵn ô "Chọn phiếu xuất kho"; YCXH chỉ lập được từ ds YCXH → HRM BỔ SUNG cho chọn YCXH ngay trong form.
- **Quyền**: ERP KHÔNG gác quyền riêng cho create PXH (route chỉ sso.check+userLogin, controller/menu không check). → KHÔNG tạo quyền mới, KHÔNG phân cấp; reuse gate `'Kế toán kho'` (assertCanExportGoods) như luồng PXK hiện có.
- **Cascade YCXH khi xuất thẳng**: → status **9 (Đang hạch toán)** — khớp ERP `ProductExportRequest::approve()` nhánh `is_export_direct` (ERP ProductExportRequest.php:2819-2827). Set `is_export_direct=1`, `warehouse_export_id=null`.
- **Nguồn YCXH đủ điều kiện**: `is_export_direct=1` + trạng thái chưa hạch toán (mirror filter ERP + product-imports).

### FE (hrm-client)
- [x] `index.vue`: nút "Tạo mới" (primary, `ri-add-line`) ở toolbar → `/finance/product-exports/create` (reuse quyền `'Kế toán kho'`, fail-closed).
- [x] `create.vue`: chế độ chọn nguồn khi KHÔNG có query — 2 `.source-card` mở modal "Chọn phiếu xuất kho" / "Chọn phiếu YCXH (xuất thẳng)"; nhận thêm query `product_export_request_id`; computed `sourceBasePath` lái cả 3 endpoint (product-export-data / accounting-stock-of-product / product-exports) theo nhánh PXK vs YCXH; `mounted()` rẽ 3 nhánh (warehouse_export_id → PXK, product_export_request_id → YCXH, không query → source-picker); methods `openWarehouseExportModal`/`openProductExportRequestModal`/`onChooseWarehouseExport`/`onChooseProductExportRequest`; SCSS `.source-picker`/`.source-card`; `goBack` về `/finance/product-exports` (mirror `ProductImportForm.goBack`); done-screen đổi về danh sách PXH + bỏ `.text-muted` (đỏ) sang `.done-note` (#6b7280).
- [x] Modal `WarehouseExportSearchModal.vue` (mirror `WarehouseImportSearchModal.vue`, `@choose`, phân trang) — endpoint `assign/product-exports/warehouse-export-sources`.
- [x] Modal `ProductExportRequestSearchModal.vue` (mirror `ProductImportRequestSearchModal.vue`) — endpoint `assign/product-exports/product-export-request-sources`.
- [x] unsaved-changes: giữ guard sẵn có (`unsavedSnapshotSource`), không cần thêm field nguồn (nguồn nằm ngoài snapshot).
- [x] (Luồng 2) nút "Lập phiếu xuất hàng" ở màn CHI TIẾT YCXH (`ProductExportRequestForm.vue` footer readonly) → deep-link `?product_export_request_id=`. Computed `detailCanCreateProductExport` = status CHỜ DUYỆT(2) + `is_export_direct=1` + quyền `'Kế toán kho'` (khớp gate BE); đồng thời SIẾT `detailCanCreateWarehouseRequest` thêm `is_export_direct !== 1` để 2 nút loại trừ nhau (xuất thẳng đi thẳng PXH, bỏ bước ĐNXK). PXK deep-link (`warehouse_export_id`) là màn ERP, dùng lại query sẵn có — không thêm nút HRM.

### BE (hrm-api, Module Assign) ✅ XONG + VERIFY (2026-10-09)
- [x] Endpoint list/search Phiếu xuất kho cho modal: `GET assign/product-exports/warehouse-export-sources` — `ProductExportController::warehouseExportSources()` (gate `'Kế toán kho'` + company; `WarehouseExport` status CHỜ DUYỆT theo `company_id`; map id/code/type_name/warehouse_name/customer_name/created_at; shape `{data, currentPage, perPage, total, lastPage}`). **Verify tinker**: trả 5 dòng PXK đúng cấu trúc.
      - Đặt INLINE trong controller (không ở service như product-imports) — ghi chú: export controller tự chứa list query, khác style Finance; quyết định có chủ đích.
- [x] Endpoint dựng form từ YCXH: `GET assign/product-export-requests/{id}/product-export-data` — `productExportDataFromRequest()`: header + products lấy từ `product_export_request_*` (price/vat/base_unit NGAY trên dòng), kho kế toán nhánh `is_import_export_direct=1`+company+status=1+consignment; trả dưới key `warehouse_export` (FE dùng chung) với `id=null`, `product_export_request_id`, `is_export_direct=1`. **Verify tinker**: build đúng cho PYCXH-35623.
- [x] Service `createFromProductExportRequest` + store endpoint `POST assign/product-export-requests/{id}/product-exports` (`storeProductExportFromRequest`); set `is_export_direct=1`, `warehouse_export_id=null`, `product_export_request_id`, lot_id=null, `product_export_request_detail_id`, base_unit/giá từ dòng nguồn, cascade YCXH→9. **Verify tinker** (transaction+rollback, draft status=3, PYCXH-35623): 9/9 assertions PASS — is_export_direct=1, warehouse_export_id=null, PER→9, 3 detail, catalog log=1.
- [x] Gate quyền `assertCanExportFromRequest(ProductExportRequest)` — check `'Kế toán kho'` + `is_export_direct==1` + status CHỜ DUYỆT + company; mirror `assertCanExportGoods`.
- [x] Kiểm ràng buộc NOT NULL `warehouse_export_id`: cột NULLABLE trên DB gop_db — write path lưu `warehouse_export_id=null` thành công (verify ở trên).
- [x] Ghi catalog_histories cho nhánh YCXH: `createFromProductExportRequest` gán `details_rows` IN-MEMORY + `logCatalogCreate()` trước `return $pxh->fresh()`. **Verify**: catalog_histories table_name=product_exports, action=create, 1 dòng.
- [x] **GAP bổ sung (session FE)**: endpoint tồn kho cho nhánh YCXH — `POST assign/product-export-requests/{id}/accounting-stock-of-product` → `accountingStockOfProductFromRequest()` (api.php:723). Sinh đôi của `accountingStockOfProduct` (PXK) nhưng ctx lấy từ `ProductExportRequest` (company_id/employee_id=created_by/customer_id). LÝ DO: kho kế toán nhánh YCXH lọc `is_import_export_direct=1` → `accAvailable()` đọc `in_warehouse`, chỉ `fetchAccStock` mới bơm được → thiếu endpoint này thì `accQtyValid` luôn fail. `php -l` sạch.

### Verify
- [x] Playwright: Tạo mới → chọn PXK; Tạo mới → chọn YCXH (xuất thẳng); deep-link cả 2; kiểm status YCXH→9
  - **Tạo mới (không query)**: source-picker render 2 card (PXK / YCXH xuất thẳng). Chọn "Chọn phiếu xuất kho" → modal `WarehouseExportSearchModal` list 86 phiếu chờ duyệt (tìm theo mã, phân trang 1/9). Chọn PXK-30296 (kho Liên Ninh) → form load, dropdown "Kho kế toán" = **LN01 Liên Ninh - Hàng bán / LN02 Liên Ninh - Hàng khuyến mại** (lọc theo `warehouse_id`).
  - **Deep-link YCXH** (`?product_export_request_id=35623`): form xuất thẳng render đầy đủ (Mã ĐNXK PYCXH-35623, KH CARON HOLDINGS, 3 dòng hàng), dropdown "Kho kế toán" = **HN-NXT Hà Nội - Nhập xuất thẳng**.
  - **Cascade YCXH→9**: xác nhận trong code `ProductExportService::createFromProductExportRequest` (dòng 580-581 set `STATUS_DANG_HACH_TOAN=9` cho cả nháp lẫn hoàn tất). KHÔNG submit live để tránh ghi dữ liệu thật lên DB dùng chung (phiếu/khách hàng thật).
  - Console "errors" chỉ là nhiễu dev HMR của Nuxt (`export 'default' ... not found` auto-import) — không liên quan.

### Bugfix (phát hiện khi Verify) — 2026-10-09
- [x] **Dropdown "Kho kế toán" RỖNG ở luồng YCXH xuất thẳng** — va chạm enum `type`: `productExportDataFromRequest()` truyền `$per->type` (enum `product_export_requests`) vào helper DÙNG CHUNG `isConsignmentVoucherType()` (ngữ nghĩa `warehouse_exports`: 12=Xuất gửi, 14=Nhập gửi). Trong `product_export_requests` thì **12 = "Xuất hàng gửi" (hàng gửi) nhưng 14 = "Xuất bán hàng" (KHÔNG phải)** → YCXH type 14 bị nhầm là hàng gửi → rẽ `whereIn('id', consignmentWarehouseIds(cty1)=[])` → loại sạch kho → HN-NXT biến mất. FIX **cục bộ trong controller** (KHÔNG sửa helper dùng chung): thay bằng `$isConsignmentRequest = ((int)$per->type === 12)` + comment giải thích va chạm (`ProductExportController.php:791-803`). Verify: API `product-export-data` YCXH 35623/35622 trả `accounting_warehouses` count 0→1 (HN-NXT id=29); UI dropdown hiển thị đúng.
- [x] **create.vue 2 lỗi nhỏ**: dòng 87 `rows="2"` (String) → `:rows="2"` (Number, hết cảnh báo Vue — console không còn warning prop); dòng 180 indicator loading `class="text-muted"` (ĐỎ trong project) → `style="color: #6b7280"` (xám).

### Checkpoint — 2026-10-09 (Phase 3 BE)
Vừa hoàn thành: Toàn bộ BE Phase 3 — service `createFromProductExportRequest`, 2 endpoint picker (PXK + YCXH), endpoint form-data từ YCXH, store xuất thẳng, gate `assertCanExportFromRequest`, catalog log nhánh YCXH. `php -l` sạch 3 file. Verify tinker (transaction+rollback trên erp_hrm_check): write path 9/9 PASS; 3 read endpoint trả đúng cấu trúc + scope công ty.
Đang làm dở: (không có — BE đóng)
Bước tiếp theo: FE (index.vue nút "Tạo mới"; create.vue source-picker + nhận query `product_export_request_id`; `WarehouseExportSearchModal.vue` + `ProductExportRequestSearchModal.vue`; unsaved guard; Luồng 2 deep-link ở màn PXK/YCXH).
Blocked: FE phải **báo teammate erp-hrm-44 trước khi đụng form** `product-exports/create` — chưa khởi động cho tới khi thông báo.

## Phase 4 — Rebuild form `create.vue` cho giống ERP (đầy đủ) 📋 PLAN XONG, CHỜ DUYỆT (2026-10-09)

- Spec: `docs/superpowers/specs/gop-db/2026-10-09-product-export-form-rebuild-design.md`
- **Plan chi tiết (12 task TDD): `.plans/gop-db/product-export-features/plan-form-rebuild.md`**
- Tóm tắt: 1 form thống nhất, bố cục tab giống ERP, 5 computed cờ ẩn/hiện (verbatim), 27 field Thông tin chung, khối TK read-only hardcode (loại 1–4), tab Nhóm HĐ hãng (14/15), field nhập tay TK (9/10/18/19) + danh mục + upload, nút "Đổi phiếu".
- BE: 2 endpoint nạp form trả thêm `type` + field hiển thị + `tabs` + `catalogs`; store ghi cột nhập tay vào `product_exports` (KHÔNG nối hạch toán — spec §5).
- Blocked: chờ user review plan + chọn execution method; vẫn **báo teammate erp-hrm-44 trước khi đụng form**.

## Bugfix — Icon "!" báo tab đang có lỗi khi bấm Hoàn tất ✅ XONG (2026-10-21, nhánh develop)

Yêu cầu user (ảnh chụp màn "Lập phiếu xuất hàng"): "Khi tab có lỗi cần hiện thị icon ! để user biết tab nào đang lỗi". Trước đó chỉ tab "Hàng hoá" có icon, lại gắn theo `errorMsg` chung nên MỌI lỗi (bốc xếp / bút toán / phân bổ kho) đều chỉ sáng icon ở tab "Hàng hoá" → sai tab.

- [x] `create.vue` data: thêm cờ `tabErr: { info, arrange, goods }` (comment giải thích map: info=Thông tin chung/bút toán, arrange=Bốc xếp, goods=Hàng hoá/phân bổ kho).
- [x] Tab "Thông tin chung" + "Bốc xếp" (nhóm tab trên): chuyển `title` attr → slot `#title`, thêm `<i v-if="tabErr.info/arrange" class="ri-error-warning-fill goods-tab-err">` (dùng lại đúng style icon + màu `#dc3545` sẵn có của tab Hàng hoá).
- [x] Tab "Hàng hoá" (nhóm tab hàng hoá): đổi binding icon `v-if="errorMsg"` → `v-if="tabErr.goods"`.
- [x] `submit(status)`: reset 3 cờ đầu hàm; nhánh no-rows set `goods=true`; nhánh `status===1` đánh giá ĐỘC LẬP cả 3 (`validateFinalize`/`validateArrange`/`accountEntryError`) → set đúng cờ từng tab (tab nào lỗi sáng icon cùng lúc), toast vẫn hiện câu đầu tiên (`errorMsg` giữ nguyên hành vi cũ).
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create`:
      - Bấm "Hoàn tất" khi chưa có dòng hàng (real click) → toast "Không có dòng hàng để xuất." + icon `!` CHỈ ở tab "Hàng hoá" (info/arrange không sáng).
      - Drive live component (thêm 1 dòng giả, stub `validateFinalize`/`validateArrange`/`accountEntryError`, gọi `submit(1)`) — 5 kịch bản map đúng tab: goods-only→goods, arrange-only→arrange, info-only→info, all-three→cả 3 sáng cùng lúc, none→cả 3 tắt (reset).
      - DOM render: set `tabErr={info:true,arrange:true,goods:false}` → icon render đúng ở "Thông tin chung" + "Bốc xếp", KHÔNG ở "Hàng hoá". KHÔNG submit live để tránh ghi DB dùng chung (validate fail return trước khi gọi API).

## Bugfix — FK `base_unit_id` khi Lưu nháp PXH từ phiếu xuất kho (PXK) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Yêu cầu user (ảnh chụp "2. Chọn phiếu -> bấm lưu nháp báo lỗi như ảnh"): chọn 1 Phiếu xuất kho (PXK) ở màn Lập phiếu xuất hàng → bấm "Lưu nháp" → `SQLSTATE[23000] ... product_export_details_base_unit_id_foreign` (insert `base_unit_id = 0`, không có `units.id = 0`).

- Nguyên nhân: `ProductExportService::createFromWarehouseExport` (nhánh PXK) build chi tiết `product_export_details` nhưng **BỎ `base_unit_id` / `base_unit_name`** trong `fill()` → DB default 0 vi phạm FK `units(id)`. Nhánh YCXH (`createFromProductExportRequest`) không dính vì nguồn `product_export_request_details` đã có sẵn 2 cột này. Bảng nguồn `warehouse_export_lots` KHÔNG có cột base_unit → phải suy từ đơn vị gốc của sản phẩm (ERP: `$lot->product->base_unit` = `product_units.is_base=1` → `units`, `ProductExportsController.php:813`).
- [x] Build `$baseUnitMap` (product_id → {id,name}) 1 query trước vòng lặp lots (join `product_units` is_base=1 + `units`), fallback về `$lot->unit_id`/`$lot->unit_name` nếu thiếu (an toàn FK, thực tế 6287/6287 lot product đều có is_base).
- [x] Thêm `base_unit_id` + `base_unit_name` vào `fill()` chi tiết (ProductExportService.php ~287-306). `php -l` sạch.
- [x] Verify (tinker transaction+rollback trên erp_hrm_check — tái hiện ĐÚNG path lỗi `createFromWarehouseExport` status=NHAP = Lưu nháp): WE PXK-00074 (2 lots) → 2 chi tiết đều `base_unit_id=40` (hợp lệ FK), `base_unit_name=Cái`, 0 dòng base_unit_id=0 → hết lỗi `product_export_details_base_unit_id_foreign`. KHÔNG submit live để tránh ghi PXH thật lên DB dùng chung (rollback sau khi assert).

## UI — Thanh hành động dưới cùng màn Lập PXH (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Yêu cầu user (ảnh chụp "3. Đưa button Quay lại về cuối cùng / Text Hoàn tất đổi thành Gửi duyệt"): chỉnh thanh `export-actionbar` dưới cùng màn `pages/finance/product-exports/create.vue`.

- [x] Đưa nút "Quay lại" xuống CUỐI cụm (thứ tự mới: Lưu nháp → Gửi duyệt → Quay lại) — khớp quy tắc form page của `button-convention` (Lưu nháp đầu → action chính → Quay lại cuối).
- [x] Đổi nhãn nút chính "Hoàn tất" → "Gửi duyệt" (gồm cả ternary `submitting ? 'Đang lưu...' : 'Gửi duyệt'`). Đổi icon `ri-check-line` → `ri-send-plane-line` (icon chuẩn Gửi/Submit của `button-convention`) vì hành động đổi từ "hoàn tất/xác nhận" sang "gửi duyệt". Giữ nguyên `submit(1)` (status 1) — chỉ đổi trình bày, không đụng nghiệp vụ.
- [x] Verify Playwright tại `http://127.0.0.1:3000/finance/product-exports/create`: snapshot thanh dưới cùng thứ tự nút = Lưu nháp · Gửi duyệt · Quay lại; nút chính chữ "Gửi duyệt". PASS (2026-10-21).

## UI — Bảng Chi tiết: ô "SL xuất" (4) + cột "Kho kế toán" (5) quá chật (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Yêu cầu user (ảnh "4. Ô sl xuất quá bé, k báo lỗi rõ ràng k biết sai lỗi gì" / "5. Dropdown xổ xuống quá dài so với chiều ngang, giãn rộng cột"): bảng Chi tiết tab "Hàng hoá", cụm cột kho kế toán.

- [x] **(4) Ô "SL xuất"**: `<th>` min-width 104px (đo thật: ô input 91px đọc rõ số); thêm method `accQtyError(acc)` trả câu lỗi rõ nghĩa (`Phải > 0` / `Vượt SL được xuất (X)`); render `<div class="fld-err">` dưới input khi `acc._touched && !accQtyValid(acc)` (giống ô Kho kế toán có "Trùng kho."); bỏ icon `.is-invalid` của Bootstrap chiếm chỗ trên input số inline (giữ viền đỏ) bằng CSS `.er-table .form-control.is-invalid { background-image: none; padding-right: 6px !important }` — **phải `!important`** vì Bootstrap đặt `padding-right` của `.is-invalid` kèm `!important`, không thì số bị đẩy lệch ~32px khỏi mép phải.
- [x] **(5) Cột "Kho kế toán"** — **user chốt dùng V2BaseSelect** (thay vì giữ `<select>` native): thay native `<select>` bằng `V2BaseSelect` (search box + dropdown gọn cuộn được, không kéo giãn cột theo option dài); `<th>` min-width 220px để cột đủ rộng dưới `table-layout: auto`. Thêm: import + đăng ký `V2BaseSelect` (file đăng ký component tường minh); computed `accountingWarehouseOptions` map `{id, name: '<code> — <name>'}`; method `onAccWarehouseChange(row, acc, idx, val)` coerce value STRING→Number (V2BaseSelect trả chuỗi) trước khi gọi `onAccChange` (lookup kho dùng `===`); viền đỏ trùng kho qua `:class="{ 'v2-select--invalid': isDupAcc(...) }"` + CSS `.v2-select--invalid ::v-deep .select2-selection { border-color: #dc3545 !important }` kèm dòng `.fld-err` "Trùng kho.".
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?product_export_request_id=35623`: cột Kho kế toán 220px / SL xuất 104px (đọc được); V2BaseSelect render + dropdown có ô search; chọn kho → `onAccWarehouseChange` coerce Number → `onAccChange` fetch tồn (SL được xuất = 3, ô SL xuất bật lên); SL xuất=5 → "Vượt SL được xuất (3)" + viền đỏ + số đọc rõ (padding-right 6px, không bị icon che); SL xuất=0 → "Phải > 0"; thêm dòng kho 2 cùng kho → cả 2 dòng viền đỏ + "Trùng kho.".

## UI — Tab "Bốc xếp": bo góc ô + bỏ placeholder option 2 dropdown (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Yêu cầu user (ảnh chụp "1. Bo góc lại các textbox và ô dropdown xổ xuống như tab Thông tin chung" / "2. Bỏ các giá trị placeholder trong các dropdown Hình thức thuê và Loại bốc xếp"): tab "Bốc xếp" màn `pages/finance/product-exports/create.vue`.

- [x] **(1) Bo góc 5px** khớp tab "Thông tin chung" (V2BaseInput/V2BaseSelect đều `border-radius: 5px`): CSS `.arr-field .form-control { border-radius: 5px }` cho mọi textbox số; 2 `<select>` native (Hình thức thuê, Loại bốc xếp) đổi sang `V2BaseSelect size="sm"` (vỏ `.select2-selection--single` sẵn `border-radius: 5px`) → cùng góc với ô bên tab chung.
- [x] **(2) Bỏ option placeholder gạch ngang** `— Không dùng bốc xếp —` / `— Chọn loại —`: V2BaseSelect dùng prop `placeholder` (không render thành option) + `allow-clear` (nút × giữ vai trò off-switch thay cho option rỗng). Data `rentTypeOptions=[{id:1,name:'Công ty'},{id:2,name:'Thuê ngoài'}]`; computed `arrangeGoodOptions` map `{id, name: type_name}`; methods `onRentTypeSelect`/`onArrangeTypeSelect` coerce STRING→Number (rent_type='' = off → `arrangeEngaged=false` → Loại bốc xếp `:disabled`).
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172` (nguồn PXK-30172, type 7, status 2, cty 1): border-radius ô số = 5px, `.select2-selection--single` = 5px (khớp tab chung); dropdown "Hình thức thuê" chỉ còn `["Công ty","Thuê ngoài"]`, "Loại bốc xếp" chỉ còn 7 loại thật — **KHÔNG còn option gạch ngang**; rent_type='' → "Loại bốc xếp" `disabled=true` (off-switch qua × hoạt động đúng). Ảnh: `.playwright-mcp/arrange-tab-verified.png`.

## UI — Nút "Gửi duyệt" phải hỏi xác nhận `$confirm()` (button-convention §6c) (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Phát hiện khi rà lại thanh `export-actionbar`: nút "Gửi duyệt" (`submit(1)`, status 1 = đẩy phiếu đi duyệt) là nút ĐỔI TRẠNG THÁI nhưng **tự dựng ngoài `V2Footer`** nên không được hỏi hộ → `button-convention` §6c bắt buộc tự gọi `$confirm()`. (Nút "Lưu nháp" `submit(3)` KHÔNG hỏi — chỉ lưu nháp, chưa đẩy đi đâu.)

- [x] Thêm `await this.$confirm({...})` trong `submit(status)` (`create.vue` ~dòng 1355), đặt trong nhánh `status === 1` **SAU validate** (form lỗi thì toast + return, không hỏi vô ích) và **TRƯỚC** `this.submitting = true` / `$safeLoadingStart()` (đúng thứ tự §6c: hỏi trước khi bật lớp tải). `if (!ok) return`.
  - `title: 'Xác nhận gửi duyệt'` · `message: 'Tạo phiếu xuất hàng${srcLabel} và gửi đi duyệt?'` (srcLabel = ` (nguồn PXK-xxxxx)` hoặc ` (nguồn <YCXH>)` tùy `sourceType`, lấy từ computed `pxkCode`/`ycxhCode`; nguồn trống thì bỏ cụm) · `textAccept: 'Gửi duyệt'` (đúng chữ nút gốc) · **KHÔNG `danger`** (nhóm gửi duyệt = bước tiến luồng, không đỏ).
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172` (nguồn PXK-30172):
      - Real click "Gửi duyệt" khi form chưa phân bổ kho (SL xuất=0) → toast validate ("Tổng SL các kho kế toán... phải bằng SL thực xuất (50).") + **KHÔNG hiện popup** → đúng "hỏi SAU validate".
      - Gọi đúng `$confirm` mà `submit()` dựng (qua `window.$nuxt.$confirm`) → popup render: title "Xác nhận gửi duyệt", message "Tạo phiếu xuất hàng (nguồn PXK-30172) và gửi đi duyệt?", nút accept "Gửi duyệt" class `v2-btn--primary v2-btn--primary-info` (teal, KHÔNG danger), nút "Hủy" tertiary. Ảnh: `.playwright-mcp/gui-duyet-confirm-dialog.png`.
      - Bấm "Hủy" → popup đóng sạch (0 modal), URL không đổi (vẫn màn create), không submit.

## UI — Tab "Bốc xếp": đồng bộ cỡ chữ các ô (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL, chưa commit)

Yêu cầu user (ảnh "3. Đồng bộ size chữ", gạch đỏ dưới "Hình thức thuê", "Loại bốc xếp", "Đơn giá bốc xếp", "Tài khoản nợ"): cỡ chữ trong tab "Bốc xếp" lệch nhau.

- [x] **Đo thật (Playwright)**: select2 (Hình thức thuê, Loại bốc xếp, Nhà cung cấp, Tài khoản nợ, Mã phí, Vụ việc) = **12px**; ô nhập tay native `.form-control-sm` (Khối lượng, Đơn giá bốc xếp, Số tiền, VAT %, Tiền VAT, Số tiền sau VAT) = **10.24px** (rơi về `.form-control-sm` toàn cục, KHÔNG nhận rule 12px vốn scoped trong block tab Hàng hoá). → lệch.
- [x] **Fix**: thêm `font-size: 12px` vào rule `.arr-field .form-control` (đã có `border-radius: 5px`) → ô nhập tay = 12px, khớp select2 = 12px (chuẩn nhà cho ô `sm`). KHÔNG đụng select2 (đã 12px đúng chuẩn).
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172`: mọi control trong tab Bốc xếp đều 12px. Đo lại 12 ô → `distinctSizes: ["12px"]` (6 select2 + 6 ô nhập tay). Ảnh: `.playwright-mcp/arrange-tab-fontsize-synced.png`.

## UI — Popup "Thêm nhanh Mã phí / Vụ việc" thiếu trường + placeholder (create.vue) ✅ XONG (nhánh develop — GIỮ LOCAL)

Yêu cầu user (ảnh "4. Popup Thêm nhanh mã phí thiếu trường / Thêm placeholder cho tất cả các trường / Sửa tương tự với vụ việc"): popup "+" thêm nhanh ở tab Bốc xếp (ô Mã phí, ô Vụ việc) đang chỉ có **Mã*/Tên***, thiếu so với màn danh mục gốc (CostDebtModal/WorkModal có đủ **Mã · Tên · Trạng thái(Hoạt động) · Ghi chú**).

- [x] Dựng lại popup thêm nhanh (inline trong `create.vue`, dùng chung cho cả 2 loại qua `quickAdd.type`) theo **đúng pattern `pages/finance/cost-debts/CostDebtModal.vue` + `pages/finance/works/WorkModal.vue`**: chuyển từ `b-modal` thô + `<input class="form-control">` sang `V2BaseModal` + `V2BaseInput`/`V2BaseTextarea`/`V2BaseSelectInModal`/`V2BaseLabel`/`V2BaseButton` (CLAUDE.md cấm HTML form thô, select trong modal = `V2BaseSelectInModal`).
  - Trường: **Mã** (`V2BaseInput`, `*`) · **Tên** (`V2BaseInput`, `*`) · **Trạng thái** (`V2BaseSelectInModal`, options Hoạt động(1)/Khóa(2), mặc định `1`, `allowClear=false`) · **Ghi chú** (`V2BaseTextarea` 3 dòng). Nhãn type-aware: `work` → "Mã vụ việc"/"Tên vụ việc", còn lại → "Mã phí"/"Tên mã phí" (bám HRM catalog, KHÔNG bám chữ ERP).
  - **Placeholder cho tất cả**: Mã = `VD: VV001`/`VD: MP001`; Tên = `Nhập tên vụ việc`/`Nhập tên mã phí`; Trạng thái = `Chọn trạng thái`; Ghi chú = `Nhập ghi chú`.
  - Footer theo `button-convention`: Lưu(primary, icon save) → Đóng(tertiary, mũi tên) — bỏ nút "Huỷ"(light) cũ (light cấm trong modal footer).
- [x] `saveQuickAdd` gửi thêm `note` + `status` trong payload (BE `WorkRequest`/`CostDebtRequest` đã nhận `status:nullable|in:1,2`; service đọc `note` qua `$request->all()` → **KHÔNG sửa BE**). Giữ nguyên luồng chọn-ngược (set `arrange.work`/`arrange.cost_debt` + `workInitial`/`costDebtInitial`).
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172`: chọn "Hình thức thuê"=Công ty để bật khối Bốc xếp → mở "+" Mã phí → popup "Thêm mã phí" 4 trường đủ placeholder (`VD: MP001` / `Nhập tên mã phí` / Trạng thái mặc định **Hoạt động** / `Nhập ghi chú`), footer Lưu(teal)→Đóng, icon price-tag; mở "+" Vụ việc → title "Thêm vụ việc", nhãn đổi "Mã vụ việc"/"Tên vụ việc", placeholder `VD: VV001`/`Nhập tên vụ việc`, icon briefcase. 0 console error cả 2 lần mở. (Không chạy "lưu thật" để tránh tạo bản ghi rác vào danh mục chung `erp_hrm_check`; logic `saveQuickAdd` bám y CostDebtModal.)

### Checkpoint — 2026-10-21 16:43
Vừa hoàn thành: Popup "Thêm nhanh Mã phí / Vụ việc" — đủ 4 trường + placeholder + type-aware, verify Playwright 2 loại OK.
Đang làm dở: (không)
Bước tiếp theo: chờ user chốt task kế / có đẩy develop không.
Blocked: (không)

## UI — Dropdown "Nhà cung cấp" (Bốc xếp) hiển thị dạng "mã - tên" (create.vue) ✅ XONG (2026-10-21, nhánh develop — GIỮ LOCAL)

Yêu cầu user (ảnh "5. Giá trị trong dropdown NCC để dạng mã - tên"): ô "Nhà cung cấp" ở tab Bốc xếp đang hiện **tên trần** (A ÁNH, A BĂNG…), phải đổi thành **`mã - tên`** cho đồng bộ với "Vụ việc" (`RRP - Rủi ro theo phòng`), "Tài khoản nợ" (`111 - Tiền mặt`) và ô NCC disabled ở tab Thông tin chung (dòng 115 đã ghép `supplier_code - supplier_name`).

- [x] BE `CustomerManagerService::suppliers()` (dòng ~885): thêm cột `code` vào `get(['id', 'code', 'fullname as name'])` — **thuần bổ sung**, 6 caller khác (`warehouse-imports/barcode`, `ArrangeDeliveryForm`, `ProductImportForm`, `EquipmentTab`, `AddExternalEquipmentModal`) chỉ đọc `.id`/`.name` nên không ảnh hưởng. Keyword đã sẵn `like code` nên tìm theo mã vẫn chạy.
- [x] FE `create.vue` `fetchSuppliers` (dòng ~1170): map `(s) => ({ id: s.id, name: s.code ? `${s.code} - ${s.name}` : s.name })` — y khuôn `fetchWorks`/`fetchCostDebts`. Chỉ sửa trong create.vue (đúng phạm vi yêu cầu), KHÔNG đổi 5 màn còn lại.
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172`: bật khối Bốc xếp (set `rent_type=2` Thuê ngoài) → mở dropdown NCC, gõ "a" → mỗi dòng hiện `mã - tên` (`4ACTIVE - 4ACTIVESYSTEMS GMBH`, `22TTUPMI-67 - A ÁNH`, `3DBETA - 3D BETA S.R.L`…); tìm theo mã vẫn ra kết quả; chọn 1 NCC → ô hiển thị `4ACTIVE - 4ACTIVESYSTEMS GMBH` (đồng bộ "Tài khoản nợ" `6428 - Chi phí bằng tiền khác`); 0 console error liên quan suppliers/fetch. Ảnh: dropdown + chip đều đúng khuôn.

### Checkpoint — 2026-10-21 17:05
Vừa hoàn thành: Task 5 — dropdown NCC (Bốc xếp) hiển thị `mã - tên`. BE thêm cột `code` (thuần bổ sung), FE map trong `fetchSuppliers` của create.vue (chỉ màn này). Verify Playwright PASS (options + search theo mã + chip chọn đều đúng, 0 console error).
Đang làm dở: (không)
Bước tiếp theo: chờ user chốt yêu cầu kế tiếp. Toàn bộ thay đổi GIỮ LOCAL trên `develop` (hrm-api + hrm-client), chưa commit/push.
Blocked: (không)

## UI — Ô "Khối lượng/Số giờ", VAT %, Số tiền người thực hiện (Bốc xếp) chặn nhập sai định dạng (create.vue) ✅ XONG (2026-10-22, nhánh develop — GIỮ LOCAL)

Yêu cầu user (ảnh "6. Nhập thời gian/khối lượng k đúng định dạng k báo lỗi"): ô "Khối lượng (Tấn)/Số giờ" tab Bốc xếp đang là `<input type="number">` thô → gõ sai định dạng (`--1`) hiện trên ô nhưng model rỗng, KHÔNG báo lỗi, KHÔNG chặn. **Hướng A (user chốt 2026-10-22):** đổi các ô nhập số sửa được trong khối Bốc xếp sang `V2BaseCurrencyInput` — tự chặn ký tự sai ngay khi gõ (không bao giờ nhập được `--1`/chữ/số âm), hiển thị số chuẩn quốc tế `1,234.5`, emit số thuần nên công thức tính tiền không đổi. Đúng CLAUDE.md "màn mới dùng V2Base".

- [x] FE `create.vue`: import + đăng ký `V2BaseCurrencyInput` trong `components`.
- [x] FE `create.vue` ô Khối lượng/Số giờ → `V2BaseCurrencyInput v-model="arrange.weight" :disabled="!arrangeEngaged"` (bỏ `class="text-right"` thừa — component tự căn phải qua `--currency`).
- [x] FE `create.vue` ô VAT % → `V2BaseCurrencyInput :disabled="!arrangeEngaged" v-model="arrange.vat"` (KHÔNG set `max` để tránh tự kéo về trần — vi phạm "không tự sửa giá trị").
- [x] FE `create.vue` ô Số tiền người thực hiện (`exe.employee_price`) → `V2BaseCurrencyInput v-model="exe.employee_price"`.
- [x] Giữ computations: `arrangeTotal`/`arrangeVatPrice`/`buildArrangePayload` dùng `Number(...) || 0` — V2BaseCurrencyInput emit số thuần/`null` nên OK, không phải sửa.
- [x] Verify Playwright `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=30172`: bật Bốc xếp (rent_type=1) → ô Khối lượng gõ `--1`→`1`, `abc`→``, `-5`→`5`, `12ab34`→`1,234`, `1234.5`→`1,234.5` (model = số thuần `1234.5`); VAT gõ `1a0.5`→`10.5`; thêm 1 dòng người thực hiện → ô Số tiền cũng là V2BaseCurrencyInput (tổng 3 ô). 0 console error.

### Checkpoint — 2026-10-22 08:55
Vừa hoàn thành: Task 6 — đổi 3 ô nhập số sửa được ở tab Bốc xếp (Khối lượng/Số giờ, VAT %, Số tiền người thực hiện) từ `<input type="number">` thô sang `V2BaseCurrencyInput` (Hướng A user chốt). Ô tự chặn ký tự sai ngay khi gõ, hiển thị `1,234.5`, emit số thuần. Verify Playwright PASS: masking đúng, format đúng, model số thuần, 0 console error.
Đang làm dở: (không)
Bước tiếp theo: chờ user chốt yêu cầu kế tiếp. Toàn bộ thay đổi Task 6 GIỮ LOCAL trên `develop` (hrm-client), chưa commit/push.
Blocked: (không)

---

## Màn DANH SÁCH Phiếu xuất bán hàng mượn (`/finance/borrow-sells`) — 5 điểm QA đối chiếu ERP ✅ XONG (2026-10-22, nhánh develop — GIỮ LOCAL)

QA đối chiếu ERP `warehouse/borrow_sells?type=all` vs HRM `/finance/borrow-sells`, 5 điểm:
1. **Thừa bộ lọc trạng thái** — chỉ 1 giá trị "Đã duyệt", ERP không có → **user chốt: bỏ FIELD lọc + ẩn CỘT mặc định** (giữ trong Cấu hình cột, `isVisible: false`).
2. **Thêm sort** 5 cột: Mã phiếu (`code`), Loại phiếu (`type_name`), Mã HĐ (`contract_code`), Phiếu yêu cầu (`borrow_sell_request_code`), Người tạo (`creator_name`).
3. **Link Phiếu yêu cầu** — cột `borrow_sell_request_code` → `/finance/borrow-sell-requests/{id}`.
4. **Khác biệt ERP "Loại"=Hàng bán vs HRM "Loại phiếu"=HĐ hãng/dịch vụ/HRM** — KHÔNG sửa (user chốt: cố ý, cột `type` ERP là loại HÀNG luôn=1, HRM hiển thị `contractable_type`, bug #11566-Phase2 đã có comment).
5. **Link Mã HĐ đủ MỌI loại HĐ** — HĐ HRM/dịch vụ link nội bộ, HĐ hãng (chưa chuyển HRM) link sang ERP.

### BE (hrm-api)
- [x] `BorrowSell.php`: thêm const `SORTABLE_COLUMNS` (map key cột FE → biểu thức sort) + method `applySort($query, $request)` đọc `sort_by`/`sort_dir`, validate `$dir` ∈ asc/desc (an toàn concat), morph string truyền `?` binding. `code`/`type_name` = `orderBy` cột own; `contract_code`/`borrow_sell_request_code`/`creator_name` = `orderByRaw` subquery; luôn `orderByDesc('id')` tie-break. Gỡ `orderByDesc('id')` khỏi builder gốc, gọi `applySort()` trước `return`.
- [x] `BorrowSellListResource.php`: trả thêm `borrow_sell_request_id` (cho FE link điểm 3); `contractUrl()` thêm nhánh `CONTRACT_FIRM` → `{ERP_URL}/admin/sale/firm-contracts/{id}` (điểm 5), thiếu ERP_URL trả null.

### FE (hrm-client `pages/finance/borrow-sells/index.vue`)
- [x] Điểm 1: gỡ field `status` khỏi `filterFields()` + xoá const `STATUS_OPTIONS` + gỡ `status: ''` khỏi `initialStateForm` (mergeKnownFilters tự loại giá trị status cũ còn trong localStorage → không lọc ngầm); cột `status` thêm `isVisible: false`.
- [x] Điểm 2: `data()` thêm `sortBy: ''`/`sortDirection: 'desc'`; `<V2BaseDataTable>` thêm `:sortBy`/`:sortDirection`/`@sort`; method `handleSort({field,direction})` (về trang 1 + loadData); `buildParams()` gửi `sort_by`/`sort_dir` khi có sortBy; 5 cột thêm `sortable: true`.
- [x] Điểm 3: cell `borrow_sell_request_code` → `<nuxt-link :to="/finance/borrow-sell-requests/{id}">` dùng `item.borrow_sell_request_id`, fallback text.
- [x] Điểm 5: cell `contract_code` — `isExternalUrl()` (regex `^https?://`) → `<a target="_blank" rel="noopener">` (ERP, HĐ hãng); đường dẫn tương đối → `<nuxt-link>` (nội bộ); null → text.
- [x] Verify Playwright `http://127.0.0.1:3000/finance/borrow-sells` (2026-10-22, PASS): (a) `filterLabels` KHÔNG còn "Trạng thái"; header bảng KHÔNG có cột "Trạng thái", nhưng trong "Cấu hình cột" vẫn có mục "Trạng thái" (checkbox **unchecked** = ẩn mặc định); (b) đúng 5 cột sortable (Mã phiếu/Loại phiếu/Mã HĐ/Phiếu yêu cầu/Người tạo); click "Mã phiếu" → API gửi `?sort_by=code&sort_dir=asc` (200), dòng đầu đổi từ PXBHM-04313 (mới nhất) → PXBHM-00001 (asc), icon header `ri-arrow-up-line`; (c) Phiếu yêu cầu = `<nuxt-link>` nội bộ `/finance/borrow-sell-requests/{id}` (không target); (d) Mã HĐ HĐ hãng = `<a target="_blank" rel="noopener" href="{ERP_URL}/admin/sale/firm-contracts/{id}">`, Mã phiếu = nuxt-link nội bộ; **0 console error**.
