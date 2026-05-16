# Danh mục Module Scaffold — Design

**Ngày:** 2026-05-16
**Trạng thái:** Approved (chờ implementation plan)

## 1. Mục tiêu

Scaffold khung module `Category` (Danh mục) — Backend + Frontend — nhất quán với pattern Accounting đã scaffold trước đây (xem `.plans/ke-toan-module-scaffold/`). Chưa có entity nghiệp vụ; chỉ có dashboard placeholder để verify module enabled và sẵn sàng cho các task thêm danh mục con sau.

Đồng thời dọn `CLAUDE.md`, `docs/`, `.plans/` cho dự án mới — chỉ tập trung vào 4 phân hệ: Hành chính nhân sự (Human), Chấm công (Timesheet), Tính lương (Payroll), **Danh mục (Category)**. Các module khác (Training/Assign/Decision/CRM/Rice/Management) ở code BE/FE tạm thời giữ nguyên, sẽ dọn ở task khác.

## 2. Phạm vi

**In scope:**
- Tạo module BE `Modules/Category/` với cấu trúc folder chuẩn, 1 `DashboardController` placeholder
- Tạo FE pages `pages/category/` với layout riêng `layouts/category.vue` (sidebar + topbar inline trong layout)
- Wiring tile "Danh mục" trên home + BasicSubsystem (luôn hiển thị, không có flag toggle)
- Dọn CLAUDE.md, docs/, .plans/

**Out of scope:**
- Entity danh mục con và CRUD của chúng (làm sau)
- Migration cho bảng nghiệp vụ
- Dọn code BE/FE của các module Training/Assign/Decision/CRM/Rice/Management

## 3. Backend scaffold

### 3.1 Cấu trúc folder `nhatlinh-api/Modules/Category/`

Copy skeleton từ `Modules/Decision/`, giữ tất cả folder rỗng để sẵn sàng cho entity sau:

```
Modules/Category/
├── Config/config.php                        ['name' => 'Category']
├── Console/                                 (rỗng)
├── Database/{Migrations,Seeders,factories}/ (rỗng)
├── Entities/                                (rỗng)
├── Export/                                  (rỗng)
├── Http/
│   ├── Controllers/Api/V1/DashboardController.php
│   ├── Requests/                            (rỗng)
│   └── Middleware/                          (rỗng)
├── Jobs/                                    (rỗng)
├── Providers/
│   ├── CategoryServiceProvider.php
│   └── RouteServiceProvider.php             (prefix 'api/v1/category', middleware 'auth:api')
├── Resources/{views,lang,assets}/           (rỗng)
├── Routes/
│   ├── api.php                              (GET /dashboard → DashboardController@index)
│   └── web.php                              (shell rỗng)
├── Rules/                                   (rỗng)
├── Services/                                (rỗng)
├── Transformers/                            (rỗng)
├── composer.json                            (namespace "Modules\\Category\\")
└── module.json                              (name=Category, alias=category, provider=CategoryServiceProvider)
```

### 3.2 DashboardController

```php
namespace Modules\Category\Http\Controllers\Api\V1;

class DashboardController extends Controller {
    public function index() {
        try {
            return response()->json(['code' => 200, 'data' => ['module' => 'category']]);
        } catch (\Throwable $e) {
            \Log::error($e);
            return response()->json(['code' => 500, 'message' => $e->getMessage()], 500);
        }
    }
}
```

### 3.3 Đăng ký module

- Thêm `"Category": true` vào `nhatlinh-api/modules_statuses.json`
- `composer dump-autoload` → `php artisan module:list` → kỳ vọng `Category | Enabled`
- Verify endpoint: `GET /api/v1/category/dashboard` với JWT → `{ code: 200, data: { module: 'category' } }`

## 4. Frontend scaffold

### 4.1 File mới

```
nhatlinh-client/
├── assets/images/icon_danh_muc.svg          (placeholder, copy từ icon_quyet_dinh.svg)
├── assets/scss/custom-category.scss         (re-import custom-assign.scss)
├── layouts/category.vue                      (layout DUY NHẤT chứa inline sidebar + topbar)
└── pages/category/
    ├── index.vue                             (layout: 'category', placeholder V2BaseTitleSubInfo)
    └── dashboard.vue                         (layout: 'category', placeholder)
```

**Quy tắc inline:** Sidebar và topbar chỉ được sử dụng bởi `layouts/category.vue` → viết trực tiếp template + script + style trong file layout, KHÔNG tách thành component riêng trong `components/category-components/`.

### 4.2 File sửa

- `components/BasicSubsystem.vue` — thêm tile "Danh mục" (luôn hiển thị, không cần computed flag)
- `pages/index.vue` — thêm tile "Danh mục" tương tự

KHÔNG sửa `store/actions.js` và KHÔNG thêm checkbox vào `pages/timesheet/setting/setting-master/index.vue` — module Danh mục luôn bật, không có flag toggle.

### 4.3 Verify FE

- `yarn dev` build không lỗi
- Tile "Danh mục" hiện ngay ở home + BasicSubsystem (không phụ thuộc flag)
- Click tile → vào `/category/dashboard`, render placeholder với sidebar + topbar riêng từ `layouts/category.vue`

## 5. Cleanup docs/CLAUDE/.plans

### 5.1 `CLAUDE.md` (`/Users/manhcuong/Desktop/CLAUDE.md`)

Bảng "Kiến trúc Module" rút còn 4 hàng:

| # | Module | Backend | Frontend |
|---|--------|---------|----------|
| 1 | Hành chính nhân sự | `Modules/Human` | `pages/human` |
| 2 | Chấm công | `Modules/Timesheet` | `pages/timesheet` |
| 3 | Tính lương | `Modules/Payroll` | `pages/payroll` |
| 4 | Danh mục | `Modules/Category` | `pages/category` |

Các phần khác (Tech Stack, Base Classes, Pattern CRUD, Quy tắc BE/FE, V2Base Components) giữ nguyên.

### 5.2 `docs/`

**Xóa:**
- `docs/assign.md`, `docs/decision.md`, `docs/training.md`, `docs/tranning.md`, `docs/rice.md`, `docs/accounting.md`, `docs/management.md`, `docs/notify-task-report-mobile.md`
- `docs/menu-sidebar-assign.xlsx`, `docs/Form bao gia sample.xlsx`
- `docs/api/daily-report-mobile.md` (và folder `docs/api/` nếu trống)
- `docs/srs/`: xóa tất cả TRỪ `SRS_Bonus_Component.docx`, `SRS_Bonus_Distribution.docx`, `bonus-component.md`
- `docs/test-cases/bomlist-testcases.md` (và folder `docs/test-cases/` nếu trống)

**Giữ:**
- `docs/human.md`, `docs/timesheet.md`, `docs/payroll.md`
- `docs/conventions.md`, `docs/shared.md`, `docs/onboarding.md`
- `docs/claude-code-skills-guide.{md,html,pdf}`
- `docs/superpowers/` (giữ nguyên)

**Thêm mới:**
- `docs/category.md` — stub mô tả module Category: mục đích, vị trí folder BE/FE, link tới spec này. Danh mục con sẽ bổ sung sau.

### 5.3 `.plans/`

- **Giữ:** `.plans/ke-toan-module-scaffold/` (làm mẫu chuẩn cho task scaffold module)
- **Xóa:** 66 folder plan còn lại
- **Rút gọn `.plans/STATUS.md`:** giữ lại 1 entry mẫu (entry của `ke-toan-module-scaffold`) làm template tracking, xóa các entry khác

### 5.4 Cách xóa

Dùng `rm` thường (dự án hiện không phải git repo ở root `nhatlinh/`).

## 6. Verification checklist

**Backend:**
- [ ] `php artisan module:list` hiển thị `Category | Enabled`
- [ ] `GET /api/v1/category/dashboard` với JWT trả `{ code: 200, data: { module: 'category' } }`

**Frontend:**
- [ ] `yarn dev` build không lỗi/warning mới
- [ ] Tile "Danh mục" hiện ở `pages/index.vue` + `BasicSubsystem.vue` (luôn hiển thị)
- [ ] Click tile → `/category/dashboard` render placeholder với layout riêng

**Cleanup:**
- [ ] CLAUDE.md bảng module chỉ còn 4 hàng
- [ ] `docs/category.md` đã tạo
- [ ] Các file md/xlsx thuộc module loại đã xóa hết
- [ ] `.plans/` chỉ còn `ke-toan-module-scaffold/` và `STATUS.md` rút gọn

## 7. Convention cho entity danh mục con (áp dụng ở task sau)

Khi thêm entity danh mục con đầu tiên vào module Category, luồng BE đầy đủ:

```
Route (Routes/api.php, static TRƯỚC wildcard, middleware 'auth:api')
  → Controller (extends App\Http\Controllers\ApiController)
  → Request (extends Modules\Training\Http\Requests\BaseRequest) — 1 FILE DUY NHẤT cho cả store + update
  → Service (Services/XxxService.php) — store/update/destroy wrap DB::transaction()
  → Model (extends App\Models\BaseModel, $guarded = [])
  → Resource (Transformers/Xxx/) — tách 2 file: XxxListResource + XxxDetailResource
  → Migration — mọi cột phải có ->comment(), KHÔNG foreign key constraint
```

**Quy tắc Request:**
- Mỗi entity chỉ tạo 1 file `XxxRequest.php` dùng chung cho cả store + update. Cả Controller@store và Controller@update type-hint cùng class. KHÔNG tách `StoreRequest.php` + `UpdateRequest.php`.
- TẤT CẢ Request ở MỌI module đều extends `Modules\Training\Http\Requests\BaseRequest`. KHÔNG tạo `BaseRequest.php` riêng trong `Modules/Category/Http/Requests/` (hay module khác).
- Trong `rules()` dùng `$this->isMethod('post')` hoặc check `$this->route('id')` để phân biệt store/update (ví dụ unique rule loại trừ id hiện tại khi update).

**Quy tắc Component FE:** sub-component chỉ dùng bởi đúng 1 page/layout viết inline trong file đó, không tách file riêng trong `components/`.

## 8. References

- Plan mẫu chuẩn: `.plans/ke-toan-module-scaffold/plan.md`
- Convention chung: `docs/conventions.md`
