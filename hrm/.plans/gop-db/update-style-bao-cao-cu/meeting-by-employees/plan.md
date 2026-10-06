# Update style — Báo cáo meeting nhân viên theo thời gian · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **REQUIRED skill khi code FE:** `report-styles` (HRM/.claude/skills/report-styles). Excel: `export-excel`. In: `print-page` mục 4d.
> **ĐƯỢC PHÉP CODE** — user trả lời "làm" 05/10/2026 (phạm vi: worktree wt-update-style-mbe, nhánh gop_db-update-style-meeting-by-employees, commit nhánh đó, PHPUnit DB local hrm_erp; không push/merge).

**Goal:** Viết lại `/assign/report/meeting-by-employees` theo khuôn report-styles (cây Công ty ▸ Phòng ban ▸ Nhân viên ▸ Meeting,
phân trang theo NHÂN VIÊN, thời lượng phút-người) và sửa lỗi bản cũ: lọc KH/Dự án chết, popup trạng thái gọi route không tồn tại,
phân trang cắt ngang NV, người tham gia KH đếm lượt.

**Architecture:**
- **BE:** controller + service mới, chỉ đọc. Mọi con số tính từ MỘT tập dòng lá L = (NV công ty × meeting) lấy bằng 1 query phẳng
  `meeting_employees ⨝ meetings ⨝ employees ⨝ employee_infos` (đã áp kỳ + #11145 + bộ lọc + quyền), gom cây/totals/phân trang trong
  PHP. Chi tiết hiển thị (dự án, KH, nội dung…) chỉ nạp cho meeting trên trang. Đếm người dùng lại `MeetingParticipantCounter`.
- **FE:** copy màn báo cáo 1 `pages/assign/report/meeting-by-projects/` (đã theo `template/` + ô Kỳ), đổi tiền tố `mbp-` → `mbe-`,
  cây 2 cấp → 4 cấp (CSS d2/d3 lấy từ `template/components/TrackingTable.vue`), thêm popup Nhân viên + khối chọn cột in.
- **Dọn dẹp:** gỡ endpoint / component cũ sau khi grep cả 2 repo.

**Tech Stack:** Laravel 8 (PHP 7.4 — `php@7.4`, có ext `intl`), Maatwebsite Excel, Nuxt 2 / Vue 2 (node 12, heap 8192), PHPUnit trên DB
local `hrm_erp`, Playwright MCP.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-05-update-style-bao-cao-meeting-theo-nhan-vien-design.md`
**Mockup đã duyệt:** `./mockup.html` (comment đầu file a → m) · **Design tóm tắt:** `./design.md` (15 quyết định)
**Khuôn / bài học:** `../meeting-by-projects/plan.md` + `sdd-ledger.md` (Ruling + minor + final review I1–I3 đã gộp vào plan này).

## Global Constraints

- Nhánh `gop_db-update-style-meeting-by-employees` tách từ `origin/gop_db` (cả 2 repo), làm trong worktree
  `websites/wt-update-style-mbe/{hrm-api,hrm-client}`. Cổng: api **8019**, client **3019** (05/10 đã kiểm `lsof`: 8018/3018 của
  báo cáo 1 đang chạy, 8019/3019 trống). Xong chỉ push nhánh feature; merge `gop_db` cần lệnh riêng của user.
- KHÔNG migration, KHÔNG seeder, KHÔNG quyền mới. Quyền giữ nguyên (seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1020-1022`,
  DB local khớp): **1057** "Xem báo cáo meeting theo nhân viên theo tổng công ty" · **1058** "… theo công ty" · **1059** "… theo phòng ban".
  Không bypass super admin.
- KHÔNG dùng `mysql2`. Meeting tính theo #11145: `start_date <= now` + status ∈ `Meeting::PAST_REPORT_STATUSES` (3, 4) HOẶC
  `start_date > now` + status ∈ `Meeting::FUTURE_REPORT_STATUSES` (2). Hủy = 0 phút.
- Kỳ: `period` = week | month | year (mặc định) | last_year | custom (+ `from`, `to` d/m/Y; thiếu hoặc from > to → 422) — dùng lại
  `MeetingByProjectsReportService::period()`.
- Thời lượng dòng cha / TỔNG / tổng hợp = PHÚT-NGƯỜI (Σ dòng lá). Số meeting / trạng thái / hình thức / loại = đếm meeting KHÔNG trùng.
- Nhóm "chưa có giá trị" gửi `0`: `meeting_type_id=0` = NULL hoặc 0 · `mode_id=0` = NULL / 0 / ngoài {1,2} · `scope_company_id=0` /
  `scope_department_id=0` = NULL hoặc 0.
- Mọi `LIKE` từ ô tìm phải escape `\`, `%`, `_`. Mọi `orderBy` phải có tiebreak id. Sắp tên tiếng Việt ở PHP dùng `Collator('vi_VN')`.
- Excel: số thô + `data-format`; SĐT/mã là CHUỖI (`WithCustomValueBinder`); tải bằng link `?token=`, không blob. In qua
  `ReportPrintPreviewModal` (`print-list-data`), không mở tab `/print`. FE gửi `scope_label` cho Excel/in popup.
- Số FE format `en-US` (`num()`); ngày `dd/mm/yyyy`. Trạng thái do BE trả `status_text` + `status_color`.
- KHÔNG `git stash` (repo dùng chung). KHÔNG `pkill` theo tên — kill đúng PID theo cổng. Mỗi commit kèm 2 dòng attribution của phiên.
- e2e chỉ chạy khi user yêu cầu, `--workers=1`, truyền `API_BASE=http://127.0.0.1:8019 BASE_URL=http://127.0.0.1:3019`.

## Review Focus

1. Meeting có NV trong phạm vi lẫn NV ngoài phạm vi (khác phòng đang lọc / công ty khác ngoài quyền) → NV ngoài phạm vi KHÔNG có
   dòng, KHÔNG cộng phút-người, nhưng VẪN đếm Người tham gia (Task 2: `test_nguoi_tham_gia_tinh_ca_nv_ngoai_pham_vi`).
2. Trang 2 của phân trang theo NV vẫn có dòng Công ty/Phòng, số trên đó là tổng ĐỦ cả đơn vị (Task 2:
   `test_phan_trang_theo_nhan_vien_dong_cha_tong_du`).
3. User 1058 gửi `company_id` công ty khác qua URL → BE bỏ qua (Task 2: `test_quyen_cong_ty_bo_qua_company_id_la`); user 1059 chỉ
   thấy NV phòng quản lý (Task 2: `test_quyen_phong_ban_chi_nv_phong_quan_ly`).
4. Bấm số ở dòng Phòng / dòng NV / ô trạng thái → popup có đúng số dòng của ô; cột NV tham gia in đậm đúng phạm vi báo cáo
   (Task 3: `test_item_list_khop_o_bam_va_in_scope`).
5. Ô tìm gõ `%` / `_` → không khớp tất cả (Task 3: `test_item_list_q_escape`); lọc KH ra cả meeting KHÔNG gắn dự án nhưng có KH
   (Task 2: `test_loc_khach_hang_va_du_an`).

---

## File map

**hrm-api (tạo mới)**
- `Modules/Assign/Services/Report/MeetingByEmployeesReportService.php`: kỳ (uỷ quyền), lọc meeting, lọc NV + quyền
  (`applyEmployeeScope` — dùng chung `Meeting::canView`), dòng lá, totals, `index`, `itemRows/itemList`, `participantRows/participantList`,
  `employeeRows/employeeList`, `filterOptions`.
- `Modules/Assign/Services/Report/MeetingByEmployeesPrintService.php`: in `summary | detail | meetings | participants | employees` + `columns`.
- `Modules/Assign/Http/Controllers/Api/V1/MeetingByEmployeesReportController.php`
- `Modules/Assign/Export/MeetingByEmployeesReportExport.php` (cây) · `MeetingByEmployeesListExport.php` (meeting) ·
  `MeetingByEmployeesEmployeeExport.php` (nhân viên). Người tham gia DÙNG LẠI `MeetingByProjectsParticipantExport` (blade chung chung).
- `resources/views/exports/assign/meeting_by_employees_{report,list,employees}.blade.php`
- `resources/views/prints/assign/meeting_by_employees_{summary,detail,meetings,employees}.blade.php` (người tham gia dùng lại
  `prints/assign/meeting_by_projects_participants.blade.php`)
- `tests/Feature/MeetingByEmployees/{MeetingFixture.php,ReportApiTest.php,DrillApiTest.php,ExportPrintTest.php,MeetingCanViewTest.php}`

**hrm-api (sửa / xoá)**
- Sửa: `Modules/Assign/Routes/api.php` (khối "báo cáo meeting" dòng ~1196–1202), `Modules/Assign/Entities/Meeting/Meeting.php` (`canView`).
- Xoá ở Task 9: `Services/Report/MeetingByEmployeesService.php`; 6 method `meetingByEmployees`, `meetingByEmployeesExport`,
  `getMeetingsByTypeByEmployees`, `getMeetingsByModeByEmployees`, `getParticipantsByScopeByEmployees`, `getChartDataByEmployees` +
  thuộc tính/constructor `meetingByEmployeesService` + import thừa trong `ReportController.php`; `Transformers/MeetingResource/{MeetingByEmployeesResource,
  ChartDataByEmployeesResource,MeetingByStatusResource,ParticipantsByScopeResource,ChartDataResource}.php`; `app/ExcelExport/MeetingByEmployeesExport.php`;
  `resources/views/exports/meeting_by_employees_report.blade.php`.

**hrm-client (`pages/assign/report/meeting-by-employees/`)**
- Viết lại: `index.vue`. Tạo: `api.js`, `format.js`, `components/{MeetingSummary,MeetingTree,MeetingListModal,ParticipantListModal,
  EmployeeListModal,PrintOptionsModal,DrillNum,InfoTip}.vue`.
- Xoá ở Task 9: `print.vue`, `components/{MeetingByEmployeesTable,MeetingByEmployeesPrintConfigModal,MeetingsByModeModal,MeetingsByStatusModal,
  MeetingsByTypeModal,ParticipantModal,ParticipantsByScopeModal,TopDepartmentsChart}.vue` (file cùng tên ở folder khác KHÔNG đụng).
- Sửa comment: `components/BaseMeetingChart.vue:132`, `pages/assign/report/potential-customer-care/components/CareTrackingTable.vue:25`.
- e2e (ngoài git): `HRM/e2e/tests/assign/meeting-by-employees.api.spec.ts`, `meeting-by-employees.spec.ts`.

---

### Task 1: Dựng worktree 2 repo

**Files:** không có file code.

- [x] **Step 1: Tạo nhánh + worktree**

```bash
M=/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM
W=/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-update-style-mbe
git -C $M/hrm-api fetch origin gop_db && git -C $M/hrm-api worktree add -b gop_db-update-style-meeting-by-employees $W/hrm-api origin/gop_db
git -C $M/hrm-client fetch origin gop_db && git -C $M/hrm-client worktree add -b gop_db-update-style-meeting-by-employees $W/hrm-client origin/gop_db
```

- [x] **Step 2: Copy (KHÔNG symlink) vendor / node_modules + .env, autoload trỏ worktree**

```bash
cp -Rc $M/hrm-api/vendor $W/hrm-api/vendor && cp $M/hrm-api/.env $W/hrm-api/.env
cp -Rc $M/hrm-client/node_modules $W/hrm-client/node_modules && cp $M/hrm-client/.env $W/hrm-client/.env
cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php $(which composer) dump-autoload -q && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear
/opt/homebrew/opt/php@7.4/bin/php -r 'require "vendor/autoload.php"; echo (new ReflectionClass("Modules\\Assign\\Entities\\Meeting\\Meeting"))->getFileName(), PHP_EOL;'
```
Expected: đường dẫn chứa `wt-update-style-mbe/hrm-api`. Ra checkout chính / `wt-update-style-mbp` thì DỪNG sửa trước (memory
worktree-vendor-symlink-autoload-bug).

- [x] **Step 3: Server cổng riêng**

```bash
lsof -nP -iTCP:8019 -iTCP:3019 -sTCP:LISTEN   # phải rỗng
cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan serve --port 8019     # background, ghi PID
# .env của client WORKTREE: trỏ API 127.0.0.1:8019 (sửa .env của worktree, KHÔNG sửa checkout chính)
cd $W/hrm-client && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npx nuxt --port 3019 --hostname 127.0.0.1  # background
```
Mở `http://127.0.0.1:3019/assign/report/meeting-by-employees`: màn cũ phải chạy (mốc so sánh). Chụp lại 1 ảnh + số tổng để báo user khi so.

---

### Task 2: Service lõi — lọc meeting, lọc NV + quyền, dòng lá, totals, `index` (cây + phân trang theo NV)

**Files:**
- Create: `Modules/Assign/Services/Report/MeetingByEmployeesReportService.php`
- Create: `Modules/Assign/Http/Controllers/Api/V1/MeetingByEmployeesReportController.php` (`index` + `filterOptions` tối thiểu)
- Create: `tests/Feature/MeetingByEmployees/MeetingFixture.php`, `tests/Feature/MeetingByEmployees/ReportApiTest.php`
- Modify: `Modules/Assign/Routes/api.php` — thêm route TẠM `-v2` (route cũ chạy tiếp cho FE cũ tới Task 9).

**Interfaces:**
- Consumes: `MeetingByProjectsReportService::period(Request): [Carbon $from, Carbon $to, string $label]`, `::MODES`, `::UNSET_TYPE_NAME`,
  `::UNSET_MODE_NAME`; `MeetingParticipantCounter::keys(array $ids): Collection<{meeting_id:int, key:string}>`.
- Produces:
  - Hằng `PERM_ALL`, `PERM_COMPANY`, `PERM_DEPT`, `STATUSES = [2,3,4]`, `STATUS_LABELS = [2=>'Chốt lịch',3=>'Hoàn thành',4=>'Đã hủy']`,
    `PRINT_COLUMNS` (11 khoá → nhãn).
  - `period(Request): array` · `hasReportPermission(): bool` · `applyEmployeeScope($q, string $info = 'i', string $emp = 'e'): void`
  - `leafQuery(Request $r, array $skip = [], bool $withRowScope = true): Builder` (chưa select) · `leaves(Request $r, bool $withRowScope = true): Collection<array Leaf>`
  - Leaf = `{employee_id, employee_name, employee_code, position, company_id, company_name, company_code, department_id, department_name,
    department_code, meeting_id, status, start_date, start_time, end_time, type_id, type_name, mode_id, mode_name, role, duration}` (id 0 = chưa có)
  - `participantKeys(array $meetingIds): array<int, string[]>` · `totals(Collection $leaves, array $keys): array{employees, meetings,
    duration, participants, by_status{'2','3','4'}, by_mode{'1','2','0'}, by_type[{id,name,count}]}`
  - `meetingDetails(array $ids, array $keys): array<int, array>` · `meetingRow(array $leaf, array $detail): array` (MeetingRow của spec §4)
  - `index(Request $r, bool $all = false): array{summary, groups, meta}`
  - static `viCompare(string, string): int`, `likeValue(string): string`, `breakdownText(array $totals, string $key): string`, `typeText(array $totals): string`, `timeText(array $row): string`

- [x] **Step 1: Fixture**

```php
<?php

namespace Tests\Feature\MeetingByEmployees;

use App\Models\TpEmployee;
use App\Support\RequestCache;
use Carbon\Carbon;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\ProspectiveProject;

/**
 * Dữ liệu test báo cáo meeting theo nhân viên trên DB local thật (khuôn tests/Feature/MeetingByProjects).
 * CÔ LẬP bằng ngày họp: dữ liệu thật bắt đầu 18/05/2026 → test dùng kỳ Tuỳ chọn đúng 1 ngày PAST_DAY (quá khứ) /
 * FUTURE_DAY (tương lai, cho Chốt lịch #11145).
 */
trait MeetingFixture
{
    protected $fxMeetingIds = [];
    protected $fxProjectIds = [];
    protected $fxRoleIds = [];
    protected $fxManageIds = [];

    protected static $PAST_DAY = '2001-03-15';
    protected static $FUTURE_DAY = '2031-03-15';

    /** Tham số kỳ Tuỳ chọn đúng 1 ngày 'Y-m-d' */
    protected function day(string $ymd): array
    {
        $d = Carbon::parse($ymd)->format('d/m/Y');

        return ['period' => 'custom', 'from' => $d, 'to' => $d];
    }

    /** 1 NV (employees.id) có hồ sơ hiện tại thuộc công ty / phòng, trừ các id cho trước */
    protected function employeeWhere(array $where, array $except = []): int
    {
        $q = DB::table('employees as e')->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')->whereNotIn('e.id', $except ?: [0]);
        foreach ($where as $col => $val) {
            $q->where('i.' . $col, $val);
        }

        return (int) $q->orderBy('e.id')->value('e.id');
    }

    protected function freshCustomers(int $n = 1): array
    {
        return DB::table('customers')->whereNull('deleted_at')
            ->whereNotIn('id', DB::table('meetings')->whereNotNull('customer_id')->select('customer_id'))
            ->whereNotIn('id', DB::table('prospective_projects')->whereNotNull('customer_id')->select('customer_id'))
            ->orderByDesc('id')->limit($n)->pluck('id')->map('intval')->all();
    }

    protected function makeProject(int $creatorId, int $customerId, array $attrs = []): ProspectiveProject
    {
        $src = ProspectiveProject::whereNull('parent_id')->orderByDesc('id')->firstOrFail();
        $p = $src->replicate();
        $p->forceFill(array_merge([
            'code' => 'PHPUNIT-MBE-' . uniqid(), 'name' => 'PHPUnit dự án ' . uniqid(), 'customer_id' => $customerId,
            'status' => 4, 'created_by' => $creatorId, 'main_sale_employee_id' => $creatorId, 'company_id' => 1, 'parent_id' => null,
        ], $attrs));
        $p->saveQuietly();
        $this->fxProjectIds[] = $p->id;

        return $p->fresh();
    }

    /**
     * Meeting mặc định: PAST_DAY 09:00–10:00 (60'), Hoàn thành, Trực tiếp, KHÔNG khách hàng, không dự án, người tạo / chủ trì = 27.
     * $members = [['type'=>1,'employee_id'=>27,'role'=>'Chủ trì'], ['type'=>2,'name'=>'Anh Minh','phone'=>'0912345678']]
     * $attrs['customer_id'] có thì tự điền customer_code / customer_name từ bảng customers.
     */
    protected function makeMeeting(array $attrs = [], array $members = [], ?ProspectiveProject $project = null): Meeting
    {
        $m = Meeting::orderByDesc('id')->firstOrFail()->replicate();
        $m->code = 'PHPUNIT-MBE-' . uniqid();
        $cus = !empty($attrs['customer_id']) ? DB::table('customers')->where('id', $attrs['customer_id'])->first(['code', 'name']) : null;
        $m->forceFill(array_merge([
            'name' => 'PHPUnit meeting ' . uniqid(), 'status' => Meeting::HOAN_THANH, 'mode_id' => 1,
            'start_date' => self::$PAST_DAY . ' 09:00:00', 'end_date' => self::$PAST_DAY . ' 10:00:00',
            'customer_id' => null, 'customer_code' => $cus ? $cus->code : null, 'customer_name' => $cus ? $cus->name : null,
            'created_by' => 27, 'host_employee_id' => 27, 'company_id' => 1, 'content' => 'PHPUnit nội dung',
        ], $attrs));
        $m->saveQuietly();
        $this->fxMeetingIds[] = $m->id;
        foreach ($members as $i => $mb) {
            DB::table('meeting_employees')->insert(array_merge(['meeting_id' => $m->id, 'sort_order' => $i, 'created_at' => now(), 'updated_at' => now()], $mb));
        }
        if ($project) {
            $this->linkProject($m, $project);
        }

        return $m->fresh();
    }

    protected function linkProject(Meeting $m, ProspectiveProject $p): void
    {
        DB::table('prospective_project_meetings')->insert([
            'prospective_project_id' => $p->id, 'meeting_id' => $m->id, 'meeting_code' => $m->code,
            'meeting_name' => $m->name ?: 'PHPUnit', 'created_at' => now(), 'updated_at' => now(),
        ]);
    }

    /** NV thành phần phía công ty */
    protected function emp(int $id, string $role = ''): array
    {
        return ['type' => 1, 'employee_id' => $id, 'role' => $role];
    }

    protected function grant(int $empId, int $permissionId): void
    {
        $companyId = (int) DB::table('employee_infos')->where('id', DB::table('employees')->where('id', $empId)->value('employee_info_id'))->value('company_id');
        $roleId = DB::table('roles')->insertGetId(['name' => 'PHPUNIT-MBE-' . uniqid(), 'guard_name' => 'api', 'status' => 1, 'company_id' => $companyId]);
        $this->fxRoleIds[] = $roleId;
        DB::table('employee_has_roles')->insert(['role_id' => $roleId, 'model_type' => 'Modules\Timesheet\Entities\Employee', 'employee_id' => $empId, 'position' => 0, 'company_id' => $companyId]);
        DB::table('role_has_permissions')->insert(['permission_id' => $permissionId, 'role_id' => $roleId, 'company_id' => $companyId]);
        Artisan::call('cache:clear');
        RequestCache::flush();
    }

    /** Cho $empId quản lý phòng $deptId (listManageDepartmentIds đọc employee_manage_departments) */
    protected function manageDepartment(int $empId, int $companyId, int $deptId): void
    {
        $this->fxManageIds[] = DB::table('employee_manage_departments')->insertGetId([
            'employee_id' => $empId, 'company_id' => $companyId, 'department_id' => $deptId, 'all_department' => 0,
            'created_at' => now(), 'updated_at' => now(),
        ]);
        Artisan::call('cache:clear');
        RequestCache::flush();
    }

    protected function actAs(int $empId): void
    {
        RequestCache::flush();
        $this->withHeader('Authorization', 'Bearer ' . auth('api')->login(TpEmployee::findOrFail($empId)));
    }

    protected function cleanupMeetingFixture(): void
    {
        if ($this->fxRoleIds) {
            DB::table('role_has_permissions')->whereIn('role_id', $this->fxRoleIds)->delete();
            DB::table('employee_has_roles')->whereIn('role_id', $this->fxRoleIds)->delete();
            DB::table('roles')->whereIn('id', $this->fxRoleIds)->delete();
        }
        DB::table('employee_manage_departments')->whereIn('id', $this->fxManageIds ?: [0])->delete();
        DB::table('meeting_employees')->whereIn('meeting_id', $this->fxMeetingIds ?: [0])->delete();
        DB::table('prospective_project_meetings')->whereIn('meeting_id', $this->fxMeetingIds ?: [0])->delete();
        Meeting::whereIn('id', $this->fxMeetingIds ?: [0])->delete();
        ProspectiveProject::whereIn('id', $this->fxProjectIds ?: [0])->delete();
        $this->fxMeetingIds = $this->fxProjectIds = $this->fxRoleIds = $this->fxManageIds = [];
        Artisan::call('cache:clear');
        RequestCache::flush();
    }
}
```

Kiểm trước khi chạy: `Meeting` có cột `content`, `company_id`, `host_employee_id` (đã xem `SHOW COLUMNS meetings` 05/10 — có).
`employee_manage_departments` có `all_department`, `part_ids` (đã xem — có). Nếu `replicate()` mang theo cột NOT NULL khác thì giữ.

- [x] **Step 2: Viết test fail (`ReportApiTest`)**

```php
<?php

namespace Tests\Feature\MeetingByEmployees;

use Modules\Assign\Entities\Meeting\Meeting;
use Tests\TestCase;

/**
 * Actor (DB local, đã tra 05/10): A = 27 (công ty 1, phòng 42) · VIEWER = 28 (công ty 1, phòng 42, KHÔNG có 1057–1059)
 * · B = 1180 (công ty 1, phòng 5). NV công ty 2 tra động bằng employeeWhere(['company_id' => 2]).
 */
class ReportApiTest extends TestCase
{
    use MeetingFixture;

    private const A = 27;
    private const VIEWER = 28;
    private const B = 1180;
    private const PERM_ALL = 1057;
    private const PERM_COMPANY = 1058;
    private const PERM_DEPT = 1059;
    private const URL = '/api/v1/assign/report/meeting-by-employees-v2';

    protected function tearDown(): void
    {
        $this->cleanupMeetingFixture();
        parent::tearDown();
    }

    private function api(int $emp, string $path = '', array $q = [])
    {
        $this->actAs($emp);

        return $this->getJson(self::URL . $path . ($q ? '?' . http_build_query($q) : ''));
    }

    /** id NV (đã sắp) có trong cây */
    private function employeeIds(array $data): array
    {
        $ids = [];
        foreach ($data['groups'] as $c) {
            foreach ($c['departments'] as $d) {
                foreach ($d['employees'] as $e) {
                    $ids[] = $e['employee_id'];
                }
            }
        }
        sort($ids);

        return $ids;
    }

    private function dept(array $data, int $deptId): array
    {
        foreach ($data['groups'] as $c) {
            foreach ($c['departments'] as $d) {
                if ($d['department_id'] === $deptId) {
                    return $d;
                }
            }
        }
        $this->fail('Không thấy phòng ' . $deptId);
    }

    public function test_tap_meeting_theo_quy_tac_11145(): void
    {
        $mk = function (string $day, int $status) {
            return $this->makeMeeting(['start_date' => "$day 09:00:00", 'end_date' => "$day 10:00:00", 'status' => $status], [$this->emp(self::A)]);
        };
        $pastDone = $mk(self::$PAST_DAY, Meeting::HOAN_THANH);
        $pastCancel = $mk(self::$PAST_DAY, Meeting::HUY);
        $mk(self::$PAST_DAY, Meeting::CHOT_LICH);
        $mk(self::$PAST_DAY, Meeting::LEN_LICH);
        $futureFixed = $mk(self::$FUTURE_DAY, Meeting::CHOT_LICH);
        $mk(self::$FUTURE_DAY, Meeting::HOAN_THANH);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $past = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->assertOk()->json('data');
        $this->assertSame(2, $past['summary']['meetings']);
        $this->assertEquals(['2' => 0, '3' => 1, '4' => 1], $past['summary']['by_status']);
        $this->assertSame(60, $past['summary']['duration'], 'Hủy = 0 phút');
        $ids = array_column($past['groups'][0]['departments'][0]['employees'][0]['meetings'], 'id');
        sort($ids);
        $this->assertSame([$pastDone->id, $pastCancel->id], $ids);

        $future = $this->api(self::VIEWER, '', $this->day(self::$FUTURE_DAY))->assertOk()->json('data');
        $this->assertSame(1, $future['summary']['meetings']);
        $this->assertSame($futureFixed->id, $future['groups'][0]['departments'][0]['employees'][0]['meetings'][0]['id']);
    }

    public function test_phut_nguoi_va_meeting_khong_trung(): void
    {
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::VIEWER), $this->emp(self::B)]);       // 60' × 3 NV
        $this->makeMeeting(['start_date' => self::$PAST_DAY . ' 14:00:00', 'end_date' => self::$PAST_DAY . ' 14:30:00'], [$this->emp(self::A)]); // 30'
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->assertOk()->json('data');
        $this->assertSame(3, $d['summary']['employees']);
        $this->assertSame(2, $d['summary']['meetings']);
        $this->assertSame(210, $d['summary']['duration']);
        $company = $d['groups'][0];
        $this->assertSame($d['summary']['duration'], $company['totals']['duration']);
        $this->assertSame(150, $this->dept($d, 42)['totals']['duration']);
        $this->assertSame(2, $this->dept($d, 42)['totals']['meetings']);
        $this->assertSame(60, $this->dept($d, 5)['totals']['duration']);
        $this->assertSame($company['totals']['duration'], array_sum(array_map(function ($x) { return $x['totals']['duration']; }, $company['departments'])));
        foreach ($company['departments'] as $dep) {
            $this->assertSame($dep['totals']['duration'], array_sum(array_map(function ($e) { return $e['totals']['duration']; }, $dep['employees'])));
            $this->assertSame($dep['totals']['meetings'], array_sum($dep['totals']['by_status']));
        }
        // Σ số meeting dòng con (2 + 1) > dòng công ty (2): đếm meeting không trùng — đúng quyết định #12
        $this->assertSame(2, $company['totals']['meetings']);
    }

    public function test_nv_trung_trong_mot_meeting_gop_mot_dong(): void
    {
        $this->makeMeeting([], [$this->emp(self::A, ''), $this->emp(self::A, 'Chủ trì')]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->assertOk()->json('data');
        $this->assertSame(60, $d['summary']['duration']);
        $this->assertSame(1, $d['summary']['participants']);
        $rows = $d['groups'][0]['departments'][0]['employees'][0]['meetings'];
        $this->assertCount(1, $rows);
        $this->assertSame('Chủ trì', $rows[0]['role']);
    }

    public function test_nguoi_tham_gia_tinh_ca_nv_ngoai_pham_vi(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::B), $this->emp($c2), ['type' => 2, 'name' => 'Anh Minh', 'phone' => '0912 345 678']]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + ['department_id' => 42])->assertOk()->json('data');
        $this->assertSame([self::A], $this->employeeIds($d));
        $this->assertSame(60, $d['summary']['duration']);
        $this->assertSame(4, $d['summary']['participants']);
    }

    public function test_phan_trang_theo_nhan_vien_dong_cha_tong_du(): void
    {
        $third = $this->employeeWhere(['company_id' => 1, 'department_id' => 42], [self::A, self::VIEWER]);
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::VIEWER), $this->emp($third)]);
        $this->makeMeeting(['start_date' => self::$PAST_DAY . ' 14:00:00', 'end_date' => self::$PAST_DAY . ' 14:30:00'], [$this->emp(self::A)]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $q = $this->day(self::$PAST_DAY) + ['per_page' => 1];
        $p1 = $this->api(self::VIEWER, '', $q + ['page' => 1])->assertOk()->json('data');
        $p2 = $this->api(self::VIEWER, '', $q + ['page' => 2])->assertOk()->json('data');
        $this->assertSame(3, $p2['meta']['total']);
        $this->assertCount(1, $p2['groups']);
        $this->assertCount(1, $p2['groups'][0]['departments']);
        $this->assertCount(1, $p2['groups'][0]['departments'][0]['employees']);
        $dept = $p2['groups'][0]['departments'][0]['totals'];
        $this->assertSame(3, $dept['employees']);
        $this->assertSame(2, $dept['meetings']);
        $this->assertSame(210, $dept['duration']);
        $this->assertSame($p1['groups'][0]['totals'], $p2['groups'][0]['totals'], 'dòng công ty lặp với tổng ĐỦ');
        $this->assertNotSame($p1['groups'][0]['departments'][0]['employees'][0]['employee_id'], $p2['groups'][0]['departments'][0]['employees'][0]['employee_id']);
    }

    public function test_quyen_tong_cong_ty_thay_moi_cong_ty_va_loc_cong_ty(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::B), $this->emp($c2)]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $all = [self::A, self::B, $c2];
        sort($all);
        $this->assertSame($all, $this->employeeIds($this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->json('data')));
        $this->assertSame([$c2], $this->employeeIds($this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + ['company_id' => 2])->json('data')));
        $this->assertTrue($this->api(self::VIEWER, '/filter-options', $this->day(self::$PAST_DAY))->json('data.can_change_company'));
    }

    public function test_quyen_cong_ty_bo_qua_company_id_la(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::B), $this->emp($c2)]);
        $this->grant(self::VIEWER, self::PERM_COMPANY);

        $expect = [self::A, self::B];
        sort($expect);
        $this->assertSame($expect, $this->employeeIds($this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + ['company_id' => 2])->json('data')));
        $this->assertFalse($this->api(self::VIEWER, '/filter-options', $this->day(self::$PAST_DAY))->json('data.can_change_company'));
    }

    public function test_quyen_phong_ban_chi_nv_phong_quan_ly(): void
    {
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::B)]);
        $this->grant(self::VIEWER, self::PERM_DEPT);
        $this->manageDepartment(self::VIEWER, 1, 42);

        $this->assertSame([self::A], $this->employeeIds($this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->json('data')));
    }

    public function test_khong_quyen_chi_thay_chinh_minh(): void
    {
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::VIEWER)]);
        $this->makeMeeting(['start_date' => self::$PAST_DAY . ' 14:00:00', 'end_date' => self::$PAST_DAY . ' 15:00:00'], [$this->emp(self::A)]);

        $d = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->assertOk()->json('data');
        $this->assertSame([self::VIEWER], $this->employeeIds($d));
        $this->assertSame(1, $d['summary']['meetings']);
        $this->assertSame(2, $d['summary']['participants'], 'người tham gia vẫn gồm A (ngoài phạm vi)');
    }

    public function test_loc_khach_hang_va_du_an(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $withProject = $this->makeMeeting(['customer_id' => $cus], [$this->emp(self::A)], $p);
        $noProject = $this->makeMeeting(['customer_id' => $cus], [$this->emp(self::A)]);
        $this->makeMeeting([], [$this->emp(self::A)]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $ids = function (array $q) {
            $rows = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + $q)->assertOk()->json('data.groups.0.departments.0.employees.0.meetings') ?: [];
            $out = array_column($rows, 'id');
            sort($out);

            return $out;
        };
        $this->assertSame([$withProject->id, $noProject->id], $ids(['customer_id' => $cus]));   // Ruling R1
        $this->assertSame([$withProject->id], $ids(['project_id' => $p->id]));
        $this->assertCount(3, $ids([]));
        $row = collect($this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->json('data.groups.0.departments.0.employees.0.meetings'))->firstWhere('id', $noProject->id);
        $this->assertSame($cus, $row['customer_id']);
        $this->assertNull($row['project_id']);
    }

    public function test_hinh_thuc_va_loai_chua_xac_dinh_gui_0(): void
    {
        $this->makeMeeting(['mode_id' => null, 'meeting_type_id' => null], [$this->emp(self::A)]);
        $this->makeMeeting(['mode_id' => 3, 'meeting_type_id' => 2], [$this->emp(self::A)]);   // loại 2 có thật (status 1, local 05/10)
        $this->makeMeeting(['mode_id' => 2, 'meeting_type_id' => 2], [$this->emp(self::A)]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY))->json('data');
        $this->assertEquals(['1' => 0, '2' => 1, '0' => 2], $d['summary']['by_mode']);
        $this->assertSame(2, $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + ['mode_id' => 0])->json('data.summary.meetings'));
        $this->assertSame(1, $this->api(self::VIEWER, '', $this->day(self::$PAST_DAY) + ['meeting_type_id' => 0])->json('data.summary.meetings'));
    }

    public function test_ky_custom_thieu_ngay_422(): void
    {
        $this->api(self::VIEWER, '', ['period' => 'custom', 'from' => '15/03/2001'])->assertStatus(422);
        $this->api(self::VIEWER, '', ['period' => 'custom', 'from' => '16/03/2001', 'to' => '15/03/2001'])->assertStatus(422);
    }
}
```

- [x] **Step 3: Chạy test, phải FAIL**

Run: `cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/MeetingByEmployees/ReportApiTest.php`
Expected: FAIL — 404 (route chưa có).

- [x] **Step 4: Viết service**

```php
<?php

namespace Modules\Assign\Services\Report;

use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\ProspectiveProject;

/**
 * Báo cáo meeting nhân viên theo thời gian (update-style-bao-cao-cu/meeting-by-employees, spec 2026-10-05).
 *
 * MỌI con số đi từ 1 tập DÒNG LÁ L = (NV công ty × meeting): meeting theo #11145 + kỳ + bộ lọc meeting; NV theo bộ lọc đơn vị
 * trên hồ sơ HIỆN TẠI + quyền (applyEmployeeScope — dùng chung với Meeting::canView). Dòng cha đếm meeting KHÔNG trùng, thời lượng
 * là PHÚT-NGƯỜI (Σ lá). Người tham gia đếm trên meeting của dòng, gồm cả người ngoài phạm vi (MeetingParticipantCounter).
 */
class MeetingByEmployeesReportService
{
    const PERM_ALL = 'Xem báo cáo meeting theo nhân viên theo tổng công ty';  // 1057
    const PERM_COMPANY = 'Xem báo cáo meeting theo nhân viên theo công ty';   // 1058
    const PERM_DEPT = 'Xem báo cáo meeting theo nhân viên theo phòng ban';    // 1059
    const MODES = MeetingByProjectsReportService::MODES;
    const STATUSES = [Meeting::CHOT_LICH, Meeting::HOAN_THANH, Meeting::HUY];
    /** Nhãn ở khối tổng hợp / dòng cha (design #5: "Đã hủy"); badge dòng meeting vẫn dùng Meeting::resolveStatusName */
    const STATUS_LABELS = [Meeting::CHOT_LICH => 'Chốt lịch', Meeting::HOAN_THANH => 'Hoàn thành', Meeting::HUY => 'Đã hủy'];
    const UNSET_TYPE_NAME = MeetingByProjectsReportService::UNSET_TYPE_NAME;
    const UNSET_MODE_NAME = MeetingByProjectsReportService::UNSET_MODE_NAME;
    const UNSET_UNIT_NAME = 'Chưa xác định';
    /** Cột chọn được khi in (#10, #15) — STT + cột Đối tượng luôn in */
    const PRINT_COLUMNS = [
        'pos' => 'Chức vụ', 'cnt' => 'Số meeting', 'st' => 'Trạng thái', 'time' => 'Thời gian', 'dur' => 'Thời lượng (phút)',
        'type' => 'Loại meeting', 'people' => 'Người tham gia', 'proj' => 'Dự án', 'kh' => 'Khách hàng', 'content' => 'Nội dung',
        'minutes' => 'Biên bản',
    ];
    private const PER_PAGE = 20;
    private const MAX_PER_PAGE = 500;
    private const CHUNK = 1000;

    public function period(Request $r): array
    {
        return app(MeetingByProjectsReportService::class)->period($r);
    }

    public function hasReportPermission(): bool
    {
        return isCurrentEmployeeHasPermission(self::PERM_ALL) || isCurrentEmployeeHasPermission(self::PERM_COMPANY)
            || isCurrentEmployeeHasPermission(self::PERM_DEPT);
    }

    /**
     * Phạm vi NV theo quyền báo cáo — NGUỒN DUY NHẤT (báo cáo, filter-options, Meeting::canView). Giữ đúng 4 mức bản cũ
     * (MeetingByEmployeesService::buildMemberPermissionConstraint): 1057 tất cả · 1058 hồ sơ thuộc công ty hiện tại ·
     * 1059 phòng / bộ phận mình quản lý · không quyền → chính mình.
     */
    public function applyEmployeeScope($q, string $info = 'i', string $emp = 'e'): void
    {
        if (isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            return;
        }
        if (isCurrentEmployeeHasPermission(self::PERM_COMPANY)) {
            $q->where("$info.company_id", (int) auth()->user()->current_company_role);

            return;
        }
        if (isCurrentEmployeeHasPermission(self::PERM_DEPT)) {
            $depts = (array) listManageDepartmentIds();
            $parts = (array) listManagePartIds();
            $q->where(function ($w) use ($info, $depts, $parts) {
                $w->whereIn("$info.department_id", $depts ?: [0])->orWhereIn("$info.part_id", $parts ?: [0]);
            });

            return;
        }
        $q->where("$emp.id", (int) auth()->user()->id);
    }

    /** '%kw%' đã escape \ % _ (ô tìm gõ % không được khớp tất cả) */
    public static function likeValue(string $kw): string
    {
        return '%' . addcslashes(trim($kw), '\\%_') . '%';
    }

    /** 0 = nhóm "chưa có" (NULL hoặc 0 lưu sót) */
    private function whereIdOrUnset($q, string $col, int $val): void
    {
        if ($val === 0) {
            $q->where(function ($w) use ($col) {
                $w->whereNull($col)->orWhere($col, 0);
            });
        } else {
            $q->where($col, $val);
        }
    }

    /** Tập meeting M: #11145 + kỳ + bộ lọc cấp meeting. $skip = khoá bỏ qua (filter-options: ô không tự bó mình). */
    public function applyMeetingFilters($q, Request $r, array $skip = []): void
    {
        [$from, $to] = $this->period($r);
        $now = Carbon::now()->format('Y-m-d H:i:s');
        // Kỳ luôn có → meeting thiếu start_date không vào kỳ nào (Ruling R2; bản cũ cũng vậy vì luôn lọc năm)
        $q->whereBetween('m.start_date', [$from->format('Y-m-d H:i:s'), $to->format('Y-m-d H:i:s')])
            ->where(function ($w) use ($now) {
                // #11145: xét mốc của TỪNG meeting — đã qua giờ: Hoàn thành / Hủy · chưa tới giờ: Chốt lịch
                $w->where(function ($past) use ($now) {
                    $past->where('m.start_date', '<=', $now)->whereIn('m.status', Meeting::PAST_REPORT_STATUSES);
                })->orWhere(function ($future) use ($now) {
                    $future->where('m.start_date', '>', $now)->whereIn('m.status', Meeting::FUTURE_REPORT_STATUSES);
                });
            });
        $has = function (string $key) use ($r, $skip) {
            return !in_array($key, $skip, true) && $r->filled($key);
        };
        if ($has('status')) {
            $q->where('m.status', (int) $r->get('status'));
        }
        if ($has('meeting_id')) {
            $q->where('m.id', (int) $r->get('meeting_id'));
        }
        if ($has('meeting_type_id')) {
            $this->whereIdOrUnset($q, 'm.meeting_type_id', (int) $r->get('meeting_type_id'));
        }
        if ($has('mode_id')) {
            $mode = (int) $r->get('mode_id');
            if ($mode === 0) {
                // "Chưa xác định": NULL / 0 / ngoài MODES — khớp cách totals() gom nhóm '0' (ruling báo cáo 1)
                $q->where(function ($w) {
                    $w->whereNull('m.mode_id')->orWhereNotIn('m.mode_id', array_keys(self::MODES));
                });
            } else {
                $q->where('m.mode_id', $mode);
            }
        }
        $project = function ($e) {
            $e->select(DB::raw(1))->from('prospective_project_meetings as ppm')
                ->join('prospective_projects as pp', 'pp.id', '=', 'ppm.prospective_project_id')
                ->whereColumn('ppm.meeting_id', 'm.id')->where('pp.status', '!=', ProspectiveProject::STATUS_DANG_TAO);
        };
        if ($has('customer_id')) {
            // Ruling R1: KH của meeting HOẶC KH của dự án gắn (mockup hiện KH cả với meeting không gắn dự án)
            $cus = (int) $r->get('customer_id');
            $q->where(function ($w) use ($cus, $project) {
                $w->where('m.customer_id', $cus)->orWhereExists(function ($e) use ($cus, $project) {
                    $project($e);
                    $e->where('pp.customer_id', $cus);
                });
            });
        }
        if ($has('project_id')) {
            $pid = (int) $r->get('project_id');
            $q->whereExists(function ($e) use ($pid, $project) {
                $project($e);
                $e->where('pp.id', $pid);
            });
        }
        if ($has('q')) {
            $like = self::likeValue((string) $r->get('q'));
            $q->where(function ($w) use ($like, $project) {
                $w->where('m.code', 'like', $like)->orWhere('m.name', 'like', $like)
                    ->orWhere('m.customer_name', 'like', $like)->orWhere('m.customer_code', 'like', $like)
                    ->orWhereExists(function ($e) use ($like, $project) {
                        $project($e);
                        $e->where(function ($x) use ($like) {
                            $x->where('pp.code', 'like', $like)->orWhere('pp.name', 'like', $like);
                        });
                    });
            });
        }
    }

    /** Bộ lọc đơn vị của BÁO CÁO trên hồ sơ hiện tại (i = employee_infos, e = employees) */
    public function applyEmployeeFilters($q, Request $r, array $skip = []): void
    {
        $has = function (string $key) use ($r, $skip) {
            return !in_array($key, $skip, true) && $r->filled($key);
        };
        if ($has('company_id') && isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            $q->where('i.company_id', (int) $r->get('company_id'));   // không quyền tổng công ty → BỎ QUA (ô bị khoá)
        }
        if ($has('department_id')) {
            $q->where('i.department_id', (int) $r->get('department_id'));
        }
        if ($has('part_id')) {
            $q->where('i.part_id', (int) $r->get('part_id'));
        }
        if ($has('employee_id')) {
            $q->where('e.id', (int) $r->get('employee_id'));
        }
    }

    /** Phạm vi DÒNG BẤM (drill) — khoá riêng scope_* để in_scope (#14) vẫn tính theo phạm vi báo cáo (Ruling R4) */
    public function applyRowScope($q, Request $r): void
    {
        if ($r->filled('scope_company_id')) {
            $this->whereIdOrUnset($q, 'i.company_id', (int) $r->get('scope_company_id'));
        }
        if ($r->filled('scope_department_id')) {
            $this->whereIdOrUnset($q, 'i.department_id', (int) $r->get('scope_department_id'));
        }
        if ($r->filled('scope_employee_id')) {
            $q->where('e.id', (int) $r->get('scope_employee_id'));
        }
    }

    /** 1 dòng = 1 dòng meeting_employees phía công ty (chưa gộp trùng), đã áp mọi bộ lọc + quyền, CHƯA select */
    public function leafQuery(Request $r, array $skip = [], bool $withRowScope = true)
    {
        $q = DB::table('meeting_employees as me')
            ->join('meetings as m', 'm.id', '=', 'me.meeting_id')
            ->join('employees as e', 'e.id', '=', 'me.employee_id')
            ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
            ->where('me.type', 1);
        $this->applyMeetingFilters($q, $r, $skip);
        $this->applyEmployeeFilters($q, $r, $skip);
        if ($withRowScope) {
            $this->applyRowScope($q, $r);
        }
        $this->applyEmployeeScope($q, 'i', 'e');

        return $q;
    }

    /** Dòng lá đã gộp trùng (NV, meeting), sắp đúng thứ tự cây (Ruling R6) */
    public function leaves(Request $r, bool $withRowScope = true): Collection
    {
        $rows = $this->leafQuery($r, [], $withRowScope)
            ->leftJoin('companies as c', 'c.id', '=', 'i.company_id')
            ->leftJoin('departments as d', 'd.id', '=', 'i.department_id')
            ->leftJoin('working_positions as wp', 'wp.id', '=', 'i.employee_work_position_id')
            ->leftJoin('meeting_types as mt', 'mt.id', '=', 'm.meeting_type_id')
            ->select([
                'e.id as employee_id', 'i.fullname', 'i.code as employee_code', 'wp.name as position',
                'i.company_id', 'c.name as company_name', 'c.code as company_code',
                'i.department_id', 'd.name as department_name', 'd.code as department_code',
                'm.id as meeting_id', 'm.status', 'm.start_date', 'm.end_date', 'm.meeting_type_id', 'mt.name as type_name', 'm.mode_id', 'me.role',
                DB::raw('CASE WHEN m.status = ' . Meeting::HUY . ' THEN 0 ELSE GREATEST(COALESCE(TIMESTAMPDIFF(MINUTE, m.start_date, m.end_date), 0), 0) END as duration'),
            ])
            ->orderByRaw('(i.company_id IS NULL OR i.company_id = 0)')->orderBy('c.name')->orderBy('i.company_id')
            ->orderByRaw('(i.department_id IS NULL OR i.department_id = 0)')->orderBy('d.name')->orderBy('i.department_id')
            ->orderBy('i.fullname')->orderBy('e.id')
            ->orderBy('m.start_date')->orderBy('m.id')->orderBy('me.sort_order')->orderBy('me.id')
            ->get();

        $out = [];
        foreach ($rows as $x) {
            $k = $x->employee_id . '|' . $x->meeting_id;
            $role = trim((string) $x->role);
            if (isset($out[$k])) {
                // 1 NV 2 lần trong 1 meeting → 1 dòng; giữ vai trò KHÁC RỖNG đầu tiên
                if ($out[$k]['role'] === '' && $role !== '') {
                    $out[$k]['role'] = $role;
                }
                continue;
            }
            $start = $x->start_date ? Carbon::parse($x->start_date) : null;
            $end = $x->end_date ? Carbon::parse($x->end_date) : null;
            $typeId = (int) $x->meeting_type_id;
            $modeId = (int) $x->mode_id;
            $out[$k] = [
                'employee_id' => (int) $x->employee_id, 'employee_name' => (string) $x->fullname, 'employee_code' => (string) $x->employee_code,
                'position' => (string) $x->position,
                'company_id' => (int) $x->company_id, 'company_name' => (int) $x->company_id ? (string) $x->company_name : self::UNSET_UNIT_NAME,
                'company_code' => (string) $x->company_code,
                'department_id' => (int) $x->department_id, 'department_name' => (int) $x->department_id ? (string) $x->department_name : self::UNSET_UNIT_NAME,
                'department_code' => (string) $x->department_code,
                'meeting_id' => (int) $x->meeting_id, 'status' => (int) $x->status,
                'start_date' => $start ? $start->format('Y-m-d') : null, 'start_time' => $start ? $start->format('H:i') : null,
                'end_time' => $end ? $end->format('H:i') : null,
                'type_id' => $typeId, 'type_name' => $typeId && $x->type_name ? (string) $x->type_name : self::UNSET_TYPE_NAME,
                'mode_id' => $modeId, 'mode_name' => self::MODES[$modeId] ?? self::UNSET_MODE_NAME,
                'role' => $role, 'duration' => (int) $x->duration,
            ];
        }

        return collect(array_values($out));
    }

    /** meeting_id => [khoá người không trùng] (chia khúc) — khoá do MeetingParticipantCounter quyết định */
    public function participantKeys(array $meetingIds): array
    {
        $out = [];
        foreach (array_chunk($meetingIds, self::CHUNK) as $chunk) {
            foreach (app(MeetingParticipantCounter::class)->keys($chunk) as $x) {
                $out[$x['meeting_id']][$x['key']] = $x['key'];
            }
        }

        return array_map('array_values', $out);
    }

    /** Số liệu 1 nút cây (spec §3.3): meeting không trùng, thời lượng phút-người, người tham gia trên meeting của nút */
    public function totals(Collection $leaves, array $keys): array
    {
        $u = $leaves->unique('meeting_id')->values();
        $people = [];
        foreach ($u as $x) {
            foreach ($keys[$x['meeting_id']] ?? [] as $k) {
                $people[$k] = true;
            }
        }
        $byStatus = [];
        foreach (self::STATUSES as $s) {
            $byStatus[(string) $s] = $u->where('status', $s)->count();
        }
        $byMode = ['1' => $u->where('mode_id', 1)->count(), '2' => $u->where('mode_id', 2)->count()];
        $byMode['0'] = $u->count() - $byMode['1'] - $byMode['2'];
        $byType = $u->groupBy('type_id')->map(function ($g) {
            return ['id' => $g->first()['type_id'], 'name' => $g->first()['type_name'], 'count' => $g->count()];
        })->values()->all();
        usort($byType, function ($a, $b) {
            return self::viCompare($a['name'], $b['name']) ?: $a['id'] <=> $b['id'];
        });

        return [
            'employees' => $leaves->pluck('employee_id')->unique()->count(),
            'meetings' => $u->count(),
            'duration' => (int) $leaves->sum('duration'),
            'participants' => count($people),
            'by_status' => $byStatus,
            'by_mode' => $byMode,
            'by_type' => $byType,
        ];
    }

    /** Chi tiết HIỂN THỊ (không ảnh hưởng số liệu) — chỉ nạp cho meeting cần hiện (trang / Excel / in) */
    public function meetingDetails(array $ids, array $keys): array
    {
        $out = [];
        foreach (array_chunk($ids, self::CHUNK) as $chunk) {
            $projects = DB::table('prospective_project_meetings as ppm')
                ->join('prospective_projects as p', 'p.id', '=', 'ppm.prospective_project_id')
                ->whereIn('ppm.meeting_id', $chunk)->where('p.status', '!=', ProspectiveProject::STATUS_DANG_TAO)
                ->orderBy('ppm.id')
                ->get(['ppm.meeting_id', 'p.id', 'p.code', 'p.name', 'p.customer_id', 'p.customer_code', 'p.customer_name'])
                ->groupBy('meeting_id');
            $meetings = DB::table('meetings as m')->whereIn('m.id', $chunk)->get([
                'm.id', 'm.code', 'm.name', 'm.content', 'm.customer_id', 'm.customer_code', 'm.customer_name',
                DB::raw('EXISTS(SELECT 1 FROM meeting_reports mr WHERE mr.meeting_id = m.id) as has_report'),
            ]);
            foreach ($meetings as $m) {
                $list = $projects->get($m->id, collect());
                $p = $list->first();   // Ruling R5: dự án gắn ĐẦU TIÊN (ppm.id nhỏ nhất)
                $fromProject = !$m->customer_id && $p && $p->customer_id;   // Ruling R1: KH của meeting, thiếu thì KH dự án
                $out[(int) $m->id] = [
                    'code' => (string) $m->code, 'name' => (string) $m->name, 'content' => htmlToText($m->content),
                    'customer_id' => $fromProject ? (int) $p->customer_id : ($m->customer_id ? (int) $m->customer_id : null),
                    'customer_code' => (string) ($fromProject ? $p->customer_code : $m->customer_code),
                    'customer_name' => (string) ($fromProject ? $p->customer_name : $m->customer_name),
                    'project_id' => $p ? (int) $p->id : null, 'project_code' => $p ? (string) $p->code : '',
                    'project_name' => $p ? (string) $p->name : '', 'project_count' => $list->count(),
                    'has_report' => (bool) $m->has_report, 'participants' => count($keys[(int) $m->id] ?? []),
                ];
            }
        }

        return $out;
    }

    /** MeetingRow (spec §4) = dữ liệu dòng lá + chi tiết hiển thị */
    public function meetingRow(array $leaf, array $detail): array
    {
        return array_merge($detail, [
            'id' => $leaf['meeting_id'], 'role' => $leaf['role'], 'status' => $leaf['status'],
            'status_text' => Meeting::resolveStatusName($leaf['status']), 'status_color' => Meeting::resolveStatusColor($leaf['status']),
            'start_date' => $leaf['start_date'], 'start_time' => $leaf['start_time'], 'end_time' => $leaf['end_time'],
            'duration' => $leaf['duration'], 'type_id' => $leaf['type_id'], 'type_name' => $leaf['type_name'],
            'mode_id' => $leaf['mode_id'], 'mode_name' => $leaf['mode_name'],
        ]);
    }

    public function index(Request $r, bool $all = false): array
    {
        [$from, $to, $label] = $this->period($r);
        $leaves = $this->leaves($r);
        $keys = $this->participantKeys($leaves->pluck('meeting_id')->unique()->values()->all());
        $empIds = $leaves->pluck('employee_id')->unique()->values();   // thứ tự cây (SQL đã sắp)
        $total = $empIds->count();
        $perPage = $all ? max(1, $total) : min(self::MAX_PER_PAGE, max(1, (int) $r->get('per_page', self::PER_PAGE)));
        $page = $all ? 1 : max(1, (int) $r->get('page', 1));
        $onPage = array_flip($empIds->forPage($page, $perPage)->all());
        $pageLeaves = $leaves->filter(function ($x) use ($onPage) {
            return isset($onPage[$x['employee_id']]);
        });
        $details = $this->meetingDetails($pageLeaves->pluck('meeting_id')->unique()->values()->all(), $keys);
        // Dòng Công ty / Phòng: tổng ĐỦ cả đơn vị (không theo trang) — quyết định #4
        $byCompany = $leaves->groupBy('company_id');
        $byDept = $leaves->groupBy(function ($x) {
            return $x['company_id'] . '|' . $x['department_id'];
        });

        $groups = [];
        foreach ($pageLeaves->groupBy('company_id') as $cid => $cLeaves) {
            $c = $cLeaves->first();
            $departments = [];
            foreach ($cLeaves->groupBy('department_id') as $did => $dLeaves) {
                $d = $dLeaves->first();
                $employees = [];
                foreach ($dLeaves->groupBy('employee_id') as $eLeaves) {
                    $e = $eLeaves->first();
                    $employees[] = [
                        'employee_id' => $e['employee_id'], 'name' => $e['employee_name'], 'code' => $e['employee_code'],
                        'position' => $e['position'], 'totals' => $this->totals($eLeaves, $keys),
                        'meetings' => $eLeaves->map(function ($x) use ($details) {
                            return $this->meetingRow($x, $details[$x['meeting_id']] ?? []);
                        })->values()->all(),
                    ];
                }
                $departments[] = [
                    'department_id' => (int) $did, 'name' => $d['department_name'], 'code' => $d['department_code'],
                    'totals' => $this->totals($byDept[$cid . '|' . $did], $keys), 'employees' => $employees,
                ];
            }
            $groups[] = [
                'company_id' => (int) $cid, 'name' => $c['company_name'], 'code' => $c['company_code'],
                'totals' => $this->totals($byCompany[$cid], $keys), 'departments' => $departments,
            ];
        }

        return [
            'summary' => $this->totals($leaves, $keys),
            'groups' => $groups,
            'meta' => [
                'total' => $total, 'per_page' => $perPage, 'current_page' => $page,
                'period_label' => $label, 'from' => $from->format('d/m/Y'), 'to' => $to->format('d/m/Y'),
            ],
        ];
    }

    /** So tên tiếng Việt (Collator vi_VN — ext intl có trên php@7.4); thiếu intl thì so chuỗi thường */
    public static function viCompare(string $a, string $b): int
    {
        static $collator = null;
        if ($collator === null) {
            $collator = class_exists(\Collator::class) ? new \Collator('vi_VN') : false;
        }

        return $collator ? (int) $collator->compare($a, $b) : strcmp(mb_strtolower($a), mb_strtolower($b));
    }

    /** "2 Chốt lịch · 5 Hoàn thành · 1 Đã hủy" / "3 Trực tiếp · 1 Chưa xác định" — Excel + bản in */
    public static function breakdownText(array $totals, string $key): string
    {
        $parts = [];
        foreach ($totals[$key] as $id => $n) {
            if ((int) $n > 0) {
                $name = $key === 'by_status' ? (self::STATUS_LABELS[(int) $id] ?? '') : (self::MODES[(int) $id] ?? self::UNSET_MODE_NAME);
                $parts[] = $n . ' ' . $name;
            }
        }

        return implode(' · ', $parts);
    }

    public static function typeText(array $totals): string
    {
        return implode(' · ', array_map(function ($t) {
            return $t['count'] . ' ' . $t['name'];
        }, $totals['by_type']));
    }

    /** "dd/mm/yyyy HH:ii - HH:ii" */
    public static function timeText(array $m): string
    {
        if (empty($m['start_date'])) {
            return '';
        }

        return Carbon::parse($m['start_date'])->format('d/m/Y') . ' ' . $m['start_time'] . ($m['end_time'] ? ' - ' . $m['end_time'] : '');
    }
}
```

Kiểm trên `origin/gop_db` trước khi chạy (đã xem 05/10): `htmlToText()` ở `app/Helper/FormatHelper.php:1215`; bảng `working_positions`
có cột `name`; `MeetingByProjectsReportService::UNSET_TYPE_NAME/UNSET_MODE_NAME/MODES` là `const` public.

- [x] **Step 5: Controller + route tạm**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Modules\Assign\Services\Report\MeetingByEmployeesReportService;

/** Báo cáo meeting nhân viên theo thời gian (khuôn MeetingByProjectsReportController). Gate nằm trong service. */
class MeetingByEmployeesReportController extends ApiController
{
    private $service;

    public function __construct(MeetingByEmployeesReportService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->index($request));
    }

    /** TỐI THIỂU (Task 4 thay bản đủ) */
    public function filterOptions(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, ['can_change_company' => isCurrentEmployeeHasPermission(MeetingByEmployeesReportService::PERM_ALL)]);
    }
}
```
Trong `Modules/Assign/Routes/api.php`, ngay dưới 6 route cũ `meeting-by-employees*` (khối `prefix /assign/report` dòng ~1196):
```php
        // Báo cáo meeting nhân viên theo thời gian — bản mới (update-style-bao-cao-cu). Tạm ở -v2 tới Task 9.
        Route::get('/meeting-by-employees-v2', [MeetingByEmployeesReportController::class, 'index']);
        Route::get('/meeting-by-employees-v2/filter-options', [MeetingByEmployeesReportController::class, 'filterOptions']);
```
Thêm `use Modules\Assign\Http\Controllers\Api\V1\MeetingByEmployeesReportController;` cạnh `use …MeetingByProjectsReportController;` (dòng 78).

- [x] **Step 6: Chạy test, phải PASS**

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/MeetingByEmployees/ReportApiTest.php`
Expected: 12 tests PASS. Gợi ý khi fail: `by_status` phải là object khoá chuỗi; `employeeWhere(['company_id'=>2])` ra 0 → DB local
thiếu NV công ty 2 (đổi sang công ty 4, 209 NV).

- [x] **Step 7: Commit (hrm-api)**

```bash
git add Modules/Assign/Services/Report/MeetingByEmployeesReportService.php Modules/Assign/Http/Controllers/Api/V1/MeetingByEmployeesReportController.php \
  Modules/Assign/Routes/api.php tests/Feature/MeetingByEmployees
git commit -m "Báo cáo meeting theo nhân viên (mới): dòng lá NV × meeting, quyền 4 mức, phút-người, phân trang theo nhân viên"
```

---

### Task 3: Drill — `item-list`, `participant-list`, `employee-list`

**Files:**
- Modify: `MeetingByEmployeesReportService.php` (thêm `itemRows`, `itemList`, `companyMembers`, `participantRows`, `participantList`, `employeeRows`, `employeeList`)
- Modify: controller + 3 route `-v2`
- Create: `tests/Feature/MeetingByEmployees/DrillApiTest.php`

**Interfaces:**
- Consumes: Task 2 (`leaves`, `leafQuery`, `participantKeys`, `meetingDetails`, `meetingRow`, `viCompare`); `MeetingParticipantCounter::listFor(array $ids, array $customerNameByMeeting)`.
- Produces:
  - `itemRows(Request): Collection<MeetingRow + employees[{id,name,code,in_scope}]>` (không có `role`) · `itemList(Request): {rows, meta{total, per_page, current_page, minutes}}`
  - `participantRows(Request): array<{side, name, position, unit, phone, meeting_count}>` · `participantList(Request): {rows, meta}`
  - `employeeRows(Request): array<{employee_id, name, code, company_name, department_id, department_name, position, meetings, duration}>` · `employeeList(Request): {rows, meta}`
  - Tham số: `scope_company_id`, `scope_department_id`, `scope_employee_id` (dòng bấm) · `status`, `meeting_type_id`, `mode_id`, `meeting_id` · `q` (meeting) · `pq` (người) · `eq` (nhân viên) · `side`.

- [x] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingByEmployees;

use Modules\Assign\Entities\Meeting\Meeting;
use Tests\TestCase;

class DrillApiTest extends TestCase
{
    use MeetingFixture;

    private const A = 27;
    private const VIEWER = 28;
    private const B = 1180;
    private const URL = '/api/v1/assign/report/meeting-by-employees-v2';

    protected function tearDown(): void
    {
        $this->cleanupMeetingFixture();
        parent::tearDown();
    }

    private function api(string $path, array $q = [])
    {
        $this->actAs(self::VIEWER);

        return $this->getJson(self::URL . $path . '?' . http_build_query($this->day(self::$PAST_DAY) + $q))->assertOk();
    }

    public function test_item_list_khop_o_bam_va_in_scope(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $m1 = $this->makeMeeting(['status' => Meeting::HUY], [$this->emp(self::A), $this->emp($c2)]);
        $this->makeMeeting(['mode_id' => null], [$this->emp(self::A), $this->emp(self::B)]);
        $this->makeMeeting([], [$this->emp(self::B)]);
        $this->grant(self::VIEWER, 1058);   // công ty 1: NV công ty 2 ngoài phạm vi

        $d = $this->api('')->json('data');
        $sum = $d['summary'];
        $list = $this->api('/item-list')->json('data');
        $this->assertSame($sum['meetings'], $list['meta']['total']);
        $this->assertSame(120, $list['meta']['minutes'], 'phút meeting (mỗi meeting 1 lần, Hủy 0) — khác phút-người');
        $this->assertSame($sum['by_status']['4'], $this->api('/item-list', ['status' => 4])->json('data.meta.total'));
        $this->assertSame($sum['by_mode']['0'], $this->api('/item-list', ['mode_id' => 0])->json('data.meta.total'));
        $dept42 = collect($d['groups'][0]['departments'])->firstWhere('department_id', 42);
        $this->assertSame($dept42['totals']['meetings'], $this->api('/item-list', ['scope_company_id' => 1, 'scope_department_id' => 42])->json('data.meta.total'));
        $this->assertSame(2, $this->api('/item-list', ['scope_employee_id' => self::B])->json('data.meta.total'));

        $row = collect($list['rows'])->firstWhere('id', $m1->id);
        $flags = collect($row['employees'])->pluck('in_scope', 'id')->all();
        $this->assertSame([self::A => true, $c2 => false], $flags);
        // Popup mở từ dòng NV B: cờ in_scope vẫn theo phạm vi BÁO CÁO (A vẫn đậm) — Ruling R4
        $rowB = collect($this->api('/item-list', ['scope_employee_id' => self::B])->json('data.rows'))->first(function ($x) {
            return count($x['employees']) === 2;
        });
        $this->assertTrue(collect($rowB['employees'])->firstWhere('id', self::A)['in_scope']);
    }

    public function test_item_list_q_escape(): void
    {
        $this->makeMeeting(['name' => 'Họp 50% tiến độ'], [$this->emp(self::A)]);
        $this->makeMeeting(['name' => 'Họp khác'], [$this->emp(self::A)]);
        $this->grant(self::VIEWER, 1057);

        $this->assertSame(1, $this->api('/item-list', ['q' => '50%'])->json('data.meta.total'));
        $this->assertSame(1, $this->api('/item-list', ['q' => '%'])->json('data.meta.total'));
        $this->assertSame(0, $this->api('/item-list', ['q' => '_'])->json('data.meta.total'));
    }

    public function test_participant_list_gop_va_loc(): void
    {
        [$cus] = $this->freshCustomers();
        $m1 = $this->makeMeeting(['customer_id' => $cus], [$this->emp(self::A), ['type' => 2, 'name' => 'Anh  Minh', 'phone' => '0912 345 678'], ['type' => 2, 'name' => '', 'phone' => '']]);
        $this->makeMeeting(['customer_id' => $cus], [$this->emp(self::A), $this->emp(self::B), ['type' => 2, 'name' => 'anh minh', 'phone' => '0912345678']]);
        $this->grant(self::VIEWER, 1057);

        $this->assertSame(4, $this->api('')->json('data.summary.participants'));
        $rows = collect($this->api('/participant-list')->json('data.rows'));
        $this->assertCount(4, $rows);
        $minh = $rows->first(function ($x) { return mb_strtolower(preg_replace('/\s+/u', ' ', $x['name'])) === 'anh minh'; });
        $this->assertSame(2, $minh['meeting_count']);
        $this->assertSame(\DB::table('customers')->where('id', $cus)->value('name'), $minh['unit']);
        $this->assertCount(2, $this->api('/participant-list', ['side' => 'company'])->json('data.rows'));
        $this->assertCount(3, $this->api('/participant-list', ['meeting_id' => $m1->id])->json('data.rows'));
        $this->assertCount(3, $this->api('/participant-list', ['scope_employee_id' => self::B])->json('data.rows'));
    }

    public function test_employee_list_khop_so_nhan_vien(): void
    {
        $this->makeMeeting([], [$this->emp(self::A), $this->emp(self::B)]);
        $this->makeMeeting(['start_date' => self::$PAST_DAY . ' 14:00:00', 'end_date' => self::$PAST_DAY . ' 14:30:00'], [$this->emp(self::A)]);
        $this->grant(self::VIEWER, 1057);

        $sum = $this->api('')->json('data.summary');
        $rows = collect($this->api('/employee-list')->json('data.rows'));
        $this->assertCount($sum['employees'], $rows);
        $this->assertSame(['meetings' => 2, 'duration' => 90], array_intersect_key($rows->firstWhere('employee_id', self::A), ['meetings' => 0, 'duration' => 0]));
        $this->assertSame($sum['duration'], $rows->sum('duration'));
        $codeB = \DB::table('employees as e')->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')->where('e.id', self::B)->value('i.code');
        $this->assertCount(1, $this->api('/employee-list', ['eq' => $codeB])->json('data.rows'));
    }
}
```

- [x] **Step 2: Chạy, phải FAIL** — `vendor/bin/phpunit tests/Feature/MeetingByEmployees/DrillApiTest.php` → 404.

- [x] **Step 3: Thêm vào service**

```php
    /** Meeting không trùng của L ∩ dòng bấm, sắp theo thời gian — nguồn popup / Excel / in danh sách meeting */
    public function itemRows(Request $r): Collection
    {
        $u = $this->leaves($r)->unique('meeting_id')->sortBy(function ($x) {
            return ($x['start_date'] ?? '0000-00-00') . ' ' . ($x['start_time'] ?? '00:00') . ' ' . str_pad((string) $x['meeting_id'], 10, '0', STR_PAD_LEFT);
        })->values();
        $ids = $u->pluck('meeting_id')->all();
        $details = $this->meetingDetails($ids, $this->participantKeys($ids));
        $members = $this->companyMembers($ids, $r);

        return $u->map(function ($x) use ($details, $members) {
            $row = $this->meetingRow($x, $details[$x['meeting_id']] ?? []);
            unset($row['role']);
            $row['employees'] = $members[$x['meeting_id']] ?? [];

            return $row;
        });
    }

    /**
     * meeting_id => TẤT CẢ NV công ty của meeting (#14) [{id, name, code, in_scope}]. in_scope = cặp (NV, meeting) thuộc L của
     * BÁO CÁO (bộ lọc + quyền, KHÔNG theo dòng bấm — Ruling R4). Lộ tên NV ngoài quyền là chủ đích (user chấp nhận, chỉ tên).
     */
    private function companyMembers(array $ids, Request $r): array
    {
        $out = [];
        foreach (array_chunk($ids, self::CHUNK) as $chunk) {
            $inScope = [];
            foreach ($this->leafQuery($r, [], false)->whereIn('m.id', $chunk)->distinct()->get(['me.meeting_id', 'me.employee_id']) as $x) {
                $inScope[$x->meeting_id . '|' . $x->employee_id] = true;
            }
            $rows = DB::table('meeting_employees as me')
                ->join('employees as e', 'e.id', '=', 'me.employee_id')
                ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
                ->whereIn('me.meeting_id', $chunk)->where('me.type', 1)
                ->orderBy('me.sort_order')->orderBy('me.id')
                ->get(['me.meeting_id', 'e.id', 'i.fullname', 'i.code']);
            foreach ($rows as $x) {
                $mid = (int) $x->meeting_id;
                if (!isset($out[$mid][(int) $x->id])) {
                    $out[$mid][(int) $x->id] = ['id' => (int) $x->id, 'name' => (string) $x->fullname, 'code' => (string) $x->code, 'in_scope' => isset($inScope[$mid . '|' . $x->id])];
                }
            }
        }

        return array_map('array_values', $out);
    }

    public function itemList(Request $r): array
    {
        $rows = $this->itemRows($r);
        $perPage = min(self::MAX_PER_PAGE, max(1, (int) $r->get('per_page', self::MAX_PER_PAGE)));
        $page = max(1, (int) $r->get('page', 1));

        return [
            'rows' => $rows->forPage($page, $perPage)->values()->all(),
            'meta' => ['total' => $rows->count(), 'per_page' => $perPage, 'current_page' => $page, 'minutes' => (int) $rows->sum('duration')],
        ];
    }

    public function participantRows(Request $r): array
    {
        $ids = $this->leaves($r)->pluck('meeting_id')->unique()->values()->all();
        $customers = array_map(function ($d) { return $d['customer_name']; }, $this->meetingDetails($ids, []));
        $list = app(MeetingParticipantCounter::class)->listFor($ids, $customers);
        $side = $r->get('side');
        $kw = mb_strtolower(trim((string) $r->get('pq')));
        $list = array_values(array_filter($list, function ($x) use ($side, $kw) {
            if (in_array($side, ['company', 'customer'], true) && $x['side'] !== $side) {
                return false;
            }

            return $kw === '' || mb_strpos(mb_strtolower($x['name'] . ' ' . $x['phone']), $kw) !== false;
        }));
        usort($list, function ($a, $b) {   // listFor sắp byte-wise → sắp lại theo tiếng Việt
            return strcmp($a['side'], $b['side']) ?: self::viCompare($a['name'], $b['name']);
        });

        return $list;
    }

    public function participantList(Request $r): array
    {
        $rows = $this->participantRows($r);

        return ['rows' => $rows, 'meta' => ['total' => count($rows), 'per_page' => count($rows), 'current_page' => 1]];
    }

    /** Popup Nhân viên (#13): NV của L ∩ dòng bấm, đúng thứ tự cây; `eq` tìm tên / mã NV */
    public function employeeRows(Request $r): array
    {
        $kw = mb_strtolower(trim((string) $r->get('eq')));

        return $this->leaves($r)->groupBy('employee_id')->map(function ($l) {
            $x = $l->first();

            return [
                'employee_id' => $x['employee_id'], 'name' => $x['employee_name'], 'code' => $x['employee_code'],
                'company_name' => $x['company_name'], 'department_id' => $x['department_id'], 'department_name' => $x['department_name'],
                'position' => $x['position'], 'meetings' => $l->count(), 'duration' => (int) $l->sum('duration'),
            ];
        })->filter(function ($x) use ($kw) {
            return $kw === '' || mb_strpos(mb_strtolower($x['name'] . ' ' . $x['code']), $kw) !== false;
        })->values()->all();
    }

    public function employeeList(Request $r): array
    {
        $rows = $this->employeeRows($r);

        return ['rows' => $rows, 'meta' => ['total' => count($rows), 'per_page' => count($rows), 'current_page' => 1]];
    }
```

- [x] **Step 4: Controller (`itemList`, `participantList`, `employeeList` — khuôn `index`) + route**

```php
        Route::get('/meeting-by-employees-v2/item-list', [MeetingByEmployeesReportController::class, 'itemList']);
        Route::get('/meeting-by-employees-v2/participant-list', [MeetingByEmployeesReportController::class, 'participantList']);
        Route::get('/meeting-by-employees-v2/employee-list', [MeetingByEmployeesReportController::class, 'employeeList']);
```

- [x] **Step 5: Chạy 2 file PASS** — `vendor/bin/phpunit tests/Feature/MeetingByEmployees` → 16 tests PASS.

- [x] **Step 6: Commit** `git commit -am "Báo cáo meeting theo nhân viên: popup danh sách meeting (NV tham gia + phạm vi), người tham gia, nhân viên"` (nhớ `git add` file test mới).

---

### Task 4: `filter-options` đủ

**Files:**
- Modify: service (`filterOptions`), controller (thay bản tối thiểu), test `ReportApiTest.php` (+1 test)

**Interfaces:**
- Produces: `filterOptions(Request): {companies[{id,name}], departments[{id,name,company_id}], parts[{id,name,department_id}],
  employees[{id,name,company_id,department_id,part_id}], customers[{id,code,name}], projects[{id,code,name,customer_id}],
  meeting_types[{id,name,description}], modes[{id,name}], can_change_company}`.

- [x] **Step 1: Test fail**

```php
    public function test_filter_options_theo_quyen_va_khong_tu_bo_minh(): void
    {
        [$cus] = $this->freshCustomers();
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $p = $this->makeProject(self::A, $cus);
        $this->makeMeeting(['customer_id' => $cus], [$this->emp(self::A), $this->emp($c2)], $p);
        $this->makeMeeting([], [$this->emp(self::B)]);
        $this->grant(self::VIEWER, self::PERM_COMPANY);

        $o = $this->api(self::VIEWER, '/filter-options', $this->day(self::$PAST_DAY) + ['employee_id' => self::A, 'department_id' => 42])->assertOk()->json('data');
        $empIds = array_column($o['employees'], 'id');
        $this->assertContains(self::B, $empIds, 'ô NV / Phòng không tự bó theo chính nó');
        $this->assertNotContains($c2, $empIds, 'NV công ty khác ngoài quyền 1058');
        $this->assertContains(5, array_column($o['departments'], 'id'));
        $this->assertSame([1], array_column($o['companies'], 'id'));
        $this->assertContains($cus, array_column($o['customers'], 'id'));
        $this->assertContains($p->id, array_column($o['projects'], 'id'));
        $this->assertSame([['id' => 1, 'name' => 'Trực tiếp'], ['id' => 2, 'name' => 'Online']], $o['modes']);
        $this->assertFalse($o['can_change_company']);
    }
```
(Công ty hiện tại của actor 28 là 1 — `current_company_role` của TpEmployee; nếu DB local khác thì assert theo `auth()->user()->current_company_role`.)

- [x] **Step 2: FAIL. Step 3: Code**

```php
    /** Danh mục ô lọc trong quyền + kỳ (Ruling R3: đơn vị / NV có ≥ 1 dòng lá); mỗi nhóm bỏ chính khoá của nó */
    public function filterOptions(Request $r): array
    {
        $canAll = isCurrentEmployeeHasPermission(self::PERM_ALL);
        $units = $this->leafQuery($r, ['department_id', 'part_id', 'employee_id'], false)
            ->leftJoin('departments as d', 'd.id', '=', 'i.department_id')
            ->leftJoin('parts as pt', 'pt.id', '=', 'i.part_id')
            ->distinct()
            ->get(['e.id', 'i.fullname', 'i.code', 'i.company_id', 'i.department_id', 'i.part_id', 'd.name as department_name',
                'd.code as department_code', 'pt.name as part_name']);
        $sortByName = function (array $rows) {
            usort($rows, function ($a, $b) { return self::viCompare($a['name'], $b['name']) ?: $a['id'] <=> $b['id']; });

            return $rows;
        };
        $departments = $sortByName($units->filter(function ($x) { return $x->department_id; })->unique('department_id')->map(function ($x) {
            return ['id' => (int) $x->department_id, 'name' => (string) $x->department_name, 'company_id' => (int) $x->company_id];
        })->values()->all());
        $parts = $sortByName($units->filter(function ($x) { return $x->part_id; })->unique('part_id')->map(function ($x) {
            return ['id' => (int) $x->part_id, 'name' => (string) $x->part_name, 'department_id' => (int) $x->department_id];
        })->values()->all());
        $employees = $sortByName($units->unique('id')->map(function ($x) {
            return [
                'id' => (int) $x->id,
                'name' => employeeOptionLabel(['fullname' => $x->fullname, 'code' => $x->code, 'department_code' => $x->department_code]),
                'company_id' => (int) $x->company_id, 'department_id' => (int) $x->department_id, 'part_id' => $x->part_id ? (int) $x->part_id : null,
            ];
        })->values()->all());

        $cusFromMeeting = $this->leafQuery($r, ['customer_id', 'project_id'], false)->whereNotNull('m.customer_id')
            ->distinct()->get(['m.customer_id as id', 'm.customer_code as code', 'm.customer_name as name']);
        $linked = $this->leafQuery($r, ['customer_id', 'project_id'], false)
            ->join('prospective_project_meetings as ppm', 'ppm.meeting_id', '=', 'm.id')
            ->join('prospective_projects as p', 'p.id', '=', 'ppm.prospective_project_id')
            ->where('p.status', '!=', ProspectiveProject::STATUS_DANG_TAO)
            ->distinct()->get(['p.id', 'p.code', 'p.name', 'p.customer_id', 'p.customer_code', 'p.customer_name']);
        $customers = $sortByName($cusFromMeeting->map(function ($c) { return ['id' => (int) $c->id, 'code' => (string) $c->code, 'name' => (string) $c->name]; })
            ->merge($linked->filter(function ($p) { return $p->customer_id; })->map(function ($p) {
                return ['id' => (int) $p->customer_id, 'code' => (string) $p->customer_code, 'name' => (string) $p->customer_name];
            }))->unique('id')->values()->all());
        $projectId = $r->filled('project_id') ? (int) $r->get('project_id') : null;
        // Ô Dự án không tự bó: lấy lại khi đang lọc dự án
        $projectsSrc = $projectId === null ? $linked : $this->leafQuery($r, ['project_id'], false)
            ->join('prospective_project_meetings as ppm', 'ppm.meeting_id', '=', 'm.id')
            ->join('prospective_projects as p', 'p.id', '=', 'ppm.prospective_project_id')
            ->where('p.status', '!=', ProspectiveProject::STATUS_DANG_TAO)
            ->distinct()->get(['p.id', 'p.code', 'p.name', 'p.customer_id']);
        $projects = $projectsSrc->unique('id')->sortByDesc('id')->map(function ($p) {
            return ['id' => (int) $p->id, 'code' => (string) $p->code, 'name' => (string) $p->name, 'customer_id' => $p->customer_id ? (int) $p->customer_id : null];
        })->values()->all();
        $companies = $canAll
            ? DB::table('companies')->orderBy('name')->orderBy('id')->get(['id', 'name'])
            : DB::table('companies')->where('id', auth()->user()->current_company_role)->get(['id', 'name']);

        return [
            'companies' => $companies->map(function ($c) { return ['id' => (int) $c->id, 'name' => $c->name]; })->values()->all(),
            'departments' => $departments, 'parts' => $parts, 'employees' => $employees,
            'customers' => $customers, 'projects' => $projects,
            'meeting_types' => DB::table('meeting_types')->where('status', 1)->orderBy('name')->orderBy('id')->get(['id', 'name', 'description'])
                ->map(function ($x) { return (array) $x; })->all(),
            'modes' => array_map(function ($id) { return ['id' => $id, 'name' => self::MODES[$id]]; }, array_keys(self::MODES)),
            'can_change_company' => $canAll,
        ];
    }
```
Lưu ý: `$linked` đã bỏ khoá `customer_id` + `project_id` → khi KHÔNG lọc dự án, danh sách dự án vẫn bị bó theo KH? Không: `$linked`
bỏ cả 2 khoá. FE tự lọc dự án theo KH đang chọn (như báo cáo 1). Kiểm `employeeOptionLabel()` đọc khoá `fullname/code/department_code`
(`app/Helper/FormatHelper.php:1254` — đã xem).

- [x] **Step 4: Controller `filterOptions` gọi service (xoá bản tối thiểu).**
- [x] **Step 5: PASS cả thư mục (17 tests) → Commit** `git commit -am "Báo cáo meeting theo nhân viên: danh mục ô lọc theo quyền + kỳ"`

---

### Task 5: Excel (3 file mới + 1 dùng lại) + bản in 5 chế độ, chọn cột

**Files:**
- Create: `Modules/Assign/Export/MeetingByEmployeesReportExport.php`, `MeetingByEmployeesListExport.php`, `MeetingByEmployeesEmployeeExport.php`
- Create: `resources/views/exports/assign/meeting_by_employees_{report,list,employees}.blade.php`
- Create: `Modules/Assign/Services/Report/MeetingByEmployeesPrintService.php`,
  `resources/views/prints/assign/meeting_by_employees_{summary,detail,meetings,employees}.blade.php`
- Modify: controller (`export`, `exportItemList`, `exportParticipantList`, `exportEmployeeList`, `printListData`) + 5 route
- Create: `tests/Feature/MeetingByEmployees/ExportPrintTest.php`

**REQUIRED skills:** `export-excel` (số thô + `data-format="#,##0"`, logo `EmbedsCompanyLetterhead`, `WithColumnWidths`, mô tả
nhiều dòng qua `htmlToText`, chuỗi số giữ CHUỖI), `print-page` mục 4d (trần `printListMaxRows()` = 2000, `printListPayload`).

**Interfaces:**
- Consumes: `index($r, true)`, `itemRows`, `participantRows`, `employeeRows`, `breakdownText`, `typeText`, `timeText`, `PRINT_COLUMNS`.
- Produces: `MeetingByEmployeesPrintService::{render(Request): array, letterhead(): string, periodMeta(Request): array, columns(Request): string[]}`;
  route `export`, `item-list/export`, `participant-list/export`, `employee-list/export`, `print-list-data?mode=…&columns=…`.

- [x] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingByEmployees;

use Illuminate\Http\Request;
use Maatwebsite\Excel\Facades\Excel;
use Modules\Assign\Export\MeetingByEmployeesReportExport;
use Modules\Assign\Services\Report\MeetingByEmployeesPrintService;
use Modules\Assign\Services\Report\MeetingByEmployeesReportService;
use PhpOffice\PhpSpreadsheet\Cell\DataType;
use PhpOffice\PhpSpreadsheet\IOFactory;
use Tests\TestCase;

class ExportPrintTest extends TestCase
{
    use MeetingFixture;

    private const URL = '/api/v1/assign/report/meeting-by-employees-v2';

    protected function tearDown(): void
    {
        $this->cleanupMeetingFixture();
        parent::tearDown();
    }

    private function q(array $extra = []): string
    {
        return '?' . http_build_query($this->day(self::$PAST_DAY) + $extra);
    }

    public function test_excel_4_file_va_5_ban_in(): void
    {
        $m = $this->makeMeeting([], [$this->emp(27, 'Chủ trì'), ['type' => 2, 'name' => 'Anh Minh', 'phone' => '0912']]);
        $name27 = \DB::table('employees as e')->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')->where('e.id', 27)->value('i.fullname');
        $this->grant(28, 1057);
        $this->actAs(28);

        foreach (['/export', '/item-list/export', '/participant-list/export', '/employee-list/export'] as $path) {
            $res = $this->get(self::URL . $path . $this->q());
            $res->assertOk();
            $this->assertStringContainsString('.xlsx', $res->headers->get('content-disposition'), $path);
        }
        $expect = ['summary' => $m->code, 'detail' => $m->code, 'meetings' => $m->code, 'participants' => 'Anh Minh', 'employees' => $name27];
        foreach ($expect as $mode => $needle) {
            $html = $this->getJson(self::URL . '/print-list-data' . $this->q(['mode' => $mode]))->assertOk()->json('data.template');
            $this->assertStringContainsString($needle, $html, $mode);
        }
        $this->assertStringContainsString('Chủ trì', $this->getJson(self::URL . '/print-list-data' . $this->q(['mode' => 'detail']))->json('data.template'));
    }

    public function test_ban_in_chon_cot_ap_ca_2_ban(): void
    {
        $this->makeMeeting(['content' => 'NOIDUNG-PHPUNIT'], [$this->emp(27)]);
        $this->grant(28, 1057);
        $this->actAs(28);

        foreach (['summary', 'detail'] as $mode) {
            $html = $this->getJson(self::URL . '/print-list-data' . $this->q(['mode' => $mode, 'columns' => 'st,dur']))->assertOk()->json('data.template');
            $this->assertStringContainsString('Trạng thái', $html, $mode);
            $this->assertStringNotContainsString('NOIDUNG-PHPUNIT', $html, $mode);
            $this->assertStringNotContainsString('>Nội dung<', $html, $mode);
            $all = $this->getJson(self::URL . '/print-list-data' . $this->q(['mode' => $mode]))->json('data.template');
            $this->assertStringContainsString('NOIDUNG-PHPUNIT', $all, $mode . ' — thiếu columns = in đủ cột');
        }
    }

    public function test_ban_in_vuot_tran_thi_bi_chan(): void
    {
        $this->makeMeeting([], [$this->emp(27)]);
        $this->grant(28, 1057);
        $this->actAs(28);
        $this->app->bind(MeetingByEmployeesPrintService::class, function ($app) {
            return new class($app->make(MeetingByEmployeesReportService::class)) extends MeetingByEmployeesPrintService {
                protected function printListPayload(string $html, int $total): array
                {
                    return ['template' => $total > 0 ? '' : $html, 'total' => $total, 'limit' => 0, 'truncated' => $total > 0];
                }
            };
        });
        foreach (['summary', 'detail', 'meetings', 'participants', 'employees'] as $mode) {
            $data = $this->getJson(self::URL . '/print-list-data' . $this->q(['mode' => $mode]))->assertOk()->json('data');
            $this->assertTrue($data['truncated'], $mode);
        }
    }

    public function test_excel_cay_so_tho_va_dong_tong(): void
    {
        $this->makeMeeting([], [$this->emp(27), $this->emp(1180)]);
        $this->grant(28, 1057);
        $this->actAs(28);
        $r = Request::create('/x', 'GET', $this->day(self::$PAST_DAY));
        $report = app(MeetingByEmployeesReportService::class)->index($r, true);

        $file = tempnam(sys_get_temp_dir(), 'mbe') . '.xlsx';
        file_put_contents($file, Excel::raw((new MeetingByEmployeesReportExport())->forReport($report, '', ''), \Maatwebsite\Excel\Excel::XLSX));
        $sheet = IOFactory::load($file)->getActiveSheet();
        unlink($file);

        $this->assertSame('TỔNG', $sheet->getCell('A6')->getValue());
        $this->assertSame(DataType::TYPE_NUMERIC, $sheet->getCell('G6')->getDataType());   // G = Thời lượng (phút-người)
        $this->assertSame(120, (int) $sheet->getCell('G6')->getValue());
        $this->assertSame(DataType::TYPE_STRING, $sheet->getCell('A9')->getDataType());    // "1.1" không bị ép số
    }
}
```

- [x] **Step 2: FAIL (404).**

- [x] **Step 3: 3 Export + blade** — copy khuôn `Modules/Assign/Export/MeetingByProjectsReportExport.php` / `MeetingByProjectsListExport.php`
  + blade `exports/assign/meeting_by_projects_{report,list}.blade.php` (đọc trên worktree), đổi:
  - **Report (cây)** `forReport(array $report, string $letterhead, string $scopeLabel)`: dòng 1 trống cho logo, dòng 2 tiêu đề "BÁO CÁO MEETING NHÂN VIÊN THEO
    THỜI GIAN", dòng 3 kỳ + `scopeLabel`, dòng 5 tiêu đề cột, dòng 6 TỔNG. Cột: A STT (I / 1 / 1.1 / 1.1.1 — luôn CHUỖI qua
    `bindValue` cột A) · B Công ty / Phòng / Nhân viên / Meeting (NV: "Tên (mã)"; meeting: "mã - tên") · C Chức vụ (NV: hồ sơ; meeting:
    vai trò) · D Số meeting · E Trạng thái (`breakdownText(by_status)` ở dòng cha; dòng meeting: `status_text`) · F Thời gian · G Thời lượng
    (phút) · H Loại meeting (`typeText` / `type_name`) · I Người tham gia · J Dự án ("mã - tên", "+n dự án" khi `project_count > 1`) ·
    K Khách hàng · L Nội dung · M Biên bản (Có/Chưa có). D, G, I: SỐ THÔ + `data-format="#,##0"`. Dòng Công ty/Phòng/NV in đậm.
    Bề rộng: A 8 · B 48 · C 22 · D 11 · E 30 · F 22 · G 14 · H 30 · I 13 · J 34 · K 34 · L 50 · M 11.
  - **List (meeting)**: STT · Mã meeting · Tên meeting · Thời gian · Thời lượng (phút) · Trạng thái · Loại · Hình thức · Nhân viên tham gia
    (công ty) (tên nối "; ") · Dự án · Khách hàng · Người tham gia · Biên bản. Dòng kỳ `periodMeta` + `scopeLabel`.
  - **Employee**: STT · Mã NV · Họ tên · Công ty · Phòng ban · Chức vụ · Số meeting · Thời lượng (phút). Mã NV là CHUỖI (`bindValue` cột B).
  - Người tham gia: KHÔNG tạo mới — controller dùng `MeetingByProjectsParticipantExport` (blade không nhắc "dự án").
  - Tên file: `bao-cao-meeting-theo-nhan-vien.xlsx`, `danh-sach-meeting-theo-nhan-vien.xlsx`, `danh-sach-nguoi-tham-gia-meeting.xlsx`,
    `danh-sach-nhan-vien-hop-meeting.xlsx`.

- [x] **Step 4: Print service + 4 blade**

```php
<?php

namespace Modules\Assign\Services\Report;

use Carbon\Carbon;
use Illuminate\Http\Request;
use Modules\Assign\Services\Concerns\PrintsCompanyLetterhead;
use Modules\CustomerCare\Services\Concerns\LimitsPrintListRows;

/**
 * Bản in báo cáo meeting theo nhân viên cho ReportPrintPreviewModal (khuôn MeetingByProjectsPrintService).
 * mode = summary (cây, mặc định) | detail (NV × meeting) | meetings | participants | employees.
 * `columns` (chuỗi khoá PRINT_COLUMNS) áp cho summary + detail (#15); thiếu / rỗng / toàn khoá lạ = in đủ.
 */
class MeetingByEmployeesPrintService
{
    use PrintsCompanyLetterhead;
    use LimitsPrintListRows;

    private $report;

    public function __construct(MeetingByEmployeesReportService $report)
    {
        $this->report = $report;
    }

    public function letterhead(): string
    {
        return $this->currentCompanyLetterhead();
    }

    public function columns(Request $request): array
    {
        $all = array_keys(MeetingByEmployeesReportService::PRINT_COLUMNS);
        $want = array_values(array_intersect($all, array_map('trim', explode(',', (string) $request->input('columns', '')))));

        return $want ?: $all;
    }

    public function render(Request $request): array
    {
        switch ($request->input('mode')) {
            case 'detail':
                return $this->renderDetail($request);
            case 'meetings':
                return $this->renderRows($request, $this->report->itemRows($request)->all(), 'prints.assign.meeting_by_employees_meetings');
            case 'participants':
                return $this->renderRows($request, $this->report->participantRows($request), 'prints.assign.meeting_by_projects_participants');
            case 'employees':
                return $this->renderRows($request, $this->report->employeeRows($request), 'prints.assign.meeting_by_employees_employees');
            default:
                return $this->renderSummary($request);
        }
    }

    private function renderSummary(Request $request): array
    {
        $report = $this->report->index($request, true);
        $total = 0;   // số dòng in = công ty + phòng + NV + meeting
        foreach ($report['groups'] as $c) {
            $total++;
            foreach ($c['departments'] as $d) {
                $total++;
                foreach ($d['employees'] as $e) {
                    $total += 1 + count($e['meetings']);
                }
            }
        }
        if ($total > static::printListMaxRows()) {
            return $this->printListPayload('', $total);
        }

        return $this->printListPayload(view('prints.assign.meeting_by_employees_summary', [
            'report' => $report, 'cols' => $this->columns($request), 'scopeLabel' => trim((string) $request->input('scope_label', '')),
            'letterhead' => $this->currentCompanyLetterhead(), 'printedAt' => Carbon::now()->format('d/m/Y H:i'),
        ])->render(), $total);
    }

    /** Bản Chi tiết: mỗi dòng 1 NV × 1 meeting, thứ tự cây */
    private function renderDetail(Request $request): array
    {
        $rows = [];
        foreach ($this->report->index($request, true)['groups'] as $c) {
            foreach ($c['departments'] as $d) {
                foreach ($d['employees'] as $e) {
                    foreach ($e['meetings'] as $m) {
                        $rows[] = ['company' => $c['name'], 'department' => $d['name'], 'employee' => $e, 'meeting' => $m];
                    }
                }
            }
        }

        return $this->renderRows($request, $rows, 'prints.assign.meeting_by_employees_detail');
    }

    private function renderRows(Request $request, array $rows, string $view): array
    {
        $total = count($rows);
        if ($total > static::printListMaxRows()) {
            return $this->printListPayload('', $total);
        }

        return $this->printListPayload(view($view, [
            'rows' => $rows, 'cols' => $this->columns($request), 'meta' => $this->periodMeta($request),
            'scopeLabel' => trim((string) $request->input('scope_label', '')),
            'letterhead' => $this->currentCompanyLetterhead(), 'printedAt' => Carbon::now()->format('d/m/Y H:i'),
        ])->render(), $total);
    }

    public function periodMeta(Request $request): array
    {
        [$from, $to, $label] = $this->report->period($request);

        return ['period_label' => $label, 'from' => $from->format('d/m/Y'), 'to' => $to->format('d/m/Y')];
    }
}
```
Blade copy `prints/assign/meeting_by_projects_{summary,detail}.blade.php` (A4 ngang, letterhead, thead lặp trang), đổi:
- `summary`: cột STT + "Công ty / Phòng / Nhân viên / Meeting" LUÔN in; 11 cột còn lại bọc `@if (in_array('<khoá>', $cols))` cả
  `<th>` lẫn `<td>` (khoá theo `PRINT_COLUMNS`). Dòng TỔNG đầu bảng.
- `detail`: STT · Công ty · Phòng ban · Nhân viên (mã) · Meeting (mã - tên) LUÔN in; tick: Chức vụ = "chức vụ hồ sơ · vai trò" (Ruling R8) ·
  Trạng thái · Thời gian · Thời lượng · Loại · Người tham gia · Dự án · Khách hàng · Nội dung · Biên bản. Khoá `cnt` (Số meeting)
  BỎ QUA ở bản này (mỗi dòng 1 meeting — Ruling R8).
- `meetings`: cột như Excel List; `employees`: như Excel Employee. Cả 2 có dòng kỳ `meta` + `scopeLabel`.

- [x] **Step 5: Controller + route**

```php
        Route::get('/meeting-by-employees-v2/export', [MeetingByEmployeesReportController::class, 'export']);
        Route::get('/meeting-by-employees-v2/item-list/export', [MeetingByEmployeesReportController::class, 'exportItemList']);
        Route::get('/meeting-by-employees-v2/participant-list/export', [MeetingByEmployeesReportController::class, 'exportParticipantList']);
        Route::get('/meeting-by-employees-v2/employee-list/export', [MeetingByEmployeesReportController::class, 'exportEmployeeList']);
        // Tên `print-list-data` là contract của utils/mixins/reportPrintPreviewMixin.js — đừng đổi
        Route::get('/meeting-by-employees-v2/print-list-data', [MeetingByEmployeesReportController::class, 'printListData']);
```
Method controller khuôn `MeetingByProjectsReportController::export/exportItemList/exportParticipantList/printListData`
(letterhead + `scope_label` + `periodMeta`). `exportParticipantList` dùng `new MeetingByProjectsParticipantExport()`.

- [x] **Step 6: PASS cả thư mục (21 tests) + mở 1 file Excel thật (tải qua `http://127.0.0.1:8019/...?token=`) kiểm logo / số có
  phân cách / không tam giác xanh ở SĐT và mã NV / cột không bị cắt → Commit**

```bash
git add Modules/Assign/Export Modules/Assign/Services/Report/MeetingByEmployeesPrintService.php resources/views tests/Feature/MeetingByEmployees Modules/Assign/Http Modules/Assign/Routes/api.php
git commit -m "Báo cáo meeting theo nhân viên: Excel cây / meeting / người tham gia / nhân viên và bản in 5 chế độ có chọn cột"
```

---

### Task 6: Nới `Meeting::canView()` theo phạm vi báo cáo (#9)

**Files:**
- Modify: `Modules/Assign/Entities/Meeting/Meeting.php` (`canView` dòng ~639 + method mới + `use`)
- Create: `tests/Feature/MeetingByEmployees/MeetingCanViewTest.php`

- [x] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingByEmployees;

use App\Models\TpEmployee;
use Modules\Assign\Entities\Meeting\Meeting;
use Tests\TestCase;

class MeetingCanViewTest extends TestCase
{
    use MeetingFixture;

    protected function tearDown(): void
    {
        $this->cleanupMeetingFixture();
        parent::tearDown();
    }

    private function canView(int $emp, int $meetingId): bool
    {
        $this->actAs($emp);
        auth('api')->setUser(TpEmployee::findOrFail($emp));

        return Meeting::findOrFail($meetingId)->canView();
    }

    public function test_quyen_cong_ty_xem_meeting_co_nv_cong_ty_minh(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        // người tạo / chủ trì = 27, VIEWER 28 KHÔNG là thành phần; company_id của meeting = 2 để luật "xem theo công ty" cũ không phủ
        $own = $this->makeMeeting(['company_id' => 2], [$this->emp(1180)]);
        $foreign = $this->makeMeeting(['company_id' => 2], [$this->emp($c2)]);
        $this->assertFalse($this->canView(28, $own->id), 'chưa có quyền thì luật cũ phải chặn — nếu true, đổi actor');

        $this->grant(28, 1058);
        $this->assertTrue($this->canView(28, $own->id));
        $this->assertFalse($this->canView(28, $foreign->id));
    }

    public function test_quyen_phong_ban_xem_meeting_co_nv_phong_quan_ly(): void
    {
        $inDept = $this->makeMeeting([], [$this->emp(1180)]);          // 1180 thuộc phòng 5
        $otherDept = $this->makeMeeting([], [$this->emp(27)]);         // 27 thuộc phòng 42
        $this->grant(28, 1059);
        $this->manageDepartment(28, 1, 5);

        $this->assertTrue($this->canView(28, $inDept->id));
        $this->assertFalse($this->canView(28, $otherDept->id), 'NV phòng 42 — 28 không quản lý phòng 42');
    }

    public function test_quyen_tong_cong_ty_xem_moi_meeting_co_nv_cong_ty(): void
    {
        $c2 = $this->employeeWhere(['company_id' => 2]);
        $foreign = $this->makeMeeting(['company_id' => 2], [$this->emp($c2)]);
        $noEmployee = $this->makeMeeting(['company_id' => 2], [['type' => 2, 'name' => 'Khách', 'phone' => '1']]);
        $this->grant(28, 1057);

        $this->assertTrue($this->canView(28, $foreign->id));
        $this->assertFalse($this->canView(28, $noEmployee->id), 'meeting không có NV công ty → không nới');
    }
}
```
Lưu ý mốc: dòng `assertFalse` đầu tiên phải đúng trên DB local. Nếu 28 xem được theo luật cũ (vd có quyền "Xem danh sách meeting theo …")
thì đổi actor sang NV không có quyền meeting nào (`SELECT` qua `employee_has_roles` ⨝ `role_has_permissions`). Ở test phòng ban: 27 cùng
phòng 42 với 28 nhưng 28 KHÔNG quản lý phòng 42 → kỳ vọng false; nếu `listManageDepartmentIds()` của 28 đã có sẵn phòng 42 (dữ liệu
thật) thì đổi `$otherDept` sang NV phòng khác.

- [x] **Step 2: FAIL. Step 3: Code**

```php
    public function canView()
    {
        return $this->canViewByMeetingRules() || $this->canViewByServiceDemandReport() || $this->canViewByPotentialCustomerTracking()
            || $this->canViewByMeetingByProjectsReport() || $this->canViewByMeetingByEmployeesReport();
    }

    /**
     * Quyền xem meeting theo phạm vi báo cáo meeting theo nhân viên (update-style-bao-cao-cu, quyết định #9 05/10/2026): ai thấy
     * meeting trong báo cáo thì mở được chi tiết — dùng CHUNG MeetingByEmployeesReportService::applyEmployeeScope():
     * 1057 → meeting có NV công ty bất kỳ · 1058 → có NV hồ sơ thuộc công ty hiện tại · 1059 → có NV phòng / bộ phận mình quản lý.
     * Không quyền → false (luật cũ đã cho người tham gia xem). Không lọc trạng thái / kỳ. Chỉ là quyền XEM.
     */
    private function canViewByMeetingByEmployeesReport()
    {
        $report = app(MeetingByEmployeesReportService::class);
        if (!$report->hasReportPermission()) {
            return false;
        }
        $q = \DB::table('meeting_employees as me')
            ->join('employees as e', 'e.id', '=', 'me.employee_id')
            ->join('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
            ->where('me.meeting_id', $this->id)->where('me.type', 1);
        $report->applyEmployeeScope($q, 'i', 'e');

        return $q->exists();
    }
```
Thêm `use Modules\Assign\Services\Report\MeetingByEmployeesReportService;` cạnh `use …MeetingByProjectsReportService;`.

- [x] **Step 4: PASS + chạy lại test canView có sẵn**: `vendor/bin/phpunit tests/Feature/MeetingByEmployees && vendor/bin/phpunit --filter "CanView|ServiceDemand|PotentialCustomerTracking|MeetingByProjects"`
- [x] **Step 5: Commit** `git commit -am "Meeting: quyền báo cáo meeting theo nhân viên được xem meeting có nhân viên trong phạm vi"` (add test mới).

---

### Task 7: FE — khung màn, bộ lọc, khối tổng hợp, bảng cây 4 cấp

**Files (hrm-client, `pages/assign/report/meeting-by-employees/`):**
- Rewrite: `index.vue`
- Create: `api.js`, `format.js`, `components/{MeetingSummary,MeetingTree,DrillNum,InfoTip}.vue`

**REQUIRED:** đọc `HRM/.claude/skills/report-styles/SKILL.md` + mở `mockup.html` (đã duyệt) cạnh code. CSS copy, không tự viết.

**Interfaces:**
- Consumes: `GET assign/report/meeting-by-employees-v2` (+ `/filter-options`). `API` đổi về `…/meeting-by-employees` ở Task 9.
- Produces:
  - `MeetingSummary`: props `summary, periodLabel, from, to`; emit `drill({ status?, mode_id?, title })` · `drill-people({ title })` · `drill-employees({ title })`.
  - `MeetingTree`: props `groups, summary, level (1..4), pagination`; emit `drill({ scope_company_id?, scope_department_id?, scope_employee_id?,
    status?, meeting_type_id?, title })`, `drill-people({ scope_*?, meeting_id?, title })`, `open-meeting(row)`, `open-minutes(row)`,
    `update:level`, `page-change`, `page-size-change`.

- [x] **Step 1: Copy nền**

```bash
S=$W/hrm-client/pages/assign/report/meeting-by-projects
D=$W/hrm-client/pages/assign/report/meeting-by-employees
T=/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.claude/skills/report-styles/template
cp $S/components/DrillNum.vue $S/components/InfoTip.vue $D/components/
cp $S/format.js $D/format.js
printf "/** Gốc API báo cáo meeting nhân viên theo thời gian — CHỈ ĐỌC (hrm-api Modules/Assign). */\nexport const API = 'assign/report/meeting-by-employees-v2'\n" > $D/api.js
cp $S/components/MeetingSummary.vue $D/components/MeetingSummary.vue
cp $S/components/MeetingTree.vue $D/components/MeetingTree.vue
```
`index.vue` cũ GIỮ tới Step 4 (đọc lại `pageTitleInfo`, key `table`). `InfoTip.vue`: id `mbp-info-` → `mbe-info-`. Mọi class `mbp-` → `mbe-`.

- [x] **Step 2: `MeetingSummary.vue`** — giữ template/SCSS, đổi `blocks()` + tiêu đề:
  - `.rsum-goal__title`: `Meeting nhân viên {{ periodLabel }} ({{ from }} – {{ to }})`; meta `· N nhân viên · N meeting`.
  - Khối `scope` "PHẠM VI": Nhân viên → `drill-employees` · Meeting → `drill({title})` · Người tham gia → `drill-people` · Tổng thời lượng
    (phút) `drill = null` (in `num()` thường) + `InfoTip` "Phút-người: cộng dồn thời lượng của từng nhân viên tham gia — 1 meeting 60 phút
    có 3 nhân viên tính 180 phút. Meeting Hủy tính 0. Khác tổng phút ở danh sách meeting (mỗi meeting tính 1 lần)".
  - Khối `state` "TRẠNG THÁI & HÌNH THỨC": Chốt lịch `status: 2` · Hoàn thành `status: 3` · Đã hủy `status: 4` · Trực tiếp `mode_id: 1` ·
    Online `mode_id: 2` · Chưa xác định `mode_id: 0` (GỬI 0, đừng bỏ); ô = 0 bỏ qua.

- [x] **Step 3: `MeetingTree.vue`** — nền là file vừa copy (đã có `CountList`, `applyLevel`, sticky, TỔNG), sửa:
  - Thêm lại CSS cấp `d2`/`d3` NGUYÊN VĂN từ `$T/components/TrackingTable.vue` (thụt 74/96px, vạch `::before` left 46/68, nền `#fafcfe`,
    dòng mở `#e9f3f9`/`#f1f8fb`, lá `#fff` chữ xám). d0 = Công ty, d1 = Phòng, d2 = Nhân viên, d3 = Meeting.
  - `COLS` 13 cột + `<colgroup>` theo mockup mục i: no 64 · name (còn lại, ≥ 440) · pos 170 · cnt 100 · st 270 · time 170 · dur 120 ·
    type 230 · people 120 · proj 260 · kh 260 · content 320 · minutes 90; `min-width: 2614px`. ⓘ tiêu đề cột lấy NGUYÊN VĂN mảng
    `COLS` trong `mockup.html` dòng 2811–2824.
  - `flatRows`: d0 `roman(i)` · d1 `${i}` · d2 `${i}.${j}` · d3 `${i}.${j}.${k}`; khoá dòng `c{cid}` / `c{cid}-d{did}` / `e{eid}` /
    `e{eid}-m{mid}`. `levelOptions = [{1,'Chỉ công ty'},{2,'Đến phòng ban'},{3,'Đến nhân viên'},{4,'Tất cả cấp'}]`, mặc định 3;
    `applyLevel(level)`: mở d0 khi ≥ 2, d1 khi ≥ 3, d2 khi = 4 (1 map `expanded{}` dùng chung với `.rsum-caret`).
  - Ô dòng cha (Công ty / Phòng / NV / TỔNG): Số meeting `DrillNum` · Trạng thái `CountList` 3 mục (Chốt lịch / Hoàn thành / Đã hủy, mỗi
    số bấm `drill({…scope, status})`) · Thời lượng `num(totals.duration)` căn phải không bấm · Loại `CountList` từ `by_type` (cắt "…", `:title`
    đủ; bấm gửi `meeting_type_id` = id, nhóm chưa phân loại gửi 0) · Người tham gia `DrillNum` → `drill-people({…scope})`. Chức vụ: dòng NV
    = `position`, Công ty/Phòng/TỔNG trống. Thời gian/Dự án/KH/Nội dung/Biên bản trống.
  - scope: Công ty `{scope_company_id}` · Phòng `{scope_company_id, scope_department_id}` · NV `{scope_employee_id}` · TỔNG `{}`.
  - Dòng meeting (d3): tên = mã (link `open-meeting`) + " - " + tên, chữ xám · Chức vụ = `role` · Trạng thái `V2BaseBadge :color="status_color"` ·
    Thời gian `dmy(start_date)` + giờ mờ · Thời lượng (Hủy hiện "0" xám `#c2cbd6`) · Loại `type_name` · Người tham gia `DrillNum` →
    `drill-people({ meeting_id, title })` · Dự án mã (link `/assign/prospective-projects/{id}` `target="_blank"`) + tên, `project_count > 1`
    thêm `.code-sub` "+{n-1} dự án" · KH tên + mã `.code-sub` · Nội dung 1 dòng cắt "…" + `:title` · Biên bản "Xem" (`open-minutes`) / "Chưa có" mờ.
  - `V2BasePagination item-label="nhân viên"`, `:page-size-options="[10, 20, 50, 100]"`.

- [x] **Step 4: `index.vue`** — copy `$S/index.vue` rồi sửa:
  - Comment đầu file theo màn này; `table="assign_meeting_by_employees_report"`; tiêu đề "Bộ lọc báo cáo meeting nhân viên theo thời gian";
    InfoTip "MỤC ĐÍCH BÁO CÁO": câu `pageTitleInfo` cũ ("Xem được mỗi nhân viên trong khoảng thời gian được chọn có bao nhiêu cuộc meeting…")
    + "Đã qua giờ: tính Hoàn thành + Hủy (Hủy 0 phút) · chưa tới giờ: tính Chốt lịch".
  - `filterFields` theo mockup mục a (2 hàng đủ 12 cột): hàng 1 Kỳ theo dõi (ⓘ) 3 · Công ty (slot, khoá theo `can_change_company`) 3 · Phòng ban 3 ·
    Bộ phận 3; hàng 2 Nhân viên 3 · Khách hàng (slot `V2BaseSelectRemote`, ≥ 2 ký tự, lọc tại FE trên `options.customers`) 3 · Dự án 2 ·
    Loại meeting (slot `MeetingTypeSelect` trong `V2BaseFloatingField`) 2 · Hình thức 2. Kỳ = Tuỳ chọn: chèn ô Thời gian sau Kỳ, chia lại
    hàng 1 Kỳ 2 · Thời gian 4 · Công ty 3 · Phòng ban 3, hàng 2 sáu ô × 2. Bỏ ô Giai đoạn / NV tạo dự án của báo cáo 1.
  - Cascade tại FE: `departmentOptions` lọc theo `company_id`; `partOptions` theo `department_id`; `employeeOptions` theo `company_id` /
    `department_id` / `part_id`; `projectOptions` theo `customer_id`. Đổi ô cha → xoá ô con không còn khớp. `keepSelectedOptions()` giữ mục đang chọn.
  - `loadOptions()` gọi lại khi đổi Kỳ / Công ty (danh mục theo kỳ — Ruling R3).
  - Bỏ `ProjectPhaseSelect`, `loadProjectPhases`, `creatorOptions`. `level: 3`, `perPage: 20`.
  - Gắn `@drill-employees` (Task 8 nối popup; Task 7 để stub `onDrillEmployees(){}`).

- [x] **Step 5: Kiểm Playwright MCP trên `http://127.0.0.1:3019/assign/report/meeting-by-employees` (ĐO DOM, skill mục 6)**
  - `th.top === body.top` (vùng cuộn) sau khi cuộn trong `V2BaseTableScroll`; `getComputedStyle(th).color` = `rgb(10, 124, 136)`.
  - `padding-left` d0/d1/d2/d3 = 30/52/74/96px; nền dòng theo skill mục 2; `table.offsetWidth >= 2614`, có 2 thanh cuộn.
  - Đổi cấp 1→4: số `.rsum-tb__row--d0/d1/d2/d3` đúng (cấp 3: d3 = 0; cấp 4: d3 = Σ meetings của NV trên trang).
  - Khối tổng hợp = dòng TỔNG (đọc text 2 nơi: Nhân viên, Meeting, Người tham gia, Thời lượng); Σ thời lượng dòng Phòng = dòng Công ty.
  - Phân trang: chọn 10/trang → trang 2 có lại dòng Công ty + Phòng, số trên đó BẰNG trang 1.
  - 1366px: các ô `.rsum-blk__item` cùng `top`, nhãn không xuống dòng; trang không cuộn ngang.
  - Kỳ Tuỳ chọn chưa đủ 2 ngày → KHÔNG có request (`browser_network_requests`).
  - Tài khoản KHÔNG quyền (`e2e_cmd_noperm@test.local`, theo memory e2e-env-ghim-cong-va-tai-khoan-noperm): ô Công ty khoá, chỉ thấy dòng
    của chính mình; tài khoản 1180 (có 1057): ô Công ty mở.
  - Chụp màn so `mockup.html` cùng kích thước 1366 × 900.

- [x] **Step 6: Commit (hrm-client)**

```bash
git add pages/assign/report/meeting-by-employees
git commit -m "Báo cáo meeting theo nhân viên: khung màn mới — bộ lọc Kỳ, khối tổng hợp, cây Công ty ▸ Phòng ▸ Nhân viên ▸ Meeting"
```

---

### Task 8: FE — popup meeting / người tham gia / nhân viên, panel meeting, biên bản, In (chọn cột) / Excel

**Files:**
- Create: `components/MeetingListModal.vue`, `components/ParticipantListModal.vue`, `components/EmployeeListModal.vue`, `components/PrintOptionsModal.vue`
- Modify: `index.vue`

**Interfaces:**
- Consumes: `/item-list` (+ `employees[].in_scope`, `meta.minutes`), `/participant-list`, `/employee-list`, `/print-list-data`, 4 route Excel; emit Task 7.
- Produces: `PrintOptionsModal` emit `print({ mode: 'summary'|'detail', columns: string[] })`.

- [x] **Step 1: `MeetingListModal.vue`** — copy `$S/components/MeetingListModal.vue`, đổi:
  - `COLUMNS` theo mockup k: STT · Meeting (mã link + tên) · Thời gian · Thời lượng (phút) · Trạng thái (badge) · Loại · Hình thức ·
    Nhân viên tham gia (công ty) · Dự án · Khách hàng. Ô NV tham gia: nối tên bằng ", ", `in_scope` bọc `<b>`; `:title` đủ.
  - `FILTER_FIELDS`: Trạng thái (`status`: 2/3/4), Loại (`meeting_type_id`), Hình thức (`mode_id`, có "Chưa xác định" = 0). Ô đã bị ô số
    cố định (`fixed`) thì ẩn. Ô tìm khớp BE `q` (mã/tên meeting, KH, dự án).
  - `metaText`: `N meeting · {meta.minutes} phút họp · Kỳ …`. Dòng chú thích xám dưới bảng (mockup k): "Tên in đậm: nhân viên thuộc phạm vi
    đang xem. Thời lượng ở đây là phút họp của từng meeting (mỗi meeting tính 1 lần), khác tổng phút-người ở báo cáo."
  - Footer In / Xuất Excel danh sách / Đóng (giữ của nền).
- [x] **Step 2: `ParticipantListModal.vue`** — copy nguyên `$S/components/ParticipantListModal.vue` (cột Phía + ô lọc Phía, tìm gửi `pq`).
- [x] **Step 3: `EmployeeListModal.vue`** — copy `ParticipantListModal.vue` làm vỏ, cột (#13): STT · Nhân viên (tên + mã `.code-sub`) · Công ty ·
  Phòng ban · Chức vụ · Số meeting · Thời lượng (phút) (2 cột số căn phải `num()`); ô lọc Phòng ban (từ chính `rows`, lọc tại chỗ) + ô tìm
  tên/mã (tại chỗ). `metaText`: `N nhân viên · {Σ duration} phút-người · Kỳ …`. Footer In / Excel / Đóng; `own` gửi BE =
  `{ department_id?, eq? }` (BE `employeeRows` hiểu cả 2). Tương tự `own` của popup meeting = `{ status?, meeting_type_id?, mode_id?, q? }`,
  popup người = `{ side?, pq? }`.
- [x] **Step 4: `PrintOptionsModal.vue`** — copy `$S/components/PrintOptionsModal.vue` (tiền tố `mbe-`, id `mbe-print-options-modal`), thêm khối
  "Chọn cột in" NGAY DƯỚI 2 lựa chọn (mockup l): tiêu đề + checkbox "Chọn tất cả" (`indeterminate` khi chọn 1 phần) · 11 ô tick 2 cột trong
  `.column-list` (khoá = `PRINT_COLUMNS` BE: pos, cnt, st, time, dur, type, people, proj, kh, content, minutes) · ghi chú "Cột chọn ở đây áp cho
  **cả 2 bản in**. Cột **STT** và **Công ty / Phòng / Nhân viên / Meeting** luôn được in." · bỏ hết rồi bấm In → `.text-danger` "Vui lòng chọn ít
  nhất 1 cột để in", KHÔNG đóng popup. Mở lại = chọn hết. Mô tả 2 bản theo mockup. CSS khối cột: lấy NGUYÊN VĂN `<style id="mk-extra-css">`
  phần `.mbe-print-cols` / `.column-list` / `.fixed-columns-note` trong `mockup.html` (đã port từ `MeetingByEmployeesPrintConfigModal.vue` cũ). Checkbox
  bấm vào NHÃN (memory hrm-client-radio-label-lech-nua-dong).
- [x] **Step 5: Nối vào `index.vue`** (khuôn `onDrill` / `fetchDrill` / `onDrillPeople` / `drillBaseParams` / `downloadExcel` của nền):
  - `onDrill(filter)` → `MeetingListModal` (lặp trang 500 `item-list`); `onDrillPeople(filter)` → `ParticipantListModal`;
    `onDrillEmployees(filter)` → `EmployeeListModal` (`employee-list`, `employeesSeq` riêng).
  - `cleanParams` GIỮ số 0 (nhóm chưa xác định, `scope_department_id=0`).
  - `onOpenMeeting(row)` → `MeetingDetailDrawer` `header-gradient="linear-gradient(135deg, #0a1c3d, #06b6d4)"`,
    `:above-modal="drill.visible || people.visible || employees.visible"`. `onOpenMinutes(row)` → `loadPrintPreview('assign/meeting/' + id + '/print', 'Xem biên bản cuộc họp', false)`.
  - `onPrintReport({ mode, columns })` → `openPrintList(API, { ...drillBaseParams(), mode, columns: columns.join(',') }, …)`.
  - Footer popup: In → `openPrintList(API, { ...params, ...own, mode: 'meetings' | 'participants' | 'employees', scope_label: title })`;
    Excel → `item-list/export` / `participant-list/export` / `employee-list/export` kèm `scope_label`.
- [x] **Step 6: Playwright MCP (đo)**
  - Bấm "Đã hủy" ở 1 dòng Phòng → số dòng popup = số đã bấm; bấm Số meeting dòng NV → = `totals.meetings` của NV.
  - Popup meeting: đếm `<b>` trong ô NV tham gia = số NV in_scope (so response); có NV công ty khác (nếu dữ liệu có) ở chữ thường.
  - Bấm Nhân viên ở khối tổng hợp → số dòng popup = ô Nhân viên; Σ cột Thời lượng = ô Tổng thời lượng.
  - Bấm Người tham gia ở dòng TỔNG → số dòng = `summary.participants`.
  - Mở panel meeting từ trong popup: panel nằm trên popup (`z-index` / `getBoundingClientRect`); tài khoản chỉ có 1058 mở được meeting
    mình không tham gia (không 403 — memory toast 403 interceptor).
  - In: bỏ tick "Nội dung" → bản xem trước không có cột Nội dung (đếm `th`) ở CẢ 2 bản; bỏ hết → hiện lỗi, popup còn mở.
  - Excel 4 nút tải được, tên file đúng. Console sạch.
- [x] **Step 7: Commit** `git commit -m "Báo cáo meeting theo nhân viên: popup meeting / người tham gia / nhân viên, panel meeting, biên bản, In chọn cột / Excel"`

---

### Task 9: Chuyển route chính + dọn bản cũ

**Files:**
- Modify (api): `Modules/Assign/Routes/api.php` — đổi 10 route `-v2` về `/meeting-by-employees…`, xoá 6 route cũ (dòng ~1197–1202).
  `ReportController.php`: xoá 6 method + thuộc tính / tham số constructor `meetingByEmployeesService` + import `MeetingByEmployeesExport`,
  `MeetingByEmployeesService`, `MeetingByEmployeesResource`, `MeetingByStatusResource`, `ParticipantsByScopeResource`, `ChartDataResource`,
  `ChartDataByEmployeesResource` (và `MeetingProject`, `ProjectPhases` nếu grep thấy không còn dùng — minor của báo cáo 1).
  Xoá file: `Services/Report/MeetingByEmployeesService.php`, 5 Transformer, `app/ExcelExport/MeetingByEmployeesExport.php`,
  `resources/views/exports/meeting_by_employees_report.blade.php`.
- Modify (client): `api.js` → `'assign/report/meeting-by-employees'`. Xoá `print.vue` + 8 component cũ. Sửa 2 comment.
- Modify tests: `URL` → `/api/v1/assign/report/meeting-by-employees` (4 file).

- [x] **Step 1: Grep trước khi xoá (cả 2 repo)**

```bash
cd $W/hrm-api && git grep -n "MeetingByEmployeesService\|MeetingByEmployeesResource\|MeetingByEmployeesExport\|meeting_by_employees_report\|ChartDataByEmployeesResource\|MeetingByStatusResource\|ParticipantsByScopeResource\|ChartDataResource\|ByEmployees(" -- Modules app routes resources tests | grep -v "MeetingByEmployeesReport"
cd $W/hrm-client && git grep -n "TopDepartmentsChart\|MeetingByEmployeesTable\|MeetingByEmployeesPrintConfigModal\|meeting-by-employees/print\|meeting-by-employees/chart-data\|meeting-by-employees/meetings-by\|participants-by-scope" -- pages components utils layouts plugins store
```
Expected: chỉ còn chỗ thuộc chính màn này / 2 comment đã biết (`BaseMeetingChart.vue:132`, `CareTrackingTable.vue:25`). Gặp chỗ GỌI thật
khác thì DỪNG hỏi user.

- [x] **Step 2: Xoá + đổi route + sửa comment**
  - `BaseMeetingChart.vue:132`: đổi ví dụ `api-endpoint="assign/report/<báo cáo>/chart-data"` (không còn route nào cụ thể).
  - `CareTrackingTable.vue:25`: "Khuôn gốc: … (đã gỡ 10/2026, xem pages/assign/report/meeting-by-employees/components/MeetingTree.vue)".

- [x] **Step 3: Chạy lại toàn bộ test BE liên quan**

Run: `vendor/bin/phpunit tests/Feature/MeetingByEmployees && vendor/bin/phpunit --filter "MeetingByProjects|MeetingByMarket|CanView|ServiceDemand|PotentialCustomerTracking"`
Expected: PASS hết. Đếm route bằng `grep -c "meeting-by-employees" Modules/Assign/Routes/api.php` = 10 (route:list crash có sẵn trên gop_db —
ledger báo cáo 1).

- [x] **Step 4: FE build kiểm import**: restart nuxt cổng 3019 (kill đúng PID theo cổng, `rm -rf .nuxt/components`), mở màn, console không có
  "Can't resolve"; mở thêm `/assign/report/meeting-by-projects`, `/assign/report/potential-customer-care`, `/assign/report/solutions-work-summary-by-department`
  (dùng `_meeting-reports.scss`) → vẫn chạy.

- [x] **Step 5: Commit 2 repo**

```bash
git commit -am "Báo cáo meeting theo nhân viên: chuyển sang API mới, gỡ endpoint / component cũ (biểu đồ Top phòng ban, 4 popup, print.vue)"
```

---

### Task 10: e2e spec + đóng gói

**Files:**
- Create: `HRM/e2e/tests/assign/meeting-by-employees.api.spec.ts`, `meeting-by-employees.spec.ts` (khuôn `meeting-by-projects{.api,}.spec.ts`;
  thư mục e2e KHÔNG thuộc git). Cổng mặc định trong spec 8019/3019, comment bắt buộc truyền `API_BASE`/`BASE_URL`.

- [x] **Step 1: Spec API** (fixture SQL tự dọn, ngày 15/03/2001 như PHPUnit; cấp quyền bằng role tạm + xoá cache — memory e2e-cap-quyen-sql-phai-xoa-cache):
  1. Không quyền: chỉ dòng của chính mình; 1058: không thấy NV công ty khác, `company_id` lạ bị bỏ qua; 1057: thấy mọi công ty, `can_change_company`.
  2. Khớp số: `summary.meetings = item-list.meta.total`, `summary.employees = employee-list.meta.total`, Σ by_status = meetings.
  3. Phút-người: Σ thời lượng phòng = công ty = summary.duration; Hủy 0 phút.
  4. Phân trang theo NV: `per_page=1` trang 2 có dòng Công ty/Phòng với totals bằng trang 1.
  5. `period=custom` thiếu ngày → 422 ở mọi endpoint.
  6. Drill `mode_id=0` / `meeting_type_id=0` = by_mode[0] / by_type id 0; Excel `mode_id=0` → 200 xlsx.
  7. `in_scope`: meeting có NV công ty khác, user 1058 → cờ false đúng NV đó.
  8. `print-list-data` 5 chế độ + `columns=st` ẩn cột Nội dung.
- [x] **Step 2: Spec UI**: đo khuôn (`th` sticky, thụt d0..d3, nền TỔNG, 2 thanh cuộn, `min-width` 2614); tổng hợp = TỔNG = số dòng popup; đổi
  cấp; Kỳ Tuỳ chọn; trang 2 lặp dòng cha; popup NV; In bỏ cột; panel meeting trên popup; tài khoản không quyền ô Công ty khoá. Chờ theo
  `waitForResponse`, KHÔNG `networkidle`; nút `V2BaseButton` bấm theo `title`/locator chuẩn hoá khoảng trắng (memory).
- [x] **Step 3: KHÔNG tự chạy.** Báo user, hỏi có chạy không. Nếu chạy: `--workers=1`, truyền env cổng 8019/3019, đọc DÒNG TỔNG KẾT (serial:
  ca fail làm các ca sau "did not run").
- [x] **Step 4: Tài liệu**: `design.md` (trạng thái), `../design.md` bảng theo dõi dòng 2, `.plans/gop-db/STATUS.md` (soát marker xung đột).
- [x] **Step 5: Hỏi user** push nhánh `gop_db-update-style-meeting-by-employees` 2 repo và có merge `gop_db` không (lệnh riêng).

---

## Câu hỏi tồn — ĐÃ CHỐT 05/10/2026: Q1–Q4 đều theo phương án A (design.md #16–#19), plan giữ nguyên

1. **Q1 — Nguồn Khách hàng (R1).** DB local: 787/856 meeting có `customer_id` riêng, chỉ 86 meeting gắn dự án. Quyết định #2 ghi "ô Dự án/KH
   trống" khi không gắn dự án, nhưng mockup đã duyệt lại hiện KH cho meeting không gắn dự án (MT-2026-00380 Ford, MT-2026-00360 Toyota).
   - (A — ruling tạm) Cột KH + lọc KH theo KH của MEETING (thiếu thì lấy KH dự án) → lọc KH ra cả meeting không gắn dự án.
   - (B) Chỉ theo KH của DỰ ÁN → ~700 meeting có KH vẫn hiện ô KH trống, lọc KH bỏ sót chúng.
2. **Q2 — Xuất Excel (R7).** (A — ruling tạm) Excel chính = cây đủ 13 cột, không chọn bản/cột (như báo cáo 1). (B) Excel cũng có popup chọn
   Tổng hợp/Chi tiết + tick cột như In → thêm `mode`/`columns` vào `/export` + 1 Excel bản Chi tiết (thêm ~1 file export + test).
3. **Q3 — Danh mục ô Phòng ban / Bộ phận / Nhân viên (R3).** (A — ruling tạm) chỉ đơn vị/NV CÓ meeting trong kỳ (trong quyền) → danh sách
   ngắn, đổi kỳ thì danh mục đổi. (B) mọi phòng/bộ phận/NV trong quyền (như ô cũ `V2BaseCompanyDepartmentFilter`) → chọn NV không họp sẽ ra
   báo cáo rỗng; NV đã nghỉ có meeting cũ vẫn cần hiện thì phải gồm cả NV nghỉ việc.
4. **Q4 — Quyền "theo phòng ban" 1059 (R10).** Giữ đúng bản cũ: chỉ NV thuộc phòng/bộ phận mình QUẢN LÝ — trưởng phòng không thuộc phòng
   mình quản lý (ít gặp) sẽ không thấy chính mình. (A — ruling tạm) giữ; (B) cộng thêm dòng của chính mình.

Điểm đã tự chốt khác (không hỏi, ghi để user biết): R2 meeting thiếu giờ bắt đầu không vào kỳ (local 0) · R4 cờ in đậm theo phạm vi báo cáo,
không theo dòng bấm · R5 ô Dự án = dự án gắn đầu tiên + "+n" · R6 thứ tự cây (meeting trong NV theo thời gian tăng dần, bản cũ giảm dần) ·
R8 bản in Chi tiết: Chức vụ = "chức vụ · vai trò", không in cột Số meeting · R9 NV đã nghỉ vẫn hiện nếu có meeting trong kỳ.
Ngoài luồng (note, không vá): 5 dòng `meeting_employees.type='company'` (meeting 858–862, fixture e2e cũ của NV 1180).

## Phạm vi code (để hỏi "làm")

- **hrm-api** · nhánh `gop_db-update-style-meeting-by-employees` (từ `origin/gop_db`) · worktree `websites/wt-update-style-mbe/hrm-api` ·
  tạo 1 service + 1 print service + 1 controller + 3 Export + 7 blade + 5 file test; sửa `Routes/api.php`, `Meeting.php`; xoá 1 service cũ,
  5 Transformer, 1 Export + 1 blade cũ, 6 method `ReportController`. **Không migration, không seeder, không quyền mới.** PHPUnit chạy trên
  DB local `hrm_erp` (fixture tự tạo/dọn: meetings, meeting_employees, ppm, prospective_projects, roles tạm, employee_manage_departments).
- **hrm-client** · cùng tên nhánh · worktree `websites/wt-update-style-mbe/hrm-client` · viết lại `index.vue` + 10 file mới trong
  `pages/assign/report/meeting-by-employees/`; xoá `print.vue` + 8 component cũ; sửa 2 comment.
- **e2e** (ngoài git): 2 spec, chỉ viết.

### Checkpoint — 2026-10-05 (wrap up)
Vừa hoàn thành: Task 1–10 (SDD, review từng task + final review sạch) → ĐÃ MERGE gop_db (api 9696baa26, client 6c0b509de). Bổ sung cùng
ngày: ô lọc Trạng thái (Hoàn thành / Đã hủy) + cột Loại thành "n loại" + popup theo loại × trạng thái + NV tham gia thành số + popup NV
(phòng ban · chức vụ · vai trò) → ĐÃ MERGE gop_db (api 60aa9bfa0, client 81b715269). Chi tiết: `bo-sung-loai-va-nv-tham-gia.md`, sổ `sdd-ledger.md`.
Đang làm dở: không.
Bước tiếp theo: chạy e2e `e2e/tests/assign/meeting-by-employees{.api,}.spec.ts` (14 ca UI + 10 ca API, `--workers=1`, API_BASE 8019 / BASE_URL 3019)
khi user yêu cầu; kiểm trên staging: logo Excel/in, tài khoản chỉ 1058 mở chi tiết meeting, cột Chốt lịch của popup theo loại. Sau đó chọn báo cáo cũ thứ 3.
Blocked: 
