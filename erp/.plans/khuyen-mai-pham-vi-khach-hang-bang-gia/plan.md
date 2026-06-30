# Chương trình khuyến mại — Phạm vi áp dụng (Chọn KH + Bảng giá) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Steps dùng checkbox `- [ ]`.

**Goal:** Tab "Phạm vi áp dụng" của Chương trình khuyến mại (`new_combo_categories`): đổi "Nhóm khách hàng" → "Chọn khách hàng" (multi-select ajax), thêm khối "Bảng giá áp dụng" (radio + multi-select `price_types`); enforce thực tế khi áp KM.

**Architecture:** Tái dùng cờ `combo_categories.customers` (1=toàn bộ / 2=chọn KH cụ thể), thêm cờ `price_lists` (1/2). 2 pivot mới. Sửa `ComboCategory::checkActive` + `ComboCampaign::checkActive` (thêm `$price_type`) và truyền `price_type` ở call site. KM cũ không migrate → pivot rỗng coi như không giới hạn (legacy-safe).

**Tech Stack:** Laravel 6 / PHP 7.4, Blade + AngularJS 1.3.9, MySQL, select2.

> ⚠️ **CẢNH BÁO MÔI TRƯỜNG:** `.env` local trỏ thẳng **DB production `erp_new`**. KHÔNG chạy `php artisan migrate` tùy tiện ở local — migration sẽ tạo bảng trên PROD. Chạy migrate trên server lúc deploy (hoặc xác nhận với chủ dự án trước). Mọi verify dữ liệu chỉ dùng SELECT/tinker.

> ⚠️ Git: KHÔNG commit/push khi chưa có yêu cầu (theo CLAUDE.md). Các step "Commit" bên dưới chỉ thực hiện khi user yêu cầu.

---

## File Structure

**Tạo mới:**
- `database/migrations/2026_06_19_000000_add_price_lists_scope_to_combo_categories.php` — cột `price_lists` + 2 bảng pivot.

**Sửa:**
- `app/Model/Sale/ComboCategory.php` — quan hệ `applied_customers()`, `price_types()`; `price_lists` vào `getDataForEdit/Show/Use`; `checkActive`.
- `app/Model/Sale/ComboCampaign.php` — `checkActive` (thêm `$price_type`).
- `app/Http/Controllers/Sale/NewComboCategoryController.php` — validate + sync ở `store()` và `update()`.
- `resources/views/sale/new_combo_categories/form.blade.php` — khối KH (đổi) + khối Bảng giá (mới).
- `resources/views/partials/classes/sale/ComboCategory.blade.php` — init `price_lists`, map `customer_ids`/`price_list_ids`/`selected_customers`, nguồn `price_types`.
- `public/js/angular/app.directive.js` — THÊM directive `ngSelect2CustomerMulti` (additive).
- Call site enforce: `app/Contract.php:2474`, `app/Model/Sale/Firm/Quotation/FirmQuotation.php:551`, `app/Quotation.php:270`, `app/Model/Warehouse/ProductExportRequest.php:2013`, `app/Model/Sale/ContractAdditionAnnex.php:125`, `app/Http/Controllers/Sale/NewComboCategoryController.php:169,191`.

---

# PHASE 1 — Form + Lưu

## Task 1: Migration (cột + 2 pivot)

**Files:** Create `database/migrations/2026_06_19_000000_add_price_lists_scope_to_combo_categories.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddPriceListsScopeToComboCategories extends Migration
{
    public function up()
    {
        Schema::table('combo_categories', function (Blueprint $table) {
            $table->unsignedTinyInteger('price_lists')->default(1)->after('customer_group_id');
        });

        Schema::create('combo_category_has_customers', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('combo_category_id');
            $table->unsignedBigInteger('customer_id');
            $table->timestamps();
            $table->index('combo_category_id');
            $table->index('customer_id');
        });

        Schema::create('combo_category_has_price_types', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('combo_category_id');
            $table->unsignedBigInteger('price_type_id');
            $table->timestamps();
            $table->index('combo_category_id');
            $table->index('price_type_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('combo_category_has_price_types');
        Schema::dropIfExists('combo_category_has_customers');
        Schema::table('combo_categories', function (Blueprint $table) {
            $table->dropColumn('price_lists');
        });
    }
}
```

- [ ] **Step 2: Lint**

Run: `php -l database/migrations/2026_06_19_000000_add_price_lists_scope_to_combo_categories.php`
Expected: `No syntax errors detected`

- [ ] **Step 3: Chạy migrate TRÊN SERVER (không local)** — `php artisan migrate`. Xác nhận 3 thay đổi: cột `price_lists`, bảng `combo_category_has_customers`, `combo_category_has_price_types`.

---

## Task 2: Model ComboCategory — quan hệ + load data

**Files:** Modify `app/Model/Sale/ComboCategory.php`

- [ ] **Step 1: Thêm 2 quan hệ** (sau method `customer_groups()` ~dòng 38)

```php
    public function applied_customers () {
        return $this->belongsToMany('App\Model\Sale\Customer', 'combo_category_has_customers', 'combo_category_id', 'customer_id');
    }

    public function price_types () {
        return $this->belongsToMany('App\Model\Product\PriceType', 'combo_category_has_price_types', 'combo_category_id', 'price_type_id');
    }
```

- [ ] **Step 2: Eager-load ở `getDataForEdit` + `getDataForShow` + `getDataForUse`** — thêm vào mảng `with([...])` (cạnh `customer_groups`):

```php
                'applied_customers' => function($q) {
                    $q->select(['customers.id', 'customers.code', 'customers.fullname']);
                },
                'price_types' => function($q) {
                    $q->select(['price_types.id']);
                },
```

(Áp cho cả 3 method.)

- [ ] **Step 3: Lint**

Run: `php -l app/Model/Sale/ComboCategory.php`
Expected: `No syntax errors detected`

---

## Task 3: Directive ngSelect2CustomerMulti (multi-select KH ajax + preload)

**Files:** Modify `public/js/angular/app.directive.js` (THÊM directive mới, ngay sau `ngSelect2Customer` kết thúc ~dòng 461)

- [ ] **Step 1: Thêm directive**

```js
    .directive("ngSelect2CustomerMulti", function ($timeout) {
        return {
            restrict: 'AC',
            require: 'ngModel',
            link: function (scope, element, attrs, ngModel) {
                $timeout(function () {
                    var $el = $(element);
                    $el.select2({
                        placeholder: "Nhập tên, SĐT hoặc mã KH để tìm",
                        multiple: true,
                        allowClear: true,
                        ajax: {
                            delay: 350,
                            url: urlSearchCustomer,
                            data: function (params) { return { keywords: params.term }; },
                            dataType: 'json',
                            processResults: function (data) {
                                return { results: data.data.map(function (c) {
                                    return { id: c.id, text: c.code + ' - ' + c.fullname };
                                }) };
                            }
                        }
                    });

                    // preload các KH đã chọn (edit/show)
                    var preselected = scope.$eval(attrs.preselected) || [];
                    preselected.forEach(function (c) {
                        if (!$el.find("option[value='" + c.id + "']").length) {
                            $el.append(new Option(c.text, c.id, true, true));
                        }
                    });
                    var initVals = (ngModel.$modelValue || []).map(String);
                    $el.val(initVals).trigger('change');

                    // select2 -> ng-model (mảng số)
                    $el.on('change', function () {
                        var vals = ($el.val() || []).map(Number);
                        if (scope.$root.$$phase) {
                            ngModel.$setViewValue(vals);
                        } else {
                            scope.$apply(function () { ngModel.$setViewValue(vals); });
                        }
                    });

                    if (attrs.disabledExpr) {
                        scope.$watch(attrs.disabledExpr, function (v) { $el.prop('disabled', !!v); });
                    }
                });
            }
        };
    })
```

- [ ] **Step 2: Kiểm tra cú pháp JS** — mở file, đảm bảo dấu `.directive(...)` nối đúng chuỗi (file dùng pattern `app.directive(...).directive(...)`). Không có lỗi thừa/thiếu dấu phẩy/ngoặc.

- [ ] **Step 3 (verify browser sau khi xong FE):** select2 KH search ra kết quả, chọn nhiều, bỏ chọn, preload đúng khi edit.

---

## Task 4: Form blade — khối Khách hàng + khối Bảng giá

**Files:** Modify `resources/views/sale/new_combo_categories/form.blade.php`

- [ ] **Step 1: Thay khối Khách hàng** — thay đoạn dòng 165-184 (radio "Nhóm khách hàng" + select `customer_groups`) bằng:

```html
                                    <div class="radio radio-inverse d-flex align-items-center">
                                        <label class="range-radio">
                                            <input type="radio" ng-model="form.customers" value="2">
                                            <i class="helper"></i> Chọn khách hàng
                                        </label>
                                        <select class="form-control" ng-select2-customer-multi
                                                preselected="form.selected_customers"
                                                disabled-expr="form.customers != 2"
                                                ng-model="form.customer_ids" multiple></select>
                                    </div>
                                </div>
                                <span class="invalid-feedback d-block" role="alert"
                                    ng-if="errors && errors['customers']">
                                    <strong><% errors['customers'][0] %></strong>
                                </span>
                                <span class="invalid-feedback d-block" role="alert"
                                    ng-if="errors && errors['customer_ids']">
                                    <strong><% errors['customer_ids'][0] %></strong>
                                </span>
```

(Giữ nguyên radio "Toàn bộ khách hàng" dòng 159-164 ở trên.)

- [ ] **Step 2: Thêm khối Bảng giá** — chèn 1 `col-md-6` mới NGAY SAU `</div>` đóng col Khách hàng (sau dòng 185 cũ), trước col Nhân viên:

```html
                            <div class="col-md-6">
                                <div class="form-radio mt-2">
                                    <div class="radio radio-inverse">
                                        <label>
                                            <input type="radio" ng-model="form.price_lists" value="1">
                                            <i class="helper"></i> Toàn bộ bảng giá
                                        </label>
                                    </div>
                                    <div class="radio radio-inverse d-flex align-items-center">
                                        <label class="range-radio">
                                            <input type="radio" ng-model="form.price_lists" value="2">
                                            <i class="helper"></i> Bảng giá áp dụng
                                        </label>
                                        <select class="form-control select2" ng-disabled="form.price_lists != 2" ng-model="form.price_list_ids" multiple>
                                            <option ng-repeat="p in form.all_price_types" value="<% p.id %>" ng-selected="arrayInclude(form.price_list_ids, p.id)">
                                                <% p.name %>
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <span class="invalid-feedback d-block" role="alert"
                                    ng-if="errors && errors['price_list_ids']">
                                    <strong><% errors['price_list_ids'][0] %></strong>
                                </span>
                            </div>
```

- [ ] **Step 3 (verify):** Tab Phạm vi áp dụng hiển thị: Công ty / Khách hàng (Toàn bộ / Chọn khách hàng) / Bảng giá (Toàn bộ / Bảng giá áp dụng) / Nhân viên. Không lỗi JS console.

---

## Task 5: Class ComboCategory — init + map dữ liệu

**Files:** Modify `resources/views/partials/classes/sale/ComboCategory.blade.php`

- [ ] **Step 1: Thêm nguồn price_types + init mặc định.** Trong constructor: sau dòng `this.all_departments = ...` (dòng 8) thêm:

```js
			this.all_price_types = @json(\App\Model\Product\PriceType::getAll());
```

Sau khối gán default (sau dòng 19 `this.customers = this.customers || 1;`) thêm:

```js
            this.price_lists = this.price_lists || 1;
            this.customer_ids = (form && form.applied_customers) ? form.applied_customers.map(c => c.id) : (this.customer_ids || []);
            this.price_list_ids = (form && form.price_types) ? form.price_types.map(p => p.id) : (this.price_list_ids || []);
            this.selected_customers = (form && form.applied_customers) ? form.applied_customers.map(c => ({ id: c.id, text: c.code + ' - ' + c.fullname })) : [];
```

- [ ] **Step 2: Đảm bảo submit data có `customers`, `customer_ids`, `price_lists`, `price_list_ids`** — kiểm tra nơi build payload submit (search "submit_data" / nơi controller gửi `$http.post`). Vì class gán thẳng thuộc tính nên các field này tự nằm trong object; xác nhận payload gửi lên có 4 field (đặc biệt `customer_ids`, `price_list_ids` là mảng).

- [ ] **Step 3 (verify):** Mở Network tab khi Lưu → payload chứa `customers`, `customer_ids[]`, `price_lists`, `price_list_ids[]`.

---

## Task 6: Controller store() — validate + sync

**Files:** Modify `app/Http/Controllers/Sale/NewComboCategoryController.php`

- [ ] **Step 1: Sửa validate trong `store()`** — thay 2 dòng `customer_groups` (dòng 243-244) bằng, và thêm block price_lists:

```php
          'customers' => 'required|in:1,2',
          'customer_ids' => 'required_if:customers,2|nullable|array|min:1',
          'customer_ids.*' => 'exists:customers,id',
          'price_lists' => 'required|in:1,2',
          'price_list_ids' => 'required_if:price_lists,2|nullable|array|min:1',
          'price_list_ids.*' => 'exists:price_types,id',
```

- [ ] **Step 2: Sửa message** (khối messages, cạnh `customer_groups.required_if`):

```php
              'customer_ids.required_if' => 'Bắt buộc phải chọn',
              'price_list_ids.required_if' => 'Bắt buộc phải chọn',
```
(Xoá/để lại message cũ `customer_groups.required_if` không sao — không còn field đó.)

- [ ] **Step 3: Gán cờ + sync** — sau `$object->customers = $request->customers;` (dòng ~392) thêm `$object->price_lists = $request->price_lists;`. Thay khối sync customer_groups (dòng 413-415) bằng:

```php
          if ($object->customers == ThisModel::MOT_PHAN) {
              $object->applied_customers()->sync($request->customer_ids ?? []);
          } else {
              $object->applied_customers()->sync([]);
          }
          if ($object->price_lists == ThisModel::MOT_PHAN) {
              $object->price_types()->sync($request->price_list_ids ?? []);
          } else {
              $object->price_types()->sync([]);
          }
```

- [ ] **Step 4: Lint** — `php -l app/Http/Controllers/Sale/NewComboCategoryController.php` → `No syntax errors detected`.

---

## Task 7: Controller update() — validate + sync

**Files:** Modify `app/Http/Controllers/Sale/NewComboCategoryController.php`

- [ ] **Step 1:** Áp dụng Y HỆT Task 6 cho method `update()` (validate ~dòng 496-498, messages ~569, gán cờ ~656, sync ~663-665). Dùng cùng các đoạn code ở Task 6 Step 1/2/3.

- [ ] **Step 2: Lint** — `php -l ...NewComboCategoryController.php` → sạch.

- [ ] **Step 3 (verify E2E Phase 1):** Trên 1 môi trường có DB đã migrate:
  1. Thêm KM: chọn "Chọn khách hàng" + vài KH, "Bảng giá áp dụng" + vài bảng giá → Lưu → kiểm DB `combo_category_has_customers`, `combo_category_has_price_types` có dòng đúng; `customers=2`, `price_lists=2`.
  2. Sửa KM đó → preload đúng KH + bảng giá đã chọn.
  3. Duyệt/Xem chi tiết → hiển thị readonly đúng.
  4. Chọn "Toàn bộ khách hàng" / "Toàn bộ bảng giá" → Lưu → pivot tương ứng rỗng.
  5. Bỏ trống khi chọn "Chọn khách hàng"/"Bảng giá áp dụng" → báo lỗi inline "Bắt buộc phải chọn".

---

# PHASE 2 — Enforce

## Task 8: ComboCategory::checkActive — KH cụ thể + bảng giá

**Files:** Modify `app/Model/Sale/ComboCategory.php` (method `checkActive`, dòng 168-194)

- [ ] **Step 1: Đổi chữ ký + nhánh** — thay:

```php
    public static function checkActive($id, $customer_id, $employee_id) {
        $combo = self::findOrFail($id);
        if (!$combo->approved || $combo->status != 1 || $combo->from_date > date('Y-m-d') || $combo->to_date < date('Y-m-d')) return false;
        if ($combo->customers == self::MOT_PHAN) {
            $customer_groups = CustomerHasGroup::where('customer_id', $customer_id)->pluck('customer_group_id')->toArray();
            $exist = ComboCategoryHasCustomerGroup::where('combo_category_id', $combo->id)
                ->whereIn('customer_group_id', $customer_groups)
                ->first();
            if (!$exist) return false;
        }
```

bằng:

```php
    public static function checkActive($id, $customer_id, $employee_id, $price_type = null) {
        $combo = self::findOrFail($id);
        if (!$combo->approved || $combo->status != 1 || $combo->from_date > date('Y-m-d') || $combo->to_date < date('Y-m-d')) return false;
        if ($combo->customers == self::MOT_PHAN) {
            $customer_ids = \DB::table('combo_category_has_customers')->where('combo_category_id', $combo->id)->pluck('customer_id')->toArray();
            // legacy-safe: KM cũ pivot rỗng -> không giới hạn KH
            if (!empty($customer_ids) && !in_array($customer_id, $customer_ids)) return false;
        }
        if ($combo->price_lists == self::MOT_PHAN) {
            $price_type_ids = \DB::table('combo_category_has_price_types')->where('combo_category_id', $combo->id)->pluck('price_type_id')->toArray();
            if (!empty($price_type_ids) && (empty($price_type) || !in_array($price_type, $price_type_ids))) return false;
        }
```

(giữ nguyên 2 nhánh `scope` và `sellers` phía sau.)

- [ ] **Step 2: Cập nhật call site preview** trong `NewComboCategoryController.php:169` và `:191`: thêm `$request->price_type` làm tham số 4:

```php
                if (ThisModel::checkActive($object->id, $request->customer_id, $request->employee_id, $request->price_type)) {
```
```php
        if (!ThisModel::checkActive($id, $request->customer_id, $request->employee_id, $request->price_type)) {
```

- [ ] **Step 3: Lint** — `php -l app/Model/Sale/ComboCategory.php` + controller → sạch.

---

## Task 9: ComboCampaign::checkActive — KH cụ thể + bảng giá

**Files:** Modify `app/Model/Sale/ComboCampaign.php` (method `checkActive`, dòng 354-381)

- [ ] **Step 1: Đổi chữ ký + nhánh** — thay đầu method:

```php
    public static function checkActive($id, $customer_id, $employee_id, $price_type = null) {
        $object = self::findOrFail($id);
        $combo = $object->category;
        if ($object->status != 1 || !$combo->approved || $combo->status != 1 || $combo->from_date > date('Y-m-d') || $combo->to_date < date('Y-m-d')) return false;
        if ($combo->customers == self::MOT_PHAN) {
            $customer_ids = \DB::table('combo_category_has_customers')->where('combo_category_id', $combo->id)->pluck('customer_id')->toArray();
            if (!empty($customer_ids) && !in_array($customer_id, $customer_ids)) return false;
        }
        if ($combo->price_lists == self::MOT_PHAN) {
            $price_type_ids = \DB::table('combo_category_has_price_types')->where('combo_category_id', $combo->id)->pluck('price_type_id')->toArray();
            if (!empty($price_type_ids) && (empty($price_type) || !in_array($price_type, $price_type_ids))) return false;
        }
```

(giữ nguyên nhánh `scope`, `sellers`, `return true` phía sau.)

- [ ] **Step 2: Lint** — `php -l app/Model/Sale/ComboCampaign.php` → sạch.

---

## Task 10: Truyền price_type tại call site áp KM thật

**Files:** Modify từng call site `ComboCampaign::checkActive(...)` — thêm tham số `price_type` của chứng từ.

- [ ] **Step 1: `app/Contract.php:2474`** — đổi:
```php
                if (!ComboCampaign::checkActive($c['combo_campaign_id'], $this->customer_id, $this->created_by, $this->price_type)) return false;
```

- [ ] **Step 2: `app/Model/Sale/Firm/Quotation/FirmQuotation.php:551`** — thêm `$this->price_type` làm tham số 4.

- [ ] **Step 3: `app/Quotation.php:270`** — `PromoCampaign::checkActive(...)` KHÔNG đổi (PromoCampaign out of scope). Chỉ đổi các lời gọi `ComboCampaign::checkActive` nếu có ở file này. Kiểm tra: nếu dòng 270 là `PromoCampaign` thì bỏ qua.

- [ ] **Step 4: `app/Model/Warehouse/ProductExportRequest.php:2013`** (ComboCampaign) — thêm `$this->price_type`.

- [ ] **Step 5: `app/Model/Sale/ContractAdditionAnnex.php:125`** — thêm `$this->price_type`.

- [ ] **Step 6: Xác minh từng file có thuộc tính `price_type`** — `grep -n "price_type" <file>` trước khi sửa; nếu tên khác (vd `price_type_id`) thì dùng đúng tên. Lint từng file sau sửa.

- [ ] **Step 7 (verify E2E Phase 2):**
  - Tạo KM mới `customers=2` (KH A) + `price_lists=2` (bảng giá X), đã duyệt, còn hiệu lực.
  - Lập báo giá/HĐ cho KH A, bảng giá X → KM áp được.
  - Đổi sang KH B hoặc bảng giá Y → KM KHÔNG áp.
  - KM cũ (pivot rỗng) → vẫn áp như trước (không bị chặn nhầm).

---

### Checkpoint — 2026-06-19
Vừa hoàn thành: TOÀN BỘ code Phase 1 + Phase 2 (subagent-driven, `php -l` sạch 12 file, qua review cuối). Đã tạo migration + 2 quan hệ model + directive `ngSelect2CustomerMulti` + form 4 cột + class + store/update + checkActive (2 model) + truyền price_type ở 6 call site (gồm ComboCampaignsController preview fix sau review).
Đang làm dở: không (code xong).
Bước tiếp theo (USER):
1. Chạy `php artisan migrate` TRÊN SERVER (không local — env→DB prod).
2. Browser test Phase 1 (thêm/sửa/duyệt/xem + lưu KH/bảng giá) + Phase 2 (áp KM thực tế lọc theo KH/bảng giá; KM cũ không vỡ).
3. Commit khi muốn (chưa commit gì).
Follow-up (ĐÃ LÀM): thêm `price_type` vào call preview combo (getListDataForUse/getDataForUse) ở 6 form áp KM: firm quotations/orders/ztect_orders (`$scope.form.price_type`), sale_orders + contracts/createEditJs (`$scope.form.price_type`), contract_addition_annexes (`$scope.form.parent_contract.price_type`). SKIP phiếu xuất kho (không có price_type). project_quotations/quotations chỉ có quotation_templates (không liên quan combo).
Blocked:

## Self-review checklist (đã rà)
- Spec coverage: form KH/bảng giá (Task 4,5), DB (Task 1), model (Task 2), store/update (Task 6,7), enforce (Task 8,9,10) — đủ.
- Tên nhất quán: quan hệ `applied_customers()`, `price_types()`; field `customer_ids`, `price_list_ids`, cờ `price_lists`; pivot `combo_category_has_customers`, `combo_category_has_price_types`.
- Legacy-safe: pivot rỗng → bỏ qua (Task 8,9).
- Rủi ro còn lại: payload submit phải gửi `customer_ids`/`price_list_ids` dạng mảng (Task 5 Step 2 verify); directive multi-select cần test browser kỹ (Task 3).
