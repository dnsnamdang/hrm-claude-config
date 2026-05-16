# Progress Version Snapshot — Design Spec

**Ngày:** 2026-04-29
**Module:** Assign (Giao việc)
**Phạm vi:** Giải pháp + Hạng mục

---

## Mục tiêu

1. Snapshot `weight` và `progress_percent` của version cũ vào bản ghi version tương ứng khi tạo version mới (lưu lịch sử, không hiển thị UI).
2. Tab Tiến độ của giải pháp có hạng mục chỉ hiển thị các hạng mục thuộc version giải pháp hiện tại (dựa vào `solution_module_versions.solution_version_id`).
3. Tab Tiến độ của giải pháp không có hạng mục và của hạng mục đã filter đúng theo version — **không cần thay đổi**.

---

## DB Schema

### Migration 1 — Thêm cột snapshot vào `solution_versions`

```sql
ALTER TABLE solution_versions
    ADD COLUMN progress_percent TINYINT UNSIGNED NOT NULL DEFAULT 0
        COMMENT 'Snapshot tiến độ tổng hợp (%) tại thời điểm tạo version mới';
```

### Migration 2 — Thêm cột snapshot vào `solution_module_versions`

```sql
ALTER TABLE solution_module_versions
    ADD COLUMN weight           TINYINT UNSIGNED NOT NULL DEFAULT 0
        COMMENT 'Snapshot trọng số hạng mục tại thời điểm tạo version mới',
    ADD COLUMN progress_percent TINYINT UNSIGNED NOT NULL DEFAULT 0
        COMMENT 'Snapshot tiến độ hạng mục (%) tại thời điểm tạo version mới';
```

**Lưu ý:**
- `solution_module_versions` đã có sẵn `solution_version_id` (migration `2026_04_07_100000`).
- Không tạo bảng mới.
- Các cột snapshot chỉ để lưu lịch sử, không ảnh hưởng logic đọc/ghi hiện tại.

---

## Backend Changes

### 1. `SolutionModuleService::createNewVersion`

**File:** `Modules/Assign/Services/SolutionModuleService.php`

Trước khi tạo record version mới: snapshot version cũ, sau đó reset progress về 0:

```php
// Snapshot version cũ
if ($solutionModule->current_version_id) {
    SolutionModuleVersion::where('id', $solutionModule->current_version_id)->update([
        'weight'           => $solutionModule->weight ?? 0,
        'progress_percent' => $solutionModule->progress_percent ?? 0,
    ]);
}

// Reset progress về 0 — version mới chưa có task nào
$solutionModule->update(['progress_percent' => 0]);
```

Vị trí: thêm ngay trước dòng `SolutionModuleVersion::create([...])`.

---

### 2. `SolutionService::createNewVersion`

**File:** `Modules/Assign/Services/SolutionService.php`

Trước khi tạo record version mới: snapshot version cũ, sau đó reset progress về 0:

```php
// Snapshot progress version cũ
if ($solution->current_version_id) {
    SolutionVersion::where('id', $solution->current_version_id)->update([
        'progress_percent' => $solution->progress_percent ?? 0,
    ]);
}

// Reset progress về 0 — version mới chưa có task/hạng mục nào
$solution->update(['progress_percent' => 0]);
```

Vị trí: thêm sau đoạn `snapshotVersionMembers` hiện có (dòng ~2173), trước `SolutionVersion::create([...])`.

---

### 3. `SolutionService::getProgressByModules`

**File:** `Modules/Assign/Services/SolutionService.php`

**Hiện tại:** Lấy tất cả modules của solution không filter theo version.

**Sau thay đổi:** Chỉ lấy modules có `solution_module_versions` record với `solution_version_id = current_version_id`.

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
    // ... phần còn lại giữ nguyên
}
```

---

## Business Rules

| Rule | Mô tả |
|---|---|
| Snapshot chỉ khi có version hiện tại | Nếu `current_version_id` null (chưa tạo version nào) thì bỏ qua snapshot |
| Snapshot 1 lần duy nhất | Khi tạo V(n+1), snapshot V(n). Không retroactively update version cũ hơn |
| Reset progress sau snapshot | Sau khi snapshot V(n), reset `progress_percent = 0` trên solution/module — version mới chưa có task/hạng mục nào |
| Filter hạng mục theo version | Hạng mục không có `solution_module_versions.solution_version_id = current_version_id` sẽ không hiển thị trong tab Tiến độ của giải pháp |
| Không thay đổi logic weight hiện tại | `solution_modules.weight` vẫn là nguồn chính để đọc/ghi trọng số |

---

## Edge Cases

| Tình huống | Xử lý |
|---|---|
| Giải pháp có hạng mục nhưng hạng mục chưa tạo version mới kể từ khi giải pháp lên V2 | Hạng mục đó không hiển thị trong tab Tiến độ V2 (user đã xác nhận — option a) |
| Tạo version đầu tiên (V1) — chưa có version cũ để snapshot | Skip snapshot, không có gì để lưu |
| `progress_percent` của solution/module = 0 tại thời điểm tạo version | Snapshot 0, hợp lệ |

---

## Files cần thay đổi

| File | Loại thay đổi |
|---|---|
| `database/migrations/2026_04_29_000001_add_progress_percent_to_solution_versions.php` | Tạo mới — migration 1 |
| `database/migrations/2026_04_29_000002_add_snapshot_columns_to_solution_module_versions.php` | Tạo mới — migration 2 |
| `Modules/Assign/Services/SolutionService.php` | Sửa `createNewVersion` + `getProgressByModules` |
| `Modules/Assign/Services/SolutionModuleService.php` | Sửa `createNewVersion` |

**Frontend:** Không cần thay đổi — snapshot là data lịch sử, không hiển thị UI. Filter modules theo version xử lý hoàn toàn ở BE.
