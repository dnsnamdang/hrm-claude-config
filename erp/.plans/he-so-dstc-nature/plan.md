# Hệ số DSTC theo tính chất hàng hoá (product_natures) — Plan B (ERP, Phase 3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để thực thi từng task. Các step dùng checkbox (`- [ ]`).

**Goal:** ERP ngừng đọc hệ số quy đổi DSTC theo enum cũ `products.product_type` (bảng `company_product_types`); chuyển sang leo cây phân loại mới → `product_nature_id` → tra bảng chung `company_product_natures`, và gỡ màn khai hệ số cũ trên ERP.

**Architecture:** ERP + HRM dùng CHUNG một DB (`erp_hrm_check`). ERP tạo 1 helper tĩnh `App\Support\ProductNatureDstcCoefficient` đọc **thẳng DB chung** bằng `DB::table()` + JOIN cây (KHÔNG gọi API HRM), **mirror y hệt** helper HRM `Modules\MasterData\Support\ProductNatureDstcCoefficient` (Plan A Task 3) để 2 app không lệch hệ số. Thay 15 điểm đọc ở luồng hợp đồng hãng/dịch vụ/đơn nguyên tắc. Khai cấu hình chỉ còn ở HRM `sale/regulation-config`.

**Tech Stack:** Laravel 6.20.44 / PHP 7.4, Eloquent + `DB` facade (`Illuminate\Support\Facades\DB`). KHÔNG dùng facade `Http`, cú pháp PHP8, hay `DB_CONNECTION_SECOND`/mysql2 — DB là chung một kết nối mặc định.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-19-he-so-dstc-theo-tinh-chat-nature-design.md` (các executor đọc cả spec lẫn plan).

**Nhánh ERP:** `feat/2d1-erp-khong-loi` (hiện worktree đang checkout `gop_db`; phải checkout nhánh feature trước khi code).

## Phụ thuộc chéo (QUAN TRỌNG)

Plan B **phụ thuộc Plan A Task 1** (HRM migration tạo bảng `company_product_natures` trên DB chung). ERP KHÔNG tạo bảng này. Task 1 của Plan B là **cổng kiểm tra tiền đề**: nếu bảng/cây chưa có trên DB chung → DỪNG, chạy Plan A Task 1 trước.

## Global Constraints

- DB chung `erp_hrm_check`; mọi truy vấn qua kết nối mặc định. **KHÔNG** `DB_CONNECTION_SECOND`/mysql2.
- **KHÔNG commit/push** khi user chưa yêu cầu. Mỗi task kết thúc bằng "soạn commit message, CHƯA chạy git".
- **KHÔNG drop / migrate / sửa** bảng cũ `company_product_types` — giữ nguyên để đối chiếu lịch sử. Chỉ ngừng đọc/ghi.
- Mọi script tinker **PHẢI** bọc `DB::beginTransaction()` … `DB::rollBack()`; đọc `grep DB_ .env` trước khi chạy để biết đang trỏ DB nào (local .env ERP đổi target theo lúc).
- **Query cây phải GIỐNG HỆT** helper HRM (Plan A Task 3): cùng thứ tự JOIN, cùng cột. Lệch JOIN → lệch hệ số giữa 2 app.
- Công thức tính giá **không đổi**: `standard_price = … * price_type_coefficient * product_type_coefficient`. Chỉ đổi NGUỒN của `product_type_coefficient`.
- Helper không bao giờ trả `null` (luôn float, fallback `1.0`). Các dòng gán `$x[...] = $product_type_coefficient ?? 1;` giữ nguyên (no-op, giảm diff).
- Hệ số lưu `0` (khai tường minh) được tôn trọng (helper tra theo key tồn tại, không theo truthiness).
- KHÔNG đụng các file `ProductExportRequest*` (feature khác).
- ERP: KHÔNG đọc `vendor/`, `node_modules/`.

## Review Focus

- **Hàng chưa phân loại (`products.product_type_id` NULL) hoặc cây gãy** → `forProduct` trả `1.0` (JOIN INNER không ra dòng → `value()` = null → 1.0). Test ở Task 2.
- **Sentinel 0 = "Dịch vụ":** `forService` tra đúng `product_nature_id = 0`; đảm bảo không có `product_natures.id = 0` thật làm nhiễu. Test ở Task 2.
- **Hệ số lưu `0` tường minh** (công ty cố tình khai 0) phải trả `0.0`, KHÔNG rơi về 1. Test ở Task 2.
- **Company chưa khai nature đó** → `1.0` (key không có trong map). Test ở Task 2.
- **Màn Quy chế ERP vẫn lưu được** price_types + rule_commissions sau khi gỡ card product_types (không vỡ `saveHistoryChangeRegulation` nhờ guard `if ($originalProductTypes)`). Test ở Task 4.

---

## Task 1: Kiểm tra tiền đề DB chung (cổng, read-only)

**Files:** không sửa file. Chạy tinker read-only.

**Interfaces:**
- Consumes: bảng `company_product_natures` (Plan A Task 1), `products.product_type_id`, cây `product_types / product_families / product_function_groups`.
- Produces: xác nhận DB sẵn sàng cho Task 2–3.

- [ ] **Step 1: Xác định DB đang trỏ**

```bash
cd /Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev
grep -E '^DB_(CONNECTION|HOST|DATABASE)=' .env
```
Ghi lại tên DB (mong đợi `erp_hrm_check` hoặc bản dev tương đương). Nếu trỏ prod → dừng, hỏi user.

- [ ] **Step 2: Kiểm tra schema tiền đề (read-only)**

```bash
php artisan tinker --execute="
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;
foreach (['company_product_natures','product_natures','product_function_groups','product_families','product_types','products'] as \$t) {
    echo \$t.': '.(Schema::hasTable(\$t) ? 'OK' : 'MISSING').PHP_EOL;
}
echo 'products.product_type_id: '.(Schema::hasColumn('products','product_type_id') ? 'OK' : 'MISSING').PHP_EOL;
echo 'company_product_natures cols: '.implode(',', Schema::getColumnListing('company_product_natures')).PHP_EOL;
echo 'product_natures.id=0 exists? '.(DB::table('product_natures')->where('id',0)->exists() ? 'YES(!)' : 'no').PHP_EOL;
"
```
Mong đợi: tất cả `OK`; cột `company_product_natures` gồm `company_id, product_nature_id, coefficient, name`; `product_natures.id=0` = `no` (nếu `YES` → sentinel 0 trùng dữ liệu thật, báo user trước khi tiếp).

- [ ] **Step 3: Quyết định cổng**

Nếu có `MISSING` liên quan `company_product_natures` → DỪNG: Plan A Task 1 chưa chạy trên DB chung. Nếu thiếu cây/`product_type_id` → DỪNG: migration phân loại HRM chưa chạy. Ngược lại → tiếp Task 2. (Không commit.)

---

## Task 2: Helper `App\Support\ProductNatureDstcCoefficient`

**Files:**
- Create: `app/Support/ProductNatureDstcCoefficient.php`
- Test: tinker script (Laravel 6 không có suite PHPUnit cho luồng này; test bằng tinker bọc transaction).

**Interfaces:**
- Consumes: DB chung (Task 1).
- Produces (các task sau gọi): 
  - `\App\Support\ProductNatureDstcCoefficient::forProduct(?int $companyId, $erpProductId): float`
  - `\App\Support\ProductNatureDstcCoefficient::forService(?int $companyId): float`
  - `\App\Support\ProductNatureDstcCoefficient::forNature(?int $companyId, int $natureId): float`

- [ ] **Step 1: Viết test tinker (chạy TRƯỚC khi có file → fail)**

Lưu script vào scratchpad, ví dụ `/private/tmp/claude-501/.../scratchpad/dstc_helper_test.php`:

```php
<?php
use Illuminate\Support\Facades\DB;
use App\Support\ProductNatureDstcCoefficient;

DB::beginTransaction();
try {
    // Dùng 1 công ty test id lớn để không đụng dữ liệu thật
    $companyId = 999999001;

    // (a) forNature: company chưa khai nature 777 -> 1.0
    assert(ProductNatureDstcCoefficient::forNature($companyId, 777) === 1.0);

    // (b) khai nature 777 = 2.5 -> 2.5 ; nature 0 (Dịch vụ) = 0 (tường minh) -> 0.0
    DB::table('company_product_natures')->insert([
        ['company_id' => $companyId, 'product_nature_id' => 777, 'coefficient' => 2.5, 'name' => 'NatureTest', 'created_at' => now(), 'updated_at' => now()],
        ['company_id' => $companyId, 'product_nature_id' => 0,   'coefficient' => 0,   'name' => 'Dịch vụ',    'created_at' => now(), 'updated_at' => now()],
    ]);
    ProductNatureDstcCoefficient::clearCache(); // nạp lại map sau khi insert
    assert(ProductNatureDstcCoefficient::forNature($companyId, 777) === 2.5);
    assert(ProductNatureDstcCoefficient::forService($companyId) === 0.0); // hệ số 0 tường minh được tôn trọng

    // (c) forProduct: product không tồn tại / chưa phân loại -> 1.0
    assert(ProductNatureDstcCoefficient::forProduct($companyId, 0) === 1.0);
    assert(ProductNatureDstcCoefficient::forProduct($companyId, 999999999) === 1.0);

    // (d) forProduct trên 1 SP đã phân loại thật (nếu có): khai nature của nó = 3 -> 3.0
    $sample = DB::table('products as p')
        ->join('product_types as pt', 'pt.id', '=', 'p.product_type_id')
        ->join('product_families as pf', 'pf.id', '=', 'pt.product_family_id')
        ->join('product_function_groups as fg', 'fg.id', '=', 'pf.product_function_group_id')
        ->select('p.id as pid', 'fg.product_nature_id as nid')
        ->first();
    if ($sample) {
        DB::table('company_product_natures')->insert([
            'company_id' => $companyId, 'product_nature_id' => $sample->nid, 'coefficient' => 3, 'name' => 'X', 'created_at' => now(), 'updated_at' => now(),
        ]);
        ProductNatureDstcCoefficient::clearCache();
        assert(ProductNatureDstcCoefficient::forProduct($companyId, $sample->pid) === 3.0);
        echo "forProduct classified: OK (pid={$sample->pid}, nid={$sample->nid})".PHP_EOL;
    } else {
        echo "forProduct classified: SKIP (chưa có SP phân loại trong DB)".PHP_EOL;
    }

    echo "ALL ASSERTS PASSED".PHP_EOL;
} finally {
    DB::rollBack();
}
```

- [ ] **Step 2: Chạy test → fail**

```bash
php artisan tinker < /private/tmp/claude-501/.../scratchpad/dstc_helper_test.php
```
Expected: lỗi `Class 'App\Support\ProductNatureDstcCoefficient' not found`.

- [ ] **Step 3: Tạo helper**

```php
<?php

namespace App\Support;

use Illuminate\Support\Facades\DB;

/**
 * Hệ số quy đổi theo tính chất hàng hoá (DSTC) — đọc bảng CHUNG company_product_natures.
 *
 * Leo cây (GIỐNG HỆT HRM \Modules\MasterData\Support\ProductNatureDstcCoefficient):
 *   products.product_type_id -> product_types.product_family_id
 *   -> product_families.product_function_group_id -> product_function_groups.product_nature_id
 *
 * product_nature_id = 0 là dòng "Dịch vụ" (sentinel). Không ra nature / company chưa khai => 1.0.
 * Hệ số lưu 0 tường minh được tôn trọng (tra theo key tồn tại, không theo truthiness).
 */
class ProductNatureDstcCoefficient
{
    /** @var array<int,array<int,float>> cache [companyId => [natureId => coefficient]] trong 1 request */
    private static $maps = [];

    /** Hệ số theo sản phẩm thật (leo cây ra product_nature_id). */
    public static function forProduct(?int $companyId, $erpProductId): float
    {
        if (!$erpProductId) {
            return 1.0;
        }
        $natureId = DB::table('products as p')
            ->join('product_types as pt', 'pt.id', '=', 'p.product_type_id')
            ->join('product_families as pf', 'pf.id', '=', 'pt.product_family_id')
            ->join('product_function_groups as fg', 'fg.id', '=', 'pf.product_function_group_id')
            ->where('p.id', $erpProductId)
            ->value('fg.product_nature_id');
        if ($natureId === null) {
            return 1.0;
        }
        return self::forNature($companyId, (int) $natureId);
    }

    /** Hệ số cho dòng "Dịch vụ" (HĐ dịch vụ, không gắn hàng thật). */
    public static function forService(?int $companyId): float
    {
        return self::forNature($companyId, 0);
    }

    /** Hệ số theo product_nature_id (0 = Dịch vụ). Chưa khai => 1.0. */
    public static function forNature(?int $companyId, int $natureId): float
    {
        if ($companyId === null) {
            return 1.0;
        }
        $companyId = (int) $companyId;
        if (!array_key_exists($companyId, self::$maps)) {
            self::$maps[$companyId] = DB::table('company_product_natures')
                ->where('company_id', $companyId)
                ->pluck('coefficient', 'product_nature_id')
                ->map(function ($c) {
                    return (float) $c;
                })
                ->toArray();
        }
        $map = self::$maps[$companyId];
        return array_key_exists($natureId, $map) ? (float) $map[$natureId] : 1.0;
    }

    /** Xoá cache map (dùng cho test sau khi insert cấu hình mới). */
    public static function clearCache(): void
    {
        self::$maps = [];
    }
}
```

> **Mirror-check:** so khớp khối JOIN với helper HRM (Plan A Task 3) — phải trùng từng dòng `join()` và `value('fg.product_nature_id')`. Nếu Plan A dùng alias/thứ tự khác → sửa 1 trong 2 cho khớp, ưu tiên bản này.

- [ ] **Step 4: Chạy test → pass**

```bash
php artisan tinker < /private/tmp/claude-501/.../scratchpad/dstc_helper_test.php
```
Expected: in `ALL ASSERTS PASSED` (và dòng `forProduct classified: OK/SKIP`). Dọn script: `rm -f /private/tmp/claude-501/.../scratchpad/dstc_helper_test.php`.

- [ ] **Step 5: Soạn commit (CHƯA chạy git)**

Message dự kiến: `feat(dstc): them helper ProductNatureDstcCoefficient doc company_product_natures (ERP)`. Theo ràng buộc, CHƯA chạy git — chờ user yêu cầu.

---

## Task 3: Thay 15 điểm đọc hệ số sang helper

**Files:**
- Modify: `app/Model/Customers/WrServiceContract.php` (6 điểm: ~1227/1277/1345/1438/1465/1530; `use` dòng 12)
- Modify: `app/Services/Sale/Firm/Contract/FirmContractService.php` (3 điểm: ~718 ternary / 862 / 1047; `use` dòng 14)
- Modify: `app/Services/Sale/Firm/Contract/ZTFirmContractService.php` (2 điểm: ~674 / 800; `use` dòng 13)
- Modify: `app/Services/Sale/Firm/Order/PrincipleOrderService.php` (2 điểm: ~320 / 368; `use` dòng 11)
- Modify: `app/Services/Sale/Firm/Order/ZTPrincipleOrderService.php` (2 điểm: ~319 / 365; `use` dòng 12)

**Interfaces:**
- Consumes: `\App\Support\ProductNatureDstcCoefficient::forProduct/forService` (Task 2). Dùng **FQCN inline** (không thêm `use`) để mỗi edit tự chứa.
- Produces: không.

> **Khuôn thay (same-shape, lặp ở mọi điểm):** chỉ đổi DÒNG gán `$product_type_coefficient = CompanyProductTypes::query()…->value('coefficient');`. Giữ nguyên dòng `… = $product_type_coefficient ?? 1;` ngay sau (no-op). `$product_obj`/`$product` đã được nạp sẵn ở dòng trên tại mọi điểm "product".

- [ ] **Step 1: WrServiceContract.php — 2 điểm "service" (~1227, ~1345, ~1438)**

Có **3** điểm `'service'` ở file này (1227, 1345, 1438). Mỗi điểm, thay:
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', 'service')->value('coefficient');
```
thành:
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forService((int) $company_id);
```
(dòng `$product[...]`/`$service[...] = $product_type_coefficient ?? 1;` giữ nguyên.)

- [ ] **Step 2: WrServiceContract.php — 3 điểm "product" (~1277, ~1465, ~1530)**

Mỗi điểm có `$product_obj = Product::query()->find(...)` ở dòng trên. Thay:
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', $product_obj->product_type)->value('coefficient');
```
thành:
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product_obj->id);
```

- [ ] **Step 3: WrServiceContract.php — gỡ `use` thừa**

```bash
grep -n "CompanyProductTypes" app/Model/Customers/WrServiceContract.php
```
Expected: chỉ còn dòng `use App\Model\Common\CompanyProductTypes;` (12). Xoá dòng đó.

- [ ] **Step 4: FirmContractService.php — 3 điểm**

Điểm ~718 (ternary, `$product_obj` đã nạp): thay khối
```php
$product_type_coefficient = $product_obj
    ? (CompanyProductTypes::query()
        ->where('company_id', $company_id)
        ->where('product_type_id', $product_obj->product_type)
        ->value('coefficient') ?? 1)
    : 1;
```
thành:
```php
$product_type_coefficient = $product_obj
    ? \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product_obj->id)
    : 1;
```

Điểm ~862 (`$product_obj = Product::query()->find($product['product_id']);` ở dòng trên): thay
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', $product_obj->product_type)->value('coefficient');
```
thành:
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product_obj->id);
```

Điểm ~1047 (service, company var = `$user_info->company_id`): thay
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $user_info->company_id)->where('product_type_id', 'service')->value('coefficient');
```
thành:
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forService((int) $user_info->company_id);
```
Rồi `grep -n CompanyProductTypes app/Services/Sale/Firm/Contract/FirmContractService.php` → chỉ còn `use` (14) → xoá dòng `use App\Model\Common\CompanyProductTypes;`.

- [ ] **Step 5: ZTFirmContractService.php — 2 điểm**

Điểm ~674 (product, `$product_obj = Product::query()->find($product['product_id']);` ở dòng trên):
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', $product_obj->product_type)->value('coefficient');
```
→
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product_obj->id);
```

Điểm ~800 (service, `$user_info->company_id`):
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $user_info->company_id)->where('product_type_id', 'service')->value('coefficient');
```
→
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forService((int) $user_info->company_id);
```
Rồi `grep -n CompanyProductTypes app/Services/Sale/Firm/Contract/ZTFirmContractService.php` → chỉ còn `use` (13) → xoá.

- [ ] **Step 6: PrincipleOrderService.php — 2 điểm**

Điểm ~320 (product, `$product` là Product model đã nạp trong vòng lặp):
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', $product->product_type)->value('coefficient');
```
→
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product->id);
```

Điểm ~368 (service, trong `syncCosts`, company var = `$company_id` đã set `auth()->user()->info->company_id`):
```php
$product_type_coefficient = CompanyProductTypes::query()->where('company_id', $company_id)->where('product_type_id', 'service')->value('coefficient');
```
→
```php
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forService((int) $company_id);
```
Rồi `grep -n CompanyProductTypes app/Services/Sale/Firm/Order/PrincipleOrderService.php` → chỉ còn `use` (11) → xoá.

- [ ] **Step 7: ZTPrincipleOrderService.php — 2 điểm**

Giống Step 6 nhưng file ZT (product ~319 dùng `$product->id`; service ~365 dùng `$company_id`):
```php
// ~319
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forProduct((int) $company_id, $product->id);
// ~365
$product_type_coefficient = \App\Support\ProductNatureDstcCoefficient::forService((int) $company_id);
```
Rồi `grep -n CompanyProductTypes app/Services/Sale/Firm/Order/ZTPrincipleOrderService.php` → chỉ còn `use` (12) → xoá.

- [ ] **Step 8: Grep xác nhận không còn điểm đọc cũ trong luồng bán hàng**

```bash
grep -rnE "CompanyProductTypes::query\(\)->where\('company_id'" app/Model/Customers/WrServiceContract.php app/Services/Sale/Firm
```
Expected: rỗng (0 dòng).

```bash
grep -rnE "where\('product_type_id', '?service'?\)|where\('product_type_id', \\\$product" app/Services/Sale/Firm app/Model/Customers/WrServiceContract.php
```
Expected: rỗng — mọi điểm key `'service'`/`$…->product_type` cho hệ số DSTC đã chuyển. (Nếu còn dòng khác dùng `product_type` cho mục đích KHÁC — vd `Serial::where('product_type','tp')` — bỏ qua, không thuộc DSTC.)

- [ ] **Step 9: Smoke test tinker (1 product + 1 service)**

Lưu script scratchpad; chạy trong transaction, dựng input tối thiểu cho 1 nhánh Firm (product) và 1 nhánh Service, so `standard_price` trước/sau. Vì dựng đủ input hợp đồng phức tạp, smoke tối thiểu = gọi trực tiếp helper trong ngữ cảnh thật:

```php
<?php
use Illuminate\Support\Facades\DB;
use App\Support\ProductNatureDstcCoefficient;
DB::beginTransaction();
try {
    // chọn 1 company thật có khai nature (nếu có) + 1 product phân loại
    $cfg = DB::table('company_product_natures')->whereKeyNot(0)->first();
    if ($cfg) {
        $coef = ProductNatureDstcCoefficient::forNature((int)$cfg->company_id, (int)$cfg->product_nature_id);
        echo "forNature company={$cfg->company_id} nature={$cfg->product_nature_id} => {$coef} (DB lưu {$cfg->coefficient})".PHP_EOL;
        assert($coef === (float)$cfg->coefficient);
    } else {
        echo "SKIP: chưa company nào khai nature".PHP_EOL;
    }
    echo "SMOKE OK".PHP_EOL;
} finally { DB::rollBack(); }
```
Chạy, kỳ vọng `SMOKE OK`. Dọn `rm -f` script.

- [ ] **Step 10: Soạn commit (CHƯA chạy git)**

Message dự kiến: `refactor(dstc): doc he so DSTC tu company_product_natures tai 15 diem (WrServiceContract/Firm/Order)`. CHƯA chạy git.

---

## Task 4: Gỡ màn khai hệ số cũ trên ERP (Quy chế công ty)

**Files:**
- Modify: `app/Http/Controllers/Common/CompaniesController.php` (getRegulations ~377/379; postRegulations ~446 + lời gọi saveHistory ~449; `use` CommonCompanyProductTypes dòng 26)
- Modify: `app/Http/Requests/CompanyRegulationRequest.php` (rule dòng 45 + message dòng 91)
- Modify: `resources/views/common/companies/regulation.blade.php` (card "Hệ số quy đổi theo tính chất hàng hóa", ~489–~517)

**Interfaces:**
- Consumes: không.
- Produces: không. (Model `Company::syncProductTypes` + relation `productTypes()` để lại làm dead code — KHÔNG xoá để tránh đụng chạm; không còn caller.)

- [ ] **Step 1: Controller getRegulations — gỡ nạp product_types**

Xoá 2 dòng:
```php
$companyProductType = CommonCompanyProductTypes::select(DB::raw('product_type_id as value'), 'coefficient', 'name')->where('company_id', $company->id)->get()->toArray();
```
```php
$company->product_types = $companyProductType;
```

- [ ] **Step 2: Controller `use` — gỡ import giờ thừa**

```bash
grep -n "CommonCompanyProductTypes" app/Http/Controllers/Common/CompaniesController.php
```
Expected: rỗng sau Step 1 → xoá dòng `use App\Model\Common\CompanyProductTypes as CommonCompanyProductTypes;` (26). (KHÔNG đụng dòng 33 `use App\Model\Order\CompanyProductTypes;` — đã là import thừa sẵn, ngoài phạm vi.)

- [ ] **Step 3: Controller postRegulations — ngừng ghi + chỉnh lời gọi history**

Xoá dòng:
```php
$originalProductTypes = $company->productTypes->toArray();
```
```php
$company->syncProductTypes($request->product_types ?? []);
```
Đổi lời gọi history (truyền `[]` cho 2 tham số product_types, giữ nguyên price_types):
```php
$company->saveHistoryChangeRegulation($company->id, $original, $company->attributesToArray(), $originalProductTypes, $originalPriceTypes, $request->product_types, $request->price_types, $data_include);
```
thành:
```php
$company->saveHistoryChangeRegulation($company->id, $original, $company->attributesToArray(), [], $originalPriceTypes, [], $request->price_types, $data_include);
```
(Guard `if ($originalProductTypes)` trong `saveHistoryChangeRegulation` khiến `[]` bỏ qua nhánh product_types — không vỡ.)

- [ ] **Step 4: Request — gỡ rule product_types**

Trong `CompanyRegulationRequest::rules()` xoá:
```php
'product_types.*.coefficient' => 'required',
```
Trong `messages()` xoá:
```php
'product_types.*.coefficient.required' => 'Bắt buộc phải nhập',
```
(Là rule wildcard → không ép product_types tồn tại; gỡ chỉ để sạch. Giữ `price_types.*.coefficient`.)

- [ ] **Step 5: Blade — gỡ card hệ số theo tính chất**

Xoá nguyên khối `<div class="card"> … </div>` chứa `<h4>Hệ số quy đổi theo tính chất hàng hóa …</h4>` (có nút `ng-click="company.updateProductType()"` và bảng `ng-repeat="type in company.product_types …"`), tức khối bắt đầu ở dòng `<div class="card">` ngay trên h4 đó và kết thúc ở `</div>` ngay TRƯỚC `<div class="card">` của h4 "Tỷ lệ chia DS theo quy chế phối hợp thực hiện". **GIỮ** `<div class="col-md-6">` bao ngoài (nó còn bọc card "Tỷ lệ chia DS").

Để `company.product_types` không còn phần tử nào render, giữ nguyên JS `$scope.product_types` (dead data, vô hại) — KHÔNG sửa `partials/classes/common/CompanyRegulation` (class dùng chung với form price_types). Ghi chú trong plan: dọn JS `$scope.product_types` để lần sau, ngoài phạm vi.

- [ ] **Step 6: Verify màn Quy chế vẫn lưu được (BE + UI)**

BE: đọc lại `postRegulations` không còn tham chiếu `product_types` ngoài 2 `[]`. 
UI (Playwright MCP, `http://127.0.0.1:3000` nếu bật, hoặc URL ERP): mở `company.getRegulations`, sửa 1 hệ số loại giá + lưu → thành công, không lỗi 500, card "tính chất hàng hóa" biến mất. (Nếu không tiện UI → smoke bằng tinker gọi `postRegulations` qua request giả lập là tùy chọn; tối thiểu xác nhận code-path không còn gọi `syncProductTypes`.)
Dọn PNG: `rm -f *.png` cụ thể.

- [ ] **Step 7: Soạn commit (CHƯA chạy git)**

Message dự kiến: `chore(dstc): go card khai he so theo tinh chat hang hoa khoi Quy che cong ty ERP (chuyen sang HRM regulation-config)`. CHƯA chạy git.

---

## Task 5: Rà soát toàn cục + chuẩn bị bàn giao

**Files:** không sửa (chỉ kiểm).

**Interfaces:** Consumes kết quả Task 2–4.

- [ ] **Step 1: Không còn consumer khác của hệ số cũ**

```bash
grep -rnE "company_product_types|->product_types|syncProductTypes" app/ resources/ --include=*.php --include=*.blade.php | grep -viE "reset_price_when_zero_inventory_product_types"
```
Rà từng dòng còn lại: xác nhận không có nơi nào khác ĐỌC hệ số DSTC từ `company_product_types`/`$company->product_types` cho mục đích tính giá. (Bảng `company_product_types` giữ nguyên; `syncProductTypes`/`productTypes()` còn tồn tại trong Company model nhưng không caller — chấp nhận.)

- [ ] **Step 2: Helper là nguồn hệ số DSTC duy nhất**

```bash
grep -rn "ProductNatureDstcCoefficient" app/ | sort
```
Expected: 1 định nghĩa (`app/Support/ProductNatureDstcCoefficient.php`) + 15 lời gọi trong 5 file luồng bán hàng.

- [ ] **Step 3: Bàn giao**

Tổng hợp: helper + 15 điểm + gỡ màn khai. Chờ user xác nhận trước khi commit cả Plan A (HRM) và Plan B (ERP). CHƯA chạy git.

---

## Self-Review (đã rà khi viết)

- **Spec coverage:** Phase 3 spec = helper (Task 2) + 16→**15** điểm đọc (Task 3; spec ghi 16 nhưng grep thực tế 15: WrServiceContract 6 + FirmContract 3 + ZTFirm 2 + PrincipleOrder 2 + ZTPrincipleOrder 2) + gỡ màn khai (Task 4). Tiền đề DB (Task 1) phủ rủi ro spec nêu "cần xác nhận trạng thái DB". ✔
- **Placeholder scan:** mọi step có code/lệnh cụ thể; đường dẫn scratchpad `/private/tmp/claude-501/.../scratchpad/` rút gọn `...` là phần session-id, thay bằng thư mục scratchpad thực lúc chạy. Không có TODO/TBD logic. ✔
- **Type consistency:** `forProduct(?int,$id):float`, `forService(?int):float`, `forNature(?int,int):float`, `clearCache():void` dùng nhất quán giữa Task 2 (định nghĩa) và Task 3 (lời gọi). Mirror HRM Plan A Task 3. ✔
- **Review Focus:** 5 dòng (NULL product_type_id, sentinel 0, hệ số 0 tường minh, company chưa khai, màn Quy chế vẫn lưu) đều có test ở Task 2/Task 4. ✔
- **Số điểm "service" WrServiceContract:** 3 (1227/1345/1438), không phải 2 — đã đếm lại từ grep verbatim. ✔

---

## Follow-up (2026-10-26): Đơn hàng nguyên tắc chỉ cảnh báo DSTC trên mặt hàng có SL ≠ 0

**Yêu cầu user:** Với **đơn hàng nguyên tắc** (Principle Order), chặn/cảnh báo "chưa đủ điều kiện tính DSTC" CHỈ áp cho hàng hoá có số lượng (`quantity`) khác 0. Đơn nguyên tắc cho phép liệt kê dòng SL=0 (chỉ khai nguyên tắc, chưa đặt thực), không nên chặn vì những dòng đó.

**Phạm vi:** CHỈ đơn hàng nguyên tắc — KHÔNG đụng HĐ hãng / phụ lục / HĐ dịch vụ.
- `PrincipleOrderController::store/update` (PrincipleOrderService)
- `ZtecPrincipleOrderController::store/update` (ZTPrincipleOrderService)

**Cách sửa:** trait `ValidatesProductNatureDstc::validateProductNatureDstc(Request, bool $onlyNonZeroQty = false)` — khi `true`, bỏ dòng có `quantity` rỗng/0 khi gom product_id. Truyền `true` tại 4 call-site đơn nguyên tắc. Field SL = `quantity`.

- [x] Thêm tham số `$onlyNonZeroQty` + lọc quantity trong trait (+ helper dstcRowHasQty)
- [x] Truyền `true` ở PrincipleOrderController :83, :288
- [x] Truyền `true` ở ZtecPrincipleOrderController :137, :514
- [x] Verify: php -l sạch 3 file + unit-test dstcRowHasQty 7/7 PASS (qty 0/' 0'/thiếu→bỏ khi flag, qty>0→xét, flag=false luôn xét); commit gop_db
