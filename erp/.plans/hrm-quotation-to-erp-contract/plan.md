# Lập HĐ ERP từ báo giá HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (khuyến nghị) để thực thi từng task; review giữa các task. Steps dùng checkbox (`- [ ]`).

**Goal:** Cho phép lập `firm_contract` ERP trực tiếp từ báo giá Assign HRM (trúng thầu + đồng bộ hết hàng tạm + VND), không qua `firm_quotation` ERP.

**Architecture:** ERP đọc báo giá HRM qua connection `hrm` (service mới). Tái dùng form "Lập hợp đồng" ERP với nguồn mới "Báo giá HRM" (firm_quotation_tab_id/product_id để null — schema đã nullable từ v2.3). Fork tối thiểu trong `saveFirmContractData()`/`syncTabsFromQuotation()` để build tab/product từ data POST khi không có `firm_quotation`. Ghi ngược `quotations.erp_firm_contract_id` chống trùng.

**Tech Stack:** Laravel 8 (Eloquent, connection `hrm`), AngularJS + Blade (form HĐ + popup).

> **Lưu ý dự án:** KHÔNG commit/push git khi chưa được yêu cầu. Đụng luồng lõi tài chính (`FirmContractService`) → review kỹ từng task. Cặp HRM (Phase 3): `HRM/.plans/hrm-quotation-to-erp-contract/`.

**Spec:** `.plans/hrm-quotation-to-erp-contract/design.md`

---

## PHASE 1 — ERP Backend

### Task 1.0 — SPIKE: ĐÃ XONG (2026-06-15). Kết quả chốt:

**Đã verify:**
- `quotation_product_prices.unit_id` (HRM) = `units.id` **ERP** (model `TpUnit` connection `mysql2` table `units`). → unit_id dùng TRỰC TIẾP, KHÔNG map. Tương tự `model_id/brand_id/origin_id` = id ERP.
- Cột HRM: SL = **`qty_needed`** (double), giá = **`quoted_price`**, **`vat_percent`** per dòng, `code`, `name`, `erp_product_id`, `discount_amount`. (KHÔNG có cột `quantity`/`unit_name`.)
- `firm_contracts.firm_quotation_id` **đã nullable** (migration 2025_07_19_102356). → Task 1.1 chỉ thêm `hrm_quotation_id`.
- `firm_contract_tab_products.product_id` & `firm_contract_tabs.firm_quotation_tab_id`/`..._tab_product_id` đã nullable (v2.3).
- `product_id` luôn có (eligibility ép mọi dòng có `erp_product_id`).
- `doctrine/dbal ^2.10` đã cài.
- Product ERP có `products.unit_id` (đơn vị mặc định) + `ProductUnit.is_base`. `Product::getPriceByUnitAndType($pid,$unitId,$priceType)` → `ProductUnitPrice` có `sale_max_percent` (nếu `unitId` null → lấy `is_base`).

**Mapping chốt (1 dòng HRM → firm_contract_tab_product):**
| Cột HĐ | Nguồn |
|---|---|
| product_id | `erp_product_id` |
| product_name / code | HRM `name`/`code` (fallback `Product->name/code`) |
| unit_id | HRM `unit_id` (id ERP, trực tiếp); nếu null → `products.unit_id` |
| unit_name / unit_coefficient | từ ERP `units`/`product_units` theo unit_id |
| model/brand/origin _id | HRM (id ERP); _name resolve từ ERP nếu cần (nullable→trống) |
| quantity / root_quantity | HRM `qty_needed` |
| price | HRM `quoted_price` |
| vat_percent | HRM `vat_percent` |
| price_extra / price_discount | 0 (NV ERP chỉnh trên form) |
| price_with_extra/after_discount/allocated_price/sale_max_percent/*_coefficient/net_price/standard_price | tính Y HỆT nhánh hiện có `syncTabsFromQuotation` (dòng ~669-694) với unit_id trên |

**Mapping 1 tab mặc định:** name="Hàng hóa", firm_quotation_tab_id=null, total_cost=Σ(qty_needed*quoted_price), total_extra=0, total_discount=0, vat_percent=(của dòng đầu/đa số), vat_cost=Σ tiền VAT dòng, total_after_vat=total_before_vat+vat_cost.

**$quotation usages cần guard khi null** (trong `saveFirmContractData`): `$quotation->delivery_cost`, `$quotation->delivery_vat_percent`, và `$quotation->status = DA_LAP_HD; save()` → default 0 + bỏ qua khi HRM.

---

### Task 1.0-OLD (tham khảo) — chốt cách build tab/product chuẩn cho nguồn HRM

**Files (chỉ đọc):**
- `app/Services/Sale/Firm/Contract/FirmContractService.php:433-718` (`saveFirmContractData`, `syncTabsFromQuotation`)
- `app/Services/Sale/Firm/Quotation/FirmQuotationService.php` (`getDataForContract`)

- [ ] **Step 1:** Đọc `syncTabsFromQuotation()` (dòng 621-718), liệt kê CHÍNH XÁC mọi field của `firm_contract_tabs` và `firm_contract_tab_products` được set, và nguồn của từng field (từ `FirmQuotationTab`/`FirmQuotationTabProduct->attributesToArray()` hay từ `$product` POST). Xác định field nào lấy từ record báo giá (sẽ phải thay bằng data HRM khi nguồn HRM): `name`, `total_cost`, `product_name`, `code`, `unit_id`, `unit_name`, `unit_coefficient`, `model/brand/origin`, `product_attributes`, `price`, `quantity`, `vat_percent`, `sale_max_percent`...
- [ ] **Step 2:** Ghi lại (trong checkpoint plan) "bảng ánh xạ HRM→firm_contract_tab_product": cột HRM `quotation_product_prices` (code, name, erp_product_id, quoted_price, vat_percent, quantity, unit?) → cột HĐ. Xác định các field HĐ cần mà HRM KHÔNG có (unit_id, unit_name, unit_coefficient, model/brand/origin, sale_max_percent) → lấy từ `Product::find(erp_product_id)` (unit mặc định + thuộc tính) như `syncTabsFromQuotation` đang làm với `Product::getPriceByUnitAndType`, `CompanyPriceTypes`, `CompanyProductTypes`.
- [ ] **Step 3:** Quyết định & ghi lại: 1 tab mặc định tên "Hàng hóa" (hoặc theo báo giá HRM), `firm_quotation_tab_id = null`. Output spike: pseudo-mapping đầy đủ để Task 1.5 implement không phải đoán.

> Đây là spike điều tra (không sửa code) — bắt buộc vì pricing là tài chính, không được đoán.

---

### Task 1.1: Migration schema

**Files:**
- Create: `database/migrations/2026_06_15_100000_add_hrm_quotation_id_to_firm_contracts.php`

- [ ] **Step 1: Viết migration**

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddHrmQuotationIdToFirmContracts extends Migration
{
    public function up()
    {
        // firm_quotation_id ĐÃ nullable (migration 2025_07_19_102356) — chỉ thêm cột mới
        Schema::table('firm_contracts', function (Blueprint $table) {
            $table->unsignedBigInteger('hrm_quotation_id')->nullable()->after('firm_quotation_id');
            $table->index('hrm_quotation_id');
        });
    }

    public function down()
    {
        Schema::table('firm_contracts', function (Blueprint $table) {
            $table->dropIndex(['hrm_quotation_id']);
            $table->dropColumn('hrm_quotation_id');
        });
    }
}
```

> Lưu ý: `->change()` cần `doctrine/dbal`. Kiểm tra đã cài chưa (`composer show doctrine/dbal`). Nếu chưa, đổi `firm_quotation_id` sang nullable bằng raw SQL `DB::statement('ALTER TABLE firm_contracts MODIFY firm_quotation_id BIGINT UNSIGNED NULL')`.

- [ ] **Step 2: Chạy migration**

Run: `php artisan migrate`
Expected: migrate OK, `firm_contracts` có `hrm_quotation_id`, `firm_quotation_id` nullable.

- [ ] **Step 3:** Thêm `hrm_quotation_id` vào `$fillable` của `app/Model/Sale/Firm/Contract/FirmContract.php`.

---

### Task 1.2: Service đọc báo giá HRM

**Files:**
- Create: `app/Services/Hrm/HrmQuotationReader.php`
- Reference (pattern): `app/Services/Hrm/CustomerScopeReader.php`

- [ ] **Step 1: Viết service** (đọc connection `hrm`)

```php
<?php
namespace App\Services\Hrm;

use Illuminate\Support\Facades\DB;

class HrmQuotationReader
{
    const HRM = 'hrm';
    const STATUS_TRUNG_THAU = 7;

    /** Danh sách báo giá HRM đủ điều kiện lập HĐ ERP (DataTable nguồn). */
    public function eligibleQuery()
    {
        return DB::connection(self::HRM)->table('quotations as q')
            ->leftJoin('currencies as c', 'c.id', '=', 'q.currency_id')
            ->where('q.status', self::STATUS_TRUNG_THAU)
            ->where('q.tmp_sync_status', 'synced')
            ->whereNull('q.erp_firm_contract_id')
            ->where(function ($w) {
                $w->where('c.code', 'VND')->orWhereNull('q.currency_id'); // VND mặc định
            })
            ->select('q.id', 'q.code', 'q.customer_name', 'q.customer_code',
                     'q.customer_tax_code', 'q.total_after_vat', 'q.created_at');
    }

    /** Lấy 1 báo giá + sản phẩm để prefill form HĐ. Trả null nếu không đủ điều kiện. */
    public function getForContract($hrmQuotationId)
    {
        $q = $this->eligibleQuery()->where('q.id', $hrmQuotationId)->first();
        if (!$q) return null;

        $products = DB::connection(self::HRM)->table('quotation_product_prices')
            ->where('quotation_id', $hrmQuotationId)
            ->get(['id', 'erp_product_id', 'code', 'name', 'unit_id', 'quoted_price', 'vat_percent', 'discount_amount',
                    DB::raw('qty_needed as quantity')]);

        // Bắt buộc mọi dòng đã có erp_product_id (đã sync hết hàng tạm)
        if ($products->whereNull('erp_product_id')->count() > 0) return null;

        return ['quotation' => $q, 'products' => $products];
    }
}
```

> `quotation_product_prices` có cột `quantity` không — Task 1.0 Step 2 phải xác nhận tên cột SL thật (có thể là `quantity` hoặc khác). Sửa select theo thực tế.

- [ ] **Step 2:** `php -l app/Services/Hrm/HrmQuotationReader.php` → sạch.

---

### Task 1.3: Resolve khách hàng ERP + endpoint prefill

**Files:**
- Create/Modify: `app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php` (controller mới cho nguồn HRM trong màn HĐ)
- Modify: `routes/web.php` (prefix `admin/sale/firm-contracts` hoặc nhóm phù hợp)

- [ ] **Step 1: Controller**

```php
public function searchData(Request $request, HrmQuotationReader $reader)
{
    $query = $reader->eligibleQuery();
    return DataTables::of($query)
        ->addColumn('action', function ($o) { return $o->id; })
        ->make(true);
}

public function getDataForContract($id, HrmQuotationReader $reader)
{
    $data = $reader->getForContract($id);
    if (!$data) return $this->responseErrors('Báo giá HRM không đủ điều kiện lập hợp đồng');

    $q = $data['quotation'];
    $customer = \App\Model\Sale\Customer::query()
        ->when($q->customer_code, fn($w) => $w->orWhere('code', $q->customer_code))
        ->when($q->customer_tax_code, fn($w) => $w->orWhere('tax_code', $q->customer_tax_code))
        ->where('status', '<>', 0)->first();
    if (!$customer) return $this->responseErrors("Không tìm thấy khách hàng ERP (code={$q->customer_code})");

    // Map sản phẩm → cấu trúc 1 tab (product_id = erp_product_id)
    $products = $data['products']->map(function ($p) {
        $product = \App\Model\Warehouse\Product::find($p->erp_product_id); // xác nhận namespace Product ở Task 1.0
        return [
            'firm_quotation_tab_product_id' => null,
            'product_id' => $p->erp_product_id,
            'product_name' => $p->name,
            'code' => $p->code,
            'unit_id' => $product->unit_id ?? null,      // theo spike
            'quantity' => $p->quantity,
            'price' => $p->quoted_price,
            'vat_percent' => $p->vat_percent,
            'price_extra' => 0, 'price_discount' => 0,
        ];
    });

    return $this->responseSuccess([
        'hrm_quotation_id' => $q->id,
        'hrm_quotation_code' => $q->code,
        'customer' => $customer,
        'tabs' => [[
            'firm_quotation_tab_id' => null,
            'name' => 'Hàng hóa',
            'total_discount' => 0,
            'products' => $products,
        ]],
    ]);
}
```

> Namespace model `Customer`/`Product` xác nhận chính xác ở Task 1.0 (đọc `use` trong `FirmContractService`).

- [ ] **Step 2: Routes** (nhóm `admin/sale`, middleware như màn HĐ)

```php
Route::get('firm-contracts/hrm-quotations/searchData', 'Sale\Firm\HrmQuotationContractController@searchData')->name('firmContract.hrmQuotations.searchData');
Route::get('firm-contracts/hrm-quotations/{id}/getDataForContract', 'Sale\Firm\HrmQuotationContractController@getDataForContract')->name('firmContract.hrmQuotations.getDataForContract');
```

- [ ] **Step 3:** `php -l` 2 file → sạch. Test thủ công: gọi `searchData` (đã login) trả list; `getDataForContract/{id}` trả customer + tabs.

---

### Task 1.4: Nới FirmContractStoreRequest cho nguồn HRM

**Files:**
- Modify: `app/Http/Requests/Sale/Firm/Contract/FirmContractStoreRequest.php`

- [ ] **Step 1:** Đổi rule để nguồn HRM hợp lệ:

```php
$isHrm = !empty($this->input('hrm_quotation_id'));

'firm_quotation_id' => [$isHrm ? 'nullable' : 'required', 'nullable', 'exists:firm_quotations,id'],
'hrm_quotation_id'  => [$isHrm ? 'required' : 'nullable', 'integer'],
'tabs.*.firm_quotation_tab_id'         => [$isHrm ? 'nullable' : 'required', 'nullable', 'exists:firm_quotation_tabs,id'],
'tabs.*.products.*.firm_quotation_tab_product_id' => [$isHrm ? 'nullable' : 'required', 'nullable', 'exists:firm_quotation_tab_products,id'],
```

(Giữ nguyên `tabs.*.products.*.product_id => required|exists:products,id` — nguồn HRM vẫn product thật.)

- [ ] **Step 2:** `php -l` → sạch.

---

### Task 1.5: Fork FirmContractService cho nguồn HRM

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/FirmContractController.php:142-253` (`store`)
- Modify: `app/Services/Sale/Firm/Contract/FirmContractService.php` (`store`, `saveFirmContractData`, `syncTabsFromQuotation`)

- [ ] **Step 1: Controller store()** — resolve nguồn:

Thay đoạn lấy `$quotation`:
```php
$hrmQuotationId = $request->input('hrm_quotation_id');
if ($hrmQuotationId) {
    $quotation = null; // nguồn HRM — không có firm_quotation
} else {
    $quotation = FirmQuotation::query()->where('id', $storeValues['firm_quotation_id'])->firstOrFail();
    if (!$quotation->canCreateContract()) {
        return $this->responseErrors('Báo giá đã chọn không hợp lệ');
    }
}
$firm_contract = $firmContractService->store($storeValues, $quotation);
```
Thêm `'hrm_quotation_id'` vào mảng `$request->only([...])`.

- [ ] **Step 2: Service `saveFirmContractData($contract, $data, $quotation, ...)`** — guard mọi chỗ dùng `$quotation` khi null (theo spike Task 1.0):
  - `$contract->total_cost = $quotation ? $quotation->delivery_cost : 0;` (và `delivery_cost`, `delivery_vat_percent` tương tự, default 0).
  - Bỏ qua block notification giữ nguyên.
  - Cuối hàm: thay `$quotation->status = DA_LAP_HD; $quotation->save();` bằng:
    ```php
    if ($quotation) {
        $quotation->status = FirmQuotation::DA_LAP_HD;
        $quotation->save();
    } else {
        // nguồn HRM: lưu liên kết + ghi ngược HRM (Task 1.6)
        $contract->hrm_quotation_id = $data['hrm_quotation_id'];
        $contract->save();
        app(\App\Services\Hrm\HrmQuotationWriteback::class)->markContractCreated($data['hrm_quotation_id'], $contract->id);
    }
    ```

- [ ] **Step 3: Fork `syncTabsFromQuotation($tabs, $contract)`** — khi `firm_quotation_tab_id` null, build `$t_attributes`/`$p_attributes` từ data POST thay vì từ record `FirmQuotationTab`/`FirmQuotationTabProduct`. Theo bảng ánh xạ ở spike Task 1.0:
  - Tab: `name` từ `$tab['name']`, `total_cost` = Σ(quantity*price), `firm_quotation_tab_id=null`.
  - Product: `product_name/code/unit_id/quantity/price/vat_percent` từ `$product` POST; `product_id` = `$product['product_id']`; lấy `unit_name/unit_coefficient/model/brand/origin/product_attributes` từ `Product::find($product['product_id'])`; `sale_max_percent`, `price_type_coefficient`, `product_type_coefficient`, `net_price`, `standard_price` tính y hệt nhánh hiện có (dòng ~690-707).
  - Giữ nguyên toàn bộ phép tính tổng (`total_product_cost`, `total_product_vat`...) để số tiền HĐ đúng.

> Đây là task rủi ro nhất. Implement bám sát code gốc `syncTabsFromQuotation` (Task 1.0 đã liệt kê field). Test bằng Task 1.7.

- [ ] **Step 4:** `php -l` các file → sạch.

---

### Task 1.6: Ghi ngược HRM (chống trùng)

**Files:**
- Create: `app/Services/Hrm/HrmQuotationWriteback.php`
- Phụ thuộc: migration HRM `quotations.erp_firm_contract_id` (làm ở repo HRM — xem cặp HRM Task H1)

- [ ] **Step 1: Service ghi ngược**

```php
<?php
namespace App\Services\Hrm;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class HrmQuotationWriteback
{
    public function markContractCreated($hrmQuotationId, $erpContractId): void
    {
        try {
            DB::connection('hrm')->table('quotations')
                ->where('id', $hrmQuotationId)
                ->update(['erp_firm_contract_id' => $erpContractId, 'updated_at' => now()]);
        } catch (\Throwable $e) {
            Log::error("Writeback erp_firm_contract_id thất bại: hrm_quotation={$hrmQuotationId}, contract={$erpContractId} — " . $e->getMessage());
        }
    }
}
```

> Ghi ngược lỗi không rollback HĐ (HĐ đã commit) — chỉ log để xử lý tay. Cân nhắc retry sau (ngoài phạm vi).

---

### Task 1.7: Test BE (luồng tạo HĐ từ HRM)

- [ ] **Step 1:** Tinker/HTTP: POST `admin/sale/firm-contracts` với `hrm_quotation_id` + tabs (1 tab, product_id thật, quantity/price/vat) + đủ field chỉ-ERP hợp lệ → tạo HĐ thành công, `hrm_quotation_id` set, `firm_quotation_id` null, tổng tiền đúng (đối chiếu Σ quantity*price + VAT).
- [ ] **Step 2:** Kiểm tra `quotations.erp_firm_contract_id` (DB HRM) được set.
- [ ] **Step 3:** Báo giá đó gọi lại `getDataForContract` → trả lỗi "không đủ điều kiện" (đã có HĐ).

---

## PHASE 2 — ERP Frontend (màn tạo hợp đồng)

> Phụ thuộc Phase 1. File: `resources/views/sale/firm/contracts/form.blade.php` + `formJs.blade.php` (popup `chooseQuotationModal`, `addQuotationParent`, `form.selectQuotation`).

### Task 2.1: Thêm nguồn "Báo giá HRM" vào popup chọn báo giá
- [ ] Thêm nút/tab "Báo giá HRM" cạnh "chọn báo giá" → mở `BaseSearchModal` thứ 2 dùng `firmContract.hrmQuotations.searchData` (cột: số BG, khách hàng, ngày).
- [ ] Callback chọn → GET `firmContract.hrmQuotations.getDataForContract/{id}` → `form.selectQuotation(data)` (tái dùng), set `form.hrm_quotation_id`, ẩn nút chọn firm_quotation thường (1 nguồn/HĐ).
- [ ] Đảm bảo payload lưu gửi kèm `hrm_quotation_id` (xác nhận `form` có field này).

### Task 2.2: Deep-link `?hrm_quotation_id=`
- [ ] `FirmContractController::create()` đọc `?hrm_quotation_id`, truyền vào blade; JS auto gọi `getDataForContract` + prefill khi load.

### Task 2.3: Verify FE
- [ ] Popup "Báo giá HRM" hiện list đúng; chọn → prefill KH + SP; lưu → HĐ tạo; deep-link tự prefill.

---

## PHASE 3 — HRM (repo HRM, xem `HRM/.plans/hrm-quotation-to-erp-contract/plan.md`)

### Task H1: Migration HRM `quotations.erp_firm_contract_id` (nullable)
### Task H2: Resource báo giá trả `erp_firm_contract_id` + cờ đủ điều kiện (status=7 + synced + VND)
### Task H3: FE nút "Lập hợp đồng ERP" → deep-link `{ERP_BASE}/admin/sale/firm-contracts/create?hrm_quotation_id={id}`; ẩn khi đã có `erp_firm_contract_id`
### Task H4: Verify nút hiện/ẩn đúng + deep-link mở ERP

---

## Self-Review

- **Spec coverage:** điều kiện đủ (7+synced+VND+chưa HĐ) → Task 1.2 eligibleQuery; resolve KH → 1.3; schema → 1.1; nới request → 1.4; fork service + 1 tab + không set DA_LAP_HD → 1.5; ghi ngược chống trùng → 1.6 (+H1); popup + prefill + deep-link → 2.x; nút HRM → H3. Đủ.
- **Placeholder scan:** Các điểm "theo spike" trỏ về Task 1.0 (điều tra có chủ đích, không phải TODO yêu cầu). Tên cột SL/namespace model phải chốt ở Task 1.0 trước khi code 1.3/1.5.
- **Type consistency:** `hrm_quotation_id` xuyên suốt (migration→fillable→request→controller→service→writeback→FE); route name `firmContract.hrmQuotations.*` nhất quán.

### Checkpoint — 2026-06-15 (PHASE 1 BE DONE)
Vừa hoàn thành: **Toàn bộ Phase 1 BE** (không commit git theo yêu cầu):
- 1.1 Migration ERP `firm_contracts.hrm_quotation_id` (đã chạy) + fillable. Migration HRM `quotations.erp_firm_contract_id` (đã chạy, tiền đề).
- 1.2 `app/Services/Hrm/HrmQuotationReader.php` (eligibleQuery + getForContract; VND resolve từ currencies ERP, lọc qua connection hrm).
- 1.3 `app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php` (searchData + getDataForContract, resolve KH theo code→tax_code) + 2 route (đặt trước `/{id}`, đã verify route:list).
- 1.4 `FirmContractStoreRequest`: nới `firm_quotation_id` + `tabs.*.firm_quotation_tab_id` + `..._tab_product_id` khi có `hrm_quotation_id`; thêm rule `hrm_quotation_id`.
- 1.5 `FirmContractController::store` rẽ nhánh nguồn HRM ($quotation=null, validate qua reader). `FirmContractService`: guard `$quotation` null (delivery 0, không set DA_LAP_HD), `syncDataFromQuotation` rẽ nhánh, method MỚI `syncTabsFromHrm` (build tab/product từ POST, mirror pricing, unit_id HRM=ERP).
- 1.6 `app/Services/Hrm/HrmQuotationWriteback.php` (ghi ngược erp_firm_contract_id, log nếu lỗi).
- Lint: tất cả `php -l` sạch. Route đăng ký OK. Smoke-test reader: SQL well-formed, VND lookup OK; chỉ timeout mạng tới DB HRM (môi trường này không tới host HRM — chạy được trên dev thật).
Đang làm dở: chưa test E2E (cần môi trường ERP với tới HRM + data thật).
Bước tiếp theo: **user test E2E**.
Blocked: E2E phụ thuộc môi trường + data.

### Checkpoint — 2026-06-15 (PHASE 2 + 3 DONE — toàn bộ feature code xong)
**Phase 2 (ERP FE)** — không commit:
- `form.blade.php`: vùng chọn báo giá thêm nút "Thêm báo giá HRM" + chip "[HRM] <code>" + ẩn nút khi đã chọn 1 nguồn.
- `formJs.blade.php`: `chooseHrmQuotationModal` (DataTable từ `firmContract.hrmQuotations.searchData`) + `addHrmQuotation(id)` (gọi getDataForContract, `form.selectHrmQuotation`) + deep-link `@if($hrm_quotation_id)` auto-nạp.
- `FirmContract.blade.php` (class JS): method `selectHrmQuotation(data)` (prefill KH+SP, không set firm_quotation_id; removeQuotation→reset() đã xóa hrm) + `submit_data` thêm `hrm_quotation_id`.
- `FirmContractController::create`: truyền `$hrm_quotation_id` (deep-link).
- `HrmQuotationContractController::getDataForContract`: enrich (load customer deputies/vehicle_manufacts/parent; product unit_name/sale_max_percent/allocated_price; trả customer_* + costs/revenue_costs rỗng).

**Phase 3 (HRM)** — không commit:
- `QuotationController::byProject`: thêm `buildContractSummary($projectId)` → `contract` trong response (quotation_code, erp_firm_contract_id, is_vnd, can_create_contract, erp_contract_url=config('app.erp_url')+/admin/sale/firm-contracts/create?hrm_quotation_id=). Điều kiện: status=7 + mọi dòng có erp_product_id + VND + chưa có erp_firm_contract_id.
- `ProspectiveProjectQuotationsTab.vue`: banner "Lập hợp đồng ERP" (nút deep-link target _blank khi can_create_contract; badge "Đã lập HĐ ERP" / "ngoại tệ" / "chờ đồng bộ") + data `contract` + gán `res.contract`.

Lint: TẤT CẢ `php -l` sạch (7 file ERP + 1 file HRM). Vue/Blade chưa build (cần dev server).

### Checkpoint — 2026-06-15 (REFACTOR: DB-direct → API)
Theo yêu cầu user, chuyển toàn bộ truy cập dữ liệu HRM từ **đọc DB connection `hrm`** sang **gọi API HTTP** (tạm KHÔNG auth — bổ sung sau):
- **HRM**: 3 endpoint mới (public, ngoài group `auth:api`) trong `Modules/Assign/Routes/api.php` + 3 method `QuotationController`: `erpEligible` (list đủ điều kiện), `erpContractData` (chi tiết KH snapshot + sản phẩm), `erpMarkContract` (ghi `erp_firm_contract_id`). Eligibility (status=7 + mọi dòng có erp_product_id + VND + chưa lập HĐ) + lọc VND qua `TpCurrency` (mysql2).
- **ERP**: thêm `config/services.php` → `hrm.base_url` (env `HRM_API_BASE_URL`). Service mới `app/Services/Hrm/HrmApiService.php` (Http client: eligible/contractData/markContractCreated). **XÓA** `HrmQuotationReader.php` + `HrmQuotationWriteback.php` (DB-based). `HrmQuotationContractController` + `FirmContractController::store` + `FirmContractService` writeback đổi sang `HrmApiService`. Resolve KH/đơn vị/sản phẩm vẫn ở ERP (theo code/erp_product_id trong payload API).
- Lint tất cả sạch; route `hrm-quotations` ERP vẫn OK; không còn ref class đã xóa.
- **Config cần set khi test:** `HRM_API_BASE_URL` (ERP .env) trỏ tới base API HRM (vd `https://hrm.eteksofts.com`); `ERP_URL` (HRM .env) trỏ web ERP cho deep-link.

### Checkpoint — 2026-06-16 (BUGFIX: popup trống — ERP là Laravel 6)
ERP = **Laravel 6.20.44** (CLAUDE.md ghi 8 là SAI) → facade `Http` (Laravel 7+) không tồn tại → `HrmApiService` ném "Class not found" → catch → trả rỗng → popup "Báo giá HRM" trống. **Fix:** viết lại `HrmApiService` dùng **Guzzle** (`GuzzleHttp\Client`, có sẵn). Verify: eligible(eii=30)→BG-44, eligible(eii=999)→rỗng, contractData(44,30)→6 SP. (Memory: [[erp-is-laravel-6]].)

### Checkpoint — 2026-06-16 (SCOPE: chỉ người tạo báo giá mới lập được HĐ)
Logic đúng của firm-contracts = **người tạo báo giá** mới lập HĐ (không phải quyền). Áp cho nguồn HRM: ERP↔HRM map qua **`employee_info_id`** (HRM `quotations.created_by`=employee id; `employees.employee_info_id` chung; ERP `employees.employee_info_id`).
- **HRM** `erpEligibleQuery($employeeInfoId)`: lọc `created_by IN (employees where employee_info_id=?)`. `erpEligible`/`erpContractData` nhận `employee_info_id` từ request. `buildContractSummary`: banner chỉ hiện khi `created_by == auth()->id()` (người tạo).
- **ERP** `HrmApiService::eligible/contractData(...$employeeInfoId)`: gửi `employee_info_id`. `HrmQuotationContractController` (searchData/getDataForContract) + `FirmContractController::store`: dùng `auth()->user()->employee_info_id`.
- Verify: eligible(eii=30)→BG-44; eligible(eii=999)→rỗng. Lint sạch cả 2 repo.
- **Test fixture:** BG-2026-00044 (dev) đã eligible (sửa currency→VNĐ); người tạo = Khúc Ngọc Nghĩa (employee_info_id=30) → ERP account `Nghiakn.kd2@tanphat.com` (ERP emp 41) là người lập được HĐ từ BG-44.

### Checkpoint — 2026-06-16 (ENHANCE: nhóm HRM → tab HĐ)
Trước đây gom hết SP vào 1 tab "Hàng hóa". Sửa để **mỗi nhóm báo giá HRM (`quotation_groups`) = 1 tab HĐ ERP**:
- **HRM** `QuotationController::erpContractData`: trả thêm `quotation_group_id` mỗi SP + `groups` (id, name, sort_order).
- **ERP** `HrmQuotationContractController::getDataForContract`: gom SP theo `quotation_group_id` → N tab (name=tên nhóm, theo sort_order); SP không nhóm → tab "Hàng hóa". (so khớp loose để int/string JSON đều đúng).
- `syncTabsFromHrm` (BE) + form đa-tab (FE) KHÔNG sửa — đã hỗ trợ N tab sẵn.
- `php -l` 2 file sạch.

**TODO user test E2E:**
0. Báo giá HRM có nhiều nhóm → mỗi nhóm thành 1 tab riêng bên HĐ ERP (tên tab = tên nhóm); SP không nhóm vào tab "Hàng hóa".
1. ERP: mở Lập hợp đồng → nút "Thêm báo giá HRM" → chọn → form prefill KH+SP → nhập người ký/template/lịch TT → Lưu → HĐ tạo (hrm_quotation_id set, firm_quotation_id null, tổng tiền đúng).
2. Ghi ngược HRM `quotations.erp_firm_contract_id`; báo giá biến mất khỏi popup + nút HRM đổi "Đã lập HĐ ERP".
3. HRM: tab Báo giá dự án → banner "Lập hợp đồng ERP" → nút mở ERP deep-link prefill đúng.
4. Báo giá ngoại tệ / chưa sync hết → không lập được.

### Checkpoint — 2026-06-16 (FIX: sửa HĐ HRM bấm lưu báo "bắt buộc báo giá")
- **Triệu chứng:** Mở HĐ nguồn HRM (id=1131 trên dev_erp_2, `firm_quotation_id=null`, `hrm_quotation_id=44`) → Sửa → Lưu → lỗi đòi báo giá.
- **Root cause:** `FirmContractController::update()` (khác `store()`) chưa có nhánh HRM: (a) `$request->only([...])` thiếu `'hrm_quotation_id'` → bị strip; (b) gọi `FirmQuotation::firstOrFail()` vô điều kiện → `firm_quotation_id=null` → `ModelNotFoundException`.
- **Fix:** thêm `'hrm_quotation_id'` vào `$request->only` của update(); branch `if ($request->input('hrm_quotation_id')) $quotation=null; else firstOrFail()`. Không re-validate eligibility (báo giá đã gắn chính HĐ này). `FirmContractService::update`→`saveFirmContractData` (line 578-581) lưu lại `hrm_quotation_id`. `php -l` sạch.
- **Lưu ý môi trường:** HĐ 1130 (từng verify) ở DB **production**; trên dev_erp_2 HĐ HRM là **1131**. Tinker & web đều đang ở dev_erp_2.
- **TODO user:** mở `/admin/sale/firm-contracts/1131/edit` → Lưu → không còn lỗi; `hrm_quotation_id` vẫn =44 sau lưu.

### Checkpoint — 2026-06-16 (FIX bổ sung: FormRequest update chưa nới HRM)
- Sửa controller update() chưa đủ — **FormRequest `FirmContractUpdateRequest` chạy validate TRƯỚC** vẫn require `firm_quotation_id` → trả `{firm_quotation_id: ["Bắt buộc phải nhập"]}` khi sửa HĐ HRM.
- **Fix:** copy pattern HRM từ `FirmContractStoreRequest` sang `FirmContractUpdateRequest`: thêm `$isHrm = !empty(hrm_quotation_id)`; `firm_quotation_id` + `tabs.*.firm_quotation_tab_id` + `tabs.*.products.*.firm_quotation_tab_product_id` → `$isHrm ? 'nullable' : 'required'`; thêm rule `hrm_quotation_id`.
- Chuỗi đủ: `getDataForEdit` trả `hrm_quotation_id` (qua `$contract->toArray()`) → edit.blade set `$scope.form.hrm_quotation_id` → `submit_data` gửi đi → `$isHrm=true` → qua FormRequest → controller branch `$quotation=null`. **KHÔNG cần chọn lại báo giá khi sửa.**
- `php -l` sạch.

### Checkpoint — 2026-06-16 (FIX: VAT prefill HRM phải theo product master ERP)
- **Triệu chứng:** Sửa HĐ HRM → tab Điều khoản thanh toán báo "Tổng số tiền thanh toán phải bằng tổng số tiền" (Số tiền=24,120,000 vs Số tiền thanh toán=23,800,000).
- **Root cause:** `FirmContractService::getDataForEdit` (hàm dùng chung, line 1296-1301) **luôn ép `vat_percent` mọi SP = VAT product master ERP** (quy ước ERP). Prefill HRM `getDataForContract` lấy VAT theo **báo giá HRM** (Con A2/Con B=0%) ≠ master (8%) → lưu 0% → lúc sửa getDataForEdit đổi thành 8% → FE tính lại total_after_vat=24,120,000 (vat 1,120,000) trong khi `_amount` lưu 23,800,000 → lệch → FormRequest fail `abs(totalAmount-totalPaymentAmount)>1`.
- **Fix:** `HrmQuotationContractController::getDataForContract` — `vat_percent` lấy từ `$product->vat_percent` (master ERP), fallback VAT báo giá HRM nếu không map được product. Verify: prefill(44) giờ trả vat_cost=1,120,000, total_after_vat=24,120,000 = đúng giá trị edit.
- **Hệ quả nghiệp vụ:** VAT HĐ ERP LUÔN theo product master, KHÔNG giữ VAT báo giá HRM (ERP design — sửa HĐ nào cũng reset về master). Nếu HRM ↔ master lệch VAT → phải đồng bộ VAT master ERP cho khớp.
- **Lưu ý 1131:** HĐ test cũ vẫn lưu VAT 0% → sửa vẫn lệch. Tạo HĐ mới từ BG-44 (đã eligible) để test sạch; 1131 bỏ/xoá.

### Checkpoint — 2026-06-16 (Chuẩn bị test luồng NÚT BẤM bên HRM)
- Điều kiện hiện nút (`buildContractSummary`): báo giá trúng thầu (status=7) + mọi SP có erp_product_id + VND + erp_firm_contract_id rỗng + **người login HRM = người tạo báo giá** (`created_by==auth id`).
- Fixture: BG-2026-00044 (project_id=**80**, created_by=**emp 41 = Nghiakn.kd2@tanphat.com**, info_id=30). Đã reset `erp_firm_contract_id=null` (trước đó bị HĐ 1132 chiếm). canCreate=TRUE khi login emp 41. SP synced 6/6.
- Config local đã đúng: ERP→HRM `services.hrm.base_url=http://127.0.0.1:8000`; HRM→ERP `ERP_URL=http://127.0.0.1:8001`. ERP emp41 info_id=30 khớp scope.
- Deep-link: `http://127.0.0.1:8001/admin/sale/firm-contracts/create?hrm_quotation_id=44`. `create()` đọc query → formJs auto `addHrmQuotation(44)`.
- **Cần login Nghiakn ở CẢ HRM (emp41) lẫn ERP (emp41/info_id 30)** thì prefill mới qua scope.
