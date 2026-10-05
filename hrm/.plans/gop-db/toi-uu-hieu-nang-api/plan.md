# Tối ưu hiệu năng API dùng chung (nhánh `gop_db`) — @namdangit

Mục tiêu: cắt các query lặp ở **code dùng chung**, tác động lên MỌI API, không sửa riêng 1 màn.

## Phase 1 — Đệm theo request cho code dùng chung (BE)

- [x] Thêm `app/Support/RequestCache.php` — đệm sống trong 1 request, `flush()` ở ranh giới job queue
- [x] `AppServiceProvider`: `Queue::before/after` gọi `RequestCache::flush()` (worker sống lâu, static không tự sạch)
- [x] `BaseModel::hasColumnCached()` thay `Schema::hasColumn()` trong hook `creating`/`saving` (9 chỗ) — bỏ 4 query `information_schema` mỗi lần save
- [x] `BaseModel::currentEmployeeInfo()` — gộp 3 lần `EmployeeInfo::find()` trùng nhau trong 1 lần save
- [x] `BaseModel::cachedEmployeeName()` — 4 accessor `employee_create_name` / `employee_update_name` (+ bản `HasTime`) đệm theo `employees.id`, giữ nguyên quan hệ Eloquent để không mất global scope `CompanyActiveScope`
- [x] `BaseModel::isCurrentEmployeeHasPermission()` — đệm danh sách quyền theo `employee_info_id`
- [x] `PermissionService::isCurrentEmployeeHasPermission()` — đệm theo (`employee_info_id`, công ty)
- [x] Global function `isCurrentEmployeeHasPermission()` + `getAllCurrentPermission()` ở `app/Helper/PermissionHelper.php` (602 chỗ gọi) — đệm tương tự
- [x] `CheckPermission` middleware — đệm `getAllPermissions()` theo `employees.id`
- [x] `ErpPermissionHelper::erpEmployeeId()` + `userCan()` — đệm (trước đây gọi lại trên từng dòng danh sách)
- [x] `TpEmployee::getCurrentCompanyRoleAttribute()` — thuộc tính nằm trong `$appends`, 502 chỗ đọc, mỗi lần 1 query

### Kiểm chứng
- [x] So JSON 10 endpoint trước/sau → **giống hệt từng byte**
- [x] `CheckPermission` trả đúng 200/403 y bản cũ (kể cả chuỗi nhiều quyền `A|B`)
- [x] 6 user khác nhau trong CÙNG 1 tiến trình cho kết quả quyền khác nhau đúng → key đệm không rò chéo user
- [x] Ghi dữ liệu: `updated_by` / `company_id` vẫn được gán đúng

### Kết quả đo (20 dòng/trang, DB `local_hrm_erp`)
| API | Query trước | Query sau |
|---|---|---|
| `/assign/customers` | 190 | **31** |
| `/human/employee-infos` | 62 | **26** |
| `/assign/issues` | 23 | **11** |
| `/assign/prospective-projects` | 60 | **37** |
| `/assign/tasks` | 71 | **54** |
| Ghi 30 dòng (`save()`) | 208 query / 343ms | **33 query / 71ms** |

## Phase 2 — Còn tồn (chưa làm)

- [ ] N+1 viết tay trong từng Resource (không dùng accessor chung): `QuotationResource.php:98` (40 query/trang), `DepartmentResource/DepartmentListResource.php:38` (20), `Timesheet/EmployeeResource/ListResource.php:23` (13) → fix bằng `with(['employee_update.info'])` ở Service của từng màn
- [ ] `CustomerListResource.php:67,71` trả trùng `creator_name`/`editor_name` đã join sẵn — bỏ 2 dòng accessor
- [ ] `CustomerListResource.php:72` hard-code `'is_can_edit' => true` — vi phạm rule fail-closed
- [ ] Máy dev: API chạy `php -S` 1 worker → mọi request xếp hàng. Đặt `PHP_CLI_SERVER_WORKERS=8` hoặc chuyển php-fpm/Octane

### Checkpoint — 2026-09-21
Vừa hoàn thành: Phase 1 (11 file BE), đã đo và đối chiếu JSON trước/sau.
Đang làm dở: không.
Bước tiếp theo: Phase 2 — eager load cho Resource viết tay, và đổi cách chạy API dev.
Blocked:
