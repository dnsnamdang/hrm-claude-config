# Điều khoản báo giá / thanh toán per-company (GIAI ĐOẠN 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port 2 màn quản lý điều khoản của ERP (`quotation_terms` theo loại báo giá, `payment_method_terms` theo phương thức thanh toán) vào màn regulation-config của HRM dưới dạng 2 tab "thư viện" **tách riêng theo công ty**, rồi gỡ 2 màn admin điều khoản bên ERP (ERP chỉ còn tiêu thụ qua `getForSelect` đã lọc công ty).

**Architecture:** Thêm cột `company_id` vào 2 bảng ERP dùng chung (backfill về công ty id 1). HRM thêm 2 Entity trỏ 2 bảng đó, 1 `SHAPE_LIBRARY` mới trong `RegulationTabRegistry`, CRUD từng-dòng theo công ty trong `RegulationConfigService`/`RegulationConfigController` (mirror khối grid có sẵn, đổi ownership từ department → company), và render tab "library" ở FE với modal CKEditor. Không ghi lịch sử (bám ERP). ERP chỉ sửa chiều đọc + gỡ 2 màn admin.

**Tech Stack:** hrm-api (Laravel 8 / PHP 7.4, module `Modules/MasterData`), hrm-client (Nuxt 2 / Vue 2, Node 14), ERP `ERP/TanPhatDev` (Laravel 8 / PHP 7.4, Blade + AngularJS). DB dùng chung `erp_hrm_check`. Test: PHPUnit (feature) + Playwright (`HRM/e2e`, Node 20).

**Spec:** `HRM/.plans/gop-db/dieukhoan-per-company/design.md`

## Global Constraints

- **Scope thư mục:** thao tác HRM chỉ trong `HRM/`, thao tác ERP chỉ trong `ERP/TanPhatDev/`. KHÔNG tạo file ở root `ERP-HRM/`. Đường dẫn dưới đây ghi tương đối từ `HRM/` hoặc `ERP/TanPhatDev/` (đã ghi rõ mỗi task).
- **gop_db:** DB dùng chung; ghi vào bảng ERP có sẵn; CHỈ thêm cột (nullable) khi nghiệp vụ thực sự cần; KHÔNG tạo bảng mới; KHÔNG dùng `mysql2`/`DB_CONNECTION_SECOND`.
- **Cách 1 (chốt):** dữ liệu tách theo công ty (thêm `company_id`), KHÔNG giữ global.
- **3a (chốt):** backfill 8 `quotation_terms` + 11 `payment_method_terms` về **công ty id 1** (Tân Phát mẹ).
- **4a (chốt):** sửa cả chiều ĐỌC bên ERP để lọc theo công ty đăng nhập.
- **1-ii (chốt):** GỠ 2 màn admin điều khoản bên ERP (route + menu + 2 controller + 2 view dir). GIỮ 2 model ERP. GIỮ perm ERP id 169/174 trong seeder (đừng xoá — tránh vỡ FK `role_has_permissions`).
- **Quyền HRM:** dùng chung gate màn regulation-config = `'Cài đặt cấu hình'` (`RegulationConfigController::PERM_EDIT`). KHÔNG tạo permission riêng. KHÔNG hard-code `true` (fail-closed).
- **Lịch sử:** KHÔNG ghi `regulation_config_histories` cho điều khoản (bám ERP). Chỉ `created_by`/`updated_by`.
- **Route regex có sẵn = `[a-z]+`** (không nhận `_`) → tab key phải KHÔNG dấu gạch dưới: **`dieukhoanbaogia`**, **`dieukhoanthanhtoan`**.
- **Subsystem:** 2 tab library KHÔNG khai key `subsystem` trong `data.js` → mặc định `'master-data'` → hiển thị ở `/sale/regulation-config` (trang này `extends RegulationConfigScreen` không override subsystem; KHÔNG có subsystem `'sale'` — design.md ghi `subsystem:'sale'` là SAI).
- **UI HRM:** modal bắt buộc `V2BaseSelectInModal` cho select; số định dạng quốc tế (`,` nghìn, `.` thập phân); `.text-muted` là ĐỎ → dùng `#6b7280`; xác nhận xoá qua `$confirm`; nút không dùng được thì ẨN (không disable). Nhiều file hrm-client là **CRLF** — giữ nguyên xuống dòng, không convert.
- **Enum (mirror ERP):**
  - `quotation_terms.type`: `1` Báo giá bán hàng · `2` Báo giá thúc đẩy bán · `3` Báo giá gói dịch vụ · `4` Báo giá dự án · `7` Báo giá sửa chữa và vật tư thay thế.
  - `payment_method_terms.payment_method_id`: `1` Thanh toán khi giao hàng · `2` Thanh toán gối đầu · `3` Thanh toán ngay · `4` Thanh toán theo tháng.
- **Ngoài phạm vi G1:** luồng lập báo giá/hợp đồng HRM; G2 (17 field config per-company) — spec riêng.

---

## File Structure

**hrm-api** (`HRM/hrm-api/`, module `Modules/MasterData`):
- `Database/Migrations/2026_09_24_000001_add_company_id_to_term_tables.php` — CREATE. Thêm `company_id` + index cho 2 bảng, backfill về công ty 1, idempotent.
- `Entities/QuotationTerm.php` — CREATE. Trỏ bảng `quotation_terms`, hằng `TYPES`.
- `Entities/PaymentMethodTerm.php` — CREATE. Trỏ bảng `payment_method_terms`, hằng `PAYMENT_METHODS`.
- `Support/RegulationTabRegistry.php` — MODIFY. Thêm `SHAPE_LIBRARY` + 2 tab.
- `Services/RegulationConfigService.php` — MODIFY. Thêm khối CRUD điều khoản theo công ty.
- `Http/Requests/RegulationTermRowRequest.php` — CREATE. Validate title/discriminator/content.
- `Http/Controllers/V1/RegulationConfigController.php` — MODIFY. Nhánh `show()` library + 3 method CRUD + guard `assertVersionTab` chặn library.
- `Routes/api.php` — MODIFY. Thêm route `terms[/{id}]`.
- `Tests/Feature/RegulationTermTest.php` — CREATE. Cô lập công ty (abort 403).

**hrm-client** (`HRM/hrm-client/`):
- `components/regulation-config/data.js` — MODIFY. Thêm 2 group `type:'library'` (KHÔNG `subsystem`).
- `components/regulation-config/RegulationConfigScreen.vue` — MODIFY. Const `LIBRARY_TABS`, computed `curTabIsLibrary`, savebar v-if, render block library + modal, watcher branch, methods.

**e2e** (`HRM/e2e/`):
- `pages/RegulationConfigPage.ts` — CREATE hoặc MODIFY (nếu đã tồn tại thì thêm method).
- `tests/regulation-config/dieukhoan.spec.ts` — CREATE.

**ERP** (`ERP/TanPhatDev/`):
- `app/Model/Common/QuotationTerm.php` — MODIFY `getForSelect` (thêm lọc công ty).
- `app/Model/Common/PaymentMethodTerm.php` — MODIFY `getForSelect` (thêm lọc công ty).
- `routes/web.php` — REMOVE 2 route group (dòng ~5551-5571).
- `resources/views/layouts/topmenubar.blade.php` — REMOVE 2 menu (dòng ~2002-2003).
- `app/Http/Controllers/Common/QuotationTermsController.php` — DELETE.
- `app/Http/Controllers/Common/PaymentMethodTermsController.php` — DELETE.
- `resources/views/common/quotation_terms/` — DELETE dir.
- `resources/views/common/payment_method_terms/` — DELETE dir.

---

## Task 1: Migration — thêm `company_id` + backfill công ty 1

**Files:**
- Create: `HRM/hrm-api/Modules/MasterData/Database/Migrations/2026_09_24_000001_add_company_id_to_term_tables.php`

**Interfaces:**
- Consumes: bảng ERP `quotation_terms`, `payment_method_terms` (đang KHÔNG có `company_id`).
- Produces: cột `quotation_terms.company_id`, `payment_method_terms.company_id` (BIGINT UNSIGNED NULL, có index). Mọi dòng hiện có = `1`.

- [ ] **Step 1: Viết migration idempotent**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * G1 điều khoản per-company: thêm company_id (nullable, ERP-tolerant) vào 2 bảng điều khoản
 * dùng chung với ERP, rồi backfill toàn bộ dòng cũ (do Tân Phát tạo) về công ty id 1.
 */
class AddCompanyIdToTermTables extends Migration
{
    public function up()
    {
        foreach (['quotation_terms', 'payment_method_terms'] as $table) {
            if (Schema::hasTable($table) && !Schema::hasColumn($table, 'company_id')) {
                Schema::table($table, function (Blueprint $t) {
                    $t->unsignedBigInteger('company_id')->nullable()->index()->after('id');
                });
            }
            // Backfill: mọi dòng cũ về công ty mẹ Tân Phát (id 1).
            DB::table($table)->whereNull('company_id')->update(['company_id' => 1]);
        }
    }

    public function down()
    {
        foreach (['quotation_terms', 'payment_method_terms'] as $table) {
            if (Schema::hasTable($table) && Schema::hasColumn($table, 'company_id')) {
                Schema::table($table, function (Blueprint $t) {
                    $t->dropColumn('company_id'); // chỉ bỏ cột, KHÔNG xoá dữ liệu điều khoản
                });
            }
        }
    }
}
```

- [ ] **Step 2: Chạy migration**

Run: `cd HRM/hrm-api && php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_09_24_000001_add_company_id_to_term_tables.php`
Expected: OK. `SHOW COLUMNS FROM quotation_terms LIKE 'company_id'` có 1 dòng; `SELECT COUNT(*) FROM quotation_terms WHERE company_id IS NULL` = 0; tương tự `payment_method_terms`.

- [ ] **Step 3: Verify backfill**

Run: `cd HRM/hrm-api && php artisan tinker --execute="echo DB::table('quotation_terms')->where('company_id',1)->count().'|'.DB::table('payment_method_terms')->where('company_id',1)->count();"`
Expected: in ra `8|11`.

- [ ] **Step 4: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Database/Migrations/2026_09_24_000001_add_company_id_to_term_tables.php
git commit -m "feat(regulation-config): add company_id to term tables + backfill company 1"
```

---

## Task 2: HRM Entity `QuotationTerm` + `PaymentMethodTerm`

**Files:**
- Create: `HRM/hrm-api/Modules/MasterData/Entities/QuotationTerm.php`
- Create: `HRM/hrm-api/Modules/MasterData/Entities/PaymentMethodTerm.php`
- Test: `HRM/hrm-api/Modules/MasterData/Tests/Feature/RegulationTermTest.php` (chỉ 1 test constant ở task này; ownership ở Task 4)

**Interfaces:**
- Consumes: bảng `quotation_terms`, `payment_method_terms` (đã có `company_id` từ Task 1). `App\Models\BaseModel` (auto `created_at`/`updated_at`; `created_by`/`updated_by` khai `$fillable`).
- Produces:
  - `QuotationTerm::TYPES` = `[1=>'Báo giá bán hàng', 2=>..., 7=>...]`; `QuotationTerm::optionsForSelect(): array` trả `[['id'=>int,'name'=>string], ...]`.
  - `PaymentMethodTerm::PAYMENT_METHODS` = `[1=>..., 4=>...]`; `PaymentMethodTerm::optionsForSelect(): array` cùng dạng.
  - Cả 2 `$fillable` gồm `title, content, <discriminator>, company_id, created_by, updated_by`.

- [ ] **Step 1: Viết test hằng số + options (failing)**

Thêm vào `HRM/hrm-api/Modules/MasterData/Tests/Feature/RegulationTermTest.php`:

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\MasterData\Entities\QuotationTerm;
use Modules\MasterData\Entities\PaymentMethodTerm;

class RegulationTermTest extends TestCase
{
    use DatabaseTransactions;

    /** @test */
    public function entities_expose_enum_options_for_select()
    {
        $qt = QuotationTerm::optionsForSelect();
        $this->assertSame(
            [1 => 'Báo giá bán hàng', 2 => 'Báo giá thúc đẩy bán', 3 => 'Báo giá gói dịch vụ', 4 => 'Báo giá dự án', 7 => 'Báo giá sửa chữa và vật tư thay thế'],
            QuotationTerm::TYPES
        );
        $this->assertSame(['id' => 1, 'name' => 'Báo giá bán hàng'], $qt[0]);

        $this->assertSame(
            [1 => 'Thanh toán khi giao hàng', 2 => 'Thanh toán gối đầu', 3 => 'Thanh toán ngay', 4 => 'Thanh toán theo tháng'],
            PaymentMethodTerm::PAYMENT_METHODS
        );
        $this->assertSame(['id' => 1, 'name' => 'Thanh toán khi giao hàng'], PaymentMethodTerm::optionsForSelect()[0]);
    }
}
```

- [ ] **Step 2: Chạy test — fail vì class chưa có**

Run: `cd HRM/hrm-api && php artisan test --filter=entities_expose_enum_options_for_select`
Expected: FAIL — `Class "Modules\MasterData\Entities\QuotationTerm" not found`.

- [ ] **Step 3: Viết 2 Entity**

`HRM/hrm-api/Modules/MasterData/Entities/QuotationTerm.php`:

```php
<?php

namespace Modules\MasterData\Entities;

use App\Models\BaseModel;

/**
 * Điều khoản báo giá theo loại (per-company). Trỏ bảng ERP dùng chung `quotation_terms`.
 * ERP tiêu thụ qua QuotationTerm::getForSelect() (đã lọc công ty). Không ghi lịch sử.
 */
class QuotationTerm extends BaseModel
{
    protected $table = 'quotation_terms';

    protected $fillable = ['title', 'content', 'type', 'company_id', 'created_by', 'updated_by'];

    /** Mirror ERP app/Model/Common/QuotationTerm.php::TYPES. */
    const TYPES = [
        1 => 'Báo giá bán hàng',
        2 => 'Báo giá thúc đẩy bán',
        3 => 'Báo giá gói dịch vụ',
        4 => 'Báo giá dự án',
        7 => 'Báo giá sửa chữa và vật tư thay thế',
    ];

    /** Options cho FE select: [['id'=>int,'name'=>string], ...] theo thứ tự khai TYPES. */
    public static function optionsForSelect(): array
    {
        $out = [];
        foreach (self::TYPES as $id => $name) {
            $out[] = ['id' => $id, 'name' => $name];
        }
        return $out;
    }
}
```

`HRM/hrm-api/Modules/MasterData/Entities/PaymentMethodTerm.php`:

```php
<?php

namespace Modules\MasterData\Entities;

use App\Models\BaseModel;

/**
 * Điều khoản theo phương thức thanh toán (per-company). Trỏ bảng ERP dùng chung `payment_method_terms`.
 */
class PaymentMethodTerm extends BaseModel
{
    protected $table = 'payment_method_terms';

    protected $fillable = ['title', 'content', 'payment_method_id', 'company_id', 'created_by', 'updated_by'];

    /** Mirror ERP public/js/constant.js:259 RULE_CONTRACT_PAYMENT_METHODS. */
    const PAYMENT_METHODS = [
        1 => 'Thanh toán khi giao hàng',
        2 => 'Thanh toán gối đầu',
        3 => 'Thanh toán ngay',
        4 => 'Thanh toán theo tháng',
    ];

    public static function optionsForSelect(): array
    {
        $out = [];
        foreach (self::PAYMENT_METHODS as $id => $name) {
            $out[] = ['id' => $id, 'name' => $name];
        }
        return $out;
    }
}
```

- [ ] **Step 4: Chạy test — pass**

Run: `cd HRM/hrm-api && php artisan test --filter=entities_expose_enum_options_for_select`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Entities/QuotationTerm.php Modules/MasterData/Entities/PaymentMethodTerm.php Modules/MasterData/Tests/Feature/RegulationTermTest.php
git commit -m "feat(regulation-config): add QuotationTerm/PaymentMethodTerm entities"
```

---

## Task 3: Registry — `SHAPE_LIBRARY` + 2 tab

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Support/RegulationTabRegistry.php`

**Interfaces:**
- Consumes: `QuotationTerm::class`, `PaymentMethodTerm::class` (Task 2). Hằng có sẵn `SCOPE_COMPANY`, `SHAPE_SCALAR`, `SHAPE_GRID`. Helper có sẵn `scalarCompanyKeys()`/`scalarKeysForStore()` lọc `shape===SHAPE_SCALAR` → `SHAPE_LIBRARY` tự động bị bỏ qua (như `SHAPE_GRID`).
- Produces:
  - `const SHAPE_LIBRARY = 'library';`
  - 2 tab def key `dieukhoanbaogia` và `dieukhoanthanhtoan`, mỗi def có `'shape'=>SHAPE_LIBRARY`, `'scope'=>SCOPE_COMPANY`, `'no_hen'=>true`, `'model'=>...::class`, `'discriminator'=>'type'|'payment_method_id'`, `'fields'=>[...]`.
  - `RegulationTabRegistry::get('dieukhoanbaogia')['discriminator'] === 'type'`; `...['dieukhoanthanhtoan']['discriminator'] === 'payment_method_id'`.

- [ ] **Step 1: Viết test registry (failing)**

Thêm vào `HRM/hrm-api/Modules/MasterData/Tests/Feature/RegulationTermTest.php` (cùng class):

```php
    /** @test */
    public function registry_exposes_two_library_tabs()
    {
        $baogia = \Modules\MasterData\Support\RegulationTabRegistry::get('dieukhoanbaogia');
        $this->assertSame(\Modules\MasterData\Support\RegulationTabRegistry::SHAPE_LIBRARY, $baogia['shape']);
        $this->assertSame(\Modules\MasterData\Support\RegulationTabRegistry::SCOPE_COMPANY, $baogia['scope']);
        $this->assertTrue($baogia['no_hen']);
        $this->assertSame('type', $baogia['discriminator']);
        $this->assertSame(\Modules\MasterData\Entities\QuotationTerm::class, $baogia['model']);

        $tt = \Modules\MasterData\Support\RegulationTabRegistry::get('dieukhoanthanhtoan');
        $this->assertSame('payment_method_id', $tt['discriminator']);
        $this->assertSame(\Modules\MasterData\Entities\PaymentMethodTerm::class, $tt['model']);

        // SHAPE_LIBRARY không lọt vào danh sách scalar (không bị coi là field cấu hình lưu configs).
        $this->assertNotContains('dieukhoanbaogia', array_keys(\Modules\MasterData\Support\RegulationTabRegistry::scalarKeysForStore()));
    }
```

*(Ghi chú cho người thực thi: `scalarKeysForStore()` trả mảng key→store; test dùng `array_keys`. Nếu chữ ký trả khác, chỉnh assert cho khớp — điểm cốt lõi là 2 tab library KHÔNG xuất hiện trong danh sách scalar.)*

- [ ] **Step 2: Chạy test — fail**

Run: `cd HRM/hrm-api && php artisan test --filter=registry_exposes_two_library_tabs`
Expected: FAIL — `get('dieukhoanbaogia')` abort 404 (tab chưa khai).

- [ ] **Step 3: Thêm hằng + 2 tab vào registry**

Trong `RegulationTabRegistry.php`, cạnh các hằng shape (`SHAPE_SCALAR`, `SHAPE_GRID`), thêm:

```php
    const SHAPE_LIBRARY = 'library';
```

Trong mảng trả về của `tabs()` (nơi khai các tab như `chietkhau`, `hoahong`), thêm 2 entry (dùng FQCN hoặc `use` sẵn có ở đầu file cho 2 Entity):

```php
        'dieukhoanbaogia' => [
            'scope'         => self::SCOPE_COMPANY,
            'shape'         => self::SHAPE_LIBRARY,
            'no_hen'        => true,
            'model'         => \Modules\MasterData\Entities\QuotationTerm::class,
            'discriminator' => 'type',
            'fields'        => [
                'title'   => ['label' => 'Tiêu đề điều khoản', 'type' => 'string',  'required' => true,  'input' => 'text'],
                'type'    => ['label' => 'Loại báo giá',       'type' => 'integer', 'required' => true,  'input' => 'select'],
                'content' => ['label' => 'Nội dung',           'type' => 'string',  'required' => false, 'input' => 'rich'],
            ],
        ],
        'dieukhoanthanhtoan' => [
            'scope'         => self::SCOPE_COMPANY,
            'shape'         => self::SHAPE_LIBRARY,
            'no_hen'        => true,
            'model'         => \Modules\MasterData\Entities\PaymentMethodTerm::class,
            'discriminator' => 'payment_method_id',
            'fields'        => [
                'title'             => ['label' => 'Tiêu đề điều khoản',    'type' => 'string',  'required' => true,  'input' => 'text'],
                'payment_method_id' => ['label' => 'Phương thức thanh toán','type' => 'integer', 'required' => true,  'input' => 'select'],
                'content'           => ['label' => 'Nội dung',             'type' => 'string',  'required' => false, 'input' => 'rich'],
            ],
        ],
```

- [ ] **Step 4: Chạy test — pass**

Run: `cd HRM/hrm-api && php artisan test --filter=registry_exposes_two_library_tabs`
Expected: PASS.

- [ ] **Step 5: Verify không vỡ pipeline scalar/grid có sẵn**

Run: `cd HRM/hrm-api && php artisan test Modules/MasterData/Tests/Feature/RegulationConfigSchemaTest.php Modules/MasterData/Tests/Feature/RegulationHistoryTest.php`
Expected: PASS (SHAPE_LIBRARY bị các helper scalar/grid bỏ qua, không rớt vào getHistory/scalarKeysForStore).

- [ ] **Step 6: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Support/RegulationTabRegistry.php Modules/MasterData/Tests/Feature/RegulationTermTest.php
git commit -m "feat(regulation-config): register 2 library term tabs (SHAPE_LIBRARY)"
```

---

## Task 4: Service — CRUD điều khoản theo công ty (ownership abort 403)

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Services/RegulationConfigService.php`
- Test: `HRM/hrm-api/Modules/MasterData/Tests/Feature/RegulationTermTest.php`

**Interfaces:**
- Consumes: `RegulationTabRegistry::get()`, `::fields()`, hằng `SHAPE_LIBRARY`. Entity `::optionsForSelect()`. `auth()->id()` truyền vào từ controller (`$actorId`).
- Produces (public method mới trên `RegulationConfigService`):
  - `getTermConfig(int $companyId, string $tabKey): array` → `['fields'=>[['key','label','input','options'?], ...], 'rows'=>[ ['id','title','content', <discriminator>=>int|null], ... ]]`.
  - `createTerm(string $tabKey, int $companyId, array $input, int $actorId): array` → 1 row đã present.
  - `updateTerm(string $tabKey, int $termId, int $companyId, array $input, int $actorId): array` → row đã present (abort 403 nếu row.company_id ≠ companyId).
  - `deleteTerm(string $tabKey, int $termId, int $companyId): void` (abort 403 nếu khác công ty).

- [ ] **Step 1: Viết test cô lập công ty (failing)**

Thêm vào `RegulationTermTest.php`:

```php
    private function service(): \Modules\MasterData\Services\RegulationConfigService
    {
        return app(\Modules\MasterData\Services\RegulationConfigService::class);
    }

    /** @test */
    public function terms_are_isolated_per_company()
    {
        $svc = $this->service();

        // Công ty 100 tạo 1 điều khoản báo giá.
        $rowA = $svc->createTerm('dieukhoanbaogia', 100, ['title' => 'ĐK A', 'type' => 1, 'content' => '<p>Nội dung A</p>'], 34);
        $this->assertSame('ĐK A', $rowA['title']);
        $this->assertSame(1, $rowA['type']);

        // getTermConfig công ty 100 thấy dòng vừa tạo; công ty 200 KHÔNG thấy.
        $cfg100 = $svc->getTermConfig(100, 'dieukhoanbaogia');
        $this->assertContains('ĐK A', array_column($cfg100['rows'], 'title'));
        $this->assertSame('select', collect($cfg100['fields'])->firstWhere('key', 'type')['input']);
        $this->assertSame(['id' => 1, 'name' => 'Báo giá bán hàng'], collect($cfg100['fields'])->firstWhere('key', 'type')['options'][0]);

        $cfg200 = $svc->getTermConfig(200, 'dieukhoanbaogia');
        $this->assertNotContains('ĐK A', array_column($cfg200['rows'], 'title'));

        // Công ty 200 KHÔNG sửa/xoá được điều khoản của công ty 100 → abort 403.
        try {
            $svc->updateTerm('dieukhoanbaogia', $rowA['id'], 200, ['title' => 'hack', 'type' => 1, 'content' => ''], 34);
            $this->fail('Đáng lẽ abort 403');
        } catch (\Symfony\Component\HttpKernel\Exception\HttpException $e) {
            $this->assertSame(403, $e->getStatusCode());
        }

        // Công ty 100 sửa được.
        $upd = $svc->updateTerm('dieukhoanbaogia', $rowA['id'], 100, ['title' => 'ĐK A2', 'type' => 2, 'content' => '<p>B</p>'], 34);
        $this->assertSame('ĐK A2', $upd['title']);
        $this->assertSame(2, $upd['type']);

        // Xoá bởi công ty khác → 403; đúng công ty → OK.
        try {
            $svc->deleteTerm('dieukhoanbaogia', $rowA['id'], 200);
            $this->fail('Đáng lẽ abort 403');
        } catch (\Symfony\Component\HttpKernel\Exception\HttpException $e) {
            $this->assertSame(403, $e->getStatusCode());
        }
        $svc->deleteTerm('dieukhoanbaogia', $rowA['id'], 100);
        $this->assertNotContains('ĐK A2', array_column($svc->getTermConfig(100, 'dieukhoanbaogia')['rows'], 'title'));
    }
```

- [ ] **Step 2: Chạy test — fail**

Run: `cd HRM/hrm-api && php artisan test --filter=terms_are_isolated_per_company`
Expected: FAIL — `Call to undefined method ...::createTerm()`.

- [ ] **Step 3: Thêm khối method vào `RegulationConfigService`**

Thêm (cạnh khối grid `getGridConfig`/`createGridRow`), nhớ `use Modules\MasterData\Support\RegulationTabRegistry;` đã có sẵn ở đầu file:

```php
    /** Model + cột phân loại (discriminator) của 1 tab thư viện điều khoản; abort 404 nếu không phải library. */
    private function termMeta(string $tabKey): array
    {
        $def = RegulationTabRegistry::get($tabKey);
        abort_if(($def['shape'] ?? null) !== RegulationTabRegistry::SHAPE_LIBRARY, 404, 'Tab này không phải thư viện điều khoản');
        return [$def['model'], $def['discriminator']];
    }

    /** Present 1 dòng điều khoản → mảng phẳng cho FE. */
    private function presentTerm($row, string $discriminator): array
    {
        return [
            'id'          => (int) $row->id,
            'title'       => (string) $row->title,
            'content'     => (string) $row->content,
            $discriminator => $row->{$discriminator} !== null ? (int) $row->{$discriminator} : null,
        ];
    }

    /** Đặc tả cột + danh sách dòng của 1 công ty (điểm vào show() shape=library). */
    public function getTermConfig(int $companyId, string $tabKey): array
    {
        [$model, $discriminator] = $this->termMeta($tabKey);
        $discLabel = RegulationTabRegistry::fields($tabKey)[$discriminator]['label'];

        $fields = [
            ['key' => 'title',       'label' => 'Tiêu đề điều khoản', 'input' => 'text'],
            ['key' => $discriminator, 'label' => $discLabel,           'input' => 'select', 'options' => $model::optionsForSelect()],
            ['key' => 'content',     'label' => 'Nội dung',           'input' => 'rich'],
        ];

        $rows = $model::where('company_id', $companyId)
            ->orderBy('title', 'ASC')
            ->get()
            ->map(function ($r) use ($discriminator) {
                return $this->presentTerm($r, $discriminator);
            })
            ->all();

        return ['fields' => $fields, 'rows' => $rows];
    }

    public function createTerm(string $tabKey, int $companyId, array $input, int $actorId): array
    {
        [$model, $discriminator] = $this->termMeta($tabKey);
        $row = new $model();
        $row->title            = $input['title'];
        $row->content          = $input['content'] ?? '';
        $row->{$discriminator} = $input[$discriminator];
        $row->company_id       = $companyId;
        $row->created_by       = $actorId;
        $row->updated_by       = $actorId;
        $row->save();
        return $this->presentTerm($row->fresh(), $discriminator);
    }

    public function updateTerm(string $tabKey, int $termId, int $companyId, array $input, int $actorId): array
    {
        [$model, $discriminator] = $this->termMeta($tabKey);
        $row = $model::findOrFail($termId);
        abort_if((int) $row->company_id !== $companyId, 403, 'Điều khoản không thuộc công ty này');
        $row->title            = $input['title'];
        $row->content          = $input['content'] ?? '';
        $row->{$discriminator} = $input[$discriminator];
        $row->updated_by       = $actorId;
        $row->save();
        return $this->presentTerm($row->fresh(), $discriminator);
    }

    public function deleteTerm(string $tabKey, int $termId, int $companyId): void
    {
        [$model] = $this->termMeta($tabKey);
        $row = $model::findOrFail($termId);
        abort_if((int) $row->company_id !== $companyId, 403, 'Điều khoản không thuộc công ty này');
        $row->delete();
    }
```

- [ ] **Step 4: Chạy test — pass**

Run: `cd HRM/hrm-api && php artisan test --filter=terms_are_isolated_per_company`
Expected: PASS.

*(Ghi chú: nếu `BaseModel` có hook creating/updating tự set `created_by = Auth::id()` và ghi đè khi Auth null → test dùng `DatabaseTransactions` không acting-as, `Auth::id()` = null. Việc gán tường minh `$row->created_by = $actorId` trước `save()` là để dữ liệu đúng; nếu hook nuốt giá trị, không ảnh hưởng test này vì test không assert created_by. Không cần acting-as.)*

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Services/RegulationConfigService.php Modules/MasterData/Tests/Feature/RegulationTermTest.php
git commit -m "feat(regulation-config): per-company term CRUD service (ownership 403)"
```

---

## Task 5: FormRequest `RegulationTermRowRequest`

**Files:**
- Create: `HRM/hrm-api/Modules/MasterData/Http/Requests/RegulationTermRowRequest.php`

**Interfaces:**
- Consumes: `RegulationTabRegistry::get($tabKey)['discriminator']`; route param `{tabKey}`. Enum keys từ `QuotationTerm::TYPES` / `PaymentMethodTerm::PAYMENT_METHODS`.
- Produces: `authorize(): bool` = `true` (quyền đã gate ở route middleware `checkPermission:Cài đặt cấu hình`); `rules()` = `['title'=>'required|string|max:255', <discriminator>=>'required|integer|in:<danh sách enum>', 'content'=>'nullable|string']`; `messages()` tiếng Việt.

- [ ] **Step 1: Viết FormRequest**

```php
<?php

namespace Modules\MasterData\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Modules\MasterData\Support\RegulationTabRegistry;

/**
 * Validate 1 dòng điều khoản thư viện. Cột phân loại (type / payment_method_id) suy từ tab trên route,
 * danh sách hợp lệ lấy từ model (mirror ERP). Quyền đã gate ở middleware route.
 */
class RegulationTermRowRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        $def = RegulationTabRegistry::get($this->route('tabKey'));
        $discriminator = $def['discriminator'];
        $model = $def['model'];
        $validIds = implode(',', array_column($model::optionsForSelect(), 'id'));

        return [
            'title'        => 'required|string|max:255',
            $discriminator => 'required|integer|in:' . $validIds,
            'content'      => 'nullable|string',
        ];
    }

    public function messages()
    {
        return [
            'title.required' => 'Vui lòng nhập tiêu đề điều khoản.',
            'title.max'      => 'Tiêu đề điều khoản tối đa 255 ký tự.',
            'type.required'              => 'Vui lòng chọn loại báo giá.',
            'type.in'                    => 'Loại báo giá không hợp lệ.',
            'payment_method_id.required' => 'Vui lòng chọn phương thức thanh toán.',
            'payment_method_id.in'       => 'Phương thức thanh toán không hợp lệ.',
        ];
    }
}
```

- [ ] **Step 2: Verify cú pháp**

Run: `cd HRM/hrm-api && php -l Modules/MasterData/Http/Requests/RegulationTermRowRequest.php`
Expected: `No syntax errors detected`.

- [ ] **Step 3: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Http/Requests/RegulationTermRowRequest.php
git commit -m "feat(regulation-config): add RegulationTermRowRequest validation"
```

---

## Task 6: Controller — nhánh `show()` library + 3 method CRUD

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`

**Interfaces:**
- Consumes: `$this->service` (`getTermConfig`/`createTerm`/`updateTerm`/`deleteTerm` — Task 4), `RegulationTermRowRequest` (Task 5), `RegulationTabRegistry::SHAPE_LIBRARY`, có sẵn `guard()`, `currentCompanyId()`, `responseSuccessJson()`, `auth()->id()`.
- Produces (public method mới):
  - `storeTermRow(RegulationTermRowRequest $request, $tabKey)` → 200 `['row'=>, 'config'=>]`.
  - `updateTermRow(RegulationTermRowRequest $request, $tabKey, $termId)` → 200 `['row'=>, 'config'=>]`.
  - `destroyTermRow(Request $request, $tabKey, $termId)` → 200 `['config'=>]`.
  - `show()` trả `getTermConfig()` khi `shape===SHAPE_LIBRARY`.
  - `assertVersionTab()` (nếu tồn tại) chặn thêm `SHAPE_LIBRARY` (library không đi qua pipeline version).

- [ ] **Step 1: Thêm nhánh library vào `show()`**

Trong `show()`, cạnh nhánh `if (($def['shape'] ?? null) === RegulationTabRegistry::SHAPE_GRID) { ... getGridConfig ... }`, thêm TRƯỚC nhánh grid:

```php
        if (($def['shape'] ?? null) === RegulationTabRegistry::SHAPE_LIBRARY) {
            return $this->responseSuccessJson('OK', 200, $this->service->getTermConfig($companyId, $tabKey));
        }
```

*(Ghi chú: `$companyId` trong `show()` đã được resolve theo cơ chế scope company hiện có. Library luôn scope company nên không cần department.)*

- [ ] **Step 2: Chặn library khỏi pipeline version**

Nếu có `assertVersionTab(string $tabKey)` (dùng ở `store()`/`cancel()` để chặn `SHAPE_GRID`), thêm điều kiện chặn cả library:

```php
        abort_if(($def['shape'] ?? null) === RegulationTabRegistry::SHAPE_LIBRARY, 404, 'Tab thư viện điều khoản không dùng lưu phiên bản');
```

đặt cạnh dòng abort cho `SHAPE_GRID` trong helper đó.

- [ ] **Step 3: Thêm helper + 3 method CRUD**

```php
    /** Chốt tab phải là thư viện điều khoản (shape=library). */
    private function assertLibraryTab(string $tabKey): void
    {
        $def = RegulationTabRegistry::get($tabKey);
        abort_if(($def['shape'] ?? null) !== RegulationTabRegistry::SHAPE_LIBRARY, 404, 'Tab này không phải thư viện điều khoản');
    }

    public function storeTermRow(RegulationTermRowRequest $request, $tabKey)
    {
        $this->guard();
        $this->assertLibraryTab($tabKey);
        $companyId = $this->currentCompanyId();
        $row = $this->service->createTerm($tabKey, $companyId, $request->validated(), auth()->id());
        return $this->responseSuccessJson('Đã thêm điều khoản', 200, [
            'row'    => $row,
            'config' => $this->service->getTermConfig($companyId, $tabKey),
        ]);
    }

    public function updateTermRow(RegulationTermRowRequest $request, $tabKey, $termId)
    {
        $this->guard();
        $this->assertLibraryTab($tabKey);
        $companyId = $this->currentCompanyId();
        $row = $this->service->updateTerm($tabKey, (int) $termId, $companyId, $request->validated(), auth()->id());
        return $this->responseSuccessJson('Đã cập nhật điều khoản', 200, [
            'row'    => $row,
            'config' => $this->service->getTermConfig($companyId, $tabKey),
        ]);
    }

    public function destroyTermRow(Request $request, $tabKey, $termId)
    {
        $this->guard();
        $this->assertLibraryTab($tabKey);
        $companyId = $this->currentCompanyId();
        $this->service->deleteTerm($tabKey, (int) $termId, $companyId);
        return $this->responseSuccessJson('Đã xoá điều khoản', 200, [
            'config' => $this->service->getTermConfig($companyId, $tabKey),
        ]);
    }
```

Đảm bảo `use Modules\MasterData\Http\Requests\RegulationTermRowRequest;` ở đầu file, và `use Illuminate\Http\Request;` đã có sẵn.

- [ ] **Step 4: Verify cú pháp**

Run: `cd HRM/hrm-api && php -l Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`
Expected: `No syntax errors detected`.

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php
git commit -m "feat(regulation-config): controller library show branch + term CRUD endpoints"
```

---

## Task 7: Routes — `terms[/{id}]`

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Routes/api.php`

**Interfaces:**
- Consumes: `RegulationConfigController@storeTermRow/updateTermRow/destroyTermRow` (Task 6). Group có sẵn: prefix `/v1/master-data`, middleware `auth:api` → inner `checkPermission:Cài đặt cấu hình`.
- Produces: 3 route trong group `checkPermission` (regex `[a-z]+` cho tabKey, `[0-9]+` cho termId):
  - `POST regulation-config/{tabKey}/terms`
  - `PUT regulation-config/{tabKey}/terms/{termId}`
  - `DELETE regulation-config/{tabKey}/terms/{termId}`

- [ ] **Step 1: Thêm route (cạnh nhóm route grid, TRONG group `checkPermission`)**

```php
        // Thư viện điều khoản per-company (dieukhoanbaogia / dieukhoanthanhtoan): CRUD từng dòng theo công ty.
        Route::post('regulation-config/{tabKey}/terms', 'V1\RegulationConfigController@storeTermRow')
            ->where('tabKey', '[a-z]+');
        Route::put('regulation-config/{tabKey}/terms/{termId}', 'V1\RegulationConfigController@updateTermRow')
            ->where(['tabKey' => '[a-z]+', 'termId' => '[0-9]+']);
        Route::delete('regulation-config/{tabKey}/terms/{termId}', 'V1\RegulationConfigController@destroyTermRow')
            ->where(['tabKey' => '[a-z]+', 'termId' => '[0-9]+']);
```

- [ ] **Step 2: Verify route đăng ký đúng**

Run: `cd HRM/hrm-api && php artisan route:list --path=master-data/regulation-config | grep terms`
Expected: 3 dòng POST/PUT/DELETE `.../terms` với middleware `checkPermission:Cài đặt cấu hình`.

- [ ] **Step 3: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Routes/api.php
git commit -m "feat(regulation-config): add term CRUD routes"
```

---

## Task 8: HTTP feature test — quyền + luồng CRUD qua route

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Tests/Feature/RegulationTermTest.php`

**Interfaces:**
- Consumes: route Task 7, JWT thật (mirror `RegulationHistoryTest::seedHttpUser`), `RegulationConfigController::PERM_EDIT`.
- Produces: 2 test HTTP — không quyền → 403; có quyền → tạo/xoá 1 dòng OK và cô lập theo `current_company_role`.

- [ ] **Step 1: Thêm helper seed user + 2 test (failing nếu route/quyền sai)**

Thêm vào `RegulationTermTest.php` (mirror `RegulationHistoryTest`):

```php
    private function seedHttpUser(int $companyId, bool $withPerm)
    {
        $infoId = \Illuminate\Support\Facades\DB::table('employee_infos')->insertGetId([
            'company_role'   => $companyId,
            'code'           => 'RT' . uniqid(),
            'fullname'       => 'Term HTTP Tester',
            'telephone'      => '0900000000',
            'department_id'  => 0,
            'birthday'       => '2000-01-01',
            'id_card'        => '000000000000',
            'grant_date'     => '2020-01-01',
            'grant_location' => 'HN',
            'gender'         => 1,
            'marital_status' => 1,
            'enter_date'     => '2020-01-01',
            'email'          => 'rt-info-' . uniqid() . '@example.com',
            'created_at'     => now(),
            'updated_at'     => now(),
        ]);
        $employeeId = \Illuminate\Support\Facades\DB::table('employees')->insertGetId([
            'email'            => 'rt-actor-' . uniqid() . '@example.com',
            'password'         => bcrypt('secret'),
            'token_version'    => 1,
            'employee_info_id' => $infoId,
            'status'           => 1,
            'login_count'      => 0,
            'created_at'       => now(),
            'updated_at'       => now(),
        ]);
        if ($withPerm) {
            $permission = \Spatie\Permission\Models\Permission::where('name', \Modules\MasterData\Http\Controllers\V1\RegulationConfigController::PERM_EDIT)
                ->where('guard_name', 'api')->firstOrFail();
            \Illuminate\Support\Facades\DB::table('employee_has_permissions')->insert([
                'permission_id' => $permission->id,
                'model_type'    => \Modules\Timesheet\Entities\Employee::class,
                'employee_id'   => $employeeId,
            ]);
        }
        $user = \App\Models\TpEmployee::find($employeeId);
        $this->withToken(\Tymon\JWTAuth\Facades\JWTAuth::fromUser($user));
        return $employeeId;
    }

    /** @test */
    public function http_store_term_without_permission_returns_403()
    {
        $this->seedHttpUser(300, false);
        $this->postJson('/api/v1/master-data/regulation-config/dieukhoanbaogia/terms', [
            'title' => 'x', 'type' => 1, 'content' => '<p>x</p>',
        ])->assertStatus(403);
    }

    /** @test */
    public function http_store_and_delete_term_scoped_to_current_company()
    {
        $this->seedHttpUser(301, true);

        $create = $this->postJson('/api/v1/master-data/regulation-config/dieukhoanbaogia/terms', [
            'title' => 'ĐK HTTP', 'type' => 3, 'content' => '<p>Nội dung</p>',
        ])->assertStatus(200)->json();
        $id = $create['data']['row']['id'];
        $this->assertSame(3, $create['data']['row']['type']);
        $this->assertContains('ĐK HTTP', array_column($create['data']['config']['rows'], 'title'));

        // show trả đúng dòng của công ty 301.
        $this->getJson('/api/v1/master-data/regulation-config/dieukhoanbaogia')
            ->assertStatus(200)
            ->assertJsonFragment(['title' => 'ĐK HTTP']);

        // xoá OK.
        $this->deleteJson('/api/v1/master-data/regulation-config/dieukhoanbaogia/terms/' . $id)
            ->assertStatus(200);
    }
```

*(Ghi chú: đường dẫn key trong `responseSuccessJson` — `data.row`, `data.config` — theo chuẩn response của controller. Nếu wrapper khác (`result`/không `data`), người thực thi chỉnh `->json()` path cho khớp helper thật; điểm cốt lõi là status 200/403 và title xuất hiện.)*

- [ ] **Step 2: Chạy toàn bộ test của file**

Run: `cd HRM/hrm-api && php artisan test Modules/MasterData/Tests/Feature/RegulationTermTest.php`
Expected: tất cả PASS.

- [ ] **Step 3: Commit**

```bash
cd HRM/hrm-api && git add Modules/MasterData/Tests/Feature/RegulationTermTest.php
git commit -m "test(regulation-config): HTTP permission + CRUD flow for term tabs"
```

---

## Task 9: FE `data.js` — 2 group `type:'library'`

**Files:**
- Modify: `HRM/hrm-client/components/regulation-config/data.js`

**Interfaces:**
- Consumes: cấu trúc `DATA.company.groups` có sẵn (mỗi group `{id, name, sub, icon, type, ...}`).
- Produces: 2 group `dieukhoanbaogia` / `dieukhoanthanhtoan` với `type:'library'`, `discriminator`, `discriminatorLabel`, `rows:[]`, **KHÔNG có key `subsystem`** (mặc định `master-data` → xuất hiện ở `/sale/regulation-config`).

- [ ] **Step 1: Thêm 2 group vào cuối `DATA.company.groups`**

```js
    {
      id: 'dieukhoanbaogia',
      name: 'Điều khoản báo giá',
      sub: 'Thư viện điều khoản theo loại báo giá (theo công ty)',
      icon: 'doc',
      type: 'library',
      discriminator: 'type',
      discriminatorLabel: 'Loại báo giá',
      rows: [],
    },
    {
      id: 'dieukhoanthanhtoan',
      name: 'Điều khoản thanh toán',
      sub: 'Thư viện điều khoản theo phương thức thanh toán (theo công ty)',
      icon: 'doc',
      type: 'library',
      discriminator: 'payment_method_id',
      discriminatorLabel: 'Phương thức thanh toán',
      rows: [],
    },
```

*(Giữ nguyên style xuống dòng của file — nếu file là CRLF, không convert sang LF.)*

- [ ] **Step 2: Verify không lỗi cú pháp JS**

Run: `cd HRM/hrm-client && node -e "require('./components/regulation-config/data.js'); console.log('ok')"`
Expected: `ok` (nếu file dùng ESM `export`, thay bằng kiểm tra qua eslint/`node --input-type=module`; điểm cốt lõi: file parse được, 2 group mới có mặt).

- [ ] **Step 3: Commit**

```bash
cd HRM/hrm-client && git add components/regulation-config/data.js
git commit -m "feat(regulation-config): add 2 library term groups (master-data subsystem)"
```

---

## Task 10: FE screen — render library + modal CKEditor + methods

**Files:**
- Modify: `HRM/hrm-client/components/regulation-config/RegulationConfigScreen.vue`

**Interfaces:**
- Consumes: endpoint `master-data/regulation-config/{tabKey}` (GET → `{fields, rows}`), `.../terms[/{id}]` (POST/PUT/DELETE); `CompactReviewEditor` (đã import, list components dòng ~1157); store actions `apiGetMethod`/`apiPostMethod`/`apiPutMethod`/`apiDelete`; computed có sẵn `curGroup`, `companyId()`, `canEditRegulation()`, `subsystem`, helper `markFormPristine()`; V2 components `V2BaseModal`, `V2BaseInput`, `V2BaseSelectInModal`.
- Produces: const `LIBRARY_TABS`; computed `curTabIsLibrary`; render block `v-else-if="curGroup.type === 'library'"` + modal `ref="termModal"`; data props `libLoading, libFieldOptions, termForm, termEditing, termError, termSaving`; methods `fetchLibraryTab, applyLibraryConfig, termOptLabel, openTerm, closeTerm, saveTerm, deleteTerm`.

- [ ] **Step 1: Thêm const + data props**

Cạnh `GRID_DEPT_TABS`:

```js
const LIBRARY_TABS = ['dieukhoanbaogia', 'dieukhoanthanhtoan']
```

Trong `data()`:

```js
      libLoading: false,
      libFieldOptions: {}, // { type: [{id,name}], payment_method_id: [...] }
      termForm: { id: null, title: '', content: '', type: null, payment_method_id: null },
      termEditing: false,
      termError: {},
      termSaving: false,
```

- [ ] **Step 2: computed `curTabIsLibrary` + sửa savebar v-if**

Thêm computed:

```js
    curTabIsLibrary() {
      return !!this.curGroup && this.curGroup.type === 'library'
    },
```

Sửa dòng savebar (dòng ~64) từ `v-if="!curTabIsGrid"` → :

```html
        v-if="!curTabIsGrid && !curTabIsLibrary"
```

- [ ] **Step 3: Render block library (đặt sau block `v-else-if="curGroup.type === 'ladder'"`)**

```html
          <div v-else-if="curGroup.type === 'library'" class="library-tab">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div class="group-sub" style="color:#6b7280">{{ curGroup.sub }}</div>
              <b-button v-if="canEditRegulation" variant="primary" size="sm" @click="openTerm(null)">
                <i class="ri-add-line"></i> Thêm mới
              </b-button>
            </div>
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th style="width:32%">Tiêu đề điều khoản</th>
                  <th style="width:24%">{{ curGroup.discriminatorLabel }}</th>
                  <th>Nội dung</th>
                  <th style="width:110px" class="text-center">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!curGroup.rows.length">
                  <td colspan="4" class="text-center" style="color:#6b7280">Chưa có điều khoản nào</td>
                </tr>
                <tr v-for="row in curGroup.rows" :key="row.id">
                  <td>{{ row.title }}</td>
                  <td>{{ termOptLabel(row[curGroup.discriminator]) }}</td>
                  <td><div class="rich-cell" v-html="row.content"></div></td>
                  <td class="text-center">
                    <b-button v-if="canEditRegulation" variant="link" size="sm" @click="openTerm(row)" title="Sửa">
                      <i class="ri-edit-line"></i>
                    </b-button>
                    <b-button v-if="canEditRegulation" variant="link" size="sm" class="text-danger" @click="deleteTerm(row)" title="Xoá">
                      <i class="ri-delete-bin-line"></i>
                    </b-button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
```

- [ ] **Step 4: Modal thêm/sửa (đặt cạnh modal grid `ref="regModal"`)**

```html
    <V2BaseModal ref="termModal" :title="termEditing ? 'Sửa điều khoản' : 'Thêm điều khoản'" size="lg" @ok="saveTerm" ok-title="Lưu" cancel-title="Huỷ">
      <div class="form-group">
        <label>Tiêu đề điều khoản <span class="text-danger">*</span></label>
        <V2BaseInput v-model="termForm.title" :disabled="!canEditRegulation" />
        <small v-if="termError.title" class="text-danger">{{ termError.title }}</small>
      </div>
      <div class="form-group">
        <label>{{ curGroup && curGroup.discriminatorLabel }} <span class="text-danger">*</span></label>
        <V2BaseSelectInModal
          v-model="termForm[curGroup.discriminator]"
          :options="libFieldOptions[curGroup.discriminator] || []"
          :reduce="o => o.id"
          label="name"
          :disabled="!canEditRegulation"
        />
        <small v-if="termError[curGroup.discriminator]" class="text-danger">{{ termError[curGroup.discriminator] }}</small>
      </div>
      <div class="form-group">
        <label>Nội dung</label>
        <CompactReviewEditor v-model="termForm.content" label="" remove-buttons="" :height="220" :disabled="!canEditRegulation" class="rich-editor" />
      </div>
    </V2BaseModal>
```

*(Ghi chú: props `V2BaseSelectInModal` — `:reduce`/`label` — theo cách dùng đang có trong repo. Nếu component nhận `value-field`/`text-field` thay vì `:reduce`/`label`, chỉnh cho khớp; mục tiêu: bind về id enum, hiển thị name.)*

- [ ] **Step 5: Watcher branch — nạp library khi scope company**

Trong `curGroup` watcher (immediate), thêm nhánh (cạnh các nhánh fetchTab/fetchGridTab):

```js
        if (scope === 'company' && LIBRARY_TABS.includes(g.id) && !this.libLoading) {
          this.fetchLibraryTab(g.id)
          return
        }
```

*(Đặt trước/ sau nhánh company API_TABS tuỳ thứ tự — điều kiện `LIBRARY_TABS.includes(g.id)` là loại trừ, không đụng nhánh khác.)*

- [ ] **Step 6: Methods (cạnh fetchGridTab/openReg/saveReg/deleteReg)**

```js
    async fetchLibraryTab(tabKey) {
      this.libLoading = true
      try {
        const res = await this.$store.dispatch('apiGetMethod', {
          url: `master-data/regulation-config/${tabKey}`,
        })
        this.applyLibraryConfig(tabKey, (res && res.data) || res)
      } finally {
        this.libLoading = false
        this.$nextTick(() => this.markFormPristine())
      }
    },
    applyLibraryConfig(tabKey, config) {
      if (!config) return
      const group = this.curGroups.find(g => g.id === tabKey)
      if (!group) return
      const discField = (config.fields || []).find(f => f.key === group.discriminator)
      this.$set(this.libFieldOptions, group.discriminator, (discField && discField.options) || [])
      group.rows = config.rows || []
    },
    termOptLabel(id) {
      const opts = this.libFieldOptions[this.curGroup.discriminator] || []
      const found = opts.find(o => o.id === id)
      return found ? found.name : ''
    },
    openTerm(row) {
      this.termError = {}
      this.termEditing = !!row
      const disc = this.curGroup.discriminator
      this.termForm = {
        id: row ? row.id : null,
        title: row ? row.title : '',
        content: row ? row.content : '',
        [disc]: row ? row[disc] : null,
      }
      this.$refs.termModal.show()
    },
    async saveTerm(bvEvent) {
      if (bvEvent && bvEvent.preventDefault) bvEvent.preventDefault()
      this.termError = {}
      this.termSaving = true
      const disc = this.curGroup.discriminator
      const tabKey = this.curGroup.id
      const payload = { title: this.termForm.title, content: this.termForm.content, [disc]: this.termForm[disc] }
      try {
        let res
        if (this.termEditing) {
          res = await this.$store.dispatch('apiPutMethod', {
            url: `master-data/regulation-config/${tabKey}/terms/${this.termForm.id}`,
            payload,
          })
        } else {
          res = await this.$store.dispatch('apiPostMethod', {
            url: `master-data/regulation-config/${tabKey}/terms`,
            payload,
          })
        }
        this.applyLibraryConfig(tabKey, ((res && res.data) || res).config)
        this.$refs.termModal.hide()
      } catch (e) {
        if (e && e.response && e.response.status === 422) {
          const errs = (e.response.data && e.response.data.errors) || {}
          const flat = {}
          Object.keys(errs).forEach(k => { flat[k] = Array.isArray(errs[k]) ? errs[k][0] : errs[k] })
          this.termError = flat
        } else {
          throw e
        }
      } finally {
        this.termSaving = false
      }
    },
    async deleteTerm(row) {
      const ok = await this.$confirm('Bạn chắc chắn muốn xoá điều khoản này?')
      if (!ok) return
      const tabKey = this.curGroup.id
      const res = await this.$store.dispatch('apiDelete', `master-data/regulation-config/${tabKey}/terms/${row.id}`)
      this.applyLibraryConfig(tabKey, ((res && res.data) || res).config)
    },
```

*(Ghi chú: dạng bóc `res.data` / `.config` bám theo response `responseSuccessJson('...',200,['row'=>,'config'=>])`. Nếu store đã bóc sẵn `data`, dùng thẳng `res.config`. `$confirm` trả boolean theo convention repo — nếu là promise resolve/reject, đổi sang try/catch. Người thực thi khớp với helper thật khi wiring.)*

- [ ] **Step 7: SCSS (nếu chưa có) cho `.rich-editor` label ẩn + `.rich-cell`**

Trong khối `<style>` (giữ pattern có sẵn):

```css
.rich-editor :deep(label) { display: none; }
.library-tab .rich-cell { max-height: 120px; overflow: auto; }
```

- [ ] **Step 8: Chạy dev, verify màn hình**

Run (thủ công): bật API `:8000` + client `:3000`, mở `/sale/regulation-config`, chọn công ty, mở tab "Điều khoản báo giá" và "Điều khoản thanh toán".
Expected: KHÔNG có nút "Lưu cấu hình" đầu trang cho 2 tab; bảng danh sách render; "Thêm mới" mở modal có select enum + CKEditor; lưu/sửa/xoá cập nhật bảng; công ty Tân Phát (id 1) thấy 8/11 dòng cũ.

- [ ] **Step 9: Commit**

```bash
cd HRM/hrm-client && git add components/regulation-config/RegulationConfigScreen.vue
git commit -m "feat(regulation-config): library term tabs UI + CKEditor modal (per-company)"
```

---

## Task 11: ERP — chiều đọc `getForSelect` lọc theo công ty

**Files:**
- Modify: `ERP/TanPhatDev/app/Model/Common/QuotationTerm.php`
- Modify: `ERP/TanPhatDev/app/Model/Common/PaymentMethodTerm.php`

**Interfaces:**
- Consumes: `auth()->user()->info->company_id` (null-safe form vì `getForSelect` là static gọi từ Blade `@json` không context).
- Produces: `getForSelect` chỉ trả điều khoản của công ty đăng nhập hiện tại.

- [ ] **Step 1: Sửa `QuotationTerm::getForSelect`**

Trong `ERP/TanPhatDev/app/Model/Common/QuotationTerm.php`, thêm lọc công ty:

```php
    public static function getForSelect($type = null)
    {
        $companyId = optional(optional(auth()->user())->info)->company_id;

        $q = self::query()->select(['id', 'title', 'content']);
        if ($companyId) {
            $q->where('company_id', $companyId);
        }
        if ($type) {
            $q->where('type', $type);
        }
        return $q->orderBy('title', 'ASC')->get();
    }
```

- [ ] **Step 2: Sửa `PaymentMethodTerm::getForSelect`**

Trong `ERP/TanPhatDev/app/Model/Common/PaymentMethodTerm.php`, CHỈ thêm lọc công ty — **KHÔNG** đụng dòng `where('type', ...)` (bug cũ trên cột không tồn tại, ngoài phạm vi):

```php
    public static function getForSelect($type = null)
    {
        $companyId = optional(optional(auth()->user())->info)->company_id;

        $q = self::query()->select(['id', 'title', 'content', 'payment_method_id']);
        if ($companyId) {
            $q->where('company_id', $companyId);
        }
        if ($type) {
            $q->where('type', $type); // GIỮ NGUYÊN: bug cũ, không sửa trong G1
        }
        return $q->orderBy('title', 'ASC')->get();
    }
```

- [ ] **Step 3: Verify cú pháp**

Run: `cd ERP/TanPhatDev && php -l app/Model/Common/QuotationTerm.php && php -l app/Model/Common/PaymentMethodTerm.php`
Expected: `No syntax errors detected` cả 2.

- [ ] **Step 4: Regression tinker — Tân Phát vẫn thấy 8/11 dòng**

Run: `cd ERP/TanPhatDev && grep DB_ .env` (xác nhận DB target trước), rồi kiểm truy vấn lọc:
`php artisan tinker --execute="echo App\Model\Common\QuotationTerm::where('company_id',1)->count().'|'.App\Model\Common\PaymentMethodTerm::where('company_id',1)->count();"`
Expected: `8|11`.

- [ ] **Step 5: Commit**

```bash
cd ERP/TanPhatDev && git add app/Model/Common/QuotationTerm.php app/Model/Common/PaymentMethodTerm.php
git commit -m "feat(terms): filter getForSelect by current company"
```

---

## Task 12: ERP — gỡ 2 màn admin điều khoản

**Files:**
- Modify: `ERP/TanPhatDev/routes/web.php` (dòng ~5551-5571)
- Modify: `ERP/TanPhatDev/resources/views/layouts/topmenubar.blade.php` (dòng ~2002-2003)
- Delete: `ERP/TanPhatDev/app/Http/Controllers/Common/QuotationTermsController.php`
- Delete: `ERP/TanPhatDev/app/Http/Controllers/Common/PaymentMethodTermsController.php`
- Delete: `ERP/TanPhatDev/resources/views/common/quotation_terms/` (dir)
- Delete: `ERP/TanPhatDev/resources/views/common/payment_method_terms/` (dir)

**Interfaces:**
- Consumes: 2 route group `quotation_terms` / `payment_method_terms`, 2 menu link `route('quotationTerms.index')` / `route('paymentMethodTerms.index')`.
- Produces: không còn route/menu/controller/view của 2 màn admin. GIỮ 2 model (`app/Model/Common/*Term.php`), GIỮ perm 169/174 trong seeder.

- [ ] **Step 1: Xác nhận không còn tham chiếu khác tới 2 route name**

Run: `cd ERP/TanPhatDev && grep -rn "quotationTerms\.\|paymentMethodTerms\." --include=*.php --include=*.blade.php --include=*.js resources routes app public | grep -v vendor`
Expected: chỉ thấy đúng 2 dòng menu (topmenubar) + định nghĩa route group. Nếu có link khác → ghi lại, gỡ luôn ở step 3 (tránh 404).

- [ ] **Step 2: Đọc 2 route group để chép chính xác đoạn cần xoá**

Run: `cd ERP/TanPhatDev && sed -n '5545,5575p' routes/web.php`
Expected: thấy 2 `Route::group([...'checkPermission:Quản lý điều khoản báo giá'...])` và `...phương thức thanh toán...`. Xoá trọn 2 group này (mọi route bên trong).

- [ ] **Step 3: Gỡ route + menu**

- Xoá 2 route group trong `routes/web.php` (đoạn ~5551-5571 xác nhận ở step 2).
- Xoá 2 `<h3 class="ruby-list-heading">` link trong `topmenubar.blade.php` (dòng ~2002-2003) + bất kỳ link phát sinh từ step 1.

- [ ] **Step 4: Xoá 2 controller + 2 view dir**

```bash
cd ERP/TanPhatDev
rm app/Http/Controllers/Common/QuotationTermsController.php
rm app/Http/Controllers/Common/PaymentMethodTermsController.php
rm -rf resources/views/common/quotation_terms
rm -rf resources/views/common/payment_method_terms
```

- [ ] **Step 5: Verify route:list không còn 2 màn, route khác không vỡ**

Run: `cd ERP/TanPhatDev && php artisan route:list 2>&1 | grep -i "quotationTerms\|paymentMethodTerms"`
Expected: rỗng (không còn route). Và lệnh `php artisan route:list` chạy KHÔNG lỗi (không còn controller mồ côi được tham chiếu).

- [ ] **Step 6: Verify model + perm còn nguyên**

Run: `cd ERP/TanPhatDev && ls app/Model/Common/QuotationTerm.php app/Model/Common/PaymentMethodTerm.php && grep -n "Quản lý điều khoản" database/seeds/PermissionsTableSeeder.php`
Expected: 2 model còn; 2 dòng perm (id 169/174) còn trong seeder.

- [ ] **Step 7: Commit**

```bash
cd ERP/TanPhatDev && git add -A routes/web.php resources/views/layouts/topmenubar.blade.php app/Http/Controllers/Common resources/views/common
git commit -m "chore(terms): remove ERP admin term screens (managed via HRM now)"
```

---

## Task 13: Playwright e2e — thêm/sửa/xoá điều khoản

**Files:**
- Create/Modify: `HRM/e2e/pages/RegulationConfigPage.ts`
- Create: `HRM/e2e/tests/regulation-config/dieukhoan.spec.ts`

**Interfaces:**
- Consumes: FE Task 10 render + modal; storageState auth có sẵn (`HRM/e2e`); helper `pickSelect2` (nếu select là Select2) hoặc thao tác `V2BaseSelectInModal` trực tiếp.
- Produces: 1 test: vào `/sale/regulation-config`, mở tab điều khoản báo giá, thêm 1 dòng (title + chọn loại + gõ nội dung CKEditor), thấy dòng trong bảng, sửa title, xoá.

- [ ] **Step 1: Page object (thao tác tab library)**

`HRM/e2e/pages/RegulationConfigPage.ts` (tạo mới hoặc thêm method):

```ts
import { Page, expect } from '@playwright/test';

export class RegulationConfigPage {
  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto('/sale/regulation-config', { waitUntil: 'domcontentloaded' });
    await this.page.getByText('Điều khoản báo giá').first().waitFor({ timeout: 15000 });
  }

  async openBaogiaTab() {
    await this.page.getByText('Điều khoản báo giá').first().click();
    await this.page.getByRole('button', { name: 'Thêm mới' }).waitFor({ timeout: 10000 });
  }

  async addTerm(title: string, contentText: string) {
    await this.page.getByRole('button', { name: 'Thêm mới' }).click();
    await this.page.locator('.modal input[type="text"]').first().fill(title);
    // chọn loại báo giá (option đầu) — Select2 hoặc v-select; ưu tiên click mở rồi chọn item
    await this.page.locator('.modal .select2-selection__rendered, .modal .vs__dropdown-toggle').first().click();
    await this.page.locator('li.select2-results__option, .vs__dropdown-option').first().click();
    // CKEditor iframe
    const frame = this.page.frameLocator('.modal .cke_wysiwyg_frame').first();
    await frame.locator('body').click();
    await frame.locator('body').type(contentText);
    await this.page.locator('.modal').getByRole('button', { name: 'Lưu' }).click();
    await expect(this.page.getByRole('row', { name: new RegExp(title) })).toBeVisible({ timeout: 10000 });
  }

  async deleteTerm(title: string) {
    const row = this.page.getByRole('row', { name: new RegExp(title) });
    await row.getByTitle('Xoá').click();
    await this.page.locator('.modal-footer').getByRole('button', { name: /Đồng ý|Xác nhận|OK/ }).click();
    await expect(this.page.getByRole('row', { name: new RegExp(title) })).toHaveCount(0, { timeout: 10000 });
  }
}
```

*(Ghi chú: selector CKEditor/Select2 dò lại bằng `npm run codegen` trên app thật nếu không khớp — theo skill playwright-setup, KHÔNG sửa `.vue` để thêm `data-testid` khi chưa hỏi.)*

- [ ] **Step 2: Spec**

`HRM/e2e/tests/regulation-config/dieukhoan.spec.ts`:

```ts
import { test, expect } from '@playwright/test';
import { RegulationConfigPage } from '../../pages/RegulationConfigPage';

test.describe('Khai Quy chế — Thư viện điều khoản báo giá (per-company)', () => {
  test('thêm rồi xoá một điều khoản báo giá', async ({ page }) => {
    const p = new RegulationConfigPage(page);
    const title = 'ĐK E2E ' + Date.now();
    await p.goto();
    await p.openBaogiaTab();
    await p.addTerm(title, 'Nội dung điều khoản e2e');
    await p.deleteTerm(title);
  });
});
```

- [ ] **Step 3: Liệt kê test (không cần app)**

Run: `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test --list`
Expected: liệt kê `dieukhoan.spec.ts` không lỗi TS/config.

- [ ] **Step 4: Chạy e2e (cần FE :3000 + API :8000 đang chạy)**

Run: `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/regulation-config/dieukhoan.spec.ts`
Expected: PASS. Nếu selector lệch → `npm run codegen`, chỉnh page object, chạy lại.

- [ ] **Step 5: Commit**

```bash
cd HRM/e2e && git add pages/RegulationConfigPage.ts tests/regulation-config/dieukhoan.spec.ts
git commit -m "test(e2e): add/edit/delete quotation term in regulation-config"
```

---

## Self-Review

**1. Spec coverage** (design.md §GIAI ĐOẠN 1):
- §1.1 Schema (company_id nullable + index + backfill 1 + down drop cột) → Task 1. ✓
- §1.2 Model + hằng TYPES/PAYMENT_METHODS → Task 2 ✓; Service CRUD ownership 403 → Task 4 ✓; Controller show library + CRUD + gate → Task 6 ✓; Registry SHAPE_LIBRARY + 2 tab + filter bỏ qua library → Task 3 ✓; KHÔNG ghi lịch sử → Task 4 (service không đụng RegulationConfigHistory) ✓.
- §1.3 FE data.js 2 tab + type library + subsystem → Task 9 (reconciliation: KHÔNG khai subsystem) ✓; screen render + modal CKEditor + ẩn nút Lưu + không cột hẹn → Task 10 ✓; hiển thị dưới "Theo công ty" → Task 10 watcher scope company ✓.
- §1.4 ERP getForSelect lọc công ty → Task 11 ✓; gỡ 2 màn admin (route/menu/controller/view) giữ model → Task 12 ✓.
- §1.5 Test BE cô lập 403 → Task 4 + Task 8 ✓; Playwright thêm/sửa/xoá + rich → Task 13 ✓; regression ERP tinker → Task 11 step 4 ✓.
- §1.6 Rủi ro (ERP không vỡ; không còn link route đã gỡ; CKEditor modal) → Task 12 step 1/5, Task 10 ✓.
Không có mục spec G1 thiếu task. G2 ngoài phạm vi (đúng spec).

**2. Placeholder scan:** Không có "TBD/TODO". Các "Ghi chú" là hướng dẫn khớp helper thật (response wrapper, `$confirm` boolean, props V2Base, selector CKEditor) — kèm cách xác định, không phải placeholder code. Mọi step code có code thật.

**3. Type consistency:**
- Tab keys `dieukhoanbaogia`/`dieukhoanthanhtoan` nhất quán Task 3/6/7/9/10/13. ✓
- `discriminator` = `type` | `payment_method_id` nhất quán registry (T3) → service `termMeta` (T4) → FormRequest (T5) → FE `curGroup.discriminator` (T9/T10). ✓
- `getTermConfig/createTerm/updateTerm/deleteTerm` chữ ký khớp giữa service (T4), controller (T6), test (T4/T8). ✓
- `optionsForSelect()` trả `['id'=>,'name'=>]` — dùng ở entity (T2), service field options (T4), FormRequest `in:` (T5), FE select `:reduce=id/label=name` (T10). ✓
- `SHAPE_LIBRARY` hằng (T3) dùng ở service/controller (T4/T6). ✓
- Route regex `[a-z]+` khớp tab keys không gạch dưới (Global Constraints + T7). ✓

Các reconciliation đã nhúng: (1) tab key không `_`; (2) không khai subsystem ở data.js; (3) library scope company → watcher branch + `curTabIsLibrary` hide savebar.

---

---

## Điều chỉnh sau nghiệm thu — Bảng thư viện: bỏ cột Nội dung, thêm Ngày tạo/Người tạo (2026-09-24)

Yêu cầu: bảng danh sách điều khoản (cả tab Báo giá + Thanh toán) bỏ cột **Nội dung**, thêm **Ngày tạo** + **Người tạo**. Cột nội dung (rich HTML + placeholder `{{VAT_NOTE}}`…) tràn dài, khó đọc; ngày/người tạo hữu ích hơn cho tra soát.

- [x] **BE** `RegulationConfigService::presentTerm()` — thêm `created_at` (format `d/m/Y`) + `created_by_name` (accessor `employee_create_name` của BaseModel, khuôn `mã - tên`). GIỮ `content` trong payload (form Sửa vẫn nạp ô nội dung từ `r.content`).
- [x] **BE** `getTermConfig()` — eager-load `->with('employee_create.info')` tránh N+1.
- [x] **FE** `RegulationConfigScreen.vue` block `type==='library'` — thead bỏ `<th>Nội dung</th>`, thêm `Ngày tạo`/`Người tạo`; tbody bỏ ô `v-html="r.content"`, thêm `{{ r.created_at }}` / `{{ r.created_by_name || '—' }}`; colspan dòng rỗng 5→6 (4→5).
- [x] Test: `RegulationTermTest` 6/6 pass; Playwright: bảng hiển thị đúng 6 cột (không còn Nội dung), form Sửa vẫn nạp CKEditor nội dung.

Quyết định đã chốt: Ngày tạo hiện `dd/mm/yyyy` (không kèm giờ); Người tạo khuôn `mã - tên`. Chỉ bỏ nội dung khỏi BẢNG, KHÔNG bỏ khỏi form Thêm/Sửa.

---
---

# GIAI ĐOẠN 2 — `configs` per-company (17 field điều khoản/cấu hình)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development` (khuyến nghị) hoặc `superpowers:executing-plans` để thực thi từng task. Bước dùng checkbox `- [ ]`.

**Goal:** Chuyển ~17 field `store='config'` (điều khoản báo giá, hệ số giá, cảnh báo mượn/giữ, phân nhóm thị trường…) từ **1 hàng `configs` singleton dùng chung** sang **`configs` per-company** (mỗi công ty 1 hàng), để mỗi công ty cấu hình riêng — cả chiều GHI (màn quy chế HRM + admin ERP) lẫn chiều ĐỌC (~166 điểm ERP đọc qua `Config::getConfig()`).

**Architecture:** Phương án A — thêm `company_id` vào `configs`, clone singleton thành mỗi công ty 1 hàng, và lọc theo công ty tại **1 điểm trung tâm** `Config::getConfig()` (ERP) + tại 3 điểm chạm DB của `RegulationConfigService` (HRM). HRM tái dùng đúng cơ chế version/hẹn-ngày sẵn có: field `store='config'` giữ `scope_type='global'` làm **bộ chọn store** (route sang bảng `configs`) nhưng `scope_id` đổi từ `0` → `companyId`, và mọi truy vấn `configs` thêm `WHERE company_id`.

**Tech Stack:** ERP `ERP/TanPhatDev` (Laravel 6.20/PHP 7.4, Blade + AngularJS) · HRM hrm-api (Laravel 8/PHP 7.4, `Modules/MasterData`) · hrm-client (Nuxt 2/Vue 2, Node 14) · Test: PHPUnit + tinker + Playwright (Node 20).

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-09-24-config-per-company-g2-design.md`

## Global Constraints (G2)

- **Nhánh `gop_db`**: KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`. Bảng trùng tên ưu tiên bản ERP. Tài liệu về `HRM/.plans/gop-db/`, spec về `docs/superpowers/specs/gop-db/`. KHÔNG commit/push khi user chưa yêu cầu.
- **Scope thư mục**: thao tác HRM trong `HRM/`, thao tác ERP trong `ERP/TanPhatDev/`. KHÔNG tạo file ở root `ERP-HRM/`.
- **CRLF**: nhiều file `hrm-client` (và một số `hrm-api`) là CRLF — kiểm `grep -c $'\r' <file>` trước khi sửa; dòng thêm mới cũng phải CRLF; sau khi sửa chạy `git diff --stat` để chắc không nuốt `\r`.
- **Định dạng số quốc tế** (`,` nghìn, `.` thập phân); **ngày `dd/mm/yyyy`**.
- **Model mới `extends BaseModel`**; audit `created_by/updated_by` = `auth()->id()`.
- **Fail-closed quyền**: KHÔNG hard-code cờ quyền `= true`.
- **KHÔNG DROP 2 cột chết** `quotation_footer`, `coefficient_cost_price_service` — chỉ ẨN khỏi UI (quyết định user "ẩn", 2026-09-24). BE vẫn chấp nhận, vô hại.
- **KHÔNG sửa dữ liệu lịch sử cũ** (`scope_type='global', scope_id=0`) — để nguyên làm dấu vết; chỉ bản ghi MỚI theo company.
- Mọi task/fix ghi vào plan.md này (append, đánh `[x]` khi xong).

## ⚠️ Điểm cần user xác nhận trước khi thực thi Task 19-20 (đã phát hiện khi lập plan)

Tab `chung` (scope=GLOBAL) chứa `logo`/`header`… (KHÔNG nằm trong 17 field), hiện ghi `configs` singleton. Vì migration bỏ singleton (mọi hàng `configs` đều có `company_id`, ERP `getConfig()` lọc theo công ty), **không còn "hàng global" để ghi** → tab `chung` **buộc cũng phải flip per-company** (transparent với UI, không đổi FE). Đây là hệ quả BẮT BUỘC của schema, nhưng vượt khỏi khung "17 field" mà spec nêu.
→ **Đề xuất (khuyến nghị): flip luôn `chung`** (nhất quán: cả hàng `configs` đã per-company; `logo/header` per-company thực ra đúng hơn). Phương án thay thế (giữ 1 hàng "global" cho `chung` song song các hàng per-company) phức tạp & mong manh hơn → không khuyến nghị. **Cần user chốt trước khi làm Task 20.**

---

### Task 14: Migration `configs` + `company_id` + clone per-company (HRM)

**Files:**
- Create: `HRM/hrm-api/database/migrations/2026_09_24_000001_add_company_id_to_configs_and_clone_per_company.php`
- Test: `HRM/hrm-api/tests/Feature/ConfigPerCompanyMigrationTest.php` (hoặc script tinker ở scratchpad nếu test infra chưa sẵn — xem Step 2)

**Interfaces:**
- Consumes: bảng `configs` (singleton, ~49 cột, chưa có `company_id`), `companies` (danh sách công ty), `contract_rows` (fk `config_id`).
- Produces: `configs.company_id` (unsignedBigInteger nullable + index); mỗi công ty trong `companies` có đúng 1 hàng `configs`; hàng singleton cũ nhận `company_id=1`; `contract_rows` được nhân bản cho từng hàng `configs` mới. Idempotent.

- [ ] **Step 1: Viết test kiểm bất biến sau migration**

```php
// tests/Feature/ConfigPerCompanyMigrationTest.php
public function test_every_company_has_exactly_one_config_row_after_migrate()
{
    $companyIds = DB::table('companies')->pluck('id');
    foreach ($companyIds as $cid) {
        $count = DB::table('configs')->where('company_id', $cid)->count();
        $this->assertSame(1, $count, "Công ty $cid phải có đúng 1 hàng configs");
    }
    // hàng singleton cũ → company 1
    $this->assertTrue(DB::table('configs')->where('company_id', 1)->exists());
    // cột tồn tại
    $this->assertTrue(Schema::hasColumn('configs', 'company_id'));
}
```

- [ ] **Step 2: Chạy test để chắc nó FAIL**

Run: `cd HRM/hrm-api && php artisan test --filter=ConfigPerCompanyMigrationTest`
Expected: FAIL (cột `company_id` chưa có / công ty khác chưa có hàng).
*(Nếu suite Feature cần DB test chưa dựng: thay bằng script tinker ở `<scratchpad>/verify_config_migration.php` assert 3 điều trên, chạy `php artisan tinker < script` — phải in FAIL trước migrate.)*

- [ ] **Step 3: Viết migration**

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

class AddCompanyIdToConfigsAndClonePerCompany extends Migration
{
    public function up()
    {
        // 1) Thêm cột (idempotent)
        if (!Schema::hasColumn('configs', 'company_id')) {
            Schema::table('configs', function (Blueprint $t) {
                $t->unsignedBigInteger('company_id')->nullable()->index()->after('id');
            });
        }

        // 2) Backfill: hàng singleton hiện có → company 1 (công ty gốc ERP)
        $singleton = DB::table('configs')->orderBy('id')->first();
        if (!$singleton) { return; } // DB rỗng bất thường → thôi
        if ($singleton->company_id === null) {
            DB::table('configs')->where('id', $singleton->id)->update(['company_id' => 1]);
            $singleton = DB::table('configs')->where('id', $singleton->id)->first();
        }
        $srcId = $singleton->id; // hàng nguồn để clone

        // 3) Clone cho MỌI công ty chưa có hàng (guard: chỉ tạo công ty thiếu)
        $existing = DB::table('configs')->whereNotNull('company_id')->pluck('company_id')->all();
        $companyIds = DB::table('companies')->pluck('id')->all();
        foreach ($companyIds as $cid) {
            if (in_array($cid, $existing)) { continue; }
            $clone = (array) DB::table('configs')->where('id', $srcId)->first();
            unset($clone['id']);
            $clone['company_id'] = $cid;
            $newId = DB::table('configs')->insertGetId($clone);
            // 3b) Clone contract_rows (fk=config_id) của hàng nguồn sang hàng mới
            $rows = DB::table('contract_rows')->where('config_id', $srcId)->get();
            foreach ($rows as $r) {
                $row = (array) $r; unset($row['id']);
                $row['config_id'] = $newId;
                DB::table('contract_rows')->insert($row);
            }
        }
    }

    public function down()
    {
        // Chỉ gỡ cột — KHÔNG xoá các hàng đã clone (không thể phân biệt an toàn dữ liệu người dùng đã sửa)
        if (Schema::hasColumn('configs', 'company_id')) {
            Schema::table('configs', function (Blueprint $t) {
                $t->dropIndex(['company_id']);
                $t->dropColumn('company_id');
            });
        }
    }
}
```

- [ ] **Step 4: Chạy migrate + test → PASS**

Run: `cd HRM/hrm-api && grep DB_ .env` (xác nhận DB đích đúng — theo memory ERP local .env có thể trỏ prod/dev; migration đụng dữ liệu thật) → `php artisan migrate` → `php artisan test --filter=ConfigPerCompanyMigrationTest`
Expected: migrate OK, test PASS. Chạy lại `php artisan migrate:refresh`? KHÔNG (dữ liệu chung). Chạy `php artisan migrate` lần 2 KHÔNG được (đã migrate) → kiểm idempotent bằng cách gọi lại logic up() qua tinker trên DB đã có cột: không tạo trùng hàng.

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api
git add database/migrations/2026_09_24_000001_add_company_id_to_configs_and_clone_per_company.php tests/Feature/ConfigPerCompanyMigrationTest.php
git commit -m "feat(gopdb): configs thêm company_id + clone per-company (G2 dieukhoan-per-company)"
```

---

### Task 15: ERP `Config::getConfig()` per-company + `resolveCompanyId()` (ERP)

**Files:**
- Modify: `ERP/TanPhatDev/app/Model/Common/Config.php` (method `getConfig`, dòng ~11-18)
- Test: `ERP/TanPhatDev/<scratchpad>/verify_getconfig.php` (script tinker; ERP L6 không có Feature test cho model này — dùng tinker assert)

**Interfaces:**
- Consumes: `configs.company_id` (từ Task 14); `auth()->user()->info->company_id` (quan hệ user→info sẵn có ở ERP).
- Produces: `Config::getConfig($column = null, $companyId = null)` — resolve công ty theo thứ tự `param → auth info → 1`, trả hàng/cột của đúng công ty; fallback công ty 1 rồi `first()` khi thiếu (deploy-tolerant). Chữ ký tương thích ngược mọi call cũ `getConfig()` / `getConfig('col')`.

- [ ] **Step 1: Viết script assert (test)**

```php
// <scratchpad>/verify_getconfig.php  — chạy: php artisan tinker < verify_getconfig.php
// Giả định công ty 1 và 2 có warning_day khác nhau để phân biệt.
DB::table('configs')->where('company_id', 1)->update(['warning_day' => 7]);
DB::table('configs')->where('company_id', 2)->update(['warning_day' => 30]);
$a = \App\Model\Common\Config::getConfig('warning_day', 1);
$b = \App\Model\Common\Config::getConfig('warning_day', 2);
echo ($a == 7 && $b == 30) ? "PASS\n" : "FAIL got a=$a b=$b\n";
$row = \App\Model\Common\Config::getConfig(null, 2);
echo ($row && (int)$row->company_id === 2) ? "PASS row\n" : "FAIL row\n";
```

- [ ] **Step 2: Chạy → FAIL**

Run: `cd ERP/TanPhatDev && php artisan tinker < <scratchpad>/verify_getconfig.php`
Expected: FAIL — `getConfig` cũ bỏ qua `$companyId`, luôn trả hàng đầu (company 1) → `b` sai (=7, không phải 30).

- [ ] **Step 3: Sửa `getConfig` + thêm `resolveCompanyId`**

```php
// app/Model/Common/Config.php
public static function getConfig($column = null, $companyId = null)
{
    $companyId = self::resolveCompanyId($companyId);
    $row = self::where('company_id', $companyId)->first();
    if (!$row && $companyId !== 1) {
        $row = self::where('company_id', 1)->first(); // công ty tạo sau, chưa backfill
    }
    if (!$row) { $row = self::first(); } // deploy dở / chưa migrate → giữ code không vỡ
    if ($column) { return $row ? $row->{$column} : null; }
    return $row;
}

/** param → auth()->user()->info->company_id → 1 */
private static function resolveCompanyId($companyId = null)
{
    if ($companyId) { return (int) $companyId; }
    $auth = auth()->user();
    if ($auth && $auth->info && $auth->info->company_id) { return (int) $auth->info->company_id; }
    return 1;
}
```

Ghi chú: nếu `getConfig('col')` cũ dùng `self::query()->value($column)` → bản mới đọc `$row->{$column}` sau khi lọc công ty (giữ đúng semantic, chỉ khác theo công ty). KHÔNG thêm cache tĩnh (tùy chọn tối ưu, không bắt buộc — nếu đo thấy nặng thì cache `[companyId => row]` static, clear khi `save()`).

- [ ] **Step 4: Chạy script → PASS**

Run: `cd ERP/TanPhatDev && php artisan tinker < <scratchpad>/verify_getconfig.php`
Expected: `PASS` + `PASS row`.

- [ ] **Step 5: Commit**

```bash
cd ERP/TanPhatDev
git add app/Model/Common/Config.php
git commit -m "feat(gopdb): Config::getConfig lọc theo công ty đăng nhập (G2)"
```

---

### Task 16: ERP — 7 điểm đọc trực tiếp model `Config` → `Config::getConfig()` (ERP)

> **RULING 2026-09-24 (mở rộng scope):** scan thực tế `app/` thấy 7 điểm đọc trực tiếp `App\Model\Common\Config` (bypass `getConfig`), không phải 4 như liệt kê ban đầu. Sau migrate, `Config::first()`/`Config::query()->first()` trả nhầm hàng công ty 1 cho mọi user. Tất cả 7 đều ở REQUEST-context (có auth) → thay bằng `Config::getConfig()`, KHÔNG cần truyền `$companyId`. `CommonConfig` = alias của cùng model. NGOÀI scope: `ServicePriceConfig::find(1)`, `CompanyBonusEndYearConfig` (model khác, đã có company_id riêng); dòng 2636 ProductsController đã comment.

**Files (7 điểm / 5 file):**
- Modify: `ERP/TanPhatDev/app/ProductApprove.php:37` — `Config::first()` (static `getProductTypes` → `product_types`)
- Modify: `ERP/TanPhatDev/app/ProductTemplate.php:7551` — `Config::first()` (`getProductTypes`)
- Modify: `ERP/TanPhatDev/app/Product.php:8196` — `Config::first()` (`getProductTypes`)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/ReportController.php:1254` — `Config::query()->first()` (`customerCareFrequencySearchData` → `customer_is_following`/`customer_taken_care`)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/ProductsController.php:1549` — `CommonConfig::first()` (`store` → `coefficient_ecommerce_price`)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/ProductsController.php:2320` — `CommonConfig::first()` (`getProductsAndPrices` → `is_company_price`)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/ProductsController.php:2691` — `CommonConfig::first()` (`updatePrice` → `coefficient_ecommerce_price`)

**Interfaces:**
- Consumes: `Config::getConfig()` (Task 15).
- Produces: 7 điểm đọc config nay đi qua lõi resolve company (tự đúng công ty trong request có auth). PASS = grep bypass-read model `Config` trong 5 file này RỖNG.

- [ ] **Step 1: Xác minh ngữ cảnh từng điểm (grep)**

Run: `cd ERP/TanPhatDev && grep -n "Config::first()" app/ProductTemplate.php app/Product.php app/ProductApprove.php app/Http/Controllers/ReportController.php`
Với mỗi điểm, kiểm hàm bao quanh chạy trong **request có auth** hay **job/cron**. Nếu là job/cron → phải truyền `$companyId` (lấy từ đối tượng đang xử lý), KHÔNG để resolve về công ty 1. Ghi kết luận từng điểm vào plan trước khi sửa.

- [ ] **Step 2: Viết assert nhanh (test)**

Không có unit test riêng cho 4 điểm này → dùng grep-assert: sau khi sửa, `grep -rn "Config::first()" app/ProductTemplate.php app/Product.php app/ProductApprove.php app/Http/Controllers/ReportController.php` phải RỖNG (đã thay hết). Đây là điều kiện PASS của task.

- [ ] **Step 3: Thay từng điểm**

Đổi `Config::first()` → `Config::getConfig()` (request có auth), hoặc `Config::getConfig(null, $companyId)` (job/cron — `$companyId` từ ngữ cảnh, vd `$product->company_id` / `$report->company_id`). GIỮ nguyên biến nhận (`$config = ...`) và cách dùng phía sau.

- [ ] **Step 4: Chạy grep-assert → RỖNG + smoke test**

Run: `grep -rn "Config::first()" app/ProductTemplate.php app/Product.php app/ProductApprove.php app/Http/Controllers/ReportController.php` → RỖNG.
Smoke: mở 1 luồng dùng mỗi điểm (in báo giá / duyệt sản phẩm / report) trên dev, xác nhận không lỗi.

- [ ] **Step 5: Commit**

```bash
cd ERP/TanPhatDev
git add app/ProductTemplate.php app/Product.php app/ProductApprove.php app/Http/Controllers/ReportController.php
git commit -m "feat(gopdb): 4 điểm Config::first() -> getConfig theo công ty (G2)"
```

---

### Task 17: ERP `ConfigsController` per-company write + guard + chỉ báo công ty (ERP)

**Files:**
- Modify: `ERP/TanPhatDev/app/Http/Controllers/Common/ConfigsController.php` (`edit()`, `update()`)
- Modify: `ERP/TanPhatDev/resources/views/common/configs/edit.blade.php` (chỉ báo công ty đầu form)
- Test: `ERP/TanPhatDev/<scratchpad>/verify_configs_update.php` (tinker assert)

**Interfaces:**
- Consumes: `Config::getConfig()` (Task 15) — nay trả hàng công ty đăng nhập.
- Produces: `update()` ghi đúng hàng công ty đăng nhập; **guard**: nếu hàng trả về `company_id != auth company` → tạo hàng mới cho công ty đăng nhập (clone rồi gán `company_id`) TRƯỚC khi save, KHÔNG ghi đè hàng công ty 1. `ContractRow::where('config_id', $config->id)` tự đúng theo id hàng công ty hiện tại.

- [ ] **Step 1: Viết assert (test)**

```php
// <scratchpad>/verify_configs_update.php
// Mô phỏng: đăng nhập user công ty 2, cập nhật quotation_valid_days=99
$before1 = \App\Model\Common\Config::getConfig('quotation_valid_days', 1);
// ... (gọi update path với auth công ty 2; hoặc test logic guard tách riêng) ...
$after2  = \App\Model\Common\Config::getConfig('quotation_valid_days', 2);
$after1  = \App\Model\Common\Config::getConfig('quotation_valid_days', 1);
echo ($after2 == 99 && $after1 == $before1) ? "PASS isolation\n" : "FAIL a1=$after1 a2=$after2\n";
```

- [ ] **Step 2: Chạy → FAIL** (update cũ ghi hàng đầu = công ty 1 → `after1` bị đổi thành 99).

Run: `cd ERP/TanPhatDev && php artisan tinker < <scratchpad>/verify_configs_update.php` → FAIL.

- [ ] **Step 3: Sửa `update()` + `edit()` + guard**

```php
// ConfigsController::update() — đầu hàm, sau khi lấy config
$config = Config::getConfig(); // nay trả hàng công ty đăng nhập (hoặc fallback công ty 1)
$authCompanyId = (int) (auth()->user()->info->company_id ?? 1);
// GUARD: công ty đăng nhập chưa có hàng riêng → getConfig fallback trả hàng công ty 1.
// Không được ghi đè hàng công ty 1: clone sang hàng mới của công ty đăng nhập.
if ((int) $config->company_id !== $authCompanyId) {
    $clone = $config->replicate();
    $clone->company_id = $authCompanyId;
    $clone->save();
    $config = $clone;
}
// ... gán ~40 cột như cũ rồi $config->save();
// ContractRow::where('config_id', $config->id)->delete(); + rebuild — tự đúng vì $config->id là hàng công ty này
```

`edit()`: đảm bảo đổ form từ `Config::getConfig()` (đã tự lọc công ty). Không cần sửa nhiều.

- [ ] **Step 4: Chỉ báo công ty trong `edit.blade.php`**

Thêm đầu form (theo skill hiển thị ERP; tối thiểu text):
```blade
<div class="alert alert-info">Đang cấu hình cho công ty: <strong>{{ optional($config->company)->name ?? ('#'.$config->company_id) }}</strong></div>
```
(Kiểm quan hệ `company()` trên model Config; nếu chưa có, dùng `\App\Model\Common\Company::find($config->company_id)->name`.)

- [ ] **Step 5: Chạy assert → PASS + smoke**

Run: tinker script → `PASS isolation`. Smoke: đăng nhập 2 công ty khác nhau, sửa quotation_valid_days mỗi bên, xác nhận không đè nhau + chỉ báo công ty hiện đúng tên.

- [ ] **Step 6: Commit**

```bash
cd ERP/TanPhatDev
git add app/Http/Controllers/Common/ConfigsController.php resources/views/common/configs/edit.blade.php
git commit -m "feat(gopdb): ConfigsController ghi config theo công ty + guard hàng mới (G2)"
```

---

### Task 18: ERP — 2 console command lặp per-company (ERP) ⚠️ regression trọng yếu

**Files:**
- Modify: `ERP/TanPhatDev/app/Console/Commands/BorrowWarning.php:50-52`
- Modify: `ERP/TanPhatDev/app/Console/Commands/PrepickWarning.php:50-52`
- Test: `ERP/TanPhatDev/<scratchpad>/verify_warning_percompany.php` (tinker assert)

**Interfaces:**
- Consumes: `Config::getConfig('warning_day', $companyId)` (Task 15); danh sách công ty có hàng config.
- Produces: mỗi command lặp qua từng công ty, dùng `warning_day` CỦA công ty đó, và **lọc dữ liệu cảnh báo theo đúng công ty** (không gửi trùng N lần).

- [ ] **Step 1: Xác minh scope công ty của query cảnh báo hiện tại**

Run: `cd ERP/TanPhatDev && sed -n '1,120p' app/Console/Commands/BorrowWarning.php app/Console/Commands/PrepickWarning.php` (đọc để biết query đơn mượn/giữ join qua đâu để suy ra công ty). **Kết luận bắt buộc ghi vào plan:** đơn thuộc công ty nào (cột/nào join `company_id`)? Nếu query cũ KHÔNG phân công ty → phải thêm điều kiện công ty trong vòng lặp, nếu không mỗi công ty gửi lại toàn bộ đơn (gửi trùng).

- [ ] **Step 2: Viết assert (test)**

```php
// <scratchpad>/verify_warning_percompany.php
// Đặt warning_day khác nhau, chạy handle(), đếm số cảnh báo mỗi công ty đúng theo đơn của công ty đó.
// Tối thiểu: assert command đọc đúng warning_day per-company (không phải 1 giá trị chung).
```
(Nếu khó dựng dữ liệu đơn: tối thiểu assert vòng lặp gọi `getConfig('warning_day', $cid)` cho mỗi `$cid` và không còn đọc `warning_day` toàn cục 1 lần.)

- [ ] **Step 3: Sửa mỗi command sang vòng lặp per-company**

```php
foreach (DB::table('configs')->whereNotNull('company_id')->pluck('company_id')->unique() as $companyId) {
    $warningDay = \App\Model\Common\Config::getConfig('warning_day', $companyId);
    $date = Carbon::now()->addDays((int) $warningDay)->format('Y-m-d');
    // query đơn mượn/giữ CỦA $companyId (thêm where company_id nếu Step 1 kết luận query cũ không phân công ty),
    // gửi cảnh báo — GIỮ nguyên phần gửi, chỉ bọc theo công ty.
}
```

- [ ] **Step 4: Chạy assert + chạy thử command trên dev → PASS, không gửi trùng**

Run: `cd ERP/TanPhatDev && php artisan tinker < <scratchpad>/verify_warning_percompany.php` → PASS. Chạy `php artisan <borrow-warning-signature>` trên dev (kiểm log/notification không nhân đôi).

- [ ] **Step 5: Commit**

```bash
cd ERP/TanPhatDev
git add app/Console/Commands/BorrowWarning.php app/Console/Commands/PrepickWarning.php
git commit -m "feat(gopdb): BorrowWarning/PrepickWarning lặp warning_day per-company (G2)"
```

---

### Task 19: HRM `RegulationConfigService` — chiều ĐỌC config-store per-company (HRM)

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Services/RegulationConfigService.php` — `getCurrentValues()` (dòng 281), `subtableFkValue()` (dòng 88-94)
- Test: `HRM/hrm-api/tests/Feature/RegulationConfigPerCompanyReadTest.php`

**Interfaces:**
- Consumes: `configs.company_id` (Task 14); `$scopeId` truyền vào `getCurrentValues` chính là `companyId` (getTabConfig gọi `getCurrentValues($companyId,...)`; applyVersion gọi với `version.scope_id` — sau Task 20 = companyId).
- Produces: `getCurrentValues($scopeId=companyId, $tabKey, 'config')` đọc `configs WHERE company_id=$scopeId`; `subtableFkValue` (fk=config_id, contract_rows) trả id hàng `configs` CỦA công ty đó.

- [ ] **Step 1: Viết test đọc per-company**

```php
// tests/Feature/RegulationConfigPerCompanyReadTest.php
public function test_getCurrentValues_reads_config_row_of_that_company()
{
    DB::table('configs')->where('company_id', 1)->update(['quotation_valid_days' => 15]);
    DB::table('configs')->where('company_id', 2)->update(['quotation_valid_days' => 45]);
    $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
    $v1 = $svc->getCurrentValues(1, 'baogia', 'config');
    $v2 = $svc->getCurrentValues(2, 'baogia', 'config');
    $this->assertSame(15, (int) $v1['quotation_valid_days']);
    $this->assertSame(45, (int) $v2['quotation_valid_days']);
}
```

- [ ] **Step 2: Chạy → FAIL**

Run: `cd HRM/hrm-api && php artisan test --filter=RegulationConfigPerCompanyReadTest`
Expected: FAIL — `getCurrentValues` cũ đọc `configs->first()` (luôn công ty 1) → `v2` = 15 chứ không 45.

- [ ] **Step 3: Sửa 2 điểm đọc**

`getCurrentValues` dòng 281:
```php
// TRƯỚC: $configRow = $needConfig ? DB::table('configs')->first() : null;
$configRow  = $needConfig ? DB::table('configs')->where('company_id', $scopeId)->first() : null;
```
`subtableFkValue` dòng 88-94:
```php
private function subtableFkValue(array $meta, int $scopeId): ?int
{
    if (($meta['fk'] ?? null) === 'company_id') {
        return $scopeId ?: null;
    }
    // config_id (contract_rows): hàng configs CỦA công ty $scopeId (không còn singleton)
    return DB::table('configs')->where('company_id', $scopeId)->value('id') ?: null;
}
```
Cập nhật docblock 2 method cho khớp (bỏ chữ "singleton").

- [ ] **Step 4: Chạy test → PASS**

Run: `cd HRM/hrm-api && php artisan test --filter=RegulationConfigPerCompanyReadTest` → PASS.

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api
git add Modules/MasterData/Services/RegulationConfigService.php tests/Feature/RegulationConfigPerCompanyReadTest.php
git commit -m "feat(gopdb): RegulationConfigService đọc config-store theo company_id (G2)"
```

---

### Task 20: HRM `RegulationConfigService` — chiều GHI/version config-store per-company (HRM)

> ⚠️ Chỉ bắt đầu sau khi user chốt "Điểm cần user xác nhận" (flip tab `chung`) ở đầu G2.

**Files:**
- Modify: `HRM/hrm-api/Modules/MasterData/Services/RegulationConfigService.php` — `createGlobalVersion()` (741-766), `saveTabVersions()` (813, 822), `scopeSpecsForTab()` (315, 318), `applyVersion()` nhánh global (930-957), `getHistory` filter (1448, 1631), controller check (`RegulationConfigController.php:122`)
- Test: `HRM/hrm-api/tests/Feature/RegulationConfigPerCompanyWriteTest.php`

**Interfaces:**
- Consumes: Task 19 (đọc per-company), `configs.company_id`.
- Produces: field `store='config'` tạo version `scope_type='global', scope_id=companyId` (thay vì 0); `applyVersion` ghi `configs WHERE company_id=$scopeId` + subtable contract_rows theo hàng công ty; lịch sử `scope_id=companyId`; lưu công ty A KHÔNG ảnh hưởng công ty B.

**Cơ chế (đã khoá khi lập plan):** giữ `scope_type='global'` làm **bộ chọn store** (`storeForScopeType('global')='config'` → route nhánh configs), CHỈ đổi `scope_id` từ `0` → `companyId` xuyên suốt path config, và thêm `WHERE company_id` ở nhánh ghi. KHÔNG remap sang `scope_type='company'` (sẽ vỡ store-routing → ghi nhầm bảng `companies`).

- [ ] **Step 1: Viết test lưu per-company không đè nhau**

```php
// tests/Feature/RegulationConfigPerCompanyWriteTest.php
public function test_saveTab_config_field_is_isolated_per_company()
{
    $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
    // Lưu cho công ty 1: quotation_valid_days=10 (áp ngay: effective_date = hôm nay)
    $svc->saveTabVersions(1, 'baogia', now()->toDateString(),
        ['quotation_valid_days' => 10], null, 1);
    // Lưu cho công ty 2: quotation_valid_days=20
    $svc->saveTabVersions(2, 'baogia', now()->toDateString(),
        ['quotation_valid_days' => 20], null, 1);
    $this->assertSame(10, (int) DB::table('configs')->where('company_id', 1)->value('quotation_valid_days'));
    $this->assertSame(20, (int) DB::table('configs')->where('company_id', 2)->value('quotation_valid_days'));
}
```

- [ ] **Step 2: Chạy → FAIL**

Run: `cd HRM/hrm-api && php artisan test --filter=RegulationConfigPerCompanyWriteTest`
Expected: FAIL — createGlobalVersion ghi `scope_id=0` + applyVersion ghi `configs->value('id')` singleton → cả 2 lần ghi cùng 1 hàng (công ty 1), công ty 2 = 20 đè lên, công ty 1 không thành 10.

- [ ] **Step 3: Sửa path version config → per-company**

3a) `createGlobalVersion` — thêm `$companyId`, dùng làm `scope_id`:
```php
public function createGlobalVersion(int $companyId, string $tabKey, string $effectiveDate, array $values, ?string $note, int $actorId): RegulationScheduledVersion
{
    $payload = $this->normalizeValues($values, $tabKey, 'config');
    $version = new RegulationScheduledVersion([
        'scope_type' => self::SCOPE_GLOBAL,      // bộ chọn store = configs (GIỮ)
        'scope_id'   => $companyId,              // TRƯỚC: 0
        'tab_key'    => $tabKey,
        'effective_date' => $effectiveDate,
        'status'     => RegulationScheduledVersion::STATUS_PENDING,
        'payload'    => $payload, 'diff_snapshot' => [], 'note' => $note,
    ]);
    $version->created_by = $actorId; $version->updated_by = $actorId; $version->save();
    $this->recomputeDiffChain($companyId, $tabKey, self::SCOPE_GLOBAL); // TRƯỚC: 0
    $version = $version->fresh();
    if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
        $this->applyDueVersions(null, $companyId, $tabKey);              // TRƯỚC: 0
        $version = $version->fresh();
    }
    return $version;
}
```

3b) `saveTabVersions` — truyền companyId (dòng 813 tab GLOBAL `chung`, dòng 822 nhánh MIXED):
```php
$created[] = $this->createGlobalVersion($companyId, $tabKey, $effectiveDate, $values, $note, $actorId);
```

3c) `scopeSpecsForTab` (315, 318) — config đọc theo company:
```php
if ($scope === RegulationTabRegistry::SCOPE_GLOBAL) {
    return [[self::SCOPE_GLOBAL, $companyId]];                          // TRƯỚC: 0
}
if ($scope === RegulationTabRegistry::SCOPE_MIXED) {
    return [[self::SCOPE_COMPANY, $companyId], [self::SCOPE_GLOBAL, $companyId]]; // TRƯỚC: global 0
}
```

3d) `applyVersion` nhánh global (930-957) — lọc theo company_id (`$scopeId` = companyId):
```php
} else { // config store → configs của công ty $scopeId
    $configId = DB::table('configs')->where('company_id', $scopeId)->value('id');
    abort_if(!$configId, 500, 'configs công ty '.$scopeId.' không tồn tại');
    // ... phần tách subtable applySubtable((int)$configId, ...) GIỮ nguyên (id đúng hàng công ty)
    // ... DB::table('configs')->where('id', $configId)->update(...) GIỮ (id đã đúng hàng công ty)
    if (!empty($diffs)) {
        RegulationConfigHistory::create([
            'scope_type' => self::SCOPE_GLOBAL,
            'scope_id'   => $scopeId,                                    // TRƯỚC: 0
            'tab_key'    => $tabKey, 'diff' => $diffs,
            'source' => 'apply', 'created_by' => $locked->created_by,
        ]);
    }
}
```

3e) `getHistory` filter global (1448, 1631) — đọc lịch sử MỚI theo company nhưng vẫn gộp dấu vết cũ scope_id=0:
```php
// TRƯỚC: $qq->where('scope_type', self::SCOPE_GLOBAL)->where('scope_id', 0);
$qq->where('scope_type', self::SCOPE_GLOBAL)->whereIn('scope_id', [0, $companyId]);
```
(Giữ `0` để lịch sử cũ vẫn hiện; thêm `$companyId` cho bản ghi mới. Xác nhận biến `$companyId`/`$scopeId` sẵn trong scope 2 closure này khi sửa.)

3f) `RegulationConfigController.php:122` — điều kiện nhận version global: `(int)$version->scope_id === 0` nay có thể là companyId. Sửa: bỏ ràng buộc `=== 0`, hoặc đổi thành `>= 0` (chấp nhận cả 0 cũ lẫn companyId). Đọc ngữ cảnh dòng 122 trước khi sửa để không nới lỏng quyền ngoài ý định.

- [ ] **Step 4: Chạy test → PASS + regression toàn bộ suite regulation-config**

Run:
```
cd HRM/hrm-api
php artisan test --filter=RegulationConfigPerCompanyWriteTest
php artisan test --filter=RegulationConfig   # toàn bộ test regulation-config cũ vẫn xanh
```
Expected: PASS + không vỡ test cũ (đặc biệt luồng company-store + department + hẹn ngày).

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-api
git add Modules/MasterData/Services/RegulationConfigService.php Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php tests/Feature/RegulationConfigPerCompanyWriteTest.php
git commit -m "feat(gopdb): RegulationConfigService ghi config-store per-company qua scope_id=companyId (G2)"
```

---

### Task 21: HRM hrm-client — ẨN 2 field chết khỏi màn quy chế (FE)

**Files:**
- Modify: `HRM/hrm-client/components/regulation-config/data.js` (bỏ 2 field khỏi danh sách hiển thị tab tương ứng)
- (Nếu render trực tiếp) Modify: `HRM/hrm-client/components/regulation-config/RegulationConfigScreen.vue`

**Interfaces:**
- Consumes: cấu hình field tab từ `data.js` / API `getTabConfig`.
- Produces: 2 field `quotation_footer`, `coefficient_cost_price_service` KHÔNG còn render trên UII. BE vẫn chấp nhận nếu có (không validate bắt buộc) — không ai sửa được nữa.

- [ ] **Step 1: Kiểm CRLF + định vị 2 field**

Run: `cd HRM/hrm-client && grep -c $'\r' components/regulation-config/data.js && grep -n "quotation_footer\|coefficient_cost_price_service" components/regulation-config/data.js components/regulation-config/RegulationConfigScreen.vue`
Ghi lại: file CRLF hay LF (dòng sửa phải theo đúng kiểu).

- [ ] **Step 2: Viết assert (test)**

Playwright là kênh kiểm chính (Step trong Task 22). Ở mức FE-only: sau khi ẩn, `grep -n "quotation_footer\|coefficient_cost_price_service" components/regulation-config/data.js` không còn nằm trong mảng field hiển thị (chỉ được còn ở chỗ vô hại nếu có). Điều kiện PASS.

- [ ] **Step 3: Ẩn 2 field**

Bỏ 2 entry field khỏi mảng field của tab tương ứng trong `data.js` (giữ CRLF nếu file CRLF). KHÔNG xoá logic BE, KHÔNG xoá cột DB.

- [ ] **Step 4: Kiểm build FE không lỗi**

Run: `cd HRM/hrm-client && git diff --stat` (số dòng đổi nhỏ, đúng vùng — không nuốt CRLF toàn file). Mở màn quy chế trên dev, xác nhận 2 field biến mất, các field khác nguyên vẹn.

- [ ] **Step 5: Commit**

```bash
cd HRM/hrm-client
git add components/regulation-config/data.js components/regulation-config/RegulationConfigScreen.vue
git commit -m "feat(gopdb): ẩn 2 field config chết khỏi màn quy chế (G2)"
```

---

### Task 22: HRM Playwright e2e — kiểm per-company + 2 field ẩn (HRM)

**Files:**
- Create/Modify: `HRM/e2e/tests/regulation-config/per-company.spec.ts`
- (Có thể tái dùng) `HRM/e2e/pages/RegulationConfigPage.ts`

**Interfaces:**
- Consumes: màn quy chế `/…regulation-config` chạy trên FE `:3000` + API `:8000`; đăng nhập qua storageState.
- Produces: chứng minh (1) cấu hình field config ở công ty A không đổi giá trị công ty B; (2) 2 field chết không render.

- [ ] **Step 1: Viết spec**

```ts
// tests/regulation-config/per-company.spec.ts
import { test, expect } from '@playwright/test';
test.describe('Quy chế — config per-company', () => {
  test('2 field chết không hiển thị', async ({ page }) => {
    await page.goto('/…/regulation-config', { waitUntil: 'domcontentloaded' });
    await expect(page.getByText('Điều khoản báo giá mặc định')).toHaveCount(0);
    await expect(page.getByText('Hệ số giá vốn dịch vụ')).toHaveCount(0);
  });
  test('đổi cấu hình công ty A không đổi công ty B', async ({ page }) => {
    // chọn công ty A ở khung "Theo công ty", set quotation_valid_days, Lưu (áp ngay)
    // chọn công ty B, xác nhận giá trị KHÁC (không bị đổi theo A)
  });
});
```

- [ ] **Step 2: Chạy → FAIL/đỏ hợp lý trước khi có Task 20-21** (nếu chạy tách). Sau khi Task 20-21 xong → chạy PASS.

Run: `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test per-company.spec.ts`
(Cần FE `:3000` + API `:8000` đang chạy; token `.auth/user.json` còn hạn — làm mới bằng `--project=setup`.)

- [ ] **Step 3: Chạy full → PASS**

Run: như trên → 2 test xanh. Lỗi selector → `npm run codegen` dò lại (theo skill `playwright-setup`).

- [ ] **Step 4: Commit**

```bash
cd HRM/e2e
git add tests/regulation-config/per-company.spec.ts pages/RegulationConfigPage.ts
git commit -m "test(gopdb): e2e config per-company + ẩn 2 field chết (G2)"
```

---

## Self-Review G2 (rà sau khi viết plan)

**1. Spec coverage** (đối chiếu spec 2026-09-24 mục 4-7):
- 4.2 migration company_id + clone all companies + clone contract_rows → Task 14 ✓
- 5.1 getConfig + resolveCompanyId → Task 15 ✓ · 5.2 (4 điểm first()) → Task 16 ✓ · 5.3 (3 kênh share) → tự đúng, không cần task (đã ghi trong spec) ✓ · 5.4 (2 console command) → Task 18 ✓
- 6 ConfigsController per-company + guard + chỉ báo → Task 17 ✓
- 7.2 (đọc/ghi/version 17 field) → Task 19 (đọc) + Task 20 (ghi/version) ✓ · 7.4 (ẩn 2 field) → Task 21 ✓ · 7.5 (lịch sử company) → Task 20 Step 3d/3e ✓
- Kiểm per-company + ẩn field → Task 22 ✓

**2. Placeholder scan:** không còn "TBD/TODO"; các "xác minh khi viết plan" của spec đã chuyển thành Step grep/đọc-cụ-thể trong Task 16/17/18/20. Sạch.

**3. Type consistency:** `createGlobalVersion(int $companyId, ...)` — chữ ký mới thêm tham số đầu, đã cập nhật 2 caller (Task 20 3b) + docblock. `scope_id` config = companyId nhất quán giữa createGlobalVersion / scopeSpecsForTab / applyVersion / getHistory / recomputeDiffChain / applyDueVersions. `getConfig($column=null, $companyId=null)` tương thích ngược. Nhất quán.

**4. Điểm mở đã nêu để user chốt:** flip tab `chung` (logo/header) per-company — hệ quả bắt buộc của schema, cần xác nhận trước Task 20 (đã ghi ⚠️ đầu G2).

---

### Checkpoint — 2026-09-24
Vừa hoàn thành: viết xong plan G2 (Task 14-22) append vào plan.md; đã grep xác minh cơ chế thật của `RegulationConfigService` (store per-field trong registry; config-store dùng scope_type=global làm bộ chọn store).
Đang làm dở: chưa thực thi task nào — chờ user duyệt plan + chốt điểm mở (flip tab `chung`) + chọn chế độ execution (subagent-driven vs inline).
Bước tiếp theo: user review plan → chốt flip `chung` → chọn execution mode → bắt đầu Task 14.
Blocked: (để trống)
