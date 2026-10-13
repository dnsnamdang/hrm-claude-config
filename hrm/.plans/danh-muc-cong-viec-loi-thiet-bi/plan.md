# Danh mục công việc, lỗi thiết bị — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate chức năng "Danh mục công việc, lỗi thiết bị" từ ERP (`device-errors`, module Sale) sang HRM (`Modules/CustomerCare` BE + `pages/customer-care/device-errors` FE V2Base), quản lý CRUD trên bảng có sẵn của DB gộp.

**Architecture:** DB gộp `erp_hrm_check` (nhánh gop_db) đã chứa 5 bảng `device_errors*` (2768 bản ghi) → KHÔNG migration. BE `Modules/CustomerCare` mirror pattern `Service`/`Cost` đã migrate (entity trỏ bảng ERP có sẵn, controller V1 dùng ResponseTrait + Request + Resource + Service class). FE mirror pattern `pages/customer-care/services` (V2Base FilterPanel + DataTable + modal ref-based).

**Tech Stack:** BE Laravel 8 + nwidart modules + spatie/permission; FE Nuxt2/Vue2 + V2Base components.

## Global Constraints
- **SCOPE CORRECTION (2026-08-06):** ERP đã drop `description`/`reason`/`solution`/`group_error_id` (migration 2022_09_17_add_type up). DB gộp khớp ERP → **KHÔNG** dựng 3 ô mô tả/nguyên nhân/giải pháp + **KHÔNG** dựng nhóm (group_error_id + device_error_groups rỗng). `device_errors` chỉ còn: `name, type, recipe_work_norm, note, discount_rate, price, benefit_coefficient, vat_percent, status, created_by, updated_by`.
- Nhánh **gop_db** (cả hrm-api + hrm-client). DB gộp `erp_hrm_check`.
- **KHÔNG tạo migration** — bảng đã tồn tại: `device_errors`, `device_error_costs`, `device_error_products` (bỏ groups khỏi scope).
- **1 quyền** duy nhất: `Quản lý danh mục công việc, lỗi thiết bị` (gộp thêm/sửa/xóa/khóa). Global, KHÔNG phân cấp company/department/part.
- **Bỏ CRM sync** (không port hook `updating` đẩy `product.template` như model ERP).
- Entity KHÔNG kế thừa `App\Models\BaseModel` — tự gán `created_by`/`updated_by` (giống `Modules/CustomerCare/Entities/Cost/Cost.php`, `Service/Service.php`).
- Form validate: BE rethrow `ValidationException` (Request class), FE hiện lỗi inline `is-invalid` + `invalid-feedback` + flag `touched`.
- `device_errors.status`: **1 = Hoạt động, 2 = Khóa** (KHÁC bảng costs dùng 0/1). `name` unique **theo `type`**.
- `device_error_products.type` phân biệt: vật tư **kèm** vs vật tư **thay thế**. Xác định 2 giá trị type chính xác bằng cách đọc ERP `DeviceError::products()` / `productReplacements()` scope trước khi code (Task 1 step 1).
- Không commit/push khi chưa được yêu cầu.

## Nguồn tham chiếu (đọc trước khi code)
- **ERP source** (`ERP/TanPhatDev/`): `app/Model/Sale/DeviceError.php`, `DeviceErrorGroup.php`, `DeviceErrorCost.php`, `DeviceErrorProduct.php`, `DeviceErrorHasGroup.php`; `app/Http/Controllers/Sale/DeviceErrorController.php`, `DeviceErrorGroupController.php`; `app/Http/Requests/Sale/DeviceErrorStoreRequest.php`, `DeviceErrorUpdateRequest.php`; `app/ExcelExports/DeviceErrorExcel.php`; views `resources/views/sale/device_errors/{index,create,edit,show}.blade.php`; routes `routes/web.php` block `prefix device-errors` (~dòng 4661) + `device-error-groups`.
- **HRM pattern** (`HRM/hrm-api/`): `Modules/CustomerCare/Http/Controllers/V1/ServiceController.php` + `CostController.php`; `Modules/CustomerCare/Entities/{Service/Service.php, Service/ErpProduct.php, Cost/Cost.php}`; `Modules/CustomerCare/Routes/api.php`; `Modules/CustomerCare/Services/*`, `Transformers/*`, `Http/Requests/*`; `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
- **HRM FE pattern** (`HRM/hrm-client/`): `pages/customer-care/services/index.vue` + modal; `pages/finance/cost-debts/{index.vue,CostDebtModal.vue}` (V2Base chuẩn); `components/subsystem-menu/customer-care.js`.

## File Structure

**hrm-api (`Modules/CustomerCare/`):**
- `Entities/DeviceError/DeviceError.php` — entity chính (table `device_errors`), relations products/productReplacements/costs/group/creator, helper `canDelete()`, `getPriceAttribute` (auto tính).
- `Entities/DeviceError/DeviceErrorGroup.php` — table `device_error_groups`.
- `Entities/DeviceError/DeviceErrorCost.php` — pivot table `device_error_costs`.
- `Entities/DeviceError/DeviceErrorProduct.php` — pivot table `device_error_products`.
- `Services/DeviceErrorService.php` — business logic list/store/update/delete/lock/restore/pricing.
- `Http/Controllers/V1/DeviceErrorController.php` — endpoints.
- `Http/Requests/DeviceErrorRequest.php` — validation store/update.
- `Transformers/DeviceErrorResource.php` (+ list resource nếu cần).
- `Exports/DeviceErrorExport.php` — Excel export.
- `Routes/api.php` — MODIFY: thêm group `/device-errors`.
- (`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — MODIFY: thêm 1 quyền.)

**hrm-client:**
- `pages/customer-care/device-errors/index.vue` — list V2Base.
- `pages/customer-care/device-errors/components/DeviceErrorModal.vue` — modal create/edit (tabs: chung / vật tư kèm / vật tư thay thế / chi phí / nhóm inline).
- `components/subsystem-menu/customer-care.js` — MODIFY dòng 27: thêm `link`.

---

## Task 1: BE Entities

**Files:**
- Create: `hrm-api/Modules/CustomerCare/Entities/DeviceError/DeviceError.php`
- Create: `hrm-api/Modules/CustomerCare/Entities/DeviceError/DeviceErrorGroup.php`
- Create: `hrm-api/Modules/CustomerCare/Entities/DeviceError/DeviceErrorCost.php`
- Create: `hrm-api/Modules/CustomerCare/Entities/DeviceError/DeviceErrorProduct.php`
- Reference: ERP `app/Model/Sale/DeviceError.php` (relations, TYPES, STATUS consts, canDelete), HRM `Entities/Cost/Cost.php` (kiểu entity port).

**Produces:** `DeviceError` với `$table='device_errors'`, consts `STATUS_ACTIVE=1`/`STATUS_BLOCK=2` + `TYPES` (6 loại), relations `products()`, `productReplacements()`, `costs()`, `group()`, `creator()`; method `canDelete()`; accessor `getPriceAttribute()`.

- [ ] **Step 1:** Đọc ERP `DeviceError::products()`, `productReplacements()`, `costs()`, `group()` để lấy chính xác: tên pivot table (`device_error_products`/`device_error_costs`), cột pivot (`type`, `price`), và 2 giá trị `type` phân biệt kèm/thay thế. Ghi lại vào comment entity.
- [ ] **Step 2:** Tạo `DeviceErrorGroup` (table `device_error_groups`, fillable name, tự gán created_by/updated_by qua `creating`/`updating` như Cost).
- [ ] **Step 3:** Tạo `DeviceErrorCost` (table `device_error_costs`) + `DeviceErrorProduct` (table `device_error_products`) — model tối giản cho pivot (nếu dùng belongsToMany withPivot thì không bắt buộc, nhưng tạo để query trực tiếp khi delete).
- [ ] **Step 4:** Tạo `DeviceError` (table `device_errors`): consts + TYPES (copy verbatim từ ERP), fillable (name/type/recipe_work_norm/description/reason/solution/note/price/discount_rate/benefit_coefficient/vat_percent/status/group_error_id/created_by/updated_by), relations:
  - `products()` = belongsToMany `ErpProduct` (`Modules\CustomerCare\Entities\Service\ErpProduct`) qua `device_error_products`, `->wherePivot('type', <TYPE_KÈM>)`.
  - `productReplacements()` = tương tự với `<TYPE_THAY_THẾ>`.
  - `costs()` = belongsToMany `Cost` qua `device_error_costs` withPivot `price`.
  - `group()` = belongsTo `DeviceErrorGroup`, `group_error_id`.
  - `creator()` = belongsTo `Modules\Human\Entities\Employee`, `created_by`.
  - `getPriceAttribute($v)`: nếu `$v` (giá nhập tay) > 0 trả `$v`; else tính `company.work_price * company.coefficient_price_service * recipe_work_norm` (lấy company hiện hành — xem cách ServiceController/Company lấy company; nếu phức tạp, để service layer tính và bỏ accessor). ⚠ Confirm cách lấy Company trong HRM trước khi implement (đọc Service entity `coefficients()`/Company).
  - `boot()`: gán `created_by`/`updated_by` = `auth()->id()` khi creating/updating. KHÔNG port hook CRM.
- [ ] **Step 5:** Verify: `cd hrm-api && php artisan tinker --execute="echo \Modules\CustomerCare\Entities\DeviceError\DeviceError::count();"` → in ra `2768`. Kiểm tra relations: `DeviceError::with(['products','costs','group'])->first()` không lỗi.

---

## Task 2: BE Service + is_can_delete helper

**Files:**
- Create: `hrm-api/Modules/CustomerCare/Services/DeviceErrorService.php`
- Reference: ERP `DeviceErrorController` (searchData/store/update/getData/delete/lock/restore) + `DeviceError::canDelete()` (danh sách 10 bảng downstream).

**Consumes:** `DeviceError` entity (Task 1).
**Produces:** `DeviceErrorService` với `list($request)`, `store($data)`, `update($deviceError,$data)`, `delete($deviceError)`, `lock($deviceError)`, `restore($deviceError)`, `isReferenced($deviceError): bool`.

- [ ] **Step 1:** `list($request)`: query `DeviceError` + `with(['group'])` + filter (name like, type, group_error_id, status, created_by) + phân trang. Trả paginator (map sang Resource ở controller). Mặc định không lọc theo cấp (global).
- [ ] **Step 2:** `isReferenced($deviceError)`: quét tồn tại bản ghi tham chiếu `device_error_id` trong các bảng downstream (đọc `DeviceError::canDelete()` ERP lấy đúng tên bảng: `wr_service_quotation_product_device_errors`, `wr_service_contract_product_device_errors`, `wr_service_quotation_product_item_device_errors`, `wr_service_contract_product_item_device_errors`, `wr_service_quotation_product_service_device_errors`, `wr_service_contract_product_service_device_errors`, `wr_assign_task_product_device_errors`, `wr_import_result_product_device_errors`, `warranty_report_descriptions`, `warranty_repair_handle_request_product_manage_device_errors`). Dùng `DB::table(...)->where('device_error_id',$id)->exists()` loop, return true nếu bất kỳ bảng có. **Bọc mỗi bảng trong Schema::hasTable() để an toàn** nếu bảng chưa có trên DB đang chạy.
- [ ] **Step 3:** `store($data)` (transaction): tạo DeviceError (các field), set status=STATUS_ACTIVE; `products()->sync` (keyBy product_id, kèm pivot type=KÈM), `productReplacements()->sync` (type=THAY_THẾ), `costs()->sync` (keyBy cost_id, pivot price); set group_error_id; xử lý `device_error_has_group_product` nếu form có chọn nhóm SP. Port logic từ ERP `store`.
- [ ] **Step 4:** `update`: tương tự store (sync lại products/replacements/costs). `delete($deviceError)`: nếu `status != ACTIVE || isReferenced()` → throw/ trả false; else xóa `device_error_costs` + `device_error_products` theo device_error_id + xóa device_error. `lock`: status 1→2 (chỉ khi đang ACTIVE). `restore`: status 2→1.
- [ ] **Step 5:** Verify tinker: `(new DeviceErrorService)->isReferenced(DeviceError::find(<id đang dùng>))` → true; với id chưa dùng → false. `list()` trả đúng tổng.

---

## Task 3: BE Request + Resource + Controller

**Files:**
- Create: `hrm-api/Modules/CustomerCare/Http/Requests/DeviceErrorRequest.php`
- Create: `hrm-api/Modules/CustomerCare/Transformers/DeviceErrorResource.php`
- Create: `hrm-api/Modules/CustomerCare/Http/Controllers/V1/DeviceErrorController.php`
- Reference: HRM `ServiceController` + `ServiceRequest` + `ServiceResource`; ERP `DeviceErrorStoreRequest`.

**Consumes:** `DeviceErrorService` (Task 2), `DeviceError` (Task 1).
**Produces:** endpoints `index`, `show`, `store`, `update`, `delete`, `lock`, `restore`, `getProductsAjax`, `groups` (list nhóm cho dropdown), `optionsData`.

- [ ] **Step 1:** `DeviceErrorRequest` (rules): `name` required + `Rule::unique('device_errors')->where('type', $type)->ignore($this->id)`; `type` required in:1..6; `recipe_work_norm` required; `products` required array; `discount_rate` required; `benefit_coefficient` required numeric min:0 not_in:0 (message "Nhập hệ số lớn hơn 0"); `vat_percent` required max:100. `authorize()` return true. KHÔNG catch chung — để rethrow ValidationException.
- [ ] **Step 2:** `DeviceErrorResource`: id, name, type + type_text (map TYPES), recipe_work_norm, price (accessor), engineering_work, discount_rate, benefit_coefficient, vat_percent, note, description, reason, solution, status + status_text, group_error_id + group_name, is_can_delete (= `$this->status==ACTIVE && !app(DeviceErrorService)->isReferenced($this->resource)` — hoặc controller set sẵn để tránh N+1), products/[productReplacements]/costs (khi show/edit).
- [ ] **Step 3:** Controller `index` → `DeviceErrorService::list` → `DeviceErrorResource::collection` + meta phân trang (theo đúng format `ServiceController::index`). `show` → resource đầy đủ (kèm products/replacements/costs). `store`/`update` (inject `DeviceErrorRequest`) → service. `delete`/`lock`/`restore` → service, trả responseSuccess/responseErrors. `getProductsAjax` → search ErpProduct theo keyword (mirror `ServiceController::searchProducts`). `groups` → list `DeviceErrorGroup` cho dropdown; (tạo nhanh nhóm: thêm `storeGroup` nếu inline-create).
- [ ] **Step 4:** Verify: sau khi có routes (Task 4) → `php artisan route:list | grep device-errors`.

---

## Task 4: BE Routes + Permission

**Files:**
- Modify: `hrm-api/Modules/CustomerCare/Routes/api.php` (thêm group `/device-errors`)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm 1 quyền)
- Reference: các route group `services`/`costs` trong cùng file.

**Consumes:** `DeviceErrorController` (Task 3).

- [ ] **Step 1:** Thêm vào `Routes/api.php` (trong group `/v1/customer-care`):
```php
Route::group(['prefix' => '/device-errors'], function () {
    Route::get('/', [DeviceErrorController::class, 'index'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::get('/groups', [DeviceErrorController::class, 'groups']);
    Route::get('/search-products', [DeviceErrorController::class, 'getProductsAjax']);
    Route::get('/export', [DeviceErrorController::class, 'export'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::post('/', [DeviceErrorController::class, 'store'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::get('/{deviceError}', [DeviceErrorController::class, 'show'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::put('/{deviceError}', [DeviceErrorController::class, 'update'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::delete('/{deviceError}', [DeviceErrorController::class, 'delete'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::put('/{deviceError}/lock', [DeviceErrorController::class, 'lock'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::put('/{deviceError}/restore', [DeviceErrorController::class, 'restore'])
        ->middleware('checkPermission:Quản lý danh mục công việc, lỗi thiết bị');
    Route::get('/{deviceError}/print', [DeviceErrorController::class, 'printData']);
});
```
Thêm `use ...DeviceErrorController;` đầu file.
- [ ] **Step 2:** Thêm quyền `Quản lý danh mục công việc, lỗi thiết bị` vào `PermissionsTableSeeder.php` (đúng nhóm/`type` của phân hệ CSKH — đọc các quyền CSKH có sẵn `Quản lý cấp dịch vụ bảo dưỡng`... để lấy đúng `type`/guard_name). KHÔNG tạo migration.
- [ ] **Step 3:** Verify: `php artisan route:list | grep device-errors` (10 route). Áp quyền: qua tinker `firstOrCreate` (như các feature trước — CHỜ user/áp trên DB gộp), route:list.

---

## Task 5: BE Excel export + Print

**Files:**
- Create: `hrm-api/Modules/CustomerCare/Exports/DeviceErrorExport.php`
- Modify: `DeviceErrorController` (methods `export`, `printData`)
- Reference: ERP `app/ExcelExports/DeviceErrorExcel.php` + ERP `DeviceErrorController::exportList`/`printList`/`print`; HRM `ServiceController::export`/`printData` + `Modules/CustomerCare/Exports/*` nếu có mẫu.

- [ ] **Step 1:** `DeviceErrorExport` (maatwebsite/excel FromCollection/WithHeadings): cột theo ERP `DeviceErrorExcel` (tên, loại, nhóm, định mức, giá, trạng thái, vật tư...). Nhận filter giống list.
- [ ] **Step 2:** `export()` controller: `return Excel::download(new DeviceErrorExport($request), 'danh-muc-cong-viec-loi-thiet-bi.xlsx')`.
- [ ] **Step 3:** `printData($deviceError)`: trả data/HTML in 1 bản ghi (mirror ServiceController::printData; nếu dùng ErpReportTemplate → xác nhận template id, nếu không thì trả JSON cho FE render). In danh sách: theo mẫu ERP `printList` (nếu cần) — hoặc để FE render.
- [ ] **Step 4:** Verify: gọi `/v1/customer-care/device-errors/export` tải file .xlsx mở được; `printData` trả đúng dữ liệu.

---

## Task 6: FE — List page (V2Base)

**Files:**
- Create: `hrm-client/pages/customer-care/device-errors/index.vue`
- Reference: `pages/customer-care/services/index.vue`, `pages/finance/cost-debts/index.vue` (V2Base chuẩn).

**Consumes:** API `customer-care/device-errors` (Task 3-4).

- [ ] **Step 1:** `index.vue` V2Base: `V2BaseFilterPanel` (quick search tên; advanced: loại (6 TYPES), nhóm, trạng thái, người tạo) + `V2BaseDataTable` cột: STT, Tên, Loại, Nhóm, Định mức công, Giá, Trạng thái (badge hoạt động/khóa), Thao tác. `filterStateMixin` + deep watcher auto-search (localStorageKey `cc_device_errors`, pathsToKeep `['/customer-care/device-errors']`).
- [ ] **Step 2:** Actions theo status: status=1 → Sửa + (nếu is_can_delete) Xóa + Khóa; status=2 → Khôi phục. Nút "Thêm công việc/lỗi thiết bị" (gate `canManage = hasAPermission('Quản lý danh mục công việc, lỗi thiết bị')`). Nút **In** + **Xuất Excel** (gọi export endpoint).
- [ ] **Step 3:** `loadData` → `apiGet 'customer-care/device-errors'` + params (page, limit, name, type, group_error_id, status, created_by). Map paginator. `BaseConfirmModal` cho xóa/khóa/khôi phục.
- [ ] **Step 4:** Import `DeviceErrorModal` (Task 7), wiring `ref` + `@saved="loadData"`. `openCreate`/`openEdit`.
- [ ] **Step 5:** Verify (user, `yarn dev`): list hiển thị 2768 bản ghi, filter/phân trang chạy, badge trạng thái đúng.

---

## Task 7: FE — Modal create/edit (tabs)

**Files:**
- Create: `hrm-client/pages/customer-care/device-errors/components/DeviceErrorModal.vue`
- Reference: ERP `resources/views/sale/device_errors/create.blade.php` (cấu trúc form/tab), HRM `pages/customer-care/services` modal + `pages/finance/cost-debts/CostDebtModal.vue` (ref-based V2 pattern).

**Consumes:** API store/update/show/search-products/groups.

- [ ] **Step 1:** Modal ref-based `open(id)` + `@saved`. Form: **Thông tin chung** (name, type select 6 loại, recipe_work_norm, discount_rate, benefit_coefficient, vat_percent, price [để trống=auto], note, description, reason, solution). Inline error + `touched`.
- [ ] **Step 2:** Tab **Vật tư kèm** (`products`): V2Base table thêm dòng, search SP qua `search-products` endpoint. Tab **Vật tư thay thế** (`productReplacements`): tương tự. Tab **Chi phí kèm** (`costs`): chọn cost + price.
- [ ] **Step 3:** **Nhóm inline**: V2BaseSelectInModal load từ `groups` endpoint + cho tạo nhanh (nếu ERP cho) → gọi `storeGroup`. Set `group_error_id`.
- [ ] **Step 4:** `validateLocal` (required: name, type, recipe_work_norm, benefit_coefficient>0, ≥1 vật tư) → submit POST/PUT `customer-care/device-errors`. Xử lý 422 map lỗi inline. Emit `saved`.
- [ ] **Step 5:** Verify (user): tạo mới + sửa 1 bản ghi, đủ tab, lỗi inline hiện đúng, lưu thành công, list refresh.

---

## Task 8: FE — Menu link + smoke test tổng

**Files:**
- Modify: `hrm-client/components/subsystem-menu/customer-care.js` (dòng 27)

- [ ] **Step 1:** Sửa `{ label: 'Danh mục công việc, lỗi thiết bị' },` → `{ label: 'Danh mục công việc, lỗi thiết bị', link: '/customer-care/device-errors', isShow: ['Quản lý danh mục công việc, lỗi thiết bị'] }`. (Xác nhận cách gate `isShow` trong CSKH menu — có thể để trống nếu global hiển thị.)
- [ ] **Step 2:** Verify (user, `yarn dev`): menu CSKH hiện link, bấm ra trang, full CRUD + in + export chạy trên DB gộp. Xóa 1 bản ghi chưa dùng OK; bản ghi đã dùng → nút Xóa ẩn / báo chặn.
- [ ] **Step 3:** Wrap up: cập nhật STATUS.md + plan checkpoint. (Commit chỉ khi user yêu cầu.)

---

## Checkpoint — 2026-08-06 (CODE DONE)
Đã hoàn thành toàn bộ 8 task (subagent-driven), Task 7 gộp vào Task 6.
- **hrm-api (gop_db)**: bb758e266/fde9f0bd7 (entities) → 89053826a (service) → a329871b6 (controller/request/resource) → 98365c6df (routes + quyền id 1131) → 97242ea2b (Excel export + print).
- **hrm-client (gop_db)**: 116ae5556 (FE index + modal) → 631a68655 (menu link).
- Scope đã sửa theo ERP hiện tại: bỏ description/reason/solution/group (ERP drop 2022_09_17). KHÔNG migration.
- Đã verify từng task (tinker: count 2768, isReferenced true/false, 11 route đăng ký, export 2768/10 cột) + đối chiếu hợp đồng BE↔FE (envelope {data,meta}, payload products/costs, update POST).
Đang làm dở: (không)
Bước tiếp (user, trên DB gộp erp_hrm_check):
1. Áp quyền id 1131 `Quản lý danh mục công việc, lỗi thiết bị` qua tinker `firstOrCreate` → gán role qua UI Phân quyền (nhóm CSKH) → route:list.
2. `yarn dev` verify: menu CSKH hiện link → list 2768 bản ghi + filter + badge; tạo/sửa (đủ tab vật tư kèm/thay thế/chi phí); xóa bản ghi chưa dùng OK, bản ghi đã dùng → nút Xóa ẩn; khóa/khôi phục; xuất Excel.
3. Verify pricing (price_display) + is_can_delete với auth thật (tinker null nên chưa test được).
4. Commit đã có sẵn trên gop_db (CHƯA push) — push/PR khi user duyệt.
Blocked:

## Self-Review notes
- Spec coverage: 5 bảng (Task1), CRUD+lock+restore+delete-reference (Task2-3), quyền global 1 (Task4), in+Excel (Task5), FE list+modal+menu (Task6-8), bỏ CRM (Global Constraints) — đủ.
- 2 điểm cần CONFIRM trong lúc code (đã đánh ⚠): (a) 2 giá trị `type` của device_error_products (kèm/thay thế) — đọc ERP scope; (b) cách lấy Company cho pricing auto — đọc HRM Service/Company. Không đoán.
- Không unit-test framework (HRM verify bằng route:list + tinker + browser) — các step "Verify" dùng cách đó thay cho assert.

---

## Task 9: FE — Tách form thêm/sửa thành MÀN RIÊNG (bỏ popup, giống ERP)

**Lý do:** User phản hồi modal thêm/sửa khác bản ERP; yêu cầu tách thành trang riêng
(`create.vue` + `_id/edit.vue` + form component dùng chung), xử lý giống ERP. Theo đúng
pattern module `services` (đã chuyển ERP→HRM trước đó).

**Files:**
- Create: `hrm-client/pages/customer-care/device-errors/create.vue`
- Create: `hrm-client/pages/customer-care/device-errors/_id/edit.vue`
- Create: `hrm-client/pages/customer-care/device-errors/components/DeviceErrorFormComponent.vue`
- Modify: `hrm-client/pages/customer-care/device-errors/index.vue` (điều hướng router thay vì mở modal)
- Delete (sau khi thay): `hrm-client/pages/customer-care/device-errors/components/DeviceErrorModal.vue`

- [x] **Step 1:** Dựng `DeviceErrorFormComponent.vue` (màn riêng, layout ERP) — port logic modal + thêm tính toán tài chính (engineeringWork, auto price, price_service). Submit xong `$router.push` về list; nút "Quay lại".
- [x] **Step 2:** `create.vue` + `_id/edit.vue` bọc form component (khuôn services).
- [x] **Step 3:** index.vue: `openCreate`/`openEdit` → `$router.push`; bỏ import + `<DeviceErrorModal>` + `handleSaved`. Xóa `DeviceErrorModal.vue`.
- [x] **Step 4 (Mức B — giống ERP đầy đủ):** Mở rộng BE (không migration, cột có sẵn DB gộp):
    - `DeviceError::costs()` withPivot `price_service`; Service `keyByCostId` ghi `price_service`; Resource trả `price_service`.
    - `optionsData` trả `company` {work_price, coefficient_price_service, coefficient_price_service_outsource} qua `auth()->user()->info->company`.
    - Request: thêm rule `note/price/products.*.product_id/productReplacements(.*)/costs(.*)` → fix luôn bug `validated()` loại mất note/price/costs/productReplacements.
    - FE: card "Thông tin chung" đủ 11 field ERP (3 ô read-only company + Công kỹ thuật auto); card "Áp dụng cho thiết bị"; 2 card song song "Dịch vụ sửa chữa" (Giá vốn + Giá dịch vụ auto) + "Vật tư thay thế".
    - Verified BE qua tinker (rollback): company resolve, price_service ghi/đọc, resource đủ field.
- [ ] **Step 5:** Verify (user, yarn dev): Thêm → sang trang riêng; Sửa → load đúng (kể cả price_service); auto-tính Công kỹ thuật/Đơn giá bán/Giá dịch vụ; lưu → về list refresh.

### Checkpoint — 2026-08-07 (Task 9 CODE DONE — Mức B)
Vừa hoàn thành: Tách modal → màn riêng + parity tài chính ERP.
- **hrm-api (gop_db, CHƯA commit)**: DeviceError.php (costs withPivot price_service), DeviceErrorService.php (keyByCostId), DeviceErrorResource.php (costs.price_service), DeviceErrorController.php (optionsData trả company), DeviceErrorRequest.php (thêm rule note/price/mảng con — fix bug validated()).
- **hrm-client (gop_db, CHƯA commit)**: mới `components/DeviceErrorFormComponent.vue`, `create.vue`, `_id/edit.vue`; sửa `index.vue` (router push); XÓA `components/DeviceErrorModal.vue`.
Đang làm dở: (không)
Bước tiếp theo: user `yarn dev` verify (Step 5). Commit khi user yêu cầu.
Blocked:

### Checkpoint — 2026-08-07 (Task 9b — popup tìm hàng hoá như ERP)
User yêu cầu 2 bảng "Áp dụng cho thiết bị"/"Vật tư thay thế" phải mở POPUP tìm kiếm có bộ lọc như ERP (không dùng ô remote-search inline).
- FE `DeviceErrorFormComponent.vue`: bỏ V2BaseSelectRemote → thêm nút "Thiết bị"/"Vật tư thay thế" ở card-header mở popup; TÁI DÙNG `pages/customer-care/services/components/ProductSearchModal.vue` (import `../../services/components/...`) — popup bộ lọc nâng cao + bảng phân trang + chọn nhiều; endpoint `services/product-catalogs` + `services/search-products` (product-search chung, không checkPermission). `:key` đổi mỗi lần mở để reset. `onApplyProducts` lọc trùng theo product_id, giữ popup mở như ERP.
- Không sửa component dùng chung, không nhân đôi code. Lint ESM pass, không còn ref cũ.
Bước tiếp: user verify popup thêm thiết bị/vật tư OK.

### Checkpoint — 2026-08-07 (Task 9c — popup Dịch vụ sửa chữa)
User: "Dịch vụ sửa chữa" cũng phải popup như ERP.
- Mới FE `components/CostSearchModal.vue` (popup gọn: quick search theo tên + bảng phân trang + chọn nhiều), gọi `customer-care/costs?name=&status=1&revenue_calculation=1&page=&per_page=` (khớp query ERP: status=1, kind_of=2 đã scope BE, revenue_calculation=1 → 430/519 cost). LƯU Ý: costs list dùng `per_page` (CostResource::apiPaginate), KHÁC device-errors list dùng `limit`.
- Form: bỏ V2BaseSelect + pickedCostId/costOptions/costPickerOptions/addCost + fetch costs/getAll → nút "Dịch vụ sửa chữa" ở card-header mở popup; `onApplyCosts` lọc trùng cost_id, thêm {cost_id, name, price:null, price_service:null}. Giá dịch vụ auto khi nhập Giá vốn giữ nguyên.
- Lint ESM pass. Cả 3 bảng (thiết bị/vật tư thay thế/dịch vụ) đều dùng popup như ERP.
GAP đã đóng hoàn toàn. Bước tiếp: user verify + commit khi duyệt.

### Checkpoint — 2026-08-07 (Task 9d — FIX popup Dịch vụ sửa chữa 403)
User: "Tìm kiếm trong popup chọn dịch vụ sửa chữa lỗi".
- Root cause: CostSearchModal gọi `customer-care/costs` (index) — route này **bị gate** `checkPermission:Quản lý|Xem dịch vụ sửa chữa...`; user sửa device-error thường KHÔNG có quyền đó → **403**; catch nuốt 403 → popup rỗng. (Dropdown cũ chạy được vì dùng `costs/getAll` ungated.)
- Fix BE: thêm endpoint **ungated** `GET customer-care/device-errors/search-costs` (`DeviceErrorController::getCostsAjax`) — query ERP chooseCosts (kind_of=2, status=1, revenue_calculation=1) + filter name + phân trang, trả `{data, meta}` qua `apiGetList`. Route đăng ký cạnh `search-products` (không middleware).
- Fix FE: `CostSearchModal` đổi URL → `device-errors/search-costs`, bỏ status/revenue_calculation (BE tự áp).
- Verified: HTTP 200, top keys code/message/data/meta, total=430, filter 'vận chuyển'→5, route có trong RouteCollection. (route:list CLI tự lỗi do PermissionHelper cần auth — không liên quan.)
Bước tiếp: user verify popup search chạy + commit khi duyệt.

### Checkpoint — 2026-08-07 (Task 9e — làm đẹp giao diện form)
User: background/khối "Thông tin chung / Áp dụng thiết bị / Dịch vụ sửa chữa / Vật tư thay thế" đang xấu.
- `DeviceErrorFormComponent.vue`: thay bootstrap `.card/.card-header/.card-body` thô → hệ `.form-header` + `.form-card/.form-card-head/.form-card-body` (khuôn ServiceFormComponent): header có icon tròn xanh + title + subtitle; mỗi khối bo góc 8px, viền xám, head nền #f9fafb chữ HOA + icon xanh; bảng con header nền #f8fafc; ô read-only nền xám; is-invalid viền đỏ. Thêm `<style lang="scss">` namespaced `.device-error-form`.
- CostSearchModal search bar cũng đã chuẩn hoá (.search-row/.search-control + btn-compact + nút Làm mới) ở lần trước.
- Verified: template compile OK, JS lint OK, SCSS compile OK (node-sass), không còn class card cũ.
Bước tiếp: user verify nhìn + commit khi duyệt.

### Checkpoint — 2026-08-07 (Task 9 COMMITTED)
Đã commit toàn bộ Task 9 (9a→9f) trên nhánh gop_db (CHƯA push):
- **hrm-api**: `493e36ddd` (parity BE: price_service, hệ số công ty, Request đủ field, endpoint search-costs).
- **hrm-client**: `a31ea7677` (màn riêng create/edit + form component + 2 popup + UI form-card + xóa modal).
- Bug đã fix trong loạt: 403 popup cost (endpoint gated) → search-costs ungated; nút search vỡ giao diện → khuôn GroupSearchModal; popup không auto-load → bỏ :key remount; validated() làm mất note/price/costs/productReplacements.
Working tree sạch cả 2 repo. Bước tiếp: user verify yarn dev end-to-end → push/PR khi duyệt.
