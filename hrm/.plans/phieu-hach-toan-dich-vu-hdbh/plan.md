# Phiếu hạch toán dịch vụ — HĐBH (ERP→HRM) — PLAN Phase 1 (chỉ-đọc)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port màn **Phiếu hạch toán dịch vụ HĐBH** (ERP `Sale\ServiceAccounting`) sang HRM ở mức **chỉ-đọc**: danh sách + chi tiết + Excel + lịch sử + quyền + menu, kèm **checkpoint đối chiếu số liệu** với ERP trước khi mở Phase 2 (ghi sổ).

**Architecture:** Phiếu `service_accounting` **cùng hình dạng bảng với YC sibling** (`service_accounting_requests` — KHÔNG có cột org/customer, suy từ `employee_create.info` + `contractable`=FirmContract). Lấy **khuôn scope/search/canView từ YC** (`ServiceAccountingRequest`), **khuôn bút toán/export/shell read-only từ phiếu HDDV** (`WrAccountingService`). BE: entity `extends Model` trên bảng ERP của DB gộp (KHÔNG migration), service + list-resource + controller `ApiController`, export `DynamicExport`. FE: Nuxt2 `pages/finance/service-accounting/` với 4 mixin chuẩn, `V2Base*`, detail shell `Form + SystemInfoSection + V2Footer`.

**Tech Stack:** PHP 7.4 / Laravel 8, spatie permission guard `api`, maatwebsite/excel (`DynamicExport` + `ExportColumnRegistry`); Nuxt 2.14 / Vue 2 / Node 14.21.3; MySQL DB gộp `erp_hrm_check`. Test BE = PHPUnit (`Modules/Finance/Tests/Feature`), FE = Playwright MCP (chạy app bằng skill `run-hrm`).

**Spec:** `.plans/phieu-hach-toan-dich-vu-hdbh/design.md` (đã user duyệt 03/11/2026)

## Global Constraints

- **KHÔNG migration** — bảng ERP (`service_accounting`, `service_accounting_items`, `service_accounting_costs`, `account_details`) có sẵn trên DB gộp `erp_hrm_check`.
- **Nhánh feature riêng** tách từ `develop` cho **cả** hrm-api + hrm-client; merge về develop sau khi xong. ERP `gop_db` chỉ đọc.
- **Scope = FirmContract-only** (DB 1275/1275): mọi query lọc `contractable_type = App\Model\Sale\Firm\Contract\FirmContract` + null-guard; KHÔNG port nhánh else `getDataCreateDept`.
- **Quyền fail-closed**, guard `api`, **type = 23 (Bán hàng)**, khai qua `$this->perm([...])` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (KHÔNG `id` cứng, KHÔNG dùng lại quyền ERP guard web). **3 cấp** xem (tổng cty/cty/phòng ban) — bỏ cấp "bộ phận".
- **Số liệu format chuẩn quốc tế** (`1,234,567.89`): BE trả **số thô** (float), FE format bằng `toLocaleString('en-US')`.
- **FE** dùng `V2Base*`; màn này **KHÔNG** thuộc nhóm kho nên dùng `V2BaseFormSection` (như HDDV), KHÔNG bắt buộc `V2BaseFormCard`.
- **Badge trạng thái:** BE quyết `status` (int) + `status_name` + `status_color` (hex); FE chỉ render `<V2BaseBadge :color>`, KHÔNG tự map số→chữ/màu.
- **Slug màn** (thống nhất mọi nơi): `service_accounting` (ExportColumnRegistry key, `columnScreenKey`, catalog-histories entity_type); **API prefix** `finance/service-accounting`; **FE route** `/finance/service-accounting`.
- **Phase 1 KHÔNG ghi gì** — không endpoint store/update/destroy, không ghi `account_details`, không catalog-history log (đó là Phase 2).

## Review Focus

1. **`contractable` null / FirmContract đã xóa** — `show` + list resource phải null-guard: không 500, "Số hợp đồng"/khách hàng rỗng → chuỗi trống. *(Task 3: `test_show_null_guards_missing_contractable`)*
2. **Phiếu toàn cost (items = 0 — data thật)** — bảng Dịch vụ render rỗng, tổng vẫn đúng từ costs. *(Task 3: `test_show_renders_empty_service_table_when_cost_only`)*
3. **User không quyền & không phải owner/approver** — list rỗng, `show` trả 403. *(Task 2: `test_list_excludes_rows_for_unprivileged_user`; Task 3: `test_show_forbidden_without_permission_returns_403`)*
4. **Phiếu nháp (Đang tạo) của người khác** — ẩn khỏi list với viewer 3-cấp, chỉ owner thấy (dù prod 0 nháp, logic phải đúng — seed nháp trong test). *(Task 2: `test_list_hides_others_draft_shows_own_draft`)*
5. **VAT suy theo `type` với mảng rỗng / cột vắng** — Dịch vụ→`revenue_costs[0].vat_percent`, Chi phí→`costs[0].vat_percent`, Vận chuyển→`delivery_vat_percent`; mảng rỗng/cột thiếu → **fallback 0**, không lỗi. *(Task 3: `test_vat_percent_falls_back_to_zero`)*

---

## File Structure

**BE (hrm-api):**
- `Modules/Finance/Entities/ServiceAccounting/ServiceAccounting.php` (Create)
- `Modules/Finance/Entities/ServiceAccounting/ServiceAccountingItem.php` (Create)
- `Modules/Finance/Entities/ServiceAccounting/ServiceAccountingCost.php` (Create)
- `Modules/Finance/Services/ServiceAccountingService.php` (Create)
- `Modules/Finance/Transformers/ServiceAccountingResource/ServiceAccountingListResource.php` (Create)
- `Modules/Finance/Http/Controllers/V1/ServiceAccountingController.php` (Create)
- `Modules/Finance/Providers/FinanceServiceProvider.php` (Modify — morphMap, nếu cần đăng ký FQN FirmContract)
- `Modules/Finance/Routes/api.php` (Modify — group `/service-accounting`)
- `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (Modify — 3 quyền xem)
- `app/ExcelExport/ExportColumnRegistry.php` (Modify — entry `service_accounting`)
- `Modules/Finance/Tests/Feature/ServiceAccountingReadApiTest.php` (Create — list/show/export)
- `Modules/Finance/Tests/Feature/ServiceAccountingCheckpointTest.php` (Create — đối chiếu số liệu)

**FE (hrm-client):**
- `pages/finance/service-accounting/index.vue` (Create — list)
- `pages/finance/service-accounting/_id/index.vue` (Create — detail shell)
- `pages/finance/service-accounting/components/ServiceAccountingForm.vue` (Create — read-only form)
- `pages/finance/service-accounting/components/JournalTable.vue` (Create — bút toán; port từ HDDV)
- `pages/finance/service-accounting/components/ServiceTable.vue` + `CostTable.vue` (Create hoặc reuse từ `service-accounting-requests`)
- `components/subsystem-menu/finance.js` (Modify — gắn link vào stub dòng ~314)
- `components/subsystem-menu/sale-hub.js` (Modify — thêm mục dưới "Dịch vụ")

---

### Task 1: Entity layer (ServiceAccounting + Item + Cost + morphMap)

**Files:**
- Create: `Modules/Finance/Entities/ServiceAccounting/ServiceAccounting.php`
- Create: `Modules/Finance/Entities/ServiceAccounting/ServiceAccountingItem.php`
- Create: `Modules/Finance/Entities/ServiceAccounting/ServiceAccountingCost.php`
- Modify: `Modules/Finance/Providers/FinanceServiceProvider.php` (chỉ nếu `registerMorphMap` chưa có FQN FirmContract dùng cho whereHasMorph)
- Test: `Modules/Finance/Tests/Feature/ServiceAccountingReadApiTest.php` (phần entity)

**Interfaces:**
- Produces:
  - `ServiceAccounting extends Illuminate\Database\Eloquent\Model`, `use ChecksEmployeePermission`, `$table='service_accounting'`, `$guarded=['id']`, `$dates=['approved_at','created_at','updated_at']`.
  - Hằng: `DANG_TAO=1`, `DA_DUYET=2`; `DICH_VU=1`, `CHI_PHI=2`, `VAN_CHUYEN=3`; `INVOICEABLE_TYPE='App\\Model\\Sale\\ServiceAccounting'`; `CONTRACTABLE_FIRM_CONTRACT='App\\Model\\Sale\\Firm\\Contract\\FirmContract'`; `PERMISSION_VIEW_ALL_COMPANY`/`_COMPANY`/`_DEPARTMENT` (= 3 chuỗi quyền §Task2); `STATUSES` (mảng `['id','name','type','color']`: Đang tạo `#64748B`/secondary, Đã duyệt `#16A34A`/success); `TYPES`; `SORTABLE_COLUMNS=['code'=>'code','createdAt'=>'created_at','approvedAt'=>'approved_at','status'=>'status']`.
  - Quan hệ: `items():hasMany(ServiceAccountingItem,'service_accounting_id')`; `costs():hasMany(ServiceAccountingCost,'service_accounting_id')`; `serviceAccountingRequest():belongsTo(ServiceAccountingRequest,'service_accounting_request_id')`; `contractable():morphTo()`; `approver():belongsTo(Employee,'approver_id')`; `employee_create():belongsTo(Employee,'created_by')`; `accounting():hasMany(\Modules\Finance\Entities\Account\AccountDetail,'invoiceable_id','id')->where('invoiceable_type', self::INVOICEABLE_TYPE)` (bỏ điều kiện `money_value_exchange<>0` hay giữ — **giữ** như HDDV để loại dòng rỗng).
  - Method (signature, body do implementer viết theo mẫu HDDV/YC): `statusMeta(): array`, `typeMeta(): array`, `contractCode(): ?string` (null-safe), `totalPayment(): float`, `isOwnedByCurrent(): bool`, `canView(): bool` (3 cấp, suy org từ `employee_create.info` — **mẫu `ServiceAccountingRequest::canView` nhưng BỎ cấp part**, và quy tắc nháp: `status==DANG_TAO` chỉ owner/approver thấy), `static searchByFilter($request): Builder`, các screen-flag static `isBigBoss/isBoss/isManager/hasAccountingPermission/isSuperAdmin`.
  - `searchByFilter`: `with(['contractable'=>morphWith FirmContract load customer+employeeCreate.info, 'employee_create.info','approver.info'])`; **luôn** `where('contractable_type', self::CONTRACTABLE_FIRM_CONTRACT)`; `type=='all'` → `applyAllScope` (3 cấp qua employee_create.info) + ẩn nháp người khác; else → `where('created_by', auth id)`; rồi `applyFilters` + `applySort`.
  - `ServiceAccountingItem extends Model`, `$table='service_accounting_items'`, `$guarded=['id']`; `ServiceAccountingCost extends Model`, `$table='service_accounting_costs'`, `$guarded=['id']`, quan hệ `cost():belongsTo(...)` (bảng danh mục chi phí, mẫu YC `ServiceAccountingRequestCost`).
- Consumes: `Modules\Finance\Entities\ServiceAccountingRequest\ServiceAccountingRequest` (quan hệ + mẫu scope), `Modules\Finance\Entities\Account\AccountDetail` (quan hệ accounting), `ChecksEmployeePermission` trait.

- [ ] **Step 1: Viết test đỏ** `ServiceAccountingReadApiTest::test_entity_relations_and_scope_on_real_firm_contract_rows`

```php
// DatabaseTransactions. Lấy 1 phiếu thật trên DB gộp:
$row = ServiceAccounting::query()->where('contractable_type', ServiceAccounting::CONTRACTABLE_FIRM_CONTRACT)->first();
if (!$row) { $this->markTestSkipped('no service_accounting rows'); }
$row->load(['costs','contractable','employee_create.info','accounting']);
$this->assertSame(ServiceAccounting::CONTRACTABLE_FIRM_CONTRACT, $row->contractable_type);
$this->assertTrue($row->accounting->count() >= 0);
$this->assertIsFloat($row->totalPayment());
// searchByFilter luôn kẹp FirmContract:
$sql = ServiceAccounting::searchByFilter(new Request(['type'=>'all']))->toSql();
$this->assertStringContainsString('contractable_type', $sql);
```

- [ ] **Step 2: Chạy test — đỏ** `Expected: FAIL (class ServiceAccounting not found)`
- [ ] **Step 3:** Tạo 3 entity + hằng + quan hệ + method theo Interfaces (mẫu: `ServiceAccountingRequest.php` cho scope/canView, `WrAccountingService.php` cho `accounting()`/`statusMeta`/`totalPayment`). Đăng ký morphMap FQN FirmContract trong `FinanceServiceProvider` nếu `whereHasMorph` cần.
- [ ] **Step 4: Chạy test — xanh** `Expected: PASS`
- [ ] **Step 5: Commit** `feat(finance): ServiceAccounting entity layer (read-only, FirmContract scope)`

---

### Task 2: List endpoint + quyền + meta

**Files:**
- Create: `Modules/Finance/Transformers/ServiceAccountingResource/ServiceAccountingListResource.php`
- Create: `Modules/Finance/Http/Controllers/V1/ServiceAccountingController.php` (method `index`)
- Modify: `Modules/Finance/Routes/api.php` (group `/service-accounting` → `GET /` index)
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
- Create/append: `Modules/Finance/Services/ServiceAccountingService.php` (`searchByFilter`, `meta`)
- Test: `ServiceAccountingReadApiTest.php`

**Interfaces:**
- Produces:
  - Quyền (group `'Phiếu hạch toán dịch vụ HĐBH'`, guard `api`, type `23`): `'Xem phiếu hạch toán dịch vụ HĐBH - theo tổng công ty'`, `'- theo công ty'`, `'- theo phòng ban'`. (Hằng `PERMISSION_VIEW_*` ở Task 1 trỏ đúng 3 chuỗi này.)
  - `ServiceAccountingListResource extends ResourceCollection`, `toArray($request)` emit mỗi dòng: `id, code, type, type_name, contract_id, contract_code, customer_id, customer_label, sale_name, payed_cost(float), total_payment(float), created_by, creator_name, created_at(d/m/Y H:i), approver_id, approver_name, approved_at, status(int), status_name, status_color`. **KHÔNG** `is_can_edit/delete` (Phase 1). Key khớp `ExportColumnRegistry::COLUMNS['service_accounting']` (Task 4). Có `resolveCustomer/CreatorNames` batched (chống N+1).
  - `ServiceAccountingService::searchByFilter(Request): LengthAwarePaginator` (`->paginate($request->per_page ?? 10)`); `ServiceAccountingService::meta(): array` (`is_big_boss/is_boss/is_manager/is_all_company/statuses/types`); `static formatDateTime($v): ?string` → `d/m/Y H:i`.
  - `ServiceAccountingController::index(Request)` → `ServiceAccountingListResource($paginator)->additional(['total'=>..,'lastPage'=>..,'currentPage'=>..,'perPage'=>..] + $service->meta())`. Route ungated (BE scope theo quyền; owner luôn thấy phiếu mình).
  - Bộ lọc (`applyFilters`): `startDate/endDate`(created_at), `code`(like), `status`, `company`/`department`(ánh xạ qua employee_create.info), `contract_code`(whereHasMorph FirmContract code), `customer`(whereHasMorph customer_id), `cost`(whereHas costs.cost_id), `money_from/money_to`(payed_cost). Default sort `created_at DESC`.
- Consumes: Task 1 entity + `searchByFilter`.

- [ ] **Step 1: Viết test đỏ** — 3 test:
  - `test_list_scopes_by_permission_level`: seed/dùng user có quyền "theo công ty" → chỉ thấy phiếu người cùng công ty; user "tổng công ty" → thấy tất cả FirmContract.
  - `test_list_excludes_rows_for_unprivileged_user` (Review Focus #3): user không quyền + không owner → `data` rỗng.
  - `test_list_hides_others_draft_shows_own_draft` (Review Focus #4): seed 1 phiếu `DANG_TAO` của user khác + 1 của chính user → viewer 3-cấp chỉ thấy phiếu `DA_DUYET` + nháp của mình.
  - Auth: `actingAs($employee, 'api')` (mẫu HTTP feature test sẵn có trong `Modules/*/Tests/Feature`).
- [ ] **Step 2: Chạy — đỏ** `Expected: FAIL (route/controller chưa có)`
- [ ] **Step 3:** Khai 3 quyền (`$this->perm`), viết ListResource + service `searchByFilter`/`meta` + controller `index` + route. Badge quadruple từ `statusMeta()`.
- [ ] **Step 4: Chạy — xanh** `Expected: PASS` (chạy `php artisan db:seed --class=...PermissionsTableSeeder` hoặc seed quyền trong `setUp` test trước khi assert).
- [ ] **Step 5: Commit** `feat(finance): ServiceAccounting list endpoint + view permissions`

---

### Task 3: Detail (show) endpoint + bút toán

**Files:**
- Modify: `ServiceAccountingController.php` (`show`)
- Modify: `ServiceAccountingService.php` (`findForShow`, `detailData`, `journalRows`, `journalObject`, `vatPercentFor`)
- Modify: `Modules/Finance/Routes/api.php` (`GET /{id}`)
- Test: `ServiceAccountingReadApiTest.php`

**Interfaces:**
- Produces:
  - `ServiceAccountingService::findForShow(int $id): ServiceAccounting` — eager load `['contractable.customer.deputies','items','costs.cost','serviceAccountingRequest','employee_create.info','approver.info','accounting.account']` (**chỉ `accounting.account`** — KHÔNG bê eager-load sâu ERP).
  - `ServiceAccountingService::detailData(ServiceAccounting $m): array` — emit: header (id, code, type/type_name, status badge quadruple, note, comment), `contract_id`/`contract_code` (**chữ, không link** — màn HĐ hãng chưa port), customer (id/name/label/address/mobile từ `contractable.customer`, **null-safe**), `sale_name` (người lập HĐ), created_by/creator_name/created_at, approver_id/name/approved_at, `items` (rows), `costs` (rows), `journal` (= `journalRows()`), và `pre_tax/vat/vat_percent/total` (suy theo `type`, **fallback 0**).
  - `journalRows(ServiceAccounting): array` — map `accounting` (cột phẳng) → `{account_name, account_number(=account.identify_number), debit, credit (theo type 1/2 từ money_value_exchange), object_code, object_name (customer|employee|service_name), work_code, work_name, group, group_number}`; đánh `group_number` tăng theo `group`; lookup customer/employee/work **batched** (chống N+1) — mẫu `WrAccountingServiceService::journalRows`.
  - `vatPercentFor(ServiceAccounting): float` — Dịch vụ→`contractable->revenue_costs[0]->vat_percent` (`revenue_costs=costs`), Chi phí→`contractable->costs[0]->vat_percent`, Vận chuyển→`contractable->delivery_vat_percent`; thiếu → `0`. **Xác minh tên cột VAT trên `firm_contracts`/`firm_contract_costs` lúc build** (đã thấy nhóm `total_*_vat`, `delivery_before_vat`).
  - `ServiceAccountingController::show($id)` → `findForShow` → `if(!$m->canView()) responseJson(...,403)` → `responseJson($service->detailData($m))`.
- Consumes: Task 1 entity, `Account\AccountDetail` (cột phẳng + `account()`).

- [ ] **Step 1: Viết test đỏ** — 4 test:
  - `test_show_returns_header_costs_and_journal_for_real_voucher`: lấy phiếu thật `DA_DUYET` (markTestSkipped nếu không có); assert `code`, `journal` non-empty khớp `accounting->count()`, mỗi journal row có `account_number`.
  - `test_show_null_guards_missing_contractable` (RF #1): tạo phiếu trỏ `contractable_id` không tồn tại → `show` 200, customer rỗng, không 500.
  - `test_show_renders_empty_service_table_when_cost_only` (RF #2): phiếu items=0, costs>0 → `items=[]`, `total` tính từ costs.
  - `test_vat_percent_falls_back_to_zero` (RF #5): FirmContract thiếu mảng/cột VAT → `vat_percent===0`.
  - `test_show_forbidden_without_permission_returns_403` (RF #3).
- [ ] **Step 2: Chạy — đỏ**
- [ ] **Step 3:** Viết `findForShow`/`detailData`/`journalRows`/`vatPercentFor` + controller `show` + route.
- [ ] **Step 4: Chạy — xanh**
- [ ] **Step 5: Commit** `feat(finance): ServiceAccounting detail + journal rendering (flat columns)`

---

### Task 4: Excel export

**Files:**
- Modify: `app/ExcelExport/ExportColumnRegistry.php` (entry `'service_accounting'`)
- Modify: `ServiceAccountingController.php` (`export`)
- Modify: `ServiceAccountingService.php` (`exportRows`)
- Modify: `Modules/Finance/Routes/api.php` (`GET /export`)
- Test: `ServiceAccountingReadApiTest.php`

**Interfaces:**
- Produces:
  - `ExportColumnRegistry::COLUMNS['service_accounting']` = 9 cột (khớp key ListResource): `code`→'Mã', `created_at`→'Ngày lập', `contract_code`→'Số hợp đồng', `customer_label`→'Khách hàng', `total_payment`→'Tổng thanh toán', `creator_name`→'Người lập', `approved_at`→'Ngày duyệt', `status_name`→'Trạng thái' (STT do `DynamicExport` tự đánh). Thứ tự khớp ERP `getDataForExport`.
  - `ServiceAccountingService::exportRows(Request): array` — reuse query `searchByFilter` **không phân trang** (`->get()`) rồi `(new ServiceAccountingListResource($items))->toArray($request)`.
  - `ServiceAccountingController::export(Request)` → `(new DynamicExport())->forData($service->exportRows($request))->withColumns(ExportColumnRegistry::resolve('service_accounting',$request))->withTitle('Phiếu hạch toán dịch vụ HĐBH')` → `Excel::download(...)`.
- Consumes: Task 2 ListResource + service query.

- [ ] **Step 1: Viết test đỏ** `test_export_returns_xlsx_with_expected_columns`: GET `/finance/service-accounting/export?type=all&fields=...` → 200, content-type xlsx; assert `ExportColumnRegistry::resolve('service_accounting', $req)` chứa 8 label trên.
- [ ] **Step 2: Chạy — đỏ**
- [ ] **Step 3:** Thêm registry entry + `exportRows` + controller `export` + route.
- [ ] **Step 4: Chạy — xanh**
- [ ] **Step 5: Commit** `feat(finance): ServiceAccounting Excel export`

---

### Task 5: FE danh sách + menu

**Files:**
- Create: `pages/finance/service-accounting/index.vue`
- Modify: `components/subsystem-menu/finance.js` (gắn `link` vào stub ~dòng 314)
- Modify: `components/subsystem-menu/sale-hub.js` (thêm mục dưới "Dịch vụ")

**Interfaces:**
- Consumes: BE `GET finance/service-accounting` (list + meta) + `/export`.
- Produces: route `/finance/service-accounting?type=all`.

- [ ] **Step 1:** Port `index.vue` từ `pages/finance/wr-accounting-services/index.vue`:
  - Mixin: `PageTitleMixin, filterStateMixin, columnCustomizationMixin, exportFieldsMixin`; `columnScreenKey='service_accounting'`; `API_PREFIX='finance/service-accounting'`.
  - Cột `allColumns`: STT · Mã(link `/finance/service-accounting/{id}`) · Số hợp đồng · Khách hàng · Tổng thanh toán(money) · Người lập · Ngày duyệt · Trạng thái(`V2BaseBadge :color=status_color`). `exportFields` + `exportFieldKeyMap` khớp registry.
  - Toolbar **chỉ**: Xuất Excel (`exportFieldsMixin` + `downloadExcel(this.$axios,'finance/service-accounting/export?...',filename)`, `per_page:10000`) + Cấu hình cột. **KHÔNG Tạo mới** (phiếu sinh từ YC — Phase 2).
  - Row actions: **chỉ Lịch sử** (`CatalogHistoryModal`, entity `service_accounting`). Lọc: `V2BaseSmartFilterPanel` + `V2BaseCompanyDepartmentFilter` + `V2BaseSelectRemote` (contract_code/customer/cost) + date range + status.
  - Money: `toLocaleString('en-US')`.
- [ ] **Step 2:** Menu: `finance.js` stub `{ label:'Phiếu hạch toán dịch vụ - HĐBH' }` → thêm `link:'/finance/service-accounting?type=all'`; `sale-hub.js` thêm `{ n:'Phiếu hạch toán dịch vụ - HĐBH', link:'/finance/service-accounting?type=all' }` dưới title "Dịch vụ", ngay sau YC HĐBH.
- [ ] **Step 3: Verify (Playwright)** — chạy app (`skill run-hrm`), mở `http://127.0.0.1:3000/finance/service-accounting?type=all`:
  - Menu có link (không còn xám); list render; cột đúng thứ tự; badge màu từ `status_color`; Xuất Excel tải file; không console error liên quan.
- [ ] **Step 4: Commit** `feat(finance-fe): ServiceAccounting list page + menu link`

---

### Task 6: FE chi tiết (shell + form + bút toán + lịch sử)

**Files:**
- Create: `pages/finance/service-accounting/_id/index.vue`
- Create: `pages/finance/service-accounting/components/ServiceAccountingForm.vue`
- Create: `pages/finance/service-accounting/components/JournalTable.vue`
- Create/Reuse: `components/ServiceTable.vue` + `CostTable.vue` (reuse từ `service-accounting-requests` nếu tương thích)

**Interfaces:**
- Consumes: BE `GET finance/service-accounting/{id}` (`detailData`).
- Produces: route `/finance/service-accounting/{id}`.

- [ ] **Step 1:** `_id/index.vue` shell (mẫu HDDV `_id/index.vue`): `<ServiceAccountingForm :id>` + `<SystemInfoSection entity-type="service_accounting" endpoint-base="catalog-histories">` + `<V2Footer url-back="/finance/service-accounting?type=all">`. **Footer chỉ Quay lại** (không Sửa/Xóa — Phase 2).
  - *Lưu ý:* Phase 1 chưa ghi catalog-history → phần "thay đổi" của `SystemInfoSection` rỗng; vẫn hiện người lập/người duyệt/ngày từ `detailData`. Không coi là lỗi.
- [ ] **Step 2:** `ServiceAccountingForm.vue` (mẫu `WrAccountingServiceForm.vue`): `V2BaseFormSection` "Thông tin chung" (`#actions`=`CreatorInfoLine`), các `V2BaseLabel`+`V2BaseInput :disabled` (Mã, Số HĐ=chữ, Khách hàng, Loại, Ghi chú, VAT%); rồi `ServiceTable` (Dịch vụ — rỗng khi items=0), `CostTable` (Chi phí/Vận chuyển), `JournalTable` (bút toán). Số: `toLocaleString('en-US')`.
- [ ] **Step 3:** `JournalTable.vue` (port từ HDDV): cột `account_name, account_number, debit(phải), credit(phải), object_code, object_name, work_code(, work_name)`.
- [ ] **Step 4: Verify (Playwright)** — mở 1 phiếu thật `/finance/service-accounting/{id}`:
  - Thông tin chung + bảng Chi phí + bảng bút toán render; tổng Nợ=Có; VAT% hiển thị; footer chỉ "Quay lại"; không console error liên quan.
- [ ] **Step 5: Commit** `feat(finance-fe): ServiceAccounting detail page + journal/history`

---

### Task 7: Checkpoint đối chiếu số liệu (cổng mở Phase 2)

**Files:**
- Create: `Modules/Finance/Tests/Feature/ServiceAccountingCheckpointTest.php`

**Interfaces:**
- Consumes: `ServiceAccountingService::detailData` + `journalRows`; bảng `account_details` thật.

- [ ] **Step 1: Viết test** `test_rendered_journal_reconciles_with_stored_account_details`:
  - Lấy **N=20** phiếu `DA_DUYET` FirmContract ngẫu nhiên có `accounting` (markTestSkipped nếu DB rỗng).
  - Với mỗi phiếu: `journal = journalRows($m)`; assert **ΣNợ (debit) == ΣCó (credit)** (cân đối); assert tổng `money_value_exchange` theo `group` khớp tổng cột phẳng `account_details` của phiếu; assert số dòng journal == `accounting->count()`.
  - `test_total_payment_matches_payed_cost_within_tolerance`: `detailData.total` ≈ `payed_cost` (sai số ≤ 1đ) cho N phiếu.
- [ ] **Step 2: Chạy — xanh.** Nếu lệch → **DỪNG**, báo user (đây là cổng số liệu của design §1.4), **KHÔNG** sửa công thức để ép khớp cho tới khi user xác nhận.
- [ ] **Step 3: Commit** `test(finance): ServiceAccounting numbers checkpoint (gate Phase 2)`
- [ ] **Step 4:** Báo user kết quả checkpoint + xin chốt mở **Phase 2** (plan riêng).

---

## Self-review (đã chạy)

1. **Spec coverage:** design §1 Phase-1 (list/show/export/history/quyền/menu/checkpoint) → Task 2/3/4/6(history)/2(quyền)/5(menu)/7. Phase-2 KHÔNG trong plan này (cố ý, cổng checkpoint). ✓
2. **Step scan:** mỗi step 1 việc kiểm được; không body thừa (chỉ signature + test). ✓
3. **Type consistency:** key ListResource (Task 2) = ExportColumnRegistry (Task 4) = FE columns (Task 5); `accounting.account`/cột phẳng (Task 1 quan hệ) = `journalRows` (Task 3) = `JournalTable` (Task 6). Slug `service_accounting` thống nhất. ✓
4. **Review Focus:** 5 mục → test ở Task 2/3. ✓
5. **Proportion:** plan ngắn hơn code sẽ sinh; chủ yếu quyết định + tên test. ✓

**⚠️ Build-time verify (không đoán):** tên cột VAT `firm_contracts`/`firm_contract_costs`; cơ chế `actingAs(...,'api')` theo 1 feature test Finance/MasterData sẵn có; quan hệ `cost()` của `ServiceAccountingCost` (mẫu YC); có cần `registerMorphMap` thêm FQN FirmContract cho `whereHasMorph` không.

---
---

# PHASE 2 — GHI SỔ (write-side) — PLAN

> **Cổng vào:** Task 7 (checkpoint số liệu) XANH — ĐÃ qua ở Phase 1. Phase 2 **ghi `account_details`** (khó lùi) nên final review bắt buộc trên model mạnh nhất.
> **REQUIRED SUB-SKILL:** `superpowers:executing-plans` (native inline, user đã chọn) + `superpowers:test-driven-development` mỗi task. Full suite: `php -d memory_limit=-1 ./vendor/bin/phpunit Modules/Finance/Tests/Feature` (KHÔNG `artisan test` — OOM). Baseline 173 test, 21 fail pre-existing KHÔNG liên quan (FastDelivery*/PrepickTracking*/WarehouseInventory*).

**Goal (Phase 2):** Cho phép **tạo phiếu hạch toán DV HĐBH từ 1 YC** (`service_accounting_request_id` bắt buộc), **duyệt = sinh bút toán** ghi `account_details` + lật YC → `Đã hạch toán (5)` + cập nhật ngày bàn giao HĐ; **Sửa/Xóa** chỉ khi người lập & `Đang tạo (1)` — bám ERP `Sale\ServiceAccountingController` + `FirmContractCostService` 1:1, scope FirmContract-only.

**Architecture (Phase 2):** Engine bút toán = **port ERP `FirmContractCostService::getDataCostAccounting`** vào service Finance mới. **3 cụm SA-riêng** (doanh thu 5113/Work18, giảm trừ 5213/Work19, giá vốn 632/1541 theo-cost) viết mới (TK/Work khác trait sẵn có). **4 cụm nặng** (thưởng HĐ, TNCN, NS tháng-quý, quỹ rủi ro) **tái dùng `Modules/Assign/Services/Accounting/SupportAccountingTrait`** — nạp nguồn hỗ-trợ-hạch-toán bằng entity Assign `SupportAccounting` (CÙNG bảng `firm_support_accounting`, đã có `departments()`/`department_main()`). Ghi sổ qua `AccountDetail::createDataSaveDept` + `saveAccountDetail` (đã có, key thô → cột phẳng). Bọc **transaction + rollback** (sửa bug ERP store thiếu `DB::rollBack()` ở 2 nhánh `return` sớm).

## Global Constraints (Phase 2 — bổ sung)

- **Ghi sổ chỉ khi `status == DA_DUYET (2)`**; `DANG_TAO (1)` = chỉ lưu phiếu + copy items/costs, KHÔNG ghi `account_details`.
- **Idempotent:** trước khi ghi, xoá `account_details` cũ của phiếu (`invoiceable_id = phiếu, invoiceable_type = ServiceAccounting::INVOICEABLE_TYPE`) rồi ghi lại — tránh nhân đôi khi update.
- **Quyền ghi mới:** `Hạch toán dịch vụ HĐBH` (type 23 Bán hàng, guard `api`), khai `$this->perm([...])` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — KHÔNG `id`, KHÔNG `guard_name`. Route `store`/`update`/`destroy` gắn `checkPermission:Hạch toán dịch vụ HĐBH`.
- **canEdit/canDelete fail-closed BE:** `created_by == auth()->id() && status == DANG_TAO`; vi phạm → `423` (update) / `403|404` (destroy), chặn NGAY đầu service trước validate nghiệp vụ. FE ẩn nút (không disable) khi không owner / không `DANG_TAO`.
- **KHÔNG lộ trace:** nhánh lỗi trả message nghiệp vụ, KHÔNG `Log::error($e)` kèm response (ERP lộ `$exception->getMessage()`); log nội bộ được, response chỉ câu ngắn.
- **Số bút toán khớp ERP TUYỆT ĐỐI** — Task 10 golden test đối chiếu 1:1 với `account_details` thật; lệch → DỪNG, systematic-debugging, **KHÔNG sửa công thức để ép khớp**.

## Review Focus (Phase 2)

1. **Ghi sổ 2 lần (update phiếu đã duyệt lại)** — phải xoá bút toán cũ trước khi ghi, ΣNợ=ΣCó sau update, không nhân đôi dòng. *(Task 11: `test_update_reposts_without_duplicating_account_details`)*
2. **Nhánh posting lỗi giữa chừng** (TK thiếu trong `accounts`, `getData` trả false) — **rollback sạch**: phiếu KHÔNG lưu `DA_DUYET`, YC KHÔNG lật, `account_details` 0 dòng. *(Task 11: `test_posting_failure_rolls_back_everything`)*
3. **Phiếu VẬN CHUYỂN (type 3) & CHI_PHI (type 2)** — bỏ cụm giá vốn với type 3, bỏ 4 cụm nặng với type≠1; chỉ type 1 (DỊCH VỤ) chạy đủ 8 cụm. *(Task 9: `test_van_chuyen_skips_cost_cluster`, `test_only_dich_vu_runs_heavy_clusters`)*
4. **`support_accounting` thiếu / phòng rỗng / mẫu số = 0** — `percent_export_* = 0`, 4 cụm nặng ra 0 dòng (bị `intval(value)<=0` loại), không chia 0, không 500. *(Task 9: `test_zero_denominator_yields_no_heavy_lines`)*
5. **PLBS/HDDA_PLBS** — bút toán ghi về **HĐ gốc** (`parent_contract_id`), `account_details.contractable_id` = cha, không phải phụ lục. *(Task 9: `test_plbs_posts_to_parent_contract`)*
6. **Không quyền `Hạch toán dịch vụ HĐBH`** — `store`/`update`/`destroy` trả 403 dù là owner. *(Task 11: `test_write_endpoints_forbidden_without_permission`)*

---

## File Structure (Phase 2)

**BE (hrm-api):**
- Modify `Modules/Finance/Entities/ServiceAccounting/ServiceAccounting.php` — `generateCode()`, `canEdit()`, `canDelete()`, `syncItems()`, `syncCosts()`, fillable write-side.
- Modify `Modules/Finance/Entities/Contract/FirmContract.php` — consts `PL_BO_SUNG`/`HDDA_PLBS`, `parent_contract()`, `updateHandoverDate()`.
- Create `Modules/Finance/Services/FirmContractServiceAccountingPostingService.php` — engine bút toán (port ERP `FirmContractCostService`).
- Modify `Modules/Finance/Services/ServiceAccountingService.php` — `store()`, `update()`, `destroy()`.
- Create `Modules/Finance/Http/Requests/ServiceAccounting/ServiceAccountingStoreRequest.php` + `ServiceAccountingUpdateRequest.php`.
- Modify `Modules/Finance/Http/Controllers/V1/ServiceAccountingController.php` — `store`/`update`/`destroy`.
- Modify `Modules/Finance/Routes/api.php` — 3 route + `checkPermission`.
- Create `Modules/Finance/Services/ServiceAccountingNotifyService.php` — thông báo duyệt (mẫu `ServiceAccountingRequestNotifyService`).
- Modify `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — quyền `Hạch toán dịch vụ HĐBH`.
- Create tests: `ServiceAccountingWriteApiTest.php`, `FirmContractServiceAccountingPostingTest.php`, `ServiceAccountingPostingReconcileTest.php`.

**FE (hrm-client):**
- Create `pages/finance/service-accounting/create.vue` + `components/ServiceAccountingForm.vue`.
- Modify `pages/finance/service-accounting/_id/index.vue` — footer Sửa/Xóa (ẩn nếu không owner/`DANG_TAO`).

---

### Task 8: Entity write-side + FirmContract deps

**Files:**
- Modify: `Modules/Finance/Entities/ServiceAccounting/ServiceAccounting.php`
- Modify: `Modules/Finance/Entities/Contract/FirmContract.php`
- Test: `Modules/Finance/Tests/Feature/ServiceAccountingWriteApiTest.php` (phần entity)

**Interfaces:**
- Produces: `ServiceAccounting::generateCode(): string` (pattern `<company_code>.HTDV.NNNNN`, `autoGenerateCode` tương đương — dùng helper mã HRM sẵn có, build-time verify tên); `canEdit(): bool` / `canDelete(): bool` = `created_by == auth()->id() && status == DANG_TAO`; `syncItems(array $items): bool`; `syncCosts(array $costs): bool`; `FirmContract::parent_contract()`, `FirmContract::updateHandoverDate(): void`, consts `PL_BO_SUNG`/`HDDA_PLBS`.
- Consumes: YC bảng `service_accounting_request_items` / `_costs` (copy cột — port ERP `ServiceAccounting::syncItems/syncCosts`, ERP model dòng 353–415).

- [ ] **Step 1:** Test `test_can_edit_delete_only_owner_and_draft` — owner+`DANG_TAO`→true; owner+`DA_DUYET`→false; người khác+`DANG_TAO`→false (3 assert).
- [ ] **Step 2:** Chạy — FAIL (method chưa có). → implement `canEdit`/`canDelete` (copy ERP model:154–165, đổi `Auth::id()`→`auth()->id()`). Chạy — PASS.
- [ ] **Step 3:** Test `test_sync_items_costs_copy_from_request` — seed YC + item/cost; gọi `syncItems`/`syncCosts`; assert `service_accounting_items`/`_costs` có dòng copy đúng (`service_id`, `price`, `value_discount`, `coefficient_cost_price`, `total_price`). **BỎ guard `accounted`** (cột không tồn tại ở HRM — xem Ruling 8.1).
- [ ] **Step 4:** Chạy FAIL → implement `syncItems`/`syncCosts` (port ERP model:353–415, BỎ 2 nhánh `if ($sr->accounted) return false;`; GIỮ nhánh `name==='Chi phí vận chuyển' && DA_DUYET → contractable->accounted_delivery_cost=true` vì cột `firm_contracts.accounted_delivery_cost` CÓ). Chạy PASS.
- [ ] **Step 5:** Test `test_update_handover_date_and_parent_contract_relation` — FirmContract PLBS có `parent_contract`; `updateHandoverDate()` set `handover_date`. **Port ERP `FirmContract::updateHandoverDate()` + `parent_contract()`** (đọc ERP `app/Model/Sale/Firm/Contract/FirmContract.php` lúc build — build-time verify thân hàm). Chạy FAIL→PASS.
- [ ] **Step 6: Commit** `feat(finance): ServiceAccounting write-side entity + FirmContract posting deps`

---

### Task 9: Posting engine — `FirmContractServiceAccountingPostingService`

**Files:**
- Create: `Modules/Finance/Services/FirmContractServiceAccountingPostingService.php`
- Test: `Modules/Finance/Tests/Feature/FirmContractServiceAccountingPostingTest.php`

**Interfaces:**
- Produces: `getDataCostAccounting(ServiceAccounting $sa): array` → `[bool $ok, array $accounts]` (mảng vế `createDataSaveDept`); `private prepareData($sa, $contract): array`.
- Consumes: `AccountDetail::createDataSaveDept(&$accounts,$number,$value,$type,$ref,$objects,$note)` (đã có, key thô `customer_id`/`employee_id`/`work_id`/`service_accounting_cost_id`/`group`); `SupportAccountingTrait` (4 method nặng: `bonusContractAccounting`, `vatExtraCostAccounting`, `monthlyAndQuarterlyCommissionAccounting`, `riskFundAccounting`); Assign `SupportAccounting` (bảng `firm_support_accounting`, `departments()`/`department_main()`).

> **Port 1:1 ERP `FirmContractCostService` (`app/Services/Sale/Firm/Contract/FirmContractCostService.php:109–273`).** Dịch key `::class` → key thô: `Customer::class=>customer_id` → `['customer_id'=>...]`; `Employee::class=>...` → `['employee_id'=>...]`; `Work::class=>N` → `['work_id'=>N]`; `ServiceAccountingCost::class=>id` → `['service_accounting_cost_id'=>id]`.

- [ ] **Step 1:** Test `test_revenue_cluster_posts_1311_5113_33311_work18` — stub SA type 1 + 1 cost; assert 3 vế: `1311 Nợ (total+vat) ref[5113,33311] customer_id`; `5113 Có (total) ref[1311] employee_id=created_by work_id=18`; `33311 Có (vat) ref[1311]`; tất cả cùng `group`.
- [ ] **Step 2:** FAIL → implement `getDataCostAccounting` khung + `prepareData` + `revenueAccounting` (SA-riêng: TK **5113**, Work **18** — KHÁC trait 5111/Work15). `prepareData` port ERP:157–207 (đọc `support_accounting->before_vat_total/_delivery_cost/_product/_repair_service`; `vat_percent` theo type 1→`revenue_costs[0]`, 2→`costs[0]`, else→`delivery_vat_percent`). PASS.
- [ ] **Step 3:** Test `test_deduction_cluster_5213_33311_1311_work19` + `test_cost_cluster_632_1541_per_cost` (632 Nợ tổng ref[1541]; mỗi cost 1541 Có `price*coefficient_cost_price/100` ref[632] `service_accounting_cost_id`). FAIL → implement `revenueDeductionAccounting` (5213/Work19) + `costAccounting` (632/1541). PASS.
- [ ] **Step 4:** Test `test_van_chuyen_skips_cost_cluster` (type 3 → KHÔNG cụm giá vốn) + `test_only_dich_vu_runs_heavy_clusters` (type 2 → KHÔNG 4 cụm nặng; type 1 → CÓ). FAIL → thêm nhánh `if type != VAN_CHUYEN costAccounting`, `if type == DICH_VU { 4 cụm nặng }` + `use SupportAccountingTrait` + định nghĩa hằng `WORK_*` khớp ERP (thưởng HH=12, HH tháng=13, HH quý=14, quỹ rủi ro=6, giảm trừ=19, doanh thu=18). PASS.
- [ ] **Step 5:** Test `test_zero_denominator_yields_no_heavy_lines` (support_accounting mẫu số 0 → percent=0 → 4 cụm 0 dòng, không chia 0) + `test_plbs_posts_to_parent_contract` (contractable PLBS → sau Task 11 contractable_id = parent). FAIL→PASS (guard mẫu số trong `prepareData`).
- [ ] **Step 6: Nạp nguồn hỗ-trợ-hạch-toán.** `$sa->contractable->support_accounting` trả stub `FirmSupportAccounting` (đọc được cột scalar, THIẾU `departments`/`department_main`). 4 cụm nặng cần quan hệ → trong service nạp `\Modules\Assign\Entities\Contract\SupportAccounting::where('contractable_id',$contract->id)->where('contractable_type', <FirmContract FQN>)->first()` truyền vào cụm nặng. **Ruling 9.1** (ghi ledger): trait type-hint `Assign\Contract` cho `$contract` — nếu PHP reject `FirmContract` (Finance), **nới type-hint** trait về không-ràng-buộc (4 method chỉ đọc `company_id`/`customer_id`/`created_by` + quan hệ phòng); đổi file dùng chung → mục này cần xác minh không vỡ `ProductExportPostingService`. Test trait-reuse: `test_bonus_ns_clusters_produce_lines_for_dich_vu`.
- [ ] **Step 7:** Chạy full file xanh. **Commit** `feat(finance): ServiceAccounting posting engine (port FirmContractCostService)`

---

### Task 10: Golden reconcile — bút toán sinh ra KHỚP `account_details` thật

**Files:**
- Create: `Modules/Finance/Tests/Feature/ServiceAccountingPostingReconcileTest.php`

**Interfaces:**
- Consumes: `FirmContractServiceAccountingPostingService::getDataCostAccounting`; `account_details` thật (1275 phiếu FirmContract đã hạch toán, 7257 dòng).

- [ ] **Step 1:** Test `test_generated_journal_matches_stored_account_details` — lấy **mẫu** phiếu `DA_DUYET` thật đủ 3 type (vd 15 DỊCH VỤ + 10 CHI_PHI + 10 VẬN CHUYỂN; `markTestSkipped` nếu DB rỗng). Mỗi phiếu: `getDataCostAccounting($phiếu)` → chuẩn hoá (TK `identify_number`, `money_value`, `type`, `group`, `work_id`, `service_accounting_cost_id`, `customer_id`/`employee_id`) → so **multiset** với `account_details` thật của phiếu (lọc `value>0`). Assert KHỚP từng vế (sai số tiền = 0 đồng).
- [ ] **Step 2: Chạy.** Lệch → **DỪNG**, systematic-debugging (so field lệch đầu tiên), **KHÔNG** sửa công thức ép khớp cho tới khi hiểu gốc. Khi gốc là khác biệt dữ liệu (vd phiếu cũ công thức đời trước) → ghi **Ruling** + thu hẹp mẫu sang phiếu gần đây, KHÔNG nới assert.
- [ ] **Step 3:** XANH trên mẫu. **Commit** `test(finance): ServiceAccounting posting reconciles 1:1 with real account_details`

---

### Task 11: Service store/update/destroy + controller + routes + request + quyền + notify

**Files:**
- Modify: `Modules/Finance/Services/ServiceAccountingService.php`, `Http/Controllers/V1/ServiceAccountingController.php`, `Routes/api.php`
- Create: `Http/Requests/ServiceAccounting/ServiceAccountingStoreRequest.php` + `ServiceAccountingUpdateRequest.php`, `Services/ServiceAccountingNotifyService.php`
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
- Test: `Modules/Finance/Tests/Feature/ServiceAccountingWriteApiTest.php`

**Interfaces:**
- Produces: `POST finance/service-accounting` (store), `POST finance/service-accounting/{id}` (update), `DELETE finance/service-accounting/{id}` (destroy) — tất cả `checkPermission:Hạch toán dịch vụ HĐBH`.
- Consumes: Task 8 (`generateCode`/`syncItems`/`syncCosts`/`canEdit`/`canDelete`/`updateHandoverDate`); Task 9 (`getDataCostAccounting`); `AccountDetail::saveAccountDetail($accounts,$invId,$invType,$invCode,$meta)`; YC `ServiceAccountingRequest` (consts `DA_HACH_TOAN=5`, `approver_id`/`approved_at`).

> **Port ERP `ServiceAccountingController::store/update/delete` (`:123–350`)** nhưng (a) **bọc transaction + rollback mọi nhánh lỗi** (sửa bug ERP: 2 nhánh `return responseErrors` trong khối `DA_DUYET` KHÔNG `DB::rollBack()`); (b) **FirmContract-only** — bỏ nhánh `else getDataCreateDept`; (c) **bỏ** `service_export_request` flip (class vắng — Ruling 11.1) ; (d) notify theo `NotificationMeta::build` (Ruling: thay `NotificationHelper::sendNotify`).

- [ ] **Step 1:** Quyền — thêm dòng `$this->perm(['name'=>'Hạch toán dịch vụ HĐBH','display_name'=>...,'group'=>...,'type'=>23])` vào seeder; `php artisan permission:sync --dry-run` thấy quyền mới. (Không test riêng — kiểm ở Step 7.)
- [ ] **Step 2:** Test `test_store_draft_creates_without_posting` — `status=DANG_TAO` + `service_accounting_request_id` + items/costs → tạo phiếu, copy items/costs, `account_details` 0 dòng, YC KHÔNG lật. FAIL → implement `store()` phần nháp (generateCode, fill contractable từ YC, syncItems/syncCosts). PASS.
- [ ] **Step 3:** Test `test_store_approved_posts_and_flips_request` — `status=DA_DUYET` → `account_details` > 0 (ΣNợ=ΣCó), YC `status=5 + approver_id + approved_at`, `handover_date` set. FAIL → implement nhánh `DA_DUYET` (posting service → `saveAccountDetail` với meta org theo phiếu → flip YC → `updateHandoverDate`) trong transaction. PASS.
- [ ] **Step 4:** Test `test_update_reposts_without_duplicating_account_details` (Review Focus 1) + `test_posting_failure_rolls_back_everything` (Review Focus 2 — ép `saveAccountDetail` false bằng TK không tồn tại → assert 0 dòng, phiếu không `DA_DUYET`, YC không lật). FAIL → implement `update()` (xoá bút toán cũ theo invoiceable trước khi ghi lại; rollback). PASS.
- [ ] **Step 5:** Test `test_update_delete_blocked_when_not_owner_or_approved` (423/403) + `test_destroy_removes_draft_owned` + `test_write_endpoints_forbidden_without_permission` (Review Focus 6 — 403). FAIL → implement guard `canEdit`/`canDelete` đầu service + `destroy()` + route `checkPermission` + FormRequest (nếu FormRequest nuốt guard → chuyển guard sang middleware, bám khuôn khoá bản ghi trong CLAUDE.md). PASS.
- [ ] **Step 6:** Notify — `ServiceAccountingNotifyService` theo `NotificationMeta::build` (mẫu `ServiceAccountingRequestNotifyService`), gọi khi duyệt (báo người lập YC). Test `test_approve_notifies_request_creator`. FAIL→PASS.
- [ ] **Step 7: Full suite** `php -d memory_limit=-1 ./vendor/bin/phpunit Modules/Finance/Tests/Feature` — xanh (trừ 21 pre-existing). **Commit** `feat(finance): ServiceAccounting store/update/destroy + posting + permission`

---

### Task 12: FE — form tạo/sửa + nút Sửa/Xóa

**Files:**
- Create: `pages/finance/service-accounting/create.vue`, `components/ServiceAccountingForm.vue`
- Modify: `pages/finance/service-accounting/_id/index.vue`

**Interfaces:**
- Consumes: BE store/update/destroy; `detailData` Phase 1; cờ BE `is_can_edit`/`is_can_delete` (thêm vào detail resource Task 11).
- Produces: route `/finance/service-accounting/create` + edit qua `_id`.

- [ ] **Step 1:** `ServiceAccountingForm.vue` — chọn YC nguồn (`service_accounting_request_id`), hiển thị items/costs copy (readonly bảng), ô `payed_cost`/`note`; nút **Lưu nháp** / **Lưu và duyệt** (`status` 1/2). Dùng `V2Base*`, `unsavedChangesMixin`, số `toLocaleString('en-US')`. `create.vue` = shell gọi Form.
- [ ] **Step 2:** `_id/index.vue` footer — thêm **Sửa** (`/create?id=` hoặc `_id?edit`) + **Xóa** (`$confirm`), **ẩn** (v-if, không disable) khi `!is_can_edit`/`!is_can_delete`. Đồng bộ nút chi tiết ↔ danh sách (CLAUDE.md).
- [ ] **Step 3: Verify (Playwright, `http://127.0.0.1:3000`)** — (a) tạo nháp từ 1 YC → phiếu `Đang tạo`; (b) sửa phiếu nháp của mình thấy nút Sửa/Xóa, phiếu đã duyệt KHÔNG thấy; (c) không console error.
- [ ] **Step 4: Commit** `feat(finance-fe): ServiceAccounting create/edit form + Sửa/Xóa actions`

---

## Self-review Phase 2 (đã chạy)

1. **Spec coverage:** design §3 posting (getDataCostAccounting, PLBS→parent, rollback-fix, 4 dependency) → Task 8/9/11; §6 quyết định (canEdit/canDelete owner+DANG_TAO; tạo từ YC; FirmContract-only) → Task 8/11; quyền mới → Task 11; FE tạo/sửa → Task 12. ✓
2. **Dependency design §3 (4 mục):** (1) `getDataCostAccounting` → Task 9 (port + tái dùng trait); (2) `updateHandoverDate` → Task 8 (port); (3) `ServiceExportRequest` → **Ruling 11.1 skip** (class vắng); (4) cờ `accounted` → **Ruling 8.1 drop** (cột vắng, YC→5 thay vai trò chống double). ✓
3. **Type consistency:** `getDataCostAccounting(ServiceAccounting)` (Task 9) = caller Task 11; `createDataSaveDept` key thô (Task 9) = cột phẳng `saveAccountDetail` (đã có) = golden chuẩn hoá (Task 10); `INVOICEABLE_TYPE` = key xoá idempotent (Task 11). ✓
4. **Review Focus:** 6 mục → test Task 9 (3,4,5) + Task 11 (1,2,6). ✓
5. **Proportion:** plan = quyết định + tên test + con trỏ dòng ERP; thân hàm KHÔNG chép (port theo path). ✓

**⚠️ Build-time verify Phase 2 (không đoán):** thân `FirmContract::updateHandoverDate()` + `parent_contract()` đọc từ ERP lúc build; helper sinh mã HRM tương đương `autoGenerateCode`; `WORK_*` id khớp `account_details.work_id` thật (đối chiếu ở Task 10); trait type-hint có reject `FirmContract` không (Ruling 9.1); `type` quyền (23 Bán hàng) + `group` hiển thị; detail resource cần thêm `is_can_edit`/`is_can_delete`; FE đường vào Sửa (`create?id` vs `_id?edit`) theo khuôn HDDV/YC.

**Rulings đã chốt sẵn trong plan (sẽ ledger khi execute):**
- **8.1** — BỎ guard `accounted` ở syncItems/syncCosts (cột không tồn tại HRM; chống double = YC lật status 5). *Cost nếu sai:* lý thuyết double-accounting 1 request-item qua 2 phiếu — chặn bởi YC rời pool duyệt sau lật.
- **9.1** — Tái dùng `SupportAccountingTrait`; nếu type-hint reject FirmContract thì nới hint (đổi file chung → xác minh `ProductExportPostingService` không vỡ). *Cost nếu sai:* phải tách bản sao 4 method vào service Finance.
- **11.1** — SKIP lật `ServiceExportRequest` (class vắng ở HRM). *Cost nếu sai:* PXK dịch vụ không tự chuyển "Đã hạch toán" — bổ sung khi có class.
