# Task 5 brief

## Task 5: Service — áp dụng phiên bản (áp-ngay + core cron) + ghi history

**Files:**
- Modify: `Modules/MasterData/Services/RegulationConfigService.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (thêm test)

**Interfaces:**
- Consumes: `getCurrentCongnoValues`, `buildDiffSnapshot`, `CONGNO_FIELDS`, model `Company`, `CompanyRegulationHistory`.
- Produces:
  - `applyVersion(RegulationScheduledVersion $version): void` — trong transaction: đọc giá trị hiện hành (baseline) → ghi đè 7 cột `companies` từ `payload` + set `updated_by = $version->created_by` → insert `company_regulation_histories` mỗi field đổi (`created_by = $version->created_by`) → set `status=applied, applied_at=now`. Idempotent: nếu `status != pending` → return ngay.
  - `applyDueCongnoVersions(?\Carbon\Carbon $today=null): int` — quét MỌI bản `pending` toàn hệ thống có `effective_date <= today`, nhóm theo `(company)`, áp theo `effective_date` tăng dần (bản sau đè bản trước), trả về số bản đã áp. Dùng cho cron.
  - `createCongnoVersion(...)` mở rộng: sau khi tạo, nếu `effective_date <= today` thì gọi `applyVersion` ngay (áp-ngay). (Sửa lại phần cuối Task 4.)

- [ ] **Step 1: Viết test áp-ngay + history + idempotent (failing)**

```php
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

        // 2 bản quá hạn cùng company: hôm qua 1.6, hôm nay 1.7 => kết quả cuối 1.7
        $svc->createCongnoVersion($companyId, now()->subDay()->toDateString(),
            array_merge($base, ['interest_rate' => 1.6]), 'a', 1);
        // tạo bản tương lai rồi kéo về quá khứ để tránh áp-ngay lúc tạo:
        $v2 = $svc->createCongnoVersion($companyId, now()->addYear()->toDateString(),
            array_merge($base, ['interest_rate' => 1.7]), 'b', 1);
        $v2->effective_date = now()->toDateString();
        $v2->saveQuietly();

        $applied = $svc->applyDueCongnoVersions();
        $this->assertGreaterThanOrEqual(2, $applied);
        $this->assertSame(1.7, (float) \App\Models\Company::find($companyId)->interest_rate);
    }
```

- [ ] **Step 2: Chạy test → fail**

Run: `php artisan test --filter=RegulationCongnoVersioningTest`
Expected: 2 test mới FAIL (method `applyVersion`/`applyDueCongnoVersions` chưa có; áp-ngay chưa nối).

- [ ] **Step 3: Bổ sung apply vào service + nối áp-ngay**

Thêm `use` đầu file: `use Illuminate\Support\Facades\DB;`, `use Modules\MasterData\Entities\CompanyRegulationHistory;`, `use Carbon\Carbon;`.

```php
    public function applyVersion(RegulationScheduledVersion $version): void
    {
        if ($version->status !== RegulationScheduledVersion::STATUS_PENDING) {
            return; // idempotent
        }
        $companyId = (int) $version->scope_id;

        DB::transaction(function () use ($version, $companyId) {
            $old = $this->getCurrentCongnoValues($companyId);
            $new = $this->normalizeValues($version->payload ?? []);

            $company = Company::findOrFail($companyId);
            foreach (self::CONGNO_FIELDS as $key => $meta) {
                $company->{$key} = $new[$key];
            }
            $company->updated_by = $version->created_by; // cron không có auth
            $company->save();

            foreach ($this->buildDiffSnapshot($old, $new) as $diff) {
                CompanyRegulationHistory::create([
                    'company_id' => $companyId,
                    'created_by' => $version->created_by,
                    'field_name' => $diff['key'],
                    'name' => $diff['label'],
                    'value_before' => $diff['old'],
                    'value_after' => $diff['new'],
                ]);
            }

            $version->status = RegulationScheduledVersion::STATUS_APPLIED;
            $version->applied_at = now();
            $version->saveQuietly();
        });
    }

    public function applyDueCongnoVersions(?Carbon $today = null): int
    {
        $today = $today ?: now();
        $count = 0;

        $due = RegulationScheduledVersion::where('tab_key', self::TAB_CONGNO)
            ->where('scope_type', self::SCOPE_COMPANY)
            ->pending()
            ->whereDate('effective_date', '<=', $today->toDateString())
            ->orderBy('scope_id')->orderBy('effective_date')->orderBy('id')
            ->get();

        foreach ($due as $version) {
            $this->applyVersion($version);
            $count++;
        }
        return $count;
    }
```

Sửa cuối `createCongnoVersion` (thay `return $version->fresh();`):

```php
        $this->recomputeDiffChain($companyId);

        $version = $version->fresh();
        if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
            $this->applyVersion($version);              // áp-ngay khi ngày <= hôm nay
            $version = $version->fresh();
        }
        return $version;
```

> Ghi chú implementer: `value_before/value_after` là `decimal(16)` → lưu chuỗi số từ diff là hợp lệ; test dùng `rtrim` để so sánh vì DB có thể trả `1.60`. Cột `interest_rate` trên `companies` là decimal (giữ phần thập phân); các cột còn lại integer.

- [ ] **Step 4: Chạy toàn bộ test → pass**

Run: `php artisan test --filter=RegulationCongnoVersioningTest`
Expected: tất cả PASS.

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Services/RegulationConfigService.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): apply versions to companies + write company_regulation_histories (apply-now + cron core)"
```

---

