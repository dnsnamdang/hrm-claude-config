# YCXH loại 14 — "Chọn nhóm hàng hóa" (tab theo nhóm) + field Thông tin chung — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Trên màn Tạo/Sửa YCXH loại 14 (Xuất bán hàng, nguồn HĐ hãng), port đầy đủ như ERP: thêm **Nhóm VAT** (dropdown required), **Chọn nhóm hàng hóa** (multi-select required → mỗi nhóm = 1 tab chi tiết, lưu N bản ghi `product_export_request_tabs`), **Tên viết tắt** + **Địa chỉ giao hàng** (hiển thị).

**Architecture:** BE (`Modules/Assign`) trả thêm `customer_unit`/`delivery_place`/`tabs[]`/`selected_tab_ids`/`firm_tab_vat_percent`, thêm rule `firm_tab_ids`, và refactor service để lặp **N tab** theo nhóm (1 tab/`firm_contract_tab_id`) thay vì 1 tab cứng. FE (`ProductExportRequestForm.vue`) thêm 2 dòng hiển thị, 2 selector V2Base (Nhóm VAT + Chọn nhóm hàng hóa), đổi bảng phẳng → **b-tabs theo nhóm**, submit gom mọi nhóm + gửi `firm_tab_ids`. Không migration — mọi bảng/cột đã có trong DB gộp.

**Tech Stack:** hrm-api = PHP 7.4 / Laravel 8 (`Modules/Assign`, PHPUnit feature test chạy trên DB dev `erp_new`/`hrm_erp_test`, dùng `DatabaseTransactions` + HĐ hãng thật id `24930`). hrm-client = Nuxt 2.14 / Vue 2 / Bootstrap-Vue 2.15 (`b-tabs`, `V2BaseSelect`, Select2). Nhánh `develop` (con của `gop_db`) cả 2 repo.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-13-ycxh-type14-nhom-hang-hoa-design.md` (tóm tắt: `HRM/.plans/gop-db/ycxh-type14-nhom-hang-hoa/design.md`).

## Global Constraints

- **KHÔNG migration mới, KHÔNG `mysql2`/`DB_CONNECTION_SECOND`.** Bảng `product_export_request_tabs` (có cột `firm_contract_tab_id`), `product_export_request_tab_products` (có `firm_contract_tab_id` + `firm_contract_tab_product_id`), `product_export_request_details`, và cột `product_export_requests.firm_tab_vat_percent` đều đã tồn tại. Ưu tiên bản bảng ERP.
- **Nguồn đọc (bảng ERP, read-only từ HRM):** `firm_contracts`, `firm_quotations` (join qua `firm_contracts.firm_quotation_id`), `firm_contract_tabs`, `firm_contract_tab_products`. Trên `firm_contract_tab_products`, cột `parent_id` = `firm_contract_tabs.id` (= id nhóm).
- **Nguồn field hiển thị (đã xác minh 2026-10-13):** `delivery_place` KHÔNG nằm trên `firm_contracts` — là accessor ERP đọc `firm_quotation->delivery_place`. `gara_name` cũng nằm trên `firm_quotations`, KHÔNG trên `firm_contracts`. `customer_short_name` KHÔNG tồn tại cho HĐ hãng (không có ở `firm_contracts`/`firm_quotations`/`customers`). → `customer_unit` port getter ERP `customer_type == 1 ? gara_name : (customer_short_name ?: customer_name)` với `customer_type`+`customer_name` từ `firm_contracts`, `gara_name` từ `firm_quotations`, `customer_short_name` = '' (luôn fallback `customer_name` khi type≠1). Thiếu cột/row → trả `''` (FE hiện ô trống, KHÔNG `—`).
- **Một phiếu một VAT:** `firm_tab_vat_percent` là 1 cột trên header phiếu (1 dropdown/phiếu). Persist nó khi create + update (model `$guarded = []` → mass-assignable).
- **Validate:** FE realtime vee-validate + báo đỏ inline; BE rethrow `ValidationException` → 422. "Lưu nháp" (status 3) chỉ nới `required`. KHÔNG khai `messages()` cho rule phổ biến (lang `vi` có sẵn).
- **Số:** quốc tế `1,234,567.89` (FE `toLocaleString('en-US')`); ngày giữ `dd/mm/yyyy`.
- **UI:** element form MỚI dùng `V2Base*` (Nhóm VAT/Chọn nhóm hàng hóa). Các ô TRONG BẢNG chi tiết (checkbox/number) giữ nguyên markup thô hiện có của màn này — port pattern sẵn có, không đổi. Ô hiển thị readonly dùng pattern `ro-panel`/`ro-value` sẵn có trên màn (không "—", ô rỗng gắn class `ro-empty`). nav-tabs dùng `<b-tabs nav-class="nav-tabs nav-bordered">` + `<b-tab>` — copy pattern từ `pages/finance/product-imports/components/ProductImportForm.vue:170-172`.
- **Cờ quyền fail-closed** (không hard-code `=true`) — plan này không thêm cờ quyền mới. Sau save thành công → `markFormSaved()` + `$router.push` về danh sách (giữ nguyên hành vi hiện có).
- **Git:** không commit/push khi chưa được yêu cầu.

## Review Focus

- **Đổi Nhóm VAT sau khi đã chọn nhóm:** phải reset `selectedTabIds` + bỏ tick/SL các dòng → tránh "gửi âm thầm" dòng VAT cũ (lặp lại finding MEDIUM#3 đợt trước). Test ở Task 7 (FE Playwright) + đảm bảo `buildProducts` chỉ gom dòng thuộc VAT hiện hành.
- **Nhóm được chọn nhưng không tick dòng nào trong nhóm đó:** vẫn tạo 1 tab (rỗng) cho nhóm (parity ERP); `selected_tab_ids` phải đọc từ bảng `product_export_request_tabs` (KHÔNG từ `tab_products`) để lúc Sửa lại không mất nhóm rỗng. Test ở Task 4 (BE) + Task 2 (BE).
- **HĐ chỉ 1 mức VAT:** Nhóm VAT vẫn hiện (1 option, auto chọn), danh sách nhóm vẫn populate. Test ở Task 6 (FE).
- **Phiếu nháp cũ (tạo trước khi ghi `firm_contract_tab_id`/chưa gửi `firm_tab_ids`):** BE fallback suy nhóm từ `parent_id` dòng đã chọn; FE fallback suy `selectedTabIds` từ `parent_id` của `selected_lines` khi `selected_tab_ids` rỗng. Test ở Task 4 (BE) + Task 8 (FE).
- **Sửa phiếu gửi duyệt:** kiểm "còn được xuất" phải loại trừ chính phiếu (`excludeRequestId`) xuyên qua đường N-tab mới. Test ở Task 4 (BE).

---

## File Structure

**hrm-api** (`/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api`):
- `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` — `createData()`/`editData()` nhánh 14: thêm `customer_unit`, `delivery_place`, `tabs[]`, (edit) `selected_tab_ids`, (edit) `firm_tab_vat_percent`; thêm private helper `firmContractDisplaySnapshot()` + `firmContractTabs()`; `rulesForType()` thêm `firm_tab_ids`.
- `Modules/Assign/Services/ProductExportRequestService.php` — tách `writeFirmContractTabs()` (lặp N tab) + `writeFirmContractTabLines()` (ghi dòng 1 tab); `createFromFirmContract()` + `updateFromRequest()` gọi wrapper; persist `firm_tab_vat_percent`.
- `tests/Feature/ProductExportRequest/FirmContractTabsTest.php` — **MỚI**: test createData/editData shape + N-tab service + fallback + exclude-self.

**hrm-client** (`/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client`):
- `pages/finance/product-export-requests/components/ProductExportRequestForm.vue` — toàn bộ thay đổi FE (panel 2 field, 2 selector, b-tabs chi tiết, buildProducts/paymentSummary/validateForm/load).

**ERP** (đối chiếu, read-only — KHÔNG sửa): `resources/views/warehouse/product_export_requests/form.blade.php`, `resources/views/partials/classes/warehouse/ProductExportRequest.blade.php:240-242`.

---

## Task 1: BE — helper snapshot `customer_unit` + `delivery_place`

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (thêm 2 private method sau `firmContractProductLines()`, ~sau dòng 496)
- Test: `tests/Feature/ProductExportRequest/FirmContractTabsTest.php` (tạo mới)

**Interfaces:**
- Produces:
  - `private function firmContractDisplaySnapshot(int $firmContractId): array` → `['customer_unit' => string, 'delivery_place' => string]`.
  - `private function firmContractTabs(int $firmContractId): \Illuminate\Support\Collection` → collection các `['id' => int, 'name' => string]` (chỉ nhóm có ≥1 dòng `firm_contract_tab_products`).
- Consumes: không có (đọc DB trực tiếp).

- [ ] **Step 1: Viết test thất bại** — tạo file test với case createData trả 2 field hiển thị.

```php
<?php

namespace Tests\Feature\ProductExportRequest;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class FirmContractTabsTest extends TestCase
{
    use DatabaseTransactions, ProductExportRequestFixture;

    /** HĐ hãng thật trong DB dev (giống ContractSubmitTest). */
    private const FIRM_ID = 24930;

    protected function setUp(): void
    {
        parent::setUp();
        $this->loginAs13();
    }

    private function requireFirm(): object
    {
        $firm = DB::table('firm_contracts')->where('id', self::FIRM_ID)->first();
        if (!$firm) {
            $this->markTestSkipped('Không có HĐ hãng ' . self::FIRM_ID . ' trong DB dev.');
        }
        DB::table('firm_contracts')->where('id', self::FIRM_ID)->update(['status' => 3, 'created_by' => 13]);
        return DB::table('firm_contracts')->where('id', self::FIRM_ID)->first();
    }

    public function test_create_data_tra_customer_unit_va_delivery_place(): void
    {
        $this->requireFirm();
        $res = $this->getJson('/api/v1/assign/product-export-requests/create-data?type=14&firm_contract_id=' . self::FIRM_ID);
        $res->assertStatus(200);
        $contract = $res->json('data.contract');
        $this->assertArrayHasKey('customer_unit', $contract);
        $this->assertArrayHasKey('delivery_place', $contract);
        // customer_unit không bao giờ null (fallback '' hoặc customer_name).
        $this->assertNotNull($contract['customer_unit']);
    }
}
```

- [ ] **Step 2: Chạy test, xác nhận FAIL**

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_create_data_tra_customer_unit_va_delivery_place`
Expected: FAIL — `assertArrayHasKey('customer_unit')` vì createData chưa trả field.

- [ ] **Step 3: Thêm 2 helper** vào controller (sau `firmContractProductLines()`):

```php
    /**
     * Snapshot hiển thị bổ sung cho loại 14 (port ERP):
     *  - delivery_place: accessor ERP đọc firm_quotation->delivery_place (KHÔNG có cột trên firm_contracts).
     *  - customer_unit : getter ERP customer_type==1 ? gara_name : (customer_short_name ?: customer_name).
     *    gara_name nằm trên firm_quotations; customer_short_name không tồn tại cho HĐ hãng → '' → type≠1
     *    luôn fallback customer_name. Thiếu row/cột → ''.
     */
    private function firmContractDisplaySnapshot(int $firmContractId): array
    {
        $fc = DB::table('firm_contracts')
            ->leftJoin('firm_quotations', 'firm_quotations.id', '=', 'firm_contracts.firm_quotation_id')
            ->where('firm_contracts.id', $firmContractId)
            ->first([
                'firm_contracts.customer_type',
                'firm_contracts.customer_name',
                'firm_quotations.gara_name as fq_gara_name',
                'firm_quotations.delivery_place as fq_delivery_place',
            ]);

        if (!$fc) {
            return ['customer_unit' => '', 'delivery_place' => ''];
        }

        $garaName = (string) ($fc->fq_gara_name ?? '');
        $customerShortName = ''; // không có nguồn cho HĐ hãng
        $customerName = (string) ($fc->customer_name ?? '');
        $customerUnit = ((int) $fc->customer_type === 1)
            ? $garaName
            : ($customerShortName !== '' ? $customerShortName : $customerName);

        return [
            'customer_unit' => $customerUnit,
            'delivery_place' => (string) ($fc->fq_delivery_place ?? ''),
        ];
    }

    /**
     * Danh sách nhóm hàng hóa (firm_contract_tabs) có ≥1 dòng sản phẩm — mỗi nhóm = 1 tab chi tiết.
     */
    private function firmContractTabs(int $firmContractId)
    {
        return DB::table('firm_contract_tabs')
            ->where('firm_contract_tabs.firm_contract_id', $firmContractId)
            ->whereExists(function ($q) {
                $q->select(DB::raw(1))
                    ->from('firm_contract_tab_products as fctp')
                    ->whereColumn('fctp.parent_id', 'firm_contract_tabs.id');
            })
            ->orderBy('firm_contract_tabs.id')
            ->get(['firm_contract_tabs.id', 'firm_contract_tabs.name'])
            ->map(function ($t) {
                return ['id' => (int) $t->id, 'name' => (string) $t->name];
            })
            ->values();
    }
```

- [ ] **Step 4: Nối helper vào createData** — trong nhánh `XUAT_BAN_HD_HANG` (sau khi dựng `$payload['contract']`, ~sau dòng 397), merge 2 field + thêm tabs:

```php
                    $snapshot = $this->firmContractDisplaySnapshot($firmContractId);
                    $payload['contract']['customer_unit'] = $snapshot['customer_unit'];
                    $payload['contract']['delivery_place'] = $snapshot['delivery_place'];
                    $payload['tabs'] = $this->firmContractTabs($firmContractId);
```

- [ ] **Step 5: Chạy test, xác nhận PASS**

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_create_data_tra_customer_unit_va_delivery_place`
Expected: PASS (hoặc SKIP nếu DB dev không có HĐ 24930 — chạy lại khi có).

- [ ] **Step 6: `php -l`** file controller sạch.

Run: `php -l Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php`

---

## Task 2: BE — editData nhánh 14 trả `customer_unit`, `delivery_place`, `tabs[]`, `selected_tab_ids`, `firm_tab_vat_percent`

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (nhánh `elseif ((int) $req->type === ProductExportRequest::XUAT_BAN_HD_HANG)` trong `editData()`, ~1182-1210)
- Test: `tests/Feature/ProductExportRequest/FirmContractTabsTest.php`

**Interfaces:**
- Consumes: `firmContractDisplaySnapshot()`, `firmContractTabs()` (Task 1).
- Produces: `editData` nhánh 14 trả thêm keys: `contract`-less (màn Sửa đọc trực tiếp từ `$detail`) → thêm vào `$detail`: `customer_unit`, `delivery_place`, `tabs`, `selected_tab_ids` (array int), `firm_tab_vat_percent` (float|null).

> **selected_tab_ids đọc từ bảng `product_export_request_tabs`** (không từ tab_products) để không mất nhóm rỗng (xem Review Focus). Fallback: nếu rỗng → distinct `parent_id` của tab_products của phiếu (phiếu cũ chưa ghi `firm_contract_tab_id` trên bảng tabs).

- [ ] **Step 1: Thêm test editData** vào file test:

```php
    public function test_edit_data_tra_tabs_va_selected_tab_ids(): void
    {
        $firm = $this->requireFirm();
        // Tạo phiếu nháp N-tab qua service rồi đọc lại editData.
        $lines = DB::table('firm_contract_tab_products')
            ->where('firm_contract_id', self::FIRM_ID)->orderBy('id')->get(['id', 'parent_id']);
        if ($lines->isEmpty()) {
            $this->markTestSkipped('HĐ hãng không có dòng.');
        }
        $first = $lines->first();
        $req = app(\Modules\Assign\Services\ProductExportRequestService::class)->createFromFirmContract([
            'status' => 3,
            'firm_contract_id' => self::FIRM_ID,
            'firm_tab_vat_percent' => (float) DB::table('firm_contract_tab_products')->where('id', $first->id)->value('vat_percent'),
            'firm_tab_ids' => [(int) $first->parent_id],
            'products' => [['contract_product_id' => (int) $first->id, 'qty' => 1]],
        ]);

        $res = $this->getJson('/api/v1/assign/product-export-requests/' . $req->id . '/edit-data');
        $res->assertStatus(200);
        $d = $res->json('data');
        $this->assertArrayHasKey('tabs', $d);
        $this->assertArrayHasKey('selected_tab_ids', $d);
        $this->assertContains((int) $first->parent_id, array_map('intval', $d['selected_tab_ids']));
        $this->assertArrayHasKey('customer_unit', $d);
        $this->assertArrayHasKey('delivery_place', $d);
    }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL**

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_edit_data_tra_tabs_va_selected_tab_ids`
Expected: FAIL — thiếu `tabs`/`selected_tab_ids` (và/hoặc `createFromFirmContract` chưa nhận `firm_tab_ids`; Task 4 sẽ hoàn thiện service — nếu service chưa persist N-tab, test này vẫn fail ở assertContains → để nguyên, PASS sau Task 4).

- [ ] **Step 3: Bổ sung vào nhánh 14 của `editData`** (cuối khối, sau `vat_options`):

```php
                // Field hiển thị bổ sung (Tên viết tắt + Địa chỉ giao hàng) — port ERP.
                $snapshot = $this->firmContractDisplaySnapshot((int) $req->firm_contract_id);
                $detail['customer_unit'] = $snapshot['customer_unit'];
                $detail['delivery_place'] = $snapshot['delivery_place'];
                // Danh sách nhóm hàng hóa của HĐ + VAT đã lưu trên phiếu.
                $detail['tabs'] = $this->firmContractTabs((int) $req->firm_contract_id);
                $detail['firm_tab_vat_percent'] = $req->firm_tab_vat_percent !== null
                    ? (float) $req->firm_tab_vat_percent
                    : null;
                // Nhóm đã chọn: ưu tiên bảng tabs (giữ được nhóm rỗng), fallback tab_products cho phiếu cũ.
                $selectedTabIds = DB::table('product_export_request_tabs')
                    ->where('parent_id', $req->id)
                    ->whereNotNull('firm_contract_tab_id')
                    ->distinct()
                    ->pluck('firm_contract_tab_id')
                    ->map(function ($v) {
                        return (int) $v;
                    })->values();
                if ($selectedTabIds->isEmpty()) {
                    $selectedTabIds = DB::table('product_export_request_tab_products')
                        ->where('product_export_request_id', $req->id)
                        ->whereNotNull('firm_contract_tab_id')
                        ->distinct()
                        ->pluck('firm_contract_tab_id')
                        ->map(function ($v) {
                            return (int) $v;
                        })->values();
                }
                $detail['selected_tab_ids'] = $selectedTabIds;
```

- [ ] **Step 4: Chạy test** — Expected PASS sau khi Task 4 xong; nếu chạy ngay sau Task 2 mà service chưa N-tab thì `selected_tab_ids` có thể rỗng (phiếu ghi 1 tab không set `firm_contract_tab_id`) → chấp nhận fail tạm, xác nhận lại ở Task 4 Step 6.

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_edit_data_tra_tabs_va_selected_tab_ids`

- [ ] **Step 5: `php -l`** sạch.

---

## Task 3: BE — `rulesForType()` thêm `firm_tab_ids` khi gửi duyệt loại 14

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (`rulesForType()`, block `if ($isFirmContract)` ~1080-1083)
- Test: `tests/Feature/ProductExportRequest/FirmContractTabsTest.php`

**Interfaces:**
- Produces: khi status=2 & loại 14, rules có `firm_tab_ids => required|array|min:1`, `firm_tab_ids.* => integer|exists:firm_contract_tabs,id`.

- [ ] **Step 1: Thêm test** — gửi duyệt thiếu `firm_tab_ids` → 422.

```php
    public function test_gui_duyet_thieu_firm_tab_ids_tra_422(): void
    {
        $firm = $this->requireFirm();
        $line = DB::table('firm_contract_tab_products')->where('firm_contract_id', self::FIRM_ID)->orderBy('id')->first(['id', 'parent_id', 'vat_percent']);
        if (!$line) {
            $this->markTestSkipped('HĐ hãng không có dòng.');
        }
        $this->postRequest([
            'type' => 14, 'status' => 2, 'firm_contract_id' => self::FIRM_ID,
            'warehouse_id' => 1, 'transition_type' => 1,
            'firm_tab_vat_percent' => (float) $line->vat_percent,
            // KHÔNG gửi firm_tab_ids
            'products' => [['contract_product_id' => (int) $line->id, 'qty' => 1]],
        ])->assertStatus(422)->assertJsonValidationErrors('firm_tab_ids');
    }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL** (hiện trả 200 hoặc fail ở chỗ khác vì chưa có rule).

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_gui_duyet_thieu_firm_tab_ids_tra_422`

- [ ] **Step 3: Sửa block `if ($isFirmContract)`** trong `rulesForType()`:

```php
        if ($isFirmContract) { // Loại 14 (Xuất bán hàng): gửi duyệt mới bắt buộc VAT + nhóm hàng hóa + kho xuất
            $rules['firm_tab_vat_percent'] = 'required|numeric';
            $rules['firm_tab_ids'] = 'required|array|min:1';
            $rules['firm_tab_ids.*'] = 'integer|exists:firm_contract_tabs,id';
            $rules['warehouse_id'] = 'required_unless:is_export_direct,1|nullable|integer';
        }
```

- [ ] **Step 4: Chạy test, xác nhận PASS**

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_gui_duyet_thieu_firm_tab_ids_tra_422`

- [ ] **Step 5: `php -l`** sạch.

---

## Task 4: BE — Service lặp **N tab** theo nhóm + persist `firm_tab_vat_percent`

**Files:**
- Modify: `Modules/Assign/Services/ProductExportRequestService.php` (`createFromFirmContract()` ~1095-1165; `writeFirmContractLines()` ~1183-1284 → tách; `updateFromRequest()` nhánh firm ~1590-1602)
- Test: `tests/Feature/ProductExportRequest/FirmContractTabsTest.php`

**Interfaces:**
- Produces:
  - `private function writeFirmContractTabs(FirmContract $firmContract, ProductExportRequest $req, array $data, int $status, ?int $excludeRequestId, bool $checkQty = true): void` — chạy check gửi duyệt + lặp tạo N `ProductExportRequestTab` (1/nhóm) + ghi dòng từng nhóm.
  - `private function writeFirmContractTabLines(ProductExportRequest $req, FirmContract $firmContract, ProductExportRequestTab $tab, $groupLines, array $qtyByLine, array $productMeta): void` — ghi `tab_products` + `details` cho các dòng của 1 tab (body cũ của `writeFirmContractLines`, bỏ phần check).
- Consumes: `assertSubmitProductsRequired()`, `assertFirmContractLineQtyWithinRemaining()`, `resolveModelBrand()` (giữ nguyên).

> **Nhóm cần tạo tab** = `firm_tab_ids` (FE gửi); rỗng (nháp cũ) → fallback distinct `parent_id` của dòng đã chọn. Nhóm có trong `firm_tab_ids` nhưng không có dòng tick → vẫn tạo tab rỗng (parity ERP).

- [ ] **Step 1: Thêm test N-tab** — chọn dòng ở ≥1 nhóm, submit, đếm tabs = số nhóm chọn.

```php
    public function test_tao_n_tab_theo_nhom_da_chon(): void
    {
        $this->requireFirm();
        // Gom dòng theo nhóm (parent_id), chọn tối đa 2 nhóm đầu, mỗi nhóm 1 dòng.
        $lines = DB::table('firm_contract_tab_products')
            ->where('firm_contract_id', self::FIRM_ID)->orderBy('id')->get(['id', 'parent_id', 'vat_percent']);
        $byGroup = $lines->groupBy('parent_id');
        $groups = $byGroup->keys()->take(2);
        if ($groups->isEmpty()) {
            $this->markTestSkipped('HĐ hãng không có nhóm.');
        }
        $vat = (float) $byGroup[$groups->first()]->first()->vat_percent;
        $products = [];
        $tabIds = [];
        foreach ($groups as $g) {
            // chỉ lấy dòng cùng mức VAT với nhóm đầu để hợp lệ "một phiếu một VAT"
            $line = $byGroup[$g]->firstWhere('vat_percent', $vat);
            if (!$line) { continue; }
            $tabIds[] = (int) $g;
            $products[] = ['contract_product_id' => (int) $line->id, 'qty' => 1];
        }
        if (count($products) < 1) {
            $this->markTestSkipped('Không gom được dòng cùng VAT.');
        }

        $req = app(\Modules\Assign\Services\ProductExportRequestService::class)->createFromFirmContract([
            'status' => 3,
            'firm_contract_id' => self::FIRM_ID,
            'firm_tab_vat_percent' => $vat,
            'firm_tab_ids' => $tabIds,
            'products' => $products,
        ]);

        $tabCount = DB::table('product_export_request_tabs')->where('parent_id', $req->id)->count();
        $this->assertSame(count($tabIds), $tabCount, 'Số tab phải bằng số nhóm đã chọn');
        // firm_tab_vat_percent được persist.
        $this->assertEquals($vat, (float) DB::table('product_export_requests')->where('id', $req->id)->value('firm_tab_vat_percent'));
        // Mỗi tab mang đúng firm_contract_tab_id.
        $savedTabIds = DB::table('product_export_request_tabs')->where('parent_id', $req->id)->pluck('firm_contract_tab_id')->map(fn($v) => (int) $v)->sort()->values()->all();
        sort($tabIds);
        $this->assertSame($tabIds, $savedTabIds);
    }

    public function test_fallback_suy_nhom_tu_parent_id_khi_thieu_firm_tab_ids(): void
    {
        $this->requireFirm();
        $line = DB::table('firm_contract_tab_products')->where('firm_contract_id', self::FIRM_ID)->orderBy('id')->first(['id', 'parent_id', 'vat_percent']);
        if (!$line) { $this->markTestSkipped('HĐ hãng không có dòng.'); }
        $req = app(\Modules\Assign\Services\ProductExportRequestService::class)->createFromFirmContract([
            'status' => 3,
            'firm_contract_id' => self::FIRM_ID,
            'firm_tab_vat_percent' => (float) $line->vat_percent,
            // KHÔNG gửi firm_tab_ids (phiếu nháp cũ)
            'products' => [['contract_product_id' => (int) $line->id, 'qty' => 1]],
        ]);
        $this->assertSame(
            (int) $line->parent_id,
            (int) DB::table('product_export_request_tabs')->where('parent_id', $req->id)->value('firm_contract_tab_id')
        );
    }
```

- [ ] **Step 2: Chạy test, xác nhận FAIL** (service hiện tạo 1 tab, `firm_contract_tab_id` null, `firm_tab_vat_percent` không persist).

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_tao_n_tab_theo_nhom_da_chon`

- [ ] **Step 3: Tách `writeFirmContractLines` → `writeFirmContractTabs` + `writeFirmContractTabLines`.** Thay nguyên method `writeFirmContractLines(...)` bằng 2 method:

```php
    /**
     * Ghi dòng hàng HĐ hãng thành N TAB (1 tab / firm_contract_tabs.id). Dùng chung
     * createFromFirmContract (tạo) và updateFromRequest (sửa — sau deleteLines).
     * Nhóm tạo tab = $data['firm_tab_ids'] (FE gửi); rỗng → fallback distinct parent_id dòng đã chọn.
     * Nhóm có trong firm_tab_ids nhưng không tick dòng → vẫn tạo tab rỗng (parity ERP).
     */
    private function writeFirmContractTabs(
        FirmContract $firmContract,
        ProductExportRequest $req,
        array $data,
        int $status,
        ?int $excludeRequestId,
        bool $checkQty = true
    ): void {
        $products = $data['products'] ?? [];
        $qtyByLine = [];
        foreach ($products as $p) {
            if (!empty($p['contract_product_id'])) {
                $qtyByLine[(int) $p['contract_product_id']] = (float) ($p['qty'] ?? 0);
            }
        }
        $hasSelection = !empty($qtyByLine);

        // Gửi duyệt mà không có dòng hàng → bắt buộc nhập.
        if ($status === ProductExportRequest::STATUS_CHO_DUYET && !$hasSelection) {
            $this->assertSubmitProductsRequired([]);
        }
        // Check SL còn lại — CHỈ khi Gửi duyệt (nháp bỏ qua).
        if ($checkQty && $status === ProductExportRequest::STATUS_CHO_DUYET && $hasSelection) {
            $this->assertFirmContractLineQtyWithinRemaining((int) $firmContract->id, $products, $excludeRequestId);
        }

        // Dòng HĐ hãng cho các sản phẩm đã chọn (giữ nguyên query cũ).
        $lines = $hasSelection
            ? DB::table('firm_contract_tab_products as fctp')
                ->where('fctp.firm_contract_id', $firmContract->id)
                ->whereIn('fctp.id', array_keys($qtyByLine))
                ->orderBy('fctp.id')
                ->get([
                    'fctp.id', 'fctp.parent_id', 'fctp.product_id', 'fctp.code', 'fctp.product_name',
                    'fctp.model_id', 'fctp.model_name', 'fctp.brand_id', 'fctp.brand_name',
                    'fctp.unit_id', 'fctp.unit_name', 'fctp.quantity',
                    'fctp.standard_price', 'fctp.net_price', 'fctp.price_extra', 'fctp.vat_percent',
                ])
            : collect();

        $linesByGroup = $lines->groupBy('parent_id');

        // Nhóm cần tạo tab: firm_tab_ids FE gửi; fallback = các parent_id có dòng.
        $tabIds = array_values(array_unique(array_map('intval', $data['firm_tab_ids'] ?? [])));
        if (empty($tabIds)) {
            $tabIds = $linesByGroup->keys()->map(function ($v) {
                return (int) $v;
            })->all();
        }
        if (empty($tabIds)) {
            return; // nháp sớm: chưa chọn nhóm & chưa tick dòng.
        }

        // Tên nhóm (firm_contract_tabs.name) cho các nhóm sẽ tạo tab.
        $groupNames = DB::table('firm_contract_tabs')
            ->whereIn('id', $tabIds)
            ->pluck('name', 'id');

        $productMeta = $this->resolveModelBrand($lines->pluck('product_id')->all());

        foreach ($tabIds as $gid) {
            $tab = new ProductExportRequestTab();
            $tab->fill([
                'parent_id' => $req->id,
                'firm_contract_id' => $firmContract->id,
                'firm_contract_tab_id' => $gid,
                'name' => $groupNames[$gid] ?? $firmContract->code,
            ]);
            $tab->save();

            $groupLines = $linesByGroup->get($gid, collect());
            if ($groupLines->isNotEmpty()) {
                $this->writeFirmContractTabLines($req, $firmContract, $tab, $groupLines, $qtyByLine, $productMeta);
            }
        }
    }

    /**
     * Ghi tab_products + details phẳng cho các dòng thuộc 1 tab. (Body cũ của writeFirmContractLines,
     * bỏ phần check — check đã chạy ở writeFirmContractTabs.) Xem docblock 2 cột khoá bên dưới.
     *
     * ⚠️ firm_contract_tab_id = firm_contract_tab_products.PARENT_ID (id firm_contract_tabs);
     *    firm_contract_tab_product_id = id CHÍNH dòng SP (= contract_product_id FE gửi).
     */
    private function writeFirmContractTabLines(
        ProductExportRequest $req,
        FirmContract $firmContract,
        ProductExportRequestTab $tab,
        $groupLines,
        array $qtyByLine,
        array $productMeta
    ): void {
        foreach ($groupLines as $line) {
            $qty = $qtyByLine[(int) $line->id] ?? 0.0;
            if ($qty <= 0) {
                continue;
            }

            $tp = new ProductExportRequestTabProduct();
            $tp->fill([
                'parent_id' => $tab->id,
                'product_export_request_id' => $req->id,
                'firm_contract_id' => $firmContract->id,
                'firm_contract_tab_id' => $line->parent_id,
                'firm_contract_tab_product_id' => $line->id,
                'product_id' => $line->product_id,
                'unit_id' => $line->unit_id,
                'need_export' => 1,
                'qty' => $qty,
                'contract_qty' => (float) $line->quantity,
                'vat_percent' => (float) ($line->vat_percent ?? 0),
            ]);
            $tp->save();

            $listedPrice = (float) $line->standard_price;
            $extraPrice = (float) ($line->price_extra ?? 0);
            $allocatedPrice = (float) ($line->net_price ?? 0);
            $salePrice = $listedPrice + $extraPrice;
            $meta = $productMeta[(int) $line->product_id] ?? null;
            DB::table('product_export_request_details')->insert([
                'parent_id' => $req->id,
                'product_id' => $line->product_id,
                'unit_id' => $line->unit_id,
                'product_name' => $line->product_name,
                'code' => $line->code,
                'model_id' => $line->model_id ?: ($meta->model_id ?? null),
                'brand_id' => $line->brand_id ?: ($meta->brand_id ?? null),
                'model_name' => $line->model_name,
                'brand_name' => $line->brand_name,
                'unit_name' => $line->unit_name,
                'qty' => $qty,
                'price' => $listedPrice,
                'extra_price' => $extraPrice,
                'allocated_price' => $allocatedPrice,
                'total_amount' => $qty * $salePrice,
                'vat_percent' => (float) ($line->vat_percent ?? 0),
                'need_export' => 1,
                'detail_type' => 1,
                'firm_contract_tab_product_id' => $line->id,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
```

- [ ] **Step 4: Cập nhật `createFromFirmContract`** — persist `firm_tab_vat_percent` + gọi wrapper N-tab. Trong `$req->fill([...])` thêm dòng (cạnh `transition_type`):

```php
                // Một phiếu một VAT (header) — persist để màn Sửa dựng lại + downstream parity ERP.
                'firm_tab_vat_percent' => isset($data['firm_tab_vat_percent']) ? (float) $data['firm_tab_vat_percent'] : null,
```

Và thay khối tạo 1 tab (`if ($firmContract) { $tab = new ProductExportRequestTab()...writeFirmContractLines(...) }`) bằng:

```php
            // Chưa chọn HĐ hãng (nháp sớm) → chỉ lưu phiếu trống, chưa có dòng hàng.
            if ($firmContract) {
                $this->writeFirmContractTabs($firmContract, $req, $data, $status, null);
            }
```

- [ ] **Step 5: Cập nhật `updateFromRequest`** nhánh firm. Trong khối set field (cạnh `$req->total_km_expected = ...`, trước `$req->save()`) thêm:

```php
                $req->firm_tab_vat_percent = isset($data['firm_tab_vat_percent']) ? (float) $data['firm_tab_vat_percent'] : $req->firm_tab_vat_percent;
```

Và thay khối sau `deleteLines` (`if ($isFirmContractType) { if ($firmContract) { $tab = new ...writeFirmContractLines(...) } }`) bằng:

```php
            if ($isFirmContractType) {
                // Chưa chọn HĐ hãng (nháp) → chỉ dọn dòng, không ghi gì.
                if ($firmContract) {
                    // Check SL còn lại đã chạy ở trên (trước deleteLines) → bỏ qua lần 2 (checkQty=false).
                    $this->writeFirmContractTabs($firmContract, $req, $data, (int) $req->status, (int) $req->id, false);
                }
            } elseif ($isContractType) {
```

- [ ] **Step 6: Chạy toàn bộ test file, xác nhận PASS** (gồm Task 2 edit-data test giờ đã đủ điều kiện).

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php`
Expected: tất cả PASS (hoặc SKIP khi thiếu HĐ 24930).

- [ ] **Step 7: Thêm test exclude-self khi Sửa gửi duyệt** (Review Focus #5) — sửa phiếu không tự chặn chính nó:

```php
    public function test_sua_gui_duyet_khong_tu_chan_chinh_minh(): void
    {
        $this->requireFirm();
        $line = DB::table('firm_contract_tab_products')->where('firm_contract_id', self::FIRM_ID)->orderBy('id')->first(['id', 'parent_id', 'vat_percent']);
        if (!$line) { $this->markTestSkipped('HĐ hãng không có dòng.'); }
        $vat = (float) $line->vat_percent;
        // Tạo nháp rồi PUT gửi duyệt cùng SL — không được 422 vì tự trừ chính mình.
        $id = $this->postRequest([
            'type' => 14, 'status' => 3, 'firm_contract_id' => self::FIRM_ID, 'warehouse_id' => 1, 'transition_type' => 1,
            'firm_tab_vat_percent' => $vat, 'firm_tab_ids' => [(int) $line->parent_id],
            'products' => [['contract_product_id' => (int) $line->id, 'qty' => 1]],
        ])->json('data.id');

        $this->putRequest($id, [
            'type' => 14, 'status' => 2, 'firm_contract_id' => self::FIRM_ID, 'warehouse_id' => 1, 'transition_type' => 1,
            'firm_tab_vat_percent' => $vat, 'firm_tab_ids' => [(int) $line->parent_id],
            'products' => [['contract_product_id' => (int) $line->id, 'qty' => 1]],
        ])->assertStatus(200);
    }
```

- [ ] **Step 8: Chạy test** + `php -l` service sạch.

Run: `php artisan test tests/Feature/ProductExportRequest/FirmContractTabsTest.php --filter test_sua_gui_duyet_khong_tu_chan_chinh_minh && php -l Modules/Assign/Services/ProductExportRequestService.php`

- [ ] **Step 9: Regression — chạy toàn bộ suite ProductExportRequest** (phải giữ 110 pass + test mới).

Run: `php artisan test tests/Feature/ProductExportRequest`
Expected: PASS (các test cũ không đổi; test mới PASS/SKIP).

---

## Task 5: FE — `data()` + computed (firmContractTabs, selectedTabIds, firmTabOptions, firmSelectedGroups) + customerInfo 2 field

**Files:**
- Modify: `pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (`data()` ~1090-1144; computed khu ~1280-1396)

**Interfaces:**
- Produces (dùng ở Task 6-8):
  - data: `firmContractTabs: []`, `selectedTabIds: []`.
  - computed `firmTabOptions()` → `[{ id, name }]` (nhóm có ≥1 dòng khớp `firmTabVatPercent`).
  - computed `firmSelectedGroups()` → `[{ id, name, lines }]` theo `selectedTabIds`, `lines` lọc theo VAT + parent_id.
  - method `firmGroupLines(tabId)` → mảng dòng của 1 nhóm (dùng trong template tab-pane).
- Consumes: `firmContractLines` (đã có), `firmTabVatPercent` (đã có), `vatOptions` (đã có), `customerInfo` (đã có).

- [ ] **Step 1: data() thêm 2 key** (cạnh `firmContractLines`/`vatOptions`):

```js
            firmContractTabs: [],
            selectedTabIds: [],
```

- [ ] **Step 2: customerInfo khởi tạo thêm 2 field** — trong khởi tạo `customerInfo: {}` (~1114) đảm bảo có `customer_unit` + `delivery_place` (nếu customerInfo là object literal có key, thêm `customer_unit: '', delivery_place: ''`; nếu là `{}` rỗng thì bỏ qua — set khi load).

- [ ] **Step 3: Thêm computed** (cạnh `firmContractDisplayLines`):

```js
        // Nhóm hàng hóa có ≥1 dòng khớp VAT đang chọn — nguồn multi-select "Chọn nhóm hàng hóa".
        firmTabOptions() {
            const vat = Number(this.firmTabVatPercent)
            const groupsWithLines = new Set(
                (this.firmContractLines || [])
                    .filter((l) => Number(l.vat_percent) === vat)
                    .map((l) => Number(l.parent_id))
            )
            return (this.firmContractTabs || [])
                .filter((t) => groupsWithLines.has(Number(t.id)))
                .map((t) => ({ id: Number(t.id), name: t.name }))
        },
        // Các nhóm đã chọn (giao với firmTabOptions) kèm dòng hàng của nhóm — nguồn nav-tabs + submit.
        firmSelectedGroups() {
            const vat = Number(this.firmTabVatPercent)
            const selected = (this.selectedTabIds || []).map((v) => Number(v))
            return (this.firmContractTabs || [])
                .filter((t) => selected.includes(Number(t.id)))
                .map((t) => ({
                    id: Number(t.id),
                    name: t.name,
                    lines: (this.firmContractLines || []).filter(
                        (l) => Number(l.vat_percent) === vat && Number(l.parent_id) === Number(t.id)
                    ),
                }))
        },
```

- [ ] **Step 4: Thêm method `firmGroupLines`** (trong `methods`, cạnh `firmLinePrice`):

```js
        firmGroupLines(tabId) {
            const vat = Number(this.firmTabVatPercent)
            return (this.firmContractLines || []).filter(
                (l) => Number(l.vat_percent) === vat && Number(l.parent_id) === Number(tabId)
            )
        },
```

- [ ] **Step 5: Kiểm biên dịch** — build dev không lỗi.

Run (nếu dev server đang chạy, bỏ qua): `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client && npx eslint pages/finance/product-export-requests/components/ProductExportRequestForm.vue`
Expected: không lỗi cú pháp mới (cảnh báo style cũ bỏ qua).

---

## Task 6: FE — panel 2 field + Nhóm VAT required + Chọn nhóm hàng hóa multi-select

**Files:**
- Modify: `ProductExportRequestForm.vue` (panel KH ~259-283; khối firm detail header ~469-474)

**Interfaces:**
- Consumes: `customerInfo.customer_unit`, `customerInfo.delivery_place` (Task 9 load), `firmTabOptions` (Task 5), `isFirmContractType`, `isEdit` (cờ màn Sửa — xác minh tên cờ hiện có khi code; nếu không có dùng `!!form.id`).
- Produces: `selectedTabIds` v-model; reset khi đổi VAT (`onFirmVatChange`).

- [ ] **Step 1: Thêm 2 dòng hiển thị vào panel KH** — ngay sau dòng "Địa chỉ" (span-2), trong `fld-grid cols-3`:

```html
                            <div v-if="isFirmContractType" class="fld">
                                <span class="ro-lbl">Tên viết tắt</span>
                                <div class="ro-value" :class="{ 'ro-empty': !customerInfo.customer_unit }">{{ customerInfo.customer_unit }}</div>
                            </div>
                            <div v-if="isFirmContractType" class="fld" style="grid-column: span 2">
                                <span class="ro-lbl">Địa chỉ giao hàng</span>
                                <div class="ro-value" :class="{ 'ro-empty': !customerInfo.delivery_place }">{{ customerInfo.delivery_place }}</div>
                            </div>
```

- [ ] **Step 2: Thay khối "Nhóm theo VAT"** (hiện `v-if="vatOptions.length > 1"`) bằng Nhóm VAT luôn hiện (required, khóa khi Sửa) + Chọn nhóm hàng hóa. Đặt đầu `<template v-if="isFirmContractType">`:

```html
                        <div class="fld-grid cols-3 mb-2">
                            <div class="fld" style="max-width: 260px">
                                <V2BaseLabel required>Nhóm VAT</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="firmTabVatPercent"
                                    :options="vatOptions"
                                    placeholder="Chọn mức VAT"
                                    :disabled="isFirmLocked"
                                    @change="onFirmVatChange"
                                />
                                <div v-if="touched && isFirmContractType && (firmTabVatPercent === null || firmTabVatPercent === '')" class="fld-err">
                                    Bắt buộc phải nhập
                                </div>
                            </div>
                            <div class="fld" style="grid-column: span 2">
                                <V2BaseLabel required>Chọn nhóm hàng hóa</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="selectedTabIds"
                                    :options="firmTabOptions"
                                    :extraSettings="{ multiple: true }"
                                    placeholder="Chọn nhóm hàng hóa"
                                    :disabled="isFirmLocked"
                                />
                                <div v-if="touched && isFirmContractType && !selectedTabIds.length" class="fld-err">
                                    Bắt buộc phải nhập
                                </div>
                            </div>
                        </div>
```

> `isFirmLocked` = computed `this.isFirmContractType && !!this.form.id` (khóa 2 selector khi Sửa — parity ERP `ng-disabled=form.id`). `touched` là cờ đã có trên màn (bật sau submit đầu) — xác minh tên khi code; nếu màn dùng cờ khác cho inline-error thì theo đúng cờ đó.

- [ ] **Step 3: Thêm computed `isFirmLocked`** (cạnh `isFirmContractType`):

```js
        isFirmLocked() {
            return this.isFirmContractType && !!this.form.id
        },
```

- [ ] **Step 4: Thêm method `onFirmVatChange`** (reset nhóm + tick khi đổi VAT — Review Focus #1):

```js
        onFirmVatChange() {
            // Đổi VAT → nhóm cũ không còn hợp lệ: reset lựa chọn nhóm + bỏ tick/SL để không gửi âm thầm dòng VAT cũ.
            this.selectedTabIds = []
            ;(this.firmContractLines || []).forEach((l) => {
                l._checked = false
                l._qty = null
            })
        },
```

- [ ] **Step 5: Playwright kiểm** (`http://127.0.0.1:3000`, login Admin): mở Tạo loại 14 → chọn HĐ hãng → panel hiện **Tên viết tắt** + **Địa chỉ giao hàng**; chọn **Nhóm VAT** → **Chọn nhóm hàng hóa** liệt kê nhóm; HĐ 1 VAT → VAT auto 1 option. Không console error.

---

## Task 7: FE — chi tiết chuyển bảng phẳng → **b-tabs theo nhóm**

**Files:**
- Modify: `ProductExportRequestForm.vue` (khối bảng firm detail ~476-544)

**Interfaces:**
- Consumes: `firmSelectedGroups`, `firmGroupLines(tabId)` (Task 5).
- Produces: render N tab, mỗi tab = 1 bảng dòng của nhóm; placeholder khi chưa chọn nhóm.

- [ ] **Step 1: Bọc bảng hiện có vào `<b-tabs>`** — thay `<V2BaseTableScroll>...bảng cũ...</V2BaseTableScroll>` (dùng `firmContractDisplayLines`) bằng:

```html
                        <div v-if="!selectedTabIds.length" class="text-center" style="color: #6b7280; padding: 14px">
                            {{ form.firm_contract_id ? 'Chọn nhóm hàng hóa để hiển thị hàng hoá.' : 'Chọn hợp đồng hãng để hiển thị hàng hoá.' }}
                        </div>
                        <b-tabs v-else nav-class="nav-tabs nav-bordered" class="pnh-tabs">
                            <b-tab v-for="group in firmSelectedGroups" :key="'ftab-' + group.id" :title="group.name">
                                <V2BaseTableScroll max-height="520">
                                    <table class="table table-bordered table-sm mb-0 er-table">
                                        <thead class="bg-light">
                                            <tr>
                                                <th style="width: 44px" class="text-center">STT</th>
                                                <th style="width: 70px" class="text-center">Cần xuất</th>
                                                <th style="min-width: 220px">Tên hàng</th>
                                                <th style="width: 120px">Model</th>
                                                <th style="width: 120px">Mã</th>
                                                <th style="width: 80px">ĐVT</th>
                                                <th class="text-center" style="width: 90px">Hợp đồng</th>
                                                <th class="text-center" style="width: 90px">Đã xuất</th>
                                                <th class="text-center" style="width: 90px">Đang xuất</th>
                                                <th class="text-center" style="width: 100px">Còn được xuất</th>
                                                <th class="text-center" style="width: 110px">Đề nghị</th>
                                                <th class="text-right" style="width: 110px">Giá niêm yết</th>
                                                <th class="text-right" style="width: 100px">Giá bán</th>
                                                <th class="text-right" style="width: 120px">Thành tiền</th>
                                                <th class="text-right" style="width: 110px">Giảm</th>
                                                <th class="text-center" style="width: 60px">VAT%</th>
                                                <th class="text-right" style="width: 130px">Sau VAT</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(line, idx) in firmGroupLines(group.id)" :key="'f-' + group.id + '-' + line.contract_product_id">
                                                <td class="text-center">{{ idx + 1 }}</td>
                                                <td class="text-center"><input type="checkbox" v-model="line._checked" /></td>
                                                <td>
                                                    <div>{{ line.name }}</div>
                                                    <div v-if="line.brand_name" class="er-muted" style="font-size: 11px">{{ line.brand_name }}</div>
                                                </td>
                                                <td>{{ line.model_name || '' }}</td>
                                                <td>{{ line.code || '' }}</td>
                                                <td>{{ line.unit_name || '' }}</td>
                                                <td class="text-center">{{ numOrEmpty(line.contract_qty) }}</td>
                                                <td class="text-center">{{ numOrEmpty(line.exported_qty) }}</td>
                                                <td class="text-center">{{ numOrEmpty(line.in_flight_qty) }}</td>
                                                <td class="text-center">{{ numOrEmpty(line.remaining_qty) }}</td>
                                                <td>
                                                    <input
                                                        type="number"
                                                        class="form-control form-control-sm text-right"
                                                        :class="{ 'is-invalid': line._checked && !firmContractQtyValid(line) }"
                                                        min="0"
                                                        step="any"
                                                        :disabled="!line._checked"
                                                        v-model.number="line._qty"
                                                    />
                                                    <div v-if="line._checked && !firmContractQtyValid(line)" class="fld-err">
                                                        Vượt số lượng còn được xuất ({{ numOrEmpty(line.remaining_qty) }}).
                                                    </div>
                                                </td>
                                                <td class="text-right">{{ numOrEmpty(line.quoted_price) }}</td>
                                                <td class="text-right">{{ numOrEmpty(firmLinePrice(line).sale) }}</td>
                                                <td class="text-right">{{ numOrEmpty(firmLinePrice(line).saleAmount) }}</td>
                                                <td class="text-right">{{ numOrEmpty(firmLinePrice(line).discountAmount) }}</td>
                                                <td class="text-center">{{ numOrEmpty(line.vat_percent) }}</td>
                                                <td class="text-right">{{ numOrEmpty(firmLinePrice(line).afterVat) }}</td>
                                            </tr>
                                            <tr v-if="!firmGroupLines(group.id).length">
                                                <td colspan="17" class="text-center" style="color: #6b7280; padding: 14px">Nhóm không có dòng hàng phù hợp.</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </V2BaseTableScroll>
                            </b-tab>
                        </b-tabs>
```

> nav-tabs copy pattern từ `pages/finance/product-imports/components/ProductImportForm.vue:170` (`<b-tabs nav-class="nav-tabs nav-bordered" class="pnh-tabs">`). Giữ nguyên markup ô trong bảng (checkbox/number thô) như bản phẳng cũ — port pattern sẵn có của màn.

- [ ] **Step 2: Playwright kiểm** — chọn ≥2 nhóm → hiện ≥2 tab, mỗi tab đúng dòng của nhóm; đổi Nhóm VAT → nhóm reset, tab biến mất. Không console error.

---

## Task 8: FE — submit (`buildProducts` + `firm_tab_ids`), `paymentSummary`, `validateForm`, load Tạo/Sửa

**Files:**
- Modify: `ProductExportRequestForm.vue` (`buildProducts` ~2199-2221; `paymentSummary` ~1280-1305; `validateForm` ~2223-2349; `onSubmitClick` ~2351-2408; `loadFirmContractLines` ~1883-1912; `applyInitialData` ~2020-2037)

**Interfaces:**
- Consumes: `firmSelectedGroups`, `selectedTabIds`, `firmContractQtyValid`, detail từ BE (`tabs`, `selected_tab_ids`, `customer_unit`, `delivery_place`, `firm_tab_vat_percent`).
- Produces: payload loại 14 thêm `firm_tab_ids`.

- [ ] **Step 1: `buildProducts()` nhánh 14 — gom mọi nhóm đã chọn:**

```js
            // Loại 14: gom dòng _checked hợp lệ của TẤT CẢ nhóm đã chọn (không chỉ 1 VAT đang xem).
            if (this.isFirmContractType) {
                const out = []
                this.firmSelectedGroups.forEach((g) => {
                    g.lines.forEach((line) => {
                        if (line._checked && this.firmContractQtyValid(line)) {
                            out.push({ contract_product_id: line.contract_product_id, qty: Number(line._qty) })
                        }
                    })
                })
                return out
            }
```

- [ ] **Step 2: `paymentSummary` dùng cùng tập dòng** — thay chỗ sum `firmContractDisplayLines` (checked+valid) bằng gom qua `firmSelectedGroups`:

```js
            // Loại 14: tổng trên dòng đã chọn của mọi nhóm (đúng VAT hiện hành).
            const firmLines = this.firmSelectedGroups.reduce((acc, g) => acc.concat(g.lines), [])
            // ... phần còn lại giữ nguyên, thay firmContractDisplayLines → firmLines ...
```

- [ ] **Step 3: `onSubmitClick` — thêm `firm_tab_ids` vào payload loại 14** (cạnh `firm_tab_vat_percent`):

```js
                payload.firm_tab_ids = this.selectedTabIds.map((v) => Number(v))
```

- [ ] **Step 4: `validateForm(status)` — gửi duyệt loại 14 kiểm nhóm:** sau kiểm `firm_contract_id` + `firmTabVatPercent`, thêm:

```js
                if (this.isFirmContractType && status === 2 && !this.selectedTabIds.length) {
                    ok = false // báo đỏ ô "Chọn nhóm hàng hóa" (đã có inline error Task 6)
                }
```

(Giữ kiểm ≥1 dòng qty>0 hợp lệ qua `buildProducts().length` như hiện có.)

- [ ] **Step 5: `loadFirmContractLines` (Tạo) — nạp tabs + 2 field:** sau khi set `vatOptions`/`firmContractLines`/`firmTabVatPercent`, thêm:

```js
                this.firmContractTabs = data.tabs || []
                this.selectedTabIds = [] // để trống, bắt user chọn chủ động (Quyết định đã chốt)
                this.$set(this.customerInfo, 'customer_unit', (data.contract && data.contract.customer_unit) || '')
                this.$set(this.customerInfo, 'delivery_place', (data.contract && data.contract.delivery_place) || '')
```

- [ ] **Step 6: `applyInitialData` (Sửa) — dựng lại nhóm + 2 field + VAT:** trong nhánh 14, sau khi set `firmContractLines`/tick từ `selected_lines`, thêm:

```js
                this.firmContractTabs = d.tabs || []
                this.$set(this.customerInfo, 'customer_unit', d.customer_unit || '')
                this.$set(this.customerInfo, 'delivery_place', d.delivery_place || '')
                // VAT: ưu tiên giá trị đã persist; fallback suy từ dòng đã tick (phiếu cũ).
                if (d.firm_tab_vat_percent !== null && d.firm_tab_vat_percent !== undefined) {
                    this.firmTabVatPercent = Number(d.firm_tab_vat_percent)
                }
                // Nhóm đã chọn: ưu tiên selected_tab_ids; fallback suy từ parent_id của dòng đã tick.
                let selTabs = (d.selected_tab_ids || []).map((v) => Number(v))
                if (!selTabs.length) {
                    const vat = Number(this.firmTabVatPercent)
                    selTabs = [
                        ...new Set(
                            (this.firmContractLines || [])
                                .filter((l) => l._checked && Number(l.vat_percent) === vat)
                                .map((l) => Number(l.parent_id))
                        ),
                    ]
                }
                this.selectedTabIds = selTabs
```

- [ ] **Step 7: Playwright kiểm end-to-end** (`http://127.0.0.1:3000`):
  1. Tạo loại 14 → chọn HĐ → Nhóm VAT → 2 nhóm → tick + nhập SL ở cả 2 tab → Gửi duyệt → về danh sách, không lỗi.
  2. Mở **Sửa** phiếu nháp vừa tạo → dựng lại đúng VAT + 2 nhóm (2 selector khóa) + tick/SL.
  3. Gửi duyệt thiếu Nhóm VAT / chưa chọn nhóm → báo đỏ đúng ô; BE trả 422 (network).
  4. Kiểm tinker read-only: `product_export_request_tabs` có N dòng/phiếu, `details` đủ dòng.
- [ ] **Step 8: Dọn phiếu test** khỏi DB dev sau verify.

---

## Self-Review (đã chạy khi viết plan)

1. **Spec coverage:** §1 mục 1-6 ↔ Task 1-2 (customer_unit/delivery_place), Task 2 (tabs/selected_tab_ids), Task 3 (firm_tab_ids rule), Task 4 (N tab + persist VAT), Task 6 (2 selector + panel), Task 7 (nav-tabs), Task 8 (submit/load). §7 loại 15 + 3 check phụ = ngoài phạm vi (đúng). §5 DTO ↔ Task 1/2/8. §6 edge ↔ Review Focus + Task 4/6/8. §9 Quyết định (Hướng A, 1 VAT/phiếu, không migration, selectedTabIds trống khi tạo) ↔ Task 4/6/8 Step 5. Không gap.
2. **Placeholder scan:** mọi step có code thật; không TBD/TODO.
3. **Type consistency:** `writeFirmContractTabs`/`writeFirmContractTabLines` chữ ký nhất quán giữa khai báo (Task 4 Step 3) và chỗ gọi (Step 4/5); `firmTabOptions`/`firmSelectedGroups`/`firmGroupLines` dùng thống nhất `id`/`name`/`lines` ở Task 5-8; `selectedTabIds` luôn normalize `Number()`; `firm_tab_ids` payload (FE Task 8) ↔ rule (BE Task 3) ↔ service đọc `$data['firm_tab_ids']` (Task 4).
4. **Review Focus:** 5 mục đều có task sở hữu test/kiểm (đã ghi trong từng mục).

**Điểm cần implementer xác minh tại chỗ (đã nêu inline):** tên cờ `touched`/`isEdit` trên màn (dùng `!!form.id` nếu không có `isEdit`); cấu trúc hiện tại của `paymentSummary` để thay đúng biến; vị trí chính xác các anchor dòng (số dòng có thể lệch sau các đợt sửa trước).
