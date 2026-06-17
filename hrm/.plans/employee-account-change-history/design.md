# Lịch sử thay đổi cho màn Quản lý tài khoản nhân viên (human/employee)

- **Ngày:** 2026-06-01
- **Tác giả:** @khoipv
- **Phạm vi:** Bổ sung tính năng "Lịch sử thay đổi" cho màn `human/employee` (màn quản lý tài
  khoản đăng nhập của nhân viên), tham khảo pattern lịch sử của màn `assign/tasks`.

## 1. Bối cảnh

Màn `human/employee` quản lý **tài khoản đăng nhập** (entity `Employee`): liên kết
email/password/trạng thái/công ty với một hồ sơ nhân sự (`employee_info_id`). Hiện màn này
**chưa có lịch sử thay đổi** nào.

Lưu ý: đã tồn tại hệ thống log riêng cho **hồ sơ** nhân sự (`employee_infos_logs` /
`EmployeeInfoLog`, gắn với quyết định) — nhưng đó phục vụ màn `employee_info`, **không** áp dụng
cho màn account này. Tính năng dưới đây là một hệ thống lịch sử **độc lập**, mirror theo
`task_history` của module Assign.

### Pattern tham khảo (assign/tasks)

- Bảng `task_history`: `task_id, action (create|update|change_status), old_value (JSON),
  new_value (JSON), changed_by, changed_at`.
- `TaskService::logHistory()` + `buildHistorySnapshot()` ghi snapshot khi create/update.
- `DetailTaskResource::formatHistory()` resolve ID→tên, enum→nhãn, format ngày.
- Frontend `TaskHistoryModal.vue`: timeline, diff old/new JSON phía client, mở từ action trên
  từng dòng danh sách.

## 2. Các quyết định thiết kế đã chốt

- **Điểm truy cập:** nút "Lịch sử" trên từng dòng ở `pages/human/employee/index.vue`, mở modal
  (giống tasks).
- **Cách lấy dữ liệu:** endpoint riêng `GET /human/employee/{id}/histories` (KHÔNG nhồi vào
  resource detail dùng chung). Đồng nhất với pattern `get-logs` sẵn có trong module Human.
- **Trường theo dõi:** `email`, `status`, `rice_setting_location_id`, `company_ids`, và cờ
  `password_changed`. **Mật khẩu không bao giờ lưu giá trị** — chỉ ghi cờ "đã đổi".
- **Action:** `create`, `update`, `change_status` (mirror tasks).

## 3. Backend

### 3.1. Migration — bảng `employee_history`

File: `hrm-api/Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php`

Mirror `task_history`. **Bắt buộc có PHPDoc trên `up()` và `down()`** theo file mẫu của project.

| Cột          | Kiểu                              | Ghi chú                                       |
| ------------ | --------------------------------- | --------------------------------------------- |
| `id`         | `id()`                            |                                               |
| `employee_id`| `unsignedBigInteger`              | ID tài khoản nhân viên                        |
| `action`     | `string`                          | `create` / `update` / `change_status`         |
| `old_value`  | `text` nullable                   | Snapshot cũ (JSON)                            |
| `new_value`  | `text` nullable                   | Snapshot mới (JSON)                           |
| `changed_by` | `unsignedBigInteger`              | Người thực hiện (`auth()->id()`)              |
| `changed_at` | `timestamp` `useCurrent()`        | Thời điểm thay đổi                            |
| `timestamps` |                                   |                                               |

`down()`: `Schema::dropIfExists('employee_history')`.

### 3.2. Entity — `EmployeeHistory`

File: `hrm-api/Modules/Human/Entities/EmployeeHistory.php`

```php
namespace Modules\Human\Entities;

use App\Models\BaseModel;

class EmployeeHistory extends BaseModel
{
    protected $table = 'employee_history';
    protected $fillable = ['employee_id', 'action', 'old_value', 'new_value', 'changed_by', 'changed_at'];

    public function employee()
    {
        return $this->belongsTo(Employee::class, 'employee_id');
    }

    public function user() // người thực hiện thay đổi
    {
        return $this->belongsTo(Employee::class, 'changed_by');
    }
}
```

Thêm quan hệ vào `Employee` (mirror `Task::history()`):

```php
public function history()
{
    return $this->hasMany(EmployeeHistory::class, 'employee_id')->orderBy('changed_at', 'asc');
}
```

### 3.3. Ghi lịch sử trong `EmployeeService`

Thêm 2 helper private (mirror `TaskService`):

- `logHistory($employeeId, $action, $oldValue, $newValue)` → `EmployeeHistory::create([...])` với
  `changed_by => auth()->id()`, `changed_at => now()`.
- `buildHistorySnapshot(Employee $employee, bool $passwordChanged = false): array` trả về:
  - `email`
  - `status`
  - `employee_info_id`
  - `rice_setting_location_id`
  - `company_ids` → `$employee->companies()->pluck('companies.id')->toArray()` (load lại sau
    `sync()` để lấy giá trị mới)
  - `password_changed` → `$passwordChanged`

**`createEmployee()`** (nhánh tạo mới `Employee` — nhánh `else`, sau `companies()->sync()` và
`save()`): gọi
`$this->logHistory($employee->id, 'create', null, json_encode($this->buildHistorySnapshot($employee)))`.
→ Bao phủ cả luồng tạo thủ công (`human/employee/add`) **và** luồng tự tạo tài khoản khi tạo hồ sơ
(`EmployeeInfoController::store` gọi `createEmployee`). Nhánh `if (!empty($id))` (fill bản ghi cũ)
**không** ghi history (đây là edge-case cập nhật, không phải tạo mới).

**`updateEmployee()`**:

1. Đầu hàm, sau khi tìm được `$employee`: `$oldSnapshot = $this->buildHistorySnapshot($employee);`
   và lưu `$oldStatus = $employee->status;`
2. Xác định `$passwordChanged = !empty($dataEmployee['password']) && !empty($dataEmployee['change_pass']);`
3. Thực hiện cập nhật + `companies()->sync()` như hiện tại.
4. Reload quan hệ companies, build `$newSnapshot = $this->buildHistorySnapshot($employee, $passwordChanged);`
5. Ghi log (mirror logic tasks):
   - Nếu `status` đổi **và** không có thay đổi nào khác (so sánh các trường còn lại của
     snapshot, bỏ qua `password_changed=false`) → `change_status` với
     `old_value = (string)$oldStatus`, `new_value = (string)$employee->status`.
   - Ngược lại → `update` với `old_value = json_encode($oldSnapshot)`,
     `new_value = json_encode($newSnapshot)`.

**`EmployeeController::updateStatus()`**: trước khi đổi, lấy `$old = $employee->status;` sau khi
`save()` → `logHistory($employee->id, 'change_status', (string)$old, (string)$request->status)`.
(Service không can thiệp ở đây vì updateStatus thao tác model trực tiếp.)

### 3.4. Endpoint & Resource

**Route** (`hrm-api/Modules/Human/Routes/api.php`, trong group `/human/employee`, đặt **trước**
`Route::get('/{id}', ...)` để tránh nuốt route):

```php
Route::get('/{id}/histories', [EmployeeController::class, 'histories']);
```

**`EmployeeController::histories($id)`**:

```php
$histories = EmployeeHistory::with('user.info')
    ->where('employee_id', $id)
    ->orderBy('changed_at', 'asc')
    ->get();

return $this->responseJson('success', Response::HTTP_OK,
    EmployeeHistoryResource::collection($histories)->resolve());
```

**`EmployeeHistoryResource`** (`hrm-api/Modules/Human/Transformers/EmployeeResource/EmployeeHistoryResource.php`):

Trả về mỗi item:

- `id`, `action`
- `old_value`, `new_value`: resolve ID→tên trong JSON snapshot (mirror
  `DetailTaskResource::resolveIdFields`):
  - `company_ids` (mảng) → mảng tên công ty (`Company::whereIn('id', ...)`)
  - `rice_setting_location_id` → tên địa điểm (bảng rice setting location)
  - `employee_info_id` → họ tên (`EmployeeInfo`/`info.fullname`)
  - `status` → nhãn (1: "Hoạt động", 0: "Khóa")
  - `password_changed` giữ nguyên (frontend hiển thị "Đã thay đổi")
  - Với `change_status`, `old_value`/`new_value` là chuỗi status thô → resource trả nguyên,
    frontend map sang nhãn.
- `changed_by_name`: `optional(optional($item->user)->info)->fullname ?? optional($item->user)->email`
- `changed_at`: `Carbon::parse(...)->format('d/m/Y H:i:s')`

> Gom batch resolve ID giống `formatHistory` của tasks để tránh N+1 (thu thập toàn bộ company_ids /
> rice location ids / employee_info_ids trước, query 1 lần, rồi map). Có thể đặt logic này trong
> một method tĩnh/collection của resource hoặc trong controller trước khi tạo resource.

## 4. Frontend

### 4.1. `EmployeeHistoryModal.vue`

File: `hrm-client/pages/human/employee/components/EmployeeHistoryModal.vue`

Copy cấu trúc + CSS timeline của `pages/assign/tasks/components/TaskHistoryModal.vue`, điều chỉnh:

- Tiêu đề modal: "Lịch sử thay đổi tài khoản"; id modal: `employee-history-modal`.
- `ACTION_LABELS`: `{ create: 'Tạo mới tài khoản', update: 'Cập nhật thông tin', change_status: 'Thay đổi trạng thái' }`.
- `ACTION_COLORS`: giữ nguyên (create=green, update=amber, change_status=blue).
- `STATUS_LABELS`: `{ 1: 'Hoạt động', 0: 'Khóa' }`.
- `FIELD_LABELS`:
  - `email` → "Email"
  - `status` → "Trạng thái"
  - `company_ids` → "Công ty"
  - `rice_setting_location_id` → "Địa điểm nhận suất ăn"
  - `employee_info_id` → "Hồ sơ liên kết"
  - `password_changed` → "Mật khẩu"
- `LIST_FIELDS`: `['company_ids']` (diff added/removed như tasks).
- `IGNORED_FIELDS`: các trường kỹ thuật không hiển thị.
- Xử lý đặc biệt `password_changed`: khi `true` → dòng "Mật khẩu: Đã thay đổi" (không hiển thị
  old/new). Khi diff, nếu `password_changed` từ false→true thì render dòng này; bỏ qua nếu false.
- `fetchHistory(id)`: gọi `apiGetMethod` tới `human/employee/${id}/histories`, đọc mảng trả về
  (đã format sẵn server-side). Vì server đã resolve tên, phần `diffJson` chỉ cần so sánh chuỗi/
  mảng đã resolve.
- `open(item)`: set tiêu đề phụ (email hoặc tên), show modal, fetch.

### 4.2. `index.vue` — nút "Lịch sử" trên mỗi dòng

File: `hrm-client/pages/human/employee/index.vue`

- Trong `template v-slot:cell(Actions)`, thêm nút giữa Sửa và Xóa:

```html
<b-button
    variant="info"
    class="btn-mini"
    @click="$refs.employeeHistoryModal.open(item)"
    v-if="hasPermissionEmployeeAccount"
    title="Lịch sử thay đổi"
>
    <i class="ri-history-line"></i>
</b-button>
```

- Import + đăng ký component `EmployeeHistoryModal` (dynamic import như tasks), đặt
  `<EmployeeHistoryModal ref="employeeHistoryModal" />` trong template.

## 5. Bảo mật & lưu ý

- **Không bao giờ** ghi giá trị mật khẩu (cả plain lẫn hash) vào `old_value`/`new_value`. Chỉ cờ
  `password_changed`.
- Endpoint `/histories` gắn cùng nhóm middleware/permission như các route `/human/employee` khác
  (quyền "Quản lý tài khoản nhân viên").
- Snapshot lưu `company_ids` dạng ID; tên được resolve lúc đọc → tránh lưu tên cũ bị lệch khi công
  ty đổi tên.

## 6. Phạm vi KHÔNG làm (YAGNI)

- Không đụng tới hệ thống `employee_infos_logs` của màn hồ sơ.
- Không log thao tác `delete` thành action riêng (xóa = set status=0, đã được phản ánh qua luồng
  cập nhật trạng thái nếu đi qua các path trên; `EmployeeService::deleteEmployee` không bắt buộc
  ghi history ở giai đoạn này).
- Không theo dõi `rice_ssn` (auto-derive từ hồ sơ) và không tách `employee_info_id` thành thay đổi
  (chỉ set lúc tạo, disabled khi sửa).

## 7. Danh sách file thay đổi

**hrm-api:**

- (mới) `Modules/Human/Database/Migrations/2026_06_01_000001_create_employee_history_table.php`
- (mới) `Modules/Human/Entities/EmployeeHistory.php`
- (mới) `Modules/Human/Transformers/EmployeeResource/EmployeeHistoryResource.php`
- (sửa) `Modules/Human/Entities/Employee.php` — thêm `history()`
- (sửa) `Modules/Human/Services/EmployeeService.php` — `logHistory`, `buildHistorySnapshot`, ghi
  log trong `createEmployee`/`updateEmployee`
- (sửa) `Modules/Human/Http/Controllers/Api/V1/EmployeeController.php` — `histories()` + ghi log
  trong `updateStatus()`
- (sửa) `Modules/Human/Routes/api.php` — route `/{id}/histories`

**hrm-client:**

- (mới) `pages/human/employee/components/EmployeeHistoryModal.vue`
- (sửa) `pages/human/employee/index.vue` — nút "Lịch sử" + đăng ký modal
