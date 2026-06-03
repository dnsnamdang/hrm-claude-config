# HRM Project — Hướng dẫn cho AI

## Nguyên tắc chung

- Luôn gợi ý và làm việc bằng tiếng Việt
- Không xử lý commit hay đẩy code lên git
- Không đọc file thư viện hệ thống — tốn token không cần thiết
- Ưu tiên dùng helper có sẵn, tạo helper mới nếu logic dùng lại nhiều nơi
- Khi cần sửa hàm dùng chung → hỏi ý kiến trước khi làm
- FE: Tuân thủ style list của module đang triển khai (mỗi module có thể khác nhau)
- Trước khi làm màn danh sách mới → hỏi có cần phân quyền theo cấp không
- Trước khi viết accessor `is_can_delete` → hỏi điều kiện xóa cụ thể của màn đó
- Mọi form có validate: BE phải rethrow `ValidationException` (không catch chung `Exception`), FE phải hiện lỗi inline tại từng input required (viền đỏ `is-invalid` + text lỗi `invalid-feedback`), dùng flag `touched` để chỉ hiện sau lần submit đầu
- `.claude`, `.plans`, `docs`, `CLAUDE.md` là symlink sang `hrm-claude-config/` — ghi file vào các path này bình thường, KHÔNG cần hỏi xác nhận

---

## Tech Stack

|                |                                               |
| -------------- | --------------------------------------------- |
| **Backend**    | PHP 7.4, Laravel 8 (`^8.65`), MySQL, Redis    |
| **Auth**       | JWT (`tymon/jwt-auth ^1.0`) + Laravel Sanctum |
| **Permission** | `spatie/laravel-permission ^5.4`              |
| **Module**     | `nwidart/laravel-modules ^8.2`                |
| **Excel**      | `maatwebsite/excel ^3.1`                      |
| **Storage**    | AWS S3                                        |
| **Frontend**   | Nuxt 2.14 (Vue 2), Node 14.21.3               |
| **CSS**        | Bootstrap 4 + Bootstrap-Vue 2.15              |
| **State**      | Vuex 3.5                                      |
| **HTTP**       | @nuxtjs/axios                                 |
| **Date**       | dayjs, vue2-datepicker                        |
| **Editor**     | Quill, CKEditor 5                             |
| **Chart**      | ApexCharts, Highcharts, Chart.js              |

---

## Kiến trúc Module

| #   | Module                      | Backend             | Frontend          |
| --- | --------------------------- | ------------------- | ----------------- |
| 1   | Hành chính nhân sự          | `Modules/Human`     | `pages/human`     |
| 2   | Chấm công                   | `Modules/Timesheet` | `pages/timesheet` |
| 3   | Tính lương                  | `Modules/Payroll`   | `pages/payroll`   |
| 4   | Đào tạo                     | `Modules/Training`  | `pages/training`  |
| 5   | Giao việc ← đang phát triển | `Modules/Assign`    | `pages/assign`    |
| 6   | Quyết định                  | `Modules/Decision`  | `pages/decision`  |
| 7   | CRM                         | `Modules/CRM`       | `pages/client`    |

---

## Tài liệu chi tiết

| Cần gì                                           | Đọc file nào                                |
| ------------------------------------------------ | ------------------------------------------- |
| Base classes, V2Base components, API store calls | `docs/shared.md`                            |
| Pattern CRUD đầy đủ (code mẫu)                   | `docs/conventions.md`                       |
| Onboarding dev mới                               | `docs/onboarding.md`                        |
| Design + Plan của từng feature                   | `.plans/[feature]/` (xem quy luật bên dưới) |

---

## Convention Database (toàn project)

- **Cấp tổ chức**: luôn dùng `company_id`, `department_id`, `part_id` — tất cả `unsignedBigInteger nullable`. KHÔNG dùng `branch_id`.
- **Audit**: dùng `$table->timestamps()` (tạo `created_at`, `updated_at`) + thêm thủ công `created_by`, `updated_by` (`unsignedBigInteger nullable`). KHÔNG dùng SoftDeletes cho entity chính (chỉ dùng cho bảng phụ như comment/log nếu thực sự cần).
- **Version solution**: các entity gắn với solution phải có `solution_version_id` NOT NULL. Nếu áp dụng cả cấp module thì thêm `solution_module_id` + `solution_module_version_id` (nullable).
- **File đính kèm**: KHÔNG tạo bảng pivot riêng. Dùng bảng `files` chung với `table='<table_name>'` + `table_id=<entity_id>`. Model khai báo:
  ```php
  public function files() {
      return $this->hasMany(File::class, 'table_id', 'id')
          ->where('table', '<table_name>');
  }
  ```
- **Mã code tự sinh**: pattern `PREFIX-YYYY-NNNNN`, implement `getNextCode()` trên Entity (copy pattern `BomList::getNextCode()`).
- **Permission**: Khi thêm/sửa/đổi tên/xóa permission → sửa trực tiếp trong file `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`. KHÔNG tạo migration riêng cho permission.
- **Middleware checkPermission**: Khi có quyền tương ứng trong `PermissionsTableSeeder`, các route thao tác dữ liệu (store, update, destroy, approve, toggle,...) phải gắn middleware `checkPermission:TênQuyền`. Route xem (index, show) chỉ gắn nếu có quyền xem riêng. Cú pháp: `->middleware('checkPermission:Tên quyền')`, nhiều quyền dùng `|`: `->middleware('checkPermission:Quyền A|Quyền B')`. Không gắn middleware nếu chưa có quyền tương ứng trong seeder.

**Skills tự động:** Trước khi thực hiện bất kỳ task nào, quét `.claude/skills/` → đọc tên thư mục → nếu task khớp với tên skill thì đọc `SKILL.md` tương ứng và follow hướng dẫn bên trong. Ví dụ: yêu cầu "tạo SRS" → đọc `.claude/skills/srs-documenter/SKILL.md`, yêu cầu "fix bug" → đọc `.claude/skills/bug-fixer/SKILL.md`.

---

## Quy luật tổ chức tài liệu feature

Tất cả tài liệu của 1 feature nằm trong `.plans/[feature]/`. KHÔNG tạo file trong `docs/superpowers/specs/`.

**Feature nhỏ (1-2 phase):**

```
.plans/[feature]/
├── design.md          ← design duy nhất
├── plan.md            ← plan duy nhất
├── srs.html + srs.docx ← SRS (tạo khi được yêu cầu, cả 2 format)
└── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
```

**Feature lớn (3+ phase):**

```
.plans/[feature]/
├── design.md          ← tóm tắt tổng thể feature (scope, hiện trạng, quyết định chung)
├── design-phase{N}.md ← design chi tiết cho từng phase lớn
├── plan.md            ← TẤT CẢ tasks (append phase mới vào cuối, trước checkpoint)
├── srs.html + srs.docx ← SRS (tạo khi được yêu cầu, cả 2 format)
├── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
└── (các file phụ: testcase, script...)
```

**Quy tắc:**

- `design.md`: tóm tắt chung, KHÔNG chứa spec chi tiết từng phase
- `design-phase{N}.md`: spec đầy đủ (DB, BE, FE, edge cases) — tạo khi phase có nhiều thay đổi
- `plan.md`: 1 file duy nhất chứa tất cả phase, append liên tục
- SRS: 2 file output (`srs.html` + `srs.docx`) — lưu cùng folder feature
- Testcase: chỉ Excel (`testcase.xlsx`) — lưu cùng folder feature
- KHÔNG tạo `plan-phase{N}.md` riêng (đã có convention cũ nhưng không tiếp tục)

---

## Quản lý session

**Bắt đầu session mới — bắt buộc theo thứ tự:**

1. Đọc `.plans/STATUS.md`
2. Tìm feature đang ở mục "Đang làm"
3. Đọc `.plans/[feature]/design.md` + `plan.md`
4. Báo lại: "Đang làm [feature], checkpoint cuối: [X], task tiếp theo: [Y]"
5. Chờ xác nhận trước khi bắt đầu

**Khi nhận yêu cầu làm tiếp / cập nhật feature đã có — theo thứ tự:**

1. Cập nhật `STATUS.md` → chuyển feature về "Đang làm"
2. Đọc lại toàn bộ `.plans/[feature-name]/` (design.md + plan.md)
3. Kiểm tra branch:
   - Feature đã merge vào nhánh hiện tại → hỏi có tạo branch mới để update không? (cả API và Client)
   - Feature vẫn ở branch riêng → hỏi có chuyển về branch đó để làm tiếp không? (cả API và Client)
4. Yêu cầu nhập spec để brainstorming yêu cầu mới

**Khi nhận yêu cầu "tạo tính năng mới" / "tạo feature" — làm NGAY:**

1. Tạo folder `.plans/[feature-name]/`
2. Tạo file `.plans/[feature-name]/design.md` (placeholder, sẽ fill sau brainstorming)
3. Tạo file `.plans/[feature-name]/plan.md` (placeholder, sẽ fill sau khi lên plan)
4. Tạo file `docs/superpowers/specs/YYYY-MM-DD-<feature-name>-design.md` (placeholder, sẽ fill sau brainstorming)
5. Cập nhật `STATUS.md` → thêm vào "Đang làm" (kèm link tới spec chi tiết)
6. Sau đó mới bắt đầu brainstorming / hỏi yêu cầu

**Phân biệt 3 tài liệu của 1 feature:**

- `.plans/[feature]/design.md` — **TÓM TẮT** (1-2 trang): mục tiêu, scope, các quyết định lớn, link sang spec chi tiết
- `.plans/[feature]/plan.md` — task **TỔNG QUÁT** theo Phase → BE/FE (định dạng progress-manager)
- `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` — **SPEC ĐẦY ĐỦ**: schema DB, migration script, API contract, validation rule, business rule chi tiết, edge case, downstream impact, UX chi tiết
- Khi brainstorming: fill `docs/superpowers/specs/...` trước (chi tiết) → tóm tắt vào `.plans/[feature]/design.md`
- Khi `wrap up` lần đầu: cả 2 file design phải đầy đủ

**Khi nhận yêu cầu mới (feature/fix/task) — BẮT BUỘC trước khi code:**

1. Cập nhật `.plans/[feature]/plan.md` với danh sách task cụ thể
2. Đánh `[x]` khi xong mỗi task
3. Kể cả fix bug nhỏ cũng phải có task trong plan.md

**Khi nghe "wrap up" — làm ngay 4 việc theo thứ tự:**

1. Cập nhật `plan.md` — đánh `[x]` task xong, ghi checkpoint
2. Cập nhật `STATUS.md` — trạng thái feature hiện tại
3. Nếu là lần wrap up đầu tiên của feature (design.md còn trống hoặc chỉ có placeholder) → cập nhật `.plans/[feature]/design.md` (tóm tắt) VÀ `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` (chi tiết đầy đủ) dựa trên hiểu biết đã tích luỹ trong session (scope, data structure, UI, business rules, API endpoints, edge case, downstream impact)
4. Báo ra chat: "Đã cập nhật xong. Bước tiếp theo: [X]"

Không làm gì khác cho đến khi 3 việc này xong.

**Checkpoint format bắt buộc:**

```
### Checkpoint — [timestamp]
Vừa hoàn thành: [task vừa xong]
Đang làm dở: [file + dòng + dừng ở đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```

**Quy tắc STATUS.md — chỉ cập nhật khi có 1 trong 4 sự kiện:**

1. Tạo feature mới → thêm vào "Đang làm"
2. Nghe "wrap up" → cập nhật Checkpoint
3. Chuyển feature → move giữa các mục
4. Merge xong → move vào "Hoàn thành", giữ tối đa 3 entry

---

## Quy tắc team

- `CLAUDE.md`, `.claude/skills/`, `docs/` là tài sản chung — sửa qua PR, không tự ý sửa
- Mỗi dev KHÔNG tạo CLAUDE.md, .claude/skills/, docs/ riêng
- Mỗi feature trong `.plans/` ghi rõ người phụ trách (`@username`)
- Muốn thêm skill mới → tạo PR với SKILL.md đầy đủ
- Dev mới vào → đọc `docs/onboarding.md` trước

---

## Custom skills

Các skill tùy chỉnh nằm trong `.claude/skills/`.
Trước khi implement bất kỳ pattern lặp lại nào,
kiểm tra `.claude/skills/` xem đã có SKILL.md chưa.
Nếu có → đọc trước khi viết code.

**Skill bắt buộc đọc theo ngữ cảnh:**

| Khi làm gì                                          | Đọc skill nào                                |
| --------------------------------------------------- | -------------------------------------------- |
| Tạo/sửa button (nút bấm) trên FE hrm-client         | `.claude/skills/button-convention/SKILL.md`  |
| Tạo/sửa modal, popup, dialog trên FE hrm-client     | `.claude/skills/modal-popup/SKILL.md`        |
| Tạo màn danh sách mới ở hrm-client                  | `.claude/skills/list-page/SKILL.md` (nếu có) |
| Làm code trong project **elearning** (Vue 3 + Vite) | `.claude/skills/elearning-base/SKILL.md`     |
| Validate, error, toast trong elearning              | `.claude/skills/elearning-validate/SKILL.md` |
| Auth, SSO, profile, avatar trong elearning          | `.claude/skills/elearning-auth/SKILL.md`     |

→ Gặp ngữ cảnh trên → **đọc SKILL.md trước khi viết code**, không cần user nhắc.

---

## Lưu ý fix bug

Lỗi BE → đọc log tại:
`hrm-api/storage/logs/laravel-[ngày-hôm-nay].log`

---

## Khi làm việc với git

- Repo API nằm ở: /hrm-api
- Repo Client nằm ở: /hrm-client

## Không làm

- Không commit hay push git khi chưa có yêu cầu
- Không đọc file trong `vendor/`, `node_modules/`
- Không tự sửa hàm dùng chung khi chưa được xác nhận
- Không tự quyết định điều kiện `is_can_delete` — phải hỏi
- Không tự thêm phân quyền theo cấp — phải hỏi

---

## Dự án TanPhatDev (ERP Tân Phát)

### Tổng quan

Hệ thống ERP quản lý bán hàng, kho, kế toán, bảo hành, vận chuyển cho công ty Tân Phát. Repo nằm tại `/TanPhatDev`. Đây là dự án **Laravel thuần** (không dùng `nwidart/laravel-modules`), frontend render bằng **Blade + AngularJS 1.3.9** (KHÔNG phải Vue/Nuxt như hrm-client).

### Tech Stack

|                |                                                           |
| -------------- | --------------------------------------------------------- |
| **Backend**    | PHP 7.4, Laravel 8, MySQL                                |
| **Frontend**   | Blade template + AngularJS 1.3.9 + jQuery + Bootstrap 4  |
| **DataTable**  | Yajra DataTables (server-side) + datatables.net           |
| **Select**     | Select2 (nhiều variant: `select2`, `select2-in-modal`, `select2-ajax`, `select2-create`) |
| **Auth**       | Laravel Auth (session-based) + SSO                        |
| **Storage**    | AWS S3 (`CmcS3Helper`)                                   |
| **Excel**      | `maatwebsite/excel` — class trong `app/ExcelExports/`     |

### Cấu trúc thư mục

```
TanPhatDev/
├── app/
│   ├── Http/
│   │   ├── Controllers/          ← Phân theo module: Sale/, Warehouse/, Common/, Accounting/, Customercare/, Order/, ...
│   │   ├── Middleware/           ← CheckPermission, CheckRole, CheckDueConfigs, ...
│   │   └── Traits/              ← ResponseTrait (responseSuccess/responseErrors), HistoryTrait
│   ├── Model/                   ← Phân theo module: Sale/, Warehouse/, Common/, Accounting/, ...
│   ├── Services/                ← Business logic phức tạp: Sale/Firm/, DeliveryTrip/, Accounting/, ...
│   ├── Helpers/                 ← CmcS3Helper, NotificationHelper, FormatHelper, CodeHelper, ...
│   └── ExcelExports/            ← Maatwebsite Excel export classes
├── resources/views/
│   ├── layouts/app.blade.php    ← Layout chính, load Angular + globals
│   ├── partials/                ← Shared components: confirm, modals, createDeliveryTrip, ...
│   ├── warehouse/               ← Views kho: delivery_trips, warehouse_exports, warehouse_imports, ...
│   ├── sale/                    ← Views bán hàng: customers, suppliers, quotation_templates, ...
│   ├── accounting/              ← Views kế toán
│   ├── orders/                  ← Views đơn hàng
│   ├── income_expenditure/      ← Views thu chi
│   └── ...
├── public/js/
│   ├── angular/app.js           ← Angular module 'App' config (interpolation: <% %>)
│   ├── angular/app.directive.js ← Custom Angular directives
│   └── app.js                   ← jQuery utils: select2 init, DataTable helpers, format functions
├── routes/web.php               ← Tất cả routes (file đơn, rất dài)
└── database/
    ├── migrations/
    └── seeds/UpdateDB.php       ← Script fix data chạy qua tinker (không phải seeder chuẩn)
```

### Angular + Blade Pattern (QUAN TRỌNG)

Dự án dùng **AngularJS 1.3.9** (rất cũ) kết hợp Blade. Các rule bắt buộc:

- **Interpolation**: dùng `<% %>` thay vì `{{ }}` (đã config trong `angular/app.js`)
- **`ng-app="App"`** trên `<body>` → Angular compile **toàn bộ DOM** trong body
- **`ng-controller`** khai báo trên div, controller define trong `<script>` inline hoặc `@section('script')`
- **KHÔNG đặt `<select>` hardcode bên trong vùng Angular compile** mà không có `ng-model` hoặc `ng-non-bindable` — Angular 1.3.9 cố compile và crash `childNodes`. Nếu cần select ngoài Angular (ví dụ select2-ajax cho search column), dùng `ng-non-bindable` trên parent element
- **`@json()` trong `<script>`**: data PHP serialize vào JS. Luôn null-check khi access relation trong `.map()` (ví dụ `val.license_plate ? val.license_plate.name : ''`)
- **`ng-repeat` trên `<option>`**: nếu data có relation null, expression `v.supplier.code` crash. Luôn dùng ternary check: `v.supplier ? v.supplier.code : ''`

### Select2 Variants

| Class               | Init khi nào                | Dùng cho                        |
| -------------------- | --------------------------- | ------------------------------- |
| `select2`            | Page load                   | Select tĩnh ngoài modal         |
| `select2-in-modal`   | Modal show (`show.bs.modal`)| Select tĩnh trong modal         |
| `select2-ajax`       | Focus event                 | Search server-side, ngoài modal |
| `select2-ajax-modal` | Focus event                 | Search server-side, trong modal |
| `select2-create`     | Thủ công trong code         | Select tạo mới item             |

### DataTable Pattern (server-side)

**Controller** (`searchData` method):
```php
use Yajra\DataTables\DataTables;
public function searchData(Request $request) {
    $query = ThisModel::query()->with([...]);
    return DataTables::of($query)
        ->editColumn('field', function ($obj) { ... })
        ->addColumn('action', function ($obj) { ... })
        ->rawColumns(['action', 'status'])
        ->make(true);
}
```

**Blade** (khung chuẩn):
```html
<div ng-controller="ControllerName">
    <table id="table-list">
        <thead>...</thead>
        <thead class="search-column"><tr id="search-header">
            <th class="text-search" data-column="code"></th>
            <th class="select-search" data-column="status"></th>
        </tr></thead>
    </table>
</div>
@section('script')
<script>
    column_data = { status: [...] };
    app.controller('ControllerName', function($scope, $http) {
        initSearchColumn('table-list');
        var datatable = $('#table-list').DataTable({
            serverSide: true,
            ajax: { url: '...', data: function(d) { mergeSearch(d); } },
            columns: [...],
            initComplete: datatableInitComplete(),
            drawCallback: function() { saveSearch(datatable); }
        });
    });
</script>
@endsection
```

### Global JS (public/js/app.js)

Hàm dùng chung, load trên mọi trang:
- `initSearchColumn(table_id)` — tạo input/select search cho DataTable header
- `datatableInitComplete()` — fill options vào select search từ `column_data`
- `mergeSearch(d)` — gom search params gửi server
- `saveSearch(table)` / `restoreSearch(table, object)` — lưu/khôi phục filter vào localStorage
- `triggerSelect2()` — trigger change tất cả select2
- `parseNumberString()`, `numberWithCommas()`, `formatCurrency()` — format số
- `buildFormData()`, `jsonToFormData()` — convert JSON → FormData

### Global Variables (layouts/app.blade.php)

Có sẵn trên mọi trang:
- `EMPLOYEES` — `Employee::getAll()` (chỉ status=1)
- `ALL_EMPLOYEES` — `Employee::getAll(true)` (kể cả nghỉ việc)
- `CONFIG` — `Config::getConfig()`
- `DEFAULT_USER` — thông tin user login (id, company_id, department_id, part_id, ...)
- `CSRF_TOKEN` — auto-refresh qua AJAX
- `price_types` — danh sách loại giá

### Response Pattern (BE → FE)

```php
// BE - Controller dùng ResponseTrait
use App\Http\Traits\ResponseTrait;
return $this->responseSuccess($data, 'Thao tác thành công');
return $this->responseErrors('Lỗi gì đó', $errors, 400);
```
```js
// FE - check response.success
$.ajax({
    success: function(response) {
        if (response.success) { toastr.success(response.message); }
        else { $scope.errors = response.errors; toastr.warning(response.message); }
    },
    error: function() { toastr.error('Đã có lỗi xảy ra'); }
});
```

### Validation Error Display (FE)

```html
<span class="invalid-feedback d-block" role="alert">
    <strong><% errors.field_name[0] %></strong>
</span>
```

### Module chính

| Module         | Prefix route           | Controller dir          | Nghiệp vụ                     |
| -------------- | ---------------------- | ----------------------- | ------------------------------ |
| Kho            | `admin/warehouse/`     | `Warehouse/`            | Nhập/xuất/tồn kho, chuyến xe  |
| Bán hàng       | `admin/sale/`          | `Sale/`, `Sale/Firm/`   | KH, NCC, HĐ, báo giá, quyết toán |
| Đơn hàng       | `admin/orders/`        | `Order/`                | PI, PO, order summary          |
| Kế toán        | `admin/accounting/`    | `Accounting/`           | Hạch toán, công nợ, sổ chi tiết |
| Thu chi         | `admin/income/`        | `IncomeExpenditure/`    | Phiếu thu, chi, báo có/nợ     |
| Bảo hành       | `admin/customercare/`  | `Customercare/`         | Bảo hành sửa chữa, HĐ DV     |
| Danh mục chung | `admin/`               | `Common/`               | Xe, tuyến, NV, phòng ban      |
| Hợp đồng       | `admin/contracts/`     | `Contract/`             | HĐ mua, bán, phụ lục          |

### Data Fix Pattern

Tạo method trong `database/seeds/UpdateDB.php`, chạy qua tinker:
```
php artisan tinker
>>> (new \Database\Seeds\UpdateDB)->fixSomething()
```

### Lưu ý khi fix bug TanPhatDev

- Log lỗi: `TanPhatDev/storage/logs/laravel-YYYY-MM-DD.log`
- `APP_DEBUG=true` trên local → PHP notice/warning có thể phá JS nếu output vào giữa `<script>` block
- Khi sửa hàm `getForSelect()` hoặc hàm trả data cho `@json()` → luôn kiểm tra null relation trước khi access property
- Nhiều model dùng `auth()->user()->info->company_id` — nếu chạy trong tinker sẽ ra notice vì không có auth context
