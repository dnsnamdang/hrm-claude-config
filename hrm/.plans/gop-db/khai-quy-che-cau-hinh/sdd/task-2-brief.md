# Task 2 brief

## Task 2: Models `RegulationScheduledVersion` + `CompanyRegulationHistory`

**Files:**
- Create: `Modules/MasterData/Entities/RegulationScheduledVersion.php`
- Create: `Modules/MasterData/Entities/CompanyRegulationHistory.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php`

**Interfaces:**
- Produces:
  - `RegulationScheduledVersion` (extends `App\Models\BaseModel`): casts `payload` + `diff_snapshot` → array, `effective_date` → date, `applied_at` → datetime; `$fillable` gồm scope_type, scope_id, tab_key, effective_date, status, payload, diff_snapshot, note, applied_at; scope helper `scopePending`, `scopeApplied`, `scopeFor($scopeType,$scopeId,$tabKey)`; relation `employeeCreate()` (kế thừa từ BaseModel qua created_by).
  - `CompanyRegulationHistory` (extends `Illuminate\Database\Eloquent\Model`, KHÔNG BaseModel): `$table='company_regulation_histories'`, `$fillable=['company_id','created_by','field_name','name','value_before','value_after']`, `public $timestamps=true`.

- [ ] **Step 1: Viết test đọc/tạo bản ghi version (failing)**

`Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php`:

```php
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
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api && php artisan test --filter=RegulationCongnoVersioningTest::it_casts_payload_and_diff_to_array`
Expected: FAIL — "Class 'Modules\MasterData\Entities\RegulationScheduledVersion' not found".

- [ ] **Step 3: Viết model `RegulationScheduledVersion`**

```php
<?php

namespace Modules\MasterData\Entities;

use App\Models\BaseModel;

class RegulationScheduledVersion extends BaseModel
{
    protected $table = 'regulation_scheduled_versions';

    protected $fillable = [
        'scope_type', 'scope_id', 'tab_key', 'effective_date',
        'status', 'payload', 'diff_snapshot', 'note', 'applied_at',
    ];

    protected $casts = [
        'payload' => 'array',
        'diff_snapshot' => 'array',
        'effective_date' => 'date',
        'applied_at' => 'datetime',
    ];

    const STATUS_PENDING = 'pending';
    const STATUS_APPLIED = 'applied';
    const STATUS_CANCELED = 'canceled';

    public function scopePending($q) { return $q->where('status', self::STATUS_PENDING); }
    public function scopeApplied($q) { return $q->where('status', self::STATUS_APPLIED); }

    public function scopeFor($q, $scopeType, $scopeId, $tabKey)
    {
        return $q->where('scope_type', $scopeType)
                 ->where('scope_id', $scopeId)
                 ->where('tab_key', $tabKey);
    }
}
```

- [ ] **Step 4: Viết model `CompanyRegulationHistory`**

```php
<?php

namespace Modules\MasterData\Entities;

use Illuminate\Database\Eloquent\Model;

class CompanyRegulationHistory extends Model
{
    protected $table = 'company_regulation_histories';

    protected $fillable = [
        'company_id', 'created_by', 'field_name', 'name', 'value_before', 'value_after',
    ];

    public $timestamps = true;
}
```

- [ ] **Step 5: Chạy test để xác nhận pass**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::it_casts_payload_and_diff_to_array`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add Modules/MasterData/Entities/RegulationScheduledVersion.php Modules/MasterData/Entities/CompanyRegulationHistory.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): add versioning + company regulation history models"
```

---

