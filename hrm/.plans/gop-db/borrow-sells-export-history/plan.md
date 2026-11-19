# Phiếu xuất bán hàng mượn (PXBHM) — bổ sung Xuất Excel + Lịch sử

Màn `finance/borrow-sells` đang thiếu 2 chức năng so với màn mẫu `finance/product-exports`:

1. **Xuất Excel toàn bộ danh sách** (theo bộ lọc đang áp) — chưa có.
2. **Lịch sử** ở CẢ 2 nơi: popup ở màn danh sách + mục trong màn xem chi tiết `_id/index.vue` — chưa có.

Khuôn tham chiếu (vừa dựng xong trong cùng session): `finance/product-exports` — có đủ cả 2 tính năng, hạ tầng dùng chung đã sẵn (`exportListFile`, `CatalogHistoryModal`, `SystemInfoSection`, trait `LogsCatalogHistory`, `CatalogHistoryService`, route `catalog-histories/{table}/{id}`).

## Chốt với user (§0 skill entity-history + export-excel) — ĐÃ "ok"

1. `borrow_sells` **CHỈ có luồng tạo** (controller chỉ index/store/show/printData — không update/status/cancel) ⇒ lịch sử chỉ có đúng 1 dòng "Tạo mới"/phiếu. User chốt VẪN làm đủ 2 nơi.
2. **Cột xuất Excel = 8 cột danh sách**: Mã phiếu (code), Loại phiếu (type_name), Số HĐ (contract_code), Khách hàng (customer_name), Người tạo (creator_name), Tổng tiền (sum_amount_after_extra_after_vat), Ngày tạo (created_at), Trạng thái (status_name).
3. **Lịch sử track**: header (loại HĐ, số HĐ, khách hàng, ghi chú, VAT%, chịu phí ship, tổng tiền) + bảng hàng (`details_rows`). KHÔNG track `status` (không có luồng đổi trạng thái).
4. **Quyền xem lịch sử**: không có quyền riêng (ai vào được màn thì xem được).

## Việc cần làm

### A. Xuất Excel
- [x] BE: `BorrowSellController` thêm const `EXPORT_COLUMNS` (8 cột) + method `exportRows(Request)` — dùng lại `BorrowSell::searchByFilter($request)`, phân trang `page`/`limit`, số thô cho cột tiền (float), qua `BorrowSellListResource`.
- [x] BE: route `GET /borrow-sells/export-rows` trong `Modules/Finance/Routes/api.php` (nhóm prefix `/borrow-sells`). ⚠️ đặt TRƯỚC `GET /{id}` để không bị nuốt.
- [x] FE: tạo `pages/finance/borrow-sells/components/export-excel.js` (8 cột `{id,name}`).
- [x] FE: `index.vue` thêm nút "Xuất Excel" + `ExportFieldsModal` + import `exportListFile` + computed `exportFields`/`visibleExportFields` + `openExportModal`/`exportExcel` (endpoint `finance/borrow-sells/export-rows`).

### B. Lịch sử
- [x] BE: `BorrowSellService` thêm `use LogsCatalogHistory` + `catalogTable()='borrow_sells'` + `catalogColumns()` (header + `details_rows`) + `catalogDisplay()` + `detailRows()`; gọi `logCatalogCreate()` cuối `store()` (trong transaction, trước `return`), set in-memory `contract_code`/`customer_name`/`details_rows`.
- [x] BE: `CatalogHistoryService::TABLES` thêm entry `'borrow_sells'` với nhãn cột tiếng Việt.
- [x] FE (danh sách): `index.vue` thêm action "Lịch sử" (icon `ri-history-line`) + `<CatalogHistoryModal ref="historyModal" />` + import + `goHistory(item)` → `open('borrow_sells', item.id, item.code)`.
- [x] FE (chi tiết): `_id/index.vue` thêm `<SystemInfoSection entity-type="borrow_sells" :entity-id="id" endpoint-base="catalog-histories" />`.

### B2. Fix bug kích hoạt action "Lịch sử" (phát sinh trong lúc verify)
- [x] FE: `index.vue` `handleRowAction(action, item)` so sánh SAI `action.key === 'history'`. `V2BaseRowActions.emitAction()` đã `this.$emit('action', action.key)` — tức handler cha nhận **CHUỖI** key, không phải object. So với `.key` của chuỗi → luôn `undefined` → bấm "Lịch sử" không mở popup. Sửa thành `action === 'history'`. (Pattern đúng: khớp các màn khác đã dùng `@action` của `V2BaseRowActions`.)

### C. Kiểm chứng (Playwright MCP, `http://127.0.0.1:3000`)
- [x] Xuất Excel: popup "Chọn trường xuất Excel" đủ 8 cột tick sẵn → "Xuất file" bắn 3 lượt `export-rows` (page 1/2/3) + tải letterhead → file `phieu-xuat-ban-hang-muon_*.xlsx` tải về. Đọc lại file bằng PhpSpreadsheet: 1 dòng tiêu đề, 9 header (STT + 8), ~4307 dòng dữ liệu, cột Tổng tiền (G) là **ô SỐ** `numFmt #,##0` (không phải chuỗi). Đạt skill `export-excel` §7.
- [x] Popup Lịch sử ở màn danh sách: "Lịch sử thay đổi: PXBHM-04313", bộ lọc "Loại hành động" đúng 3 nhóm, "Người thực hiện" đủ danh sách NV theo công ty người tạo, 1 dòng "Tạo mới · Hệ thống".
- [x] Mục Lịch sử ở màn chi tiết (`SystemInfoSection`): mở `/finance/borrow-sells/4313` qua ĐIỀU HƯỚNG SPA (click mã phiếu, KHÔNG hard-navigate) → render đúng; bấm "Xem lịch sử" + "Bộ lọc" thấy 3 nhóm hành động + danh sách người thực hiện đầy đủ + 1 dòng "09/10/2026 14:58 · Tạo mới · Hệ thống". Ảnh: `hrm-client/borrow-sells-detail-history-verified.png`.
  - ⚠️ Ghi chú vận hành: **hard-navigate** thẳng URL `/finance/borrow-sells/{id}` trong Playwright có lúc rơi vào trang 404 tĩnh (`pages/extras/404.vue`) — KHÔNG phải bug phân quyền (route detail không gắn middleware, `show()` gate bằng `canView()` trả 403→toast chứ không 404). Vào màn qua điều hướng SPA là chuẩn.
- [x] Dọn dữ liệu thử: xoá 1 dòng log `catalog_histories` của `borrow_sells` id 4313 (log test chèn tay 09/10 14:58, trong khi phiếu tạo thật 07/09) → còn 0 dòng.
- [ ] Báo cáo tiếng Việt; KHÔNG git commit.

### Checkpoint — 2026-10-09
Vừa hoàn thành: verify Playwright đủ 3 tính năng (Xuất Excel + Lịch sử danh sách + Lịch sử chi tiết) + fix bug `handleRowAction` + dọn log test 4313.
Đang làm dở: không.
Bước tiếp theo: báo cáo user. Chờ user xác nhận trước khi commit.
Blocked: không.

## File đụng tới
- `hrm-api/Modules/Finance/Http/Controllers/V1/BorrowSellController.php`
- `hrm-api/Modules/Finance/Routes/api.php`
- `hrm-api/Modules/Finance/Services/BorrowSell/BorrowSellService.php`
- `hrm-api/app/Services/CatalogHistoryService.php`
- `hrm-client/pages/finance/borrow-sells/components/export-excel.js` (mới)
- `hrm-client/pages/finance/borrow-sells/index.vue`
- `hrm-client/pages/finance/borrow-sells/_id/index.vue`

---

# PHASE 2 — Mở rộng bộ lọc màn danh sách `finance/borrow-sells`

Brainstorming (bounded) đã chốt với user ("ok làm đi"). Bổ sung đủ các bộ lọc còn thiếu vào màn
danh sách, mirror `BorrowSellRequest::searchByFilter` (org/khách qua `whereHas('borrowSellRequest')`,
hàng hoá qua `borrow_sell_products`, số HĐ morph 3 bảng).

## Thiết kế đã duyệt (10 bộ lọc)

| # | Bộ lọc | Nguồn BE | Control FE |
|---|---|---|---|
| 1 | Công ty | `whereHas(borrowSellRequest, company_id)` | V2BaseCompanyDepartmentFilter slot `#field-org` (ĐẦU) |
| 2 | Phòng ban | `whereHas(borrowSellRequest, department_id)` | cùng cụm org |
| 3 | Mã phiếu | `code LIKE` | Tìm nhanh (đã có) — giữ |
| 4 | Loại | `contractable_type` | select "Loại hợp đồng" (đã có) + THÊM "HĐ HRM" (type 3) |
| 5 | Số hợp đồng | morph `firm_contracts`/`wr_service_contracts`/`hrm_contracts` theo `code LIKE` | text |
| 6 | Khách hàng | `whereHas(borrowSellRequest, customer_id)` | V2BaseSelectRemote slot `#field-customer_id` |
| 7 | Phiếu yêu cầu | `borrow_sell_request_id` → request `code LIKE` | text |
| 8 | Tên mã hàng hoá | `borrow_sell_products.product_name` OR `code` LIKE → `pluck(parent_id)` → `whereIn(id)` | 1 text (cả tên+mã) |
| 9 | Người yêu cầu | `whereHas(borrowSellRequest, created_by)` | select NV (bộ lọc nâng cao) |
| 10 | Người tạo | `borrow_sells.created_by` | select NV (bộ lọc nâng cao) |

## Việc cần làm

### A. BE — `BorrowSell::searchByFilter`
- [x] import `DB` facade + `BorrowSellProduct`.
- [x] Công ty/Phòng ban: `whereHas('borrowSellRequest', ...)` theo `company_id`/`department_id` (gộp 1 closure).
- [x] Số HĐ: closure morph 3 nhánh (CONTRACT_FIRM→firm_contracts, CONTRACT_WR_SERVICE→wr_service_contracts, CONTRACT_HRM→hrm_contracts) theo `code LIKE`.
- [x] Khách hàng: `whereHas('borrowSellRequest', customer_id)`.
- [x] Phiếu yêu cầu: `whereHas('borrowSellRequest', code LIKE)`.
- [x] Tên mã hàng hoá: 1 param `product_name` → OR `product_name`/`code` LIKE trên `borrow_sell_products` → pluck parent_id → `whereIn(id)`.
- [x] Người yêu cầu: `whereHas('borrowSellRequest', created_by)`.
- [x] Người tạo: `where('created_by', ...)`.
- [x] GIỮ nguyên 4 tầng quyền + eager load + orderByDesc hiện có.

### B. FE — `pages/finance/borrow-sells/index.vue`
- [x] Mở rộng `initialStateForm` + keys riêng: company_id, department_id, part_id, employee_id, contract_code, customer_id, borrow_sell_request_code, product_name, requested_by (Người yêu cầu), created_by (Người tạo).
- [x] CONTRACT_TYPE_OPTIONS thêm HĐ HRM.
- [x] `filterFields` thêm: org (đầu), contract_code, customer_id, borrow_sell_request_code, product_name, Người yêu cầu, Người tạo; giữ contractable_type + status + date_range.
- [x] Thêm components V2BaseCompanyDepartmentFilter + V2BaseSelectRemote; slot `#field-org` + `#field-customer_id`; `permissions` fail-closed theo quyền thật; `fetchCustomers` + `customerInitialOption`; `employeeOptions` từ store.
- [x] Cập nhật/gỡ comment cũ "BE CHỈ đọc 5 param" / "KHÔNG thêm ô".

### B-fix. Cụm Công ty–Phòng ban không render (phát sinh trong lúc verify)
Khi verify: slot `#field-org` được panel render nhưng `V2BaseCompanyDepartmentFilter` KHÔNG hiện ô nào
→ 3 cờ `permissions` đều `false`. Gốc: cờ dựng ở `mounted()` bằng `hasAPermission('Xem phiếu hàng mượn…')`
đọc `$store.state.permissions` (guard `api`, 584 quyền, KHÔNG có quyền "mượn" nào). Quyền "hàng mượn" của
user được cấp qua vai trò ERP guard `web`; BE `currentEmployeeHasPermission` tra bảng `permissions` CHỈ
theo tên (không lọc guard) nên vẫn thấy, còn store FE thì không → FE fail-closed ra rỗng dù BE cho ALL_COMPANY.
- [x] FE: thêm data `scopeFlags` fail-closed (`canViewAllCompany/canViewCompany/canViewDepartment = false`).
- [x] FE: `loadData()` sau response set `scopeFlags` từ `response.canViewAllCompany/canViewCompany/canViewDepartment` (meta BE, phẳng cấp 1).
- [x] FE: đổi `permissions` từ data + gán ở `mounted()` → **computed** map `scopeFlags` → `{ is_all_company, is_company, is_department, is_part:false }`.
- [x] FE: gỡ khối gán `this.permissions` ở `mounted()` + entry `permissions: {}` trong data.

### C. Kiểm chứng (Playwright, `http://127.0.0.1:3000`)
- [x] Mở màn, mở "Tìm kiếm nâng cao": đủ 11 ô, cao **32px bằng nhau** (console check trả mảng rỗng, mọi ô = 32px), cụm Công ty–Phòng ban render ĐẦU.
- [x] Lọc thử từng nhóm → lưới trả đúng:
  - Số HĐ `HĐ_TPV_MT_KD_26_0587_087` → 4304→**1** (PXBHM-04310) — nhánh morph `firm_contracts`.
  - Người tạo = Cao Thị Thùy Linh (id 407) → cả trang đều do đúng NV lập.
  - Tên/mã hàng hóa `dầu` → 4304→**958** — nhánh BorrowSellProduct pluck parent_id.
  - Loại = HĐ hãng (contractable_type) → cả trang đều "HĐ hãng".
  - Công ty (whereHas): cty1=1619 + cty2=13 + cty3=2429 + cty4=242 + cty8=1 = **4304** (phân hoạch khớp đúng tổng).
  - Phiếu yêu cầu `PYCXBHM-04392` (LIKE trong whereHas) → 4304→**1** (PXBHM-04313).
  - Phòng ban / Khách hàng / Người yêu cầu: cùng cơ chế `whereHas('borrowSellRequest')` đã được Công ty chứng minh.
- [x] Dọn dữ liệu thử: không ghi DB (chỉ là trạng thái lọc UI) → đã reset toàn bộ filter, lưới về **4304**.
- [x] Báo cáo tiếng Việt; KHÔNG git commit.

---

## Phase B — Sửa UI màn DANH SÁCH (bounded, approved "ok")

5 thay đổi cột/UI trên `finance/borrow-sells` (danh sách). Thiết kế bounded đã chốt "ok".

### B1. BE — `BorrowSellListResource` + `BorrowSell` entity
- [x] Ẩn **Tổng tiền** trên lưới nhưng GIỮ `sum_amount_after_extra_after_vat` trong response (Excel export còn dùng).
- [x] Thêm field: `updated_at` (`formatDateTime`), `updater_name` (`employeeAuditLabel` của `employee_update`), `borrow_sell_request_code` (optional borrowSellRequest), `requester_name` (created_by của phiếu YC gốc).
- [x] Thêm `contract_url`: `/assign/contracts/{id}` (CONTRACT_HRM) · `/customer-care/wr-service-contracts/{id}` (CONTRACT_WR_SERVICE) · `null` (CONTRACT_FIRM — HRM không có màn chi tiết firm_contracts → FE render text thường). Fail-safe: null khi thiếu `contractable_id`/`contractCode`.
- [x] `BorrowSell::employee_update()` belongsTo Employee theo `updated_by` (entity extends Model thuần nên khai tay); searchByFilter eager-load `employee_update.info.department`.

### B2. FE — `pages/finance/borrow-sells/index.vue`
- [x] Ẩn cột **Tổng tiền** khỏi `allColumns`.
- [x] Thêm 4 cột: **Ngày cập nhật** (`updated_at`), **Người cập nhật** (`updater_name`), **Phiếu yêu cầu** (`borrow_sell_request_code`), **Người yêu cầu** (`requester_name`).
- [x] Cột **Mã HĐ**: slot `#cell-contract_code` render `<nuxt-link v-if="item.contract_url" :to="item.contract_url">` ngược lại `<span>` text thường.
- [x] Giãn cột **Mã HĐ 150→190px** và **Khách hàng 220→280px**.
- [x] Ẩn nút **Xem chi tiết** ở cột Hành động — `getRowActions()` chỉ còn `history` (Lịch sử).

### B3. Kiểm chứng (Playwright, `http://127.0.0.1:3000`)
- [x] Header đúng thứ tự: STT · Mã phiếu · Loại phiếu · Mã HĐ · Khách hàng · Phiếu yêu cầu · Người yêu cầu · Người tạo · Ngày tạo · Ngày cập nhật · Người cập nhật · Trạng thái · Hành động (KHÔNG còn Tổng tiền).
- [x] Lọc **HĐ dịch vụ** (CONTRACT_WR_SERVICE) → 70 dòng, mọi Mã HĐ render `<nuxt-link>` tới `/customer-care/wr-service-contracts/{id}` (6512, 6584, 6590…).
- [x] **HĐ hãng** (CONTRACT_FIRM) → Mã HĐ là text thường, KHÔNG link (fail-safe đúng).
- [x] **HĐ HRM** (CONTRACT_HRM) → 0 dòng với dữ liệu hiện tại ("Không có dữ liệu phù hợp bộ lọc") → nhánh `/assign/contracts/{id}` xác nhận qua review code (FE render mọi `contract_url` qua cùng 1 slot `<nuxt-link>`); hạn chế dữ liệu, KHÔNG phải defect.
- [x] Cột Hành động chỉ còn nút Lịch sử; API list trả 200 OK; console errors là noise môi trường (socket.io reconnect :8891), không do thay đổi.
- [x] Báo cáo tiếng Việt; KHÔNG git commit.

> **Lưu ý Phase 2 (chưa đụng):** cột "Loại phiếu" (`type_name` suy từ `$item->type`) có thể lệch nhãn so với `contractable_type` — memory `hrm-borrow-sell-request-typename-mislabel`. User chốt để Phase 2, KHÔNG sửa ở phase này.

---

## Phase 2 — Sửa nhãn "Loại phiếu" sai (bounded, approved "ok" 2026-10-09)

**Bug:** cột Loại phiếu MỌI dòng ra "HĐ hãng". Gốc: `type_name = $typeNames[$item->type]` mà
cột `type` của ERP là loại HÀNG (bán/khuyến mãi) và **luôn = 1** → không phải loại hợp đồng.
Loại hợp đồng đúng nằm ở `contractable_type` (morph): 4234 FirmContract + 70 WrServiceContract.

- [x] BE `BorrowSellListResource`: thêm helper `contractTypeName($contractableType)` (FIRM→HĐ hãng,
  WR_SERVICE→HĐ dịch vụ, HRM→HĐ HRM, khác→null); đổi `type_name` sang suy từ `contractable_type`;
  gỡ property `$typeNames` không còn dùng.
- [x] KHÔNG đụng FE (`#cell-type_name` đã render `item.type_name`); bộ lọc `contractable_type` vốn đã đúng.
- [x] Kiểm chứng: `php -l` sạch; mô phỏng trên dữ liệu thật → HĐ hãng 4234 + HĐ dịch vụ 70.
- [x] Playwright (API thật 200 OK): lọc `contractable_type=WrServiceContract` → total 70, mọi dòng
  `type_name="HĐ dịch vụ"` + `contract_url=/customer-care/wr-service-contracts/{id}` (trước là "HĐ hãng" sai).

---

## Task C — Màn XEM CHI TIẾT phiếu xuất bán hàng mượn (bounded, approved "ok" 2026-10-09)

Đồng bộ form Xem chi tiết `finance/borrow-sells/_id` với màn ERP `borrow_sells/show`. 3 khoảng trống:

1. **Form chung** đồng bộ: bổ sung Người yêu cầu + Phòng yêu cầu + mã phiếu xuất mượn (PYCXH) vào
   kv-grid "Thông tin chung" (scope user chốt = **chỉ bổ sung field còn thiếu**, GIỮ layout kv-grid
   hiện tại, KHÔNG dựng lại kiểu ERP).
2. **Bảng chi tiết tách 2 tab** như ERP: "Hàng hóa" (`products`) + "Nhóm" (`tabs[].products`).
3. **Bảng "Thông tin thanh toán hợp đồng"** (mẫu HĐ_TPE_HN_KDXM_26_0398_03) — hiện đang THIẾU hẳn.

### Chốt scope (brainstorm bounded, user trả lời)
- Form sync = **"Chỉ bổ sung field còn thiếu"** (3 field, giữ kv-grid).
- Fix `type_name` DETAIL = **"Có, fix trong task này"** (suy từ `contractable_type` như list resource).
- Payment table FIRM-only: `need_contract_info = contract && type != 3 && !has_rebate_price`
  (`has_rebate_price` = contractable_type == WrServiceContract) → ẩn với HĐ dịch vụ và HĐ type 3.
- Nhóm tab cũng guard `form.contract.type != 3` (như ERP `ng-if`).
- KHÔNG đụng: luồng Phase 1 (phiếu YÊU CẦU), `BorrowSellListResource`, `BorrowSellPostingService` (dùng chung).

### C-BE. `BorrowSellDetailResource.php` + `BorrowSellController::show()` eager loads
- [x] Fix `type_name`: thêm helper `contractTypeName($contractableType)` (mirror list), suy từ
  `contractable_type`; gỡ property `$typeNames`.
- [x] `tabs[].products[]`: resolve display fields (match contract_product theo `product_id|unit_id`
  → product/model/brand/unit name + giá niêm yết `price` + `price_after_extra` + `discount_price`)
  + `details` (kèm `product_export_request_code`); `borrow_sell_qty = Σ details.qty`.
- [x] `contract_payment` block (FIRM-only, mirror `need_contract_info`): load `firm_support_accounting`
  (contractable_id + CONTRACT_FIRM); rows Hàng hóa / Gói dịch vụ (chỉ khi ≠0) / Dịch vụ đi kèm / Chi phí
  khác / Vận chuyển + total (price = hàng hoá+repair+other+delivery, KHÔNG gồm gói dịch vụ & price_total)
  + before_vat_total + VAT (firm.total_vat) + Thưởng NVKD (market_costs_percent/total_market_costs)
  + payed_cost (firm.total_after_vat); % tính sẵn BE (guard chia 0).
- [x] requester_name + requester_department (từ `borrowSellRequest.employee_create.info.department`)
  + PYCXH code (batch `product_export_requests.code` cho details hàng hoá + tab).
- [x] `show()` eager-load thêm `tabs.products.details`, `borrowSellRequest.employee_create.info.department`.
- [x] Verify tinker 2 phiếu thật: 4312 (HĐ hãng, contract HĐ_TPE_HN_KDXM_26_0398_03, 1 tab "Nhóm 1"
  2 sp, contract_payment 4 dòng, VAT 47320, payed 638820) + 4228 (HĐ dịch vụ, 0 tab, contract_payment=null,
  need_contract_info=false). `php -l` sạch cả 2 file.

### C-FE. `pages/finance/borrow-sells/_id/index.vue`
- [x] Tách bảng phẳng "Danh sách hàng hoá" thành inner `b-tabs`: "Hàng hoá" (products, bảng 11 cột +
  pay-box 6 dòng) + 1 tab/`tabs[]` tên `tab.name` (bảng Nhóm 9 cột). Nguồn phiếu mượn PYCXH render.
- [x] Thêm card "Thông tin thanh toán hợp đồng ({{ contract_code }})" (`v-if="needContractInfo && contractPayment"`,
  khuôn `c-section`) khi `contract_payment` có; bảng 6 cột + tfoot Tổng cộng + pay-box 4 dòng;
  số dùng `formatNum` (`toLocaleString('en-US')`).
- [x] Thêm 2 field (Người yêu cầu `requester_name`, Phòng yêu cầu `requester_department`) vào kv-grid
  "Thông tin chung" sau "Phiếu YC xuất bán" (mã PYCXH `borrow_sell_request_code` đã hiện sẵn).
- [x] Computed `tabs()`/`contractPayment()`/`needContractInfo()`.

### C-TEST (Playwright `http://127.0.0.1:3000`)
- [x] Verify API (tinker, C-BE): 4312 HĐ hãng có 1 tab Nhóm + contract_payment; 4228 HĐ dịch vụ 0 tab + payment null.
- [x] FIRM **4312** (điều hướng SPA qua danh sách): kv-grid thêm Người yêu cầu (Đinh Thế Tài) + Phòng
  yêu cầu (PHÒNG THIẾT BỊ XE MÁY); `type_name="HĐ hãng"`; 2 inner tab "Hàng hoá" + "Nhóm 1" (9 cột, 2 dòng);
  card "Thông tin thanh toán hợp đồng (HĐ_TPE_HN_KDXM_26_0398_03)" đủ bảng + pay-box (trước thuế 591,500 /
  VAT 47,320 / Thưởng NVKD 0% / sau thuế 638,820); số en-US.
- [x] WR_SERVICE **4228**: `type_name="HĐ dịch vụ"`; Người yêu cầu (Lê Thị Thanh Vy) + Phòng yêu cầu
  (Phòng Chăm sóc khách hàng SG) render; **CHỈ 1 tab "Hàng hoá"** (KHÔNG có tab Nhóm); **KHÔNG có card
  Thông tin thanh toán hợp đồng**; số en-US (1,200,000 / 96,000 / 1,296,000).
- [x] Báo cáo tiếng Việt. ĐÃ commit & push gop_db theo lệnh user 10/10 (api `9177aa457`, client `12d2c1d44`).

### Checkpoint — 2026-10-10 (Task C xong — ĐÃ COMMIT & PUSH)
Vừa hoàn thành: C-BE (`BorrowSellDetailResource` + `show()` eager loads) + C-FE (`_id/index.vue`:
2 field kv-grid, inner b-tabs Hàng hoá/Nhóm, card Thông tin thanh toán hợp đồng) + C-TEST Playwright
đủ 2 ca (FIRM 4312 hiện 2 tab + payment; WR_SERVICE 4228 ẩn tab Nhóm + ẩn payment). type_name detail
đã fix suy từ contractable_type. ĐÃ commit đúng 3 file Task C (api `9177aa457` 2 file, client `12d2c1d44`
1 file) + push gop_db — KHÔNG gom các thay đổi task ProductImport/ProductExport khác đang lẫn trong working tree.
Đang làm dở: không.
Bước tiếp theo: không — feature borrow-sells-export-history hoàn tất.
Blocked: không.
