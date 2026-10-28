# Rebuild màn Phiếu xuất hàng HRM cho giống ERP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng lại màn tạo Phiếu xuất hàng HRM (`create.vue`) thành MỘT form thống nhất khớp ERP: hai đường nạp (PXK / YCXH) → cùng state, cho chọn lại nguồn, các khối tự ẩn/hiện theo loại xuất, khối tài khoản read-only (loại 1–4), tab Nhóm HĐ hãng (14/15), và các field nhập tay tài khoản (loại 9/10/18/19).

**Architecture:** FE Nuxt 2/Vue 2 (`hrm-client`) rebuild `pages/finance/product-exports/create.vue` thành bố cục tab, điều khiển bằng 5 computed cờ chạy theo `type`. BE Laravel 8 (`hrm-api`, module `Assign`) bổ sung 2 endpoint nạp form (`productExportData`, `productExportDataFromRequest`) để trả `type` + ~27 field hiển thị + `tabs` + danh mục; store ghi thêm các cột nhập tay vào bảng dùng chung `product_exports` (DB gộp `erp_hrm_check`) **không nối hạch toán**.

**Tech Stack:** Vue 2.6 / Nuxt 2.14, V2Base* components, Laravel 8 / PHP 7.4, MySQL dùng chung `erp_hrm_check`, Playwright MCP (http://127.0.0.1:3000) để verify FE, `php artisan tinker` để verify BE.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-09-product-export-form-rebuild-design.md` (plan argue từ spec này; executor đọc cả hai).

## Global Constraints

- **gop_db**: DB dùng chung `erp_hrm_check`, ưu tiên bảng ERP sẵn có. **KHÔNG** dùng `DB_CONNECTION_SECOND` / `mysql2`.
- **Mảng cờ ẩn/hiện — copy verbatim ERP** (`ProductExport.blade.php:335-349`): `has_customer=[1,2,8,12,14,16,17]`, `is_sale=[1,11,13,14,16,17]`, `show_allocated_price=[1,4,11,13,14,16,17]`, `has_contract=[1,2,8,11,13,14,16,17]`, `has_delivery = (warehouse_export.transition_type == 2)`.
- **HĐ hãng = loại 14, 15** (KHÔNG phải 20/21).
- **Loại 15 = Cách A**: không nằm trong bất kỳ mảng cờ nào → render tối giản; chỉ hiện tab Nhóm nếu phiếu có `tabs`. Không thêm logic ERP không có.
- **Khối tài khoản read-only (hardcode, chỉ hiển thị)** theo `type`: `1`→Nợ 1311 · Doanh thu 5111 · Kho 1561 · Thuế 33311 · Giá vốn 632 · Chiết khấu 5211 · Giảm giá 5213; `2`→Giá vốn 632 · Kho 1561; `3`→Nợ 157 · Kho 1561; `4`→Nợ 3311 · Kho 1561 · Kho 1331.
- **KHÔNG đụng hạch toán**: field nhập tay loại 9/10/18/19 chỉ GHI CỘT trên `product_exports` (`account_debt`, `account_has`, `cost_debt_id`, `work`, `accounting_date`, `branch_transfer_coefficient`, `attachments`), **KHÔNG** nối `postAccounting` cho các loại này (G1–G4 ngoài phạm vi — spec §5). Hạch toán 20/21 + bốc xếp đã port, giữ nguyên.
- **Giữ nguyên khối Bốc xếp** (`arrange_delivery` + `executors`) và bảng Hàng hóa hiện có — chỉ bọc vào tab, không refactor logic đã chạy.
- **UI**: `V2Base*` bắt buộc (không raw HTML form element); `button-convention` (icon + `size="sm"`, variant/màu/chữ chuẩn); `.text-muted` ĐỎ → dùng `#6b7280`; đỏ chỉ dành cho lỗi validate; số theo en-US (`toLocaleString('en-US')`). Nút ghi dữ liệu: `$safeLoadingStart()`/`$safeLoadingFinish()` (finally) + `:interactable="!submitting"`. Sau khi lưu → về danh sách.
- **Quyền fail-closed**: reuse gate `'Kế toán kho'` (`assertCanExportGoods` / `assertCanExportFromRequest`) — KHÔNG tạo quyền mới, KHÔNG phân cấp.
- **Git**: KHÔNG commit/push khi chưa có yêu cầu của user. Mỗi task kết bằng bước **Checkpoint** (ghi STATUS + chờ review), không `git commit`.
- **Hàm dùng chung**: KHÔNG tự sửa (`FirmContractExportStockService`, helper kho, Resource dùng chung) — chỉ gọi lại (read-only reuse) hoặc thêm method mới cục bộ. `is_can_delete` / phân quyền theo cấp phải hỏi user.
- **Phối hợp**: FE đụng `product-exports/create` phải báo teammate (ghi chú erp-hrm-44 trong plan.md gốc) trước khi khởi động.

## Review Focus

- **Đổi nguồn PXK→YCXH rồi submit**: `type`, `tabs`, `products`, `account_debt`, `accounting_warehouses` của nguồn CŨ phải reset sạch khi chọn nguồn mới → test ở Task 12 (sau `onChoose*` gọi `resetSourceState()` rồi `fetchData()`).
- **Loại 15 có `firm_contract_id`**: phải hiện tab Nhóm NHƯNG KHÔNG hiện khối KH/HĐ/NVKD/TK read-only (15 không ∈ cờ nào) → điều kiện tab Nhóm gắn vào `form.tabs.length`, KHÔNG gắn `hasContract` → test ở Task 11.
- **Loại 14 nhiều Nhóm**: `remainingByContractProduct` trả map phẳng theo `contract_product_id`; nếu không join được `firm_contract_tabs.name` thì tab hiện tên rỗng → test ở Task 3 (tab có `name` khác rỗng).
- **Loại 9/10/18/19 submit thiếu TK/mã phí/vụ việc**: ERP validate `642*`→`cost_debt`, `154*`→`work` bắt buộc; FE phải chặn inline ĐỎ, BE validate trả 422 (không 500) → test ở Task 5 + Task 10.
- **Luồng YCXH `id=null`**: nếu BE không đổ `type` vào object `warehouse_export` thì mọi cờ=false → form trắng; phải test cả 2 nguồn đều có `type` → test ở Task 1.

---

## File Structure

**BE** — `hrm-api/Modules/Assign/`
- `Http/Controllers/Api/V1/ProductExportController.php`
  - `productExportData($warehouseExportId)` (:437) — enrich payload (type, fields, tabs, catalogs).
  - `productExportDataFromRequest($productExportRequestId)` (:764) — enrich tương tự.
  - `storeProductExport` (:526) + `storeProductExportFromRequest` (:849) — validate + nhận field nhập tay.
  - Thêm 2 private helper mới: `enrichWarehouseExportDisplay()`, `buildFirmContractTabs()`, `formCatalogs()`.
- `Services/ProductExportService.php`
  - `createFromWarehouseExport` (:134) + `createFromProductExportRequest` (:386) — map cột nhập tay vào `product_exports`.

**FE** — `hrm-client/pages/finance/product-exports/create.vue` (rebuild) + có thể tách:
- `components/assign/product-export/ProductExportAccountBlock.vue` (khối TK read-only hardcode).
- `components/assign/product-export/ProductExportGroupTabs.vue` (tab Nhóm read-only).

---

## Task 1: BE — trả `type` ở cả 2 endpoint nạp form

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportController.php:437` (`productExportData`) và `:764` (`productExportDataFromRequest`)

**Interfaces:**
- Produces: payload `warehouse_export` object có thêm key `type` (int). FE Task 6 đọc `data.warehouse_export.type`.

- [ ] **Step 1: Xác định điểm build `warehouse_export`** — Đọc 2 method `productExportData` (:437) và `productExportDataFromRequest` (:764) để thấy nơi dựng object `warehouse_export` trả về (hiện 4 key: `warehouse_export`, `products`, `accounting_warehouses`, `arrange_goods`).

- [ ] **Step 2: Thêm `type` vào object trả về**

```php
// productExportData(): $we = WarehouseExport đã load
$warehouseExport['type'] = (int) $we->type;

// productExportDataFromRequest(): $per = ProductExportRequest
$warehouseExport['type'] = (int) $per->type;
```

- [ ] **Step 3: Verify (tinker) — cả 2 nguồn có `type`**

```bash
cd hrm-api && php artisan tinker
```
```php
// PXK: thay <WE_ID> bằng 1 warehouse_export tồn tại (vd lấy từ warehouse-export-sources)
$c = app(\Modules\Assign\Http\Controllers\Api\V1\ProductExportController::class);
// hoặc gọi query trực tiếp để xác nhận cột type có giá trị:
\Modules\Assign\Entities\Warehouse\WarehouseExport::find(<WE_ID>)->type;         // kỳ vọng: int loại xuất
\Modules\Assign\Entities\Warehouse\ProductExportRequest::find(<PER_ID>)->type;   // kỳ vọng: int loại xuất
```
Expected: cả hai trả về số nguyên loại xuất (không null).

- [ ] **Step 4: Verify (Playwright) — response endpoint chứa `type`**
Mở `http://127.0.0.1:3000/finance/product-exports/create?warehouse_export_id=<WE_ID>`, xem network request `product-export-data` → JSON `warehouse_export.type` có giá trị. Lặp với `?product_export_request_id=<PER_ID>`.
Expected: cả hai response có `warehouse_export.type`.

- [ ] **Step 5: Checkpoint** — Ghi vào `plan.md` Phase 4: "Task 1 xong — 2 endpoint trả `type`." Chờ review. (KHÔNG commit.)

---

## Task 2: BE — enrich `warehouse_export` đủ field hiển thị read-only

**Files:**
- Modify: `ProductExportController.php` — thêm private `enrichWarehouseExportDisplay(array $we, $source): array` và gọi trong cả 2 endpoint.

**Interfaces:**
- Consumes: `type` (Task 1).
- Produces: object `warehouse_export` có thêm các key RO (string, nullable): `stocker_name`, `receiver_name`, `sale_employee_name`, `contract_link`, `contract_code`, `supplier_code`, `supplier_name`, `emplement_contract_code`, `emplement_contract_link`, `export_requester`, `export_request_department`, `accounting_date`, `export_request_code`, `is_export_direct` (bool), `join_export_request` (`{id,code}`|null), `branch_transfer_coefficient`, `account_debt`, `account_has`, `cost_debt_id`, `work`, `documents` (mảng url). (`customer_name`, `warehouse_name` đã có.) FE Task 8 bind các key này.

- [ ] **Step 1: Đọc nguồn ERP để khớp ngữ nghĩa từng field** — Đọc `ERP .../app/Model/Warehouse/ProductExport.php:242-358` (`getDataForEdit`) và `.../WarehouseExport.php:329-401` + `.../ProductExportRequest.php:1207-1276` (bản đồ nguồn đã xác minh): thủ kho=`employee_create.info.fullname`, kho=`warehouse.name`, người nhận=`receiver.info.fullname`, NVKD=`employee_create_contract.fullname` (loại 1/2/8), HĐ link=`contract.link || firm_contract.link || wr_service_contract.link`, HĐ mua+NCC (loại 4) từ `product_import_request`, người yêu cầu/phòng ban từ `product_export_request.employee_create`.

- [ ] **Step 2: Viết helper enrich (luồng PXK — `WarehouseExport`)**

```php
/**
 * Bổ sung các field CHỈ HIỂN THỊ (read-only) vào object warehouse_export cho form tạo PXH.
 * Dựa bản đồ nguồn ERP getDataForEdit/getDataForProductExport. Giữ chuỗi/null, không expose id thừa.
 */
private function enrichWarehouseExportDisplay(array $we, \Modules\Assign\Entities\Warehouse\WarehouseExport $src): array
{
    $src->loadMissing(['warehouseExportRequest']);
    $we['is_export_direct']          = false;
    $we['stocker_name']              = optional(optional($src->employee_create)->info)->fullname;   // xác nhận relation ở BaseModel
    $we['receiver_name']             = optional(optional($src->receiver)->info)->fullname;
    $we['warehouse_name']            = $we['warehouse_name'] ?? optional($src->warehouse)->name;
    $we['accounting_date']           = $src->accounting_date;
    $we['branch_transfer_coefficient'] = $src->branch_transfer_coefficient;
    $we['account_debt']              = $src->account_debt;
    $we['account_has']               = $src->account_has;
    $we['cost_debt_id']              = $src->cost_debt_id;
    $we['work']                      = $src->work;
    $we['documents']                 = $src->attachments ? array_map('trim', explode(',', $src->attachments)) : [];
    // HĐ + NVKD + người yêu cầu/phòng ban + HĐ mua/NCC: điền theo nhánh loại (Step 3)
    return $this->fillContractDisplay($we, $src);
}
```
> Lưu ý: `WarehouseExport` là model mỏng (chỉ relation `warehouseExportRequest`). Các relation `employee_create`/`warehouse`/`receiver`/`customer` nếu CHƯA khai trên entity HRM thì phải join/truy vấn trực tiếp (không `mysql2`) — Step 1 xác định rõ cách lấy; dùng `optional()` để null-safe (PHP 7.4 không có `?->`).

- [ ] **Step 3: Viết `fillContractDisplay()` theo loại** — điền `contract_code`/`contract_link` (has_contract), `sale_employee_name` (NVKD), `emplement_contract_code`/`emplement_contract_link` (type 19), `supplier_code`/`supplier_name`+`contract_code` (type 4), `export_requester`/`export_request_department`, `join_export_request`. Nguồn gắn HĐ: `emplement_contract_id/_type` (polymorphic: type==3→`wrServiceContract`, ngược lại `firmContract`) hoặc `firm_contract_id` (relation `firmContract()`). Lấy `link` qua accessor `getLinkAttribute` của contract tương ứng.

- [ ] **Step 4: Luồng YCXH** — viết nhánh enrich từ `ProductExportRequest` (có relation `creator`, `emplementContract`, `firmContract`, `wrServiceContract`, cột snapshot customer). Set `is_export_direct=true`, `export_request_code=$per->code`, `stocker_name=null` (chưa có kho), gói MỌI field vào cùng object `warehouse_export` (id=null) để FE dùng chung binding.

- [ ] **Step 5: Gọi helper trong cả 2 endpoint** — `$warehouseExport = $this->enrichWarehouseExportDisplay($warehouseExport, $we);` (PXK) và nhánh YCXH tương ứng.

- [ ] **Step 6: Verify (tinker)** — build payload cho 1 PXK loại 1 (có HĐ+KH) và 1 YCXH, assert: `contract_link` không null khi `type ∈ has_contract`; `supplier_name` không null khi `type==4`; `accounting_date` có khi `type ∈ {9,10,18,19}`; `documents` là mảng.

- [ ] **Step 7: Verify (Playwright)** — mở create với 1 PXK loại 1: network response `warehouse_export` có `stocker_name`, `receiver_name`, `contract_link`, `customer_name`. Với YCXH: `is_export_direct=true`, `export_request_code` có giá trị.

- [ ] **Step 8: Checkpoint** — ghi STATUS, chờ review.

---

## Task 3: BE — trả `tabs` (Nhóm HĐ hãng, loại 14/15)

**Files:**
- Modify: `ProductExportController.php` — thêm private `buildFirmContractTabs(?int $firmContractId): array`, gọi trong cả 2 endpoint.

**Interfaces:**
- Consumes: `FirmContractExportStockService::remainingByContractProduct($firmContractId)` (:49, read-only reuse — trả map `[contract_product_id => ['needed','exported','in_flight','remaining']]`).
- Produces: key `tabs` = `[{ id:int, name:string, products:[{ product_id, code, product_name, unit_name, qty, remaining }] }]`; `[]` khi không có HĐ hãng. FE Task 11 `v-for` trên `form.tabs`.

- [ ] **Step 1: Xác nhận cột `firm_contract_tabs`** — Đọc ERP `app/Model/Sale/Firm/Contract/FirmContract.php` (relation `tabs`) + migration `firm_contract_tabs` / `firm_contract_tab_products` để lấy đúng tên cột `name`, khóa `firm_contract_id`, `parent_id` (= tab id), `contract_product_id` (= `firm_contract_tab_products.id`), `product_id`, `unit_id`, `qty`/`contract_qty`.

- [ ] **Step 2: Viết helper**

```php
/**
 * Dựng cấu trúc Nhóm (tab + products) từ HĐ hãng cho form PXH loại 14/15.
 * Tái dùng FirmContractExportStockService::remainingByContractProduct (KHÔNG sửa service).
 */
private function buildFirmContractTabs(?int $firmContractId): array
{
    if (!$firmContractId) return [];

    $remaining = app(\Modules\Assign\Services\FirmContractExportStockService::class)
        ->remainingByContractProduct((int) $firmContractId);   // map theo contract_product_id

    $tabs = \DB::table('firm_contract_tabs')
        ->where('firm_contract_id', $firmContractId)
        ->orderBy('id')
        ->get(['id', 'name']);

    $result = [];
    foreach ($tabs as $tab) {
        $rows = \DB::table('firm_contract_tab_products as p')
            ->leftJoin('products as pr', 'pr.id', '=', 'p.product_id')
            ->leftJoin('units as u', 'u.id', '=', 'p.unit_id')
            ->where('p.parent_id', $tab->id)
            ->get(['p.id as contract_product_id', 'p.product_id', 'p.qty',
                   'pr.code', 'pr.name as product_name', 'u.name as unit_name']);

        $result[] = [
            'id'       => (int) $tab->id,
            'name'     => $tab->name,
            'products' => $rows->map(function ($r) use ($remaining) {
                return [
                    'product_id'   => (int) $r->product_id,
                    'code'         => $r->code,
                    'product_name' => $r->product_name,
                    'unit_name'    => $r->unit_name,
                    'qty'          => (float) $r->qty,
                    'remaining'    => (float) ($remaining[$r->contract_product_id]['remaining'] ?? 0),
                ];
            })->values(),
        ];
    }
    return $result;
}
```
> Nếu tên cột thực tế khác (Step 1), chỉnh đúng tại query — không để tên phỏng đoán.

- [ ] **Step 3: Gọi trong 2 endpoint** — PXK: `$tabs = $this->buildFirmContractTabs($we->firm_contract_id ?? null);`. YCXH: `$per->firm_contract_id`. Thêm `'tabs' => $tabs` vào payload.

- [ ] **Step 4: Verify (tinker)** — chọn 1 phiếu nguồn loại 14 có HĐ hãng, assert `count($tabs) >= 1`, mỗi tab có `name` khác rỗng, `products` không rỗng, `remaining` là số. Phiếu loại ≠ 14/15 → `tabs == []`.

- [ ] **Step 5: Verify (Playwright)** — nguồn loại 14: network response có `tabs` với `name` + `products`. Nguồn loại 1: `tabs: []`.

- [ ] **Step 6: Checkpoint** — ghi STATUS, chờ review.

---

## Task 4: BE — trả danh mục cho field nhập tay (loại 9/10/18/19)

**Files:**
- Modify: `ProductExportController.php` — thêm private `formCatalogs(int $type): array`, gọi trong 2 endpoint.

**Interfaces:**
- Produces: key `catalogs` = `{ types:[{id,name}], accounts_s:[{id,name,identify_number,level}], cost_debts:[{id,code,name}], works:[{id,code,name}] }`. Chỉ cần đầy khi `type ∈ {9,10,18,19}`; loại khác trả `types` (cho select loại) + 3 mảng rỗng để nhẹ payload. FE Task 10 bind các select.

- [ ] **Step 1: Xác nhận API danh mục sẵn có** — `\Modules\Finance\Entities\Account\Account` (bảng `accounts`, cột `identify_number`, `name`, `level`, `status`), `\Modules\Finance\Entities\Work` (bảng `works`, `code`/`name`/`status`), `\Modules\Finance\Entities\CostDebt` (bảng `cost_debts`, `code`/`name`/`status`). STATUS hoạt động = 1.

- [ ] **Step 2: Viết helper**

```php
private function formCatalogs(int $type): array
{
    $types = collect(\Modules\Assign\Services\ProductExportService::exportTypesForSelect()) // nếu đã có; nếu chưa, build từ enum ExportModel
        ->map(fn ($name, $id) => ['id' => (int) $id, 'name' => $name])->values();

    $needAccounting = in_array($type, [9, 10, 18, 19], true);
    if (!$needAccounting) {
        return ['types' => $types, 'accounts_s' => [], 'cost_debts' => [], 'works' => []];
    }

    $accounts = \Modules\Finance\Entities\Account\Account::where('status', 1)
        ->orderBy('identify_number')
        ->get(['id', 'name', 'identify_number', 'level'])
        ->map(fn ($a) => [
            'id' => (int) $a->id,
            'name' => $a->identify_number . ' - ' . $a->name,
            'identify_number' => $a->identify_number,
            'level' => (int) $a->level,
        ]);

    return [
        'types'      => $types,
        'accounts_s' => $accounts,
        'cost_debts' => \Modules\Finance\Entities\CostDebt::where('status', 1)->orderBy('code')->get(['id', 'code', 'name']),
        'works'      => \Modules\Finance\Entities\Work::where('status', 1)->orderBy('code')->get(['id', 'code', 'name']),
    ];
}
```
> Nếu `ExportModel` enum chưa có helper select, build mảng `{id,name}` từ hằng loại (ERP `constant.js:171-205` là nguồn đối chiếu tên loại). KHÔNG hardcode rời rạc ở nhiều nơi — gom 1 chỗ.

- [ ] **Step 3: Gọi trong 2 endpoint** — `$catalogs = $this->formCatalogs((int) $warehouseExport['type']);` thêm `'catalogs' => $catalogs`.

- [ ] **Step 4: Verify (tinker)** — type 18 → `accounts_s`/`cost_debts`/`works` không rỗng, `accounts_s[0].name` dạng `"1111 - Tiền mặt"`; type 1 → 3 mảng rỗng, `types` vẫn đầy.

- [ ] **Step 5: Checkpoint** — ghi STATUS, chờ review.

---

## Task 5: BE — store nhận + ghi field nhập tay (KHÔNG nối hạch toán)

**Files:**
- Modify: `ProductExportController.php:526` (`storeProductExport`) + `:849` (`storeProductExportFromRequest`) — validation + payload.
- Modify: `Services/ProductExportService.php:134` (`createFromWarehouseExport`) + `:386` (`createFromProductExportRequest`) — map cột.

**Interfaces:**
- Consumes: payload FE thêm (Task 12): `account_debt`, `account_has`, `cost_debt_id`, `work`, `accounting_date`, `branch_transfer_coefficient`, `attachments[]` (file).
- Produces: `product_exports` lưu các cột tương ứng khi `type ∈ {9,10,18,19}` (và `branch_transfer_coefficient` khi `type==7`). KHÔNG gọi `postAccounting` cho các loại này.

- [ ] **Step 1: Thêm validation rule có điều kiện** — trong cả 2 store method, thêm (chỉ áp khi `type ∈ {9,10,18,19}`):

```php
// $type lấy từ nguồn ($we->type / $per->type)
if (in_array($type, [9, 10, 18, 19], true)) {
    $rules['account_debt']  = 'nullable|string|max:20';
    $rules['account_has']   = 'nullable|string|max:20';
    $rules['accounting_date'] = 'nullable|date';
    $rules['cost_debt_id']  = 'nullable|integer';
    $rules['work']          = 'nullable|string|max:50';
    // ERP: TK 642* bắt buộc mã phí; TK 154* bắt buộc vụ việc
    if (Str::startsWith((string) $request->input('account_debt'), '642')) $rules['cost_debt_id'] = 'required|integer';
    if (Str::startsWith((string) $request->input('account_debt'), '154')) $rules['work'] = 'required|string|max:50';
}
if ($type === 7) $rules['branch_transfer_coefficient'] = 'nullable|numeric';
```
Trả lỗi validate dạng 422 (không 500).

- [ ] **Step 2: Thêm key vào `$request->only([...])`** — bổ sung `account_debt, account_has, accounting_date, cost_debt_id, work, branch_transfer_coefficient` vào mảng truyền sang service.

- [ ] **Step 3: Map cột trong service** — trong `createFromWarehouseExport` (:146-171) và `createFromProductExportRequest` (:392-423), set vào ProductExport khi key tồn tại trong `$data`:

```php
foreach (['account_debt', 'account_has', 'cost_debt_id', 'work', 'accounting_date', 'branch_transfer_coefficient'] as $col) {
    if (array_key_exists($col, $data) && $data[$col] !== null && $data[$col] !== '') {
        $pxh->{$col} = $data[$col];
    }
}
```
> Bảng `product_exports` dùng chung = bảng ERP, các cột này tồn tại vật lý. KHÔNG thêm gọi `postAccounting` cho 9/10/18/19.

- [ ] **Step 4: Verify (tinker, transaction + rollBack)** — tạo nháp (status=3) 1 phiếu type 18 với `account_debt='6421'`, `account_has='1111'`, `cost_debt_id=<id>`, `accounting_date='2026-10-09'`: assert 4 cột lưu đúng trên `product_exports`; `postAccounting` KHÔNG sinh dòng kế toán (đếm `product_export_detail_accounting` = như trước). Test thiếu `cost_debt_id` khi `account_debt='6421'` → validate 422.

- [ ] **Step 5: Checkpoint** — ghi STATUS, chờ review.

---

## Task 5b: BE — upload `attachments` + trả `documents` (ERP-compatible)

**Files:**
- Modify: `ProductExportController.php` (2 store method) + `ProductExportService.php` (2 create method).

**Interfaces:**
- Produces: file upload → lưu chuỗi url nối `', '` vào cột `product_exports.attachments`; read endpoint trả `documents` = `explode(', ')` (Task 2 đã làm phần đọc).

- [ ] **Step 1: Xác định uploader HRM sẵn có** — Đọc cách HRM upload file (YCXH `ProductExportRequest::files()` + controller store của YCXH, hoặc helper S3 dùng chung trong `hrm-api`). Khớp với pattern ERP `ProductExportsController.php:662-679` (`CmcS3Helper::putFile($file,'warehouse_exports')` → `join(', ')` lưu cột `attachments`).

- [ ] **Step 2: Nhận file + lưu cột** — trong store (khi `type ∈ {9,10,18,19}` và `$request->hasFile('attachments')`): đẩy từng file qua uploader đã xác định (Step 1), nối url `', '`, lưu `$pxh->attachments`. Giữ đường dẫn đầy đủ (không cắt tên).

- [ ] **Step 3: Verify (tinker/Playwright)** — upload 1 file ở form type 18 → `product_exports.attachments` chứa url; mở lại form → `documents` trả mảng 1 phần tử. (Dùng Playwright `browser_file_upload`.)

- [ ] **Step 4: Checkpoint** — ghi STATUS, chờ review.

---

## Task 6: FE — state + computed cờ + fetchData wiring

**Files:**
- Modify: `hrm-client/pages/finance/product-exports/create.vue` (`data()`, `fetchData()` :610, `computed`)

**Interfaces:**
- Consumes: payload BE (`warehouse_export.type`, `tabs`, `catalogs`, các field RO/EDIT).
- Produces: state `form.type`, `form.tabs`, `catalogs`, field EDIT; computed `hasCustomer`/`isSale`/`showAllocatedPrice`/`hasContract`/`hasDelivery`. Task 7–12 dùng.

- [ ] **Step 1: Đọc cấu trúc hiện có** — Đọc `create.vue` quanh `data()`, `fetchData()` (:610), `submit()` (:964), source picker (:26/:31) để biết tên biến hiện (`info`, `rows`, `arrange`, `executors`, `note`, `sourceType`, `sourceId`).

- [ ] **Step 2: Thêm state**

```js
data() {
  return {
    // ...state hiện có...
    form: { type: null, tabs: [] },
    catalogs: { types: [], accounts_s: [], cost_debts: [], works: [] },
    editFields: {
      account_debt: null, account_has: null, cost_debt_id: null,
      work: null, accounting_date: null, branch_transfer_coefficient: null,
      documents: [], attachments: [],
    },
  }
}
```

- [ ] **Step 3: Thêm computed cờ (verbatim)**

```js
computed: {
  exportType() { return Number(this.form.type) || null },
  hasCustomer() { return [1,2,8,12,14,16,17].includes(this.exportType) },
  isSale() { return [1,11,13,14,16,17].includes(this.exportType) },
  showAllocatedPrice() { return [1,4,11,13,14,16,17].includes(this.exportType) },
  hasContract() { return [1,2,8,11,13,14,16,17].includes(this.exportType) },
  hasDelivery() { return Number(this.info?.transition_type) === 2 },
}
```

- [ ] **Step 4: Nạp trong `fetchData()`** — sau khi nhận `data`: `this.form.type = data.warehouse_export.type`; `this.form.tabs = data.tabs || []`; `this.catalogs = data.catalogs || {...}`; `this.editFields = { account_debt: data.warehouse_export.account_debt, ... , documents: data.warehouse_export.documents || [], attachments: [] }`. Giữ `this.info = data.warehouse_export`.

- [ ] **Step 5: Verify (Playwright)** — mở create PXK loại 1: Vue devtools / `browser_evaluate` xác nhận `hasCustomer=true`, `hasContract=true`, `showAllocatedPrice=true`; loại 7: `hasContract=false`.

- [ ] **Step 6: Checkpoint** — ghi STATUS, chờ review.

---

## Task 7: FE — bố cục tab bọc các khối hiện có

**Files:**
- Modify: `create.vue` (template)

**Interfaces:**
- Consumes: `hasDelivery` (Task 6).
- Produces: 3 tab "Thông tin chung" / "Vận chuyển" (`v-if="hasDelivery"`) / "Bốc xếp"; card chi tiết "Hàng hóa" + chỗ cho tab Nhóm.

- [ ] **Step 1: Thêm khung tab** — dùng component tab của hệ (xác nhận tên tab component đang dùng ở detail page `_id/index.vue` để đồng bộ). Bọc: khối Thông tin chung (sẽ dựng Task 8–10) vào tab 1; khối Vận chuyển vào tab 2 (`v-if="hasDelivery"`); khối Bốc xếp hiện có vào tab 3 **giữ nguyên nội dung**.

- [ ] **Step 2: Giữ nguyên bảng Hàng hóa** — đặt trong card chi tiết, không đổi logic.

- [ ] **Step 3: Verify (Playwright)** — mở create: thấy 3 tab; nguồn `transition_type!=2` → tab "Vận chuyển" ẩn; chuyển tab không mất dữ liệu bảng Hàng hóa.

- [ ] **Step 4: Checkpoint** — ghi STATUS, chờ review.

---

## Task 8: FE — khối "Thông tin chung" 27 field read-only ẩn/hiện

**Files:**
- Modify: `create.vue` (tab Thông tin chung)

**Interfaces:**
- Consumes: `info.*` (các key RO Task 2), cờ Task 6.
- Produces: render điều kiện đúng bảng field spec §3.2.

- [ ] **Step 1: Dựng field RO theo điều kiện** — mỗi field dùng `V2Base*` ở chế độ hiển thị (disabled / read-only):
  - Luôn: Loại xuất (RO, select disabled từ `catalogs.types` theo `form.type`), Xuất thẳng (checkbox disabled `info.is_export_direct`), Người yêu cầu (`info.export_requester`), Phòng ban (`info.export_request_department`).
  - `v-if="!info.is_export_direct"`: Chọn phiếu xuất kho (`info.code`), Thủ kho (`info.stocker_name`), Kho (`info.warehouse_name`), Người nhận (`info.receiver_name`).
  - `v-if="info.is_export_direct"`: Chọn YCXH (`info.export_request_code`).
  - `v-if="exportType===19"`: Hợp đồng emplement (`info.emplement_contract_code` + link `info.emplement_contract_link`).
  - `v-if="exportType===4"`: Hợp đồng mua (`info.contract_code`), NCC (`info.supplier_code` - `info.supplier_name`).
  - `v-if="hasContract"`: HĐ link (`info.contract_link`), NVKD (`info.sale_employee_name`), Tỷ giá (hardcode "1" + "VND").
  - `v-if="hasCustomer"`: Khách hàng (`info.customer_name`) + khối giao hàng (địa chỉ/liên hệ sẵn có).
  - `v-if="['18','19','9','10'].includes(String(exportType))"`: Ngày hạch toán (`info.accounting_date`, RO ở đây — nhập tay nằm ở Task 10 nếu ERP cho sửa; theo spec #5 RO).
  - Phiếu xuất ghép: `v-if="info.is_export_direct && info.join_export_request"` link `join_export_request.code`.
  - Ghi chú (`V2BaseTextarea`, editable) — giữ.

- [ ] **Step 2: Màu/chữ** — nhãn field theo ERP; không dùng `.text-muted` (đỏ) cho chữ phụ → `#6b7280`.

- [ ] **Step 3: Verify (Playwright)** — loại 1: hiện KH + HĐ link + NVKD + Tỷ giá, KHÔNG hiện HĐ mua/NCC. loại 4: hiện HĐ mua + NCC, KHÔNG hiện KH. loại 7: ẩn hết khối HĐ/KH. YCXH: hiện "Chọn YCXH", ẩn Thủ kho/Kho.

- [ ] **Step 4: Checkpoint** — ghi STATUS, chờ review.

---

## Task 9: FE — khối tài khoản read-only hardcode (loại 1–4)

**Files:**
- Create: `hrm-client/components/assign/product-export/ProductExportAccountBlock.vue`
- Modify: `create.vue` (nhúng sau khối Thông tin chung)

**Interfaces:**
- Consumes: prop `type` (Number).
- Produces: bảng số hiệu TK hardcode chỉ hiện `type ∈ {1,2,3,4}`.

- [ ] **Step 1: Viết component** — map hardcode:

```js
const ACCOUNT_MAP = {
  1: [['Nợ','1311'],['Doanh thu','5111'],['Kho','1561'],['Thuế','33311'],['Giá vốn','632'],['Chiết khấu','5211'],['Giảm giá','5213']],
  2: [['Giá vốn','632'],['Kho','1561']],
  3: [['Nợ','157'],['Kho','1561']],
  4: [['Nợ','3311'],['Kho','1561'],['Kho','1331']],
}
```
Render `v-if="ACCOUNT_MAP[type]"` thành bảng nhãn–số hiệu, read-only, chữ phụ `#6b7280`.

- [ ] **Step 2: Nhúng** — `<ProductExportAccountBlock :type="exportType" />` sau khối Thông tin chung (sau `<hr>` như ERP).

- [ ] **Step 3: Verify (Playwright)** — loại 1: hiện 7 dòng TK đúng số hiệu; loại 3: 2 dòng (157, 1561); loại 7/14/18: khối ẩn.

- [ ] **Step 4: Checkpoint** — ghi STATUS, chờ review.

---

## Task 10: FE — field nhập tay tài khoản (loại 9/10/18/19)

**Files:**
- Modify: `create.vue` (tab Thông tin chung, nhánh `type ∈ {9,10,18,19}`)

**Interfaces:**
- Consumes: `catalogs.accounts_s/cost_debts/works`, `editFields`.
- Produces: select TK nợ/có + mã phí + vụ việc + ngày hạch toán + hệ số điều chuyển + upload file, bind `editFields.*`, validate inline.

- [ ] **Step 1: Dựng select + input** (dùng `V2BaseSelect`/`V2BaseDatePicker`/`V2BaseInput`):
  - `v-if="['18','19'].includes(String(exportType))"`: TK nợ (`editFields.account_debt`, options `catalogs.accounts_s` theo `identify_number`).
  - `v-if="exportType===18"`: TK có (`editFields.account_has`).
  - `v-if="['9','10'].includes(String(exportType))"`: TK nợ (`editFields.account_debt`).
  - `v-if="['18','19'].includes(String(exportType))"`: Mã phí (`editFields.cost_debt_id`, options `catalogs.cost_debts`).
  - `v-if="['18','19','9','10'].includes(String(exportType))"`: Vụ việc (`editFields.work`, options `catalogs.works`), Ngày hạch toán (`editFields.accounting_date`).
  - `v-if="exportType===7"`: Hệ số điều chuyển (`editFields.branch_transfer_coefficient`, số en-US).
  - `v-if="['18','19'].includes(String(exportType))"`: File đính kèm (upload `editFields.attachments`, hiện `editFields.documents` làm link tải).

- [ ] **Step 2: Validate inline (ERP rule)** — `account_debt` bắt đầu `642` → mã phí bắt buộc; bắt đầu `154` → vụ việc bắt buộc. Hiển thị lỗi ĐỎ dưới field (đỏ chỉ cho lỗi validate).

- [ ] **Step 3: Verify (Playwright)** — loại 18: hiện TK nợ/có + mã phí + vụ việc + upload; chọn TK `642x` bỏ trống mã phí → lỗi đỏ, chặn submit. loại 1: không field nhập tay nào.

- [ ] **Step 4: Checkpoint** — ghi STATUS, chờ review.

---

## Task 11: FE — tab Nhóm + cột phân bổ giá theo showAllocatedPrice

**Files:**
- Create: `hrm-client/components/assign/product-export/ProductExportGroupTabs.vue`
- Modify: `create.vue` (card chi tiết)

**Interfaces:**
- Consumes: `form.tabs` (Task 3), `showAllocatedPrice` (Task 6).
- Produces: tab "Nhóm" read-only + cột "ĐG/TT sau giảm/phân bổ" hiện theo `showAllocatedPrice`.

- [ ] **Step 1: Viết `ProductExportGroupTabs`** — prop `tabs`; `v-for` mỗi tab 1 bảng read-only (Mã hàng / Tên / ĐVT / SL HĐ / Còn lại). Số en-US.

- [ ] **Step 2: Nhúng** — `<ProductExportGroupTabs v-if="form.tabs.length" :tabs="form.tabs" />` trong card chi tiết, cạnh tab "Hàng hóa". **Điều kiện là `form.tabs.length`, KHÔNG gắn `hasContract`** (để loại 15 Cách A vẫn hiện Nhóm).

- [ ] **Step 3: Cột phân bổ giá** — ở bảng Hàng hóa, các cột "ĐG sau giảm / TT sau giảm / phân bổ" `v-if="showAllocatedPrice"`.

- [ ] **Step 4: Verify (Playwright)** — loại 14 có HĐ hãng: hiện tab Nhóm với tên + hàng; cột phân bổ hiện. loại 15 có `tabs`: hiện tab Nhóm NHƯNG ẩn KH/HĐ/TK read-only (Cách A). loại 2: ẩn tab Nhóm, ẩn cột phân bổ.

- [ ] **Step 5: Checkpoint** — ghi STATUS, chờ review.

---

## Task 12: FE — nút "Đổi phiếu" (re-pick) + submit payload

**Files:**
- Modify: `create.vue` (thanh nguồn + `submit()` :964)

**Interfaces:**
- Consumes: modal `WarehouseExportSearchModal` / `ProductExportRequestSearchModal` (đã có).
- Produces: nút "Đổi phiếu" reset + mở picker; submit kèm field nhập tay.

- [ ] **Step 1: Nút "Đổi phiếu"** — ở thanh nguồn tab Thông tin chung: `V2BaseButton secondary size="sm"` icon `ri-refresh-line`, `@click="repick"`. `repick()` set `sourcePickerMode=true` và mở lại modal theo nguồn hiện tại.

- [ ] **Step 2: `resetSourceState()`** — khi chọn nguồn mới (`onChooseWarehouseExport`/`onChooseProductExportRequest`): reset `form.type=null`, `form.tabs=[]`, `editFields` về mặc định, `rows=[]`, `arrange`/`executors` giữ theo logic hiện có, rồi gọi `fetchData()`.

- [ ] **Step 3: Submit payload** — mở rộng `submit(status)` (:964): khi `exportType ∈ {9,10,18,19}` thêm `account_debt, account_has, cost_debt_id, work, accounting_date` vào payload; `exportType===7` thêm `branch_transfer_coefficient`; nếu có file dùng `FormData` append `attachments[]`. Giữ nguyên `{status, note, products, arrange_delivery, executors}`. Nút có `$safeLoadingStart/Finish` + `:interactable="!submitting"`. Sau lưu → về `/finance/product-exports`.

- [ ] **Step 4: Verify (Playwright)** — chọn PXK loại 1 → "Đổi phiếu" → chọn YCXH loại khác: `form.type`/`tabs`/`editFields` reset, không rò field cũ. Submit nháp loại 18 (trên phiếu test, transaction nếu có) → payload có field nhập tay; submit thiếu mã phí khi TK 642 → bị chặn.

- [ ] **Step 5: Checkpoint** — ghi STATUS, chờ review.

---

## Self-Review (đã chạy khi viết plan)

1. **Spec coverage**: §3.1→T1; §3.2 (27 field)→T2+T8; §3.2b (danh mục + nhập tay + upload)→T4+T5+T5b+T10; §3.3 (tabs)→T3+T11; §3.4 (TK hardcode)→T9; §4.1 state→T6; §4.2 computed→T6; §4.3 tab→T7; §4.4 re-pick→T12; §4.5 loại 15→T11 (điều kiện `tabs.length`); §4.6 submit→T12; §4.7 UI→Global Constraints. ✅ đủ.
2. **Placeholder scan**: không "TBD/TODO"; các điểm cần xác nhận cột DB đều là bước "đọc file X dòng Y" cụ thể (T2.1, T3.1, T4.1, T5b.1), không phải placeholder.
3. **Type consistency**: `enrichWarehouseExportDisplay`/`buildFirmContractTabs`/`formCatalogs` (BE), `exportType`/`hasCustomer`/`showAllocatedPrice` (FE), `editFields.*` (keys cố định) nhất quán across tasks.
4. **Review Focus**: 5 input class đã gắn test ở T12 (đổi nguồn), T11 (loại 15 + tên tab), T3 (tab name), T5+T10 (validate 642/154), T1 (type cả 2 nguồn).

## Execution Handoff

Plan lưu tại `HRM/.plans/gop-db/product-export-features/plan-form-rebuild.md`. Phase 1–3 (đã xong) ở `plan.md` cùng thư mục — không đụng.
