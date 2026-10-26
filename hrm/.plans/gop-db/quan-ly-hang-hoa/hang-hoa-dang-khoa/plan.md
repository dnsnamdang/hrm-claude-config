# Hàng hoá đang khoá — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn `/master-data/products/locked` liệt kê hàng đang khoá của công ty đang làm việc (Ngừng KD + ERP đã xoá) và khôi phục từng dòng / hàng loạt theo luật đủ giá + đủ phân loại; các màn khác không còn hàng khoá; Thùng rác ERP trỏ sang HRM.

**Architecture:** BE thêm màn thứ 6 `locked` vào `ProductService::applyScreen()` + một lớp luật `ProductRestoreRule` (biểu thức SQL "đủ điều kiện" + đọc gộp lý do thiếu theo trang) dùng chung cho cột "Khôi phục về", ô lọc, và `ProductLifecycleService::restore()`. FE thêm 1 page `extends ProductListPage`, cờ màn `restore`, hành động dòng + thanh hàng loạt "Khôi phục"; cờ `can_unlock` thay bằng `can_restore` ở cả danh sách và footer chi tiết.

**Tech Stack:** Laravel 8 / PHP 7.4 (`php@7.4`), PHPUnit; Nuxt 2 / Vue 2; ERP Laravel Blade.

**Spec:** `.plans/gop-db/quan-ly-hang-hoa/hang-hoa-dang-khoa/design.md`

## Global Constraints

- Nhánh: `gop_db` ở cả 3 checkout chính (`HRM/hrm-api`, `HRM/hrm-client`, `ERP/TanPhatDev`). DB local `hrm_erp_21_10_prod`.
- **Không migration, không seeder, không quyền mới, không ghi DB ngoài test** (spec §5).
- **Không commit / push** — user tự báo (HRM CLAUDE.md + memory *khong-hoi-commit-user-tu-bao*). Mỗi task kết thúc bằng `git status` + `git diff --stat` thay cho commit.
- Quyền ghi duy nhất: `'Xây dựng thông tin hàng hoá'`; xem màn không gate (K4).
- Đủ giá = mọi ĐVT có đủ `price_type_id` 1–6 với `price > 0`, riêng Bán lẻ (1) `price > 1`, tại công ty đang làm việc (K2). Đủ phân loại = `product_type_id` trỏ tới `product_types` có thật **và** `product_characteristic_id` NOT NULL (K3, spec §3.2).
- Đích: đủ cả hai ⇒ pcc `status = 3`; thiếu ⇒ `status = 1` + `info_entered_at` (giữ mốc cũ, NULL thì `now()`).
- Hàng loạt trần **100** id/lượt (K5). Trùng Tên+Model chỉ cảnh báo (K6).
- PHPUnit chạy bằng `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit` trong transaction (`DatabaseTransactions`) — memory *phpunit-chay-tren-db-env-de-lai-rac*: chỉ chạy các file test của task, sau cùng soát `catalog_histories` / `companies.updated_by` không có rác mới.
- FE: badge chữ + màu do BE trả (`*_text` + `*_color`, 9 mã màu chuẩn); nút không dùng được thì ẩn; xác nhận dùng `this.$confirm`.
- Ghi chú lệch spec (chốt khi viết plan, theo HRM CLAUDE.md "hành động chi tiết = danh sách"): footer chi tiết của hàng đang khoá hiện nút **Khôi phục** (thay Mở khóa), không gỡ trắng.

## Review Focus

1. **Hàng ERP đã xoá có `pcc` hàng tạm (6/7/8) của công ty chủ** — phải KHÔNG hiện ở màn locked và restore bỏ qua (hàng tạm xoá mềm "không còn ở đâu"). Test ở Task 2 + Task 3.
2. **Đua 2 người khôi phục cùng mã** — lượt 2 phải ra `skipped` "Hàng không còn ở trạng thái khoá", không ghi đè trạng thái 3 thành 1. Test ở Task 3.
3. **Hàng có ĐVT nhưng thiếu hẳn 1 dòng giá (không phải giá 0)** — phải tính thiếu giá, lý do nêu đúng tên loại giá + ĐVT. Test ở Task 1.
4. **Hàng không có ĐVT nào** — phải tính "thiếu giá" (không được coi là đủ vì `NOT EXISTS` rỗng). Test ở Task 1.
5. **Người đang làm ở công ty khác công ty chủ** — không thấy hàng ERP đã xoá của công ty chủ và restore bỏ qua "Hàng không thuộc công ty". Test ở Task 2 + Task 3.

---

### Task 1: Luật khôi phục `ProductRestoreRule`

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductRestoreRule.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductRestoreRuleTest.php`

**Interfaces:**
- Produces:
  - `ProductRestoreRule::readySql(): string` — biểu thức SQL boolean, 1 tham số bind `?` = company id, dùng trong `selectRaw` / `whereRaw` trên query có bảng `products`.
  - `ProductRestoreRule::reasons(array $productIds, int $companyId): array` — `[product_id => string[]]`, mảng rỗng = đủ điều kiện.
  - `ProductRestoreRule::duplicates(array $productIds): array` — `[product_id => code của hàng status 1 trùng Tên+Model]`.
  - Hằng `PRICE_TYPES = [1,2,3,4,5,6]`, `RETAIL = 1`, `TARGET_TRADING = 'trading'`, `TARGET_ENTERED = 'entered'`, `TARGET_TEXT`, `TARGET_COLOR` (`trading` ⇒ `'Đang kinh doanh'` `#16A34A`; `entered` ⇒ `'Đã nhập thông tin'` `#F59E0B`).

- [ ] **Step 1: Viết test đỏ**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Services\Product\ProductRestoreRule;
use Tests\TestCase;

/** Luật khôi phục hàng đang khoá — `.plans/gop-db/quan-ly-hang-hoa/hang-hoa-dang-khoa/design.md` §3.2 */
class ProductRestoreRuleTest extends TestCase
{
    use DatabaseTransactions;

    private const A = 1;
    private const B = 6;

    /** @var string */
    private $token;
    private $seq = 0;

    protected function setUp(): void
    {
        parent::setUp();
        $this->token = 'RR' . substr(uniqid(), -7);
    }

    private function product(array $extra = []): int
    {
        $this->seq++;

        return (int) DB::table('products')->insertGetId($extra + [
            'code' => $this->token . '-' . $this->seq,
            'name' => 'Hàng khôi phục ' . $this->token . ' ' . $this->seq,
            'status' => 0,
            'company_id' => self::A,
            'brand_id' => (int) DB::table('brands')->value('id'),
            'product_type_id' => (int) DB::table('product_types')->value('id'),
            'product_characteristic_id' => (int) DB::table('product_characteristics')->value('id'),
            'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function unit(int $productId, bool $base = true): int
    {
        return (int) DB::table('product_units')->insertGetId([
            'product_id' => $productId, 'unit_id' => (int) DB::table('units')->value('id'),
            'is_base' => $base ? 1 : 0, 'unit_coefficient' => 1, 'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    /** 6 dòng giá cho ĐVT tại công ty; `$override` = [price_type_id => price | null (bỏ dòng)] */
    private function prices(int $unitId, int $company, array $override = []): void
    {
        foreach (ProductRestoreRule::PRICE_TYPES as $type) {
            $price = array_key_exists($type, $override) ? $override[$type] : 100000;
            if ($price === null) {
                continue;
            }
            DB::table('product_unit_prices')->insert([
                'price_type_id' => $type, 'product_unit_id' => $unitId, 'company_id' => $company,
                'price' => $price, 'coefficient' => 1, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    private function ready(int $productId, int $company): bool
    {
        return (bool) DB::table('products')->where('products.id', $productId)
            ->selectRaw(ProductRestoreRule::readySql() . ' as ok', [$company])->value('ok');
    }

    /** @test */
    public function du_6_gia_moi_dvt_va_du_phan_loai_thi_san_sang()
    {
        $id = $this->product();
        $this->prices($this->unit($id), self::A);
        $this->prices($this->unit($id, false), self::A);

        $this->assertTrue($this->ready($id, self::A));
        $this->assertSame([], ProductRestoreRule::reasons([$id], self::A)[$id]);
    }

    /** @test */
    public function gia_ban_le_1_dong_la_chua_co_gia()
    {
        $id = $this->product();
        $this->prices($this->unit($id), self::A, [1 => 1]);

        $this->assertFalse($this->ready($id, self::A));
        $this->assertStringContainsString('Bán lẻ', implode(' ', ProductRestoreRule::reasons([$id], self::A)[$id]));
    }

    /** @test */
    public function thieu_han_dong_gia_hoac_gia_0_o_dvt_phu_la_thieu()
    {
        $missing = $this->product();
        $this->prices($this->unit($missing), self::A, [4 => null]);
        $zero = $this->product();
        $this->prices($this->unit($zero), self::A);
        $this->prices($this->unit($zero, false), self::A, [6 => 0]);

        $this->assertFalse($this->ready($missing, self::A));
        $this->assertFalse($this->ready($zero, self::A));
        $reasons = ProductRestoreRule::reasons([$missing, $zero], self::A);
        $this->assertStringContainsString('Đại lý cấp 3', implode(' ', $reasons[$missing]));
        $this->assertNotEmpty($reasons[$zero]);
    }

    /** @test */
    public function khong_co_dvt_nao_la_thieu_gia()
    {
        $id = $this->product();

        $this->assertFalse($this->ready($id, self::A));
        $this->assertSame(['Chưa có đơn vị tính / giá bán'], ProductRestoreRule::reasons([$id], self::A)[$id]);
    }

    /** @test */
    public function gia_cong_ty_khac_khong_tinh()
    {
        $id = $this->product();
        $this->prices($this->unit($id), self::B);

        $this->assertFalse($this->ready($id, self::A));
        $this->assertTrue($this->ready($id, self::B));
    }

    /** @test */
    public function thieu_phan_loai_thi_khong_san_sang()
    {
        $noType = $this->product(['product_type_id' => null]);
        $this->prices($this->unit($noType), self::A);
        $noChar = $this->product(['product_characteristic_id' => null]);
        $this->prices($this->unit($noChar), self::A);

        $this->assertFalse($this->ready($noType, self::A));
        $this->assertFalse($this->ready($noChar, self::A));
        $this->assertContains('Chưa đủ phân loại', ProductRestoreRule::reasons([$noType], self::A)[$noType]);
    }

    /** @test */
    public function trung_ten_model_voi_hang_dang_hoat_dong()
    {
        $model = (int) DB::table('product_models')->value('id');
        $active = $this->product(['status' => 1, 'name' => 'Trùng ' . $this->token, 'model_id' => $model]);
        $deleted = $this->product(['name' => 'Trùng ' . $this->token, 'model_id' => $model]);
        $alone = $this->product();

        $dup = ProductRestoreRule::duplicates([$deleted, $alone]);
        $this->assertSame(DB::table('products')->where('id', $active)->value('code'), $dup[$deleted]);
        $this->assertArrayNotHasKey($alone, $dup);
    }
}
```

- [ ] **Step 2: Chạy test, phải đỏ**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductRestoreRuleTest.php`
Expected: FAIL — `Class 'Modules\MasterData\Services\Product\ProductRestoreRule' not found`.

- [ ] **Step 3: Viết lớp luật**

```php
<?php

namespace Modules\MasterData\Services\Product;

use Illuminate\Support\Facades\DB;

/**
 * Luật khôi phục hàng đang khoá (`hang-hoa-dang-khoa/design.md` §3.2, chốt K2/K3 22/10/2026).
 *
 * Đủ điều kiện về *Đang kinh doanh* = (1) có ≥ 1 ĐVT và MỌI ĐVT có đủ 6 loại giá > 0 tại công ty (Bán lẻ > 1 đ —
 * 1 đ là quy ước "chưa có giá") + (2) Loại SP có thật + có Đặc tính. Thiếu ⇒ *Đã nhập thông tin*.
 * Một nguồn luật cho cột "Khôi phục về", ô lọc và `ProductLifecycleService::restore()`.
 */
class ProductRestoreRule
{
    const PRICE_TYPES = [1, 2, 3, 4, 5, 6];
    const RETAIL = 1;

    const TARGET_TRADING = 'trading';
    const TARGET_ENTERED = 'entered';

    const TARGET_TEXT = [
        self::TARGET_TRADING => 'Đang kinh doanh',
        self::TARGET_ENTERED => 'Đã nhập thông tin',
    ];

    const TARGET_COLOR = [
        self::TARGET_TRADING => '#16A34A',
        self::TARGET_ENTERED => '#F59E0B',
    ];

    const REASON_NO_UNIT = 'Chưa có đơn vị tính / giá bán';
    const REASON_CLASSIFICATION = 'Chưa đủ phân loại';

    /** Số loại giá "có thật" của 1 ĐVT tại công ty — bind 1 `?` = company id */
    private static function validPriceCountSql(string $unitAlias): string
    {
        return '(select count(distinct rp.price_type_id) from product_unit_prices rp'
            . ' where rp.product_unit_id = ' . $unitAlias . '.id and rp.company_id = ?'
            . ' and rp.price_type_id in (' . implode(',', self::PRICE_TYPES) . ')'
            . ' and rp.price > case when rp.price_type_id = ' . self::RETAIL . ' then 1 else 0 end)';
    }

    /** Biểu thức boolean trên bảng `products`; bind đúng 1 tham số = company id */
    public static function readySql(): string
    {
        return '(products.product_characteristic_id is not null'
            . ' and exists (select 1 from product_types rt where rt.id = products.product_type_id)'
            . ' and exists (select 1 from product_units ru where ru.product_id = products.id)'
            . ' and not exists (select 1 from product_units ru2 where ru2.product_id = products.id'
            . ' and ' . self::validPriceCountSql('ru2') . ' < ' . count(self::PRICE_TYPES) . '))';
    }

    /**
     * Lý do chưa đủ điều kiện cho từng hàng (đọc gộp — 3 query cho cả trang). `[]` = đủ.
     *
     * @return array<int, string[]>
     */
    public static function reasons(array $productIds, int $companyId): array
    {
        $productIds = array_values(array_unique(array_map('intval', $productIds)));
        $out = array_fill_keys($productIds, []);
        if (!$productIds) {
            return $out;
        }

        $typeNames = DB::table('price_types')->whereIn('id', self::PRICE_TYPES)->pluck('name', 'id');
        $units = DB::table('product_units as pu')->leftJoin('units as u', 'u.id', '=', 'pu.unit_id')
            ->whereIn('pu.product_id', $productIds)->get(['pu.id', 'pu.product_id', 'u.name as unit_name']);
        $valid = DB::table('product_unit_prices')->whereIn('product_unit_id', $units->pluck('id')->all())
            ->where('company_id', $companyId)->whereIn('price_type_id', self::PRICE_TYPES)
            ->whereRaw('price > case when price_type_id = ' . self::RETAIL . ' then 1 else 0 end')
            ->get(['product_unit_id', 'price_type_id'])->groupBy('product_unit_id');

        $byProduct = $units->groupBy('product_id');
        foreach ($productIds as $id) {
            if (!isset($byProduct[$id])) {
                $out[$id][] = self::REASON_NO_UNIT;
                continue;
            }
            foreach ($byProduct[$id] as $unit) {
                $have = isset($valid[$unit->id]) ? $valid[$unit->id]->pluck('price_type_id')->map('intval')->all() : [];
                $missing = array_diff(self::PRICE_TYPES, $have);
                if ($missing) {
                    $names = array_map(function ($t) use ($typeNames) {
                        return $typeNames[$t] ?? ('Loại giá ' . $t);
                    }, array_values($missing));
                    $out[$id][] = 'Thiếu giá ' . implode(', ', $names) . ' (' . ($unit->unit_name ?: 'ĐVT') . ')';
                }
            }
        }

        $unclassified = DB::table('products')->whereIn('id', $productIds)
            ->where(function ($q) {
                $q->whereNull('product_characteristic_id')
                    ->orWhereNotExists(function ($s) {
                        $s->select(DB::raw(1))->from('product_types')->whereColumn('product_types.id', 'products.product_type_id');
                    });
            })->pluck('id');
        foreach ($unclassified as $id) {
            $out[(int) $id][] = self::REASON_CLASSIFICATION;
        }

        return $out;
    }

    /**
     * Hàng `products.status = 1` KHÁC cùng Tên + Model (cảnh báo K6). `[product_id => code hàng trùng]`.
     *
     * @return array<int, string>
     */
    public static function duplicates(array $productIds): array
    {
        if (!$productIds) {
            return [];
        }

        return DB::table('products as d')
            ->join('products as a', function ($j) {
                $j->on('a.name', '=', 'd.name')->whereRaw('a.model_id <=> d.model_id')
                    ->whereColumn('a.id', '<>', 'd.id')->where('a.status', '=', 1);
            })
            ->whereIn('d.id', $productIds)
            ->groupBy('d.id')
            ->selectRaw('d.id, min(a.code) as code')
            ->pluck('code', 'id')->mapWithKeys(function ($code, $id) {
                return [(int) $id => $code];
            })->all();
    }

    public static function target(bool $ready): string
    {
        return $ready ? self::TARGET_TRADING : self::TARGET_ENTERED;
    }
}
```

- [ ] **Step 4: Chạy test, phải xanh**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductRestoreRuleTest.php`
Expected: OK (7 tests).

- [ ] **Step 5: Đo hiệu năng `readySql` trên toàn tập công ty 1**

Run (tinker `--execute`, memory *tinker-file-arg-treo*):
```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='$t=microtime(true); echo DB::table("products")->where("status",0)->where("company_id",1)->whereRaw(Modules\MasterData\Services\Product\ProductRestoreRule::readySql(),[1])->count(), " ", round(microtime(true)-$t,2), "s\n";' 2>&1 | grep -v -i imagick
```
Expected: số ≈ 500 (không vượt 503 — mốc đo 22/10 chưa tính phân loại); thời gian ghi lại. **> 2s ⇒ DỪNG, báo user** (spec §6: cân nhắc bỏ ô lọc "Khôi phục về").

- [ ] **Step 6: Soát thay đổi** — `git -C HRM/hrm-api status --short` chỉ có 2 file mới của task.

---

### Task 2: Màn `locked` ở BE + loại hàng khoá khỏi màn khác + Excel

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductService.php` (hằng màn :30-36, `index()` :65-109, `applyScreen()` :190-252)
- Modify: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/ProductController.php` (thêm `locked()` sau `temp()` :53-56; `listOf()` :78-83)
- Modify: `hrm-api/Modules/MasterData/Routes/api.php` (:491-506)
- Modify: `hrm-api/Modules/MasterData/Transformers/Product/ProductListResource.php` (mảng trả về)
- Modify: `hrm-api/app/ExcelExport/ExportColumnRegistry.php` (sau `products_temp`)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductExportService.php` (`lookups()` / `cell()` cho 3 cột mới)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductLockedScreenTest.php`

**Interfaces:**
- Consumes: `ProductRestoreRule::readySql()`, `::reasons()`, `::duplicates()`, `::TARGET_*` (Task 1).
- Produces:
  - `ProductService::SCREEN_LOCKED = 'locked'`; `ProductService::lockedScopeSql(int $companyId): string` (biểu thức WHERE của màn, không bind) — Task 3 dùng để xét hàng "đang thuộc màn".
  - `GET /api/v1/master-data/products/locked` — mỗi dòng thêm: `lock_source` (`stopped`|`erp_deleted`), `lock_source_text`, `lock_source_color` (`#DC2626` / `#6B7280`), `locked_at` (`d/m/Y`), `restore_target` (`trading`|`entered`), `restore_target_text`, `restore_target_color`, `restore_reasons` (string[]), `duplicate_code` (string|null), `can_restore` (bool).
  - Tham số lọc: `lock_source=stopped|erp_deleted`, `restore_target=trading|entered`.
  - `GET /products/locked/export-rows` (quyền xuất Excel), registry `products_locked`.

- [ ] **Step 1: Viết test đỏ**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\ProductCompany;
use Tests\TestCase;

/** Màn Hàng hoá đang khoá — `hang-hoa-dang-khoa/design.md` §3.1, §3.3 */
class ProductLockedScreenTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private const A = 1;
    private const B = 6;
    private const URL = '/api/v1/master-data/products';

    private $token;
    private $seq = 0;

    protected function setUp(): void
    {
        parent::setUp();
        $this->token = 'LK' . substr(uniqid(), -7);
    }

    private function product(int $status, int $company = self::A, array $extra = []): int
    {
        $this->seq++;

        return (int) DB::table('products')->insertGetId($extra + [
            'code' => $this->token . '-' . $this->seq, 'name' => 'Hàng khoá ' . $this->token . ' ' . $this->seq,
            'status' => $status, 'company_id' => $company, 'brand_id' => (int) DB::table('brands')->value('id'),
            'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function row(int $productId, int $company, ?int $status): void
    {
        DB::table('product_company_coefficients')->insert([
            'product_id' => $productId, 'company_id' => $company, 'coefficient' => 1, 'status' => $status,
            'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function ids(string $screen, string $query = ''): array
    {
        return collect($this->getJson(self::URL . "/$screen?per_page=100&keyword=" . $this->token . $query)->assertOk()->json('data'))
            ->pluck('id')->sort()->values()->all();
    }

    /** @test */
    public function man_locked_gom_2_nguon_cua_cong_ty_dang_lam()
    {
        $stopped = $this->product(1);
        $this->row($stopped, self::A, ProductCompany::STATUS_STOPPED);
        $erpDeleted = $this->product(0);
        $erpDeletedLegacyRow = $this->product(0);
        $this->row($erpDeletedLegacyRow, self::A, null);
        $tempDeleted = $this->product(0);
        $this->row($tempDeleted, self::A, ProductCompany::STATUS_TEMP);
        $otherOwner = $this->product(0, self::B);
        $trading = $this->product(1);
        $this->row($trading, self::A, ProductCompany::STATUS_TRADING);

        $this->actAs(self::A, []);
        $this->assertSame(collect([$stopped, $erpDeleted, $erpDeletedLegacyRow])->sort()->values()->all(), $this->ids('locked'));
        $this->assertSame([$stopped], $this->ids('locked', '&lock_source=stopped'));
    }

    /** @test */
    public function cong_ty_khac_khong_thay_hang_erp_da_xoa_cua_cong_ty_chu()
    {
        $this->product(0, self::A);
        $this->actAs(self::B, []);

        $this->assertSame([], $this->ids('locked'));
    }

    /** @test */
    public function dong_tra_nguon_khoa_dich_khoi_phuc_ly_do_va_co_quyen()
    {
        $id = $this->product(0);
        $this->actAs(self::A, []);
        $row = collect($this->getJson(self::URL . '/locked?per_page=100&keyword=' . $this->token)->json('data'))->firstWhere('id', $id);

        $this->assertSame('erp_deleted', $row['lock_source']);
        $this->assertSame('ERP đã xoá', $row['lock_source_text']);
        $this->assertSame('entered', $row['restore_target']);
        $this->assertSame('Đã nhập thông tin', $row['restore_target_text']);
        $this->assertContains('Chưa có đơn vị tính / giá bán', $row['restore_reasons']);
        $this->assertFalse($row['can_restore']);   // không quyền ⇒ false (fail-closed)

        $this->actAs(self::A, ['Xây dựng thông tin hàng hoá']);
        $row = collect($this->getJson(self::URL . '/locked?per_page=100&keyword=' . $this->token)->json('data'))->firstWhere('id', $id);
        $this->assertTrue($row['can_restore']);
        $this->assertSame([$id], $this->ids('locked', '&restore_target=entered'));
        $this->assertSame([], $this->ids('locked', '&restore_target=trading'));
    }

    /** @test */
    public function man_cong_ty_va_kho_khong_con_hang_ngung_kinh_doanh()
    {
        $stopped = $this->product(1);
        $this->row($stopped, self::A, ProductCompany::STATUS_STOPPED);
        $trading = $this->product(1);
        $this->row($trading, self::A, ProductCompany::STATUS_TRADING);

        $this->actAs(self::A, ['Xây dựng thông tin hàng hoá']);
        $this->assertSame([$trading], $this->ids('company'));
        $this->assertSame([], $this->ids('company', '&company_status=4'));
        $this->assertNotContains($stopped, $this->ids('warehouse'));
        $this->assertContains($trading, $this->ids('warehouse'));
    }

    /** @test */
    public function xuat_excel_man_locked_co_3_cot_moi()
    {
        $this->product(0);
        $this->actAs(self::A, ['Xuất excel danh sách hàng hoá']);
        $res = $this->getJson(self::URL . '/locked/export-rows?keyword=' . $this->token . '&fields[]=code&fields[]=lock_source_text&fields[]=restore_target_text&fields[]=locked_at')
            ->assertOk();

        $this->assertSame(['STT', 'Mã hàng', 'Nguồn khoá', 'Khôi phục về', 'Ngày khoá'], $res->json('data.headings'));
        $this->assertSame('ERP đã xoá', $res->json('data.rows.0.2'));
    }
}
```

> Nếu `ProductExportController` gói kết quả không qua `data.` (kiểm bằng ca export có sẵn trong `ProductExportApiTest.php`), sửa đường dẫn JSON cho khớp trước khi chạy.

- [ ] **Step 2: Chạy test, phải đỏ**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductLockedScreenTest.php`
Expected: FAIL — 404 ở route `/products/locked`.

- [ ] **Step 3: `ProductService` — hằng màn + phạm vi + cột**

Thêm hằng và đưa vào `SCREENS`:
```php
    const SCREEN_LOCKED = 'locked';

    const SCREENS = [self::SCREEN_WAREHOUSE, self::SCREEN_COMPANY, self::SCREEN_ENTERING, self::SCREEN_TRADING, self::SCREEN_TEMP, self::SCREEN_LOCKED];
```

Thêm hàm công khai (đặt trước `applyScreen`):
```php
    /**
     * Phạm vi màn Hàng hoá đang khoá (K1): (A) Ngừng kinh doanh tại công ty · (B) ERP đã xoá do công ty tạo, trừ hàng tạm
     * đã xoá mềm (dòng chủ 6/7/8 — "không còn ở đâu", Phase 6). Cần leftJoin `pcs` (`withCompanyStatus`). Không bind.
     */
    public static function lockedScopeSql(int $companyId): string
    {
        $temp = implode(',', ProductCompany::TEMP_STATUSES);

        return '(' . Product::companyStatusSql($companyId) . ' = ' . ProductCompany::STATUS_STOPPED
            . ' or (products.status = ' . Product::STATUS_DELETED . ' and products.company_id = ' . $companyId
            . ' and not exists (select 1 from product_company_coefficients pct where pct.product_id = products.id'
            . ' and pct.company_id = products.company_id and pct.status in (' . $temp . '))))';
    }
```

Trong `applyScreen()`:
- `SCREEN_WAREHOUSE`: ngay sau dòng `->where('products.status', '<>', Product::STATUS_DELETED);` thêm
```php
                // Hàng đang khoá chỉ ở màn Hàng hoá đang khoá (K7): bỏ cả hàng Ngừng KD tại công ty đang làm việc
                $query->whereRaw('(' . $statusSql . ' IS NULL OR ' . $statusSql . ' <> ?)', [ProductCompany::STATUS_STOPPED]);
```
- `SCREEN_COMPANY`: đổi dòng whereRaw đầu thành
```php
                // Phase 6: hàng tạm (6/7/8) không hiện · K7 (22/10): Ngừng KD (4) chỉ ở màn Hàng hoá đang khoá
                $query->whereRaw($statusSql . ' IS NOT NULL AND ' . $statusSql . ' NOT IN (' . $tempList . ',' . ProductCompany::STATUS_STOPPED . ')');
```
- Thêm case:
```php
            case self::SCREEN_LOCKED:
                $query->whereRaw(self::lockedScopeSql($companyId));
                if ($request->get('lock_source') === 'stopped') {
                    $query->whereRaw($statusSql . ' = ?', [ProductCompany::STATUS_STOPPED]);
                } elseif ($request->get('lock_source') === 'erp_deleted') {
                    $query->where('products.status', Product::STATUS_DELETED);
                }
                if (in_array($request->get('restore_target'), [ProductRestoreRule::TARGET_TRADING, ProductRestoreRule::TARGET_ENTERED], true)) {
                    $query->whereRaw(
                        ($request->get('restore_target') === ProductRestoreRule::TARGET_TRADING ? '' : 'not ') . ProductRestoreRule::readySql(),
                        [$companyId]
                    );
                }
                break;
```

Trong `index()` sau khối `if ($screen === self::SCREEN_TEMP) {...}` thêm:
```php
        if ($screen === self::SCREEN_LOCKED) {
            // Ngày khoá: dòng pcc (Ngừng KD) / dòng products (ERP đã xoá); cờ "đủ điều kiện" cho cột Khôi phục về
            $query->addSelect('pcs.updated_at as pcs_updated_at')
                ->selectRaw(ProductRestoreRule::readySql() . ' as restore_ready', [$companyId]);
        }
```
`use` thêm `Modules\MasterData\Services\Product\ProductRestoreRule` không cần (cùng namespace).

- [ ] **Step 4: Controller + route**

`ProductController` thêm sau `temp()`:
```php
    /** Hàng hoá đang khoá — Ngừng KD + ERP đã xoá của công ty đang làm việc, không gate quyền xem (K4) */
    public function locked(Request $request)
    {
        return $this->listOf($request, ProductService::SCREEN_LOCKED);
    }
```
Đổi `listOf()` để nạp gộp lý do + trùng cho cả trang (1 lần, không N+1):
```php
    private function listOf(Request $request, string $screen)
    {
        $request->merge(['per_page' => max(1, min((int) ($request->per_page ?: 20), self::MAX_PER_PAGE))]);
        $page = $this->service->index($request, $screen)->paginate((int) $request->per_page);
        if ($screen === ProductService::SCREEN_LOCKED) {
            $ids = $page->getCollection()->pluck('id')->all();
            $reasons = ProductRestoreRule::reasons($ids, $this->service->currentCompanyId());
            $duplicates = ProductRestoreRule::duplicates($ids);
            $page->getCollection()->each(function ($p) use ($reasons, $duplicates) {
                $p->setAttribute('restore_reasons', $reasons[$p->id] ?? []);
                $p->setAttribute('duplicate_code', $duplicates[$p->id] ?? null);
            });
        }

        return $this->apiGetList(ProductListResource::apiPaginate($page, $request));
    }
```
> Trước khi viết: mở `Modules/Human/Transformers/ApiResource.php` xem `apiPaginate()` nhận Builder hay paginator. Nếu chỉ nhận Builder, giữ nguyên `apiPaginate($builder, $request)` và đặt việc nạp gộp vào một hook tĩnh của `ProductListResource` (vd `ProductListResource::$lockedLookups`) gán trước khi gọi — không để Resource tự query từng dòng.

`Routes/api.php`: sau `Route::get('/temp', ...)` thêm
```php
        Route::get('/locked', $list . '@locked');   // Hàng hoá đang khoá — không gate quyền xem (K4)
```
và thêm `'locked' => null,` vào `$exportGates`.

- [ ] **Step 5: `ProductListResource` — cột màn locked**

Sau `'can_unlock' => ...` thêm:
```php
            // Màn Hàng hoá đang khoá (22/10): chỉ có khi ProductService gắn `restore_ready`
            'lock_source' => $this->when($this->hasLockedColumns(), function () {
                return $this->lockSource();
            }),
            'lock_source_text' => $this->when($this->hasLockedColumns(), function () {
                return $this->lockSource() === 'erp_deleted' ? 'ERP đã xoá' : 'Ngừng kinh doanh';
            }),
            'lock_source_color' => $this->when($this->hasLockedColumns(), function () {
                return $this->lockSource() === 'erp_deleted' ? '#6B7280' : '#DC2626';
            }),
            'locked_at' => $this->when($this->hasLockedColumns(), function () {
                return Helper::formatDateTime($this->lockSource() === 'erp_deleted' ? $this->updated_at : $this->pcs_updated_at, 'd/m/Y');
            }),
            'restore_target' => $this->when($this->hasLockedColumns(), function () {
                return ProductRestoreRule::target((bool) $this->restore_ready);
            }),
            'restore_target_text' => $this->when($this->hasLockedColumns(), function () {
                return ProductRestoreRule::TARGET_TEXT[ProductRestoreRule::target((bool) $this->restore_ready)];
            }),
            'restore_target_color' => $this->when($this->hasLockedColumns(), function () {
                return ProductRestoreRule::TARGET_COLOR[ProductRestoreRule::target((bool) $this->restore_ready)];
            }),
            'restore_reasons' => $this->when($this->hasLockedColumns(), function () {
                return array_values((array) $this->resource->getAttribute('restore_reasons'));
            }),
            'duplicate_code' => $this->when($this->hasLockedColumns(), function () {
                return $this->resource->getAttribute('duplicate_code');
            }),
            'can_restore' => $this->when($this->hasLockedColumns(), $canBuild),
```
và 2 hàm riêng:
```php
    private function hasLockedColumns(): bool
    {
        return array_key_exists('restore_ready', $this->resource->getAttributes());
    }

    private function lockSource(): string
    {
        return (int) $this->status === 0 ? 'erp_deleted' : 'stopped';
    }
```
`use Modules\MasterData\Services\Product\ProductRestoreRule;`

- [ ] **Step 6: Excel**

`ExportColumnRegistry::COLUMNS` thêm sau `products_temp`:
```php
        'products_locked' => [
            'code' => 'Mã hàng',
            'name' => 'Tên hàng hoá',
            'model_name' => 'Model',
            'product_nature_name' => 'Tính chất hàng hoá',
            'product_function_group_name' => 'Nhóm chức năng',
            'product_family_name' => 'Nhóm sản phẩm',
            'product_type_name' => 'Loại sản phẩm',
            'brand_name' => 'Thương hiệu',
            'manufacturer_name' => 'Hãng sản xuất',
            'barcode' => 'Barcode',
            'unit_name' => 'ĐVT',
            'origin_name' => 'Xuất xứ',
            'order_code_name' => 'Code đặt hàng',
            'english_name' => 'Tên tiếng Anh',
            'vat_percent' => '% VAT',
            'owner_company_name' => 'Công ty quản lý',
            'creator_name' => 'Người nhập thông tin',
            'lock_source_text' => 'Nguồn khoá',
            'restore_target_text' => 'Khôi phục về',
            'locked_at' => 'Ngày khoá',
        ],
```
`ProductExportService::cell()`: thêm 3 nhánh theo khuôn các nhánh có sẵn (đọc `$item->status`, `$item->restore_ready`, `$item->pcs_updated_at` / `$item->updated_at` từ dòng toBase) — chữ lấy đúng hằng như Resource (`'ERP đã xoá'` / `'Ngừng kinh doanh'`, `ProductRestoreRule::TARGET_TEXT`), ngày `d/m/Y`. Không cần lookup thêm.

- [ ] **Step 7: Chạy test, phải xanh**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductLockedScreenTest.php Modules/MasterData/Tests/Feature/ProductRestoreRuleTest.php`
Expected: OK (12 tests).

- [ ] **Step 8: Chạy bộ hàng hoá liên quan (màn khác đổi phạm vi)**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter 'ProductReadApiTest|ProductLifecycleApiTest|TempProductScreenTest|ProductExport' Modules/MasterData/Tests`
Expected: chỉ ca dựa vào "Dữ liệu công ty có status 4" đổi kết quả (vd `co_xoa_khoa_mo_khoa_theo_trang_thai`, `sau_khi_khoa_...`) — sửa ca đó theo luật K7 (đọc dòng status 4 từ màn `locked` thay vì `company`). Mọi ca khác xanh.

- [ ] **Step 9: Đo thời gian 1 trang màn locked công ty 1** — `curl` / Playwright gọi `GET /products/locked?per_page=20` bằng token e2e (đọc `.auth`), ghi thời gian; > 2s thì báo user trước khi đi tiếp.

---

### Task 3: Khôi phục ở BE — `restore()` + `POST /products/restore` + `can_restore` ở chi tiết

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductLifecycleService.php` (thêm mục Khôi phục sau `unlock()` :303-316; `unlock()` gọi `restore`)
- Modify: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/ProductLifecycleController.php`
- Modify: `hrm-api/Modules/MasterData/Routes/api.php` (:535-538)
- Modify: `hrm-api/Modules/MasterData/Entities/Product/Product.php` (thêm `restorableAt()` cạnh `unlockableAt()` :476)
- Modify: `hrm-api/Modules/MasterData/Transformers/Product/ProductDetailResource.php` (:51)
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductHistoryService.php` (`logStatus()` :321 — action `restore`)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/ProductRestoreApiTest.php`; sửa `ProductLifecycleApiTest.php` (ca unlock)

**Interfaces:**
- Consumes: `ProductRestoreRule::readySql()`, `::TARGET_*` (Task 1); `ProductService::lockedScopeSql()` (Task 2).
- Produces:
  - `ProductLifecycleService::restore(array $productIds): array` ⇒ `['trading' => [{id, code}], 'entered' => [{id, code}], 'skipped' => [{id, code, message}]]`.
  - `POST /api/v1/master-data/products/restore` body `{product_ids: int[]}` (1–100), quyền `Xây dựng thông tin hàng hoá` + `dueConfig:Cập nhật hàng hóa`; 422 khi rỗng / > 100.
  - `PUT /products/{id}/unlock` vẫn tồn tại, trả **cùng shape** `restore()` (FE không còn gọi, giữ để client cũ không 404).
  - Chi tiết `GET /products/{id}`: `can_restore` (bool) thay `can_unlock` (bỏ khoá `can_unlock`).
  - Hằng thông báo: `MESSAGE_NOT_LOCKED = 'Hàng không còn ở trạng thái khoá.'`, `MESSAGE_NOT_OWNER = 'Hàng không thuộc công ty đang làm việc.'`, `MESSAGE_RESTORE_CAP = 'Khôi phục tối đa 100 hàng hoá mỗi lượt.'`.

- [ ] **Step 1: Viết test đỏ**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\Product\ProductCompany;
use Modules\MasterData\Services\Product\ProductRestoreRule;
use Tests\TestCase;

/** Khôi phục hàng đang khoá — `hang-hoa-dang-khoa/design.md` §3.2 */
class ProductRestoreApiTest extends TestCase
{
    use DatabaseTransactions;
    use Concerns\ActsAsProductUser;

    private const A = 1;
    private const B = 6;
    private const URL = '/api/v1/master-data/products';
    private const PERM = 'Xây dựng thông tin hàng hoá';

    private $token;
    private $seq = 0;

    protected function setUp(): void
    {
        parent::setUp();
        $this->token = 'RS' . substr(uniqid(), -7);
    }

    private function product(int $status, bool $classified = true, int $company = self::A): int
    {
        $this->seq++;

        return (int) DB::table('products')->insertGetId([
            'code' => $this->token . '-' . $this->seq, 'name' => 'Hàng KP ' . $this->token . ' ' . $this->seq,
            'status' => $status, 'company_id' => $company, 'brand_id' => (int) DB::table('brands')->value('id'),
            'product_type_id' => $classified ? (int) DB::table('product_types')->value('id') : null,
            'product_characteristic_id' => $classified ? (int) DB::table('product_characteristics')->value('id') : null,
            'deleted_at' => $status === 0 ? now() : null,
            'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function fullPrices(int $productId, int $company = self::A): void
    {
        $unit = (int) DB::table('product_units')->insertGetId([
            'product_id' => $productId, 'unit_id' => (int) DB::table('units')->value('id'), 'is_base' => 1,
            'unit_coefficient' => 1, 'created_at' => now(), 'updated_at' => now(),
        ]);
        foreach (ProductRestoreRule::PRICE_TYPES as $type) {
            DB::table('product_unit_prices')->insert([
                'price_type_id' => $type, 'product_unit_id' => $unit, 'company_id' => $company, 'price' => 50000,
                'coefficient' => 1, 'created_at' => now(), 'updated_at' => now(),
            ]);
        }
    }

    private function row(int $productId, int $company, ?int $status, float $coef = 1, $infoEnteredAt = null): int
    {
        return (int) DB::table('product_company_coefficients')->insertGetId([
            'product_id' => $productId, 'company_id' => $company, 'coefficient' => $coef, 'status' => $status,
            'info_entered_at' => $infoEnteredAt, 'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    private function rowOf(int $productId, int $company = self::A)
    {
        return DB::table('product_company_coefficients')->where('product_id', $productId)->where('company_id', $company)->first();
    }

    private function restore(array $ids)
    {
        return $this->postJson(self::URL . '/restore', ['product_ids' => $ids]);
    }

    /** @test */
    public function ngung_kd_du_gia_va_phan_loai_ve_dang_kinh_doanh()
    {
        $id = $this->product(1);
        $this->fullPrices($id);
        $this->row($id, self::A, ProductCompany::STATUS_STOPPED, 1.07);
        $this->actAs(self::A, [self::PERM]);

        $this->restore([$id])->assertOk()->assertJsonPath('data.trading.0.id', $id)->assertJsonCount(0, 'data.entered');
        $this->assertSame(ProductCompany::STATUS_TRADING, (int) $this->rowOf($id)->status);
        $this->assertSame(1.07, (float) $this->rowOf($id)->coefficient);
    }

    /** @test */
    public function ngung_kd_thieu_gia_ve_da_nhap_thong_tin_giu_moc_cu()
    {
        $id = $this->product(1);
        $old = '2026-09-01 08:00:00';
        $this->row($id, self::A, ProductCompany::STATUS_STOPPED, 1, $old);
        $this->actAs(self::A, [self::PERM]);

        $this->restore([$id])->assertOk()->assertJsonPath('data.entered.0.id', $id);
        $row = $this->rowOf($id);
        $this->assertSame(ProductCompany::STATUS_ENTERING_INFO, (int) $row->status);
        $this->assertSame($old, (string) $row->info_entered_at);
    }

    /** @test */
    public function du_gia_nhung_thieu_phan_loai_ve_da_nhap_thong_tin()
    {
        $id = $this->product(1, false);
        $this->fullPrices($id);
        $this->row($id, self::A, ProductCompany::STATUS_STOPPED);
        $this->actAs(self::A, [self::PERM]);

        $this->restore([$id])->assertOk()->assertJsonPath('data.entered.0.id', $id);
        $this->assertNotNull($this->rowOf($id)->info_entered_at);
    }

    /** @test */
    public function erp_da_xoa_chua_co_dong_sinh_dong_va_bat_lai_hang()
    {
        $id = $this->product(0);
        $this->fullPrices($id);
        $employee = $this->actAs(self::A, [self::PERM]);

        $this->restore([$id])->assertOk()->assertJsonPath('data.trading.0.id', $id);
        $p = DB::table('products')->where('id', $id)->first();
        $this->assertSame(1, (int) $p->status);
        $this->assertNull($p->deleted_at);
        $this->assertSame($employee, (int) $p->updated_by);
        $row = $this->rowOf($id);
        $this->assertSame(ProductCompany::STATUS_TRADING, (int) $row->status);
        $this->assertSame(1.0, (float) $row->coefficient);
        $this->assertNotNull($row->info_entered_at);
    }

    /** @test */
    public function erp_da_xoa_co_dong_he_so_cu_thi_update_giu_he_so()
    {
        $id = $this->product(0);
        $rowId = $this->row($id, self::A, null, 1.05);
        $this->actAs(self::A, [self::PERM]);

        $this->restore([$id])->assertOk()->assertJsonPath('data.entered.0.id', $id);
        $row = $this->rowOf($id);
        $this->assertSame($rowId, (int) $row->id);
        $this->assertSame(1.05, (float) $row->coefficient);
        $this->assertSame(ProductCompany::STATUS_ENTERING_INFO, (int) $row->status);
        $this->assertSame(1, DB::table('product_company_coefficients')->where('product_id', $id)->count());
    }

    /** @test */
    public function bo_qua_hang_khong_khoa_cong_ty_khac_hang_tam_da_xoa_va_lan_2()
    {
        $trading = $this->product(1);
        $this->row($trading, self::A, ProductCompany::STATUS_TRADING);
        $otherOwner = $this->product(0, true, self::B);
        $tempDeleted = $this->product(0);
        $this->row($tempDeleted, self::A, ProductCompany::STATUS_TEMP);
        $stopped = $this->product(1);
        $this->row($stopped, self::A, ProductCompany::STATUS_STOPPED);
        $this->actAs(self::A, [self::PERM]);

        $res = $this->restore([$trading, $otherOwner, $tempDeleted, $stopped, 999999999])->assertOk();
        $this->assertSame([$stopped], array_column($res->json('data.entered'), 'id'));
        $skipped = collect($res->json('data.skipped'))->keyBy('id');
        $this->assertSame('Hàng không còn ở trạng thái khoá.', $skipped[$trading]['message']);
        $this->assertSame('Hàng không thuộc công ty đang làm việc.', $skipped[$otherOwner]['message']);
        $this->assertSame('Hàng không còn ở trạng thái khoá.', $skipped[$tempDeleted]['message']);
        $this->assertArrayHasKey(999999999, $skipped->all());
        $this->assertSame(ProductCompany::STATUS_TRADING, (int) $this->rowOf($trading)->status);

        // Lượt 2 (đua): hàng vừa khôi phục không bị ghi lại
        $this->restore([$stopped])->assertOk()->assertJsonPath('data.skipped.0.message', 'Hàng không còn ở trạng thái khoá.');
    }

    /** @test */
    public function khong_quyen_403_va_tran_100()
    {
        $id = $this->product(0);
        $this->actAs(self::A, []);
        $this->restore([$id])->assertStatus(403);
        $this->assertSame(0, (int) DB::table('products')->where('id', $id)->value('status'));

        $this->actAs(self::A, [self::PERM]);
        $this->restore(range(1, 101))->assertStatus(422);
        $this->restore([])->assertStatus(422);
    }

    /** @test */
    public function ghi_lich_su_trang_thai()
    {
        $id = $this->product(1);
        $this->row($id, self::A, ProductCompany::STATUS_STOPPED);
        $this->actAs(self::A, [self::PERM]);
        $before = DB::table('catalog_histories')->where('table', 'products')->where('table_id', $id)->count();

        $this->restore([$id])->assertOk();
        $this->assertSame($before + 1, DB::table('catalog_histories')->where('table', 'products')->where('table_id', $id)->count());
        $this->assertSame('restore', DB::table('catalog_histories')->where('table', 'products')->where('table_id', $id)->orderByDesc('id')->value('action'));
    }

    /** @test */
    public function chi_tiet_tra_can_restore_thay_can_unlock()
    {
        $id = $this->product(1);
        $this->row($id, self::A, ProductCompany::STATUS_STOPPED);
        $this->actAs(self::A, [self::PERM]);

        $data = $this->getJson(self::URL . "/$id")->assertOk()->json('data');
        $this->assertTrue($data['can_restore']);
        $this->assertArrayNotHasKey('can_unlock', $data);

        $erp = $this->product(0);
        $this->assertTrue($this->getJson(self::URL . "/$erp")->assertOk()->json('data.can_restore'));
    }
}
```
> Tên bảng/cột lịch sử (`catalog_histories.table`, `table_id`, `action`) kiểm bằng `ProductHistoryService::TABLE` + `catalog->log()` trước khi chạy; sai thì sửa ca `ghi_lich_su_trang_thai` cho đúng cột thật.

- [ ] **Step 2: Chạy test, phải đỏ**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductRestoreApiTest.php`
Expected: FAIL — 404/405 ở `POST /products/restore`.

- [ ] **Step 3: `Product::restorableAt()`**

Cạnh `unlockableAt()`:
```php
    /**
     * Cờ `can_restore` (Hàng hoá đang khoá, 22/10, chưa xét quyền): Ngừng KD tại công ty, hoặc ERP đã xoá do chính công
     * ty tạo mà không phải hàng tạm đã xoá mềm. Cùng phạm vi `ProductService::lockedScopeSql()`.
     */
    public function restorableAt(int $companyId, ?int $companyStatus): bool
    {
        if ((int) $this->status === self::STATUS_DELETED) {
            return (int) $this->company_id === $companyId && !($companyStatus !== null && ProductCompany::isTemp($companyStatus));
        }

        return ProductCompany::isLocked($companyStatus);
    }
```
> Ca hàng ERP đã xoá có dòng chủ 6/7/8 nhưng người xem đứng ở công ty chủ ⇒ `$companyStatus` chính là dòng chủ ⇒ đúng. Không còn ai gọi `unlockableAt()` sau Step 5 ⇒ xoá hàm.

- [ ] **Step 4: `ProductLifecycleService::restore()`**

Thêm hằng cạnh các `MESSAGE_*`:
```php
    const MESSAGE_NOT_LOCKED = 'Hàng không còn ở trạng thái khoá.';
    const MESSAGE_NOT_OWNER = 'Hàng không thuộc công ty đang làm việc.';
    const MESSAGE_RESTORE_CAP = 'Khôi phục tối đa 100 hàng hoá mỗi lượt.';
    const RESTORE_CAP = 100;
```
Thêm mục mới sau `unlock()` và đổi `unlock()` thành đi qua luật chung:
```php
    /** `PUT /products/{id}/unlock` — giữ route cho client cũ; cùng luật khôi phục (K7: không còn đường 4 → 3 không xét giá) */
    public function unlock(int $productId): array
    {
        return $this->restore([$productId]);
    }

    /* =====================================================================
     | Khôi phục — màn Hàng hoá đang khoá (design §3.2)
     * ================================================================== */

    /**
     * `POST /products/restore` — từng mã: phải đang thuộc màn của công ty đang làm việc; đích theo `ProductRestoreRule`.
     * Xét từng mã, mã không hợp lệ bỏ qua kèm lý do (200), như Lấy về (2-C2).
     */
    public function restore(array $productIds): array
    {
        $this->write->assertCanWrite();
        $ids = array_values(array_unique(array_filter(array_map('intval', $productIds))));
        if (!$ids) {
            $this->fail('Chưa chọn hàng hoá.');
        }
        if (count($ids) > self::RESTORE_CAP) {
            $this->fail(self::MESSAGE_RESTORE_CAP);
        }
        $companyId = $this->companyId();

        return DB::transaction(function () use ($ids, $companyId) {
            $out = ['trading' => [], 'entered' => [], 'skipped' => []];
            $products = Product::query()->lockForUpdate()->whereIn('id', $ids)->get()->keyBy('id');
            $rows = DB::table('product_company_coefficients')->whereIn('product_id', $ids)->lockForUpdate()->get()->groupBy('product_id');
            $ready = Product::query()->whereIn('products.id', $products->keys()->all())
                ->selectRaw('products.id, ' . ProductRestoreRule::readySql() . ' as ok', [$companyId])
                ->pluck('ok', 'id');

            foreach ($ids as $id) {
                $product = $products->get($id);
                if (!$product) {
                    $out['skipped'][] = ['id' => $id, 'code' => null, 'message' => 'Hàng hoá không tồn tại.'];
                    continue;
                }
                $row = ($rows[$id] ?? collect())->firstWhere('company_id', $companyId);
                $status = $row && $row->status !== null ? (int) $row->status : null;
                $erpDeleted = (int) $product->status === Product::STATUS_DELETED;
                if ($erpDeleted && (int) $product->company_id !== $companyId) {
                    $out['skipped'][] = ['id' => $id, 'code' => $product->code, 'message' => self::MESSAGE_NOT_OWNER];
                    continue;
                }
                if (!$product->restorableAt($companyId, $status)) {
                    $out['skipped'][] = ['id' => $id, 'code' => $product->code, 'message' => self::MESSAGE_NOT_LOCKED];
                    continue;
                }

                $target = !empty($ready[$id]) ? ProductCompany::STATUS_TRADING : ProductCompany::STATUS_ENTERING_INFO;
                if ($erpDeleted) {
                    DB::table('products')->where('id', $id)->update([
                        'status' => Product::STATUS_ACTIVE, 'deleted_at' => null, 'updated_by' => $this->userId(), 'updated_at' => now(),
                    ]);
                }
                $set = ['status' => $target, 'updated_by' => $this->userId(), 'updated_at' => now()];
                if ($target === ProductCompany::STATUS_ENTERING_INFO || !$row || $row->info_entered_at === null) {
                    // Đã nhập thông tin = status 1 + mốc (giữ mốc cũ); hàng về 3 cũng gắn mốc để sau này khoá–khôi phục lại không thành "chưa nhập"
                    $set['info_entered_at'] = $row && $row->info_entered_at !== null ? $row->info_entered_at : now();
                }
                if ($row) {
                    DB::table('product_company_coefficients')->where('id', $row->id)->update($set);
                } else {
                    // Hàng ERP đã xoá chưa có dòng công ty ⇒ sinh dòng coef 1 (như G4); company_id gán TAY (DB::table)
                    DB::table('product_company_coefficients')->insert($set + [
                        'product_id' => $id, 'company_id' => $companyId, 'coefficient' => 1,
                        'created_by' => $this->userId(), 'created_at' => now(),
                    ]);
                }
                $this->history()->logStatus($id, $companyId, $status, $target, 'restore', $erpDeleted ? 'Khôi phục hàng ERP đã xoá' : null);
                $out[$target === ProductCompany::STATUS_TRADING ? 'trading' : 'entered'][] = ['id' => $id, 'code' => $product->code];
            }

            return $out;
        });
    }
```
`use` thêm `Modules\MasterData\Services\Product\ProductRestoreRule` không cần (cùng namespace).

Ở `ProductHistoryService::logStatus()` không cần sửa (đã nhận `$action`); kiểm `$from === $to` không chặn (ERP đã xoá: `null → 3` khác nhau). Nếu bảng nhãn hành động lịch sử (FE `SystemInfoSection` / BE map action ⇒ chữ) có danh sách cố định, thêm `'restore' => 'Khôi phục'` — grep `'unlock' =>` trong `ProductHistoryService.php` và `hrm-client/components` để thêm cùng chỗ.

- [ ] **Step 5: Controller, route, chi tiết**

`ProductLifecycleController`:
```php
    /** Hàng hoá đang khoá — từng dòng hoặc hàng loạt (≤ 100) */
    public function restore(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->restore((array) $request->input('product_ids', [])));
    }
```
(`use Illuminate\Http\Request;`). Docblock lớp: bỏ "Từng dòng, không hàng loạt (V7)", ghi "Khôi phục hàng loạt ≤ 100 (K5, 22/10)".

`Routes/api.php` sau dòng `unlock`:
```php
        // Hàng hoá đang khoá (22/10): khôi phục từng dòng / hàng loạt — đứng TRƯỚC `GET /{product}` (không trùng mẫu số)
        Route::post('/restore', $lifecycle . '@restore')->middleware(['checkPermission:' . $build, 'dueConfig:Cập nhật hàng hóa']);
```

`ProductDetailResource` :51 đổi:
```php
            'can_restore' => $canBuild && $this->resource->restorableAt($companyId, $status),
```
và `ProductListResource` đổi khoá `'can_unlock' => ...` thành
```php
            'can_restore' => $canBuild && $this->resource->restorableAt($companyId, $status),
```
— đồng thời **bỏ** dòng `'can_restore' => $this->when($this->hasLockedColumns(), $canBuild),` thêm ở Task 2 Step 5 (một nguồn cờ).

- [ ] **Step 6: Sửa ca cũ của `ProductLifecycleApiTest`**

- `flags()` (:136): đổi `'can_unlock' => $row['can_unlock']` ⇒ `'can_restore' => $row['can_restore']`; mọi kỳ vọng `can_unlock` trong các ca đổi tên tương ứng.
- `khoa_mo_khoa_dong_that` / `khoa_hang_cu_da_backfill_giu_he_so_va_dong`: `unlock()` nay trả shape `restore` và hàng fixture KHÔNG có giá ⇒ đích 1. Đổi assert:
```php
        $this->unlock($id)->assertOk()->assertJsonPath('data.entered.0.id', $id);
        $this->assertSame(ProductCompany::STATUS_ENTERING_INFO, (int) $this->rowOf($id, self::A)->status);
        $this->assertSame(1.07, (float) $this->rowOf($id, self::A)->coefficient);
```
- `khoa_mo_khoa_bi_chan`: ca unlock hàng không ở 4 trước đây 422 `MSG_NOT_STOPPED`; nay 200 + `data.skipped.0.message` = `'Hàng không còn ở trạng thái khoá.'`. Sửa kỳ vọng, xoá hằng `MSG_NOT_STOPPED` và `MESSAGE_UNLOCK_ONLY_STOPPED` nếu không còn dùng.

- [ ] **Step 7: Chạy test, phải xanh**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductRestoreApiTest.php Modules/MasterData/Tests/Feature/ProductLifecycleApiTest.php Modules/MasterData/Tests/Feature/ProductLockedScreenTest.php Modules/MasterData/Tests/Feature/ProductRestoreRuleTest.php`
Expected: OK, 0 failure.

- [ ] **Step 8: Chạy cả MasterData** — `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests` ; so số đỏ với lượt chạy trên code gốc (chạy `git stash`-KHÔNG được — memory *khong-git-stash-repo-dung-chung*; thay bằng ghi lại danh sách ca đỏ trước khi bắt đầu Task 1 bằng cùng lệnh). Ca đỏ mới ⇒ sửa; đỏ sẵn ⇒ ghi vào báo cáo.

- [ ] **Step 9: Soát rác DB** — sau khi chạy PHPUnit:
```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo DB::table("products")->where("code","like","RR%")->orWhere("code","like","LK%")->orWhere("code","like","RS%")->count(),"\n";' 2>&1 | grep -v -i imagick
```
Expected: `0`.

---

### Task 4: FE — màn Hàng hoá đang khoá, khôi phục, footer chi tiết

**Files:**
- Create: `hrm-client/pages/master-data/products/locked.vue`
- Modify: `hrm-client/utils/product-list-screens.js` (thêm `locked` sau `temp`; header comment)
- Modify: `hrm-client/components/product/ProductListPage.vue` (thanh hàng loạt :194-224, `canSelectRows` :859, `hasActionsColumn` :869, `tickCap` :893, `rowActionsOf` :973-1000, `onRowAction` :1004, `isRowSelectable` :1035, cột mới trong khối render ô, bộ lọc `lock_source` / `restore_target`)
- Modify: `hrm-client/utils/productLifecycle.js` (thay `unlock` bằng `restore`)
- Modify: `hrm-client/pages/master-data/products/_id/index.vue` (:52-66 footer, :194)
- Modify: `hrm-client/pages/master-data/products/_id/edit.vue` (:57 câu 423)
- Modify: `hrm-client/components/subsystem-menu/master-data.js` (sau mục "Hàng đang kinh doanh" :89-92)

**Interfaces:**
- Consumes: API Task 2 (`GET /products/locked`, cột `lock_source*`, `locked_at`, `restore_target*`, `restore_reasons`, `duplicate_code`, `can_restore`) + Task 3 (`POST /products/restore` ⇒ `{trading, entered, skipped}`; chi tiết `can_restore`).
- Produces: `confirmAndRun(vm, 'restore', product)` trong `utils/productLifecycle.js`; `restoreProducts(vm, rows)` (hàng loạt) cùng file.

- [ ] **Step 1: Đọc khuôn trước khi sửa** — đọc `.claude/skills/list-page/SKILL.md` (mục 3c badge, 7.2 footer), `.claude/skills/button-convention/SKILL.md` (chữ "Khôi phục", icon), `.claude/skills/modal-popup/SKILL.md` mục 3a; trong `ProductListPage.vue` tìm cách màn `entering` khai cột `info_status` (template ô + ô lọc `info_status`) — cột/ô lọc mới chép đúng khuôn đó.

- [ ] **Step 2: Cấu hình màn + page + menu**

`utils/product-list-screens.js` thêm sau `temp`:
```js
    // 22/10/2026 — Hàng hoá đang khoá (`.plans/gop-db/quan-ly-hang-hoa/hang-hoa-dang-khoa/design.md`): Ngừng KD (4) +
    // ERP đã xoá của công ty đang làm việc. Không gate xem (K4); Khôi phục từng dòng + hàng loạt ≤ 100 (K5, quyền 1652).
    locked: {
        slug: 'locked',
        exportFileSlug: 'hang_hoa_dang_khoa',
        path: '/master-data/products/locked',
        title: 'Hàng hoá đang khoá',
        filterTitle: 'Bộ lọc hàng hoá đang khoá',
        columns: [...CORE_COLUMNS, ...OPTIONAL_COLUMNS, 'owner_company_name', 'creator_name', 'lock_source', 'locked_at', 'restore_target'],
        defaultColumns: [...CORE_COLUMNS, 'lock_source', 'locked_at', 'restore_target'],
        filters: ['lock_source', 'restore_target', 'classification', 'brand_id', 'manufacture_id', 'origin_id', 'model_id'],
        catalogRow: false,
        restore: true,
    },
```
Thêm định nghĩa cột (nhãn `Nguồn khoá`, `Ngày khoá`, `Khôi phục về`) và ô lọc (`lock_source`: Ngừng kinh doanh / ERP đã xoá; `restore_target`: Đang kinh doanh / Đã nhập thông tin) vào đúng bảng định nghĩa cột / ô lọc mà `info_status` đang dùng; `productExportFields()` khớp registry `products_locked` (`lock_source` ⇒ `lock_source_text`, `restore_target` ⇒ `restore_target_text`).

`pages/master-data/products/locked.vue`:
```vue
<script>
import ProductListPage from '@/components/product/ProductListPage.vue'

/**
 * Hàng hoá đang khoá — Ngừng kinh doanh + hàng ERP đã xoá của công ty đang làm việc; Khôi phục về Đang kinh doanh khi đủ
 * 6 giá + phân loại, không thì về Đã nhập thông tin. Logic ở `ProductListPage.vue`, cấu hình ở `utils/product-list-screens.js`.
 */
export default {
    extends: ProductListPage,
    layout: 'default-sidebar',
    productScreen: 'locked',
}
</script>
```

Menu `master-data.js` thêm sau "Hàng đang kinh doanh":
```js
            {
                // 22/10/2026: không gate quyền xem (K4) — hàng khoá chỉ hiện ở màn này (K7)
                label: 'Hàng hoá đang khoá',
                link: '/master-data/products/locked',
            },
```

- [ ] **Step 3: Ô bảng 3 cột mới** — trong khối render ô của `ProductListPage.vue` theo khuôn `info_status`:
  - `lock_source`: `<V2BaseBadge :color="item.lock_source_color">{{ item.lock_source_text }}</V2BaseBadge>`
  - `locked_at`: chữ thường.
  - `restore_target`: badge `restore_target_color/text`; dưới badge, khi `item.restore_reasons.length`, 1 dòng chữ xám `#6b7280` 12px nối `restore_reasons.join(' · ')` cắt 1 dòng + tooltip đủ (khuôn tooltip đang dùng cho ô cắt dòng của bảng — tìm `v2-cell` có tooltip, không `title=""`).
  - Cạnh tên hàng khi `item.duplicate_code`: icon `ri-error-warning-line` màu `#F59E0B` + `b-popover` `custom-class="info-popover"` nội dung `Trùng Tên + Model với hàng đang hoạt động ${item.duplicate_code}` (khuôn info-icon-tooltip).

- [ ] **Step 4: Hành động dòng + hàng loạt**

Computed:
```js
        /** Màn Hàng hoá đang khoá: Khôi phục (quyền 1652, fail-closed) — từng dòng + tick hàng loạt ≤ 100 */
        canRestore() {
            return !!this.screen.restore && this.canBuildProduct
        },
```
- `canSelectRows`: `return this.canBuildCatalog || this.canTakeBack || this.canPriceAsk || this.canRestore`
- `hasActionsColumn`: trước dòng `return !!(this.screen.rowActions ...)` thêm `if (this.screen.restore) return this.canRestore`
- `tickCap`: `return this.canTakeBack || this.canRestore ? TAKE_CAP : Infinity` (TAKE_CAP = 100; thông báo trần dùng câu riêng `RESTORE_CAP_MESSAGE = 'Khôi phục tối đa 100 hàng hoá mỗi lượt'` khi `canRestore`).
- `isRowSelectable`: dòng đầu thêm `if (this.canRestore) return !!row.can_restore`
- `rowActionsOf`: đầu hàm thêm
```js
            if (this.screen.restore) {
                return [
                    { key: 'restore', title: 'Khôi phục', icon: 'ri-arrow-go-back-line', visible: this.canRestore && !!item.can_restore },
                    this.historyAction(),
                ]
            }
```
và xoá dòng `{ key: 'unlock', ... }`; sửa docblock (bỏ "4: Mở khóa").
- `onRowAction`: `else if (key === 'restore') { this.restoreRows([item]) }`; bỏ `'unlock'` khỏi điều kiện `runLifecycle`.
- Thanh hàng loạt thêm nút (sau nút Lấy về):
```vue
                        <V2BaseButton v-if="canRestore" primary size="sm" class="btn-compact" title="Khôi phục các hàng đã chọn" :interactable="!restoring" @click="restoreRows(selectedRows)">
                            <template #prefix><i class="ri-arrow-go-back-line" style="font-size: 13px"></i></template>
                            Khôi phục
                        </V2BaseButton>
```
- data: `restoring: false`. method:
```js
        /** Khôi phục (22/10): hỏi → POST restore → toast kết quả + mã bỏ qua → bỏ tick → tải lại, ở lại màn */
        async restoreRows(rows) {
            if (this.restoring || !rows.length) return
            this.restoring = true
            try {
                const res = await restoreProducts(this, rows, this.currentCompanyName)
                if (!res.ok && !res.reload) return
                if (rows.length === 1) this.$delete(this.listSelected, rows[0].id)
                else this.listSelected = {}
                this.loadData()
            } finally {
                this.restoring = false
            }
        },
```
import `restoreProducts` từ `@/utils/productLifecycle.js`.

- [ ] **Step 5: `utils/productLifecycle.js`**

Header: thay dòng `PUT .../unlock` bằng `POST master-data/products/restore {product_ids} → { data: { trading: [{id, code}], entered: [...], skipped: [{id, code, message}] } }`. Bỏ nhánh câu hỏi/thông báo `unlock` (`confirmOptions` cuối hàm, `successMessage`, `FALLBACK_ERROR.unlock`). Thêm:
```js
const RESTORE_SKIPPED_SHOW = 5

function restoreQuestion(rows, company) {
    const dup = rows.filter((r) => r.duplicate_code)
    const head =
        rows.length === 1
            ? `Khôi phục hàng hoá ${rows[0].code} tại ${company}? Hàng về ${rows[0].restore_target_text || 'trạng thái theo giá bán hiện có'}.`
            : `Khôi phục ${rows.length} hàng hoá đã chọn tại ${company}? Hàng đủ 6 loại giá và phân loại về Đang kinh doanh, còn lại về Đã nhập thông tin.`
    const warn = dup.length
        ? ` Lưu ý: ${dup.slice(0, RESTORE_SKIPPED_SHOW).map((r) => `${r.code} trùng ${r.duplicate_code}`).join(', ')}${dup.length > RESTORE_SKIPPED_SHOW ? '…' : ''}.`
        : ''
    return { title: 'Xác nhận khôi phục', message: head + warn, textAccept: 'Khôi phục', acceptIcon: 'ri-arrow-go-back-line', danger: false }
}

/**
 * Khôi phục 1 hay nhiều hàng (màn Hàng hoá đang khoá + footer chi tiết). Trả `{ ok, data }` | `{ ok: false, cancelled }` |
 * `{ ok: false, status, reload }` như `confirmAndRun`. BE xét từng mã, trả 200 kể cả khi bỏ qua hết.
 */
export async function restoreProducts(vm, rows, companyName) {
    if (vm._productLifecycleBusy) return { ok: false, cancelled: true }
    const company = companyName || currentCompanyName(vm.$store)
    if (!(await vm.$confirm(restoreQuestion(rows, company)))) return { ok: false, cancelled: true }

    vm._productLifecycleBusy = true
    vm.$safeLoadingStart()
    try {
        const res = await vm.$store.dispatch('apiPostMethod', { url: `${API}/restore`, payload: { product_ids: rows.map((r) => r.id) } })
        const { trading = [], entered = [], skipped = [] } = (res && res.data) || {}
        const what = (list) => (list.length === 1 ? list[0].code : `${list.length} hàng hoá`)
        if (trading.length) vm.$toasted.global.success({ message: `Đã khôi phục ${what(trading)} — trạng thái Đang kinh doanh` })
        if (entered.length) vm.$toasted.global.success({ message: `Đã khôi phục ${what(entered)} — trạng thái Đã nhập thông tin` })
        if (skipped.length) {
            const listed = skipped.slice(0, RESTORE_SKIPPED_SHOW).map((s) => `${s.code || `#${s.id}`} (${s.message})`).join(', ')
            vm.$toasted.global.warning({ message: `Bỏ qua ${skipped.length} hàng hoá: ${listed}${skipped.length > RESTORE_SKIPPED_SHOW ? '…' : ''}` })
        }
        return { ok: true, data: { trading, entered, skipped } }
    } catch (error) {
        const status = error && error.response && error.response.status
        if (![403, 500, 504].includes(status)) {
            const body = (error && error.response && error.response.data) || {}
            vm.$toasted.global.error({ message: body.message || 'Khôi phục hàng hoá không thành công' })
        }
        return { ok: false, status, reload: status === 404 || status === 423 }
    } finally {
        vm._productLifecycleBusy = false
        vm.$safeLoadingFinish()
    }
}
```
> Khuôn toast bỏ qua chép từ `notifyTakeResult` (ProductListPage :1150) — nếu nó dùng `warning` hay `error` khác, theo đúng nó.

- [ ] **Step 6: Footer chi tiết + edit**

`_id/index.vue`: thay nút `can_unlock` (:65-68) bằng
```vue
                <V2BaseButton v-if="canBuild && product.can_restore" primary size="sm" status="success" class="mr-2 mb-2" @click="restore">
                    <template #prefix><i class="ri-arrow-go-back-line"></i></template>
                    Khôi phục
                </V2BaseButton>
```
(giữ đúng class lề như nút Khóa bên cạnh), method:
```js
        async restore() {
            const res = await restoreProducts(this, [this.product])
            if (res.ok) {
                this.markFormSaved && this.markFormSaved()
                this.$router.push('/master-data/products/locked')
            } else if (res.reload) {
                this.loadData ? this.loadData() : this.$nuxt.refresh()
            }
        },
```
(tên hàm tải lại lấy đúng hàm đang dùng ở nhánh `runLifecycle` :194). Sửa comment :52. `edit.vue` :57 câu mặc định ⇒ `'Hàng hoá đang khoá, vui lòng khôi phục ở màn Hàng hoá đang khoá trước khi cập nhật.'`.

- [ ] **Step 7: Kiểm nhanh không còn dấu vết `unlock`** — `grep -rn "can_unlock\|'unlock'" hrm-client/components/product hrm-client/pages/master-data/products hrm-client/utils/productLifecycle.js` phải rỗng; `grep -rn '<input \|<button \|class="btn ' hrm-client/pages/master-data/products/locked.vue` rỗng.

- [ ] **Step 8: Kiểm bằng Playwright MCP (bắt buộc)** — mở `http://127.0.0.1:3000` (memory: restart Nuxt nếu báo thiếu component; không chạy `networkidle`). Tài khoản có 1652 tại công ty 1 (role tạm nếu cần — memory *local-dev-duoc-cap-quyen-de-test*, gỡ + `Cache::forget` spatie khi xong). Đo bằng DOM:
  1. Menu Hàng hoá, vật tư có mục "Hàng hoá đang khoá" (đếm link trên hub).
  2. `/master-data/products/locked`: số dòng tổng ở phân trang = `total` của API cùng bộ lọc; 3 cột mặc định có badge (`getComputedStyle` màu nền khác nhau theo nguồn); dòng lý do xám `#6b7280`, 1 dòng.
  3. Lọc Khôi phục về = Đang kinh doanh ⇒ request có `restore_target=trading`, số dòng khớp API; ghi thời gian request.
  4. Tick 2 dòng ⇒ thanh "Đã chọn 2" + nút Khôi phục; 2 nút liền nhau cách 12px.
  5. Khôi phục 1 dòng **trên dữ liệu test tự tạo** (chèn 1 hàng `status 0` mã `E2ELK…` qua tinker, xoá lại sau) ⇒ toast đúng đích, dòng biến mất, hàng xuất hiện ở màn Hàng hoá nhập thông tin / Đang kinh doanh tương ứng.
  6. Không quyền (tài khoản không 1652): không cột Hành động, không ô tick.
  7. `/master-data/products/company` lọc Trạng thái không còn option Ngừng kinh doanh.
  8. Chi tiết hàng đang khoá: footer có "Khôi phục", không có "Mở khóa"; số nút = số nút ở dòng danh sách.
  9. Console 0 lỗi; màn 1280 không cuộn ngang trang.

- [ ] **Step 9: Cập nhật e2e (không tự chạy cả bộ)** — memory *e2e-hrm-lech-ban-worktree*: diff `HRM/e2e` với `wt-chuyen-doi-hang-hoa/e2e` trước. Thêm `e2e/tests/products-locked.spec.ts` (ca: có quyền thấy cột Hành động + khôi phục 1 dòng fixture; không quyền không có cột; màn company không có option 4) và sửa spec lifecycle cũ đang bấm "Mở khóa" sang luồng mới. Chỉ chạy khi user yêu cầu (`--workers=1`).

---

### Task 5: ERP — Thùng rác trỏ sang HRM

**Files:**
- Modify: `ERP/TanPhatDev/app/Http/Middleware/ProductMovedToHrm.php` (`TARGETS`, sau `'temp-list'`)
- Modify: `ERP/TanPhatDev/routes/web.php:606`
- Modify: `ERP/TanPhatDev/resources/views/products/list.blade.php:42-44`

**Interfaces:**
- Consumes: route HRM `/master-data/products/locked` (Task 4).
- Produces: khoá `'product-locked'`.

- [ ] **Step 1: Middleware** — thêm vào `TARGETS`:
```php
        // 22/10/2026 — Thùng rác hàng hoá ⇒ màn Hàng hoá đang khoá HRM (khôi phục chỉ làm ở HRM)
        'product-locked' => '/master-data/products/locked',
```

- [ ] **Step 2: Route** — `routes/web.php:606` đổi thành:
```php
        Route::get('/deleted', 'ProductsController@deleted')->name('products.deleted')->middleware('productMovedToHrm:product-locked')->middleware('checkPermission:Sửa hàng hóa', 'checkDueConfigs');
```

- [ ] **Step 3: Nút** — `products/list.blade.php:42`:
```blade
							<a href="{{ \App\Http\Middleware\ProductMovedToHrm::buildHrmUrl('product-locked') }}" class="btn btn-secondary">
								Thùng rác
							</a>
```
> Kiểm chữ ký `buildHrmUrl($key, $id = null)` trong middleware trước khi viết; nếu bắt buộc `$id` thì truyền `null`.

- [ ] **Step 4: Kiểm** — `cd ERP/TanPhatDev && php -l app/Http/Middleware/ProductMovedToHrm.php && php -l routes/web.php`; `php artisan route:list --name=products.deleted` (sau `config:clear` — memory *erp-local-config-cache-tro-production*) thấy middleware `productMovedToHrm:product-locked`; KHÔNG `view:cache` để lint Blade (memory *erp-blade-json-directive-gotcha*) — mở trang danh sách hàng hoá ERP bằng Playwright, đo `href` nút Thùng rác kết thúc `/master-data/products/locked`, mở `/products/deleted` ra trang "Chức năng đã chuyển sang HRM" có link đúng.

---

### Task 6: Tổng kiểm + cập nhật tài liệu

- [ ] **Step 1:** Chạy lại 4 file test mới/sửa + cả `Modules/MasterData/Tests`; so danh sách đỏ với mốc ghi trước Task 1.
- [ ] **Step 2:** `git -C HRM/hrm-api diff --stat`, `git -C HRM/hrm-client diff --stat`, `git -C ERP/TanPhatDev diff --stat` — chỉ các file trong plan; `git diff --numstat` không có file bị đổi EOL toàn bộ.
- [ ] **Step 3:** Soát rác DB (Task 3 Step 9) + role tạm đã gỡ.
- [ ] **Step 4:** Cập nhật `design.md` (ghi chú footer "Khôi phục" thay "gỡ Mở khoá"), checkpoint cuối file này, dòng đầu `SO-CHOT-VA-TON.md`. **Không commit** — báo user kết quả kèm số đo.

---

### Checkpoint — 22/10/2026 (wrap up)
Vừa hoàn thành: Task 1–6 + review cuối (3 lỗi đã sửa) — ĐÃ PUSH gop_db: api `7f6ae6e4d`, client `aea4d8983`, ERP `710d383568`.
Đang làm dở: —
Bước tiếp theo: user nghiệm thu local ⇒ pull prod; chạy e2e 5 spec đã sửa khi có tài khoản e2e trên DB dev.
Blocked: e2e chưa provision trên `hrm_erp_21_10_prod`.

### Checkpoint — 22/10/2026 (thực thi)
Vừa hoàn thành: Task 1–6 (native, user "Làm, native"); ledger `progress.md` ghi mọi ruling.
Đang làm dở: review cuối toàn nhánh.
Bước tiếp theo: xử lý phát hiện Critical/Important của review; user tự commit/push (3 repo gop_db).
Blocked: e2e không chạy được trên `hrm_erp_21_10_prod` (không có tài khoản e2e) — spec đã sửa, chờ môi trường.
