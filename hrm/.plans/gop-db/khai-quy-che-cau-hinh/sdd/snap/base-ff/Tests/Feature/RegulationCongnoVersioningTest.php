<?php

namespace Modules\MasterData\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\MasterData\Entities\RegulationScheduledVersion;
use Modules\MasterData\Http\Controllers\V1\RegulationConfigController;

class RegulationCongnoVersioningTest extends TestCase
{
    use DatabaseTransactions;

    /** @test */
    public function it_casts_payload_and_diff_to_array()
    {
        $v = RegulationScheduledVersion::create([
            'scope_type' => 'company',
            'scope_id' => 999999,          // company giả, không áp trong test này
            'tab_key' => 'congno',
            'effective_date' => '2099-01-01',
            'status' => 'pending',
            'payload' => ['interest_rate' => 1.6],
            'diff_snapshot' => [['key' => 'interest_rate', 'label' => 'Lãi suất', 'old' => '1.5', 'new' => '1.6', 'unit' => '%']],
            'note' => 'test',
        ]);

        $fresh = RegulationScheduledVersion::find($v->id);
        $this->assertIsArray($fresh->payload);
        $this->assertSame(1.6, (float) $fresh->payload['interest_rate']);
        $this->assertIsArray($fresh->diff_snapshot);
        $this->assertSame('pending', $fresh->status);
    }

    /** @test */
    public function it_reads_current_congno_values_from_companies()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000,
            'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30,
            'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60,
            'warning_due_date' => 7,
            'interest_rate' => 1.5,
        ]);

        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $values = $svc->getCurrentCongnoValues($companyId);

        $this->assertSame(200000000, $values['limit_export_debt_employee']);
        $this->assertSame(1.5, (float) $values['interest_rate']);

        $config = $svc->getCongnoConfig($companyId);
        $this->assertCount(7, $config['fields']);
        $this->assertNull($config['applied_version']); // chưa hẹn bản nào → Bản gốc
        $this->assertSame([], $config['pending']);
        // field đầu đúng metadata
        $this->assertSame('limit_export_debt_employee', $config['fields'][0]['key']);
        $this->assertSame('Hạn mức công nợ xuất hàng NV', $config['fields'][0]['label']);
    }

    /** @test */
    public function it_creates_pending_version_with_diff_and_rechains()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);

        $base = $svc->getCurrentCongnoValues($companyId);

        // V1: đổi lãi suất 1.5 -> 1.6, hiệu lực xa
        $v1 = $svc->createCongnoVersion($companyId, '2099-01-01',
            array_merge($base, ['interest_rate' => 1.6]), 'Tăng lãi suất', 1);
        $this->assertSame('pending', $v1->status);
        $this->assertCount(1, $v1->fresh()->diff_snapshot);
        $this->assertSame('interest_rate', $v1->fresh()->diff_snapshot[0]['key']);
        $this->assertSame('1.5', (string) $v1->fresh()->diff_snapshot[0]['old']);

        // V2: hiệu lực SAU V1, đổi lãi suất 1.6 -> 1.7 => "cũ" phải là 1.6 (payload V1), không phải 1.5
        $v2 = $svc->createCongnoVersion($companyId, '2099-02-01',
            array_merge($base, ['interest_rate' => 1.7]), 'Tăng tiếp', 1);
        $diff2 = collect($v2->fresh()->diff_snapshot)->firstWhere('key', 'interest_rate');
        $this->assertSame('1.6', (string) $diff2['old']);
        $this->assertSame('1.7', (string) $diff2['new']);

        // Huỷ V1 => baseline của V2 quay lại giá trị hiện hành 1.5
        $svc->cancelCongnoVersion($v1->id);
        $diff2b = collect($v2->fresh()->diff_snapshot)->firstWhere('key', 'interest_rate');
        $this->assertSame('1.5', (string) $diff2b['old']);
    }

    /** @test */
    public function it_applies_now_when_date_is_today_and_writes_history()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $base = $svc->getCurrentCongnoValues($companyId);

        $today = now()->toDateString();
        $v = $svc->createCongnoVersion($companyId,
            $today, array_merge($base, ['interest_rate' => 1.6, 'warning_due_date' => 10]),
            'Áp ngay', 1);

        // đã áp: companies cập nhật + status applied
        $this->assertSame('applied', $v->fresh()->status);
        $this->assertSame(1.6, (float) \App\Models\Company::find($companyId)->interest_rate);
        $this->assertSame(10, (int) \App\Models\Company::find($companyId)->warning_due_date);

        // history: đúng 2 dòng (interest_rate, warning_due_date), created_by = actor
        $rows = \Modules\MasterData\Entities\CompanyRegulationHistory::where('company_id', $companyId)->get();
        $this->assertCount(2, $rows);
        $this->assertEqualsCanonicalizing(
            ['interest_rate', 'warning_due_date'],
            $rows->pluck('field_name')->all()
        );
        $ir = $rows->firstWhere('field_name', 'interest_rate');
        $this->assertSame('1.5', rtrim(rtrim((string) $ir->value_before, '0'), '.'));
        $this->assertSame('1.6', rtrim(rtrim((string) $ir->value_after, '0'), '.'));
        $this->assertSame(1, (int) $ir->created_by);

        // idempotent: áp lại no-op
        $svc->applyVersion($v->fresh());
        $this->assertCount(2, \Modules\MasterData\Entities\CompanyRegulationHistory::where('company_id', $companyId)->get());
    }

    /** @test */
    public function cron_applies_due_pending_in_date_order()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $base = $svc->getCurrentCongnoValues($companyId);

        // Tạo cả 2 bản ở TƯƠNG LAI để tránh áp-ngay lúc tạo, rồi kéo về ngày quá hạn -> giữ pending
        $v1 = $svc->createCongnoVersion($companyId, now()->addYear()->toDateString(),
            array_merge($base, ['interest_rate' => 1.6]), 'a', 1);
        $v1->effective_date = now()->subDay()->toDateString(); // hôm qua
        $v1->saveQuietly();

        $v2 = $svc->createCongnoVersion($companyId, now()->addYear()->addDay()->toDateString(),
            array_merge($base, ['interest_rate' => 1.7]), 'b', 1);
        $v2->effective_date = now()->toDateString(); // hôm nay
        $v2->saveQuietly();

        $applied = $svc->applyDueCongnoVersions();
        $this->assertGreaterThanOrEqual(2, $applied);
        $this->assertSame(1.7, (float) \App\Models\Company::find($companyId)->interest_rate);
    }

    /** @test */
    public function command_applies_due_versions()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $base = $svc->getCurrentCongnoValues($companyId);
        $v = $svc->createCongnoVersion($companyId, now()->addYear()->toDateString(),
            array_merge($base, ['interest_rate' => 1.9]), 'future', 1);
        $v->effective_date = now()->toDateString();   // kéo về hôm nay, vẫn pending
        $v->saveQuietly();

        $this->artisan('regulation-config:apply-scheduled')->assertExitCode(0);
        $this->assertSame(1.9, (float) \App\Models\Company::find($companyId)->interest_rate);
        $this->assertSame('applied', $v->fresh()->status);
    }

    /**
     * XANH THẬT #1 — API tạo pending version + trả config, với 1 nhân viên có quyền
     * "Cài đặt cấu hình" ĐĂNG NHẬP THẬT (không mock quyền/gate). Dựng context: 1 dòng bảng
     * `employees` dùng đồng thời qua 2 model (App\Models\TpEmployee để actingAs guard 'api',
     * Modules\Timesheet\Entities\Employee để gán quyền qua spatie giveDirectPermissionTo — cùng
     * 1 bảng vật lý). teams-feature của spatie đang tắt (`config('permission.teams') === false`)
     * nên gán trực tiếp không cần set permissionsTeamId.
     */
    public function test_api_creates_pending_version_and_returns_config()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $this->actingAsSeededUserWithPermission();

        $payload = [
            'company_id' => $companyId,
            'effective_date' => '2099-01-01',
            'note' => 'Tăng lãi suất',
            'values' => [
                'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
                'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
                'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.6,
            ],
        ];
        $res = $this->postJson('/api/v1/master-data/regulation-config/congno/versions', $payload);
        $res->assertStatus(200);
        $res->assertJsonPath('data.config.pending.0.diff_snapshot.0.key', 'interest_rate');

        $get = $this->getJson('/api/v1/master-data/regulation-config/congno?company_id=' . $companyId);
        $get->assertStatus(200);
        $get->assertJsonCount(7, 'data.fields');
    }

    /**
     * XANH THẬT #2 — Route HTTP đăng ký đúng dưới prefix /api/v1/master-data và guard quyền
     * ("Cài đặt cấu hình") fail-closed cho 1 nhân viên ĐÃ ĐĂNG NHẬP nhưng KHÔNG có quyền này
     * → 403 ở cả 4 endpoint, không phải 404/500.
     *
     * Group route đã bọc middleware auth:api (khớp mọi module khác) → nhân viên đã đăng nhập
     * nhưng thiếu quyền lọt qua middleware rồi bị guard() chặn 403. Guest thật (chưa auth) bị
     * middleware chặn 401 trước khi vào controller — xem test riêng bên dưới.
     */
    public function test_api_routes_registered_and_permission_guard_fails_closed_without_auth()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $version = $svc->createCongnoVersion($companyId, '2099-01-01',
            array_merge($svc->getCurrentCongnoValues($companyId), ['interest_rate' => 1.6]), 'x', 1);

        // Nhân viên đăng nhập thật nhưng KHÔNG được cấp quyền "Cài đặt cấu hình".
        $email = 'regulation-config-noperm-' . uniqid() . '@example.com';
        $employeeId = \Illuminate\Support\Facades\DB::table('employees')->insertGetId([
            'email' => $email,
            'password' => bcrypt('secret'),
            'token_version' => 1,
            'employee_info_id' => 999999998,
            'status' => 1,
            'login_count' => 0,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        $user = \App\Models\TpEmployee::find($employeeId);
        // Custom Authenticate middleware buộc parseToken() → phải gửi JWT thật, actingAs không đủ.
        $this->withToken(\Tymon\JWTAuth\Facades\JWTAuth::fromUser($user));

        $this->getJson('/api/v1/master-data/regulation-config/congno?company_id=' . $companyId)
            ->assertStatus(403);

        $this->postJson('/api/v1/master-data/regulation-config/congno/versions', [
            'company_id' => $companyId,
            'effective_date' => '2099-01-01',
            'values' => [
                'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
                'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
                'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.6,
            ],
        ])->assertStatus(403);

        $this->putJson('/api/v1/master-data/regulation-config/congno/versions/' . $version->id, [
            'company_id' => $companyId,
            'effective_date' => '2099-01-02',
            'values' => [
                'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
                'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
                'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.7,
            ],
        ])->assertStatus(403);

        $this->deleteJson('/api/v1/master-data/regulation-config/congno/versions/' . $version->id)
            ->assertStatus(403);
    }

    /**
     * XANH THẬT #3 — guest (chưa đăng nhập) bị middleware auth:api chặn 401 ở CẢ 4 endpoint,
     * không lọt vào controller (tránh 500 do ResponseTrait deref auth()->user() null).
     */
    public function test_api_rejects_guest_with_401_on_all_endpoints()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);

        $this->getJson('/api/v1/master-data/regulation-config/congno?company_id=' . $companyId)
            ->assertStatus(401);

        $this->postJson('/api/v1/master-data/regulation-config/congno/versions', [])
            ->assertStatus(401);

        $this->putJson('/api/v1/master-data/regulation-config/congno/versions/1', [])
            ->assertStatus(401);

        $this->deleteJson('/api/v1/master-data/regulation-config/congno/versions/1')
            ->assertStatus(401);
    }

    private function actingAsSeededUserWithPermission()
    {
        $email = 'regulation-config-test-' . uniqid() . '@example.com';
        $employeeId = \Illuminate\Support\Facades\DB::table('employees')->insertGetId([
            'email' => $email,
            'password' => bcrypt('secret'),
            'token_version' => 1,
            'employee_info_id' => 999999999,
            'status' => 1,
            'login_count' => 0,
            'created_at' => now(),
            'updated_at' => now(),
        ]);

        // Gán quyền trực tiếp qua bảng pivot spatie (employee_has_permissions): Employee entity
        // (Modules\Timesheet\Entities\Employee) không khớp model provider của guard 'api'
        // (App\Models\TpEmployee) nên gọi HasPermissions::givePermissionTo() thẳng sẽ bị spatie từ
        // chối (GuardDoesNotMatch, guard suy ra rỗng) — insert thẳng vào pivot để bỏ qua check này,
        // đúng với cách isCurrentEmployeeHasPermission() đọc lại (chỉ join qua getAllPermissions(),
        // không validate guard).
        $permission = \Spatie\Permission\Models\Permission::where('name', RegulationConfigController::PERM_EDIT)
            ->where('guard_name', 'api')->firstOrFail();
        \Illuminate\Support\Facades\DB::table('employee_has_permissions')->insert([
            'permission_id' => $permission->id,
            'model_type' => \Modules\Timesheet\Entities\Employee::class,
            'employee_id' => $employeeId,
        ]);

        $user = \App\Models\TpEmployee::find($employeeId);
        // Custom Authenticate middleware buộc parseToken() → phải gửi JWT thật, actingAs không đủ.
        $this->withToken(\Tymon\JWTAuth\Facades\JWTAuth::fromUser($user));

        return $user;
    }

    private function makeCompanyWithCongno(array $congno): int
    {
        // Tạo company tối thiểu; 7 cột congno có sẵn trên DB gộp.
        $company = \App\Models\Company::create(array_merge([
            'name' => 'Test Co ' . uniqid(),
        ], $congno));
        return $company->id;
    }
}
