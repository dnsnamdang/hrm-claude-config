<?php

namespace Modules\MasterData\Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Modules\MasterData\Entities\RegulationScheduledVersion;

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

    private function makeCompanyWithCongno(array $congno): int
    {
        // Tạo company tối thiểu; 7 cột congno có sẵn trên DB gộp.
        $company = \App\Models\Company::create(array_merge([
            'name' => 'Test Co ' . uniqid(),
        ], $congno));
        return $company->id;
    }
}
