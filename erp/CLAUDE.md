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