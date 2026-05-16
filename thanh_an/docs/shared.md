# Shared — Base Classes, Components & Utilities

## Cấu trúc thư mục mỗi Module Backend

```
Modules/{ModuleName}/
├── Entities/                       # Eloquent Model (extends BaseModel)
├── Http/
│   ├── Controllers/Api/V1/         # API Controller (extends BaseApiController)
│   └── Requests/                   # Form Request (extends BaseRequest)
├── Services/                       # Business logic (extends BaseService)
├── Transformers/                   # API Resource (extends ApiResource)
├── Routes/
│   └── api.php
└── Database/
    └── migrations/
```

Migration cũng có thể nằm ở: `hrm-thanhan-api/database/migrations/`

**Lưu ý về các module có cấu trúc khác:**
- `Modules/Management` hiện chưa có `Services/` và `Transformers/`, `Http/Controllers/Api` không có `V1/`
- `Modules/Training` `Http/Controllers/Api` không có `V1/`

---

## Base Classes Backend

### BaseModel — `app/Models/BaseModel.php`
- Tự động set `created_by`, `updated_by`, `company_id`, `department_id` khi create/update
- Relationships có sẵn: `employee_create()`, `employee_update()`, `employeeApprove()`
- Accessors: `employee_create_name` (chỉ có accessor này; `employee_update_name` và `employee_approve_name` chưa được khai báo — nếu cần thì tự viết)
- Scope: `scopeCompany($query)` — lọc theo company

### BaseApiController — `app/Http/Controllers/Api/BaseApiController.php`
- Class abstract, dùng trait `App\Http\Controllers\Api\Traits\ResponseTrait`
- Controller trong module **extend `BaseApiController`** (không phải `ApiController`)

### ResponseTrait — `app/Http/Controllers/Api/Traits/ResponseTrait.php`
- `responseJson($message, $code, $data)` — trả JSON chuẩn
- `apiGetList($data, array $additional = [], $code = 200)` — trả danh sách có phân trang
- `responseSuccess($data, $message, $code)`, `responseErrors(...)` — tiện ích khác
- Response format: `{ code, message, data, errors }`

### ApiResource — `Modules/{Module}/Transformers/ApiResource.php`
- Extends `JsonResource`, tự thêm `code` và `message` vào response
- **Lưu ý:** Module `Human`, `Timesheet` có `ApiResource::apiPaginate($query, $request, $maxPageSize = null)`. Module `Assign`, `Payroll` có `ApiResource` bản giản lược (không có `apiPaginate`)
- Luôn tách 2 file: `SomeResource` (list) và `DetailSomeResource` (detail)
- Message dùng chung → viết trong `/resources/lang/vi/validation.php`

### BaseRequest — `Modules/Training/Http/Requests/BaseRequest.php`
- Extends `FormRequest`
- Validation fail → ném exception HTTP 422: `{ code: 422, errors: { field: 'message' } }`

### BaseService — `Modules/Training/Services/BaseService.php`
- Có method `checkPermissionList($query, array $permissions, $table = null)` để lọc theo phân quyền cấp
- Module `Timesheet`, `Human` service extend class này

---

## Helpers Backend

### Global helpers (autoload từ `composer.json`)
- `app/Helper/PermissionHelper.php` — các hàm permission: `isCurrentEmployeeHasPermission()`, `listManageDepartmentIds()`, `listManageEmployeeIdsByGroup()`, v.v.
- `app/Helper/FormatHelper.php` — các hàm format: `formatCurrency()`, `truncate_number()`, `convertNumberToWords()`, v.v.

### Helper tiện ích ở module
- `Modules/Human/Helper/Helper.php` — có method static `formatDate($date)`, `formatTime($time)`, `formatDateTime($datetime)`

---

## Middleware phân quyền

### `checkPermission` — `app/Http/Middleware/CheckPermission.php`
- Đăng ký trong `app/Http/Kernel.php` mảng `$routeMiddleware`
- Dùng trong route: `->middleware('checkPermission:Tên quyền')`
- Nhận permission dạng pipe-separated: `'checkPermission:Perm1|Perm2'`
- Fail → HTTP 403

---

## Phân quyền danh sách theo cấp

Ở Thành An, business chỉ dùng **3 cấp**: **tổng công ty → công ty → nhóm nghiệp vụ**

Method `checkPermissionList($query, array $permissions, $table)` của `BaseService` nhận mảng 5 phần tử; với dns, bỏ qua index [2] (phòng ban) bằng cách truyền `null`:

| Index | Cấp | dns dùng? |
|---|---|---|
| [0] | Tổng công ty (không filter) | ✅ |
| [1] | Công ty (filter `company_id`) | ✅ |
| [2] | Phòng ban (filter theo `listManageDepartmentIds()`) | ❌ truyền `null` |
| [3] | Nhóm nghiệp vụ (filter theo `listManageEmployeeIdsByGroup()`) | ✅ |
| [4] | Bản thân — chỉ thấy bản ghi mình tạo (giá trị `true` để bật fallback) | ✅ |

**Backend:**
```php
$this->checkPermissionList($query, [
    'Xem danh sách ... theo tổng công ty',     // [0]
    'Xem danh sách ... theo công ty',           // [1]
    null,                                        // [2] phòng ban
    'Xem danh sách ... theo nhóm nghiệp vụ',    // [3]
    true                                         // [4] fallback về bản thân
], 'table_name');
```

**Frontend:** filter tương ứng thường gồm công ty + nhóm nghiệp vụ. Component `CompanyDepartmentFilter` ở `components/common/` có thể tái dùng — nếu không khớp với 3-cấp của dns thì tạo filter riêng (công ty + group) ở module.

---

## Base Components Frontend

Dùng `Base*` (custom wrapper) kết hợp với Bootstrap-Vue.

### Custom Base Components (nằm ở `components/`)

| Component | Dùng cho |
|-----------|----------|
| `BaseAddButton` | Nút thêm |
| `BaseCurrencyInput` | Input tiền tệ |
| `BaseDatePicker` | Chọn ngày (wrapper quanh vue2-datepicker) |
| `BaseHelperError` | Hiển thị lỗi validation |
| `BaseInputField` | Input text custom |
| `BaseSelect2` | Dropdown wrapper quanh `v-select2-component` |
| `BaseSelect2Multi` | Dropdown multi-select |
| `BaseStatusColor` | Badge trạng thái (màu + text) |
| `BaseUploadFile` / `BaseUploadFileProduct` / `BaseUploadFileBidPackage` / `BaseUploadFileSelfNotification` | Các variant upload file theo ngữ cảnh |

### Common components (`components/common/`)

| Component | Dùng cho |
|-----------|----------|
| `CompanyDepartmentFilter` | Filter công ty / phòng ban cho phân quyền cấp |

### Bootstrap-Vue (dùng trực tiếp, không cần wrap)

| Component | Mô tả |
|-----------|-------|
| `<b-table>` | Bảng dữ liệu (có sort/pagination qua props) |
| `<b-pagination>` | Phân trang |
| `<b-form-input>` | Input text |
| `<b-form-select>` | Select đơn giản |
| `<b-form-checkbox>` | Checkbox |
| `<b-button>` | Nút bấm |
| `<b-modal>` | Modal |
| `<b-collapse>` | Collapsible (thường dùng cho filter panel) |
| `<b-dropdown>` | Dropdown menu |
| `<b-spinner>` | Loading indicator |

### Third-party

- `v-select2-component` → `<Select2>` — dùng cho advanced select (thường thông qua `BaseSelect2`)
- `multiselect` (`vue-multiselect`) — multi-select ở 1 số màn (ví dụ `payroll/manpower-allocations`)
- `dayjs` (qua `@/utils/plugins/dayjs.js`) — format date display
- `moment` — vẫn còn dùng ở 1 số nơi (đang chuyển dần sang dayjs)

### Badge trạng thái

Hiện dùng inline `<span class="badge ...">` hoặc component `BaseStatusColor`, chưa có component base table-wide cho badge status.

---

## Utilities Frontend

```javascript
// Build query string cho GET request (hỗ trợ array params)
import { buildQuery, buildQueryString } from '@/utils/url-action'

// Tính STT — getNumericalOrder(page, perPage, index)
import { getNumericalOrder } from '@/utils/common.js'

// Date — LUÔN dùng file này, không tự viết riêng
import dayjs from '@/utils/plugins/dayjs.js'
// Nếu thiếu plugin → bổ sung vào file này để tái sử dụng
// Hiển thị: 'DD/MM/YYYY HH:mm' hoặc 'DD/MM/YYYY'
// Chỉ áp cho hiển thị data, KHÔNG áp cho input (BaseDatePicker)

// Các util khác ở common.js
import { getStatusClass, getStatusText } from '@/utils/common.js'
```

---

## API call từ Vuex Store

Store có 2 họ action: họ ngắn (`apiGet`, `apiPost`...) và họ `*Method` (`apiGetMethod`, `apiPostMethod`...). Kiểm tra signature trong `store/` trước khi dùng nếu không chắc. Ví dụ thực tế:

```javascript
// GET — dùng để lấy list, response bao gồm { data, meta } hoặc raw response
const response = await this.$store.dispatch('apiGet', `category/array_products${buildQueryString(params)}`)
// Hoặc dùng apiGetMethod nếu muốn chỉ data (check signature từng trường hợp)
const { data, meta } = await this.$store.dispatch('apiGetMethod', 'assign/tasks')

// POST
const response = await this.$store.dispatch('apiPostMethod', {
    url: 'assign/tasks',
    payload: { title: 'Task mới' }
})

// PUT
const response = await this.$store.dispatch('apiPutMethod', {
    url: `assign/tasks/${id}`,
    payload: { title: 'Sửa task' }
})

// DELETE — tên là apiDelete (không có apiDeleteMethod)
const response = await this.$store.dispatch('apiDelete', `assign/tasks/${id}`)

// Master select
const { data } = await this.$store.dispatch('apiGetMasterSelect', 'meeting_types')
const { data } = await this.$store.dispatch('apiGetMasterSelectCreatedBy', 'some_table')
const { data } = await this.$store.dispatch('apiGetMasterSelectUpdatedBy', 'some_table')
```

**Không tồn tại trong dns:**
- `apiDeleteMethod` — dùng `apiDelete` thay thế
- `apiExportExcel` — export Excel không có action dùng chung; mỗi module tự xử lý (xem `.skills/export-excel/SKILL.md`)
- `apiGetMasterSelectByCurrentCompany`, `apiGetMasterSelectAll` — không có

---

## SCSS

Các file style nằm ở `assets/scss/`:
- `app.scss`, `bootstrap.scss` — base
- `custom.scss`, `custom-form.scss`, `custom-table.scss`, `custom-theme.scss` — override Bootstrap
- `category.scss`, `custom-assign.scss`, `custom-timesheet.scss`, `custom-client.scss` — theo module
- `editor.scss` — style cho editor

