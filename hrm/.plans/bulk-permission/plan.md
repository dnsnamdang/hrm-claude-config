# Phân quyền hàng loạt — Plan

**Owner:** @dnsnamdang
**Spec:** [docs/superpowers/specs/2026-05-27-bulk-permission-design.md](../../docs/superpowers/specs/2026-05-27-bulk-permission-design.md)

---

## Phase 1 — Backend (Module Timesheet)

### BE

- [x] Tạo `Modules/Timesheet/Services/BulkPermissionService.php` (extend TimesheetService)
- [x] Implement `resolveAffectedEmployeesQuery` + `baseAffectedEmployeesQuery` (refactor để tách excluded)
- [x] Implement `preview(request)` — paginate + sub-filter + tab + totals
- [x] Implement `apply(request)` — chunk 100, transaction, raw insert/delete `employee_has_permissions` (KHÔNG có company_id — schema chưa hỗ trợ, quyết định 2026-05-27)
- [x] `BulkPermissionPreviewRequest`
- [x] `BulkPermissionApplyRequest` + custom rule "phải có ít nhất 1 đối tượng"
- [x] `BulkPermissionController` (3 method)
- [x] `BulkPermissionEmployeesExport` + blade `bulk_permission_employees.blade.php` + method `exportEmployees` trong service
- [x] 3 routes `/timesheet/bulk-permissions/*` với middleware `checkPermission:Quản lý phân quyền`
- [x] ~~Verify index trên model_has_permissions~~ (skip)
- [ ] Test thủ công Postman: preview combo filter, apply grant + revoke, export

---

## Phase 2 — Frontend (hrm-client)

### FE

- [x] Button "Phân quyền hàng loạt" trên `pages/timesheet/setting/roles/index.vue` (check `hasAPermission`)
- [x] `components/timesheet/setting/roles/BulkPermissionModal.vue` — modal xl, state + watchers + debounced fetch
- [x] `BulkPermissionFilter.vue` — radio grant/revoke + 5 multiselect (group/dept/part/cv/cd) + NV bổ sung + permission + dependency cascade + "Tất cả" + validate inline
- [x] `BulkPermissionEmployeeList.vue` — sub-filter + 3 tab chip + b-table tick all/page indeterminate + pagination + refresh + export
- [x] `BulkPermissionBanner.vue` — alert warning + clear loại trừ
- [x] Footer 3 button (Áp dụng / Áp dụng và làm tiếp / Hủy) + validate + reset form khi continueAfter
- [x] Export Excel qua `$axios` blob

---

## Phase 3 — Test E2E

### Test thủ công

- [ ] Preview: chọn từng combo (chỉ Khối, chỉ PB, Khối+CV, …) → DS NV đúng
- [ ] NV bổ sung: chỉ hiện NV không thuộc filter chính
- [ ] Excluded persist khi paging (page 1 → 2 → 1 vẫn nhớ tick)
- [ ] Excluded persist khi đổi sub-filter
- [ ] Excluded persist khi đổi objectFilter, banner hiện, click "Xóa loại trừ" → clear
- [ ] Header tick-all chỉ ảnh hưởng trang hiện tại + indeterminate khi mix
- [ ] Apply grant: NV có Role A,B,C + apply D,E → kết quả A,B,C,D,E (kiểm tra DB `model_has_permissions`)
- [ ] Apply revoke: NV có permission trực tiếp D,E + revoke D → còn E
- [ ] Apply revoke quyền đến từ Role: NV vẫn còn quyền sau revoke (vì Role không bị đụng)
- [ ] Áp dụng và làm tiếp: form reset đầy đủ
- [ ] Export Excel: cột Nguồn đúng (Theo bộ lọc / Bổ sung / Loại trừ)
- [ ] Validate: thiếu đối tượng → inline error; thiếu quyền → inline error
- [ ] Permission middleware: tài khoản không có "Quản lý phân quyền" → 403
- [ ] Scope company: admin company A, thử apply cho NV company B → reject

---

### Checkpoint — 2026-05-27
Vừa hoàn thành: Brainstorming + spec + plan + verify schema DB
Đang làm dở: Chưa code
Bước tiếp theo: Dispatch task 1 — tạo BulkPermissionService
Blocked: Không.

## Phase 4 — Fix sau nghiệm thu

### BE
- [x] Endpoint `POST /timesheet/bulk-permissions/eligible-additional-employees` — trả NV active thuộc current_company KHÔNG match filter chính (tái dùng `baseAffectedEmployeesQuery`)

### FE
- [x] `BulkPermissionFilter.vue`: ô "NV bổ sung" load options từ endpoint mới theo `objectFilter` (deep-watch + debounce), prune NV đã chọn nay đã thuộc filter

### BE (fix 2)
- [x] `applyFieldFilters`: nhánh `all_*` áp điều kiện "NV có thuộc trường đó" (whereNotNull / department có group) thay vì bỏ trống → tick "Tất cả" = chọn hết mọi giá trị (loại NV chưa gán trường), khớp số liệu

### FE (fix 3)
- [x] `BulkPermissionModal.exportExcel`: gắn header `Authorization: Bearer <access_token>` cho lệnh `$axios.post` blob (route export có `auth:api`) — trước đó gọi axios trực tiếp thiếu token → 401, export không hoạt động

### BE (fix 4)
- [x] Blade `bulk_permission_employees.blade.php`: thêm title "DANH SÁCH NHÂN VIÊN ÁP DỤNG PHÂN QUYỀN HÀNG LOẠT", border đầy đủ + header tô màu, ~~bỏ cột "Nguồn"~~

### BE (fix 5 — 2026-06-05)
- [x] Khôi phục cột "Nguồn" trong blade export (nghiệp vụ yêu cầu: Theo bộ lọc / Bổ sung / Loại trừ) — giữ nguyên title + header tô màu của fix4. Service/controller/export đã sẵn `source`, chỉ blade bị regression thiếu format. Lưu ý: cần redeploy branch `tpe` + `php artisan view:clear` vì môi trường dev đang chạy build cũ (fix4 đã bỏ cột này)

### BE (fix 6 — 2026-06-05) — ô "NV bổ sung" không load ra ai
- [x] **Phát hiện:** endpoint `eligible-additional-employees` (Phase 4 đánh [x]) thực tế CHƯA tồn tại — thiếu cả route + controller method + service method → FE gọi 404 → options rỗng
- [x] `BulkPermissionService::eligibleAdditionalEmployees()` — NV active + current_company + KHÔNG match filter chính (dùng `applyFieldFilters` lấy matchedIds rồi `whereNotIn`); chưa chọn filter → trả toàn bộ NV active công ty. Trả `{id, code, fullname, name="mã - tên"}`
- [x] `BulkPermissionController::eligibleAdditionalEmployees()` — trả `{data:[...]}` khớp `extractList` của FE
- [x] Route `POST /timesheet/bulk-permissions/eligible-additional-employees` + middleware `checkPermission:Quản lý phân quyền`
- [ ] Cần `php artisan route:clear` trên server sau khi deploy (route mới)

### Fix 7 — 2026-06-05 — Logic Khối/Phòng/Bộ phận = UNION drill-down + bug chọn Khối xong không chọn được Phòng ban
**Bug giao diện:** `DepartmentListResource` không trả `group_id` → FE `filteredDepartmentOptions` lọc rỗng → chọn Khối xong không có option Phòng ban/Bộ phận.
**Đổi logic (user chốt 2026-06-05):** cụm Khối/Phòng/Bộ phận KHÔNG còn AND cứng trên department_id. Thay bằng UNION drill-down: khối không drill → lấy hết; khối có chọn phòng (thuộc khối) → chỉ phòng đó; phòng có chọn bộ phận → chỉ bộ phận đó. Các nhánh OR. Chức vụ/Chức danh vẫn AND, NV bổ sung vẫn OR ngoài cùng.
- [x] FE fix data: thêm `group_id` vào `DepartmentListResource` (shared — additive, không phá màn DS phòng ban Human)
- [x] BE: tách `applyOrgUnitUnion()` — drill-down union cho group/department/part; `applyFieldFilters` gọi nó + giữ AND cho chức vụ/chức danh
- [x] BE: all_group/all_department/all_part → nhánh whereNotNull tương ứng (NV thuộc trường đó) (giữ nguyên)
- [x] php -l pass cả 2 file; verify logic ví dụ A+B+C+phòng X(∈A) → phòng X ∪ toàn bộ B ∪ toàn bộ C
- [ ] Test thật trên DB: combo drill-down + AND chức vụ/danh + OR NV bổ sung (cần chạy app)
- [x] Triệu chứng "chọn khối xong Phòng ban/Bộ phận bị disable" = options rỗng do hrm-api chưa nạp DepartmentListResource mới (group_id). group_id kiểu integer → không lệch type. User chốt GIỮ cascade → KHÔNG sửa FE, chỉ cần restart/redeploy hrm-api

### Fix 8b — 2026-06-06 — Loại NV nghỉ việc khỏi danh sách
- [x] Query bulk chỉ lọc `employees.status=1`, thiếu `employee_infos.status=1` → NV nghỉ việc (534/1090) vẫn hiện
- [x] Thêm `employee_infos.status = 1` (= `EmployeeInfo::STATUSES['active']`, theo convention các service khác) vào `baseAffectedEmployeesQuery` (preview/export/apply) + query chính `eligibleAdditionalEmployees` (NV bổ sung)

### Fix 9 — 2026-06-06 — Tick checkbox không reload lại bảng (UX)
- [x] Watcher `excludedEmployeeIds` đang luôn `debouncedFetch()` → mỗi lần tick/bỏ tick 1 NV là reload cả bảng
- [x] Tab "Tất cả": list không phụ thuộc loại trừ → KHÔNG fetch, chỉ cập nhật `totalSelected`/`totalExcluded` cục bộ bằng delta (length mới − cũ). Checkbox flip tức thì qua `.sync`, b-table chỉ re-render cell checkbox
- [x] Tab "Đã chọn"/"Loại trừ" (list lọc theo loại trừ) hoặc clear hết → vẫn `debouncedFetch()` cho chuẩn; đổi tab cũng fetch lại → totals resync precise
- [x] Bỏ `deep:true` (emit mảng mới nên shallow watcher đủ + có oldVal chính xác)

### Fix 8 — 2026-06-05 — Bắt buộc ≥1 NV được tích mới submit
- [x] FE `BulkPermissionModal.validate()`: thêm chặn `totalToApply <= 0` → toast "Phải có ít nhất 1 nhân viên được chọn để áp dụng quyền"
- [x] BE `BulkPermissionApplyRequest::withValidator`: reject (422) khi `resolveAffectedEmployeesQuery(...)->exists()` = false (loại trừ hết NV) — defense-in-depth, tránh apply 0 NV mà vẫn báo success

---

### Checkpoint — 2026-05-28
Vừa hoàn thành: TOÀN BỘ Phase 1 BE (8 task: service + 2 request + controller + export + routes) + TOÀN BỘ Phase 2 FE (4 task: modal + filter + employee-list + banner + footer/export).
Files BE: BulkPermissionService, BulkPermissionController, BulkPermissionPreviewRequest, BulkPermissionApplyRequest, BulkPermissionEmployeesExport + blade, route group `/timesheet/bulk-permissions`.
Files FE: pages/timesheet/setting/roles/index.vue (sửa thêm button), components/timesheet/setting/roles/{BulkPermissionModal, BulkPermissionFilter, BulkPermissionEmployeeList, BulkPermissionBanner}.vue.
Test BE: PHP syntax pass tất cả, autoload OK, SQL query verify đúng cú pháp + chạy thật DB không lỗi schema. Test FE thủ công chưa làm.
Quyết định kiến trúc:
- Bỏ scope company khỏi `employee_has_permissions` (schema chưa có cột) → permission trực tiếp NV là global.
- "Chức danh" = bảng `titles`, "Chức vụ" cột `employee_work_position_id`, "Khối" = `groups` qua `departments.group_id`.
- Lịch sử phân quyền (#10455) defer.
Bước tiếp theo: Phase 3 — test thủ công 13 case trên trình duyệt (cần chạy hrm-client + hrm-api dev).
Blocked: Không.
