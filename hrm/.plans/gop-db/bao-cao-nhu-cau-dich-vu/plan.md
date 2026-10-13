# Báo cáo tổng hợp nhu cầu làm dịch vụ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Sinh "nhu cầu làm dịch vụ" từ meeting giới thiệu SP (Q4 = Có), tự đổi trạng thái theo báo giá DV / hợp đồng DV, và dựng báo cáo tổng hợp ở phân hệ CSKH trước bán.

**Architecture:** Bảng mới `meeting_service_demands` (1 dòng / meeting). MỌI chuyển trạng thái đi qua 1 service `ServiceDemandStatusService`; các luồng meeting / báo giá / hợp đồng / cron chỉ gọi vào service đó. Báo cáo là service đọc riêng (`ServiceDemandReportService`) + trang Nuxt copy khuôn `pages/sale/prepick-tracking`.

**Tech Stack:** Laravel 8 / PHP 7.4 (`/opt/homebrew/opt/php@7.4/bin/php`), PHPUnit chạy trên DB local `hrm_erp` (không RefreshDatabase — tự dọn), Nuxt 2 / Vue 2 (node 12 + heap 8192), Playwright (`HRM/e2e`).

**Spec:** `.plans/gop-db/bao-cao-nhu-cau-dich-vu/design.md` (21 quyết định) + `mockup.html` (bản chốt UI, token đo thật ở comment đầu file).

## Global Constraints

- **CHƯA ĐƯỢC CODE.** Theo `ERP-HRM/CLAUDE.md`: trước Task 1 phải hỏi user 1 câu riêng nêu phạm vi (repo `hrm-api` + `hrm-client`, nhánh `gop_db-bao-cao-nhu-cau-dich-vu` checkout từ `gop_db`, migration chạy vào DB local `hrm_erp`, insert 2 quyền vào DB local) và nhận câu "làm" rõ ràng.
- Nhánh: `gop_db-bao-cao-nhu-cau-dich-vu` ở **cả** `hrm-api` và `hrm-client`, checkout từ `gop_db`. Không `git stash` (repo dùng chung nhiều session) — chỉ `git add` đúng file của task.
- Không dùng `mysql2` / `DB_DATABASE_SECOND`; `provinces`, `wards`, `customers` đã có trong DB gộp `hrm_erp`.
- Trạng thái nhu cầu: `1 Đang theo dõi #0EA5E9` · `2 Đã lập báo giá #2563EB` · `3 Đã lập hợp đồng #16A34A` · `4 Đóng #6B7280`. Lý do đóng: `1 Hết hạn theo dõi` · `2 HĐ không duyệt` · `3 Huỷ duyệt HĐ` · `4 Đóng HĐ`. Chữ + màu do BE trả, FE dùng `V2BaseBadge :color`.
- Quyền: `Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty` (id **1660**) · `Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo công ty` (id **1661**), group `Báo cáo tổng hợp nhu cầu làm dịch vụ`, type 4, guard `api`. Không bypass super admin. Không gán sẵn role.
- Cấu hình: `general_regulations.service_demand_due_days`, default **30**, theo công ty. M dùng chung `demand_warning_days`.
- PHP: commit message tiếng Việt kiểu repo; cuối message thêm 2 dòng attribution của session.
- FE: mọi task đụng UI phải đo bằng Playwright MCP (số từ DOM) trước khi báo xong; không tự chạy cả bộ e2e trừ khi user yêu cầu; nếu chạy thì `--workers=1`.
- Chạy PHPUnit: `cd HRM/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter <Tên>`.

## Review Focus

1. **Báo giá "Lưu và duyệt" ngay lần tạo đầu** (store với status 2) — nhu cầu phải nhảy thẳng 1 → 2 và ghi người xử lý; không chỉ đường update. → test ở Task 5.
2. **Hai báo giá cùng chọn 1 nhu cầu** (người B mở form trước khi người A lưu nháp) — lần lưu thứ 2 phải bị chặn bằng lỗi validate, không ghi đè liên kết. → test ở Task 5.
3. **HĐ bị Không duyệt → sửa → trình lại → Duyệt** — nhu cầu phải từ Đóng sang Đã lập HĐ, xoá `close_reason`. → test ở Task 6.
4. **Người không có quyền nào nhưng là người xử lý** (lập báo giá, không chủ trì/không dự họp) — phải thấy nhu cầu đó trong báo cáo; người ngoài hoàn toàn không thấy. → test ở Task 10.
5. **Cron chạy 2 lần cùng ngày / chạy bù** — không cảnh báo trùng, `closed_at = due_date` chứ không phải ngày chạy. → test ở Task 7.

---

## Sơ đồ file

**hrm-api**
| File | Trách nhiệm |
|---|---|
| Create `Modules/Assign/Database/Migrations/2026_10_05_000001_create_meeting_service_demands_table.php` | bảng nhu cầu |
| Create `Modules/Assign/Database/Migrations/2026_10_05_000002_add_service_demand_due_days_to_general_regulations.php` | cột cấu hình N |
| Create `Modules/Assign/Entities/Meeting/MeetingServiceDemand.php` | entity + hằng số + text/màu |
| Create `Modules/Assign/Services/ServiceDemand/ServiceDemandStatusService.php` | MỌI chuyển trạng thái |
| Create `Modules/Assign/Services/ServiceDemand/ServiceDemandNotifier.php` | thông báo sắp hết hạn |
| Create `Modules/Assign/Services/Report/ServiceDemandReportService.php` | dữ liệu báo cáo + quyền |
| Create `Modules/Assign/Http/Controllers/Api/V1/ServiceDemandReportController.php` | API báo cáo |
| Create `Modules/Assign/Export/ServiceDemandExport.php` + `ServiceDemandListExport.php` + blade | Excel |
| Create `app/Console/Commands/Assign/CloseExpiredServiceDemandsCommand.php` | cron hết hạn + cảnh báo |
| Create `app/Console/Commands/Assign/BackfillServiceDemandsCommand.php` | sinh bù |
| Modify `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` (update ~L700, changeStatus ~L392) | gọi tạo nhu cầu |
| Modify `Modules/Assign/Services/MyJobService.php` (L23-35, L903-934, L1049-1101) + `app/Services/SettingHistory/Adapters/DeadlineConfigAdapter.php` + `Modules/Timesheet/Entities/GeneralRegulation.php` | cấu hình N |
| Modify `Modules/CustomerCare/Services/WrQuotationService.php` (store/update L389-397, delete L672, prefill L868) | gắn/gỡ nhu cầu |
| Modify `Modules/CustomerCare/Http/Requests/WrServiceQuotation/WrQuotationRequest.php` | rule `service_demand_id` |
| Modify `Modules/CustomerCare/Http/Controllers/V1/WrQuotationController.php` + `Routes/api.php` (~L370) | endpoint danh sách chọn |
| Modify `Modules/CustomerCare/Transformers/WrServiceQuotationResource/WrQuotationResource.php` | khối `service_demand` |
| Modify `Modules/CustomerCare/Services/WrServiceContractService.php` (L1411-1460) | hook HĐ |
| Modify `Modules/Assign/Routes/api.php` (~L1220) · `app/Console/Kernel.php` (~L71) · `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | route · lịch · quyền |
| Create `tests/Feature/ServiceDemand/*Test.php` + `tests/Feature/ServiceDemand/ServiceDemandFixture.php` | test |

**hrm-client**
| File | Trách nhiệm |
|---|---|
| Create `pages/assign/report/service-demand/{index.vue,api.js,format.js}` | trang báo cáo |
| Create `pages/assign/report/service-demand/components/{DemandSummary,DemandTable,DemandListModal,PrintOptionsModal,DrillNum,InfoTip}.vue` | khối con |
| Modify `components/subsystem-menu/presale.js` (L119-124) | menu |
| Modify `pages/customer-care/wr-quotations/components/WrQuotationForm.vue` (L96-110, L931-947) + `_id/index.vue` | ô chọn nhu cầu |
| Modify `pages/assign/settings/index.vue` (~L1224-1250, L1649, L2287) | ô cấu hình N |

**HRM/e2e** (không nằm trong git — chỉ lưu file)
| Create `tests/assign/service-demand.api.spec.ts` · `tests/assign/service-demand.spec.ts` · `utils/serviceDemandFixture.ts` |

---

### Task 0: Xin phép code + tạo nhánh

- [x] **Step 1:** Hỏi user (1 câu riêng): *"Bắt đầu code feature nhu cầu làm dịch vụ: repo hrm-api + hrm-client, nhánh `gop_db-bao-cao-nhu-cau-dich-vu` từ `gop_db`, 2 migration chạy vào DB local `hrm_erp`, insert 2 quyền id 1660/1661 vào DB local. Làm không?"* — chỉ tiếp khi nhận "làm".
- [x] **Step 2:** Kiểm id quyền ngay lúc này (có thể đã bị nhánh khác chiếm):

```bash
cd HRM/hrm-api
for b in $(git branch -a --format='%(refname:short)'); do git show "$b:Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php" 2>/dev/null | grep -o "'id' => 166[0-9]"; done | sort -u
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo json_encode(DB::table("permissions")->whereBetween("id",[1655,1670])->pluck("id"));'
```
Expected: không thấy 1660/1661. Nếu đã bị chiếm → chọn cặp trống kế tiếp và **sửa mọi chỗ 1660/1661 trong plan này**.

- [x] **Step 3:** Tạo nhánh ở cả 2 repo:

```bash
cd HRM/hrm-api && git checkout gop_db && git pull && git checkout -b gop_db-bao-cao-nhu-cau-dich-vu
cd ../hrm-client && git checkout gop_db && git pull && git checkout -b gop_db-bao-cao-nhu-cau-dich-vu
```

---

### Task 1: Bảng + entity + cột cấu hình

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_10_05_000001_create_meeting_service_demands_table.php`
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_10_05_000002_add_service_demand_due_days_to_general_regulations.php`
- Create: `hrm-api/Modules/Assign/Entities/Meeting/MeetingServiceDemand.php`
- Modify: `hrm-api/Modules/Timesheet/Entities/GeneralRegulation.php` ($fillable, cạnh `demand_warning_days`)
- Test: `hrm-api/tests/Feature/ServiceDemand/MeetingServiceDemandEntityTest.php`

**Interfaces — Produces:**
- `MeetingServiceDemand` const `DANG_THEO_DOI=1, DA_LAP_BAO_GIA=2, DA_LAP_HOP_DONG=3, DA_DONG=4`; `CLOSE_EXPIRED=1, CLOSE_CONTRACT_REJECTED=2, CLOSE_CONTRACT_UNAPPROVED=3, CLOSE_CONTRACT_CLOSED=4`; `STATUS_TEXT`, `STATUS_COLOR`, `CLOSE_REASON_TEXT`; accessors `status_text`, `status_color`, `close_reason_text`; relations `meeting()`, `quotation()`, `contract()`, `handler()`.
- `MeetingServiceDemand::DEFAULT_DUE_DAYS = 30`.

- [x] **Step 1: Viết test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Illuminate\Support\Facades\Schema;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Tests\TestCase;

class MeetingServiceDemandEntityTest extends TestCase
{
    public function test_bang_va_cot_cau_hinh_ton_tai(): void
    {
        $this->assertTrue(Schema::hasTable('meeting_service_demands'));
        foreach (['meeting_id', 'company_id', 'customer_id', 'status', 'close_reason', 'tracking_start_date',
            'due_days_snapshot', 'due_date', 'wr_service_quotation_id', 'handler_employee_id', 'quoted_at',
            'wr_service_contract_id', 'contracted_at', 'closed_at', 'expiry_warned_at'] as $col) {
            $this->assertTrue(Schema::hasColumn('meeting_service_demands', $col), $col);
        }
        $this->assertTrue(Schema::hasColumn('general_regulations', 'service_demand_due_days'));
    }

    public function test_text_va_mau_trang_thai_do_be_tra(): void
    {
        $d = new MeetingServiceDemand(['status' => MeetingServiceDemand::DA_DONG, 'close_reason' => MeetingServiceDemand::CLOSE_CONTRACT_REJECTED]);
        $this->assertSame('Đóng', $d->status_text);
        $this->assertSame('#6B7280', $d->status_color);
        $this->assertSame('HĐ không duyệt', $d->close_reason_text);

        $d->status = MeetingServiceDemand::DA_LAP_BAO_GIA;
        $this->assertSame('Đã lập báo giá', $d->status_text);
        $this->assertSame('#2563EB', $d->status_color);
    }
}
```

- [x] **Step 2: Chạy, xác nhận đỏ**

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingServiceDemandEntityTest`
Expected: FAIL (`Class ... MeetingServiceDemand not found` / hasTable false)

- [x] **Step 3: Migration bảng**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Nhu cầu làm dịch vụ (sửa chữa – bảo dưỡng) — feature bao-cao-nhu-cau-dich-vu.
 * 1 meeting "Họp tìm hiểu & giới thiệu SP" Hoàn thành + Q4 = Có  ->  đúng 1 dòng (unique meeting_id).
 * Liên kết báo giá nằm Ở ĐÂY (unique) — 1 nhu cầu ↔ 1 báo giá; không thêm cột vào wr_service_quotations.
 */
class CreateMeetingServiceDemandsTable extends Migration
{
    public function up()
    {
        if (Schema::hasTable('meeting_service_demands')) {
            return;
        }
        Schema::create('meeting_service_demands', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('meeting_id')->unique();
            $table->unsignedInteger('company_id')->nullable()->comment('Công ty của NGƯỜI CHỦ TRÌ lúc tạo');
            $table->unsignedInteger('customer_id')->nullable();
            $table->unsignedTinyInteger('status')->default(1)->comment('1 Đang theo dõi · 2 Đã lập báo giá · 3 Đã lập hợp đồng · 4 Đóng');
            $table->unsignedTinyInteger('close_reason')->nullable()->comment('1 Hết hạn · 2 HĐ không duyệt · 3 Huỷ duyệt HĐ · 4 Đóng HĐ');
            $table->date('tracking_start_date');
            $table->unsignedSmallInteger('due_days_snapshot')->default(0);
            $table->date('due_date')->nullable()->comment('null khi N = 0 (không hết hạn)');
            $table->unsignedBigInteger('wr_service_quotation_id')->nullable()->unique();
            $table->unsignedInteger('handler_employee_id')->nullable()->comment('Người xử lý = người tạo báo giá');
            $table->dateTime('quoted_at')->nullable();
            $table->unsignedBigInteger('wr_service_contract_id')->nullable();
            $table->dateTime('contracted_at')->nullable();
            $table->dateTime('closed_at')->nullable();
            $table->dateTime('expiry_warned_at')->nullable();
            $table->timestamps();

            $table->index(['status', 'due_date']);
            $table->index('company_id');
            $table->index(['customer_id', 'status']);
            $table->index('wr_service_contract_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('meeting_service_demands');
    }
}
```

- [x] **Step 4: Migration cột cấu hình**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/** N = "Thời gian theo dõi nhu cầu dịch vụ (ngày)" — theo công ty, default 30 (feature bao-cao-nhu-cau-dich-vu) */
class AddServiceDemandDueDaysToGeneralRegulations extends Migration
{
    public function up()
    {
        if (!Schema::hasColumn('general_regulations', 'service_demand_due_days')) {
            Schema::table('general_regulations', function (Blueprint $table) {
                $table->unsignedSmallInteger('service_demand_due_days')->default(30)
                    ->comment('Thời gian theo dõi nhu cầu làm dịch vụ (ngày); 0 = không hết hạn');
            });
        }
    }

    public function down()
    {
        if (Schema::hasColumn('general_regulations', 'service_demand_due_days')) {
            Schema::table('general_regulations', function (Blueprint $table) {
                $table->dropColumn('service_demand_due_days');
            });
        }
    }
}
```

- [x] **Step 5: Entity**

```php
<?php

namespace Modules\Assign\Entities\Meeting;

use Illuminate\Database\Eloquent\Model;
use Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation;
use Modules\Human\Entities\Employee;

/**
 * Nhu cầu làm dịch vụ. ĐỪNG đổi status bằng forceFill rải rác — mọi chuyển trạng thái đi qua
 * Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService.
 */
class MeetingServiceDemand extends Model
{
    protected $table = 'meeting_service_demands';

    const DANG_THEO_DOI = 1;
    const DA_LAP_BAO_GIA = 2;
    const DA_LAP_HOP_DONG = 3;
    const DA_DONG = 4;

    const CLOSE_EXPIRED = 1;
    const CLOSE_CONTRACT_REJECTED = 2;
    const CLOSE_CONTRACT_UNAPPROVED = 3;
    const CLOSE_CONTRACT_CLOSED = 4;

    const DEFAULT_DUE_DAYS = 30;

    const STATUS_TEXT = [
        self::DANG_THEO_DOI => 'Đang theo dõi',
        self::DA_LAP_BAO_GIA => 'Đã lập báo giá',
        self::DA_LAP_HOP_DONG => 'Đã lập hợp đồng',
        self::DA_DONG => 'Đóng',
    ];

    /** Bảng 9 màu chuẩn (CLAUDE.md): theo dõi · đang thực hiện · hoàn thành · đã đóng */
    const STATUS_COLOR = [
        self::DANG_THEO_DOI => '#0EA5E9',
        self::DA_LAP_BAO_GIA => '#2563EB',
        self::DA_LAP_HOP_DONG => '#16A34A',
        self::DA_DONG => '#6B7280',
    ];

    const CLOSE_REASON_TEXT = [
        self::CLOSE_EXPIRED => 'Hết hạn theo dõi',
        self::CLOSE_CONTRACT_REJECTED => 'HĐ không duyệt',
        self::CLOSE_CONTRACT_UNAPPROVED => 'Huỷ duyệt HĐ',
        self::CLOSE_CONTRACT_CLOSED => 'Đóng HĐ',
    ];

    protected $fillable = [
        'meeting_id', 'company_id', 'customer_id', 'status', 'close_reason', 'tracking_start_date',
        'due_days_snapshot', 'due_date', 'wr_service_quotation_id', 'handler_employee_id', 'quoted_at',
        'wr_service_contract_id', 'contracted_at', 'closed_at', 'expiry_warned_at',
    ];

    protected $casts = [
        'tracking_start_date' => 'date',
        'due_date' => 'date',
        'quoted_at' => 'datetime',
        'contracted_at' => 'datetime',
        'closed_at' => 'datetime',
        'expiry_warned_at' => 'datetime',
    ];

    public function meeting()
    {
        return $this->belongsTo(Meeting::class, 'meeting_id');
    }

    public function quotation()
    {
        return $this->belongsTo(WrServiceQuotation::class, 'wr_service_quotation_id');
    }

    public function contract()
    {
        return $this->belongsTo(WrServiceContract::class, 'wr_service_contract_id');
    }

    public function handler()
    {
        return $this->belongsTo(Employee::class, 'handler_employee_id');
    }

    public function getStatusTextAttribute(): string
    {
        return self::STATUS_TEXT[(int) $this->status] ?? '';
    }

    public function getStatusColorAttribute(): string
    {
        return self::STATUS_COLOR[(int) $this->status] ?? '';
    }

    public function getCloseReasonTextAttribute(): ?string
    {
        return $this->close_reason ? (self::CLOSE_REASON_TEXT[(int) $this->close_reason] ?? null) : null;
    }
}
```

- [x] **Step 6:** Thêm `'service_demand_due_days',` vào `$fillable` của `Modules/Timesheet/Entities/GeneralRegulation.php` ngay sau `'demand_warning_days',`.
- [x] **Step 7: Chạy migration + test**

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan config:clear
/opt/homebrew/opt/php@7.4/bin/php artisan module:migrate Assign
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit --filter MeetingServiceDemandEntityTest
```
Expected: 2 tests PASS. (Nếu `module:migrate` không có, dùng `php artisan migrate --path=Modules/Assign/Database/Migrations/2026_10_05_000001_create_meeting_service_demands_table.php` rồi file thứ 2.)

- [x] **Step 8: Commit**

```bash
git add Modules/Assign/Database/Migrations/2026_10_05_00000{1,2}_*.php Modules/Assign/Entities/Meeting/MeetingServiceDemand.php Modules/Timesheet/Entities/GeneralRegulation.php tests/Feature/ServiceDemand/MeetingServiceDemandEntityTest.php
git commit -m "Nhu cầu làm dịch vụ: bảng meeting_service_demands + cấu hình N theo công ty"
```

---

### Task 2: Fixture test + `ServiceDemandStatusService`

**Files:**
- Create: `hrm-api/tests/Feature/ServiceDemand/ServiceDemandFixture.php`
- Create: `hrm-api/Modules/Assign/Services/ServiceDemand/ServiceDemandStatusService.php`
- Test: `hrm-api/tests/Feature/ServiceDemand/ServiceDemandStatusServiceTest.php`

**Interfaces — Produces** (`ServiceDemandStatusService`, resolve bằng `app()`):
- `createForMeeting(Meeting $m, ?Carbon $startDate = null): ?MeetingServiceDemand` — idempotent; null khi meeting không đủ điều kiện.
- `dueDaysForCompany(?int $companyId): int`
- `syncQuotationLink(WrServiceQuotation $q, ?int $demandId): void` — gắn/gỡ; nếu `$q->status == 2` thì gọi `onQuotationApproved`.
- `onQuotationApproved(WrServiceQuotation $q): void`
- `unlinkQuotation(WrServiceQuotation $q): void`
- `onContractApproved(WrServiceContract $c): void`
- `onContractClosed(WrServiceContract $c, int $reason): void`
- `closeExpired(MeetingServiceDemand $d): void` — `closed_at = due_date`
- `isEligibleMeeting(Meeting $m): bool`

- [x] **Step 1: Fixture (dựng dữ liệu bằng replicate bản ghi thật, tự dọn)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Modules\Assign\Entities\MeetingType;
use Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation;

/**
 * Dựng dữ liệu cho test nhu cầu dịch vụ trên DB local thật (không RefreshDatabase — khớp các test
 * Feature khác của repo). Mọi bản ghi tạo ra được ghi lại để tearDown() xoá.
 * Dùng replicate() bản ghi thật cùng loại để khỏi phải biết hết cột NOT NULL.
 */
trait ServiceDemandFixture
{
    protected $fxMeetingIds = [];
    protected $fxQuotationIds = [];
    protected $fxContractIds = [];

    protected function makeMeeting(array $attrs = []): Meeting
    {
        $typeId = MeetingType::where('code', MeetingType::CODE_PRODUCT_INTRO)->value('id');
        $src = Meeting::where('meeting_type_id', $typeId)->whereNotNull('customer_id')->orderByDesc('id')->firstOrFail();
        $m = $src->replicate();
        $m->code = 'PHPUNIT-NCDV-' . uniqid();
        $m->fill(array_merge([
            'status' => Meeting::HOAN_THANH,
            'has_maintenance_demand' => 1,
            'completed_at' => now()->subDays(2),
        ], $attrs));
        $m->saveQuietly();
        $this->fxMeetingIds[] = $m->id;

        return $m->fresh();
    }

    protected function makeQuotation(int $customerId, int $status = WrServiceQuotation::STATUS_QT_CREATING, ?int $createdBy = null): WrServiceQuotation
    {
        $src = WrServiceQuotation::where('type', WrServiceQuotation::TYPE_QUOTATION)->orderByDesc('id')->firstOrFail();
        $q = $src->replicate();
        $q->code = 'PHPUNIT-BG-' . uniqid();
        $q->customer_id = $customerId;
        $q->status = $status;
        $q->created_by = $createdBy ?: $src->created_by;
        $q->saveQuietly();
        $this->fxQuotationIds[] = $q->id;

        return $q->fresh();
    }

    protected function makeContract(int $quotationId, int $status): WrServiceContract
    {
        $src = WrServiceContract::where('type', WrServiceContract::TYPE_CONTRACT)->orderByDesc('id')->firstOrFail();
        $c = $src->replicate();
        $c->code = 'PHPUNIT-HD-' . uniqid();
        $c->wr_service_quotation_id = $quotationId;
        $c->status = $status;
        $c->saveQuietly();
        $this->fxContractIds[] = $c->id;

        return $c->fresh();
    }

    protected function cleanupServiceDemandFixture(): void
    {
        MeetingServiceDemand::whereIn('meeting_id', $this->fxMeetingIds)->delete();
        DB::table('catalog_histories')->whereIn('table_id', $this->fxQuotationIds)->where('table_name', 'wr_service_quotations')->delete();
        DB::table('catalog_histories')->whereIn('table_id', $this->fxContractIds)->where('table_name', 'wr_service_contracts')->delete();
        WrServiceContract::whereIn('id', $this->fxContractIds)->delete();
        WrServiceQuotation::whereIn('id', $this->fxQuotationIds)->delete();
        Meeting::whereIn('id', $this->fxMeetingIds)->forceDelete();
        $this->fxMeetingIds = $this->fxQuotationIds = $this->fxContractIds = [];
    }
}
```

> Nếu `Meeting` không dùng SoftDeletes thì `forceDelete()` → đổi thành `delete()`; kiểm bằng `grep -n SoftDeletes Modules/Assign/Entities/Meeting/Meeting.php` trước khi chạy.

- [x] **Step 2: Viết test service (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Carbon\Carbon;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract as C;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation as Q;
use Tests\TestCase;

class ServiceDemandStatusServiceTest extends TestCase
{
    use ServiceDemandFixture;

    private ServiceDemandStatusService $svc;

    protected function setUp(): void
    {
        parent::setUp();
        $this->svc = app(ServiceDemandStatusService::class);
    }

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    public function test_tao_nhu_cau_khi_meeting_du_dieu_kien_va_idempotent(): void
    {
        $m = $this->makeMeeting();
        $d = $this->svc->createForMeeting($m);
        $this->assertNotNull($d);
        $this->assertSame(D::DANG_THEO_DOI, (int) $d->status);
        $this->assertSame($m->completed_at->toDateString(), $d->tracking_start_date->toDateString());
        $n = $this->svc->dueDaysForCompany($d->company_id);
        $this->assertSame($n, (int) $d->due_days_snapshot);
        $this->assertSame($n ? $d->tracking_start_date->copy()->addDays($n)->toDateString() : null, optional($d->due_date)->toDateString());

        $this->svc->createForMeeting($m);
        $this->assertSame(1, D::where('meeting_id', $m->id)->count());
    }

    public function test_khong_tao_khi_q4_khong_hoac_chua_hoan_thanh(): void
    {
        $this->assertNull($this->svc->createForMeeting($this->makeMeeting(['has_maintenance_demand' => 0])));
        $this->assertNull($this->svc->createForMeeting($this->makeMeeting(['status' => Meeting::CHOT_LICH])));
    }

    public function test_bao_gia_nhap_chi_khoa_khong_doi_trang_thai(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id, Q::STATUS_QT_CREATING);
        $this->svc->syncQuotationLink($q, $d->id);
        $d->refresh();
        $this->assertSame($q->id, (int) $d->wr_service_quotation_id);
        $this->assertSame(D::DANG_THEO_DOI, (int) $d->status);
        $this->assertNull($d->handler_employee_id);
    }

    public function test_bao_gia_duyet_chuyen_da_lap_bao_gia_va_ghi_nguoi_xu_ly(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id, Q::STATUS_QT_APPROVED, 24);
        $this->svc->syncQuotationLink($q, $d->id);
        $d->refresh();
        $this->assertSame(D::DA_LAP_BAO_GIA, (int) $d->status);
        $this->assertSame(24, (int) $d->handler_employee_id);
        $this->assertNotNull($d->quoted_at);
    }

    public function test_go_lien_ket_giu_nguyen_trang_thai(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id);
        $this->svc->syncQuotationLink($q, $d->id);
        $this->svc->syncQuotationLink($q, null);
        $d->refresh();
        $this->assertNull($d->wr_service_quotation_id);
        $this->assertSame(D::DANG_THEO_DOI, (int) $d->status);
    }

    public function test_duyet_bao_gia_sau_khi_nhu_cau_da_dong_vi_het_han_van_ghi_de(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id);
        $this->svc->syncQuotationLink($q, $d->id);
        $d->forceFill(['due_date' => Carbon::yesterday()])->save();
        $this->svc->closeExpired($d->fresh());
        $q->status = Q::STATUS_QT_APPROVED;
        $this->svc->onQuotationApproved($q);
        $d->refresh();
        $this->assertSame(D::DA_LAP_BAO_GIA, (int) $d->status);
        $this->assertNull($d->close_reason);
        $this->assertNull($d->closed_at);
    }

    public function test_hd_duyet_roi_khong_duyet_roi_duyet_lai(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id, Q::STATUS_QT_APPROVED);
        $this->svc->syncQuotationLink($q, $d->id);
        $c = $this->makeContract($q->id, C::HD_REJECTED);

        $this->svc->onContractClosed($c, D::CLOSE_CONTRACT_REJECTED);
        $d->refresh();
        $this->assertSame(D::DA_DONG, (int) $d->status);
        $this->assertSame(D::CLOSE_CONTRACT_REJECTED, (int) $d->close_reason);
        $this->assertSame($q->id, (int) $d->wr_service_quotation_id);

        $this->svc->onContractApproved($c);
        $d->refresh();
        $this->assertSame(D::DA_LAP_HOP_DONG, (int) $d->status);
        $this->assertSame($c->id, (int) $d->wr_service_contract_id);
        $this->assertNull($d->close_reason);
    }

    public function test_dong_vi_het_han_closed_at_bang_due_date(): void
    {
        $d = $this->svc->createForMeeting($this->makeMeeting());
        $d->forceFill(['due_date' => Carbon::parse('2026-01-15')])->save();
        $this->svc->closeExpired($d->fresh());
        $d->refresh();
        $this->assertSame(D::DA_DONG, (int) $d->status);
        $this->assertSame(D::CLOSE_EXPIRED, (int) $d->close_reason);
        $this->assertSame('2026-01-15', $d->closed_at->toDateString());
    }
}
```

- [x] **Step 3:** Run `--filter ServiceDemandStatusServiceTest` → FAIL (class not found).
- [x] **Step 4: Service**

```php
<?php

namespace Modules\Assign\Services\ServiceDemand;

use Carbon\Carbon;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Modules\Assign\Entities\MeetingType;
use Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Entities\GeneralRegulation;

/**
 * NƠI DUY NHẤT đổi trạng thái nhu cầu làm dịch vụ (design.md mục 4).
 * Bất biến: chứng từ phía sau được DUYỆT luôn ghi đè trạng thái (kể cả khi nhu cầu đang Đóng).
 */
class ServiceDemandStatusService
{
    public function isEligibleMeeting(Meeting $m): bool
    {
        return (int) $m->status === Meeting::HOAN_THANH
            && (int) $m->has_maintenance_demand === 1
            && optional($m->meetingType)->code === MeetingType::CODE_PRODUCT_INTRO;
    }

    /** N theo công ty; công ty chưa có cấu hình -> mặc định 30 */
    public function dueDaysForCompany(?int $companyId): int
    {
        $config = $companyId ? GeneralRegulation::where('company_id', $companyId)->first() : null;

        return $config && $config->service_demand_due_days !== null
            ? max(0, (int) $config->service_demand_due_days)
            : MeetingServiceDemand::DEFAULT_DUE_DAYS;
    }

    /**
     * @param Carbon|null $startDate mốc bắt đầu tính hạn; null = ngày hoàn thành meeting.
     *        Lệnh sinh bù truyền NGÀY DEPLOY (design #13).
     */
    public function createForMeeting(Meeting $m, ?Carbon $startDate = null): ?MeetingServiceDemand
    {
        $m->loadMissing('meetingType');
        if (!$this->isEligibleMeeting($m)) {
            return null;
        }

        $existing = MeetingServiceDemand::where('meeting_id', $m->id)->first();
        if ($existing) {
            return $existing;
        }

        $start = ($startDate ?: Carbon::parse($m->completed_at ?: now()))->copy()->startOfDay();
        // Công ty / phòng ban tính theo NGƯỜI CHỦ TRÌ (design #19), không theo meetings.company_id (người tạo)
        $hostCompanyId = optional(optional(Employee::with('info')->find($m->host_employee_id))->info)->company_id ?: $m->company_id;
        $n = $this->dueDaysForCompany($hostCompanyId ? (int) $hostCompanyId : null);

        return MeetingServiceDemand::create([
            'meeting_id' => $m->id,
            'company_id' => $hostCompanyId,
            'customer_id' => $m->customer_id,
            'status' => MeetingServiceDemand::DANG_THEO_DOI,
            'tracking_start_date' => $start->toDateString(),
            'due_days_snapshot' => $n,
            'due_date' => $n > 0 ? $start->copy()->addDays($n)->toDateString() : null,
        ]);
    }

    /** Gắn / đổi / gỡ nhu cầu của 1 báo giá. Gọi trong transaction của store/update báo giá. */
    public function syncQuotationLink(WrServiceQuotation $q, ?int $demandId): void
    {
        MeetingServiceDemand::where('wr_service_quotation_id', $q->id)
            ->when($demandId, function ($query) use ($demandId) {
                $query->where('id', '!=', $demandId);
            })
            ->update(['wr_service_quotation_id' => null]);

        if ($demandId) {
            MeetingServiceDemand::where('id', $demandId)->update(['wr_service_quotation_id' => $q->id]);
        }

        if ((int) $q->status === WrServiceQuotation::STATUS_QT_APPROVED) {
            $this->onQuotationApproved($q);
        }
    }

    public function onQuotationApproved(WrServiceQuotation $q): void
    {
        $d = MeetingServiceDemand::where('wr_service_quotation_id', $q->id)->first();
        if (!$d || (int) $d->status === MeetingServiceDemand::DA_LAP_HOP_DONG) {
            return;
        }
        $d->forceFill([
            'status' => MeetingServiceDemand::DA_LAP_BAO_GIA,
            'handler_employee_id' => $q->created_by,
            'quoted_at' => now(),
            'close_reason' => null,
            'closed_at' => null,
        ])->save();
    }

    /** Xoá báo giá (chỉ khi còn nháp): gỡ liên kết, giữ trạng thái (design #8) */
    public function unlinkQuotation(WrServiceQuotation $q): void
    {
        MeetingServiceDemand::where('wr_service_quotation_id', $q->id)->update(['wr_service_quotation_id' => null]);
    }

    public function onContractApproved(WrServiceContract $c): void
    {
        $d = $this->demandOfContract($c);
        if (!$d) {
            return;
        }
        $d->forceFill([
            'status' => MeetingServiceDemand::DA_LAP_HOP_DONG,
            'wr_service_contract_id' => $c->id,
            'contracted_at' => now(),
            'close_reason' => null,
            'closed_at' => null,
        ])->save();
    }

    public function onContractClosed(WrServiceContract $c, int $reason): void
    {
        $d = $this->demandOfContract($c);
        if (!$d) {
            return;
        }
        $d->forceFill([
            'status' => MeetingServiceDemand::DA_DONG,
            'close_reason' => $reason,
            'wr_service_contract_id' => $c->id,
            'closed_at' => now(),
        ])->save();
    }

    /** closed_at = CHÍNH ngày hết hạn, không phải ngày cron chạy (cron chạy bù vẫn đúng kỳ) */
    public function closeExpired(MeetingServiceDemand $d): void
    {
        if ((int) $d->status !== MeetingServiceDemand::DANG_THEO_DOI || !$d->due_date) {
            return;
        }
        $d->forceFill([
            'status' => MeetingServiceDemand::DA_DONG,
            'close_reason' => MeetingServiceDemand::CLOSE_EXPIRED,
            'closed_at' => $d->due_date->copy()->startOfDay(),
        ])->save();
    }

    private function demandOfContract(WrServiceContract $c): ?MeetingServiceDemand
    {
        if ((int) $c->type !== WrServiceContract::TYPE_CONTRACT || !$c->wr_service_quotation_id) {
            return null;
        }

        return MeetingServiceDemand::where('wr_service_quotation_id', $c->wr_service_quotation_id)->first();
    }
}
```

> Kiểm trước khi chạy: `Meeting` có quan hệ `meetingType()` chưa (`grep -n "function meetingType\|function type(" Modules/Assign/Entities/Meeting/Meeting.php`). Tên khác thì thay trong `isEligibleMeeting` + `loadMissing`. `EmployeeInfo` có `company_id` (đã kiểm: có).

- [x] **Step 5:** Run `--filter ServiceDemandStatusServiceTest` → 8 PASS.
- [x] **Step 6: Commit** — `git add tests/Feature/ServiceDemand/ServiceDemandFixture.php tests/Feature/ServiceDemand/ServiceDemandStatusServiceTest.php Modules/Assign/Services/ServiceDemand/ServiceDemandStatusService.php` · message `Nhu cầu làm dịch vụ: service chuyển trạng thái + test vòng đời`.

---

### Task 3: Móc vào meeting Hoàn thành

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` — `update` sau dòng `$this->service->syncInvestmentScopes(...)` (~L701); `changeStatus` sau `$entity->save();` (~L392)
- Test: `hrm-api/tests/Feature/ServiceDemand/MeetingHookTest.php`

**Interfaces — Consumes:** `ServiceDemandStatusService::createForMeeting(Meeting): ?MeetingServiceDemand`.

- [x] **Step 1: Test (đỏ)** — gọi thẳng controller qua HTTP với user là người tạo meeting.

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Modules\Human\Entities\Employee;
use Tests\TestCase;

class MeetingHookTest extends TestCase
{
    use ServiceDemandFixture;

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    public function test_change_status_sang_hoan_thanh_sinh_nhu_cau(): void
    {
        $m = $this->makeMeeting(['status' => Meeting::CHOT_LICH, 'completed_at' => null]);
        $this->actingAs(Employee::findOrFail($m->created_by), 'api')
            ->postJson('/api/v1/assign/meeting/' . $m->id . '/change-status', ['status' => Meeting::HOAN_THANH])
            ->assertStatus(200);

        $this->assertSame(1, MeetingServiceDemand::where('meeting_id', $m->id)->count());
    }
}
```

> Nếu `actingAs(..., 'api')` không qua được middleware JWT của repo: thay bằng `$token = auth('api')->login($employee)` + header `Authorization: Bearer`. Xem cách `tests/Feature/MeetingRoomBookingServiceRequestTest.php` đăng nhập và làm y vậy.

- [x] **Step 2:** Run `--filter MeetingHookTest` → FAIL (count 0).
- [x] **Step 3: Sửa `update`** — thêm ngay sau `$this->service->syncInvestmentScopes($request->investment_scopes, $entity);`:

```php
            // Nhu cầu làm dịch vụ (bao-cao-nhu-cau-dich-vu): meeting giới thiệu SP vừa Hoàn thành + Q4 = Có
            // -> sinh 1 nhu cầu. Idempotent, gọi mỗi lần lưu cũng an toàn.
            app(\Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService::class)->createForMeeting($entity->fresh());
```

- [x] **Step 4: Sửa `changeStatus`** — thêm ngay sau `$entity->save();` (trong try):

```php
            // API này đổi được sang Hoàn thành mà KHÔNG qua update() -> phải sinh nhu cầu ở đây nữa
            if ((int) $newStatus === Meeting::HOAN_THANH) {
                app(\Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService::class)->createForMeeting($entity->fresh());
            }
```

- [x] **Step 5:** Run `--filter MeetingHookTest` → PASS. Run lại `--filter ServiceDemand` → toàn bộ PASS.
- [x] **Step 6: Commit** — `MeetingController.php` + `MeetingHookTest.php`, message `Nhu cầu làm dịch vụ: sinh nhu cầu khi meeting giới thiệu SP hoàn thành`.

---

### Task 4: Cấu hình N (BE + màn Cấu hình hạn)

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/MyJobService.php` — `DEADLINE_TRACKED_FIELDS` (L23-35), `getDeadlineConfig` (L903-934), `saveDeadlineConfig` (L1049-1101)
- Modify: `hrm-api/app/Services/SettingHistory/Adapters/DeadlineConfigAdapter.php` (nhãn L60-72)
- Modify: `hrm-client/pages/assign/settings/index.vue` (input ~L1224-1250, data L1649-1658, `getDefaultDeadlineConfig` L2287-2300)
- Test: `hrm-api/tests/Feature/ServiceDemand/DeadlineConfigTest.php`

- [x] **Step 1: Test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Illuminate\Http\Request;
use Modules\Assign\Services\MyJobService;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Entities\GeneralRegulation;
use Tests\TestCase;

class DeadlineConfigTest extends TestCase
{
    public function test_luu_va_doc_service_demand_due_days(): void
    {
        $user = Employee::findOrFail(24);
        $this->actingAs($user, 'api');
        $svc = app(MyJobService::class);
        $row = GeneralRegulation::where('company_id', $user->current_company_role)->first();
        $old = $row ? $row->service_demand_due_days : null;

        $payload = array_merge($svc->getDeadlineConfig(), ['service_demand_due_days' => 45]);
        $saved = $svc->saveDeadlineConfig(new Request($payload));
        $this->assertSame(45, (int) $saved['service_demand_due_days']);
        $this->assertSame(45, (int) $svc->getDeadlineConfig()['service_demand_due_days']);

        if ($old !== null) {
            GeneralRegulation::where('company_id', $user->current_company_role)->update(['service_demand_due_days' => $old]);
        }
    }
}
```

- [x] **Step 2:** Run → FAIL (undefined index).
- [x] **Step 3: BE** — trong `MyJobService`:
  - `DEADLINE_TRACKED_FIELDS`: thêm `'service_demand_due_days',` (comment `// bao-cao-nhu-cau-dich-vu — N theo dõi nhu cầu dịch vụ`).
  - `getDeadlineConfig`: nhánh default thêm `'service_demand_due_days' => MeetingServiceDemand::DEFAULT_DUE_DAYS,`; nhánh có cấu hình thêm `'service_demand_due_days' => $generalRegulation->service_demand_due_days ?? MeetingServiceDemand::DEFAULT_DUE_DAYS,`.
  - `saveDeadlineConfig`: cả `create([...])` và `update([...])` thêm `'service_demand_due_days' => max(0, (int) ($request->service_demand_due_days ?? MeetingServiceDemand::DEFAULT_DUE_DAYS)),`; mảng return thêm `'service_demand_due_days' => $generalRegulation->service_demand_due_days,` (thiếu là FE mất giá trị sau khi Lưu — bài học #11377 BUG 1).
  - `use Modules\Assign\Entities\Meeting\MeetingServiceDemand;` đầu file.
  - `DeadlineConfigAdapter`: thêm nhãn `'service_demand_due_days' => 'Thời gian theo dõi nhu cầu dịch vụ (ngày)',` cạnh `demand_warning_days`.
- [x] **Step 4:** Run `--filter DeadlineConfigTest` → PASS.
- [x] **Step 5: FE** — `pages/assign/settings/index.vue`: copy nguyên khối input của `demand_warning_days` (~L1224-1250) đặt NGAY SAU nó, đổi:
  - nhãn `Thời gian theo dõi nhu cầu dịch vụ`, đơn vị `ngày`
  - `v-model.number="deadlineConfig.service_demand_due_days"`, `name="service_demand_due_days"`
  - `v-validate="'required|non_negative_integer|max_value:3650'"`, thông báo lỗi theo `errors.first('service_demand_due_days')`
  - data default (L1649-1658) + `getDefaultDeadlineConfig` (L2287-2300): `service_demand_due_days: 30`
  - `saveDeadlineConfig` (L2257-2284): validate thêm field này giống `demand_warning_days`.
- [x] **Step 6: Kiểm Playwright MCP** trên `http://127.0.0.1:3000/assign/settings` › Quản lý dự án › Cấu hình hạn: đo dòng mới nằm ngay dưới "Cảnh báo trước khi đóng nhu cầu" (toạ độ y lớn hơn đúng 1 hàng), nhập 45 → Lưu → reload → ô vẫn 45; nhập -1 → hiện lỗi, không gọi API. Trả lại giá trị cũ sau khi kiểm.
- [x] **Step 7: Commit** cả 2 repo (mỗi repo 1 commit), message `Cấu hình hạn: thêm thời gian theo dõi nhu cầu dịch vụ`.

---

### Task 5: Báo giá DV — chọn nhu cầu (BE)

**Files:**
- Modify: `hrm-api/Modules/CustomerCare/Http/Requests/WrServiceQuotation/WrQuotationRequest.php` (cuối `rules()`)
- Modify: `hrm-api/Modules/CustomerCare/Services/WrQuotationService.php` (store/update L389-397, delete L672, prefillFromQuotation L868)
- Modify: `hrm-api/Modules/CustomerCare/Http/Controllers/V1/WrQuotationController.php` (method mới `serviceDemands`, eager-load ở `findForRead` L510)
- Modify: `hrm-api/Modules/CustomerCare/Routes/api.php` (route tĩnh trước `/{id}`, cạnh `/prefill`)
- Modify: `hrm-api/Modules/CustomerCare/Transformers/WrServiceQuotationResource/WrQuotationResource.php`
- Test: `hrm-api/tests/Feature/ServiceDemand/QuotationLinkTest.php`

**Interfaces:**
- Consumes: `syncQuotationLink`, `unlinkQuotation`.
- Produces: `GET /api/v1/customer-care/wr-quotations/service-demands?customer_id=&include_id=` → `data: [{id, meeting_id, meeting_code, meeting_name, completed_date, host_name, host_department, due_date, days_left, status, status_text, status_color}]`; resource chi tiết thêm `service_demand_id` + `service_demand: {id, meeting_id, meeting_code, completed_date, host_name, due_date, status_text, status_color}|null`.

- [x] **Step 1: Test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation as Q;
use Modules\Human\Entities\Employee;
use Tests\TestCase;

class QuotationLinkTest extends TestCase
{
    use ServiceDemandFixture;

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    private function demand(): D
    {
        return app(ServiceDemandStatusService::class)->createForMeeting($this->makeMeeting());
    }

    public function test_danh_sach_chon_chi_dang_theo_doi_chua_gan_cua_dung_khach(): void
    {
        $d = $this->demand();
        $this->actingAs(Employee::findOrFail(24), 'api');
        $ids = collect($this->getJson('/api/v1/customer-care/wr-quotations/service-demands?customer_id=' . $d->customer_id)
            ->assertOk()->json('data'))->pluck('id');
        $this->assertTrue($ids->contains($d->id));

        $q = $this->makeQuotation($d->customer_id);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q, $d->id);
        $ids = collect($this->getJson('/api/v1/customer-care/wr-quotations/service-demands?customer_id=' . $d->customer_id)->json('data'))->pluck('id');
        $this->assertFalse($ids->contains($d->id), 'đã gắn báo giá khác thì không được chọn');

        $ids = collect($this->getJson('/api/v1/customer-care/wr-quotations/service-demands?customer_id=' . $d->customer_id . '&include_id=' . $d->id)->json('data'))->pluck('id');
        $this->assertTrue($ids->contains($d->id), 'include_id giữ lại nhu cầu đang gắn khi sửa');
    }

    public function test_request_chan_nhu_cau_da_gan_bao_gia_khac_va_sai_khach(): void
    {
        $d = $this->demand();
        $q1 = $this->makeQuotation($d->customer_id);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q1, $d->id);

        $rule = (new \Modules\CustomerCare\Http\Requests\WrServiceQuotation\WrQuotationRequest())->serviceDemandRule($d->customer_id, null);
        $v = validator(['service_demand_id' => $d->id], ['service_demand_id' => $rule]);
        $this->assertTrue($v->fails());

        $v = validator(['service_demand_id' => $d->id], ['service_demand_id' => (new \Modules\CustomerCare\Http\Requests\WrServiceQuotation\WrQuotationRequest())->serviceDemandRule($d->customer_id + 999999, $q1->id)]);
        $this->assertTrue($v->fails(), 'sai khách hàng');

        $v = validator(['service_demand_id' => $d->id], ['service_demand_id' => (new \Modules\CustomerCare\Http\Requests\WrServiceQuotation\WrQuotationRequest())->serviceDemandRule($d->customer_id, $q1->id)]);
        $this->assertFalse($v->fails(), 'chính báo giá đang gắn thì hợp lệ');
    }

    public function test_copy_bao_gia_khong_mang_nhu_cau(): void
    {
        $d = $this->demand();
        $q = $this->makeQuotation($d->customer_id);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q, $d->id);
        $this->actingAs(Employee::findOrFail(24), 'api');
        $data = app(\Modules\CustomerCare\Services\WrQuotationService::class)->prefillFromQuotation($q->fresh());
        $this->assertNull($data['service_demand_id'] ?? null);
        $this->assertNull($data['service_demand'] ?? null);
    }

    public function test_xoa_bao_gia_nhap_go_lien_ket(): void
    {
        $d = $this->demand();
        $q = $this->makeQuotation($d->customer_id);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q, $d->id);
        $this->actingAs(Employee::findOrFail(24), 'api');
        app(\Modules\CustomerCare\Services\WrQuotationService::class)->delete($q->fresh());
        $this->assertNull($d->fresh()->wr_service_quotation_id);
        $this->assertSame(D::DANG_THEO_DOI, (int) $d->fresh()->status);
    }
}
```

> Review Focus #1 (store status 2) và #2 (2 người chọn trùng) được chốt bằng `test_bao_gia_duyet_...` (Task 2) + `test_request_chan_...` ở trên; thêm ở Task 12 1 ca e2e "Lưu và duyệt" ngay lần tạo.

- [x] **Step 2:** Run `--filter QuotationLinkTest` → FAIL.
- [x] **Step 3: Request** — thêm vào `WrQuotationRequest`:

```php
    /**
     * Nhu cầu làm dịch vụ chọn được khi: đúng khách của báo giá, và
     *   (Đang theo dõi + chưa gắn báo giá nào)  HOẶC  chính là nhu cầu báo giá này đang gắn (đang sửa).
     * Chặn ở máy chủ vì 2 người có thể mở form cùng lúc (design Review Focus #2).
     */
    public function serviceDemandRule($customerId, $quotationId): array
    {
        return ['nullable', 'integer', function ($attribute, $value, $fail) use ($customerId, $quotationId) {
            $d = \Modules\Assign\Entities\Meeting\MeetingServiceDemand::find($value);
            if (!$d || (int) $d->customer_id !== (int) $customerId) {
                return $fail('Nhu cầu dịch vụ không thuộc khách hàng đang chọn.');
            }
            $isMine = $quotationId && (int) $d->wr_service_quotation_id === (int) $quotationId;
            $isFree = !$d->wr_service_quotation_id && (int) $d->status === \Modules\Assign\Entities\Meeting\MeetingServiceDemand::DANG_THEO_DOI;
            if (!$isMine && !$isFree) {
                $fail('Nhu cầu dịch vụ đã được chọn ở báo giá khác hoặc không còn theo dõi, vui lòng chọn lại.');
            }
        }];
    }
```
  và cuối `rules()` (trước `return $rules;`):

```php
        $rules['service_demand_id'] = $this->serviceDemandRule($this->get('customer_id'), $this->route('id'));
```

- [x] **Step 4: Service** — trong `WrQuotationService`:

```php
    public function store(array $data): WrServiceQuotation
    {
        return DB::transaction(function () use ($data) {
            $model = $this->syncTotals(parent::store($this->packAttachments($this->fillWorkCost($data))));
            app(ServiceDemandStatusService::class)->syncQuotationLink($model, $data['service_demand_id'] ?? null);

            return $model;
        });
    }

    public function update(WrServiceQuotation $model, array $data): WrServiceQuotation
    {
        return DB::transaction(function () use ($model, $data) {
            $model = $this->syncTotals(parent::update($model, $this->packAttachments($this->fillWorkCost($data))));
            app(ServiceDemandStatusService::class)->syncQuotationLink($model, $data['service_demand_id'] ?? null);

            return $model;
        });
    }
```
  - `delete()`: dòng đầu trong closure thêm `app(ServiceDemandStatusService::class)->unlinkQuotation($model);`
  - `prefillFromQuotation()`: cạnh `$data['attachments'] = [];` thêm `$data['service_demand_id'] = null; $data['service_demand'] = null;`
  - `use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;` (và `DB` nếu chưa import).
- [x] **Step 5: Controller + route**

```php
    /** Ô "Nhu cầu dịch vụ" ở form báo giá: nhu cầu Đang theo dõi, chưa gắn báo giá, của khách đang chọn */
    public function serviceDemands(Request $request)
    {
        $customerId = (int) $request->get('customer_id');
        $includeId = (int) $request->get('include_id');
        if (!$customerId) {
            return $this->responseSuccess('success', []);
        }

        $rows = \Modules\Assign\Entities\Meeting\MeetingServiceDemand::query()
            ->with(['meeting:id,code,name,completed_at,host_employee_id', 'meeting.host.info.department'])
            ->where('customer_id', $customerId)
            ->where(function ($q) use ($includeId) {
                $q->where(function ($free) {
                    $free->where('status', \Modules\Assign\Entities\Meeting\MeetingServiceDemand::DANG_THEO_DOI)
                        ->whereNull('wr_service_quotation_id');
                });
                if ($includeId) {
                    $q->orWhere('id', $includeId);
                }
            })
            ->orderByDesc('tracking_start_date')
            ->get()
            ->map(function ($d) {
                $host = optional(optional($d->meeting)->host);
                return [
                    'id' => $d->id,
                    'meeting_id' => $d->meeting_id,
                    'meeting_code' => optional($d->meeting)->code,
                    'meeting_name' => optional($d->meeting)->name,
                    'completed_date' => optional(optional($d->meeting)->completed_at)->format('d/m/Y'),
                    'host_name' => optional($host->info)->fullname,
                    'host_department' => optional(optional($host->info)->department)->name,
                    'due_date' => optional($d->due_date)->format('d/m/Y'),
                    'days_left' => $d->due_date ? now()->startOfDay()->diffInDays($d->due_date, false) : null,
                    'status' => (int) $d->status,
                    'status_text' => $d->status_text,
                    'status_color' => $d->status_color,
                ];
            })->values();

        return $this->responseSuccess('success', $rows);
    }
```
  Route (đặt ngay dưới `Route::get('/prefill', ...)`): `Route::get('/service-demands', [WrQuotationController::class, 'serviceDemands']);`

> Kiểm tên quan hệ người chủ trì: `grep -n "function host" Modules/Assign/Entities/Meeting/Meeting.php`. Khác tên thì sửa `meeting.host...`.

- [x] **Step 6: Resource** — `WrQuotationResource::toArray` thêm:

```php
            'service_demand_id' => optional($this->serviceDemand)->id,
            'service_demand' => $this->serviceDemand ? [
                'id' => $this->serviceDemand->id,
                'meeting_id' => $this->serviceDemand->meeting_id,
                'meeting_code' => optional($this->serviceDemand->meeting)->code,
                'completed_date' => optional(optional($this->serviceDemand->meeting)->completed_at)->format('d/m/Y'),
                'host_name' => optional(optional(optional($this->serviceDemand->meeting)->host)->info)->fullname,
                'due_date' => optional($this->serviceDemand->due_date)->format('d/m/Y'),
                'status_text' => $this->serviceDemand->status_text,
                'status_color' => $this->serviceDemand->status_color,
            ] : null,
```
  và thêm vào entity `WrServiceQuotation`:

```php
    public function serviceDemand()
    {
        return $this->hasOne(\Modules\Assign\Entities\Meeting\MeetingServiceDemand::class, 'wr_service_quotation_id');
    }
```
  `findForRead` (controller L510-541) thêm eager-load `'serviceDemand.meeting.host.info'`.
- [x] **Step 7:** Run `--filter QuotationLinkTest` → PASS; `--filter ServiceDemand` → toàn bộ PASS.
- [x] **Step 8: Commit** — message `Báo giá DV: chọn nhu cầu làm dịch vụ, khoá chọn khi lưu nháp, chuyển trạng thái khi duyệt`.

---

### Task 6: Hợp đồng DV — hook duyệt / không duyệt / huỷ duyệt / đóng

**Files:**
- Modify: `hrm-api/Modules/CustomerCare/Services/WrServiceContractService.php` (L1411-1460)
- Test: `hrm-api/tests/Feature/ServiceDemand/ContractHookTest.php`

- [x] **Step 1: Test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Modules\CustomerCare\Entities\WrServiceContract\WrServiceContract as C;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation as Q;
use Modules\CustomerCare\Services\WrServiceContractService;
use Modules\Human\Entities\Employee;
use Tests\TestCase;

class ContractHookTest extends TestCase
{
    use ServiceDemandFixture;

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    private function setupContract(int $status): array
    {
        $d = app(ServiceDemandStatusService::class)->createForMeeting($this->makeMeeting());
        $q = $this->makeQuotation($d->customer_id, Q::STATUS_QT_APPROVED);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q, $d->id);
        $this->actingAs(Employee::findOrFail(24), 'api');

        return [$d, $this->makeContract($q->id, $status)];
    }

    public function test_approve_chuyen_da_lap_hop_dong(): void
    {
        [$d, $c] = $this->setupContract(C::HD_WAITING);
        app(WrServiceContractService::class)->approve($c);
        $this->assertSame(D::DA_LAP_HOP_DONG, (int) $d->fresh()->status);
    }

    public function test_reject_unapprove_close_chuyen_dong_dung_ly_do(): void
    {
        [$d, $c] = $this->setupContract(C::HD_WAITING);
        app(WrServiceContractService::class)->reject($c, 'test');
        $this->assertSame(D::CLOSE_CONTRACT_REJECTED, (int) $d->fresh()->close_reason);

        [$d2, $c2] = $this->setupContract(C::HD_EFFECTIVE);
        app(WrServiceContractService::class)->unApprove($c2, 'test');
        $this->assertSame(D::CLOSE_CONTRACT_UNAPPROVED, (int) $d2->fresh()->close_reason);

        [$d3, $c3] = $this->setupContract(C::HD_EFFECTIVE);
        app(WrServiceContractService::class)->close($c3);
        $this->assertSame(D::CLOSE_CONTRACT_CLOSED, (int) $d3->fresh()->close_reason);
        $this->assertSame(D::DA_DONG, (int) $d3->fresh()->status);
    }
}
```

> `approve/reject/...` gửi thông báo thật qua `WrServiceContractNotifier` — bọc test bằng `Notification::fake()` + `Queue::fake()` ở `setUp` nếu notifier bắn job/redis lỗi trên máy test.

- [x] **Step 2:** Run → FAIL.
- [x] **Step 3: Sửa 4 method** — mỗi method thêm 1 lệnh vào callback `$truocKhiLuu` (chạy TRONG transaction, cùng commit với đổi trạng thái HĐ):

```php
    public function approve(WrServiceContract $model, ?string $note = null): WrServiceContract
    {
        return $this->doiTrangThai($model, WrServiceContract::HD_EFFECTIVE, $note, function ($model) {
            $model->approver_id = auth()->id();
            $model->approved_time = now();
            app(ServiceDemandStatusService::class)->onContractApproved($model);
        }, function ($model) {
            app(WrServiceContractNotifier::class)->notifyApproved($model);
        });
    }
```
  - `reject`: thêm `app(ServiceDemandStatusService::class)->onContractClosed($model, MeetingServiceDemand::CLOSE_CONTRACT_REJECTED);`
  - `unApprove`: `... CLOSE_CONTRACT_UNAPPROVED`
  - `close`: `... CLOSE_CONTRACT_CLOSED`
  - import `Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService` + `Modules\Assign\Entities\Meeting\MeetingServiceDemand`.
- [x] **Step 4:** Run `--filter ContractHookTest` → PASS; `--filter ServiceDemand` → PASS.
- [x] **Step 5: Commit** — message `Hợp đồng DV: cập nhật nhu cầu làm dịch vụ khi duyệt / không duyệt / huỷ duyệt / đóng`.

---

### Task 7: Cron hết hạn + cảnh báo

**Files:**
- Create: `hrm-api/app/Console/Commands/Assign/CloseExpiredServiceDemandsCommand.php`
- Create: `hrm-api/Modules/Assign/Services/ServiceDemand/ServiceDemandNotifier.php`
- Modify: `hrm-api/app/Console/Kernel.php` (sau khối L68-71)
- Test: `hrm-api/tests/Feature/ServiceDemand/CloseExpiredCommandTest.php`

**Interfaces — Produces:** `ServiceDemandNotifier::notifyExpiringSoon(MeetingServiceDemand $d, int $remainDays): void`; `ServiceDemandNotifier::PREFIX = 'NCDV'`.

- [x] **Step 1: Đọc skill `notification-convention`** (bắt buộc trước khi viết nội dung thông báo) — xác nhận prefix `NCDV` hợp lệ theo bảng prefix của skill; nếu skill yêu cầu đăng ký prefix ở 1 file danh mục thì thêm vào đó.
- [x] **Step 2: Test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Carbon\Carbon;
use Illuminate\Support\Facades\Artisan;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;
use Modules\Assign\Services\ServiceDemand\ServiceDemandNotifier;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Tests\TestCase;

class CloseExpiredCommandTest extends TestCase
{
    use ServiceDemandFixture;

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        Carbon::setTestNow();
        parent::tearDown();
    }

    public function test_dong_qua_han_va_canh_bao_mot_lan(): void
    {
        $notifier = \Mockery::mock(ServiceDemandNotifier::class);
        $notifier->shouldReceive('notifyExpiringSoon')->once();
        $this->app->instance(ServiceDemandNotifier::class, $notifier);

        $svc = app(ServiceDemandStatusService::class);
        $expired = $svc->createForMeeting($this->makeMeeting());
        $expired->forceFill(['due_date' => Carbon::today()->subDay(), 'due_days_snapshot' => 30])->save();
        $soon = $svc->createForMeeting($this->makeMeeting());
        $soon->forceFill(['due_date' => Carbon::today()->addDays(2), 'due_days_snapshot' => 30])->save();

        Artisan::call('assign:close-expired-service-demands');
        Artisan::call('assign:close-expired-service-demands'); // chạy lần 2 cùng ngày: không cảnh báo trùng

        $this->assertSame(D::DA_DONG, (int) $expired->fresh()->status);
        $this->assertSame(Carbon::today()->subDay()->toDateString(), $expired->fresh()->closed_at->toDateString());
        $this->assertSame(D::DANG_THEO_DOI, (int) $soon->fresh()->status);
        $this->assertNotNull($soon->fresh()->expiry_warned_at);
    }

    public function test_dry_run_khong_ghi(): void
    {
        $d = app(ServiceDemandStatusService::class)->createForMeeting($this->makeMeeting());
        $d->forceFill(['due_date' => Carbon::today()->subDay()])->save();
        Artisan::call('assign:close-expired-service-demands', ['--dry-run' => true]);
        $this->assertSame(D::DANG_THEO_DOI, (int) $d->fresh()->status);
    }
}
```
  (Giả định `demand_warning_days` của công ty test = 3 → nhu cầu còn 2 ngày phải được cảnh báo; nếu DB local cấu hình khác, đặt `due_date = today + (M - 1)` đọc M từ `GeneralRegulation` trong test.)

- [x] **Step 3:** Run → FAIL (command not found).
- [x] **Step 4: Notifier**

```php
<?php

namespace Modules\Assign\Services\ServiceDemand;

use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Modules\Human\Entities\Employee;
use Modules\Timesheet\Services\EmployeeInfoService;

/** Thông báo nhu cầu làm dịch vụ sắp hết hạn theo dõi — người nhận: chủ trì + người tạo meeting (design #15) */
class ServiceDemandNotifier
{
    const PREFIX = 'NCDV';

    public function notifyExpiringSoon(MeetingServiceDemand $d, int $remainDays): void
    {
        $meeting = $d->meeting;
        if (!$meeting) {
            return;
        }
        $ids = array_values(array_unique(array_filter([$meeting->host_employee_id, $meeting->created_by])));
        $employees = Employee::whereIn('id', $ids)->whereNotNull('employee_info_id')->get();
        if ($employees->isEmpty()) {
            return;
        }

        $data = [
            'url' => '/assign/report/service-demand?demand_id=' . $d->id,
            'title' => buildNotificationContent(
                self::PREFIX,
                'Sắp đến hạn',
                ($meeting->customer_name ?: 'Khách hàng') . ' - ' . $meeting->code,
                sprintf('Tự đóng sau %d ngày nếu chưa lập báo giá.', $remainDays)
            ),
            'type' => 'service_demand',
            'id' => $d->id,
        ];

        foreach ($employees as $employee) {
            try {
                EmployeeInfoService::sendNotification($employee->employee_info_id, $data, true);
            } catch (\Exception $e) {
                Log::error(sprintf('[service-demand] Không gửi được cảnh báo nhu cầu #%d tới NV #%d: %s', $d->id, $employee->id, $e->getMessage()));
            }
        }
    }
}
```

- [x] **Step 5: Command**

```php
<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand;
use Modules\Assign\Services\ServiceDemand\ServiceDemandNotifier;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Modules\Timesheet\Entities\GeneralRegulation;

/**
 * Cảnh báo + tự đóng NHU CẦU LÀM DỊCH VỤ quá hạn theo dõi (bao-cao-nhu-cau-dich-vu, design #4/#15).
 * Chỉ áp cho nhu cầu "Đang theo dõi" (kể cả đang gắn báo giá nháp — design #9 cho phép duyệt ghi đè sau).
 * Cùng luật cảnh báo với nhu cầu đầu tư: chỉ khi N > M > 0, 1 lần (expiry_warned_at).
 */
class CloseExpiredServiceDemandsCommand extends Command
{
    protected $signature = 'assign:close-expired-service-demands {--dry-run : Chỉ liệt kê, không ghi DB}';

    protected $description = 'Cảnh báo trước hạn + đóng nhu cầu làm dịch vụ quá thời gian theo dõi';

    private const DEFAULT_WARNING_DAYS = 3;

    public function handle(ServiceDemandStatusService $status, ServiceDemandNotifier $notifier)
    {
        $today = Carbon::today();
        $dryRun = (bool) $this->option('dry-run');
        $closed = $warned = 0;

        $demands = MeetingServiceDemand::with('meeting')
            ->where('status', MeetingServiceDemand::DANG_THEO_DOI)
            ->whereNotNull('due_date')
            ->get();

        foreach ($demands as $d) {
            if ($today->gte($d->due_date)) {
                $this->line(sprintf('ĐÓNG #%d (meeting %d) — hết hạn %s', $d->id, $d->meeting_id, $d->due_date->format('d/m/Y')));
                if (!$dryRun) {
                    $status->closeExpired($d);
                }
                $closed++;
                continue;
            }

            $m = $this->warningDays($d->company_id);
            if (!($d->due_days_snapshot > $m && $m > 0) || $d->expiry_warned_at) {
                continue;
            }
            if ($today->lt($d->due_date->copy()->subDays($m))) {
                continue;
            }

            if (!$dryRun) {
                $notifier->notifyExpiringSoon($d, $today->diffInDays($d->due_date));
                $d->forceFill(['expiry_warned_at' => now()])->save();
            }
            $warned++;
        }

        $message = sprintf('%s %d nhu cầu dịch vụ, cảnh báo %d.', $dryRun ? '[dry-run] Sẽ đóng' : 'Đã đóng', $closed, $warned);
        $this->info($message);
        if (!$dryRun && ($closed || $warned)) {
            Log::info('[assign:close-expired-service-demands] ' . $message);
        }

        return 0;
    }

    private function warningDays(?int $companyId): int
    {
        $config = $companyId ? GeneralRegulation::where('company_id', $companyId)->first() : null;

        return $config && $config->demand_warning_days !== null ? (int) $config->demand_warning_days : self::DEFAULT_WARNING_DAYS;
    }
}
```

- [x] **Step 6:** `Kernel.php` sau khối `assign:close-expired-customer-demands`:

```php
        $schedule->command('assign:close-expired-service-demands')
            ->dailyAt('01:25')
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping();
```
  (Nếu command không tự load, đăng ký trong `$commands` của Kernel giống `CloseExpiredCustomerDemandsCommand`.)
- [x] **Step 7:** Run `--filter CloseExpiredCommandTest` → PASS.
- [x] **Step 8: Commit** — message `Nhu cầu làm dịch vụ: cron đóng quá hạn + thông báo sắp hết hạn`.

---

### Task 8: Lệnh sinh bù

**Files:**
- Create: `hrm-api/app/Console/Commands/Assign/BackfillServiceDemandsCommand.php`
- Test: `hrm-api/tests/Feature/ServiceDemand/BackfillCommandTest.php`

- [x] **Step 1: Test (đỏ)**

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Carbon\Carbon;
use Illuminate\Support\Facades\Artisan;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;
use Tests\TestCase;

class BackfillCommandTest extends TestCase
{
    use ServiceDemandFixture;

    protected function tearDown(): void
    {
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    public function test_sinh_bu_tinh_han_tu_hom_nay_va_idempotent(): void
    {
        $m = $this->makeMeeting(['completed_at' => Carbon::parse('2026-03-01 10:00')]);
        Artisan::call('assign:backfill-service-demands', ['--meeting' => $m->id]);
        Artisan::call('assign:backfill-service-demands', ['--meeting' => $m->id]);

        $rows = D::where('meeting_id', $m->id)->get();
        $this->assertCount(1, $rows);
        $this->assertSame(Carbon::today()->toDateString(), $rows[0]->tracking_start_date->toDateString());
    }

    public function test_dry_run_khong_ghi(): void
    {
        $m = $this->makeMeeting();
        Artisan::call('assign:backfill-service-demands', ['--meeting' => $m->id, '--dry-run' => true]);
        $this->assertSame(0, D::where('meeting_id', $m->id)->count());
    }
}
```

- [x] **Step 2:** Run → FAIL.
- [x] **Step 3: Command**

```php
<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\MeetingType;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;

/**
 * Sinh bù nhu cầu làm dịch vụ cho meeting đã Hoàn thành + Q4 = Có TRƯỚC khi có feature (design #13).
 * Hạn theo dõi tính từ NGÀY CHẠY LỆNH (= ngày deploy) + N; ngày hoàn thành meeting giữ nguyên để báo cáo
 * lọc kỳ đúng. Chạy tay 1 lần sau deploy, xem trước bằng --dry-run. Idempotent.
 */
class BackfillServiceDemandsCommand extends Command
{
    protected $signature = 'assign:backfill-service-demands {--dry-run} {--meeting= : Chỉ 1 meeting (dùng cho test)}';

    protected $description = 'Sinh bù nhu cầu làm dịch vụ cho meeting cũ (hạn tính từ hôm nay)';

    public function handle(ServiceDemandStatusService $svc)
    {
        $typeId = MeetingType::where('code', MeetingType::CODE_PRODUCT_INTRO)->value('id');
        $query = Meeting::query()
            ->where('meeting_type_id', $typeId)
            ->where('status', Meeting::HOAN_THANH)
            ->where('has_maintenance_demand', 1)
            ->whereNotExists(function ($sub) {
                $sub->selectRaw(1)->from('meeting_service_demands')->whereColumn('meeting_service_demands.meeting_id', 'meetings.id');
            });
        if ($this->option('meeting')) {
            $query->where('id', (int) $this->option('meeting'));
        }

        $count = 0;
        $query->orderBy('id')->chunkById(200, function ($meetings) use ($svc, &$count) {
            foreach ($meetings as $m) {
                if (!$this->option('dry-run')) {
                    $svc->createForMeeting($m, Carbon::today());
                }
                $count++;
            }
        });

        $this->info(sprintf('%s %d nhu cầu làm dịch vụ.', $this->option('dry-run') ? '[dry-run] Sẽ sinh' : 'Đã sinh', $count));

        return 0;
    }
}
```

- [x] **Step 4:** Run `--filter BackfillCommandTest` → PASS.
- [x] **Step 5:** Chạy thật `php artisan assign:backfill-service-demands --dry-run` trên DB local → kỳ vọng ~76 (đếm 04/10/2026). **Không chạy bản ghi thật** trừ khi user cho phép (nằm trong phạm vi Task 0 thì được).
- [x] **Step 6: Commit** — message `Nhu cầu làm dịch vụ: lệnh sinh bù cho meeting cũ`.

---

### Task 9: Quyền

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (ngay dưới khối "Báo cáo kết quả chăm sóc khách hàng tiềm năng" L1076-1079)

- [x] **Step 1:** Thêm vào seeder:

```php
        // Báo cáo tổng hợp nhu cầu làm dịch vụ (bao-cao-nhu-cau-dich-vu) — 2 cấp, không có cấp phòng ban
        Permission::create(['id' => 1660, 'guard_name' => 'api', 'name' => 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty', 'display_name' => 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty', 'group' => 'Báo cáo tổng hợp nhu cầu làm dịch vụ', 'type' => 4]);
        Permission::create(['id' => 1661, 'guard_name' => 'api', 'name' => 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo công ty', 'display_name' => 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo công ty', 'group' => 'Báo cáo tổng hợp nhu cầu làm dịch vụ', 'type' => 4]);
```

- [x] **Step 2:** Kiểm trùng id: `grep -o "'id' => [0-9]*" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sed "s/'id' => //" | sort -n | uniq -d` → rỗng.
- [x] **Step 3:** **KHÔNG chạy seeder** (truncate cả bảng). Insert tay vào DB local (trong phạm vi Task 0):

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='foreach ([[1660,"theo tổng công ty"],[1661,"theo công ty"]] as [$id,$s]) { $n="Xem báo cáo tổng hợp nhu cầu làm dịch vụ ".$s; DB::table("permissions")->updateOrInsert(["id"=>$id],["guard_name"=>"api","name"=>$n,"display_name"=>$n,"group"=>"Báo cáo tổng hợp nhu cầu làm dịch vụ","type"=>4,"created_at"=>now(),"updated_at"=>now()]); } app(\Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions(); echo "ok";'
/opt/homebrew/opt/php@7.4/bin/php artisan cache:clear
```
- [x] **Step 4: Commit** — message `Quyền: 2 quyền xem báo cáo tổng hợp nhu cầu làm dịch vụ (1660-1661)`.

---

### Task 10: API báo cáo (dữ liệu + quyền)

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/ServiceDemandReportService.php`
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ServiceDemandReportController.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (sau khối potential-customer-care ~L1220)
- Test: `hrm-api/tests/Feature/ServiceDemand/ReportApiTest.php`

**Interfaces — Produces** (FE Task 13-14 dùng):
- `GET /api/v1/assign/report/service-demand` params: `period` (`week|month|year|last_year|custom`, mặc định `year`), `from`, `to` (d/m/Y, khi custom), `company_id`, `department_id`, `host_employee_id`, `province_id`, `customer_id`, `status`, `handler_employee_id`, `level` (`0|1`), `page`, `per_page` →
  `{ meta: {from, to, label}, summary: {needs, customers, provinces, by_status: {1:n,2:n,3:n,4:n}, contract_rate}, total: {needs, quotations, contracts}, groups: [{province_id, province_name, needs, quotations, contracts, customers: [{customer_id, name, code, needs: [Row]}]}], pagination: {total, per_page, current_page} }`
- `Row` = `{id, meeting_id, meeting_code, completed_date, host_name, contact_name, contact_phone, status, status_text, status_color, close_reason_text, days_left, quotation_id, quotation_code, quotation_is_draft, handler_name, has_quotation, contract_id, contract_code, contract_approved_date, province_id, province_name, customer_id, customer_name, customer_code}`
- Envelope: `responseJson('success', 200, $data)` của repo — kiểm shape thật (`data.rows` hay `rows`) bằng 1 lần gọi tay trước khi viết `ReportApiTest::ids()`.
- `GET .../service-demand/demand-list` cùng params + `pv` (province_id), `has_quotation`, `has_contract` → `{ total, rows: [Row + province_name, customer_name, customer_code], pagination }`
- `GET .../service-demand/filter-options` → `{ companies, departments, hosts, provinces, customers, handlers, statuses, can_change_company }`
- Quyền: tổng công ty → không giới hạn; theo công ty → `meeting_service_demands.company_id = current_company_role OR meetings.host_employee_id = me`; không quyền → host = me OR có trong `meeting_employees` OR `handler_employee_id = me`. `company_id` từ request bị **bỏ qua** nếu không có quyền tổng công ty.

- [x] **Step 1: Test (đỏ)** — 4 ca quyền + kỳ.

```php
<?php

namespace Tests\Feature\ServiceDemand;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Services\ServiceDemand\ServiceDemandStatusService;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation as Q;
use Modules\Human\Entities\Employee;
use Tests\TestCase;

/**
 * Actor (kiểm bằng tinker TRƯỚC khi chạy, KHÔNG có quyền 1660/1661 qua role):
 *   HOST = người chủ trì meeting fixture · OUTSIDER = 28 · HANDLER = 27 (tạo báo giá, không dự họp)
 */
class ReportApiTest extends TestCase
{
    use ServiceDemandFixture;

    private const OUTSIDER = 28;
    private const HANDLER = 27;
    private $granted = [];

    protected function tearDown(): void
    {
        foreach ($this->granted as $empId) {
            DB::table('employee_has_permissions')->where('employee_id', $empId)->whereIn('permission_id', [1660, 1661])->delete();
        }
        Artisan::call('cache:clear');
        $this->cleanupServiceDemandFixture();
        parent::tearDown();
    }

    private function ids(int $empId, array $q = []): array
    {
        $this->actingAs(Employee::findOrFail($empId), 'api');
        return collect($this->getJson('/api/v1/assign/report/service-demand/demand-list?' . http_build_query($q + ['period' => 'year', 'per_page' => 500]))
            ->assertOk()->json('data.rows'))->pluck('id')->all();
    }

    public function test_khong_quyen_chi_thay_cua_minh_va_nguoi_xu_ly(): void
    {
        $m = $this->makeMeeting(['completed_at' => now()->startOfYear()->addDay()]);
        $d = app(ServiceDemandStatusService::class)->createForMeeting($m);

        $this->assertContains($d->id, $this->ids((int) $m->host_employee_id), 'chủ trì thấy');
        $this->assertNotContains($d->id, $this->ids(self::OUTSIDER), 'người ngoài KHÔNG thấy');

        $q = $this->makeQuotation($d->customer_id, Q::STATUS_QT_APPROVED, self::HANDLER);
        app(ServiceDemandStatusService::class)->syncQuotationLink($q, $d->id);
        $this->assertContains($d->id, $this->ids(self::HANDLER), 'người xử lý thấy');
    }

    public function test_quyen_tong_cong_ty_thay_het(): void
    {
        $m = $this->makeMeeting(['completed_at' => now()->startOfYear()->addDay()]);
        $d = app(ServiceDemandStatusService::class)->createForMeeting($m);
        DB::table('employee_has_permissions')->insert(['employee_id' => self::OUTSIDER, 'permission_id' => 1660]);
        $this->granted[] = self::OUTSIDER;
        Artisan::call('cache:clear');
        $this->assertContains($d->id, $this->ids(self::OUTSIDER));
    }

    public function test_loc_ky_theo_ngay_hoan_thanh_meeting(): void
    {
        $m = $this->makeMeeting(['completed_at' => now()->subYear()->startOfYear()->addDays(5)]);
        $d = app(ServiceDemandStatusService::class)->createForMeeting($m);
        $host = (int) $m->host_employee_id;
        $this->assertNotContains($d->id, $this->ids($host, ['period' => 'year']));
        $this->assertContains($d->id, $this->ids($host, ['period' => 'last_year']));
    }
}
```

> **Trước khi chạy:** kiểm bảng gán quyền trực tiếp cho nhân viên (`employee_has_permissions` hay tên khác) bằng `SHOW TABLES LIKE '%has_permissions%'` và kiểm 27/28 không có sẵn 1660/1661 qua role. Sai tên bảng thì sửa test, đừng đoán.

- [x] **Step 2:** Run → FAIL (404).
- [x] **Step 3: Service** — `ServiceDemandReportService` gồm:

```php
<?php

namespace Modules\Assign\Services\Report;

use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\MeetingServiceDemand as D;

/**
 * Báo cáo tổng hợp nhu cầu làm dịch vụ (bao-cao-nhu-cau-dich-vu). Trạng thái là trạng thái HIỆN TẠI.
 * Kỳ lọc theo meetings.completed_at. Công ty/phòng ban theo NGƯỜI CHỦ TRÌ (employee_infos), không theo
 * meetings.company_id/department_id (đó là của người tạo).
 */
class ServiceDemandReportService
{
    const PERM_ALL = 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo tổng công ty';
    const PERM_COMPANY = 'Xem báo cáo tổng hợp nhu cầu làm dịch vụ theo công ty';
    const DEFAULT_PER_PAGE = 10;

    public function period(Request $r): array
    {
        $today = Carbon::today();
        switch ($r->get('period', 'year')) {
            case 'week': return [$today->copy()->startOfWeek(), $today->copy()->endOfWeek(), 'tuần này'];
            case 'month': return [$today->copy()->startOfMonth(), $today->copy()->endOfMonth(), 'tháng ' . $today->format('m/Y')];
            case 'last_year': $y = $today->copy()->subYear(); return [$y->copy()->startOfYear(), $y->copy()->endOfYear(), 'năm ' . $y->year];
            case 'custom':
                return [Carbon::createFromFormat('d/m/Y', $r->get('from'))->startOfDay(), Carbon::createFromFormat('d/m/Y', $r->get('to'))->endOfDay(), 'tuỳ chọn'];
            default: return [$today->copy()->startOfYear(), $today->copy()->endOfYear(), 'năm ' . $today->year];
        }
    }

    /** Truy vấn gốc: đã áp kỳ + quyền + bộ lọc. Mỗi dòng = 1 nhu cầu. */
    public function baseQuery(Request $r)
    {
        [$from, $to] = $this->period($r);
        $q = DB::table('meeting_service_demands as d')
            ->join('meetings', 'meetings.id', '=', 'd.meeting_id')
            ->leftJoin('employees as he', 'he.id', '=', 'meetings.host_employee_id')
            ->leftJoin('employee_infos as hi', 'hi.id', '=', 'he.employee_info_id')
            ->leftJoin('customers as c', 'c.id', '=', 'd.customer_id')
            ->leftJoin('provinces as p', 'p.id', '=', 'c.province_id')
            ->leftJoin('wr_service_quotations as q', 'q.id', '=', 'd.wr_service_quotation_id')
            ->leftJoin('wr_service_contracts as k', 'k.id', '=', 'd.wr_service_contract_id')
            ->leftJoin('employees as hd', 'hd.id', '=', 'd.handler_employee_id')
            ->leftJoin('employee_infos as hdi', 'hdi.id', '=', 'hd.employee_info_id')
            ->whereBetween('meetings.completed_at', [$from, $to]);

        $this->applyPermission($q);

        if ($r->filled('company_id') && isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            $q->where('d.company_id', (int) $r->company_id);
        }
        foreach (['department_id' => 'hi.department_id', 'host_employee_id' => 'meetings.host_employee_id',
            'province_id' => 'c.province_id', 'customer_id' => 'd.customer_id', 'status' => 'd.status',
            'handler_employee_id' => 'd.handler_employee_id', 'pv' => 'c.province_id'] as $key => $col) {
            if ($r->filled($key)) {
                $q->where($col, (int) $r->get($key));
            }
        }
        if ($r->boolean('has_quotation')) {
            $q->whereNotNull('d.handler_employee_id');
        }
        if ($r->boolean('has_contract')) {
            $q->whereNotNull('d.wr_service_contract_id');
        }

        return $q->select([
            'd.*', 'meetings.code as meeting_code', 'meetings.completed_at', 'meetings.customer_contact_name as contact_name',
            'meetings.customer_contact_phone as contact_phone', 'hi.fullname as host_name',
            'c.fullname as customer_name', 'c.code as customer_code', 'c.province_id', 'p.name as province_name',
            'q.code as quotation_code', 'q.status as quotation_status', 'k.code as contract_code', 'k.approved_time as contract_approved_time',
            'hdi.fullname as handler_name',
        ]);
    }

    private function applyPermission($q): void
    {
        $me = auth()->user()->id;
        if (isCurrentEmployeeHasPermission(self::PERM_ALL)) {
            return;
        }
        if (isCurrentEmployeeHasPermission(self::PERM_COMPANY)) {
            $company = auth()->user()->current_company_role;
            $q->where(function ($w) use ($company, $me) {
                $w->where('d.company_id', $company)->orWhere('meetings.host_employee_id', $me);
            });
            return;
        }
        $q->where(function ($w) use ($me) {
            $w->where('meetings.host_employee_id', $me)
                ->orWhere('d.handler_employee_id', $me)
                ->orWhereExists(function ($s) use ($me) {
                    $s->selectRaw(1)->from('meeting_employees')
                        ->whereColumn('meeting_employees.meeting_id', 'meetings.id')
                        ->where('meeting_employees.employee_id', $me);
                });
        });
    }

    public function toRow($x): array
    {
        $dueDate = $x->due_date ? Carbon::parse($x->due_date) : null;
        return [
            'id' => (int) $x->id,
            'meeting_id' => (int) $x->meeting_id,
            'meeting_code' => $x->meeting_code,
            'completed_date' => $x->completed_at ? Carbon::parse($x->completed_at)->format('d/m/Y') : null,
            'host_name' => $x->host_name,
            'contact_name' => $x->contact_name,
            'contact_phone' => $x->contact_phone,
            'status' => (int) $x->status,
            'status_text' => D::STATUS_TEXT[(int) $x->status] ?? '',
            'status_color' => D::STATUS_COLOR[(int) $x->status] ?? '',
            'close_reason_text' => $x->close_reason ? (D::CLOSE_REASON_TEXT[(int) $x->close_reason] ?? null) : null,
            'days_left' => ((int) $x->status === D::DANG_THEO_DOI && $dueDate) ? Carbon::today()->diffInDays($dueDate, false) : null,
            'quotation_id' => $x->wr_service_quotation_id ? (int) $x->wr_service_quotation_id : null,
            'quotation_code' => $x->quotation_code,
            'quotation_is_draft' => $x->wr_service_quotation_id && (int) $x->quotation_status === 1,
            'handler_name' => $x->handler_name,
            'has_quotation' => (bool) $x->handler_employee_id, // đã có báo giá ĐƯỢC DUYỆT (nháp không tính)
            'contract_id' => $x->wr_service_contract_id ? (int) $x->wr_service_contract_id : null,
            'contract_code' => $x->contract_code,
            'contract_approved_date' => ((int) $x->status === D::DA_LAP_HOP_DONG && $x->contract_approved_time) ? Carbon::parse($x->contract_approved_time)->format('d/m/Y') : null,
            'province_id' => $x->province_id ? (int) $x->province_id : null,
            'province_name' => $x->province_name ?: 'Chưa xác định thị trường',
            'customer_id' => (int) $x->customer_id,
            'customer_name' => $x->customer_name,
            'customer_code' => $x->customer_code,
        ];
    }

    /** Màn chính: tổng hợp + cây, phân trang theo nhóm TỈNH */
    public function index(Request $r): array
    {
        [$from, $to, $label] = $this->period($r);
        $rows = $this->baseQuery($r)->orderBy('p.name')->orderBy('c.fullname')->orderByDesc('meetings.completed_at')->get()->map(function ($x) {
            return $this->toRow($x);
        });

        $byStatus = [1 => 0, 2 => 0, 3 => 0, 4 => 0];
        foreach ($rows as $row) {
            $byStatus[$row['status']]++;
        }
        $count = function ($list) {
            return [
                'needs' => count($list),
                'quotations' => collect($list)->where('has_quotation', true)->count(),
                'contracts' => collect($list)->whereNotNull('contract_id')->count(),
            ];
        };

        $groups = $rows->groupBy('province_name')->map(function ($list, $name) use ($count) {
            return array_merge(['province_id' => $list->first()['province_id'], 'province_name' => $name], $count($list->all()), [
                'customers' => $list->groupBy('customer_id')->map(function ($cl) {
                    return ['customer_id' => $cl->first()['customer_id'], 'name' => $cl->first()['customer_name'], 'code' => $cl->first()['customer_code'], 'needs' => $cl->values()->all()];
                })->values()->all(),
            ]);
        })->values();

        $perPage = min(100, max(1, (int) $r->get('per_page', self::DEFAULT_PER_PAGE)));
        $page = max(1, (int) $r->get('page', 1));

        return [
            'meta' => ['from' => $from->format('d/m/Y'), 'to' => $to->format('d/m/Y'), 'label' => $label],
            'summary' => [
                'needs' => $rows->count(),
                'customers' => $rows->pluck('customer_id')->unique()->count(),
                'provinces' => $rows->pluck('province_name')->unique()->count(),
                'by_status' => $byStatus,
                'contract_rate' => $rows->count() ? round($byStatus[3] * 100 / $rows->count(), 1) : null,
            ],
            'total' => $count($rows->all()),
            'groups' => $groups->forPage($page, $perPage)->values()->all(),
            'pagination' => ['total' => $groups->count(), 'per_page' => $perPage, 'current_page' => $page],
        ];
    }

    public function demandList(Request $r): array
    {
        $q = $this->baseQuery($r)->orderBy('p.name')->orderBy('c.fullname')->orderByDesc('meetings.completed_at');
        $perPage = min(500, max(1, (int) $r->get('per_page', 20)));
        $page = $q->paginate($perPage);

        return [
            'total' => $page->total(),
            'rows' => collect($page->items())->map(function ($x) {
                return $this->toRow($x);
            })->all(),
            'pagination' => ['total' => $page->total(), 'per_page' => $perPage, 'current_page' => $page->currentPage()],
        ];
    }
}
```
  - `filterOptions(Request $r)`: chạy `baseQuery($r)` (bỏ chính filter đang hỏi), `distinct` ra từng danh sách `[id, name]`; `companies` chỉ trả đủ khi có `PERM_ALL`, còn lại chỉ công ty hiện tại; `can_change_company = isCurrentEmployeeHasPermission(PERM_ALL)`; `statuses` = 4 trạng thái từ `D::STATUS_TEXT`.

> Kiểm tên cột trước khi chạy: `employees.employee_info_id`, `employee_infos.fullname/department_id`, `customers.fullname/province_id`, `wr_service_contracts.approved_time` (đã thấy ở `WrServiceContractService::approve`). Dùng `Schema::hasColumn` trong tinker nếu nghi ngờ — không đoán.

- [x] **Step 4: Controller + route**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Modules\Assign\Services\Report\ServiceDemandReportService;

/**
 * Báo cáo tổng hợp nhu cầu làm dịch vụ. Route KHÔNG gắn checkPermission: quyền theo cấp nằm trong
 * service để giữ fallback "của mình + người xử lý" cho người không có quyền (giống báo cáo CSKH tiềm năng).
 */
class ServiceDemandReportController extends ApiController
{
    private ServiceDemandReportService $service;

    public function __construct(ServiceDemandReportService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->index($request));
    }

    public function filterOptions(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->filterOptions($request));
    }

    public function demandList(Request $request)
    {
        return $this->responseJson('success', Response::HTTP_OK, $this->service->demandList($request));
    }
}
```
  Route (sau khối potential-customer-care):

```php
        // Báo cáo tổng hợp nhu cầu làm dịch vụ (bao-cao-nhu-cau-dich-vu) — quyền theo cấp nằm trong service
        Route::get('/service-demand', [ServiceDemandReportController::class, 'index']);
        Route::get('/service-demand/filter-options', [ServiceDemandReportController::class, 'filterOptions']);
        Route::get('/service-demand/demand-list', [ServiceDemandReportController::class, 'demandList']);
```
  (import controller ở đầu file routes như các controller report khác.)
- [x] **Step 5:** Run `--filter ReportApiTest` → PASS. Kiểm thêm bằng tay: `GET /api/v1/assign/report/service-demand?period=year` với token admin trả `groups` có `customers[].needs[]`.
- [x] **Step 6: Commit** — message `Báo cáo nhu cầu làm dịch vụ: API tổng hợp, danh sách, bộ lọc + phân quyền 2 cấp`.

---

### Task 11: Xuất Excel + dữ liệu in

**Files:**
- Create: `hrm-api/Modules/Assign/Export/ServiceDemandExport.php`, `ServiceDemandListExport.php`
- Create: `hrm-api/resources/views/exports/assign/service_demand_report.blade.php`, `service_demand_list.blade.php`
- Modify: `ServiceDemandReportController` (+ `export`, `exportDemandList`, `printListData`), `Modules/Assign/Routes/api.php`

- [x] **Step 1: Đọc skill `export-excel` và `print-page`** — làm đúng khuôn (logo theo công ty, cột không bị cắt, ngày dd/mm/yyyy, `print-list-data` là contract của `reportPrintPreviewMixin`).
- [x] **Step 2:** Copy khuôn từ `Modules/Assign/Export/PotentialCustomerCareExport.php` + `PotentialCustomerCareDemandExport.php` + blade tương ứng; dữ liệu lấy từ `ServiceDemandReportService::index()` (in đủ mọi cấp: dòng TỔNG, dòng tỉnh, dòng khách hàng/nhu cầu) và `demandList()` (per_page = 100000). Cột Excel = đúng 9 cột màn hình; Người liên hệ ghi `Tên – SĐT`; Báo giá nháp ghi `BGDV-xxx (nháp)`.
- [x] **Step 3:** Route:

```php
        Route::get('/service-demand/export', [ServiceDemandReportController::class, 'export']);
        Route::get('/service-demand/demand-list/export', [ServiceDemandReportController::class, 'exportDemandList']);
        // Tên `print-list-data` là contract của utils/mixins/reportPrintPreviewMixin.js — đừng đổi
        Route::get('/service-demand/print-list-data', [ServiceDemandReportController::class, 'printListData']);
```
- [x] **Step 3b: Test** — thêm vào `ReportApiTest`:

```php
    public function test_export_tra_file_xlsx(): void
    {
        $this->actingAs(Employee::findOrFail(24), 'api');
        $res = $this->get('/api/v1/assign/report/service-demand/export?period=year');
        $res->assertOk();
        $this->assertStringContainsString('spreadsheetml', $res->headers->get('content-type'));
    }
```
- [x] **Step 4:** Run `--filter ReportApiTest` → PASS; mở file xlsx tải về bằng tay kiểm logo + cột (theo checklist skill export-excel).
- [x] **Step 5: Commit** — message `Báo cáo nhu cầu làm dịch vụ: xuất Excel + dữ liệu in`.

---

### Task 12: Form báo giá DV — ô "Nhu cầu dịch vụ" (FE)

**Files:**
- Modify: `hrm-client/pages/customer-care/wr-quotations/components/WrQuotationForm.vue` (L96-110 khối Địa chỉ sửa chữa; `onCustomerSelected` L931-947; payload lưu; nạp dữ liệu khi sửa ~L828)
- Modify: `hrm-client/pages/customer-care/wr-quotations/_id/index.vue` (màn xem)

- [x] **Step 1:** Đổi `col-md-6` của "Địa chỉ sửa chữa" → `col-md-3`, chèn NGAY SAU nó:

```vue
                    <div class="col-md-3">
                        <div class="form-group">
                            <V2BaseLabel>Nhu cầu dịch vụ</V2BaseLabel>
                            <V2BaseSelect
                                v-model="form.service_demand_id"
                                :options="serviceDemandOptions"
                                :disabled="!form.customer_id || !canChooseCustomer"
                                placeholder="Chọn nhu cầu từ meeting"
                                @input="onServiceDemandChange"
                            />
                            <div v-if="selectedServiceDemand" class="field-line mt-1 d-flex align-items-center flex-wrap">
                                <V2BaseBadge :color="selectedServiceDemand.status_color" size="xs">{{ selectedServiceDemand.status_text }}</V2BaseBadge>
                                <span class="ml-2 v2-hint">Chủ trì: {{ selectedServiceDemand.host_name }} · Hạn {{ selectedServiceDemand.due_date || '—' }}</span>
                            </div>
                            <div v-if="touched && fieldError('service_demand_id')" class="invalid-feedback d-block">{{ fieldError('service_demand_id') }}</div>
                        </div>
                    </div>
```
  > `canChooseCustomer = false` (lập từ phiếu CCTT, khách bị khoá) **vẫn phải chọn được nhu cầu** → đổi `:disabled` thành `!form.customer_id` nếu đúng luồng đó vẫn cho chọn (design: "ai cũng chọn được"). Đọc `canChooseCustomer` để quyết, ghi lại lý do trong comment.
- [x] **Step 2:** data: `form.service_demand_id: null`, `serviceDemandList: []`; computed:

```js
        serviceDemandOptions() {
            return this.serviceDemandList.map((d) => ({
                id: d.id,
                name: `${d.meeting_code} · Họp ngày ${d.completed_date || '—'} — ${d.host_name || ''}${d.days_left !== null ? ` (còn ${d.days_left} ngày)` : ''}`,
            }))
        },
        selectedServiceDemand() {
            return this.serviceDemandList.find((d) => d.id === this.form.service_demand_id) || null
        },
```
  methods:

```js
        async loadServiceDemands() {
            this.serviceDemandList = []
            if (!this.form.customer_id) return
            try {
                const res = await this.$store.dispatch('apiGetMethod', {
                    url: 'customer-care/wr-quotations/service-demands',
                    params: { customer_id: this.form.customer_id, include_id: this.form.service_demand_id || undefined },
                })
                this.serviceDemandList = res?.data || []
            } catch (e) {
                console.error('Error loading service demands:', e)
            }
        },
        onServiceDemandChange(value) {
            this.form.service_demand_id = value || null
        },
```
  - `onCustomerSelected`: thêm `this.form.service_demand_id = null` rồi `await this.loadServiceDemands()` cuối hàm.
  - Khi nạp báo giá để sửa (khối `if (data.customer_id) { await this.loadCustomerDetail(...) }` ~L828): gán `this.form.service_demand_id = data.service_demand_id || null` TRƯỚC, rồi `await this.loadServiceDemands()`.
  - Payload lưu: thêm `service_demand_id: this.form.service_demand_id || null`.
  - Tên action store (`apiGetMethod`) — kiểm tên thật trong file (đang dùng `apiPostMethod` ở L1037); nếu GET dùng action khác thì làm theo.
- [x] **Step 3: Màn xem** (`_id/index.vue`): trong khối thông tin khách, thêm 1 ô "Nhu cầu dịch vụ": `service_demand.meeting_code` (link → mở `MeetingDetailDrawer` với `meeting-id`) + badge + "Chủ trì: … · Hạn …"; null thì `—`.
- [x] **Step 4: Kiểm Playwright MCP** (`/customer-care/wr-quotations/create`):
  - đo hàng 2 có đúng 4 ô cùng `y`, cùng `width` (±1px);
  - ô Nhu cầu `disabled` khi chưa chọn khách; chọn khách có nhu cầu → mở ô thấy option; chọn → hiện badge "Đang theo dõi";
  - đổi sang khách khác → ô về rỗng;
  - **Lưu nháp** → mở lại màn sửa → ô vẫn chọn đúng nhu cầu; DB: `status = 1`, `wr_service_quotation_id` = báo giá;
  - **Lưu và duyệt ngay lần tạo** (Review Focus #1) → DB `status = 2`, `handler_employee_id` = người tạo;
  - mở form thứ 2 cho cùng khách → nhu cầu vừa gắn **không** còn trong danh sách.
  Dọn dữ liệu thử sau khi kiểm.
- [x] **Step 5: Commit** (hrm-client) — message `Báo giá DV: ô chọn nhu cầu làm dịch vụ`.

---

### Task 13: Trang báo cáo — bộ lọc, khối tổng hợp, bảng cây (FE)

**Files:**
- Create: `hrm-client/pages/assign/report/service-demand/index.vue`, `api.js`, `format.js`
- Create: `components/DemandSummary.vue`, `components/DemandTable.vue`, `components/DrillNum.vue`, `components/InfoTip.vue`
- Modify: `hrm-client/components/subsystem-menu/presale.js` (L119-124)

**Interfaces — Consumes:** API Task 10. **Produces:** event `drill(filter: {pv?, status?, has_quotation?, has_contract?, title})`, `open-meeting(meetingId)` từ `DemandTable`/`DemandSummary` lên `index.vue`.

- [x] **Step 1:** Copy khuôn: `cp pages/sale/prepick-tracking/{api.js,format.js} pages/assign/report/service-demand/` và `cp pages/sale/prepick-tracking/components/{DrillNum,InfoTip}.vue pages/assign/report/service-demand/components/`. `api.js` đổi base thành `assign/report/service-demand`.
- [x] **Step 2: `index.vue`** — dựng theo skeleton `pages/sale/prepick-tracking/index.vue` L17-200 (wrapper `v2-styles` › `V2BaseSmartFilterPanel floating :show-quick-search="false" title="Bộ lọc báo cáo tổng hợp nhu cầu làm dịch vụ" reset-button-text="Xóa lọc"`), layout `default-sidebar` (memory hub 3 cấp). Bộ lọc theo đúng thứ tự mockup:
  1. `period` — "Kỳ theo dõi": `[{value:'week',label:'Tuần này'},{value:'month',label:'Tháng này'},{value:'year',label:'Năm nay'},{value:'last_year',label:'Năm trước'},{value:'custom',label:'Tuỳ chọn'}]`, mặc định `year`, không có "Tất cả", không nút ×.
  2. `range` — date-range "Thời gian", chỉ hiện khi `period === 'custom'`, `resetKeys: ['from','to']`, `inputCount: 1` (khuôn TKT `index.vue:229-243`).
  3. `company_id` — "Công ty" + InfoTip *"Lọc theo công ty / phòng ban của NGƯỜI CHỦ TRÌ meeting thu thập nhu cầu — không phải công ty / phòng ban của khách hàng hay người lập báo giá."*; khoá khi `!can_change_company`.
  4. `department_id` — "Phòng ban" + cùng InfoTip.
  5. `host_employee_id` — "Người chủ trì meeting".
  6. `province_id` — "Tỉnh / thành phố".
  7. `customer_id` — "Khách hàng" (`V2BaseSelectRemote`, tối thiểu 2 ký tự).
  8. `status` — "Trạng thái nhu cầu".
  9. `handler_employee_id` — "Người xử lý nhu cầu" + InfoTip *"Người xử lý = người lập báo giá dịch vụ từ nhu cầu. Nhu cầu chưa lập báo giá thì chưa có người xử lý."*
  `#header-actions`: "In danh sách" (secondary, `ri-printer-line`) · "Xuất Excel" (secondary `status="success"`, `ri-file-excel-2-line`) — chỉ `btn-compact`, không mr/ml (memory SmartFilterPanel). `#title-suffix`: InfoTip "MỤC ĐÍCH BÁO CÁO".
  Đọc `?demand_id=` khi vào trang (từ thông báo) → gọi `demand-list` với `id` đó và mở panel meeting của nhu cầu (Task 14).
- [x] **Step 3: `DemandSummary.vue`** — copy `prepick-tracking/components/TrackingSummary.vue`, giữ CSS `.rsum*`, đổi nội dung:
  - dòng `.rsum-goal`: **"Nhu cầu làm dịch vụ {meta.label} ({from} – {to})"** + ⓘ + `· {needs} nhu cầu · {customers} khách hàng · {provinces} tỉnh / thành phố` + nút Thu gọn/Mở rộng;
  - khối 1 "PHẠM VI THEO DÕI" (3 ô: Nhu cầu làm dịch vụ / Khách hàng / Tỉnh-TP) — số là `DrillNum`, emit `drill({title})`;
  - khối 2 "TRẠNG THÁI HIỆN TẠI CỦA NHU CẦU" (4 ô theo `by_status`, %, viền màu theo trạng thái như mockup) — emit `drill({status, title})`; góc phải `"{needs} nhu cầu · lập hợp đồng {contract_rate}%"`.
- [x] **Step 4: `DemandTable.vue`** — copy `prepick-tracking/components/TrackingTable.vue` (giữ `.ptr-table`, `.market-table-wrap`, `table.rsum-tb` sticky, caret, thanh cấp, `table-layout: fixed`, phân trang `V2BasePagination item-label="tỉnh / thành phố"` sizes `[10,25,50,100]`, dòng rỗng `tr.rsum-tb__row--muted` "Không có nhu cầu khớp bộ lọc."), đổi:
  - `colgroup`: `58px · auto · 11% · 130px · 110px · 10% · 128px · 11% · 11%`;
  - header: STT · "Thị trường / Khách hàng" + select cấp (`Chỉ Tỉnh / thành phố` | `Đến Khách hàng`, mặc định Đến Khách hàng) · Người liên hệ · Meeting xác định nhu cầu · Ngày hoàn thành meeting · Người chủ trì meeting · Trạng thái ⓘ · Báo giá · Hợp đồng. `th` cho `white-space: normal` (tối đa 2 dòng);
  - dòng TỔNG (`rsum-tb__sec`, STT "TỔNG", tên "TỈNH / THÀNH PHỐ / KHÁCH HÀNG" ⓘ): cột Meeting `DrillNum(total.needs) nhu cầu`, Báo giá `DrillNum(total.quotations) báo giá` (`has_quotation`), Hợp đồng `DrillNum(total.contracts) hợp đồng` (`has_contract`);
  - dòng tỉnh (d0, STT 1,2…): giống TỔNG nhưng số của tỉnh, filter kèm `pv`; KHÔNG ghi số khách hàng;
  - dòng nhu cầu (d1, STT `i.j`): ô STT + Khách hàng `rowspan = needs.length` (tên + `code-sub`); Người liên hệ = tên + `<div class="project-sub v2-hint"><i class="ri-phone-line"></i> {{ phone }}</div>`; Meeting = link `#28539d` → emit `open-meeting`; Trạng thái = `V2BaseBadge :color` + dòng phụ (`còn N ngày` — cam khi < 10, hoặc `close_reason_text`); Báo giá = mã link (nowrap) + `(nháp)` nếu `quotation_is_draft` + "Người xử lý: …"; Hợp đồng = mã link + "Duyệt dd/mm/yyyy".
  - Mã báo giá/HĐ link tới `/customer-care/wr-quotations/{id}` và màn xem HĐ tương ứng (kiểm route thật trước khi gắn).
- [x] **Step 5: Menu** — `presale.js` nhóm "Báo cáo thị trường", sau dòng CSKH tiềm năng: `{ label: 'Báo cáo tổng hợp nhu cầu làm dịch vụ', link: '/assign/report/service-demand' },` (không `isShow`, giống mục CSKH tiềm năng — BE lọc).
- [x] **Step 6: Kiểm Playwright MCP** ở 1366 / 1600 / 1920px, so từng số với comment đầu `mockup.html`:
  - không cuộn ngang; không ô nào `scrollWidth > clientWidth`; tiêu đề cột cao ≤ 49px;
  - `th` 12px/800 `#0a7c88`, dòng TỔNG nền `#fdf1ea`, dòng tỉnh mở nền `#dceaf4` + `::before` 3px `#0a7c88`;
  - menu "Báo cáo tổng hợp nhu cầu làm dịch vụ" hiện trong hub Báo cáo (đếm link bằng DOM);
  - đổi Kỳ → `.rsum-goal` đổi nhãn; chọn Tuỳ chọn → hiện ô Thời gian;
  - đăng nhập user **không quyền** → chỉ thấy nhu cầu của mình (so số dòng với API).
- [x] **Step 7: Commit** (hrm-client) — message `Báo cáo tổng hợp nhu cầu làm dịch vụ: bộ lọc, khối tổng hợp, bảng cây`.

---

### Task 14: Popup drill, panel meeting, in / xuất Excel (FE)

**Files:**
- Create: `hrm-client/pages/assign/report/service-demand/components/DemandListModal.vue`, `PrintOptionsModal.vue`
- Modify: `hrm-client/pages/assign/report/service-demand/index.vue`

- [x] **Step 1: `DemandListModal.vue`** — dùng `V2BaseReportModal` + `reportDrillListMixin` (spec `.plans/gop-db/base-popup-bao-cao/design.md`; khuôn gần nhất `pages/sale/prepick-tracking/components/HoldListModal.vue`):
  - banner: lead "Bạn đang xem nhu cầu làm dịch vụ:", title = filter.title, meta `"{n} nhu cầu · Kỳ {label} ({from} – {to})"`, có nút toàn màn hình;
  - bộ lọc riêng: tìm (khách hàng / meeting / báo giá) · Tỉnh · Phòng ban · Chủ trì · Trạng thái · Người xử lý; đổi lọc → trang 1; đếm "N / M nhu cầu";
  - cột (schema, `cell-<key>` slots — memory V2BaseDataTable): STT · Tỉnh / thành phố ⇅ · Khách hàng ⇅ · Người liên hệ · Meeting xác định nhu cầu · Ngày hoàn thành ⇅ · Người chủ trì · Trạng thái · Báo giá · Hợp đồng — ô hiển thị y bảng chính;
  - footer: In danh sách · Xuất Excel danh sách (success) · Đóng;
  - bấm mã meeting → emit `open-meeting`.
- [x] **Step 2: Panel meeting** trong `index.vue`:

```vue
        <MeetingDetailDrawer
            :show="meetingDrawer.show"
            :item="{ type: 'meeting', id: meetingDrawer.id }"
            :above-modal="drillOpen"
            :extra-blocks="meetingDrawer.extraBlocks"
            header-gradient="linear-gradient(135deg, #0a1c3d, #06b6d4)"
            @close="meetingDrawer.show = false"
            @edit="goEditMeeting"
            @view-report="openMeetingReport"
        />
```
  import `MeetingDetailDrawer from '@/pages/assign/my-todo/components/calendar/WorkItemDetailDrawer.vue'`. `extraBlocks` = `[{ title: 'Nhu cầu làm dịch vụ', fields: [{label:'Trạng thái', value: status_text, color: status_color}, {label:'Hạn theo dõi', value: days_left !== null ? 'còn ' + days_left + ' ngày' : '—'}, {label:'Báo giá', value: quotation_code || '—'}, {label:'Người xử lý', value: handler_name || '—'}, {label:'Hợp đồng', value: contract_code || '—'}, {label:'Lý do đóng', value: close_reason_text || '—'}] }]`. `goEditMeeting` / `openMeetingReport` copy từ `pages/assign/report/potential-customer-care/index.vue:607-633`.
  > **`WorkItemDetailDrawer` CHƯA có prop đổi gradient** (header tính màu theo loại ở L283-287). Thêm prop tuỳ chọn `headerGradient: { type: String, default: '' }` — có giá trị thì dùng, không thì giữ công thức cũ. Đây là component dùng chung: mở báo cáo CSKH tiềm năng + màn my-todo kiểm lại header vẫn như cũ (đo `backgroundImage`).
- [x] **Step 3: In / Excel** — copy `prepick-tracking/components/PrintOptionsModal.vue` + `reportPrintPreviewMixin` (`ReportPrintPreviewModal`), endpoint Task 11; nút Excel gọi `/export` với đúng bộ lọc đang áp.
- [x] **Step 4: Kiểm Playwright MCP:**
  - bấm số "Đã lập báo giá" ở khối tổng hợp → popup có đúng số dòng = số trên ô; bấm "Hà Nội · N báo giá" → popup N dòng, tiêu đề "… · Đã có báo giá";
  - trong popup bấm mã meeting → panel hiện TRÊN popup (`elementFromPoint` trong vùng panel trả về panel), header `backgroundImage` = `linear-gradient(135deg, rgb(10, 28, 61), rgb(6, 182, 212))`, có khối "Nhu cầu làm dịch vụ";
  - đóng panel → popup vẫn mở; bấm nền ngoài → đóng popup;
  - mở `/assign/report/service-demand?demand_id=<id>` → panel tự mở đúng nhu cầu;
  - In danh sách mở preview; Xuất Excel tải được file.
  - Header panel ở `/assign/report/potential-customer-care` KHÔNG đổi.
- [x] **Step 5: Commit** (hrm-client) — message `Báo cáo nhu cầu làm dịch vụ: popup danh sách, panel meeting, in và xuất Excel`.

---

### Task 15: E2E + chốt tài liệu

**Files:**
- Create: `HRM/e2e/utils/serviceDemandFixture.ts`, `HRM/e2e/tests/assign/service-demand.api.spec.ts`, `HRM/e2e/tests/assign/service-demand.spec.ts`
- Modify: `.plans/gop-db/STATUS.md`, `.plans/gop-db/bao-cao-nhu-cau-dich-vu/plan.md` (checkpoint)

- [x] **Step 1: Fixture** theo khuôn `utils/prepickTrackingFixture.ts`: seed 4 nhu cầu (1 mỗi trạng thái) cho user e2e + 2 user `noperm` và `perm` (chỉ quyền 1660 gán trực tiếp); gọi `flushApiPermissionCache()` sau mỗi lần cấp/thu quyền.
- [x] **Step 2: API spec** — (a) số của riêng fixture theo từng trạng thái khớp `summary.by_status`; (b) `total.needs` = tổng `groups[].needs`; (c) `noperm` không thấy nhu cầu của người khác, `perm` thấy; (d) `demand-list?status=2` = số ô Đã lập báo giá.
- [x] **Step 3: UI spec** (serial) — khuôn đo của `tests/sale/prepick-tracking.spec.ts`: footer không đè bảng, sticky header, số khối cuộn = 1, badge đúng màu, InfoTip ở Công ty/Phòng ban/Người xử lý, drill → popup → panel `above-modal`, ô chọn nhu cầu ở form báo giá (Lưu nháp + Lưu và duyệt). Dùng `getByRole` không regex có glyph icon cho nút V2BaseButton (memory).
- [x] **Step 4:** Chỉ chạy nếu user yêu cầu: `npx playwright test tests/assign/service-demand* --project=api --no-deps --workers=1` rồi project UI; đọc dòng tổng kết (serial: "did not run" ≠ passed).
- [x] **Step 5:** Cập nhật `STATUS.md` (trạng thái + hash commit 2 repo) + checkpoint cuối plan.md. Chạy `git grep -n '<<<<<<<\|>>>>>>>'` cả 2 repo trước khi báo xong.

---

## Checkpoint

- 04/10/2026: plan viết xong, chờ user duyệt + chọn cách thực thi. Chưa đụng source.
- 04/10/2026: thực thi Subagent-driven xong 15/15 task (mỗi task review riêng; Task 10/13/14 qua 1 vòng sửa) + review toàn nhánh + 1 lượt sửa cuối. API 27f222a83..3e21fea8c · FE 6e31e81ae..2873546e3. Lệch plan có ghi nhận: entity extends BaseModel (+created_by/updated_by); quyền công ty = công ty ∪ (chủ trì/dự họp/người xử lý); demand-list thêm `id`, `pv=0`, `q`; print-list-data trả {template,…} theo skill print-page; khoá dòng khi gắn nhu cầu (chống tranh chấp); cron có `--demand=*` cho test. Còn chờ user: panel meeting 403, prefix NCDV, nghĩa cột Hợp đồng, chạy backfill thật, chạy e2e, push/merge.
- 04/10/2026: e2e chạy (API 19/19, UI 16+1 skip); sửa sticky header (FE 9d09740d1); MERGE --no-ff + PUSH gop_db: hrm-api 706635ece, hrm-client 1ad497c05. Còn mở: panel meeting 403 (chờ user), prefix NCDV, nghĩa cột Hợp đồng.
- 04/10/2026 (lượt 2): nới quyền xem meeting (1660/1661, meeting có nhu cầu), đếm HĐ có hiệu lực, duyệt prefix NCDV → MERGE + PUSH gop_db: hrm-api b211161a1, hrm-client 01a5d1b92. Worktree + SDD workspace đã xoá. Feature đóng, chờ deploy.

### Checkpoint — 2026-10-04 (wrap up)
Vừa hoàn thành: toàn bộ 15 task + review cuối + e2e (API 21/21 · UI 16 + 1 skip) + lượt 2 (nới Meeting::canView theo quyền báo cáo, đếm HĐ có hiệu lực, duyệt prefix NCDV). Đã MERGE + PUSH gop_db: hrm-api b211161a1 · hrm-client 01a5d1b92. Worktree đã xoá.
Đang làm dở: không.
Bước tiếp theo: deploy theo checklist ở STATUS.md (migrate 2 file 2026_10_05_* · INSERT tay quyền 1660/1661 + cache:clear · backfill --dry-run rồi chạy thật · gán quyền cho role). Sau deploy: kiểm ca e2e 15 (lập báo giá từ phiếu CCTT) trên môi trường có dữ liệu.
Blocked:

