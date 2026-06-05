# Sao chép mẫu phiếu thu thập thông tin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để triển khai từng task. Steps dùng checkbox (`- [ ]`).
>
> **Lưu ý project:** KHÔNG commit/push git khi chưa được yêu cầu (bỏ mọi bước commit). FE tuân style module hiện tại. BE rethrow ValidationException (ở đây copy-data là read-only, không validate).

**Goal:** Thêm nút "Sao chép" ở list `assign/form-templates` → vào form Tạo mới đã prefill từ mẫu gốc (đã lọc câu hỏi theo Phạm vi áp dụng), user chọn lại Nhóm giải pháp rồi Lưu qua endpoint `store` sẵn có.

**Architecture:** Hướng A — 1 endpoint đọc BE `GET /assign/form-templates/{id}/copy-data` trả dữ liệu đã lọc + clear `industry_id` + ép draft; FE `add.vue` đọc `?copyFrom` rồi prefill `FormBuilder`. Không tạo record DB cho tới khi user bấm Lưu.

**Tech Stack:** Laravel 8 (PHP 7.4) — Module Assign; Nuxt 2 (Vue 2) — pages/assign/form-templates.

**Spec đầy đủ:** `docs/superpowers/specs/2026-06-05-copy-form-template-design.md`

---

## File Structure

| File | Trách nhiệm | Loại |
|---|---|---|
| `hrm-api/Modules/Assign/Services/FormTemplateService.php` | Thêm `prepareCopyData()` + 2 helper `isScopeAll()`, `copyQuestions()` | Modify |
| `hrm-api/Modules/Assign/Http/Controllers/Api/V1/FormTemplateController.php` | Thêm method `copyData()` | Modify |
| `hrm-api/Modules/Assign/Routes/api.php` | Thêm route `GET /{formTemplate}/copy-data` | Modify |
| `hrm-client/pages/assign/form-templates/index.vue` | Thêm action `copy` (row action + handler) | Modify |
| `hrm-client/pages/assign/form-templates/add.vue` | Nhánh prefill khi có `?copyFrom` + loading gate | Modify |

> Quan hệ `FormQuestion::surveyQuestion()` và `FormGroup::surveyQuestion()` đã có sẵn → không cần thêm.

---

## Phase 1 — Backend

### Task 1: Thêm logic build dữ liệu copy vào FormTemplateService

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/FormTemplateService.php`

- [ ] **Step 1: Thêm import SurveyQuestion**

Trong khối `use` đầu file (cạnh các `use Modules\Assign\Entities\...`), thêm:

```php
use Modules\Assign\Entities\SurveyQuestion;
```

- [ ] **Step 2: Thêm 3 method vào class `FormTemplateService`**

Thêm vào trong class (ví dụ ngay trước method `destroy`):

```php
/**
 * Chuẩn bị dữ liệu để sao chép mẫu phiếu sang form Tạo mới.
 * - Giữ name + scope_id (Nhóm ngành); để trống industry_id (Nhóm giải pháp); ép trạng thái Nháp.
 * - Giữ tất cả Section + thứ tự position (kể cả Section rỗng sau khi lọc).
 * - Câu hỏi/nhóm có application_scope = Theo nhóm giải pháp (2) thì bỏ qua; còn lại clone.
 *
 * @param FormTemplate $template
 * @return array
 */
public function prepareCopyData(FormTemplate $template): array
{
    $template->load([
        'sections.groups.surveyQuestion',
        'sections.groups.questions.surveyQuestion',
        'sections.groups.questions.options',
        'sections.groups.questions.children.surveyQuestion',
        'sections.groups.questions.children.options',
        'sections.questions.surveyQuestion',
        'sections.questions.options',
        'sections.questions.children.surveyQuestion',
        'sections.questions.children.options',
    ]);

    $sections = $template->sections
        ->sortBy('position')
        ->map(function ($sec) {
            return [
                'title' => $sec->title,
                'description' => $sec->description,
                'position' => $sec->position,
                'groups' => $sec->groups
                    ->filter(function ($grp) {
                        return $this->isScopeAll($grp->surveyQuestion);
                    })
                    ->sortBy('position')
                    ->map(function ($grp) {
                        return [
                            'title' => $grp->title,
                            'description' => $grp->description,
                            'position' => $grp->position,
                            'originalHierarchyId' => $grp->survey_question_id,
                            'questions' => $this->copyQuestions($grp->questions),
                        ];
                    })->values()->toArray(),
                'questions' => $this->copyQuestions($sec->questions),
            ];
        })->values()->toArray();

    return [
        'name' => $template->name,
        'scope_id' => $template->scope_id,
        'industry_id' => null,
        'status' => FormTemplate::STATUS_DRAFT,
        'sections' => $sections,
    ];
}

/**
 * True nếu câu hỏi/nhóm được clone.
 * Null (dữ liệu cũ không gắn thư viện) => clone (coi như "Tất cả").
 * Chỉ bỏ khi application_scope == APPLICATION_SCOPE_APPLICATION (Theo nhóm giải pháp).
 *
 * @param SurveyQuestion|null $surveyQuestion
 * @return bool
 */
protected function isScopeAll($surveyQuestion): bool
{
    if (!$surveyQuestion) {
        return true;
    }

    return (int) $surveyQuestion->application_scope !== SurveyQuestion::APPLICATION_SCOPE_APPLICATION;
}

/**
 * Lọc + map collection câu hỏi (đệ quy children) sang shape mà FormBuilder cần.
 * Cha bị bỏ thì con bỏ theo (filter ở cấp cha). Bỏ DB id vì luôn tạo mới.
 *
 * @param \Illuminate\Support\Collection|null $questions
 * @return array
 */
protected function copyQuestions($questions): array
{
    if (!$questions) {
        return [];
    }

    return $questions
        ->filter(function ($q) {
            return $this->isScopeAll($q->surveyQuestion);
        })
        ->sortBy('position')
        ->map(function ($q) {
            return [
                'localId' => $q->local_id ?: ('q-' . $q->id),
                'libraryId' => $q->survey_question_id,
                'type' => $q->type,
                'label' => $q->label,
                'key' => $q->key,
                'code' => $q->code,
                'description' => $q->description,
                'placeholder' => $q->placeholder,
                'required' => (bool) $q->required,
                'visibility' => $q->visibility,
                'position' => $q->position,
                'options' => $q->options
                    ? $q->options->sortBy('position')->map(function ($o) {
                        return [
                            'code' => $o->code,
                            'label' => $o->label,
                            'value' => $o->value,
                        ];
                    })->values()->toArray()
                    : [],
                'children' => $this->copyQuestions($q->children),
            ];
        })->values()->toArray();
}
```

- [ ] **Step 3: Kiểm tra syntax**

Run: `php -l Modules/Assign/Services/FormTemplateService.php` (tại thư mục `hrm-api`)
Expected: `No syntax errors detected`

---

### Task 2: Thêm controller method `copyData`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/FormTemplateController.php`

- [ ] **Step 1: Thêm method `copyData` vào class**

Thêm ngay sau method `show` (kết thúc dòng ~86):

```php
/**
 * Trả dữ liệu mẫu phiếu đã lọc để prefill form Tạo mới (sao chép).
 *
 * @param FormTemplate $formTemplate
 * @return \Illuminate\Http\JsonResponse
 */
public function copyData(FormTemplate $formTemplate)
{
    try {
        $data = $this->formTemplateService->prepareCopyData($formTemplate);

        return $this->responseJson('success', Response::HTTP_OK, $data);
    } catch (Exception $e) {
        Log::error($e);

        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

- [ ] **Step 2: Kiểm tra syntax**

Run: `php -l Modules/Assign/Http/Controllers/Api/V1/FormTemplateController.php`
Expected: `No syntax errors detected`

---

### Task 3: Thêm route copy-data

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php`

- [ ] **Step 1: Thêm route trước `GET /{formTemplate}`**

Trong group `prefix => '/assign/form-templates'`, thêm dòng sau ngay **trước** dòng `Route::get('/{formTemplate}', ...)` (dòng ~229) để route param không nuốt path:

```php
Route::get('/{formTemplate}/copy-data', [FormTemplateController::class, 'copyData'])->middleware('checkPermission:Quản lý danh mục mẫu phiếu thu thập thông tin');
```

- [ ] **Step 2: Kiểm tra route đăng ký**

Run: `php artisan route:list --path=form-templates` (tại `hrm-api`)
Expected: thấy dòng `GET|HEAD  api/v1/assign/form-templates/{formTemplate}/copy-data` → `FormTemplateController@copyData`

- [ ] **Step 3: Smoke test endpoint qua tinker**

Run: `php artisan tinker`
```php
$t = \Modules\Assign\Entities\FormTemplate::first();
$svc = app(\Modules\Assign\Services\FormTemplateService::class);
$data = $svc->prepareCopyData($t);
// Kiểm tra: industry_id == null, status == 1, name giữ nguyên, sections là mảng giữ đủ section
dump($data['industry_id'], $data['status'], $data['name'], count($data['sections']));
```
Expected: `null`, `1`, tên mẫu gốc, số section = số section của mẫu gốc (không mất section nào). Không có Exception.

---

## Phase 2 — Frontend

### Task 4: Thêm action "Sao chép" vào list

**Files:**
- Modify: `hrm-client/pages/assign/form-templates/index.vue`

- [ ] **Step 1: Thêm action `copy` vào `getRowActions(item)`**

Trong `getRowActions`, thêm action `copy` vào mảng `actions` (đặt sau action `view`, trước `edit`):

```js
actions.push({
    key: 'copy',
    title: 'Sao chép mẫu',
    icon: 'ri-file-copy-line',
    class: 'btn btn-light border btn-sm mr-1',
})
```

> Đặt push này ngay sau khối khởi tạo `const actions = [ { key: 'view', ... } ]` và trước khối push `edit`, để thứ tự nút là: Xem → Sao chép → Sửa → (Khoá/Xoá).

- [ ] **Step 2: Thêm case `copy` vào `handleRowAction(payload)`**

Trong `switch (action)`, thêm:

```js
case 'copy':
    this.copyTemplate(item)
    break
```

- [ ] **Step 3: Thêm method `copyTemplate`**

Thêm method (ví dụ ngay sau `createTemplate`):

```js
copyTemplate(t) {
    this.$router.push(`/assign/form-templates/add?copyFrom=${t.id}`)
},
```

- [ ] **Step 4: Kiểm tra giao diện**

Chạy FE (`npm run dev` tại `hrm-client`), mở `/assign/form-templates`.
Expected: mỗi dòng có nút sao chép (icon copy) ở mọi trạng thái; click điều hướng tới `/assign/form-templates/add?copyFrom=<id>`.

---

### Task 5: Prefill form Tạo mới khi có `?copyFrom`

**Files:**
- Modify: `hrm-client/pages/assign/form-templates/add.vue`

- [ ] **Step 1: Gate FormBuilder sau loading (giống edit.vue)**

Thay block `<template>` hiện tại bằng:

```html
<template>
    <div>
        <div v-if="loadingCopy" class="p-4 text-center text-muted">Đang tải dữ liệu sao chép...</div>
        <div v-else>
            <FormBuilder
                ref="formBuilder"
                title=""
                :initial-form="formTemplate"
                :initial-sections="sections"
                :show-save-draft="false"
                :errors="formError"
                @form-meta-changed="handleFormMetaChanged"
                @sections-changed="handleSectionsChanged"
                @save-draft="handleSaveDraft"
                @preview-submit="handlePreviewSubmit"
            />
            <V2Footer :menu="menu" @submitForm="submitForm" @saveAndApprove="submitForm(2)" />
        </div>
    </div>
</template>
```

- [ ] **Step 2: Thêm cờ `loadingCopy` vào `data()`**

Trong `data()`, thêm field:

```js
loadingCopy: false,
```

- [ ] **Step 3: Bật loading sớm trong `created` + tải dữ liệu trong `mounted`**

Thêm vào component (cùng cấp với `methods`):

```js
created() {
    if (this.$route.query.copyFrom) {
        this.loadingCopy = true
    }
},
async mounted() {
    const copyFrom = this.$route.query.copyFrom
    if (copyFrom) {
        await this.loadCopyData(copyFrom)
    }
},
```

- [ ] **Step 4: Thêm method `loadCopyData`**

Thêm vào `methods`:

```js
async loadCopyData(id) {
    try {
        this.loadingCopy = true
        const res = await this.$store.dispatch('apiGetMethod', `assign/form-templates/${id}/copy-data`)
        const payload = res.data || res

        this.formTemplate = {
            name: payload.name || '',
            fieldId: payload.scope_id || '',
            industryId: '',
            status: 'draft',
        }
        this.sections = payload.sections || []
    } catch (e) {
        this.$toasted?.global?.error?.({ message: 'Không thể tải dữ liệu mẫu phiếu để sao chép' })
    } finally {
        this.loadingCopy = false
    }
},
```

- [ ] **Step 5: Verify luồng end-to-end trên browser**

Kịch bản:
1. Vào `/assign/form-templates`, bấm Sao chép ở một mẫu có cả câu hỏi "Tất cả" và "Theo nhóm giải pháp".
2. Form Tạo mới mở ra: Tên giữ nguyên, Nhóm ngành giữ nguyên, **Nhóm giải pháp trống**.
3. Các Section giữ đủ + đúng thứ tự; chỉ còn câu hỏi "Tất cả"; câu hỏi "Theo nhóm giải pháp" đã bị loại.
4. Bấm Lưu khi chưa chọn Nhóm giải pháp → báo lỗi inline required (validate sẵn có).
5. Chọn Nhóm giải pháp → Lưu → tạo mẫu mới thành công (status Nháp), về list.

Expected: đúng toàn bộ 5 bước trên.

---

## Phase 3 — Ràng buộc unique industry_id (bổ sung 2026-06-05)

### Task 6: Mỗi nhóm giải pháp chỉ tồn tại ở 1 mẫu phiếu

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/FormTemplate/FormTemplateRequest.php`

- [x] **Step 1: Thêm `use Illuminate\Validation\Rule;`**
- [x] **Step 2: Đổi rule `industry_id` sang mảng + `Rule::unique('form_templates','industry_id')->ignore(optional($this->route('formTemplate'))->id)`** — unique toàn cục, mọi trạng thái, áp dụng cả store + update (loại trừ chính bản ghi khi sửa).
- [x] **Step 3: Bỏ check cũ published-only trong `withValidator` (đã bị bao trùm) + bỏ `normalizeStatus()` dead-code + bỏ import `FormTemplate` không dùng.**
- [x] **Step 4: Thêm message `industry_id.unique` = "Nhóm giải pháp này đã được sử dụng ở một mẫu phiếu khác".**
- [x] **Step 5: `php -l` PASS.**

> **Lý do lỗ hổng cũ:** check cũ chỉ chặn lúc TẠO MỚI + Published; luồng "Lưu & Duyệt" / "tạo Nháp rồi sửa thành Published" đi qua `update` nên không bị chặn → sinh data trùng (industry_id=130 ở template 16,17,19 đều Published).
>
> **CẢNH BÁO DATA CŨ:** đang có industry_id=130 trùng ở 3 mẫu (16,17,19). Rule mới sẽ khiến **sửa bất kỳ mẫu nào trong nhóm trùng đó bị lỗi** ở field industry cho tới khi dọn còn 1 mẫu/industry. Cần user quyết định cách dọn.
>
> **Ghi chú:** endpoint `unlock` (FormTemplateController) còn check published-uniqueness riêng — giờ dư thừa nhưng vô hại, để nguyên (khác code path, ngoài phạm vi).

## Phase 4 — Nút Sao chép ở màn chi tiết (bổ sung 2026-06-05)

### Task 7: Thêm nút "Sao chép" trong màn chi tiết

**Files:**
- Modify: `hrm-client/pages/assign/form-templates/_id/index.vue`

- [x] **Step 1: Gắn nút vào slot `#custom-actions` của `V2Footer`** — `V2BaseButton primary size="sm"` icon `ri-file-copy-line`, text "Sao chép" (theo button-convention: hành động chính của màn → primary; render trước nút "Quay lại").
- [x] **Step 2: Import `V2BaseButton` + khai báo trong `components`.**
- [x] **Step 3: Thêm method `copyTemplate()` → `$router.push('/assign/form-templates/add?copyFrom=' + $route.params.id)`** (cùng đích như nút copy ở list).

## Self-Review (đã chạy)

- **Spec coverage:** Nút sao chép (Task 4) ✓; điều hướng add?copyFrom (Task 4) ✓; giữ name+scope, clear industry, ép draft (Task 1) ✓; giữ 100% section + position (Task 1) ✓; lọc application_scope 1 clone / 2 bỏ + phòng thủ null + cha bỏ con bỏ (Task 1) ✓; endpoint + permission (Task 2,3) ✓; prefill FE + loading gate (Task 5) ✓; lưu qua store sẵn có (không sửa) ✓.
- **Placeholder scan:** không có TBD/TODO; mọi step có code/command cụ thể.
- **Type consistency:** `prepareCopyData` / `isScopeAll` / `copyQuestions` thống nhất giữa Task 1–2; key FE (`fieldId`, `industryId`, `sections`) khớp `add.vue`/`FormMeta.vue`; shape `sections` khớp `FormTemplateService::store` (`localId`, `libraryId`, `originalHierarchyId`, `options`, `children`).
- **Không sửa hàm dùng chung:** transformer giữ nguyên; chỉ thêm method mới.

---

## Checkpoint — 2026-06-05 (CODE DONE)
Vừa hoàn thành: Triển khai đủ Phase 1 (BE) + Phase 2 (FE) theo plan.
- BE: `FormTemplateService::prepareCopyData/isScopeAll/copyQuestions` + `FormTemplateController::copyData` + route `GET /{formTemplate}/copy-data`. `php -l` PASS. Tinker verify: name+scope giữ, industry=null, status=1, section giữ đủ, scope=1 clone / scope=2 bỏ (template 5: 11→10 câu).
- FE: `index.vue` thêm action `copy` + `copyTemplate()`; `add.vue` gate `loadingCopy` + `created/mounted` đọc `?copyFrom` + `loadCopyData()`.
Đang làm dở: không.
Bước tiếp theo: user chạy `npm run dev` (hrm-client) + verify browser 5 kịch bản ở Task 5 Step 5.
Blocked: route:list không chạy được do lỗi sẵn có module Decision (không liên quan) — đã verify route bằng cách khác (logic service qua tinker).
