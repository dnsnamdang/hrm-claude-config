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
}
