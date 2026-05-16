# Danh mục Module Scaffold — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold khung module `Category` (Danh mục) — BE Laravel module + FE Nuxt pages với layout riêng — nhất quán pattern Accounting đã scaffold. Đồng thời dọn `CLAUDE.md`, `docs/`, `.plans/` cho dự án mới chỉ tập trung 4 module (HCNS/Timesheet/Payroll/Category).

**Architecture:** BE copy skeleton từ `Modules/Decision/` (folder rỗng + ServiceProvider + RouteServiceProvider + DashboardController placeholder). FE tạo layout `layouts/category.vue` (sidebar + topbar inline trực tiếp trong layout, KHÔNG tách component riêng) + 2 pages placeholder. Tile "Danh mục" luôn hiển thị ở home + BasicSubsystem, không có flag toggle.

**Tech Stack:** PHP 7.4, Laravel 8, nwidart/laravel-modules, Nuxt 2 (Vue 2), Bootstrap 4, SCSS

**Spec:** `docs/superpowers/specs/2026-05-16-category-module-scaffold-design.md`

**Plan mẫu chuẩn:** `.plans/ke-toan-module-scaffold/plan.md`

---

## Phase 1 — Backend scaffold

### Task 1: Tạo cấu trúc folder và file config module

**Files:**
- Create: `nhatlinh-api/Modules/Category/module.json`
- Create: `nhatlinh-api/Modules/Category/composer.json`
- Create: `nhatlinh-api/Modules/Category/Config/config.php`
- Create: `nhatlinh-api/Modules/Category/Routes/api.php`
- Create: `nhatlinh-api/Modules/Category/Routes/web.php`

- [ ] **Step 1:** Tạo các folder rỗng trong `nhatlinh-api/Modules/Category/`

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-api/Modules
mkdir -p Category/{Config,Console,Database/Migrations,Database/Seeders,Database/factories,Entities,Export,Http/Controllers/Api/V1,Http/Requests,Http/Middleware,Jobs,Providers,Resources/views,Resources/lang,Resources/assets,Routes,Rules,Services,Transformers}
```

- [ ] **Step 2:** Tạo `module.json`

```json
{
    "name": "Category",
    "alias": "category",
    "description": "",
    "keywords": [],
    "priority": 0,
    "providers": ["Modules\\Category\\Providers\\CategoryServiceProvider"],
    "aliases": {},
    "files": [],
    "requires": []
}
```

- [ ] **Step 3:** Tạo `composer.json`

```json
{
    "name": "Category",
    "description": "",
    "authors": [
        {
            "name": "Nicolas Widart",
            "email": "n.widart@gmail.com"
        }
    ],
    "extra": {
        "laravel": {
            "providers": [],
            "aliases": {}
        }
    },
    "autoload": {
        "psr-4": {
            "Modules\\Category\\": ""
        }
    }
}
```

- [ ] **Step 4:** Tạo `Config/config.php`

```php
<?php

return [
    'name' => 'Category'
];
```

- [ ] **Step 5:** Tạo `Routes/web.php` (shell rỗng)

```php
<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
*/
```

- [ ] **Step 6:** Tạo `Routes/api.php` với route dashboard placeholder

```php
<?php

use Illuminate\Support\Facades\Route;
use Modules\Category\Http\Controllers\Api\V1\DashboardController;

Route::group(['prefix' => '/v1/category', 'middleware' => 'auth:api'], function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});
```

### Task 2: Tạo ServiceProvider và RouteServiceProvider

**Files:**
- Create: `nhatlinh-api/Modules/Category/Providers/CategoryServiceProvider.php`
- Create: `nhatlinh-api/Modules/Category/Providers/RouteServiceProvider.php`

- [ ] **Step 1:** Tạo `Providers/CategoryServiceProvider.php`

```php
<?php

namespace Modules\Category\Providers;

use Illuminate\Support\ServiceProvider;

class CategoryServiceProvider extends ServiceProvider
{
    protected $moduleName = 'Category';
    protected $moduleNameLower = 'category';

    public function boot()
    {
        $this->registerConfig();
        $this->loadMigrationsFrom(module_path($this->moduleName, 'Database/Migrations'));
    }

    public function register()
    {
        $this->app->register(RouteServiceProvider::class);
    }

    protected function registerConfig()
    {
        $this->publishes([
            module_path($this->moduleName, 'Config/config.php') => config_path($this->moduleNameLower . '.php'),
        ], 'config');
        $this->mergeConfigFrom(
            module_path($this->moduleName, 'Config/config.php'),
            $this->moduleNameLower
        );
    }

    public function provides()
    {
        return [];
    }
}
```

- [ ] **Step 2:** Tạo `Providers/RouteServiceProvider.php`

```php
<?php

namespace Modules\Category\Providers;

use Illuminate\Support\Facades\Route;
use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;

class RouteServiceProvider extends ServiceProvider
{
    protected $moduleNamespace = 'Modules\Category\Http\Controllers';

    public function boot()
    {
        parent::boot();
    }

    public function map()
    {
        $this->mapApiRoutes();
        $this->mapWebRoutes();
    }

    protected function mapWebRoutes()
    {
        Route::middleware('web')
            ->namespace($this->moduleNamespace)
            ->group(module_path('Category', '/Routes/web.php'));
    }

    protected function mapApiRoutes()
    {
        Route::prefix('api')
            ->middleware('api')
            ->namespace($this->moduleNamespace)
            ->group(module_path('Category', '/Routes/api.php'));
    }
}
```

### Task 3: Tạo DashboardController placeholder

**Files:**
- Create: `nhatlinh-api/Modules/Category/Http/Controllers/Api/V1/DashboardController.php`

- [ ] **Step 1:** Tạo controller

```php
<?php

namespace Modules\Category\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Support\Facades\Log;

class DashboardController extends ApiController
{
    public function index()
    {
        try {
            return response()->json([
                'code' => 200,
                'data' => ['module' => 'category'],
            ]);
        } catch (\Throwable $e) {
            Log::error($e);
            return response()->json([
                'code' => 500,
                'message' => $e->getMessage(),
            ], 500);
        }
    }
}
```

### Task 4: Đăng ký module và verify

**Files:**
- Modify: `nhatlinh-api/modules_statuses.json`

- [ ] **Step 1:** Thêm `"Category": true` vào `modules_statuses.json` (giữ alphabet-style của file hiện tại)

File hiện tại:
```json
{
    "Timesheet": true,
    "Payroll": true,
    "Human": true,
    "Management": true,
    "Assign": true,
    "Training": true,
    "Decision": true,
    "Rice": true,
    "Test": true,
    "CRM": true
}
```

Sau khi sửa:
```json
{
    "Timesheet": true,
    "Payroll": true,
    "Human": true,
    "Management": true,
    "Assign": true,
    "Training": true,
    "Decision": true,
    "Rice": true,
    "Test": true,
    "CRM": true,
    "Category": true
}
```

- [ ] **Step 2:** Chạy composer dump-autoload

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-api
composer dump-autoload
```

- [ ] **Step 3:** Verify module đã enabled

```bash
php artisan module:list
```

Expected output có dòng: `Category | Enabled`

- [ ] **Step 4:** Verify route đã đăng ký

```bash
php artisan route:list --path=api/v1/category
```

Expected output có dòng: `GET|HEAD | api/v1/category/dashboard | ... DashboardController@index | api,auth:api`

- [ ] **Step 5:** Manual test endpoint (user thực hiện)

Gọi `GET /api/v1/category/dashboard` với JWT hợp lệ → kỳ vọng response:
```json
{ "code": 200, "data": { "module": "category" } }
```

---

## Phase 2 — Frontend scaffold

### Task 5: Tạo icon và SCSS

**Files:**
- Create: `nhatlinh-client/assets/images/icon_danh_muc.svg`
- Create: `nhatlinh-client/assets/scss/custom-category.scss`

- [ ] **Step 1:** Copy icon placeholder

```bash
cp /Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-client/assets/images/icon_quyet_dinh.svg \
   /Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-client/assets/images/icon_danh_muc.svg
```

- [ ] **Step 2:** Tạo `assets/scss/custom-category.scss` re-import style chung

```scss
@import './custom-assign.scss';
```

### Task 6: Tạo layout `layouts/category.vue` (sidebar + topbar inline)

**Files:**
- Create: `nhatlinh-client/layouts/category.vue`

- [ ] **Step 1:** Tạo file `layouts/category.vue` với sidebar + topbar viết inline trực tiếp trong layout (KHÔNG tách component riêng)

```vue
<script>
import { mapState } from 'vuex'

export default {
    components: {},
    data() {
        return {
            employeeAvatar: '/assets/images/users/default.png',
            employeeInfo: null,
        }
    },
    computed: {
        ...mapState(['layout']),
    },
    mounted() {
        this.employeeInfo = this.$store.state.auth?.user || null
        this.employeeAvatar = this.employeeInfo?.avatar || '/assets/images/users/default.png'
    },
    methods: {
        logout() {
            this.$auth.logout()
        },
    },
}
</script>

<template>
    <div class="default-layout">
        <div id="wrapper" class="container-page">
            <!-- Topbar inline -->
            <div class="navbar-custom">
                <div class="container-fluid">
                    <ul class="list-unstyled topnav-menu float-right mb-0">
                        <b-nav-item-dropdown
                            variant="white"
                            class="d-none d-lg-inline-block topbar-dropdown"
                            toggle-class="nav-link"
                            right
                            menu-class="dropdown-lg p-0"
                        >
                            <template v-slot:button-content>
                                <i class="fe-grid noti-icon" style="color: #fff"></i>
                            </template>
                            <div class="px-lg-2">
                                <div class="row no-gutters">
                                    <div class="col">
                                        <a class="dropdown-icon-item" href="/human/dashboard/">
                                            <img src="@/assets/images/icon_hcns.svg" alt="HCNS" />
                                            <span>HCNS</span>
                                        </a>
                                    </div>
                                    <div class="col">
                                        <a class="dropdown-icon-item" href="/timesheet/dashboard/">
                                            <img src="@/assets/images/icon_cham_cong.svg" alt="Chấm công" />
                                            <span>Chấm công</span>
                                        </a>
                                    </div>
                                    <div class="col">
                                        <a class="dropdown-icon-item" href="/payroll/dashboard/">
                                            <img src="@/assets/images/icon_tinh_luong.svg" alt="Tính lương" />
                                            <span>Tính lương</span>
                                        </a>
                                    </div>
                                    <div class="col">
                                        <a class="dropdown-icon-item" href="/category/dashboard/">
                                            <img src="@/assets/images/icon_danh_muc.svg" alt="Danh mục" />
                                            <span>Danh mục</span>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </b-nav-item-dropdown>

                        <b-nav-item-dropdown
                            right
                            class="notification-list topbar-dropdown"
                            menu-class="profile-dropdown"
                            toggle-class="p-0"
                        >
                            <template slot="button-content" class="nav-link dropdown-toggle">
                                <div class="nav-user mr-0">
                                    <img :src="employeeAvatar" alt="user-image" class="rounded-circle" />
                                    <span v-if="employeeInfo" class="pro-user-name ml-1">
                                        {{ employeeInfo.fullname }}
                                        <i class="mdi mdi-chevron-down"></i>
                                    </span>
                                </div>
                            </template>
                            <b-dropdown-item :to="{ path: `/change_password` }">
                                <i class="fa fa-key"></i>
                                <span>Đổi mật khẩu</span>
                            </b-dropdown-item>
                            <b-dropdown-divider></b-dropdown-divider>
                            <b-dropdown-item @click="logout">
                                <i class="fa fa-power-off"></i>
                                <span>Đăng xuất</span>
                            </b-dropdown-item>
                        </b-nav-item-dropdown>
                    </ul>
                </div>
            </div>

            <div class="content-page">
                <div class="row content-page-box">
                    <!-- Sidebar inline -->
                    <div class="slide-data">
                        <div class="category-sidebar">
                            <div class="sidebar-logo">
                                <img src="@/assets/images/icon_danh_muc.svg" alt="Danh mục" />
                                <span>Danh mục</span>
                            </div>
                            <ul class="sidebar-menu list-unstyled">
                                <li>
                                    <nuxt-link to="/category/dashboard">
                                        <i class="fe-home"></i>
                                        <span>Tổng quan</span>
                                    </nuxt-link>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="slide-content">
                        <div class="content">
                            <div class="container-fluid">
                                <Nuxt />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/custom-category.scss';

.content-page {
    padding: 70px 15px 0 0;
    .content-page-box {
        min-height: calc(100vh - 70px);
        display: flex;
        .slide-data {
            width: 240px;
            padding-left: 10px;
        }
        .slide-content {
            padding: 16px 24px;
            width: calc(100vw - 250px);
            max-height: calc(100vh - 70px);
            overflow: scroll;
        }
    }
}

.category-sidebar {
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 0;
        font-weight: 600;
        img { width: 24px; height: 24px; }
    }
    .sidebar-menu {
        li a {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            color: #333;
            text-decoration: none;
            border-radius: 4px;
            &:hover, &.nuxt-link-active { background: #f1f3f7; color: #0066cc; }
        }
    }
}
</style>
```

### Task 7: Tạo 2 page placeholder

**Files:**
- Create: `nhatlinh-client/pages/category/index.vue`
- Create: `nhatlinh-client/pages/category/dashboard.vue`

- [ ] **Step 1:** Tạo `pages/category/index.vue`

```vue
<script>
export default {
    layout: 'category',
    data() {
        return {}
    },
}
</script>

<template>
    <div>
        <V2BaseTitleSubInfo title="Danh mục" sub-info="Phân hệ quản lý các danh mục dùng chung" />
        <p>Chào mừng đến phân hệ Danh mục. Chọn mục từ thanh điều hướng bên trái để bắt đầu.</p>
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

- [ ] **Step 2:** Tạo `pages/category/dashboard.vue`

```vue
<script>
export default {
    layout: 'category',
    data() {
        return {}
    },
}
</script>

<template>
    <div>
        <V2BaseTitleSubInfo title="Tổng quan Danh mục" sub-info="Trang tổng quan phân hệ Danh mục" />
        <p>Placeholder dashboard — sẽ bổ sung số liệu/widget sau khi có danh mục con.</p>
    </div>
</template>

<style scoped lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

### Task 8: Thêm tile "Danh mục" vào BasicSubsystem và pages/index.vue

**Files:**
- Modify: `nhatlinh-client/components/BasicSubsystem.vue`
- Modify: `nhatlinh-client/pages/index.vue`

- [ ] **Step 1:** Sửa `components/BasicSubsystem.vue` — thêm tile "Danh mục" sau tile "Tính lương" (dòng 51)

Tìm đoạn:
```html
                        <div class="col-md-4">
                            <a class="dropdown-icon-item" href="/payroll/dashboard/">
                                <img src="@/assets/images/icon_tinh_luong.svg" alt="Tính lương" />
                                <span>Tính lương</span>
                            </a>
                        </div>
```

Thay bằng:
```html
                        <div class="col-md-4">
                            <a class="dropdown-icon-item" href="/payroll/dashboard/">
                                <img src="@/assets/images/icon_tinh_luong.svg" alt="Tính lương" />
                                <span>Tính lương</span>
                            </a>
                        </div>
                        <div class="col-md-4">
                            <a class="dropdown-icon-item" href="/category/dashboard/">
                                <img src="@/assets/images/icon_danh_muc.svg" alt="Danh mục" />
                                <span>Danh mục</span>
                            </a>
                        </div>
```

- [ ] **Step 2:** Sửa `pages/index.vue` — thêm tile "Danh mục" sau tile "Tính lương" (dòng 36)

Tìm đoạn:
```html
            <div class="item-system">
                <div class="card card-system">
                    <a class="dropdown-icon-item" href="/payroll/dashboard/">
                        <img src="@/assets/images/icon_tinh_luong.svg" alt="Tính lương" />
                        <span class="text-system">Tính lương</span>
                    </a>
                </div>
            </div>
```

Thay bằng:
```html
            <div class="item-system">
                <div class="card card-system">
                    <a class="dropdown-icon-item" href="/payroll/dashboard/">
                        <img src="@/assets/images/icon_tinh_luong.svg" alt="Tính lương" />
                        <span class="text-system">Tính lương</span>
                    </a>
                </div>
            </div>
            <div class="item-system">
                <div class="card card-system">
                    <a class="dropdown-icon-item" href="/category/dashboard/">
                        <img src="@/assets/images/icon_danh_muc.svg" alt="Danh mục" />
                        <span class="text-system">Danh mục</span>
                    </a>
                </div>
            </div>
```

### Task 9: Verify Frontend

- [ ] **Step 1:** Build dev không lỗi (user thực hiện)

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh/nhatlinh-client
yarn dev
```

Expected: build success, no new error/warning

- [ ] **Step 2:** Manual test (user thực hiện)

1. Vào trang chủ `/` → kỳ vọng thấy tile "Danh mục" trong `pages/index.vue`
2. Click tile dropdown phân hệ ở navbar → kỳ vọng thấy "Danh mục" trong dropdown (`BasicSubsystem.vue`)
3. Click tile → vào `/category/dashboard` → kỳ vọng render placeholder với sidebar trái + topbar trên
4. Sidebar có 1 mục "Tổng quan" link tới `/category/dashboard`
5. Vào `/category/` → render `pages/category/index.vue` với layout giống

---

## Phase 3 — Cleanup CLAUDE.md, docs/, .plans/

### Task 10: Sửa CLAUDE.md — rút bảng module còn 4 hàng

**Files:**
- Modify: `/Users/manhcuong/Desktop/CLAUDE.md`

- [ ] **Step 1:** Sửa bảng "Kiến trúc Module"

Tìm bảng hiện tại (7 hàng từ Human đến CRM):
```markdown
| 1   | Hành chính nhân sự | `Modules/Human`     | `pages/human`     |
| 2   | Chấm công          | `Modules/Timesheet` | `pages/timesheet` |
| 3   | Tính lương         | `Modules/Payroll`   | `pages/payroll`   |
| 4   | Đào tạo            | `Modules/Training`  | `pages/training`  |
| 5   | Giao việc          | `Modules/Assign`    | `pages/assign`    |
| 6   | Quyết định         | `Modules/Decision`  | `pages/decision`  |
| 7   | CRM                | `Modules/CRM`       | `pages/client`    |
```

Thay bằng:
```markdown
| 1   | Hành chính nhân sự | `Modules/Human`     | `pages/human`     |
| 2   | Chấm công          | `Modules/Timesheet` | `pages/timesheet` |
| 3   | Tính lương         | `Modules/Payroll`   | `pages/payroll`   |
| 4   | Danh mục           | `Modules/Category`  | `pages/category`  |
```

### Task 11: Xóa các file docs không dùng

**Files:**
- Delete: nhiều file trong `docs/`

- [ ] **Step 1:** Xóa md file thuộc module loại

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh
rm -f docs/assign.md docs/decision.md docs/training.md docs/tranning.md docs/rice.md docs/accounting.md docs/management.md docs/notify-task-report-mobile.md
```

- [ ] **Step 2:** Xóa xlsx thuộc module loại

```bash
rm -f "docs/menu-sidebar-assign.xlsx" "docs/Form bao gia sample.xlsx"
```

- [ ] **Step 3:** Xóa `docs/api/daily-report-mobile.md` và folder rỗng

```bash
rm -f docs/api/daily-report-mobile.md
rmdir docs/api 2>/dev/null || true
```

- [ ] **Step 4:** Xóa `docs/srs/` — giữ lại 3 file Payroll

```bash
cd docs/srs
ls | grep -vE '^(SRS_Bonus_Component\.docx|SRS_Bonus_Distribution\.docx|bonus-component\.md)$' | xargs -I {} rm -f "{}"
cd /Users/manhcuong/Desktop/dns/nhatlinh
ls docs/srs/
```

Expected ls output: 3 file: `SRS_Bonus_Component.docx`, `SRS_Bonus_Distribution.docx`, `bonus-component.md`

- [ ] **Step 5:** Xóa `docs/test-cases/bomlist-testcases.md` và folder rỗng

```bash
rm -f docs/test-cases/bomlist-testcases.md
rmdir docs/test-cases 2>/dev/null || true
```

### Task 12: Tạo `docs/category.md` stub

**Files:**
- Create: `docs/category.md`

- [ ] **Step 1:** Tạo file

```markdown
# Danh mục (Category)

## Mục đích

Phân hệ quản lý các danh mục dùng chung cho toàn bộ hệ thống (ngành nghề, loại tài liệu, vai trò dự án, ...). Các module nghiệp vụ khác (HCNS, Chấm công, Tính lương) tham chiếu danh mục con từ phân hệ này.

## Vị trí

- **Backend:** `nhatlinh-api/Modules/Category/`
- **Frontend:** `nhatlinh-client/pages/category/`
- **Route prefix:** `/api/v1/category`
- **Layout FE:** `nhatlinh-client/layouts/category.vue`

## Trạng thái hiện tại

Đã scaffold base (module Laravel + layout + dashboard placeholder). Chưa có entity danh mục con — sẽ bổ sung ở task sau theo nhu cầu.

## Spec

`docs/superpowers/specs/2026-05-16-category-module-scaffold-design.md`

## Convention khi thêm entity danh mục con

Luồng BE: Route → Controller (`extends ApiController`) → Request (1 file dùng chung cho store + update, `extends Modules\Training\Http\Requests\BaseRequest`) → Service (wrap `DB::transaction()` cho store/update/destroy) → Model (`extends BaseModel`, `$guarded = []`) → Resource (tách 2 file: List + Detail) → Migration (cột có `->comment()`, không foreign key constraint).
```

### Task 13: Dọn `.plans/` — chỉ giữ 1 plan mẫu

**Files:**
- Delete: 66 folder trong `.plans/`
- Modify: `.plans/STATUS.md`

- [ ] **Step 1:** Liệt kê các folder cần giữ

Giữ duy nhất: `ke-toan-module-scaffold/`

- [ ] **Step 2:** Xóa tất cả folder khác

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh/.plans
ls -d */ | grep -v '^ke-toan-module-scaffold/$' | xargs rm -rf
ls
```

Expected ls output: chỉ còn `ke-toan-module-scaffold/` và `STATUS.md`

- [ ] **Step 3:** Rút gọn `STATUS.md` còn 1 entry mẫu

Thay toàn bộ nội dung file `.plans/STATUS.md` bằng:

```markdown
# STATUS.md

## Đang làm

- ke-toan-module-scaffold → @manhcuong → .plans/ke-toan-module-scaffold/plan.md
  Trạng thái: DONE — giữ làm mẫu chuẩn cho task scaffold module mới.
  Spec: docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md
  Checkpoint: 2026-04-21 — Module Accounting Enabled, route /api/v1/accounting/dashboard hoạt động, FE tile + layout riêng đã wiring.

## Đã làm

(none)
```

### Task 14: Verify cleanup

- [ ] **Step 1:** Verify CLAUDE.md bảng module

```bash
grep -A 6 "Kiến trúc Module" /Users/manhcuong/Desktop/CLAUDE.md | head -10
```

Expected: bảng có đúng 4 hàng (Human/Timesheet/Payroll/Category)

- [ ] **Step 2:** Verify docs/ chỉ còn file hợp lệ

```bash
cd /Users/manhcuong/Desktop/dns/nhatlinh
ls docs/
```

Expected: thấy `human.md`, `timesheet.md`, `payroll.md`, `category.md`, `conventions.md`, `shared.md`, `onboarding.md`, `claude-code-skills-guide.md`, `claude-code-skills-guide.html`, `claude-code-skills-guide.pdf`, `srs/`, `superpowers/`. KHÔNG còn `assign.md`, `decision.md`, `training.md`, `tranning.md`, `rice.md`, `accounting.md`, `management.md`, `notify-task-report-mobile.md`, `menu-sidebar-assign.xlsx`, `Form bao gia sample.xlsx`, `api/`, `test-cases/`.

- [ ] **Step 3:** Verify `.plans/` chỉ còn 1 folder

```bash
ls /Users/manhcuong/Desktop/dns/nhatlinh/.plans/
```

Expected: `ke-toan-module-scaffold` + `STATUS.md`

---

## Tổng kết verification (cuối plan)

**Backend:**
- [ ] `php artisan module:list` → `Category | Enabled`
- [ ] `GET /api/v1/category/dashboard` với JWT trả `{ code: 200, data: { module: 'category' } }`

**Frontend:**
- [ ] `yarn dev` build không lỗi
- [ ] Tile "Danh mục" hiện ở `pages/index.vue` và `BasicSubsystem.vue` (luôn hiển thị)
- [ ] `/category/dashboard` + `/category/` render placeholder với layout riêng (sidebar + topbar inline)

**Cleanup:**
- [ ] `CLAUDE.md` bảng module còn 4 hàng (Human/Timesheet/Payroll/Category)
- [ ] `docs/category.md` đã tạo
- [ ] `docs/` đã xóa hết file thuộc module loại
- [ ] `.plans/` chỉ còn `ke-toan-module-scaffold/` + `STATUS.md` rút gọn
