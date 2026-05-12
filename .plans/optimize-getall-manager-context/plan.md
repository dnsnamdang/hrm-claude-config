# Optimize getAll API khi tạo Task/Issue từ màn Manager — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Khi tạo task/issue từ màn manager, API getAll chỉ trả về bản ghi tương ứng thay vì toàn bộ danh sách. Lock select trong modal.

**Architecture:** FE truyền `id` param khi gọi getAll → BE filter `where('id', $request->id)`. Dùng lại cơ chế `lockedDefaults` (task modal) và `lockSolution`/`lockModule` (issue modal) để lock select.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2)

---

## Phase 1 — Backend

### Task 1: Thêm filter `id` vào ProspectiveProjectService::getAll

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/ProspectiveProjectService.php:188` (sau dòng `->where('status', '!=', 1);`)

- [ ] **Step 1: Thêm filter id**

Sau dòng `->where('status', '!=', 1);` (line 188), trước block `if (isset($request->forRequestSolution))`, thêm:

```php
if (isset($request->id)) {
    $query->where('prospective_projects.id', $request->id);
}
```

---

### Task 2: Thêm filter `id` vào SolutionService::getAll

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/SolutionService.php:170` (sau dòng `->whereNotIn('status', [...]);`)

- [ ] **Step 1: Thêm filter id**

Sau dòng `->whereNotIn('status', [Solution::STATUS_TAO_NHAP, Solution::STATUS_DONG]);` (line 170), trước block `if (isset($request->keyword))`, thêm:

```php
if (isset($request->id)) {
    $query->where('solutions.id', $request->id);
}
```

---

## Phase 2 — Frontend: CreateTaskModal

### Task 3: Truyền id param khi gọi getProjectOptions và getSolutionOptions

**Files:**
- Modify: `hrm-client/pages/assign/tasks/components/CreateTaskModal.vue`

- [ ] **Step 1: Sửa `getProjectOptions()` (line ~2192)**

Hiện tại:
```javascript
`assign/prospective-projects/getAll?per_page=10000`
```

Sửa thành:
```javascript
async getProjectOptions() {
    try {
        let url = 'assign/prospective-projects/getAll?per_page=10000'
        if (this.lockedDefaults?.project_id) {
            url += `&id=${this.lockedDefaults.project_id}`
        }
        const { data, meta } = await this.$store.dispatch(
            'apiGetMethod',
            url,
        )
        // ... phần còn lại giữ nguyên
```

Lưu ý: `lockedDefaults` đã được set trong `onShown()` TRƯỚC khi gọi `loadInitialOptions()` — KHÔNG ĐÚNG. Thực tế `onShown()` gọi `loadInitialOptions()` ở line 1856, rồi MỚI set `lockedDefaults` ở line 1862. Cần dùng `pendingDefaults` thay vì `lockedDefaults`.

Sửa lại đúng:
```javascript
async getProjectOptions() {
    try {
        let url = 'assign/prospective-projects/getAll?per_page=10000'
        if (this.pendingDefaults?.project_id) {
            url += `&id=${this.pendingDefaults.project_id}`
        }
        const { data, meta } = await this.$store.dispatch(
            'apiGetMethod',
            url,
        )
        // ... giữ nguyên phần map projectOptions
```

- [ ] **Step 2: Sửa `getSolutionOptions()` (line ~2227)**

Hiện tại:
```javascript
`assign/solutions/getAll?per_page=10000`
```

Sửa thành:
```javascript
async getSolutionOptions() {
    try {
        let url = 'assign/solutions/getAll?per_page=10000'
        if (this.pendingDefaults?.solution_id) {
            url += `&id=${this.pendingDefaults.solution_id}`
        }
        const { data, meta } = await this.$store.dispatch(
            'apiGetMethod',
            url,
        )
        // ... giữ nguyên phần filter + map solutionOptions + allSolutionModules
```

- [ ] **Step 3: Bỏ điều kiện cache `length === 0` trong `loadInitialOptions()`**

Hiện tại (line 1875-1880):
```javascript
async loadInitialOptions() {
    if (this.projectOptions.length === 0) await this.getProjectOptions()
    if (this.solutionOptions.length === 0) await this.getSolutionOptions()
    if (this.attachmentTypeOptions.length === 0) await this.getAttachmentTypeOptions()
}
```

Khi có `pendingDefaults`, cần gọi lại API với filter id dù đã có cache. Sửa:
```javascript
async loadInitialOptions() {
    const hasDefaults = !!this.pendingDefaults?.solution_id || !!this.pendingDefaults?.project_id
    if (this.projectOptions.length === 0 || hasDefaults) await this.getProjectOptions()
    if (this.solutionOptions.length === 0 || hasDefaults) await this.getSolutionOptions()
    if (this.attachmentTypeOptions.length === 0) await this.getAttachmentTypeOptions()
}
```

---

## Phase 3 — Frontend: CreateIssueModal

### Task 4: Truyền id param khi gọi fetchOptions + thêm lockProject

**Files:**
- Modify: `hrm-client/pages/assign/issues/components/CreateIssueModal.vue`

- [ ] **Step 1: Thêm data property `lockProject` (gần line 903)**

Tìm block khai báo `lockModule` và `lockSolution` trong data():
```javascript
lockModule: false,
lockSolution: false,
```

Thêm:
```javascript
lockModule: false,
lockSolution: false,
lockProject: false,
```

- [ ] **Step 2: Set `lockProject` trong method `open()` (line ~958)**

Hiện tại:
```javascript
this.lockModule = initialData.lockModule === true
this.lockSolution = initialData.lockSolution === true
```

Thêm:
```javascript
this.lockModule = initialData.lockModule === true
this.lockSolution = initialData.lockSolution === true
this.lockProject = initialData.lockProject === true
```

- [ ] **Step 3: Reset `lockProject` trong `resetForm()` (line ~997)**

Hiện tại:
```javascript
resetForm() {
    this.form = this.getInitialForm()
    this.errors = {}
    this.attachments = []
    this.pendingScrollCommentId = null
}
```

Thêm:
```javascript
resetForm() {
    this.form = this.getInitialForm()
    this.errors = {}
    this.attachments = []
    this.pendingScrollCommentId = null
    this.lockProject = false
    this.lockSolution = false
    this.lockModule = false
}
```

- [ ] **Step 4: Disable select dự án khi lockProject (template line ~95)**

Hiện tại:
```html
:disabled="lockSolution || isReadOnly"
```

Sửa:
```html
:disabled="lockProject || lockSolution || isReadOnly"
```

- [ ] **Step 5: Sửa `fetchOptions()` truyền id param (line ~1003)**

Hiện tại:
```javascript
const [projectsRes, solutionsRes, tasksRes] = await Promise.all([
    this.$store.dispatch('apiGetMethod', 'assign/prospective-projects/getAll?per_page=10000'),
    this.$store.dispatch('apiGetMethod', 'assign/solutions/getAll?per_page=10000'),
    this.$store.dispatch('apiGetMethod', 'assign/tasks/getAll'),
])
```

Sửa:
```javascript
let projectUrl = 'assign/prospective-projects/getAll?per_page=10000'
if (this.form.project_id) {
    projectUrl += `&id=${this.form.project_id}`
}
let solutionUrl = 'assign/solutions/getAll?per_page=10000'
if (this.form.solution_id) {
    solutionUrl += `&id=${this.form.solution_id}`
}
const [projectsRes, solutionsRes, tasksRes] = await Promise.all([
    this.$store.dispatch('apiGetMethod', projectUrl),
    this.$store.dispatch('apiGetMethod', solutionUrl),
    this.$store.dispatch('apiGetMethod', 'assign/tasks/getAll'),
])
```

Giải thích: `this.form` đã được gán `initialData` trước khi `fetchOptions()` chạy (trong `open()` line 966: `this.form = { ...this.getInitialForm(), ...initialData }`), nên `this.form.project_id` và `this.form.solution_id` đã có giá trị.

---

## Phase 4 — Frontend: Cập nhật nơi gọi modal truyền lockProject

### Task 5: Thêm lockProject vào IssueTab của Solution Manager

**Files:**
- Modify: `hrm-client/pages/assign/solutions/components/manager/IssueTab.vue:617-622`

- [ ] **Step 1: Thêm `lockProject: true`**

Hiện tại:
```javascript
createIssue() {
    this.$refs.createIssueModal.open(null, false, false, {
        solution_id: this.solution.id,
        project_id: this.solution.prospective_project_id || null,
        lockSolution: true,
    })
}
```

Sửa:
```javascript
createIssue() {
    this.$refs.createIssueModal.open(null, false, false, {
        solution_id: this.solution.id,
        project_id: this.solution.prospective_project_id || null,
        lockSolution: true,
        lockProject: true,
    })
}
```

---

### Task 6: Thêm lockProject vào IssueTab của Solution Module Manager

**Files:**
- Modify: `hrm-client/pages/assign/solution-modules/_id/components/IssueTab.vue:557-565`

- [ ] **Step 1: Thêm `lockProject: true`**

Hiện tại:
```javascript
createIssue() {
    this.$refs.createIssueModal.open(null, false, false, {
        solution_id: this.moduleData.solution_id || null,
        module_id: this.moduleData.id || null,
        project_id: this.moduleData.prospective_project_id || this.moduleData.project_id || null,
        lockModule: true,
        lockSolution: true,
    })
}
```

Sửa:
```javascript
createIssue() {
    this.$refs.createIssueModal.open(null, false, false, {
        solution_id: this.moduleData.solution_id || null,
        module_id: this.moduleData.id || null,
        project_id: this.moduleData.prospective_project_id || this.moduleData.project_id || null,
        lockModule: true,
        lockSolution: true,
        lockProject: true,
    })
}
```

---

## Tổng kết files thay đổi

| # | File | Thay đổi |
|---|------|----------|
| 1 | `hrm-api/Modules/Assign/Services/ProspectiveProjectService.php` | +3 dòng filter id |
| 2 | `hrm-api/Modules/Assign/Services/SolutionService.php` | +3 dòng filter id |
| 3 | `hrm-client/pages/assign/tasks/components/CreateTaskModal.vue` | Truyền id param + reload khi có defaults |
| 4 | `hrm-client/pages/assign/issues/components/CreateIssueModal.vue` | Truyền id param + lockProject |
| 5 | `hrm-client/pages/assign/solutions/components/manager/IssueTab.vue` | +1 dòng lockProject |
| 6 | `hrm-client/pages/assign/solution-modules/_id/components/IssueTab.vue` | +1 dòng lockProject |
