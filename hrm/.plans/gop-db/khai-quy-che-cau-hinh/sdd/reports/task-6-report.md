# Task 6 report — FormRequest + Controller + Routes

## Files created / modified

Created:
- `Modules/MasterData/Http/Requests/ScheduleRegulationVersionRequest.php`
- `Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`

Modified:
- `Modules/MasterData/Routes/api.php` — added 4 routes inside the existing `/v1/master-data` group.
- `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` — appended 2 HTTP tests + 1 private helper (5 pre-existing tests left intact, untouched).
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/khai-quy-che-cau-hinh/design.md` — appended "## Slice 1 — Quyền" note.

`git status --short` in `hrm-api` confirms only these files (plus the already-untracked Task 3-5 artifacts: Migration, `Entities/RegulationScheduledVersion.php`, `Entities/CompanyRegulationHistory.php`, `Services/RegulationConfigService.php`) were touched. No `git add`/`git commit` was run (no-commit rule respected). Note: `hrm-api` has unrelated pre-existing modified files from other work (Assign/Finance modules) not touched by me.

## PERM_EDIT chosen

`const PERM_EDIT = 'Cài đặt cấu hình';` — confirmed via seeder grep: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:248` → `Permission::create(['id' => 149, 'guard_name' => 'api', 'name' => 'Cài đặt cấu hình', 'group' => 'Cấu hình', 'type' => 3]);`. Confirmed `Modules/Human/Http/Controllers/Api/V1/CompanyController` does not gate any config edits with a dedicated permission (only unrelated report-scope permissions used). design.md updated with a "## Slice 1 — Quyền" section documenting this.

## Handler.php finding re 422/403

`app/Exceptions/Handler.php::render()` only special-cases `NotFoundHttpException` and `ModelNotFoundException` (both forced to JSON 404). Everything else — including `abort(403, ...)` and `abort(422, ...)` (from `HttpException`/`abort_unless` in the service) — falls through to `parent::render()`, i.e. Laravel's default exception handler. Since test/HTTP requests send `Accept: application/json` (via `postJson`/`getJson`/etc.), Laravel's default renderer converts `HttpException` to a clean JSON response with the correct status code automatically. **No try/catch wrapping was needed** — verified empirically: `abort(403, ...)` in `guard()` returns `403` cleanly in tests (see below), and 422 from `abort_unless` in the service (used already by Task 3-5 tests, e.g. `updateCongnoVersion`/`cancelCongnoVersion`) is exercised indirectly by the existing service tests without issue.

## Real (unrelated) bug found — NOT fixed, reported only

The **pre-verified fact #3** in the brief ("unauthenticated requests get 403, not 401") turned out to be **incorrect in practice**: `ResponseTrait::isCurrentEmployeeHasPermission()` does `$employee_info_id = auth()->user()->employee_info_id;` with **no null check**. Since these routes have no `auth:api` middleware, a truly unauthenticated (guest) request reaches the controller with `auth()->user() === null`, causing `ErrorException: Trying to get property 'employee_info_id' of non-object` → **HTTP 500**, not 403. Reproduced this directly in a first test-writing attempt.

This is a latent bug in the **shared** `ResponseTrait` (used across many controllers, not something introduced by this task), and `ResponseTrait.php` is **not** in the list of files I'm allowed to touch for Task 6, so I did not fix it. Instead I adjusted my "fail-closed guard" test to authenticate a real employee **without** the permission (rather than a true guest) so it correctly exercises the 403 path without tripping the pre-existing null-safety gap. Flagging this for the controller/reviewer to decide whether a separate fix task is warranted (e.g. null-check + `abort(401)` in `isCurrentEmployeeHasPermission`, or requiring `auth:api` middleware on these routes).

## Test path taken

**Both the brief's authenticated-200 flow AND the 403-guard test were achieved as real, unmocked, green tests** (no `markTestSkipped` needed) — better than the "expected infeasible" fallback anticipated in the task instructions.

Steps to make the authenticated flow work:
1. `config('auth.guards.api')` uses driver `jwt`, provider `users` → model `App\Models\TpEmployee`, table `employees`.
2. `Modules\Timesheet\Entities\Employee` (used internally by `isCurrentEmployeeHasPermission`) is a **different model class over the same `employees` table**.
3. Created one raw row in `employees` via `DB::table('employees')->insertGetId(...)`, then:
   - `actingAs(\App\Models\TpEmployee::find($id), 'api')` to satisfy the auth guard.
   - Granting `'Cài đặt cấu hình'` directly required a workaround: calling `Employee::givePermissionTo()` throws `Spatie\Permission\Exceptions\GuardDoesNotMatch` because `Modules\Timesheet\Entities\Employee`'s class doesn't match the `auth.providers.users.model` (`App\Models\TpEmployee`), so spatie's guard-name inference (`Guard::getNames()`) resolves to an **empty** collection for that class → any permission assignment attempt is rejected. Worked around by inserting directly into the `employee_has_permissions` pivot table (bypasses spatie's guard validation; `isCurrentEmployeeHasPermission` only reads via `getAllPermissions()`, which does not validate guard).
4. Confirmed `config('permission.teams') === false`, so no `company_id`/team scoping needed for the pivot row (default `company_id` isn't even a column on this pivot table).

Result:
- `test_api_creates_pending_version_and_returns_config` — **exact brief scenario**: authenticated employee with the real permission, POST creates a pending version, asserts `data.config.pending.0.diff_snapshot.0.key === 'interest_rate'`, then GET asserts `data.fields` has 7 entries. Full 200 flow, no mocking of the gate.
- `test_api_routes_registered_and_permission_guard_fails_closed_without_auth` — authenticated employee **without** the permission, asserts 403 on all 4 endpoints (GET/POST/PUT/DELETE), proving both route registration under the correct prefix and fail-closed guard behavior.

All 5 pre-existing service tests are untouched and still pass.

## Test command + actual output

```
cd /Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api
vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
```

```
PHPUnit 9.5.26 by Sebastian Bergmann and contributors.

.......                                                             7 / 7 (100%)

Time: 00:03.524, Memory: 64.50 MB

OK (7 tests, 38 assertions)
```

## Route confirmation

`php artisan route:list --path=master-data` **fails in this environment** with an unrelated pre-existing error:
```
ErrorException: Trying to get property 'employee_info_id' of non-object
  at app/Helper/PermissionHelper.php:23
  ... isCurrentEmployeeHasPermission("Xem danh sách đề nghị tra soát công - tổng công ty")
  ... Modules/Timesheet/Http/Controllers/Api/V1/RequestUpdateTimeSheetController.php:51
```
This is triggered during route-list's route collection/boot by a completely different module/controller (Timesheet), not by anything in this task, and not fixable within Task 6's allowed files.

Used an equivalent tinker check instead to confirm registration:
```php
php artisan tinker --execute="
foreach (app('router')->getRoutes() as \$r) {
    if (strpos(\$r->uri(), 'master-data/regulation-config') !== false) {
        echo implode('|', \$r->methods()) . ' ' . \$r->uri() . ' -> ' . \$r->getActionName() . PHP_EOL;
    }
}
"
```
Output:
```
GET|HEAD api/v1/master-data/regulation-config/congno -> Modules\MasterData\Http\Controllers\V1\RegulationConfigController@showCongno
POST api/v1/master-data/regulation-config/congno/versions -> Modules\MasterData\Http\Controllers\V1\RegulationConfigController@store
PUT api/v1/master-data/regulation-config/congno/versions/{id} -> Modules\MasterData\Http\Controllers\V1\RegulationConfigController@update
DELETE api/v1/master-data/regulation-config/congno/versions/{id} -> Modules\MasterData\Http\Controllers\V1\RegulationConfigController@cancel
```
All 4 routes registered correctly under the expected controller/namespace.

## Confirmation

- Only allowed files touched (verified via `git status --short`): the 4 Task 6 files + `design.md`.
- No `git add` / `git commit` was run — changes left uncommitted per the no-commit rule.
