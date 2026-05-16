# Spec — Đổi danh mục Nhóm giải pháp & Ứng dụng sang multi-select

> **Trạng thái:** đã chốt design qua brainstorming 2026-04-10.
> **Tác giả:** @manhcuong
> **Tóm tắt ngắn:** xem `.plans/category-multi-select/design.md`.

## 1. Mục tiêu & bối cảnh

Trong module Assign, hai danh mục cấu hình **Nhóm giải pháp** (`industries`) và **Ứng dụng** (`applications`) đang dùng FK đơn để tham chiếu các danh mục cha (Nhóm ngành, Lĩnh vực khách hàng). Nghiệp vụ thực tế: 1 Nhóm giải pháp có thể thuộc nhiều Nhóm ngành, 1 Ứng dụng có thể thuộc nhiều Nhóm ngành / Nhóm giải pháp / Lĩnh vực khách hàng.

→ Đổi 4 trường FK đơn sang multi-select qua 4 pivot table.

## 2. Phạm vi

| # | Bảng nguồn | Cột FK cũ (drop) | Pivot table mới | Cột pivot |
|---|---|---|---|---|
| 1 | `industries` | `scope_id` | `industry_scopes` | `industry_id`, `scope_id` |
| 2 | `applications` | `scope_id` | `application_scopes` | `application_id`, `scope_id` |
| 3 | `applications` | `industry_id` | `application_industries` | `application_id`, `industry_id` |
| 4 | `applications` | `customer_scope_id` | `application_customer_scopes` | `application_id`, `customer_scope_id` |

**Không thay đổi:**
- Bảng `scopes`, `industries`, `customer_scopes`, `applications` ở mức column khác
- Tất cả downstream consumer (Solution, ProspectiveProject, FormTemplate, SurveyQuestion, ProjectPhase…) — đều có FK riêng tới `industries.id` / `applications.id`, không join qua các cột sắp drop
- Routes, Controller — chỉ Service/Model/Request/Resource đổi

## 3. Quyết định đã chốt qua brainstorming

| # | Quyết định | Lựa chọn | Hệ quả |
|---|---|---|---|
| 1 | Xử lý cột FK đơn cũ | Drop hẳn, migrate data sang pivot trong cùng migration | Sạch DB, không backward compat |
| 2 | Cascade dropdown industry theo scope trong form Application | Union + auto-cleanup | Khi bỏ 1 scope, industry không còn thuộc set còn lại bị tự rớt |
| 3 | Filter ở list page | Vẫn single-select | UI không đổi, BE chuyển sang `whereHas` |
| 4 | Hiển thị cột bảng đa giá trị | Liệt kê comma-separated | Resource trả thêm trường `*_names` cho FE dùng trực tiếp |
| 5 | Import Excel format | 1 cell, ngăn dấu phẩy: `NN.0001, NN.0002` | Parser BE/FE phải split |
| 6 | Validation `required` | Phải chọn ≥ 1 | `array \| min:1` |
| 7 | Quy tắc `isCanUnlockUpdate` | STRICT — TẤT CẢ parent đã chọn phải Active | Khoá 1 parent → khoá luôn child |
| 8 | Quy tắc `isCanLockUpdate` | Giữ nguyên — còn ≥ 1 child active → không cho khoá | Đếm child qua pivot |
| 9 | Sort cột Nhóm ngành ở list Nhóm giải pháp | Bỏ sort | Cột hiển thị-only |

## 4. Schema migration chi tiết

**File:** `hrm-api/database/migrations/2026_04_10_000001_convert_industries_applications_to_multi_select.php`

### up()

```php
public function up()
{
    // ===== 1. Tạo 4 pivot table =====
    Schema::create('industry_scopes', function (Blueprint $t) {
        $t->id();
        $t->unsignedBigInteger('industry_id')->comment('FK industries.id');
        $t->unsignedBigInteger('scope_id')->comment('FK scopes.id');
        $t->timestamps();
        $t->unique(['industry_id', 'scope_id']);
        $t->index('scope_id');
    });

    Schema::create('application_scopes', function (Blueprint $t) {
        $t->id();
        $t->unsignedBigInteger('application_id')->comment('FK applications.id');
        $t->unsignedBigInteger('scope_id')->comment('FK scopes.id');
        $t->timestamps();
        $t->unique(['application_id', 'scope_id']);
        $t->index('scope_id');
    });

    Schema::create('application_industries', function (Blueprint $t) {
        $t->id();
        $t->unsignedBigInteger('application_id')->comment('FK applications.id');
        $t->unsignedBigInteger('industry_id')->comment('FK industries.id');
        $t->timestamps();
        $t->unique(['application_id', 'industry_id']);
        $t->index('industry_id');
    });

    Schema::create('application_customer_scopes', function (Blueprint $t) {
        $t->id();
        $t->unsignedBigInteger('application_id')->comment('FK applications.id');
        $t->unsignedBigInteger('customer_scope_id')->comment('FK customer_scopes.id');
        $t->timestamps();
        $t->unique(['application_id', 'customer_scope_id']);
        $t->index('customer_scope_id');
    });

    // ===== 2. Backfill dữ liệu cũ → pivot (chỉ insert nếu FK cha tồn tại) =====
    DB::statement("
        INSERT INTO industry_scopes (industry_id, scope_id, created_at, updated_at)
        SELECT i.id, i.scope_id, NOW(), NOW()
        FROM industries i
        INNER JOIN scopes s ON s.id = i.scope_id
        WHERE i.scope_id IS NOT NULL
    ");
    DB::statement("
        INSERT INTO application_scopes (application_id, scope_id, created_at, updated_at)
        SELECT a.id, a.scope_id, NOW(), NOW()
        FROM applications a
        INNER JOIN scopes s ON s.id = a.scope_id
        WHERE a.scope_id IS NOT NULL
    ");
    DB::statement("
        INSERT INTO application_industries (application_id, industry_id, created_at, updated_at)
        SELECT a.id, a.industry_id, NOW(), NOW()
        FROM applications a
        INNER JOIN industries i ON i.id = a.industry_id
        WHERE a.industry_id IS NOT NULL
    ");
    DB::statement("
        INSERT INTO application_customer_scopes (application_id, customer_scope_id, created_at, updated_at)
        SELECT a.id, a.customer_scope_id, NOW(), NOW()
        FROM applications a
        INNER JOIN customer_scopes cs ON cs.id = a.customer_scope_id
        WHERE a.customer_scope_id IS NOT NULL
    ");

    // ===== 3. Drop cột cũ =====
    Schema::table('industries', fn(Blueprint $t) => $t->dropColumn('scope_id'));
    Schema::table('applications', function (Blueprint $t) {
        $t->dropColumn(['scope_id', 'industry_id', 'customer_scope_id']);
    });
}
```

### down() — rollback dev (lossy)

```php
public function down()
{
    Schema::table('industries', fn(Blueprint $t) =>
        $t->unsignedBigInteger('scope_id')->nullable()->after('id')
    );
    Schema::table('applications', function (Blueprint $t) {
        $t->unsignedBigInteger('scope_id')->nullable()->after('id');
        $t->unsignedBigInteger('industry_id')->nullable()->after('scope_id');
        $t->unsignedBigInteger('customer_scope_id')->nullable()->after('industry_id');
    });

    DB::statement("UPDATE industries i
        SET scope_id = (SELECT scope_id FROM industry_scopes
                        WHERE industry_id = i.id ORDER BY id LIMIT 1)");
    DB::statement("UPDATE applications a
        SET scope_id = (SELECT scope_id FROM application_scopes
                        WHERE application_id = a.id ORDER BY id LIMIT 1)");
    DB::statement("UPDATE applications a
        SET industry_id = (SELECT industry_id FROM application_industries
                           WHERE application_id = a.id ORDER BY id LIMIT 1)");
    DB::statement("UPDATE applications a
        SET customer_scope_id = (SELECT customer_scope_id FROM application_customer_scopes
                                 WHERE application_id = a.id ORDER BY id LIMIT 1)");

    Schema::dropIfExists('application_customer_scopes');
    Schema::dropIfExists('application_industries');
    Schema::dropIfExists('application_scopes');
    Schema::dropIfExists('industry_scopes');
}
```

> ⚠️ Production: bắt buộc backup DB trước khi chạy migration. Down() chỉ giữ lại 1 FK đầu tiên (LIMIT 1) — nếu rollback sau khi user đã add nhiều giá trị mới sẽ mất dữ liệu.

## 5. Backend — Model

### `Modules\Assign\Entities\Industries`

**Bỏ:**
- `'scope_id'` khỏi `$fillable`
- Method `scope()` belongsTo

**Thêm:**
```php
public function scopes()
{
    return $this->belongsToMany(
        Scope::class,
        'industry_scopes',
        'industry_id',
        'scope_id'
    )->withTimestamps();
}

public function applications()
{
    return $this->belongsToMany(
        Applications::class,
        'application_industries',
        'industry_id',
        'application_id'
    )->withTimestamps();
}
```

**Sửa:**
```php
public function isCanUnlockUpdate()
{
    return $this->scopes()->exists()
        && $this->scopes()->where('scopes.status', '!=', Scope::STATUS_ACTIVE)->doesntExist();
}

public function isCanLockUpdate()
{
    // Giữ nguyên ngữ nghĩa: không còn application active liên kết
    return $this->applications()->where('applications.status', Applications::STATUS_ACTIVE)->doesntExist();
}

public function isCodeEditable()
{
    return $this->applications()->count() == 0;
}

public function isCanDelete()
{
    return $this->applications()->count() == 0;
}
```

### `Modules\Assign\Entities\Applications`

**Bỏ:**
- `'scope_id'`, `'industry_id'`, `'customer_scope_id'` khỏi `$fillable`
- 3 method `scope()`, `industry()`, `customerScope()` belongsTo

**Thêm:**
```php
public function scopes()
{
    return $this->belongsToMany(Scope::class, 'application_scopes',
        'application_id', 'scope_id')->withTimestamps();
}
public function industries()
{
    return $this->belongsToMany(Industries::class, 'application_industries',
        'application_id', 'industry_id')->withTimestamps();
}
public function customerScopes()
{
    return $this->belongsToMany(CustomerScope::class, 'application_customer_scopes',
        'application_id', 'customer_scope_id')->withTimestamps();
}
```

**Sửa:**
```php
public function isCanUnlockUpdate()
{
    $industriesOk = $this->industries()->exists()
        && $this->industries()->where('industries.status', '!=', Industries::STATUS_ACTIVE)->doesntExist();
    $csOk = $this->customerScopes()->exists()
        && $this->customerScopes()->where('customer_scopes.status', '!=', CustomerScope::STATUS_ACTIVE)->doesntExist();
    return $industriesOk && $csOk;
}
```

`isCanDelete()` giữ nguyên (chỉ phụ thuộc downstream `prospectiveProjects`, `formTemplates`, `surveyQuestions`).

## 6. Backend — Service

### `IndustriesService`

| Chỗ sửa | Trước | Sau |
|---|---|---|
| Filter `scope_id` | `where('industries.scope_id', $request->scope_id)` | `whereHas('scopes', fn($q) => $q->where('scopes.id', $request->scope_id))` |
| Đếm applications (2 chỗ `selectSub`) | `from('applications').whereColumn('applications.industry_id', 'industries.id').count(*)` | `from('application_industries').whereColumn('application_industries.industry_id', 'industries.id').selectRaw('count(distinct application_id)')` |
| `store()` | sau create → `$industry->scopes()->sync($request->scope_ids)` |
| `update()` | sau update → `$industry->scopes()->sync($request->scope_ids)` |

### `ApplicationService`

| Chỗ sửa | Trước | Sau |
|---|---|---|
| Filter `scope_id` | `where('scope_id', $request->scope_id)` | `whereHas('scopes', fn($q) => $q->where('scopes.id', $request->scope_id))` |
| Filter `industry_id` | `where('industry_id', ...)` | `whereHas('industries', ...)` |
| Filter `customer_scope_id` | `where('customer_scope_id', ...)` | `whereHas('customerScopes', ...)` |
| `store/update` payload | set 3 cột FK | bỏ khỏi `create/update`, thay bằng 3 lệnh `sync(scope_ids/industry_ids/customer_scope_ids)` |
| Validate cascade (line 280-281, 421) | `if ($industry->scope_id != $scope->id)` | xem snippet bên dưới |
| Import `bulkInsert` (line 450-484) | hardcode 3 cột FK | gom dữ liệu cha → sync pivot từng dòng (hoặc bulk insert pivot sau) |

**Snippet validate cascade mới:**
```php
$invalidIndustries = Industries::whereIn('id', $request->industry_ids)
    ->whereDoesntHave('scopes', fn($q) => $q->whereIn('scopes.id', $request->scope_ids))
    ->pluck('name');
if ($invalidIndustries->isNotEmpty()) {
    throw new Exception('Các nhóm giải pháp sau không thuộc nhóm ngành đã chọn: '
        . $invalidIndustries->implode(', '));
}
```

### `ScopeService` (4 chỗ count)

```php
// Đếm industries thuộc 1 scope
->selectSub(function ($q) {
    $q->from('industry_scopes')
      ->whereColumn('industry_scopes.scope_id', 'scopes.id')
      ->selectRaw('count(distinct industry_id)');
}, 'industries_count')
// Tương tự với application_scopes → count distinct application_id
```

### `CustomerScopeService` (1 chỗ count)
```php
->selectSub(function ($q) {
    $q->from('application_customer_scopes')
      ->whereColumn('application_customer_scopes.customer_scope_id', 'customer_scopes.id')
      ->selectRaw('count(distinct application_id)');
}, 'applications_count')
```

## 7. Backend — Request validation

### `IndustriesRequest`
```php
'scope_ids'   => 'required|array|min:1',
'scope_ids.*' => 'integer|exists:scopes,id',
'name'        => 'required|string|max:255|unique:industries,name,' . $this->id,
'code'        => '...giữ nguyên...',
```

### `ApplicationsRequest`
```php
'scope_ids'             => 'required|array|min:1',
'scope_ids.*'           => 'integer|exists:scopes,id',
'industry_ids'          => 'required|array|min:1',
'industry_ids.*'        => 'integer|exists:industries,id',
'customer_scope_ids'    => 'required|array|min:1',
'customer_scope_ids.*'  => 'integer|exists:customer_scopes,id',
'name'                  => '...giữ nguyên...',
'code'                  => '...giữ nguyên...',
```

Cascade validation: chuyển vào `withValidator()` để gọi 1 lần & trả lỗi cụ thể, tránh duplicate code với Service.

## 8. Backend — Resource transformer

### `IndustryResource` (list)
```php
return [
    'id' => $this->id,
    'code' => $this->code,
    'name' => $this->name,
    'status' => $this->status,
    'scopes' => $this->scopes->map(fn($s) => ['id' => $s->id, 'name' => $s->name])->values(),
    'scope_names' => $this->scopes->pluck('name')->implode(', '),
    'applications_count' => $this->applications_count, // selectSub
    'is_can_lock_update' => $this->isCanLockUpdate(),
    'is_can_unlock_update' => $this->isCanUnlockUpdate(),
    // ... các field khác giữ nguyên
];
```

### `IndustryDetailResource`
```php
'scopes' => $this->scopes->map(fn($s) => ['id' => $s->id, 'name' => $s->name])->values(),
// (không cần scope_names trong detail)
```

### `ApplicationsResource` (list)
```php
'scopes' => $this->scopes->map(fn($s) => ['id' => $s->id, 'name' => $s->name])->values(),
'scope_names' => $this->scopes->pluck('name')->implode(', '),
'industries' => $this->industries->map(fn($i) => ['id' => $i->id, 'name' => $i->name])->values(),
'industry_names' => $this->industries->pluck('name')->implode(', '),
'customer_scopes' => $this->customerScopes->map(fn($cs) => ['id' => $cs->id, 'name' => $cs->name])->values(),
'customer_scope_names' => $this->customerScopes->pluck('name')->implode(', '),
```

### `getAll` master select của Industries
Trả thêm `scope_ids[]` để FE form Application cascade dropdown:
```php
['id' => $i->id, 'name' => $i->name, 'scope_ids' => $i->scopes->pluck('id')->values()]
```

## 8.bis Downstream FE consumers (bổ sung 2026-04-10)

Sau khi audit, **14 file FE đang dùng pattern `industry.scope_id` / `application.industry_id`** để cascade dropdown. Khi BE drop các cột này, master select trả về sẽ thiếu field → cascade vỡ.

### Vuex store `store/optionsSelect.js`

**`fetchIndustries`** (line 246-261)
```js
const industries = data.map((industry) => ({
    id: industry.id,
    text: industry.name,
    scope_ids: industry.scope_ids || [],   // ← đổi từ scope_id (single) sang scope_ids (array)
}))
```

**`fetchApplications`** (line 280-297)
```js
const applications = data.map((application) => ({
    id: application.id,
    text: application.name,
    scope_ids: application.scope_ids || [],
    industry_ids: application.industry_ids || [],
    customer_scope_ids: application.customer_scope_ids || [],
}))
```

### Pattern chuyển đổi cascade

**Trước:**
```js
filtered = all.filter(industry =>
    String(industry.scope_id) === String(this.form.scope_ids[0])
)
// hoặc
filtered = all.filter(industry =>
    this.form.scope_ids.some(s => String(s) === String(industry.scope_id))
)
```

**Sau:**
```js
filtered = all.filter(industry =>
    industry.scope_ids?.some(sid => this.form.scope_ids.includes(sid))
)
```

### Danh sách 14 file phải audit + fix

| # | File | Loại |
|---|---|---|
| 1 | `pages/assign/project_phase/components/ProjectPhaseForm.vue` | Cascade — chắc chắn fix |
| 2 | `components/V2BaseFieldCategoryApplicationFilter.vue` | Cascade — chắc chắn fix |
| 3 | `pages/assign/request-solution/components/RequestSolutionForm.vue` | Audit (form data riêng) |
| 4 | `pages/assign/request-solution/components/FormTab.vue` | Audit |
| 5 | `pages/assign/prospective-projects/components/ProjectInfoSection.vue` | Audit |
| 6 | `pages/assign/meeting/components/MeetingForm.vue` | Audit (line 413 đọc từ project) |
| 7 | `pages/assign/meeting/components/MeetingProject.vue` | Audit |
| 8 | `pages/assign/questions/components/QuestionForm.vue` | Audit |
| 9 | `pages/assign/form-templates/components/AddQuestionQuickModal.vue` | Audit |
| 10 | `pages/assign/report/prospective-projects/components/ProspectiveProjectsFilter.vue` | Audit |
| 11 | `pages/assign/solutions/index.vue` | Audit |
| 12 | `pages/assign/questions/index.vue` | Audit |
| 13 | `pages/assign/application/index.vue` | Chính (đã có trong Phase 6) |
| 14 | `components/modal/application-modal.vue` | Chính (đã có trong Phase 6) |

**Phân loại "Audit":** đọc kỹ xem field `scope_id`/`industry_id` trong file đang được dùng để (a) cascade dropdown từ master select → fix, hay (b) lưu vào table riêng của entity đó (vd `request_solutions.scope_id`) → không cần đổi.

## 9. Frontend

### 9.1 `industry-modal.vue`

- `data.scope_id` → `data.scope_ids: []`
- `<V2BaseSelectInModal v-model="data.scope_ids" :options="scopes" multiple />` (verify prop `multiple` có sẵn — task đầu Phase BE/FE)
- Validation FE: `if (!data.scope_ids?.length) error.scope_ids = 'Bắt buộc chọn ít nhất 1'`
- Submit: payload có `scope_ids`
- Hiển thị view-mode: dùng `data.scope_names`

### 9.2 `application-modal.vue`

- 3 binding array: `scope_ids`, `industry_ids`, `customer_scope_ids`
- 3 select đổi sang multi
- Cascade union + auto-cleanup:
  ```js
  computed: {
    filteredIndustries() {
      if (!this.data.scope_ids?.length) return []
      const set = new Set(this.data.scope_ids)
      return this.allIndustries.filter(i => i.scope_ids?.some(sid => set.has(sid)))
    },
  },
  watch: {
    'data.scope_ids'() {
      const validIds = new Set(this.filteredIndustries.map(i => i.id))
      const before = this.data.industry_ids?.length || 0
      this.data.industry_ids = (this.data.industry_ids || []).filter(id => validIds.has(id))
      const removed = before - this.data.industry_ids.length
      if (removed > 0) {
        this.$bvToast.toast(`Đã tự bỏ chọn ${removed} nhóm giải pháp do không còn thuộc nhóm ngành đã chọn`,
          { title: 'Cảnh báo', variant: 'warning' })
      }
    },
  },
  ```
- API getAll industries cần trả thêm `scope_ids` (đã quy định ở §8)

### 9.3 List page `pages/assign/solution-groups/index.vue`

- Filter `scope_id` giữ single, không đổi
- Cột Nhóm ngành: `{{ item.scope_names }}` (string)
- Bỏ sort cột Nhóm ngành (xoá `sortable: true` nếu có)

### 9.4 List page `pages/assign/application/index.vue`

- 3 filter giữ single
- 3 cột hiển thị: `scope_names`, `industry_names`, `customer_scope_names`
- Sort 3 cột này — kiểm tra & bỏ nếu có

### 9.5 Import Excel

- File mẫu: cập nhật text mô tả các cột Nhóm ngành / Nhóm giải pháp / Lĩnh vực khách hàng — "Có thể nhập nhiều mã, ngăn nhau bằng dấu phẩy"
- FE parse: `cell.split(',').map(s => s.trim()).filter(Boolean)`
- Validate: từng code phải tồn tại trong master, cascade industry∈scope phải pass
- Payload import gửi BE: row có 3 mảng codes thay vì 3 single
- Cân nhắc helper `parseCommaCodes(value)` ở `utils/import-error-helper.js` nếu lặp lại

## 10. Edge case

| # | Edge case | Xử lý |
|---|---|---|
| 1 | Bản ghi cũ có FK NULL | Migration không insert dòng pivot → bản ghi không có giá trị nào → cần edit thủ công sau migration. Báo cho PM kiểm tra trước khi deploy |
| 2 | FK cũ trỏ tới ID không tồn tại | INNER JOIN trong INSERT chặn → bản ghi rác bị bỏ qua |
| 3 | Lock parent → child không mở khoá được | Hiển thị toast/tooltip rõ: "Nhóm giải pháp X đang khoá. Mở khoá hoặc bỏ khỏi Ứng dụng" |
| 4 | Cascade auto-cleanup gây mất chọn bất ngờ | Toast cảnh báo số lượng bị bỏ |
| 5 | Import code không tồn tại | Báo lỗi từng code: "Dòng X: code 'NN.9999' không tồn tại" |
| 6 | Update với pivot | Dùng `sync()`, không dùng `attach()` |
| 7 | Permission xem theo cấp | Không thay đổi (không thuộc scope feature này) |

## 11. Rollback

- **Dev**: `php artisan migrate:rollback --step=1` — down() đã viết, lossy
- **Code**: revert PR (BE + FE cùng lúc)
- **Production**: backup DB trước khi deploy. Nếu cần rollback sau khi đã có dữ liệu mới, phải restore từ backup chứ không dùng down()

## 12. Test case checklist

### Backend
- [ ] Migration up chạy được trên DB rỗng
- [ ] Migration up chạy được trên DB có data — số dòng pivot khớp số bản ghi có FK cũ != null & cha tồn tại
- [ ] Migration down rollback được (dev)
- [ ] Filter list `scope_id` (single) trả đúng kết quả qua pivot
- [ ] Filter list `industry_id`, `customer_scope_id` tương tự
- [ ] Store/update Industry với `scope_ids` → pivot có đúng số dòng
- [ ] Store/update Application với 3 mảng → 3 pivot đúng
- [ ] Validate cascade industry∈scope: pass khi hợp lệ, fail với message rõ ràng
- [ ] `isCanUnlockUpdate` Industry: 1 scope inactive → false; tất cả active → true
- [ ] `isCanUnlockUpdate` Application: 1 industry inactive → false; 1 customer_scope inactive → false; tất cả active → true
- [ ] `isCanLockUpdate` Industry: còn 1 application active → false; không còn → true
- [ ] Import Excel parse cell `"NN.0001, NN.0002"` thành 2 dòng pivot
- [ ] Import báo lỗi rõ khi 1 code không tồn tại
- [ ] Đếm applications_count Industry, industries_count/applications_count Scope, applications_count CustomerScope đều đúng qua pivot
- [ ] Downstream Solution/ProspectiveProject/FormTemplate vẫn hoạt động bình thường (không regression)

### Frontend
- [ ] Form Industry: chọn nhiều scope, lưu, reload, hiện đúng các scope đã chọn
- [ ] Form Application: chọn nhiều scope → industry dropdown hiện union; bỏ 1 scope → industry tự rớt + toast
- [ ] List Industry: cột Nhóm ngành hiện comma-separated, không sort được
- [ ] List Application: 3 cột comma-separated
- [ ] Filter Industry single vẫn lọc đúng
- [ ] Filter Application 3 single đều OK
- [ ] Import file mẫu mới: parse OK, validate OK, import OK
- [ ] Import báo lỗi UI khi cell có code sai

## 13. Tổng hợp endpoint

| Endpoint | Thay đổi |
|---|---|
| `GET assign/industries` | Resource trả `scopes[]`, `scope_names`. Filter `scope_id` qua pivot |
| `GET assign/industries/{id}` | DetailResource trả `scopes[]` |
| `POST assign/industries` | Body: `scope_ids[]` |
| `PUT assign/industries/{id}` | Body: `scope_ids[]` |
| `POST assign/industries/import` | Parse comma codes |
| `GET assign/industries/getAll` (master) | Trả thêm `scope_ids[]` cho cascade FE |
| `GET assign/applications` | Resource trả 3 array + 3 `*_names`. 3 filter qua pivot |
| `GET assign/applications/{id}` | DetailResource trả 3 array |
| `POST assign/applications` | Body: 3 `*_ids` array |
| `PUT assign/applications/{id}` | Body: 3 `*_ids` array |
| `POST assign/applications/import` | Parse 3 cột comma codes |
| Tất cả các endpoint downstream tham chiếu industries/applications | Không đổi |

## 14. Hot-fix downstream sau migration (2026-04-10)

> ⚠️ Giả định ban đầu — "downstream không bị ảnh hưởng" — sai. Sau khi user chạy migration, API `GET /assign/scopes` crash do `Scope::industries()` còn `hasMany(Industries::class, 'scope_id')`. Audit phát hiện 7 chỗ còn tham chiếu cột đã drop:

### BE — Relations còn dùng FK đơn (gây crash)
- `Modules/Assign/Entities/Scope/Scope.php`: `industries()`/`applications()` `hasMany` qua `scope_id` → đổi `belongsToMany` qua pivot `industry_scopes`/`application_scopes`. `isCanLockUpdate` qualify `industries.status` + dùng `doesntExist()`
- `Modules/Assign/Entities/CustomerScope/CustomerScope.php`: `applications()` `hasMany` qua `customer_scope_id` → đổi `belongsToMany` qua pivot `application_customer_scopes`. `isCanLockUpdate` qualify `applications.status`

### BE — Service đọc cột đã drop
- `Services/ProspectiveProjectService::autoFillFromApplication`: đọc `$app->scope_id`/`industry_id`/`customer_scope_id` → eager load 3 pivot, fallback lấy first phần tử, chỉ fill khi PP chưa có giá trị
- `Services/Report/SolutionsWorkSummaryByDepartmentReportService`:
  - `with('industry')` của Application — relation singular không tồn tại → đổi `with(['industries:id','scopes:id'])`
  - `resolveSolutionCatalogIds` fallback đọc `$appModel->scope_id`/`industry_id` và `$industryModel->scope_id` → đọc qua pivot, hỗ trợ cả 2 trường hợp đã/chưa eager load

### BE — Resource trả field cũ
- `Transformers/SurveyQuestionsResource`: trả `industry.scope_id`, `application.scope_id`, `application.industry_id` → đổi sang `scope_ids[]` / `industry_ids[]` array, lấy từ relation pivot (an toàn cả khi chưa eager load)

### FE — Vuex consumer còn map field cũ
- `store/optionsSelect.js` `fetchIndustries`/`fetchApplications`: map `scope_id`/`industry_id`/`customer_scope_id` (singular) → đổi sang `*_ids` array (đọc từ `industry.scopes`, `application.scopes`/`industries`/`customer_scopes` mà BE eager load)
- `pages/assign/form-templates/components/FormMeta.vue`: `industryOptions`/`appOptions` cascade filter còn pattern `===` so sánh field singular → đổi sang `(arr || []).map(String).includes(targetId)` (đồng bộ với 11 trang đã migrate ở Phase 8)

### Bài học
- Khi drop FK, **không thể chỉ search SQL `JOIN`** — phải search cả: relation method định nghĩa qua tên cột (literal `'scope_id'` trong PHP), eager load `with('relation_name')`, property access `$model->field`, Resource serialization, FE store mapper, FE cascade filter.
- Verify "không bị ảnh hưởng" cần grep theo **tên cột** trong context PHP, không chỉ grep theo SQL join.
