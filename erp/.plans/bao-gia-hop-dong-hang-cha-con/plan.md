# Plan — Hàng hoá 2 cấp cha-con (Báo giá / Hợp đồng hãng)

> **Cho agentic worker:** dùng skill `superpowers:subagent-driven-development` hoặc `executing-plans` để chạy từng task. Dự án Laravel 6 + AngularJS 1.3.9, KHÔNG có test framework → mỗi task verify bằng `php -l` + test browser thủ công (không pytest/TDD).
>
> **Spec:** xem `design.md` cùng thư mục. **Không commit/push** khi chưa được yêu cầu.

**Goal:** Cho phép khai báo hàng hoá 2 cấp cha-con (tỉ lệ cố định, SL con auto) trên báo giá hãng + hợp đồng hãng; áp quỹ nghĩa vụ giao LINKED khi tạo yêu cầu xuất hàng.

**Architecture:** Thêm 2 cột self-ref (`child_parent_id`, `child_ratio`) vào dòng hàng BG+HĐ; carryover BG→HĐ remap id; refactor attribution `exported_qty` sang id dòng; service tính quỹ cha-con áp ở bước yêu cầu xuất hàng; FE Angular gom nhóm + auto SL con + loại con khỏi tổng tiền; bản in chỉ in cha.

**Tech Stack:** PHP 7.4 / Laravel 6, MySQL, Blade, AngularJS 1.3.9 (`<% %>`), Yajra DataTables.

## Global Constraints

- Phạm vi: CHỈ báo giá hãng (`FirmQuotation`) + hợp đồng hãng (`FirmContract`). KHÔNG đụng ZT/dự án/dịch vụ/HRM.
- Tỉ lệ con = **số nguyên dương**. SL con = SL cha × tỉ lệ (auto, khoá sửa tay).
- Tiền: **chỉ cha** cộng vào tổng. Con hiện trên FORM (đơn giá + thành tiền dòng) nhưng không cộng tổng; con KHÔNG in ra.
- Quan hệ cha-con gắn theo **id DÒNG**, không theo `product_id`.
- Quỹ cha-con trừ theo `exported_qty`; áp ở **yêu cầu xuất hàng**, KHÔNG ở phiếu xuất kho. `warehouse_exported_qty` giữ nguyên logic cũ.
- BE validate phải rethrow `ValidationException` (không catch chung). FE hiện lỗi inline (`is-invalid` + `invalid-feedback`).
- Mọi sửa hàm dùng chung → legacy-safe: dòng không cha-con (`child_parent_id = null`) chạy y như cũ.
- Công thức quỹ (cụm cha P, SL HĐ = Q, con i tỉ lệ r_i; a = exported_qty cha, delivered_i = exported_qty con i):
  - `P_remaining = Q − a − max_i(delivered_i / r_i)`
  - `child_i_remaining = (Q × r_i) − delivered_i − (r_i × a)`
- ⚠️ KHÔNG `php artisan migrate` ở local (env local trỏ DB production). Migrate trên server khi deploy.

---

## Phase 1 — Schema & Model (nền tảng)

### Task 1.1: Migration thêm cột cha-con vào 2 bảng *_tab_products

**Files:**
- Create: `database/migrations/2026_06_20_100001_add_child_columns_to_firm_quotation_tab_products.php`
- Create: `database/migrations/2026_06_20_100002_add_child_columns_to_firm_contract_tab_products.php`

- [ ] **Step 1: Viết migration báo giá**

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddChildColumnsToFirmQuotationTabProducts extends Migration
{
    public function up()
    {
        Schema::table('firm_quotation_tab_products', function (Blueprint $table) {
            $table->unsignedBigInteger('child_parent_id')->nullable()->after('parent_id')
                ->comment('id dòng hàng CHA trong cùng bảng (null = độc lập/cha)');
            $table->integer('child_ratio')->nullable()->after('child_parent_id')
                ->comment('tỉ lệ con/cha (chỉ có ở dòng con)');
        });
    }
    public function down()
    {
        Schema::table('firm_quotation_tab_products', function (Blueprint $table) {
            $table->dropColumn(['child_parent_id', 'child_ratio']);
        });
    }
}
```

- [ ] **Step 2: Viết migration hợp đồng** — copy y hệt, đổi class `AddChildColumnsToFirmContractTabProducts` + bảng `firm_contract_tab_products`.

- [ ] **Step 3: Kiểm cú pháp**

Run: `php -l database/migrations/2026_06_20_100001_add_child_columns_to_firm_quotation_tab_products.php && php -l database/migrations/2026_06_20_100002_add_child_columns_to_firm_contract_tab_products.php`
Expected: `No syntax errors detected` cả 2.

### Task 1.2: Migration thêm `firm_contract_tab_product_id` vào product_export_request_tab_products

**Files:**
- Create: `database/migrations/2026_06_20_100003_add_firm_contract_tab_product_id_to_export_request.php`

- [ ] **Step 1: Viết migration**

```php
Schema::table('product_export_request_tab_products', function (Blueprint $table) {
    $table->unsignedBigInteger('firm_contract_tab_product_id')->nullable()
        ->after('firm_contract_tab_id')
        ->comment('id dòng HĐ gốc, dùng attribution exported_qty chính xác cho cha-con');
});
```
+ `down()` dropColumn tương ứng.

- [ ] **Step 2: `php -l`** file migration → `No syntax errors detected`.

### Task 1.3: Cập nhật $fillable + relation 2 model

**Files:**
- Modify: `app/Model/Sale/Firm/Quotation/FirmQuotationTabProduct.php`
- Modify: `app/Model/Sale/Firm/Contract/FirmContractTabProduct.php`

**Interfaces — Produces:**
- `child_parent_id`, `child_ratio` fillable trên cả 2 model.
- `children()`, `childParent()` trên cả 2 model.

- [ ] **Step 1: FirmQuotationTabProduct** — thêm `'child_parent_id', 'child_ratio'` vào `$fillable`; thêm:

```php
public function children() {
    return $this->hasMany(self::class, 'child_parent_id', 'id');
}
public function childParent() {
    return $this->belongsTo(self::class, 'child_parent_id', 'id');
}
```

- [ ] **Step 2: FirmContractTabProduct** — y hệt Step 1 (đúng class HĐ).

- [ ] **Step 3: `php -l`** cả 2 file → sạch.

---

## Phase 2 — Refactor attribution `exported_qty` sang id dòng (RỦI RO NHẤT, làm sớm)

> Mục tiêu: dòng nguồn yêu cầu xuất lưu `firm_contract_tab_product_id`; cộng `exported_qty`/`warehouse_exported_qty` match theo id dòng. Legacy-safe: `firm_contract_tab_product_id` null → fallback khóa cũ `(firm_contract_id, parent_id, product_id, unit_id)`.

### Task 2.1: Lưu `firm_contract_tab_product_id` khi sync yêu cầu xuất

**Files:**
- Modify: `app/Model/Warehouse/ProductExportRequestTab.php` (method `syncTabProducts`, ~dòng 15-31)

- [ ] **Step 1: Thêm gán cột** trong vòng lặp, ngay sau `$p->firm_contract_tab_id = ...;`:

```php
$p->firm_contract_tab_product_id = $pro['firm_contract_tab_product_id'] ?? null;
```

- [ ] **Step 2: `php -l`** → sạch.
- [ ] **Step 3 (ghi chú):** xác nhận FE gửi `firm_contract_tab_product_id` mỗi product (service set ở dòng 359). Nếu FE strip → sửa ở Task 5.3.

### Task 2.2: Refactor `ProductExport::syncFirmContractTabProducts` match theo id dòng

**Files:**
- Modify: `app/Model/Warehouse/ProductExport.php` (dòng ~1676-1690, phần cộng về `FirmContractTabProduct`)

- [ ] **Step 1: Đổi query match** — ưu tiên id dòng, fallback khóa cũ:

```php
$contract_product = null;
if (!empty($p->firm_contract_tab_product_id)) {
    $contract_product = FirmContractTabProduct::query()
        ->where('id', $p->firm_contract_tab_product_id)->first();
}
if (!$contract_product) { // legacy fallback
    $contract_product = FirmContractTabProduct::query()->where([
        'firm_contract_id' => $p->firm_contract_id,
        'parent_id' => $p->firm_contract_tab_id,
        'product_id' => $p->product_id,
        'unit_id' => $p->unit_id,
    ])->first();
}
if ($contract_product) {
    $contract_product->exported_qty += $p->qty;
    if ($this->is_export_direct) {
        $contract_product->warehouse_exported_qty += $p->qty;
    }
    $contract_product->need_repair = $need_repair;
    $contract_product->save();
}
```

- [ ] **Step 2: Đảm bảo `$p` có `firm_contract_tab_product_id`.** Truy nguồn `$p` (ProductExportTab products khi build phiếu xuất từ yêu cầu xuất); nếu chưa carry field từ `ProductExportRequestTabProduct` → bổ sung copy field tại chỗ build (tìm + sửa, ghi rõ file+dòng).
- [ ] **Step 3: `php -l`** → sạch.

### Task 2.3: Refactor attribution về `ProductExportRequestTabProduct`

**Files:**
- Modify: `app/Model/Warehouse/ProductExport.php` (dòng ~1691-1702)

- [ ] **Step 1:** đoạn cộng `productExportRequestTabProduct->exported_qty` — đổi match sang `firm_contract_tab_product_id` (ưu tiên) fallback khóa cũ.
- [ ] **Step 2: `php -l`** → sạch.

### Task 2.4: Refactor `WarehouseExportRequest` match theo id dòng

**Files:**
- Modify: `app/Model/Warehouse/WarehouseExportRequest.php` (~dòng 943-954)

- [ ] **Step 1:** áp pattern ưu-tiên-id-fallback-khóa-cũ như Task 2.2 Step 1 (chỉ cộng `warehouse_exported_qty`).
- [ ] **Step 2: `php -l`** → sạch.

---

## Phase 3 — BE store/update cha-con (báo giá + carryover HĐ)

### Task 3.1: Lưu cha-con khi store/update báo giá

**Files:**
- Modify: `app/Services/Sale/Firm/FirmQuotationService.php` (method `syncProducts`, ~dòng 345-387)

**Interfaces — Consumes:** mỗi product request thêm `tmp_row_id` (id tạm FE), `child_parent_tmp_id` (tmp dòng cha), `child_ratio`.
**Produces:** dòng con lưu `child_parent_id` = id thật dòng cha.

- [ ] **Step 1: Map tmp→real, cha trước con.** FE đảm bảo cha đứng trước con (Task 4.2). Trong vòng lặp:

```php
$tmpToReal = [];
foreach ($products as $pro) {
    unset($pro['child_parent_id']); // tránh fill nhầm id tạm
    $p = new $model_class;
    $p->fill($pro);
    $p->parent_id = $parent_id;
    $p->firm_quotation_id = $firm_quotation_id;
    // ... logic cũ (unit_coefficient, total_cost, product_name...) ...
    $p->child_ratio = !empty($pro['child_ratio']) ? (int) $pro['child_ratio'] : null;
    if (!empty($pro['child_parent_tmp_id']) && isset($tmpToReal[$pro['child_parent_tmp_id']])) {
        $p->child_parent_id = $tmpToReal[$pro['child_parent_tmp_id']];
    } else {
        $p->child_parent_id = null;
    }
    $p->save();
    if (!empty($pro['tmp_row_id'])) {
        $tmpToReal[$pro['tmp_row_id']] = $p->id;
    }
}
```

- [ ] **Step 2: `php -l`** → sạch.

### Task 3.2: Validate cha-con khi store/update báo giá

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/FirmQuotationController.php` (store ~127-206, update ~258-349)

- [ ] **Step 1: Thêm rule + check logic** (rethrow ValidationException):

```php
'tabs.*.products.*.child_ratio' => 'nullable|integer|min:1',
```
+ check thủ công: product có `child_parent_tmp_id` → `child_ratio` required ≥ 1; cấm cấp 3 (dòng được trỏ làm cha không được đồng thời có `child_parent_tmp_id`). Vi phạm → `throw ValidationException::withMessages([...])`.

- [ ] **Step 2: `php -l`** → sạch.

### Task 3.3: Carryover cha-con BG → HĐ (remap id)

**Files:**
- Modify: `app/Services/Sale/Firm/Contract/FirmContractService.php` (method `syncTabsFromQuotation`, ~dòng 605-702)

**Interfaces — Consumes:** mỗi product HĐ có `firm_quotation_tab_product_id` (id dòng BG gốc).
**Produces:** dòng con HĐ có `child_parent_id` = id dòng cha HĐ; `child_ratio` copy từ BG.

- [ ] **Step 1: Build map id BG → id HĐ.** Sau `$firm_contract_product->save();`, lưu `$quotationToContract[$firm_quotation_product->id] = $firm_contract_product->id;` và giữ tham chiếu `$contractByQuotationId[$firm_quotation_product->id] = $firm_contract_product;`. **Đảm bảo lượt 1 KHÔNG mang `child_parent_id` của BG** (unset trước fill/attributesToArray).

- [ ] **Step 2: Lượt 2 set child_parent_id** (sau khi lưu hết tab/product):

```php
foreach ($contractByQuotationId as $qId => $contractProduct) {
    $qProduct = FirmQuotationTabProduct::find($qId);
    if ($qProduct && $qProduct->child_parent_id
        && isset($quotationToContract[$qProduct->child_parent_id])) {
        $contractProduct->child_parent_id = $quotationToContract[$qProduct->child_parent_id];
        $contractProduct->child_ratio = $qProduct->child_ratio;
        $contractProduct->save();
    }
}
```

- [ ] **Step 3: `php -l`** → sạch.

### Task 3.4: HĐ khoá cấu trúc cha-con

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/FirmContractController.php` (store/update)

- [ ] **Step 1:** Cấu trúc cha-con HĐ CHỈ đến từ carryover BG (Task 3.3). Nếu request HĐ gửi `child_parent_id`/`child_ratio` không qua BG → bỏ qua, không cho đổi. Thêm chú thích.
- [ ] **Step 2: `php -l`** → sạch.

---

## Phase 4 — FE form Angular (báo giá + HĐ)

> Tìm path class HĐ tương ứng: `resources/views/partials/classes/sale/firm/contract/FirmContractTabProduct.blade.php`, `FirmContractTab.blade.php` (đối xứng với quotation). Xác nhận trước khi sửa.

### Task 4.1: Class product FE — thuộc tính cha-con + SL con auto

**Files:**
- Modify: `resources/views/partials/classes/sale/firm/quotation/FirmQuotationTabProduct.blade.php`
- Modify: `resources/views/partials/classes/sale/firm/contract/FirmContractTabProduct.blade.php`

**Interfaces — Produces:** product có `tmp_row_id`, `child_parent_tmp_id`, `child_ratio`; getter `is_child`; con: `quantity` auto = cha × ratio.

- [ ] **Step 1: BG product class** — trong `after()`: `this.tmp_row_id = form.tmp_row_id || randomString();` `this.child_parent_tmp_id = form.child_parent_tmp_id || null;` `this.child_ratio = form.child_ratio || null;`. Thêm:

```javascript
get is_child() { return !!this.child_parent_tmp_id; }
get quantity() {
    if (this.is_child) {
        let p = (this.parent.products || []).find(x => x.tmp_row_id == this.child_parent_tmp_id);
        return p ? (p._quantity || 0) * (this.child_ratio || 0) : 0;
    }
    return this._quantity || 0;
}
```
(Kiểm `quantity` cũ là getter/field — nếu đang dùng `this.quantity` làm field thì chuyển sang `_quantity` backing để không vỡ binding.)

- [ ] **Step 2: HĐ product class** — áp tương tự (HĐ load từ BG; `child_parent_tmp_id` map ở Task 4.4).
- [ ] **Step 3:** mở form BG + HĐ trên browser, console JS sạch.

### Task 4.2: Tab class — loại con khỏi tổng + addChild/removeChild

**Files:**
- Modify: `resources/views/partials/classes/sale/firm/quotation/FirmQuotationTab.blade.php`
- Modify: `resources/views/partials/classes/sale/firm/contract/FirmContractTab.blade.php`

- [ ] **Step 1: Sửa getter tổng** (`total_cost`, `vat_cost`, `cost_after_vat`) — chỉ cộng dòng KHÔNG phải con:

```javascript
get total_cost() {
    return roundNumber(this.products.filter(p => !p.is_child)
        .reduce((acc, cur) => acc + cur.total_cost, 0), 0);
}
```
(áp tương tự `vat_cost`, `cost_after_vat`.)

- [ ] **Step 2: `addChild`** — chèn con ngay sau cha (và sau các con hiện có của cha):

```javascript
addChild(parentProduct, childData, ratio) {
    let child = new FirmQuotationTabProduct(childData, this);
    child.child_parent_tmp_id = parentProduct.tmp_row_id;
    child.child_ratio = ratio || 1;
    let idx = this._products.indexOf(parentProduct);
    let insertAt = idx + 1;
    while (insertAt < this._products.length
           && this._products[insertAt].child_parent_tmp_id == parentProduct.tmp_row_id) {
        insertAt++;
    }
    this._products.splice(insertAt, 0, child);
    this.parent.calculateProducts();
}
```
(HĐ tab dùng class HĐ tương ứng.)

- [ ] **Step 3: `removeProduct`** — khi xoá cha, xoá luôn con (`child_parent_tmp_id == parent.tmp_row_id`) trước/cùng lúc.
- [ ] **Step 4:** browser console sạch.

### Task 4.3: UI bảng báo giá — nút "+ con" + render gom nhóm

**Files:**
- Modify: `resources/views/sale/firm/quotations/form.blade.php` (bảng hàng ~377-479)
- Modify: `resources/views/sale/firm/quotations/formJs.blade.php` (thêm `openChildPicker`/`addChildProduct`)

- [ ] **Step 1: Render con thụt lề** — sửa `<tr ng-repeat>`:

```html
<tr ng-repeat="(indexP, product) in tab.products"
    ng-class="{'odd-row': $index % 2 == 0, 'child-row': product.is_child, 'invalid': !form.checkValidTabProduct(product)}">
```
Ô tên hàng thụt lề khi con (`ng-style="product.is_child && {'padding-left':'30px'}"`). Ô SL: con hiển thị `<% product.quantity %>` read-only (không input); thêm ô tỉ lệ con `<input ng-model="product.child_ratio" ng-if="product.is_child" class="form-control only-number">`.

- [ ] **Step 2: Nút "+ con"** trên dòng cha:

```html
<button type="button" class="btn btn-xs btn-info" ng-if="!product.is_child && !form.isShow"
        ng-click="openChildPicker(tab, product)">+ con</button>
```

- [ ] **Step 3: formJs** — `openChildPicker(tab, parentProduct)` mở modal chọn sản phẩm (tái dùng modal chọn hàng có sẵn); chọn xong gọi `tab.addChild(parentProduct, data, 1)`. Thêm CSS `.child-row { background: #f7fbff; }`.

- [ ] **Step 4: browser test** — thêm cha → "+ con" → chọn mã + tỉ lệ → SL con = SL cha × tỉ lệ; sửa SL cha → con đổi; tổng KHÔNG cộng con; xoá cha → con biến mất.

### Task 4.4: UI bảng HĐ + carryover hiển thị + khoá cha-con

**Files:**
- Modify: `resources/views/sale/firm/contracts/form.blade.php` (bảng hàng ~505-567)
- Modify: `resources/views/sale/firm/contracts/formJs.blade.php` (`selectQuotation`/`addQuotationParent`)

- [ ] **Step 1: Map id BG → tmp khi nạp HĐ.** Trong `selectQuotation`, dựng products với `tmp_row_id` từ id dòng BG; `child_parent_tmp_id` = tmp của dòng cha (map `firm_quotation_tab_product_id` cha → tmp). Đảm bảo `is_child`/`quantity` chạy.
- [ ] **Step 2: Render gom nhóm** giống 4.3 Step 1. **KHOÁ**: KHÔNG nút "+ con", tỉ lệ read-only.
- [ ] **Step 3: browser test** — lập HĐ từ BG cha-con → cụm hiển thị đúng, SL con đúng, tổng theo cha, không sửa cấu trúc.

### Task 4.5: Submit — gửi cha-con xuống BE

**Files:**
- Modify: `resources/views/sale/firm/quotations/formJs.blade.php`
- Modify: `resources/views/sale/firm/contracts/formJs.blade.php`

- [ ] **Step 1:** serialize product gửi BE kèm `tmp_row_id`, `child_parent_tmp_id`, `child_ratio`; cha đứng trước con.
- [ ] **Step 2: browser test** — submit BG cha-con, Network payload đủ field; kiểm DB (log/tinker readonly) dòng con `child_parent_id` đúng.

---

## Phase 5 — Quỹ xuất hàng (yêu cầu xuất)

### Task 5.1: Service tính "còn được xuất" theo cụm cha-con

**Files:**
- Modify: `app/Services/Sale/Firm/Contract/FirmContractProductExportService.php` (`getDataForWarehouseExport` ~26-178; build dòng ~359)

**Interfaces — Produces:** dòng trả FE có `qty` (còn được xuất, cha-con aware) + `firm_contract_tab_product_id`, `child_parent_id`, `child_ratio`.

- [ ] **Step 1: Hàm tính remaining cụm:**

```php
private function calcChildAwareRemaining($products) // Collection<FirmContractTabProduct> của 1 HĐ
{
    $childrenByParent = $products->filter(fn($p) => $p->child_parent_id)
        ->groupBy('child_parent_id');
    $remaining = [];
    foreach ($products as $p) {
        if ($p->child_parent_id) continue; // xử lý ở cụm cha
        $children = $childrenByParent->get($p->id, collect());
        if ($children->isEmpty()) {
            $remaining[$p->id] = max(0, $p->quantity - $p->exported_qty);
            continue;
        }
        $a = $p->exported_qty; $Q = $p->quantity; $maxChild = 0;
        foreach ($children as $c) {
            $maxChild = max($maxChild, $c->child_ratio > 0 ? $c->exported_qty / $c->child_ratio : 0);
        }
        $remaining[$p->id] = max(0, $Q - $a - $maxChild);
        foreach ($children as $c) {
            $remaining[$c->id] = max(0, ($Q * $c->child_ratio) - $c->exported_qty - ($c->child_ratio * $a));
        }
    }
    return $remaining;
}
```

- [ ] **Step 2:** Dùng map remaining gán vào `qty` từng dòng (thay `quantity - exported_qty` ở ~165/~359), vẫn trừ tiếp `join_exporting_qty`.
- [ ] **Step 3:** Dòng trả FE giữ `firm_contract_tab_product_id` (dòng 359) + thêm `child_parent_id`, `child_ratio`.
- [ ] **Step 4: `php -l`** → sạch.

### Task 5.2: Validate quỹ khi store yêu cầu xuất

**Files:**
- Modify: `app/Http/Controllers/Warehouse/ProductExportRequestsController.php` (store ~373; validate ~408-418)

- [ ] **Step 1: Validate BE** — load HĐ + dòng, tính remaining (Task 5.1), đối chiếu mỗi `tabs.*.products.*.qty` (cộng dồn dòng cùng cụm) ≤ remaining; thêm ràng buộc cụm `a + max_i((delivered_i + qty_i)/r_i) ≤ Q` cho cha. Vượt → `throw ValidationException::withMessages([...])` chỉ rõ dòng.
- [ ] **Step 2:** Xác nhận `syncTabProducts` nhận `firm_contract_tab_product_id` (Task 2.1) + FE gửi (Task 5.3).
- [ ] **Step 3: `php -l`** → sạch.

### Task 5.3: FE yêu cầu xuất — hiển thị "còn được xuất" + chặn vượt + gửi id dòng

**Files:**
- Modify: blade + js màn tạo yêu cầu xuất hàng từ HĐ (tìm trong `resources/views/warehouse/`, dùng `getDataForWarehouseExport`).

- [ ] **Step 1:** Giữ danh sách phẳng (không gom nhóm). Cột "còn được xuất" = `qty` từ service. Input SL ≤ `qty`; vượt → lỗi inline + chặn submit.
- [ ] **Step 2:** Payload submit gửi `firm_contract_tab_product_id` mỗi dòng.
- [ ] **Step 3: browser test** — yêu cầu xuất từ HĐ cha-con: xuất B=4 → A còn 0, C còn 4 (đúng bảng ví dụ); nhập vượt bị chặn.

### Task 5.5: FE carry `firm_contract_tab_product_id` vào payload phiếu xuất kho *(phát sinh từ Phase 2b)*

**Files:**
- Modify: FE tạo phiếu xuất kho (ProductExport/WarehouseExport) — màn build payload `tabs[].products[]` từ dữ liệu yêu cầu xuất; + BE serve dữ liệu yêu cầu xuất cho màn này (nếu chưa trả `firm_contract_tab_product_id`).

> Phase 2b đã thêm cột `firm_contract_tab_product_id` vào `product_export_tab_products`/`warehouse_export_tab_products` + lưu ở `syncTabProducts`. Nguồn `product_export_request_tab_products` đã có cột (Task 2.1). Cần FE phiếu xuất kho gửi field này mỗi product. Hiện có bridge fallback nên KHÔNG regression; task này để đạt attribution chính xác tuyệt đối khi 2 con trùng (product_id,unit_id) cùng tab.

- [ ] **Step 1:** Tìm màn/JS tạo phiếu xuất kho từ yêu cầu xuất; đảm bảo mỗi product trong payload có `firm_contract_tab_product_id` (lấy từ dữ liệu yêu cầu xuất). Sửa BE serve data nếu thiếu.
- [ ] **Step 2: browser test** — tạo phiếu xuất kho từ HĐ cha-con (2 con trùng mã cùng tab); kiểm `product_export_tab_products.firm_contract_tab_product_id` đúng; exported_qty cộng đúng dòng.

### Task 5.4: Chặn giảm SL cha dưới mức đã xuất quy đổi khi sửa HĐ

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/FirmContractController.php` (update) hoặc `FirmContractService`

- [ ] **Step 1:** Update HĐ, dòng cha có cụm: `Q_min = a + max_i(delivered_i/r_i)`; `quantity` mới < `Q_min` → `ValidationException`. Con: cần `Q*r_i ≥ delivered_i + r_i*a`.
- [ ] **Step 2: `php -l`** → sạch.

---

## Phase 6 — Bản in (chỉ in cha)

### Task 6.1: Bản in báo giá lọc bỏ con

**Files:**
- Modify: builder HTML bảng hàng báo giá in. **Xác định chính xác** nguồn products cho `resources/views/sale/firm/quotations/partials/pdf.blade.php` (khảo sát chỉ `app/Quotation.php::getProductTableAttribute` — xác nhận đúng model dùng cho FirmQuotation; nếu khác, sửa đúng nơi).

- [ ] **Step 1:** Trong vòng lặp render dòng, bỏ qua dòng `child_parent_id != null` (chỉ in cha).
- [ ] **Step 2: `php -l`** file sửa → sạch.
- [ ] **Step 3: browser test** — in báo giá cha-con → chỉ thấy cha.

### Task 6.2: Bản in hợp đồng lọc bỏ con (nếu có)

**Files:**
- Tìm bản in/Excel HĐ hãng. Khảo sát ban đầu: **chưa có bản in HTML riêng** cho HĐ hãng.

- [ ] **Step 1:** Nếu có route/blade/Excel in HĐ → lọc bỏ dòng `child_parent_id != null`. Nếu KHÔNG có → đánh dấu N/A, ghi rõ trong checkpoint.

---

## Phase 7 — Rà soát & nghiệm thu

- [ ] **Task 7.1:** `php -l` toàn bộ file đã sửa → sạch.
- [ ] **Task 7.2:** Chạy tay 6 kịch bản bảng ví dụ (design.md mục 6) trên 1 HĐ test (A=2,B=4,C=4), xác nhận "còn được xuất" khớp.
- [ ] **Task 7.3:** Legacy-safe: 1 HĐ KHÔNG cha-con → xuất hàng, `exported_qty` vẫn đúng (fallback khóa cũ).
- [ ] **Task 7.4:** Edge: mã con trùng ở 2 cụm → 2 dòng, quỹ riêng; xuất con lệch → `max(delivered_i/r_i)` đúng.
- [ ] **Task 7.5:** Migrate trên server (3 migration) + smoke test E2E (BG → HĐ → yêu cầu xuất → xuất kho → in).

---

## Checkpoint

### Checkpoint — 2026-06-20 (Phase 1 xong)
Vừa hoàn thành: **Phase 1 (Task 1.1/1.2/1.3)** — 3 migration (`2026_06_20_100001/100002/100003`) + thêm `child_parent_id`,`child_ratio` vào $fillable + `children()`/`childParent()` ở `FirmQuotationTabProduct` & `FirmContractTabProduct`. `php -l` sạch 5 file. Review working-tree: PASS. CHƯA migrate (chạy trên server khi deploy).
Đang làm dở: chuẩn bị Phase 2 (refactor attribution exported_qty → id dòng).
Bước tiếp theo: Task 2.1–2.4.
Blocked: —

**Ledger:**
- Phase 1 (T1.1, T1.2, T1.3): ✅ complete (review clean, không commit theo quy tắc dự án)
- Phase 2 (T2.1–2.4) + 2b: ✅ complete. Thêm migration `2026_06_20_100004` (cột `firm_contract_tab_product_id` vào `product_export_tab_products`+`warehouse_export_tab_products`). Sửa `ProductExportRequestTab`, `ProductExportTab`, `WarehouseExportTab` (lưu cột), `ProductExport::syncFirmContractTabProducts` + `WarehouseExportRequest` (attribution ưu tiên id → bridge → khóa cũ). `php -l` sạch. Review PASS. **Phát sinh Task 5.5** (FE phiếu xuất kho carry cột — bridge fallback nên chưa regression).

- Phase 3 (T3.1–3.4): ✅ complete. `FirmQuotationService::syncProducts` map tmp→real (path thật `app/Services/Sale/Firm/Quotation/`); validate trong `CreateFirmQuotationRequest`/`UpdateFirmQuotationRequest` (rule + check cấp 3); `FirmContractService::syncTabsFromQuotation` unset id BG lượt 1 + remap lượt 2; `FirmContractController` thêm comment khoá (request không set 2 cột). `php -l` sạch 5 file. Review PASS. Note: `syncGroupsFromQuotation` (group dự án) chưa carryover — ngoài scope hãng.

- Phase 4a (T4.1, T4.2): ✅ complete. Class product BG+HĐ: thêm `tmp_row_id`/`child_parent_tmp_id`/`child_ratio`/`is_child`/`_effective_quantity`; con SL auto = cha×ratio (BG: prototype getter; HĐ: `Object.defineProperty` trong after() — con HĐ phải tạo kèm child_parent_tmp_id trong childData). `submit_data` đã gắn 3 field cha-con + dùng `_effective_quantity` → **Task 4.5 (submit) coi như đã xử lý ở class, chỉ cần verify form submit dùng submit_data**. Tab BG+HĐ: mọi getter tổng `.filter(p=>!p.is_child)`; thêm `addChild`/`removeProduct` (xoá cha → xoá con). `php -l` blade sạch.
  - ⚠️ **FLAG verify browser:** (1) tổng HĐ nhánh thường dùng `_total_cost` snapshot — xác nhận loại con đúng; (2) cơ chế `Object.defineProperty` quantity cho con HĐ — xác nhận hiển thị đúng.

- Phase 4b (T4.3, T4.4, T4.5): ✅ complete.
  - Báo giá: `form.blade.php` (child-row, thụt lề, ô tỉ lệ input, nút "+con"); `formJs.blade.php` (`openChildPicker` + wrap `addProduct` tái dùng modal chọn SP); `FirmQuotationTabProduct::getDataForQuotationEdit()` override append tmp_row_id/child_parent_tmp_id/child_ratio (parent method tồn tại ở BaseQuotationProduct:97; dùng cả edit-load lẫn getDataForContract).
  - HĐ: `form.blade.php` (child-row, thụt lề, nhãn tỉ lệ read-only, ẩn nút xoá con); `FirmContractService::getDataForEdit` map tmp_row_id/child_parent_tmp_id (gọi từ FirmContractController:323). `selectQuotation` giữ field qua constructor (không cần sửa).
  - Submit (T4.5): `submit_data` class đã gắn field cha-con + dùng `_effective_quantity` → đã xử lý.
  - `php -l` sạch.
  - ⚠️ **FLAG (hỏi/verify sau):** (1) màn XEM HĐ (getDataForShow) chưa map cha-con → con hiện phẳng khi view; (2) dòng con HĐ vẫn có input `total_extra_cost`/`discount` (vô hại vì bị loại khỏi tổng, có thể khoá nếu muốn). Đều KHÔNG chặn.

- Phase 5 BE (T5.1, T5.2, T5.4): ✅ complete. `FirmContractProductExportService::calcChildAwareRemaining()` (public, đúng công thức, legacy-safe) + tích hợp vào `getDataForWarehouseExport` (qty=remaining cha-con, giữ `firm_contract_tab_product_id`, thêm child_parent_id/child_ratio). `ProductExportRequestsController::store` validate quỹ (gom theo fctp_id, throw ValidationException; skip nếu FE chưa gửi fctp_id). `FirmContractController::update` chặn giảm SL cha < Q_min. `php -l` sạch. Review PASS. Minor: 1 ternary thừa.
  - **Phụ thuộc:** FE yêu cầu xuất phải gửi `firm_contract_tab_product_id` (T5.3) để validate có hiệu lực.

- Phase 5 FE (T5.3, T5.5) — opus: ✅ complete. Payload `firm_contract_tab_product_id` đã có sẵn ở `submit_data` các class warehouse + 3 method serve BE → T5.5 không cần thêm. T5.3 sửa `ProductExportRequestTabProduct.blade.php`: `max_export_qty=form.qty` (remaining BE), getter `max_allowed_qty` (ưu tiên BE, fallback cũ), setter clamp. `php -l` sạch. Review PASS.
- Phase 6 (T6.1, T6.2) — opus: ✅ complete. Builder thật: `FirmQuotationPrint` (5 method, gồm Excel) + `FirmContractPrint` (3 nhánh). Skip `child_parent_id != null` đầu mỗi loop; STT đổi sang counter thủ công (không nhảy số). Filter chỉ theo child_parent_id → an toàn loại báo giá/HĐ khác. `php -l` sạch. Review PASS. Concern: `ZTFirmContractPrint` + Excel export HĐ chưa lọc (ngoài scope ZT).
- Task 7.1: ✅ `php -l` 28 file (24 sửa + 4 migration) — TẤT CẢ SẠCH.

- Review tổng cuối (opus) + fix: ✅ done. **Critical #1** (tổng tiền HĐ phồng tiền con ở `syncTabsFromQuotation`) — ĐÃ SỬA: loại con khỏi `total_extra`/`total_product_cost` (vẫn save dòng con + remap chạy). **#3** ép `SL con = SL cha × tỉ lệ` server-side ở `syncProducts`. Minor #6 (ternary thừa) + #7 (comment sai) dọn. `php -l` sạch. Critical #2 (validate chỉ XUAT_BAN_HD_HANG) — chấp nhận: KM dùng combo riêng, cha-con chỉ rút qua XUAT_BAN_HD_HANG.

### Checkpoint — 2026-06-20 (CODE + REVIEW + smoke-test DONE)
Vừa hoàn thành: Phase 1–6 + review cuối + fix. `php -l` sạch 28 file. **Đã migrate 4 file trên LOCAL `dev_erp_2`** (local KHÔNG trỏ prod — memory cũ sai, đã sửa). **T7.2 ✅: tinker test `calcChildAwareRemaining` — cả 6 kịch bản (chua xuat/B=4/B=4,C=4/A=1/B=2/A=2) KHỚP CHÍNH XÁC bảng design §6.** KHÔNG commit.
Bước tiếp theo: USER test browser FE (mục ⚠️ verify 2,3,4,5,7 — UI Angular không tự test được) + migrate trên SERVER prod khi deploy.

**Đã verify runtime trên `dev_erp_2` (tinker, rollback):**
- T7.2 ✅ `calcChildAwareRemaining`: 6/6 kịch bản khớp design §6.
- FIX #3 ✅ `syncProducts`: cha qty=2 → con ép qty=4 (ratio2)/qty=6 (ratio3) dù FE gửi 999; `child_parent_id` remap tmp→real id đúng. (product 3895/3896/3897, FQ 2016, rollback sạch.)

**Chưa verify runtime (drive tinker dễ fatal do tính giá/deps; test trên browser E2E):**
- Critical #1 (carryover tổng HĐ loại con) → lập HĐ từ BG cha-con, xem tổng tiền = chỉ cha.
- Attribution `exported_qty` 2 con trùng mã → xuất hàng, xem cộng đúng dòng.
Blocked: —

### Checkpoint — 2026-06-22 (loạt fix FE/BE sau test browser — Fix #4→#18)
Nhánh: `hop_dong_cha_con`. **KHÔNG commit.** Tất cả thay đổi đang ở working tree (28 file M + 4 migration ??).
Vừa hoàn thành (mỗi mục có entry chi tiết ở phần "Fix #N" trên):
- #4 bug nút "+con" thêm nhầm thành cha (formJs `$scope.addProduct` trùng định nghĩa).
- #5 UX cột tỉ lệ + chặn vỡ nhóm khi kéo-thả (normalizeChildOrder).
- #6 DUYỆT báo giá SQL `Unknown column 'child_ratio'` (syncProducts chỉ gán child cols cho TabProduct) + #2 FE bỏ con khỏi groups (tạm).
- #7 màn TẠO HĐ từ BG không hiện cha-con (getDataForContract map tmp_row_id/child_parent_tmp_id).
- #8 JS "Cannot redefine property: quantity" (FirmContractTabProduct: bỏ 'quantity' khỏi number, dùng class get/set).
- #9 HĐ phân bổ vượt trội/giảm giá chỉ cho cha (allocationExtraCost/allocationDiscountCost), con vẫn nhập tay.
- #10 màn xuất hàng VAT options lấy từ `firm_contract_tab_products` (gồm con) — không từ groups.
- #11 HĐ bảng chính: dòng con mọi cột "thành tiền" = 0 (display), giữ đơn giá+SL; export định giá con bình thường (price×qty).
- #12 màn CHI TIẾT (show) HĐ map cha-con (getDataForShow); báo giá form_show hiện cha-con (indent/└/tỉ lệ).
- #13 REVERT: con vào lại tab tổng hợp VAT (groups); báo giá tổng `total_product_cost/vat` chuyển sang tabs (parent-only).
- #14 HĐ tab tổng hợp VAT: group product con → thành tiền = 0 (FirmContractGroupProduct.is_child).
- #15 quỹ cha-con trừ pending (in-flight) — `calcChildAwareRemaining($products,$pendingByRowId)` consumed=exported+pending; helper `getInFlightQtyByKey`.
- #16 validate bất biến cụm (cha+con cùng lúc) — `calcChildAwareRemaining(...,$clamp=false)`, remaining thô <0 ⇒ chặn (store).
- #17 validate cả màn SỬA (update) — `getInFlightQtyByKey(...,$excludeRequestId=$object->id)` loại trừ chính nó.
- #18 validate trả HTTP 200 + `responseErrors` (message rõ) thay vì `throw ValidationException` (422 → "Đã có lỗi xảy ra").
- Data dev_erp_2: thêm `EmployeeManageDepartment(emp 13, dept 43, c1)` để emp 13 (namdangit@gmail.com) duyệt được yêu cầu xuất #1038 (TP duyệt).
Đang làm dở: — (loạt fix trên đã xong từng phần, `php -l` sạch các file BE; FE blade chưa test browser).
Bước tiếp theo: USER test browser toàn bộ luồng (BG→HĐ→xuất hàng cha-con) trên `dev_erp_2`; các mục [ ] "Verify browser" trong từng Fix #N.
Blocked: —

## ⚠️ Cần verify khi test (browser/runtime — chưa kiểm được tĩnh)
1. Tổng tiền HĐ có cụm cha-con = chỉ cha (sau fix #1). So tổng in (chỉ cha) vs tổng lưu DB.
2. EDIT lại HĐ/BG đã lưu → cụm cha-con hiển thị đúng, SL con auto, thứ tự cha trước con (getter con tìm được cha).
3. `Object.defineProperty` quantity con HĐ hiển thị đúng.
4. Màn yêu cầu xuất: xuất B=4 → A còn 0, C còn 4 (bảng ví dụ design §6); nhập vượt bị chặn (FE+BE).
5. Phiếu xuất kho: 2 con trùng mã cùng tab → `firm_contract_tab_product_id` + exported_qty cộng đúng dòng.
6. Cụm cha-con có nằm cùng 1 tab không (calcChildAwareRemaining filter theo tab_ids) + màn xuất load đủ cụm.
7. Bản in BG + HĐ chỉ in cha; STT không nhảy số.
8. Legacy: HĐ/BG KHÔNG cha-con chạy y như cũ (xuất kho, attribution, tổng tiền).

## Fix #4 — Bấm "+con" thêm nhầm thành hàng cha (BG hãng)
- [x] Root cause: `formJs.blade.php` định nghĩa `$scope.addProduct` 2 lần — bản child-aware (dòng 57–105) bị bản phẳng (dòng 152–186) định nghĩa SAU ghi đè; `_addProductOriginal` cũng capture sai vì chạy trước bản phẳng.
- [x] Sửa: chuyển khối wrapper (57–105) xuống sau bản phẳng → `_addProductOriginal` = bản phẳng, `$scope.addProduct` = bản child-aware.
- [ ] Verify browser: bấm "+con" → hàng con thụt lề dưới cha, không nhảy thành dòng cha.

## Fix #5 — UX cột tỉ lệ + chặn vỡ nhóm khi kéo-thả (BG hãng)
- [x] Tách "Tỉ lệ" thành **cột riêng** trên bảng hàng hoá BG hãng, đặt **trước cột SL**: header `<th>Tỉ lệ</th>` (width 110px), ô con = `×` tách rời + ô số (flex căn giữa dọc/ngang, gap 8px, input 60px — bỏ input-group cho gọn), dòng cha/độc lập = `-`; cột SL hàng con = span readonly; colspan no-data 13→14; border-left `.child-row`. Chỉ áp `form.blade.php` (màn XEM `form_show` vẫn hiện con phẳng — giới hạn cũ).
- [x] Kéo-thả: thêm `normalizeChildOrder(tab)` ép con luôn nằm ngay dưới cha sau khi drop (giữ gom nhóm); gắn `ui-sortable="productSortableOptions"` cho cả 2 tbody. Data vốn an toàn (con tìm cha qua `child_parent_tmp_id`, không theo vị trí) — fix chỉ để không vỡ bố cục hiển thị.
- [ ] Verify browser: kéo con ra chỗ khác → snap về dưới cha; kéo cha → con đi theo; tỉ lệ hiển thị dạng `× N`.

## Fix #6 — Duyệt báo giá lỗi SQL "Unknown column 'child_ratio'" (group_products)
- [x] Root cause: `FirmQuotationService::syncProducts()` dùng chung cho cả `FirmQuotationTabProduct` (bảng có cột child) và `FirmQuotationGroupProduct` (bảng `firm_quotation_group_products` summary gộp VAT — KHÔNG có cột). Code luôn chạy `$p->child_ratio = ...` / `$p->child_parent_id = ...` (kể cả gán `null`) cho mọi dòng → Eloquent đưa 2 cột vào INSERT của group_products → lỗi.
- [x] Fix BE: bọc block gán cha-con trong `if ($model_class === FirmQuotationTabProduct::class)` — group_products không đụng cột child. (`php -l` sạch.)
- [x] Fix FE (đúng đắn): `groupByVatAndMerge` loại dòng con (`if (prod.is_child) return`) ở `FirmQuotation.blade.php` + `FirmContract.blade.php` → summary VAT chỉ gồm cha (không đội số tiền + không lưu con vào group_products). `calculateProducts()` rebuild groups mỗi lần đổi hàng + trong `submit_data`.
- [x] Contract an toàn sẵn: `syncGroupsFromQuotation` dùng `fill()` + đã `unset` child cols (dòng 694); chỉ tab products (bảng có cột) được gán.
- [ ] Verify browser: duyệt lại báo giá có cụm cha-con → không lỗi SQL; summary VAT/tổng tiền = chỉ cha.

## Fix #7 — Màn TẠO HĐ từ báo giá không hiển thị cấp cha-con
- [x] Root cause: `FirmQuotationService::getDataForContract()` không set `tmp_row_id`/`child_parent_tmp_id` cho tab products (khác `getDataForEdit` đã set). FE `FirmContractTabProduct.is_child` dựa vào `child_parent_tmp_id` → null → bảng HĐ hiện phẳng (mất indent/`└`/tỉ lệ). Display logic ở `contracts/form.blade.php` (child-row/indent/`└`/"(tỉ lệ N)") đã có sẵn, chỉ thiếu dữ liệu.
- [x] Fix BE: thêm map `tmp_row_id = (string)id` + `child_parent_tmp_id = (string)child_parent_id` cho mọi tab product trước `return` (mirror getDataForEdit). `php -l` sạch.
- [ ] Verify browser: tạo HĐ từ BG có cụm cha-con → con thụt lề dưới cha, hiện "(tỉ lệ N)", SL con = cha×tỉ lệ.

## Fix #8 — JS "Cannot redefine property: quantity" khi tạo/sửa HĐ cha-con
- [x] Root cause: `initGetSet` (app.js:782) tạo property qua `Object.defineProperty` KHÔNG `configurable` → 'quantity' (trong `this.number` của FirmContractTabProduct) thành non-configurable. `after()` lại `Object.defineProperty(this,'quantity')` để override cho dòng con → throw. Trước Fix #7, `child_parent_tmp_id` luôn null nên nhánh này không chạy; set xong thì lộ.
- [x] Fix (mirror báo giá): bỏ 'quantity' khỏi `this.number`; xoá block defineProperty trong `after()`; thêm class `get/set quantity()` (con = cha×tỉ lệ khoá sửa, thường = format `_quantity`). KHÔNG đụng `initGetSet` (hàm chung).
- [x] Đồng thời chữa crash khi EDIT HĐ cha-con (getDataForEdit cũng set child_parent_tmp_id).
- [ ] Verify browser: mở lại màn tạo HĐ từ BG cha-con → không còn lỗi console; SL con auto theo cha.

## Fix #9 — HĐ: tiền & phân bổ chỉ theo hàng cha
- [x] Getter tổng (tab: total_extra/total_discount/total_after_discount/cost_after_vat; grand: total_product_*) đã filter `!is_child` từ trước — tổng đã đúng theo cha.
- [x] `FirmContractTab.allocationExtraCost()`: phân bổ tự động doanh số vượt trội CHỈ rải cho cha (`!is_child`), KHÔNG đụng dòng con (giữ giá trị con để user tự nhập); bù lệch làm tròn chỉ vào cha.
- [x] `FirmContract.allocationDiscountCost()`: phân bổ tự động giảm giá tương tự — chỉ cha, không đụng con; bù lệch chỉ vào cha.
- [x] Per-row dòng con: GIỮ NGUYÊN — vẫn hiện các cột tiền theo dòng + ô nhập vượt trội/giảm giá cho phép user tự nhập tay.

## Fix #10 — Màn xuất hàng: không xuất được con có VAT khác mọi VAT cha (regression Fix #2)
- [x] Root cause: `getDataForWarehouseExport` (+ `getDataForBorrowSell`) lấy `vat_percent_options` từ `$contract->groups` (summary gộp VAT — Fix #2 đã loại con) → VAT riêng của con biến mất khỏi dropdown → không chọn xuất con được. `calcChildAwareRemaining` vốn tính trên TOÀN BỘ dòng HĐ (không lọc VAT) nên quỹ cha-con đúng bất kể batch VAT.
- [x] Giải pháp: lấy `vat_percent_options` = distinct `vat_percent` từ `firm_contract_tab_products` (gồm con) — đúng nguồn mà bộ lọc xuất `fctp.vat_percent` dùng. Con xuất ở batch VAT riêng, tách khỏi cha; xuất con → exported_qty con tăng → quỹ cha giảm. Sửa cả 2 site (xuất hàng + bán mượn). `php -l` sạch.
- [ ] Verify browser: HĐ có con VAT lệch cha → dropdown VAT hiện đủ; chọn VAT con → xuất con được; remaining con/cha trừ đúng theo design §6.

## Fix #11 — HĐ: dòng con thành tiền = 0 (chỉ hiện đơn giá + SL); export vẫn định giá con bình thường
- [x] Quyết định cuối: thay vì lọc con khỏi tổng nhiều nơi, dòng con trên BẢNG HĐ hiển thị mọi cột "thành tiền" = 0 (Thành tiền, Doanh số vượt trội, Thành tiền bán, Giảm giá, Thành tiền sau giảm, Thành tiền sau VAT), GIỮ đơn giá / đơn giá bán / đơn giá sau giảm / VAT% / SL / tỉ lệ.
- [x] FE `contracts/form.blade.php` bảng chính: bọc các ô amount bằng `ng-if` (cha → giá trị; con → `0`); ô nhập vượt trội/giảm giá ẩn ở con, hiện `0`.
- [x] Export KHÔNG đổi: `FirmContractProductExportService` tính `total_amount = fctp.price * qty` (đọc giá thật của con, không dùng total đã lưu) → xuất hàng con vẫn ra thành tiền = SL × đơn giá bình thường.
- [x] Tổng HĐ (tab + grand) vẫn parent-only (getter filter `!is_child` + con=0). Bảng nhóm giữ loại con (Fix #2). Báo giá giữ nguyên (groups loại con).
- [ ] Verify browser: HĐ — dòng con mọi cột tiền = 0, có đơn giá+SL+tỉ lệ; tổng = chỉ cha. Xuất hàng con → thành tiền = SL×đơn giá.

## Fix #12 — Màn CHI TIẾT (show) HĐ + báo giá không hiện cha-con
- [x] HĐ show: reuse `contracts/form.blade.php` (đã có cha-con + zero con) nhưng `FirmContractService::getDataForShow` chưa map `tmp_row_id`/`child_parent_tmp_id` → is_child=false → con phẳng. Fix: thêm map (giống getDataForEdit) trước `return`. KHÔNG cần làm lại HĐ (data `child_parent_id` đã lưu sẵn trong DB).
- [x] Báo giá show: data ĐÃ có `child_parent_tmp_id` (qua `getDataForQuotationEdit()` dòng 88-91), nhưng blade `form_show.blade.php` render phẳng. Fix blade: thêm `child-row`, thụt lề + `└`, hiện "(tỉ lệ N)" dưới SL, CSS `.child-row`. (Show báo giá: con vẫn hiện thành tiền theo dòng — không zero như HĐ.)
- [ ] Verify browser: mở chi tiết HĐ → con thụt lề, thành tiền=0, có đơn giá+SL+tỉ lệ; chi tiết báo giá → con thụt lề, có tỉ lệ.

## Fix #13 — Revert: con VÀO LẠI tab tổng hợp VAT (groups); tổng tách sang tabs (parent-only)
- [x] Bỏ `if (prod.is_child) return` trong `groupByVatAndMerge` ở CẢ FirmContract + FirmQuotation → con hiện lại trong tab tổng hợp theo VAT (đủ nhóm VAT của con, vd 8%).
- [x] Báo giá: chuyển `total_product_cost`/`total_product_vat` từ `groups.reduce` → `tabs.reduce` (tab.total_cost/vat_cost đã loại con) → tổng/thanh toán vẫn parent-only dù groups chứa con. Grand total (total_cost/vat/after_vat) + submit_data chain qua đây → OK.
- [x] Contract: tổng vốn từ tabs + field loaded (KHÔNG từ groups) nên chỉ cần revert exclusion, tổng không đổi.
- [x] An toàn: BE Fix #1 vẫn guard child cols ở group_products (không crash); export đã đọc tab_products VAT (Fix #10) nên không phụ thuộc groups. Per-group total trong summary có thể gồm con ("không quan trọng" theo yêu cầu).
- [ ] Verify browser: tab tổng hợp VAT (HĐ + báo giá) hiện nhóm VAT của con; tổng/thanh toán = chỉ cha; xuất hàng con vẫn OK.

## Fix #14 — HĐ tab tổng hợp VAT: thành tiền con vẫn ≠ 0
- [x] Root cause: sau Fix #13 con vào lại groups; `FirmContractGroupProduct` tính `total_cost = price × quantity` (gồm con) → tab tổng hợp HĐ hiện thành tiền con ≠ 0 (trái với HĐ phải = 0).
- [x] Fix: thêm getter `is_child` cho `FirmContractGroupProduct` (mọi `tab_products` đều là con) → zero `total_cost`/`total_extra`/`total_discount`/`total_cost_after_extra` cho group con. Giữ SL + đơn giá. Footer per-VAT-group (`group.total_cost` sum) → cũng loại con.
- [x] CHỈ contract (FirmContractGroupProduct); báo giá (FirmQuotationGroupProduct) giữ nguyên — summary báo giá vẫn hiện amount con. Groups recompute từ tabs (constructor) nên `tab_products` là instance có `is_child` → chạy đúng trên cả show.
- [ ] Verify browser: chi tiết HĐ → tab tổng hợp VAT: dòng con thành tiền = 0 (vẫn thấy SL + đơn giá), nhóm VAT con vẫn hiện; tổng VAT-group = chỉ cha.

## Fix #15 — Quỹ cha-con không trừ yêu cầu đang chờ xuất (pending) → vẫn xuất được con dù cha đã yêu cầu đủ
- [x] Root cause: `calcChildAwareRemaining` chỉ dùng `exported_qty` (cộng khi làm phiếu, KHÔNG phải lúc duyệt yêu cầu); pending trừ qua `join_exporting_qty` theo product_id+tab → cha & con khác product_id nên yêu cầu cha pending KHÔNG trừ quỹ con. Validate store còn không trừ pending nào.
- [x] Fix: `calcChildAwareRemaining($products, $pendingByRowId=[])` dùng `consumed = exported + pending`. Thêm helper `getInFlightQtyByKey()` (yêu cầu xuất bán + phiếu xuất + bán mượn in-flight) trả map theo product_id|tab|unit.
- [x] Áp ở DISPLAY (`getDataForWarehouseExport`: build pendingByRowId từ $tab_products, bỏ trừ join lần 2) + VALIDATE store (`ProductExportRequestsController:626`: pendingByRowId qua helper).
- [x] Verify runtime (tinker, synthetic): cha pending đủ → con remaining=0 (bị chặn); con pending đủ → cha=0; legacy/exported giữ đúng. `php -l` sạch 2 file.
- [ ] Verify browser: HĐ cha-con, tạo yêu cầu xuất CHA đủ Q (chưa làm phiếu) → tạo yêu cầu xuất CON bị chặn "vượt quỹ".

## Fix #16 — Validate xuất: cha+con cùng tab cùng lúc → vượt quỹ cụm (xuất gấp đôi)
- [x] Root cause: validate cũ kiểm tra TỪNG dòng (`req[cha] ≤ quỹ cha` và `req[con] ≤ quỹ con`) — mỗi cái lọt nhưng cộng lại vi phạm bất biến cụm `a + max(delivered_i/r_i) ≤ Q` → xuất cả cha lẫn con = gấp đôi quỹ.
- [x] Fix: `calcChildAwareRemaining(..., $clamp=false)` trả remaining THÔ (cho âm). Validate: cộng SL yêu cầu vào pending → tính remaining thô → bất kỳ dòng < 0 ⇒ chặn (`ProductExportRequestsController` store). Bắt cả vượt-dòng lẫn vượt-cụm.
- [x] Verify runtime (tinker): cha2+con4 cùng lúc→CHẶN; chỉ cha2/chỉ con4→OK; cha1+con2→OK; cha1+con3→CHẶN. `php -l` sạch.
- [ ] Verify browser: 1 yêu cầu chọn cả cha (đủ Q) + con (đủ Q×r) cùng tab VAT → bị chặn "vượt quỹ cha-con của cụm".
- Follow-up (UX, tùy chọn): FE màn yêu cầu xuất chưa trừ động (gõ SL cha → max con co lại); hiện chỉ BE chặn khi submit.

## Fix #17 — Validate quỹ cha-con cả màn SỬA yêu cầu xuất hàng (update)
- [x] Thêm validate bất biến cụm vào `ProductExportRequestsController::update` (mirror store, sau khối firm contract).
- [x] Khác store: yêu cầu đang sửa đã nằm trong pending → thêm param `$excludeRequestId` cho `getInFlightQtyByKey` (loại `per.id != $id` ở pr subquery), gọi với `$object->id` → không trừ trùng SL của chính nó.
- [x] `php -l` sạch 2 file.
- [ ] Verify browser: sửa yêu cầu xuất HĐ cha-con — giữ nguyên SL → lưu OK; tăng SL cha+con vượt quỹ cụm → bị chặn.

## Fix #18 — Validate quỹ trả "Đã có lỗi xảy ra" thay vì message rõ
- [x] Root cause: dùng `throw ValidationException` → HTTP 422 → FE rơi vào `error:` callback → toastr "Đã có lỗi xảy ra". Controller này theo convention trả HTTP 200 + `success=false` + `message` (FE đọc `response.success`).
- [x] Fix: đổi cả store + update sang `return $this->responseErrors($message, $errors)` (ResponseTrait, HTTP 200, success=false) → FE hiện `response.message` qua toastr.warning.
- [ ] Verify browser: tạo/sửa yêu cầu xuất vượt quỹ cụm → hiện thông báo "Số lượng xuất vượt quỹ giao của cụm hàng cha-con...".

## Follow-up minor (tùy chọn, chưa làm)
- FE inline validate tỉ lệ con (viền đỏ `is-invalid` khi tỉ lệ rỗng/0) — BE đã chặn `integer|min:1`.
- Màn XEM HĐ (getDataForShow) chưa map cha-con → con hiện phẳng khi view.
- Dòng con HĐ còn input `total_extra_cost`/`discount` (vô hại, bị loại khỏi tổng).
- ZTFirmContractPrint + Excel export HĐ chưa lọc con (ZT ngoài scope).
- Task 5.5: FE phiếu xuất kho payload `firm_contract_tab_product_id` — đã có sẵn (xác nhận khi test #5).
