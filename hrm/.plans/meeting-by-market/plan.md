# Báo cáo Kết quả meeting theo thị trường — Implementation Plan

> **For agentic workers:** Thực thi bằng superpowers:subagent-driven-development (khuyến nghị) hoặc executing-plans, task-by-task. Steps dùng checkbox `- [ ]`.
> **Spec đầy đủ:** `docs/superpowers/specs/2026-08-16-meeting-by-market-design.md` · **Tóm tắt:** `.plans/meeting-by-market/design.md`

**Goal:** Thêm báo cáo độc lập `/assign/report/meeting-by-market` liệt kê meeting có khách hàng, nhóm Thị trường (Tỉnh KH) → Khách hàng → Meeting, 13 cột + 2 popup + Xuất Excel + phân quyền theo cấp.

**Architecture:** BE thêm route group `assign/report/meeting-by-market` + Controller + Service riêng (query `meetings` DB HRM, resolve tỉnh KH batch qua ERP `mysql2`, scoping quyền fail-closed). FE trang report mới bám pattern `meeting-by-projects`. Phụ thuộc: thêm `assign_requests.meeting_id` + lưu khi tạo phiếu công tác từ meeting để join cột chấm công GPS.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL (2 connection: `mysql` HRM + `mysql2` ERP) · Nuxt 2 (Vue 2) / Bootstrap-Vue · spatie/permission · maatwebsite/excel.

## Global Constraints

- **KHÔNG commit/push git** (quy tắc dự án). Mỗi task kết thúc bằng bước **xác minh**, không `git commit` (chỉ commit khi user yêu cầu).
- **Fail-closed phân quyền:** cờ quyền FE khởi tạo `false`, chỉ set từ `hasAPermission(...)`. TUYỆT ĐỐI KHÔNG `= true` / `|| true`. BE scoping trong service.
- **Thị trường = Tỉnh của KH:** `meeting.customer_id → ERP customers.province_id → provinces.name` qua `mysql2` (`env('DB_DATABASE_SECOND')`), batch 2 connection — KHÔNG join xuyên DB.
- **`assign_requests.meeting_id` BẮT BUỘC nullable**, không NOT NULL, không default, không FK cứng.
- Branch `meeting-schedule` (api + client). KHÔNG đọc `vendor/`, `node_modules/`.
- Chỉ meeting có `customer_id`; status IN (1,2,3,4) (bỏ 0=Đang tạo).
- Không sửa hàm dùng chung ngoài phạm vi đã chốt (chỉ thêm field `meeting_id` vào luồng tạo phiếu công tác).
- Verify BE: `php -l <file>` sau mỗi file PHP sửa (php@7.4). Không PHP notice giữa output.

---

## PHASE 0 — Phụ thuộc: `assign_requests.meeting_id` (BE + FE)

> Làm trước vì cột 13 (Phiếu công tác/chấm công) phụ thuộc. Độc lập với phần report.

### Task 0.1: Migration thêm `assign_requests.meeting_id`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_08_16_000001_add_meeting_id_to_assign_requests_table.php`

- [ ] **Step 1:** Viết migration:
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddMeetingIdToAssignRequestsTable extends Migration
{
    public function up()
    {
        if (!Schema::hasColumn('assign_requests', 'meeting_id')) {
            Schema::table('assign_requests', function (Blueprint $table) {
                $table->unsignedBigInteger('meeting_id')->nullable()->after('id')->index();
            });
        }
    }
    public function down()
    {
        if (Schema::hasColumn('assign_requests', 'meeting_id')) {
            Schema::table('assign_requests', function (Blueprint $table) {
                $table->dropColumn('meeting_id');
            });
        }
    }
}
```
- [ ] **Step 2:** `php -l` file migration → no syntax error.
- [ ] **Step 3:** Chạy `php artisan migrate` (env local). Kỳ vọng: tạo cột `meeting_id` nullable, không lỗi.
- [ ] **Step 4 (xác minh):** `php artisan tinker` → `Schema::hasColumn('assign_requests','meeting_id')` trả `true`; tạo/kiểm 1 phiếu công tác cũ (không meeting) vẫn hoạt động (cột null).

### Task 0.2: BE lưu `meeting_id` khi tạo phiếu công tác

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/AssignRequest.php` (cho phép mass-assign `meeting_id` — kiểm `$fillable`/`$guarded`)
- Modify: nơi persist assign_request khi tạo phiếu công tác (`hrm-api/Modules/Assign/Services/AssignBusinessService.php` — tìm hàm store/create nhận request rồi `AssignRequest::create(...)`/`->fill(...)`).

**Interfaces:**
- Produces: `assign_requests.meeting_id` được set = `request('meeting_id')` khi có.

- [ ] **Step 1:** Đọc `AssignRequest.php`: nếu dùng `$guarded = []` → không cần sửa; nếu `$fillable` liệt kê cột → thêm `'meeting_id'`. Đọc `AssignBusinessService` tìm chỗ tạo assign_request.
- [ ] **Step 2:** Tại chỗ tạo assign_request, thêm gán `'meeting_id' => $request->meeting_id ?? null` (validate: nullable, integer, exists meetings.id nếu có — không bắt buộc).
- [ ] **Step 3:** `php -l` các file sửa.
- [ ] **Step 4 (xác minh):** Gọi API tạo phiếu công tác kèm `meeting_id` (curl/tinker) → bản ghi `assign_requests` mới có `meeting_id`. Tạo phiếu KHÔNG kèm `meeting_id` → `meeting_id` null, không lỗi.

### Task 0.3: FE gửi `meeting_id` khi submit phiếu công tác từ meeting

**Files:**
- Modify: `hrm-client/components/assign-components/assign-business/AssignBusinessForm.vue`

- [ ] **Step 1:** Trong `data().form`, thêm `meeting_id: null`.
- [ ] **Step 2:** Khi có `$route.query.meeting_id` (created hook ~L2575): set `this.form.meeting_id = Number(this.$route.query.meeting_id)`.
- [ ] **Step 3:** Trong `onMeetingChange(meetingId)` (business_type=2, chọn meeting thủ công): set `this.form.meeting_id = meetingId || null`. Khi clear meeting → `this.form.meeting_id = null`.
- [ ] **Step 4:** Đảm bảo payload submit gồm `meeting_id` (kiểm hàm build payload/`buildFormData`).
- [ ] **Step 5 (xác minh):** Build FE (node12+heap8192). Tạo phiếu công tác từ nút "Tạo phiếu công tác khác" trên meeting → DB `assign_requests.meeting_id` = id meeting. Tạo phiếu công tác thường (không từ meeting) → không lỗi, `meeting_id` null.

---

## PHASE 1 — BE: Permission + Route skeleton

### Task 1.1: Thêm 3 permission mới

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- [ ] **Step 1:** Tìm `max id` thực tế trong seeder (hiện ~1106). Sau block "Báo cáo meeting theo dự án" (id 1060-1062), thêm:
```php
// Báo cáo kết quả meeting theo thị trường
Permission::create(['id' => <max+1>, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả meeting theo thị trường theo tổng công ty', 'display_name' => 'Xem báo cáo kết quả meeting theo thị trường theo tổng công ty', 'group' => 'Báo cáo kết quả meeting theo thị trường', 'type' => 4]);
Permission::create(['id' => <max+2>, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả meeting theo thị trường theo công ty', 'display_name' => 'Xem báo cáo kết quả meeting theo thị trường theo công ty', 'group' => 'Báo cáo kết quả meeting theo thị trường', 'type' => 4]);
Permission::create(['id' => <max+3>, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả meeting theo thị trường theo phòng ban', 'display_name' => 'Xem báo cáo kết quả meeting theo thị trường theo phòng ban', 'group' => 'Báo cáo kết quả meeting theo thị trường', 'type' => 4]);
```
- [ ] **Step 2:** `php -l` seeder.
- [ ] **Step 3:** Seed 3 permission vào DB local: `php artisan tinker` → `Permission::create([...])` cho 3 bản ghi (hoặc chạy lại seeder nếu an toàn). Kỳ vọng: 3 quyền xuất hiện, group 'Báo cáo kết quả meeting theo thị trường'.
- [ ] **Step 4:** Gán 3 quyền cho role admin/test user để verify về sau.

### Task 1.2: Route group skeleton + Controller rỗng

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (thêm trong group `/assign/report`)
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingByMarketReportController.php`

**Interfaces:**
- Produces: `GET assign/report/meeting-by-market` → `index`; `.../export` → `export`; `.../{meeting}/attendance` → `attendance`.

- [ ] **Step 1:** Trong group `/assign/report` (cạnh meeting-by-projects/employees), thêm:
```php
// Báo cáo kết quả meeting theo thị trường
Route::get('/meeting-by-market', [MeetingByMarketReportController::class, 'index']);
Route::get('/meeting-by-market/export', [MeetingByMarketReportController::class, 'export']);
Route::get('/meeting-by-market/{meeting}/attendance', [MeetingByMarketReportController::class, 'attendance']);
```
+ `use` class. (KHÔNG gắn `checkPermission` chặn cứng — scoping trong service, giữ fallback "của chính mình".)
- [ ] **Step 2:** Tạo Controller với 3 method trả stub (`index` gọi service, tạm `responseSuccess([])`).
- [ ] **Step 3:** `php -l` cả 2 file.
- [ ] **Step 4 (xác minh):** `curl` `GET /api/v1/assign/report/meeting-by-market` (kèm token) → 200, body rỗng hợp lệ.

---

## PHASE 2 — BE: Service (query + tỉnh KH + scoping + filter + nhóm)

### Task 2.1: Service — query meetings + filter + scoping fail-closed

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php`

**Interfaces:**
- Produces: `getFilteredQuery(Request): Builder` (query `meetings` đã áp filter + `applyPermissionFilter`); `applyPermissionFilter($query): void`.

- [ ] **Step 1:** Viết `getFilteredQuery`: `Meeting::query()->whereNotNull('customer_id')->whereIn('status',[1,2,3,4])` + filter: `company_id`, `department_id`, `part_id`; `employee_id` (meeting mà `created_by=employee_id` OR EXISTS meeting_employees); `meeting_type_id`; `status`; period → `whereDate('start_date', ...)` theo `period`/`start_date`/`end_date`. (Lọc `province_id` xử lý ở tầng PHP sau khi resolve — Task 2.3.)
- [ ] **Step 2:** Viết `applyPermissionFilter` bám mẫu `MeetingByProjectsService` (§8.2 spec): tổng công ty→return; công ty→`company_id=current_company_role OR created_by=userId`; phòng ban→`department_id IN listManageDepartmentIds() OR part_id IN listManagePartIds() OR created_by=userId`; không quyền→`created_by=userId OR EXISTS meeting_employees(employee_id=userId)`. Dùng `isCurrentEmployeeHasPermission('Xem báo cáo kết quả meeting theo thị trường theo ...')`.
- [ ] **Step 3:** `php -l`.
- [ ] **Step 4 (xác minh):** tinker: gọi `getFilteredQuery(new Request([]))->count()` với user có quyền tổng công ty vs user không quyền → số lượng khác nhau đúng scope.

### Task 2.2: Service — resolve Tỉnh KH batch qua ERP (`mysql2`)

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php`

**Interfaces:**
- Produces: `resolveCustomerProvinces(array $customerIds): array` → map `customer_id => ['province_id'=>, 'province_name'=>, 'fullname'=>, 'code'=>]`.

- [ ] **Step 1:** Viết `resolveCustomerProvinces`: `$erpDb = env('DB_DATABASE_SECOND'); \App\Models\TpCustomer::query()->leftJoin($erpDb.'.provinces as p','p.id','=','customers.province_id')->whereIn('customers.id',$customerIds)->select('customers.id','customers.fullname','customers.code','customers.province_id','p.name as province_name')->get()->keyBy('id')` → array. (Bám `MeetingController::getListCustomer`.)
- [ ] **Step 2:** Null-safe: customer_id không thấy bên ERP / province null → province_id=null, province_name=null.
- [ ] **Step 3:** `php -l`.
- [ ] **Step 4 (xác minh):** tinker: `resolveCustomerProvinces([<vài customer_id thật>])` → trả tên tỉnh đúng; id không tồn tại → không lỗi.

### Task 2.3: Service — nhóm Thị trường → KH → Meeting + filter tỉnh + phân trang

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php`

**Interfaces:**
- Produces: `getData(Request): array` (cấu trúc nhóm §10.1 spec) + `getTotalMeetings(Request): int`.

- [ ] **Step 1:** `getData`: chạy query (Task 2.1) `->with(['company_members','customer_members','projects','meetingType','creator'])` (eager, tránh N+1), lấy meetings đã sort (province sau khi resolve → sort PHP). Batch `resolveCustomerProvinces(distinct customer_id)`. Gán province cho từng meeting.
- [ ] **Step 2:** Nếu `request->province_id` set → lọc meeting theo province_id (tầng PHP; giá trị đặc biệt cho "Chưa xác định" = null-marker, vd `province_id='__none__'`).
- [ ] **Step 3:** Nhóm: province (name A→Z, "Chưa xác định thị trường" cuối) → customer (name A→Z) → meetings (start_date ASC). Map mỗi meeting sang field response (§10.1): id, name, meeting_type_name, start_date, end_date, mode_id, location, online_link (escape), host_name (=creator fullname, null→"—"), company_members[], customer_members[], status, status_name, cancel_reason, has_report (MeetingReport exists), projects[{id,code,name}], business_trips[{id,code,has_timesheet}] (Task 3.1).
- [ ] **Step 4:** Phân trang server-side theo meeting (flatten sort) rồi dựng nhóm cho trang hiện tại; `getTotalMeetings` đếm tổng. (Nếu dataset nhỏ có thể trả full — theo per_page.)
- [ ] **Step 5:** `php -l`.
- [ ] **Step 6 (xác minh):** tinker/curl `index` → JSON nhóm đúng, tỉnh đúng, "Chưa xác định" cuối, đếm total khớp.

### Task 2.4: Controller `index` nối service + Resource (nếu cần)

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingByMarketReportController.php`

- [ ] **Step 1:** `index`: `try { $data=$service->getData($request); $total=$service->getTotalMeetings($request); return $this->apiGetList(...) or responseSuccess(['data'=>$data,'meta'=>['total_meetings'=>$total]]); } catch(\Exception $e){ Log::error($e); return $this->responseErrors(...); }`. Rethrow `ValidationException` nếu có validate.
- [ ] **Step 2:** `php -l`.
- [ ] **Step 3 (xác minh):** `curl index` với filter (period, status, company_id) → data đổi đúng.

---

## PHASE 3 — BE: Chấm công GPS + Export

### Task 3.1: Service — gắn business_trips (phiếu công tác) cho meeting

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php`

**Interfaces:**
- Produces: `attachBusinessTrips(Collection $meetings): void` (gán `business_trips[]` mỗi meeting) — batch `assign_requests WHERE meeting_id IN(...) AND type=PHIEU_CONG_TAC`; `has_timesheet` = tồn tại `timesheets(job_type='new_business_trip', job_id=assign_request.id)`.

- [ ] **Step 1:** Batch load assign_requests theo `meeting_id IN` (dùng hằng `AssignRequest::PHIEU_CONG_TAC`). Batch check timesheets có GPS theo `job_id IN(assign ids)`.
- [ ] **Step 2:** Gán `business_trips = [{id, code, has_timesheet}]` cho từng meeting (nhóm theo meeting_id). Không có → `[]`.
- [ ] **Step 3:** `php -l`.
- [ ] **Step 4 (xác minh):** Với meeting đã có phiếu công tác (Phase 0) → business_trips có mã + has_timesheet đúng; meeting không phiếu → `[]`.

### Task 3.2: Controller `attendance` — GPS timesheets popup

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingByMarketReportController.php`
- (nếu tách) Modify service: `getAttendanceByMeeting($meetingId): array`.

**Interfaces:**
- Produces: `GET .../{meeting}/attendance` → nhóm theo nhân sự: `[{employee_name, records:[{type,time,place,lat,lng}]}]`.

- [ ] **Step 1:** Lấy assign_request ids của meeting (meeting_id=param, type PCT). `Timesheet::where('job_type','new_business_trip')->whereIn('job_id',$ids)->orderBy('verify_date')` → nhóm theo `employee_info_id` → tên (EmployeeInfo). Map type check-in/out theo `verify_type`/`verify_state`, time=`verify_date`, place, lat, lng.
- [ ] **Step 2:** Áp scoping quyền (chỉ mở meeting user được xem — tái dùng getFilteredQuery + whereKey). Không quyền/không thuộc scope → 403/rỗng.
- [ ] **Step 3:** `php -l`.
- [ ] **Step 4 (xác minh):** `curl attendance` cho meeting có chấm công → nhóm nhân sự + mốc GPS đúng; meeting không chấm công → rỗng.

### Task 3.3: Export Excel

**Files:**
- Create: `hrm-api/Modules/Assign/ExcelExports/MeetingByMarketExport.php` (hoặc tái dùng lớp export báo cáo có sẵn — kiểm `ExcelExports/`/pattern `meetingByProjectsExport`)
- Modify: Controller `export`.

- [ ] **Step 1:** Kiểm cách `meetingByProjectsExport` xuất (maatwebsite class hay build tay). Bám theo. Mỗi meeting 1 dòng phẳng, lặp Thị trường/KH; cột popup rút gọn thành text (Biên bản→"Có/Không"; PCT→mã; Chấm công→số mốc/bỏ).
- [ ] **Step 2:** Controller `export`: dùng cùng `getFilteredQuery`+resolve (không phân trang) → trả `Excel::download(...)` hoặc blob.
- [ ] **Step 3:** `php -l`.
- [ ] **Step 4 (xác minh):** `curl export` → tải xlsx, mở kiểm cột + số dòng khớp index.

---

## PHASE 4 — FE: Trang report + filter + quyền (fail-closed)

### Task 4.1: Trang skeleton + permissions fail-closed + tải data

**Files:**
- Create: `hrm-client/pages/assign/report/meeting-by-market/index.vue`

**Interfaces:**
- Produces: page route `/assign/report/meeting-by-market`, layout `default-sidebar`, gọi `assign/report/meeting-by-market`.

- [ ] **Step 1:** Scaffold theo `meeting-by-projects/index.vue` (bỏ phần thừa). `created()`: set `this.permissions = { is_all_company: this.hasAPermission('Xem báo cáo kết quả meeting theo thị trường theo tổng công ty'), is_company: this.hasAPermission('...theo công ty'), is_department: this.hasAPermission('...theo phòng ban'), is_part: false }` — **KHÔNG `|| true`** (mỗi cờ mặc định false). (is_part không có quyền riêng → false.)
- [ ] **Step 2:** `data()` filters: period, start_date, end_date, company_id, department_id, part_id, employee_id, province_id, status, meeting_type_id. Method `handleSearch()` gọi store `apiGetMethod('assign/report/meeting-by-market'+query)`.
- [ ] **Step 3 (xác minh):** Build FE, mở `/assign/report/meeting-by-market` → trang load, gọi API, render tạm JSON count. Kiểm Vue: cờ quyền đúng theo user (không bật true khống).

### Task 4.2: Toolbar filter (Kỳ + cascade org + Thị trường/Trạng thái/Loại + Xoá + Excel)

**Files:**
- Modify: `hrm-client/pages/assign/report/meeting-by-market/index.vue`
- Dùng: `components/V2BaseCompanyDepartmentFilter.vue`

- [ ] **Step 1:** Template: `<V2BaseCompanyDepartmentFilter :permissions="permissions" v-model=...>` (bind company/department/part/employee). Kiểm props thực tế của component (v-model hay form object) để bind đúng.
- [ ] **Step 2:** Select Kỳ (7 option) — chọn "Tuỳ chọn" hiện Từ ngày/Đến ngày. Select Thị trường (options tỉnh — lấy distinct từ data trả về hoặc endpoint provinces), Trạng thái (Lên lịch/Chốt lịch/Hoàn thành/Hủy), Loại meeting (`apiGetMasterSelect('meeting_types')`). Nút Xoá lọc reset. Nút Xuất Excel.
- [ ] **Step 3:** Đổi filter → `handleSearch()`.
- [ ] **Step 4 (xác minh):** Đổi từng filter → data đổi đúng; ô lọc org ẩn/hiện theo cấp quyền (test user thấp quyền không thấy select Công ty).

---

## PHASE 5 — FE: Bảng 13 cột (rowspan nhóm)

### Task 5.1: Component bảng — dựng rowspan + 11 cột cơ bản

**Files:**
- Create: `hrm-client/pages/assign/report/meeting-by-market/components/MeetingByMarketTable.vue`

**Interfaces:**
- Consumes: prop `data` (nhóm province→customers→meetings) từ index.
- Produces: emit `open-detail(meeting)`, `open-minutes(meeting)`, `open-attendance(meeting)`, `open-project(project)`.

- [ ] **Step 1:** Render `<table>` header 13 cột (§4 spec). Body: lặp province → customer → meeting; tính `rowspan` ô Thị trường (tổng meeting trong province) + ô Khách hàng (tổng meeting trong customer). Style bám mockup `.market-table` (port CSS phần cần).
- [ ] **Step 2:** Cột 3–10: Tên meeting (link emit open-detail), Loại, Thời gian (format HH:mm DD/MM/YYYY, multi-day khoảng ngày), Địa điểm (mode 2→"Trực tuyến"+link escape), Người chủ trì (host_name), TP công ty (chip +N), TP KH (chip +N), Trạng thái (badge màu theo status).
- [ ] **Step 3:** Empty state "Không có meeting phù hợp với bộ lọc." khi data rỗng.
- [ ] **Step 4 (xác minh):** Build FE, render với data thật → rowspan gộp đúng, "Chưa xác định thị trường" cuối, badge màu đúng, chip +N khi >3.

### Task 5.2: Bảng — cột 11/12/13 (Biên bản/Lý do huỷ · Dự án TKT · Phiếu công tác)

**Files:**
- Modify: `hrm-client/pages/assign/report/meeting-by-market/components/MeetingByMarketTable.vue`

- [ ] **Step 1:** Cột 11: status=3 → nút "Xem biên bản" (emit open-minutes); status=4 → text `cancel_reason`; khác → "—".
- [ ] **Step 2:** Cột 12: `projects[]` → chip mã (emit open-project); rỗng → "—".
- [ ] **Step 3:** Cột 13: `business_trips[]` → chip mã phiếu; nếu `has_timesheet` → nút "Xem lịch sử chấm công" (emit open-attendance); rỗng → "—".
- [ ] **Step 4 (xác minh):** Render: meeting Hoàn thành có biên bản → nút hiện; Huỷ → lý do; có phiếu công tác + chấm công → chip + nút.

---

## PHASE 6 — FE: 2 popup + chi tiết meeting

### Task 6.1: Modal Biên bản cuộc họp

**Files:**
- Create: `hrm-client/pages/assign/report/meeting-by-market/components/MeetingMinutesModal.vue` (hoặc tái dùng component xem biên bản có sẵn nếu tồn tại — kiểm `components/assign/meeting/`)
- Modify: index.vue (lắng nghe `open-minutes`)

- [ ] **Step 1:** Kiểm có component biên bản dùng lại được không (màn meeting show/print). Nếu có → dùng lại. Nếu không → modal mới: bảng STT/Nội dung/Phương án/Người đề xuất/Người thực hiện/Hạn dự kiến + Kết luận (`conclusion`). Nguồn: `MeetingReport` của meeting (dùng field trả sẵn trong data hoặc gọi API show meeting/report).
- [ ] **Step 2:** Empty → "Chưa có nội dung biên bản".
- [ ] **Step 3 (xác minh):** Bấm "Xem biên bản" → modal đúng nội dung; meeting Hoàn thành chưa có report → empty state.

### Task 6.2: Modal Lịch sử chấm công GPS

**Files:**
- Create: `hrm-client/pages/assign/report/meeting-by-market/components/MeetingAttendanceModal.vue`
- Modify: index.vue (lắng nghe `open-attendance` → gọi `assign/report/meeting-by-market/{id}/attendance`)

- [ ] **Step 1:** Mở modal → gọi API attendance (Task 3.2), loading state. Render: mỗi nhân sự 1 khối, list mốc (Check-in/out, thời gian, địa chỉ `place`, toạ độ lat/lng — kèm link map optional).
- [ ] **Step 2:** Empty → "Chưa có lịch sử chấm công".
- [ ] **Step 3 (xác minh):** Bấm nút chấm công → modal hiện đúng mốc GPS theo nhân sự (data Phase 0).

### Task 6.3: Mở chi tiết meeting + mở dự án (tái dùng route)

**Files:**
- Modify: index.vue (lắng nghe `open-detail`, `open-project`)

- [ ] **Step 1:** `open-detail(meeting)` → `router.push`/mở màn chi tiết meeting có sẵn (kiểm route meeting show). `open-project(project)` → route dự án TKT có sẵn.
- [ ] **Step 2 (xác minh):** Click tên meeting → mở đúng meeting; click chip dự án → mở đúng dự án.

---

## PHASE 7 — FE: Menu + Print + Export

### Task 7.1: Thêm menu Báo cáo

**Files:**
- Modify: sidebar/menu config (kiểm nơi khai menu report — vd `components/.../sidebar` hoặc file menu Assign).

- [ ] **Step 1:** Thêm mục "Kết quả meeting theo thị trường" → `/assign/report/meeting-by-market`, hiển thị khi có ≥1 trong 3 quyền mới (fail-closed).
- [ ] **Step 2 (xác minh):** User có quyền thấy menu; user không quyền không thấy.

### Task 7.2: Nút Xuất Excel + trang Print

**Files:**
- Modify: index.vue (nút Excel → tải blob `.../export`)
- Create: `hrm-client/pages/assign/report/meeting-by-market/print.vue` (nếu cần bản in — bám `meeting-by-projects/print.vue`)

- [ ] **Step 1:** Nút Excel: `this.$axios.get('/api/v1/assign/report/meeting-by-market/export'+query, {responseType:'blob'})` → download.
- [ ] **Step 2:** Print (nếu làm): render bảng in bám filter hiện tại.
- [ ] **Step 3 (xác minh):** Bấm Xuất Excel → file tải đúng dữ liệu đang lọc.

---

## PHASE 8 — Verify tổng thể (Playwright + permission cases)

### Task 8.1: Verify E2E + phân quyền

- [ ] **Step 1:** Build client (node12+heap8192) + api (php7.4 artisan serve :8000). Đăng nhập user quyền tổng công ty → mở `/assign/report/meeting-by-market`.
- [ ] **Step 2 (Playwright):** Verify: nhóm Thị trường→KH→Meeting (rowspan), 13 cột, badge trạng thái, filter (kỳ/org/thị trường/trạng thái/loại) đổi data, Xuất Excel, popup Biên bản, popup Chấm công GPS, link meeting/dự án.
- [ ] **Step 3 (permission — BẮT BUỘC, chống fail-open):** Đăng nhập user **không quyền** → chỉ thấy meeting mình tạo/mình dự, KHÔNG lộ meeting công ty khác; ô lọc Công ty/PB ẩn; cờ quyền FE không bật true. User quyền phòng ban → đúng scope phòng/bộ phận. (xem `always-test-permission-cases`.)
- [ ] **Step 4 (xác minh cột PCT):** Tạo phiếu công tác từ 1 meeting (Phase 0) → cột Phiếu công tác hiện mã + popup chấm công GPS đúng.
- [ ] **Step 5:** Screenshot lưu folder feature; ghi checkpoint vào plan.md.

---

## Ghi chú thực thi

- **Không commit git** — chỉ verify. User yêu cầu mới commit.
- Thứ tự đề xuất: Phase 0 (phụ thuộc) → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Phase 0 có thể làm song song phần BE report nhưng cột 13 cần Phase 0 xong để verify.
- Mỗi task PHP: `php -l` trước khi coi là xong. Mỗi task FE: build được, không lỗi console.

## 🔖 TODO phiên sau — Fix lỗi tải file toàn app (DEFER theo yêu cầu user 2026-08-16)

**Lỗi hệ thống:** ~154 màn (Assign 62 · Training 36 · Decision 30 · Human 12 · Timesheet 11 · Payroll 3) dùng pattern `axios responseType arraybuffer/blob → new Blob → createObjectURL → <a download='tên'> click`. **Safari/webview bỏ qua `download` attr với blob URL → file tên UUID không đuôi, không mở được** (file-saver cũng fallback→UUID).

**Cách fix chuẩn (ĐÃ VERIFY trên 3 báo cáo meeting):** tải TRỰC TIẾP từ server bằng anchor tới `<baseURL>/api/v1/<path>/export?<params>&token=<jwt>` (jwt-auth chấp nhận query token; server maatwebsite `Excel::download` gắn sẵn `Content-Disposition: attachment; filename=...`) → trình duyệt tự đặt tên đúng MỌI browser.

**Plan phiên sau:**
1. Tạo helper dùng chung `hrm-client/utils/download-file.js`: `downloadFromServer({ axios, path, params })` — cũng là 1 "shared element" (khớp task refactor filter dùng chung).
2. Thay thế đồng loạt hàm export server-fetch-blob → gọi helper (làm theo module, Assign trước).
3. Ngoại lệ tách riêng: màn tự dựng file client-side (exceljs/SheetJS, không endpoint) → không dùng server-download được.
4. ⚠️ Token qua query vào server log — cân nhắc download-token 1 lần nếu cần bảo mật.
Khảo sát: `grep -rln "responseType.*arraybuffer\|responseType.*blob" pages/<module>/` + có createObjectURL + download.

---

## Trạng thái thực thi (Subagent-Driven, 2026-08-16)

**✅ CODE HOÀN TẤT Phase 0–7 + Final whole-branch review CLEAN.** Thực thi qua subagent (mỗi task: implementer + review + fix loop), KHÔNG commit git.

- [x] Phase 0 — meeting_id: migration + BE persist (AssignBusinessService::create) + FE send (AssignBusinessForm, guard NaN)
- [x] Phase 1 — 3 permission (id 1113/1114/1115) + route group + controller skeleton
- [x] Phase 2 — MeetingByMarketService: getFilteredQuery/applyPermissionFilter(fail-closed)/resolveCustomerProvinces(2-DB ERP)/getData(nhóm+phân trang)/getTotalMeetings + wire index
- [x] Phase 3 — attachBusinessTrips + getAttendanceByMeeting(GPS, nhãn Vào/Ra theo ngày) + Export Excel (getFlatRowsForExport + MeetingByMarketExport + view; batch attachHostAndReportInfo bỏ N+1)
- [x] Phase 4 — index.vue: layout + cờ quyền fail-closed (no ||true) + toolbar filter (period/custom + cascade org + thị trường/trạng thái/loại) + Xuất Excel
- [x] Phase 5 — MeetingByMarketTable.vue (13 cột rowspan, badge, chip +N, XSS-safe) + wire emit/route
- [x] Phase 6 — MeetingMinutesModal (reuse assign/meeting/{id}) + MeetingAttendanceModal (GPS) theo modal-popup SKILL
- [x] Phase 7 — menu-sidebar.js (ungated giống 2 báo cáo anh em) + wire Xuất Excel blob. Print.vue DEFER.
- [x] Final review (opus) CLEAN sau fix wave (FE pagination + orphaned province + meeting.code)
- [x] Phase 8 — Playwright verify PASS (data thật, fail-closed 0→18, bảng/rowspan/badge/biên bản/filter/pagination OK; popup chấm công & tier cty/phòng ban chưa test UI)
- [x] **Phase 9 — Khối SUMMARY (bổ sung theo yêu cầu user)**: dải tổng hợp như mockup tab 3 = Tổng meeting + Theo trạng thái + Theo thị trường + Tổng hợp (Dự án / KH mới / Tỷ lệ hoàn thành). Verify live: Hero 18 + Tổng hợp[9/17/22,2%] + Trạng thái[6/7/4/1 ∑18] + Thị trường[∑18].
  - [x] S1 (BE): `getSummary(Request)` → meta.summary {total, by_status[], by_province[], total_projects, new_customers, completion_rate}. + BONUS fix Critical: period=custom trước đó bị vô hiệu → nay lọc đúng. Memo getSortedFlatMeetings.
  - [x] S2 (FE): component summary bar (port style mockup buildSummaryBarInnerHtml §4039) render meta.summary; cập nhật khi filter đổi.
- [x] **Phase 12 — Bug Xuất Excel "không xem được" (FIXED)**: BE/file xlsx HỢP LỆ (verify openpyxl 19 dòng, cấu trúc zip chuẩn). **Root cause: file tải về tên UUID không đuôi `.xlsx` → Safari (macOS) BỎ QUA `download="tên"` trên blob URL** (Chrome tôn trọng nên Playwright/tôi không repro). Fix: đổi `exportExcel()` từ anchor+createObjectURL sang **`file-saver` saveAs(blob, filename)** (pattern chuẩn repo, vd pages/training/questions) + set MIME type blob. Verify Chrome: tải đúng tên .xlsx, 0 lỗi. **Đã confirm bundle đang chạy CÓ fix (usesFileSaver:true) → fix live.** Fix luôn 2 sibling: meeting-by-projects + meeting-by-employees (file-saver + đổi .xls→.xlsx). User hard-refresh VẪN UUID → trình duyệt user (Safari/webview) không đặt được tên khi tải blob (file-saver cũng fallback→UUID). **FIX CUỐI: chuyển cả 3 báo cáo (market + projects + employees) sang TẢI TRỰC TIẾP TỪ SERVER** — anchor tới `.../export?token=<jwt>` (jwt-auth chấp nhận query token), server trả kèm `Content-Disposition: attachment; filename=...xlsx` → trình duyệt tự đặt tên đúng trên MỌI trình duyệt (không phụ thuộc download attr/blob). Verify Playwright: nút tải đúng tên + openpyxl mở OK 19 dòng + Content-Disposition xác nhận. ⚠️ token đi qua query (vào server log) — chấp nhận cho tool nội bộ; có thể đổi sang download-token 1 lần nếu cần bảo mật hơn.
- [x] **Phase 11 — Fix (user yêu cầu)**: (1) click tên meeting → mở `/assign/meeting/{id}/show` ở TAB MỚI (onOpenDetail dùng window.open + $router.resolve) — verify live tab mới bật. (2) Meeting có customer_id nhưng snapshot customer_name/code NULL (vd meeting 35 → KH 20617 Phương Anh) hiển thị "—": fix fallback trong `attachProvinceInfo` lấy fullname/code resolve từ ERP khi snapshot rỗng → verify live 0 ô "—", hiện tên KH thật. (Không loại khỏi báo cáo vì meeting THẬT có KH.)
- [x] **Phase 10 — UI polish (user yêu cầu)**: (1) gộp "Kỳ báo cáo" vào hàng Thị trường/Trạng thái/Loại meeting (org cascade thành hàng riêng) — verify live: 4 field cùng row, Kỳ không đứng riêng; (2) border-top `2px solid #06b6d4` cho dòng đầu mỗi nhóm khách hàng (`market-table__row--customer-start`) — verify live 17 nhóm có border cyan. Thuần layout/CSS, không đụng logic.

### Checkpoint — 2026-08-16 (code done)
Vừa hoàn thành: Toàn bộ code BE+FE (Phase 0–7) qua Subagent-Driven + Final review clean. Chưa commit git.
Đang làm dở: (không) — chờ user build + verify.
Bước tiếp theo: USER build client (node12+heap8192) + api (php7.4 artisan serve) → mở `/assign/report/meeting-by-market` → Playwright verify: nhóm rowspan/13 cột/filter/phân trang/Xuất Excel/popup biên bản/popup chấm công GPS + **test phân quyền 4 tier** (có/không quyền → scope đúng, không leak). Commit khi user yêu cầu.
Blocked:

### Checkpoint — 2026-08-16 (wrap up cuối phiên)
Vừa hoàn thành: Feature meeting-by-market HOÀN CHỈNH (Phase 0–12) + verify Playwright data thật (fail-closed 0→18, 13 cột rowspan, 2 popup, phân trang, summary, filter). Các fix/polish theo user: Phase 10 (gộp filter Kỳ + border KH), Phase 11 (click meeting mở tab mới + fallback tên KH khi snapshot null), Phase 12 (fix Xuất Excel Safari → tải trực tiếp server ?token + Content-Disposition, áp cho 3 báo cáo meeting). Verify export: openpyxl mở OK, tên file đúng. Chưa commit git.
Đang làm dở: (không).
Bước tiếp theo (phiên sau, theo ý user):
  1. Fix lỗi tải file toàn app (~151 màn còn lại) — helper `downloadFromServer` + migrate (xem mục "TODO phiên sau" đầu file).
  2. Refactor filter báo cáo thành element dùng chung phân hệ (brainstorm dở).
  3. Treo nhỏ: revoke/giữ test `role_has_permissions(18,1113,1)`; verify UI popup chấm công + tier quyền cty/phòng ban; nút "Xem biên bản" đang gate quyền DS meeting (khác quyền báo cáo).
Blocked:
