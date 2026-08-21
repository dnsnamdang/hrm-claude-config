# Phiếu chờ duyệt tập trung (ERP) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development hoặc superpowers:executing-plans để thực thi từng task. Các step dùng checkbox (`- [ ]`).

**Goal:** Gom mọi "phiếu chờ duyệt" của ~130 luồng ERP về 1 màn tập trung (hộp duyệt cá nhân, lọc + deep-link mở phiếu) + 1 màn Báo cáo phê duyệt, backed bởi bảng registry `approval_inbox` + log `approval_inbox_logs`.

**Architecture:** Mỗi luồng nghiệp vụ đẩy trạng thái phiếu vào registry qua `ApprovalInboxService` (push/advance/resolve). Màn tập trung + báo cáo chỉ ĐỌC registry/log. Không sửa logic duyệt gốc; nút "Duyệt" deep-link `route('<luồng>.show', id)` sang màn sẵn có.

**Tech Stack:** PHP 7.4, Laravel 8, MySQL, Blade + AngularJS 1.3.9, Yajra DataTables (server-side), maatwebsite/excel, spatie-like `Permission` model (`app/Model/Common/Permission.php`), `Auth::user()->can()`.

## Global Constraints

- Dự án ERP `TanPhatDev`, nhánh hiện tại **`master`** → **tạo feature branch** trước khi code (vd `phieu-cho-duyet-tap-trung`). Hỏi user xác nhận nhánh.
- ERP-first: `source_system='erp'`. Sau khi gộp DB xong, HRM ghi chung bảng này (ngoài phạm vi plan).
- **KHÔNG sửa logic duyệt gốc của từng luồng** — chỉ CHÈN lời gọi `ApprovalInboxService` cạnh chỗ đổi `status`.
- Current user: `Auth::user()`; company của user: `auth()->user()->info->company_id`; user id: `Auth::user()->id`; quyền: `Auth::user()->can('<tên quyền>')`.
- Quy ước status registry: `1=pending, 2=approved, 3=rejected, 4=canceled`.
- **Verification (bám thực tế ERP — không có test DB cho feature legacy mới):** mỗi task verify bằng `php -l` (lint) + `php artisan migrate` trên dev + **kịch bản tinker** (theo Data Fix Pattern trong CLAUDE.md) + **Playwright browser** cho màn hình. PHPUnit tồn tại (`phpunit.xml`) nhưng test DB gộp không ổn định → dùng tinker làm bước verify chính; unit test thuần (không DB) thêm khi khả thi.
- Không commit/push khi chưa có yêu cầu (theo CLAUDE.md). Mỗi task kết thúc bằng 1 commit cục bộ trên feature branch.

---

## Phase 0 — Khảo sát & Thiết kế ✅
- [x] Kiểm tra nhánh git (ERP=master; HRM=gop_db)
- [x] Khảo sát HRM (7 module) + ERP (~130 khối, 24 nhóm)
- [x] Chốt quyết định thiết kế + inventory authoritative (xem Phase 3)
- [x] `design.md` (schema + push + màn + báo cáo + edge case)
- [x] Mockup `mockup.html` (màn tập trung) + `mockup-report.html` (báo cáo) — verify Playwright 1440, **user đã chốt**

---

## Phase 1 — Khung (Framework)

### Task 1: Migration bảng `approval_inbox`

**Files:**
- Create: `database/migrations/2026_08_12_000001_create_approval_inbox_table.php`

**Produces:** bảng `approval_inbox` với unique `(source_system, source_table, source_id)`.

- [ ] **Step 1: Viết migration**
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateApprovalInboxTable extends Migration
{
    public function up()
    {
        Schema::create('approval_inbox', function (Blueprint $t) {
            $t->bigIncrements('id');
            $t->string('source_system', 10)->default('erp');
            $t->string('doc_type', 64);
            $t->string('doc_type_label', 255)->nullable();
            $t->string('group_code', 64)->nullable();
            $t->string('source_table', 64);
            $t->unsignedBigInteger('source_id');
            $t->string('code', 64)->nullable();
            $t->string('title', 500)->nullable();
            $t->unsignedBigInteger('requester_id')->nullable();
            $t->string('requester_name', 255)->nullable();
            $t->date('document_date')->nullable();
            $t->string('required_permission', 255);
            $t->json('alt_permissions')->nullable();
            $t->unsignedBigInteger('company_id')->nullable();
            $t->unsignedBigInteger('department_id')->nullable();
            $t->unsignedBigInteger('part_id')->nullable();
            $t->unsignedBigInteger('approver_id')->nullable();
            $t->unsignedTinyInteger('current_level')->default(1);
            $t->dateTime('level_started_at')->nullable();
            $t->unsignedTinyInteger('round')->default(1);
            $t->decimal('amount', 20, 2)->nullable();
            $t->string('approve_route', 255)->nullable();
            $t->json('approve_params')->nullable();
            $t->unsignedTinyInteger('status')->default(1);
            $t->dateTime('resolved_at')->nullable();
            $t->unsignedBigInteger('resolved_by')->nullable();
            $t->unsignedBigInteger('created_by')->nullable();
            $t->unsignedBigInteger('updated_by')->nullable();
            $t->timestamps();
            $t->unique(['source_system', 'source_table', 'source_id'], 'uq_inbox_source');
            $t->index(['status', 'required_permission', 'company_id'], 'idx_inbox_filter');
            $t->index('doc_type', 'idx_inbox_doctype');
            $t->index('group_code', 'idx_inbox_group');
        });
    }
    public function down() { Schema::dropIfExists('approval_inbox'); }
}
```
- [ ] **Step 2: Lint** — `php -l database/migrations/2026_08_12_000001_create_approval_inbox_table.php` → No syntax errors
- [ ] **Step 3: Migrate dev** — `php artisan migrate --path=database/migrations/2026_08_12_000001_create_approval_inbox_table.php` → Migrated. Verify tinker: `php artisan tinker` → `Schema::hasTable('approval_inbox')` = true
- [ ] **Step 4: Commit** — `git add database/migrations/2026_08_12_000001_create_approval_inbox_table.php && git commit -m "feat(approval-inbox): migration bảng approval_inbox"`

### Task 2: Migration bảng `approval_inbox_logs`

**Files:**
- Create: `database/migrations/2026_08_12_000002_create_approval_inbox_logs_table.php`

**Produces:** bảng log bước duyệt (phục vụ báo cáo TG theo cấp + lý do từ chối).

- [ ] **Step 1: Viết migration**
```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateApprovalInboxLogsTable extends Migration
{
    public function up()
    {
        Schema::create('approval_inbox_logs', function (Blueprint $t) {
            $t->bigIncrements('id');
            $t->unsignedBigInteger('inbox_id');
            $t->unsignedTinyInteger('round')->default(1);
            $t->unsignedTinyInteger('level')->default(1);
            $t->string('required_permission', 255)->nullable();
            $t->unsignedBigInteger('actor_id')->nullable();
            $t->string('action', 20); // approve | reject | cancel
            $t->dateTime('started_at')->nullable();
            $t->dateTime('ended_at')->nullable();
            $t->string('note', 1000)->nullable();
            $t->timestamps();
            $t->index('inbox_id', 'idx_log_inbox');
            $t->index('actor_id', 'idx_log_actor');
            $t->index(['inbox_id', 'round', 'level'], 'idx_log_step');
        });
    }
    public function down() { Schema::dropIfExists('approval_inbox_logs'); }
}
```
- [ ] **Step 2: Lint** — `php -l database/migrations/2026_08_12_000002_create_approval_inbox_logs_table.php`
- [ ] **Step 3: Migrate dev** — `php artisan migrate --path=database/migrations/2026_08_12_000002_create_approval_inbox_logs_table.php`; tinker `Schema::hasTable('approval_inbox_logs')` = true
- [ ] **Step 4: Commit** — `git commit -am "feat(approval-inbox): migration bảng approval_inbox_logs"`

### Task 3: Models `ApprovalInbox` + `ApprovalInboxLog`

**Files:**
- Create: `app/Model/ApprovalInbox/ApprovalInbox.php`
- Create: `app/Model/ApprovalInbox/ApprovalInboxLog.php`

**Produces:** `ApprovalInbox::{PENDING,APPROVED,REJECTED,CANCELED}`; quan hệ `logs()`; casts json.

- [ ] **Step 1: ApprovalInbox model**
```php
<?php
namespace App\Model\ApprovalInbox;
use Illuminate\Database\Eloquent\Model;

class ApprovalInbox extends Model
{
    const PENDING = 1, APPROVED = 2, REJECTED = 3, CANCELED = 4;
    protected $table = 'approval_inbox';
    protected $guarded = [];
    protected $casts = ['alt_permissions' => 'array', 'approve_params' => 'array'];

    public function logs() { return $this->hasMany(ApprovalInboxLog::class, 'inbox_id', 'id'); }
}
```
- [ ] **Step 2: ApprovalInboxLog model**
```php
<?php
namespace App\Model\ApprovalInbox;
use Illuminate\Database\Eloquent\Model;

class ApprovalInboxLog extends Model
{
    protected $table = 'approval_inbox_logs';
    protected $guarded = [];
}
```
- [ ] **Step 3: Lint** — `php -l app/Model/ApprovalInbox/ApprovalInbox.php && php -l app/Model/ApprovalInbox/ApprovalInboxLog.php`
- [ ] **Step 4: Verify tinker** — `(new \App\Model\ApprovalInbox\ApprovalInbox)->getTable()` = `'approval_inbox'`; `\App\Model\ApprovalInbox\ApprovalInbox::PENDING` = 1
- [ ] **Step 5: Commit** — `git commit -am "feat(approval-inbox): models ApprovalInbox + ApprovalInboxLog"`

### Task 4: `ApprovalInboxService` (push / advance / resolve)

**Files:**
- Create: `app/Services/ApprovalInbox/ApprovalInboxService.php`

**Interfaces / Produces:**
- `push(array $e): ApprovalInbox` — tạo mới hoặc **tái kích hoạt** (round++) dòng đang resolved. `$e` keys: `source_table, source_id, doc_type, doc_type_label, group_code, code, title, requester_id, requester_name, document_date, required_permission, alt_permissions, company_id, department_id, part_id, approver_id, amount, approve_route, approve_params, level(optional)`.
- `advance(array $src, string $newPermission, int $newLevel, array $altPerms = [], $actorId = null): void`
- `resolve(array $src, string $status, $actorId = null, ?string $reason = null): void` — `$status` ∈ `approved|rejected|canceled`
- `$src` keys: `source_table, source_id, [source_system]`.

- [ ] **Step 1: Viết service**
```php
<?php
namespace App\Services\ApprovalInbox;

use App\Model\ApprovalInbox\ApprovalInbox;
use App\Model\ApprovalInbox\ApprovalInboxLog;
use Carbon\Carbon;

class ApprovalInboxService
{
    public function push(array $e): ApprovalInbox
    {
        $row = ApprovalInbox::firstOrNew([
            'source_system' => $e['source_system'] ?? 'erp',
            'source_table'  => $e['source_table'],
            'source_id'     => $e['source_id'],
        ]);
        $reactivating = $row->exists && (int) $row->status !== ApprovalInbox::PENDING;
        $row->fill([
            'doc_type' => $e['doc_type'],
            'doc_type_label' => $e['doc_type_label'] ?? null,
            'group_code' => $e['group_code'] ?? null,
            'code' => $e['code'] ?? null,
            'title' => $e['title'] ?? null,
            'requester_id' => $e['requester_id'] ?? null,
            'requester_name' => $e['requester_name'] ?? null,
            'document_date' => $e['document_date'] ?? null,
            'required_permission' => $e['required_permission'],
            'alt_permissions' => $e['alt_permissions'] ?? null,
            'company_id' => $e['company_id'] ?? null,
            'department_id' => $e['department_id'] ?? null,
            'part_id' => $e['part_id'] ?? null,
            'approver_id' => $e['approver_id'] ?? null,
            'amount' => $e['amount'] ?? null,
            'approve_route' => $e['approve_route'] ?? null,
            'approve_params' => $e['approve_params'] ?? null,
            'current_level' => $e['level'] ?? 1,
            'level_started_at' => Carbon::now(),
            'status' => ApprovalInbox::PENDING,
            'resolved_at' => null,
            'resolved_by' => null,
        ]);
        if ($reactivating) {
            $row->round = (int) $row->round + 1;
        }
        $row->save();
        return $row;
    }

    public function advance(array $src, string $newPermission, int $newLevel, array $altPerms = [], $actorId = null): void
    {
        $row = $this->find($src);
        if (!$row) return;
        ApprovalInboxLog::create([
            'inbox_id' => $row->id, 'round' => $row->round, 'level' => $row->current_level,
            'required_permission' => $row->required_permission, 'actor_id' => $actorId,
            'action' => 'approve', 'started_at' => $row->level_started_at, 'ended_at' => Carbon::now(),
        ]);
        $row->update([
            'required_permission' => $newPermission,
            'alt_permissions' => $altPerms ?: null,
            'current_level' => $newLevel,
            'level_started_at' => Carbon::now(),
        ]);
    }

    public function resolve(array $src, string $status, $actorId = null, ?string $reason = null): void
    {
        $row = $this->find($src);
        if (!$row) return;
        $map = ['approved' => ApprovalInbox::APPROVED, 'rejected' => ApprovalInbox::REJECTED, 'canceled' => ApprovalInbox::CANCELED];
        ApprovalInboxLog::create([
            'inbox_id' => $row->id, 'round' => $row->round, 'level' => $row->current_level,
            'required_permission' => $row->required_permission, 'actor_id' => $actorId,
            'action' => $status === 'approved' ? 'approve' : ($status === 'rejected' ? 'reject' : 'cancel'),
            'started_at' => $row->level_started_at, 'ended_at' => Carbon::now(), 'note' => $reason,
        ]);
        $row->update([
            'status' => $map[$status] ?? ApprovalInbox::CANCELED,
            'resolved_at' => Carbon::now(), 'resolved_by' => $actorId,
        ]);
    }

    protected function find(array $src): ?ApprovalInbox
    {
        return ApprovalInbox::where('source_system', $src['source_system'] ?? 'erp')
            ->where('source_table', $src['source_table'])
            ->where('source_id', $src['source_id'])->first();
    }
}
```
- [ ] **Step 2: Lint** — `php -l app/Services/ApprovalInbox/ApprovalInboxService.php`
- [ ] **Step 3: Verify tinker (kịch bản end-to-end nhiều vòng + nhiều cấp)** — chạy:
```php
$s = new \App\Services\ApprovalInbox\ApprovalInboxService();
$src = ['source_table' => 'firm_contracts', 'source_id' => 999999];
$s->push(['source_table'=>'firm_contracts','source_id'=>999999,'doc_type'=>'firm_contract','group_code'=>'QUAN_LY_HOP_DONG','required_permission'=>'Duyệt hợp đồng','company_id'=>1,'code'=>'HĐ-TEST','approve_route'=>'firmContract.show']);
$s->advance($src, 'Ban giám đốc duyệt', 2);          // duyệt cấp 1 → sang cấp 2
$s->resolve($src, 'rejected', 1, 'Thiếu chứng từ');   // BGĐ từ chối
$s->push(['source_table'=>'firm_contracts','source_id'=>999999,'doc_type'=>'firm_contract','group_code'=>'QUAN_LY_HOP_DONG','required_permission'=>'Duyệt hợp đồng','company_id'=>1,'code'=>'HĐ-TEST','approve_route'=>'firmContract.show']); // gửi lại
$row = \App\Model\ApprovalInbox\ApprovalInbox::where('source_id',999999)->first();
// KỲ VỌNG: status=1 (pending), round=2, current_level=1; logs()->count()=2 (1 approve cấp1, 1 reject có note)
[$row->status, $row->round, $row->current_level, $row->logs()->count(), $row->logs()->where('action','reject')->first()->note];
// dọn: $row->logs()->delete(); $row->delete();
```
Expected: `[1, 2, 1, 2, "Thiếu chứng từ"]`
- [ ] **Step 4: Commit** — `git commit -am "feat(approval-inbox): ApprovalInboxService push/advance/resolve"`

### Task 5: Config map `doc_type` → route/bảng/quyền/nhóm

**Files:**
- Create: `config/approval_inbox.php`

**Produces:** `config('approval_inbox.types')` — map mỗi `doc_type` → `['label','group','source_table','approve_route','permissions'=>[...cấp...]]`. Dùng cho push, backfill, và hiển thị. Điền dần theo Phase 3 (bắt đầu nhóm pilot).

- [ ] **Step 1: Tạo config (khởi tạo nhóm pilot QUAN_LY_HOP_DONG + QUAN_LY_BAO_GIA)**
```php
<?php
return [
    'types' => [
        'firm_contract' => [
            'label' => 'Hợp đồng bán hàng', 'group' => 'QUAN_LY_HOP_DONG',
            'source_table' => 'firm_contracts', 'approve_route' => 'firmContract.show',
            'permissions' => ['Duyệt hợp đồng'],
        ],
        'project_quotation' => [
            'label' => 'Báo giá dự án', 'group' => 'QUAN_LY_BAO_GIA',
            'source_table' => 'project_quotations', 'approve_route' => 'ProjectQuotation.show',
            'permissions' => ['Duyệt báo giá'],
        ],
        // ... bổ sung dần theo Phase 3
    ],
    'groups' => [ // code => label (24 nhóm — copy từ approveList)
        'QUAN_LY_HOP_DONG' => 'Quản lý hợp đồng',
        'QUAN_LY_BAO_GIA' => 'Quản lý báo giá',
        // ... (điền đủ 24 nhóm)
    ],
];
```
- [ ] **Step 2: Lint** — `php -l config/approval_inbox.php`
- [ ] **Step 3: Verify tinker** — `config('approval_inbox.types.firm_contract.approve_route')` = `'firmContract.show'`
- [ ] **Step 4: Commit** — `git commit -am "feat(approval-inbox): config map doc_type (pilot 2 nhóm)"`

### Task 6: Permission màn tập trung + báo cáo

**Files:**
- Modify: `database/seeds/PermissionsTableSeeder.php` (thêm ở cuối)

**Produces:** 2 quyền: `Xem phiếu chờ duyệt tập trung`, `Xem báo cáo phê duyệt`.

- [ ] **Step 1: Xác định id kế tiếp** — `grep -oE "'id' => [0-9]+" database/seeds/PermissionsTableSeeder.php | sort -t' ' -k3 -n | tail -1` → lấy id lớn nhất, +1/+2 cho 2 quyền mới (gọi `<ID1>`, `<ID2>`)
- [ ] **Step 2: Thêm vào seeder** (đặt trước dòng đóng hàm)
```php
Permission::create(['id' => <ID1>, 'name' => 'Xem phiếu chờ duyệt tập trung', 'display_name' => 'Xem', 'group' => 'Phiếu chờ duyệt tập trung', 'group_category' => 'Hệ thống']);
Permission::create(['id' => <ID2>, 'name' => 'Xem báo cáo phê duyệt', 'display_name' => 'Xem', 'group' => 'Phiếu chờ duyệt tập trung', 'group_category' => 'Hệ thống']);
```
- [ ] **Step 3: Lint** — `php -l database/seeds/PermissionsTableSeeder.php`
- [ ] **Step 4: Insert dev (không reseed toàn bộ)** — tinker:
```php
\App\Model\Common\Permission::create(['id'=><ID1>,'name'=>'Xem phiếu chờ duyệt tập trung','display_name'=>'Xem','group'=>'Phiếu chờ duyệt tập trung','group_category'=>'Hệ thống']);
\App\Model\Common\Permission::create(['id'=><ID2>,'name'=>'Xem báo cáo phê duyệt','display_name'=>'Xem','group'=>'Phiếu chờ duyệt tập trung','group_category'=>'Hệ thống']);
```
Gán 2 quyền cho role của user test → verify `Auth::user()->can('Xem phiếu chờ duyệt tập trung')`.
- [ ] **Step 5: Commit** — `git commit -am "feat(approval-inbox): thêm 2 permission màn tập trung + báo cáo"`

### Task 7: Command backfill `approval-inbox:backfill`

**Files:**
- Create: `app/Console/Commands/BackfillApprovalInbox.php`
- Modify: `app/Console/Kernel.php` (đăng ký command)

**Produces:** `php artisan approval-inbox:backfill {group?}` — quét trạng thái pending hiện tại của các luồng (theo Phase 3, dùng chính điều kiện lọc của `approveList`) và `push()` vào registry (idempotent). Bắt đầu nhóm pilot.

- [ ] **Step 1: Command (khởi tạo backfill nhóm QUAN_LY_HOP_DONG — firm_contract)**
```php
<?php
namespace App\Console\Commands;

use App\Model\Sale\Firm\Contract\FirmContract;
use App\Services\ApprovalInbox\ApprovalInboxService;
use Illuminate\Console\Command;

class BackfillApprovalInbox extends Command
{
    protected $signature = 'approval-inbox:backfill {group?}';
    protected $description = 'Nạp phiếu chờ duyệt hiện tại vào registry approval_inbox';

    public function handle(ApprovalInboxService $svc)
    {
        $group = $this->argument('group');
        if (!$group || $group === 'QUAN_LY_HOP_DONG') {
            $n = 0;
            FirmContract::where('status', FirmContract::CHO_DUYET)->chunkById(200, function ($rows) use ($svc, &$n) {
                foreach ($rows as $c) {
                    $svc->push([
                        'source_table' => 'firm_contracts', 'source_id' => $c->id,
                        'doc_type' => 'firm_contract', 'doc_type_label' => 'Hợp đồng bán hàng',
                        'group_code' => 'QUAN_LY_HOP_DONG', 'code' => $c->code,
                        'requester_id' => $c->created_by, 'company_id' => $c->company_id,
                        'approver_id' => $c->approver_id, 'required_permission' => 'Duyệt hợp đồng',
                        'approve_route' => 'firmContract.show',
                        'approve_params' => ['id' => $c->id],
                    ]);
                    $n++;
                }
            });
            $this->info("QUAN_LY_HOP_DONG: đã nạp {$n} phiếu.");
        }
        return 0;
    }
}
```
> Lưu ý: xác nhận hằng `FirmContract::CHO_DUYET` (mẫu `FirmContract.php:97-110`); tên cột `approver_id`/`company_id` theo model thật.
- [ ] **Step 2: Đăng ký** trong `app/Console/Kernel.php` mảng `$commands` (nếu chưa auto-load): thêm `\App\Console\Commands\BackfillApprovalInbox::class`
- [ ] **Step 3: Lint** — `php -l app/Console/Commands/BackfillApprovalInbox.php`
- [ ] **Step 4: Verify** — `php artisan approval-inbox:backfill QUAN_LY_HOP_DONG` → in số phiếu; tinker `\App\Model\ApprovalInbox\ApprovalInbox::where('doc_type','firm_contract')->count()` > 0 và khớp `FirmContract::where('status',2)->count()`. Chạy lại lần 2 → count KHÔNG tăng (idempotent).
- [ ] **Step 5: Commit** — `git commit -am "feat(approval-inbox): command backfill (nhóm hợp đồng)"`

### Task 8: Controller + routes màn tập trung

**Files:**
- Create: `app/Http/Controllers/ApprovalInbox/ApprovalInboxController.php`
- Modify: `routes/web.php` (trong group `admin`)

**Interfaces / Produces:** route `approvalInbox.index`, `approvalInbox.searchData`; query "phiếu cần tôi duyệt".

- [ ] **Step 1: Controller**
```php
<?php
namespace App\Http\Controllers\ApprovalInbox;

use App\Http\Controllers\Controller;
use App\Model\ApprovalInbox\ApprovalInbox;
use Illuminate\Http\Request;
use Yajra\DataTables\DataTables;

class ApprovalInboxController extends Controller
{
    public function index()
    {
        return view('approval_inbox.index', [
            'groups' => config('approval_inbox.groups', []),
            'types'  => config('approval_inbox.types', []),
        ]);
    }

    public function searchData(Request $request)
    {
        $query = $this->pendingForCurrentUser();
        return DataTables::of($query)
            ->editColumn('document_date', fn($o) => optional($o->document_date)->format('d/m/Y'))
            ->addColumn('action', function ($o) {
                $url = $o->approve_route ? route($o->approve_route, ($o->approve_params['id'] ?? $o->source_id)) : '#';
                return '<a href="' . $url . '" class="btn btn-sm btn-success">Duyệt</a>';
            })
            ->rawColumns(['action'])
            ->make(true);
    }

    /** Phiếu đang chờ mà user hiện tại có quyền duyệt (theo quyền + phạm vi công ty) hoặc là approver đích danh. */
    protected function pendingForCurrentUser()
    {
        $user = auth()->user();
        $companyId = optional($user->info)->company_id;

        // các quyền duyệt mà user thực sự có, trong tập required_permission đang pending
        $perms = ApprovalInbox::where('status', ApprovalInbox::PENDING)
            ->distinct()->pluck('required_permission')
            ->filter(fn($p) => $user->can($p))->values()->all();

        return ApprovalInbox::where('status', ApprovalInbox::PENDING)
            ->where(function ($q) use ($perms, $companyId, $user) {
                $q->where(function ($q2) use ($perms, $companyId) {
                    $q2->whereIn('required_permission', $perms)
                       ->where(function ($q3) use ($companyId) {
                           $q3->whereNull('company_id')->orWhere('company_id', $companyId);
                       });
                })->orWhere('approver_id', $user->id);
            });
    }
}
```
> Lọc phạm vi v1 = theo `company_id` của user. Biến thể "xem theo tổng công ty/phòng ban" xử lý ở Phase sau khi gắn luồng có scope đó.
- [ ] **Step 2: Routes** (thêm trong `Route::group(['prefix'=>'admin','middleware'=>['sso.check','userLogin']], ...)`)
```php
Route::group(['prefix' => 'approval-inbox'], function () {
    Route::get('/', 'ApprovalInbox\ApprovalInboxController@index')->name('approvalInbox.index')->middleware('checkPermission:Xem phiếu chờ duyệt tập trung');
    Route::get('/search-data', 'ApprovalInbox\ApprovalInboxController@searchData')->name('approvalInbox.searchData');
});
```
> Xác nhận tên middleware quyền của ERP (`checkPermission` hoặc tương đương) — grep `CheckPermission` trong `app/Http/Middleware`.
- [ ] **Step 3: Lint** — `php -l app/Http/Controllers/ApprovalInbox/ApprovalInboxController.php`
- [ ] **Step 4: Verify** — `php artisan route:list | grep approvalInbox` hiện 2 route.
- [ ] **Step 5: Commit** — `git commit -am "feat(approval-inbox): controller + routes màn tập trung"`

### Task 9: Blade màn tập trung (DataTable + AngularJS) — port `mockup.html`

**Files:**
- Create: `resources/views/approval_inbox/index.blade.php`

**Consumes:** route `approvalInbox.searchData`; `config('approval_inbox.*')`. **FE source of truth = `mockup.html`** (bố cục, cột, bộ lọc, badge nhóm, deep-link nút Duyệt).

- [ ] **Step 1: Viết Blade** theo khung DataTable chuẩn ERP (`@extends('layouts.app')`, `.card > .card-block > table`, `new DATATABLE('table-id', {...})`), cột: STT · Loại phiếu · Mã · Đối tác · Người yêu cầu · Ngày lập · Cấp duyệt · Hành động; `search_columns`: doc_type (select từ config types), group_code (select), created_by (select-ajax `employee.searchEmployeeByKeyword`), `search_by_time: true`. Sidebar "Lọc theo nhóm" = list `config('approval_inbox.groups')` + count (đọc từ 1 endpoint đếm hoặc render server). Nút Duyệt = link `approve_route` (đã build ở controller addColumn).
- [ ] **Step 2: Verify Playwright 1440** — đăng nhập user có quyền + có phiếu (đã backfill Task 7). Chụp: danh sách hiện phiếu firm_contract, lọc theo nhóm/loại chạy, nút Duyệt điều hướng `firmContract.show/{id}`. 0 lỗi console Angular.
- [ ] **Step 3: Commit** — `git commit -am "feat(approval-inbox): màn tập trung (Blade + DataTable)"`

### Task 10: Controller + route Báo cáo phê duyệt

**Files:**
- Modify: `app/Http/Controllers/ApprovalInbox/ApprovalInboxController.php` (thêm `report`, `reportData`)
- Modify: `routes/web.php`

**Produces:** route `approvalInbox.report`, `approvalInbox.reportData` — trả KPI + chuỗi thời gian + phân bố nhóm + hiệu suất người duyệt + chi tiết, **đếm theo LƯỢT (log rows)**, TG theo từng cấp, lý do từ chối (`note`).

- [ ] **Step 1: Thêm methods** — `report()` trả view `approval_inbox.report` (options lọc: companies/depts/parts, approvers = distinct `actor_id` từ log, types). `reportData(Request)` tổng hợp từ `approval_inbox_logs` join `approval_inbox` với các filter: kỳ (started_at range), company/department/part (của inbox), actor_id (người duyệt), doc_type, action(result). Trả JSON:
```php
return response()->json([
  'kpi' => ['total'=>..,'approved'=>..,'rejected'=>..,'pending'=>..,'avg_hours'=>..,'overdue'=>..,'ontime_rate'=>..],
  'weekly' => [['label'=>'Tuần 01','approved'=>..,'rejected'=>..], ...],
  'groups' => [['name'=>..,'count'=>..], ...],
  'approvers' => [['name'=>..,'role'=>..,'dept'=>..,'approved'=>..,'rejected'=>..,'avg_hours'=>..,'longest'=>..], ...], // ẩn khi lọc 1 người
  'detail' => [['type'=>..,'code'=>..,'route'=>..,'id'=>..,'requester'=>..,'approver'=>..,'level'=>..,'sent'=>..,'done'=>..,'dur_hours'=>..,'result'=>..,'reason'=>..], ...],
]);
```
TG theo cấp = `TIMESTAMPDIFF(MINUTE, started_at, ended_at)` mỗi log; `pending` = count `approval_inbox` status=1 theo cùng filter org/type (không theo actor/result).
- [ ] **Step 2: Routes**
```php
Route::get('/report', 'ApprovalInbox\ApprovalInboxController@report')->name('approvalInbox.report')->middleware('checkPermission:Xem báo cáo phê duyệt');
Route::get('/report-data', 'ApprovalInbox\ApprovalInboxController@reportData')->name('approvalInbox.reportData');
```
- [ ] **Step 3: Lint + verify** — `php -l ...Controller.php`; gọi `/admin/approval-inbox/report-data` (browser hoặc `curl` sau auth) trả JSON đúng cấu trúc; đối chiếu KPI với tinker count trên log.
- [ ] **Step 4: Commit** — `git commit -am "feat(approval-inbox): controller báo cáo phê duyệt (đếm theo lượt)"`

### Task 11: Blade Báo cáo — port `mockup-report.html`

**Files:**
- Create: `resources/views/approval_inbox/report.blade.php`
- Create: `app/ExcelExports/ApprovalReportExport.php`
- Modify: routes (thêm `approvalInbox.reportExport`)

**Consumes:** `approvalInbox.reportData`. **FE source of truth = `mockup-report.html`** (bộ lọc cascade Công ty→Phòng ban duyệt→Bộ phận duyệt, KPI gọn, 2 biểu đồ, bảng người duyệt ẩn-khi-1-người, chi tiết + lý do từ chối + link mã phiếu, 1 nút Xuất Excel).

- [ ] **Step 1: Viết Blade** — port HTML/JS từ `mockup-report.html`, thay dữ liệu tĩnh bằng AJAX `approvalInbox.reportData`; cascade selects gọi endpoint org (hoặc `@json` companies/depts/parts từ controller); ẩn bảng hiệu suất khi chọn 1 người duyệt; mã phiếu link `route(<approve_route>, id)`.
- [ ] **Step 2: ApprovalReportExport** (maatwebsite/excel) — export chi tiết phiếu đã xử lý theo filter hiện tại, cột gồm **Lý do từ chối** riêng.
- [ ] **Step 3: Verify Playwright 1440** — mở `/admin/approval-inbox/report`: KPI/biểu đồ/bảng đổ từ data thật; lọc Công ty→Phòng→Bộ phận cascade đúng; chọn 1 người duyệt → ẩn bảng hiệu suất; lọc Kết quả=Từ chối → hiện lý do; bấm Xuất Excel tải file.
- [ ] **Step 4: Commit** — `git commit -am "feat(approval-inbox): màn Báo cáo phê duyệt + Excel export"`

### Task 12: Menu + badge đếm

**Files:**
- Modify: partial menu ngang (tìm: `grep -rn "Bán hàng" resources/views/layouts resources/views/partials`)
- Modify: `ApprovalInboxController` (hoặc composer) cung cấp badge count

**Produces:** mục menu "Phiếu chờ duyệt" (link `approvalInbox.index`) + badge số phiếu chờ của user; link phụ "Báo cáo phê duyệt".

- [ ] **Step 1: Thêm menu item** vào partial menu ngang (gate bằng quyền `Xem phiếu chờ duyệt tập trung`); badge = count `pendingForCurrentUser()` (dùng lại method Task 8, tách thành method public `pendingCountForCurrentUser()`).
- [ ] **Step 2: Verify Playwright** — menu hiện, badge đúng số, click vào ra màn tập trung; link Báo cáo ra màn báo cáo.
- [ ] **Step 3: Commit** — `git commit -am "feat(approval-inbox): menu + badge đếm phiếu chờ"`

---

## Phase 2 — Instrumentation template (mẫu gắn 1 luồng)

### Task 13: Template hook 1 luồng (áp cho firm_contract) — mẫu nhân bản Phase 3

**Mục tiêu:** chèn `push/advance/resolve` vào đúng chỗ đổi `status` của luồng, KHÔNG sửa logic duyệt. Đây là **khuôn mẫu** cho mọi luồng ở Phase 3.

**Files:** `app/Http/Controllers/Sale/Firm/FirmContractController.php` (các action: store/gửi duyệt, approve, reject/cancelApprove)

- [ ] **Step 1:** Tại chỗ phiếu **chuyển sang chờ duyệt** (store gửi duyệt / set `status=CHO_DUYET`): gọi
```php
app(\App\Services\ApprovalInbox\ApprovalInboxService::class)->push([
    'source_table'=>'firm_contracts','source_id'=>$contract->id,'doc_type'=>'firm_contract',
    'doc_type_label'=>'Hợp đồng bán hàng','group_code'=>'QUAN_LY_HOP_DONG','code'=>$contract->code,
    'requester_id'=>$contract->created_by,'company_id'=>$contract->company_id,'approver_id'=>$contract->approver_id,
    'required_permission'=>'Duyệt hợp đồng','approve_route'=>'firmContract.show','approve_params'=>['id'=>$contract->id],
]);
```
- [ ] **Step 2:** Tại action **approve** — nếu còn cấp sau: `advance($src, '<quyền cấp sau>', <level+1>, [], auth()->id())`; nếu cấp cuối: `resolve($src, 'approved', auth()->id())`. (`$src = ['source_table'=>'firm_contracts','source_id'=>$contract->id]`)
- [ ] **Step 3:** Tại action **reject/cancelApprove** — `resolve($src, 'rejected', auth()->id(), $request->reason)` (truyền lý do từ form).
- [ ] **Step 4:** Verify browser end-to-end: tạo HĐ gửi duyệt → hiện ở màn tập trung của người có quyền; duyệt → biến mất/chuyển cấp; từ chối có lý do → vào báo cáo (Kết quả=Từ chối kèm lý do); gửi lại → round=2. Đối chiếu registry/log bằng tinker.
- [ ] **Step 5: Commit** — `git commit -am "feat(approval-inbox): hook luồng firm_contract (template)"`

---

## Phase 3 — Gắn từng nhóm luồng (checklist — theo template Task 13)

> Mỗi mục = 1 luồng: (1) bổ sung `doc_type` vào `config/approval_inbox.php`; (2) hook push/advance/resolve theo Task 13; (3) thêm nhánh backfill trong command Task 7; (4) verify browser + tinker. "Quyền" = `required_permission` (nhiều giá trị = nhiều cấp → dùng `advance`). Route = deep-link `route('<prefix>.show', id)`.

### QUAN_LY_HOP_DONG (ưu tiên 1)
- [ ] Hợp đồng bán hàng — `Duyệt hợp đồng` + `approver_id` — `firmContract` *(đã làm mẫu ở Task 13)*
- [ ] Phụ lục bổ sung HĐ bán hàng — `Duyệt hợp đồng` — `firmContractAdditionAnnexes`
- [ ] Phụ lục giảm HĐ bán hàng — `Duyệt hợp đồng` — `firmContractAnnexes`
- [ ] Hợp đồng nguyên tắc — `Duyệt hợp đồng nguyên tắc` — `firmContract`
- [ ] Hợp đồng nguyên tắc nha khoa (Ztec) — `Duyệt hợp đồng nguyên tắc` — `zt.firmContract`
- [ ] Phụ lục bổ sung HĐ nguyên tắc — `firmContract`
- [ ] Đơn hàng nguyên tắc nha khoa — `zt.firmContract`
- [ ] Đơn hàng nguyên tắc — `firmContract`
- [ ] Phụ lục giảm Đơn hàng nguyên tắc nha khoa — `zt.firmContractAnnexes`
- [ ] Phụ lục giảm Đơn hàng nguyên tắc — `firmContractAnnexes`
- [ ] Hợp đồng Dự án — `firmContract`
- [ ] Phụ lục bổ sung HĐ Dự án — `firmContractAdditionAnnexes`
- [ ] Phụ lục giảm HĐ Dự án — `firmContractAnnexes`
- [ ] Hợp đồng nguyên tắc gia hạn — `firmContract`
- [ ] Hợp đồng dịch vụ sửa chữa (bảo hành) — `Duyệt hợp đồng` — `WarrantyRepairContracts`
- [ ] Phụ lục giảm HĐ dịch vụ sửa chữa — `Duyệt PL giảm HDDV` — `WarrantyRepairContractAnnex`
- [ ] Phụ lục bổ sung HĐ dịch vụ sửa chữa — `WarrantyRepairContractAdditionAnnex`

### QUAN_LY_BAO_GIA
- [ ] Báo giá dự án — `Duyệt báo giá` + `approver_id` — `ProjectQuotation`

### QUAN_LY_HANG_HOA
- [ ] Hàng tạm — `Duyệt hàng tạm` (hoặc theo Assign brand/manufacture) — `tmpProduct`
- [ ] Duyệt giá hàng hoá — `Duyệt giá hàng hoá` — `products.approvePrices`
- [ ] (Xem xét) Hàng không được duyệt giá bán — `Cập nhật nhanh giá hàng hóa`
- [ ] (Xem xét) Hàng hóa chờ nhập thông tin bán hàng — `Nhập thông tin quản lý bán hàng` — `product2`

### PHIEU_GIAO_CHI_TIEU
- [ ] Phiếu giao chỉ tiêu KD theo nhân viên — `Duyệt chỉ tiêu kinh doanh theo nhân viên` — `target_business_department`

### PHIEU_BAO_THUA_THIEU
- [ ] Phiếu báo thừa-thiếu nhập kho cần xử lý — `Duyệt phiếu báo hàng thừa, thiếu nhập kho` — `warehouseImport.excShortage`
- [ ] Phiếu báo thừa-thiếu nhập kho cần duyệt — `Duyệt phiếu xử lý hàng thiếu nhập kho` — `inventory.discrepancy`

### KE_TOAN_KHO / XUAT_NHAP_HANG (nhiều cấp: KT giữ / BGĐ / TP / BKS)
- [ ] Phiếu điều chuyển hàng giữ — `Kế toán|Ban giám đốc|Trưởng phòng duyệt hàng giữ` — `PrepickTransfer2`
- [ ] Phiếu YC xuất giữ — hàng giữ (nhiều cấp) — `productPrepickRequest`
- [ ] Phiếu YC gia hạn hàng giữ — `prepickExtendRequest`
- [ ] YC gia hạn hàng mượn — `TP|BGĐ duyệt hàng mượn`/`Kế toán kho` — `borrowExtendRequest`
- [ ] YC chuyển hàng — `Kế toán kho` — `productTransferRequest`
- [ ] Phiếu nhập kho điều chỉnh kiểm kê — `warehouseInventoryImport`
- [ ] Phiếu xuất kho điều chỉnh kiểm kê — `warehouseInventoryExport`
- [ ] Phiếu YC huỷ hàng giữ — `Quản lý giữ hàng`/`Ban kiểm soát duyệt giữ hàng` — `prepickCancelRequest`
- [ ] Phiếu YC xuất hàng — `Kế toán kho`/`TP|BGĐ duyệt hàng mượn` — `productExportRequest`
- [ ] Phiếu xuất kho — `warehouseExport`
- [ ] Phiếu YC nhập hàng — `productImportRequest`
- [ ] Phiếu nhập kho — `warehouseImport`
- [ ] YC xuất hàng mượn — `TP|BGĐ duyệt xuất hàng vượt hạn mức công nợ` — `borrowExportRequest`
- [ ] YC xuất bán hàng mượn — `borrowSellRequest`
- [ ] YC xuất ghép — `joinExportRequest`
- [ ] YC xuất tách — `splitExportRequest`
- [ ] Phiếu ĐN xuất kho — `Thủ kho` — `warehouseExportRequest`
- [ ] Phiếu ĐN nhập kho — `warehouseImportRequest`
- [ ] Phiếu xuất giữ chờ BKS duyệt — `Ban kiểm soát duyệt giữ hàng`/`Trưởng phòng kế toán` — `warehousePrepickRequest`
- [ ] Phiếu YC xuất hàng (XUAT_NHAP_HANG) — `TP|BGĐ duyệt xuất hàng vượt hạn mức công nợ` — `productExportRequest`
- [ ] Phiếu YC nhập hàng cần duyệt — `Ban kiểm soát|BGD duyệt giá nhập hàng trả lại` — `productImportRequest.forManager`
- [ ] Phiếu YC nhập hàng cần TP duyệt — `Trưởng phòng duyệt yêu cầu nhập hàng` — `productImportRequest.forDepartmentManager`
- [ ] Phiếu điều chuyển hàng nhập thẳng — `Kế toán kho` — `productImportDirectTransfers` *(nhóm HANG_NHAP_THANG_CAN_XUAT)*

### DAT_MUA_HANG_NHAP_KHAU
- [ ] Đơn hỏi hàng - PO (NK) — `Duyệt đơn hỏi hàng - PO nhập khẩu` — `orderSummary2`
- [ ] PI (NK) — `Duyệt PI mua hàng nhập khẩu` — `purchaseInvoice`
- [ ] HĐĐH nhập khẩu — `Duyệt hợp đồng mua hàng nhập khẩu` — `buyContract2`
- [ ] PI cần duyệt — `Duyệt PI` — `purchaseInvoice`
- [ ] Tờ khai hải quan — `Duyệt tờ khai hải quan` — `customDeclaration`

### DAT_MUA_HANG_NGOAI
- [ ] YCĐH ngoài (Trưởng phòng) — `Duyệt yêu cầu đặt hàng ngoài` — `inlandOrderRequest.forDepartmentApprover`
- [ ] YCĐH ngoài (Kiểm soát) — `Kiểm soát yêu cầu đặt hàng ngoài` — `inlandOrderRequest.forApprover`
- [ ] HĐĐH ngoài — `Duyệt hợp đồng đặt hàng ngoài` — `inlandBuyContract`
- [ ] Phụ lục HĐ mua hàng ngoài — `inlandBuyContractAnnex`
- [ ] Phụ lục giảm HĐ mua hàng ngoài — `inlandBuyContractAnnex2`

### DAT_MUA_HANG_TRONG_NUOC
- [ ] HĐ trong nước tự do — `Duyệt hợp đồng mua hàng trong nước` — `inlandBuyContractNew`
- [ ] HĐ nguyên tắc đặt hàng trong nước — `ruleInlandBuyContract`
- [ ] HĐ trong nước theo hãng — `inlandBuyContractNew`
- [ ] PI trong nước — `Duyệt PI mua hàng trong nước` — `inlandPurchaseInvoice`
- [ ] PI trong nước theo hãng — `inlandPurchaseInvoice`
- [ ] Đơn hỏi hàng - PO trong nước tự do — `Duyệt đơn hỏi hàng - PO trong nước` — `inlandOrderSummaryNew`
- [ ] Đơn hỏi hàng - PO trong nước theo hãng — `inlandOrderSummaryNew`
- [ ] PLBS trong nước tự do — `Duyệt hợp đồng mua hàng trong nước` — `inlandBuyContractNew`
- [ ] PLBS trong nước theo hãng — `inlandBuyContractNew`

### DAT_HANG
- [ ] Phiếu YC đặt hàng — `Trưởng phòng duyệt yêu cầu đặt hàng` — `rootOrderRequest`

### KE_TOAN_MUA_HANG
- [ ] Tổng hợp chi phí nhập khẩu — `Kế toán mua hàng` — `orderImportRequest`
- [ ] YC hỏi giá — `PTKD duyệt yêu cầu hỏi giá` — `PriceAskingRequest`
- [ ] YC hỏi giá cần XNK duyệt — `XNK duyệt yêu cầu hỏi giá` — `PriceAskingRequest`
- [ ] YC tính giá — `Kế toán mua hàng` — `PriceCalculateRequest`
- [ ] YC hỏi giá vận chuyển — `Mua hàng` — `DeliveryCostAskingRequest`

### DE_NGHI_THU_CHI
- [ ] Đề nghị thu tiền — `Kế toán thanh toán`/`Kế toán` — `bill_income_request`
- [ ] Phiếu YC điều chỉnh công nợ — `bill_adjust_dept_request`
- [ ] Phiếu YC hạch toán bổ sung — `additionAccountingRequest`
- [ ] Phiếu thu tiền — `Thủ quỹ duyệt phiếu thu` — `bill_income`
- [ ] Phiếu đề nghị thanh toán — `TP|KT công nợ|KT trưởng|BGĐ duyệt đề nghị thanh toán` (nhiều cấp) — `bill_payment_request`
- [ ] Phiếu chi (KT trưởng) — `Kế toán trưởng duyệt phiếu chi` — `bill_payment`
- [ ] Phiếu chi (Thủ quỹ) — `Thủ quỹ duyệt phiếu chi` — `bill_payment`

### HACH_QUYET_TOAN
- [ ] YC hạch toán hoa hồng tháng — `Duyệt yêu cầu hạch toán hoa hồng tháng` — `monthlyCommissionAccountingRequest`
- [ ] (Xem xét) Hạch toán CP vận chuyển nhanh — `Hạch toán chi phí vận chuyển nhanh` (+ 4 mức xem) — `orderReport.fastDelivery`
- [ ] Quyết toán hợp đồng — `Kế toán|Trưởng phòng duyệt quyết toán hợp đồng` (2 cấp) — `settlementContract`
- [ ] Quyết toán hoa hồng quý — `Duyệt quyết toán hoa hồng quý` — `bill_commission_settlement_quarters`

### YEU_CAU_LAM_DICH_VU
- [ ] Kết quả giao việc chờ hạch toán dịch vụ — `Kế toán kho` — `WrApproveResults`
- [ ] YC hạch toán dịch vụ cần duyệt — `WrAccountingServiceRequest`
- [ ] YC làm dịch vụ cần duyệt — `Duyệt yêu cầu làm dịch vụ` — `serviceExportRequest`
- [ ] YC hạch toán dịch vụ cần phê duyệt — `Hạch toán yêu cầu làm dịch vụ` — `serviceAccountingRequest`
- [ ] YC mua dịch vụ — `Ban kiểm soát duyệt giá mua dịch vụ`/`Trưởng phòng duyệt yêu cầu mua dịch vụ` — `buyServiceRequest`
- [ ] HĐ mua dịch vụ — `Duyệt hợp đồng mua dịch vụ` — `buyServiceContract`
- [ ] YC hạch toán mua dịch vụ — `Hạch toán mua dịch vụ` — `buyServiceAccountingRequest`

### BAO_HANH_SUA_CHUA
- [ ] YC sửa chữa - bảo hành cần xử lý — `Xử lý yêu cầu sửa chữa` — `warrantyRepairRequest`
- [ ] Chờ duyệt phiếu nhập kết quả giao việc — `Duyệt phiếu nhập kết quả` — `WrImportResults`
- [ ] Duyệt phiếu kết quả giao việc — `Ban kiểm soát duyệt kết quả giao việc` — `WrApproveResults`
- [ ] (Xem xét) Phiếu chờ giao việc — `Tạo phiếu giao việc` — `WrAssignTasks.wait`
- [ ] (Xem xét) YC xử lý SC-BH cần cung cấp thông tin — `warrantyRepairHandleRequest`
- [ ] (Xem xét) Phiếu cung cấp thông tin cần làm báo giá — `Tạo phiếu cung cấp thông tin` — `warrantyRepairInformationRequest`

### YEU_CAU_HANG_BAO_HANH
- [ ] Phiếu YC hãng bảo hành — `firmWarrantyRequest`
- [ ] Thư YC hãng bảo hành — `firmWarranty`
- [ ] Phiếu xác nhận bảo hành — `Duyệt phiếu xác nhận bảo hành` — `firmWarrantyConfirm`

### VAN_CHUYEN
- [ ] Tổng hợp giá vận chuyển đề xuất — `Duyệt giá vận chuyển` — `DeliveryCostSummary`
- [ ] Chuyến xe chở hàng chờ hạch toán — `Hạch toán vận chuyển` — `deliveryTrip`
- [ ] Chuyến xe khác chờ hạch toán — `Hạch toán vận chuyển` — `otherDeliveryTrip`
- [ ] Chuyến xe khác chờ duyệt — `Duyệt chuyến xe khác` — `otherDeliveryTrip`
- [ ] Tổng hợp vận chuyển quốc tế (BKS) — `Ban kiểm soát duyệt giá vận chuyển quốc tế` — `delivery_international_general`
- [ ] Tổng hợp vận chuyển quốc tế (TP) — `Trưởng phòng duyệt giá vận chuyển quốc tế` — `delivery_international_general`

### KIEM_KE
- [ ] Kiểm kê vị trí — `Ban kiểm soát duyệt kết quả kiểm kê` — `positionInventoryResult`
- [ ] Kiểm kê hàng hóa — `self_inventory`
- [ ] Kế hoạch kiểm kê vị trí — `Lập phiếu kiểm kê kho theo vị trí` — `positionInventory`

### KE_HOACH_PHAT_TRIEN_THI_TRUONG
- [ ] KH PTTT nhân viên — `plan_market_employee`
- [ ] KH PTTT phòng ban — `Duyệt kế hoạch phát triển thị trường phòng` — `plan_market_department`
- [ ] KH PTTT công ty — `Duyệt kế hoạch phát triển thị trường công ty` — `plan_market_company`

### KE_HOACH_BAN_HANG
- [ ] KH bán hàng nhân viên — `Trưởng phòng duyệt kế hoạch bán hàng nhân viên` — `plan_sale_employee`
- [ ] KH bán hàng phòng ban — `Duyệt kế hoạch bán hàng phòng` — `plan_sale_department`
- [ ] KH bán hàng công ty — `Duyệt kế hoạch bán hàng công ty` — `plan_sale_company`

### Khác (nhóm cuối)
- [ ] Phiếu phân công phòng phụ trách thương hiệu-hãng — `Duyệt phiếu phân công phòng phụ trách thương hiệu hãng sản xuất` — `assign-department-brand`
- [ ] Phiếu phân chia thị trường theo nhân viên — `Duyệt phiếu phân chia thị trường theo nhân viên` — `division_market_employee`
- [ ] Phiếu YC lắp đặt bàn giao — `Trưởng phòng duyệt yêu cầu lắp đặt, bàn giao` — `assemblyRequest`

## LOẠI TRỪ khỏi registry (không phải phiếu duyệt — cảnh báo/nhắc/hàng đợi)
- Tài khoản chưa phân quyền (`HE_THONG`) · Thông báo hoàn thiện hồ sơ (`DAT_HANG`) · Cảnh báo phân công NV phụ trách hãng · Hàng mượn/giữ hết hạn (`HANG_MUON_HANG_GIU`) · Hàng nhập thẳng cần xuất (`HANG_NHAP_THANG_CAN_XUAT`)

---

## Ghi chú thực thi
- Deep-link mở phiếu = `route('<prefix>.show', id)` — verify `.show` tồn tại khi gắn từng nhóm.
- Quyền nhiều giá trị = luồng nhiều cấp → `advance` đổi `required_permission` theo cấp.
- Các mục "(Xem xét)" cần chốt có phải phiếu duyệt thật không trước khi đưa vào registry.
- Trước khi bắt đầu Phase 1: tạo feature branch từ `master`, hỏi user xác nhận.

### Checkpoint — 2026-08-12
Vừa hoàn thành: Thiết kế + 2 mockup (đã chốt) + plan triển khai chi tiết (Phase 1 khung, Phase 2 template, Phase 3 inventory ~130 luồng).
Đang làm dở: (chưa code)
Bước tiếp theo: Tạo feature branch + thực thi Phase 1 Task 1 (migration `approval_inbox`).
Blocked: (để trống)

---

## PHASE 4 — Live hooks (áp pattern firm_contract cho toàn bộ luồng)

> Mục tiêu: mỗi luồng khi gửi duyệt / duyệt / từ chối / huỷ tự cập nhật registry realtime (push/advance/resolve), bọc try/catch, không phá luồng duyệt thật. Làm từng luồng + verify rồi sang luồng sau.
> Pattern chuẩn: `.superpowers/sdd/phieu-cho-duyet-tap-trung/task-p4-firmcontract-pattern.md`

### Nhóm 1 cấp (push + resolve) — làm trước cho an toàn
- [x] P4-1 project_quotation — ProjectQuotationController (Sale/) — 1 cấp "Duyệt báo giá dự án"
- [x] P4-2 inland_buy_contract — InlandBuyContractNewController (Order/) — 1 cấp "Duyệt hợp đồng mua hàng trong nước"
- [x] P4-3 bill_income — BillIncomeController (IncomeExpenditure/) — 1 cấp "Thủ quỹ duyệt phiếu thu"
- [x] P4-4 purchase_invoice — PurchaseInvoiceController (Order/) — 1 cấp "Duyệt PI mua hàng nhập khẩu"

### Nhóm nhiều cấp (push + advance + resolve)
- [x] P4-5 product_export_request — ProductExportRequestsController (Warehouse/) — 3 cấp 2→10→11
- [x] P4-6 product_import_request — ProductImportRequestsController (Warehouse/) — 2→12/10→11
- [x] P4-7 bill_payment — BillPaymentController (IncomeExpenditure/) — 2 cấp 2→5
- [x] P4-8 settlement_contract — Sale\SettlementContractsController (route settlementContract.approve) — 3 cấp 2→3(valid_approver_id)→4
- [x] P4-9 bill_payment_request — BillPaymentRequestController (IncomeExpenditure/) — 4 cấp 2→3→4→5

### Checkpoint — 2026-08-13
Vừa hoàn thành: Phase 3 backfill-display 10/10 luồng có data (P3-1..P3-7) + e2e Playwright từng luồng PASS. TOTAL registry=427.
Đang làm dở: Bắt đầu Phase 4 live hooks (P4-1 project_quotation).
Bước tiếp theo: Wire hook push+resolve vào ProjectQuotationController theo pattern firm_contract.
Blocked: (để trống)

## Bổ sung — Phân trang màn tập trung (2026-08-13)
- [x] Thêm phân trang server-side (start/length) cho `resources/views/approval_inbox/index.blade.php` — trước đây hardcode length=200 → loại >200 phiếu (Quyết toán HĐ 265) bị cắt. Nay: page-size 20/50/100/200 (mặc định 50), dãy số trang gọn (1…p-1 p p+1…N), STT liên tục, footInfo "Hiển thị x–y / N phiếu", đổi bộ lọc tự về trang 1. Dùng recordsFiltered từ Yajra. E2E PASS (265 hiển thị đủ, chuyển trang, đổi size).

## Bổ sung — Siết bộ lọc theo scope quyền (2026-08-13)
- [x] Thêm `permission_scopes` vào `config/approval_inbox.php` (6 quyền "Trưởng phòng"=department; còn lại mặc định company; part khai sẵn cơ chế, chưa dùng). Khảo sát scope từng quyền từ gate thật (HomeController@approveList + canManagerApprove) — bảng ở `.superpowers/.../permission-scope-survey.md`.
- [x] Sửa `ApprovalInbox::pendingBuilderForUser` phân nhánh company/department/part: department→department_id ∈ phòng user QUẢN LÝ (employee_manage_departments), part→part_id ∈ employee_manage_parts. Giữ nhánh approver_id đích danh. Super Admin bypass (coi tất cả=company). Commit 9a10593.
- [x] Verify tinker data thật: Super Admin=377 (giữ nguyên); TP Bùi Duy Trước (quản lý phòng 85) CŨ 6→MỚI 0 (6 phiếu phòng khác bị ẩn đúng); manager phòng 47 THẤY đúng phiếu HĐ phòng 47. Siết đúng 2 chiều.

## Bổ sung — Cột "Thời gian gửi" (ngày - giờ) thay "Ngày lập" (2026-08-14)
- [x] Migration ALTER approval_inbox.document_date: DATE → DATETIME (giữ giờ thật của created_at nguồn)
- [x] Re-backfill full để document_date lấy full datetime created_at nguồn (trước bị cắt giờ do cột DATE)
- [x] Controller editColumn('document_date'): format 'd/m/Y' → 'd/m/Y H:i'
- [x] Blade: đổi header "Ngày lập" → "Thời gian gửi"
- [x] Verify tinker (document_date có giờ) + Playwright (cột hiện ngày-giờ)

## Bổ sung — submitted_at cố định cho KPI (2026-08-14)
- [x] Migration cột `submitted_at` DATETIME (approval_inbox)
- [x] push() set submitted_at CỐ ĐỊNH (chỉ khi tạo mới/tái kích hoạt/null; advance/re-push KHÔNG đổi). Live hook không truyền → now() (thời điểm gửi thật); backfill truyền created_at nguồn (lịch sử)
- [x] Backfill: thêm submitted_at = $c->created_at (10 khối)
- [x] Controller + Blade: cột "Thời gian gửi" + filter from/to dùng submitted_at (thay document_date)
- [x] Fallback: row đã resolve (không được re-backfill) set submitted_at = COALESCE(document_date, created_at)
- [x] Verify tinker (push mới=now, advance/re-push giữ nguyên, null=0) + Playwright (cột hiện ngày-giờ). document_date giữ làm "ngày lập/chứng từ" nội bộ.
- Ghi chú KPI: TG duyệt từng cấp = logs (level_started_at→ended_at, live=thật); TG duyệt TỔNG = submitted_at→resolved_at.

---

## PHASE 5 — Mở rộng 39 loại phiếu có data (backfill-display trước, hook sau)
> Nguồn: `.superpowers/sdd/phieu-cho-duyet-tap-trung/missing-flows-survey.md`. User chốt: làm TẤT CẢ 39 luồng nhóm A. Mỗi luồng: điều tra gate thật (status→quyền→scope→route→bảng→partner) → config entry → backfill branch. Nền config-driven. Verify Playwright mỗi batch.

### Batch 1 — Đặt/mua hàng (DAT_HANG / DAT_MUA_HANG_*)
- [x] RootOrderRequest (YC đặt hàng, 160, 2 cấp) · InlandOrderRequest (YCĐH ngoài, 11, 2 cấp) · InlandOrderSummaryNew (PO trong nước, 10) · InlandPurchaseInvoice (PI trong nước, 20) ✓commit 464a258
### Batch 2 — Mua hàng/giá (DAT_MUA_HANG_* / KE_TOAN_MUA_HANG)
- [x] PriceAskingRequest (hỏi giá PTKD+XNK, 37, 2 cấp) · PriceCalculateRequest (tính giá, 4) · OrderImportRequest (chi phí NK, 3) · BuyContract2 (HĐĐH nhập khẩu, 4) · InlandBuyContract (HĐĐH ngoài, 4) · DeliveryCostAskingRequest (hỏi giá vận chuyển, 1)
### Batch 3 — Kho (KE_TOAN_KHO / XUAT_NHAP_HANG)
- [x] WarehouseExport (xuất kho, 119) · WarehouseExportRequest (ĐN xuất kho, 112) · WarehouseImport (nhập kho, 27) · WarehouseImportRequest (ĐN nhập kho, 31) · ProductTransferRequest (chuyển hàng, 25) · JoinExportRequest (xuất ghép, 2) · ProductImportDirectTransfer (điều chuyển nhập thẳng, 1) · ExcShortageWarehouseImport (báo thừa thiếu, 3)
### Batch 4 — Hàng giữ/mượn (HANG_MUON_HANG_GIU)
- [x] ProductPrepickRequest (YC xuất giữ, 8, 3 cấp) · WarehousePrepickRequest (xuất giữ BKS, 6) · PrepickTransfer2 (điều chuyển giữ, 3) · BorrowExtendRequest (gia hạn mượn, 4) · BorrowSellRequest (xuất bán mượn, 2) · PrepickExtendRequest (gia hạn giữ, 2)
### Batch 5 — Thu chi/kế toán (DE_NGHI_THU_CHI / HACH_QUYET_TOAN)
- [x] AdditionAccountingRequest (hạch toán bổ sung, 42) · BillAdjustDeptRequest (điều chỉnh công nợ, 21) · ServiceAccountingRequest (hạch toán DV, 16) · WrAccountingServiceRequest (hạch toán DV kho, 6) · BillIncomeRequest (đề nghị thu, 3) · BuyServiceAccountingRequest (hạch toán mua DV, 2)
### Batch 6 — Bảo hành/vận chuyển/kế hoạch (BAO_HANH_SUA_CHUA / VAN_CHUYEN / khác)
- [x] WrImportResult (nhập kết quả giao việc, 198 — VERIFY ký duyệt thật) · FirmWarrantyRequest (YC hãng BH, 13) · FirmWarranty (thư hãng BH, 7) · WrServiceContract (HĐ dịch vụ sửa chữa, 1) · SummaryShippingPrice (VC quốc tế, 8, 2 cấp) · OtherDeliveryTrip (chuyến xe khác, 1) · AssignDepartmentBallot (phân công hãng, 6) · SalesEmployeePlan (KH bán hàng NV, 1) · AssemblyRequest (lắp đặt bàn giao, 1)

> Nhóm B (30 luồng pending=0) — thêm sau khi phát sinh data.

### Checkpoint — 2026-08-14
Vừa hoàn thành: Phase 4 (10/10 live hook) + phân trang màn + siết scope quyền (16 quyền department, config permission_scopes) + cột "Thời gian gửi"/submitted_at cố định cho KPI + Phase 5 (39/39 loại backfill-display, 9 batch). Registry: 49 loại config, 1344 phiếu. Màn Super Admin: 49 loại / 21 nhóm / 934 phiếu (company 1).
Đang làm dở: (không) — dừng ở mốc hoàn tất Phase 5 backfill-display.
Bước tiếp theo: Live hook cho 39 loại P5 (push/advance/resolve như Phase 4) — đợt riêng. + Nhóm B 30 luồng pending=0 khi phát sinh data. + (tùy chọn) report KPI dùng submitted_at→resolved_at (để bên báo cáo).
Blocked: (để trống)
Commits chính: Phase4 6d18e07..438e91d · phân trang c30648f · scope 9a10593/a2516c3/3bd1185 · submitted_at af0f982/f85e922 · Phase5 464a258..183eddf.

### Checkpoint — 2026-08-16
Vừa hoàn thành: (không có việc mới) — xác nhận trạng thái sau wrap up 2026-08-14. Working tree sạch, mọi thay đổi đã commit tới 183eddf (P5 batch9). Registry 49 loại config / 1344 phiếu.
Đang làm dở: (không)
Bước tiếp theo: (đợt sau) Live hook 39 loại Phase 5 + backfill định kỳ; report KPI (submitted_at→resolved_at); nhóm B 30 luồng pending=0; fix concern (dd($e) BillPaymentRequestController, gate thủ kho over-inclusive).
Blocked: (để trống)

## Bổ sung — Giới hạn danh mục lọc theo phạm vi user (2026-08-17)
- [x] index(): danh mục Công ty/Phòng ban/Bộ phận suy từ distinct company_id/department_id/part_id của pendingBuilderForUser (khớp per-permission: company-scope→toàn cty có phiếu, department-scope→phòng quản lý). Không special-case Super Admin.
- [x] employeeOptions(): giới hạn "Người yêu cầu" theo cùng tập org scope (không chọn filter → chỉ NV trong phạm vi user, không phải all).
- [x] Verify tinker (user department-scope thấy ít phòng, user company-scope thấy nhiều) + Playwright.

## Bổ sung — Bỏ lọc Công ty + phòng ban subtext + xuất Excel (2026-08-17)
- [x] Bỏ dropdown "Công ty" khỏi bộ lọc (chỉ 1 cty của user). Phòng ban hiện thẳng danh mục scoped, bỏ cascade theo công ty. Part vẫn cascade theo phòng.
- [x] Cột "Người yêu cầu": thêm tên phòng ban dạng subtext dưới tên NV (searchData trả department_name).
- [x] Nút "Xuất Excel" theo bộ lọc hiện tại (route + ExcelExport class + FE build query giống searchData).
- [x] Verify Playwright.

## Bổ sung — UX bộ lọc + bảng (2026-08-17)
- [x] Đưa Phòng ban → Bộ phận → Người yêu cầu lên đầu bộ lọc
- [x] Đổi tên cột + filter "Cấp duyệt" → "Quyền áp dụng" (blade + Excel heading)
- [x] Bảng: không wrap dữ liệu (nowrap mọi cột) + scroll ngang (tablewrap overflow-x)
- [x] Toàn bộ select bộ lọc (Loại/Quyền/Phòng/Bộ phận) → select2 search
- [x] Verify Playwright

## Bổ sung — Full width + count trong select + fix select2 + truncate đối tác (2026-08-17)
- [x] Bỏ sidebar "Lọc theo nhóm" → nội dung 100% width (bỏ grid 250px)
- [x] Đưa số phiếu vào từng option select Loại phiếu (typeCounts từ builder) + "Tất cả loại (N)"
- [x] Fix select2 mở dropdown vỡ layout (dropdownParent vào vùng ng-non-bindable, bỏ dropdownAutoWidth)
- [x] Cột Đối tác: max-width + ellipsis (…) + title full text
- [x] Verify Playwright

## Bổ sung — bỏ filter Quyền áp dụng (2026-08-17)
- [x] Bỏ dropdown filter "Quyền áp dụng" (f-level) + fillCapDuyet + vars perms không dùng. Giữ nguyên CỘT "Quyền áp dụng" trong bảng. Verify Playwright.

## Bổ sung — comment menu "Chờ duyệt" cũ (2026-08-17)
- [x] Comment (Blade {{-- --}}) block menu mega "Chờ duyệt" cũ (topmenubar.blade.php ~2077-2432). Giữ menu "Phiếu chờ duyệt" tập trung. Verify Playwright: menu cũ mất, menu mới còn.
- [ ] (Ghi nhận ngoài scope) report.blade.php:307 còn alert() placeholder cho deep-link Mã phiếu — cần thay bằng link thật khi làm màn báo cáo.

### Checkpoint — 2026-08-17 (loạt UX màn danh sách)
Vừa hoàn thành (đã commit tới b9c1919): giới hạn danh mục lọc theo phạm vi user (1b865bb) · bỏ lọc Công ty + phòng ban subtext + xuất Excel (d758f5e) · sắp filter Phòng/BP/Người YC lên đầu + đổi "Cấp duyệt"→"Quyền áp dụng" + nowrap+scroll ngang + select2 search (2fe2a64) · bỏ sidebar full-width + count trong select loại + fix select2 vỡ layout + truncate đối tác (929484f) · nới select Quyền áp dụng chống wrap (bd08187) · bỏ filter Quyền áp dụng (92accd6) · comment menu "Chờ duyệt" cũ (b9c1919).
Đang làm dở: (không) — user đã commit, dừng để test.
Bước tiếp theo: User test màn danh sách. Sau khi test xong → làm màn Báo cáo phê duyệt (report.blade.php: thay alert() placeholder dòng 307 bằng deep-link thật; wire reportData KPI submitted_at→resolved_at + logs). Xa hơn: live hook 39 loại P5; nhóm B 30 luồng pending=0.
Blocked: (để trống)

## Bổ sung — Testcase Excel màn danh sách (2026-08-17)
- [x] Tạo `.plans/phieu-cho-duyet-tap-trung/testcase.xlsx` (53 TC, P0=47%, 9 section: Phân quyền + I..VIII) + generator `generate-testcase.py`. Đủ 4 khối chuẩn (9 mục mô tả / TEST SUMMARY / header 15 cột / TC-ROLE+La mã), dropdown Passed/Failed/Pending/Not Executed. Phạm vi: MÀN DANH SÁCH (báo cáo phê duyệt để test sau).

### Checkpoint — 2026-08-17 (testcase)
Vừa hoàn thành: Tạo testcase.xlsx (53 TC, P0 47%) cho màn danh sách để đưa tester. Nhánh phieu-cho-duyet-tap-trung ĐÃ MERGE vào develop_01 (commit merge 6134e90). Working tree sạch.
Đang làm dở: (không).
Bước tiếp theo: (1) Tester test màn danh sách theo testcase.xlsx → mình fix bug nếu có. (2) Sau đó: màn Báo cáo phê duyệt (report.blade.php:307 alert placeholder → deep-link thật; wire reportData KPI submitted_at→resolved_at + logs) + testcase cho báo cáo. (3) Xa hơn: live hook 39 loại P5; nhóm B 30 luồng pending=0.
Blocked: (để trống)

---

## PHASE — Hoàn thiện màn Báo cáo phê duyệt (2026-08-18)

**Nhánh:** `approvals-report` (checkout mới từ `develop_01`).
**Bối cảnh:** màn báo cáo đã dựng gần đủ ở đợt trước (route `report`/`reportData`, controller `report()`+`reportData()`, blade port đầy đủ mockup KPI/chart/bảng). Đợt này chỉ **hoàn thiện phần còn thiếu** — KHÔNG dựng lại.
**Quyết định đã chốt (user 2026-08-18):**
- KPI "TG duyệt TB" → **GIỮ tính theo từng cấp** (logs `started_at→ended_at`). KHÔNG đổi công thức, KHÔNG thêm chỉ số full-cycle.
- Deep-link mã phiếu → mở **tab mới (`target="_blank"`)**.
- Scope đợt này: R1 deep-link thật · R2 xuất Excel báo cáo · R3 testcase Excel báo cáo · R4 verify Playwright.

**Files chạm tới:**
- Modify: `app/Http/Controllers/ApprovalInbox/ApprovalInboxController.php`
- Modify: `resources/views/approval_inbox/report.blade.php`
- Create: `app/ExcelExports/ApprovalReportExport.php`
- Modify: `routes/web.php`
- Create: `.plans/phieu-cho-duyet-tap-trung/testcase-report.xlsx` (+ generator)

### Task R1 — Deep-link thật ở bảng chi tiết (thay alert) — ✅ CODE XONG
- [x] **BE**: `reportData()` map `$detail` thêm field `'url'` = `route($r->approve_route, $r->source_id)` bọc try/catch (mirror `searchData`: lỗi/route rỗng → `''`). Bỏ field `route` (thay bằng `url`).
- [x] **FE** `report.blade.php`: `renderDetail` — `codeCell` → `<a class="lnk" href="{url}" target="_blank" rel="noopener">{code} ↗</a>` khi có `url`; không có → text thường. Đã xóa hàm `arGoView` alert.
- [x] `php -l` controller sạch.
- [ ] **Verify browser** (gộp vào R4): click mã phiếu → mở đúng phiếu ở tab mới.

### Task R2 — Xuất Excel báo cáo — ✅ CODE XONG
- [x] **Refactor BE**: tách `reportRows(Request)` (query logs join inbox + filter) dùng chung reportData + reportExport; thêm helper `reportDurationHours($r)` (TG theo cấp).
- [x] **Create** `app/ExcelExports/ApprovalReportExport.php` (mirror `ApprovalInboxExcel`, 11 cột A–K): STT · Loại phiếu · Mã phiếu · Người yêu cầu · Người duyệt · Quyền áp dụng · Ngày gửi · Ngày duyệt · TG duyệt (giờ) · Kết quả · Lý do từ chối. Kết quả map `approve`→"Đã duyệt", `reject`→"Từ chối".
- [x] **BE method** `reportExport(Request)`: `reportRows()` → sort `ended_at` desc (KHÔNG cắt 100) → map → `Excel::download(new ApprovalReportExport($data), 'bao-cao-phe-duyet-YmdHis.xlsx')`.
- [x] **Route** `approvalInbox.reportExport` (GET /report-export) + `checkPermission:Xem báo cáo phê duyệt` — verify `route:list` OK.
- [x] **FE**: `AR_EXPORT_URL` → `route('approvalInbox.reportExport')`; nút Excel build query `buildQuery(currentFilter())` → `window.open(url+?qs)`.
- [x] `php -l` sạch cả controller + Excel class.
- [ ] **Verify browser** (gộp vào R4): bấm Xuất Excel → tải file, đủ cột + Lý do từ chối ở dòng Từ chối; số dòng khớp filter.

### Task R3 — Testcase Excel báo cáo — ✅ XONG
- [x] Sinh `testcase-report.xlsx` (**50 TC, P0=50%**) + generator `generate-testcase-report.py`. File RIÊNG, không đụng `testcase.xlsx` màn danh sách.
- [x] Đủ 4 khối chuẩn: 9 mục mô tả / TEST SUMMARY (5 COUNTIF) / header 15 cột / TC section (TC-ROLE + I..VIII La mã) + dropdown Passed/Failed/Pending/Not Executed.
- [x] Cover: phân quyền "Xem báo cáo phê duyệt" (có/không quyền → 403 cả 3 route report/reportData/reportExport), bộ lọc (kỳ/cascade Cty→Phòng→BP/người duyệt/loại/kết quả), 7 KPI, 2 biểu đồ, bảng người duyệt ẩn khi lọc 1 người, deep-link tab mới, xuất Excel (11 cột + Lý do từ chối, toàn bộ không cắt 100, khớp màn hình), edge case (data rỗng, kỳ custom trống, phiếu nhiều vòng/nhiều cấp, lý do rỗng), cô lập dữ liệu org.

### Task R4 — Verify Playwright — ✅ XONG (localhost:8001, DNS Admin)
- [x] Màn `/admin/approval-inbox/report` load OK, đăng nhập sẵn (2 console error chỉ là ảnh 404 logo/avatar, không liên quan).
- [x] KPI/biểu đồ/bảng đổ **data thật**: total=19, approved=18 (95%), rejected=1, pending=1343, avg=0.5h, ontime=100%; chi tiết 19 dòng, người duyệt 2, biểu đồ 1 cột tuần + 7 nhóm.
- [x] **R1 deep-link**: mã phiếu `TPE.DNTT0526.00298` → `href=/admin/income-expenditure/bill_payment_requests/3527/show`, `target="_blank"` ✅
- [x] **Filter Kết quả=Từ chối**: total=1, hiện badge Từ chối + lý do "⤷ test reject" ✅
- [x] **Lọc 1 người duyệt (DNS Admin)**: ẩn bảng "Hiệu suất theo người duyệt" + hiện infobar đúng text ✅
- [x] **R2 Excel**: `GET /report-export` → 200, `Content-Type` xlsx, `Content-Disposition: attachment; filename=bao-cao-phe-duyet-*.xlsx`, 8227 bytes, header PK hợp lệ ✅
- Ghi chú: `overdue=1343` = `pending` do bản ghi backfill có `level_started_at` = ngày tạo cũ (>3 ngày) — đúng dữ liệu, không phải bug code. Cascade Cty→Phòng→BP + đổi kỳ là JS thuần cùng pattern màn danh sách (đã verify trước), không chặn.

### Checkpoint — 2026-08-18 (hoàn thành phase báo cáo)
Vừa hoàn thành: R1 (deep-link thật) + R2 (Excel export) + R3 (testcase-report.xlsx 50 TC) + R4 (verify Playwright localhost:8001 — deep-link/Excel/filter Từ chối/ẩn bảng 1 người đều đạt). `php -l` sạch, route đăng ký đúng middleware.
Đang làm dở: (không) — code hoàn thiện, **CHƯA commit**.
Bước tiếp theo: user review + commit nhánh `approvals-report` → PR về `develop_01`. Xa hơn (ngoài phase này): live hook 39 loại P5; nhóm B 30 luồng pending=0.
Blocked: (để trống)

### Checkpoint — 2026-08-20 (wrap up session)
Vừa hoàn thành: đóng session — không có thay đổi code mới so với checkpoint 2026-08-18 (yêu cầu "nút reset bộ lọc" đã huỷ vì user nhầm dự án khác, KHÔNG đụng file nào cho việc đó).
Đang làm dở: (không).
Trạng thái phase Báo cáo phê duyệt: **XONG code R1–R4, CHƯA commit** trên nhánh `approvals-report` (checkout từ develop_01). 5 file: Controller (M), report.blade.php (M), ApprovalReportExport.php (mới), web.php (M), testcase-report.xlsx + generator (mới).
Bước tiếp theo: user review + commit `approvals-report` → PR về `develop_01`.
Blocked: (để trống)

---

## PHASE — Fix registry kẹt "chờ duyệt" khi nguồn đã rời trạng thái chờ duyệt (2026-08-20)

**Nhánh:** `approvals-report` (làm luôn trên nhánh hiện tại, user chốt — không đổi nhánh, không commit).
**Triệu chứng (user báo):** Phiếu yêu cầu xuất hàng (PYCXH) sau khi Phiếu xuất hàng con duyệt → `status` gốc = DA_HACH_TOAN(5). Màn **danh sách PYCXH** hiển thị đúng "Đã hạch toán" (đọc cột `status`). Nhưng màn **Tổng hợp chờ duyệt** vẫn hiện "chờ duyệt Kế toán kho".

**Root cause (đã verify code):**
- Màn tổng hợp đọc `approval_inbox`, KHÔNG đọc `status` gốc.
- `push()` tạo dòng registry cấp "Kế toán kho" khi PYCXH ở CHO_DUYET (`ProductExportRequestsController@store:928`).
- Khi PYCXH **rời** nhóm chờ duyệt {CHO_DUYET, DOI_TP_DUYET, DOI_BGD_DUYET} sang trạng thái xử lý tiếp (DANG_LAP_DE_NGHI... → DA_HACH_TOAN), việc chuyển status nằm ở **controller phía sau** (`WarehouseExportRequestsController:528`, `WarehouseExport`, `ProductExport`) — những chỗ này KHÔNG gọi `resolve()`. Live-hook PYCXH chỉ cover: gửi duyệt (push), TP/BGĐ duyệt vượt hạn mức (advance/resolve), từ chối (resolve rejected). **Thiếu nhánh "rời chờ duyệt đi tiếp".**
- Backfill định nghĩa pending = status ∈ {CHO_DUYET, DOI_TP_DUYET, DOI_BGD_DUYET} (BackfillApprovalInbox:205-207). Nhưng backfill **chỉ push, KHÔNG resolve dòng stale** → chạy lại backfill KHÔNG dọn được data đã kẹt.
- `cancel()` (status→DA_HUY_PHIEU=6) cũng CHƯA có hook resolve → phiếu huỷ cũng kẹt pending.

**Hướng fix (user chốt):** (1) Fix code tập trung ở Model; (2) Dọn data stale toàn bộ doc_type.

### Task F1 — Model-event resolve khi PYCXH rời nhóm chờ duyệt — ✅ CODE XONG
- [x] Thêm `self::updated()` trong `ProductExportRequest::boot()` (cạnh hook `created` sẵn có).
- [x] Điều kiện: `wasChanged('status')` && old ∈ {CHO_DUYET, DOI_TP_DUYET, DOI_BGD_DUYET} && new ∉ tập đó.
- [x] Bỏ qua `new == DANG_TAO` (từ chối/về nháp — đã có hook `deny()` resolve 'rejected', tránh double).
- [x] `new == DA_HUY_PHIEU` → `resolve('canceled')`; còn lại (đi tiếp) → `resolve('approved')`.
- [x] Guard idempotent: chỉ resolve khi CÒN dòng `ApprovalInbox` PENDING (vì `resolve()` không tự idempotent → tránh log trùng).
- [x] Bọc try/catch + `optional(Auth::user())->id` (an toàn khi chạy console/tinker). `php -l` sạch.

### Task F2 — Reconcile dọn data stale toàn bộ doc_type — ✅ CODE XONG (user chạy còn lại)
- [x] Thêm option `--prune` vào `approval-inbox:backfill`: recorder (anon subclass ApprovalInboxService override `push()`) ghi lại mọi key `(source_table#source_id)` thực sự pending khi enumerate.
- [x] Sau khi chạy hết các block, `pruneStale()`: mọi dòng `ApprovalInbox` PENDING KHÔNG nằm trong tập vừa enumerate → `resolve('canceled', null, 'auto-reconcile: nguồn không còn chờ duyệt')`. Gom `$stale` trước rồi resolve (tránh mutate khi chunk theo status).
- [x] Chạy `--prune` không kèm group → prune toàn bộ; kèm group → chỉ prune `group_code` đó (tránh resolve nhầm group chưa enumerate).
- [x] Dùng 'canceled' (trung tính) để KHÔNG bịa số "đã duyệt" trong báo cáo cho data lịch sử không rõ kết cục. `php -l` sạch.
- [ ] **User chạy** (không phải Claude — tránh chạy nhầm DB prod do config cache): `php artisan config:clear` trước, rồi `php artisan approval-inbox:backfill --prune` trên DB local đúng.

### Task F3 — Verify — 🔶 php -l xong, chờ user verify runtime
- [x] `php -l` cả Model + Command — sạch (cảnh báo imagick.so là nhiễu môi trường).
- [ ] User verify: 1 PYCXH đã DA_HACH_TOAN không còn ở màn tổng hợp; PYCXH mới rời CHO_DUYET → biến mất khỏi inbox ngay (live).

### Task F4 — Rà soát luồng tương tự + fix gap cùng loại — ✅ CODE XONG
Rà toàn bộ 49 doc_type (agent audit + verify tay). Kết quả:
- **10 loại có live-hook**: 7 loại OK (firm_contract, project_quotation, settlement_contract, inland_buy_contract, purchase_invoice, bill_income, bill_payment — self-contained, status không bị downstream đẩy).
- **`product_import_request`** — **GAP y hệt PYCXH** (đã verify: `boot()` không hook; downstream `WarehouseImportRequest:454/594`, `WarehouseImport:1565/1622`, `ProductImport:1600` đẩy status 1/4/5/8/9 không resolve). **→ FIX**: thêm `self::updated()` vào `ProductImportRequest::boot()`, resolve khi rời {CHO_DUYET=2, CHO_BAN_KIEM_SOAT_DUYET=10, CHO_BGD_DUYET=11, CHO_TP_DUYET=12}, bỏ qua DANG_TAO(3), DA_HUY_PHIEU→canceled. `php -l` sạch.
- **`bill_payment_request`** — **GAP cancel-exit** (đã verify `changeStatus:566-609`: resolve chỉ bắt STATUS_REJECT; đường "không duyệt" set STATUS_CANCEL(9)/reset CREATING(1) không resolve → kẹt pending). **→ FIX** surgical: thêm nhánh `elseif ($request->status == STATUS_CANCEL)` → `resolve('canceled')`. `php -l` sạch.
- [x] Fix `ProductImportRequest.php` (model-event).
- [x] Fix `BillPaymentRequestController.php@changeStatus` (cancel-exit).

### Task F5 — 39 loại Phase 5 (chỉ backfill-display, không live-hook) — 🔶 KHUYẾN NGHỊ, chưa làm
- Không có chốt live nào → luôn dựa backfill/prune. Rủi ro forward-exit rõ nhất: borrow_sell_request, warehouse_export_request, warehouse_import_request, product_transfer_request, join_export_request, product_prepick_request/prepick_*.
- [x] **ĐÃ SETUP cron** (user chốt): `app/Console/Kernel.php` thêm `$schedule->command('approval-inbox:backfill --prune')->everyThirtyMinutes()->withoutOverlapping()->runInBackground()->emailOutputOnFailure(...)`. `php -l` sạch. LƯU Ý: chỉ chạy trên server có cron `* * * * * php artisan schedule:run` cho TanPhatDev (production); crontab local chỉ có schedule:run cho zkapp. Tần suất 30' chỉnh được ở Kernel.php.

### Task F6 — Check 2 luồng user chỉ định (lắp đặt bàn giao + giao việc khác) — ✅ XONG
- **`assembly_request` (YC lắp đặt bàn giao)** — có forward-exit gap (pending=CHO_TP_DUYET=6, chỉ backfill-display, chưa có push/resolve; approve→CHO_GIAO_VIEC, unApprove→TU_CHOI đều không resolve). **→ FIX** thêm live-hook controller-based (khớp pattern 10 loại live):
  - [x] Helper `approvalInboxEntry()` (mirror backfill payload, submitted_at=now).
  - [x] push khi vào CHO_TP_DUYET ở `store()` + `update()`.
  - [x] resolve('approved') ở `approve()` (→CHO_GIAO_VIEC); resolve('rejected') ở `unApprove()` (→TU_CHOI).
  - [x] `php -l` sạch (dùng `\Log` FQ nên không cần import).
- **`assign_other_request` (YC giao việc khác)** — **KHÔNG phải luồng duyệt** (đã verify: chỉ 4 status {DANG_TAO,CHO_GIAO_VIEC,DA_GIAO_VIEC,TU_CHOI}, không có CHO_TP_DUYET/canApprove; route `.approve` trỏ method KHÔNG tồn tại = route chết; không trong registry lẫn approveList cũ). Là luồng "chờ giao việc", KHÔNG đưa vào registry chờ duyệt. **→ Bỏ qua.**

### Checkpoint — 2026-08-20 (fix registry kẹt chờ duyệt + rà luồng tương tự + 2 luồng chỉ định)
Vừa hoàn thành: F1 `ProductExportRequest::updated()`; F2 `--prune`; F4 fix `ProductImportRequest` (model-event) + `BillPaymentRequestController@changeStatus` (cancel-exit); F6 fix `assembly_request` (live-hook controller push/resolve), xác nhận `assign_other_request` không phải luồng duyệt. `php -l` sạch tất cả. CHƯA commit.
Đang làm dở: (không).
Bước tiếp theo: user chạy `config:clear` + `approval-inbox:backfill --prune` dọn data kẹt; quyết F5 (cron prune định kỳ cho phần còn lại của 39 loại). Verify màn tổng hợp.
Blocked: (để trống)
File đã sửa (5): `app/Model/Warehouse/ProductExportRequest.php`, `app/Model/Warehouse/ProductImportRequest.php`, `app/Console/Commands/BackfillApprovalInbox.php`, `app/Http/Controllers/IncomeExpenditure/BillPaymentRequestController.php`, `app/Http/Controllers/Customercare/AssemblyRequestController.php`.

### Task F7 — Live-hook 36 loại backfill-display còn lại (workflow 8 batch) — 🔶 PHẦN LỚN XONG
Cơ chế: hook tay từng controller (user chốt) qua multi-agent workflow (8 batch theo module, mỗi loại sở hữu Controller+Model riêng, chuẩn vàng = block backfill).
- [x] **31 loại HOOKED** (php -l sạch toàn bộ, KHÔNG đụng file downstream cấm — đã verify tay): warehouse_export_request, join_export_request, warehouse_import, warehouse_import_request, order_import_request, exc_shortage_warehouse_import, product_import_direct_transfer, product_transfer_request, product_prepick_request, warehouse_prepick_request, prepick_transfer2, prepick_extend_request, borrow_extend_request, borrow_sell_request, root_order_request, inland_order_request, inland_order_summary_new, inland_purchase_invoice, price_asking_request, price_calculate_request, delivery_cost_asking_request, service_accounting_request, wr_accounting_service_request, buy_service_accounting_request, addition_accounting_request, wr_import_result, firm_warranty_request, firm_warranty, wr_service_contract, assign_department_ballot, sales_employee_plan. (~45 file: controller push/resolve + 19 model-event self::updated cho loại bị downstream đẩy).
- [ ] **3 loại UNCERTAIN** (agent chủ ý KHÔNG làm nửa vời — exit approve/cancel nằm ở file downstream dùng chung + dùng query `->update()` bypass model-event → cần sửa file dùng chung mới đủ resolve, nếu chỉ push+reject sẽ để phiếu đã duyệt kẹt pending):
  - `warehouse_export`: approve 2→7 ở `ProductExportsController@store:805` (`$parent->approve()`); cần model-event trong `WarehouseExport.php` hoặc resolve tại đó. Push=`WarehouseExportsController` khi 3→2; reject=deny@1456.
  - `bill_adjust_dept_request`: approve `BillAdjustDeptController:231/315` + `BillAdjustDept.php:565` (query update), cancel `:328`; reject hookable `BillAdjustDeptRequestController:517`; push ready store:190/update:242.
  - `bill_income_request`: approve `BillIncomeController:251`+`BillIncome.php:509`, cancel `:272`; reject hookable `BillIncomeRequestController:307`; push ready store:153/update:196.
- [ ] **4 loại CHƯA LÀM** — batch BUY-SHIP bị safety-classifier chặn nhầm (do 2 lần user click nhầm reject trước đó): buy_contract2, inland_buy_contract_old, summary_shipping_price, other_delivery_trip.

### Task F8 — Hoàn tất 7 loại còn lại (3 uncertain + 4 BUY-SHIP) — ✅ XONG
- [x] `warehouse_export` (tự làm): model-event `self::saved()` trong `WarehouseExport.php` — push khi vào DANG_LAY(2), resolve khi rời (7→approved, 4→rejected, 8→canceled), guard PENDING.
- [x] `bill_adjust_dept_request` (agent): push+reject ở `BillAdjustDeptRequestController`; resolve approved/canceled sau query-update ở `BillAdjustDeptController` (guard hasPending).
- [x] `bill_income_request` (agent): push+reject ở `BillIncomeRequestController`; resolve approved sau query-update ở `BillIncomeController`+`BillIncome.php`, canceled ở `BillIncomeController` (guard).
- [x] `buy_contract2`, `inland_buy_contract_old` (agent): push khi status==2, resolve approved/rejected trong approve().
- [x] `summary_shipping_price` (agent, 2 cấp): push TP → re-push BKS (company_id=null, KHÔNG dùng advance vì service không set null được) → resolve. **Đánh đổi: mất log advance từng cấp cho loại này** (inbox vẫn đúng).
- [x] `other_delivery_trip` (agent): push submitApprove; model-event resolve trong `OtherDeliveryTrip.php`.
- [x] **Verify tay: 64 file .php thay đổi, php -l 0 lỗi. Không xung đột helper (2 helper ở DeliveryInternational là cố ý 2 cấp).**

**Edge case — ĐÃ XỬ (user chốt):**
- [x] `BillAdjustDeptController::delete()`: xóa phiếu kế toán → revert request về AWAITING_APPROVE → **đã thêm re-push** (push idempotent tái kích hoạt dòng resolved về PENDING). `php -l` sạch. (bill_income delete là hard-delete → không cần.)
- [x] `summary_shipping_price` re-push thay advance (mất log advance từng cấp): user OK.

### Checkpoint — 2026-08-20 (HOÀN TẤT live-hook toàn bộ 47 doc_type)
Vừa hoàn thành: live-hook 38 loại backfill-display còn lại (workflow 31 + BUY-SHIP 4 + warehouse_export/bill_adjust/bill_income 3) → toàn bộ 47 doc_type registry giờ có live push/resolve. 64 file .php thay đổi, php -l 0 lỗi (verify tay bằng git).
Đang làm dở: (không) — CHƯA commit.
Bước tiếp theo: (1) user quyết edge-case delete() re-push; (2) user chạy `config:clear`+`approval-inbox:backfill --prune` dọn data + verify màn tổng hợp; (3) review + commit.
Blocked: (để trống)

### Checkpoint — 2026-08-21 (wrap up — deploy dev + verify đang chờ)
Vừa hoàn thành:
- Toàn bộ 47 doc_type registry đã có live-hook (F1–F8). Edge-case delete() re-push xong. Cron `approval-inbox:backfill --prune` mỗi 30' đã đăng ký ở `app/Console/Kernel.php`.
- **ĐÃ MERGE `approvals-report` → `develop_01`** (merge commit `46ab7152e5`) và **deploy lên VPS DEV** (`/var/www/html/TanPhatDev`, APP_ENV=dev, DB=dev_128, Apache2 mod_php, OPcache `validate_timestamps=On` → tự nạp code mới; cron `schedule:run` đã có sẵn).
- Chạy `php artisan approval-inbox:backfill --prune` trên dev_128: enumerate cả 47 loại OK (framework 6.20.45 không lỗi), **Prune stale đóng 0 dòng** (registry khớp nguồn, không drift).

Đang làm dở / CHỜ USER:
- **Nghi vấn cần chốt**: user nói bug (PYCXH kẹt "chờ duyệt Kế toán kho") thấy trên CHÍNH dev này, nhưng prune đóng 0 dòng. Đã đưa lệnh tinker verify (liệt kê approval_inbox PENDING source_table=product_export_requests kèm per.status thật). CHỜ output:
  - Nếu có dòng PENDING mà src_status ∉ {2,10,11} → prune SÓT → phải sửa `pruneStale()`/`BackfillApprovalInbox`.
  - Nếu sạch → registry đã đồng bộ, reload màn kiểm chứng.
- **CHƯA rõ user đã chạy `php artisan queue:restart`** (worker `tanphat_qtt` giữ code cũ) — cần xác nhận.
- Chưa deploy PROD (env `TANPHATERP`): lặp lại `queue:restart` + `backfill --prune` trên box prod (nơi có phiếu kẹt thật nếu bug ở prod).

Bước tiếp theo: nhận output lệnh tinker verify + trả lời queue:restart → nếu prune sót thì sửa; nếu sạch thì đóng bug. Sau đó deploy prod.
Blocked: chờ user paste kết quả tinker verify.
