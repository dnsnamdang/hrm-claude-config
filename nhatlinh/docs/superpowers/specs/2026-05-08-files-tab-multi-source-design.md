# Files Tab Multi-Source — Spec chi tiết

## Mục tiêu

Mở rộng tab Files trong quản lý giải pháp và quản lý hạng mục để hiển thị file từ 3 nguồn: **Task**, **Issue**, và **Hồ sơ trình duyệt (HSTD)**.

Hiện tại tab Files chỉ query `files WHERE table='tasks'`. Sau thay đổi, sẽ UNION thêm `table='issues'` và `table='solution_review_profiles'` / `table='solution_module_review_profiles'`.

---

## Scope

### Solutions Manager (`/assign/solutions/{id}/manager` → tab Files)

3 nguồn file:
1. **Task**: `files.table='tasks'` JOIN `tasks` WHERE `tasks.solution_id = $solution->id`
2. **Issue**: `files.table='issues'` JOIN `issues` WHERE `issues.solution_id = $solution->id`
3. **HSTD giải pháp**: `files.table='solution_review_profiles'` JOIN `solution_review_profiles` WHERE `solution_review_profiles.solution_id = $solution->id`

### Module Manager (`/assign/solution-modules/{id}/manager` → tab Files)

3 nguồn file:
1. **Task**: `files.table='tasks'` JOIN `tasks` WHERE `tasks.solution_module_id = $module->id`
2. **Issue**: `files.table='issues'` JOIN `issues` WHERE `issues.module_id = $module->id`
3. **HSTD hạng mục**: `files.table='solution_module_review_profiles'` JOIN `solution_module_review_profiles` WHERE `solution_module_review_profiles.solution_module_id = $module->id`

---

## Backend

### 1. Query UNION ALL

Thay đổi method `getFileListForSolution()` trong `SolutionService` và `getFileListForModule()` trong `SolutionModuleService`.

Mỗi method sẽ build 3 sub-query với cùng format cột, rồi UNION ALL:

**Cột chung cho mỗi sub-query:**

| Cột | Mô tả |
|-----|-------|
| `files.id` | ID file |
| `files.name` | Tên tài liệu |
| `files.file_name` | Tên file gốc |
| `files.file_path` | Đường dẫn file |
| `files.file_size` | Dung lượng |
| `files.created_at` | Ngày tạo |
| `files.created_by` | Người tạo (ID) |
| `files.attachment_type_id` | Nhóm tài liệu (ID) |
| `attachment_types.name as attachment_type_name` | Tên nhóm tài liệu |
| `source` | Giá trị cố định: `'task'`, `'issue'`, `'review_profile'` |
| `linked_id` | ID entity liên kết (task.id / issue.id / profile.id) |
| `linked_code` | Mã entity (task.code / issue.code / profile.code) |
| `linked_name` | Tên entity (task.title / issue.title / profile.name) |
| `module_id` | ID hạng mục (nullable) |
| `module_name` | Tên hạng mục (nullable) |
| `version` | Version (dynamic, giữ logic hiện tại) |
| `status` | Trạng thái (dynamic, giữ logic hiện tại) |

**Sub-query 1 — Task** (giữ nguyên logic hiện tại):
```sql
SELECT files.*, 'task' as source,
  tasks.id as linked_id, tasks.code as linked_code, tasks.title as linked_name,
  solution_modules.id as module_id, solution_modules.project_item_name as module_name,
  attachment_types.name as attachment_type_name
FROM files
JOIN tasks ON tasks.id = files.table_id
LEFT JOIN solution_modules ON solution_modules.id = tasks.solution_module_id
LEFT JOIN attachment_types ON attachment_types.id = files.attachment_type_id
WHERE files.table = 'tasks' AND tasks.solution_id = ?
```

**Sub-query 2 — Issue:**
```sql
SELECT files.*, 'issue' as source,
  issues.id as linked_id, issues.code as linked_code, issues.title as linked_name,
  solution_modules.id as module_id, solution_modules.project_item_name as module_name,
  attachment_types.name as attachment_type_name
FROM files
JOIN issues ON issues.id = files.table_id
LEFT JOIN solution_modules ON solution_modules.id = issues.module_id
LEFT JOIN attachment_types ON attachment_types.id = files.attachment_type_id
WHERE files.table = 'issues' AND issues.solution_id = ?
```

**Sub-query 3 — HSTD giải pháp:**
```sql
SELECT files.*, 'review_profile' as source,
  solution_review_profiles.id as linked_id,
  solution_review_profiles.code as linked_code,
  solution_review_profiles.name as linked_name,
  NULL as module_id, NULL as module_name,
  attachment_types.name as attachment_type_name
FROM files
JOIN solution_review_profiles ON solution_review_profiles.id = files.table_id
LEFT JOIN attachment_types ON attachment_types.id = files.attachment_type_id
WHERE files.table = 'solution_review_profiles'
  AND solution_review_profiles.solution_id = ?
```

**Sub-query 3 (Module Manager) — HSTD hạng mục:**
```sql
SELECT files.*, 'review_profile' as source,
  solution_module_review_profiles.id as linked_id,
  solution_module_review_profiles.code as linked_code,
  solution_module_review_profiles.name as linked_name,
  NULL as module_id, NULL as module_name,
  attachment_types.name as attachment_type_name
FROM files
JOIN solution_module_review_profiles ON solution_module_review_profiles.id = files.table_id
LEFT JOIN attachment_types ON attachment_types.id = files.attachment_type_id
WHERE files.table = 'solution_module_review_profiles'
  AND solution_module_review_profiles.solution_module_id = ?
```

**Implementation pattern:**
Dùng `DB::table(DB::raw("({$q1} UNION ALL {$q2} UNION ALL {$q3}) as combined_files"))` để wrap, sau đó áp filter + sort + paginate trên subquery.

Hoặc dùng Eloquent `unionAll()`:
```php
$taskQuery = $this->buildTaskFileQuery($solution);
$issueQuery = $this->buildIssueFileQuery($solution);
$reviewQuery = $this->buildReviewProfileFileQuery($solution);

$unionQuery = $taskQuery->unionAll($issueQuery)->unionAll($reviewQuery);
```

### 2. Filter mở rộng

**Filter `source` (mới):**
- Nếu `$request->source` được truyền, chỉ build sub-query tương ứng thay vì UNION cả 3.
- Giá trị: `'task'`, `'issue'`, `'review_profile'`

**Filter `keyword`:**
- Mỗi sub-query tự áp `WHERE ... LIKE` trên các cột phù hợp trước khi UNION.
- Task: `files.name, files.file_name, tasks.code, tasks.title, solution_modules.project_item_name, attachment_types.name`
- Issue: `files.name, files.file_name, issues.code, issues.title, solution_modules.project_item_name, attachment_types.name`
- HSTD: `files.name, files.file_name, solution_review_profiles.code, solution_review_profiles.name, attachment_types.name`

**Filter `attachment_type_id`, `solution_module_id`, `version`, `status`, `created_by`:** Áp trên mỗi sub-query trước khi UNION (giữ nguyên logic hiện tại).

Lưu ý: `solution_module_id` filter:
- Với nguồn Task: `tasks.solution_module_id = ?`
- Với nguồn Issue: `issues.module_id = ?`
- Với nguồn HSTD: HSTD giải pháp không thuộc module → loại bỏ khỏi kết quả khi filter module

### 3. Resource — SolutionManagerFileResource

Cập nhật `toArray()`:

```php
return [
    'id' => $this->id,
    'name' => $this->name,
    'category' => $this->attachment_type_name ?: '—',
    'category_id' => $this->attachment_type_id,
    'module' => $this->module_name ?: '—',
    'module_id' => $this->module_id,
    'version' => $this->version ?? '—',
    'source' => $this->source,               // MỚI: 'task', 'issue', 'review_profile'
    'linked_name' => $this->linked_name       // MỚI: thay thế 'task'
        ?: ($this->linked_code ?: '—'),
    'linked_id' => $this->linked_id,          // MỚI: thay thế 'task_id'
    'creator' => $this->creator?->info?->fullname ?: '—',
    'creator_id' => $this->created_by,
    'created_at' => Helper::formatDateTime($this->created_at) ?: '—',
    'status' => $this->status ?? '—',
    'size' => $this->file_size ?: '—',
    'file_name' => $this->file_name,
    'file_path' => $this->file_path,
];
```

Lưu ý: Creator loading. Vì dùng raw UNION query, `with(['creator.info'])` không hoạt động trực tiếp. Cần manual load creator sau khi paginate, hoặc join thẳng vào employee table trong query.

---

## Frontend

### 1. Cả 2 FilesTab (Solutions + Module)

**Thêm filter "Nguồn":**
```vue
<V2BaseSelect
  v-model="filters.source"
  :options="sourceOptions"
  placeholder="Tất cả nguồn"
  :clearable="true"
/>
```

```js
sourceOptions: [
  { id: 'task', name: 'Task' },
  { id: 'issue', name: 'Issue' },
  { id: 'review_profile', name: 'Hồ sơ trình duyệt' },
]
```

**Thêm cột "Nguồn" vào bảng:**
```js
{
  key: 'source',
  label: 'Nguồn',
  // Render bằng V2BaseBadge
}
```

Hiển thị bằng `V2BaseBadge` với mapping màu:
```js
sourceDisplay: {
  task: { text: 'Task', color: '#3B82F6' },        // xanh dương
  issue: { text: 'Issue', color: '#EF4444' },       // đỏ
  review_profile: { text: 'HSTD', color: '#10B981' } // xanh lá
}
```

**Đổi cột "Task" → "Liên kết":**
- Key: `linked_name`
- Label: `Liên kết`
- Hiển thị: `item.linked_name` (tên/mã của task, issue, hoặc profile)

**Cập nhật `filters`:**
```js
filters: {
  keyword: undefined,
  source: undefined,           // MỚI
  attachment_type_id: undefined,
  solution_module_id: undefined,  // chỉ Solutions FilesTab
  version: undefined,
  status: undefined,
  created_by: undefined,
  sort_field: 'created_at',
  sort_dir: 'desc',
}
```

**handleReset:** Reset thêm `filters.source = undefined`.

### 2. Vị trí cột "Nguồn" trong bảng

Đặt sau cột "File" (file_name), trước cột "Nhóm tài liệu" (category):

STT | Tên tài liệu | File | **Nguồn** | Nhóm tài liệu | Hạng mục | Version | Liên kết | Người tạo | Ngày tạo | Trạng thái | Dung lượng | Thao tác

---

## Edge Cases

1. **HSTD không có `attachment_type_id`**: Nếu HSTD không lưu attachment_type_id, cột "Nhóm tài liệu" hiển thị "—".
2. **HSTD giải pháp không thuộc module**: Cột "Hạng mục" hiển thị "—".
3. **Filter module + source=review_profile (Solutions)**: HSTD giải pháp không thuộc module → không trả kết quả khi cả 2 filter cùng active.
4. **Creator loading**: Vì UNION query là raw SQL, cần join `employees` + `employee_infos` trực tiếp hoặc manual load sau paginate.

---

## Files thay đổi

### Backend
- `Modules/Assign/Services/SolutionService.php` — refactor `getFileListForSolution()`
- `Modules/Assign/Services/SolutionModuleService.php` — refactor `getFileListForModule()`
- `Modules/Assign/Transformers/FileResource/SolutionManagerFileResource.php` — thêm `source`, đổi `task` → `linked_name`

### Frontend
- `pages/assign/solutions/components/manager/FilesTab.vue` — thêm filter source, thêm cột Nguồn, đổi cột Task → Liên kết
- `pages/assign/solution-modules/_id/components/FilesTab.vue` — tương tự

---

## Không làm

- Không thêm HSTD hạng mục vào trang Solutions Manager (chỉ HSTD giải pháp)
- Không migration, không tạo bảng mới
- Không thay đổi cách upload file
- Không thay đổi file preview/download logic
