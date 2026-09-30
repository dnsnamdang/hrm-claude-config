# Final-fix brief — RegulationConfigService (Slice 1 Tab Công nợ versioning)

Đây là YÊU CẦU của bạn — làm ĐÚNG theo code cho sẵn, KHÔNG mở rộng phạm vi.
Sửa **duy nhất** file:
`hrm-api/Modules/MasterData/Services/RegulationConfigService.php`
và **thêm 2 test** vào:
`hrm-api/Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php`

KHÔNG đụng file khác. KHÔNG commit git (dự án cấm). Giữ nguyên line ending của file.

Bối cảnh: đây là vá sau review tổng thể. 4 thay đổi trong service + 2 test. Tất cả code đã cho sẵn bên dưới — chép chính xác.

---

## Thay đổi 1 — GỠ dead code `baselineForDate`

Xoá TRỌN method `public function baselineForDate(...) { ... }` (hiện ở khoảng dòng 122–136). Không nơi nào gọi (đã grep xác nhận). Không để lại comment thừa.

## Thay đổi 2 — `applyDueCongnoVersions` nhận thêm optional `$companyId`

Thay method hiện tại bằng:

```php
    public function applyDueCongnoVersions(?Carbon $today = null, ?int $companyId = null): int
    {
        $today = $today ?: now();
        $count = 0;

        $query = RegulationScheduledVersion::where('tab_key', self::TAB_CONGNO)
            ->where('scope_type', self::SCOPE_COMPANY)
            ->pending()
            ->whereDate('effective_date', '<=', $today->toDateString());

        if ($companyId !== null) {
            $query->where('scope_id', $companyId);
        }

        $due = $query->orderBy('scope_id')->orderBy('effective_date')->orderBy('id')->get();

        foreach ($due as $version) {
            $this->applyVersion($version);
            $count++;
        }
        return $count;
    }
```

(Chữ ký cũ `applyDueCongnoVersions(?Carbon $today = null)` vẫn tương thích — cron/command gọi không tham số vẫn áp mọi công ty.)

## Thay đổi 3 — `applyVersion` khoá bản ghi chống áp trùng

Thay method hiện tại bằng:

```php
    public function applyVersion(RegulationScheduledVersion $version): void
    {
        if ($version->status !== RegulationScheduledVersion::STATUS_PENDING) {
            return; // idempotent fast-path
        }

        DB::transaction(function () use ($version) {
            // Khoá bản ghi để chống áp trùng khi apply-ngay (request) chạy song song với cron.
            $locked = RegulationScheduledVersion::whereKey($version->getKey())->lockForUpdate()->first();
            if (!$locked || $locked->status !== RegulationScheduledVersion::STATUS_PENDING) {
                return; // đã bị tiến trình khác áp
            }
            $companyId = (int) $locked->scope_id;

            $old = $this->getCurrentCongnoValues($companyId);
            $new = $this->normalizeValues($locked->payload ?? []);

            $company = Company::findOrFail($companyId);
            foreach (self::CONGNO_FIELDS as $key => $meta) {
                $company->{$key} = $new[$key];
            }
            $company->updated_by = $locked->created_by; // cron không có auth
            $company->save();

            foreach ($this->buildDiffSnapshot($old, $new) as $diff) {
                CompanyRegulationHistory::create([
                    'company_id' => $companyId,
                    'created_by' => $locked->created_by,
                    'field_name' => $diff['key'],
                    'name' => $diff['label'],
                    'value_before' => $diff['old'],
                    'value_after' => $diff['new'],
                ]);
            }

            $locked->status = RegulationScheduledVersion::STATUS_APPLIED;
            $locked->applied_at = now();
            $locked->saveQuietly();
        });

        $version->refresh(); // đồng bộ trạng thái cho caller
    }
```

## Thay đổi 4a — đuôi áp-ngay của `createCongnoVersion` gọi apply-all theo cty

Trong `createCongnoVersion`, đoạn đuôi hiện tại:

```php
        $version = $version->fresh();
        if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
            $this->applyVersion($version);              // áp-ngay khi ngày <= hôm nay
            $version = $version->fresh();
        }
        return $version;
```

đổi dòng gọi `applyVersion($version)` thành:

```php
        $version = $version->fresh();
        if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
            // áp-ngay: áp TẤT CẢ bản đến hạn của công ty theo đúng thứ tự ngày (khớp cron)
            $this->applyDueCongnoVersions(null, $companyId);
            $version = $version->fresh();
        }
        return $version;
```

(`$companyId` đã có sẵn trong scope của method này.)

## Thay đổi 4b — `updateCongnoVersion` thêm đuôi áp-ngay (spec §9)

Thay method hiện tại bằng:

```php
    public function updateCongnoVersion(int $versionId, string $effectiveDate, array $values, ?string $note): RegulationScheduledVersion
    {
        $version = RegulationScheduledVersion::findOrFail($versionId);
        abort_unless($version->status === RegulationScheduledVersion::STATUS_PENDING, 422, 'Chỉ sửa được phiên bản đang chờ áp dụng');

        $companyId = (int) $version->scope_id;
        $version->effective_date = $effectiveDate;
        $version->payload = $this->normalizeValues($values);
        $version->note = $note;
        $version->save();

        $this->recomputeDiffChain($companyId);

        $version = $version->fresh();
        if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
            // áp-ngay khi sửa ngày hiệu lực về hôm nay/quá khứ (spec §9), cùng cơ chế create
            $this->applyDueCongnoVersions(null, $companyId);
            $version = $version->fresh();
        }
        return $version;
    }
```

---

## Test — thêm 2 test vào RegulationCongnoVersioningTest.php

Đọc file test hiện có TRƯỚC (9 test đang xanh) để dùng lại đúng helper tạo Company + service + hằng field. Bám sát pattern sẵn có (cách tạo company, gọi `app(RegulationConfigService::class)` hoặc biến `$this->service`, cách assert cột company + status version). 2 test mới:

### Test A — update về hôm nay thì áp ngay
- Tạo 1 version qua `createCongnoVersion` với `effective_date` = **tương lai** (vài ngày sau) → còn `pending`, cột company CHƯA đổi.
- Gọi `updateCongnoVersion($id, today, $newValues, null)` với `today` = ngày hôm nay (`now()->toDateString()`).
- Assert: version `status === 'applied'`; công ty đã mang giá trị `$newValues` (vd `interest_rate` mới); có bản ghi trong `company_regulation_histories`.

### Test B — áp-ngay áp NHIỀU bản đến hạn theo thứ tự ngày
- Tạo v1 với ngày tương lai rồi kéo `effective_date` về **hôm qua** bằng `saveQuietly()` (giữ nó `pending`, KHÔNG cho áp-ngay lúc tạo — đúng thủ thuật các test cron đang dùng, xem comment "để tránh áp-ngay lúc tạo" trong file).
- Tạo v2 qua `createCongnoVersion` với `effective_date` = **hôm nay** và giá trị khác v1 → đuôi áp-ngay gọi `applyDueCongnoVersions(null,$companyId)` → áp v1 (hôm qua) trước, rồi v2 (hôm nay).
- Assert: cả v1 và v2 `status==='applied'`; công ty mang giá trị của **v2** (bản áp sau cùng, đúng thứ tự ngày).

Nếu chi tiết field/giá trị cần số cụ thể: dùng đúng 7 field trong `CONGNO_FIELDS` (interest_rate là decimal; 6 field còn lại integer). Giá trị test tuỳ bạn chọn miễn v1 ≠ v2 để phân biệt.

---

## Chạy test (BẮT BUỘC — dùng phpunit, KHÔNG dùng `artisan test --filter`)

```
cd hrm-api && vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php --testdox
```

Phải: TẤT CẢ test (9 cũ + 2 mới) PASS. `artisan test --filter` fail trên môi trường này ("No tests executed!") — đừng dùng.

DB test = `.env` DB_DATABASE (erp_hrm_check, MySQL) — `lockForUpdate` chạy được trên MySQL trong transaction.

## Báo cáo
Ghi report đầy đủ vào: `HRM/.plans/gop-db/khai-quy-che-cau-hinh/sdd/final-fix-report.md`
(gồm: các thay đổi đã làm, kết quả `phpunit --testdox` full, số test/assertion, concern nếu có).
Trả về cho controller: STATUS + 1 dòng tóm tắt test + concern. KHÔNG tự spawn subagent nào.
