# Plan — Chọn ĐVT khi tạo/sửa báo giá (hàng ERP)

> **Cho agentic worker:** thực thi theo từng task. Bước dùng checkbox `- [ ]`.
> Design: `design.md` · Spec: `docs/superpowers/specs/2026-07-12-quotation-unit-select-design.md`

**Goal:** Cho phép chọn ĐVT cho dòng hàng ERP ở màn Tạo/Sửa báo giá (type=2); đổi ĐVT → lấy lại giá bán + giá vốn theo đúng đơn vị.

**Architecture:** BE là nguồn chân lý giá ERP — thêm helper lấy giá theo đơn vị + endpoint list đơn vị; `saveDirectProduct` re-derive giá theo `unit_id`. FE render select ở cột ĐVT dòng ERP đủ điều kiện, đổi → quy đổi tỷ giá + làm tròn + recompute.

**Tech Stack:** Laravel 8 (PHP 7.4), MySQL cross-DB `mysql2` (ERP); Nuxt2/Vue2 (hrm-client).

## Global Constraints (verbatim từ spec)
- CHỈ báo giá **type=2 (SELF_BUILT)**. Type=1 (từ BOM) KHÔNG đụng.
- CHỈ **hàng ERP đơn**: `erp_product_id != null` AND `!is_parent_with_children` AND `parent_id == null` (loại combo cha-con).
- Dropdown = **tất cả `product_units`** của sản phẩm (thiếu giá bán lẻ → 0).
- Giá vốn (`cost_price`) gate quyền **"Xem giá vốn hàng hoá"** (BE trả null nếu không quyền).
- KHÔNG migration, KHÔNG permission mới. Dùng lại cột `unit_id` sẵn có.
- Verify BE bằng `php -l`; FE bằng E2E thủ công (dự án không có test tự động). KHÔNG commit git tự động — chỉ khi user yêu cầu.
- Data model ERP (`mysql2`): `product_units(product_id, unit_id, is_base, unit_coefficient, cost_price)` + `product_unit_prices(product_unit_id, price_type_id=1 retail, price)` + `units(id, name)`.

---

### Task 1: BE helper lấy đơn vị + giá theo đơn vị

**Files:**
- Modify: `hrm-api/Modules/Human/Entities/TpProductUnitPrice.php` (thêm 2 static method, cạnh `getRetailPrices`/`getCostPrices`)

**Interfaces:**
- Produces:
  - `getUnitOptions(array $erpProductIds): array` → `[erpId => [ ['unit_id'=>int,'unit_name'=>string,'is_base'=>int,'unit_coefficient'=>float,'retail_price'=>float,'cost_price'=>float], ... ]]`
  - `getUnitPrice(int $erpProductId, ?int $unitId): array` → `['cost_price'=>float,'retail_price'=>float]`

- [ ] **Step 1: Thêm `getUnitOptions`**

```php
/**
 * Danh sách đơn vị + giá bán lẻ + giá vốn theo TỪNG đơn vị của các sản phẩm ERP.
 * KHÔNG gate cost ở đây (helper thuần data — gate tại controller).
 * @return array [erp_product_id => array<array{unit_id,unit_name,is_base,unit_coefficient,retail_price,cost_price}>]
 */
public static function getUnitOptions(array $erpProductIds): array
{
    if (empty($erpProductIds)) {
        return [];
    }

    $db2 = env('DB_DATABASE_SECOND');
    $pu  = "{$db2}.product_units";
    $pup = "{$db2}.product_unit_prices";
    $u   = "{$db2}.units";

    $rows = DB::connection('mysql2')
        ->table("{$pu} as pu")
        ->join("{$u} as u", 'u.id', '=', 'pu.unit_id')
        ->leftJoin("{$pup} as pup", function ($j) {
            $j->on('pup.product_unit_id', '=', 'pu.id')->where('pup.price_type_id', 1);
        })
        ->whereIn('pu.product_id', $erpProductIds)
        ->orderBy('pu.product_id')
        ->orderByDesc('pu.is_base')
        ->orderBy('u.name')
        ->get([
            'pu.product_id', 'pu.unit_id', 'pu.is_base', 'pu.unit_coefficient',
            'pu.cost_price', 'u.name as unit_name', 'pup.price as retail_price',
        ]);

    $result = [];
    foreach ($rows as $r) {
        $result[(int) $r->product_id][] = [
            'unit_id'          => (int) $r->unit_id,
            'unit_name'        => $r->unit_name,
            'is_base'          => (int) $r->is_base,
            'unit_coefficient' => (float) ($r->unit_coefficient ?? 1),
            'retail_price'     => (float) ($r->retail_price ?? 0),
            'cost_price'       => (float) ($r->cost_price ?? 0),
        ];
    }
    return $result;
}
```

- [ ] **Step 2: Thêm `getUnitPrice`**

```php
/**
 * Giá (cost + retail) của ĐÚNG đơn vị $unitId cho 1 sản phẩm ERP.
 * $unitId null hoặc không khớp → fallback đơn vị cơ bản (is_base=1).
 * @return array{cost_price:float, retail_price:float}
 */
public static function getUnitPrice(int $erpProductId, ?int $unitId): array
{
    $db2 = env('DB_DATABASE_SECOND');
    $pu  = "{$db2}.product_units";
    $pup = "{$db2}.product_unit_prices";

    $q = DB::connection('mysql2')
        ->table("{$pu} as pu")
        ->leftJoin("{$pup} as pup", function ($j) {
            $j->on('pup.product_unit_id', '=', 'pu.id')->where('pup.price_type_id', 1);
        })
        ->where('pu.product_id', $erpProductId);

    if ($unitId) {
        $q->where('pu.unit_id', $unitId);
    } else {
        $q->where('pu.is_base', 1);
    }

    $row = $q->select('pu.cost_price', 'pup.price as retail_price')->first();

    // Không khớp unit_id → fallback base
    if (!$row && $unitId) {
        $row = DB::connection('mysql2')
            ->table("{$pu} as pu")
            ->leftJoin("{$pup} as pup", function ($j) {
                $j->on('pup.product_unit_id', '=', 'pu.id')->where('pup.price_type_id', 1);
            })
            ->where('pu.product_id', $erpProductId)
            ->where('pu.is_base', 1)
            ->select('pu.cost_price', 'pup.price as retail_price')
            ->first();
    }

    return [
        'cost_price'   => (float) ($row->cost_price ?? 0),
        'retail_price' => (float) ($row->retail_price ?? 0),
    ];
}
```

- [ ] **Step 3: Verify syntax**

Run: `cd hrm-api && php -l Modules/Human/Entities/TpProductUnitPrice.php`
Expected: `No syntax errors detected`

---

### Task 2: BE endpoint list đơn vị (gate giá vốn)

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (thêm method `erpProductUnits`)
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (thêm route trong nhóm quotations)

**Interfaces:**
- Consumes: `TpProductUnitPrice::getUnitOptions()` (Task 1)
- Produces: `POST /assign/quotations/erp-product-units` → `{ data: { <erpId>: [ {unit_id,unit_name,is_base,unit_coefficient,retail_price,cost_price} ] } }` (cost_price=null nếu thiếu quyền)

- [ ] **Step 1: Thêm method `erpProductUnits`**

```php
/**
 * Danh sách đơn vị + giá bán/giá vốn theo từng đơn vị của các sản phẩm ERP.
 * cost_price null nếu không có quyền "Xem giá vốn hàng hoá".
 */
public function erpProductUnits(Request $request)
{
    $ids = $request->input('erp_product_ids', []);
    if (!is_array($ids) || empty($ids)) {
        return response()->json(['data' => []]);
    }
    $ids = array_values(array_unique(array_map('intval', array_slice($ids, 0, 500))));

    $map = \Modules\Human\Entities\TpProductUnitPrice::getUnitOptions($ids);
    $canViewCostPrice = isCurrentEmployeeHasPermission('Xem giá vốn hàng hoá');

    if (!$canViewCostPrice) {
        foreach ($map as $erpId => $units) {
            $map[$erpId] = array_map(function ($u) {
                $u['cost_price'] = null;
                return $u;
            }, $units);
        }
    }

    return response()->json(['data' => $map]);
}
```

- [ ] **Step 2: Thêm route** (trong nhóm prefix `/assign/quotations`, cạnh `erp-product-search`)

```php
Route::post('/erp-product-units', [QuotationController::class, 'erpProductUnits']);
```

- [ ] **Step 3: Verify syntax**

Run: `cd hrm-api && php -l Modules/Assign/Http/Controllers/Api/V1/QuotationController.php && php -l Modules/Assign/Routes/api.php`
Expected: `No syntax errors detected` (cả 2 file)

- [ ] **Step 4: Kiểm route đăng ký**

Run: `cd hrm-api && php artisan route:list --path=assign/quotations/erp-product-units`
Expected: có dòng `POST ... assign/quotations/erp-product-units`

---

### Task 3: BE re-derive giá ERP theo unit_id khi lưu (type=2)

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` — `saveDirectProduct` (~dòng 1064-1133)

**Interfaces:**
- Consumes: `TpProductUnitPrice::getUnitPrice()` (Task 1)
- Thay đổi hành vi: dòng ERP **đơn** → `estimated_price`/`quoted_price` luôn re-derive theo `(erp_product_id, unit_id)` (create + update). Giữ `import TpProductUnitPrice` đã có sẵn ở đầu file.
- ⚠️ FE **KHÔNG** gửi `is_parent_with_children` trong payload → BE tự phát hiện "combo cha" bằng cách quét con trong `$products` ở `upsertDirectProducts`, truyền cờ `$hasChildren` vào `saveDirectProduct`.
- Thay đổi signature: `saveDirectProduct(Quotation $quotation, array $p, $overrideParentId, bool $hasChildren = false): int`

- [ ] **Step 1: `upsertDirectProducts` — tính tập cha-có-con + truyền cờ**

Trong `upsertDirectProducts`, trước 2 pass lưu, dựng set key cha có con (khớp cách con tham chiếu: `parent_id` số hoặc `parent_temp_id` chuỗi):

```php
// Tập "key cha có con" để loại combo khỏi việc đổi giá theo ĐVT.
$parentKeysWithChildren = [];
foreach ($products as $c) {
    if (!empty($c['parent_id']))      $parentKeysWithChildren['id:' . $c['parent_id']] = true;
    if (!empty($c['parent_temp_id'])) $parentKeysWithChildren['tmp:' . $c['parent_temp_id']] = true;
}
$hasChildrenOf = function (array $p) use ($parentKeysWithChildren) {
    if (!empty($p['price_id']) && isset($parentKeysWithChildren['id:' . $p['price_id']])) return true;
    if (!empty($p['temp_id'])  && isset($parentKeysWithChildren['tmp:' . $p['temp_id']]))  return true;
    return false;
};
```

Truyền vào 2 lời gọi `saveDirectProduct` (cả pass 1 và pass 2):
```php
$id = $this->saveDirectProduct($quotation, $p, null, $hasChildrenOf($p));           // pass 1
...
$id = $this->saveDirectProduct($quotation, $p, $resolvedParentId, $hasChildrenOf($p)); // pass 2
```

- [ ] **Step 2: `saveDirectProduct` — cờ ERP-đơn + hàm set giá theo unit**

Đổi signature + ngay sau khi tính `$isErp`, thêm:

```php
private function saveDirectProduct(Quotation $quotation, array $p, $overrideParentId, bool $hasChildren = false): int
{
    $isErp = !empty($p['erp_product_id']);
    // ERP đơn = ERP, KHÔNG phải con, KHÔNG phải cha có con (loại combo).
    $isChild = !empty($p['parent_id']) || !empty($p['parent_temp_id']) || $overrideParentId !== null;
    $isErpSimple = $isErp && !$isChild && !$hasChildren;

    $applyErpUnitPrice = function (array &$data) use ($p, $quotation) {
        $unitId = isset($p['unit_id']) ? (int) $p['unit_id'] : null;
        $prices = \Modules\Human\Entities\TpProductUnitPrice::getUnitPrice((int) $p['erp_product_id'], $unitId);
        $rate = (float) ($quotation->exchange_rate ?: 1);
        $data['estimated_price'] = $rate > 1 ? round($prices['cost_price']   / $rate, 2) : $prices['cost_price'];
        $data['quoted_price']    = $rate > 1 ? round($prices['retail_price'] / $rate, 2) : $prices['retail_price'];
    };
    // ... phần còn lại giữ nguyên tới các nhánh update/create bên dưới
```

- [ ] **Step 3: Áp giá vào nhánh UPDATE (price_id tồn tại)**

Sửa khối update (hiện chỉ `update($data)` mà không đụng giá ERP) — thêm re-derive TRƯỚC khi update:

```php
if (!empty($p['price_id'])) {
    if ($isErpSimple) {
        $applyErpUnitPrice($data);
    }
    QuotationProductPrice::where('id', $p['price_id'])
        ->where('quotation_id', $quotation->id)
        ->update(array_merge($data, ['updated_by' => auth()->id()]));
    return (int) $p['price_id'];
}
```

- [ ] **Step 4: Áp giá vào nhánh CREATE**

Thay khối `if ($isErp) { ... getCostPrices/getRetailPrices base ... }` hiện tại bằng:

```php
if ($isErpSimple) {
    $applyErpUnitPrice($data);
} elseif ($isErp) {
    // Combo ERP: giữ nguyên lấy giá đơn vị cơ bản như cũ
    $erpId = (int) $p['erp_product_id'];
    $costVnd = TpProductUnitPrice::getCostPrices([$erpId])[$erpId] ?? 0;
    $retailVnd = TpProductUnitPrice::getRetailPrices([$erpId])[$erpId] ?? 0;
    $rate = (float) ($quotation->exchange_rate ?: 1);
    $data['estimated_price'] = $rate > 1 ? round($costVnd / $rate, 2) : $costVnd;
    $data['quoted_price'] = $rate > 1 ? round($retailVnd / $rate, 2) : $retailVnd;
}
```

- [ ] **Step 5: Verify syntax**

Run: `cd hrm-api && php -l Modules/Assign/Services/QuotationService.php`
Expected: `No syntax errors detected`

---

### Task 4: FE nạp `unit_options` cho dòng hàng ERP

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue`

**Interfaces:**
- Consumes: `POST assign/quotations/erp-product-units` (Task 2)
- Produces: mỗi dòng ERP đủ điều kiện có `row.unit_options` (mảng đơn vị) + `row.unit_price_map` (`{unit_id: {retail_price, cost_price}}`). Method `isUnitSelectable(row)`, `loadUnitOptions()`.

- [ ] **Step 1: Thêm computed/method `isUnitSelectable`**

```js
isUnitSelectable(row) {
    return this.isDirectQuotation
        && !!row.erp_product_id
        && !row.is_parent_with_children
        && !row.parent_id
        && !row.parent_temp_id
}
```

- [ ] **Step 2: Thêm method `loadUnitOptions` (gọi sau loadDetail + sau add hàng ERP)**

```js
async loadUnitOptions() {
    const ids = [...new Set(
        (this.products || []).filter((r) => this.isUnitSelectable(r)).map((r) => r.erp_product_id).filter(Boolean)
    )]
    if (!ids.length) return
    try {
        // apiPostMethod ký hiệu { url, payload } (xem onAddProductApply:3510)
        const res = await this.$store.dispatch('apiPostMethod', {
            url: 'assign/quotations/erp-product-units',
            payload: { erp_product_ids: ids },
        })
        const map = res?.data || {}
        this.products.forEach((r) => {
            if (!this.isUnitSelectable(r)) return
            const units = map[r.erp_product_id] || map[String(r.erp_product_id)] || []
            this.$set(r, 'unit_options', units)
            const priceMap = {}
            units.forEach((u) => { priceMap[u.unit_id] = { retail_price: u.retail_price, cost_price: u.cost_price } })
            this.$set(r, 'unit_price_map', priceMap)
        })
    } catch (e) {
        // im lặng: không chặn màn nếu ERP lỗi; dòng giữ text
    }
}
```

- [ ] **Step 3: Gọi `loadUnitOptions` sau khi load chi tiết + sau khi thêm hàng ERP**

Trong `loadDetail()` — sau khi set `this.products` xong: thêm `this.loadUnitOptions()`.
Trong `onAddProductApply()` (dòng ~3133) — sau khi gán `this.products` các dòng mới: thêm `this.loadUnitOptions()`.
(Cả hai tên `this.products`, `apiPostMethod {url,payload}`, `loadDetail`, `onAddProductApply` đã xác minh có thật trong `edit.vue`.)

- [ ] **Step 4: Verify build FE** (chạy ở máy user)

Run: `cd hrm-client && npm run dev` → mở màn Sửa 1 báo giá type=2 có hàng ERP → devtools Network thấy call `erp-product-units` trả units.

---

### Task 5: FE cột ĐVT dạng select + đổi ĐVT lấy lại giá

**Files:**
- Modify: `hrm-client/pages/assign/quotations/_id/edit.vue` (cột ĐVT ~dòng 410 parent, 528 child; method mới)

**Interfaces:**
- Consumes: `row.unit_options`, `row.unit_price_map` (Task 4), tỷ giá + hàm làm tròn/format sẵn có của màn.
- Produces: method `onChangeUnit(row, unitId)`.

- [ ] **Step 1: Render select ở cột ĐVT cho dòng đủ điều kiện**

Thay ô hiển thị `<span>{{ parent.unit_name }}</span>` (dòng cha) bằng:

```html
<select
    v-if="isUnitSelectable(parent) && parent.unit_options && parent.unit_options.length"
    class="form-control form-control-sm"
    :value="parent.unit_id"
    @change="onChangeUnit(parent, Number($event.target.value))"
>
    <option v-for="u in parent.unit_options" :key="u.unit_id" :value="u.unit_id">{{ u.unit_name }}</option>
</select>
<span v-else>{{ parent.unit_name }}</span>
```

> Dòng con ERP không thuộc phạm vi (combo) → giữ nguyên `<span>{{ child.unit_name }}</span>`.

- [ ] **Step 2: Thêm method `onChangeUnit`**

```js
onChangeUnit(row, unitId) {
    row.unit_id = unitId
    const opt = (row.unit_options || []).find((u) => u.unit_id === unitId)
    if (opt) row.unit_name = opt.unit_name

    const priced = (row.unit_price_map || {})[unitId]
    if (!priced) return

    // Quy đổi tỷ giá + làm tròn 2 số lẻ — mirror onAddProductApply (edit.vue:3527-3535)
    const rate = Number(this.exchangeRate) || 1
    row.quoted_price = rate > 1 ? Math.round(priced.retail_price / rate * 100) / 100 : priced.retail_price
    // Giá vốn: chỉ khi BE trả (có quyền Xem giá vốn)
    if (priced.cost_price != null) {
        row.estimated_price = rate > 1 ? Math.round(priced.cost_price / rate * 100) / 100 : priced.cost_price
    }
    // Tổng (totalImport, summaryBreakdown, thành tiền) là computed reactive → tự cập nhật.
    // row.quoted_price/estimated_price/unit_id đã tồn tại sẵn → gán trực tiếp là reactive (Vue2).
}
```

> Tên `exchangeRate` (computed:1324), pattern làm tròn 2 số lẻ, và cơ chế totals dạng computed đã xác minh trong `edit.vue`. KHÔNG cần gọi hàm recompute thủ công.

- [ ] **Step 3: TUÂN THỦ TUYỆT ĐỐI logic hiển thị Giá nhập/Thành tiền nhập** (bắt buộc, tự kiểm)

Đối chiếu `edit.vue:412-470` — `onChangeUnit` KHÔNG được phá các rule sau:
- Ô Giá nhập hàng ERP LUÔN `disabled` (khoá) — `onChangeUnit` chỉ set `estimated_price` qua model, KHÔNG mở khoá/không cho gõ tay.
- Chỉ set `estimated_price` khi `priced.cost_price != null` (có quyền). Không quyền → giữ nguyên, ô hiện `—` (gate `canViewCostPrice` của template lo).
- Giá **bán** (`quoted_price`) luôn đổi (không thuộc gate giá vốn).
- KHÔNG tự tính lại "Thành tiền nhập"/`productImportTotal`/TSLN — để computed (`lineImportTotal`, `productImportTotal`, `lineMarginPercent`) tự chạy qua gate `canViewCostPrice`.
- Làm tròn đúng pattern add flow (2 số lẻ); precision hiển thị do `V2BaseCurrencyInput :precision="roundingPrecision"` + `formatMoney` lo.
- KHÔNG log/hiện `unit_price_map.cost_price` khi null (chống leak giá vốn).

- [ ] **Step 4: Verify build + E2E** (máy user)

Run: `cd hrm-client && npm run dev`

---

## Verify tổng thể (user, sau khi build)

- [ ] Màn Sửa báo giá **type=2**, dòng **hàng ERP đơn**: cột ĐVT là **select** đủ các đơn vị của sản phẩm.
- [ ] Đổi ĐVT → **giá bán + giá vốn** dòng đổi theo đơn vị; thành tiền + tổng báo giá cập nhật.
- [ ] Không quyền "Xem giá vốn" → đổi ĐVT vẫn đổi giá bán; giá vốn giữ `—` (BE trả cost null).
- [ ] **Lưu** báo giá → mở lại: giá dòng ERP đúng theo ĐVT đã chọn (BE re-derive).
- [ ] Hàng **tạm/dịch vụ/combo ERP** + báo giá **type=1**: ĐVT vẫn **text**, không có select.
- [ ] Màn **Xem chi tiết**: ĐVT hiển thị **text**.
- [ ] Đơn vị thiếu giá bán lẻ → giá bán = 0 (hiển thị rõ).

## Ngoài phạm vi (ghi nhận)
- Type=1 (từ BOM): đổi ĐVT sẽ làm ở BOM — **phase khác**.
- Combo ERP cha-con: đổi ĐVT — **phase khác** nếu cần.

---

## Progress Ledger
- Task 1: complete (BE helpers getUnitOptions/getUnitPrice — TpProductUnitPrice.php:131-217, php -l OK, review clean). Minor (final-review triage): `if($unitId)`→`!==null` (dòng ~184, không gây bug); duplicate query fallback (style).
- Task 2: complete (endpoint erpProductUnits QuotationController.php:485-517 + route api.php:456, php -l OK, review clean — gate cost=null kín, auth:api). Minor: array_slice trước array_unique (vô hại).
- Task 3: complete (saveDirectProduct re-derive theo unit_id create+update + combo detection, QuotationService.php:1039-1158, php -l OK, review clean — combo detect chắc chắn, non-ERP không đụng). Minor: unit_id=0 edge (vô hại).
- Task 4: complete (FE loadUnitOptions + isUnitSelectable, edit.vue:2502-2540, hook fetchData:2608 + onAddProductApply:3324, review clean sau fix). FIX Critical: `!row.is_parent_with_children` (field không tồn tại) → `!this.isParentWithChildren(row)` + bỏ no-op parent_temp_id. LƯU Ý: Task 5 dùng isUnitSelectable đã đúng.
- Task 5: complete (FE cột ĐVT cha → select + onChangeUnit, edit.vue:409-420 + 2540-2556, review clean 0 finding — tuân thủ logic giá nhập, ô ERP vẫn khoá, gate cost kín, không leak).

**Final whole-branch review (opus): DUYỆT MERGE** — 0 Critical/Important. Minor (backlog/test): (1) env('DB_DATABASE_SECOND') runtime — pattern cũ, nếu config:cache thì cần đổi sang config(); (2) đổi ĐVT không auto quy đổi qty_needed (đúng scope, unit_coefficient đã trả sẵn cho tương lai); (3) unit_coefficient FE chưa dùng.

### Checkpoint — 2026-07-12
Vừa hoàn thành: feature CODE DONE toàn bộ (Task 1-5) qua subagent-driven (impl+review mỗi task, fix 1 Critical Task4, final review opus clean). Chưa commit git.
Đang làm dở: (không)
Bước tiếp theo: user build FE (hrm-client) + E2E theo mục "Verify tổng thể" trong plan; commit khi user yêu cầu (hrm-api 4 file + hrm-client edit.vue).
Blocked: (không)

### Checkpoint — 2026-07-12 (E2E Playwright)
Vừa hoàn thành: E2E Playwright PASS (3/3). Dựng harness HRM/e2e/ đồng nhất chuẩn nhatlinh (config projects api-setup→setup→chromium, POM, storageState + .auth/api.json fixtures) + `hrm-api/database/e2e_provision.php` (seed user E2E role Super admin + báo giá type=2 chứa hàng ERP 3920 nhiều ĐVT, reuse erp2326). Spec `tests/assign/quotation-unit-select.spec.ts`: đổi ĐVT Cái→Hộp → assert giá bán 90.000 + giá vốn 50.849 hiện trong dòng.
Fix trong lúc chạy: (1) employee_infos.image CHECK constraint; (2) password_changed_at để không bị ép đổi MK (setup depend api-setup); (3) chờ select ĐVT render (loadUnitOptions async) tránh flaky.
Bước tiếp: commit khi user yêu cầu (BE 4 file + FE edit.vue + e2e/ + e2e_provision.php).

### Checkpoint — 2026-07-12 (E2E đủ case permission)
E2E Playwright 5/5 PASS. Bổ sung case KHÔNG quyền "Xem giá vốn": provision thêm role "E2E No Cost" (quyền Super admin company_id=1 trừ 1045) + user e2e_assign_nocost + báo giá riêng (qid=32); login-nocost.setup.ts → user-nocost.json; spec quotation-unit-select-nocost.spec.ts (đổi ĐVT: giá bán 90.000 đổi, giá vốn 50.849 KHÔNG lộ). Chứng minh gate API. Quy tắc "luôn test đủ case theo permission" đã lưu memory.

### Bugfix — Khép rủi ro chiết khấu khi đổi ĐVT (2026-07-12)
Vấn đề: onChangeUnit đổi quoted_price nhưng không tính lại CK → CK% stale (tổng/TSLN sai), CK tiền có thể > giá mới (validation đỏ), PP2 không cảnh báo phân bổ lại.
Fix (FE edit.vue onChangeUnit): sau khi set quoted_price → nếu discount_input_mode='percent' gọi onDiscountPercentInput(row) (tính lại discount_amount theo giá mới); luôn gọi onSalePriceChange(row) (PP2 cảnh báo phân bổ lại + allocationStale). CK theo tiền giữ nguyên (validation isItemDiscountInvalid tự báo). E2E 5/5 vẫn pass (không regression).

### Quyết định nghiệp vụ — Số lượng khi đổi ĐVT (2026-07-12)
CHỐT: đổi ĐVT KHÔNG tự động quy đổi `qty_needed` — user tự sửa số lượng theo đơn vị mới. Đây là hành vi mong muốn, KHÔNG phải bug. `unit_coefficient` vẫn được BE trả (getUnitOptions) nhưng FE cố ý không dùng để auto-convert. Không cần fix.

### Bugfix phụ (phát hiện khi test) — Màn tạo báo giá chập chờn "Không tìm thấy báo giá" (2026-07-12)
Root cause: mounted() dùng Promise.all cho 4 API preload (loadCurrencies/loadConfigs/loadUnits/loadDiscountTypes) → 1 API reject tạm thời là initCreateMode() bị bỏ qua → item null → hiện "Không tìm thấy báo giá" (sai ngữ cảnh màn tạo). Refresh thì hết.
Fix (edit.vue, dùng chung tạo+sửa): (1) Promise.all → Promise.allSettled (1 preload lỗi không chặn init); (2) empty-state v-else-if="!item && !isCreateMode" (màn tạo không hiện not-found). E2E 5/5 vẫn pass. KHÔNG liên quan feature ĐVT (bug lifecycle sẵn có).

### REVERT — "Robustness fix màn tạo" là chẩn đoán SAI (2026-07-12)
Fix trước (Promise.all→allSettled + guard v-else-if="!item && !isCreateMode") gây LỖI 404: 4 preload đã try/catch nuốt lỗi → Promise.all KHÔNG bao giờ reject → allSettled vô nghĩa. Guard "!isCreateMode" khiến create mode render FORM khi item=null → crash "Cannot read properties of null (reading 'code')" → Nuxt error page (user thấy "404").
→ ĐÃ REVERT cả 2 về nguyên gốc (Promise.all + v-else-if="!item"). Verify create OK 3/3, không crash; E2E 5/5 pass. Lỗi "Không tìm thấy báo giá" chập chờn ban đầu (nếu còn) là PRE-EXISTING, KHÔNG do feature ĐVT — chưa xử lý (cần điều tra race riêng nếu user muốn).

### Checkpoint — 2026-07-12 (wrap up)
Vừa hoàn thành (user đã test OK, chưa commit git):
1. Feature chọn ĐVT hàng ERP (Task 1-5): BE helper + endpoint gate cost + saveDirectProduct re-derive theo unit; FE cột ĐVT select + onChangeUnit. E2E 5/5 pass (2 case permission có/không Xem giá vốn).
2. Fix chiết khấu khi đổi ĐVT (onChangeUnit gọi onDiscountPercentInput + onSalePriceChange).
3. Testcase Excel 30 TC (.plans/quotation-unit-select/testcase.xlsx).
4. UI popup "Thêm hàng hoá" báo giá: bỏ tab title khi 1 tab; header bảng nowrap + min-width (scroll ngang, hết bóp); prop opt-in inlineSearchButtons ở V2BaseFilterPanel (input grow đầy + nút Tìm kiếm/Làm mới inline, lấp đầy 100%).
5. REVERTED fix robustness màn tạo (chẩn đoán sai → gây 404) về nguyên gốc.

Đang làm dở: (không)
Bước tiếp theo:
  - Commit git khi user yêu cầu. Files:
    • hrm-api: Modules/Human/Entities/TpProductUnitPrice.php, Modules/Assign/Http/Controllers/Api/V1/QuotationController.php, Modules/Assign/Routes/api.php, Modules/Assign/Services/QuotationService.php, database/e2e_provision.php
    • hrm-client: pages/assign/quotations/_id/edit.vue, pages/assign/quotations/components/QuotationProductSearchModal.vue, components/V2BaseFilterPanel.vue
    • HRM/e2e/ (harness Playwright mới)
  - Deploy: KHÔNG cần migration/permission mới cho feature ĐVT.
  - Tồn (nếu cần, task riêng): lỗi "Không tìm thấy báo giá" chập chờn màn tạo là PRE-EXISTING, cần repro rõ + điều tra race.
Blocked: (không)
