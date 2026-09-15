# Task 3 brief

## Task 3: Service — metadata field + đọc cấu hình Công nợ hiện hành

**Files:**
- Create: `Modules/MasterData/Services/RegulationConfigService.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (thêm test)

**Interfaces:**
- Produces:
  - `RegulationConfigService::CONGNO_FIELDS` — mảng metadata 7 field (thứ tự Global Constraints): `[ 'key' => ['label'=>..., 'unit'=>..., 'type'=>'integer'|'decimal'] ]`.
  - `getCurrentCongnoValues(int $companyId): array` — đọc 7 cột từ `companies` theo `company_id`, trả `['limit_export_debt_employee'=>int, ..., 'interest_rate'=>float]` (ép kiểu theo metadata). Ném `ModelNotFoundException` nếu không có company.
  - `getCongnoConfig(int $companyId): array` — trả `['fields'=>[{key,label,unit,type,value}], 'applied_version'=>{effective_date,created_by,created_by_name,note}|null, 'pending'=>[{id,effective_date,created_by_name,note,diff_snapshot}]]`. `applied_version=null` ⇒ FE hiển thị nhãn "Bản gốc".

- [ ] **Step 1: Viết test cho `getCurrentCongnoValues` + `getCongnoConfig` (failing)**

Thêm vào `RegulationCongnoVersioningTest`:

```php
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
```

Thêm helper tạo company test (dùng `App\Models\Company`, guarded=[]) — đặt trong cùng class:

```php
    private function makeCompanyWithCongno(array $congno): int
    {
        // Tạo company tối thiểu; 7 cột congno có sẵn trên DB gộp.
        $company = \App\Models\Company::create(array_merge([
            'name' => 'Test Co ' . uniqid(),
        ], $congno));
        return $company->id;
    }
```

- [ ] **Step 2: Chạy test → fail**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::it_reads_current_congno_values_from_companies`
Expected: FAIL — service class chưa tồn tại.

- [ ] **Step 3: Viết `RegulationConfigService` (phần metadata + đọc)**

```php
<?php

namespace Modules\MasterData\Services;

use App\Models\Company;
use Modules\MasterData\Entities\RegulationScheduledVersion;

class RegulationConfigService
{
    const SCOPE_COMPANY = 'company';
    const TAB_CONGNO = 'congno';

    /** Metadata 7 field tab Công nợ — thứ tự cố định. */
    const CONGNO_FIELDS = [
        'limit_export_debt_employee' => ['label' => 'Hạn mức công nợ xuất hàng NV',       'unit' => 'đồng', 'type' => 'integer'],
        'adjust_odd_balance'         => ['label' => 'Số dư lẻ tối đa cho phép điều chỉnh', 'unit' => 'đồng', 'type' => 'integer'],
        'overdue_date_max_customer'  => ['label' => 'Số ngày quá hạn tính lãi (Bán lẻ)',   'unit' => 'ngày', 'type' => 'integer'],
        'overdue_date_max_agency'    => ['label' => 'Số ngày quá hạn tính lãi (Đại lý)',    'unit' => 'ngày', 'type' => 'integer'],
        'overdue_date_max_service'   => ['label' => 'Số ngày quá hạn tính lãi (Dịch vụ)',   'unit' => 'ngày', 'type' => 'integer'],
        'warning_due_date'           => ['label' => 'Thời gian cảnh báo thu nợ đến hạn',    'unit' => 'ngày', 'type' => 'integer'],
        'interest_rate'              => ['label' => 'Lãi suất',                             'unit' => '%',    'type' => 'decimal'],
    ];

    private function castValue($value, string $type)
    {
        if ($value === null) {
            return null;
        }
        return $type === 'decimal' ? (float) $value : (int) $value;
    }

    public function getCurrentCongnoValues(int $companyId): array
    {
        $company = Company::findOrFail($companyId);
        $values = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $values[$key] = $this->castValue($company->{$key}, $meta['type']);
        }
        return $values;
    }

    public function getCongnoConfig(int $companyId): array
    {
        $current = $this->getCurrentCongnoValues($companyId);

        $fields = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $fields[] = [
                'key' => $key,
                'label' => $meta['label'],
                'unit' => $meta['unit'],
                'type' => $meta['type'],
                'value' => $current[$key],
            ];
        }

        $applied = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->applied()
            ->orderByDesc('effective_date')->orderByDesc('id')
            ->first();

        $appliedVersion = $applied ? [
            'effective_date' => optional($applied->effective_date)->toDateString(),
            'created_by' => $applied->created_by,
            'created_by_name' => optional($applied->employee_create)->name ?? null,
            'note' => $applied->note,
        ] : null;

        $pending = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->pending()
            ->orderBy('effective_date')->orderBy('id')
            ->get()
            ->map(function ($v) {
                return [
                    'id' => $v->id,
                    'effective_date' => optional($v->effective_date)->toDateString(),
                    'created_by_name' => optional($v->employee_create)->name ?? null,
                    'note' => $v->note,
                    'diff_snapshot' => $v->diff_snapshot ?? [],
                ];
            })->values()->toArray();

        return [
            'fields' => $fields,
            'applied_version' => $appliedVersion,
            'pending' => $pending,
        ];
    }
}
```

> Ghi chú implementer: `employee_create` là relation kế thừa từ `BaseModel` (map `created_by` → `Modules\Human\Entities\Employee`); nếu tên accessor khác, grep BaseModel để dùng đúng (`getEmployeeCreateNameAttribute`).

- [ ] **Step 4: Chạy test → pass**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::it_reads_current_congno_values_from_companies`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Services/RegulationConfigService.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): read current congno config + field metadata"
```

---

