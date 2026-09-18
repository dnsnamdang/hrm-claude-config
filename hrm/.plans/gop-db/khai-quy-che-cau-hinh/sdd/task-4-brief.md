# Task 4 brief

## Task 4: Service — tạo/sửa/huỷ phiên bản hẹn + diff xâu chuỗi

**Files:**
- Modify: `Modules/MasterData/Services/RegulationConfigService.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (thêm test)

**Interfaces:**
- Consumes: `getCurrentCongnoValues`, `CONGNO_FIELDS` (Task 3).
- Produces:
  - `buildDiffSnapshot(array $oldValues, array $newValues): array` — trả `[{key,label,old,new,unit}]` cho field có `old != new` (so sánh dạng chuỗi để tránh sai lệch float/int; bỏ field không đổi).
  - `baselineForDate(int $companyId, string $effectiveDate, ?int $excludeVersionId=null): array` — "cũ" = payload phiên bản pending liền trước theo `effective_date` (loại trừ id đang sửa); nếu không có → `getCurrentCongnoValues`.
  - `createCongnoVersion(int $companyId, string $effectiveDate, array $values, ?string $note, int $actorId): RegulationScheduledVersion` — tạo bản `pending` (payload = 7 field đã chuẩn hoá kiểu), tính diff_snapshot theo baseline, set `created_by=$actorId`, rồi `recomputeDiffChain`. (Áp-ngay xử lý ở Task 5, gọi sau khi tạo.)
  - `updateCongnoVersion(int $versionId, string $effectiveDate, array $values, ?string $note): RegulationScheduledVersion` — chỉ sửa bản `pending`; cập nhật payload/effective_date/note; `recomputeDiffChain`.
  - `cancelCongnoVersion(int $versionId): void` — chỉ huỷ bản `pending` → `status=canceled`; `recomputeDiffChain`.
  - `recomputeDiffChain(int $companyId): void` — tính lại `diff_snapshot` cho MỌI bản `pending` (cùng company+congno) theo thứ tự `effective_date` tăng dần; baseline mỗi bản = payload bản pending liền trước, bản đầu = giá trị hiện hành.

- [ ] **Step 1: Viết test create + diff chain (failing)**

```php
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
```

- [ ] **Step 2: Chạy test → fail**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::it_creates_pending_version_with_diff_and_rechains`
Expected: FAIL — method chưa tồn tại.

- [ ] **Step 3: Bổ sung method vào `RegulationConfigService`**

```php
    public function normalizeValues(array $input): array
    {
        $values = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $raw = $input[$key] ?? null;
            $values[$key] = ($raw === null || $raw === '') ? null : $this->castValue($raw, $meta['type']);
        }
        return $values;
    }

    public function buildDiffSnapshot(array $old, array $new): array
    {
        $diffs = [];
        foreach (self::CONGNO_FIELDS as $key => $meta) {
            $o = $old[$key] ?? null;
            $n = $new[$key] ?? null;
            if ((string) $o !== (string) $n) {
                $diffs[] = [
                    'key' => $key,
                    'label' => $meta['label'],
                    'old' => $o === null ? null : (string) $o,
                    'new' => $n === null ? null : (string) $n,
                    'unit' => $meta['unit'],
                ];
            }
        }
        return $diffs;
    }

    public function createCongnoVersion(int $companyId, string $effectiveDate, array $values, ?string $note, int $actorId): RegulationScheduledVersion
    {
        $payload = $this->normalizeValues($values);
        $version = new RegulationScheduledVersion([
            'scope_type' => self::SCOPE_COMPANY,
            'scope_id' => $companyId,
            'tab_key' => self::TAB_CONGNO,
            'effective_date' => $effectiveDate,
            'status' => RegulationScheduledVersion::STATUS_PENDING,
            'payload' => $payload,
            'diff_snapshot' => [],
            'note' => $note,
        ]);
        $version->created_by = $actorId;
        $version->updated_by = $actorId;
        $version->save();

        $this->recomputeDiffChain($companyId);
        return $version->fresh();
    }

    public function updateCongnoVersion(int $versionId, string $effectiveDate, array $values, ?string $note): RegulationScheduledVersion
    {
        $version = RegulationScheduledVersion::findOrFail($versionId);
        abort_unless($version->status === RegulationScheduledVersion::STATUS_PENDING, 422, 'Chỉ sửa được phiên bản đang chờ áp dụng');

        $version->effective_date = $effectiveDate;
        $version->payload = $this->normalizeValues($values);
        $version->note = $note;
        $version->save();

        $this->recomputeDiffChain((int) $version->scope_id);
        return $version->fresh();
    }

    public function cancelCongnoVersion(int $versionId): void
    {
        $version = RegulationScheduledVersion::findOrFail($versionId);
        abort_unless($version->status === RegulationScheduledVersion::STATUS_PENDING, 422, 'Chỉ huỷ được phiên bản đang chờ áp dụng');

        $companyId = (int) $version->scope_id;
        $version->status = RegulationScheduledVersion::STATUS_CANCELED;
        $version->save();

        $this->recomputeDiffChain($companyId);
    }

    public function recomputeDiffChain(int $companyId): void
    {
        $baseline = $this->getCurrentCongnoValues($companyId);

        $pendings = RegulationScheduledVersion::for(self::SCOPE_COMPANY, $companyId, self::TAB_CONGNO)
            ->pending()
            ->orderBy('effective_date')->orderBy('id')
            ->get();

        foreach ($pendings as $v) {
            $payload = $this->normalizeValues($v->payload ?? []);
            $v->diff_snapshot = $this->buildDiffSnapshot($baseline, $payload);
            $v->saveQuietly(); // tránh đụng updated_by/log khi chỉ tính lại hiển thị
            $baseline = $payload; // bản sau lấy payload bản trước làm "cũ"
        }
    }
```

> Ghi chú implementer: `saveQuietly()` có ở Laravel 8. Nếu BaseModel override và không có, dùng `$v->save()`. `abort_unless(...,422,...)` ném `HttpException` → Task 6 map sang response 422.

- [ ] **Step 4: Chạy test → pass**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::it_creates_pending_version_with_diff_and_rechains`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add Modules/MasterData/Services/RegulationConfigService.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): create/update/cancel congno versions with chained diff"
```

---

