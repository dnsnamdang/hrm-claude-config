# Shared — Base Classes, Components & Utilities

## Cấu trúc thư mục mỗi Module Backend

```
Modules/{ModuleName}/
├── Entities/                    # Eloquent Model (extends BaseModel)
├── Http/
│   ├── Controllers/Api/V1/      # API Controller (extends ApiController)
│   └── Requests/                # Form Request (extends BaseRequest)
├── Services/                    # Business logic (extends BaseService)
├── Transformers/                # API Resource (extends ApiResource)
├── Routes/
│   └── api.php
└── Database/
    └── migrations/
```

Migration cũng có thể nằm ở: `hrm-api/database/migrations/`

---

## Base Classes Backend

### BaseModel — `app/Models/BaseModel.php`
- Tự động set `created_by`, `updated_by`, `company_id`, `department_id`, `part_id` khi create/update
- Relationships có sẵn: `employee_create()`, `employee_update()`, `employeeApprove()`
- Accessors: `employee_create_name`, `employee_update_name`, `employee_approve_name`
- Scope: `scopeCompany($query)` — lọc theo company

### ApiController — `app/Http/Controllers/ApiController.php`
- `responseJson($message, $code, $data)` — trả JSON chuẩn
- `apiGetList($resource, $additional)` — trả danh sách có phân trang
- Response format: `{ code, message, data, errors }`

### ApiResource — `Modules/Human/Transformers/ApiResource.php`
- Extends `JsonResource`, tự thêm `code` và `message` vào response
- `ApiResource::apiPaginate($query, $request)` — phân trang tự động
- Luôn tách 2 file: `SomeResource` (list) và `DetailSomeResource` (detail)
- Message dùng chung → viết trong `/resources/lang/vi/validation.php`

### BaseRequest — `Modules/Training/Http/Requests/BaseRequest.php`
- Extends `FormRequest`
- Validation fail → HTTP 422: `{ code: 422, errors: { field: 'message' } }`

### BaseService — `Modules/Training/Services/BaseService.php`
- Mọi Service đều extend class này

---

## Phân quyền danh sách theo cấp

Khi được xác nhận cần phân quyền theo cấp:

**Backend:**
```php
checkPermissionList($result, [
    'Xem danh sách ... theo tổng công ty',
    'Xem danh sách ... theo công ty',
    'Xem danh sách ... theo phòng ban',
    'Xem danh sách ... theo bộ phận',
    true
], 'table_name')
```

**Frontend:** Thêm `V2BaseCompanyDepartmentFilter` vào filter panel.

---

## V2Base Components Frontend

| Component | Dùng cho |
|-----------|----------|
| `V2BaseDataTable` | Bảng dữ liệu có phân trang, sắp xếp |
| `V2BaseFilterPanel` | Panel lọc: quick search + advanced filters |
| `V2BaseButton` | Nút bấm (primary, secondary, tertiary) |
| `V2BaseSelect` | Dropdown select |
| `V2BaseInput` | Input text |
| `V2BaseDatePicker` | Chọn ngày |
| `V2BaseLabel` | Label cho form |
| `V2BaseError` | Hiển thị lỗi validation |
| `V2BaseBadge` | Badge trạng thái — truyền `color` + `text` từ backend |
| `V2BaseTitleSubInfo` | Title + sub info trong bảng |
| `V2BaseCheckbox` | Checkbox |
| `V2BaseCurrencyInput` | Input tiền tệ |
| `V2BaseIconButton` | Nút icon |
| `V2BaseImportModal` | Modal import Excel |
| `V2BaseCompanyDepartmentFilter` | Filter phân quyền theo cấp |
| `FileAttachmentTable` | Bảng file đính kèm (upload, preview, download) |

---

## Utilities Frontend

```javascript
// Build query string cho GET request (hỗ trợ array params)
import { buildQuery } from '@/utils/url-action'

// Tính STT
import { getNumericalOrder } from '@/utils/common.js'
// getNumericalOrder(page, perPage, index)

// Date — LUÔN dùng file này, không tự viết riêng
import dayjs from '@/utils/plugins/dayjs.js'
// Nếu thiếu plugin → bổ sung vào file này để tái sử dụng
// Hiển thị: 'DD/MM/YYYY HH:mm' hoặc 'DD/MM/YYYY'
// Chỉ áp cho hiển thị data, KHÔNG áp cho input (V2BaseDatePicker)
```

---

## API call từ Vuex Store

```javascript
// GET
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

// DELETE
const response = await this.$store.dispatch('apiDeleteMethod', {
    url: `assign/tasks/${id}`
})

// Export Excel
const data = await this.$store.dispatch('apiExportExcel', {
    url: 'assign/tasks/export',
    params: { ...filters }
})

// Master select — ưu tiên dùng hàm có sẵn, KHÔNG tái dùng API index
const { data } = await this.$store.dispatch('apiGetMasterSelect', 'meeting_types')
const { data } = await this.$store.dispatch('apiGetMasterSelectByCurrentCompany', 'departments')
const { data } = await this.$store.dispatch('apiGetMasterSelectAll', 'positions')
const { data } = await this.$store.dispatch('apiGetMasterSelectCreatedBy', 'some_table')
```
