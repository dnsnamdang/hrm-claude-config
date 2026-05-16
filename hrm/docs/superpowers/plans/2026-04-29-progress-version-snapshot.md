# Progress Version Snapshot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Snapshot weight + progress_percent vào bản ghi version cũ khi tạo version mới, reset progress về 0 cho version mới, và filter hạng mục theo version giải pháp hiện tại ở tab Tiến độ.

**Architecture:** 2 migration thêm cột snapshot vào bảng version. BE thêm logic snapshot-then-reset vào 2 `createNewVersion`. Filter modules trong `getProgressByModules` qua `solution_module_versions.solution_version_id`. Không thay đổi FE.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL

---

## File Map

| File | Thay đổi |
|---|---|
| `hrm-api/database/migrations/2026_04_29_000001_add_progress_percent_to_solution_versions.php` | Tạo mới |
| `hrm-api/database/migrations/2026_04_29_000002_add_snapshot_columns_to_solution_module_versions.php` | Tạo mới |
| `hrm-api/Modules/Assign/Services/SolutionModuleService.php:1024-1058` | Sửa `createNewVersion` |
| `hrm-api/Modules/Assign/Services/SolutionService.php:2167-2208` | Sửa `createNewVersion` |
| `hrm-api/Modules/Assign/Services/SolutionService.php:2244-2274` | Sửa `getProgressByModules` |

---

## Task 1: Migration — thêm `progress_percent` vào `solution_versions`

**Files:**
- Tạo: `hrm-api/database/migrations/2026_04_29_000001_add_progress_percent_to_solution_versions.php`

- [ ] **Bước 1: Tạo file migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddProgressPercentToSolutionVersions extends Migration
{
    public function up()
    {
        Schema::table('solution_versions', function (Blueprint $table) {
            $table->unsignedTinyInteger('progress_percent')->default(0)->after('completion_date')
                ->comment('Snapshot tiến độ tổng hợp (%) tại thời điểm tạo version mới');
        });
    }

    public function down()
    {
        Schema::table('solution_versions', function (Blueprint $table) {
            $table->dropColumn('progress_percent');
        });
    }
}
```

- [ ] **Bước 2: Chạy migration**

```bash
cd hrm-api && php artisan migrate
```

Kết quả mong đợi: `Migrating: 2026_04_29_000001_add_progress_percent_to_solution_versions` → `Migrated`

- [ ] **Bước 3: Kiểm tra cột tồn tại**

```bash
php artisan tinker --execute="echo Schema::hasColumn('solution_versions', 'progress_percent') ? 'OK' : 'FAIL';"
```

Kết quả mong đợi: `OK`

---

## Task 2: Migration — thêm `weight` + `progress_percent` vào `solution_module_versions`

**Files:**
- Tạo: `hrm-api/database/migrations/2026_04_29_000002_add_snapshot_columns_to_solution_module_versions.php`

- [ ] **Bước 1: Tạo file migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddSnapshotColumnsToSolutionModuleVersions extends Migration
{
    public function up()
    {
        Schema::table('solution_module_versions', function (Blueprint $table) {
            $table->unsignedTinyInteger('weight')->default(0)->after('completion_date')
                ->comment('Snapshot trọng số hạng mục tại thời điểm tạo version mới');
            $table->unsignedTinyInteger('progress_percent')->default(0)->after('weight')
                ->comment('Snapshot tiến độ hạng mục (%) tại thời điểm tạo version mới');
        });
    }

    public function down()
    {
        Schema::table('solution_module_versions', function (Blueprint $table) {
            $table->dropColumn(['weight', 'progress_percent']);
        });
    }
}
```

- [ ] **Bước 2: Chạy migration**

```bash
php artisan migrate
```

Kết quả mong đợi: `Migrating: 2026_04_29_000002_add_snapshot_columns_to_solution_module_versions` → `Migrated`

- [ ] **Bước 3: Kiểm tra cột tồn tại**

```bash
php artisan tinker --execute="echo (Schema::hasColumn('solution_module_versions', 'weight') && Schema::hasColumn('solution_module_versions', 'progress_percent')) ? 'OK' : 'FAIL';"
```

Kết quả mong đợi: `OK`

---

## Task 3: SolutionModuleService — snapshot + reset khi tạo version mới

**Files:**
- Sửa: `hrm-api/Modules/Assign/Services/SolutionModuleService.php:1034`

- [ ] **Bước 1: Thêm snapshot + reset vào `createNewVersion`**

Mở file `Modules/Assign/Services/SolutionModuleService.php`, tìm hàm `createNewVersion` (dòng 1024). Thêm đoạn snapshot ngay trước `SolutionModuleVersion::create([...])` (dòng 1035):

```php
public function createNewVersion(Request $request, SolutionModule $solutionModule)
{
    $currentVersionCode = $solutionModule->current_version_code ?? 0;
    $newCode = $currentVersionCode + 1;

    // Chuyển hồ sơ trình duyệt đã duyệt của version hiện tại sang "Hết hiệu lực"
    SolutionModuleReviewProfile::where('solution_module_id', $solutionModule->id)
        // ->where('module_version_id', $solutionModule->current_version_id)
        ->where('status', SolutionModuleReviewProfile::STATUS_APPROVED)
        ->update(['status' => SolutionModuleReviewProfile::STATUS_EXPIRED]);

    // Snapshot weight + progress version cũ trước khi tạo version mới
    if ($solutionModule->current_version_id) {
        SolutionModuleVersion::where('id', $solutionModule->current_version_id)->update([
            'weight'           => $solutionModule->weight ?? 0,
            'progress_percent' => $solutionModule->progress_percent ?? 0,
        ]);
    }

    // Reset progress về 0 — version mới chưa có task nào
    $solutionModule->update(['progress_percent' => 0]);

    $version = SolutionModuleVersion::create([
        'solution_module_id' => $solutionModule->id,
        'solution_version_id' => $solutionModule->solution->current_version_id,
        'code' => $newCode,
        'description' => $request->input('description'),
        'start_date' => now()->toDateString(),
        'end_date' => $request->input('end_date'),
        'status' => $solutionModule->status,
        'completion_date' => null,
        'created_by' => auth()->id(),
    ]);

    $solutionModule->update([
        'current_version_id' => $version->id,
        'current_version_code' => $newCode,
    ]);

    $solutionModule->update([
        'status' => SolutionModule::STATUS_DA_DUYET,
    ]);

    return $version;
}
```

- [ ] **Bước 2: Kiểm tra thủ công**

1. Mở 1 hạng mục đang có `progress_percent > 0` và `weight > 0`
2. Vào tab Tiến độ → ghi nhớ giá trị progress hiện tại (VD: 65%) và weight
3. Tạo version mới cho hạng mục đó
4. Kiểm tra DB: `solution_module_versions` record của version CŨ phải có `weight` và `progress_percent` đúng với giá trị đã ghi nhớ
5. Kiểm tra `solution_modules.progress_percent` của hạng mục đó = 0

```bash
php artisan tinker --execute="
\$m = \Modules\Assign\Entities\SolutionModule::find(<id>);
echo 'progress_percent: ' . \$m->progress_percent . PHP_EOL;
\$v = \Modules\Assign\Entities\SolutionModuleVersion::where('solution_module_id', <id>)->orderBy('id','desc')->skip(1)->first();
echo 'snapshot weight: ' . \$v->weight . ' progress: ' . \$v->progress_percent . PHP_EOL;
"
```

---

## Task 4: SolutionService — snapshot + reset khi tạo version giải pháp mới

**Files:**
- Sửa: `hrm-api/Modules/Assign/Services/SolutionService.php:2172-2175`

- [ ] **Bước 1: Thêm snapshot + reset vào `createNewVersion`**

Mở file `Modules/Assign/Services/SolutionService.php`, tìm hàm `createNewVersion` (dòng 2167). Thêm đoạn snapshot sau `snapshotVersionMembers` (dòng 2175), trước `SolutionReviewProfile::where(...)`:

```php
public function createNewVersion(Request $request, Solution $solution)
{
    $currentVersionCode = $solution->current_version_code ?? 0;
    $newCode = $currentVersionCode + 1;

    // Snapshot members cho version hiện tại trước khi tạo version mới
    if ($solution->current_version_id) {
        $this->snapshotVersionMembers($solution, $solution->current_version_id);
    }

    // Snapshot progress version cũ
    if ($solution->current_version_id) {
        SolutionVersion::where('id', $solution->current_version_id)->update([
            'progress_percent' => $solution->progress_percent ?? 0,
        ]);
    }

    // Reset progress về 0 — version mới chưa có task/hạng mục nào
    $solution->update(['progress_percent' => 0]);

    // Chuyển hồ sơ trình duyệt đã duyệt của version hiện tại sang "Hết hiệu lực"
    SolutionReviewProfile::where('solution_id', $solution->id)
        // ->where('solution_version_id', $solution->current_version_id)
        ->where('status', SolutionReviewProfile::STATUS_APPROVED)
        ->update(['status' => SolutionReviewProfile::STATUS_EXPIRED]);

    $version = SolutionVersion::create([
        'solution_id' => $solution->id,
        'code' => $newCode,
        'description' => $request->input('description'),
        'start_date' => now()->toDateString(),
        'end_date' => $request->input('end_date'),
        'status' => $solution->status,
        'completion_date' => null,
        'created_by' => auth()->user()->id,
    ]);

    // Cập nhật current version, end_date và status cho solution
    $solution->update([
        'current_version_id' => $version->id,
        'current_version_code' => $newCode,
        'end_date' => $request->input('end_date'),
        'status' => Solution::STATUS_DANG_TRIEN_KHAI,
    ]);

    // Đồng bộ trạng thái dự án tiền khả thi về "Đang làm giải pháp"
    if ($solution->prospective_project_id) {
        app(ProspectiveProjectService::class)->syncStatusBySolution($solution->prospective_project_id);
    }

    return $version;
}
```

- [ ] **Bước 2: Kiểm tra thủ công**

1. Mở 1 giải pháp đang có `progress_percent > 0`
2. Ghi nhớ giá trị progress (VD: 40%)
3. Tạo version mới cho giải pháp đó
4. Kiểm tra DB:

```bash
php artisan tinker --execute="
\$s = \Modules\Assign\Entities\Solution::find(<id>);
echo 'progress_percent hiện tại: ' . \$s->progress_percent . PHP_EOL;
\$v = \Modules\Assign\Entities\SolutionVersion::where('solution_id', <id>)->orderBy('id','desc')->skip(1)->first();
echo 'snapshot progress: ' . \$v->progress_percent . PHP_EOL;
"
```

Kết quả mong đợi: `progress_percent hiện tại: 0`, `snapshot progress: <giá trị cũ>`

---

## Task 5: SolutionService — filter hạng mục theo version giải pháp hiện tại

**Files:**
- Sửa: `hrm-api/Modules/Assign/Services/SolutionService.php:2244-2274`

- [ ] **Bước 1: Sửa `getProgressByModules`**

Thay toàn bộ hàm `getProgressByModules` (dòng 2244-2274):

```php
private function getProgressByModules(Solution $solution, $modules)
{
    // Filter theo version giải pháp hiện tại (nếu có)
    if ($solution->current_version_id) {
        $moduleIdsInCurrentVersion = SolutionModuleVersion::where(
            'solution_version_id', $solution->current_version_id
        )->pluck('solution_module_id');

        $modules = $modules->whereIn('id', $moduleIdsInCurrentVersion);
    }

    $modules->load(['leader.info', 'tasks']);

    $items = $modules->map(function ($module) {
        $leader = $module->leader;
        $leadName = $leader && $leader->info ? $leader->info->fullname : null;

        return [
            'id' => $module->id,
            'code' => $module->code ?: '',
            'name' => $module->project_item_name,
            'leader_name' => $leadName,
            'due_date' => $module->due_date ? Carbon::parse($module->due_date)->format('d/m/Y') : null,
            'version' => SolutionModule::formatVersionCode($module->current_version_code) ?? '—',
            'weight' => $module->weight ?? 0,
            'progress_percent' => $module->progress_percent ?? 0,
            'status' => $module->status,
            'status_text' => SolutionModule::getStatusName($module->status),
            'status_color' => SolutionModule::getStatusColor($module->status),
        ];
    })->values()->toArray();

    $totalWeight = collect($items)->sum('weight');

    return [
        'mode' => 'module',
        'items' => $items,
        'total_weight' => $totalWeight,
    ];
}
```

- [ ] **Bước 2: Kiểm tra thủ công**

Kịch bản A — giải pháp V2, có hạng mục tạo version gắn V2:
1. Mở giải pháp đang ở V2
2. Vào tab Tiến độ → chỉ hiện hạng mục có `solution_module_versions.solution_version_id = V2_id`
3. Hạng mục chưa tạo version mới kể từ V1 → không hiển thị

Kịch bản B — giải pháp chưa có version (`current_version_id = null`):
1. Tab Tiến độ vẫn hiển thị tất cả hạng mục (fallback do guard `if ($solution->current_version_id)`)

Kịch bản C — gọi API trực tiếp:
```bash
curl -H "Authorization: Bearer <token>" \
  http://127.0.0.1:8000/api/v1/assign/solutions/<id>/manager/progress
```
Kết quả: `mode: "module"`, `items` chỉ chứa hạng mục thuộc version hiện tại.

---

## Checklist cuối

- [ ] 2 migration đã chạy thành công
- [ ] Tạo version mới cho hạng mục → `solution_module_versions` record cũ có `weight` + `progress_percent` đúng, `solution_modules.progress_percent` về 0
- [ ] Tạo version mới cho giải pháp → `solution_versions` record cũ có `progress_percent` đúng, `solutions.progress_percent` về 0
- [ ] Tab Tiến độ giải pháp có hạng mục → chỉ hiện hạng mục thuộc version giải pháp hiện tại
- [ ] Tab Tiến độ giải pháp không có hạng mục → không thay đổi (vẫn filter theo `solution_version_id`)
- [ ] Tab Tiến độ hạng mục → không thay đổi (vẫn filter theo `module_version_id`)
