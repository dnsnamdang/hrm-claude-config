# Optimize getAll API khi tạo Task/Issue từ màn Manager

**Ngày:** 2026-05-11
**Người phụ trách:** @dnsnamdang

## Mục tiêu

Khi tạo task/issue từ các màn quản lý giải pháp, hạng mục, dự án — các API `getAll` cho solutions và prospective-projects hiện load toàn bộ danh sách (per_page=10000). Tối ưu bằng cách truyền `id` filter từ FE xuống BE, chỉ trả về bản ghi tương ứng.

## Scope

| Màn | URL mẫu | Context truyền xuống modal |
|-----|---------|---------------------------|
| Quản lý giải pháp | `/assign/solutions/:id/manager` | `solution_id`, `project_id` |
| Quản lý hạng mục | `/assign/solution-modules/:id/manager` | `solution_id`, `solution_module_id`, `project_id` |
| Quản lý dự án | `/assign/prospective-projects/:id/manager` | `project_id` |

## Thiết kế chi tiết

### 1. Backend — Thêm filter `id` vào getAll

**File:** `Modules/Assign/Services/ProspectiveProjectService.php` — method `getAll()` (line ~156)

Thêm filter:
```php
if (isset($request->id)) {
    $query->where('prospective_projects.id', $request->id);
}
```

Vị trí: sau dòng `->where('status', '!=', 1);`, trước block `forRequestSolution`.

---

**File:** `Modules/Assign/Services/SolutionService.php` — method `getAll()` (line ~147)

Thêm filter:
```php
if (isset($request->id)) {
    $query->where('solutions.id', $request->id);
}
```

Vị trí: sau dòng `->whereNotIn('status', [...]);`, trước các block filter khác.

---

### 2. Frontend — CreateTaskModal.vue

**File:** `pages/assign/tasks/components/CreateTaskModal.vue`

#### 2a. Truyền `id` param khi gọi API

**`getProjectOptions()` (line ~2188):**
- Hiện tại: `'assign/prospective-projects/getAll?per_page=10000'`
- Sửa: nếu `this.pendingDefaults?.project_id` tồn tại → append `&id=${project_id}`

**`getSolutionOptions()` (line ~2223):**
- Hiện tại: `'assign/solutions/getAll?per_page=10000'`
- Sửa: nếu `this.pendingDefaults?.solution_id` tồn tại → append `&id=${solution_id}`

#### 2b. Lock select khi có defaults từ màn cha

Thêm data property `lockFromParent` (default `false`), set `true` khi `create(defaults)` được gọi với `solution_id` hoặc `project_id`.

Disable các V2BaseSelect:
- Select giải pháp: `:disabled="lockFromParent && !!form.solution_id"`
- Select dự án: `:disabled="lockFromParent && !!form.project_id"`
- Select hạng mục: `:disabled="lockFromParent && !!form.solution_module_id"`

Reset `lockFromParent = false` khi modal đóng (để khi mở từ nơi khác không bị lock).

---

### 3. Frontend — CreateIssueModal.vue

**File:** `pages/assign/issues/components/CreateIssueModal.vue`

#### 3a. Truyền `id` param khi gọi API

**`fetchOptions()` (line ~1003):**
- API prospective-projects: nếu `this.initialData?.project_id` → append `&id=${project_id}`
- API solutions: nếu `this.initialData?.solution_id` → append `&id=${solution_id}`

#### 3b. Lock select dự án

Đã có sẵn `lockSolution` và `lockModule`. Thêm `lockProject`:
- Thêm data property `lockProject` (default `false`)
- Set `lockProject = true` trong method `open()` khi `initialData.lockProject === true`
- Select dự án: `:disabled="lockProject || lockSolution || isReadOnly"`
- Reset `lockProject = false` khi modal đóng

#### 3c. Cập nhật các nơi gọi `open()` từ màn manager

**Các file cần cập nhật thêm `lockProject: true`:**

| File | Method | Hiện tại | Thêm |
|------|--------|----------|------|
| `solutions/components/manager/IssueTab.vue` line ~617 | `createIssue()` | `lockSolution: true` | `lockProject: true` |
| `solution-modules/_id/components/IssueTab.vue` line ~558 | `createIssue()` | `lockSolution: true, lockModule: true` | `lockProject: true` |

**Màn prospective-projects manager** — cần kiểm tra xem có IssueTab không:
- Nếu có: thêm `lockProject: true` khi gọi `open()`
- TasksTab tương tự: truyền `lockFromParent` context

---

### 4. Cập nhật các TasksTab truyền thêm context

Các nơi gọi `createTask()` cần đảm bảo truyền đầy đủ defaults:

| File | Defaults hiện tại | Không cần sửa |
|------|-------------------|---------------|
| `solutions/components/manager/TasksTab.vue` line ~941 | `{ solution_id, project_id }` | OK, đã đủ |
| `solution-modules/_id/components/TasksTab.vue` line ~761 | `{ solution_id, solution_module_id, project_id }` | OK, đã đủ |
| `prospective-projects/_id/components/TasksTab.vue` | Cần kiểm tra | Có thể cần bổ sung |

## Backward Compatibility

- BE: các nơi gọi getAll KHÔNG truyền `id` → không bị ảnh hưởng (filter chỉ áp dụng khi `isset`)
- FE: các modal mở từ nơi KHÔNG có defaults → hoạt động như cũ (load toàn bộ, không lock)

## Không làm

- Không sửa logic filter status hiện có trong getAll
- Không sửa API `getAll` cho tasks (dù cũng gọi per_page=10000)
- Không thêm phân quyền mới
