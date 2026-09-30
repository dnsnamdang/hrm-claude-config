# Final-fix report — RegulationConfigService (Slice 1 Tab Công nợ versioning)

## Phạm vi
Chỉ sửa 2 file theo đúng brief `final-fix-brief.md`:
- `hrm-api/Modules/MasterData/Services/RegulationConfigService.php`
- `hrm-api/Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php`

Không commit git, không đụng file nào khác, giữ nguyên line ending (LF, đã kiểm bằng `file` trước và sau khi sửa).

## Thay đổi đã thực hiện

1. **Gỡ dead code `baselineForDate`** — xoá trọn method (không nơi nào gọi), không để lại comment thừa.
2. **`applyDueCongnoVersions(?Carbon $today = null, ?int $companyId = null): int`** — thêm optional `$companyId`, lọc `where('scope_id', $companyId)` khi có; chữ ký cũ gọi không tham số vẫn áp mọi công ty (cron/command không đổi hành vi).
3. **`applyVersion`** — bọc `lockForUpdate()` re-fetch trong transaction để chống áp trùng khi apply-ngay (request) chạy song song với cron; nếu bản khoá không còn `pending` thì return sớm; cuối cùng `$version->refresh()` để đồng bộ trạng thái cho caller.
4. **Đuôi áp-ngay**:
   - `createCongnoVersion`: đổi `applyVersion($version)` thành `applyDueCongnoVersions(null, $companyId)`.
   - `updateCongnoVersion`: thêm đuôi áp-ngay giống create (spec §9) — khi `effective_date` sau update `<=` hôm nay thì gọi `applyDueCongnoVersions(null, $companyId)` rồi refresh.

Toàn bộ code chép đúng nguyên văn từ brief, không chỉnh sửa gì thêm.

## Test thêm

Đọc file test hiện có trước, tái dùng đúng helper `makeCompanyWithCongno()`, `app(RegulationConfigService::class)`, cách assert cột company + status version + bảng `company_regulation_histories`.

- **`it_applies_now_when_update_moves_effective_date_to_today`** (Test A): tạo version với ngày tương lai (+5 ngày) → còn pending, công ty chưa đổi. Gọi `updateCongnoVersion($id, today, ...)` → assert `status === 'applied'`, công ty mang `interest_rate = 1.8`, có 1 dòng history.
- **`it_applies_multiple_due_versions_in_date_order_on_apply_now`** (Test B): v1 tạo ở tương lai rồi kéo `effective_date` về hôm qua bằng `saveQuietly()` (giữ pending, tránh áp-ngay lúc tạo — đúng thủ thuật test cron sẵn có); v2 tạo qua `createCongnoVersion` với `effective_date` = hôm nay → đuôi áp-ngay gọi `applyDueCongnoVersions(null, $companyId)` áp cả v1 lẫn v2 theo thứ tự ngày. Assert cả v1, v2 `status === 'applied'`, công ty mang giá trị v2 (`interest_rate = 1.7`, bản áp sau cùng).

## Kết quả `phpunit --testdox`

Lệnh chạy:
```
cd hrm-api && vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php --testdox
```

Output đầy đủ:
```
PHPUnit 9.5.26 by Sebastian Bergmann and contributors.

Regulation Congno Versioning (Modules\MasterData\Tests\Feature\RegulationCongnoVersioning)
 ✔ It casts payload and diff to array
 ✔ It reads current congno values from companies
 ✔ It creates pending version with diff and rechains
 ✔ It applies now when date is today and writes history
 ✔ Cron applies due pending in date order
 ✔ It applies now when update moves effective date to today
 ✔ It applies multiple due versions in date order on apply now
 ✔ Command applies due versions
 ✔ Api creates pending version and returns config
 ✔ Api routes registered and permission guard fails closed without auth
 ✔ Api rejects guest with 401 on all endpoints

Time: 00:05.898, Memory: 82.50 MB

OK (11 tests, 53 assertions)
```

11 test (9 cũ + 2 mới), 53 assertion, TẤT CẢ PASS.

## Concern
- Không phát hiện vấn đề gì phát sinh. Repo `hrm-api` đang có các thay đổi chưa commit ở nhiều file khác (không do task này tạo ra — đã kiểm `git status` trước/sau, 2 file mục tiêu là các file duy nhất tôi chỉnh sửa; các file khác đã ở trạng thái modified/untracked từ trước khi tôi bắt đầu).
- Không commit git theo đúng ràng buộc.
