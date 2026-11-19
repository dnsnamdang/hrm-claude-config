# Lịch công tác lãnh đạo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> ⛔ **CHƯA CÓ LỆNH CODE.** Trước Task 1 phải hỏi user riêng và nhận câu "làm" kèm phạm vi: repo · nhánh · file/bảng ·
> migration nào chạy vào DB nào (CLAUDE.md gốc). Hỏi luôn **nhánh hrm-api cho API app** (xem Global Constraints).
> Không commit / push khi user chưa bảo (memory "không hỏi commit — user tự báo"). Các bước "Commit" dưới đây chỉ làm khi user cho phép.

**Goal:** Lãnh đạo tick "Báo lịch công tác lãnh đạo" trên nhắc việc cá nhân (web + app) → cả công ty nhận thông báo;
mọi nhân viên xem bảng vắng mặt của ban lãnh đạo trên app (3 chế độ, mặc định Bảng tuần).

**Architecture:** Lịch = chính dòng `personal_todos` (cha, `parent_id` null) có cờ `is_leader_schedule`. Khoảng vắng
**tính lúc đọc** (`LeaderScheduleService::rangeOf`) từ ngày/giờ bắt đầu, ngày/giờ hạn và `completed_at` — nên "hoàn
thành sớm cắt lịch" và "bỏ tick trả lại hạn gốc" không cần lưu ngày hạn gốc. Mọi đường ghi của MyTodoService chụp
`rangeOf` trước và sau, đưa cặp (trước, sau) cho `announce()` quyết định Mới / Đổi / Huỷ / im lặng; gửi bằng queue job.

**Tech Stack:** hrm-api Laravel 8 (PHP 7.4) · hrm-client Nuxt 2 / Vue 2 · TPE_APP Flutter (GetX, auto_route).

**Spec:** `HRM/.plans/gop-db/lich-cong-tac-lanh-dao/design.md` (user duyệt 05/11/2026) · mockup Pencil
`meeting-mobile.pen` Nhóm ⑮ (LCT-00…LCT-08).

## Global Constraints

- Nhánh: hrm-api + hrm-client `gop_db` (danh mục quyền theo mã chỉ có ở `gop_db`). TPE_APP `develop`. **Hỏi lại**:
  app đang chạy với API `develop` (memory "hrm-api develop đi trước gop_db") — API mới làm ở `gop_db`, có cần
  cherry-pick sang `develop` không.
- Quyền khai bằng **danh mục mã** `app/Support/Permissions/Catalog/assign.php` (seeder tên cũ không còn trên `gop_db`),
  đồng bộ bằng `php artisan permission:catalog-sync --dry-run` rồi bản thật (chỉ khi user cho chạy vào DB):
  - Q1 `assign.lich_cong_tac_lanh_dao.announce` — "Báo lịch công tác lãnh đạo"
  - Q2 `assign.lich_cong_tac_lanh_dao.configure` — "Cấu hình lịch công tác lãnh đạo"
  - Kiểm bằng `isCurrentEmployeeHasPermission('<mã>')` (công ty đang chọn); người giữ quyền theo công ty:
    `PermissionLookup::holders('<mã>', $companyId)`. **Không** bypass super admin.
- Câu chữ (nguyên văn, ngày `d/m/Y`):
  - Mới — tiêu đề: `Ông/bà: {Họ tên} - {Chức danh} có lịch công tác từ ngày {start} đến ngày {end}`
  - Đổi — tiêu đề: `Ông/bà: {Họ tên} - {Chức danh} thay đổi lịch công tác: từ ngày {start} đến ngày {end}`
  - Huỷ — tiêu đề: `Ông/bà: {Họ tên} - {Chức danh} huỷ lịch công tác từ ngày {start} đến ngày {end}` (khoảng CŨ)
  - Nội dung Mới/Đổi: `{Tiêu đề nhắc việc}` + xuống dòng + `Đề nghị các phòng ban, bộ phận sắp xếp công việc phù hợp với lịch làm việc của lãnh đạo!`
  - Nội dung Huỷ: `{Tiêu đề nhắc việc}`
  - Confirm khi lưu (web + app): `Nhắc việc này sẽ được thông báo cho toàn Công ty, bạn chắc chắn lưu?`
- Người nhận: NV `employees.status=1` + `employee_infos.status=1` có `company_employees` ở công ty của lịch (kể cả kiêm
  nhiệm), **trừ người tạo**. Không gửi sang công ty khác.
- Công ty của lịch = `auth()->user()->current_company_role` lúc tạo, ghi vào `personal_todos.company_id`, không đổi về sau.
- Nhân viên xem chỉ nhận: họ tên, chức danh, khoảng ngày giờ, tiêu đề. **Không** trả mô tả, bước con, danh sách.
- FE: validate báo đồng thời mọi ô; không dùng prop `trim` trên ô nhập; nút mobile có icon, Huỷ bên phải (memory).

## Review Focus

1. **Sửa nhắc việc nhưng không đổi ngày giờ** (chỉ sửa mô tả / tiêu đề / bước) → không được bắn thông báo "đổi lịch" cho cả công ty. Test ở Task 3 `test_sua_mo_ta_khong_bao`.
2. **Người không có Q1 gửi `is_leader_schedule=1` bằng API** (bỏ qua FE) → 403, không lưu, không gửi. Test Task 3 `test_khong_quyen_gui_co_bi_tu_choi`.
3. **Lịch nhiều tuần / qua tuần** (bắt đầu T6 tuần này, hạn T3 tuần sau) → API đọc theo tuần phải trả lịch ở cả 2 tuần. Test Task 4 `test_lich_vat_tuan_co_o_ca_hai_tuan`.
4. **Tick Hoàn thành xong bỏ tick ngay** → 2 thông báo (Đổi rồi Đổi lại) hoặc Huỷ rồi Mới, không mất lịch. Test Task 3 `test_bo_tick_hoan_thanh_tra_lai_han_goc`.
5. **NV kiêm nhiệm ở 2 công ty** chỉ thấy lịch của công ty đang chọn trên app; lãnh đạo kiêm nhiệm hiện chức danh của công ty lịch. Test Task 4 `test_chi_tra_lich_cong_ty_dang_chon`.

---

### Task 1: Quyền + lược đồ lưu

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Catalog/assign.php` (thêm 2 mục cạnh nhóm "Việc của tôi"/cuối file)
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_06_000001_add_leader_schedule_to_personal_todos.php`
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_11_06_000002_create_leader_schedule_orders_table.php`
- Create: `hrm-api/Modules/Assign/Entities/MyTodo/LeaderScheduleOrder.php`
- Modify: `hrm-api/Modules/Assign/Entities/MyTodo/PersonalTodo.php` (fillable + casts)
- Test: `hrm-api/Modules/Assign/Tests/Feature/LeaderSchedule/LeaderScheduleSchemaTest.php`

**Interfaces:**
- Produces: cột `personal_todos.is_leader_schedule` tinyint default 0 · `start_date` date null · `start_time` time null
  (index `(company_id, is_leader_schedule, start_date)`); bảng `leader_schedule_orders(id, company_id, employee_id,
  sort_order int, timestamps, created_by, updated_by)` unique `(company_id, employee_id)`; model `LeaderScheduleOrder`.

Mục danh mục (2 mục, `kind` = `action`, `scopes` = [], `legacy` = [], `platforms` = ['hrm'], `subsystem_group`
'Văn phòng số', `subsystem` 'Công việc', `feature` 'Lịch công tác lãnh đạo').

- [ ] **Step 1:** Test `test_cot_va_bang_ton_tai` — `Schema::hasColumns('personal_todos', ['is_leader_schedule','start_date','start_time'])` true; `Schema::hasTable('leader_schedule_orders')` true; `PermissionCatalog` chứa 2 mã trên.
- [ ] **Step 2:** Chạy `php artisan test Modules/Assign/Tests/Feature/LeaderSchedule/LeaderScheduleSchemaTest.php` → FAIL.
- [ ] **Step 3:** Viết 2 migration + model + 2 mục danh mục. `PersonalTodo` thêm 3 cột vào fillable, cast `is_leader_schedule` → boolean.
- [ ] **Step 4:** `php artisan migrate:status` + `migrate --pretend --path=...` cho đúng 2 file → đưa user duyệt → chạy lẻ `--path`. `permission:catalog-sync --dry-run` phải in "thêm 2", không đụng mã khác → đưa user → chạy thật. Test PASS.
- [ ] **Step 5:** Commit (khi được phép).

### Task 2: LeaderScheduleService — khoảng vắng, chức danh, người nhận, câu chữ

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/LeaderScheduleService.php`
- Create: `hrm-api/Modules/Assign/Jobs/AnnounceLeaderScheduleJob.php`
- Test: `hrm-api/Modules/Assign/Tests/Unit/LeaderScheduleRangeTest.php`, `.../Feature/LeaderSchedule/LeaderScheduleAnnounceTest.php`

**Interfaces:**
- Produces:
  - `rangeOf(PersonalTodo $t): ?array` → `['start_date'=>'Y-m-d','start_time'=>?'H:i','end_date'=>'Y-m-d','end_time'=>?'H:i']` hoặc null.
  - `titleOf(int $employeeId, int $companyId): string`
  - `recipientInfoIds(int $companyId, int $exceptEmployeeId): int[]` (employee_info ids)
  - `messageFor(string $kind /* new|change|cancel */, PersonalTodo $t, array $range, string $name, string $title): array` → `['title'=>..., 'body'=>...]`
  - `announce(?array $before, ?array $after, PersonalTodo $t, int $actorEmployeeId): ?string` → kind đã gửi hoặc null.
  - Job `AnnounceLeaderScheduleJob(int $companyId, int $exceptEmployeeId, array $payload, int $actorEmployeeInfoId)`.

Luật `rangeOf` (design 3.3 + 3.6):
- null nếu không phải lịch (`is_leader_schedule` false / có `parent_id` / thiếu `start_date` hoặc `due_date`).
- Chưa hoàn thành → khoảng nguyên `start_*` → `due_*`.
- Hoàn thành ngày D = `completed_at` (date): D < start_date → null (huỷ); start_date ≤ D < due_date → end_date = D,
  end_time = giờ của `completed_at`; D ≥ due_date → khoảng nguyên (không báo).

Luật `announce`: before null & after có → `new`; before có & after null → `cancel` (câu dùng khoảng CŨ); cả hai có &
khác nhau → `change`; còn lại null. Người tạo không có Q1 tại `company_id` của lịch → return null, không gửi (design 3.6 #6).

`titleOf`: hồ sơ chính (`employee_infos.employee_role_id` → `titles.name`) khi `employee_infos.company_id` = công ty
lịch; ngược lại lấy dòng `employee_concurrently_department_has_positions` của NV có `department_id` thuộc công ty
lịch (`title` → `titles.name` theo `title_id`), không có thì rơi về hồ sơ chính. Rỗng → bỏ cả cụm ` - {Chức danh}`.

`recipientInfoIds`: cùng điều kiện `BulkPermissionService::employeesOfCompany` (copy truy vấn, hàm kia protected), trừ
`$exceptEmployeeId`, `pluck('employees.employee_info_id')->unique()`.

Gửi: job gọi `EmployeeInfoService::sendNotification($infoId, $data, false, $actor)` từng người, `$data`:
`type` = `leaderSchedule`, `id` = todo id, `url` = `''` (web không có màn xem), `title` = câu tiêu đề, `push_title` =
câu tiêu đề, `push_body` = nội dung, `note_full` = nội dung, thêm `schedule_date` = start_date (app mở đúng tuần).
Job chạy hàng đợi mặc định; `$actor` truyền qua id rồi `Employee::find` trong `handle`.

- [ ] **Step 1:** Unit test `rangeOf`: `test_chua_xong_tra_khoang_nguyen`, `test_xong_som_cat_den_ngay_tick` (start 10/11, hạn 14/11, xong 12/11 15:30 → end 2026-11-12 15:30), `test_xong_truoc_bat_dau_la_huy` (→ null), `test_xong_sau_han_giu_nguyen`, `test_buoc_con_khong_phai_lich`.
- [ ] **Step 2:** Test `messageFor`: so khớp nguyên văn 3 câu ở Global Constraints với Họ tên "Nguyễn Trung Phong", chức danh "Chủ tịch HĐQT", 10/11/2026 → 14/11/2026.
- [ ] **Step 3:** Feature test `announce` với `Queue::fake()`: `test_moi_day_job`, `test_khong_doi_khong_day`, `test_mat_quyen_khong_day`; `test_nguoi_nhan_bo_nguoi_tao_va_nv_nghi` (dựng 1 NV nghỉ việc + người tạo trên DB local, cả hai không có trong `recipientInfoIds`).
- [ ] **Step 4:** Chạy → FAIL; viết service + job; chạy → PASS.
- [ ] **Step 5:** Commit.

### Task 3: Nối vào form lưu / sửa / tick / xoá

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoRequest.php`, `UpdatePersonalTodoRequest.php`
- Modify: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoService.php` (`storeTodo` 149, `updateTodo` 196, `syncSubItems` 266, `toggleTodo` 354, `destroyTodo` 407)
- Modify: `hrm-api/Modules/Assign/Transformers/MyTodoResource/PersonalTodoResource.php`
- Test: `hrm-api/Modules/Assign/Tests/Feature/LeaderSchedule/MyTodoLeaderScheduleTest.php`

**Interfaces:**
- Consumes: `LeaderScheduleService::rangeOf`, `announce` (Task 2).
- Produces: request nhận `is_leader_schedule` (boolean), `start_date` (date), `start_time` (H:i); resource trả thêm 3 trường.

Luật validate (thêm vào cả Store và Update):
`start_date` → `required_if:is_leader_schedule,1|nullable|date`; `due_date` → thêm `required_if:is_leader_schedule,1` và
`after_or_equal:start_date` khi có cờ; `start_time` → `nullable|date_format:H:i`. Câu lỗi: "Ngày bắt đầu là bắt buộc",
"Ngày hạn là bắt buộc", "Ngày hạn phải từ Ngày bắt đầu trở đi". Cùng ngày mà có cả 2 giờ: giờ hạn ≥ giờ bắt đầu.

Luật service:
- Payload có `is_leader_schedule=1` mà người gọi không có Q1 → `abort(403, 'Bạn không có quyền báo lịch công tác lãnh đạo')`.
- Không có Q1 và payload không gửi cờ → **giữ nguyên** 3 cột cũ (không huỷ ngầm).
- Chỉ việc cha được làm lịch (`parent_id` có → bỏ qua cờ).
- Mỗi đường ghi: `$before = rangeOf($todo->fresh())` trước transaction, `$after = rangeOf($todo->fresh())` sau, rồi
  `announce($before, $after, $todo, auth()->id())` **sau commit** (`DB::afterCommit` hoặc gọi ngoài closure).
  `toggleTodo` trên bước con: chụp trên việc cha. `destroyTodo`: `$after = null`.

- [ ] **Step 1:** Feature test (gọi HTTP `/api/v1/assign/my-todo/todos` bằng tài khoản namdangit, cấp/gỡ Q1 bằng role tạm + xoá cache quyền, `Queue::fake()`):
  `test_tao_co_co_bao_moi`, `test_thieu_ngay_bat_dau_va_ngay_han_bao_ca_hai_loi` (422 có cả 2 khoá),
  `test_khong_quyen_gui_co_bi_tu_choi` (403, không có dòng mới), `test_doi_ngay_bao_doi`, `test_sua_mo_ta_khong_bao`,
  `test_bo_tick_o_bao_huy`, `test_xoa_bao_huy`, `test_tick_xong_som_bao_doi`, `test_tick_het_buoc_con_bao_doi`,
  `test_bo_tick_hoan_thanh_tra_lai_han_goc` (2 job, job 2 khoảng = khoảng gốc), `test_mat_quyen_sua_giu_nguyen_khong_bao`,
  `test_company_id_la_cong_ty_dang_chon`.
- [ ] **Step 2:** Chạy → FAIL. Sửa request + service + resource. Chạy → PASS.
- [ ] **Step 3:** Chạy lại toàn bộ test có chữ `MyTodo`/`my-todo` trong `Modules/*/Tests` (memory "đổi luật validate → chạy test BE"). Gỡ role tạm + xoá cache.
- [ ] **Step 4:** Commit.

### Task 4: API đọc cho app

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/LeaderScheduleController.php`
- Create: `hrm-api/Modules/Assign/Transformers/LeaderScheduleResource.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (trong group `/v1` auth:api, cạnh khối My Todo ~1531)
- Modify: `LeaderScheduleService` thêm `leaders(int $companyId): Collection`, `schedulesBetween(int $companyId, string $from, string $to): Collection`
- Test: `hrm-api/Modules/Assign/Tests/Feature/LeaderSchedule/LeaderScheduleReadApiTest.php`

**Interfaces:**
- `GET v1/assign/leader-schedules/meta` → `{can_announce: bool, can_configure: bool}` (app dùng cờ này thay vì đọc tên quyền).
- `GET v1/assign/leader-schedules?from=Y-m-d&to=Y-m-d` (khoảng ≤ 62 ngày, công ty = công ty đang chọn) →
  `{leaders: [{employee_id, name, title, avatar}], schedules: [{id, employee_id, title, start_date, start_time, end_date, end_time}]}`.
  `leaders` = người giữ Q1 tại công ty, theo `leader_schedule_orders.sort_order`, người chưa có thứ tự xếp cuối theo tên.
  `schedules` = lịch của các leader đó có `rangeOf` khác null và giao `[from, to]`, khoảng lấy từ `rangeOf`.
- Không gate quyền (mọi NV công ty xem).

- [ ] **Step 1:** Test: `test_tra_ca_lanh_dao_khong_co_lich`, `test_khong_lo_mo_ta_va_buoc_con` (khoá JSON chỉ đúng 7 trường ở trên), `test_lich_vat_tuan_co_o_ca_hai_tuan`, `test_lich_huy_va_xong_truoc_bat_dau_khong_hien`, `test_xong_som_hien_khoang_cat`, `test_mat_quyen_bien_khoi_bang`, `test_chi_tra_lich_cong_ty_dang_chon`, `test_thu_tu_theo_cau_hinh_nguoi_moi_cuoi`, `test_khoang_qua_62_ngay_422`.
- [ ] **Step 2:** FAIL → viết controller/resource/route → PASS.
- [ ] **Step 3:** Commit.

### Task 5: API cấu hình thứ tự (Q2)

**Files:**
- Modify: `LeaderScheduleController` (+ `orders`, `saveOrders`), `Modules/Assign/Routes/api.php`
- Test: `hrm-api/Modules/Assign/Tests/Feature/LeaderSchedule/LeaderScheduleOrderApiTest.php`

**Interfaces:**
- `GET v1/assign/leader-schedules/orders` → `{leaders: [...như Task 4]}` của công ty đang chọn.
- `PUT v1/assign/leader-schedules/orders` body `{employee_ids: int[]}` → ghi `sort_order` = vị trí (1..n), xoá dòng của người không còn Q1.
  Cả 2 route `->middleware('checkPermission:assign.lich_cong_tac_lanh_dao.configure')` (Q2 tại công ty đang chọn — design 3.6 #8).
  `employee_ids` có id không giữ Q1 tại công ty → 422 "Danh sách lãnh đạo không hợp lệ".

- [ ] **Step 1:** Test `test_khong_q2_403`, `test_luu_thu_tu_doc_lai_dung`, `test_id_la_422`, `test_khong_dung_cong_ty_khac`.
- [ ] **Step 2:** FAIL → code → PASS. Commit.

### Task 6: Web — ô tick trên form nhắc việc

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/TodoFormModal.vue`
- Test: e2e `HRM/e2e/tests/assign/my-todo-leader-schedule.spec.ts` (+ kiểm bằng Playwright MCP)

**Interfaces:**
- Consumes: request/resource Task 3; quyền đọc từ store `permissionCodes` (`assign.lich_cong_tac_lanh_dao.announce`).

Ô tick (`b-form-checkbox`, chỉ render khi có Q1) đặt dưới hàng Ngày hạn/Giờ hạn; tick → hiện hàng **Ngày bắt đầu · Giờ
bắt đầu** đủ 12 cột ngay trên hàng Ngày hạn · Giờ hạn (memory "bố cục form không để ô lẻ"); dấu * ở Ngày bắt đầu và
Ngày hạn. Bấm Lưu khi có tick → `this.$confirm` với câu confirm ở Global Constraints → Đồng ý mới gửi. Lỗi 422 hiện đồng
thời ở các ô. Sửa nhắc việc đã là lịch → ô tick bật sẵn.

- [ ] **Step 1:** Spec: `có quyền thấy ô tick` / `không quyền không có ô tick trong DOM` / `tick + để trống 2 ngày → 2 ô đỏ cùng lúc` / `Lưu hiện confirm đúng câu, Huỷ thì không có request` / `Đồng ý → request mang is_leader_schedule=1, start_date`.
- [ ] **Step 2:** Code → kiểm Playwright MCP đo DOM (số ô, vị trí hàng mới, chữ confirm) bằng tài khoản namdangit; tái hiện cả ca không quyền.
- [ ] **Step 3:** Commit.

### Task 7: Web — màn "Cấu hình lịch công tác lãnh đạo"

**Files:**
- Create: `hrm-client/pages/assign/leader-schedule-config/index.vue` (layout `default-sidebar`)
- Modify: `hrm-client/components/menu-sidebar.js` — nhóm "Thiết lập" (~dòng 258) thêm `{ label: 'Cấu hình lịch công tác lãnh đạo', link: '/assign/leader-schedule-config', codes: ['assign.lich_cong_tac_lanh_dao.configure'] }`
- Test: e2e `HRM/e2e/tests/assign/leader-schedule-config.spec.ts`

Danh sách lãnh đạo của công ty đang chọn (avatar · tên · chức danh), kéo thả đổi thứ tự (dùng thư viện kéo thả đã có
trong hrm-client — grep `vuedraggable` trước, không thêm package mới), nút Lưu → PUT Task 5, toast thành công. Rỗng →
"Chưa có ai được gán quyền Báo lịch công tác lãnh đạo". Có cảnh báo chưa lưu (skill `unsaved-changes`).

- [ ] **Step 1:** Spec: `không Q2 không thấy menu và vào URL bị chặn` / `kéo người 3 lên đầu, Lưu, tải lại vẫn đúng thứ tự`.
- [ ] **Step 2:** Code → Playwright MCP đo → Commit.

### Task 8: App — ô tick trên form nhắc việc

**Files:**
- Modify: `TPE_APP/app/lib/ui/my_todo/personal_todo_form_page.dart`
- Modify: `TPE_APP/app/lib/data/lib/src/repository/source/remote/api/api_services/app_server/my_todo_api_service.dart` (gửi 3 trường + gọi `meta`)
- Modify: model nhắc việc cá nhân bên `lib/domain` / `lib/data` (thêm `isLeaderSchedule`, `startDate`, `startTime`)

Theo LCT-05/06/07: công tắc "Báo lịch công tác lãnh đạo" chỉ hiện khi `meta.can_announce`; bật → hiện Ngày bắt đầu ·
Giờ bắt đầu, khối xem trước câu thông báo; Lưu thiếu ngày → báo đỏ cả 2 ô cùng lúc (LCT-06); Lưu đủ → hộp xác nhận
(LCT-07), nút [Lưu và thông báo] trái · [Huỷ] phải, có icon.

- [ ] **Step 1:** Widget test: công tắc ẩn khi `can_announce=false`; bật mà để trống → 2 lỗi; xem trước khớp câu tiêu đề.
- [ ] **Step 2:** Code → chạy máy ảo (skill khảo sát Mobile MCP, flavor tpeLocal) chụp so với LCT-05/06/07 → Commit.

### Task 9: App — màn "Lịch công tác lãnh đạo" (3 chế độ) + menu + mở từ thông báo

**Files:**
- Create: `TPE_APP/app/lib/ui/leader_schedule/leader_schedule_page.dart` (khung + nút gạt 3 chế độ + đổi tuần)
- Create: `.../leader_schedule/week_grid_view.dart` (A), `day_view.dart` (B), `timeline_view.dart` (C), `schedule_detail_sheet.dart`, `leader_schedule_controller.dart`
- Create: `TPE_APP/app/lib/data/.../app_server/leader_schedule_api_service.dart`
- Modify: `TPE_APP/app/lib/ui/module_shell/module_menus.dart:273` — thêm `DrawerEntry('Lịch công tác lãnh đạo', icon: Icons.event_busy_outlined, onTap: → LeaderScheduleRoute())` ngay sau "Vấn đề"
- Modify: `TPE_APP/app/lib/ui/notification/notification_router.dart` — `case 'leaderSchedule':` mở `LeaderScheduleRoute(initialDate: schedule_date)`
- Modify: file router auto_route (đăng ký route mới)

Theo LCT-01…04: mặc định A; A = hàng lãnh đạo × T2–CN, ô cam vắng cả ngày, ô sọc vắng một phần (có giờ ở ngày đầu hoặc
ngày cuối), vuốt / ‹ › đổi tuần, khối "Hôm nay vắng" dưới bảng; chạm ô → sheet LCT-02 (tên, chức danh, khoảng, tiêu đề,
"Lịch sắp tới" 30 ngày của người đó); B = dải 7 ngày, "N vắng · M có mặt", người vắng lên đầu + "Vắng đến …", người có
mặt ghi "sắp vắng dd/mm"; C = Đang vắng → Sắp tới → Đã qua 30 ngày, ô tìm theo tên. Mỗi lần đổi tuần gọi API Task 4 một
lần (C gọi khoảng hôm nay −30 → +30).

- [ ] **Step 1:** Unit test controller: `cellState(leader, day)` trả `none|full|partial` đúng cho lịch có giờ ở ngày đầu/cuối và lịch vắt tuần; nhóm C chia đúng 3 nhóm theo hôm nay.
- [ ] **Step 2:** Code → máy ảo: so 3 chế độ với LCT-01/03/04, bấm thông báo mở đúng tuần → Commit.

---

## Self-review (đã chạy)
- Phủ spec: 3.1→T1/T3/T5 · 3.2→T3/T6/T8 · 3.3→T2/T3 · 3.4→T4/T9 · 3.5→T5/T7 · 3.6 #1–#10→T2/T3/T4/T9 · 3.7 câu đổi/huỷ→Global Constraints.
- Tên dùng thống nhất: `rangeOf`, `announce`, `messageFor`, `recipientInfoIds`, `titleOf`, mã quyền Q1/Q2, type `leaderSchedule`.
- Claude tự chốt trong plan (user soát): khoảng vắng tính lúc đọc (không lưu ngày hạn gốc); ngày trong câu dạng d/m/Y, không kèm giờ; nội dung = tiêu đề + xuống dòng + câu đề nghị; `url` thông báo để trống vì web không có màn xem; app đọc quyền qua `meta` thay vì tên quyền; giới hạn khoảng đọc 62 ngày.
