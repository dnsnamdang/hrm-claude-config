# Update style — Báo cáo thời gian meeting theo dự án · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
> **REQUIRED skill khi code FE:** `report-styles` (HRM/.claude/skills/report-styles) — copy từ `template/`, không tự viết CSS.

**Goal:** Viết lại `/assign/report/meeting-by-projects` theo khuôn report-styles và sửa 3 lỗi số liệu của bản cũ:
phân trang cắt ngang dự án, tính cả meeting ngoài bộ lọc, đếm lượt khách hàng thay vì đếm người.

**Architecture:**
- **BE:** controller + service mới, chỉ đọc. Mọi con số tính từ MỘT tập meeting M (1 truy vấn join `ppm ⨝ meetings ⨝
  prospective_projects`). Gom dự án và phân trang theo dự án làm trong PHP.
- **FE:** copy `template/` của skill, đổi tiền tố `pct-` → `mbp-`, sửa cây 4 cấp thành 2 cấp.
- **Dọn dẹp:** gỡ endpoint / component cũ sau khi grep cả 2 repo.

**Tech Stack:** Laravel (PHP 7.4, `php@7.4`), Maatwebsite Excel, Nuxt 2 / Vue 2 (node 12, heap 8192), PHPUnit trên DB local
`hrm_erp`, Playwright MCP.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-04-update-style-bao-cao-meeting-theo-du-an-design.md`
**Mockup đã duyệt:** `./mockup.html` · **Design tóm tắt:** `./design.md` (10 quyết định)

## Global Constraints

- Nhánh `gop_db-update-style-meeting-by-projects` tách từ `origin/gop_db` (cả 2 repo), làm trong worktree
  `websites/wt-update-style-mbp/{hrm-api,hrm-client}`. Xong thì chỉ push nhánh feature; merge vào `gop_db` phải được
  user cho phép riêng.
- KHÔNG migration, KHÔNG seeder, KHÔNG quyền mới. Quyền giữ nguyên: 1060 "Xem báo cáo meeting theo dự án theo tổng công
  ty", 1061 "Xem báo cáo meeting theo dự án theo công ty". Không bypass super admin.
- KHÔNG dùng `mysql2`. Meeting tính khi `status IN Meeting::REPORT_STATUSES` (2, 3). Dự án có `status != 1` (Đang tạo).
- Kỳ: `period` = week | month | year (mặc định) | last_year | custom (+ `from`, `to` d/m/Y; thiếu hoặc from > to → 422).
- Số FE format `en-US` (`num()` trong `format.js`); ngày `dd/mm/yyyy`. Trạng thái do BE trả `status_text` + `status_color`.
- Excel tải bằng link `?token=`, không dùng blob. In qua `ReportPrintPreviewModal`, không mở tab `/print`.
- KHÔNG `git stash` (repo dùng chung). Mỗi commit kèm 2 dòng attribution của phiên.
- Chạy e2e chỉ khi user yêu cầu, `--workers=1`.

## Review Focus

1. Dự án có meeting khớp lẫn meeting không khớp (Hủy, ngoài kỳ, khác loại) → chỉ meeting khớp được hiện / đếm, kể cả ô
   "Người tham gia" và "Thời lượng" (Task 2: `test_chi_tinh_meeting_khop_bo_loc`).
2. Người tham gia phía KH gõ khác nhau ("Anh  Minh" / "anh minh", "0912 345 678" / "0912345678") → 1 người. Dòng rỗng
   cả tên lẫn SĐT KHÔNG bị gộp với nhau (Task 3: `test_gop_nguoi_tham_gia_khach_hang`).
3. User chỉ có 1061 lọc `company_id` của công ty khác qua URL → BE bỏ qua, vẫn chỉ ra công ty mình (Task 2:
   `test_quyen_cong_ty_bo_qua_company_id_la`).
4. Tuần chứa giao năm, hoặc `period=custom` đúng 1 ngày → meeting cùng ngày (giờ 23:30) vẫn được tính (Task 2:
   `test_ky_custom_mot_ngay_tinh_ca_gio_cuoi_ngay`).
5. Popup mở từ dòng TỔNG khi đang lọc loại / hình thức → số dòng popup = số ở ô đã bấm (Task 3:
   `test_item_list_khop_so_o_bam`).

---

## File map

**hrm-api (tạo mới)**
- `Modules/Assign/Services/Report/MeetingByProjectsReportService.php`: kỳ, tập M, quyền, `index`, `itemList`,
  `participantList`, `filterOptions`, `meetingRows`, `participantRows`.
- `Modules/Assign/Services/Report/MeetingByProjectsPrintService.php`: bản in summary / detail / participants.
- `Modules/Assign/Http/Controllers/Api/V1/MeetingByProjectsReportController.php`
- `Modules/Assign/Export/MeetingByProjectsReportExport.php` (cây) · `MeetingByProjectsListExport.php` (meeting) ·
  `MeetingByProjectsParticipantExport.php`
- `resources/views/exports/assign/meeting_by_projects_{report,list,participants}.blade.php`
- `resources/views/prints/assign/meeting_by_projects_{summary,detail,participants}.blade.php`
- `tests/Feature/MeetingByProjects/{MeetingFixture.php,ReportApiTest.php,ExportPrintTest.php,MeetingCanViewTest.php}`

**hrm-api (sửa / xoá)**
- Sửa: `Modules/Assign/Routes/api.php` (thay 7 route cũ dòng ~1194–1200), `Modules/Assign/Entities/Meeting/Meeting.php` (`canView`).
- Xoá ở Task 9: `Services/Report/MeetingByProjectsService.php`, 7 method `meetingByProjects*` / `getMeetingsBy*` /
  `getParticipantsByScope` / `getChartData` trong `ReportController.php`, `Transformers/MeetingResource/MeetingByProjectsResource.php`,
  `app/ExcelExport/MeetingByProjectsExport.php`.

**hrm-client (`pages/assign/report/meeting-by-projects/`)**
- Viết lại: `index.vue`. Tạo: `api.js`, `format.js`, `components/{MeetingSummary,MeetingTree,MeetingListModal,ParticipantListModal,PrintOptionsModal,DrillNum,InfoTip}.vue`.
- Xoá ở Task 9: `print.vue`, `components/{MeetingByProjectsTable,MeetingsByStatusModal,MeetingsByModeModal,MeetingsByTypeModal,ParticipantModal,ParticipantsByScopeModal,ProjectStatusModal,TypeModeModal}.vue`, `components/TopProjectsChart.vue`.
- e2e: `HRM/e2e/tests/assign/meeting-by-projects.api.spec.ts`, `meeting-by-projects.spec.ts`.

---

### Task 1: Dựng worktree 2 repo

**Files:** không có file code.

- [ ] **Step 1: Tạo nhánh + worktree**

```bash
cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-api && git fetch origin gop_db
git worktree add -b gop_db-update-style-meeting-by-projects ../../../wt-update-style-mbp/hrm-api origin/gop_db
cd ../hrm-client && git fetch origin gop_db
git worktree add -b gop_db-update-style-meeting-by-projects ../../../wt-update-style-mbp/hrm-client origin/gop_db
```

- [ ] **Step 2: Copy (KHÔNG symlink) vendor / node_modules + .env**

```bash
W=/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-update-style-mbp
M=/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM
cp -Rc $M/hrm-api/vendor $W/hrm-api/vendor && cp $M/hrm-api/.env $W/hrm-api/.env
cp -Rc $M/hrm-client/node_modules $W/hrm-client/node_modules && cp $M/hrm-client/.env $W/hrm-client/.env
cd $W/hrm-api && composer dump-autoload -q && php artisan config:clear
php -r 'require "vendor/autoload.php"; echo (new ReflectionClass("Modules\\Assign\\Entities\\Meeting\\Meeting"))->getFileName(), PHP_EOL;'
```
Expected: đường dẫn in ra chứa `wt-update-style-mbp/hrm-api`. Ra checkout chính thì dừng lại sửa trước.

- [ ] **Step 3: Server cổng riêng**

```bash
cd $W/hrm-api && php artisan serve --port 8018   # background, ghi PID
cd $W/hrm-client && API_URL=http://127.0.0.1:8018 NODE_OPTIONS=--max-old-space-size=8192 npx nuxt --port 3018 --hostname 127.0.0.1  # node 12, background
```
Mở `http://127.0.0.1:3018/assign/report/meeting-by-projects`, màn cũ phải chạy được (mốc so sánh). Kiểm biến trỏ API
trong `.env` của client. Nếu không đọc `API_URL` thì sửa `.env` của worktree, KHÔNG sửa của checkout chính.

---

### Task 2: Service: kỳ, tập meeting M, quyền, `index` (summary + cây + phân trang theo dự án)

**Files:**
- Create: `Modules/Assign/Services/Report/MeetingByProjectsReportService.php`
- Create: `tests/Feature/MeetingByProjects/MeetingFixture.php`, `tests/Feature/MeetingByProjects/ReportApiTest.php`
- Create: `Modules/Assign/Http/Controllers/Api/V1/MeetingByProjectsReportController.php` (chỉ `index`)
- Modify: `Modules/Assign/Routes/api.php`: thêm `Route::get('/meeting-by-projects-v2', …)` TẠM, để route cũ vẫn chạy
  cho FE cũ tới Task 9 (Task 9 đổi về `/meeting-by-projects`).

**Interfaces:**
- Produces:
  - `period(Request): array [Carbon $from, Carbon $to, string $label]`
  - `meetingQuery(Request $r, array $skip = []): \Illuminate\Database\Query\Builder`: 1 dòng = (p, m), đã áp kỳ +
    trạng thái + bộ lọc + quyền, CHƯA select.
  - `meetingRows(Request $r, array $extra = []): Collection<array>`: dòng phẳng đã chuẩn hoá (khoá ở Step 3).
  - `index(Request $r, bool $all = false): array{summary, groups, meta}`
  - Hằng `PERM_ALL`, `PERM_COMPANY`, `MODES = [1 => 'Trực tiếp', 2 => 'Online']`.

- [ ] **Step 1: Fixture**

```php
<?php

namespace Tests\Feature\MeetingByProjects;

use App\Models\TpEmployee;
use App\Support\RequestCache;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\ProspectiveProject;

/**
 * Dữ liệu test báo cáo meeting theo dự án trên DB local thật (khuôn tests/Feature/PotentialCustomerTracking).
 * Khách hàng test = khách CHƯA có meeting / dự án → lọc customer_id là cô lập khỏi dữ liệu thật.
 */
trait MeetingFixture
{
    protected $fxMeetingIds = [];
    protected $fxProjectIds = [];
    protected $fxRoleIds = [];

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
            'code' => 'PHPUNIT-MBP-' . uniqid(), 'name' => 'PHPUnit dự án ' . uniqid(), 'customer_id' => $customerId,
            'status' => 4, 'created_by' => $creatorId, 'main_sale_employee_id' => $creatorId, 'company_id' => 1, 'parent_id' => null,
        ], $attrs));
        $p->saveQuietly();
        $this->fxProjectIds[] = $p->id;

        return $p->fresh();
    }

    /** Meeting gắn dự án; $members = [['type'=>1,'employee_id'=>27], ['type'=>2,'name'=>'Anh Minh','phone'=>'0912345678']] */
    protected function makeMeeting(ProspectiveProject $p, array $attrs = [], array $members = []): Meeting
    {
        $m = Meeting::orderByDesc('id')->firstOrFail()->replicate();
        $m->code = 'PHPUNIT-MBP-' . uniqid();
        $m->forceFill(array_merge([
            'customer_id' => $p->customer_id, 'status' => Meeting::HOAN_THANH, 'mode_id' => 1,
            'start_date' => now()->startOfYear()->addDays(10)->setTime(9, 0)->format('Y-m-d H:i:s'),
            'end_date' => now()->startOfYear()->addDays(10)->setTime(10, 30)->format('Y-m-d H:i:s'),
        ], $attrs));
        $m->saveQuietly();
        $this->fxMeetingIds[] = $m->id;
        DB::table('prospective_project_meetings')->insert([
            'prospective_project_id' => $p->id, 'meeting_id' => $m->id, 'meeting_code' => $m->code,
            'meeting_name' => $m->name ?: 'PHPUnit', 'created_at' => now(), 'updated_at' => now(),
        ]);
        foreach ($members as $i => $mb) {
            DB::table('meeting_employees')->insert(array_merge(['meeting_id' => $m->id, 'sort_order' => $i, 'created_at' => now(), 'updated_at' => now()], $mb));
        }

        return $m->fresh();
    }

    /** Cấp quyền qua ROLE tạm (isCurrentEmployeeHasPermission chỉ đọc quyền qua role) + xoá cache spatie */
    protected function grant(int $empId, int $permissionId): void
    {
        $companyId = (int) DB::table('employee_infos')->where('id', DB::table('employees')->where('id', $empId)->value('employee_info_id'))->value('company_id');
        $roleId = DB::table('roles')->insertGetId(['name' => 'PHPUNIT-MBP-' . uniqid(), 'guard_name' => 'api', 'status' => 1, 'company_id' => $companyId]);
        $this->fxRoleIds[] = $roleId;
        DB::table('employee_has_roles')->insert(['role_id' => $roleId, 'model_type' => 'Modules\Timesheet\Entities\Employee', 'employee_id' => $empId, 'position' => 0, 'company_id' => $companyId]);
        DB::table('role_has_permissions')->insert(['permission_id' => $permissionId, 'role_id' => $roleId, 'company_id' => $companyId]);
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
        DB::table('meeting_employees')->whereIn('meeting_id', $this->fxMeetingIds)->delete();
        DB::table('prospective_project_meetings')->whereIn('meeting_id', $this->fxMeetingIds)->delete();
        Meeting::whereIn('id', $this->fxMeetingIds)->delete();
        ProspectiveProject::whereIn('id', $this->fxProjectIds)->delete();
        $this->fxMeetingIds = $this->fxProjectIds = $this->fxRoleIds = [];
        Artisan::call('cache:clear');
        RequestCache::flush();
    }
}
```

- [ ] **Step 2: Viết test fail**

```php
<?php

namespace Tests\Feature\MeetingByProjects;

use Modules\Assign\Entities\Meeting\Meeting;
use Tests\TestCase;

/** Actor (DB local, công ty 1, không có 1060/1061): A = 27 · B = 1180 · VIEWER = 28. Công ty khác: 2. */
class ReportApiTest extends TestCase
{
    use MeetingFixture;

    private const A = 27;
    private const B = 1180;
    private const VIEWER = 28;
    private const PERM_ALL = 1060;
    private const PERM_COMPANY = 1061;
    private const URL = '/api/v1/assign/report/meeting-by-projects-v2';

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

    public function test_chi_tinh_meeting_khop_bo_loc(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $ok = $this->makeMeeting($p, ['meeting_type_id' => 2, 'mode_id' => 1], [['type' => 1, 'employee_id' => self::A]]);
        $this->makeMeeting($p, ['status' => Meeting::HUY], [['type' => 1, 'employee_id' => self::B]]);
        $this->makeMeeting($p, ['status' => Meeting::LEN_LICH]);
        $this->makeMeeting($p, ['start_date' => now()->subYear()->format('Y-m-d 09:00:00'), 'end_date' => now()->subYear()->format('Y-m-d 10:00:00')]);
        $this->makeMeeting($p, ['meeting_type_id' => 1]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', ['customer_id' => $cus, 'meeting_type_id' => 2])->assertOk()->json('data');
        $this->assertSame(1, $d['summary']['meetings']);
        $this->assertSame(90, $d['summary']['duration']);
        $this->assertSame(1, $d['summary']['participants']);
        $this->assertCount(1, $d['groups']);
        $this->assertSame([$ok->id], array_column($d['groups'][0]['meetings'], 'id'));
    }

    public function test_phan_trang_theo_du_an_khong_cat_ngang(): void
    {
        [$cus] = $this->freshCustomers();
        $p1 = $this->makeProject(self::A, $cus);
        $p2 = $this->makeProject(self::A, $cus);
        foreach ([1, 2, 3] as $i) {
            $this->makeMeeting($p1);
        }
        $this->makeMeeting($p2);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $page1 = $this->api(self::VIEWER, '', ['customer_id' => $cus, 'per_page' => 1, 'page' => 1])->assertOk()->json('data');
        $this->assertSame(2, $page1['meta']['total']);
        $this->assertCount(1, $page1['groups']);
        $first = $page1['groups'][0];
        $this->assertCount($first['totals']['meetings'], $first['meetings']);
        $this->assertSame(4, $page1['summary']['meetings']);
    }

    public function test_summary_bang_tong_cac_dong_du_an(): void
    {
        [$cus] = $this->freshCustomers();
        foreach ([2, 1] as $n) {
            $p = $this->makeProject(self::A, $cus);
            for ($i = 0; $i < $n; $i++) {
                $this->makeMeeting($p, ['mode_id' => $i ? 2 : 1, 'status' => $i ? Meeting::CHOT_LICH : Meeting::HOAN_THANH]);
            }
        }
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', ['customer_id' => $cus])->assertOk()->json('data');
        $sum = function ($k) use ($d) {
            return array_sum(array_map(function ($g) use ($k) { return $g['totals'][$k]; }, $d['groups']));
        };
        $this->assertSame($d['summary']['meetings'], $sum('meetings'));
        $this->assertSame($d['summary']['duration'], $sum('duration'));
        $this->assertSame(['2' => 1, '3' => 2], $d['summary']['by_status']);
        $this->assertSame(['1' => 2, '2' => 1], $d['summary']['by_mode']);
        $this->assertSame(2, $d['summary']['projects']);
        $this->assertSame(1, $d['summary']['customers']);
    }

    public function test_khong_quyen_chi_thay_du_an_minh_tao_hoac_la_nvkd(): void
    {
        [$cus] = $this->freshCustomers();
        $mine = $this->makeProject(self::VIEWER, $cus, ['main_sale_employee_id' => self::A]);
        $sale = $this->makeProject(self::A, $cus, ['main_sale_employee_id' => self::VIEWER]);
        $other = $this->makeProject(self::A, $cus, ['main_sale_employee_id' => self::A]);
        foreach ([$mine, $sale, $other] as $p) {
            $this->makeMeeting($p);
        }

        $ids = array_column($this->api(self::VIEWER, '', ['customer_id' => $cus])->assertOk()->json('data.groups'), 'project_id');
        sort($ids);
        $expect = [$mine->id, $sale->id];
        sort($expect);
        $this->assertSame($expect, $ids);
        $this->assertFalse($this->api(self::VIEWER, '/filter-options')->json('data.can_change_company'));
    }

    public function test_quyen_cong_ty_bo_qua_company_id_la(): void
    {
        [$cus] = $this->freshCustomers();
        $own = $this->makeProject(self::A, $cus, ['company_id' => 1]);
        $foreign = $this->makeProject(self::A, $cus, ['company_id' => 2]);
        $this->makeMeeting($own);
        $this->makeMeeting($foreign);
        $this->grant(self::VIEWER, self::PERM_COMPANY);

        $ids = array_column($this->api(self::VIEWER, '', ['customer_id' => $cus, 'company_id' => 2])->assertOk()->json('data.groups'), 'project_id');
        $this->assertSame([$own->id], $ids);
    }

    public function test_quyen_tong_cong_ty_thay_moi_cong_ty_va_mo_o_cong_ty(): void
    {
        [$cus] = $this->freshCustomers();
        $this->makeMeeting($this->makeProject(self::A, $cus, ['company_id' => 2]));
        $this->grant(self::VIEWER, self::PERM_ALL);

        $this->assertCount(1, $this->api(self::VIEWER, '', ['customer_id' => $cus])->json('data.groups'));
        $this->assertTrue($this->api(self::VIEWER, '/filter-options')->json('data.can_change_company'));
    }

    public function test_ky_custom_mot_ngay_tinh_ca_gio_cuoi_ngay(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $this->makeMeeting($p, ['start_date' => '2026-03-15 23:30:00', 'end_date' => '2026-03-15 23:50:00']);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $d = $this->api(self::VIEWER, '', ['customer_id' => $cus, 'period' => 'custom', 'from' => '15/03/2026', 'to' => '15/03/2026'])->assertOk()->json('data');
        $this->assertSame(1, $d['summary']['meetings']);
        $this->api(self::VIEWER, '', ['period' => 'custom', 'from' => '15/03/2026'])->assertStatus(422);
    }
}
```

- [ ] **Step 3: Chạy test, phải FAIL (404 route)**

Run: `cd $W/hrm-api && php artisan config:clear && vendor/bin/phpunit tests/Feature/MeetingByProjects/ReportApiTest.php`
Expected: FAIL. Lỗi 404 hoặc "Class … not found".

- [ ] **Step 4: Viết service**

```php
<?php

namespace Modules\Assign\Services\Report;

use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Validator;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\ProspectiveProject;

/**
 * Báo cáo thời gian meeting theo dự án (update-style-bao-cao-cu/meeting-by-projects, spec 2026-10-04).
 * MỌI con số đi từ 1 tập meeting M = meetingQuery(): meeting Chốt lịch / Hoàn thành, ngày họp trong kỳ, khớp loại /
 * hình thức / bộ lọc dự án, trong quyền. Dự án hiện khi còn ≥ 1 meeting thuộc M (khác bản cũ: lọc cấp dự án rồi
 * hiện MỌI meeting của dự án).
 */
class MeetingByProjectsReportService
{
    const PERM_ALL = 'Xem báo cáo meeting theo dự án theo tổng công ty';
    const PERM_COMPANY = 'Xem báo cáo meeting theo dự án theo công ty';
    const MODES = [1 => 'Trực tiếp', 2 => 'Online'];
    private const PER_PAGE = 20;
    private const MAX_PER_PAGE = 500;

    /** [from, to, label] — copy nguyên ServiceDemandReportService::period() (custom sai → 422). */
    public function period(Request $r): array
    {
        $today = Carbon::today();
        switch ($r->get('period', 'year')) {
            case 'week':
                return [$today->copy()->startOfWeek(), $today->copy()->endOfWeek(), 'tuần này'];
            case 'month':
                return [$today->copy()->startOfMonth(), $today->copy()->endOfMonth(), 'tháng ' . $today->format('m/Y')];
            case 'last_year':
                $y = $today->copy()->subYear();
                return [$y->copy()->startOfYear(), $y->copy()->endOfYear(), 'năm ' . $y->year];
            case 'custom':
                Validator::make($r->only('from', 'to'), [
                    'from' => 'required|date_format:d/m/Y',
                    'to' => 'required|date_format:d/m/Y',
                ])->after(function ($v) use ($r) {
                    if (!$v->errors()->any()
                        && Carbon::createFromFormat('!d/m/Y', $r->get('from'))->gt(Carbon::createFromFormat('!d/m/Y', $r->get('to')))) {
                        $v->errors()->add('to', 'Ngày kết thúc phải sau hoặc bằng ngày bắt đầu');
                    }
                })->validate();
                $from = Carbon::createFromFormat('!d/m/Y', $r->get('from'))->startOfDay();
                $to = Carbon::createFromFormat('!d/m/Y', $r->get('to'))->endOfDay();
                return [$from, $to, 'từ ' . $from->format('d/m/Y') . ' đến ' . $to->format('d/m/Y')];
            default:
                return [$today->copy()->startOfYear(), $today->copy()->endOfYear(), 'năm ' . $today->year];
        }
    }

    /** Tập M chưa select. $skip = khoá bộ lọc bỏ qua (filterOptions dùng để ô lọc không tự bó chính nó). */
    public function meetingQuery(Request $r, array $skip = [])
    {
        [$from, $to] = $this->period($r);
        $q = DB::table('prospective_project_meetings as ppm')
            ->join('meetings as m', 'm.id', '=', 'ppm.meeting_id')
            ->join('prospective_projects as p', 'p.id', '=', 'ppm.prospective_project_id')
            ->where('p.status', '!=', ProspectiveProject::STATUS_DANG_TAO)
            ->whereIn('m.status', Meeting::REPORT_STATUSES)
            ->whereBetween('m.start_date', [$from->format('Y-m-d H:i:s'), $to->format('Y-m-d H:i:s')]);

        $filters = [
            'meeting_type_id' => 'm.meeting_type_id', 'mode_id' => 'm.mode_id', 'status' => 'm.status',
            'project_creator_id' => 'p.created_by', 'customer_id' => 'p.customer_id', 'project_id' => 'p.id',
            'project_phase_id' => 'p.project_phase_id', 'meeting_id' => 'm.id',
        ];
        foreach ($filters as $key => $col) {
            if (!in_array($key, $skip, true) && $r->filled($key)) {
                $q->where($col, (int) $r->get($key));
            }
        }
        if (!in_array('company_id', $skip, true) && $r->filled('company_id') && isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            $q->where('p.company_id', (int) $r->get('company_id'));
        }
        if (!in_array('q', $skip, true) && trim((string) $r->get('q')) !== '') {
            $like = '%' . trim($r->get('q')) . '%';
            $q->where(function ($w) use ($like) {
                $w->where('m.code', 'like', $like)->orWhere('m.name', 'like', $like)
                    ->orWhere('p.code', 'like', $like)->orWhere('p.name', 'like', $like)
                    ->orWhere('p.customer_name', 'like', $like)->orWhere('p.customer_code', 'like', $like);
            });
        }
        $this->applyPermission($q);

        return $q;
    }

    /** Giữ đúng 3 mức của bản cũ (MeetingByProjectsService::applyPermissionFilter). */
    private function applyPermission($q): void
    {
        if (isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            return;
        }
        $me = (int) auth()->user()->id;
        if (isCurrentEmployeeHasPermission(self::PERM_COMPANY)) {
            $company = (int) auth()->user()->current_company_role;
            $q->where(function ($w) use ($company, $me) {
                $w->where('p.company_id', $company)->orWhere('p.created_by', $me);
            });

            return;
        }
        $q->where(function ($w) use ($me) {
            $w->where('p.created_by', $me)->orWhere('p.main_sale_employee_id', $me);
        });
    }

    /** Dòng phẳng (p, m) đã chuẩn hoá — nguồn của index / item-list / Excel / in. */
    public function meetingRows(Request $r): Collection
    {
        $rows = $this->meetingQuery($r)
            ->leftJoin('meeting_types as mt', 'mt.id', '=', 'm.meeting_type_id')
            ->leftJoin('project_phases as ph', 'ph.id', '=', 'p.project_phase_id')
            ->leftJoin('employees as ce', 'ce.id', '=', 'p.created_by')
            ->leftJoin('employee_infos as ci', 'ci.id', '=', 'ce.employee_info_id')
            ->select([
                'p.id as project_id', 'p.code as project_code', 'p.name as project_name', 'p.status as project_status',
                'p.is_parent_project', 'p.customer_id', 'p.customer_code', 'p.customer_name', 'p.created_at as project_created_at',
                'ci.fullname as creator_name', 'ph.name as phase_name',
                'm.id', 'm.code', 'm.name', 'm.status', 'm.start_date', 'm.end_date', 'm.meeting_type_id', 'mt.name as type_name', 'm.mode_id',
                DB::raw('COALESCE(TIMESTAMPDIFF(MINUTE, m.start_date, m.end_date), 0) as duration'),
                DB::raw('EXISTS(SELECT 1 FROM meeting_reports mr WHERE mr.meeting_id = m.id) as has_report'),
            ])
            ->orderByDesc('p.created_at')->orderBy('m.start_date')->orderBy('m.id')
            ->get();

        $people = app(MeetingParticipantCounter::class)->byMeeting($rows->pluck('id')->all());

        return $rows->map(function ($x) use ($people) {
            $start = $x->start_date ? Carbon::parse($x->start_date) : null;
            $end = $x->end_date ? Carbon::parse($x->end_date) : null;

            return [
                'project_id' => (int) $x->project_id, 'project_code' => (string) $x->project_code, 'project_name' => (string) $x->project_name,
                'project_status' => (int) $x->project_status,
                'project_status_text' => ProspectiveProject::resolveStatusName($x->project_status, $x->is_parent_project),
                'project_status_color' => ProspectiveProject::resolveStatusColor($x->project_status, $x->is_parent_project),
                'customer_id' => $x->customer_id ? (int) $x->customer_id : null, 'customer_code' => (string) $x->customer_code,
                'customer_name' => (string) $x->customer_name, 'creator_name' => (string) $x->creator_name, 'phase_name' => (string) $x->phase_name,
                'id' => (int) $x->id, 'code' => (string) $x->code, 'name' => (string) $x->name, 'status' => (int) $x->status,
                'status_text' => Meeting::resolveStatusName($x->status), 'status_color' => Meeting::resolveStatusColor($x->status),
                'start_date' => $start ? $start->format('Y-m-d') : null, 'start_time' => $start ? $start->format('H:i') : null,
                'end_time' => $end ? $end->format('H:i') : null, 'duration' => max(0, (int) $x->duration),
                'type_id' => $x->meeting_type_id ? (int) $x->meeting_type_id : null, 'type_name' => (string) $x->type_name,
                'mode_id' => $x->mode_id ? (int) $x->mode_id : null, 'mode_name' => self::MODES[(int) $x->mode_id] ?? '',
                'participants' => $people[(int) $x->id] ?? 0, 'has_report' => (bool) $x->has_report,
            ];
        });
    }

    /** Số liệu của 1 tập dòng (dùng cho summary, totals dự án, dòng TỔNG). */
    public function totals(Collection $rows): array
    {
        $ids = $rows->pluck('id')->unique()->values()->all();
        $byType = $rows->groupBy('type_id')->map(function ($g) {
            return ['id' => $g->first()['type_id'], 'name' => $g->first()['type_name'], 'count' => $g->count()];
        })->sortBy('name')->values()->all();

        return [
            'meetings' => count($ids),
            'duration' => (int) $rows->sum('duration'),
            'participants' => app(MeetingParticipantCounter::class)->distinct($ids),
            'by_status' => $this->countBy($rows, 'status', Meeting::REPORT_STATUSES),
            'by_mode' => $this->countBy($rows, 'mode_id', array_keys(self::MODES)),
            'by_type' => $byType,
        ];
    }

    private function countBy(Collection $rows, string $key, array $ids): array
    {
        $out = [];
        foreach ($ids as $id) {
            $out[(string) $id] = $rows->where($key, $id)->count();
        }

        return $out;
    }

    public function index(Request $r, bool $all = false): array
    {
        [$from, $to, $label] = $this->period($r);
        $rows = $this->meetingRows($r);
        $groups = $rows->groupBy('project_id')->map(function ($list) {
            $p = $list->first();

            return [
                'project_id' => $p['project_id'], 'code' => $p['project_code'], 'name' => $p['project_name'],
                'customer_id' => $p['customer_id'], 'customer_code' => $p['customer_code'], 'customer_name' => $p['customer_name'],
                'creator_name' => $p['creator_name'], 'status' => $p['project_status'], 'status_text' => $p['project_status_text'],
                'status_color' => $p['project_status_color'], 'phase_name' => $p['phase_name'],
                'totals' => $this->totals($list), 'meetings' => $list->values()->all(),
            ];
        })->values();

        $summary = $this->totals($rows) + [
            'projects' => $groups->count(),
            'customers' => $rows->pluck('customer_id')->filter()->unique()->count(),
        ];
        $perPage = $all ? max(1, $groups->count()) : min(self::MAX_PER_PAGE, max(1, (int) $r->get('per_page', self::PER_PAGE)));
        $page = $all ? 1 : max(1, (int) $r->get('page', 1));

        return [
            'summary' => $summary,
            'groups' => $groups->forPage($page, $perPage)->values()->all(),
            'meta' => [
                'total' => $groups->count(), 'per_page' => $perPage, 'current_page' => $page,
                'period_label' => $label, 'from' => $from->format('d/m/Y'), 'to' => $to->format('d/m/Y'),
            ],
        ];
    }
}
```

Đã kiểm trên `origin/gop_db` (05/10): `Meeting::resolveStatusName($s)` / `resolveStatusColor($s)` và
`ProspectiveProject::resolveStatusName($s, $isParent)` / `resolveStatusColor($s, $isParent)` có sẵn. KHÔNG cần sửa 2 entity ở task này.

`MeetingParticipantCounter` viết ở Task 3. Task này tạo bản tối thiểu để test chạy:

```php
<?php

namespace Modules\Assign\Services\Report;

use Illuminate\Support\Facades\DB;

/** Đếm người tham gia không trùng (spec 3.3) — Task 3 hoàn thiện khoá gộp phía khách hàng. */
class MeetingParticipantCounter
{
    /** @return array<int,int> meeting_id => số người */
    public function byMeeting(array $meetingIds): array
    {
        $out = [];
        foreach ($this->keys($meetingIds)->groupBy('meeting_id') as $mid => $list) {
            $out[(int) $mid] = $list->pluck('key')->unique()->count();
        }

        return $out;
    }

    public function distinct(array $meetingIds): int
    {
        return $this->keys($meetingIds)->pluck('key')->unique()->count();
    }

    /** 1 dòng meeting_employees -> { meeting_id, key } */
    public function keys(array $meetingIds)
    {
        return DB::table('meeting_employees')->whereIn('meeting_id', $meetingIds ?: [0])->whereIn('type', [1, 2])
            ->get(['id', 'meeting_id', 'employee_id', 'type', 'name', 'phone'])
            ->map(function ($x) {
                return ['meeting_id' => (int) $x->meeting_id, 'key' => $this->key($x)];
            });
    }

    public function key($x): string
    {
        if ((int) $x->type === 1) {
            return (int) $x->employee_id > 0 ? 'employee_' . (int) $x->employee_id : 'member_' . (int) $x->id;
        }

        return 'member_' . (int) $x->id;
    }
}
```

- [ ] **Step 5: Controller + route tạm**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Modules\Assign\Services\Report\MeetingByProjectsReportService;

/** Báo cáo thời gian meeting theo dự án (khuôn PotentialCustomerTrackingReportController). Gate nằm trong service. */
class MeetingByProjectsReportController extends ApiController
{
    private $service;

    public function __construct(MeetingByProjectsReportService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->index($request));
    }
}
```

Trong `Modules/Assign/Routes/api.php`, ngay dưới các route `potential-customer-tracking`:
```php
        // Báo cáo meeting theo dự án — bản mới (update-style-bao-cao-cu). Tạm ở -v2 tới Task 9.
        Route::get('/meeting-by-projects-v2', [MeetingByProjectsReportController::class, 'index']);
```
Thêm `use Modules\Assign\Http\Controllers\Api\V1\MeetingByProjectsReportController;` theo kiểu `use` của file.

Test `test_khong_quyen…` và `test_quyen_tong_cong_ty…` gọi `/filter-options`. Task 2 thêm route `filter-options` trả
tối thiểu `['can_change_company' => isCurrentEmployeeHasPermission(PERM_ALL)]`; Task 4 bổ sung các danh mục.

- [ ] **Step 6: Chạy test, phải PASS**

Run: `vendor/bin/phpunit tests/Feature/MeetingByProjects/ReportApiTest.php`
Expected: 7 tests PASS. Fail ở `by_status` thì kiểm khoá chuỗi `'2'`/`'3'` (JSON object, không phải mảng).

- [ ] **Step 7: Commit (hrm-api)**

```bash
git add Modules/Assign/Services/Report/MeetingByProjectsReportService.php Modules/Assign/Services/Report/MeetingParticipantCounter.php \
  Modules/Assign/Http/Controllers/Api/V1/MeetingByProjectsReportController.php Modules/Assign/Routes/api.php tests/Feature/MeetingByProjects \
git commit -m "Báo cáo meeting theo dự án (mới): tập meeting khớp bộ lọc, quyền 3 mức, cây dự án phân trang theo dự án"
```

---

### Task 3: Người tham gia gộp + `item-list` + `participant-list`

**Files:**
- Modify: `Modules/Assign/Services/Report/MeetingParticipantCounter.php` (khoá gộp KH + `listFor`)
- Modify: `MeetingByProjectsReportService.php` (thêm `itemList`, `participantRows`, `participantList`)
- Modify: controller + route (`/meeting-by-projects-v2/item-list`, `/participant-list`)
- Test: `tests/Feature/MeetingByProjects/ReportApiTest.php` (thêm 3 test)

**Interfaces:**
- Produces:
  - `itemList(Request): array{rows: array, meta: {total, per_page, current_page}}`
  - `participantRows(Request): array<array{side, name, position, unit, phone, meeting_count}>`
  - `participantList(Request): array{rows, meta}`
  - `MeetingParticipantCounter::listFor(array $meetingIds, array $customerNameByMeeting): array`

- [ ] **Step 1: Test fail**

```php
    public function test_gop_nguoi_tham_gia_khach_hang(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $this->makeMeeting($p, [], [['type' => 2, 'name' => 'Anh  Minh', 'phone' => '0912 345 678'], ['type' => 2, 'name' => '', 'phone' => '']]);
        $this->makeMeeting($p, [], [['type' => 2, 'name' => 'anh minh', 'phone' => '0912345678'], ['type' => 2, 'name' => '', 'phone' => ''], ['type' => 1, 'employee_id' => self::A]]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $this->assertSame(4, $this->api(self::VIEWER, '', ['customer_id' => $cus])->json('data.summary.participants'));
        $rows = collect($this->api(self::VIEWER, '/participant-list', ['customer_id' => $cus])->assertOk()->json('data.rows'));
        $minh = $rows->first(function ($x) { return mb_strtolower(preg_replace('/\s+/u', ' ', $x['name'])) === 'anh minh'; });
        $this->assertSame(2, $minh['meeting_count']);
        $this->assertSame('customer', $minh['side']);
        $this->assertSame($p->customer_name, $minh['unit']);
        $this->assertSame(1, $rows->where('side', 'company')->count());
    }

    public function test_item_list_khop_so_o_bam(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $this->makeMeeting($p, ['mode_id' => 1, 'status' => Meeting::CHOT_LICH]);
        $this->makeMeeting($p, ['mode_id' => 2, 'status' => Meeting::HOAN_THANH]);
        $this->makeMeeting($p, ['mode_id' => 2, 'status' => Meeting::HOAN_THANH, 'meeting_type_id' => 2]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $q = ['customer_id' => $cus, 'mode_id' => 2];
        $sum = $this->api(self::VIEWER, '', $q)->json('data.summary');
        $this->assertSame($sum['meetings'], $this->api(self::VIEWER, '/item-list', $q + ['per_page' => 500])->json('data.meta.total'));
        $this->assertSame($sum['by_status']['3'], $this->api(self::VIEWER, '/item-list', $q + ['status' => 3])->json('data.meta.total'));
    }

    public function test_participant_list_loc_theo_meeting_va_phia(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(self::A, $cus);
        $m1 = $this->makeMeeting($p, [], [['type' => 1, 'employee_id' => self::A], ['type' => 2, 'name' => 'Chị Hoa', 'phone' => '0987']]);
        $this->makeMeeting($p, [], [['type' => 1, 'employee_id' => self::B]]);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $this->assertCount(2, $this->api(self::VIEWER, '/participant-list', ['customer_id' => $cus, 'meeting_id' => $m1->id])->json('data.rows'));
        $this->assertCount(2, $this->api(self::VIEWER, '/participant-list', ['customer_id' => $cus, 'side' => 'company'])->json('data.rows'));
    }
```

- [ ] **Step 2: Chạy, phải FAIL**

Run: `vendor/bin/phpunit tests/Feature/MeetingByProjects/ReportApiTest.php --filter "gop_nguoi|item_list|participant_list"`
Expected: FAIL. `participants` ra 5 thay vì 4, route 404.

- [ ] **Step 3: Khoá gộp phía KH + danh sách người**

Trong `MeetingParticipantCounter::key()`, thay nhánh khách hàng:

```php
        $name = mb_strtolower(trim(preg_replace('/\s+/u', ' ', (string) $x->name)));
        $phone = preg_replace('/\D+/', '', (string) $x->phone);
        if ($name === '' && $phone === '') {
            return 'member_' . (int) $x->id;  // dòng trống: không gộp (spec 3.3)
        }

        return 'kh_' . $name . '|' . $phone;
```

Thêm method:

```php
    /**
     * Danh sách người đã gộp. Phía công ty: họ tên / chức vụ ưu tiên employee_infos (khuôn bản cũ
     * resolveCompanyParticipantFields), đơn vị = phòng ban. Phía KH: đơn vị = tên KH của dự án chứa meeting.
     * @param array<int,string> $customerNameByMeeting meeting_id => tên KH
     */
    public function listFor(array $meetingIds, array $customerNameByMeeting): array
    {
        $rows = DB::table('meeting_employees as me')
            ->leftJoin('employees as e', 'e.id', '=', 'me.employee_id')
            ->leftJoin('employee_infos as i', 'i.id', '=', 'e.employee_info_id')
            ->leftJoin('working_positions as wp', 'wp.id', '=', 'i.employee_work_position_id')
            ->leftJoin('departments as d', 'd.id', '=', 'i.department_id')
            ->whereIn('me.meeting_id', $meetingIds ?: [0])->whereIn('me.type', [1, 2])
            ->get(['me.id', 'me.meeting_id', 'me.employee_id', 'me.type', 'me.name', 'me.role', 'me.phone',
                'i.fullname', 'wp.name as wp_name', 'd.name as dept_name']);
        $bucket = [];
        foreach ($rows as $x) {
            $k = $this->key($x);
            $company = (int) $x->type === 1;
            $b = $bucket[$k] ?? [
                'side' => $company ? 'company' : 'customer',
                'name' => (string) ($company && $x->fullname ? $x->fullname : $x->name),
                'position' => (string) ($company && $x->wp_name ? $x->wp_name : $x->role),
                'unit' => (string) ($company ? $x->dept_name : ($customerNameByMeeting[(int) $x->meeting_id] ?? '')),
                'phone' => (string) $x->phone,
                'meetings' => [],
            ];
            if ($b['phone'] === '' && $x->phone) {
                $b['phone'] = (string) $x->phone;
            }
            $b['meetings'][(int) $x->meeting_id] = true;
            $bucket[$k] = $b;
        }

        $list = array_map(function ($b) {
            $b['meeting_count'] = count($b['meetings']);
            unset($b['meetings']);

            return $b;
        }, array_values($bucket));
        usort($list, function ($a, $b) {
            return [$a['side'], $a['name']] <=> [$b['side'], $b['name']];
        });

        return $list;
    }
```

Chức vụ = `EmployeeInfo::workPosition()` (`belongsTo(WorkingPosition, 'employee_work_position_id')`). Tên bảng của
`WorkingPosition` kiểm bằng `$table` của model / `SHOW TABLES LIKE 'working%'` trước khi chạy (memory: không đoán tên bảng).

- [ ] **Step 4: Service + controller + route**

Thêm vào `MeetingByProjectsReportService`:

```php
    public function itemList(Request $r): array
    {
        $rows = $this->meetingRows($r);
        $perPage = min(self::MAX_PER_PAGE, max(1, (int) $r->get('per_page', self::MAX_PER_PAGE)));
        $page = max(1, (int) $r->get('page', 1));

        return [
            'rows' => $rows->forPage($page, $perPage)->values()->all(),
            'meta' => ['total' => $rows->count(), 'per_page' => $perPage, 'current_page' => $page],
        ];
    }

    public function participantRows(Request $r): array
    {
        $rows = $this->meetingRows($r);
        $list = app(MeetingParticipantCounter::class)->listFor(
            $rows->pluck('id')->unique()->values()->all(),
            $rows->pluck('customer_name', 'id')->all()
        );
        $side = $r->get('side');
        $kw = mb_strtolower(trim((string) $r->get('pq')));

        return array_values(array_filter($list, function ($x) use ($side, $kw) {
            if (in_array($side, ['company', 'customer'], true) && $x['side'] !== $side) {
                return false;
            }

            return $kw === '' || mb_strpos(mb_strtolower($x['name'] . ' ' . $x['phone']), $kw) !== false;
        }));
    }

    public function participantList(Request $r): array
    {
        $rows = $this->participantRows($r);

        return ['rows' => $rows, 'meta' => ['total' => count($rows), 'per_page' => count($rows), 'current_page' => 1]];
    }
```

Ghi chú: tìm người dùng `pq`, KHÔNG dùng `q`, vì `q` đã lọc meeting trong `meetingQuery`.

Controller thêm `itemList`, `participantList` (khuôn `index`). Route:
```php
        Route::get('/meeting-by-projects-v2/item-list', [MeetingByProjectsReportController::class, 'itemList']);
        Route::get('/meeting-by-projects-v2/participant-list', [MeetingByProjectsReportController::class, 'participantList']);
```

- [ ] **Step 5: Chạy cả file, phải PASS**

Run: `vendor/bin/phpunit tests/Feature/MeetingByProjects/ReportApiTest.php`
Expected: 10 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add Modules/Assign/Services/Report Modules/Assign/Http/Controllers/Api/V1/MeetingByProjectsReportController.php Modules/Assign/Routes/api.php tests/Feature/MeetingByProjects
git commit -m "Báo cáo meeting theo dự án: gộp người tham gia phía KH theo tên + SĐT, popup danh sách meeting / người tham gia"
```

---

### Task 4: `filter-options`

**Files:**
- Modify: service (`filterOptions`), controller, route `/meeting-by-projects-v2/filter-options`
- Test: `ReportApiTest.php` (thêm 1 test)

**Interfaces:**
- Produces: `filterOptions(Request): array{companies, creators, customers, projects, meeting_types, phases, modes, can_change_company}`.
  - `creators[]`: `{id, name (Tên - Mã phòng - Mã NV), department_id}`
  - `customers[]`: `{id, code, name}`
  - `projects[]`: `{id, code, name, customer_id}`
  - `meeting_types[]`: `{id, name, description}`
  - `phases[]`: `{id, name, description}`
  - `modes[]`: `{id, name}`

- [ ] **Step 1: Test fail**

```php
    public function test_filter_options_bo_theo_quyen_va_khong_tu_bo_chinh_no(): void
    {
        [$cus] = $this->freshCustomers();
        $p1 = $this->makeProject(self::A, $cus);
        $p2 = $this->makeProject(self::B, $cus);
        $this->makeMeeting($p1);
        $this->makeMeeting($p2);
        $this->grant(self::VIEWER, self::PERM_ALL);

        $o = $this->api(self::VIEWER, '/filter-options', ['customer_id' => $cus, 'project_creator_id' => self::A])->assertOk()->json('data');
        $this->assertContains(self::B, array_column($o['creators'], 'id'));            // ô NV tạo không tự bó
        $this->assertSame([$p1->id], array_column(array_filter($o['projects'], function ($x) use ($cus) { return $x['customer_id'] === $cus; }), 'id'));
        $this->assertSame([['id' => 1, 'name' => 'Trực tiếp'], ['id' => 2, 'name' => 'Online']], $o['modes']);
        $this->assertTrue($o['can_change_company']);
    }
```

- [ ] **Step 2: Chạy, phải FAIL** (`creators` undefined).

- [ ] **Step 3: Viết `filterOptions`**

```php
    public function filterOptions(Request $r): array
    {
        $canAll = isCurrentEmployeeHasPermission(self::PERM_ALL);
        $distinct = function (array $skip, callable $select) use ($r) {
            return $select($this->meetingQuery($r, $skip))->get();
        };
        $creators = $distinct(['project_creator_id'], function ($q) {
            return $q->join('employees as ce', 'ce.id', '=', 'p.created_by')
                ->join('employee_infos as ci', 'ci.id', '=', 'ce.employee_info_id')
                ->leftJoin('departments as cd', 'cd.id', '=', 'ci.department_id')
                ->select(['p.created_by as id', 'ci.fullname as name', 'ci.code', 'ci.department_id', 'cd.code as department_code'])
                ->distinct()->orderBy('ci.fullname');
        })->map(function ($e) {
            $e = (array) $e;
            $e['fullname'] = $e['name'];

            return ['id' => (int) $e['id'], 'name' => employeeOptionLabel($e), 'department_id' => $e['department_id'] ? (int) $e['department_id'] : null];
        })->values()->all();
        $customers = $distinct(['customer_id', 'project_id'], function ($q) {
            return $q->whereNotNull('p.customer_id')->select(['p.customer_id as id', 'p.customer_code as code', 'p.customer_name as name'])->distinct()->orderBy('p.customer_name');
        })->map(function ($c) {
            return ['id' => (int) $c->id, 'code' => (string) $c->code, 'name' => (string) $c->name];
        })->values()->all();
        $projects = $distinct(['project_id'], function ($q) {
            return $q->select(['p.id', 'p.code', 'p.name', 'p.customer_id'])->distinct()->orderByDesc('p.id');
        })->map(function ($p) {
            return ['id' => (int) $p->id, 'code' => (string) $p->code, 'name' => (string) $p->name, 'customer_id' => $p->customer_id ? (int) $p->customer_id : null];
        })->values()->all();
        $companies = $canAll
            ? DB::table('companies')->orderBy('name')->get(['id', 'name'])
            : DB::table('companies')->where('id', auth()->user()->current_company_role)->get(['id', 'name']);

        return [
            'companies' => $companies->map(function ($c) { return ['id' => (int) $c->id, 'name' => $c->name]; })->values()->all(),
            'creators' => $creators,
            'customers' => $customers,
            'projects' => $projects,
            'meeting_types' => DB::table('meeting_types')->where('status', 1)->orderBy('name')->get(['id', 'name', 'description'])
                ->map(function ($x) { return (array) $x; })->all(),
            'phases' => DB::table('project_phases')->where('status', 1)->orderBy('name')->get(['id', 'name', 'description'])
                ->map(function ($x) { return (array) $x; })->all(),
            'modes' => array_map(function ($id) { return ['id' => $id, 'name' => self::MODES[$id]]; }, array_keys(self::MODES)),
            'can_change_company' => $canAll,
        ];
    }
```

Kiểm `employeeOptionLabel()` có trên `origin/gop_db` (`grep -rn "function employeeOptionLabel" app`). Kiểm `project_phases`
có lọc theo công ty không: FE cũ gọi endpoint nào cho ô Giai đoạn (`grep -n "phase" pages/assign/report/meeting-by-projects/index.vue`).
Endpoint cũ có lọc công ty thì `filterOptions` lọc giống hệt.

- [ ] **Step 4: Controller + route `/meeting-by-projects-v2/filter-options`; xoá bản tối thiểu ở Task 2.**

- [ ] **Step 5: Chạy cả file PASS (11 tests) → Commit**

```bash
git commit -am "Báo cáo meeting theo dự án: danh mục ô lọc theo quyền + phạm vi đang xem"
```

---

### Task 5: Excel (3 file) + bản in (3 chế độ)

**Files:**
- Create: `Modules/Assign/Export/MeetingByProjectsReportExport.php`, `MeetingByProjectsListExport.php`, `MeetingByProjectsParticipantExport.php`
- Create: `resources/views/exports/assign/meeting_by_projects_{report,list,participants}.blade.php`
- Create: `Modules/Assign/Services/Report/MeetingByProjectsPrintService.php`, `resources/views/prints/assign/meeting_by_projects_{summary,detail,participants}.blade.php`
- Modify: controller (`export`, `exportItemList`, `exportParticipantList`, `printListData`) + 4 route
- Test: `tests/Feature/MeetingByProjects/ExportPrintTest.php`

**REQUIRED skills:** `export-excel` (số thô + `data-format`, logo theo công ty đang xem, cột đủ rộng), `print-page` mục 4d
(trần số dòng, `printListPayload`).

**Interfaces:**
- Consumes: `index($r, true)`, `meetingRows($r)`, `participantRows($r)`.
- Produces: route `export`, `item-list/export`, `participant-list/export`, `print-list-data?mode=summary|detail|participants`.

- [ ] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingByProjects;

use Tests\TestCase;

class ExportPrintTest extends TestCase
{
    use MeetingFixture;

    private const URL = '/api/v1/assign/report/meeting-by-projects-v2';

    protected function tearDown(): void
    {
        $this->cleanupMeetingFixture();
        parent::tearDown();
    }

    public function test_excel_va_ban_in_dung_bo_loc(): void
    {
        [$cus] = $this->freshCustomers();
        $p = $this->makeProject(27, $cus);
        $m = $this->makeMeeting($p, [], [['type' => 2, 'name' => 'Anh Minh', 'phone' => '0912']]);
        $this->grant(28, 1060);
        $this->actAs(28);
        $q = '?customer_id=' . $cus;

        foreach (['/export', '/item-list/export', '/participant-list/export'] as $path) {
            $res = $this->get(self::URL . $path . $q);
            $res->assertOk();
            $this->assertStringContainsString('.xlsx', $res->headers->get('content-disposition'));
        }
        foreach (['summary', 'detail', 'participants'] as $mode) {
            $html = $this->getJson(self::URL . '/print-list-data' . $q . '&mode=' . $mode)->assertOk()->json('data.template');
            $this->assertStringContainsString($mode === 'participants' ? 'Anh Minh' : $m->code, $html);
        }
    }
}
```

- [ ] **Step 2: Chạy, phải FAIL (404).**

- [ ] **Step 3: Viết 3 Export + blade**

Copy khuôn `Modules/Assign/Export/PotentialCustomerTrackingListExport.php` + blade
`resources/views/exports/assign/potential_customer_tracking_list.blade.php` (đọc bằng
`git show origin/gop_db:<path>`). Đổi:
- **Report (cây):** cột A STT (I, II… / 1, 2…) · B Dự án / Meeting · C Khách hàng · D Người tạo dự án · E Tiến trình ·
  F Giai đoạn · G Số meeting · H Trạng thái · I Thời gian · J Thời lượng (phút) · K Loại meeting · L Hình thức ·
  M Người tham gia. Dòng 1 trống cho logo, dòng TỔNG ngay dưới tiêu đề. Dòng dự án in đậm. Ô Trạng thái / Loại / Hình thức
  ở dòng dự án ghi chữ "2 Chốt lịch · 5 Hoàn thành". G, J, M là SỐ THÔ + `data-format="#,##0"`.
- **List (meeting):** STT · Mã meeting · Tên meeting · Dự án · Khách hàng · Ngày · Giờ · Thời lượng · Loại · Hình thức ·
  Trạng thái · Người tham gia · Biên bản (Có/Không).
- **Participants:** STT · Phía · Họ tên · Chức vụ · Đơn vị · SĐT · Số lần tham gia meeting.

Tiêu đề phụ ghi kỳ: `$report['meta']['period_label']` + `scope_label` (FE gửi tên ô đã bấm).

- [ ] **Step 4: Print service + 3 blade**

Copy `PotentialCustomerTrackingPrintService` (trên `origin/gop_db`), đổi `render()`:
```php
    public function render(Request $request): array
    {
        switch ($request->input('mode')) {
            case 'detail':
                return $this->renderRows($request, $this->report->meetingRows($request)->all(), 'prints.assign.meeting_by_projects_detail');
            case 'participants':
                return $this->renderRows($request, $this->report->participantRows($request), 'prints.assign.meeting_by_projects_participants');
            default:
                return $this->renderSummary($request);
        }
    }
```
`renderSummary` lấy tổng = `summary.meetings + summary.projects` để so trần. Blade copy từ
`prints/assign/potential_customer_tracking_{summary,detail}.blade.php`, cột như Step 3.

- [ ] **Step 5: Controller + route**

```php
        Route::get('/meeting-by-projects-v2/export', [MeetingByProjectsReportController::class, 'export']);
        Route::get('/meeting-by-projects-v2/item-list/export', [MeetingByProjectsReportController::class, 'exportItemList']);
        Route::get('/meeting-by-projects-v2/participant-list/export', [MeetingByProjectsReportController::class, 'exportParticipantList']);
        // Tên `print-list-data` là contract của utils/mixins/reportPrintPreviewMixin.js — đừng đổi
        Route::get('/meeting-by-projects-v2/print-list-data', [MeetingByProjectsReportController::class, 'printListData']);
```
Tên file tải: `bao-cao-meeting-theo-du-an.xlsx`, `danh-sach-meeting-theo-du-an.xlsx`, `danh-sach-nguoi-tham-gia-meeting.xlsx`.

- [ ] **Step 6: PASS + mở 1 file Excel thật kiểm logo / số / độ rộng cột → Commit**

```bash
git add Modules/Assign/Export Modules/Assign/Services/Report/MeetingByProjectsPrintService.php resources/views tests/Feature/MeetingByProjects Modules/Assign/Http Modules/Assign/Routes/api.php
git commit -m "Báo cáo meeting theo dự án: Excel cây / danh sách meeting / người tham gia và 3 bản in"
```

---

### Task 6: Nới `Meeting::canView()` theo quyền báo cáo (quyết định #10)

**Files:**
- Modify: `Modules/Assign/Entities/Meeting/Meeting.php` (`canView` + method mới)
- Test: `tests/Feature/MeetingByProjects/MeetingCanViewTest.php`

- [ ] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingByProjects;

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
        auth('api')->setUser(\App\Models\TpEmployee::findOrFail($emp));

        return \Modules\Assign\Entities\Meeting\Meeting::findOrFail($meetingId)->canView();
    }

    public function test_quyen_cong_ty_xem_meeting_du_an_cong_ty_minh(): void
    {
        [$cus] = $this->freshCustomers();
        // Meeting do người khác tạo / chủ trì, VIEWER 28 không là thành phần
        $own = $this->makeMeeting($this->makeProject(27, $cus, ['company_id' => 1]), ['created_by' => 27, 'host_employee_id' => 27]);
        $foreign = $this->makeMeeting($this->makeProject(27, $cus, ['company_id' => 2]), ['created_by' => 27, 'host_employee_id' => 27]);
        $this->assertFalse($this->canView(28, $own->id), 'chưa có quyền thì luật cũ phải chặn — nếu true, đổi actor');

        $this->grant(28, 1061);
        $this->assertTrue($this->canView(28, $own->id));
        $this->assertFalse($this->canView(28, $foreign->id));
    }

    public function test_quyen_tong_cong_ty_xem_moi_meeting_gan_du_an(): void
    {
        [$cus] = $this->freshCustomers();
        $foreign = $this->makeMeeting($this->makeProject(27, $cus, ['company_id' => 2]), ['created_by' => 27, 'host_employee_id' => 27]);
        $this->grant(28, 1060);
        $this->assertTrue($this->canView(28, $foreign->id));
    }
}
```

Lưu ý: dòng `assertFalse` đầu tiên là mốc. Nếu actor 28 đã xem được theo luật cũ (vd có quyền xem meeting cấp công
ty) thì đổi sang nhân viên khác không có quyền meeting nào: `SELECT` theo `employee_has_roles` trước.

- [ ] **Step 2: FAIL. Step 3: Code**

```php
    public function canView()
    {
        return $this->canViewByMeetingRules() || $this->canViewByServiceDemandReport()
            || $this->canViewByPotentialCustomerTracking() || $this->canViewByMeetingByProjectsReport();
    }

    /**
     * Quyền xem meeting GẮN DỰ ÁN TKT theo quyền báo cáo meeting theo dự án (update-style-bao-cao-cu, user chốt
     * 05/10/2026 — khuôn canViewByServiceDemandReport): 1060 → mọi meeting gắn dự án · 1061 → dự án thuộc công ty
     * hiện tại. Chỉ là quyền XEM; chạy sau các luật cũ.
     */
    private function canViewByMeetingByProjectsReport()
    {
        $projects = \DB::table('prospective_project_meetings as ppm')->join('prospective_projects as p', 'p.id', '=', 'ppm.prospective_project_id')
            ->where('ppm.meeting_id', $this->id);
        if (isCurrentEmployeeHasPermission(MeetingByProjectsReportService::PERM_ALL)) {
            return $projects->exists();
        }
        if (isCurrentEmployeeHasPermission(MeetingByProjectsReportService::PERM_COMPANY)) {
            return $projects->where('p.company_id', auth()->user()->current_company_role)->exists();
        }

        return false;
    }
```
Thêm `use Modules\Assign\Services\Report\MeetingByProjectsReportService;` và bổ sung đoạn mô tả vào docblock của `canView()`.

- [ ] **Step 4: PASS, cộng chạy lại test có sẵn của canView** (`vendor/bin/phpunit --filter "CanView|ServiceDemand|PotentialCustomerTracking"`).
- [ ] **Step 5: Commit** `git commit -am "Meeting: quyền báo cáo meeting theo dự án được xem meeting gắn dự án trong phạm vi"`

---

### Task 7: FE: khung màn, bộ lọc, khối tổng hợp, bảng cây

**Files (hrm-client, `pages/assign/report/meeting-by-projects/`):**
- Rewrite: `index.vue`
- Create: `api.js`, `format.js`, `components/{MeetingSummary,MeetingTree,DrillNum,InfoTip}.vue`

**REQUIRED:** đọc `HRM/.claude/skills/report-styles/SKILL.md` + mở `mockup.html` (đã duyệt) cạnh code.

**Interfaces:**
- Consumes: `GET assign/report/meeting-by-projects-v2` (+ `/filter-options`). Đổi `API` về `…/meeting-by-projects` ở Task 9.
- Produces:
  - `MeetingSummary`: props `summary, periodLabel, from, to`; emit `drill({ status?, mode_id?, title })` · `drill-people({ title })`.
  - `MeetingTree`: props `groups, summary, level (1|2), pagination`; emit `drill({ project_id?, status?, type_id?, mode_id?, title })`, `drill-people({ project_id?, meeting_id?, title })`, `open-meeting(row)`, `open-minutes(row)`, `update:level`, `page-change`, `page-size-change`.

- [ ] **Step 1: Copy template**

```bash
S=/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.claude/skills/report-styles/template
D=$W/hrm-client/pages/assign/report/meeting-by-projects
cp $S/components/DrillNum.vue $S/components/InfoTip.vue $D/components/
cp $S/format.js $D/format.js
printf "/** Gốc API báo cáo meeting theo dự án — CHỈ ĐỌC (hrm-api Modules/Assign). */\nexport const API = 'assign/report/meeting-by-projects-v2'\n" > $D/api.js
cp $S/components/TrackingSummary.vue $D/components/MeetingSummary.vue
cp $S/components/TrackingTable.vue $D/components/MeetingTree.vue
```
Trong `InfoTip.vue` đổi id `pct-info-` → `mbp-info-`. Trong `format.js` bỏ `daysNote`, `typeText`, thêm:
```js
/** Số phút -> "1,250" (đơn vị "phút" do nơi gọi ghi) */
export const minutes = (v) => num(Number(v) || 0)
```

- [ ] **Step 2: `MeetingSummary.vue`**: giữ nguyên template + SCSS của file đã copy, chỉ đổi:
  - `.rsum-goal__title`: `Meeting theo dự án {{ periodLabel }} ({{ from }} – {{ to }})`;
    meta `· N dự án · N meeting · N khách hàng`.
  - `blocks()`: khối `scope` (Dự án, Meeting, Khách hàng → `drill({title})`; Người tham gia → `drill-people`;
    Tổng thời lượng: `item.drill = null`, template hiện `num()` thường thay vì `DrillNum` khi `!item.drill`) và khối
    `state` (Chốt lịch `status: 2`, Hoàn thành `status: 3`, Trực tiếp `mode_id: 1`, Online `mode_id: 2`, ô 0 bỏ
    qua; meta `N meeting`).
  - CSS: thay `.pct-blk--nc` / `.pct-blk--da` bằng `.mbp-blk--scope, .mbp-blk--state { flex: 1 1 auto; }` (đo ở
    mockup: 2 khối 1 hàng, ô cao 46px ở 1366px).

- [ ] **Step 3: `MeetingTree.vue`**: giữ SCSS của template, sửa:
  - `COLS` = 14 cột đúng thứ tự + độ rộng của mockup (`mbp-col--*`: no 64 · name auto · kh 260 · creator 160 · st 200 ·
    phase 130 · cnt 100 · mst 200 · time 170 · dur 120 · type 290 · mode 180 · people 120 · minutes 90),
    `min-width: 2504px`.
  - `flatRows`: 2 cấp (d0 dự án `roman()`, d1 meeting `1..n`). `levelOptions = [{1,'Chỉ dự án'},{2,'Đến meeting'}]`.
    `applyLevel`: `level >= 2` thì mở mọi dự án.
  - Dòng TỔNG, dòng dự án, dòng meeting: nội dung ô theo bảng mục 5 của spec. Ô "n Tên · n Tên" viết 1 component
    render-function `CountList` (khuôn `CountPair` của template). Props `items: [{key, label, value, drill}]`, số 0 bỏ qua,
    CSS con chọn qua `::v-deep`.
  - Ô chữ dài: `td.rsum-tb__txt { overflow: hidden; text-overflow: ellipsis; }` + `:title`.
  - Bỏ CSS cấp d2/d3; dòng d1 = lá (tên xám `#6b7280`, nền `#f7fbfd`, STT 11px).
  - `V2BasePagination item-label="dự án"`, `:page-size-options="[10, 20, 50, 100]"`.

- [ ] **Step 4: `index.vue`**: copy `$S/index.vue`, rồi:
  - `filterFields` theo mockup mục a:
    - Kỳ theo dõi + ô `range` khi `custom`: copy `periodOptions`, `rangeIncomplete`, nhánh `period` của
      `onFilterChange` / `buildParams` (`from`/`to` → d/m/Y) từ `pages/assign/report/service-demand/index.vue`;
    - Công ty (slot, khoá theo `can_change_company`) · Nhân viên tạo dự án (`creators`) · Khách hàng (slot
      `V2BaseSelectRemote` lọc tại FE) · Dự án (lọc theo `customer_id` đang chọn) · Hình thức (`modes`);
    - Loại meeting + Giai đoạn: slot bọc `V2BaseFloatingField :hint` quanh `MeetingTypeSelect` / `ProjectPhaseSelect`
      sẵn có (giữ tooltip từng lựa chọn).
  - Đổi khách hàng thì xoá `project_id` nếu dự án không thuộc khách mới.
  - Bỏ `ItemListModal` / `CustomerMeetingHistoryModal` / `meetingDrawerBlocks` của template (Task 8 thêm popup mới).
  - `table="assign_meeting_by_projects_report"` (giữ key cài đặt bộ lọc cũ), tiêu đề "Bộ lọc báo cáo thời gian meeting
    theo dự án", InfoTip "MỤC ĐÍCH BÁO CÁO" lấy câu `pageTitleInfo` cũ.
  - `level: 1`, `perPage: 20`.

- [ ] **Step 5: Kiểm Playwright MCP trên `http://127.0.0.1:3018` (ĐO DOM, skill mục 6)**
  - `th.top === body.top` sau khi cuộn vùng bảng.
  - `padding-left` d0 / d1 = 30 / 52px; `getComputedStyle(th).color` = `rgb(10, 124, 136)`.
  - Đổi cấp → số `.rsum-tb__row--d1` = Σ meeting của trang.
  - Ở 1366px: 9 ô `.rsum-blk__item` cùng `top`, cao ≤ 46px; trang không cuộn ngang; có 2 thanh cuộn của bảng.
  - Số ở khối tổng hợp = dòng TỔNG (đọc text 2 nơi).
  - Kỳ Tuỳ chọn chưa chọn đủ ngày thì KHÔNG có request (đếm qua `browser_network_requests`).
  - Tài khoản KHÔNG quyền (e2e Assign 1180): ô Công ty bị khoá, chỉ thấy dự án mình tạo / mình là NVKD.
  - Chụp màn so với `mockup.html` cùng kích thước.

- [ ] **Step 6: Commit (hrm-client)**

```bash
git add pages/assign/report/meeting-by-projects
git commit -m "Báo cáo meeting theo dự án: khung màn mới — bộ lọc Kỳ, khối tổng hợp, bảng cây Dự án ▸ Meeting"
```

---

### Task 8: FE: popup, panel meeting, biên bản, In / Excel

**Files:**
- Create: `components/MeetingListModal.vue`, `components/ParticipantListModal.vue`, `components/PrintOptionsModal.vue`
- Modify: `index.vue`

**Interfaces:**
- Consumes: `/item-list`, `/participant-list`, `/print-list-data`, 3 route Excel (Task 3, 5); emit của Task 7.

- [ ] **Step 1: `MeetingListModal.vue`**
  - Copy `$S/components/ItemListModal.vue`. `COLUMNS` theo mockup: STT · Meeting (mã + tên phụ) · Dự án · Khách hàng ·
    Thời gian · Thời lượng (phút) · Loại meeting · Hình thức · Trạng thái (badge) · Người tham gia · Biên bản.
  - `FILTER_FIELDS`: Loại meeting (`type_id`), Hình thức (`mode_id`). Ô nào đã bị ô số cố định thì ẩn.
  - Ô tìm khớp BE `q`: mã/tên meeting, mã/tên dự án, KH.
  - `metaText`: `N meeting · N phút · Kỳ …`.
  - Bấm mã meeting → `open-meeting`; "Xem" → `open-minutes`.

- [ ] **Step 2: `ParticipantListModal.vue`**
  - Copy cùng file. Cột: STT · Phía · Họ tên · Chức vụ · Đơn vị · SĐT · Số lần tham gia meeting.
  - Ô lọc Phía (`side`: Công ty / Khách hàng); ô tìm họ tên / SĐT gửi BE dưới tên `pq`.
  - `metaText`: `N người · X phía công ty · Y phía khách hàng · Kỳ …`.

- [ ] **Step 3: `PrintOptionsModal.vue`**: copy `$S/components/PrintOptionsModal.vue`, đổi tiền tố `pct-` → `mbp-`
  và 2 mô tả (summary: cây Dự án ▸ Meeting đủ mọi trang; detail: mỗi meeting 1 dòng).

- [ ] **Step 4: Nối vào `index.vue`** (khuôn `onDrill` / `fetchDrill` / `drillBaseParams` / `downloadExcel` của template):
  - `onDrill(filter)` → `MeetingListModal` (lặp trang 500 của `item-list`).
  - `onDrillPeople(filter)` → `ParticipantListModal` (`participant-list`).
  - `onOpenMeeting(row)` → `MeetingDetailDrawer` (`WorkItemDetailDrawer`):
    `header-gradient="linear-gradient(135deg, #0a1c3d, #06b6d4)"`, `:above-modal="drill.visible || people.visible"`.
  - `onOpenMinutes(row)` → `this.loadPrintPreview('assign/meeting/' + row.id + '/print', 'Xem biên bản cuộc họp', false)`.
  - Footer popup In → `openPrintList(API, {...params, mode: 'detail' | 'participants', scope_label})`.
    Excel → `item-list/export` / `participant-list/export`.

- [ ] **Step 5: Playwright MCP (đo)**
  - Bấm "Hoàn thành" ở 1 dòng dự án → số dòng popup = số đã bấm.
  - Bấm Người tham gia ở dòng TỔNG → số dòng = `summary.participants`.
  - Mở panel meeting từ trong popup: panel nằm trên popup (so `z-index` / `getBoundingClientRect`); tài khoản chỉ có 1061
    mở được meeting người khác chủ trì (không 403). Có toast 403 là Task 6 chưa đúng.
  - "Xem" biên bản mở `ReportPrintPreviewModal`.
  - In 2 chế độ ra bản xem trước; Excel tải được, tên file đúng.
  - Console sạch.

- [ ] **Step 6: Commit** `git commit -m "Báo cáo meeting theo dự án: popup danh sách meeting / người tham gia, panel meeting, biên bản, In / Excel"`

---

### Task 9: Chuyển route chính + dọn bản cũ

**Files:**
- Modify (api): `Modules/Assign/Routes/api.php`: đổi 8 route `-v2` về `/meeting-by-projects…`, xoá 7 route cũ.
  Xoá method cũ trong `ReportController.php` (+ property / DI `meetingByProjectsService`), xoá
  `MeetingByProjectsService.php`, `MeetingByProjectsResource.php`, `app/ExcelExport/MeetingByProjectsExport.php`.
- Modify (client): `api.js` → `'assign/report/meeting-by-projects'`. Xoá `print.vue` + 8 component cũ +
  `components/TopProjectsChart.vue`.
- Modify tests: `URL` → `/api/v1/assign/report/meeting-by-projects`.

- [ ] **Step 1: Grep trước khi xoá (cả 2 repo)**

```bash
cd $W/hrm-api && grep -rn "MeetingByProjectsService\|MeetingByProjectsResource\|MeetingByProjectsExport\|getChartData\|getMeetingsByStatus\|getParticipantsByScope\b\|meeting-by-projects" Modules app routes resources tests | grep -v "MeetingByProjectsReport"
cd $W/hrm-client && grep -rn "TopProjectsChart\|meeting-by-projects/print\|meeting-by-projects/chart-data\|meeting-by-projects/meetings-by\|participants-by-scope" pages components utils layouts plugins store
```
Expected: chỉ còn chỗ thuộc chính màn này, comment (`BaseMeetingChart.vue`, `MeetingByMarketService.php`,
`meetingTypeInfoTooltip.js`, `meeting-by-market/index.vue`) và method cùng tên của báo cáo theo nhân viên
(`…ByEmployees`, KHÔNG xoá). Gặp chỗ gọi thật khác thì dừng lại hỏi user.

- [ ] **Step 2: Xoá + đổi route + sửa comment trỏ file đã xoá**
  - Comment `MeetingByMarketService.php:165` → trỏ `MeetingByProjectsReportService::applyPermission`.
  - Comment `BaseMeetingChart.vue:132` → đổi ví dụ endpoint sang `meeting-by-employees/chart-data`, nếu route đó còn.

- [ ] **Step 3: Chạy lại toàn bộ test BE liên quan**

Run: `vendor/bin/phpunit tests/Feature/MeetingByProjects && vendor/bin/phpunit --filter "MeetingByMarket|MeetingByEmployees|CanView"`
Expected: PASS hết; `php artisan route:list | grep meeting-by-projects` ra đúng 8 route mới.

- [ ] **Step 4: FE build kiểm import**: restart nuxt (`rm -rf .nuxt/components`), mở màn, console không có
  "Can't resolve"; mở thêm `/assign/report/meeting-by-employees` và `/meeting-by-market` → vẫn chạy.

- [ ] **Step 5: Commit 2 repo**

```bash
git commit -am "Báo cáo meeting theo dự án: chuyển sang API mới, gỡ endpoint / component cũ (biểu đồ Top 5, 4 popup, print.vue)"
```

---

### Task 10: e2e spec + đóng gói

**Files:**
- Create: `HRM/e2e/tests/assign/meeting-by-projects.api.spec.ts`, `meeting-by-projects.spec.ts` (khuôn
  `e2e/tests/assign/service-demand{.api,}.spec.ts`).

- [ ] **Step 1: Viết spec API** gồm 4 ca:
  - quyền: KHÔNG quyền ≠ 1061 ≠ 1060, cả có lẫn không quyền;
  - `summary.meetings` = `item-list.meta.total`;
  - `period=custom` thiếu ngày → 422;
  - `participant-list?side=customer` không có dòng `side=company`.
- [ ] **Step 2: Viết spec UI**:
  - đo khuôn: `th` sticky, độ thụt, nền dòng TỔNG, 2 thanh cuộn;
  - số tổng hợp = dòng TỔNG = số dòng popup;
  - đổi cấp; Kỳ Tuỳ chọn; panel meeting nằm trên popup;
  - tài khoản không quyền: ô Công ty khoá.
  - Chờ theo request (`waitForResponse`), KHÔNG chờ `networkidle` (memory).
- [ ] **Step 3: KHÔNG tự chạy.** Báo user, hỏi có chạy không. Nếu chạy: `--workers=1`, đọc dòng tổng kết (serial: ca
  fail làm các ca sau "did not run").
- [ ] **Step 4: Cập nhật tài liệu**
  - `design.md` (trạng thái), `.plans/gop-db/STATUS.md`, bảng theo dõi ở `../design.md`.
  - Commit e2e (repo nào chứa `HRM/e2e` thì commit ở đó).
- [ ] **Step 5: Hỏi user** push nhánh `gop_db-update-style-meeting-by-projects` 2 repo, và có merge `gop_db` không
  (cần lệnh riêng).

---

### Checkpoint — 2026-10-05 (wrap up)
Vừa hoàn thành: 10 task theo SDD (review từng task) + review tổng + 1 đợt sửa. Nhánh `gop_db-update-style-meeting-by-projects`
(worktree `websites/wt-update-style-mbp`): api 85a1c59d7..e5a334044 (9 commit) · client a6ad678d0..7e02f5b74 (3 commit).
PHPUnit `tests/Feature/MeetingByProjects` 23/23 + `--filter "CanView|ServiceDemand|PotentialCustomerTracking"` 68/68.
Playwright MCP đo đạt (Task 7, 8). E2E `e2e/tests/assign/meeting-by-projects{.api,}.spec.ts` ĐÃ VIẾT, CHƯA CHẠY.
Quyết định tự chốt + minor hoãn: `sdd-ledger.md` cùng thư mục.
Đang làm dở: không (chưa push, chưa merge).
Bước tiếp theo — chờ user trả lời 3 câu:
  (1) Nới `Meeting::canView` thêm nhánh người tạo dự án / NVKD cho khớp phạm vi báo cáo (A) hay giữ (B)?
  (2) Chạy e2e? — PHẢI truyền `API_BASE=http://127.0.0.1:8018 BASE_URL=http://127.0.0.1:3018`, `--workers=1`.
  (3) Push nhánh 2 repo? Merge gop_db cần lệnh riêng.
Server worktree (khởi động lại nếu đã tắt): api `php@7.4 artisan serve --port 8018` trong wt-update-style-mbp/hrm-api ·
client `nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npx nuxt --port 3018` trong wt-update-style-mbp/hrm-client
(.env của client worktree đã trỏ 3018/8018).
Blocked: chờ user.

### Checkpoint — 2026-10-05 (sau 3 câu user trả lời)
Vừa hoàn thành: (1) nới `Meeting::canView` khớp đúng phạm vi báo cáo — scope dùng chung `MeetingByProjectsReportService::applyProjectScope()`
(1060 tất cả · 1061 công ty mình HOẶC dự án mình tạo · không quyền: dự án mình tạo / mình là NVKD), api e679c2762 + c66df46e7, PHPUnit 28/28 +
73/73 liên quan; (2) E2E: API 8/8 passed, UI 7/7 passed (sửa 2 lỗi ở CHÍNH spec: ép max-height phải gỡ min-height 240px; nút drill chỉ chứa số →
bắt theo title); fixture dọn sạch (0 dòng E2E-MBP/PHPUNIT-MBP); (3) ĐÃ PUSH `origin/gop_db-update-style-meeting-by-projects` cả 2 repo
(api c66df46e7 · client 7e02f5b74).
Đang làm dở: không.
Bước tiếp theo: user quyết merge vào gop_db (lệnh riêng) → deploy (không migration/seeder). Báo cáo tiếp theo của folder lớn khi user chỉ định.
Blocked:
