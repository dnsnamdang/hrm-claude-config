# Phase 1 — Chuyển 11 danh mục liên quan hàng hoá sang HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended)
> or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Dựng 11 màn danh mục bên HRM trên đúng 11 bảng ERP đang chạy, để màn Hàng hoá (Phase 2)
có đủ danh mục phụ thuộc.

**Architecture:** Mở rộng nền `BaseCatalog*` mà Phase 0 (#11421) đã dựng cho 6 danh mục phân loại,
thay vì dựng nền thứ hai. Nền đang chặn cứng trạng thái 1/2 và cột `code` bắt buộc — 11 bảng ERP
dùng trạng thái 0/1 và 7/11 bảng không có `code`. Sau khi nới 11 chỗ, mỗi màn chỉ còn 5 file mỏng
(Entity / Service / Controller / Request / Resource) + 1 thư mục FE.

**Tech Stack:** BE Laravel 8 + PHP 7.4, `nwidart/laravel-modules`, `spatie/laravel-permission`
(guard `api`), `maatwebsite/excel`. FE Nuxt 2.14 + Vue 2 + Bootstrap-Vue. DB MySQL `hrm_erp` (DB gộp).

**Spec:** `docs/superpowers/specs/gop-db/2026-09-20-chuyen-danh-muc-lien-quan-design.md`

## Global Constraints

- Nhánh **`gop_db`** ở cả 2 repo. KHÔNG checkout từ `tpe` / `main`. Merge trả về `gop_db`.
- **KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`** — trỏ DB ERP CŨ, id lệch.
- **Không migration bảng mới.** 11 bảng đã tồn tại và ERP đang ghi vào chúng.
- **Trạng thái 11 bảng này là `1 = Hoạt động`, `0 = Khóa`** — KHÁC chuẩn HRM (1/2). Không đổi số
  trong DB. Mọi Entity của Phase 1 khai `const STATUS_INACTIVE = 0;`.
- **Không đụng repo ERP** (`ERP/TanPhatDev`) một dòng nào.
- **Không đổi tên / không xoá** 11 bộ quyền guard `web` của ERP — nhóm "Hàng hoá có sẵn" đang dùng chung.
- **KHÔNG chạy `PermissionsTableSeeder`** trên DB local: nó `truncate` cả bảng `permissions`
  (đang có 1.722 dòng). Sửa file seeder cho môi trường khác, còn local thì chèn tay.
- Model mới `extends BaseModel` (hoặc `BaseCatalogModel` kế thừa nó). Lấy `auth()->id()`,
  **TUYỆT ĐỐI không** `auth()->user()->info->id`.
- Ô rỗng để **trống hẳn**, không chèn `—` / `-` / `N/A`.
- Số và tiền theo chuẩn quốc tế `1,234,567.89`. Ngày `dd/mm/yyyy`, ngày+giờ `dd/mm/yyyy HH:mm`,
  **BE trả sẵn chuỗi**, FE không format lại.
- Chữ trong ô để **thường**, kể cả cột Mã — không `font-weight-bold`.
- Nút không dùng được thì **ẩn hẳn** bằng `visible`/`v-if`, KHÔNG hiện xám.
- `V2BaseRowActions` emit **chuỗi key** → handler phải `switch (action)`. So `action.key` là nút
  chết im ru, không lỗi console.
- Repo trộn CRLF/LF: sửa hàng loạt phải kiểm `git diff --numstat` ra **0 dòng xoá** ngoài ý muốn.
- **Không tự chạy e2e** — chỉ chạy khi user yêu cầu. Vẫn phải kiểm bằng Playwright MCP.

## Môi trường — đã chuẩn bị sẵn 20/09/2026

Ba việc dưới đây **đã làm rồi**, executor không phải làm lại, nhưng phải biết để hiểu bối cảnh:

1. Chạy chọn lọc 12 migration của `Modules/MasterData`
   (`php artisan migrate --path=Modules/MasterData/Database/Migrations --force`) → 7 bảng Phase 0
   (`product_natures`, `product_function_groups`, `product_families`, `product_types`,
   `business_policies`, `product_characteristics`, `product_type_attributes`) nay đã tồn tại trên
   DB local. **Còn 61 migration khác vẫn pending — CỐ Ý không chạy** (trong đó có
   `drop_hrm_customer_tables` và 3 migration `backfill_created_by...`).
2. Chèn tay 12 quyền Phase 0 (id 1574-1585) vào bảng `permissions` (1.710 → 1.722).
3. `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php`
   → **OK (11 tests, 21 assertions)**. Đây là **mốc gốc**: sau mỗi lần đụng nền phải ra đúng con số này.

Lệnh PHP của máy này: `/opt/homebrew/opt/php@7.4/bin/php` (cảnh báo `imagick.so` khi khởi động là
bình thường, bỏ qua).

## File Structure

### Backend — `hrm-api`

**Sửa (nền dùng chung, đang phục vụ 6 màn Phase 0):**

| File | Trách nhiệm | Sửa gì |
|---|---|---|
| `Modules/MasterData/Entities/ProductClassification/BaseCatalogModel.php` | trạng thái, audit, điều kiện sửa/xoá/khoá | 3 dòng `self::` → `static::` |
| `Modules/MasterData/Http/Controllers/V1/ProductClassification/BaseCatalogController.php` | CRUD + lock/unlock + import/export | 2 dòng `BaseCatalogModel::STATUS_*` → `$catalog::STATUS_*` |
| `Modules/MasterData/Services/ProductClassification/Concerns/ImportsCatalogRows.php` | soát & ghi dòng import | 1 dòng như trên |
| `Modules/MasterData/Services/ProductClassification/BaseCatalogService.php` | lọc, sort, CRUD, ghi log | thêm hook `hasCodeField()`; bọc 3 chỗ dùng cột `code`; `catalogDisplay()` lấy hằng theo model |
| `Modules/MasterData/Http/Requests/ProductClassification/BaseCatalogRequest.php` | rule chung | thêm hook `hasCodeField()` + `statusRule()` |
| `app/Services/CatalogHistoryService.php` | registry bảng có lịch sử (64 bảng) | +11 mục |
| `app/ExcelExport/ExportColumnRegistry.php` | registry cột xuất file (63 màn) | +11 mục |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | nguồn quyền | +22 dòng (id 1590-1611) |
| `Modules/MasterData/Routes/api.php` | khai route | +1 vòng lặp 11 slug |

**Tạo mới — mỗi màn 5 file trong `Modules/MasterData/`:**

```
Entities/ProductCatalog/<Tên>.php                    # $table, hằng trạng thái 0/1, quan hệ riêng
Services/ProductCatalog/<Tên>Service.php             # modelClass, table, cột riêng, lọc riêng
Http/Controllers/V1/ProductCatalog/<Tên>Controller.php   # resource, nhãn, tên file xuất, action type-hint
Http/Requests/ProductCatalog/<Tên>Request.php        # rule riêng
Transformers/ProductCatalog/<Tên>Resource.php        # trường riêng
```

`<Tên>` lần lượt: `Origin` · `AttributeUnit` · `ProductModel` · `Unit` · `ProductAttribute` ·
`Brand` · `Manufacturer` · `OrderCode` · `AttachmentType` · `ColorCode` · `TaxRate`.

⚠️ Tên lớp **`ProductAttribute`** chứ không phải `Attribute` — `Attribute` đụng
`$model->attributes` nội bộ của Eloquent (bẫy Phase 0 đã dính, xem checkpoint `plan.md` của họ).
Tương tự **`AttributeUnit`** cho bảng `unitteches`.

### Frontend — `hrm-client`

```
pages/master-data/<slug>/index.vue           # danh sách
pages/master-data/<slug>/Add<Tên>Modal.vue   # modal thêm/sửa
components/subsystem-menu/master-data.js     # SỬA: tách nhóm "Hàng hóa" thành 2 nhóm
```

`<slug>`: `origins` · `attribute-units` · `product-models` · `units` · `attributes` · `brands` ·
`manufacturers` · `order-codes` · `attachment-types` · `color-codes` · `tax-rates`.

### Khuôn để copy

- Màn danh mục **đơn giản nhất** (chỉ code/name/description/status):
  `hrm-client/pages/master-data/business-policies/` — `index.vue` 834 dòng + modal 298 dòng.
- Màn có **cấp cha** (select cha): `hrm-client/pages/master-data/product-function-groups/`.
- ⚠️ Skill `erp-to-hrm-screen` cảnh báo copy màn đã port là nhân bản luôn cái sai. Task 4 **chạy
  checklist cho màn nguồn `business-policies` trước** rồi mới lấy nó làm khuôn cho 10 màn sau.

---

# ĐỢT 1 — Nền + 3 màn đơn giản nhất

Đợt này là **chốt chặn**: chứng minh nền mở rộng chạy được mà không làm vỡ 6 màn Phase 0, trước khi
nhân ra 8 màn còn lại.

### Task 1: Mở rộng nền `BaseCatalog*` + Entity/Service Xuất xứ

**Files:**
- Create: `Modules/MasterData/Entities/ProductCatalog/Origin.php`
- Create: `Modules/MasterData/Services/ProductCatalog/OriginService.php`
- Modify: `Modules/MasterData/Entities/ProductClassification/BaseCatalogModel.php:51,56,113`
- Modify: `Modules/MasterData/Services/ProductClassification/BaseCatalogService.php:44-52,86,121,173-180`
- Modify: `Modules/MasterData/Http/Requests/ProductClassification/BaseCatalogRequest.php:57-79`
- Modify: `Modules/MasterData/Http/Controllers/V1/ProductClassification/BaseCatalogController.php:137,157`
- Modify: `Modules/MasterData/Services/ProductClassification/Concerns/ImportsCatalogRows.php:183`
- Test: `Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php`

**Interfaces:**
- Consumes: `BaseCatalogModel`, `BaseCatalogService`, `BaseCatalogRequest` của Phase 0 (#11421).
- Produces:
  - `BaseCatalogService::hasCodeField(): bool` — mặc định `true`; lớp con của bảng không có cột
    `code` trả `false`.
  - `BaseCatalogRequest::hasCodeField(): bool` — như trên.
  - `BaseCatalogRequest::statusRule(): array` — mặc định `['nullable', 'in:1,2']`; lớp con của bảng
    ERP trả `['nullable', 'in:0,1']`.
  - `Modules\MasterData\Entities\ProductCatalog\Origin` — `const STATUS_ACTIVE = 1`,
    `const STATUS_INACTIVE = 0`, `$table = 'origins'`.
  - `Modules\MasterData\Services\ProductCatalog\OriginService` — `index(Request): Builder`,
    `getAll(Request)`, `store(Request)`, `update(Request, $catalog)`, `destroy($catalog)`
    (kế thừa `BaseCatalogService`).

- [ ] **Bước 1: Ghi lại mốc gốc — bộ test Phase 0 phải đang xanh**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php 2>&1 | tail -4
```

Mong đợi: `OK (11 tests, 21 assertions)`. Nếu KHÔNG ra con số này thì **dừng lại** — môi trường
chưa đúng, đừng sửa nền khi chưa có mốc so.

- [ ] **Bước 2: Viết Entity `Origin`**

Tạo `Modules/MasterData/Entities/ProductCatalog/Origin.php`:

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Xuất xứ — bảng ERP `origins` (113 dòng), ERP VẪN đang đọc/ghi cùng bảng.
 *
 * Trạng thái theo quy ước ERP: 1 = Hoạt động, 0 = Khóa.
 * KHÁC chuẩn HRM (1 / 2) — cố ý: đổi số trong DB là đụng ERP đang chạy.
 * Bảng KHÔNG có cột `code` và KHÔNG có cột `description`.
 */
class Origin extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'origins';

    protected $fillable = [
        'name',
        'position',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];
}
```

- [ ] **Bước 3: Viết `OriginService`**

Tạo `Modules/MasterData/Services/ProductCatalog/OriginService.php`:

```php
<?php

namespace Modules\MasterData\Services\ProductCatalog;

use Illuminate\Http\Request;
use Modules\MasterData\Entities\ProductCatalog\Origin;
use Modules\MasterData\Services\ProductClassification\BaseCatalogService;

/** Danh mục Xuất xứ — bảng ERP `origins`. */
class OriginService extends BaseCatalogService
{
    protected function modelClass(): string
    {
        return Origin::class;
    }

    protected function table(): string
    {
        return 'origins';
    }

    /** `origins` không có cột `code` */
    protected function hasCodeField(): bool
    {
        return false;
    }

    protected function fillableFrom(Request $request): array
    {
        return [
            'name' => trim((string) $request->name),
            'position' => $request->position,
            'status' => $request->status ?? Origin::STATUS_ACTIVE,
        ];
    }

    protected function sortableColumns(): array
    {
        return [
            'name' => 'origins.name',
            'position' => 'origins.position',
            'status' => 'origins.status',
            'created_at' => 'origins.created_at',
            'createdAt' => 'origins.created_at',
            'updated_at' => 'origins.updated_at',
            'updatedAt' => 'origins.updated_at',
        ];
    }

    protected function catalogColumns(): array
    {
        return ['name', 'position', 'status'];
    }
}
```

- [ ] **Bước 4: Viết bộ test — sẽ ĐỎ**

Tạo `Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php`:

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Http\Request;
use Modules\MasterData\Entities\ProductCatalog\Origin;
use Modules\MasterData\Services\ProductCatalog\OriginService;
use Tests\TestCase;

/**
 * Nền dùng chung khi danh mục nằm trên BẢNG ERP (trạng thái 0/1, có thể không có cột `code`).
 *
 * Test chạy trên DB dev có dữ liệu thật — mọi bản ghi tạo ra đều mang TEST_TOKEN và
 * bị xoá ở tearDown. Không đụng 113 dòng `origins` có sẵn.
 */
class ProductCatalogBaseTest extends TestCase
{
    private const TEST_TOKEN = 'ZZPC1TEST';

    protected function tearDown(): void
    {
        Origin::where('name', 'like', '%' . self::TEST_TOKEN . '%')->forceDelete();

        parent::tearDown();
    }

    private function makeOrigin(array $attrs = []): Origin
    {
        return Origin::create(array_merge([
            'name' => self::TEST_TOKEN . ' ' . uniqid(),
            'status' => Origin::STATUS_ACTIVE,
            'created_by' => 1,
            'updated_by' => 1,
        ], $attrs));
    }

    /** @test */
    public function trang_thai_khoa_cua_bang_erp_la_so_0()
    {
        $locked = $this->makeOrigin(['status' => Origin::STATUS_INACTIVE]);

        $this->assertSame(0, (int) $locked->status);
        $this->assertFalse($locked->isActive());
        $this->assertSame('Khóa', $locked->status_name);
    }

    /** @test */
    public function scope_active_loai_ban_ghi_status_0()
    {
        $active = $this->makeOrigin();
        $locked = $this->makeOrigin(['status' => Origin::STATUS_INACTIVE]);

        $ids = Origin::query()->active()
            ->where('name', 'like', '%' . self::TEST_TOKEN . '%')
            ->pluck('id')->all();

        $this->assertContains($active->id, $ids);
        $this->assertNotContains($locked->id, $ids);
    }

    /** @test */
    public function tim_nhanh_khong_no_tren_bang_khong_co_cot_code()
    {
        $origin = $this->makeOrigin();

        $rows = app(OriginService::class)
            ->index(new Request(['keyword' => self::TEST_TOKEN]))
            ->get();

        $this->assertTrue($rows->contains('id', $origin->id));
    }

    /** @test */
    public function ghi_va_doc_lai_khong_dung_toi_cot_code()
    {
        $origin = app(OriginService::class)->store(new Request([
            'name' => self::TEST_TOKEN . ' ghi thu',
            'position' => 7,
        ]));

        $this->assertSame(7, (int) $origin->position);
        $this->assertSame(1, (int) $origin->status);
    }
}
```

- [ ] **Bước 5: Chạy test, xác nhận ĐỎ đúng lý do**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php 2>&1 | tail -25
```

Mong đợi: đỏ. Ít nhất 2 kiểu lỗi phải thấy:
- `SQLSTATE[42S22]: Unknown column 'origins.code'` ở ca `tim_nhanh_...` và `ghi_va_doc_lai_...`
- ca `scope_active_...` sai vì `scopeActive()` vẫn so với hằng của lớp nền

Nếu đỏ vì lý do KHÁC (thiếu class, sai namespace) thì sửa cho đúng lý do trên rồi mới đi tiếp.

- [ ] **Bước 6: Sửa `BaseCatalogModel` — 3 dòng**

```bash
cd hrm-api
sed -i '' \
  -e "51s/self::STATUS_ACTIVE/static::STATUS_ACTIVE/" \
  -e "56s/self::STATUS_ACTIVE/static::STATUS_ACTIVE/" \
  -e "113s/self::STATUS_ACTIVE/static::STATUS_ACTIVE/" \
  Modules/MasterData/Entities/ProductClassification/BaseCatalogModel.php

grep -n 'self::STATUS\|static::STATUS' Modules/MasterData/Entities/ProductClassification/BaseCatalogModel.php
```

Mong đợi: 3 dòng đều là `static::STATUS_ACTIVE`, không còn `self::STATUS`.

Thêm ghi chú ngay dưới 2 hằng ở đầu class (dòng 17-18):

```php
    // `static::` chứ KHÔNG phải `self::` ở mọi chỗ đọc 2 hằng này — lớp con của bảng ERP
    // (`Modules\MasterData\Entities\ProductCatalog\*`) khai lại STATUS_INACTIVE = 0.
    // `self::` neo về class ĐỊNH NGHĨA nên ghi đè sẽ vô tác dụng, sai lặng lẽ.
    const STATUS_ACTIVE = 1;    // Hoạt động
    const STATUS_INACTIVE = 2;  // Khóa
```

- [ ] **Bước 7: Sửa `BaseCatalogService` — thêm hook + bọc 3 chỗ dùng `code` + sửa `catalogDisplay`**

Thêm hook ngay trên `fillableFrom()`:

```php
    /**
     * Bảng danh mục có cột `code` không.
     * Nhóm danh mục trên BẢNG ERP phần lớn KHÔNG có (7/11 bảng) — lớp con trả `false`.
     */
    protected function hasCodeField(): bool
    {
        return true;
    }
```

Thay `fillableFrom()`:

```php
    protected function fillableFrom(Request $request): array
    {
        $data = [
            'name' => trim((string) $request->name),
            'description' => $request->description,
            'status' => $request->status ?? 1,
        ];

        if ($this->hasCodeField()) {
            $data['code'] = strtoupper(trim((string) $request->code));
        }

        return $data;
    }
```

Bọc bộ lọc `code` trong `index()`:

```php
        if ($this->hasCodeField() && $request->filled('code')) {
```

Bọc `orWhere` trong khối `keyword` (đây là chỗ nổ SQL nặng nhất):

```php
                $query->where(function ($q) use ($escaped, $t) {
                    $q->where("$t.name", 'like', '%' . $escaped . '%');

                    // Bảng ERP phần lớn không có cột `code` — thêm vô điều kiện là
                    // SQLSTATE[42S22] ngay lần gõ ô tìm nhanh đầu tiên.
                    if ($this->hasCodeField()) {
                        $q->orWhere("$t.code", 'like', '%' . $escaped . '%');
                    }

                    // Tìm theo người tạo bằng EXISTS thay vì join (giữ câu COUNT gọn)
                    $q->orWhereRaw(
                        'exists (select 1 from employees e'
                        . ' join employee_infos ei on ei.id = e.employee_info_id'
                        . " where e.id = $t.created_by and ei.fullname like ?)",
                        ['%' . $escaped . '%']
                    );
                });
```

Sửa `catalogDisplay()`:

```php
    /** Đưa về GIÁ TRỊ HIỂN THỊ để log tự chứa (đổi danh mục sau này không làm sai log cũ). */
    protected function catalogDisplay(string $column, $value)
    {
        if ($column === 'status') {
            // Lấy hằng theo ĐÚNG model của màn: bảng mới dùng 2 = Khóa, bảng ERP dùng 0 = Khóa.
            // Hard-code '2' làm bản ghi ERP bị khóa ghi vào lịch sử là "Hoạt động" — sai lặng lẽ.
            $model = $this->modelClass();

            return (int) $value === (int) $model::STATUS_INACTIVE ? 'Khóa' : 'Hoạt động';
        }

        return $value;
    }
```

- [ ] **Bước 8: Sửa `BaseCatalogRequest` — thêm 2 hook, bọc rule `code`**

Thêm 2 hook ngay trên `ownRules()`:

```php
    /** Bảng có cột `code` không — lớp con của bảng ERP không có thì trả `false` */
    protected function hasCodeField(): bool
    {
        return true;
    }

    /** Rule trạng thái — bảng ERP dùng 0/1 nên lớp con trả `['nullable', 'in:0,1']` */
    protected function statusRule(): array
    {
        return ['nullable', 'in:1,2'];
    }
```

Thay `rules()`:

```php
    public function rules()
    {
        $id = $this->currentId();

        $rules = [
            'name' => [
                'required',
                'max:255',
                'unique:' . $this->table() . ',name,' . $id,
                'not_regex:/[,:]/',
            ],
            'description' => ['nullable', 'max:500'],
            'status' => $this->statusRule(),
        ];

        if ($this->hasCodeField()) {
            $prefixLength = strlen($this->codePrefix());

            $rules['code'] = [
                'required',
                // <PREFIX> + đúng 4 ký tự
                'size:' . ($prefixLength + 4),
                'regex:/^' . preg_quote(rtrim($this->codePrefix(), '.'), '/') . '\.[a-zA-Z0-9_]{4}$/',
                'unique:' . $this->table() . ',code,' . $id,
            ];
        }

        return array_merge($rules, $this->ownRules());
    }
```

- [ ] **Bước 9: Sửa `BaseCatalogController` — 2 dòng**

Dòng 137: `$catalog->status = BaseCatalogModel::STATUS_INACTIVE;`
→ `$catalog->status = $catalog::STATUS_INACTIVE;`

Dòng 157: `$catalog->status = BaseCatalogModel::STATUS_ACTIVE;`
→ `$catalog->status = $catalog::STATUS_ACTIVE;`

```bash
cd hrm-api
grep -n 'BaseCatalogModel::STATUS' \
  Modules/MasterData/Http/Controllers/V1/ProductClassification/BaseCatalogController.php
```

Mong đợi sau khi sửa: **không còn dòng nào**. Nếu `use Modules\...\BaseCatalogModel;` thành thừa
thì gỡ luôn dòng `use`.

- [ ] **Bước 10: Sửa `ImportsCatalogRows` — 1 dòng**

Dòng 183: `BaseCatalogModel::STATUS_INACTIVE` → lấy theo model của service.
Đọc quanh dòng đó để biết biến model đang tên gì rồi thay bằng `<biến>::STATUS_INACTIVE`;
nếu không có sẵn biến thì dùng `$this->modelClass()::STATUS_INACTIVE`.

```bash
cd hrm-api
sed -n '175,190p' Modules/MasterData/Services/ProductClassification/Concerns/ImportsCatalogRows.php
grep -rn 'BaseCatalogModel::STATUS' Modules/MasterData/
```

Mong đợi sau khi sửa: `grep` ra rỗng trên toàn `Modules/MasterData/`.

- [ ] **Bước 11: Chạy test mới — phải XANH**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php 2>&1 | tail -5
```

Mong đợi: `OK (4 tests, ...)`.

- [ ] **Bước 12: Chạy lại bộ test Phase 0 — PHẢI y hệt mốc gốc**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php 2>&1 | tail -5
```

Mong đợi: `OK (11 tests, 21 assertions)` — **đúng con số ở Bước 1**. Lệch một ca là nền đã làm vỡ
màn của @junfoke → sửa xong mới đi tiếp, không được để nợ.

- [ ] **Bước 13: Xác nhận `origins` không bị bẩn sau test**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "origins: ".DB::table("origins")->count()." (mong đợi 113)\n";
echo "rác test còn lại: ".DB::table("origins")->where("name","like","%ZZPC1TEST%")->count()." (mong đợi 0)\n";' 2>/dev/null | grep -v Warning
```

- [ ] **Bước 14: Commit**

```bash
cd hrm-api
git add Modules/MasterData/Entities/ProductCatalog/Origin.php \
        Modules/MasterData/Services/ProductCatalog/OriginService.php \
        Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php \
        Modules/MasterData/Entities/ProductClassification/BaseCatalogModel.php \
        Modules/MasterData/Services/ProductClassification/BaseCatalogService.php \
        Modules/MasterData/Services/ProductClassification/Concerns/ImportsCatalogRows.php \
        Modules/MasterData/Http/Requests/ProductClassification/BaseCatalogRequest.php \
        Modules/MasterData/Http/Controllers/V1/ProductClassification/BaseCatalogController.php
git commit -m "[gop_db] Danh mục hàng hoá P1: nới nền BaseCatalog cho bảng ERP (trạng thái 0/1, không cột code)"
```

---

### Task 2: 22 quyền mới

**Files:**
- Modify: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (thêm sau dòng 1496)

**Interfaces:**
- Produces: 22 quyền guard `api`, id **1590-1611**, `group = 'Danh mục hàng hóa'`, `type = 9`.
  Tên quyền là khoá mà route và menu FE tra theo — xem bảng dưới, **chép đúng từng chữ**.

- [ ] **Bước 1: Đo lại id lớn nhất guard `api` NGAY TRƯỚC KHI viết**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "max id guard api: ".DB::table("permissions")->where("guard_name","api")->max("id")."\n";
echo "1590-1611 đã ai dùng chưa: ".DB::table("permissions")->whereBetween("id",[1590,1611])->count()." (mong đợi 0)\n";' 2>/dev/null | grep -v Warning
```

Mong đợi: max = **1589**, và 0 bản ghi trong khoảng 1590-1611. Nếu khác (nhánh khác vừa merge vào
đã lấy mất dải này) thì **dịch cả 22 id lên sau id lớn nhất mới** và sửa luôn bảng dưới.
Đây là lỗi đã dính thật khi merge nhánh dài — git không báo xung đột vì khác dòng.

- [ ] **Bước 2: Thêm 22 dòng vào `PermissionsTableSeeder.php`**

Chèn ngay sau dòng 1496 (kết thúc khối 12 quyền Phase 0):

```php

        // 11 danh mục hàng hóa chuyển từ ERP sang (Phase 1 của feature quan-ly-hang-hoa).
        // Cùng group 'Danh mục hàng hóa' với 12 quyền Phase 0 ở trên.
        // ⚠️ Tên KHÁC quyền ERP guard 'web' (`Xem model`, `Thêm model`…) — CỐ Ý, vì nhóm màn
        // "Hàng hóa có sẵn" (`pi-*`) vẫn chạy bên ERP và đang dùng chung bộ quyền đó.
        Permission::create(['id' => 1590, 'guard_name' => 'api', 'name' => 'Xem danh mục model', 'display_name' => 'Xem danh mục model', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1591, 'guard_name' => 'api', 'name' => 'Quản lý danh mục model', 'display_name' => 'Quản lý danh mục model', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1592, 'guard_name' => 'api', 'name' => 'Xem danh mục code đặt hàng', 'display_name' => 'Xem danh mục code đặt hàng', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1593, 'guard_name' => 'api', 'name' => 'Quản lý danh mục code đặt hàng', 'display_name' => 'Quản lý danh mục code đặt hàng', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1594, 'guard_name' => 'api', 'name' => 'Xem danh mục đơn vị tính', 'display_name' => 'Xem danh mục đơn vị tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1595, 'guard_name' => 'api', 'name' => 'Quản lý danh mục đơn vị tính', 'display_name' => 'Quản lý danh mục đơn vị tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1596, 'guard_name' => 'api', 'name' => 'Xem danh mục thuộc tính', 'display_name' => 'Xem danh mục thuộc tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1597, 'guard_name' => 'api', 'name' => 'Quản lý danh mục thuộc tính', 'display_name' => 'Quản lý danh mục thuộc tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1598, 'guard_name' => 'api', 'name' => 'Xem danh mục đơn vị thuộc tính', 'display_name' => 'Xem danh mục đơn vị thuộc tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1599, 'guard_name' => 'api', 'name' => 'Quản lý danh mục đơn vị thuộc tính', 'display_name' => 'Quản lý danh mục đơn vị thuộc tính', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1600, 'guard_name' => 'api', 'name' => 'Xem danh mục thương hiệu', 'display_name' => 'Xem danh mục thương hiệu', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1601, 'guard_name' => 'api', 'name' => 'Quản lý danh mục thương hiệu', 'display_name' => 'Quản lý danh mục thương hiệu', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1602, 'guard_name' => 'api', 'name' => 'Xem danh mục hãng sản xuất', 'display_name' => 'Xem danh mục hãng sản xuất', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1603, 'guard_name' => 'api', 'name' => 'Quản lý danh mục hãng sản xuất', 'display_name' => 'Quản lý danh mục hãng sản xuất', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1604, 'guard_name' => 'api', 'name' => 'Xem danh mục xuất xứ', 'display_name' => 'Xem danh mục xuất xứ', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1605, 'guard_name' => 'api', 'name' => 'Quản lý danh mục xuất xứ', 'display_name' => 'Quản lý danh mục xuất xứ', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1606, 'guard_name' => 'api', 'name' => 'Xem danh mục file đính kèm', 'display_name' => 'Xem danh mục file đính kèm', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1607, 'guard_name' => 'api', 'name' => 'Quản lý danh mục file đính kèm', 'display_name' => 'Quản lý danh mục file đính kèm', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1608, 'guard_name' => 'api', 'name' => 'Xem danh mục mã màu', 'display_name' => 'Xem danh mục mã màu', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1609, 'guard_name' => 'api', 'name' => 'Quản lý danh mục mã màu', 'display_name' => 'Quản lý danh mục mã màu', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1610, 'guard_name' => 'api', 'name' => 'Xem danh mục thuế suất', 'display_name' => 'Xem danh mục thuế suất', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1611, 'guard_name' => 'api', 'name' => 'Quản lý danh mục thuế suất', 'display_name' => 'Quản lý danh mục thuế suất', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
```

- [ ] **Bước 3: Kiểm không trùng id và không trùng tên trong chính file seeder**

```bash
cd hrm-api
grep -oE "'id' => [0-9]+" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | sort | uniq -d
```

Mong đợi: **rỗng**. Có dòng nào in ra là id trùng — seeder sẽ nổ khoá chính khi chạy trên DB sạch.

```bash
grep -oE "'name' => '[^']+'" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | sort | uniq -d
```

Mong đợi: có thể ra vài dòng của quyền cũ trùng tên khác guard — **chỉ cần chắc 22 tên mới của
Phase 1 KHÔNG nằm trong danh sách đó**.

- [ ] **Bước 4: Chèn 22 quyền vào DB local — KHÔNG chạy seeder**

```bash
cd hrm-api
cat > /tmp/p1_perm.php <<'PHP'
<?php
$names = [
  1590 => 'Xem danh mục model',                       1591 => 'Quản lý danh mục model',
  1592 => 'Xem danh mục code đặt hàng',               1593 => 'Quản lý danh mục code đặt hàng',
  1594 => 'Xem danh mục đơn vị tính',                 1595 => 'Quản lý danh mục đơn vị tính',
  1596 => 'Xem danh mục thuộc tính',                  1597 => 'Quản lý danh mục thuộc tính',
  1598 => 'Xem danh mục đơn vị thuộc tính',           1599 => 'Quản lý danh mục đơn vị thuộc tính',
  1600 => 'Xem danh mục thương hiệu',                 1601 => 'Quản lý danh mục thương hiệu',
  1602 => 'Xem danh mục hãng sản xuất',               1603 => 'Quản lý danh mục hãng sản xuất',
  1604 => 'Xem danh mục xuất xứ',                     1605 => 'Quản lý danh mục xuất xứ',
  1606 => 'Xem danh mục file đính kèm',               1607 => 'Quản lý danh mục file đính kèm',
  1608 => 'Xem danh mục mã màu',                      1609 => 'Quản lý danh mục mã màu',
  1610 => 'Xem danh mục thuế suất',                   1611 => 'Quản lý danh mục thuế suất',
];
$now = now(); $rows = [];
foreach ($names as $id => $n) {
    $rows[] = ['id'=>$id,'guard_name'=>'api','name'=>$n,'display_name'=>$n,
               'group'=>'Danh mục hàng hóa','type'=>9,'created_at'=>$now,'updated_at'=>$now];
}
$exist = DB::table('permissions')->whereIn('id', array_keys($names))->count();
echo "đã có sẵn: $exist\n";
if ($exist === 0) { DB::table('permissions')->insert($rows); echo "ĐÃ CHÈN 22 quyền\n"; }
echo "kiểm 1590-1611: " . DB::table('permissions')->whereBetween('id',[1590,1611])->count() . " / 22\n";
PHP
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute="require '/tmp/p1_perm.php';" 2>/dev/null | grep -v Warning
```

Mong đợi: `kiểm 1590-1611: 22 / 22`.

- [ ] **Bước 5: Cấp 22 quyền cho vai trò đang dùng để kiểm thử + XOÁ CACHE spatie**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan permission:cache-reset
```

⚠️ Spatie cache quyền **24 giờ**. Cấp quyền bằng SQL mà quên xoá cache thì bấm thử ra **403** trong
khi code đúng — đã dính thật.

- [ ] **Bước 6: Commit**

```bash
cd hrm-api
git add Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
git commit -m "[gop_db] Danh mục hàng hoá P1: 22 quyền id 1590-1611"
```

---

### Task 3: Màn Xuất xứ — BE đầy đủ + 2 registry + route

**Files:**
- Create: `Modules/MasterData/Http/Requests/ProductCatalog/OriginRequest.php`
- Create: `Modules/MasterData/Transformers/ProductCatalog/OriginResource.php`
- Create: `Modules/MasterData/Http/Controllers/V1/ProductCatalog/OriginController.php`
- Modify: `Modules/MasterData/Entities/ProductCatalog/Origin.php` (thêm `childrenCount()`)
- Modify: `Modules/MasterData/Routes/api.php` (thêm vòng lặp `$erpCatalogs`)
- Modify: `app/Services/CatalogHistoryService.php` (hằng `TABLES`, +1 mục)
- Modify: `app/ExcelExport/ExportColumnRegistry.php` (+1 mục)
- Test: `Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php` (thêm 2 ca)

**Interfaces:**
- Consumes: `Origin`, `OriginService` (Task 1); 2 quyền `Xem danh mục xuất xứ` /
  `Quản lý danh mục xuất xứ` (Task 2).
- Produces: 10 endpoint dưới prefix `master-data/origins`, và **khuôn 5 file + 3 điểm đăng ký**
  mà 10 màn sau chép theo.

#### Vì sao phải khai `childrenCount()`

Nền `BaseCatalogModel::isCanDelete()` = `isActive() && childrenCount() === 0`, và `childrenCount()`
mặc định trả `0` — tức **cho xoá thoải mái**. Đúng với 6 danh mục Phase 0 (bảng mới, chưa ai dùng),
**sai nguy hiểm** với bảng ERP: `origins` đang bị **45.890 hàng hoá** trỏ vào qua `products.origin_id`.
Xoá là để lại khoá ngoại mồ côi trên dữ liệu thật của ERP.

Với nhóm này, `childrenCount()` = **số bản ghi đang dùng danh mục**. Khi > 0, nền tự chặn và trả
đúng câu QLDA_015 "Không thể xóa do dữ liệu đang được sử dụng." Thao tác thật của người dùng với
master data là **Khoá**, không phải Xoá.

- [ ] **Bước 1: Thêm ca test chặn xoá — sẽ ĐỎ**

Thêm vào `ProductCatalogBaseTest.php`:

```php
    /** @test */
    public function khong_xoa_duoc_xuat_xu_dang_co_hang_hoa_dung()
    {
        // Xuất xứ id 1 là dữ liệu thật, đang có hàng hoá trỏ vào
        $inUse = Origin::query()
            ->whereRaw('exists (select 1 from products p where p.origin_id = origins.id)')
            ->first();

        $this->assertNotNull($inUse, 'DB không có xuất xứ nào đang được dùng — ca test vô nghĩa');
        $this->assertGreaterThan(0, $inUse->childrenCount());
        $this->assertFalse($inUse->isCanDelete());
    }

    /** @test */
    public function xoa_duoc_xuat_xu_chua_ai_dung()
    {
        $fresh = $this->makeOrigin();

        $this->assertSame(0, $fresh->childrenCount());
        $this->assertTrue($fresh->isCanDelete());
    }
```

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php 2>&1 | tail -15
```

Mong đợi: ca `khong_xoa_duoc_...` ĐỎ (`childrenCount()` đang trả 0).

- [ ] **Bước 2: Thêm `childrenCount()` vào `Origin`**

```php
    /**
     * Số hàng hoá đang dùng xuất xứ này. Nền lấy con số này để chặn Xoá (QLDA_015).
     *
     * `products.origin_id` có 45.890 dòng — master data này thực tế KHÔNG bao giờ xoá được,
     * thao tác thật của người dùng là Khoá.
     */
    public function childrenCount(): int
    {
        return DB::table('products')->where('origin_id', $this->id)->count();
    }

    /** Khoá được kể cả khi đang có hàng hoá dùng — chỉ Xoá mới bị chặn */
    public function activeChildrenCount(): int
    {
        return 0;
    }
```

Thêm luôn dòng `use Illuminate\Support\Facades\DB;` vào đầu file `Origin.php` (Task 1 chưa cần
nên chưa khai).

⚠️ `activeChildrenCount()` trả `0` là **cố ý**: nền dùng nó để chặn **Khoá**. Nếu để nó đếm hàng
hoá thì sẽ không khoá được xuất xứ nào — mà khoá chính là thao tác nghiệp vụ chính của màn này.

- [ ] **Bước 3: Chạy lại test — phải XANH**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php 2>&1 | tail -5
```

Mong đợi: `OK (6 tests, ...)`.

- [ ] **Bước 4: Viết `OriginRequest`**

Tạo `Modules/MasterData/Http/Requests/ProductCatalog/OriginRequest.php`:

```php
<?php

namespace Modules\MasterData\Http\Requests\ProductCatalog;

use Modules\MasterData\Http\Requests\ProductClassification\BaseCatalogRequest;

/** Validate danh mục Xuất xứ — bảng ERP `origins`. */
class OriginRequest extends BaseCatalogRequest
{
    protected function table(): string
    {
        return 'origins';
    }

    /** Bảng không có cột `code` */
    protected function hasCodeField(): bool
    {
        return false;
    }

    protected function codePrefix(): string
    {
        return '';
    }

    /** ERP dùng 1 = Hoạt động, 0 = Khóa */
    protected function statusRule(): array
    {
        return ['nullable', 'in:0,1'];
    }

    protected function catalogLabel(): string
    {
        return 'Xuất xứ';
    }

    protected function ownRules(): array
    {
        return [
            'position' => ['nullable', 'integer', 'min:0'],
        ];
    }

    protected function ownMessages(): array
    {
        return [
            'position.integer' => 'Vui lòng nhập số nguyên',
            'position.min' => 'Không được nhỏ hơn 0',
        ];
    }

    public function attributes()
    {
        return parent::attributes() + ['position' => 'Vị trí'];
    }
}
```

- [ ] **Bước 5: Viết `OriginResource`**

Tạo `Modules/MasterData/Transformers/ProductCatalog/OriginResource.php`:

```php
<?php

namespace Modules\MasterData\Transformers\ProductCatalog;

use Modules\MasterData\Transformers\ProductClassification\BaseCatalogResource;

/**
 * Xuất xứ — bảng ERP `origins`.
 *
 * Lớp nền vẫn trả `code` và `description` (đều `null` vì bảng không có 2 cột đó).
 * Vô hại: FE không khai 2 cột này trong bộ cột của màn.
 */
class OriginResource extends BaseCatalogResource
{
    protected function ownFields($request): array
    {
        return [
            'position' => $this->position,
        ];
    }
}
```

- [ ] **Bước 6: Viết `OriginController`**

Tạo `Modules/MasterData/Http/Controllers/V1/ProductCatalog/OriginController.php`:

```php
<?php

namespace Modules\MasterData\Http\Controllers\V1\ProductCatalog;

use Modules\MasterData\Entities\ProductCatalog\Origin;
use Modules\MasterData\Http\Controllers\V1\ProductClassification\BaseCatalogController;
use Modules\MasterData\Http\Requests\ProductCatalog\OriginRequest;
use Modules\MasterData\Services\ProductCatalog\OriginService;
use Modules\MasterData\Transformers\ProductCatalog\OriginResource;

/** Danh mục Xuất xứ — bảng ERP `origins`. */
class OriginController extends BaseCatalogController
{
    public function __construct(OriginService $service)
    {
        $this->service = $service;
    }

    protected function resourceClass(): string
    {
        return OriginResource::class;
    }

    protected function catalogLabel(): string
    {
        return 'xuất xứ';
    }

    protected function exportScreen(): string
    {
        return 'origins';
    }

    protected function exportFileName(): string
    {
        return 'danh_sach_xuat_xu';
    }

    public function show(Origin $catalog)
    {
        return $this->respondShow($catalog);
    }

    public function store(OriginRequest $request)
    {
        return $this->respondStore($request);
    }

    public function update(OriginRequest $request, Origin $catalog)
    {
        return $this->respondUpdate($request, $catalog);
    }

    public function delete(Origin $catalog)
    {
        return $this->respondDelete($catalog);
    }

    public function lock(Origin $catalog)
    {
        return $this->respondLock($catalog);
    }

    public function unlock(Origin $catalog)
    {
        return $this->respondUnlock($catalog);
    }
}
```

- [ ] **Bước 7: Đăng ký lịch sử — `CatalogHistoryService::TABLES`**

Thêm vào cuối hằng `TABLES` trong `app/Services/CatalogHistoryService.php`:

```php
        // ---- 11 danh mục hàng hóa chuyển từ ERP (Phase 1 feature quan-ly-hang-hoa) ----
        // ⚠️ ERP sửa thẳng các bảng này KHÔNG đi qua đây nên KHÔNG ghi log.
        // Lịch sử chỉ phản ánh thao tác làm từ HRM — phải nói rõ với người dùng.
        'origins' => ['label' => 'xuất xứ', 'columns' => [
            'name' => 'Xuất xứ', 'position' => 'Vị trí', 'status' => 'Trạng thái',
        ]],
```

- [ ] **Bước 8: Đăng ký cột xuất file — `ExportColumnRegistry`**

Thêm vào `app/ExcelExport/ExportColumnRegistry.php`:

```php
        // Xuất xứ (/master-data/origins)
        'origins' => [
            'name' => 'Xuất xứ',
            'position' => 'Vị trí',
            'status_text' => 'Trạng thái',
            'creator_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [ ] **Bước 9: Khai route**

Thêm vào `Modules/MasterData/Routes/api.php`, **sau** vòng lặp `$productCatalogs` của Phase 0:

```php
    /*
    | 11 danh mục hàng hóa chuyển từ ERP (Phase 1 của feature quan-ly-hang-hoa).
    |
    | Dùng CHUNG bảng với ERP: trạng thái 0/1, phần lớn KHÔNG có cột `code`.
    |
    | ⚠️ `tax-rates` KHÔNG khai ở vòng lặp này. Route `tax-rates/getAll` đã được Phase 0 đăng ký
    | phía trên cho `CatalogOptionController@taxRates` (nguồn ô chọn %VAT của màn Loại sản phẩm);
    | Laravel lấy route khai TRƯỚC nên khai lại là route chết. Xem Task 14.
    */
    $erpCatalogs = [
        'origins' => ['OriginController', 'xuất xứ'],
    ];

    foreach ($erpCatalogs as $slug => [$controller, $label]) {
        $action = 'V1\ProductCatalog\\' . $controller;
        $viewPermission = 'Xem danh mục ' . $label;
        $managePermission = 'Quản lý danh mục ' . $label;

        Route::group(['prefix' => $slug], function () use ($action, $viewPermission, $managePermission) {
            Route::get('/getAll', $action . '@getAll');
            Route::get('/export', $action . '@export')
                ->middleware('checkPermission:' . $managePermission . '|' . $viewPermission);
            Route::post('/import/validate', $action . '@validateImport')
                ->middleware('checkPermission:' . $managePermission);
            Route::post('/import', $action . '@import')
                ->middleware('checkPermission:' . $managePermission);
            Route::get('/', $action . '@index')
                ->middleware('checkPermission:' . $managePermission . '|' . $viewPermission);
            Route::get('/{catalog}', $action . '@show')
                ->middleware('checkPermission:' . $managePermission . '|' . $viewPermission);
            Route::post('/', $action . '@store')->middleware('checkPermission:' . $managePermission);
            Route::put('/{catalog}', $action . '@update')->middleware('checkPermission:' . $managePermission);
            Route::delete('/{catalog}', $action . '@delete')->middleware('checkPermission:' . $managePermission);
            Route::get('/{catalog}/lock', $action . '@lock')->middleware('checkPermission:' . $managePermission);
            Route::get('/{catalog}/unlock', $action . '@unlock')->middleware('checkPermission:' . $managePermission);
        });
    }
```

- [ ] **Bước 10: Kiểm route khai đúng controller**

`php artisan route:list` của repo này **đang lỗi sẵn** ở `PermissionHelper` — dùng `Route::match`
như Phase 0 đã làm:

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
foreach (Route::getRoutes() as $r) {
    if (strpos($r->uri(), "master-data/origins") !== false) {
        echo str_pad(implode("|", $r->methods()), 12) . str_pad($r->uri(), 46) . $r->getActionName() . "\n";
    }
}' 2>/dev/null | grep -v Warning
```

Mong đợi: **10 dòng**, đều trỏ `...ProductCatalog\OriginController@...`, và `getAll` đứng TRƯỚC
`{catalog}` (nếu không sẽ bị route `/{catalog}` nuốt).

- [ ] **Bước 11: Gọi thật 4 endpoint trên dữ liệu thật**

Chạy API bằng server phụ để không tranh cổng với ai:

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan serve --port=8002 &
```

Lấy token rồi gọi (thay `<TOKEN>`):

```bash
BASE=http://127.0.0.1:8002/api/master-data/origins
curl -s -H "Authorization: Bearer <TOKEN>" "$BASE?per_page=5" | head -c 600; echo
curl -s -H "Authorization: Bearer <TOKEN>" "$BASE?keyword=Nh" | head -c 300; echo
curl -s -H "Authorization: Bearer <TOKEN>" "$BASE?status=0" | head -c 300; echo
curl -s -H "Authorization: Bearer <TOKEN>" "$BASE/getAll" | head -c 300; echo
```

Mong đợi: 4 lần **200**. Đặc biệt `keyword=` phải ra dữ liệu chứ **không** `SQLSTATE[42S22]` —
đây chính là chỗ nền cũ nổ.

- [ ] **Bước 12: Đối chiếu số dòng với SQL**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "tổng: ".DB::table("origins")->count()." (mong đợi 113)\n";
echo "hoạt động: ".DB::table("origins")->where("status",1)->count()." (mong đợi 112)\n";
echo "khóa: ".DB::table("origins")->where("status",0)->count()." (mong đợi 1)\n";' 2>/dev/null | grep -v Warning
```

Con số trên màn danh sách (và bộ lọc Trạng thái) phải khớp từng số.

- [ ] **Bước 13: Commit**

```bash
cd hrm-api
git add Modules/MasterData/Http/Requests/ProductCatalog/OriginRequest.php \
        Modules/MasterData/Transformers/ProductCatalog/OriginResource.php \
        Modules/MasterData/Http/Controllers/V1/ProductCatalog/OriginController.php \
        Modules/MasterData/Entities/ProductCatalog/Origin.php \
        Modules/MasterData/Routes/api.php \
        Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php \
        app/Services/CatalogHistoryService.php \
        app/ExcelExport/ExportColumnRegistry.php
git commit -m "[gop_db] Danh mục hàng hoá P1: API màn Xuất xứ + đăng ký lịch sử/xuất file"
```

---

### Task 4: Màn Xuất xứ — FE + tách menu 2 nhóm

**Files:**
- Create: `hrm-client/pages/master-data/origins/index.vue`
- Create: `hrm-client/pages/master-data/origins/AddOriginModal.vue`
- Modify: `hrm-client/components/subsystem-menu/master-data.js`

**Interfaces:**
- Consumes: 10 endpoint `master-data/origins` (Task 3); 2 quyền (Task 2).
- Produces: thư mục `pages/master-data/origins/` là **khuôn cho 10 màn sau** — Task 5 trở đi copy
  từ đây chứ không copy từ `business-policies`.

- [ ] **Bước 1: Chạy checklist cho MÀN NGUỒN trước khi lấy nó làm khuôn**

Skill `erp-to-hrm-screen` cảnh báo: copy màn đã port là nhân bản luôn cái sai. Soát
`business-policies` trước:

```bash
cd hrm-client
for p in "status-pill\|statusPillClass" "interactable:\|disabledTitle" "action\.key ===" \
         "V2BaseFilterPanel" "advanced-filters" "showCustomerList"; do
  echo "--- $p ---"
  grep -rn "$p" pages/master-data/business-policies/
done
grep -rn "V2BaseSelectRemote" pages/master-data/business-policies/ | grep -v 'height='
```

Mong đợi: **mọi khối đều rỗng**. Có kết quả nào thì sửa `business-policies` trước (báo user vì đó
là màn của @junfoke), hoặc chọn màn nguồn khác.

- [ ] **Bước 2: Copy khuôn**

```bash
cd hrm-client
mkdir -p pages/master-data/origins
cp pages/master-data/business-policies/index.vue pages/master-data/origins/index.vue
cp pages/master-data/business-policies/AddBusinessPolicyModal.vue \
   pages/master-data/origins/AddOriginModal.vue
```

- [ ] **Bước 3: Thay đúng các chỗ sau trong `origins/index.vue`**

| Chỗ | Từ | Thành |
|---|---|---|
| đường dẫn API (4 chỗ: list, export, delete, lock/unlock) | `master-data/business-policies` | `master-data/origins` |
| `localStorageKey` | `master_data_business_policies` | `master_data_origins` |
| `pathsToKeep` | `['/master-data/business-policies']` | `['/master-data/origins']` |
| `columnScreenKey` | `business_policies` | `origins` |
| `importApiPrefix` | `master-data/business-policies` | `master-data/origins` |
| tên component modal | `AddBusinessPolicyModal` | `AddOriginModal` |
| tiêu đề màn (`PageTitleMixin`) | Chính sách kinh doanh | Xuất xứ |
| tên quyền trong `CheckPermission` | `… chính sách kinh doanh` | `… xuất xứ` |
| **`statusOptions`** | `{ id: 1, name: 'Hoạt động' }, { id: 2, name: 'Khóa' }` | `{ id: 1, name: 'Hoạt động' }, { id: 0, name: 'Khóa' }` |
| bộ cột + `exportFields` | `code` / `description` | **bỏ 2 cột đó**, thêm `position` |
| cột làm `<nuxt-link>` | cột `code` | cột **`name`** (bảng không có mã) |

⚠️ **`statusOptions` là chỗ dễ sót nhất.** Để nguyên `id: 2` thì ô lọc "Khóa" gửi `status=2` lên BE,
truy vấn ra **0 dòng** mà không lỗi gì — nhìn y như "không có dữ liệu".

Bộ cột cuối cùng của màn này, đúng thứ tự:

```js
            columns: [
                { id: 'name', name: 'Xuất xứ' },
                { id: 'position', name: 'Vị trí' },
                { id: 'status_text', name: 'Trạng thái' },
                { id: 'creator_name', name: 'Người tạo' },
                { id: 'created_at', name: 'Ngày tạo' },
                { id: 'updater_name', name: 'Người cập nhật' },
                { id: 'updated_at', name: 'Ngày cập nhật' },
            ],
```

- [ ] **Bước 4: Thay trong `AddOriginModal.vue`**

| Chỗ | Từ | Thành |
|---|---|---|
| tên component | `AddBusinessPolicyModal` | `AddOriginModal` |
| đường dẫn API (store / update / show) | `master-data/business-policies` | `master-data/origins` |
| ô nhập | `code` (bắt buộc), `description` | **bỏ cả 2**, thêm `position` (ô số, không bắt buộc) |
| nhãn trường Tên | Chính sách kinh doanh | Xuất xứ |

Chỉ trường **Tên** gắn `required` ở FE; `position` để BE trả 422 nếu sai.

- [ ] **Bước 5: Tách nhóm menu "Hàng hóa" thành 2 nhóm**

Trong `components/subsystem-menu/master-data.js`, nhóm hiện tại nhãn `'Hàng hóa'` (6 mục Phase 0)
→ đổi nhãn thành `'Phân loại hàng hóa'`, giữ nguyên 6 `subItems`. Thêm nhóm mới ngay sau:

```js
    {
        // 11 danh mục hàng hóa chuyển từ ERP (Phase 1 feature quan-ly-hang-hoa).
        // Dùng CHUNG bảng với ERP — màn bên ERP vẫn giữ, sửa ở đâu cũng vào cùng một bảng.
        label: 'Danh mục hàng hóa',
        icon: 'ri-price-tag-3-line',
        isMenuCollapsed: false,
        subItems: [
            {
                label: 'Xuất xứ',
                link: '/master-data/origins',
                isShow: ['Quản lý danh mục xuất xứ', 'Xem danh mục xuất xứ'],
            },
        ],
    },
```

10 mục còn lại thêm dần ở các Task sau, giữ đúng thứ tự: Model · Code đặt hàng · Đơn vị tính ·
Thuộc tính · Đơn vị thuộc tính · Thương hiệu · Hãng sản xuất · Xuất xứ · File đính kèm · Mã màu ·
Thuế suất.

- [ ] **Bước 6: Kiểm bằng Playwright — ĐO SỐ, không chỉ nhìn ảnh**

Mở `/master-data/origins` rồi đo từ DOM:

1. Số dòng trang 1 = **10** (mặc định), tổng = **113** (khớp SQL ở Task 3 Bước 12).
2. Lọc Trạng thái = Khóa → **1 dòng**. Lọc = Hoạt động → **112 dòng**.
   Mở tab Network xem param gửi lên là `status=0`, KHÔNG phải `status=2`.
3. Bấm **từng ô lọc**, đối chiếu param với `BaseCatalogService::index()`.
4. Bấm **từng nút** trong cột Hành động, kể cả nút trong menu `…` — `V2BaseRowActions` emit chuỗi,
   handler phải `switch (action)`.
5. Đo chiều cao mọi ô lọc = **36px** (`getComputedStyle`); lệch 32px là quên truyền `height`.
6. Bấm Xoá một xuất xứ **đang có hàng hoá dùng** → phải ra đúng câu
   "Không thể xóa do dữ liệu đang được sử dụng."
7. Bấm Khoá rồi Mở khoá 1 bản ghi → mở popup Lịch sử, phải thấy 2 dòng nhóm "Thay đổi trạng thái",
   giá trị cũ → mới đúng chiều, và chữ phải là **Khóa/Hoạt động** (không phải số).
8. Vào chi tiết rồi quay lại → **bộ lọc còn nguyên**.

- [ ] **Bước 7: Hoàn nguyên dữ liệu đã đụng khi test**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "origins: ".DB::table("origins")->count()." (mong đợi 113)\n";
echo "hoạt động: ".DB::table("origins")->where("status",1)->count()." (mong đợi 112)\n";' 2>/dev/null | grep -v Warning
```

Bản ghi nào bị khoá khi test thì mở khoá lại.

- [ ] **Bước 8: Chạy khối grep tự kiểm trên thư mục vừa tạo**

```bash
cd hrm-client
for p in "status-pill\|statusPillClass" "interactable:\|disabledTitle" "action\.key ===" \
         "V2BaseFilterPanel" "advanced-filters" "log.action !==" "actionOptions"; do
  echo "--- $p ---"; grep -rn "$p" pages/master-data/origins/
done
```

Mong đợi: mọi khối rỗng.

- [ ] **Bước 9: Commit**

```bash
cd hrm-client
git add pages/master-data/origins components/subsystem-menu/master-data.js
git commit -m "[gop_db] Danh mục hàng hoá P1: màn Xuất xứ + tách menu 2 nhóm"
```

---

## Khuôn chung cho 10 màn còn lại (Task 5 → Task 14)

Từ đây mỗi màn đi đúng 9 bước giống Task 3 + Task 4. Phần **khác nhau giữa các màn** nằm gọn ở
Entity và ở bảng giá trị của từng task. Phần **giống hệt nhau** thì không chép lại — làm theo đúng
file đã viết ở Task 3/4:

| Việc | Làm theo | Thay gì |
|---|---|---|
| `Services/ProductCatalog/<Tên>Service.php` | `OriginService.php` (Task 1 Bước 3) | `modelClass` · `table` · `hasCodeField` · `fillableFrom` · `sortableColumns` · `catalogColumns` |
| `Http/Requests/ProductCatalog/<Tên>Request.php` | `OriginRequest.php` (Task 3 Bước 4) | `table` · `hasCodeField` · `codePrefix` · `statusRule` · `catalogLabel` · `ownRules` · `ownMessages` · `attributes` |
| `Transformers/ProductCatalog/<Tên>Resource.php` | `OriginResource.php` (Task 3 Bước 5) | `ownFields()` |
| `Http/Controllers/V1/ProductCatalog/<Tên>Controller.php` | `OriginController.php` (Task 3 Bước 6) | 4 hàm khai báo + type-hint Entity ở 6 action |
| 1 mục `CatalogHistoryService::TABLES` | Task 3 Bước 7 | `label` + nhãn cột |
| 1 mục `ExportColumnRegistry` | Task 3 Bước 8 | bộ cột |
| 1 dòng trong `$erpCatalogs` của `Routes/api.php` | Task 3 Bước 9 | `'<slug>' => ['<Tên>Controller', '<nhãn>']` |
| Thư mục `pages/master-data/<slug>/` | **copy từ `pages/master-data/origins/`** (Task 4) | bảng thay thế của từng task |
| 1 mục trong nhóm menu "Danh mục hàng hóa" | Task 4 Bước 5 | `label` · `link` · `isShow` |

**Ba điều KHÔNG được quên ở mọi màn:**

1. Entity khai `const STATUS_ACTIVE = 1; const STATUS_INACTIVE = 0;`
2. `statusOptions` ở FE là `{ id: 1, 'Hoạt động' }, { id: 0, 'Khóa' }` — để `id: 2` thì ô lọc
   "Khóa" ra 0 dòng mà không lỗi gì.
3. Entity khai `childrenCount()` = số bản ghi đang dùng, và `activeChildrenCount()` trả `0`
   (chặn Xoá nhưng vẫn cho Khoá).

---

### Task 5: Màn Đơn vị thuộc tính (`unitteches`, 103 dòng)

**Files:**
- Create: `Modules/MasterData/Entities/ProductCatalog/AttributeUnit.php`
- Create: `Modules/MasterData/Services/ProductCatalog/AttributeUnitService.php`
- Create: `Modules/MasterData/Http/Requests/ProductCatalog/AttributeUnitRequest.php`
- Create: `Modules/MasterData/Transformers/ProductCatalog/AttributeUnitResource.php`
- Create: `Modules/MasterData/Http/Controllers/V1/ProductCatalog/AttributeUnitController.php`
- Create: `hrm-client/pages/master-data/attribute-units/index.vue`
- Create: `hrm-client/pages/master-data/attribute-units/AddAttributeUnitModal.vue`
- Modify: `Modules/MasterData/Routes/api.php` · `app/Services/CatalogHistoryService.php` ·
  `app/ExcelExport/ExportColumnRegistry.php` · `hrm-client/components/subsystem-menu/master-data.js`

**Interfaces:**
- Consumes: nền đã nới (Task 1), 2 quyền id 1598/1599 (Task 2), khuôn `origins` (Task 4).
- Produces: `Modules\MasterData\Entities\ProductCatalog\AttributeUnit`, 10 endpoint
  `master-data/attribute-units`.

⚠️ Tên lớp là **`AttributeUnit`**, KHÔNG phải `Unittech` — đặt theo nghiệp vụ tiếng Việt
("đơn vị thuộc tính") cho khớp slug `attribute-units`. Bảng thật vẫn là `unitteches`.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Đơn vị thuộc tính — bảng ERP `unitteches` (103 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa. Bảng KHÔNG có cột `code`, KHÔNG có `description`
 * (dùng cột `note` thay cho diễn giải).
 */
class AttributeUnit extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'unitteches';

    protected $fillable = [
        'name',
        'note',
        'position',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số dòng thuộc tính hàng hoá đang dùng đơn vị này (51.108 dòng trên toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('attribute_products')->where('unittech_id', $this->id)->count();
    }

    /** Vẫn cho Khoá kể cả khi đang được dùng — chỉ chặn Xoá */
    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller — theo khuôn, dùng bảng giá trị này**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` | `AttributeUnit::class` |
| `table()` | `'unitteches'` |
| `hasCodeField()` (Service + Request) | `false` |
| `codePrefix()` | `''` |
| `statusRule()` | `['nullable', 'in:0,1']` |
| `catalogLabel()` (Request) | `'Đơn vị thuộc tính'` |
| `catalogLabel()` (Controller) | `'đơn vị thuộc tính'` |
| `fillableFrom()` | `name` (trim) · `note` · `position` · `status` (mặc định `STATUS_ACTIVE`) |
| `sortableColumns()` | `name` · `position` · `status` · `created_at`/`createdAt` · `updated_at`/`updatedAt`, đều tiền tố `unitteches.` |
| `catalogColumns()` | `['name', 'note', 'position', 'status']` |
| `ownRules()` | `'note' => ['nullable', 'max:255']`, `'position' => ['nullable', 'integer', 'min:0']` |
| `ownMessages()` | `note.max` → `'Nhập tối đa 255 ký tự'`; `position.integer` → `'Vui lòng nhập số nguyên'`; `position.min` → `'Không được nhỏ hơn 0'` |
| `attributes()` | `+ ['note' => 'Ghi chú', 'position' => 'Vị trí']` |
| `ownFields()` (Resource) | `['note' => $this->note, 'position' => $this->position]` |
| `exportScreen()` | `'unitteches'` |
| `exportFileName()` | `'danh_sach_don_vi_thuoc_tinh'` |

- [ ] **Bước 3: Route — thêm 1 dòng vào `$erpCatalogs`**

```php
        'attribute-units' => ['AttributeUnitController', 'đơn vị thuộc tính'],
```

- [ ] **Bước 4: `CatalogHistoryService::TABLES`**

```php
        'unitteches' => ['label' => 'đơn vị thuộc tính', 'columns' => [
            'name' => 'Đơn vị thuộc tính', 'note' => 'Ghi chú',
            'position' => 'Vị trí', 'status' => 'Trạng thái',
        ]],
```

- [ ] **Bước 5: `ExportColumnRegistry`**

```php
        // Đơn vị thuộc tính (/master-data/attribute-units)
        'unitteches' => [
            'name' => 'Đơn vị thuộc tính',
            'note' => 'Ghi chú',
            'position' => 'Vị trí',
            'status_text' => 'Trạng thái',
            'creator_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [ ] **Bước 6: FE — copy từ `origins` rồi thay**

```bash
cd hrm-client
mkdir -p pages/master-data/attribute-units
cp pages/master-data/origins/index.vue pages/master-data/attribute-units/index.vue
cp pages/master-data/origins/AddOriginModal.vue \
   pages/master-data/attribute-units/AddAttributeUnitModal.vue
```

| Chỗ | Thành |
|---|---|
| đường dẫn API (mọi chỗ) | `master-data/attribute-units` |
| `localStorageKey` | `master_data_attribute_units` |
| `pathsToKeep` | `['/master-data/attribute-units']` |
| `columnScreenKey` | `unitteches` |
| `importApiPrefix` | `master-data/attribute-units` |
| tên component modal | `AddAttributeUnitModal` |
| tiêu đề màn | `Đơn vị thuộc tính` |
| tên quyền | `Xem danh mục đơn vị thuộc tính` / `Quản lý danh mục đơn vị thuộc tính` |
| bộ cột | `name` (nuxt-link) · `note` · `position` · `status_text` · `creator_name` · `created_at` · `updater_name` · `updated_at` |
| ô nhập trong modal | `name`* · `note` · `position` |

- [ ] **Bước 7: Menu — thêm mục vào nhóm "Danh mục hàng hóa"**

```js
            {
                label: 'Đơn vị thuộc tính',
                link: '/master-data/attribute-units',
                isShow: ['Quản lý danh mục đơn vị thuộc tính', 'Xem danh mục đơn vị thuộc tính'],
            },
```

- [ ] **Bước 8: Kiểm chứng — số phải khớp**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "unitteches tổng: ".DB::table("unitteches")->count()." (mong đợi 103)\n";
echo "hoạt động: ".DB::table("unitteches")->where("status",1)->count()." (mong đợi 103)\n";
echo "khóa: ".DB::table("unitteches")->where("status",0)->count()." (mong đợi 0)\n";' 2>/dev/null | grep -v Warning
```

Playwright: tổng **103** · lọc Khóa ra **0 dòng** (bảng trống phải hiện dòng "Không có dữ liệu phù
hợp", KHÔNG phải bảng rỗng) · gõ ô tìm nhanh không lỗi · bấm Xoá một đơn vị đang được dùng phải ra
câu QLDA_015 · Khoá/Mở khoá ghi lịch sử đúng chữ.

Sau khi test xong đối chiếu lại: `unitteches` vẫn **103 dòng**, không còn bản ghi rác.

- [ ] **Bước 9: Commit**

```bash
cd hrm-api && git add Modules/MasterData app/Services/CatalogHistoryService.php app/ExcelExport/ExportColumnRegistry.php \
  && git commit -m "[gop_db] Danh mục hàng hoá P1: màn Đơn vị thuộc tính (API)"
cd ../hrm-client && git add pages/master-data/attribute-units components/subsystem-menu/master-data.js \
  && git commit -m "[gop_db] Danh mục hàng hoá P1: màn Đơn vị thuộc tính (FE)"
```

---

### Task 6: Màn Model (`product_models`, 39.796 dòng)

**Files:** như Task 5, đổi `AttributeUnit` → `ProductModel`, slug `product-models`.

**Interfaces:**
- Produces: `Modules\MasterData\Entities\ProductCatalog\ProductModel`, 10 endpoint
  `master-data/product-models`.

⚠️ Đây là màn **nhiều dòng nhất đợt 1** (39.796). Phải kiểm kỹ phân trang và tốc độ, đừng để
`getAll` bị gọi ở màn danh sách.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Model — bảng ERP `product_models` (39.796 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa. Bảng KHÔNG có `code`, KHÔNG có `description`.
 * Cột `old_name` có trong bảng nhưng KHÔNG hiện ra màn (giữ cho ERP).
 */
class ProductModel extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'product_models';

    protected $fillable = [
        'name',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số hàng hoá đang dùng model này (45.890 dòng `products.model_id` trên toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('products')->where('model_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `ProductModel::class` / `'product_models'` |
| `hasCodeField()` | `false` · `codePrefix()` `''` · `statusRule()` `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Model'` · Controller `'model'` |
| `fillableFrom()` | `name` (trim) · `status` |
| `sortableColumns()` | `name` · `status` · `created_at`/`createdAt` · `updated_at`/`updatedAt`, tiền tố `product_models.` |
| `catalogColumns()` | `['name', 'status']` |
| `ownRules()` / `ownMessages()` / `ownFields()` | rỗng (`[]`) |
| `exportScreen()` / `exportFileName()` | `'product_models'` / `'danh_sach_model'` |

- [ ] **Bước 3-5: Route + 2 registry**

```php
        'product-models' => ['ProductModelController', 'model'],
```

```php
        'product_models' => ['label' => 'model', 'columns' => [
            'name' => 'Model', 'status' => 'Trạng thái',
        ]],
```

```php
        // Model (/master-data/product-models)
        'product_models' => [
            'name' => 'Model',
            'status_text' => 'Trạng thái',
            'creator_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [ ] **Bước 6-7: FE + menu**

Copy từ `origins`. Thay: API `master-data/product-models` · `localStorageKey`
`master_data_product_models` · `columnScreenKey` `product_models` · tiêu đề `Model` ·
quyền `… model` · bộ cột chỉ còn `name` (nuxt-link) · `status_text` · 4 cột audit ·
modal chỉ 1 ô `name`*.

Menu:

```js
            {
                label: 'Model',
                link: '/master-data/product-models',
                isShow: ['Quản lý danh mục model', 'Xem danh mục model'],
            },
```

- [ ] **Bước 8: Kiểm chứng — chú ý hiệu năng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "product_models tổng: ".DB::table("product_models")->count()." (mong đợi 39.796)\n";
echo "hoạt động: ".DB::table("product_models")->where("status",1)->count()." (mong đợi 39.528)\n";
echo "khóa: ".DB::table("product_models")->where("status",0)->count()." (mong đợi 268)\n";' 2>/dev/null | grep -v Warning
```

Playwright, đo bằng số:
- Tổng hiện trên màn = **39.796**; lọc Khóa = **268**; lọc Hoạt động = **39.528**.
- Đo thời gian phản hồi của `GET master-data/product-models?per_page=10` trên tab Network —
  nếu > 2s thì báo lại, có thể phải thêm index cho `product_models.name`.
- **Kiểm `getAll` KHÔNG bị gọi** ở màn danh sách (nó trả cả 39.528 dòng đang hoạt động).
- Bấm sang trang 2, 3 rồi quay lại trang 1 → không thấy bản ghi lặp hay mất
  (nền đã chốt `id desc` cuối câu sort).

- [ ] **Bước 9: Commit** — như Task 5, đổi tên màn.

---

## 🚧 CHỐT ĐỢT 1 — làm trước khi mở Task 7

- [ ] `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php`
      → **OK (11 tests, 21 assertions)**, đúng mốc gốc
- [ ] `vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php` → xanh
- [ ] **Bấm thật 6 màn Phase 0** trên trình duyệt: `/master-data/product-natures` ·
      `product-function-groups` · `product-families` · `product-types` · `business-policies` ·
      `product-characteristics`. Mỗi màn: mở danh sách, gõ ô tìm nhanh, lọc Trạng thái,
      **khoá rồi mở khoá 1 bản ghi**, mở popup Lịch sử. Đây là nơi lỗi nền lộ ra.
- [ ] Riêng 2 màn dùng `attributes` / `tax_rates`: mở `/master-data/product-types`, thêm mới 1 loại
      sản phẩm — ô chọn **Thuộc tính** và ô **% VAT** phải còn đổ dữ liệu.
- [ ] `grep -rn 'BaseCatalogModel::STATUS' hrm-api/Modules/MasterData/` → rỗng
- [ ] 3 màn mới đều đúng số dòng khi đối chiếu SQL
- [ ] Báo user kết quả đợt 1 rồi mới sang đợt 2

---

# ĐỢT 2 — 5 màn nghiệp vụ

Thứ tự trong đợt là **bắt buộc**: Hãng sản xuất (Task 10) phải xong trước Code đặt hàng (Task 11)
vì `barcodes.manufacture_id` là NOT NULL.

### Task 7: Màn Đơn vị tính (`units`, 145 dòng)

**Files:** 5 file BE `Unit*` + `pages/master-data/units/` + 4 file đăng ký (như Task 5).

**Interfaces:** Produces `Modules\MasterData\Entities\ProductCatalog\Unit`, 10 endpoint
`master-data/units`.

**Đo trên dữ liệu thật 20/09/2026:** `can_be_base = 1` ở **94/145** dòng · `english_name` có giá
trị ở **60/145** dòng · **`code` có giá trị ở 0/145 dòng** và form ERP (`catalogs/units/create`)
cũng không có ô nhập mã.
→ **Bỏ hẳn cột Mã khỏi màn này**, `hasCodeField()` trả `false` ở cả Service lẫn Request.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Đơn vị tính — bảng ERP `units` (145 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa.
 * Bảng CÓ cột `code` nhưng 0/145 dòng dùng tới và form ERP cũng không có ô nhập
 * -> màn HRM bỏ hẳn cột Mã.
 *
 * ⚠️ Đây là danh mục bị tham chiếu rộng nhất: 234 bảng trong DB gộp có cột `unit_id`.
 */
class Unit extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'units';

    protected $fillable = [
        'name',
        'english_name',
        'position',
        'can_be_base',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số dòng đơn vị của hàng hoá đang dùng đơn vị này (46.560 dòng trên toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('product_units')->where('unit_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `Unit::class` / `'units'` |
| `hasCodeField()` (cả 2) | `false` · `codePrefix()` `''` · `statusRule()` `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Đơn vị tính'` · Controller `'đơn vị tính'` |
| `fillableFrom()` | `name` (trim) · `english_name` · `position` · `can_be_base` (ép `(int) (bool)`) · `status` |
| `sortableColumns()` | `name` · `english_name` · `position` · `status` · `created_at`/`createdAt` · `updated_at`/`updatedAt`, tiền tố `units.` |
| `catalogColumns()` | `['name', 'english_name', 'position', 'can_be_base', 'status']` |
| `ownRules()` | `english_name` → `['nullable','max:255']` · `position` → `['nullable','integer','min:0']` · `can_be_base` → `['nullable','boolean']` |
| `ownFields()` | `english_name` · `position` · `can_be_base` → `(bool)` · `can_be_base_text` → `'Có'` / `''` |
| `exportScreen()` / `exportFileName()` | `'units'` / `'danh_sach_don_vi_tinh'` |

⚠️ `can_be_base_text` trả `''` chứ **không** trả `'Không'` — quy ước ô rỗng để trống hẳn.

- [ ] **Bước 3-5: Route + 2 registry**

```php
        'units' => ['UnitController', 'đơn vị tính'],
```

```php
        'units' => ['label' => 'đơn vị tính', 'columns' => [
            'name' => 'Đơn vị tính', 'english_name' => 'Tên tiếng Anh',
            'position' => 'Vị trí', 'can_be_base' => 'Đơn vị cơ bản', 'status' => 'Trạng thái',
        ]],
```

```php
        // Đơn vị tính (/master-data/units)
        'units' => [
            'name' => 'Đơn vị tính',
            'english_name' => 'Tên tiếng Anh',
            'can_be_base_text' => 'Đơn vị cơ bản',
            'position' => 'Vị trí',
            'status_text' => 'Trạng thái',
            'creator_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

- [ ] **Bước 6-7: FE + menu**

Copy từ `origins`. Bộ cột: `name` (nuxt-link) · `english_name` · `can_be_base_text` ·
`position` · `status_text` · 4 cột audit. Modal: `name`* · `english_name` · `position` ·
`can_be_base` (checkbox "Đơn vị cơ bản").

```js
            {
                label: 'Đơn vị tính',
                link: '/master-data/units',
                isShow: ['Quản lý danh mục đơn vị tính', 'Xem danh mục đơn vị tính'],
            },
```

- [ ] **Bước 8: Kiểm chứng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "units tổng: ".DB::table("units")->count()." (mong đợi 145)\n";
echo "hoạt động: ".DB::table("units")->where("status",1)->count()." (mong đợi 144)\n";
echo "khóa: ".DB::table("units")->where("status",0)->count()." (mong đợi 1)\n";
echo "can_be_base=1: ".DB::table("units")->where("can_be_base",1)->count()." (mong đợi 94)\n";' 2>/dev/null | grep -v Warning
```

Playwright: tổng **145** · cột "Đơn vị cơ bản" có **94 ô ghi Có**, các ô còn lại **trống hẳn**
(không phải "Không", không phải `—`).

- [ ] **Bước 9: Commit**

---

### Task 8: Màn Thuộc tính (`attributes`, 446 dòng)

⚠️ **Hai điều riêng của màn này:**

1. **BỎ trường "Nhóm hàng hoá"** mà form ERP đang có (`groups[]` → pivot `attribute_groups`,
   2.434 dòng). Bảng `groups` nằm trong nhóm BỎ của feature lớn; vai trò đó đã được Phase 0 thay
   bằng `product_type_attributes` khai từ phía Loại sản phẩm. Cột này trên danh sách ERP cũng đã
   bị comment sẵn (`catalogs/attributes/list.blade.php:44`).
2. **Cột `is_filter` là cột chết** — đo thật: `is_filter = 1` ở **0/446** dòng. Không đưa lên màn.
   Cột `attributeset_id` cũng chết (bảng `attributesets` có 0 dòng, model và controller ERP đều
   không đụng).

**Tên lớp là `ProductAttribute`, KHÔNG phải `Attribute`** — `Attribute` đụng `$model->attributes`
nội bộ của Eloquent, quan hệ sẽ không bao giờ lấy được (bẫy Phase 0 đã dính với
`ProductType::productAttributes()`).

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Thuộc tính hàng hoá — bảng ERP `attributes` (446 dòng), ERP vẫn đang đọc/ghi.
 *
 * ⚠️ Tên lớp là ProductAttribute chứ KHÔNG phải Attribute: `attributes` đụng thuộc tính
 * nội bộ `$model->attributes` của Eloquent.
 *
 * ⚠️ Bảng này đang được Phase 0 dùng: pivot `product_type_attributes` (Loại sản phẩm ↔ Thuộc tính)
 * và `CatalogOptionController@attributes` (nguồn ô chọn của màn Loại sản phẩm). Sửa xong màn này
 * PHẢI bấm lại màn /master-data/product-types.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa. Không có `code`, không có `description`.
 */
class ProductAttribute extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'attributes';

    protected $fillable = [
        'name',
        'position',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số dòng thuộc tính của hàng hoá đang dùng (51.128 dòng trên toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('attribute_products')->where('attribute_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `ProductAttribute::class` / `'attributes'` |
| `hasCodeField()` | `false` · `codePrefix()` `''` · `statusRule()` `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Thuộc tính'` · Controller `'thuộc tính'` |
| `fillableFrom()` | `name` (trim) · `position` · `status` |
| `catalogColumns()` | `['name', 'position', 'status']` |
| `ownRules()` | `position` → `['nullable','integer','min:0']` |
| `ownFields()` | `position` |
| `exportScreen()` / `exportFileName()` | `'attributes'` / `'danh_sach_thuoc_tinh'` |

- [ ] **Bước 3-7: Route + registry + FE + menu** — như khuôn. Slug `attributes`, quyền
`… danh mục thuộc tính`, bộ cột `name` (nuxt-link) · `position` · `status_text` · 4 cột audit.

```php
        'attributes' => ['ProductAttributeController', 'thuộc tính'],
```

- [ ] **Bước 8: Kiểm chứng — CÓ THÊM ca riêng cho Phase 0**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "attributes tổng: ".DB::table("attributes")->count()." (mong đợi 446)\n";
echo "hoạt động: ".DB::table("attributes")->where("status",1)->count()." (mong đợi 444)\n";
echo "khóa: ".DB::table("attributes")->where("status",0)->count()." (mong đợi 2)\n";
echo "attribute_groups (pivot nhóm hàng hoá cũ, KHÔNG đụng): ".DB::table("attribute_groups")->count()." (mong đợi 2.434)\n";' 2>/dev/null | grep -v Warning
```

Playwright, **2 màn**:
1. `/master-data/attributes` — bộ lọc, sort, khoá/mở khoá, lịch sử.
2. `/master-data/product-types` (màn Phase 0) — mở form Thêm mới, ô chọn **Thuộc tính** phải vẫn
   đổ đủ **444** lựa chọn đang hoạt động. Đây là ca chứng minh không làm vỡ màn của @junfoke.

Sau test: `attribute_groups` vẫn **2.434 dòng** — màn HRM không được đụng vào pivot đó.

- [ ] **Bước 9: Commit**

---

### Task 9: Màn Thương hiệu (`brands`, 1.250 dòng)

**Màn đầu tiên trong đợt CÓ cột Mã thật.** `brands.code` NOT NULL, **0 giá trị trùng** trên 1.250
dòng → đặt được rule unique.

⚠️ Mã thương hiệu là chuỗi tự do của ERP (`varchar(255)`), **KHÔNG theo khuôn `PREFIX.xxxx`** của
Phase 0. Vì vậy:
- `hasCodeField()` ở **Service** trả `true` (để ghi / lọc / tìm theo cột `code`)
- `hasCodeField()` ở **Request** trả `false` (để nền KHÔNG áp rule `size` + `regex` của Phase 0)
- rule mã tự khai trong `ownRules()`

Đây chính là lý do Task 1 tách hook `hasCodeField()` thành **2 chỗ độc lập**.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Thương hiệu — bảng ERP `brands` (1.250 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa.
 * `code` NOT NULL, chuỗi tự do (không theo khuôn PREFIX.xxxx của Phase 0), hiện không trùng nhau.
 * `company_id` có 618/1.250 dòng để NULL — Phase 3 mới dùng tới, Phase 1 chỉ hiển thị.
 * Cột `icon` / `image` không màn nào dùng, không đưa lên giao diện.
 */
class Brand extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'brands';

    protected $fillable = [
        'code',
        'name',
        'company_id',
        'position',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số hàng hoá đang dùng thương hiệu này (45.890 dòng `products.brand_id` toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('products')->where('brand_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `Brand::class` / `'brands'` |
| `hasCodeField()` **Service** | `true` |
| `hasCodeField()` **Request** | `false` |
| `codePrefix()` | `''` · `statusRule()` `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Thương hiệu'` · Controller `'thương hiệu'` |
| `fillableFrom()` | `code` (trim, KHÔNG `strtoupper`) · `name` (trim) · `company_id` · `position` · `status` |
| `catalogColumns()` | `['code', 'name', 'company_id', 'position', 'status']` |
| `ownRules()` | `code` → `['required','max:255','unique:brands,code,' . $this->currentId()]` · `company_id` → `['nullable','integer']` · `position` → `['nullable','integer','min:0']` |
| `ownMessages()` | `code.required` → `'Bắt buộc phải nhập'` · `code.unique` → `'Đã tồn tại'` · `code.max` → `'Nhập tối đa 255 ký tự'` |
| `attributes()` | `+ ['code' => 'Mã thương hiệu', 'company_id' => 'Công ty', 'position' => 'Vị trí']` |
| `ownFields()` | `position` · `company_id` · `company_name` (tên công ty, để trống khi NULL) |
| `exportScreen()` / `exportFileName()` | `'brands'` / `'danh_sach_thuong_hieu'` |

⚠️ **KHÔNG `strtoupper`** mã thương hiệu như nền Phase 0 làm — đây là dữ liệu ERP có sẵn, viết hoa
lên là sửa dữ liệu của người khác.

- [ ] **Bước 3-7: Route + registry + FE + menu**

```php
        'brands' => ['BrandController', 'thương hiệu'],
```

Bộ cột FE: `code` (**nuxt-link**, vì màn này có mã thật) · `name` · `company_name` · `position` ·
`status_text` · 4 cột audit. Ô lọc: tìm nhanh · Mã · Tên · Trạng thái · Người cập nhật — đúng bộ
lọc ERP đang có.

- [ ] **Bước 8: Kiểm chứng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "brands tổng: ".DB::table("brands")->count()." (mong đợi 1.250)\n";
echo "hoạt động: ".DB::table("brands")->where("status",1)->count()." (mong đợi 1.244)\n";
echo "khóa: ".DB::table("brands")->where("status",0)->count()." (mong đợi 6)\n";
echo "company_id NULL: ".DB::table("brands")->whereNull("company_id")->count()." (mong đợi 618)\n";
echo "mã trùng: ".DB::table("brands")->select("code")->groupBy("code")->havingRaw("COUNT(*)>1")->get()->count()." (mong đợi 0)\n";' 2>/dev/null | grep -v Warning
```

Playwright: thêm mới với mã đã tồn tại → báo **"Đã tồn tại"** ngay dưới ô Mã · 618 ô Công ty
**trống hẳn** · cột Mã mở được tab mới bằng chuột phải.

- [ ] **Bước 9: Commit**

---

### Task 10: Màn Hãng sản xuất (`manufactures`, 1.071 dòng)

**Màn nặng nhất đợt 2.** Phải làm **trước** Task 11.

⚠️ **Bốn điều CỐ Ý không port** (đã chốt với user, ghi ở §8.1 và §9 của spec):

1. **KHÔNG lan truyền `company_id` sang `products`.** ERP `ManufacturesController@update`
   dòng 271-276 lặp mọi hàng hoá của hãng và ghi đè `products.company_id` — hãng `#394` có
   **4.514** hàng hoá, và **367 hàng hoá** đang lệch sẵn. HRM **chỉ ghi bảng `manufactures`**.
2. **KHÔNG** khối "Chi phí tính giá hàng hóa" (`manufacture_costs` có **0 dòng**, chưa từng dùng).
3. **KHÔNG** 4 cột `since_delivery_time` / `since_approved_time` / `since_PO_time` /
   `since_PI_time` — đã bị comment ngay trong hàm update của ERP.
4. **KHÔNG** 3 màn con `kpiOrder` / `kpiSale` / `configEmployee` và 3 cột tương ứng ở danh sách.

⚠️ **`manufactures.code` KHÔNG đặt rule unique.** Đo thật: mã `TIGE` đang dùng cho **2 hãng**
(`#469 Tiger Corporation` và `#1328 CÔNG TY TNHH MTV CƠ ĐIỆN TIGE`), cả hai đều đang hoạt động.
Đặt unique thì không sửa nổi 2 bản ghi đó. Chỉ `required` + `max:255`.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Hãng sản xuất — bảng ERP `manufactures` (1.071 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa.
 *
 * ⚠️ HRM CỐ Ý không port hành vi "sửa hãng -> ghi đè company_id của mọi hàng hoá thuộc hãng"
 * của ERP (ManufacturesController@update:271-276). Xem §8.1 của spec.
 *
 * ⚠️ `code` KHÔNG unique được: mã 'TIGE' đang dùng cho 2 hãng (#469, #1328), cả hai đang hoạt động.
 */
class Manufacturer extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'manufactures';

    protected $fillable = [
        'code',
        'name',
        'company_id',
        'has_vat',
        'position',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /**
     * Số bản ghi đang dùng hãng này: hàng hoá + code đặt hàng.
     * `products.manufacture_id` 45.890 dòng · `barcodes.manufacture_id` 8.664 dòng toàn bảng.
     */
    public function childrenCount(): int
    {
        return DB::table('products')->where('manufacture_id', $this->id)->count()
            + DB::table('barcodes')->where('manufacture_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `Manufacturer::class` / `'manufactures'` |
| `hasCodeField()` | Service `true` · Request `false` |
| `codePrefix()` `''` · `statusRule()` | `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Hãng sản xuất'` · Controller `'hãng sản xuất'` |
| `fillableFrom()` | `code` (trim) · `name` (trim) · `company_id` · `has_vat` (ép `(int)(bool)`) · `position` · `status` — **KHÔNG** đụng `products` |
| `catalogColumns()` | `['code', 'name', 'company_id', 'has_vat', 'position', 'status']` |
| `ownRules()` | `code` → `['required','max:255']` (**không unique**) · `company_id` → `['nullable','integer']` · `has_vat` → `['nullable','boolean']` · `position` → `['nullable','integer','min:0']` |
| `ownFields()` | `position` · `company_id` · `company_name` · `has_vat` → `(bool)` · `has_vat_text` → `'Có'` / `''` |
| `exportScreen()` / `exportFileName()` | `'manufactures'` / `'danh_sach_hang_san_xuat'` |

- [ ] **Bước 3-7: Route + registry + FE + menu**

```php
        'manufacturers' => ['ManufacturerController', 'hãng sản xuất'],
```

Bộ cột FE: `code` (nuxt-link) · `name` · `company_name` · `has_vat_text` · `position` ·
`status_text` · 4 cột audit. **Không** có 3 cột Kế hoạch mua hàng / Đại diện hãng / Cấu hình.

- [ ] **Bước 8: Kiểm chứng — có ca chứng minh KHÔNG lan truyền**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "manufactures tổng: ".DB::table("manufactures")->count()." (mong đợi 1.071)\n";
echo "hoạt động: ".DB::table("manufactures")->where("status",1)->count()." (mong đợi 1.012)\n";
echo "khóa: ".DB::table("manufactures")->where("status",0)->count()." (mong đợi 59)\n";
echo "has_vat=1: ".DB::table("manufactures")->where("has_vat",1)->count()." (mong đợi 901)\n";
echo "--- MỐC company_id của products TRƯỚC khi test ---\n";
foreach(DB::table("products")->select("company_id",DB::raw("COUNT(*) c"))->groupBy("company_id")->orderByDesc("c")->get() as $r)
  echo "  ".($r->company_id===null?"NULL":$r->company_id)." -> ".number_format($r->c)."\n";' 2>/dev/null | grep -v Warning
```

Ghi lại 5 con số đó. Rồi Playwright: mở `/master-data/manufacturers`, **sửa một hãng có nhiều
hàng hoá** (ví dụ hãng `#394` có 4.514 hàng hoá) — đổi tên hoặc đổi Công ty rồi Lưu. Chạy lại đúng
câu tinker trên: **5 con số phải y hệt**. Lệch một dòng là hành vi lan truyền của ERP đã lọt vào.

- [ ] **Bước 9: Commit**

---

### Task 11: Màn Code đặt hàng (`barcodes`, 8.664 dòng)

⚠️ **Phụ thuộc Task 10** — `barcodes.manufacture_id` là **NOT NULL**, form phải có ô chọn Hãng
sản xuất lấy từ `master-data/manufacturers/getAll`.

⚠️ Bảng **không có cột `code`**; chính cột `name` mới là "Code đặt hàng". Đừng nhầm.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Code đặt hàng — bảng ERP `barcodes` (8.664 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa (thực tế 8.664/8.664 đang hoạt động).
 * Bảng KHÔNG có cột `code` — cột `name` chính là mã code đặt hàng.
 * `manufacture_id` NOT NULL -> luôn có danh mục cha là Hãng sản xuất.
 */
class OrderCode extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'barcodes';

    protected $fillable = [
        'name',
        'manufacture_id',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    public function manufacturer()
    {
        return $this->belongsTo(Manufacturer::class, 'manufacture_id');
    }

    /** Số hàng hoá đang dùng code này (9.808 dòng `products.barcode_id` toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('products')->where('barcode_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }

    /** Danh mục cha — nền dùng để quyết định có cho Mở khoá không */
    public function parentCatalog()
    {
        return $this->manufacturer;
    }
}
```

⚠️ `parentCatalog()` khiến **không mở khoá được code đặt hàng khi hãng sản xuất đang bị khoá** —
đúng quy tắc SRS mục 11 mà nền đã cài sẵn. Có **59 hãng đang khoá**, nên ca này xảy ra thật.

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `OrderCode::class` / `'barcodes'` |
| `hasCodeField()` | `false` (cả 2) · `codePrefix()` `''` · `statusRule()` `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Code đặt hàng'` · Controller `'code đặt hàng'` |
| `listRelations()` | `['manufacturer']` |
| `applyOwnFilters()` | lọc thêm `manufacture_id` khi `$request->filled('manufacture_id')` |
| `fillableFrom()` | `name` (trim) · `manufacture_id` · `status` |
| `sortableColumns()` | thêm `manufacture_id` → `barcodes.manufacture_id` |
| `catalogColumns()` | `['name', 'manufacture_id', 'status']` |
| `ownRules()` | `manufacture_id` → `['required','integer','exists:manufactures,id']` |
| `ownMessages()` | `manufacture_id.required` → `'Bắt buộc phải chọn'` · `manufacture_id.exists` → `'Hãng sản xuất không tồn tại'` |
| `attributes()` | `+ ['manufacture_id' => 'Hãng sản xuất']` |
| `ownFields()` | `manufacture_id` · `manufacturer_name` (từ quan hệ, trống khi không có) |
| `exportScreen()` / `exportFileName()` | `'barcodes'` / `'danh_sach_code_dat_hang'` |

Trong `catalogDisplay()` của service này, cột `manufacture_id` phải trả **TÊN hãng** chứ không phải
id — nền có sẵn `parentName()` để dùng:

```php
    protected function catalogDisplay(string $column, $value)
    {
        if ($column === 'manufacture_id') {
            return $this->parentName(Manufacturer::class, $value);
        }

        return parent::catalogDisplay($column, $value);
    }
```

Không làm thì lịch sử ghi "Hãng sản xuất: 469 → 1328", người đọc không hiểu gì.

- [ ] **Bước 3-7: Route + registry + FE + menu**

```php
        'order-codes' => ['OrderCodeController', 'code đặt hàng'],
```

FE: bộ cột `name` (nuxt-link, nhãn **"Code đặt hàng"**) · `manufacturer_name` (nhãn "Hãng sản
xuất") · `status_text` · 4 cột audit. Thêm **ô lọc Hãng sản xuất** dùng `V2BaseSelectRemote`
(1.012 hãng đang hoạt động — quá nhiều cho select thường), có `height="36px"` +
`minimumInputLength`. Modal: `name`* · `manufacture_id`* (select cha, **chỉ hãng đang hoạt động**).

⚠️ Màn Sửa vẫn phải hiện đúng tên hãng **đã khoá** nếu bản ghi đang gắn hãng đó (kèm 🔒).

- [ ] **Bước 8: Kiểm chứng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "barcodes tổng: ".DB::table("barcodes")->count()." (mong đợi 8.664)\n";
echo "hoạt động: ".DB::table("barcodes")->where("status",1)->count()." (mong đợi 8.664)\n";
echo "code đặt hàng của hãng đang KHOÁ: ".DB::table("barcodes")->whereIn("manufacture_id", function($q){ $q->select("id")->from("manufactures")->where("status",0); })->count()."\n";' 2>/dev/null | grep -v Warning
```

Playwright:
- Lọc theo 1 hãng → số dòng khớp `SELECT COUNT(*) FROM barcodes WHERE manufacture_id = ?`.
- Khoá 1 code đặt hàng, khoá luôn hãng của nó, rồi bấm **Mở khoá** code → phải bị chặn với câu
  "Không thể mở khóa code đặt hàng khi danh mục cha đang bị khóa." Mở khoá hãng trước thì mở được.
  **Nhớ hoàn nguyên trạng thái hãng sau khi test.**
- Mở popup Lịch sử sau khi đổi hãng → dòng log phải in **tên hãng**, không phải số id.

- [ ] **Bước 9: Commit**

---

## 🚧 CHỐT ĐỢT 2

- [ ] 2 bộ test BE đều xanh, `ProductClassificationCatalogTest` vẫn **11/11**
- [ ] 8/11 màn chạy được, mỗi màn đối chiếu đủ 3 con số (tổng · hoạt động · khóa) với SQL
- [ ] Ca **không lan truyền `company_id`** ở Task 10 đã chạy và 5 con số `products.company_id`
      không đổi
- [ ] Màn `/master-data/product-types` của Phase 0 vẫn đổ đủ 444 thuộc tính
- [ ] Báo user rồi mới sang đợt 3

---

# ĐỢT 3 — 3 màn nhóm `Common`, mỗi màn một đặc thù

### Task 12: Màn Danh mục file đính kèm (`attachment_types`, 8 dòng)

⚠️ **Đặc thù:** bên ERP màn này **không gắn `checkPermission` ở bất kỳ route nào** — ai đăng nhập
cũng vào được. HRM là lần đầu màn này có phân quyền (id 1606/1607).

⚠️ `company_id` và `department_id` là **NOT NULL** (không có mặc định) → phải gán khi tạo mới,
lấy theo **người tạo**. Quên là `INSERT` nổ.

Mã hiện có theo khuôn `LTL.0001` … `LTL.0008` — **không ép regex**, vì ERP vẫn ghi vào cùng bảng
và có thể dùng khuôn khác.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục file đính kèm — bảng ERP `attachment_types` (8 dòng), ERP vẫn đang đọc/ghi.
 *
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa.
 * `company_id` / `department_id` NOT NULL -> gán theo người tạo khi thêm mới.
 * Mã hiện có dạng LTL.0001..LTL.0008 nhưng KHÔNG ép khuôn, vì ERP ghi chung bảng.
 */
class AttachmentType extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'attachment_types';

    protected $fillable = [
        'code',
        'name',
        'description',
        'company_id',
        'department_id',
        'part_id',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số tệp đang gắn loại này (20 dòng `files.attachment_type_id` toàn bảng) */
    public function childrenCount(): int
    {
        return DB::table('files')->where('attachment_type_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `AttachmentType::class` / `'attachment_types'` |
| `hasCodeField()` | Service `true` · Request `false` |
| `codePrefix()` `''` · `statusRule()` | `['nullable','in:0,1']` |
| `catalogLabel()` | Request `'Loại file đính kèm'` · Controller `'loại file đính kèm'` |
| `fillableFrom()` | `code` (trim) · `name` (trim) · `description` · `status`, **cộng thêm** `company_id` / `department_id` lấy từ nhân viên đang đăng nhập khi TẠO MỚI |
| `catalogColumns()` | `['code', 'name', 'description', 'status']` |
| `ownRules()` | `code` → `['required','max:255','unique:attachment_types,code,' . $this->currentId()]` |
| `exportScreen()` / `exportFileName()` | `'attachment_types'` / `'danh_sach_loai_file_dinh_kem'` |

Gán tổ chức khi tạo mới — viết trong `store()` của service (ghi đè nền):

```php
    public function store(Request $request)
    {
        // `company_id` / `department_id` NOT NULL và không có mặc định -> lấy theo người tạo.
        // Dùng auth()->id() (= employees.id), TUYỆT ĐỐI không auth()->user()->info->id.
        $employee = \Modules\Human\Entities\Employee::find(auth()->id());

        $request->merge([
            'company_id' => $request->company_id ?: ($employee->company_id ?? null),
            'department_id' => $request->department_id ?: ($employee->department_id ?? null),
        ]);

        return parent::store($request);
    }
```

và bổ sung `company_id` · `department_id` · `part_id` vào `fillableFrom()`.

- [ ] **Bước 3-7: Route + registry + FE + menu**

```php
        'attachment-types' => ['AttachmentTypeController', 'file đính kèm'],
```

Bộ cột FE: `code` (nuxt-link) · `name` · `description` · `status_text` · 4 cột audit.
Modal: `code`* · `name`* · `description`.

- [ ] **Bước 8: Kiểm chứng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "attachment_types tổng: ".DB::table("attachment_types")->count()." (mong đợi 8)\n";
echo "hoạt động: ".DB::table("attachment_types")->where("status",1)->count()." (mong đợi 8)\n";
echo "files đang gắn loại: ".DB::table("files")->whereNotNull("attachment_type_id")->count()." (mong đợi 20)\n";
echo "company_id NULL: ".DB::table("attachment_types")->whereNull("company_id")->count()." (mong đợi 0)\n";' 2>/dev/null | grep -v Warning
```

Playwright, **có ca phân quyền bắt buộc** (màn này lần đầu có quyền):
- Tài khoản **CÓ** quyền `Xem danh mục file đính kèm` → vào được, thấy 8 dòng.
- Tài khoản **KHÔNG** có quyền → mục menu **không hiện**, và vào thẳng URL phải bị chặn (403),
  không phải màn trắng.
- ⚠️ Cấp/thu quyền bằng SQL xong phải chạy `php artisan permission:cache-reset`, nếu không cache
  spatie 24h làm kết quả sai.
- Thêm mới 1 loại → kiểm `company_id` / `department_id` đã có giá trị (không NULL), rồi **xoá bản
  ghi vừa tạo** để bảng về đúng 8 dòng.

- [ ] **Bước 9: Commit**

---

### Task 13: Màn Danh mục mã màu (`code_colors`, **0 dòng**)

⚠️ **Đặc thù: bảng RỖNG.** Không có dữ liệu thật để đối chiếu → phải tự tạo, kiểm, rồi **xoá sạch**.
Và không bảng nào trong DB gộp có cột `code_color_id` → `childrenCount()` luôn `0`, tức **xoá được
tự do**. Đây là màn duy nhất trong 11 màn như vậy.

Không port `codeColor.printList` (In danh sách) của ERP — xem §9 của spec.

- [ ] **Bước 1: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Mã màu — bảng ERP `code_colors`, ERP vẫn đang đọc/ghi.
 *
 * ⚠️ Bảng RỖNG (0 dòng) tại thời điểm làm — không có dữ liệu thật để đối chiếu.
 * Trạng thái ERP: 1 = Hoạt động, 0 = Khóa.
 * `company_id` / `department_id` NOT NULL -> gán theo người tạo.
 *
 * Không bảng nào trong DB gộp có cột `code_color_id` -> childrenCount luôn 0, xoá được tự do.
 * Giữ nguyên hành vi mặc định của nền, KHÔNG khai lại childrenCount().
 */
class ColorCode extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'code_colors';

    protected $fillable = [
        'code',
        'name',
        'note',
        'company_id',
        'department_id',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];
}
```

- [ ] **Bước 2: Service · Request · Resource · Controller**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `ColorCode::class` / `'code_colors'` |
| `hasCodeField()` | Service `true` · Request `false` |
| `catalogLabel()` | Request `'Mã màu'` · Controller `'mã màu'` |
| `fillableFrom()` | `code` (trim) · `name` (trim) · `note` · `status` + `company_id`/`department_id` theo người tạo (như Task 12) |
| `catalogColumns()` | `['code', 'name', 'note', 'status']` |
| `ownRules()` | `code` → `['required','max:255','unique:code_colors,code,' . $this->currentId()]` · `note` → `['nullable','max:1000']` |
| `ownFields()` | `note` |
| `exportScreen()` / `exportFileName()` | `'code_colors'` / `'danh_sach_ma_mau'` |

- [ ] **Bước 3-7: Route + registry + FE + menu**

```php
        'color-codes' => ['ColorCodeController', 'mã màu'],
```

Bộ cột FE: `code` (nuxt-link, nhãn "Mã màu") · `name` (nhãn "Tên màu") · `note` · `status_text` ·
4 cột audit.

- [ ] **Bước 8: Kiểm chứng — tự dựng dữ liệu rồi dọn sạch**

Trước khi test, ghi mốc: `code_colors` phải đang có **0 dòng**.

Playwright, theo đúng thứ tự này:
1. Mở màn → phải hiện dòng **"Không có dữ liệu phù hợp"** (không phải bảng rỗng trắng trơn).
   Đây là ca duy nhất trong 11 màn kiểm được trạng thái bảng trống trên dữ liệu thật.
2. Thêm 3 mã màu.
3. Kiểm: danh sách ra 3 dòng · lọc theo mã ra 1 dòng · sort theo Tên đổi đúng thứ tự.
4. Thêm mã trùng → báo **"Đã tồn tại"** ngay dưới ô Mã.
5. Khoá 1 bản ghi → lọc Trạng thái = Khóa ra **1 dòng**, param gửi lên là `status=0`.
6. Mở popup Lịch sử → thấy dòng "Tạo mới" và dòng "Thay đổi trạng thái".
7. **Xoá cả 3** (màn này xoá được vì không ai tham chiếu).

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "code_colors còn lại: ".DB::table("code_colors")->count()." (PHẢI = 0)\n";
echo "catalog_histories của code_colors: ".DB::table("catalog_histories")->where("table","code_colors")->count()."\n";' 2>/dev/null | grep -v Warning
```

Bảng phải về **0 dòng**. Log lịch sử để lại là chấp nhận được (nó là log), nhưng ghi rõ trong
checkpoint là đã tạo bao nhiêu dòng log rác.

- [ ] **Bước 9: Commit**

---

### Task 14: Màn Danh mục thuế suất (`tax_rates`, 40 dòng)

**Màn lệch khuôn nhiều nhất.** Bốn đặc thù, mỗi cái đều làm vỡ nền nếu bỏ qua:

1. ⚠️ **Bảng KHÔNG có cột `name`.** Nền dùng `name` ở 3 chỗ: lọc, ô tìm nhanh, và `getAll()`
   `orderBy('name')` → cả 3 đều nổ `SQLSTATE[42S22]`. Phải thêm hook `nameColumn()` vào nền.
2. ⚠️ **`created_by` / `updated_by` là `varchar`** (giá trị thật vẫn là id: `13`, `787`).
   Subquery `employeeNameSql()` của nền so `e.id = tax_rates.created_by` — MySQL tự ép kiểu nên
   **vẫn chạy đúng** trên 40 dòng. Giữ nguyên, **không** migration đổi kiểu cột (ERP đang ghi).
3. ⚠️ **`is_sales_tax` và `is_purchases_tax` là cột chết** — đo thật: cả hai đều `= 1` ở **0/40**
   dòng. Không đưa lên màn.
4. ⚠️ **KHÔNG khai route `/getAll`.** `tax-rates/getAll` đã được Phase 0 đăng ký cho
   `CatalogOptionController@taxRates` (nguồn ô chọn %VAT của màn Loại sản phẩm) và khai TRƯỚC, nên
   route trong vòng lặp sẽ không bao giờ khớp. Giữ nguyên route của Phase 0.

- [ ] **Bước 1: Thêm hook `nameColumn()` vào nền — lần sửa nền THỨ HAI**

Trong `BaseCatalogService`, thêm cạnh `hasCodeField()`:

```php
    /**
     * Cột đóng vai trò "tên" của danh mục.
     * `tax_rates` không có cột `name` — cột `tax_rate` mới là thứ người dùng nhìn và tìm theo.
     */
    protected function nameColumn(): string
    {
        return 'name';
    }
```

Rồi thay 3 chỗ dùng `name` cứng:

```php
        // bộ lọc theo tên
        if ($request->filled('name')) {
            $escaped = escapeLikeKeyword($request->name);
            if ($escaped !== '') {
                $query->where("$t." . $this->nameColumn(), 'like', '%' . $escaped . '%');
            }
        }
```

```php
        // khối keyword
                $query->where(function ($q) use ($escaped, $t) {
                    $q->where("$t." . $this->nameColumn(), 'like', '%' . $escaped . '%');
                    ...
```

```php
    public function getAll(Request $request)
    {
        $model = $this->modelClass();

        return $model::query()
            ->active()
            ->orderBy($this->nameColumn(), 'asc')
            ->get();
    }
```

- [ ] **Bước 2: Chạy lại CẢ HAI bộ test — nền vừa bị đụng lần nữa**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php 2>&1 | tail -4
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit \
  Modules/MasterData/Tests/Feature/ProductCatalogBaseTest.php 2>&1 | tail -4
```

Mong đợi: `OK (11 tests, 21 assertions)` và bộ còn lại xanh. Lệch là dừng, sửa xong mới đi tiếp.

- [ ] **Bước 3: Entity**

```php
<?php

namespace Modules\MasterData\Entities\ProductCatalog;

use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Danh mục Thuế suất — bảng ERP `tax_rates` (40 dòng), ERP vẫn đang đọc/ghi.
 *
 * ⚠️ Bảng KHÔNG có cột `name` — `tax_rate` (decimal(5,2)) đóng vai trò đó.
 * ⚠️ `created_by` / `updated_by` khai `varchar` chứ không phải bigint như 10 bảng kia.
 *    Giá trị thật vẫn là id nhân viên. KHÔNG migration đổi kiểu (ERP đang ghi).
 * ⚠️ `is_sales_tax` / `is_purchases_tax` là cột chết (0/40 dòng dùng) -> không đưa lên màn.
 *
 * Bảng này đang được Phase 0 dùng qua `product_types.vat_percent_tax_rate_id`.
 */
class TaxRate extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'tax_rates';

    protected $fillable = [
        'tax_rate',
        'status',
        'created_by',
        'updated_by',
        'created_at',
        'updated_at',
    ];

    /** Số loại sản phẩm đang dùng thuế suất này (Phase 0) */
    public function childrenCount(): int
    {
        return DB::table('product_types')->where('vat_percent_tax_rate_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Bước 4: Service**

| Khai báo | Giá trị |
|---|---|
| `modelClass()` / `table()` | `TaxRate::class` / `'tax_rates'` |
| `hasCodeField()` | `false` |
| **`nameColumn()`** | **`'tax_rate'`** |
| `fillableFrom()` | `tax_rate` · `status` (mặc định `STATUS_ACTIVE`) — **không** `name`, **không** `description` |
| `sortableColumns()` | `tax_rate` · `status` · `created_at`/`createdAt` · `updated_at`/`updatedAt`, tiền tố `tax_rates.` |
| `catalogColumns()` | `['tax_rate', 'status']` |

- [ ] **Bước 5: Request — ghi đè `rules()` HẲN**

Nền bắt buộc có `name` (required + unique + `not_regex`), vô nghĩa với một cột số. Màn này khai
rule riêng thay vì vặn nền thêm lần nữa:

```php
<?php

namespace Modules\MasterData\Http\Requests\ProductCatalog;

use Modules\MasterData\Http\Requests\ProductClassification\BaseCatalogRequest;

/**
 * Validate danh mục Thuế suất — bảng ERP `tax_rates`.
 *
 * Ghi đè `rules()` hẳn vì bảng không có cột `name`: rule mặc định của nền
 * (name required + unique + not_regex) không áp được cho một cột decimal.
 */
class TaxRateRequest extends BaseCatalogRequest
{
    protected function table(): string
    {
        return 'tax_rates';
    }

    protected function hasCodeField(): bool
    {
        return false;
    }

    protected function codePrefix(): string
    {
        return '';
    }

    protected function catalogLabel(): string
    {
        return 'Thuế suất';
    }

    public function rules()
    {
        $id = $this->currentId();

        return [
            // decimal(5,2) -> tối đa 999.99
            'tax_rate' => [
                'required',
                'numeric',
                'min:0',
                'max:999.99',
                'unique:tax_rates,tax_rate,' . $id,
            ],
            'status' => ['nullable', 'in:0,1'],
        ];
    }

    public function messages()
    {
        return [
            'tax_rate.required' => 'Bắt buộc phải nhập',
            'tax_rate.numeric' => 'Vui lòng nhập số',
            'tax_rate.min' => 'Không được nhỏ hơn 0',
            'tax_rate.max' => 'Không được lớn hơn 999,99',
            'tax_rate.unique' => 'Đã tồn tại',
        ];
    }

    public function attributes()
    {
        return ['tax_rate' => '% Thuế suất'];
    }
}
```

- [ ] **Bước 6: Resource + Controller**

`ownFields()` trả `['tax_rate' => $this->tax_rate]`. `exportScreen()` `'tax_rates'`,
`exportFileName()` `'danh_sach_thue_suat'`, `catalogLabel()` `'thuế suất'`.

- [ ] **Bước 7: Route — KHÔNG có `/getAll`**

Khai riêng, **không** nhét vào vòng lặp `$erpCatalogs`:

```php
    /*
    | Thuế suất khai RIÊNG, KHÔNG dùng vòng lặp $erpCatalogs: route `tax-rates/getAll` đã thuộc
    | về `CatalogOptionController@taxRates` của Phase 0 (nguồn ô chọn %VAT của màn Loại sản phẩm)
    | và được khai TRƯỚC — thêm `/getAll` ở đây là route chết.
    */
    Route::group(['prefix' => 'tax-rates'], function () {
        $action = 'V1\ProductCatalog\TaxRateController';
        $view = 'Xem danh mục thuế suất';
        $manage = 'Quản lý danh mục thuế suất';

        Route::get('/export', $action . '@export')->middleware('checkPermission:' . $manage . '|' . $view);
        Route::post('/import/validate', $action . '@validateImport')->middleware('checkPermission:' . $manage);
        Route::post('/import', $action . '@import')->middleware('checkPermission:' . $manage);
        Route::get('/', $action . '@index')->middleware('checkPermission:' . $manage . '|' . $view);
        Route::get('/{catalog}', $action . '@show')->middleware('checkPermission:' . $manage . '|' . $view);
        Route::post('/', $action . '@store')->middleware('checkPermission:' . $manage);
        Route::put('/{catalog}', $action . '@update')->middleware('checkPermission:' . $manage);
        Route::delete('/{catalog}', $action . '@delete')->middleware('checkPermission:' . $manage);
        Route::get('/{catalog}/lock', $action . '@lock')->middleware('checkPermission:' . $manage);
        Route::get('/{catalog}/unlock', $action . '@unlock')->middleware('checkPermission:' . $manage);
    });
```

⚠️ Route `GET /{catalog}` đứng sau `/export` — nếu đảo thứ tự thì `/export` bị nuốt.

- [ ] **Bước 8: 2 registry + FE + menu**

```php
        'tax_rates' => ['label' => 'thuế suất', 'columns' => [
            'tax_rate' => '% Thuế suất', 'status' => 'Trạng thái',
        ]],
```

```php
        // Thuế suất (/master-data/tax-rates)
        'tax_rates' => [
            'tax_rate' => '% Thuế suất',
            'status_text' => 'Trạng thái',
            'creator_name' => 'Người tạo',
            'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật',
            'updated_at' => 'Ngày cập nhật',
        ],
```

FE: bộ cột `tax_rate` (nuxt-link, nhãn "% Thuế suất", **căn phải** vì là số) · `status_text` ·
4 cột audit. Modal chỉ 1 ô `tax_rate`*. Ô tìm nhanh ghi `Tìm theo % thuế suất`.

- [ ] **Bước 9: Kiểm chứng**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "tax_rates tổng: ".DB::table("tax_rates")->count()." (mong đợi 40)\n";
echo "hoạt động: ".DB::table("tax_rates")->where("status",1)->count()." (mong đợi 40)\n";
echo "product_types đang dùng thuế suất: ".DB::table("product_types")->whereNotNull("vat_percent_tax_rate_id")->count()."\n";' 2>/dev/null | grep -v Warning
```

Playwright, **2 màn**:
1. `/master-data/tax-rates` — tổng **40** · gõ ô tìm nhanh `2` phải ra dữ liệu, **không**
   `SQLSTATE[42S22]` (đây là ca chứng minh hook `nameColumn()` chạy) · cột % căn phải · thêm giá
   trị trùng báo "Đã tồn tại" · sort theo % đúng thứ tự số (không phải thứ tự chuỗi).
2. `/master-data/product-types` (Phase 0) — mở form Thêm mới, ô **% VAT** phải vẫn đổ đủ **40**
   lựa chọn. Chứng minh route `tax-rates/getAll` của Phase 0 không bị cướp.

Sau test: `tax_rates` vẫn **40 dòng**.

- [ ] **Bước 10: Commit**

---

## 🚧 CHỐT ĐỢT 3

- [ ] Đủ **11/11 màn** chạy được
- [ ] `ProductClassificationCatalogTest` vẫn **OK (11 tests, 21 assertions)** sau 2 lần đụng nền
- [ ] `ProductCatalogBaseTest` xanh
- [ ] `code_colors` về đúng **0 dòng** sau khi test

---

### Task 15: Rà soát cuối toàn Phase 1

**Files:** không tạo file mới; chỉ soát và sửa chỗ lệch.

- [ ] **Bước 1: Grep tự kiểm trên CẢ 11 thư mục feature**

```bash
cd hrm-client
DIRS="pages/master-data/origins pages/master-data/attribute-units pages/master-data/product-models \
pages/master-data/units pages/master-data/attributes pages/master-data/brands \
pages/master-data/manufacturers pages/master-data/order-codes pages/master-data/attachment-types \
pages/master-data/color-codes pages/master-data/tax-rates"

for p in "status-pill\|statusPillClass" "interactable:\|disabledTitle" "action\.key ===" \
         "V2BaseFilterPanel" "advanced-filters" "showCustomerList\|filtered.*= \[\]" \
         "log.action !==" "actionOptions" "|| '—'\|placeholder=\"—\""; do
  echo "=== $p ==="; grep -rn "$p" $DIRS
done

echo "=== V2BaseSelectRemote thiếu height ==="
grep -rn "V2BaseSelectRemote" $DIRS | grep -v 'height='

echo "=== statusOptions còn id: 2 (PHẢI RỖNG) ==="
grep -rn "id: 2" $DIRS
```

Mong đợi: **mọi khối rỗng**. Khối cuối là quan trọng nhất — còn `id: 2` nào là ô lọc "Khóa" của
màn đó đang chết im lặng.

- [ ] **Bước 2: Kiểm `columnScreenKey` và `localStorageKey` không trùng nhau**

```bash
cd hrm-client
grep -rhn "columnScreenKey:" $DIRS | sed "s/.*columnScreenKey: *'//;s/'.*//" | sort | uniq -d
grep -rhn "localStorageKey:" $DIRS | sed "s/.*localStorageKey: *'//;s/'.*//" | sort | uniq -d
```

Mong đợi: **rỗng cả hai**. Trùng là 2 màn ghi đè cấu hình cột của nhau.

- [ ] **Bước 3: Đối chiếu số dòng 11 bảng với SQL — lần cuối**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
$exp = ["product_models"=>39796,"barcodes"=>8664,"units"=>145,"attributes"=>446,"unitteches"=>103,
        "brands"=>1250,"manufactures"=>1071,"origins"=>113,"attachment_types"=>8,"code_colors"=>0,"tax_rates"=>40];
$bad = 0;
foreach($exp as $t=>$n){ $c=DB::table($t)->count();
  printf("%-18s %8s / %8s %s\n",$t,number_format($c),number_format($n),$c==$n?"OK":"<<< LỆCH");
  if($c!=$n) $bad++; }
echo $bad===0 ? "\nTẤT CẢ KHỚP\n" : "\nCÓ $bad BẢNG LỆCH — dữ liệu test chưa dọn sạch\n";' 2>/dev/null | grep -v Warning
```

Mong đợi: `TẤT CẢ KHỚP`. Lệch nghĩa là còn bản ghi test sót lại trên dữ liệu thật của ERP.

- [ ] **Bước 4: Kiểm 22 quyền và 11 mục menu khớp nhau**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='
echo "quyền 1590-1611: ".DB::table("permissions")->whereBetween("id",[1590,1611])->count()." / 22\n";' 2>/dev/null | grep -v Warning
cd ../hrm-client
echo "mục menu trong nhóm Danh mục hàng hóa:"
grep -c "master-data/" components/subsystem-menu/master-data.js
```

Mọi tên quyền trong `isShow` của 11 mục menu phải **khớp từng chữ** với tên trong seeder — sai một
dấu là mục menu biến mất không báo gì.

- [ ] **Bước 5: Kiểm EOL không bị đổi hàng loạt**

```bash
cd hrm-client && git diff --numstat | awk '$2 > 200 {print "NGHI NGỜ đổi EOL cả file:", $3, "xoá", $2, "dòng"}'
cd ../hrm-api && git diff --numstat | awk '$2 > 200 {print "NGHI NGỜ đổi EOL cả file:", $3, "xoá", $2, "dòng"}'
```

File nào bị đổi toàn bộ EOL sẽ hiện ra ở đây. Repo trộn CRLF/LF nên phải giữ nguyên từng dòng.

- [ ] **Bước 6: Chạy lại toàn bộ test**

```bash
cd hrm-api
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ 2>&1 | tail -6
```

⚠️ Đọc **dòng tổng kết**, đừng thấy cuối log không có chữ "failed" là yên tâm.

- [ ] **Bước 7: Kiểm Import có file mẫu tải về được — cả 11 màn**

Checklist mục F đòi "Import dùng `V2BaseImportModal`; có file mẫu tải về được". Khuôn copy từ
`origins` mang theo `CatalogImportMixin`, nhưng **file mẫu là của từng màn** (cột khác nhau).

Với mỗi màn: mở popup Import → bấm **Tải file mẫu** → mở file ra xem tiêu đề cột có đúng bộ cột
nhập được của màn đó không (không phải bộ cột của màn `origins`).

⚠️ Một điểm lệch checklist **đã biết từ Phase 0, chờ user quyết**: `V2BaseImportToolbar` (component
DÙNG CHUNG) chỉ cho bấm Import khi đã hết dòng lỗi, trong khi quy tắc là "vẫn import được, chỉ lấy
dòng hợp lệ" — và BE (`BaseCatalogController@import`) đã làm đúng quy tắc rồi. Đừng tự sửa component
dùng chung; nêu lại cho user cùng với kết quả Phase 1.

- [ ] **Bước 8: Cập nhật tài liệu**

- `.plans/gop-db/quan-ly-hang-hoa/design.md`: bảng phase, Phase 1 → 🟢 XONG
- `.plans/gop-db/STATUS.md`: mục Phase 1 → trạng thái, số file, việc còn nợ, bài học
- Thêm checkpoint vào cuối `plan.md` này theo khuôn: *Vừa hoàn thành / Đang làm dở / Bước tiếp
  theo / Blocked*

- [ ] **Bước 9: Báo user** — kèm 3 số: bao nhiêu màn xong, bộ test ra bao nhiêu, bảng nào còn lệch.

---

## Việc còn nợ sau Phase 1 (không làm trong phase này)

| Việc | Vì sao hoãn |
|---|---|
| 3 màn con Hãng sản xuất (Kế hoạch mua hàng · KPI bán hàng · Cấu hình nhân viên) | User chốt "chỉ CRUD" |
| Cách quản `products.company_id` sau khi bỏ lan truyền từ Hãng sản xuất | Thuộc Phase 3 |
| Route `unit.updateEnglishName` (quyền `Tổng hợp đặt hàng`) | Chức năng của người làm đặt hàng |
| `codeColor.printList` — In danh sách mã màu | Bảng rỗng, chưa rõ nhu cầu |
| 61 migration còn pending trên DB local | Cố ý không chạy; cần rà riêng trước khi deploy |
| Gỡ mục menu 11 màn bên ERP | User chốt **giữ nguyên cả 2 nơi** |
| Xin spec gốc Phase 0 (`docs/superpowers/specs/gop-db/2026-09-18-...`) từ @junfoke | Không có trên máy |

## LƯU Ý KHI DEPLOY môi trường khác

1. Chạy **`php artisan migrate --path=Modules/MasterData/Database/Migrations`** trước — 7 bảng
   Phase 0 có thể cũng chưa có ở đó.
2. **KHÔNG chạy `PermissionsTableSeeder`** nếu môi trường đã có dữ liệu — nó `truncate` cả bảng
   `permissions`. Chèn tay 22 dòng id 1590-1611 (script ở Task 2 Bước 4).
3. Sau khi cấp quyền: **`php artisan permission:cache-reset`** (cache spatie 24h).
4. Kiểm trùng id quyền trước khi merge: `grep -oE "'id' => [0-9]+" <seeder> | sort | uniq -d`.
5. Không có migration nào đụng 11 bảng ERP → **không cần backup 11 bảng đó**, nhưng vẫn nên
   ghi lại `COUNT(*)` trước/sau để đối chiếu.

---

## Nhật ký thực thi

### Checkpoint — 20/09/2026 (Task 1-4 xong)

**Vừa hoàn thành:** Task 1 (nới nền) · Task 2 (22 quyền) · Task 3 (API Xuất xứ) · Task 4 (FE Xuất
xứ + tách menu). Nhánh riêng `feat/p1-danh-muc-hang-hoa` ở cả 2 repo, 5 commit.

**Chuẩn bị môi trường (trước khi code):** chạy chọn lọc 12 migration `Modules/MasterData` — 7 bảng
Phase 0 **trước đó không tồn tại trên DB local**, bộ test #11421 đang **11 ERROR**; chèn tay 12
quyền 1574-1585. Sau đó test về `OK (11 tests, 21 assertions)` = mốc gốc.

**🐞 Lỗi CÓ SẴN trên `origin/gop_db` phát hiện khi chạy (không phải do Phase 1):**

1. **`app/Services/CatalogHistoryService.php` HỎNG CÚ PHÁP** — mục `meeting_room_settings` thiếu
   `]],` (vết merge giữa nhánh Phòng họp và nhánh #11421). `php -l` báo `Parse error line 570`;
   bản `git show origin/gop_db:` và working tree có **MD5 giống hệt, cùng hỏng**. Hậu quả: MỌI thao
   tác ghi lịch sử danh mục đều fatal, ảnh hưởng 6 màn #11421 + 2 màn Phòng họp + 18 màn danh mục
   cũ. Chưa ai thấy vì bộ test #11421 tạo bản ghi bằng `Model::create()` trực tiếp, không qua
   service. → Đã vá ở commit riêng `221cda7b2` (**+1 dòng**), **cần cherry-pick về `gop_db`**.
2. **`LogsCatalogHistory::logLockToggle()` và `logCatalogSave()`** hard-code `status === 2` mới coi
   là khoá → bản ghi bảng ERP (khoá = 0) bị ghi nhãn `unlock` cho **cả lần khoá**. Đã vá bằng hằng
   của chính model + `defined()` bảo vệ nên 14 service danh mục cũ không đổi hành vi.

**⚠️ Chỗ plan viết SAI / THIẾU, đã sửa khi làm — các task sau phải biết:**

| Plan viết | Thực tế |
|---|---|
| Nền cần sửa "11 chỗ, 5 file" | Còn thiếu: `BaseCatalogService` bắt buộc khai **`catalogLabel()`** (trait `ImportsCatalogRows` khai abstract) — mọi Service của 11 màn phải có |
| `ImportsCatalogRows` chỉ sửa 1 dòng (183) | Trait **bám chặt cột `code`** ở 8 chỗ: dedupe, ép khuôn `PREFIX.xxxx`, tra cha `keyBy(code)`, ghi `code`/`description`. Đã nới bằng 2 hook mới **`hasDescriptionField()`** và **`importParentKeyColumn()`** (user chốt 20/09) |
| Test dùng `created_by => 1` | `origins.created_by`/`updated_by` có **khoá ngoại tới `employees`** và NOT NULL → phải lấy id nhân viên CÓ THẬT |
| `actingAs(Employee::find(...))` | `Modules\Human\Entities\Employee` **không Authenticatable**. Guard `api` dùng `App\Models\TpEmployee` (`config/auth.php:70`) |
| "10 route mỗi màn" | Thực tế **11 route** |
| `php artisan permission:cache-reset` | Lệnh này báo **"Unable to flush cache"** trên máy này; dùng `php artisan cache:clear` |
| Task 4 Bước 1: "sửa màn nguồn nếu có vi phạm" | Đổi thành **báo user**, không tự sửa màn của người khác. Soát `business-policies`: **sạch** (`CheckPermission` đăng ký toàn cục ở `plugins/global-mixins.js` nên không cần khai trong `mixins:`) |

**Thêm việc phát sinh, đã làm:** hằng FE **`ERP_CATALOG_STATUS_OPTIONS`** (Khóa = 0) trong
`utils/product-classification.js` — 10 màn sau dùng lại. Và mọi chỗ đọc `status` ở modal phải bỏ
`|| 1` vì `0` là giá trị hợp lệ.

**Dữ liệu đã đụng trên DB local (ghi để hoàn nguyên nếu cần):**
- `permissions`: 1.710 → **1.744** (12 quyền #11421 + 22 quyền Phase 1)
- `role_has_permissions`: 16.654 → **16.676** (cấp 22 quyền cho role #18 Super admin, `company_id = 1`)
- `catalog_histories`: +11 dòng log của `origins` (từ các vòng test, là bảng log nên để lại)
- `origins`: vẫn **113 dòng / 112 hoạt động / 1 khóa**, 0 bản ghi rác

**Đang làm dở:** chưa bắt đầu Task 5.
**Bước tiếp theo:** Task 5 — màn Đơn vị thuộc tính (`unitteches`, 103 dòng).
**Blocked:** (không)

### Checkpoint — 20/09/2026 (XONG 11/11 MÀN)

**Vừa hoàn thành:** đủ **15/15 task**. 11 màn chạy được, nhánh `feat/p1-danh-muc-hang-hoa`
ở cả 2 repo (hrm-api 13 commit, hrm-client 11 commit).

| Màn | Slug | Dòng | Điểm riêng |
|---|---|---|---|
| Xuất xứ | `origins` | 113 | màn khuôn cho 10 màn sau |
| Đơn vị thuộc tính | `attribute-units` | 103 | cột `note` |
| Model | `product-models` | 39.796 | nhiều dòng nhất, 0,30-0,63s |
| Đơn vị tính | `units` | 145 | `english_name`, `can_be_base` |
| Thuộc tính | `attributes` | 446 | lớp `ProductAttribute`; BỎ trường Nhóm hàng hoá |
| Thương hiệu | `brands` | 1.250 | mã thật + unique |
| Hãng sản xuất | `manufacturers` | 1.071 | KHÔNG lan truyền `company_id`; mã KHÔNG unique |
| Code đặt hàng | `order-codes` | 8.664 | có danh mục CHA |
| File đính kèm | `attachment-types` | 8 | lần đầu có quyền; tự gán công ty/phòng ban |
| Mã màu | `color-codes` | **0** | bảng rỗng; xoá được tự do |
| Thuế suất | `tax-rates` | 40 | không cột `name`; route khai riêng |

**🐞 6 lỗi phát hiện & vá trong lúc làm — đều là lỗi IM LẶNG, test xanh không bắt được:**

1. **`CatalogHistoryService.php` hỏng cú pháp trên chính `origin/gop_db`** (vết merge, thiếu `]],`)
   → mọi thao tác ghi lịch sử danh mục fatal. Commit riêng `221cda7b2`, **cần cherry-pick về `gop_db`**.
2. **`LogsCatalogHistory` hard-code `status === 2`** ở `logLockToggle()` và `logCatalogSave()`
   → bản ghi bảng ERP (khoá = 0) bị ghi nhãn `unlock` cho cả lần KHOÁ.
3. **`entity-type="origins"` sót ở 4 màn copy** → khối Lịch sử trong popup Xem nạp lịch sử bảng khác.
4. **Màn Thuộc tính lệch tên component** (`<add-attribute-modal>` vs `AddProductAttributeModal`)
   → Vue báo "Unknown custom element", popup không mở. **Chỉ lộ khi mở trình duyệt thật.**
5. **Rule mã ghi cứng `unique:brands` ở 3 màn** → kiểm trùng trên BẢNG KHÁC, tạo được bản ghi
   trùng mã (đã tạo thật 3 dòng `ZZMAU1` rồi mới phát hiện). Nay dùng `$this->table()`.
   Kèm theo: `ManufacturerRequest` lẽ ra phải BỎ unique (mã `TIGE` trùng 2 hãng) nhưng phép thay
   chuỗi không khớp và im lặng.
6. **`OrderCodeService` thiếu `parentConfig()`** → validate import báo "hợp lệ" nhưng bản ghi ghi
   xuống không có `manufacture_id` (NOT NULL) → nổ. **Bước validate không lộ, chỉ import thật mới lộ.**

**Nền `BaseCatalog*` bị đụng 2 lần, cả 2 lần đều chứng minh không vỡ Phase 0:**
lần 1 (Task 1) thêm `hasCodeField()` / `statusRule()` / `hasDescriptionField()` /
`importParentKeyColumn()` + bỏ tham chiếu cứng hằng trạng thái; lần 2 (Task 14) thêm `nameColumn()`.
Sau mỗi lần: `ProductClassificationCatalogTest` vẫn **OK (11 tests, 21 assertions)**.

**Kiểm chứng cuối:**
- 11/11 endpoint danh sách HTTP 200; 2 endpoint nguồn ô chọn của #11421 vẫn đủ **444** thuộc tính
  và **40** thuế suất
- **11/11 bảng khớp chính xác số dòng mốc ban đầu** — 0 bản ghi rác sót lại
- `CatalogHistoryService::TABLES` 64 → **74 mục**, `ExportColumnRegistry` 63 → **74 màn**, đủ 11/11
- 22/22 quyền id 1590-1611; khoá `columnScreenKey`/`localStorageKey`/`exportFieldsModalId`/
  `importModalId`/`importApiPrefix` **không trùng nhau và không trùng 6 màn Phase 0**
- Khối grep tự kiểm của skill `erp-to-hrm-screen` chạy trên 11 thư mục: **sạch**
- `git diff --numstat`: không file nào bị đổi EOL hàng loạt
- Gate quyền kiểm 2 chiều ở màn File đính kèm: có quyền 200, thu hồi → **403** cả GET lẫn POST

**Dữ liệu đã đụng trên DB local:**
- `permissions` 1.710 → **1.744** · `role_has_permissions` 16.654 → **16.688** (cấp 34 quyền cho
  role #18 Super admin: 12 của Phase 0 + 22 của Phase 1)
- `catalog_histories` +~20 dòng log từ các vòng test (bảng log, để lại)
- ⚠️ Hãng sản xuất **#394** (`CH` / Cửa hàng lẻ) đã hoàn nguyên đúng từng trường, nhưng
  `updated_by` / `updated_at` của dòng đó mang dấu vết lần sửa thử — không khôi phục được.

**Đang làm dở:** (không)
**Bước tiếp theo:** user nghiệm thu; sau đó merge `feat/p1-danh-muc-hang-hoa` về `gop_db`.
**Blocked:** (không)

**Còn nợ / cần user quyết:**
- Cherry-pick `221cda7b2` (vá cú pháp `CatalogHistoryService`) về `gop_db` — nhánh chung đang vỡ
- `V2BaseImportToolbar` (component DÙNG CHUNG) chỉ cho Import khi hết dòng lỗi, khác rule "vẫn
  import được, chỉ lấy dòng hợp lệ" mà BE đã làm đúng — điểm lệch đã biết từ Phase 0
- 61 migration còn pending trên DB local, cố ý chưa chạy

### Checkpoint — 21/09/2026 (BỘ E2E PHASE 1)

**Vừa hoàn thành:** viết + chạy bộ e2e cho Phase 1 theo phạm vi user chốt (API cả 11 màn + UI 3 màn
đại diện). ⚠️ Thư mục `HRM/e2e` **không nằm trong repo git nào** — 2 file spec này chỉ có trên máy.

| File | Ca | Kết quả |
|---|---|---|
| `e2e/tests/master-data/product-catalog-common.api.spec.ts` | **77** (11 màn × 7) | `77 passed (1.2m)` |
| `e2e/tests/master-data/product-catalog-ui.spec.ts` | **7** | `7 passed (51.8s)` |

Cách chạy (Node 20, bỏ chuỗi setup vì `.auth/*.json` còn hiệu lực):

```bash
export PATH=~/.nvm/versions/node/v20.20.1/bin:$PATH
cd HRM/e2e
npx playwright test tests/master-data/ --project=api      --no-deps --workers=1
npx playwright test tests/master-data/ --project=chromium --no-deps --workers=1
```

**Vì sao MỘT file chạy vòng 11 màn thay vì 11 file:** 11 màn dùng chung nền `BaseCatalog*`, cái đáng
test là hành vi của NỀN áp lên từng bảng. Bảng `CATALOGS` trong spec là nguồn sự thật duy nhất —
thêm màn thứ 12 chỉ việc thêm 1 dòng.

**7 ca chung mỗi màn:** danh sách + `meta` · ô tìm nhanh không nổ SQL · lọc trạng thái dùng **0**
(và `status=2` phải ra rỗng) · vòng đời tạo → **khoá ghi 0** → mở khoá ghi 1 → xoá · bản ghi đang
khoá không xoá được · thiếu trường bắt buộc → 422 gắn đúng field · **không quyền → 403 cả đọc lẫn ghi**.

**🐞 3 lỗi SẢN PHẨM mà chỉ bộ e2e UI bắt được** (test API xanh, console sạch, nhìn màn vẫn "chạy"):

1. **Modal Thương hiệu + Hãng sản xuất THIẾU HẲN ô Công ty** — BE nhận `company_id` nhưng form
   không có ô nhập → không đặt được công ty từ giao diện.
2. **Cả 4 màn có mã dùng `V2BaseCodeInput` với prefix cứng `CSKD.`** (chép từ màn Chính sách kinh
   doanh) → ép mã theo khuôn `PREFIX.xxxx`, **mâu thuẫn với rule BE** vì mã bảng ERP là chuỗi tự do.
3. **Cả 4 màn đó hiện tooltip của "chính sách kinh doanh"** — phép thay
   `CATALOG_TOOLTIPS.brand` → `.brand` là no-op nên giữ nguyên `.businessPolicy`.

Đã vá ở commit `4ff39a185` (hrm-client).

**3 lỗi của CHÍNH BỘ TEST, mất 7 lượt chạy mới ra — ghi để lần sau khỏi vấp:**

1. `meta.per_page` trả về **CHUỖI** `'5'` trong khi `total`/`current_page` là số (Laravel nhả lại
   nguyên giá trị query string). Phải `Number(...)` khi so. Hành vi CÓ SẴN của nền, không phải Phase 1.
2. **Nhắm ô nhập bằng `input[type="text"]` thứ nhất là sai** — ô text đầu tiên trong modal là hộp
   tìm của select2. Điền nhầm vào đó thì trường bắt buộc rỗng, FE chặn submit đúng quy tắc, và ca
   test treo chờ request không bao giờ đến. Nhắm bằng **placeholder**.
3. ⭐ **`locator('button', { hasText: /^Lưu$/ })` khớp 0 phần tử.** Playwright **không chuẩn hoá
   khoảng trắng khi so bằng REGEX**, và tên khả truy cập của nút còn dính **glyph icon** ở đầu
   (`V2BaseButton` render `<i>` ở slot `#prefix`). Cả `hasText: /^Lưu$/` lẫn
   `getByRole('button', { name: /^\s*Lưu\s*$/ })` đều trượt. Cách chạy được:
   `modal.locator('button').filter({ hasText: 'Lưu' }).filter({ hasNotText: 'Tiếp tục' })`
   — lọc bằng CHUỖI (có chuẩn hoá + so chứa) rồi loại "Lưu & Tiếp tục".

**Kiểm chứng an toàn dữ liệu:** chụp số dòng 11 bảng TRƯỚC và SAU khi chạy e2e → **11/11 y hệt**,
0 bản ghi `E2E%` sót lại. Phân bố `products.company_id` cũng không đổi (44.816 / 1.056 / 14 / 3 / 1 NULL)
dù bộ UI có LƯU THẬT một hãng sản xuất.

**Đang làm dở:** (không)
**Bước tiếp theo:** user nghiệm thu; merge `feat/p1-danh-muc-hang-hoa` về `gop_db`.
**Blocked:** (không)

---

### Checkpoint — 21/09/2026 (BỎ Ô CÔNG TY + DỌN BỐ CỤC + 1 GATE QUYỀN CHẾT)

**Vừa hoàn thành:**

**1. Bỏ ô Công ty ở Thương hiệu / Hãng sản xuất — máy chủ tự gán theo người lưu** (user chốt 21/09).
Đảo ngược đúng điểm 1 của checkpoint trước (lúc đó e2e bắt "thiếu ô Công ty" và đã thêm vào).

- `BrandService` / `ManufacturerService`: thêm `store()` lấy `company_id` của người đăng nhập từ
  `employee_infos` (join qua `employees.id = auth()->id()`) rồi `$request->merge(...)`.
- `fillableFrom()` chỉ ghi `company_id` **khi request có trường đó** (`$request->has(...)`), nên
  **đường SỬA không đụng vào công ty** — người công ty khác sửa bản ghi không âm thầm kéo nó sang
  công ty mình.
- Cùng bẫy đó đã vá luôn ở `AttachmentTypeService` (`company_id`/`department_id`/`part_id`) và
  `ColorCodeService` (`company_id`/`department_id`): trước đây mỗi lần PUT là ghi đè về `null`.
- **Đo thật (không tin code đọc hợp lý):** tạo qua API không gửi `company_id` → DB ghi `1` (đúng
  công ty người tạo); đặt tay sang `4` rồi PUT không gửi `company_id` → vẫn `4`, tên đổi. Làm cho
  cả `brands` lẫn `manufactures`; xoá bản ghi thử, số dòng về đúng 1.250 / 1.071, 0 rác `ZZ%`.

**2. Bố cục popup — 6/11 màn có hàng chưa đủ 12 cột.** Bỏ ô Công ty làm "Vị trí" đứng lẻ một mình;
riêng **Đơn vị tính** thì hàng 2 cộng ra **15 cột** nên "Vị trí" tự rớt xuống dòng dưới (lỗi có sẵn,
không ai thấy). Xếp lại theo khuôn Phase 0 (`Mã 3 + Tên 6 + Trạng thái 3`, hàng phụ `6+6`):

| Màn | Trước | Sau |
|---|---|---|
| Xuất xứ | `9+3` / `3` | `6+3+3` |
| Thuộc tính | `9+3` / `3` | `6+3+3` |
| Thương hiệu | `3+6+3` / `3` | `3+4+2+3` |
| Hãng sản xuất | `3+6+3` / `3+3` | `3+6+3` / `6+6` |
| Code đặt hàng | `9+3` / `9` | `5+4+3` |
| Đơn vị tính | `9+3` / `9+3+3` = **15** | `5+4+3` / `6+6` |

Đo trên trình duyệt: 11/11 màn, mọi hàng **cùng `top`** (không rớt dòng) và lấp **786–787/800px**
bề ngang thân popup.

**3. 🔴 Màn Loại file đính kèm mất sạch nút Tạo mới / Sửa / Xoá / Khoá** — FE khai
`hasAPermission('Quản lý danh mục LOẠI file đính kèm')` còn seeder + route BE là
`'Quản lý danh mục file đính kèm'`. **Lệch một chữ, gate chết im lặng**: vào được màn, bảng có dữ
liệu, console sạch, 77 ca API vẫn xanh (API đúng chuỗi quyền). Chỉ lộ khi ca e2e mới cố bấm
"Tạo mới" trên cả 11 màn. Sửa ở `pages/master-data/attachment-types/index.vue:300`.

**Bổ sung e2e:** `[UI] Bố cục popup 11 danh mục` — 11 ca, mỗi màn mở popup Tạo mới rồi đo số dòng
thật của từng `.form-row` và % bề ngang lấp được. Ca này bắt cả 2 loại lỗi trên: cột không đủ/thừa
12, **và** gate quyền chết (không bấm được Tạo mới thì không đo được).

**Kết quả chạy lại:** API `77 passed` · UI `18 passed` (7 ca cũ + 11 ca mới), `--workers=1`.

**Đang làm dở:** (không)
**Bước tiếp theo:** user nghiệm thu Phase 1; 2 repo đang có thay đổi **chưa commit** (4 file
`hrm-api`, 7 file `hrm-client`) — chờ user bảo commit.
**Blocked:** user cần cherry-pick `221cda7b2` (vá lỗi cú pháp `CatalogHistoryService`) về `gop_db`.

---

### Checkpoint — 21/09/2026 (ĐÃ COMMIT, chưa merge)

**Vừa hoàn thành:** commit toàn bộ phần tồn của Phase 1 lên nhánh `feat/p1-danh-muc-hang-hoa`.
User chốt **chỉ commit ở nhánh hiện tại, KHÔNG merge về `gop_db`**.

| Repo | Commit | Nội dung |
|---|---|---|
| `hrm-api` | `19027c245` | `company_id` lấy theo người tạo, không ghi đè khi sửa (4 service) |
| `hrm-client` | `810d2e089` | Vá gate quyền chết ở màn Loại file đính kèm |
| `hrm-client` | `371d63a5a` | Bỏ ô Công ty 2 màn + dọn bố cục 6 popup đủ 12 cột |

Sau commit: 2 repo sạch (0 file thay đổi); nhánh vượt `gop_db` local **16 commit** (api) /
**15 commit** (client). Đã kiểm `php -l` sạch cho `CatalogHistoryService` + 4 service; diff cân
bằng, không phình do CRLF.

**✅ `221cda7b2` KHÔNG cần cherry-pick nữa.** Trên `origin/gop_db` đã có người vá đúng lỗi cú pháp
`CatalogHistoryService` ở commit `68ecde36e "fix bug"`, và **hai bản vá y hệt nhau** — cùng hash
nội dung `1a05f29eb..277787f3b`, cùng thêm `]],` ở dòng 481. Merge lúc nào cũng sạch, không nhân
đôi dòng.

⚠️ **`origin/gop_db` đã đi trước**: +3 commit (`hrm-api`), +6 commit (`hrm-client` — sửa **119
file**: migrate SmartFilterPanel cho các màn Finance, đổi URL `regulation-config`). Khi nào merge
thì phải `pull` `gop_db` trước và **chạy lại e2e**, vì bộ lọc dùng chung vừa bị đụng.

⚠️ **Bộ e2e không nằm trong git** — 77 ca API + 18 ca UI ở `HRM/e2e/` chỉ có trên máy, không theo
commit nào.

**Đang làm dở:** (không)
**Bước tiếp theo:** user nghiệm thu → quyết định thời điểm merge về `gop_db`.
**Blocked:** (không)
