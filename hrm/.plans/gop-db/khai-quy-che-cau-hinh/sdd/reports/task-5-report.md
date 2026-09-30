# Task 5 Report — Service: applyVersion + applyDueCongnoVersions + apply-now

## Files touched (ONLY these two)
- `Modules/MasterData/Services/RegulationConfigService.php` (modified)
- `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (modified — 2 tests appended)

## Imports added (top of service file)
```php
use App\Models\Company;
use Modules\MasterData\Entities\RegulationScheduledVersion;
use Illuminate\Support\Facades\DB;
use Modules\MasterData\Entities\CompanyRegulationHistory;
use Carbon\Carbon;
```
None of the three were previously present, so no duplicates.

## Methods added

### `applyVersion(RegulationScheduledVersion $version): void`
Idempotent guard (`status !== STATUS_PENDING` → return). Inside `DB::transaction`:
reads baseline via `getCurrentCongnoValues`, normalizes `$version->payload`, writes the 7 CONGNO_FIELDS onto `Company`, sets `updated_by = $version->created_by`, saves; for each `buildDiffSnapshot($old,$new)` entry inserts one `CompanyRegulationHistory` row (`created_by` = version's creator, not `auth()`); finally sets `status = applied`, `applied_at = now()`, `saveQuietly()`.

### `applyDueCongnoVersions(?Carbon $today = null): int`
Queries all `pending` `RegulationScheduledVersion` rows with `tab_key=congno`, `scope_type=company`, `effective_date <= today`, ordered by `scope_id, effective_date, id`; calls `applyVersion` on each; returns count applied. Used by cron.

### `createCongnoVersion` tail-edit (exact, verbatim from brief)
Replaced `return $version->fresh();` with:
```php
        $this->recomputeDiffChain($companyId);

        $version = $version->fresh();
        if ($version->effective_date && $version->effective_date->lte(now()->startOfDay())) {
            $this->applyVersion($version);              // áp-ngay khi ngày <= hôm nay
            $version = $version->fresh();
        }
        return $version;
```
Earlier Task 3/4 methods (`castValue`, `getCurrentCongnoValues`, `getCongnoConfig`, `normalizeValues`, `buildDiffSnapshot`, `baselineForDate`, `updateCongnoVersion`, `cancelCongnoVersion`, `recomputeDiffChain`) untouched.

## Tests appended
1. `it_applies_now_when_date_is_today_and_writes_history` — brief's version verbatim. Relies on apply-now firing when `effective_date` is today; asserts `status=applied`, `companies.interest_rate/warning_due_date` updated, exactly 2 `company_regulation_histories` rows with correct `field_name`/`value_before`/`value_after`/`created_by`, and idempotent re-apply (no duplicate history rows).

2. `cron_applies_due_pending_in_date_order` — **corrected version used, per mandated resolution** (brief's original was defective):
   - Defect: brief created the "yesterday 1.6" version directly with a past `effective_date`, but since Task 5 makes `createCongnoVersion` apply-now when `effective_date <= today`, that version would be applied immediately at creation time and never remain `pending` — leaving only 1 pending version for the cron to find, so `assertGreaterThanOrEqual(2, $applied)` would fail.
   - Fix: both versions (`$v1`, `$v2`) are created with a **future** `effective_date` (so apply-now does NOT fire at creation), then each is pulled back to a due date (`$v1` → yesterday, `$v2` → today) via direct property assignment + `saveQuietly()`, keeping both in `pending` status. The cron (`applyDueCongnoVersions()`) is then run and correctly finds and applies both, in date order (1.6 then 1.7), leaving `interest_rate = 1.7` as the final value.
   - Exact test body used matches the mandated resolution text verbatim.

The 3 pre-existing Task 3/4 tests (`it_casts_payload_and_diff_to_array`, `it_reads_current_congno_values_from_companies`, `it_creates_pending_version_with_diff_and_rechains`) were left unmodified.

## Test run — full file, final state (all pass)

Command (from `hrm-api` dir):
```
vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
```

Output:
```
PHPUnit 9.5.26 by Sebastian Bergmann and contributors.

.....                                                               5 / 5 (100%)

Time: 00:02.597, Memory: 50.50 MB

OK (5 tests, 30 assertions)
```

### Intermediate TDD checkpoint (before implementing, tests appended only)
```
PHPUnit 9.5.26 by Sebastian Bergmann and contributors.

...FE                                                               5 / 5 (100%)

Time: 00:02.988, Memory: 50.50 MB

There was 1 error:
1) ...cron_applies_due_pending_in_date_order
Error: Call to undefined method Modules\MasterData\Services\RegulationConfigService::applyDueCongnoVersions()

There was 1 failure:
1) ...it_applies_now_when_date_is_today_and_writes_history
Failed asserting that two strings are identical.
--- Expected
+++ Actual
@@ @@
-'applied'
+'pending'

ERRORS!
Tests: 5, Assertions: 19, Errors: 1, Failures: 1.
```
Confirms the 2 new tests failed pre-implementation (missing method / apply-now not wired) and the 3 pre-existing tests kept passing throughout.

## Concerns / notes
- `.env` confirmed `DB_DATABASE=erp_hrm_check` before running tests, per global constraints.
- `BaseModel` boot hooks are `Auth::user()`-guarded; no auth is present in the test run (no login performed), and no crash occurred — consistent with the verified context note. `Company` model is `$guarded=[]` plain model (not `BaseModel`), so `updated_by` assignment there is a plain attribute set, not a boot hook side effect — works as expected in both cron and web contexts.
- `applyDueCongnoVersions` groups implicitly via the `orderBy('scope_id')` global ordering rather than an explicit per-company loop; since `applyVersion` is idempotent and processes one version at a time in ascending `(scope_id, effective_date, id)` order, multiple companies interleave safely and each company's own versions apply strictly oldest-first, matching the brief's requirement ("bản sau đè bản trước").
- No migration files were touched; the 7 `companies` columns and `company_regulation_histories` table were used as pre-existing per global constraints — no schema changes made.
- No other files were staged or committed. `git status --short` after implementation shows only the two target files as newly modified/untracked by this task's work (other modified/untracked files present in the working tree predate this task and were not touched).

## Commit
Skipped per NO-COMMIT RULE — Step 5 not executed. Working tree left with uncommitted changes to the two named files only.
