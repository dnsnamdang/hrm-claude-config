# Phân hệ Kế toán (Accounting)

Tài liệu tổng quan module `Accounting` — phân hệ Kế toán của HRM. File này mô tả **khung hiện có** sau lần scaffold (2026-04-21). Mỗi khi làm feature mới trong phân hệ này, đọc trước để hiểu cấu trúc và convention đang áp dụng.

---

## 1. Trạng thái hiện tại

**Scaffold rỗng** — chưa có entity nghiệp vụ nào. Module đã đăng ký, route sample `GET /api/v1/accounting/dashboard` hoạt động, FE có layout + sidebar riêng, grid tile hiện có điều kiện theo master-setting `use_accounting`.

**Spec scaffold gốc:** `docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`

---

## 2. Backend — `hrm-api/Modules/Accounting/`

### 2.1 Cấu trúc thư mục

```
Modules/Accounting/
├── Config/config.php              # name => 'Accounting'
├── Console/
├── Database/
│   ├── Migrations/                # migration module-level (nếu có)
│   ├── Seeders/
│   └── factories/
├── Entities/                      # Eloquent Model (extends BaseModel)
├── Enums/
├── Export/                        # Excel exporter
├── Http/
│   ├── Controllers/Api/V1/
│   │   └── DashboardController.php   # sample endpoint
│   ├── Middleware/
│   └── Requests/                  # FormRequest (extends BaseRequest)
├── Jobs/
├── Mail/
├── Providers/
│   ├── AccountingServiceProvider.php
│   └── RouteServiceProvider.php
├── Repositories/
├── Resources/
│   ├── views/
│   ├── lang/
│   └── assets/
├── Routes/
│   ├── api.php                    # prefix /v1/accounting, middleware auth:api
│   └── web.php
├── Rules/
├── Services/                      # business logic
├── Transformers/                  # ApiResource (extends Human\Transformers\ApiResource)
├── module.json                    # name=Accounting, alias=accounting
└── composer.json                  # namespace Modules\\Accounting\\
```

### 2.2 Đăng ký module

- `modules_statuses.json`: cần key `"Accounting": true` để module active.
- `composer dump-autoload` bắt buộc sau khi thêm file mới ngoài autoload PSR-4.
- Verify: `php artisan module:list` → Accounting Enabled.

### 2.3 DB connection

Dùng **connection mặc định `mysql`**. Không có connection riêng. Nếu cần connection khác, sửa trong từng Model cụ thể bằng `protected $connection = '...'`.

### 2.4 Route prefix

Tất cả API: `/api/v1/accounting/...`. Middleware mặc định `auth:api`. Áp `checkPermission` ở từng route cần phân quyền (xem `CLAUDE.md` + `docs/conventions.md`).

### 2.5 Sample endpoint

`GET /api/v1/accounting/dashboard` → trả `{ code: 200, message: 'success', data: { module: 'accounting' } }`. Dùng để verify module đã hoạt động, có thể xoá hoặc thay thế khi làm dashboard thật.

---

## 3. Frontend — `hrm-client/`

### 3.1 Entry points

| Vị trí                 | File                                                                              |
| ---------------------- | --------------------------------------------------------------------------------- |
| Grid tile (popup menu) | `components/BasicSubsystem.vue` — khối `v-if="isUseAccounting"`                   |
| Grid tile (trang `/`)  | `pages/index.vue` — khối `v-if="isUseAccounting"`                                 |
| Layout riêng           | `layouts/accounting.vue`                                                          |
| Sidebar trái           | `components/accounting-components/accounting-slidebar.vue`                        |
| Topbar trên cùng       | `components/accounting-components/AccountingMenu.vue` (dùng `<BasicSubsystem />`) |
| SCSS override          | `assets/scss/custom-accounting.scss` (re-import `custom-assign.scss`)             |
| Icon placeholder       | `assets/images/icon_ke_toan.svg` (copy từ `icon_quyet_dinh.svg` — **chưa final**) |

### 3.2 Page root

- `pages/accounting/index.vue` — placeholder, `layout: 'accounting'`
- `pages/accounting/dashboard.vue` — placeholder, `layout: 'accounting'`

Mọi page trong `pages/accounting/` **phải** set `layout: 'accounting'` để dùng sidebar riêng. Nếu quên, nó sẽ rơi về `default.vue`.

### 3.3 Sidebar menu

Khai báo trong `components/accounting-components/accounting-slidebar.vue` — mảng `menuItems` trong `data()`. Hiện chỉ có 1 mục "Tổng quan". Khi thêm nhóm chức năng mới, thêm vào mảng này theo format giống Assign:

```js
{
    id: N,
    label: 'Tên nhóm',
    icon: 'fas fa-xxx',       // FontAwesome / RemixIcon
    isMenuCollapsed: false,
    isShow: true,             // hoặc bỏ + dùng permission filter
    subItems: [
        { id: N+1, label: '...', link: '/accounting/...' },
    ],
},
```

Logic `filterMenuItems` + `showMenuChild` theo permission chưa implement (khác Assign) — khi cần phân quyền sidebar, port từ `assign-slidebar.vue`.

### 3.4 Flag bật/tắt

- Vuex state: `is_use_accounting` (không init trong `store/state.js`, set dynamic).
- Nguồn: master-setting `category = 'use_accounting'`, load tại `store/actions.js` trong action fetch master-settings.
- Toggle UI: checkbox "Sử dụng kế toán" tại `/timesheet/setting/setting-master` (admin).
- Khi flag `false`: tile grid ẩn, nhưng page `/accounting/*` vẫn vào được nếu có URL trực tiếp (do route không check flag).

### 3.5 File `components/default-menu/accounting.js`

**Không dùng** cho đến hiện tại — tàn dư từ bước trung gian (thử wiring qua `layouts/default.vue` trước khi tách layout riêng). Có thể xoá an toàn hoặc giữ làm snippet reference cho menu item. Khi dọn dẹp thì xoá.

---

## 4. Convention khi phát triển feature mới trong Accounting

Tất cả tuân thủ convention chung của project (xem các file gốc). Ở đây chỉ note những điểm **đặc thù** module này:

1. **Namespace:** Controller/Service/Entity phải đặt trong `Modules\Accounting\...`. Không cross-module (tránh import `Modules\Decision\...`).
2. **Connection DB:** mysql mặc định. Nếu team kế toán yêu cầu tách DB (VD `mysql_accounting`), cần sửa Provider + Entity + wrap `DB::connection('mysql_accounting')->transaction()` thay vì `DB::transaction()`.
3. **Permission:** nhóm phân quyền đề xuất đặt prefix tiếng Việt `Kế toán / ...` để nhất quán với các module cũ (VD `Kế toán / Danh mục tài khoản`).
4. **Số tiền:** dùng `V2BaseCurrencyInput` cho input tiền, backend dùng `decimal(20, 2)` cho cột tiền — KHÔNG dùng float/double.
5. **FE style:** mọi page dùng UI v2 (V2Base components + `v2-styles.scss`). **Không** dùng component cũ (bootstrap form trần) trừ khi có lý do rõ ràng.
6. **File đính kèm:** dùng bảng `files` chung theo convention toàn project, `table='accounting_<table_name>'`.
7. **Mã code tự sinh:** pattern `PREFIX-YYYY-NNNNN`. Prefix đề xuất (chưa chốt): `KT` cho phiếu kế toán chung, `PT` cho phiếu thu, `PC` cho phiếu chi, `HD` cho hoá đơn. **Hỏi user trước khi chốt prefix.**

---

## 5. Liên kết tài liệu

- Convention CRUD đầy đủ (code mẫu): `docs/conventions.md`
- Base classes + V2Base + store helpers: `docs/shared.md`
- Pattern màn danh sách có phân quyền theo cấp: `.claude/skills/list-page/SKILL.md`
- Spec scaffold gốc (2026-04-21): `docs/superpowers/specs/2026-04-21-ke-toan-module-scaffold-design.md`
- Plan scaffold gốc: `.plans/ke-toan-module-scaffold/plan.md`

---

Mỗi chức năng khi phát triển: tạo folder `.plans/[feature]/` + spec chi tiết tại `docs/superpowers/specs/`. Cập nhật file này ở section **3.3 Sidebar menu** khi thêm nhóm mới.
