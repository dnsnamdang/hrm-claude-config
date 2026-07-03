# Báo cáo task BE — Manager gia hạn / kết thúc sớm phiếu giao công tác

- **Ngày:** 2026-06-24
- **STATUS:** DONE

## Danh sách file tạo / sửa

### 1. SỬA — `Modules/Timesheet/Services/BusinessTripAssignService.php`
Method `finishExtend($request, $type)` (~dòng 255).
- Thêm đọc `employee_info_id` (optional) → cờ `$isManager`.
- Nhánh manager: tìm `BusinessTripEmployee` theo `employee_id = employee_info_id` + `business_trip_assign_id`; không thấy → `['success'=>false,'message'=>'Không tìm thấy nhân sự trong phiếu công tác']`; check `employee_id` nằm trong `listManageEmployeeInfoIds(false, null, true)`, không → `['success'=>false,'message'=>'Bạn không có quyền thao tác với nhân sự này']`; set `$employee_info_id = $businessTripEmployee->employee_id`.
- Nhánh self giữ nguyên (khi không có `employee_info_id`).
- Message chặn trùng tách theo nhánh: self = "Bạn đã có yêu cầu...", manager = "Nhân sự này đã có yêu cầu kết thúc/gia hạn công tác đang chờ duyệt".
- Phần sau (check pending theo `$businessTripEmployee->id`, `validateExtendOverlap` khi type==2, create `BusinessTripEmployeeRequest`) dùng chung, không đổi.
- Thay đổi: +~25 dòng (block self/manager + message điều kiện).

### 2. TẠO — `Modules/Timesheet/Http/Requests/BusinessTripManagerFinishExtendRequest.php`
FormRequest mới (~49 dòng).
- rules: `id` required|exists:business_trip_assigns,id; `employee_info_id` required|exists:employee_infos,id; `date` required|date; `type` required|in:1,2.
- `authorize()` return true.
- `messages()` tiếng Việt.
- Rethrow ValidationException theo mặc định FormRequest (không catch chung).

### 3. SỬA — `Modules/Timesheet/Http/Controllers/Api/V1/BusinessTripAssignController.php`
- Thêm `use Modules\Timesheet\Http\Requests\BusinessTripManagerFinishExtendRequest;`.
- Thêm 2 method `managerFinish(BusinessTripManagerFinishExtendRequest $request)` (type=1) và `managerExtend(...)` (type=2), đặt ngay trước `listFinishExtend()`.
  - Đầu method: gate `if (!isCurrentEmployeeHasPermission('Gia hạn, kết thúc sớm phiếu công tác')) return $this->responseJson('Bạn không có quyền thực hiện chức năng này', 403);`.
  - Gọi `finishExtend($request, 1|2)`; success → gửi notification approver (mirror `finish()`/`extend()`: `listEmployeeInfoHasPermission('Quản lý phiếu đi công tác', ...)` + `sendToAllNotification`, title "kết thúc"/"gia hạn") + `responseSuccessMobileJson`; fail → `responseErrorMobileJson($msg, [], 422)`; bọc try/catch + `Log::error` như finish().
- Thay đổi: +1 dòng use, +~54 dòng 2 method.

### 4. SỬA — `Modules/Timesheet/Routes/api.php`
Trong group `/timesheet/business_trip_assigns` (auth:api), thêm ngay sau `/finish`, `/extend`:
```php
Route::post('/manager/finish', [BusinessTripAssignController::class, 'managerFinish']);
Route::post('/manager/extend', [BusinessTripAssignController::class, 'managerExtend']);
```
Không gắn `checkPermission` (gate trong controller, lý do tên quyền có dấu phẩy). +2 dòng.

## Kết quả `php -l`

```
=== Modules/Timesheet/Services/BusinessTripAssignService.php ===
No syntax errors detected in Modules/Timesheet/Services/BusinessTripAssignService.php
=== Modules/Timesheet/Http/Requests/BusinessTripManagerFinishExtendRequest.php ===
No syntax errors detected in Modules/Timesheet/Http/Requests/BusinessTripManagerFinishExtendRequest.php
=== Modules/Timesheet/Http/Controllers/Api/V1/BusinessTripAssignController.php ===
No syntax errors detected in Modules/Timesheet/Http/Controllers/Api/V1/BusinessTripAssignController.php
=== Modules/Timesheet/Routes/api.php ===
No syntax errors detected in Modules/Timesheet/Routes/api.php
```

## Điều chỉnh contract (revision 2026-06-24)
- ĐỔI param nhánh manager: `business_trip_employee_id` → `employee_info_id`. Lý do: `BusinessTripEmployeeResource` expose `id => employee_id` (= employee_info_id) nên FE chỉ có sẵn `employee_info_id`; lookup này mirror đúng nhánh self.
- Service: đọc `$targetId = $request->get('employee_info_id')`; lookup `BusinessTripEmployee::where('employee_id', $targetId)->where('business_trip_assign_id', $id)`. Phần còn lại giữ nguyên.
- FormRequest: rule `employee_info_id` => `required|exists:employee_infos,id` + message tương ứng.
- Controller `managerFinish`/`managerExtend` KHÔNG đổi.

## Điểm cần lưu ý / nghi ngờ
- `isCurrentEmployeeHasPermission(...)` được gọi dạng global helper (giống `index()` ở dòng 53 hiện có dùng `isCurrentEmployeeHasPermission(...)` không qua `$this->`). Đã dùng cùng cách → nhất quán.
- FormRequest đã validate `type` required|in:1,2 ở tầng request, nhưng controller vẫn truyền hằng số (1/2) vào service nên `type` trong body không ảnh hưởng tới loại yêu cầu thực tế (an toàn, mirror spec). Field `type` vẫn validate để FE gửi đúng payload chung.
- Không viết unit test: module không có hạ tầng test sẵn cho luồng này (test thủ công là chính theo convention dự án).
- Không đụng self-flow (`finish`/`extend`/route cũ) — `business_trip_employee_id` optional nên self chạy y như cũ.
