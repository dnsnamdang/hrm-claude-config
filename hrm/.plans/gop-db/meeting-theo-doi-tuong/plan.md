# Meeting theo đối tượng (Dự án TKT / Hợp đồng) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Loại meeting khai "Meeting theo đối tượng" (Dự án TKT / Hợp đồng) → meeting thuộc loại đó bắt buộc chọn đối tượng; bỏ checkbox "Meeting theo dự án".

**Architecture:** Thêm cột `meeting_types.target_type` + `meetings.contract_id`. Danh sách đối tượng chọn được khai 1 lần trên Entity (scope `selectableForMeeting`) và dùng chung cho endpoint chọn + validate. Validate đối tượng gom vào 1 trait dùng cho cả request tạo và sửa, chạy trong `after()` để lỗi hiện đồng thời với lỗi rule thường. FE thay checkbox bằng điều kiện tính từ loại meeting đang chọn.

**Tech Stack:** PHP 7.4 / Laravel 8 (`nwidart/laravel-modules`), PHPUnit chạy trên DB local thật (khuôn `tests/Feature/MeetingByProjects`), Nuxt 2 / Vue 2 (V2Base*), Playwright.

**Spec:** `.plans/gop-db/meeting-theo-doi-tuong/design.md`

## Global Constraints

- **Chưa được phép code.** Trước Task 1 phải hỏi user riêng, nêu phạm vi: repo `hrm-api` + `hrm-client` · nhánh `gop_db` · file ở bảng File Map · 2 migration · có chạy `migrate` vào DB local `local_hrm_erp` không. Chờ câu "làm".
- **Không commit / push** (HRM CLAUDE.md). Mỗi task kết thúc bằng bước "báo user", không có bước commit.
- Không `git stash`; kill server theo PID cổng, không `pkill` (memory).
- PHP: `/opt/homebrew/opt/php@7.4/bin/php`. Test BE: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit <file>` trong `hrm-api/`.
- `target_type`: `1` = Dự án TKT, `2` = Hợp đồng, `NULL` = không. Nguồn tên duy nhất: `MeetingType::TARGETS`.
- Dự án TKT chọn được: `status BETWEEN 2 AND 10` (cả dự án thường và dự án cha).
- Hợp đồng chọn được: bảng `hrm_contracts`, `status NOT IN (3, 10)` (Đang tạo, Đã thanh lý). Không lọc quyền. Endpoint KHÔNG trả trường tiền.
- Câu lỗi: `Vui lòng chọn Dự án TKT.` · `Vui lòng chọn Hợp đồng.` · `Loại meeting đã có meeting, chỉ được đổi Meeting theo đối tượng.`
- Chỉ kiểm dải trạng thái với đối tượng **mới chọn thêm**; đối tượng đang lưu sẵn trên meeting được giữ dù đã ra khỏi dải.
- Không thêm `target_type` vào nhập Excel loại meeting.
- E2E: viết/sửa spec nhưng **chỉ chạy khi user yêu cầu**, chạy thì `--workers=1`. Verify FE bằng Playwright MCP, đo DOM.

## Review Focus

1. **Meeting cũ có dự án, loại meeting không phải TKT** → mở Sửa vẫn thấy ô Dự án + tab "Dự án tiền khả thi", bấm Lưu không bị bắt chọn và KHÔNG mất liên kết dự án. Test: Task 3 `test_meeting_cu_co_du_an_loai_khong_tkt_khong_bat_buoc` + Task 5 bước verify MCP (c).
2. **Hợp đồng đã chọn sau đó bị thanh lý** → sửa meeting (giữ nguyên HĐ) vẫn lưu được; ô HĐ vẫn hiện HĐ đó. Test: Task 3 `test_giu_hop_dong_cu_da_thanh_ly_van_luu_duoc` + Task 2 `test_for_meeting_include_id_tra_hop_dong_ngoai_dai`.
3. **Đổi loại meeting từ Hợp đồng sang loại khác** → `contract_id` bị xoá về NULL khi lưu, không còn treo HĐ cũ. Test: Task 3 `test_doi_loai_khoi_hop_dong_xoa_contract_id` + Task 5 verify (f).
4. **Loại meeting đang dùng, admin cố đổi Tên qua API** (bỏ qua FE) → 423, không đổi gì. Test: Task 1 `test_loai_dang_dung_doi_ten_bi_chan`.
5. **Người không có quyền xem Hợp đồng** gọi endpoint chọn HĐ → vẫn 200, nhưng body không có trường tiền. Test: Task 2 `test_for_meeting_khong_tra_truong_tien` + Task 6 spec API (5).

---

## File Map

| File | Trách nhiệm | Task |
|---|---|---|
| `hrm-api/Modules/Assign/Database/Migrations/2026_10_08_000001_add_target_type_to_meeting_types_table.php` | Tạo cột `target_type` | 1 |
| `hrm-api/Modules/Assign/Database/Migrations/2026_10_08_000002_add_contract_id_to_meetings_table.php` | Tạo cột `contract_id` + index | 1 |
| `hrm-api/Modules/Assign/Entities/MeetingType.php` | Hằng TARGET_*, fillable, `isCanEditTargetOnly()` | 1 |
| `hrm-api/Modules/Assign/Http/Requests/MeetingType/MeetingTypeRequest.php` | Rule `target_type` | 1 |
| `hrm-api/Modules/Assign/Services/MeetingTypeService.php` | Lọc, lịch sử, chế độ chỉ-đổi-đối-tượng | 1 |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingTypeController.php` | Trả 423 cho chế độ chỉ-đổi-đối-tượng | 1 |
| `hrm-api/Modules/Assign/Transformers/MeetingType/MeetingTypeResource.php` + `DetailMeetingTypeResource.php` | Trả `target_type*`, `is_can_edit_target` | 1 |
| `hrm-api/app/ExcelExport/ExportColumnRegistry.php` | Cột xuất `target_type_text` | 1 |
| `hrm-api/app/Services/CatalogHistoryService.php` | Nhãn cột lịch sử | 1 |
| `hrm-api/Modules/Assign/Entities/ProspectiveProject.php` | Scope `selectableForMeeting` | 2 |
| `hrm-api/Modules/Assign/Entities/Contract/Contract.php` | Scope `selectableForMeeting` | 2 |
| `hrm-api/Modules/Assign/Services/ProspectiveProjectService.php` | `getForMeeting` lọc dải + `include_ids` | 2 |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php` + `Routes/api.php` | Endpoint `for-meeting` | 2 |
| `hrm-api/Modules/Assign/Http/Requests/Meeting/ValidatesMeetingTarget.php` (mới) | Validate đối tượng dùng chung | 3 |
| `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php` + `MeetingUpdateApiRequest.php` | Gọi trait | 3 |
| `hrm-api/Modules/Assign/Entities/Meeting/Meeting.php` | fillable `contract_id`, quan hệ `contract()` | 3 |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` | Lưu `contract_id`, suy `has_prospective_project` | 3 |
| `hrm-api/Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php` | Trả `contract` | 3 |
| `hrm-api/Modules/Assign/Services/MeetingHistoryService.php` | Dòng lịch sử "Hợp đồng" | 3 |
| `hrm-api/tests/Feature/MeetingTarget/*` (mới) | Test BE | 1-3 |
| `hrm-client/components/modal/meeting-type-modal.vue` | Ô chọn đối tượng + chế độ chỉ-đổi-đối-tượng | 4 |
| `hrm-client/pages/assign/meeting_type/index.vue` | Cột, lọc, xuất, nút Sửa | 4 |
| `hrm-client/pages/assign/meeting/components/GeneralInfo.vue` | Bỏ checkbox, ô HĐ, điều kiện hiện ô TKT | 5 |
| `hrm-client/pages/assign/meeting/components/MeetingForm.vue` | Điều kiện tab Dự án | 5 |
| `hrm-client/pages/assign/meeting/create.vue` | Bỏ `has_prospective_project` mặc định, thêm `contract_id` | 5 |
| `e2e/tests/assign/meeting-target.api.spec.ts` + `meeting-target.spec.ts` (mới) | E2E | 6 |

---

### Task 1: BE — cấu hình đối tượng trên loại meeting

**Files:** như File Map, các dòng Task 1. Test: `hrm-api/tests/Feature/MeetingTarget/MeetingTypeTargetTest.php` + fixture `MeetingTargetFixture.php`

**Interfaces:**
- Produces: `MeetingType::TARGET_PROSPECTIVE_PROJECT = 1`, `MeetingType::TARGET_CONTRACT = 2`, `MeetingType::TARGETS = [1 => 'Dự án TKT', 2 => 'Hợp đồng']`, `MeetingType::targetName($targetType): string` (trả `''` khi null); `MeetingType::isCanEditTargetOnly(): bool`. Resource trả `target_type` (int|null), `target_type_text` (string, rỗng khi null), `is_can_edit_target` (bool). Query param lọc `target_type` ∈ `'0'|'1'|'2'` (`'0'` = NULL). Fixture `MeetingTargetFixture` với `actAsManager()`, `makeType(array)`, `makeMeetingOfType(MeetingType, array)`, mảng dọn `fxTypeIds/fxMeetingIds/fxContractIds/fxProjectIds`, `cleanupMeetingTargetFixture()`.

- [x] **Step 1: Migration** (2 file, khuôn migration có sẵn trong `Modules/Assign/Database/Migrations`)

```php
// 2026_10_08_000001_add_target_type_to_meeting_types_table.php
public function up()
{
    Schema::table('meeting_types', function (Blueprint $table) {
        // Meeting theo đối tượng: 1 = Dự án TKT, 2 = Hợp đồng, NULL = không gắn đối tượng
        $table->unsignedTinyInteger('target_type')->nullable()->after('has_customer');
    });
}
public function down()
{
    Schema::table('meeting_types', function (Blueprint $table) {
        $table->dropColumn('target_type');
    });
}
```

```php
// 2026_10_08_000002_add_contract_id_to_meetings_table.php
public function up()
{
    Schema::table('meetings', function (Blueprint $table) {
        // Hợp đồng HRM (hrm_contracts) — chỉ có khi loại meeting target_type = 2
        $table->unsignedBigInteger('contract_id')->nullable()->after('customer_id');
        $table->index('contract_id');
    });
}
public function down()
{
    Schema::table('meetings', function (Blueprint $table) {
        $table->dropIndex(['contract_id']);
        $table->dropColumn('contract_id');
    });
}
```

Chạy migrate vào DB local **chỉ khi user đã cho phép ở bước hỏi phạm vi** (config:clear trước):
`/opt/homebrew/opt/php@7.4/bin/php artisan module:migrate Assign` → kiểm `SHOW COLUMNS FROM meeting_types LIKE 'target_type'` và `SHOW COLUMNS FROM meetings LIKE 'contract_id'` đều ra 1 dòng.

- [x] **Step 2: Viết fixture + test fail**

Fixture `tests/Feature/MeetingTarget/MeetingTargetFixture.php`. Trước khi viết: mở `tests/Feature/MeetingByProjects/MeetingFixture.php` (hàm `actAs`) để dùng đúng cách đăng nhập, và `SHOW COLUMNS FROM catalog_histories` để đúng tên cột bảng/bản ghi (dưới đây giả định `table_name`/`record_id` — sửa theo tên thật).

```php
<?php

namespace Tests\Feature\MeetingTarget;

use App\Models\TpEmployee;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\MeetingType;

/** Dữ liệu test trên DB local thật — mọi bản ghi tạo ra đều dọn ở tearDown */
trait MeetingTargetFixture
{
    protected $fxTypeIds = [];
    protected $fxMeetingIds = [];
    protected $fxContractIds = [];
    protected $fxProjectIds = [];

    /** Nhân viên có quyền "Quản lý danh mục loại meeting" QUA ROLE (memory quyen-chi-doc-qua-role) */
    protected function actAsManager(): void
    {
        $user = TpEmployee::findOrFail((int) env('E2E_MANAGER_EMPLOYEE_ID', 27));
        $this->actingAs($user, 'api');
        auth('api')->setUser($user);
    }

    protected function makeType(array $attrs = []): MeetingType
    {
        $t = MeetingType::create([
            'name' => 'PHPUnit loại ' . uniqid(), 'has_customer' => true, 'status' => MeetingType::STATUS_ACTIVE,
        ]);
        if ($attrs) {
            $t->forceFill($attrs)->saveQuietly();
        }
        $this->fxTypeIds[] = $t->id;
        return $t;
    }

    /** Meeting tối thiểu, chép từ 1 meeting thật rồi đổi loại (khuôn makeMeeting của MeetingFixture) */
    protected function makeMeetingOfType(MeetingType $type, array $attrs = []): Meeting
    {
        $m = Meeting::orderByDesc('id')->firstOrFail()->replicate();
        $m->forceFill(array_merge(['code' => 'PHPUNIT-MT-' . uniqid(), 'meeting_type_id' => $type->id], $attrs));
        $m->saveQuietly();
        $this->fxMeetingIds[] = $m->id;
        return $m;
    }

    protected function cleanupMeetingTargetFixture(): void
    {
        DB::table('prospective_project_meetings')->whereIn('meeting_id', $this->fxMeetingIds)->delete();
        DB::table('meetings')->whereIn('id', $this->fxMeetingIds)->delete();
        DB::table('catalog_histories')->where('table_name', 'meeting_types')->whereIn('record_id', $this->fxTypeIds)->delete();
        DB::table('meeting_types')->whereIn('id', $this->fxTypeIds)->delete();
        DB::table('hrm_contracts')->whereIn('id', $this->fxContractIds)->delete();
        DB::table('prospective_projects')->whereIn('id', $this->fxProjectIds)->delete();
    }
}
```

Test `tests/Feature/MeetingTarget/MeetingTypeTargetTest.php`:

```php
<?php

namespace Tests\Feature\MeetingTarget;

use Illuminate\Support\Facades\DB;
use Modules\Assign\Entities\MeetingType;
use Tests\TestCase;

class MeetingTypeTargetTest extends TestCase
{
    use MeetingTargetFixture;

    protected function tearDown(): void
    {
        $this->cleanupMeetingTargetFixture();
        parent::tearDown();
    }

    private function save(array $payload)
    {
        return $this->postJson('/api/v1/assign/meeting_types', $payload);
    }

    public function test_tao_loai_meeting_luu_target_type(): void
    {
        $this->actAsManager();
        $res = $this->save(['name' => 'PHPUnit loại ' . uniqid(), 'has_customer' => true, 'status' => 1, 'target_type' => 2]);
        $res->assertStatus(200);
        $this->fxTypeIds[] = $res->json('id');
        $this->assertSame(2, (int) MeetingType::find($res->json('id'))->target_type);
    }

    public function test_target_type_ngoai_1_2_bi_tu_choi(): void
    {
        $this->actAsManager();
        $res = $this->save(['name' => 'PHPUnit loại ' . uniqid(), 'status' => 1, 'target_type' => 3]);
        $this->assertContains($res->status(), [400, 422]);
        $this->assertStringContainsString('target_type', $res->getContent());
    }

    public function test_loai_dang_dung_chi_doi_duoc_target(): void
    {
        $this->actAsManager();
        $type = $this->makeType();
        $this->makeMeetingOfType($type);
        $this->save([
            'id' => $type->id, 'name' => $type->name, 'description' => $type->description,
            'has_customer' => (bool) $type->has_customer, 'status' => 1, 'target_type' => 1,
        ])->assertStatus(200);
        $this->assertSame(1, (int) $type->fresh()->target_type);
    }

    public function test_loai_dang_dung_doi_ten_bi_chan(): void
    {
        $this->actAsManager();
        $type = $this->makeType();
        $this->makeMeetingOfType($type);
        $res = $this->save([
            'id' => $type->id, 'name' => $type->name . ' đổi', 'description' => $type->description,
            'has_customer' => (bool) $type->has_customer, 'status' => 1, 'target_type' => 1,
        ]);
        $res->assertStatus(423);
        $this->assertSame('Loại meeting đã có meeting, chỉ được đổi Meeting theo đối tượng.', $res->json('message'));
        $this->assertSame($type->name, $type->fresh()->name);
        $this->assertNull($type->fresh()->target_type);
    }

    public function test_loc_target_type_0_la_null(): void
    {
        $this->actAsManager();
        $none = $this->makeType();
        $contract = $this->makeType(['target_type' => 2]);
        $ids0 = collect($this->getJson('/api/v1/assign/meeting_types?target_type=0&per_page=1000')->json('data'))->pluck('id');
        $ids2 = collect($this->getJson('/api/v1/assign/meeting_types?target_type=2&per_page=1000')->json('data'))->pluck('id');
        $this->assertTrue($ids0->contains($none->id));
        $this->assertFalse($ids0->contains($contract->id));
        $this->assertTrue($ids2->contains($contract->id));
    }

    public function test_resource_tra_target_text_va_co_sua(): void
    {
        $this->actAsManager();
        $type = $this->makeType(['target_type' => 1]);
        $this->makeMeetingOfType($type);
        $row = collect($this->getJson('/api/v1/assign/meeting_types?per_page=1000')->json('data'))->firstWhere('id', $type->id);
        $this->assertSame('Dự án TKT', $row['target_type_text']);
        $this->assertFalse($row['is_can_edit']);
        $this->assertTrue($row['is_can_edit_target']);
    }

    public function test_doi_target_ghi_lich_su(): void
    {
        $this->actAsManager();
        $type = $this->makeType();
        $this->save([
            'id' => $type->id, 'name' => $type->name, 'has_customer' => (bool) $type->has_customer,
            'status' => 1, 'target_type' => 2,
        ])->assertStatus(200);
        $log = DB::table('catalog_histories')->where('table_name', 'meeting_types')
            ->where('record_id', $type->id)->orderByDesc('id')->first();
        $this->assertNotNull($log);
        $this->assertStringContainsString('Hợp đồng', json_encode($log, JSON_UNESCAPED_UNICODE));
    }
}
```

Kiểm trước khi chạy: nhân viên 27 có quyền "Quản lý danh mục loại meeting" qua role; không có thì đổi `E2E_MANAGER_EMPLOYEE_ID`. Danh sách trả `data` ở đâu: đọc 1 response thật (`getJson(...)->json()`), sửa đường dẫn `data` nếu khuôn khác.

- [x] **Step 3: Chạy test, phải FAIL**

Run: `cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Feature/MeetingTarget/MeetingTypeTargetTest.php`
Expected: FAIL (`target_type` không được lưu / thiếu key `target_type_text`).

- [x] **Step 4: Entity** — `MeetingType.php`: thêm `'target_type'` vào `$fillable`, và:

```php
    /** Meeting theo đối tượng — nguồn tên DUY NHẤT (resource, file xuất, lịch sử đọc từ đây) */
    const TARGET_PROSPECTIVE_PROJECT = 1;
    const TARGET_CONTRACT = 2;
    const TARGETS = [
        self::TARGET_PROSPECTIVE_PROJECT => 'Dự án TKT',
        self::TARGET_CONTRACT => 'Hợp đồng',
    ];

    public static function targetName($targetType): string
    {
        return self::TARGETS[(int) $targetType] ?? '';
    }

    /**
     * Loại đã có meeting: KHÔNG sửa được tên/mô tả/khách hàng (isCanEdit = false) nhưng vẫn được
     * đổi "Meeting theo đối tượng" (design #7). Loại hệ thống khoá hoàn toàn; loại đã khoá cũng không.
     */
    public function isCanEditTargetOnly()
    {
        return !$this->isSystem()
            && $this->status == self::STATUS_ACTIVE
            && $this->meetings()->exists();
    }
```

- [x] **Step 5: Request** — `MeetingTypeRequest::rules()` thêm:
  `'target_type' => 'nullable|in:' . MeetingType::TARGET_PROSPECTIVE_PROJECT . ',' . MeetingType::TARGET_CONTRACT,`

- [x] **Step 6: Service + Controller**
  - `MeetingTypeService::catalogColumns()` → `['code', 'name', 'has_customer', 'target_type', 'description', 'status']`.
  - `catalogDisplay()` thêm trước `return $value;`:
    ```php
        if ($column === 'target_type') {
            return MeetingType::targetName($value) ?: 'Không';
        }
    ```
  - `index()` thêm sau khối `has_customer`:
    ```php
        // Meeting theo đối tượng: '0' = không gắn (NULL), '1' Dự án TKT, '2' Hợp đồng
        if (in_array((string) $request->target_type, ['0', '1', '2'], true)) {
            (int) $request->target_type === 0
                ? $query->whereNull('meeting_types.target_type')
                : $query->where('meeting_types.target_type', (int) $request->target_type);
        }
    ```
  - `updateOrCreate()` nhánh có `id`, chèn NGAY sau `$meetingType = MeetingType::find($request->id);`:
    ```php
            // Loại đã có meeting: chỉ cho đổi "Meeting theo đối tượng" (design #7)
            if ($meetingType && $meetingType->isCanEditTargetOnly()) {
                $changedOther = (string) $request->name !== (string) $meetingType->name
                    || (string) $request->description !== (string) $meetingType->description
                    || (bool) $request->has_customer !== (bool) $meetingType->has_customer
                    || (int) ($request->status ?? MeetingType::STATUS_ACTIVE) !== (int) $meetingType->status;
                if ($changedOther) {
                    return ['status' => '423', 'message' => 'Loại meeting đã có meeting, chỉ được đổi Meeting theo đối tượng.'];
                }
                $before = $this->catalogSnapshot($meetingType);
                $meetingType->update(['target_type' => $request->target_type ?: null]);
                $this->logCatalogSave($meetingType, $before);
                return response()->json($meetingType, 200);
            }
    ```
    Thêm `'target_type' => $request->target_type ?: null,` vào cả `update([...])` lẫn `create([...])` hiện có.
  - `MeetingTypeController::updateOrCreate` (dòng ~63-75): đọc cách nó đổi mảng `['status' => '404', ...]` thành response, thêm nhánh `'423'` → `$this->responseJson($result['message'], Response::HTTP_LOCKED)` cùng khuôn.

- [x] **Step 7: Resource + xuất + lịch sử**
  - `MeetingTypeResource` thêm:
    ```php
        // Meeting theo đối tượng (design meeting-theo-doi-tuong)
        'target_type' => $this->target_type !== null ? (int) $this->target_type : null,
        'target_type_text' => MeetingType::targetName($this->target_type),
        'is_can_edit_target' => $this->isCanEditTargetOnly(),
    ```
  - `DetailMeetingTypeResource` thêm `'target_type'` (như trên), `'is_can_edit' => $this->isCanEdit()`, `'is_can_edit_target' => $this->isCanEditTargetOnly()` (popup cần để khoá ô).
  - `ExportColumnRegistry` mục `meeting_types`: chèn `'target_type_text' => 'Meeting theo đối tượng',` ngay sau `has_customer_text`.
  - `CatalogHistoryService.php:633` thêm `'target_type' => 'Meeting theo đối tượng',`.

- [x] **Step 8: Chạy lại test, phải PASS** (lệnh Step 3) → 7 tests OK.
- [x] **Step 9: Báo user** kết quả test + `git -C hrm-api diff --stat`. Không commit.

---

### Task 2: BE — nguồn chọn đối tượng

**Files:** `ProspectiveProject.php`, `Contract/Contract.php`, `ProspectiveProjectService.php:451-494`, `ContractController.php`, `Routes/api.php:785-790`. Test: `tests/Feature/MeetingTarget/MeetingTargetSourceTest.php`

**Interfaces:**
- Consumes: `MeetingTargetFixture` (Task 1).
- Produces: `ProspectiveProject::MEETING_STATUS_FROM = 2`, `MEETING_STATUS_TO = 10`, `scopeSelectableForMeeting($q)`; `Contract::MEETING_EXCLUDED_STATUSES = [3, 10]`, `scopeSelectableForMeeting($q)`. Endpoint `GET /api/v1/assign/contracts/for-meeting?customer_id=&include_id=` trả mảng `{id, code, customer_id, customer_code, customer_name, customer_contact_name, customer_contact_phone, status, status_name, status_color}` (đúng thứ tự key). `getForMeeting` nhận `include_ids` (chuỗi phẩy hoặc mảng).

- [x] **Step 1: Test fail**

```php
<?php

namespace Tests\Feature\MeetingTarget;

use Modules\Assign\Entities\Contract\Contract;
use Modules\Assign\Entities\ProspectiveProject;
use Tests\TestCase;

class MeetingTargetSourceTest extends TestCase
{
    use MeetingTargetFixture;

    protected function tearDown(): void
    {
        $this->cleanupMeetingTargetFixture();
        parent::tearDown();
    }

    /** Chép 1 HĐ thật, đổi mã + trạng thái (saveQuietly: không chạy hook sinh mã / lịch sử) */
    private function makeContract(int $status): Contract
    {
        $c = Contract::orderByDesc('id')->firstOrFail()->replicate();
        $c->forceFill(['code' => 'PHPUNIT-HD-' . uniqid(), 'status' => $status, 'quotation_id' => null])->saveQuietly();
        $this->fxContractIds[] = $c->id;
        return $c;
    }

    private function forMeetingIds(string $qs = '')
    {
        return collect($this->getJson('/api/v1/assign/contracts/for-meeting' . $qs)->assertStatus(200)->json('data'))->pluck('id');
    }

    public function test_for_meeting_loai_dang_tao_va_da_thanh_ly(): void
    {
        $this->actAsManager();
        $ok = $this->makeContract(Contract::STATUS_CO_HIEU_LUC);
        $draft = $this->makeContract(Contract::STATUS_DANG_TAO);
        $done = $this->makeContract(Contract::STATUS_DA_THANH_LY);
        $ids = $this->forMeetingIds();
        $this->assertTrue($ids->contains($ok->id));
        $this->assertFalse($ids->contains($draft->id));
        $this->assertFalse($ids->contains($done->id));
    }

    public function test_for_meeting_include_id_tra_hop_dong_ngoai_dai(): void
    {
        $this->actAsManager();
        $done = $this->makeContract(Contract::STATUS_DA_THANH_LY);
        $this->assertTrue($this->forMeetingIds('?include_id=' . $done->id)->contains($done->id));
    }

    public function test_for_meeting_loc_theo_khach_hang(): void
    {
        $this->actAsManager();
        $a = $this->makeContract(Contract::STATUS_CO_HIEU_LUC);
        $rows = collect($this->getJson('/api/v1/assign/contracts/for-meeting?customer_id=' . $a->customer_id)->json('data'));
        $this->assertTrue($rows->pluck('id')->contains($a->id));
        $this->assertTrue($rows->every(function ($r) use ($a) {
            return (int) $r['customer_id'] === (int) $a->customer_id;
        }));
    }

    public function test_for_meeting_khong_tra_truong_tien(): void
    {
        $this->actAsManager();
        $this->makeContract(Contract::STATUS_CO_HIEU_LUC);
        $row = $this->getJson('/api/v1/assign/contracts/for-meeting')->json('data.0');
        $this->assertSame(
            ['id', 'code', 'customer_id', 'customer_code', 'customer_name', 'customer_contact_name',
             'customer_contact_phone', 'status', 'status_name', 'status_color'],
            array_keys($row)
        );
    }

    public function test_get_for_meeting_chi_tien_trinh_2_den_10(): void
    {
        $this->actAsManager();
        $me = auth('api')->id();
        $src = ProspectiveProject::whereNull('parent_id')->orderByDesc('id')->firstOrFail();
        $make = function (int $status) use ($src, $me) {
            $p = $src->replicate();
            $p->forceFill(['code' => 'PHPUNIT-MT-' . uniqid(), 'status' => $status, 'created_by' => $me, 'parent_id' => null])->saveQuietly();
            $this->fxProjectIds[] = $p->id;
            return $p;
        };
        $p1 = $make(1);
        $p2 = $make(2);
        $p10 = $make(10);
        $p11 = $make(11);
        $url = '/api/v1/assign/prospective-projects/getForMeeting?per_page=10000';
        $ids = collect($this->getJson($url)->json('data'))->pluck('id');
        $this->assertFalse($ids->contains($p1->id));
        $this->assertTrue($ids->contains($p2->id));
        $this->assertTrue($ids->contains($p10->id));
        $this->assertFalse($ids->contains($p11->id));
        $ids = collect($this->getJson($url . '&include_ids=' . $p11->id)->json('data'))->pluck('id');
        $this->assertTrue($ids->contains($p11->id));
    }
}
```

Nếu `hrm_contracts.quotation_id` NOT NULL/UNIQUE (kiểm `SHOW COLUMNS FROM hrm_contracts`): thay `'quotation_id' => null` bằng id báo giá chưa có HĐ (`SELECT id FROM quotations WHERE id NOT IN (SELECT quotation_id FROM hrm_contracts WHERE quotation_id IS NOT NULL) LIMIT 1`), mỗi HĐ test 1 id khác nhau.

- [x] **Step 2: Chạy, phải FAIL** — `phpunit tests/Feature/MeetingTarget/MeetingTargetSourceTest.php` → 404 route `for-meeting`, dự án tiến trình 11 vẫn có trong `getForMeeting`.

- [x] **Step 3: Scope trên Entity**

```php
// ProspectiveProject.php — cạnh các hằng STATUS
    /** Dải tiến trình được gắn vào meeting (design #1) — áp cho cả dự án thường và dự án cha */
    const MEETING_STATUS_FROM = self::STATUS_THU_THAP_THONG_TIN_DU_AN;          // 2
    const MEETING_STATUS_TO = self::STATUS_NGHIEM_THU_VA_THANH_LY_HOP_DONG;     // 10

    public function scopeSelectableForMeeting($query)
    {
        return $query->whereBetween('prospective_projects.status', [self::MEETING_STATUS_FROM, self::MEETING_STATUS_TO]);
    }
```

```php
// Contract.php — cạnh các hằng STATUS
    /** Trạng thái KHÔNG được gắn vào meeting (design #2). Lọc loại trừ để trạng thái mới tự vào. */
    const MEETING_EXCLUDED_STATUSES = [self::STATUS_DANG_TAO, self::STATUS_DA_THANH_LY];

    public function scopeSelectableForMeeting($query)
    {
        return $query->whereNotIn('hrm_contracts.status', self::MEETING_EXCLUDED_STATUSES);
    }
```

- [x] **Step 4: getForMeeting** — đầu hàm thêm:

```php
        $includeIds = $request->input('include_ids', []);
        if (!is_array($includeIds)) {
            $includeIds = explode(',', (string) $includeIds);
        }
        $includeIds = array_values(array_filter(array_map('intval', $includeIds)));
```

thay khối `->where(function ($q) use ($userId) {...});` (dòng 486-492) bằng:

```php
            // Phạm vi người dùng + dải tiến trình (design #1). include_ids: dự án đang gắn ở meeting
            // đang sửa — vẫn trả về dù đã ra khỏi dải, để ô chọn không mất lựa chọn cũ.
            ->where(function ($outer) use ($userId, $includeIds) {
                $outer->where(function ($q) use ($userId) {
                    $q->selectableForMeeting()
                        ->where(function ($s) use ($userId) {
                            $s->where('prospective_projects.created_by', $userId)
                                ->orWhere('prospective_projects.solution_employee_id', $userId)
                                ->orWhereHas('supportDepartments.supportDepartmentEmployees', function ($query) use ($userId) {
                                    $query->where('employee_id', $userId);
                                });
                        });
                });
                if (!empty($includeIds)) {
                    $outer->orWhereIn('prospective_projects.id', $includeIds);
                }
            });
```

- [x] **Step 5: Endpoint HĐ** — `Routes/api.php`, group `/assign/contracts`, đặt TRƯỚC `/{id}`:

```php
        // Ô chọn Hợp đồng ở form meeting — TẤT CẢ HĐ, không lọc quyền (design #4), không trả số tiền
        Route::get('/for-meeting', [ContractController::class, 'forMeeting']);
```

`ContractController`:

```php
    /**
     * Danh sách HĐ cho ô "Hợp đồng" ở form meeting (design #2, #4, #5).
     * Không lọc quyền xem HĐ (user chốt) → CHỈ trả trường định danh, tuyệt đối không trả số tiền.
     */
    public function forMeeting(Request $request)
    {
        try {
            $includeId = (int) $request->input('include_id');
            $query = Contract::query()->where(function ($q) use ($includeId) {
                $q->selectableForMeeting();
                if ($includeId) {
                    $q->orWhere('hrm_contracts.id', $includeId);
                }
            });
            if ($request->filled('customer_id')) {
                $query->where('hrm_contracts.customer_id', (int) $request->input('customer_id'));
            }
            $statuses = Contract::getStatusList();
            $rows = $query->orderByDesc('hrm_contracts.id')
                ->get(['id', 'code', 'customer_id', 'customer_code', 'customer_name',
                       'customer_contact_name', 'customer_contact_phone', 'status'])
                ->map(function ($c) use ($statuses) {
                    return [
                        'id' => (int) $c->id,
                        'code' => $c->code,
                        'customer_id' => $c->customer_id ? (int) $c->customer_id : null,
                        'customer_code' => $c->customer_code,
                        'customer_name' => $c->customer_name,
                        'customer_contact_name' => $c->customer_contact_name,
                        'customer_contact_phone' => $c->customer_contact_phone,
                        'status' => (int) $c->status,
                        'status_name' => $statuses[$c->status]['name'] ?? '',
                        'status_color' => $statuses[$c->status]['color'] ?? '',
                    ];
                })->values();

            return $this->responseJson('success', Response::HTTP_OK, $rows);
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
```

So với `MeetingTypeController::getAll` để chắc `responseJson(..., $data)` đặt mảng ở key `data`; test đọc `data` / `data.0`.

- [x] **Step 6: Chạy lại, phải PASS** → 5 tests OK.
- [x] **Step 7: Báo user.** Không commit.

---

### Task 3: BE — meeting lưu/validate đối tượng

**Files:** `Requests/Meeting/ValidatesMeetingTarget.php` (mới), 2 request meeting, `Meeting.php`, `MeetingController.php` (store ~238-290, update ~634-672), `MeetingTransformer.php:187`, `MeetingHistoryService.php:76`. Test: `tests/Feature/MeetingTarget/MeetingTargetSaveTest.php`

**Interfaces:**
- Consumes: `MeetingType::TARGET_*` (Task 1), `ProspectiveProject::MEETING_STATUS_FROM/TO`, `Contract::selectableForMeeting()` (Task 2), `MeetingTargetFixture`.
- Produces: trait `ValidatesMeetingTarget::addMeetingTargetRules($validator, ?Meeting $current = null): void`; `MeetingController::resolveContractId(?MeetingType $type, $contractId): ?int` (static); `Meeting::contract()` belongsTo `Contract`; transformer trả `contract_id` (int|null) + `contract` (`{id, code, customer_name, status_name, status_color}` | null). Lỗi validate key `projects` và `contract_id`.

- [x] **Step 1: Test fail** — gọi thẳng logic của trait (luồng lưu meeting đầy đủ còn đụng phòng họp, thông báo… — phần đó verify bằng e2e Task 6):

```php
<?php

namespace Tests\Feature\MeetingTarget;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Support\Facades\Validator;
use Modules\Assign\Entities\Contract\Contract;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\ProspectiveProject;
use Modules\Assign\Http\Controllers\Api\V1\MeetingController;
use Modules\Assign\Http\Requests\Meeting\ValidatesMeetingTarget;
use Tests\TestCase;

class MeetingTargetSaveTest extends TestCase
{
    use MeetingTargetFixture;

    protected function tearDown(): void
    {
        $this->cleanupMeetingTargetFixture();
        parent::tearDown();
    }

    /** Chạy đúng logic của trait trên 1 payload, trả mảng lỗi */
    private function targetErrors(array $payload, ?Meeting $current = null): array
    {
        $req = new class extends FormRequest {
            use ValidatesMeetingTarget;
            public function rules() { return []; }
        };
        $req->replace($payload);
        $v = Validator::make($payload, []);
        $req->addMeetingTargetRules($v, $current);
        $v->fails();
        return $v->errors()->toArray();
    }

    private function contract(int $status): Contract
    {
        $c = Contract::orderByDesc('id')->firstOrFail()->replicate();
        $c->forceFill(['code' => 'PHPUNIT-HD-' . uniqid(), 'status' => $status, 'quotation_id' => null])->saveQuietly();
        $this->fxContractIds[] = $c->id;
        return $c;
    }

    public function test_loai_tkt_thieu_du_an_bao_loi(): void
    {
        $t = $this->makeType(['target_type' => 1]);
        $e = $this->targetErrors(['meeting_type_id' => $t->id, 'projects' => []]);
        $this->assertSame(['Vui lòng chọn Dự án TKT.'], $e['projects']);
    }

    public function test_loai_hop_dong_thieu_hop_dong_bao_loi(): void
    {
        $t = $this->makeType(['target_type' => 2]);
        $e = $this->targetErrors(['meeting_type_id' => $t->id]);
        $this->assertSame(['Vui lòng chọn Hợp đồng.'], $e['contract_id']);
    }

    public function test_chon_moi_hop_dong_da_thanh_ly_bi_chan(): void
    {
        $t = $this->makeType(['target_type' => 2]);
        $c = $this->contract(Contract::STATUS_DA_THANH_LY);
        $this->assertArrayHasKey('contract_id', $this->targetErrors(['meeting_type_id' => $t->id, 'contract_id' => $c->id]));
    }

    public function test_giu_hop_dong_cu_da_thanh_ly_van_luu_duoc(): void
    {
        $t = $this->makeType(['target_type' => 2]);
        $c = $this->contract(Contract::STATUS_DA_THANH_LY);
        $m = $this->makeMeetingOfType($t, ['contract_id' => $c->id]);
        $this->assertArrayNotHasKey('contract_id', $this->targetErrors(['meeting_type_id' => $t->id, 'contract_id' => $c->id], $m));
    }

    public function test_chon_moi_du_an_ngoai_dai_bi_chan(): void
    {
        $t = $this->makeType(['target_type' => 1]);
        $p = ProspectiveProject::whereNull('parent_id')->orderByDesc('id')->firstOrFail()->replicate();
        $p->forceFill(['code' => 'PHPUNIT-MT-' . uniqid(), 'status' => 11, 'parent_id' => null])->saveQuietly();
        $this->fxProjectIds[] = $p->id;
        $e = $this->targetErrors(['meeting_type_id' => $t->id, 'projects' => [['prospective_project_id' => $p->id]]]);
        $this->assertArrayHasKey('projects', $e);
    }

    public function test_meeting_cu_co_du_an_loai_khong_tkt_khong_bat_buoc(): void
    {
        $t = $this->makeType();
        $this->assertSame([], $this->targetErrors(['meeting_type_id' => $t->id, 'projects' => []]));
    }

    public function test_doi_loai_khoi_hop_dong_xoa_contract_id(): void
    {
        $this->assertNull(MeetingController::resolveContractId($this->makeType(), 123));
        $this->assertSame(123, MeetingController::resolveContractId($this->makeType(['target_type' => 2]), 123));
    }
}
```

- [x] **Step 2: Chạy, phải FAIL** — trait/hàm chưa tồn tại.

- [x] **Step 3: Trait** `Modules/Assign/Http/Requests/Meeting/ValidatesMeetingTarget.php`

```php
<?php

namespace Modules\Assign\Http\Requests\Meeting;

use Modules\Assign\Entities\Contract\Contract;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\MeetingType;
use Modules\Assign\Entities\ProspectiveProject;

/**
 * Meeting theo đối tượng (design meeting-theo-doi-tuong) — dùng chung cho request TẠO và SỬA.
 * Chạy trong after() để lỗi hiện CÙNG LÚC với lỗi các rule khác khi bấm Lưu.
 * Chỉ kiểm dải trạng thái với đối tượng MỚI chọn thêm: đối tượng đã gắn sẵn trên meeting được giữ
 * dù sau đó dự án đóng / HĐ thanh lý, để sửa meeting cũ không bị chặn oan.
 */
trait ValidatesMeetingTarget
{
    public function addMeetingTargetRules($validator, ?Meeting $current = null): void
    {
        $validator->after(function ($v) use ($current) {
            $type = MeetingType::find($this->input('meeting_type_id'));
            $target = $type ? (int) $type->target_type : 0;

            if ($target === MeetingType::TARGET_PROSPECTIVE_PROJECT) {
                $projects = (array) $this->input('projects', []);
                if (count($projects) === 0) {
                    $v->errors()->add('projects', 'Vui lòng chọn Dự án TKT.');
                } else {
                    $linked = $current
                        ? $current->projects()->pluck('prospective_projects.id')->map('intval')->all()
                        : [];
                    $newIds = collect($projects)->map(function ($p) {
                        return (int) (is_array($p) ? ($p['prospective_project_id'] ?? 0) : $p);
                    })->filter()->diff($linked)->values()->all();
                    if ($newIds) {
                        $bad = ProspectiveProject::whereIn('id', $newIds)
                            ->whereNotBetween('status', [ProspectiveProject::MEETING_STATUS_FROM, ProspectiveProject::MEETING_STATUS_TO])
                            ->pluck('code')->all();
                        if ($bad) {
                            $v->errors()->add('projects', 'Dự án TKT ' . implode(', ', $bad) . ' không ở tiến trình được gắn meeting.');
                        }
                    }
                }
            }

            if ($target === MeetingType::TARGET_CONTRACT) {
                $contractId = (int) $this->input('contract_id');
                if (!$contractId) {
                    $v->errors()->add('contract_id', 'Vui lòng chọn Hợp đồng.');
                } elseif (!$current || (int) $current->contract_id !== $contractId) {
                    if (!Contract::whereKey($contractId)->selectableForMeeting()->exists()) {
                        $v->errors()->add('contract_id', 'Hợp đồng không tồn tại hoặc không ở trạng thái được chọn.');
                    }
                }
            }
        });
    }
}
```

- [x] **Step 4: Gắn vào 2 request**
  - `MeetingCreateApiRequest`: `use ValidatesMeetingTarget;` trong class; cuối `withValidator($validator)` thêm `$this->addMeetingTargetRules($validator);`; `$rules` thêm `'contract_id' => 'nullable|integer',`.
  - `MeetingUpdateApiRequest`: tương tự, truyền meeting đang sửa: `$this->addMeetingTargetRules($validator, \Modules\Assign\Entities\Meeting\Meeting::find($this->route('id')));`.
  - Cả 2 file: xoá dòng `$hasProspectiveProject = filter_var(...)` nếu grep trong file xác nhận biến không còn dùng.

- [x] **Step 5: Entity Meeting** — `$fillable` (~dòng 152) thêm `'contract_id'`; thêm quan hệ:

```php
    public function contract()
    {
        return $this->belongsTo(\Modules\Assign\Entities\Contract\Contract::class, 'contract_id');
    }
```

- [x] **Step 6: Controller** — `MeetingController`:
  - Thêm:
    ```php
    /** HĐ chỉ giữ khi loại meeting là "theo Hợp đồng"; đổi sang loại khác thì xoá (design, tự chốt) */
    public static function resolveContractId(?MeetingType $type, $contractId): ?int
    {
        return $type && (int) $type->target_type === MeetingType::TARGET_CONTRACT && $contractId
            ? (int) $contractId
            : null;
    }
    ```
  - `store()` + `update()`: bỏ `'has_prospective_project'` khỏi `$request->only([...])`; thay dòng `$storeValues['has_prospective_project'] = $request->boolean('has_prospective_project');` bằng:
    ```php
        // Checkbox "Meeting theo dự án" đã bỏ — cột giữ lại, suy từ việc có gắn dự án hay không
        $storeValues['has_prospective_project'] = count((array) $request->input('projects', [])) > 0;
        $storeValues['contract_id'] = self::resolveContractId(MeetingType::find($request->meeting_type_id), $request->input('contract_id'));
    ```
    Ở `store()` biến `$meetingType` đã có ngay phía trên — dùng lại thay cho `MeetingType::find`.

- [x] **Step 7: Transformer + lịch sử**
  - `MeetingTransformer` cạnh `has_prospective_project`:
    ```php
            // Hợp đồng gắn với meeting (design meeting-theo-doi-tuong #9)
            'contract_id' => $meeting->contract_id ? (int) $meeting->contract_id : null,
            'contract' => $meeting->contract ? [
                'id' => (int) $meeting->contract->id,
                'code' => $meeting->contract->code,
                'customer_name' => $meeting->contract->customer_name,
                'status_name' => Contract::getStatusList()[$meeting->contract->status]['name'] ?? '',
                'status_color' => Contract::getStatusList()[$meeting->contract->status]['color'] ?? '',
            ] : null,
    ```
    (`use Modules\Assign\Entities\Contract\Contract;` đầu file.)
  - `MeetingHistoryService.php:76`: thay `'Gắn dự án tiềm năng' => ...` bằng `'Hợp đồng' => $meeting->contract ? $meeting->contract->code : null,` (dự án đã có dòng "Dự án gắn kèm").

- [x] **Step 8: Chạy lại, phải PASS** → 7 tests OK. Rồi `phpunit tests/Feature/MeetingTarget` → 19 tests OK, và `phpunit tests/Feature/MeetingByProjects` để chắc không vỡ test cũ.
- [x] **Step 9: Báo user.** Không commit.

---

### Task 4: FE — danh mục loại meeting

**Files:** `hrm-client/components/modal/meeting-type-modal.vue`, `hrm-client/pages/assign/meeting_type/index.vue`

**Interfaces:**
- Consumes: resource Task 1 (`target_type`, `target_type_text`, `is_can_edit`, `is_can_edit_target`), lọc `target_type`.

Đọc trước: skill `select-and-input-state`, `modal-popup`, `list-page` (skill thắng spec về hình thức).

- [x] **Step 1: Ghi trạng thái trước** (Playwright MCP): mở `/assign/meeting_type`, đo số cột tiêu đề bảng; mở popup Thêm, đếm ô nhập trong `.modal-body`. Ghi lại số đo để so sau.

- [x] **Step 2: Popup** `meeting-type-modal.vue`
  - `data.target_type: null` trong `data()` và `resetLocalData()`; thêm `targetOptions: [{ id: 1, name: 'Dự án TKT' }, { id: 2, name: 'Hợp đồng' }]`.
  - `loadData`: thêm `target_type: response.data.data.target_type ?? null`.
  - computed:
    ```js
        /** Loại đã có meeting: chỉ đổi được "Meeting theo đối tượng" (design #7) */
        isTargetOnly() {
            return !!this.id && !this.isShow && !this.data.is_can_edit && !!this.data.is_can_edit_target
        },
    ```
  - Ô Tên / Trạng thái / Mô tả: thêm `|| isTargetOnly` vào `:disabled`. `toggleHasCustomer`: điều kiện thành `if (!this.isShow && !this.isTargetOnly)`.
  - Thay khối "Cài đặt có khách hàng" bằng 1 hàng 2 ô (memory *form-modal-bo-cuc-hang-day-du*):
    ```html
            <div class="form-row align-items-end">
                <div class="col-md-6">
                    <V2BaseLabel>Meeting theo đối tượng</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.target_type"
                        :options="targetOptions"
                        placeholder="Không gắn đối tượng"
                        size="sm"
                        :disabled="isShow"
                    />
                    <V2BaseError v-if="error.target_type" :message="error.target_type" size="sm" class="mb-0 mt-1" />
                </div>
                <div class="col-md-6">
                    <div class="d-flex align-items-center" style="min-height: 31px">
                        <V2BaseCheckbox v-model="data.has_customer" :disabled="isShow || isTargetOnly" />
                        <span class="mb-0" style="cursor: pointer" @click="toggleHasCustomer">Có khách hàng</span>
                    </div>
                </div>
            </div>
            <small v-if="isTargetOnly" class="text-muted d-block mt-2">
                Loại meeting đã có meeting nên chỉ đổi được "Meeting theo đối tượng".
            </small>
    ```
  - Kiểm `V2BaseSelectInModal` xoá chọn về `null` được (prop `allowClear` mặc định bật) — cần để quay về "không gắn".

- [x] **Step 3: Màn danh sách** `index.vue`
  - `initialStateForm` thêm `target_type: ''`; `data()` thêm `targetTypeOptions: [{ id: 1, name: 'Dự án TKT' }, { id: 2, name: 'Hợp đồng' }, { id: 0, name: 'Không' }]`.
  - Bộ lọc, sau mục `has_customer`: `{ key: 'target_type', label: 'Meeting theo đối tượng', type: 'select', options: this.targetTypeOptions, placeholder: 'Chọn đối tượng' }`.
  - Cột, sau `hasCustomer`: `{ key: 'targetType', label: 'Meeting theo đối tượng', title: 'Meeting theo đối tượng', align: 'center', width: '170px', minWidth: '170px' }` (hiện mặc định).
  - Slot (memory *v2basedatatable-slot-cell-key*):
    ```html
                <template #cell-targetType="{ item }">
                    <div class="field-line text-dark font-weight-normal">{{ item.target_type_text }}</div>
                </template>
    ```
  - `exportFields` thêm `{ id: 'target_type_text', name: 'Meeting theo đối tượng' }` sau `has_customer_text`; `exportFieldKeyMap` thêm `targetType: 'target_type_text'`.
  - `getRowActions` nút Sửa: `visible: this.canManage && !item.is_system && (!!item.is_can_edit || !!item.is_can_edit_target)`.
  - Kiểm bộ lọc gửi được giá trị `0` (memory *hrm-list-page-2-loi-bo-loc-am-tham*) — `has_customer` đang dùng `id: 0` và chạy được thì làm y vậy; nếu lớp lọc bỏ giá trị falsy thì đổi id "Không" thành chuỗi `'0'`.

- [x] **Step 4: Verify Playwright MCP — đo DOM**
  (a) Bảng có cột "Meeting theo đối tượng"; ô của loại đã cấu hình đúng chữ (đọc `textContent`).
  (b) Lọc "Không" → mọi dòng ô cột này rỗng; lọc "Hợp đồng" → mọi dòng là "Hợp đồng".
  (c) Loại đang dùng: menu ⋮ có "Sửa"; popup → ô Tên `disabled === true`, ô đối tượng không disabled; đổi sang Hợp đồng, Lưu → toast thành công, cột cập nhật.
  (d) Popup Thêm: 2 ô cùng hàng (`getBoundingClientRect().top` của nhãn 2 ô lệch < 4px).
  (e) Xuất Excel có cột "Meeting theo đối tượng" (đọc dòng tiêu đề file bằng openpyxl).
  (f) Tài khoản không quyền quản lý danh mục: không thấy "Sửa".
- [x] **Step 5: Báo user** kèm số đo.

---

### Task 5: FE — form meeting

**Files:** `GeneralInfo.vue`, `MeetingForm.vue`, `create.vue`

**Interfaces:**
- Consumes: `selectedMeetingType.target_type` (Task 1, qua `getAll`), `GET assign/contracts/for-meeting` (Task 2), `getForMeeting?include_ids=` (Task 2), lỗi BE key `projects` / `contract_id`, detail trả `contract_id` + `contract` (Task 3).
- Produces: trong `GeneralInfo`: computed `targetType` (0|1|2), `showProjectPicker`, `showContractPicker`; sự kiện `project-tab-visible` (Boolean) để `MeetingForm` bật tab.

- [x] **Step 1: Ghi trạng thái trước** (MCP): mở `/assign/meeting/create`, xác nhận có checkbox: `[...document.querySelectorAll('label')].some(l => l.textContent.includes('Meeting theo dự án'))` → true.

- [x] **Step 2: GeneralInfo — dữ liệu + computed + method**
  - `data()` thêm `contracts: []`.
  - computed:
    ```js
        targetType() {
            return Number(this.selectedMeetingType?.target_type || 0)
        },
        hasExistingProjects() {
            return Array.isArray(this.form.projects) && this.form.projects.length > 0
        },
        // Thay checkbox "Meeting theo dự án" (design #6): loại = TKT, hoặc meeting đã có dự án, hoặc tạo từ dự án
        showProjectPicker() {
            return this.targetType === 1 || this.hasExistingProjects || this.isFromProject
        },
        showContractPicker() {
            return this.targetType === 2
        },
        // Đã chọn KH → chỉ HĐ của KH đó (design #5); luôn giữ HĐ đang chọn để ô không trống
        contractsForPicker() {
            const list = this.form.customer_id
                ? this.contracts.filter((c) => c.customer_id === this.form.customer_id || c.id === this.form.contract_id)
                : this.contracts
            return list.map((c) => ({ ...c, name: c.customer_name || '' }))
        },
    ```
  - `prospectiveProjectsForPicker`: bỏ `.filter((p) => p.status != 1)` (BE đã lọc dải 2–10), giữ lọc theo khách hàng.
  - `getProspectiveProjects`: gửi kèm dự án đang gắn:
    ```js
            const linked = (this.form.projects || [])
                .map((p) => (typeof p === 'object' ? p.prospective_project_id ?? p.id : p))
                .filter(Boolean)
            const qs = linked.length ? `&include_ids=${linked.join(',')}` : ''
            // URL: `assign/prospective-projects/getForMeeting?per_page=10000${qs}`
    ```
    Kiểm thứ tự ở màn Sửa: nếu `mounted` chạy trước khi `form.projects` về (xem `_id/edit.vue` gán form lúc nào) thì gọi lại `getProspectiveProjects()` + `getContracts()` khi `form.id` có giá trị (watcher `form.id`, giống cách `getMeetingType` nạp lại kèm include_ids ở watcher `meeting_type_id`).
  - Method mới:
    ```js
        async getContracts() {
            const inc = this.form.contract_id ? `?include_id=${this.form.contract_id}` : ''
            try {
                const res = await this.$store.dispatch('apiGetMethod', `assign/contracts/for-meeting${inc}`)
                this.contracts = Array.isArray(res?.data) ? res.data : Array.isArray(res?.data?.data) ? res.data.data : []
            } catch (e) {
                console.error('Error loading contracts:', e)
                this.contracts = []
            }
        },
        handleContractChange(contractId) {
            this.$set(this.form, 'contract_id', contractId || null)
            const c = this.contracts.find((x) => x.id === contractId)
            // Chọn HĐ trước → tự điền KH + người liên hệ từ HĐ (design #5); KH đang đúng thì không đè
            if (c && c.customer_id && this.form.customer_id !== c.customer_id) {
                this.autoSelectCustomerFromProject(c.customer_id, {
                    customer_contact_name: c.customer_contact_name,
                    customer_contact_phone: c.customer_contact_phone,
                })
            }
        },
    ```
    (`autoSelectCustomerFromProject` → `projectContactPayload(project)` đọc `customer_contact_*` nên truyền object như trên là đủ; HĐ không có `customer_contact_id`.)
  - `mounted` → `Promise.all` thêm `this.getContracts()`; trong nhánh `projectId` bỏ dòng `this.form.has_prospective_project = true`.
  - Watcher `form.meeting_type_id` (khối đổi loại ~dòng 1208): `keepCustomerFromProject` → `Number(newMeetingType?.target_type || 0) !== 0 || this.isFromProject || !!this.form.projects?.length`; thêm `if (Number(newMeetingType?.target_type || 0) !== 2) this.$set(this.form, 'contract_id', null)`.
  - Watcher `form.customer_id` (đọc watcher hiện có): đổi KH mà HĐ đang chọn thuộc KH khác → `this.form.contract_id = null`.
  - Watcher `showProjectPicker` (`immediate: true`): `this.$emit('project-tab-visible', val)`.

- [x] **Step 3: GeneralInfo — template**
  - Xoá khối `<b-col md="12">` chứa `<b-form-checkbox v-model="form.has_prospective_project" ...>Meeting theo dự án</b-form-checkbox>` (dòng 255-265).
  - `<template v-if="form.has_prospective_project || isFromProject">` → `<template v-if="showProjectPicker">`; nhãn: `Dự án TKT <Required v-if="targetType === 1" />`.
  - Ngay sau template dự án thêm:
    ```html
                    <b-col md="12" v-if="showContractPicker">
                        <b-form-group>
                            <template #label> Hợp đồng <Required /></template>
                            <SearchPicker
                                v-if="!isShow"
                                :items="contractsForPicker"
                                item-key="id"
                                :search-keys="['code', 'customer_name']"
                                placeholder="Tìm hợp đồng theo mã / khách hàng..."
                                :value="form.contract_id"
                                @input="handleContractChange"
                                icon="ri-file-text-line"
                            />
                            <div v-else-if="form.contract" class="d-flex align-items-center">
                                <a :href="`/assign/contracts/${form.contract.id}`" target="_blank" rel="noopener">{{ form.contract.code }}</a>
                                <span class="ml-1">— {{ form.contract.customer_name }}</span>
                                <span
                                    class="badge ml-2"
                                    :style="{ color: form.contract.status_color, background: form.contract.status_color + '1a' }"
                                    >{{ form.contract.status_name }}</span
                                >
                            </div>
                            <V2BaseError v-if="formError['contract_id']" :message="formError['contract_id'][0]" />
                        </b-form-group>
                    </b-col>
    ```
    Trước khi chốt: `ls hrm-client/pages/assign/contracts` để lấy đúng đường dẫn màn chi tiết HĐ, và đo badge trạng thái ở màn danh sách HĐ (memory *hrm-demo-html-dung-style-v2*) để dùng cùng khuôn.
  - Khối Khách hàng `v-if="form.has_prospective_project || form.customer_id || hasCustomer"` → `v-if="showProjectPicker || showContractPicker || form.customer_id || hasCustomer"`.

- [x] **Step 4: MeetingForm.vue** — đọc template (~dòng 140-160) để lấy thẻ `<GeneralInfo ...>`, thêm `@project-tab-visible="showProjectTab = $event"`; `data()` thêm `showProjectTab: false`; dòng 474 đổi điều kiện thành `if (this.showProjectTab || this.$route?.query?.project_id)`. (Không đọc `$refs` trong computed — không reactive.)

- [x] **Step 5: create.vue** — form mặc định: bỏ `has_prospective_project: false`, thêm `contract_id: null`.

- [x] **Step 6: Verify Playwright MCP — đo DOM**
  (a) Tạo mới: đếm label chứa "Meeting theo dự án" = 0.
  (b) Chọn loại TKT → có ô "Dự án TKT" kèm `*`; loại HĐ → có ô "Hợp đồng", không có ô dự án; loại không đối tượng → không có cả 2.
  (c) Meeting cũ có dự án + loại không đối tượng (tìm bằng SQL: `meetings` join `prospective_project_meetings` + `meeting_types.target_type IS NULL`): màn Sửa có ô Dự án + tab "Dự án tiền khả thi"; Lưu không có lỗi `projects`; `SELECT COUNT(*) FROM prospective_project_meetings WHERE meeting_id=?` không đổi sau lưu.
  (d) Loại HĐ, bỏ trống HĐ + bỏ trống Tên meeting, bấm Lưu 1 lần → có cả lỗi "Vui lòng chọn Hợp đồng." và lỗi Tên (đếm `.v2-error` ≥ 2).
  (e) Chọn KH trước → dropdown HĐ chỉ chứa HĐ của KH đó; chọn HĐ trước → ô KH điền đúng `customer_name` của HĐ.
  (f) Đổi loại HĐ → loại khác, Lưu → `meetings.contract_id` NULL.
  (g) Màn chi tiết meeting có HĐ: link `href` đúng id HĐ, `target="_blank"`, badge có màu.
  (h) `/assign/meeting/create?project_id=<id>`: ô dự án hiện + khoá, đã chọn đúng dự án.
  (i) Tài khoản KHÔNG có quyền xem Hợp đồng: dropdown HĐ vẫn có dữ liệu (design #4).
- [x] **Step 7: Báo user** kèm số đo.

---

### Task 6: E2E + tài liệu

**Files:** `e2e/tests/assign/meeting-target.api.spec.ts`, `e2e/tests/assign/meeting-target.spec.ts` (mới); `.plans/gop-db/STATUS.md`; `design.md` (ghi lệch nếu có)

- [x] **Step 1: Spec API** (`serial`, khuôn `meeting-host.api.spec.ts`): (1) loại HĐ thiếu `contract_id` → 400 + "Vui lòng chọn Hợp đồng."; (2) chọn HĐ đã thanh lý → 400; (3) meeting loại HĐ lưu được, detail trả `contract.code`; (4) đổi sang loại khác → detail `contract_id` null; (5) `for-meeting` bằng token tài khoản không quyền HĐ → 200, không key nào chứa `amount`/`total`; (6) danh mục: loại đang dùng đổi tên → 423. `afterAll` trả dữ liệu về như cũ.
- [x] **Step 2: Spec UI**: các ca (a)(b)(d)(e) của Task 5 Step 6 và (c)(d) của Task 4 Step 4; mỗi ca assert số đo DOM (số phần tử, chữ, `disabled`). Không chờ `networkidle`.
- [x] **Step 3: KHÔNG tự chạy** — báo user lệnh: `cd e2e && npx playwright test tests/assign/meeting-target --workers=1`; khi chạy thì đọc dòng tổng kết (không tin "did not run").
- [x] **Step 4: Cập nhật** `.plans/gop-db/STATUS.md` (trạng thái, file đã đụng, việc còn lại: thiết kế mobile), ghi lệch vào `design.md` nếu có.

---

### Checkpoint — 2026-10-08 23:40
Vừa hoàn thành: Task 1–6 (BE 19/19 PHPUnit xanh + MeetingByProjects 28/28; FE kiểm bằng Playwright MCP; viết 2 spec e2e, CHƯA chạy).
Đang làm dở: review toàn nhánh.
Bước tiếp theo: user chạy `cd e2e && npx playwright test tests/assign/meeting-target --workers=1` (Node 20); cập nhật thiết kế app mobile sau.
Blocked:

**Lệch so với plan (ruling):** catalog_histories dùng `table_id`; DB local là `hrm_erp`; migrate bằng `--path` từng file (module:migrate kéo migration pending của feature khác); fixture tự insert hợp đồng (local rỗng, `quotation_id` NOT NULL UNIQUE FK); snapshot lịch sử meeting load thêm `contract`; chọn HĐ điền KH từ dữ liệu HĐ trước khi gọi chi tiết KH (403 khi không quyền "Xem khách hàng" làm KH bỏ trống); ô HĐ truyền `statusLabel`; ghi chú popup màu `#6b7280` (`.text-muted` = đỏ); badge HĐ dùng `V2BaseBadge`.

**Dữ liệu local đã đổi (giữ lại để dùng thử):** `meeting_types` id 16 "Họp trao đổi thực hiện hợp đồng" → Hợp đồng, id 15 "Họp dự án Tiền khả thi" → Dự án TKT (cấu hình qua UI lúc kiểm). Dữ liệu tạm (meeting 5768, HĐ 37/38, thông báo) đã xoá.

**Vấn đề ngoài luồng (chưa sửa):** form meeting có cảnh báo Vue sẵn từ trước — prop `hasCustomer` nhận Number 1 thay vì Boolean, computed `hasCustomer` trùng tên prop, computed `fields` trùng data.

### Checkpoint — 2026-10-08 23:55 (sau review toàn nhánh)
Vừa hoàn thành: sửa 4 lỗi Important của reviewer (I1 include_ids lộ dự án → meeting_id + canView; I2 bỏ SĐT khỏi for-meeting; I3 màn Sửa/Xem không tải list lúc mount; I4 giữ HĐ meeting cũ khi admin đổi cấu hình loại) + M1 spec e2e. BE 22/22 PHPUnit, MeetingByProjects 28/28; FE kiểm lại bằng MCP.
Bước tiếp theo: user chạy e2e `meeting-target*`; cập nhật thiết kế app mobile.
Minor để lại: M2 ô dự án ẩn ngay khi bỏ dự án cuối (loại không target) · M3 so sánh trim/CRLF có thể 423 nhầm · M4 BE không kiểm HĐ cùng KH meeting · M5 thêm 1 exists()/dòng ở MeetingTypeResource · M6 has_prospective_project suy theo count(projects).
Blocked:
