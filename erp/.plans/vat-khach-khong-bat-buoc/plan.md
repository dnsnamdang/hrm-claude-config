# Khách "không bắt buộc VAT" ⇒ VAT 0% trên BG/HĐ hãng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khách thuộc nhóm có cờ `customer_groups.no_require_vat` ⇒ mọi % VAT trên Báo giá hãng + Hợp đồng hãng (ERP) = 0%, không nhảy lại khi mở sửa / lập HĐ; xuất hàng tự 0%.

**Architecture:** Một class tĩnh thuần `FirmVatExemption` (ép 0 trên mảng payload / mảng dữ liệu load) + `Customer::isNoRequireVat()`. BE là nguồn sự thật: controller web báo giá ép payload trước khi lưu; service HĐ giữ cờ `$noRequireVat` suốt 1 lần lưu; 3 hàm load dữ liệu cho FE chạy `zeroLoadedData`. FE báo giá chỉ đổi getter VAT dòng hàng + VAT chi phí/vận chuyển theo `form.no_require_vat`.

**Tech Stack:** Laravel 5.x / PHP 7.4, Blade + AngularJS 1.x class pattern (`BaseClass`, `initGetSet`), PHPUnit 8 (unit thuần, `PHPUnit\Framework\TestCase`).

**Spec:** `erp/docs/superpowers/specs/2026-09-24-vat-khach-khong-bat-buoc-design.md`

## Global Constraints

- Repo `D:\CompanyProject\hrm\TanPhatDev`, nhánh `master`. **KHÔNG commit / push** (rule CLAUDE.md — user tự commit).
- Không sửa `Common\SearchController@searchCustomer` và không đổi hành vi khách thường (mọi nhánh mới chỉ chạy khi có cờ).
- Không đụng `FirmQuotationService::saveDataApi` / `apiStore` / `apiUpdate` / nguồn `hrm_quotation_id` (đợt 2).
- Không `sed -i` hàng loạt / không script regex ghi đè file (memory) — sửa bằng Edit tool, giữ CRLF.
- Blade: biến Angular dùng `<% %>`.
- Chạy test: `php vendor/phpunit/phpunit/phpunit tests/Unit/FirmVatExemptionTest.php`.

## Review Focus

1. Khách thuộc 2 nhóm (1 có cờ, 1 không) → vẫn ép 0 (accessor duyệt mọi nhóm) — test ở Task 1 qua `isNoRequireVat` gọi thật trên DB local (Task 5 bước DB).
2. BG cũ đã lưu VAT 8/10% của khách có cờ, mở sửa rồi lưu → DB về 0 hết (tab product, group, cost, delivery) — Task 5 kịch bản 2.
3. Đổi khách có cờ ↔ khách thường trên cùng form BG → VAT dòng hàng/chi phí/vận chuyển trả đúng — Task 4 bước kiểm + Task 5 kịch bản 4.
4. Payload giả VAT 10% cho khách có cờ → BE vẫn lưu 0 — Task 1 unit test + Task 5 kịch bản 5.
5. HĐ lập từ BG có cờ: tổng HĐ `total_vat = 0`, `total_after_vat = total_before_vat`, `delivery_vat = 0` — Task 5 kịch bản 3.

---

### Task 1: Helper `FirmVatExemption` + `Customer::isNoRequireVat`

**Files:**
- Create: `app/Services/Sale/Firm/FirmVatExemption.php`
- Modify: `app/Model/Sale/Customer.php` (sau `getNoRequireVatAttribute`, ~dòng 1775)
- Test: `tests/Unit/FirmVatExemptionTest.php`

**Interfaces:**
- Produces:
  - `FirmVatExemption::zeroQuotationPayload(array $data): array`
  - `FirmVatExemption::zeroLoadedData(array $result): array` (thêm `no_require_vat => true`)
  - `Customer::isNoRequireVat($customerId): bool`

- [ ] **Step 1: Viết test (fail)** — `tests/Unit/FirmVatExemptionTest.php`

```php
<?php

namespace Tests\Unit;

use App\Services\Sale\Firm\FirmVatExemption;
use PHPUnit\Framework\TestCase;

class FirmVatExemptionTest extends TestCase
{
    private function payload(): array
    {
        return [
            'delivery_cost' => 100000, 'delivery_vat_percent' => 8, 'delivery_vat' => 8000,
            'total_product_cost' => 1000000, 'total_product_vat' => 100000, 'total_product_after_vat' => 1100000,
            'total_revenue_cost' => 200000, 'total_revenue_vat' => 16000, 'total_revenue_after_vat' => 216000,
            'total_other_cost' => 50000, 'total_other_vat' => 4000, 'total_other_after_vat' => 54000,
            'total_cost' => 1350000, 'total_vat' => 128000, 'total_after_vat' => 1478000,
            'tabs' => [[
                'total_cost' => 1000000, 'vat_cost' => 100000, 'cost_after_vat' => 1100000,
                'products' => [['quantity' => 2, 'price' => 500000, 'vat_percent' => 10, 'total_cost_after_vat' => 1100000]],
            ]],
            'groups' => [[
                'total_cost' => 1000000, 'vat_percent' => 10,
                'products' => [['quantity' => 2, 'price' => 500000, 'vat_percent' => 10]],
            ]],
            'costs' => [['cost_id' => 1, 'price' => 50000, 'vat_percent' => 8]],
            'revenue_costs' => [['cost_id' => 2, 'price' => 200000, 'vat_percent' => 8]],
        ];
    }

    public function test_payload_moi_vat_ve_0_va_tong_sau_vat_bang_truoc_vat()
    {
        $d = FirmVatExemption::zeroQuotationPayload($this->payload());

        $this->assertSame(0, $d['delivery_vat_percent']);
        $this->assertSame(0, $d['delivery_vat']);
        $this->assertSame(0, $d['total_product_vat']);
        $this->assertSame(1000000, $d['total_product_after_vat']);
        $this->assertSame(0, $d['total_revenue_vat']);
        $this->assertSame(200000, $d['total_revenue_after_vat']);
        $this->assertSame(0, $d['total_other_vat']);
        $this->assertSame(50000, $d['total_other_after_vat']);
        $this->assertSame(0, $d['total_vat']);
        $this->assertSame(1350000, $d['total_after_vat']);

        $this->assertSame(0, $d['tabs'][0]['vat_cost']);
        $this->assertSame(1000000, $d['tabs'][0]['cost_after_vat']);
        $this->assertSame(0, $d['tabs'][0]['products'][0]['vat_percent']);
        $this->assertSame(1000000, $d['tabs'][0]['products'][0]['total_cost_after_vat']);
        $this->assertSame(0, $d['groups'][0]['vat_percent']);
        $this->assertSame(0, $d['groups'][0]['products'][0]['vat_percent']);
        $this->assertSame(0, $d['costs'][0]['vat_percent']);
        $this->assertSame(0, $d['revenue_costs'][0]['vat_percent']);
    }

    public function test_payload_thieu_khoa_khong_loi()
    {
        $d = FirmVatExemption::zeroQuotationPayload(['tabs' => null, 'groups' => null]);
        $this->assertSame(0, $d['delivery_vat_percent']);
        $this->assertNull($d['tabs']);
    }

    public function test_zero_loaded_data()
    {
        $r = FirmVatExemption::zeroLoadedData([
            'delivery_vat_percent' => 8,
            'tabs' => [['vat_percent' => 10, 'vat_cost' => 5, 'products' => [['vat_percent' => 10]]]],
            'groups' => [['vat_percent' => 10, 'vat_cost' => 5, 'products' => [['vat_percent' => 10]]]],
            'costs' => [['vat_percent' => 8, 'vat_cost' => 4]],
            'revenue_costs' => [['vat_percent' => 8, 'vat_cost' => 4]],
        ]);
        $this->assertTrue($r['no_require_vat']);
        $this->assertSame(0, $r['delivery_vat_percent']);
        $this->assertSame(0, $r['tabs'][0]['vat_percent']);
        $this->assertSame(0, $r['tabs'][0]['vat_cost']);
        $this->assertSame(0, $r['tabs'][0]['products'][0]['vat_percent']);
        $this->assertSame(0, $r['groups'][0]['vat_percent']);
        $this->assertSame(0, $r['groups'][0]['products'][0]['vat_percent']);
        $this->assertSame(0, $r['costs'][0]['vat_percent']);
        $this->assertSame(0, $r['costs'][0]['vat_cost']);
        $this->assertSame(0, $r['revenue_costs'][0]['vat_percent']);
    }
}
```

- [ ] **Step 2: Chạy test → FAIL** (`Class ... FirmVatExemption not found`)

Run: `php vendor/phpunit/phpunit/phpunit tests/Unit/FirmVatExemptionTest.php`

- [ ] **Step 3: Viết `app/Services/Sale/Firm/FirmVatExemption.php`**

```php
<?php

namespace App\Services\Sale\Firm;

/**
 * Khách thuộc nhóm "Khách không bắt buộc VAT" (customer_groups.no_require_vat):
 * mọi % VAT trên báo giá / hợp đồng hãng = 0%.
 * Hàm thuần trên mảng — không đụng DB.
 */
class FirmVatExemption
{
    /**
     * Payload lưu báo giá hãng (tabs/groups đã json_decode ở FormRequest).
     */
    public static function zeroQuotationPayload(array $data): array
    {
        $data['delivery_vat_percent'] = 0;
        $data['delivery_vat'] = 0;
        foreach (['total_product', 'total_revenue', 'total_other'] as $prefix) {
            $data["{$prefix}_vat"] = 0;
            $data["{$prefix}_after_vat"] = $data["{$prefix}_cost"] ?? 0;
        }
        $data['total_vat'] = 0;
        $data['total_after_vat'] = $data['total_cost'] ?? 0;

        if (!empty($data['tabs']) && is_array($data['tabs'])) {
            foreach ($data['tabs'] as &$tab) {
                if (array_key_exists('vat_percent', $tab)) $tab['vat_percent'] = 0;
                $tab['vat_cost'] = 0;
                $tab['cost_after_vat'] = $tab['total_cost'] ?? 0;
                foreach (['products', 'option_products'] as $key) {
                    if (empty($tab[$key]) || !is_array($tab[$key])) continue;
                    foreach ($tab[$key] as &$product) {
                        $product['vat_percent'] = 0;
                        if (array_key_exists('total_cost_after_vat', $product)) {
                            $product['total_cost_after_vat'] = ($product['quantity'] ?? 0) * ($product['price'] ?? 0);
                        }
                    }
                    unset($product);
                }
            }
            unset($tab);
        }

        if (!empty($data['groups']) && is_array($data['groups'])) {
            foreach ($data['groups'] as &$group) {
                $group['vat_percent'] = 0;
                foreach ($group['products'] ?? [] as $i => $product) {
                    $group['products'][$i]['vat_percent'] = 0;
                }
            }
            unset($group);
        }

        foreach (['costs', 'revenue_costs'] as $key) {
            if (empty($data[$key]) || !is_array($data[$key])) continue;
            foreach ($data[$key] as $i => $cost) {
                $data[$key][$i]['vat_percent'] = 0;
            }
        }

        return $data;
    }

    /**
     * Mảng dữ liệu trả FE khi mở sửa / lập HĐ (toArray của BG hoặc HĐ hãng).
     */
    public static function zeroLoadedData(array $result): array
    {
        $result['no_require_vat'] = true;
        $result['delivery_vat_percent'] = 0;
        if (array_key_exists('delivery_vat', $result)) $result['delivery_vat'] = 0;

        foreach (['tabs', 'groups'] as $key) {
            if (empty($result[$key]) || !is_array($result[$key])) continue;
            foreach ($result[$key] as $i => $row) {
                $result[$key][$i]['vat_percent'] = 0;
                if (array_key_exists('vat_cost', $row)) $result[$key][$i]['vat_cost'] = 0;
                foreach ($row['products'] ?? [] as $j => $product) {
                    $result[$key][$i]['products'][$j]['vat_percent'] = 0;
                }
            }
        }

        foreach (['costs', 'revenue_costs'] as $key) {
            if (empty($result[$key]) || !is_array($result[$key])) continue;
            foreach ($result[$key] as $i => $cost) {
                $result[$key][$i]['vat_percent'] = 0;
                if (array_key_exists('vat_cost', $cost)) $result[$key][$i]['vat_cost'] = 0;
            }
        }

        return $result;
    }
}
```

- [ ] **Step 4: Chạy test → PASS (3 tests)**

- [ ] **Step 5: Thêm `Customer::isNoRequireVat`** vào `app/Model/Sale/Customer.php` ngay sau `getNoRequireVatAttribute()`:

```php
    /**
     * Khách thuộc ít nhất 1 nhóm có tích "Khách không bắt buộc VAT".
     */
    public static function isNoRequireVat($customerId): bool
    {
        if (!$customerId) return false;
        $customer = self::query()->find($customerId);
        return $customer ? (bool) $customer->no_require_vat : false;
    }
```

- [ ] **Step 6:** `php -l app/Model/Sale/Customer.php app/Services/Sale/Firm/FirmVatExemption.php` → No syntax errors.

---

### Task 2: BE Báo giá hãng — ép khi lưu, ép khi load, route `customerVatInfo`

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/FirmQuotationController.php` — `store()` (~dòng 185, trước `$firmQuotationService->store($data)`), `update()` (~dòng 329, trước `->update(...)`), thêm method `customerVatInfo`
- Modify: `app/Services/Sale/Firm/Quotation/FirmQuotationService.php` — cuối `getDataForEdit()` (~dòng 652, trước `return $result;`), cuối `getDataForContract()` (trước `return $result;`)
- Modify: `routes/web.php` (~dòng 3814, nhóm `firmQuotation`)

**Interfaces:**
- Consumes: `FirmVatExemption::zeroQuotationPayload`, `::zeroLoadedData`, `Customer::isNoRequireVat`
- Produces: route `firmQuotation.customerVatInfo` (GET, `customer_id`) → `{success, data: {no_require_vat: bool}}`; dữ liệu edit/contract có `no_require_vat: true` khi khách có cờ.

- [ ] **Step 1:** Thêm `use App\Services\Sale\Firm\FirmVatExemption;` vào đầu cả controller và service.

- [ ] **Step 2:** Trong `FirmQuotationController::store()` và `::update()`, ngay trước `try {` (sau khối `$data = $request->only([...]);`):

```php
        // Khách thuộc nhóm "không bắt buộc VAT" ⇒ mọi VAT = 0% (không tin FE)
        if (Customer::isNoRequireVat($data['customer_id'] ?? null)) {
            $data = FirmVatExemption::zeroQuotationPayload($data);
        }
```

KHÔNG thêm vào `apiStore` / `apiUpdate` (đợt 2).

- [ ] **Step 3:** Cuối `FirmQuotationService::getDataForEdit()` và `::getDataForContract()`, ngay trước `return $result;`:

```php
        if (Customer::isNoRequireVat($result['customer_id'] ?? null)) {
            $result = FirmVatExemption::zeroLoadedData($result);
        }
```

- [ ] **Step 4:** Method mới trong controller (đặt sau `getDataForContract`):

```php
    /**
     * Khách có thuộc nhóm "Khách không bắt buộc VAT" không — FE báo giá hãng dùng khi chọn khách.
     */
    public function customerVatInfo(Request $request): JsonResponse
    {
        return $this->responseSuccess([
            'no_require_vat' => Customer::isNoRequireVat($request->customer_id),
        ]);
    }
```

- [ ] **Step 5:** Route — thêm ngay sau dòng `searchData` của nhóm firmQuotation (~3814), TRƯỚC các route `/{id}/...`:

```php
            Route::get('/customerVatInfo', 'Sale\Firm\FirmQuotationController@customerVatInfo')->name('firmQuotation.customerVatInfo');
```

- [ ] **Step 6:** `php -l` 2 file PHP + `php artisan route:list --name=firmQuotation.customerVatInfo` → có 1 dòng.

---

### Task 3: BE Hợp đồng hãng — cờ `$noRequireVat` khi lưu + ép khi load

**Files:**
- Modify: `app/Services/Sale/Firm/Contract/FirmContractService.php`
  - thuộc tính mới đầu class
  - `saveFirmContractData()` (~424): tính cờ trước `$contract->fill($data)`; dòng `delivery_vat_percent` (~466)
  - `syncTabsFromQuotation()` (~797 `vat_cost/total_after_vat` tab; ~826 `vat_percent` dòng hàng)
  - `syncGroupsFromQuotation()` (~918 trước tính `vat_cost`)
  - `syncCostsFromQuotation()` (~1000 trước tính `vat_cost`)
  - `getDataForEdit()` (~1388, trước `return $result;`)

**Interfaces:**
- Consumes: `Customer::isNoRequireVat`, `FirmVatExemption::zeroLoadedData`

- [ ] **Step 1:** `use App\Services\Sale\Firm\FirmVatExemption;` + thuộc tính ngay sau `class FirmContractService {`:

```php
    /** Khách thuộc nhóm "không bắt buộc VAT" ⇒ mọi VAT HĐ = 0% (set trong saveFirmContractData) */
    private $noRequireVat = false;
```

- [ ] **Step 2:** Đầu `saveFirmContractData()`, trước `$contract->fill($data);`:

```php
        // Nguồn HRM (hrm_quotation_id) để đợt 2 — không ép ở đây.
        $this->noRequireVat = empty($data['hrm_quotation_id'])
            && Customer::isNoRequireVat($data['customer_id'] ?? $contract->customer_id);
        if ($this->noRequireVat) {
            $data['vat_extra_cost_percent'] = 0;
            $data['vat_extra_cost'] = 0;
        }
```

- [ ] **Step 3:** Dòng ~466 đổi thành:

```php
        $contract->delivery_vat_percent = $this->noRequireVat ? 0 : ($quotation ? $quotation->delivery_vat_percent : 0);
```

- [ ] **Step 4:** `syncTabsFromQuotation()` — ngay sau `$t_attributes['total_after_vat'] = $tab['total_after_vat'];`:

```php
            if ($this->noRequireVat) {
                $t_attributes['vat_percent'] = 0;
                $t_attributes['vat_cost'] = 0;
                $t_attributes['total_after_vat'] = $t_attributes['total_before_vat'];
            }
```

và dòng `$p_attributes['vat_percent'] = $product['vat_percent'] ?? 0;` đổi thành:

```php
                $p_attributes['vat_percent'] = $this->noRequireVat ? 0 : ($product['vat_percent'] ?? 0);
```

- [ ] **Step 5:** `syncGroupsFromQuotation()` — ngay trước `$group['vat_cost'] = round(...)`:

```php
            if ($this->noRequireVat) {
                $group['vat_percent'] = 0;
                foreach ($products as $k => $gp) {
                    $products[$k]['vat_percent'] = 0;
                }
            }
```

- [ ] **Step 6:** `syncCostsFromQuotation()` — ngay trước `$c_attributes['vat_cost'] = round(...)`:

```php
            if ($this->noRequireVat) {
                $c_attributes['vat_percent'] = 0;
            }
```

- [ ] **Step 7:** Cuối `getDataForEdit()` trước `return $result;`:

```php
        if (Customer::isNoRequireVat($result['customer_id'] ?? null)) {
            $result = FirmVatExemption::zeroLoadedData($result);
        }
```

- [ ] **Step 8:** `php -l app/Services/Sale/Firm/Contract/FirmContractService.php` → sạch.

---

### Task 4: FE Báo giá hãng + thông báo trên HĐ

**Files:**
- Modify: `resources/views/partials/classes/sale/firm/quotation/FirmQuotationTabProduct.blade.php:87-90` (getter `vat_percent`)
- Modify: `resources/views/partials/classes/sale/firm/quotation/FirmQuotationCost.blade.php:26-32` (`set cost_id`)
- Modify: `resources/views/partials/classes/sale/firm/quotation/FirmQuotation.blade.php:45-46` (`after`) + method mới `applyCustomerVat`
- Modify: `resources/views/sale/firm/quotations/formJs.blade.php:234-239` (`setCustomer`)
- Modify: `resources/views/sale/firm/quotations/form.blade.php:~258` (dòng thông báo dưới "Chi tiết")
- Modify: `resources/views/sale/firm/contracts/form.blade.php:~391` (dòng thông báo dưới "Thông tin hàng hóa")

**Interfaces:**
- Consumes: route `firmQuotation.customerVatInfo`; field `no_require_vat` trong dữ liệu load (Task 2/3)
- Produces: `FirmQuotation.applyCustomerVat(flag)`

- [ ] **Step 1:** `FirmQuotationTabProduct` — getter:

```js
        get vat_percent()
        {
            // Khách thuộc nhóm "không bắt buộc VAT" ⇒ 0% (giữ nguyên _vat_percent để đổi khách thì trả lại)
            if (this.parent && this.parent.parent && this.parent.parent.no_require_vat) return 0;
            return this._vat_percent || 0;
        }
```

- [ ] **Step 2:** `FirmQuotationCost` — `set cost_id`:

```js
        set cost_id (value) {
            this._cost_id = value;
            if (this.parent.all_costs) {
                let cost = this.parent.all_costs.find(c => c.id == value);
                this._vat_percent = this.parent.no_require_vat ? 0 : cost.vat_percent;
            }

        }
```

- [ ] **Step 3:** `FirmQuotation.after()` — dòng `this.delivery_vat_percent = 8;` đổi thành:

```js
            this.delivery_vat_percent = this.no_require_vat ? 0 : 8;
```

và thêm method (ngay trước `calculateProducts() {`):

```js
        /**
         * Khách thuộc nhóm "không bắt buộc VAT" ⇒ VAT hàng hoá / chi phí / vận chuyển = 0%.
         * Đổi sang khách thường ⇒ trả VAT chi phí theo danh mục, vận chuyển 8%
         * (VAT hàng hoá tự trả lại qua getter FirmQuotationTabProduct.vat_percent).
         */
        applyCustomerVat(no_require_vat) {
            this.no_require_vat = !!no_require_vat;
            this.delivery_vat_percent = this.no_require_vat ? 0 : 8;
            [...this.costs, ...this.revenue_costs].forEach(c => {
                if (this.no_require_vat) {
                    c.vat_percent = 0;
                    return;
                }
                let cost = this.all_costs.find(val => val.id == c._cost_id);
                if (cost) c.vat_percent = cost.vat_percent;
            });
            this.calculateProducts();
        }
```

- [ ] **Step 4:** `formJs.blade.php` — `setCustomer`:

```js
$scope.setCustomer = function(customer) {
    console.log(customer);
    $scope.form.customer = customer;
    $scope.updateStock($scope.form);
    $scope.getListComboCategory(customer.id);
    sendRequest({
        type: 'GET',
        url: "{{ route('firmQuotation.customerVatInfo') }}",
        data: { customer_id: customer.id },
        success: function(response) {
            if (response.success) {
                $scope.form.applyCustomerVat(response.data.no_require_vat);
                $scope.$applyAsync();
            }
        }
    }, $scope);
}
```

- [ ] **Step 5:** `sale/firm/quotations/form.blade.php` — ngay sau `<h4>Chi tiết</h4>` (trong `col-md-3`):

```html
                        <div class="text-info" ng-if="form.no_require_vat" style="font-size: 12px">
                            <i class="fa fa-info-circle"></i> Khách thuộc nhóm không bắt buộc VAT — VAT = 0%
                        </div>
```

- [ ] **Step 6:** `sale/firm/contracts/form.blade.php` — ngay sau `<h4>Thông tin hàng hóa</h4>`: cùng khối như Step 5. Kiểm tra `form.no_require_vat` có vào FirmContract khi lập từ BG (hàm nạp dữ liệu BG dùng `no_set_quotation`); nếu không có thì thêm `this.no_require_vat = data.no_require_vat;` trong hàm nạp BG của `FirmContract.blade.php` (tìm `no_set_quotation.includes`).

- [ ] **Step 7:** Mở `/admin/sale/firm_quotations/create` (local), Console không lỗi JS.

---

### Task 5: Nghiệm thu local (Playwright + DB)

**Files:** không sửa code.

- [ ] **Step 1:** Chuẩn bị DB `erp_dev_30_01_26`: chọn 1 khách K1 có BG hãng, gán vào nhóm có `no_require_vat=1` (`customer_has_groups`); ghi lại để trả lại sau. 1 khách K2 thường.
- [ ] **Step 2:** `php artisan serve --port=8001`, Playwright `playwright-a`:
  1. Tạo BG hãng cho K1, thêm hàng VAT 10% + 1 chi phí → cột VAT hàng 0, nhóm "VAT 0%", tổng sau VAT = tổng trước VAT, có dòng ⓘ. Lưu. DB `firm_quotation_tab_products.vat_percent=0`, `firm_quotation_groups.vat_percent=0`, `firm_quotations.delivery_vat_percent=0,total_vat=0`.
  2. BG cũ của K1 (VAT >0, trạng thái Đang tạo) → mở sửa: hiện 0 → lưu → DB về 0.
  3. Duyệt BG → lập HĐ → VAT 0 trên form; lưu; DB `firm_contracts.total_vat=0`, `delivery_vat=0`, `firm_contract_tab_products.vat_percent=0`, `firm_contract_costs.vat_percent=0`; mở sửa HĐ vẫn 0.
  4. BG mới: chọn K1 rồi đổi sang K2 → VAT hàng về theo danh mục, vận chuyển 8%.
  5. `browser_evaluate` POST lại payload của kịch bản 1 với `vat_percent: 10` → DB vẫn 0.
  6. Đối chứng K2 từ đầu tới HĐ: VAT như cũ.
- [ ] **Step 3:** Xem ảnh chụp màn (không chỉ DOM). Đóng browser (`browser_close`). Trả lại nhóm của K1.
- [ ] **Step 4:** Cập nhật Checkpoint bên dưới + `erp/.plans/STATUS.md`.

## Checkpoint — 2026-09-24

- Vừa hoàn thành: Task 1–5. Nghiệm thu local :8001 bằng Playwright + DB: 6/6 kịch bản đạt + 1 kịch bản sao chép BG → đổi khách thường. Unit test 10/10.
  Đã dọn dữ liệu test (HĐ 1044, BG 1942/1943), khôi phục BG 1844 + nhóm khách 34 + mật khẩu user 13.
- Lỗi bắt được khi test: đoạn ép 0 lúc mở sửa BG lọt vào `getDataForShow` (đuôi giống `getDataForEdit`) → đã chuyển.
  Review độc lập: #1 đổi khách sau khi mở sửa/sao chép không trả VAT hàng → `zeroLoadedData($r, false)` giữ VAT gốc dòng hàng cho form BG.
- ⚠️ Commit `10ebb1349e` (user) CHƯA gồm 2 sửa trên — còn nằm ở working tree (FirmQuotationService, FirmVatExemption, test).
- Quyết định: phụ lục bổ sung / HĐ nguyên tắc của khách có tích cũng về 0% (dùng chung saveFirmContractData) — khớp yêu cầu "tất cả BG-HĐ".
- Hoãn (minor): API CRM `CRM/Sale/FirmQuotationController` chưa ép; race `setCustomer` async nếu bấm Lưu quá nhanh sau khi đổi khách;
  chi phí ngừng dùng / VAT sửa tay không trả lại khi đổi khách; combo lines HĐ còn hiện VAT (tổng không ảnh hưởng); đơn hàng nguyên tắc chưa theo cờ.
- Bước tiếp theo: user commit phần còn lại → đợt 2 (BG dự án TKT HRM + đường API đồng bộ).
- Blocked: —

## Phản hồi QA dev-erp 24/09/2026 (chiều)

QA báo trên dev-erp (luồng `create?copy=2076`, khách có tích): tab "Hàng mua theo CTKM", Chi phí khác,
Dịch vụ đi kèm và Vận chuyển (tab Tổng hợp báo giá, `quotations/partials/payment-info.blade.php`) vẫn 8%;
hàng hoá thường thì đúng.

**Nguyên nhân:** `develop_01` chỉ có commit `10ebb1349e` — bản đó chèn `zeroLoadedData` nhầm vào
`getDataForShow` ⇒ luồng sao chép/mở sửa (`getDataForCopy` → `getDataForEdit`) không trả cờ
`no_require_vat` ⇒ FE giữ VAT gốc. 2 sửa sau (chuyển về `getDataForEdit` + tham số `$zeroTabProducts`)
còn ở working tree `master`, CHƯA commit.

**Verify local với working tree (Playwright, `create?copy=1904` — BG có đủ CTKM + chi phí + dịch vụ + vận chuyển 2tr):**
tab CTKM 0%, Dịch vụ/Chi phí 0%, thêm mới "Phí vận chuyển hàng gấp" + "Chi phí sửa chữa, thay thế"
(mặc định 8%) → 0%, tab Tổng hợp "Vận chuyển 0 %", tổng VAT 0; Duyệt → DB 0 hết; lập HĐ → vận chuyển
VAT 0, tổng VAT 0. Không cần sửa thêm code. Đã dọn dữ liệu test.

**Việc còn lại:** user commit 3 file working tree (`FirmVatExemption.php`, `FirmQuotationService.php`,
`tests/Unit/FirmVatExemptionTest.php`) → merge `develop_01` → deploy dev-erp cho QA test lại.
