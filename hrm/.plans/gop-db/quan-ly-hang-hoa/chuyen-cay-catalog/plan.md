# Phase 2d — Cây catalog (Chương · Mục · Tiểu mục) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển 3 danh mục Chương / Mục / Tiểu mục (bảng ERP `chapters` / `job_groups` / `job_clusters`) sang HRM dưới gốc mới *Lĩnh vực Công ty kinh doanh*, ẩn hoàn toàn dữ liệu cũ, để người dùng khai cây catalog trước khi làm màn hàng hoá.

**Architecture:** BE theo khuôn danh mục Xe (Phase 2b) trên nền `BaseCatalog*` của module `MasterData`: mỗi cấp = Entity (có **global scope** loại data cũ) + Service + Request + Controller + Resource, route khai bằng 1 vòng lặp. FE theo khuôn màn `vehicle-brands` / `vehicle-models` (`vehicleCatalogScreenMixin` + `vehicleCatalogModalMixin`), ô chọn cha lọc dây chuyền tại máy khách.

**Tech Stack:** Laravel 8 / PHP 7.4 (`/opt/homebrew/opt/php@7.4/bin/php`), MySQL 8, Nuxt 2 / Vue 2 (node 12, heap 8192), Playwright (Node 20).

**Spec:** `design.md` (cùng thư mục) + `../man-danh-muc-hang-hoa/design.md` §30, §33w, §35h.

## Global Constraints

- Repo: `HRM/hrm-api`, `HRM/hrm-client` — nhánh `feat/p2d-cay-catalog` tách từ `gop_db` (chốt ở bước xin phép).
- KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`; đọc ghi thẳng bảng ERP, giữ nguyên `id`.
- Trạng thái 3 bảng ERP: `1` = Hoạt động, `0` = Khoá. `internal_business_scopes`: `1` / `2`.
- Tên tối đa 64 ký tự; unique theo cha, chỉ so bản ghi `status = 1`; cấm `,` `:` (rule nền).
- Quyền: 1670 `Xem danh mục chương` · 1671 `Quản lý danh mục chương` · 1672 `Xem danh mục mục` · 1673 `Quản lý danh mục mục` · 1674 `Xem danh mục tiểu mục` · 1675 `Quản lý danh mục tiểu mục`; type 9, group `Danh mục hàng hóa`, guard `api`.
- Super admin KHÔNG bypass — xét đúng quyền được gán.
- Mọi file sửa hàng loạt giữ EOL từng dòng (`git diff --numstat` không có dòng xoá thừa).
- FE: kiểm bằng Playwright MCP, đo bằng số từ DOM. KHÔNG tự chạy cả bộ e2e (chỉ khi user yêu cầu); vẫn viết spec.
- Không bắt chước 2 lỗi có sẵn: `order-codes/index.vue:485-494` (so `status === 2`) và `AddProductFamilyModal.vue:222-224` (gửi sai khoá lọc cha).

## Review Focus

1. **Data cũ lọt ra HRM** — mở `/{id}` của 1 chương cũ (id ≤ 65) phải 404; `getAll` Mục không được trả Mục thuộc chương cũ; ô chọn cha không được nhận id cũ (422). → test ở Task 2.
2. **Khoá Lĩnh vực đang có Chương hoạt động** — phải bị chặn ở cả nút Khoá lẫn form Sửa đổi trạng thái; xoá Lĩnh vực có Chương phải bị chặn. → test ở Task 4.
3. **Mở khoá sinh trùng tên** trong cùng cha → 400. → test ở Task 3.
4. **Đổi cha cấp trên trong popup Tiểu mục** — Mục đang chọn không còn thuộc Chương mới phải bị xoá khỏi ô; gửi cặp Chương/Mục lệch → BE 422. → test Task 3 (BE) + Task 7 (đo DOM).
5. **Trạng thái 0 bị biến thành 1** khi mở Sửa rồi Lưu (dùng `||`) — popup phải giữ 0. → đo ở Task 7.

---

### Task 0: Nhánh + migration nền

**Files:**
- Create: `hrm-api/Modules/MasterData/Database/Migrations/2026_10_04_000001_prepare_chapters_for_business_catalog.php`

**Interfaces:** Produces cột `chapters.internal_business_scope_id` (bigint unsigned nullable, FK `internal_business_scopes.id`), `chapters.scope_id` nullable.

- [ ] **Step 1: Tạo nhánh ở cả 2 repo**

```bash
cd HRM/hrm-api && git checkout gop_db && git pull --ff-only && git checkout -b feat/p2d-cay-catalog
cd ../hrm-client && git checkout gop_db && git pull --ff-only && git checkout -b feat/p2d-cay-catalog
```

- [ ] **Step 2: Viết migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Phase 2d — cây catalog đổi gốc từ `scopes` (ERP) sang `internal_business_scopes` (HRM).
 *
 *  - Thêm `internal_business_scope_id`: gốc MỚI của Chương. Chương cũ (65 dòng) để NULL ⇒ entity HRM
 *    ẩn chúng bằng global scope (design.md D3) — KHÔNG xoá, ERP còn đọc qua product_group_classifies.
 *  - Bỏ NOT NULL của `scope_id` (giữ FK): chương mới khai ở HRM không thuộc lĩnh vực cũ nào (H4).
 *
 * ERP không phải sửa dòng nào: form ERP vẫn gửi scope_id như cũ.
 */
class PrepareChaptersForBusinessCatalog extends Migration
{
    public function up(): void
    {
        Schema::table('chapters', function (Blueprint $table) {
            $table->unsignedBigInteger('scope_id')->nullable()->change();
            $table->unsignedBigInteger('internal_business_scope_id')->nullable()->after('scope_id');
            $table->foreign('internal_business_scope_id')->references('id')->on('internal_business_scopes');
        });
    }

    public function down(): void
    {
        Schema::table('chapters', function (Blueprint $table) {
            $table->dropForeign(['internal_business_scope_id']);
            $table->dropColumn('internal_business_scope_id');
        });
        // Không trả scope_id về NOT NULL: sẽ hỏng nếu đã có chương mới scope_id = NULL.
    }
}
```

- [ ] **Step 3: Chạy migration vào DB local `hrm_erp`, kiểm DDL**

```bash
cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear && /opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=Modules/MasterData/Database/Migrations/2026_10_04_000001_prepare_chapters_for_business_catalog.php
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo array_values((array)DB::select("SHOW CREATE TABLE chapters")[0])[1];'
```
Expected: `scope_id bigint unsigned DEFAULT NULL`, có `internal_business_scope_id` + FK `chapters_internal_business_scope_id_foreign`; `chapters_scope_id_foreign` vẫn còn. `select count(*) from chapters` = 65 (không đổi).

- [ ] **Step 4: Commit**

```bash
git add Modules/MasterData/Database/Migrations/2026_10_04_000001_prepare_chapters_for_business_catalog.php
git commit -m "[gop_db] Cây catalog P2d: chapters thêm internal_business_scope_id, scope_id nullable"
```

---

### Task 1: Entity 3 cấp + global scope ẩn data cũ

**Files:**
- Create: `hrm-api/Modules/MasterData/Entities/BusinessCatalog/Chapter.php`
- Create: `hrm-api/Modules/MasterData/Entities/BusinessCatalog/JobGroup.php`
- Create: `hrm-api/Modules/MasterData/Entities/BusinessCatalog/JobCluster.php`
- Test: `hrm-api/Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php`

**Interfaces:**
- Consumes: `BaseCatalogModel`, `Vehicle\Concerns\PreloadsChildrenFlag`, `Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope`.
- Produces: `Chapter::businessScope()` (belongsTo InternalBusinessScope), `Chapter::jobGroups()`; `JobGroup::chapter()`, `JobGroup::clusters()`; `JobCluster::jobGroup()`. Global scope tên `business_catalog_tree`. Hằng `STATUS_ACTIVE = 1`, `STATUS_INACTIVE = 0`.

- [ ] **Step 1: Viết test hỏng**

```php
<?php

namespace Modules\MasterData\Tests\Feature;

use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Entities\BusinessCatalog\JobCluster;
use Modules\MasterData\Entities\BusinessCatalog\JobGroup;
use Tests\TestCase;

/**
 * Phase 2d — cây catalog Chương / Mục / Tiểu mục trên 3 bảng ERP.
 * Chạy trên DB dev: mọi bản ghi mang TEST_TOKEN và bị dọn ở tearDown (con -> cha).
 */
class BusinessCatalogTreeTest extends TestCase
{
    private const TEST_TOKEN = 'T9ZCAT';

    protected function tearDown(): void
    {
        $like = '%' . self::TEST_TOKEN . '%';
        DB::table('job_clusters')->where('name', 'like', $like)->delete();
        DB::table('job_groups')->where('name', 'like', $like)->delete();
        DB::table('chapters')->where('name', 'like', $like)->delete();
        DB::table('internal_business_scopes')->where('name', 'like', $like)->delete();
        parent::tearDown();
    }

    protected function scope(array $attrs = []): InternalBusinessScope
    {
        return InternalBusinessScope::create(array_merge([
            'code' => 'LVCTKD.' . substr(uniqid(), -4),
            'name' => self::TEST_TOKEN . ' LV ' . uniqid(),
            'status' => InternalBusinessScope::STATUS_ACTIVE,
        ], $attrs));
    }

    protected function employeeId(): int
    {
        return (int) DB::table('employees')->value('id');
    }

    protected function chapter(InternalBusinessScope $scope, array $attrs = []): Chapter
    {
        return Chapter::create(array_merge([
            'name' => self::TEST_TOKEN . ' C ' . uniqid(),
            'internal_business_scope_id' => $scope->id,
            'status' => Chapter::STATUS_ACTIVE,
            'created_by' => $this->employeeId(),
        ], $attrs));
    }

    protected function group(Chapter $chapter, array $attrs = []): JobGroup
    {
        return JobGroup::create(array_merge([
            'name' => self::TEST_TOKEN . ' M ' . uniqid(),
            'chapter_id' => $chapter->id,
            'status' => JobGroup::STATUS_ACTIVE,
            'created_by' => $this->employeeId(),
        ], $attrs));
    }

    protected function cluster(JobGroup $group, array $attrs = []): JobCluster
    {
        return JobCluster::create(array_merge([
            'name' => self::TEST_TOKEN . ' TM ' . uniqid(),
            'group_id' => $group->id,
            'status' => JobCluster::STATUS_ACTIVE,
            'created_by' => $this->employeeId(),
        ], $attrs));
    }

    public function test_data_cu_bi_an_o_ca_3_cap()
    {
        $oldChapterId = (int) DB::table('chapters')->whereNull('internal_business_scope_id')->value('id');
        $oldGroupId = (int) DB::table('job_groups')->where('chapter_id', $oldChapterId)->value('id');
        $this->assertGreaterThan(0, $oldChapterId, 'DB dev phải còn chương cũ để kiểm');

        $this->assertNull(Chapter::find($oldChapterId));
        if ($oldGroupId) {
            $this->assertNull(JobGroup::find($oldGroupId));
        }
        $this->assertSame(0, JobCluster::whereHas('jobGroup', function ($q) use ($oldChapterId) {
            $q->withoutGlobalScopes()->where('chapter_id', $oldChapterId);
        })->count());
    }

    public function test_cay_moi_hien_du_3_cap()
    {
        $cluster = $this->cluster($this->group($this->chapter($this->scope())));

        $this->assertNotNull(JobCluster::find($cluster->id));
        $this->assertSame($cluster->jobGroup->chapter->businessScope->id, $cluster->jobGroup->chapter->internal_business_scope_id);
    }

    public function test_dem_con_dung_tung_cap()
    {
        $scope = $this->scope();
        $chapter = $this->chapter($scope);
        $group = $this->group($chapter);
        $this->cluster($group, ['status' => JobCluster::STATUS_INACTIVE]);

        $this->assertSame(1, $chapter->childrenCount());
        $this->assertSame(1, $chapter->activeChildrenCount());
        $this->assertSame(1, $group->childrenCount());
        $this->assertSame(0, $group->activeChildrenCount(), 'Tiểu mục đang khoá không tính là con hoạt động');
        $this->assertFalse($chapter->fresh()->isCanDelete());
        $this->assertFalse($chapter->fresh()->isCanLock());
        $this->assertTrue($group->fresh()->isCanLock());
    }
}
```

- [ ] **Step 2: Chạy — phải FAIL (class not found)**

Run: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php`
Expected: FAIL `Class "Modules\MasterData\Entities\BusinessCatalog\Chapter" not found`.

- [ ] **Step 3: Viết 3 entity**

`Chapter.php`:
```php
<?php

namespace Modules\MasterData\Entities\BusinessCatalog;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;
use Modules\MasterData\Entities\Vehicle\Concerns\PreloadsChildrenFlag;

/**
 * Chương — cấp 2 cây catalog kinh doanh, bảng ERP `chapters`. Cha: Lĩnh vực Công ty kinh doanh.
 *
 * ⚠️ Global scope `business_catalog_tree` ẨN 65 chương cũ (gốc `scopes` ERP, `internal_business_scope_id`
 * NULL) — design.md D3. Không xoá vì ERP còn đọc qua `product_group_classifies`. Mọi đường HRM (danh
 * sách, getAll, mở theo id, rule cha) đi qua entity này nên tự loại data cũ.
 * Trạng thái 1/0 theo ERP; không có `code`, `description`.
 */
class Chapter extends BaseCatalogModel
{
    use PreloadsChildrenFlag;

    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'chapters';

    protected $fillable = [
        'name', 'internal_business_scope_id', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at',
    ];

    protected static function booted()
    {
        static::addGlobalScope('business_catalog_tree', function (Builder $query) {
            $query->whereNotNull('chapters.internal_business_scope_id');
        });
    }

    /** ⚠️ KHÔNG đặt tên `scope()` — dễ lẫn với cơ chế local scope (`scopeXxx`) của Eloquent */
    public function businessScope()
    {
        return $this->belongsTo(InternalBusinessScope::class, 'internal_business_scope_id');
    }

    public function jobGroups()
    {
        return $this->hasMany(JobGroup::class, 'chapter_id');
    }

    public function parentCatalog()
    {
        return $this->businessScope;
    }

    /** Phải khớp `ChapterService::childrenExistsSql()` */
    public function childrenCount(): int
    {
        return DB::table('job_groups')->where('chapter_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return DB::table('job_groups')->where('chapter_id', $this->id)
            ->where('status', JobGroup::STATUS_ACTIVE)->count();
    }
}
```

`JobGroup.php`:
```php
<?php

namespace Modules\MasterData\Entities\BusinessCatalog;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;
use Modules\MasterData\Entities\Vehicle\Concerns\PreloadsChildrenFlag;

/**
 * Mục — cấp 3 cây catalog kinh doanh, bảng ERP `job_groups` (tên cũ "Nhóm công việc", đổi nhãn §33w).
 * Cha: Chương (`chapter_id`). Global scope: chỉ Mục có Chương thuộc cây mới (design.md D3).
 */
class JobGroup extends BaseCatalogModel
{
    use PreloadsChildrenFlag;

    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'job_groups';

    protected $fillable = [
        'name', 'chapter_id', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at',
    ];

    protected static function booted()
    {
        static::addGlobalScope('business_catalog_tree', function (Builder $query) {
            $query->whereExists(function ($q) {
                $q->select(DB::raw(1))->from('chapters as gs_c')
                    ->whereColumn('gs_c.id', 'job_groups.chapter_id')
                    ->whereNotNull('gs_c.internal_business_scope_id');
            });
        });
    }

    public function chapter()
    {
        return $this->belongsTo(Chapter::class, 'chapter_id');
    }

    public function clusters()
    {
        return $this->hasMany(JobCluster::class, 'group_id');
    }

    public function parentCatalog()
    {
        return $this->chapter;
    }

    /** Phải khớp `JobGroupService::childrenExistsSql()` */
    public function childrenCount(): int
    {
        return DB::table('job_clusters')->where('group_id', $this->id)->count();
    }

    public function activeChildrenCount(): int
    {
        return DB::table('job_clusters')->where('group_id', $this->id)
            ->where('status', JobCluster::STATUS_ACTIVE)->count();
    }
}
```

`JobCluster.php`:
```php
<?php

namespace Modules\MasterData\Entities\BusinessCatalog;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\ProductClassification\BaseCatalogModel;

/**
 * Tiểu mục — cấp 4 (lá) cây catalog kinh doanh, bảng ERP `job_clusters` (tên cũ "Cụm công việc").
 * ⚠️ Cột cha là `group_id` nhưng trỏ `job_groups`, KHÔNG phải `groups` (nhóm hàng hoá).
 * Global scope: chỉ Tiểu mục có Mục thuộc cây mới (design.md D3).
 *
 * Chưa có "con": hàng hoá gắn vào Tiểu mục (`product_business_catalogs`) làm ở màn hàng hoá — khi đó
 * bổ sung vào `childrenCount()` để chặn xoá.
 */
class JobCluster extends BaseCatalogModel
{
    const STATUS_ACTIVE = 1;
    const STATUS_INACTIVE = 0;

    protected $table = 'job_clusters';

    protected $fillable = [
        'name', 'group_id', 'status', 'created_by', 'updated_by', 'created_at', 'updated_at',
    ];

    protected static function booted()
    {
        static::addGlobalScope('business_catalog_tree', function (Builder $query) {
            $query->whereExists(function ($q) {
                $q->select(DB::raw(1))->from('job_groups as gs_g')
                    ->join('chapters as gs_c', 'gs_c.id', '=', 'gs_g.chapter_id')
                    ->whereColumn('gs_g.id', 'job_clusters.group_id')
                    ->whereNotNull('gs_c.internal_business_scope_id');
            });
        });
    }

    public function jobGroup()
    {
        return $this->belongsTo(JobGroup::class, 'group_id');
    }

    public function parentCatalog()
    {
        return $this->jobGroup;
    }

    public function childrenCount(): int
    {
        return 0;
    }

    public function activeChildrenCount(): int
    {
        return 0;
    }
}
```

- [ ] **Step 4: Chạy — PASS**

Run: như Step 2. Expected: `OK (3 tests, …)`.
Nếu `created_by` FK lỗi: kiểm `BaseModel` hook ghi `created_by` — giá trị phải là `employees.id`.

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Entities/BusinessCatalog Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php
git commit -m "[gop_db] Cây catalog P2d: entity Chương/Mục/Tiểu mục + global scope ẩn data cũ"
```

---

### Task 2: Service + Request + Resource + Controller + route + quyền + lịch sử + xuất Excel

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/BusinessCatalog/{ChapterService,JobGroupService,JobClusterService}.php`
- Create: `hrm-api/Modules/MasterData/Http/Requests/BusinessCatalog/{ChapterRequest,JobGroupRequest,JobClusterRequest}.php`
- Create: `hrm-api/Modules/MasterData/Transformers/BusinessCatalog/{ChapterResource,JobGroupResource,JobClusterResource}.php`
- Create: `hrm-api/Modules/MasterData/Http/Controllers/V1/BusinessCatalog/{ChapterController,JobGroupController,JobClusterController}.php`
- Modify: `hrm-api/Modules/MasterData/Routes/api.php` (sau khối `$vehicleCatalogs`, trước comment khối kế tiếp ~dòng 184)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sau dòng 1567 `id 1651`)
- Modify: `hrm-api/app/Services/CatalogHistoryService.php` (`const TABLES`, sau mục `vehicle_*`)
- Modify: `hrm-api/app/ExcelExport/ExportColumnRegistry.php` (`const COLUMNS`, sau `vehicle_*`)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php` (thêm ca)

**Interfaces:**
- Consumes: Task 1 entities; `BaseCatalogService/Request/Controller/Resource`; `SelectsChildrenFlag`; `ChecksParentCatalog`; `BlocksDuplicateNameOnUnlock`.
- Produces endpoints `/api/v1/master-data/{chapters|job-groups|job-clusters}` gồm `getAll`, `export`, `index`, `/{catalog}`, POST, PUT, DELETE, `/{catalog}/lock`, `/{catalog}/unlock`.
  - Resource Chương: `internal_business_scope_id`, `internal_business_scope_name`, `internal_business_scope_locked`.
  - Resource Mục: + `chapter_id`, `chapter_name`, `chapter_locked`, `internal_business_scope_id`, `internal_business_scope_name`.
  - Resource Tiểu mục: + `group_id`, `group_name`, `group_locked`, `chapter_id`, `chapter_name`, `internal_business_scope_id`, `internal_business_scope_name`.
  - `getAll` Mục trả thêm `internal_business_scope_id`; `getAll` Tiểu mục trả thêm `chapter_id`, `internal_business_scope_id`.
  - Lọc danh sách: Chương `internal_business_scope_id`; Mục `internal_business_scope_id`, `chapter_id`; Tiểu mục `internal_business_scope_id`, `chapter_id`, `group_id` (mảng hoặc số).

- [ ] **Step 1: Thêm ca test hỏng vào `BusinessCatalogTreeTest`**

```php
    /** Chạy rule FormRequest không qua HTTP (khuôn ProductClassificationCatalogTest) */
    private function rules(string $requestClass, array $payload, string $method = 'POST'): array
    {
        $formRequest = $requestClass::create('/', $method, $payload);
        $formRequest->setContainer(app())->setRedirector(app('redirect'));
        $formRequest->setRouteResolver(function () {
            return app('router')->getRoutes()->match(\Illuminate\Http\Request::create('/', 'GET'));
        });
        $v = \Validator::make($payload, $formRequest->rules(), $formRequest->messages(), $formRequest->attributes());

        return $v->errors()->toArray();
    }

    public function test_chuong_khong_nhan_linh_vuc_dang_khoa()
    {
        $scope = $this->scope(['status' => InternalBusinessScope::STATUS_INACTIVE]);
        $errors = $this->rules(\Modules\MasterData\Http\Requests\BusinessCatalog\ChapterRequest::class, [
            'name' => self::TEST_TOKEN . ' X', 'internal_business_scope_id' => $scope->id,
        ]);
        $this->assertArrayHasKey('internal_business_scope_id', $errors);
    }

    public function test_muc_khong_nhan_chuong_cu()
    {
        $oldChapterId = (int) DB::table('chapters')->whereNull('internal_business_scope_id')->value('id');
        $errors = $this->rules(\Modules\MasterData\Http\Requests\BusinessCatalog\JobGroupRequest::class, [
            'name' => self::TEST_TOKEN . ' X', 'chapter_id' => $oldChapterId,
        ]);
        $this->assertArrayHasKey('chapter_id', $errors);
    }

    public function test_ten_unique_theo_cha_va_toi_da_64()
    {
        $scope = $this->scope();
        $c1 = $this->chapter($scope);
        $name = $c1->name;
        $cls = \Modules\MasterData\Http\Requests\BusinessCatalog\ChapterRequest::class;

        $this->assertArrayHasKey('name', $this->rules($cls, ['name' => $name, 'internal_business_scope_id' => $scope->id]));
        $this->assertArrayNotHasKey('name', $this->rules($cls, ['name' => $name, 'internal_business_scope_id' => $this->scope()->id]));
        $this->assertArrayHasKey('name', $this->rules($cls, ['name' => str_repeat('a', 65), 'internal_business_scope_id' => $scope->id]));
    }

    public function test_tieu_muc_gui_cap_chuong_muc_lech_thi_422()
    {
        $scope = $this->scope();
        $groupOfC1 = $this->group($this->chapter($scope));
        $c2 = $this->chapter($scope);
        $errors = $this->rules(\Modules\MasterData\Http\Requests\BusinessCatalog\JobClusterRequest::class, [
            'name' => self::TEST_TOKEN . ' X', 'chapter_id' => $c2->id, 'group_id' => $groupOfC1->id,
        ]);
        $this->assertArrayHasKey('group_id', $errors);
    }

    public function test_getall_muc_loc_theo_chuong_va_tra_khoa_cha()
    {
        $scope = $this->scope();
        $c1 = $this->chapter($scope);
        $g1 = $this->group($c1);
        $this->group($this->chapter($scope));

        $rows = app(\Modules\MasterData\Services\BusinessCatalog\JobGroupService::class)
            ->getAll(new \Illuminate\Http\Request(['chapter_id' => $c1->id]));
        $this->assertSame([$g1->id], $rows->pluck('id')->map('intval')->all());
        $this->assertSame((int) $scope->id, (int) $rows->first()->internal_business_scope_id);
    }
```

- [ ] **Step 2: Chạy — FAIL (class not found)**

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php`

- [ ] **Step 3: Service**

`ChapterService.php`:
```php
<?php

namespace Modules\MasterData\Services\BusinessCatalog;

use Illuminate\Http\Request;
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Services\ProductClassification\BaseCatalogService;
use Modules\MasterData\Services\Vehicle\Concerns\SelectsChildrenFlag;

/** Chương — bảng ERP `chapters`, cha Lĩnh vực Công ty kinh doanh. */
class ChapterService extends BaseCatalogService
{
    use SelectsChildrenFlag;

    protected function modelClass(): string { return Chapter::class; }
    protected function table(): string { return 'chapters'; }
    protected function catalogLabel(): string { return 'chương'; }
    protected function hasCodeField(): bool { return false; }
    protected function hasDescriptionField(): bool { return false; }

    protected function listRelations(): array
    {
        return ['businessScope:id,name,status'];
    }

    protected function applyOwnFilters($query, Request $request)
    {
        if ($request->filled('internal_business_scope_id')) {
            $query->whereIn('chapters.internal_business_scope_id', (array) $request->internal_business_scope_id);
        }

        return $query;
    }

    /** KHÔNG gọi parent: nền thêm `code`/`description` mà bảng ERP không có */
    protected function fillableFrom(Request $request): array
    {
        return [
            'name' => trim((string) $request->name),
            'internal_business_scope_id' => $request->internal_business_scope_id,
            'status' => $request->status ?? Chapter::STATUS_ACTIVE,
        ];
    }

    protected function sortableColumns(): array
    {
        return [
            'name' => 'chapters.name', 'status' => 'chapters.status',
            'created_at' => 'chapters.created_at', 'createdAt' => 'chapters.created_at',
            'updated_at' => 'chapters.updated_at', 'updatedAt' => 'chapters.updated_at',
        ];
    }

    protected function catalogColumns(): array
    {
        return ['name', 'internal_business_scope_id', 'status'];
    }

    protected function catalogDisplay(string $column, $value)
    {
        if ($column === 'internal_business_scope_id') {
            return $this->parentName(InternalBusinessScope::class, $value);
        }

        return parent::catalogDisplay($column, $value);
    }

    protected function childrenExistsSql(): string
    {
        return $this->existsIn('job_groups', 'chapter_id');
    }
}
```

`JobGroupService.php`:
```php
<?php

namespace Modules\MasterData\Services\BusinessCatalog;

use Illuminate\Http\Request;
use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Entities\BusinessCatalog\JobGroup;
use Modules\MasterData\Services\ProductClassification\BaseCatalogService;
use Modules\MasterData\Services\Vehicle\Concerns\SelectsChildrenFlag;

/** Mục — bảng ERP `job_groups`, cha Chương. */
class JobGroupService extends BaseCatalogService
{
    use SelectsChildrenFlag;

    protected function modelClass(): string { return JobGroup::class; }
    protected function table(): string { return 'job_groups'; }
    protected function catalogLabel(): string { return 'mục'; }
    protected function hasCodeField(): bool { return false; }
    protected function hasDescriptionField(): bool { return false; }

    protected function listRelations(): array
    {
        return ['chapter:id,name,status,internal_business_scope_id', 'chapter.businessScope:id,name,status'];
    }

    protected function applyOwnFilters($query, Request $request)
    {
        if ($request->filled('chapter_id')) {
            $query->whereIn('job_groups.chapter_id', (array) $request->chapter_id);
        }
        if ($request->filled('internal_business_scope_id')) {
            $ids = (array) $request->internal_business_scope_id;
            $query->whereHas('chapter', function ($q) use ($ids) {
                $q->whereIn('chapters.internal_business_scope_id', $ids);
            });
        }

        return $query;
    }

    /** Ô chọn Mục ở màn Tiểu mục + form hàng hoá lọc dây chuyền tại máy khách ⇒ trả kèm khoá Lĩnh vực */
    public function getAll(Request $request)
    {
        $query = $this->optionsQuery(JobGroup::query(), $request)
            ->select('job_groups.*')
            ->selectRaw('(select c.internal_business_scope_id from chapters c where c.id = job_groups.chapter_id) as internal_business_scope_id');
        if ($request->filled('chapter_id')) {
            $query->where('job_groups.chapter_id', $request->chapter_id);
        }

        return $this->withLockedFlag($query->orderBy('job_groups.name')->get());
    }

    protected function fillableFrom(Request $request): array
    {
        return [
            'name' => trim((string) $request->name),
            'chapter_id' => $request->chapter_id,
            'status' => $request->status ?? JobGroup::STATUS_ACTIVE,
        ];
    }

    protected function sortableColumns(): array
    {
        return [
            'name' => 'job_groups.name', 'status' => 'job_groups.status',
            'created_at' => 'job_groups.created_at', 'createdAt' => 'job_groups.created_at',
            'updated_at' => 'job_groups.updated_at', 'updatedAt' => 'job_groups.updated_at',
        ];
    }

    protected function catalogColumns(): array
    {
        return ['name', 'chapter_id', 'status'];
    }

    protected function catalogDisplay(string $column, $value)
    {
        if ($column === 'chapter_id') {
            return $this->parentName(Chapter::class, $value);
        }

        return parent::catalogDisplay($column, $value);
    }

    protected function childrenExistsSql(): string
    {
        return $this->existsIn('job_clusters', 'group_id');
    }
}
```

`JobClusterService.php`:
```php
<?php

namespace Modules\MasterData\Services\BusinessCatalog;

use Illuminate\Http\Request;
use Modules\MasterData\Entities\BusinessCatalog\JobCluster;
use Modules\MasterData\Entities\BusinessCatalog\JobGroup;
use Modules\MasterData\Services\ProductClassification\BaseCatalogService;

/** Tiểu mục — bảng ERP `job_clusters`, cha Mục (`group_id` → `job_groups`). */
class JobClusterService extends BaseCatalogService
{
    protected function modelClass(): string { return JobCluster::class; }
    protected function table(): string { return 'job_clusters'; }
    protected function catalogLabel(): string { return 'tiểu mục'; }
    protected function hasCodeField(): bool { return false; }
    protected function hasDescriptionField(): bool { return false; }

    protected function listRelations(): array
    {
        return [
            'jobGroup:id,name,status,chapter_id',
            'jobGroup.chapter:id,name,status,internal_business_scope_id',
            'jobGroup.chapter.businessScope:id,name,status',
        ];
    }

    protected function applyOwnFilters($query, Request $request)
    {
        if ($request->filled('group_id')) {
            $query->whereIn('job_clusters.group_id', (array) $request->group_id);
        }
        if ($request->filled('chapter_id')) {
            $ids = (array) $request->chapter_id;
            $query->whereHas('jobGroup', function ($q) use ($ids) {
                $q->whereIn('job_groups.chapter_id', $ids);
            });
        }
        if ($request->filled('internal_business_scope_id')) {
            $ids = (array) $request->internal_business_scope_id;
            $query->whereHas('jobGroup.chapter', function ($q) use ($ids) {
                $q->whereIn('chapters.internal_business_scope_id', $ids);
            });
        }

        return $query;
    }

    public function getAll(Request $request)
    {
        $query = $this->optionsQuery(JobCluster::query(), $request)
            ->select('job_clusters.*')
            ->selectRaw('(select g.chapter_id from job_groups g where g.id = job_clusters.group_id) as chapter_id')
            ->selectRaw('(select c.internal_business_scope_id from job_groups g join chapters c on c.id = g.chapter_id where g.id = job_clusters.group_id) as internal_business_scope_id');
        if ($request->filled('group_id')) {
            $query->where('job_clusters.group_id', $request->group_id);
        }

        return $this->withLockedFlag($query->orderBy('job_clusters.name')->get());
    }

    protected function fillableFrom(Request $request): array
    {
        return [
            'name' => trim((string) $request->name),
            'group_id' => $request->group_id,
            'status' => $request->status ?? JobCluster::STATUS_ACTIVE,
        ];
    }

    protected function sortableColumns(): array
    {
        return [
            'name' => 'job_clusters.name', 'status' => 'job_clusters.status',
            'created_at' => 'job_clusters.created_at', 'createdAt' => 'job_clusters.created_at',
            'updated_at' => 'job_clusters.updated_at', 'updatedAt' => 'job_clusters.updated_at',
        ];
    }

    protected function catalogColumns(): array
    {
        return ['name', 'group_id', 'status'];
    }

    protected function catalogDisplay(string $column, $value)
    {
        if ($column === 'group_id') {
            return $this->parentName(JobGroup::class, $value);
        }

        return parent::catalogDisplay($column, $value);
    }
}
```

- [ ] **Step 4: Request**

`ChapterRequest.php`:
```php
<?php

namespace Modules\MasterData\Http\Requests\BusinessCatalog;

use Illuminate\Validation\Rule;
use Modules\Assign\Entities\InternalBusinessScope\InternalBusinessScope;
use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Http\Requests\ProductClassification\BaseCatalogRequest;
use Modules\MasterData\Http\Requests\ProductClassification\Concerns\ChecksParentCatalog;

/** Validate Chương. Tên tối đa 64 = rule ERP (màn ERP cũ còn sửa được các dòng này). */
class ChapterRequest extends BaseCatalogRequest
{
    use ChecksParentCatalog;

    protected function table(): string { return 'chapters'; }
    protected function hasCodeField(): bool { return false; }
    protected function codePrefix(): string { return ''; }
    protected function statusRule(): array { return ['nullable', 'in:0,1']; }
    protected function catalogLabel(): string { return 'Chương'; }

    protected function ownRules(): array
    {
        $current = Chapter::find($this->currentId());

        return [
            'name' => [
                'required', 'max:64',
                Rule::unique('chapters', 'name')->ignore($this->currentId())
                    ->where('internal_business_scope_id', $this->internal_business_scope_id)
                    ->where('status', Chapter::STATUS_ACTIVE),
            ],
            'internal_business_scope_id' => [
                'required',
                $this->parentRule(InternalBusinessScope::class, 'Lĩnh vực Công ty kinh doanh',
                    $current ? $current->internal_business_scope_id : null),
            ],
        ];
    }

    protected function ownMessages(): array
    {
        return [
            'name.max' => 'Nhập tối đa 64 ký tự',
            'name.unique' => 'Đã tồn tại trong lĩnh vực này',
            'internal_business_scope_id.required' => 'Bắt buộc phải chọn',
        ];
    }

    public function attributes()
    {
        return parent::attributes() + ['internal_business_scope_id' => 'Lĩnh vực Công ty kinh doanh'];
    }
}
```

`JobGroupRequest.php`: như trên với `table()` `job_groups`, `catalogLabel()` `Mục`, rule:
```php
    protected function ownRules(): array
    {
        $current = JobGroup::find($this->currentId());

        return [
            'name' => [
                'required', 'max:64',
                Rule::unique('job_groups', 'name')->ignore($this->currentId())
                    ->where('chapter_id', $this->chapter_id)
                    ->where('status', JobGroup::STATUS_ACTIVE),
            ],
            'chapter_id' => [
                'required',
                // Chapter có global scope ⇒ id chương CŨ trả "không tồn tại"
                $this->parentRule(Chapter::class, 'Chương', $current ? $current->chapter_id : null),
            ],
        ];
    }

    protected function ownMessages(): array
    {
        return [
            'name.max' => 'Nhập tối đa 64 ký tự',
            'name.unique' => 'Đã tồn tại trong chương này',
            'chapter_id.required' => 'Bắt buộc phải chọn',
        ];
    }

    public function attributes()
    {
        return parent::attributes() + ['chapter_id' => 'Chương'];
    }
```
(use `Modules\MasterData\Entities\BusinessCatalog\{Chapter, JobGroup}`, `Illuminate\Validation\Rule`, `ChecksParentCatalog`.)

`JobClusterRequest.php`: `table()` `job_clusters`, `catalogLabel()` `Tiểu mục`, rule:
```php
    protected function ownRules(): array
    {
        $current = JobCluster::find($this->currentId());

        return [
            'name' => [
                'required', 'max:64',
                Rule::unique('job_clusters', 'name')->ignore($this->currentId())
                    ->where('group_id', $this->group_id)
                    ->where('status', JobCluster::STATUS_ACTIVE),
            ],
            // Chương chỉ để lọc dây chuyền, không lưu — nhưng nếu gửi thì phải khớp Mục
            'chapter_id' => ['nullable', 'integer'],
            'group_id' => [
                'required',
                $this->parentRule(JobGroup::class, 'Mục', $current ? $current->group_id : null),
                function ($attribute, $value, $fail) {
                    if (!$this->filled('chapter_id')) return;
                    $group = JobGroup::find($value);
                    if ($group && (int) $group->chapter_id !== (int) $this->chapter_id) {
                        $fail('Mục không thuộc Chương đã chọn');
                    }
                },
            ],
        ];
    }

    protected function ownMessages(): array
    {
        return [
            'name.max' => 'Nhập tối đa 64 ký tự',
            'name.unique' => 'Đã tồn tại trong mục này',
            'group_id.required' => 'Bắt buộc phải chọn',
        ];
    }

    public function attributes()
    {
        return parent::attributes() + ['group_id' => 'Mục', 'chapter_id' => 'Chương'];
    }
```

- [ ] **Step 5: Resource**

```php
<?php
// ChapterResource.php
namespace Modules\MasterData\Transformers\BusinessCatalog;

use Modules\MasterData\Transformers\ProductClassification\BaseCatalogResource;

class ChapterResource extends BaseCatalogResource
{
    protected function ownFields($request): array
    {
        return [
            'internal_business_scope_id' => $this->internal_business_scope_id ? (int) $this->internal_business_scope_id : null,
            'internal_business_scope_name' => optional($this->businessScope)->name,
            'internal_business_scope_locked' => $this->businessScope ? !$this->businessScope->isActive() : false,
        ];
    }
}
```
```php
<?php
// JobGroupResource.php
namespace Modules\MasterData\Transformers\BusinessCatalog;

use Modules\MasterData\Transformers\ProductClassification\BaseCatalogResource;

class JobGroupResource extends BaseCatalogResource
{
    protected function ownFields($request): array
    {
        $chapter = $this->chapter;
        $scope = $chapter ? $chapter->businessScope : null;

        return [
            'chapter_id' => $this->chapter_id ? (int) $this->chapter_id : null,
            'chapter_name' => optional($chapter)->name,
            'chapter_locked' => $chapter ? !$chapter->isActive() : false,
            'internal_business_scope_id' => $scope ? (int) $scope->id : null,
            'internal_business_scope_name' => optional($scope)->name,
        ];
    }
}
```
```php
<?php
// JobClusterResource.php
namespace Modules\MasterData\Transformers\BusinessCatalog;

use Modules\MasterData\Transformers\ProductClassification\BaseCatalogResource;

class JobClusterResource extends BaseCatalogResource
{
    protected function ownFields($request): array
    {
        $group = $this->jobGroup;
        $chapter = $group ? $group->chapter : null;
        $scope = $chapter ? $chapter->businessScope : null;

        return [
            'group_id' => $this->group_id ? (int) $this->group_id : null,
            'group_name' => optional($group)->name,
            'group_locked' => $group ? !$group->isActive() : false,
            'chapter_id' => $chapter ? (int) $chapter->id : null,
            'chapter_name' => optional($chapter)->name,
            'internal_business_scope_id' => $scope ? (int) $scope->id : null,
            'internal_business_scope_name' => optional($scope)->name,
        ];
    }
}
```

- [ ] **Step 6: Controller** — mỗi cấp 1 file, khuôn `VehicleBrandController` (đủ `show/store/update/delete/lock/unlock` type-hint entity, `use BlocksDuplicateNameOnUnlock`):

| File | entity / request / service / resource | `catalogLabel()` | `exportScreen()` | `exportFileName()` | `unlockUniqueScope($c)` |
|---|---|---|---|---|---|
| `ChapterController` | Chapter / ChapterRequest / ChapterService / ChapterResource | `chương` | `chapters` | `danh_sach_chuong` | `['internal_business_scope_id' => $c->internal_business_scope_id]` |
| `JobGroupController` | JobGroup / … | `mục` | `job_groups` | `danh_sach_muc` | `['chapter_id' => $c->chapter_id]` |
| `JobClusterController` | JobCluster / … | `tiểu mục` | `job_clusters` | `danh_sach_tieu_muc` | `['group_id' => $c->group_id]` |

Ví dụ đầy đủ `ChapterController.php`:
```php
<?php

namespace Modules\MasterData\Http\Controllers\V1\BusinessCatalog;

use Modules\MasterData\Entities\BusinessCatalog\Chapter;
use Modules\MasterData\Http\Controllers\V1\ProductClassification\BaseCatalogController;
use Modules\MasterData\Http\Controllers\V1\Vehicle\Concerns\BlocksDuplicateNameOnUnlock;
use Modules\MasterData\Http\Requests\BusinessCatalog\ChapterRequest;
use Modules\MasterData\Services\BusinessCatalog\ChapterService;
use Modules\MasterData\Transformers\BusinessCatalog\ChapterResource;

/** Chương — cấp 2 cây catalog kinh doanh, bảng ERP `chapters`. */
class ChapterController extends BaseCatalogController
{
    use BlocksDuplicateNameOnUnlock;

    public function __construct(ChapterService $service) { $this->service = $service; }

    protected function resourceClass(): string { return ChapterResource::class; }
    protected function catalogLabel(): string { return 'chương'; }
    protected function exportScreen(): string { return 'chapters'; }
    protected function exportFileName(): string { return 'danh_sach_chuong'; }

    protected function unlockUniqueScope($catalog): array
    {
        return ['internal_business_scope_id' => $catalog->internal_business_scope_id];
    }

    public function show(Chapter $catalog) { return $this->respondShow($catalog); }
    public function store(ChapterRequest $request) { return $this->respondStore($request); }
    public function update(ChapterRequest $request, Chapter $catalog) { return $this->respondUpdate($request, $catalog); }
    public function delete(Chapter $catalog) { return $this->respondDelete($catalog); }
    public function lock(Chapter $catalog) { return $this->respondLock($catalog); }
    public function unlock(Chapter $catalog) { return $this->respondUnlock($catalog); }
}
```

- [ ] **Step 7: Route** — chèn sau vòng `$vehicleCatalogs` trong `Modules/MasterData/Routes/api.php`:

```php
    /*
    | Cây catalog kinh doanh — Phase 2d (Chương · Mục · Tiểu mục) trên 3 bảng ERP.
    | Slug = tên bảng (`job-groups` / `job-clusters` dù nhãn là Mục / Tiểu mục — §33w giữ tên bảng).
    | Không làm Import đợt này ⇒ không khai route import.
    */
    $businessCatalogs = [
        'chapters' => ['ChapterController', 'chương'],
        'job-groups' => ['JobGroupController', 'mục'],
        'job-clusters' => ['JobClusterController', 'tiểu mục'],
    ];

    foreach ($businessCatalogs as $slug => [$controller, $label]) {
        $action = 'V1\\BusinessCatalog\\' . $controller;
        $viewPermission = 'Xem danh mục ' . $label;
        $managePermission = 'Quản lý danh mục ' . $label;

        Route::group(['prefix' => $slug], function () use ($action, $viewPermission, $managePermission) {
            Route::get('/getAll', $action . '@getAll');
            Route::get('/export', $action . '@export')
                ->middleware('checkPermission:' . $managePermission . '|' . $viewPermission);
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

- [ ] **Step 8: Quyền** — chèn sau dòng `id 1651` của seeder:

```php

        // Cây catalog kinh doanh — Phase 2d (04/10/2026). 1652-1656 đã giữ cho 5 quyền màn hàng hoá (§35b).
        Permission::create(['id' => 1670, 'guard_name' => 'api', 'name' => 'Xem danh mục chương', 'display_name' => 'Xem danh mục chương', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1671, 'guard_name' => 'api', 'name' => 'Quản lý danh mục chương', 'display_name' => 'Quản lý danh mục chương', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1672, 'guard_name' => 'api', 'name' => 'Xem danh mục mục', 'display_name' => 'Xem danh mục mục', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1673, 'guard_name' => 'api', 'name' => 'Quản lý danh mục mục', 'display_name' => 'Quản lý danh mục mục', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1674, 'guard_name' => 'api', 'name' => 'Xem danh mục tiểu mục', 'display_name' => 'Xem danh mục tiểu mục', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
        Permission::create(['id' => 1675, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tiểu mục', 'display_name' => 'Quản lý danh mục tiểu mục', 'group' => 'Danh mục hàng hóa', 'type' => 9]);
```
Kiểm trùng id + trùng tên (bỏ dấu, mọi guard):
```bash
grep -E "^\s*Permission::create" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | grep -oE "'id' => [0-9]+" | sort | uniq -d   # phải rỗng
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo DB::table("permissions")->whereIn("id",range(1657,1662))->count()," ",DB::table("permissions")->whereIn("name",["Xem danh mục chương","Quản lý danh mục chương","Xem danh mục mục","Quản lý danh mục mục","Xem danh mục tiểu mục","Quản lý danh mục tiểu mục"])->count();'   # phải "0 0" trước khi seed
```

- [ ] **Step 9: Lịch sử + xuất Excel**

`CatalogHistoryService::TABLES` thêm:
```php
        'chapters' => ['label' => 'chương', 'columns' => [
            'name' => 'Chương', 'internal_business_scope_id' => 'Lĩnh vực Công ty kinh doanh', 'status' => 'Trạng thái',
        ]],
        'job_groups' => ['label' => 'mục', 'columns' => [
            'name' => 'Mục', 'chapter_id' => 'Chương', 'status' => 'Trạng thái',
        ]],
        'job_clusters' => ['label' => 'tiểu mục', 'columns' => [
            'name' => 'Tiểu mục', 'group_id' => 'Mục', 'status' => 'Trạng thái',
        ]],
```
`ExportColumnRegistry::COLUMNS` thêm:
```php
        'chapters' => [
            'name' => 'Chương', 'internal_business_scope_name' => 'Lĩnh vực Công ty kinh doanh',
            'status_text' => 'Trạng thái', 'creator_name' => 'Người tạo', 'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật', 'updated_at' => 'Ngày cập nhật',
        ],
        'job_groups' => [
            'name' => 'Mục', 'chapter_name' => 'Chương', 'internal_business_scope_name' => 'Lĩnh vực Công ty kinh doanh',
            'status_text' => 'Trạng thái', 'creator_name' => 'Người tạo', 'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật', 'updated_at' => 'Ngày cập nhật',
        ],
        'job_clusters' => [
            'name' => 'Tiểu mục', 'group_name' => 'Mục', 'chapter_name' => 'Chương',
            'internal_business_scope_name' => 'Lĩnh vực Công ty kinh doanh',
            'status_text' => 'Trạng thái', 'creator_name' => 'Người tạo', 'created_at' => 'Ngày tạo',
            'updater_name' => 'Người cập nhật', 'updated_at' => 'Ngày cập nhật',
        ],
```

- [ ] **Step 10: Chạy test — PASS**, rồi seed quyền + xoá cache quyền

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/BusinessCatalogTreeTest.php
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/MasterData/Tests/Feature/ProductClassificationCatalogTest.php   # nền không vỡ
/opt/homebrew/opt/php@7.4/bin/php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
/opt/homebrew/opt/php@7.4/bin/php artisan permission:cache-reset
/opt/homebrew/opt/php@7.4/bin/php artisan route:list --path=master-data/job-clusters | head
```
Expected: cả 2 file OK; 9 route mỗi slug.

- [ ] **Step 11: Commit**

```bash
git add Modules/MasterData app Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
git commit -m "[gop_db] Cây catalog P2d: API Chương/Mục/Tiểu mục + 6 quyền 1670-1675 + lịch sử + xuất Excel"
```

---

### Task 3: Kiểm API thật (curl) — khoá/mở khoá/xoá/404 data cũ

**Files:** không sửa code (chỉ kiểm); sửa nếu lộ lỗi rồi thêm ca vào `BusinessCatalogTreeTest`.

- [ ] **Step 1:** Lấy token admin (`HRM/e2e/.auth/api.json`), chạy với `API=http://127.0.0.1:8000/api/v1/master-data`:
  1. `GET $API/chapters/1` (chương cũ) → **404**.
  2. Tạo Lĩnh vực test? KHÔNG — dùng 1 Lĩnh vực đang hoạt động có sẵn; `POST $API/chapters {name:"E2ECAT C1", internal_business_scope_id}` → 200.
  3. `POST $API/job-groups {name:"E2ECAT M1", chapter_id}` → 200; `POST $API/job-clusters {name:"E2ECAT T1", chapter_id, group_id}` → 200.
  4. `GET $API/chapters/{c}/lock` → **400** (còn Mục hoạt động). Khoá Tiểu mục → Mục → Chương theo thứ tự → 200 cả 3; `status` trong DB = 0.
  5. Tạo `E2ECAT M1` mới cùng chương (đã khoá chương ⇒ phải mở chương trước): mở khoá Chương → tạo Mục trùng tên `E2ECAT M1` → 200 → mở khoá Mục cũ → **400 "trùng tên"**.
  6. `DELETE $API/chapters/{c}` khi còn Mục → **400**. Xoá con → cha → 200.
  7. `GET $API/job-groups/getAll?chapter_id={c}` chỉ trả Mục của chương đó, có `internal_business_scope_id`.
- [ ] **Step 2:** Ghi kết quả từng ca vào `plan.md` mục "Nhật ký kiểm" cuối file. Lỗi nào lộ ⇒ thêm ca test PHPUnit tái hiện TRƯỚC khi sửa.

---

### Task 4: Lĩnh vực Công ty kinh doanh — chặn xoá/khoá khi có Chương

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/InternalBusinessScope/InternalBusinessScope.php` (`isCanDelete` ~60, `isCanLockUpdate` ~66)
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/InternalBusinessScopeController.php` (`delete` ~103)
- Test: `BusinessCatalogTreeTest.php` (thêm ca)

- [ ] **Step 1: Test hỏng**

```php
    public function test_linh_vuc_co_chuong_khong_xoa_khong_khoa()
    {
        $scope = $this->scope();
        $chapter = $this->chapter($scope);

        $this->assertFalse($scope->fresh()->isCanDelete());
        $this->assertFalse($scope->fresh()->isCanLockUpdate());

        $chapter->update(['status' => Chapter::STATUS_INACTIVE]);
        $this->assertTrue($scope->fresh()->isCanLockUpdate(), 'Chương đã khoá thì cho khoá lĩnh vực');
        $this->assertFalse($scope->fresh()->isCanDelete(), 'Còn chương (dù khoá) thì không xoá');
    }
```
Run → FAIL.

- [ ] **Step 2: Sửa entity**

```php
    /** Chương của cây catalog kinh doanh (Phase 2d) — chỉ chương gốc mới, đã có global scope */
    public function catalogChapters()
    {
        return $this->hasMany(\Modules\MasterData\Entities\BusinessCatalog\Chapter::class, 'internal_business_scope_id');
    }

    /** Có nơi nào đang dùng lĩnh vực này: Nhóm ngành hoặc Chương catalog */
    public function isUsed(): bool
    {
        return !$this->scopes()->doesntExist() || $this->catalogChapters()->exists();
    }

    public function isCanDelete()
    {
        return $this->isActive() && !$this->isUsed();
    }

    public function isCanLockUpdate()
    {
        // (giữ nguyên comment cũ về `hrm_scopes`)
        return $this->scopes()->where($this->scopes()->getModel()->getTable() . '.status', Scope::STATUS_ACTIVE)->doesntExist()
            && $this->catalogChapters()->where('chapters.status', \Modules\MasterData\Entities\BusinessCatalog\Chapter::STATUS_ACTIVE)->doesntExist();
    }
```
Controller `delete`: thay `if (!$internalBusinessScope->scopes()->doesntExist())` bằng `if ($internalBusinessScope->isUsed())` (giữ câu báo).

- [ ] **Step 3:** Chạy test → PASS; chạy `HRM/e2e/tests/assign/internal-business-scope.api.spec.ts` chỉ khi user yêu cầu (ghi chú lại).
- [ ] **Step 4: Commit** `"[gop_db] Cây catalog P2d: lĩnh vực Công ty kinh doanh chặn xoá/khoá khi có Chương"`

---

### Task 5: FE nền — tooltip, helper option, menu

**Files:**
- Modify: `hrm-client/utils/product-classification.js` (`CATALOG_TOOLTIPS`, ~dòng 52-90)
- Create: `hrm-client/utils/business-catalog.js`
- Modify: `hrm-client/components/subsystem-menu/master-data.js` (sau nhóm "Xe", trước mục "Lĩnh vực Công ty kinh doanh" ~dòng 211)

- [ ] **Step 1: Tooltip** (câu đã duyệt ở §36m, F9) — thêm vào `CATALOG_TOOLTIPS`:
```js
    // Cây catalog kinh doanh — Phase 2d (câu duyệt §36m / F9)
    catalogChapter: 'Cấp 2 — nhóm lớn trong một lĩnh vực.',
    catalogJobGroup: 'Cấp 3 — nhóm chi tiết trong một chương.',
    catalogJobCluster:
        'Cấp 4 — cấp cuối của catalog, nơi xếp hàng hoá. Hàng hoá phải gắn tới Tiểu mục; một hàng hoá gắn được nhiều nhánh.',
```
- [ ] **Step 2: Helper** `utils/business-catalog.js`:
```js
/**
 * Option cho 4 ô cây catalog kinh doanh (Lĩnh vực › Chương › Mục › Tiểu mục) — Phase 2d.
 * Giữ khoá cha để lọc dây chuyền tại máy khách (giống fetchVehicleOptions, nhưng Lĩnh vực nằm ở
 * module assign nên phải nhận ĐƯỜNG đầy đủ).
 */
export const TREE_SOURCES = {
    scope: 'assign/internal-business-scopes/getAll',
    chapter: 'master-data/chapters/getAll',
    jobGroup: 'master-data/job-groups/getAll',
    jobCluster: 'master-data/job-clusters/getAll',
}

export async function fetchTreeOptions(store, source, keepKeys = []) {
    const response = await store.dispatch('apiGetMethod', TREE_SOURCES[source])
    const rows = response?.data || response || []

    return rows.map((row) => {
        const option = { id: row.id, name: row.name }
        keepKeys.forEach((key) => {
            option[key] = row[key] === null || row[key] === undefined ? null : Number(row[key])
        })
        return option
    })
}

/** Lọc option theo khoá cha; chưa chọn cha ⇒ rỗng (ô con khoá lại) */
export function childrenOf(options, key, parentId) {
    if (!parentId) return []
    return options.filter((item) => Number(item[key]) === Number(parentId))
}
```
Kiểm nhanh: `assign/internal-business-scopes/getAll` trả mảng hay `{data}` — đọc `InternalBusinessScopeController@getAll`; nếu bọc khác thì sửa dòng `rows`.
- [ ] **Step 3: Menu** — thêm nhóm:
```js
    {
        // Cây catalog kinh doanh — Phase 2d. Gốc là "Lĩnh vực Công ty kinh doanh" (mục ngay dưới).
        // ⚠️ `subItems`, KHÔNG `children` (xem nhóm Xe).
        label: 'Catalog kinh doanh',
        icon: 'ri-node-tree',
        subItems: [
            { label: 'Chương', link: '/master-data/chapters', isShow: ['Quản lý danh mục chương', 'Xem danh mục chương'] },
            { label: 'Mục', link: '/master-data/job-groups', isShow: ['Quản lý danh mục mục', 'Xem danh mục mục'] },
            { label: 'Tiểu mục', link: '/master-data/job-clusters', isShow: ['Quản lý danh mục tiểu mục', 'Xem danh mục tiểu mục'] },
        ],
    },
```
- [ ] **Step 4: Commit** `"[gop_db] Cây catalog P2d: FE tooltip + helper option + menu"`

---

### Task 6: FE 3 màn danh sách + popup

**Files:**
- Create: `hrm-client/pages/master-data/chapters/{index.vue,AddChapterModal.vue}`
- Create: `hrm-client/pages/master-data/job-groups/{index.vue,AddJobGroupModal.vue}`
- Create: `hrm-client/pages/master-data/job-clusters/{index.vue,AddJobClusterModal.vue}`

**Interfaces:** Consumes Task 2 endpoints/fields, Task 5 helper + tooltip.

- [ ] **Step 1: Màn Chương** — chép `pages/master-data/vehicle-brands/index.vue` → `chapters/index.vue`, rồi thay đúng các chỗ sau:

| Chỗ | Giá trị mới |
|---|---|
| `table="vehicle_brands"`, `columnScreenKey`, `catalogHistoryTable` | `chapters` |
| `quickSearchPlaceholder` | `Tìm theo tên chương, người tạo` |
| `title`, `head()`, `pageTitle` | `Danh sách chương` |
| `itemLabel`, `catalogLabel` | `chương` |
| `catalogSlug` | `chapters` |
| `catalogModalId`, ref modal id | `add-chapter` |
| `catalogManagePermission` | `Quản lý danh mục chương` |
| `catalogExportFileName` | `danh_sach_chuong.xlsx` |
| `localStorageKey` / `pathsToKeep` | `master_data_chapters` / `['/master-data/chapters']` |
| `exportFieldsModalId` | `chapters-export-fields-modal` |
| id 2 confirm modal | `confirm-delete-chapters`, `confirm-toggle-lock-chapters` (đúng `confirm-<việc>-<catalogSlug>`) |
| `modal-id` lịch sử, `record-prefix` | `history-chapter`, `Chương` |
| import component + tag | `AddChapterModal` / `<add-chapter-modal>` |
| `initialStateForm` | bỏ `vehicle_manufact_id`, thêm `internal_business_scope_id: undefined` |
| `mounted` | `this.scopeOptions = await fetchTreeOptions(this.$store, 'scope')` (đổi `manufactOptions` → `scopeOptions`) |
| `filterFields` ô cha | `{ key: 'internal_business_scope_id', label: 'Lĩnh vực Công ty kinh doanh', type: 'select', options: this.scopeOptions }`; ô `name` label `Chương` |
| cột | bỏ `note`; `name` label `Chương`; `vehicle_manufact_name` → `internal_business_scope_name` label `Lĩnh vực Công ty kinh doanh` width 240px; slot `#cell-internal_business_scope_name`; xoá slot `#cell-note` |
| `exportFields` | `name` Chương · `internal_business_scope_name` Lĩnh vực Công ty kinh doanh · status_text · creator_name · created_at · updater_name · updated_at (khớp registry Task 2) |

Popup `AddChapterModal.vue` — chép `AddVehicleBrandModal.vue`, đổi: `modal-id="add-chapter"`, icon `ri-book-2-line`; tiêu đề `Xem chi tiết chương` / `Sửa chương` / `Tạo mới chương`; ô 1 `Chương` (`:hint="tooltip"`, `tooltip: CATALOG_TOOLTIPS.catalogChapter`, placeholder `Nhập tên chương`, `maxlength="64"`); ô 2 `Lĩnh vực Công ty kinh doanh` → `data.internal_business_scope_id`, options `scopeOptions` từ `fetchTreeOptions(this.$store, 'scope')`; **bỏ hàng Ghi chú**; bố cục 1 hàng đủ 12 cột: `Lĩnh vực Công ty kinh doanh` (`col-md-4`) · `Chương` (`col-md-5`) · `Trạng thái` (`col-md-3`). `SystemInfoSection entity-type="chapters"`. `emptyData/fillForm/buildPayload` chỉ còn `name`, `internal_business_scope_id`, `status` (giữ cách xử lý status 0). `afterLoadItem` dùng `withLockedParent(this.scopeOptions, data.internal_business_scope_id, data.internal_business_scope_name, data.internal_business_scope_locked)` (import từ `@/utils/vehicle-catalog.js`).

- [ ] **Step 2: Màn Mục** — chép `chapters/*` vừa làm → `job-groups/*`, thay `chương`→`mục`, `chapters`→`job-groups` (slug) / `job_groups` (bảng, columnScreenKey, history, entity-type), `add-chapter`→`add-job-group`, quyền `… danh mục mục`, file `danh_sach_muc.xlsx`, tooltip `catalogJobGroup`, placeholder `Nhập tên mục`. Thêm cấp Chương:
  - Màn: `initialStateForm` có `internal_business_scope_id`, `chapter_id`; `mounted` nạp `scopeOptions` + `chapterOptionsAll = await fetchTreeOptions(this.$store, 'chapter', ['internal_business_scope_id'])`; `filterFields` 2 ô cha: Lĩnh vực (`resetKeys: ['chapter_id']` — ⚠️ chỉ nếu panel dùng resetKeys để xoá con; nếu không thì xoá con trong `handleFilterChange`), Chương `options: childrenOf(this.chapterOptionsAll, 'internal_business_scope_id', this.filters.internal_business_scope_id)` — chưa chọn Lĩnh vực thì dùng `this.chapterOptionsAll`; cột `chapter_name` (Chương, 220px) + `internal_business_scope_name` (Lĩnh vực, 220px); export thêm `chapter_name`.
  - Popup: hàng 1 `Lĩnh vực` (6, chỉ để lọc, không gửi) + `Chương` (6, khoá khi chưa chọn Lĩnh vực, options `childrenOf(chapterOptions, 'internal_business_scope_id', data.internal_business_scope_id)`); hàng 2 `Mục` (8) + `Trạng thái` (4). `watch 'data.internal_business_scope_id'` bỏ `chapter_id` khi không còn hợp lệ (khuôn `AddVehicleModelModal` watch). `fillForm` lấy `internal_business_scope_id` từ resource. `afterLoadItem`: `withLockedParent` cho Chương kèm `{ internal_business_scope_id: data.internal_business_scope_id }`. `buildPayload`: `name`, `chapter_id`, `status`.
- [ ] **Step 3: Màn Tiểu mục** — chép `job-groups/*` → `job-clusters/*`, thay nhãn `tiểu mục`, slug `job-clusters`, bảng `job_clusters`, `add-job-cluster`, quyền `… danh mục tiểu mục`, file `danh_sach_tieu_muc.xlsx`, tooltip `catalogJobCluster`. Thêm cấp Mục:
  - Màn: filter 3 ô cha Lĩnh vực › Chương › Mục (`jobGroupOptionsAll = fetchTreeOptions(…, 'jobGroup', ['chapter_id','internal_business_scope_id'])`), cột `group_name` (Mục), `chapter_name`, `internal_business_scope_name`; export thêm `group_name`.
  - Popup: hàng 1 `Lĩnh vực` (4) · `Chương` (4) · `Mục` (4) lọc dây chuyền, 2 watch xoá con lệch; hàng 2 `Tiểu mục` (8) · `Trạng thái` (4). `buildPayload`: `name`, `chapter_id` (để BE kiểm cặp), `group_id`, `status`.
- [ ] **Step 4: Build nhanh** `cd hrm-client && NODE_OPTIONS=--max_old_space_size=8192 npx nuxt build --no-generate 2>&1 | tail -20` (node 12) — hoặc mở dev server đang chạy và xem console — không có lỗi compile.
- [ ] **Step 5: Commit** `"[gop_db] Cây catalog P2d: FE 3 màn Chương/Mục/Tiểu mục"`

---

### Task 7: Kiểm bằng Playwright MCP (bắt buộc trước khi báo xong)

- [ ] **Step 1:** Restart Nuxt + `rm -rf .nuxt/components` nếu báo "Can't resolve component". Đăng nhập admin, mở hub Danh mục chung: **đếm link** nhóm "Catalog kinh doanh" = 3 (đo DOM, không nhìn ảnh).
- [ ] **Step 2:** Màn Chương: tổng bản ghi ở phân trang = số chương có `internal_business_scope_id` trong DB (**0 dòng cũ lọt**). Tạo `E2ECAT C1` → hiện 1 dòng, cột Lĩnh vực đúng tên.
- [ ] **Step 3:** Popup Tiểu mục: chọn Lĩnh vực A → Chương C1 → Mục M1; đổi Lĩnh vực sang B ⇒ đo `data.chapter_id`/`data.group_id` = null và text 2 ô trống (Review Focus 4). Ô Mục `disabled` khi chưa chọn Chương.
- [ ] **Step 4:** Mở Sửa 1 bản ghi đang Khoá → Lưu không đổi gì ⇒ DB `status` vẫn 0 (Review Focus 5). Nút "Mở khoá" gọi đúng `/unlock` (đọc network).
- [ ] **Step 5:** Tài khoản không quyền (`.auth/user-nocost.json` hoặc tài khoản test bỏ 6 quyền): vào `/master-data/chapters` ⇒ 404 middleware; có quyền Xem không có Quản lý ⇒ không có nút Tạo mới / hành động sửa-xoá-khoá (đếm nút trong DOM).
- [ ] **Step 6:** Bố cục popup: mỗi hàng đủ 12 cột (đo `getBoundingClientRect` các `.col-md-*`), không ô lẻ. Bấm Lưu form rỗng ⇒ hiện lỗi **cùng lúc** ở mọi ô bắt buộc.
- [ ] **Step 7:** Dọn dữ liệu `E2ECAT*`. Ghi số đo vào "Nhật ký kiểm".

---

### Task 8: E2E spec (viết, KHÔNG tự chạy cả bộ)

**Files:**
- Create: `HRM/e2e/tests/master-data/business-catalog-tree.api.spec.ts`

- [ ] **Step 1:** Viết spec theo khuôn `vehicle-catalog.api.spec.ts` (prefix `E2ECAT`, `CLEAN_ORDER = ['job-clusters','job-groups','chapters']`, `beforeAll`/`afterAll` cleanup), các ca:
  1. `GET chapters/{id cũ}` → 404; `job-groups/getAll` không chứa Mục thuộc chương cũ.
  2. Tên unique theo cha: cùng tên ở 2 lĩnh vực → 200; cùng lĩnh vực → 422; 65 ký tự → 422.
  3. Khoá Chương còn Mục hoạt động → 400; khoá đủ từ lá lên → 200; DB status 0.
  4. Mở khoá sinh trùng tên → 400.
  5. Tiểu mục gửi cặp Chương/Mục lệch → 422.
  6. Xoá Lĩnh vực có Chương → 400; khoá Lĩnh vực có Chương hoạt động → 400 (endpoint `assign/internal-business-scopes`).
  7. Token không quyền (`.auth/user-nocost.json`): `GET chapters` → 403; `POST` → 403.
- [ ] **Step 2:** `npx tsc --noEmit -p HRM/e2e` (hoặc `npx playwright test --list business-catalog-tree`) để chắc spec biên dịch. Chạy thật chỉ khi user yêu cầu (`--project=api --no-deps --workers=1`).
- [ ] **Step 3:** `HRM/e2e` không trong git — chỉ lưu file, ghi đường dẫn vào STATUS.

---

### Task 9: Cập nhật hồ sơ

- [ ] `../SO-CHOT-VA-TON.md` §2: dòng **2d** → "🟢 code xong, chờ nghiệm thu" + nhánh + số commit.
- [ ] `.plans/gop-db/STATUS.md`: mục mới Phase 2d (nhánh, 6 quyền, migration, lỗi im lặng bắt được).
- [ ] `../man-danh-muc-hang-hoa/design.md` §35h: H2 trỏ sang thư mục này.

---

## Nhật ký kiểm

*(điền khi thực thi)*

### Task 3 — API thật (04/10/2026, cổng 8000, token admin)

| Ca | Kết quả |
|---|---|
| GET chương cũ id=1 | 404 ✅ |
| Tạo Chương/Mục/Tiểu mục dưới lĩnh vực "Công nghiệp" | 200 ×3 ✅ |
| Khoá Chương còn Mục hoạt động | 400 "Không thể khóa chương khi vẫn còn danh mục con đang hoạt động." ✅ |
| Khoá từ lá lên (Tiểu mục → Mục → Chương) | 200 ×3, DB status = 0 ✅ |
| Sửa Chương đang khoá | 400 "Dữ liệu đã thay đổi" (nền chung — CLAUDE.md muốn 423, ghi minor) |
| Mở khoá Chương → tạo Mục trùng tên bản đang khoá | 200 ✅ ; mở khoá bản cũ → 400 "trùng tên" ✅ ; tạo trùng lần 3 → 422 ✅ |
| Xoá Chương còn Mục | 400 ✅ |
| getAll Mục `?chapter_id=` | chỉ Mục hoạt động của chương đó, có `internal_business_scope_id` ✅ |
| Danh sách Chương | total 1 (0 chương cũ lọt) ✅ |
| Dọn | 0 dòng E2ECAT còn lại; 14 dòng `catalog_histories` |

Ghi chú: mở khoá bản ghi ĐANG hoạt động báo "cha đang bị khoá" — câu của nền `BaseCatalogController::respondUnlock`, có sẵn, không sửa.

### Task 7 — Playwright MCP (04/10/2026, :3000, user E2E Assign có quyền + user-nocost)

| Kiểm | Số đo |
|---|---|
| Menu nhóm "Catalog kinh doanh" mở ra | 3 link hiện: Chương `/master-data/chapters` · Mục `/master-data/job-groups` · Tiểu mục `/master-data/job-clusters`, y = 142/180/218 |
| Danh sách Tiểu mục | 11 cột: STT · Tiểu mục · Mục · Chương · Lĩnh vực · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật · Trạng thái · Hành động; dòng ra đủ tên 3 cấp cha; người tạo "E2E Assign - HN_KD2" |
| Popup Tạo Tiểu mục lúc mở | ô disabled [Lĩnh vực=false, Chương=true, Mục=true, Trạng thái=false]; 7 lĩnh vực hoạt động |
| Chọn Lĩnh vực "Công nghiệp" → Chương | Chương mở, chỉ còn chương của lĩnh vực đó; chọn Chương → Mục mở, chỉ còn mục của chương |
| Đổi Lĩnh vực sang "Dịch vụ ô tô" (Review Focus 4) | `chapter_id = null`, `group_id = null`, 2 ô hiện "Chọn", Mục khoá lại |
| Bố cục popup | 2 hàng, mỗi hàng tổng 12 cột |
| Lưu form trống | 2 lỗi hiện CÙNG LÚC ("Bắt buộc phải nhập" ở Tiểu mục + Mục), request 422 |
| Lưu thật | payload `{name, chapter_id, group_id, status:1}` → 200, dòng mới lên đầu bảng |
| Hành động theo dòng | đang hoạt động: edit · delete · lock · history; đang khoá: unlock · history (không sửa/xoá) |
| Xem bản ghi khoá (Review Focus 5) | đủ 3 cấp cha + Trạng thái "Khóa", 0 nút Lưu |
| Mở khoá | popup "Bạn có chắc muốn mở khóa tiểu mục 'E2ECAT T-Khoa'?" → gọi đúng `job-clusters/19/unlock`, bảng đổi "Hoạt động" |
| Không quyền (user-nocost) | 3 màn đều về `/pages/extras/404`; API: GET danh sách 403, POST 403, `getAll` 200 (không gate — giống mọi danh mục) |
| Console | chỉ 404 ảnh avatar `e2e.png` (có sẵn) + 422 của lần Lưu trống (cố ý) |
| Bộ lọc màn Tiểu mục | chọn Lĩnh vực 2 → ô Chương còn đúng "E2ECAT C-A"; chọn Chương + Mục → 2 dòng; đổi Lĩnh vực sang 7 ⇒ `chapter_id`/`group_id` bị xoá, CHỈ 1 request `internal_business_scope_id=7` (không mang id cũ) |
| Màn Chương | 9 cột; chỉ 2 chương mới hiện (0/65 chương cũ lọt); popup 1 hàng 4+5+3 = 12, `maxlength=64` |
| Màn Mục | 10 cột; popup 2 hàng 12/12; ô Chương khoá tới khi chọn Lĩnh vực |


### Checkpoint — 2026-10-04 (wrap up)
Vừa hoàn thành: Phase 2d xong toàn bộ Task 0–9 + 1 lượt sửa sau review cuối (N+1 is_can_lock, trùng tên khi thiếu lĩnh vực, khoá ô Trạng thái, báo lỗi ô lọc); PHPUnit 12/12; e2e 6/6 passed.
Đang làm dở: không.
Bước tiếp theo: chờ user quyết push/merge `feat/p2d-cay-catalog` (cả 2 repo) vào gop_db — khi merge kiểm `uniq -d` id quyền với nhánh `gop_db-bao-cao-nhu-cau-dich-vu`.
Blocked: 
