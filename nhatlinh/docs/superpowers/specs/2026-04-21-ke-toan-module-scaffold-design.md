# Spec — Kế toán Module Scaffold (2026-04-21)

## 1. Mục tiêu

Tạo khung module mới **`Accounting`** (phân hệ Kế toán) ở cả BE và FE, nhất quán với các module hiện có. **Không** implement entity/CRUD nghiệp vụ nào — mục tiêu là có codebase sẵn sàng để nhận feature thực tế sau.

## 2. Scope

**IN:**
- BE: `Modules/Accounting/` với cấu trúc thư mục đầy đủ copy từ `Modules/Decision/`.
- BE: Service Provider, Route Service Provider, `module.json`, `composer.json`, đăng ký vào `modules_statuses.json`.
- BE: 1 `DashboardController::index()` sample trả JSON `{ module: 'accounting' }`.
- FE: tile trong grid `BasicSubsystem.vue` + `pages/index.vue`, flag `isUseAccounting` (Vuex state `is_use_accounting`).
- FE: icon placeholder, file menu sidebar placeholder, page `/accounting/index.vue` + `/accounting/dashboard.vue` placeholder.
- FE: master-setting `use_accounting` đọc từ API `/api/v1/master-settings` để commit flag.

**OUT (YAGNI):**
- Không tạo Entity/Model/migration dữ liệu.
- Không permission seed.
- Không Resource/Transformer/Request cụ thể.
- Không Job/Mail/Export.
- Không sidebar menu item thật (file `accounting.js` rỗng hoặc chỉ có shell).

## 3. Backend

### 3.1 Thư mục

Copy y nguyên cấu trúc `hrm-api/Modules/Decision/` sang `hrm-api/Modules/Accounting/`:

```
Modules/Accounting/
├── Config/
│   └── config.php
├── Console/
├── Database/
│   ├── factories/
│   ├── migrations/
│   └── seeders/
├── Entities/
├── Enums/
├── Export/
├── Http/
│   ├── Controllers/Api/V1/
│   │   └── DashboardController.php
│   ├── Middleware/
│   └── Requests/
├── Jobs/
├── Mail/
├── Providers/
│   ├── AccountingServiceProvider.php
│   └── RouteServiceProvider.php
├── Repositories/
├── Resources/
├── Routes/
│   └── api.php
├── Rules/
├── Services/
├── Transformers/
├── composer.json
└── module.json
```

### 3.2 File nội dung

**`module.json`** (mirror Decision):
```json
{
    "name": "Accounting",
    "alias": "accounting",
    "description": "",
    "keywords": [],
    "priority": 0,
    "providers": ["Modules\\Accounting\\Providers\\AccountingServiceProvider"],
    "aliases": {},
    "files": [],
    "requires": []
}
```

**`composer.json`**: copy từ Decision, đổi `"Modules\\Decision\\"` → `"Modules\\Accounting\\"`.

**`Providers/AccountingServiceProvider.php`**: copy từ `DecisionServiceProvider.php`, replace all `Decision` → `Accounting`, `decision` → `accounting`.

**`Providers/RouteServiceProvider.php`**: copy + replace. Route prefix `api/v1/accounting`, middleware `auth:api`.

**`Routes/api.php`**:
```php
<?php
use Illuminate\Support\Facades\Route;
use Modules\Accounting\Http\Controllers\Api\V1\DashboardController;

Route::group(['prefix' => 'v1/accounting'], function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});
```

**`Http/Controllers/Api/V1/DashboardController.php`**:
```php
<?php
namespace Modules\Accounting\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Response;

class DashboardController extends ApiController
{
    public function index()
    {
        return $this->responseJson('success', Response::HTTP_OK, [
            'module' => 'accounting',
        ]);
    }
}
```

**`Config/config.php`**:
```php
<?php
return [
    'name' => 'Accounting',
];
```

### 3.3 Đăng ký module

Sửa `hrm-api/modules_statuses.json` — thêm:
```json
"Accounting": true
```

### 3.4 DB connection

Dùng connection mặc định (`mysql`). Không tạo connection riêng, không migration nào trong lần scaffold này.

## 4. Frontend

### 4.1 Icon & assets

- Copy `hrm-client/assets/images/icon_quyet_dinh.svg` → `hrm-client/assets/images/icon_ke_toan.svg` (placeholder, user replace sau).

### 4.2 Flag `isUseAccounting`

Vuex state `is_use_accounting` — mirror pattern `is_use_decision`:

**`hrm-client/store/actions.js`** — trong action fetch master-settings (hiện gần dòng 121-125), thêm commit:
```js
commit(SET_STATE, {
    key: 'is_use_accounting',
    value: res.data.data.find((item) => item.category == 'use_accounting')?.content == 1 ? true : false,
})
```

**`hrm-client/store/state.js`** (hoặc nơi init state): thêm `is_use_accounting: false`.

Backend cần có master-setting record với `category = 'use_accounting'` (tạo thủ công hoặc seeder — ngoài scope scaffold này; nếu thiếu, flag luôn false và user enable thủ công trong DB).

### 4.3 Grid subsystem

**`hrm-client/components/BasicSubsystem.vue`** — thêm sau khối Decision:
```vue
<div class="col-md-4" v-if="isUseAccounting">
    <a class="dropdown-icon-item" href="/accounting/dashboard">
        <img src="@/assets/images/icon_ke_toan.svg" alt="Kế toán" />
        <span>Kế toán</span>
    </a>
</div>
```
Computed:
```js
isUseAccounting() {
    return this.$store.state.is_use_accounting
}
```

**`hrm-client/pages/index.vue`** — thêm tương tự khối `v-if="isUseDecision"` (dòng 53).

### 4.4 Sidebar menu file

**`hrm-client/components/default-menu/accounting.js`** — copy structure từ `decision.js`, để mảng `menuItems` rỗng (hoặc 1 item placeholder "Dashboard" trỏ `/accounting/dashboard`).

### 4.5 Pages

**`hrm-client/pages/accounting/index.vue`**:
```vue
<template>
    <div class="v2-styles">
        <V2BaseTitleSubInfo title="Phân hệ Kế toán" sub-info="Dashboard" />
    </div>
</template>
<script>
export default { name: 'AccountingIndex' }
</script>
<style lang="scss" scoped>
@import '@/assets/scss/v2-styles.scss';
</style>
```

**`hrm-client/pages/accounting/dashboard.vue`**: tương tự, title "Dashboard Kế toán".

## 5. Verify sau scaffold

1. **BE:** `php artisan module:list` — module `Accounting` status = `Enabled`.
2. **BE:** Gọi `GET /api/v1/accounting/dashboard` (kèm JWT hợp lệ) — trả `{ code: 200, message: 'success', data: { module: 'accounting' } }`.
3. **FE:** `yarn dev` build không lỗi.
4. **FE:** Set `is_use_accounting = true` trong Vuex (hoặc insert master-setting `use_accounting=1`) — tile "Kế toán" xuất hiện ở grid, click vào route `/accounting/dashboard` render placeholder.

## 6. Edge case & downstream impact

- **`modules_statuses.json`**: nếu file này được generate từ `php artisan module:enable`, có thể chạy `php artisan module:enable Accounting` thay vì sửa tay.
- **Autoload**: sau tạo `composer.json` module cần chạy `composer dump-autoload` ở root `hrm-api`.
- **Không ảnh hưởng module cũ**: tất cả thay đổi FE (BasicSubsystem, pages/index, actions.js) chỉ thêm block mới, không sửa logic cũ.
- **Permission**: vì scaffold không có permission nào, endpoint `/dashboard` chỉ cần `auth:api`. Khi làm feature thật sẽ gắn `checkPermission` sau.

## 7. Không làm

- Không tạo Entity / migration nghiệp vụ.
- Không seed permission.
- Không Resource/Transformer/Request mẫu.
- Không sidebar menu cụ thể (file `accounting.js` chỉ là shell).
- Không icon SVG final (dùng copy từ Decision làm placeholder).
