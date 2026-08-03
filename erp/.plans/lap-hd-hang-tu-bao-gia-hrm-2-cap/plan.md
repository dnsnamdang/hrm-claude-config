# Lập HĐ hãng từ báo giá HRM theo 2 cấp — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để chạy task-by-task. Steps dùng checkbox `- [ ]`.

**Goal:** Khi lập HĐ hãng ERP từ báo giá HRM, giữ nguyên cấu trúc hàng hoá 2 cấp (cha-con) thay vì import phẳng.

**Architecture:** HRM lộ thêm `parent_id`/`product_type` ở endpoint ERP đang gọi; ERP dựng lại cha-con khi prefill form (set `tmp_row_id`/`is_child`/`child_parent_tmp_id`/`child_ratio`, con thành tiền=0, gom con vào tab cha). Lưu/xuất hàng/quỹ tái dùng nguyên logic cha-con đã merge.

**Tech Stack:** ERP = Laravel 6 (PHP 7.4) + Blade/AngularJS 1.3.9; HRM = Laravel 8 (PHP 7.4). Verify = `php -l` + tinker + browser (repo KHÔNG dùng test tự động cho luồng này).

## Global Constraints
- DB KHÔNG đổi (cả 2 phía cột cha-con đã có sẵn).
- `child_ratio` tính ở ERP = `con.qty / cha.qty` (HRM không có cột ratio).
- Con: `total_cost = 0`, tiền dồn về cha; cha: `total_cost = qty × price` (HRM đã trọn gói).
- Mirror luật sửa/khoá của luồng "báo giá→HĐ" ERP hiện có; không đặt luật mới.
- KHÔNG commit/push khi chưa có yêu cầu user (quy tắc dự án). Mỗi task verify xong dừng chờ duyệt; commit gộp khi user đồng ý.
- ERP làm trên nhánh `sync_quotation` (đã merge HRM-quotation + cha-con). HRM làm trên nhánh tương ứng (xác nhận với user trước khi sửa).

## File Structure
- **HRM** — Modify: `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (`erpContractData` select). Trách nhiệm: lộ cha-con cho ERP.
- **ERP** — Modify: `app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php` (`getDataForContract` mapping). Trách nhiệm: dựng cấu trúc cha-con cho form.
- **ERP** — KHÔNG đổi: `app/Services/Hrm/HrmApiService.php` (passthrough), form/store cha-con (đã có).

---

### Task 1 (HRM): Lộ `parent_id` + `product_type` ở endpoint ERP

**Files:**
- Modify: `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (method `erpContractData`, đoạn `QuotationProductPrice::where('quotation_id',$id)->...->get([...])`)

**Interfaces:**
- Produces: payload `data.products[]` mỗi phần tử thêm 2 khoá `parent_id` (int|null), `product_type` (int). Các khoá cũ giữ nguyên (`id`, `quantity`, `quotation_group_id`, `erp_product_id`, `quoted_price`, `vat_percent`, `code`, `name`, `model_id`, `brand_id`, `origin_id`, `unit_id`, `product_attributes`, `discount_amount`).

- [ ] **Step 1: Sửa select thêm parent_id, product_type**

Trong `erpContractData`, mảng truyền vào `->get([...])` — thêm `'parent_id'` và `'product_type'`:

```php
$products = \Modules\Assign\Entities\QuotationProductPrice::where('quotation_id', $id)
    ->orderBy('sort_order')
    ->get([
        'id', 'erp_product_id', 'unit_id', 'code', 'name',
        'model_id', 'brand_id', 'origin_id', 'product_attributes',
        'quoted_price', 'vat_percent', 'discount_amount', 'quotation_group_id',
        'parent_id', 'product_type',
        \Illuminate\Support\Facades\DB::raw('qty_needed as quantity'),
    ]);
```

- [ ] **Step 2: Lint**

Run: `php -l Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`
Expected: `No syntax errors detected`

- [ ] **Step 3: Verify payload có cha-con (tinker, chọn 1 báo giá có hàng cha-con)**

Run: `php artisan tinker`
```php
$id = /* id 1 báo giá HRM có parent_id */;
\Modules\Assign\Entities\QuotationProductPrice::where('quotation_id',$id)
  ->get(['id','parent_id','product_type','qty_needed','quoted_price'])
  ->each(function($r){ echo "{$r->id} parent={$r->parent_id} type={$r->product_type} qty={$r->qty_needed}\n"; });
```
Expected: thấy ít nhất 1 dòng `parent=<id cha>` (con) và dòng cha `parent=` rỗng.

- [ ] **Step 4: Dừng — báo user verify (chưa commit)**

---

### Task 2 (ERP): Dựng cha-con trong `getDataForContract`

**Files:**
- Modify: `app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php` (method `getDataForContract`, đoạn `$rawProducts = collect(...)` → `$mapped = ...` và `$makeTab`)

**Interfaces:**
- Consumes: `data.products[]` từ Task 1 (có `id`, `parent_id`, `quantity`, `quoted_price`, `quotation_group_id`, ...).
- Produces: response `tabs[].products[]` mỗi dòng có thêm `tmp_row_id` (string), `is_child` (bool), `child_parent_tmp_id` (string|null), `child_ratio` (float); con có `total_cost = 0`; con nằm cùng tab + ngay sau cha. Form/store cha-con tiêu thụ các khoá này (đã có sẵn).

- [ ] **Step 1: Thay đoạn build `$mapped` để index SL/group + set field cha-con**

Thay đoạn từ `$rawProducts = collect($data['products']);` tới hết `$mapped = ...->values();` bằng:

```php
$rawProducts = collect($data['products']);

// Index SL + group theo hrm id (tính child_ratio + ép con vào tab cha)
$qtyByHrmId = [];
$groupByHrmId = [];
foreach ($rawProducts as $rp) {
    $rp = (array) $rp;
    $qtyByHrmId[$rp['id']] = (float) ($rp['quantity'] ?? 0);
    $groupByHrmId[$rp['id']] = $rp['quotation_group_id'] ?? null;
}

$mapped = $rawProducts->map(function ($p) use ($priceType, $qtyByHrmId, $groupByHrmId) {
    $p = (array) $p;
    $erpProductId = $p['erp_product_id'] ?? null;
    $product = $erpProductId ? Product::query()->find($erpProductId) : null;
    $unitId = $p['unit_id'] ?? ($product ? $product->unit_id : null);
    $saleMax = 0;
    try {
        $saleMax = Product::getPriceByUnitAndType($erpProductId, $unitId, $priceType)->sale_max_percent;
    } catch (\Throwable $e) {
        $saleMax = 0;
    }

    $hrmId = $p['id'];
    $parentHrmId = $p['parent_id'] ?? null;
    // Con thật sự chỉ khi parent_id trỏ tới 1 dòng CÓ trong báo giá (mồ côi → coi như dòng thường)
    $isChild = !empty($parentHrmId) && isset($qtyByHrmId[$parentHrmId]);
    $qty = (float) ($p['quantity'] ?? 0);
    $price = $p['quoted_price'] ?? 0;

    $childRatio = 0;
    if ($isChild) {
        $parentQty = $qtyByHrmId[$parentHrmId];
        $childRatio = $parentQty > 0 ? $qty / $parentQty : 0; // cha qty=0 (hiếm) → 0
    }

    // Con: thành tiền = 0 (tiền dồn về cha); con giữ đơn giá để xuất hàng tính price×qty
    $totalCost = $isChild ? 0 : ($qty * $price);

    // Tab của con = tab của cha (ép theo cha nếu lệch nhóm)
    $groupId = $isChild
        ? ($groupByHrmId[$parentHrmId] ?? ($p['quotation_group_id'] ?? null))
        : ($p['quotation_group_id'] ?? null);

    return [
        'firm_quotation_tab_product_id' => null,
        'product_id' => $erpProductId,
        'product_name' => $p['name'] ?: ($product ? $product->name : ''),
        'code' => $p['code'] ?: ($product ? $product->code : ''),
        'model_id' => $p['model_id'] ?? null,
        'brand_id' => $p['brand_id'] ?? null,
        'origin_id' => $p['origin_id'] ?? null,
        'product_attributes' => $p['product_attributes'] ?? null,
        'attribute_products' => $p['product_attributes'] ?? null,
        'unit_id' => $unitId,
        'unit_name' => $unitId ? optional(Unit::find($unitId))->name : null,
        'quantity' => $qty,
        'price' => $price,
        'allocated_price' => $price,
        'total_cost' => $totalCost,
        'vat_percent' => $product ? ($product->vat_percent ?? 0) : ($p['vat_percent'] ?? 0),
        'sale_max_percent' => $saleMax,
        'price_extra' => 0,
        'price_discount' => 0,
        // cha-con
        'tmp_row_id' => (string) $hrmId,
        'is_child' => $isChild,
        'child_parent_tmp_id' => $isChild ? (string) $parentHrmId : null,
        'child_ratio' => $childRatio,
        '__group_id' => $groupId,
    ];
})->values();
```

- [ ] **Step 2: Thêm sắp xếp cha→con trong `$makeTab` (con bám ngay sau cha)**

Thay thân `$makeTab` để order rows trước khi build (giữ nguyên phần tính total/vat/return):

```php
$makeTab = function ($name, $rows) {
    $rows = collect($rows)->values();

    // Order: mỗi cha đứng trước, con (theo child_parent_tmp_id) bám ngay sau
    $byParent = [];
    $parents = [];
    foreach ($rows as $r) {
        if (!empty($r['is_child']) && !empty($r['child_parent_tmp_id'])) {
            $byParent[$r['child_parent_tmp_id']][] = $r;
        } else {
            $parents[] = $r;
        }
    }
    $ordered = [];
    $seenParent = [];
    foreach ($parents as $p) {
        $ordered[] = $p;
        $seenParent[$p['tmp_row_id']] = true;
        foreach ($byParent[$p['tmp_row_id']] ?? [] as $c) {
            $ordered[] = $c;
        }
    }
    // Con mồ côi trong tab (hiếm — cha không cùng tab): append cuối
    foreach ($byParent as $pid => $children) {
        if (empty($seenParent[$pid])) {
            foreach ($children as $c) { $ordered[] = $c; }
        }
    }

    $rows = collect($ordered)->map(function ($r) {
        unset($r['__group_id']);
        return $r;
    })->values();

    $firstVat = $rows->isNotEmpty() ? ($rows->first()['vat_percent'] ?? 0) : 0;
    $totalCost = $rows->sum(fn ($r) => $r['total_cost'] ?? 0);
    $vatCost = $rows->sum(fn ($r) => ($r['total_cost'] ?? 0) * ($r['vat_percent'] ?? 0) / 100);
    return [
        'firm_quotation_tab_id' => null,
        'name' => $name ?: 'Hàng hóa',
        'total_cost' => $totalCost,
        'total_extra' => 0,
        'total_discount' => 0,
        'vat_percent' => $firstVat,
        'vat_cost' => round($vatCost),
        'total_after_vat' => round($totalCost + $vatCost),
        'products' => $rows,
    ];
};
```

(Phần gom tab theo `$groups`/`$ungrouped`/`$grandTotal` bên dưới GIỮ NGUYÊN — con đã được gán `__group_id` = group của cha nên tự vào đúng tab.)

- [ ] **Step 3: Lint**

Run: `php -l app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php`
Expected: `No syntax errors detected`

- [ ] **Step 4: Verify cấu trúc trả về (tinker)**

Run: `php artisan tinker` (cần auth context — chọn user là Sale của báo giá, hoặc gọi service trực tiếp)
```php
$hrm = app(\App\Services\Hrm\HrmApiService::class);
$data = $hrm->contractData(/* hrm_quotation_id có cha-con */, /* employee_info_id */);
collect($data['products'])->each(fn($p)=>print(($p['parent_id']??'-')." => id {$p['id']} qty {$p['quantity']}\n"));
```
Expected: thấy con có `parent_id`. (Phần dựng tab kiểm tra qua browser ở Task 3.)

- [ ] **Step 5: Dừng — báo user (chưa commit)**

---

### Task 3: Verify end-to-end (browser, DB dev)

**Files:** không sửa — chỉ kiểm thử.

**Tiền đề:** `.env` ERP trỏ **DB dev** (KHÔNG prod); HRM API chạy + có ≥1 báo giá HRM đủ điều kiện lập HĐ, có hàng cha-con.

- [ ] **Step 1: Báo giá phẳng (regression)** — Lập HĐ từ 1 báo giá HRM KHÔNG cha-con → form + HĐ ra y như trước (không lỗi).
- [ ] **Step 2: Báo giá cha-con** — Lập HĐ từ báo giá có cha-con → form hiện con indent (⌊) + "(tỉ lệ X)"; tiền con = 0; tổng HĐ = Σ tiền cha; `child_ratio` = con.qty/cha.qty.
- [ ] **Step 3: Lưu HĐ** → kiểm DB:
```sql
SELECT id, product_id, child_parent_id, child_ratio, total_cost
FROM firm_contract_tab_products WHERE firm_contract_id = <id HĐ vừa lập>;
```
Expected: dòng con có `child_parent_id` trỏ đúng cha + `child_ratio` đúng + `total_cost = 0`; cha có total_cost > 0.
- [ ] **Step 4: Nhóm lệch** — báo giá cha-con mà con khác `quotation_group_id` với cha → con vẫn vào tab của cha.
- [ ] **Step 5: Báo giá direct (không BOM) cha-con** → chạy đúng như Step 2–3.
- [ ] **Step 6: Xuất hàng cụm cha-con** — từ HĐ vừa lập, tạo yêu cầu xuất 1 cụm cha-con → quỹ/SL trừ đúng (tái dùng logic cha-con đã test).
- [ ] **Step 7: Mark HRM** — xác nhận báo giá HRM được set `erp_firm_contract_id` (chống lập trùng).

---

## Self-review (đã rà)
- **Spec coverage:** §4 HRM → Task 1; §5 ERP mapping → Task 2; §6 luồng + §9 test → Task 3; §7 edge (mồ côi/nhóm lệch/ratio lẻ/direct/cha qty=0) → Task 2 code + Task 3 Step 4–5. ✓
- **Placeholder scan:** không có TODO/“xử lý lỗi phù hợp”; code đầy đủ từng step. ✓
- **Type consistency:** khoá form `tmp_row_id`/`is_child`/`child_parent_tmp_id`/`child_ratio` trùng đúng tên FE/store cha-con dùng (`form.blade.php`, `FirmContractService`). ✓

## Checkpoint — 2026-06-26
Vừa hoàn thành: **Task 1 (HRM) + Task 2 (ERP) — CODE XONG** (subagent-driven, review inline khớp spec, `php -l` sạch 2 file, **CHƯA commit** theo quy tắc dự án).
- HRM `QuotationController::erpContractData`: +`parent_id`,`product_type` (1 dòng).
- ERP `HrmQuotationContractController::getDataForContract`: dựng cha-con (`tmp_row_id`/`is_child`/`child_parent_tmp_id`/`child_ratio`, con total=0, ép con vào tab cha + sắp con sau cha). 72+/11-.
Cả 2 trên nhánh `sync_quotation` (ERP + HRM), working tree còn uncommitted.
Đang làm dở: —
Bước tiếp theo: **User chạy Task 3 (E2E browser)** — `.env` ERP trỏ DB dev + HRM API chạy. Sau khi pass → commit 2 repo (khi user yêu cầu).
Blocked: (trống)
