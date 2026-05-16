# Spec chi tiết — Đổi cấp gán Câu hỏi / Phiếu thu thập từ Ứng dụng sang Nhóm giải pháp

**Ngày:** 2026-04-18
**Owner:** @manhcuong
**Trạng thái:** Design đã chốt, sẵn sàng implement

---

## 1. Bối cảnh

Hiện tại, câu hỏi khảo sát (`survey_questions`) và mẫu phiếu thu thập thông tin (`form_templates`) được gán đến cấp **Ứng dụng**. Mỗi dự án tiền khả thi (TKT) và meeting tạo nhanh dự án TKT đều match mẫu phiếu theo `application_id`.

Business decide: không cần chi tiết đến cấp Ứng dụng — **gán ở cấp Nhóm giải pháp (industry) là đủ**. Mỗi Nhóm giải pháp có tối đa **1 mẫu phiếu active** (Published), và dự án TKT tự match mẫu phiếu theo Nhóm giải pháp.

Tính năng liên quan:
- `pages/assign/questions/add` — tạo câu hỏi
- `pages/assign/form-templates/add` — tạo mẫu phiếu
- `pages/assign/prospective-projects/add` — tạo dự án TKT
- `pages/assign/meeting/create` — tạo meeting (có luồng tạo nhanh dự án TKT)

## 2. Mục tiêu

1. Bỏ gán Câu hỏi / Mẫu phiếu đến cấp Ứng dụng, chỉ giữ đến cấp Nhóm giải pháp
2. Ràng buộc mỗi Nhóm giải pháp có tối đa 1 Mẫu phiếu Published
3. Dự án TKT và Meeting match mẫu phiếu theo `industry_id` (đổi application cùng industry không reset form)
4. Dọn data redundant: các pivot `survey_question_scopes`, `survey_question_industries`, `survey_question_applications` không còn cần thiết (UI chỉ chọn 1)

## 3. Phạm vi (Scope)

### In-scope
- BE `Modules/Assign`: SurveyQuestion, FormTemplate, ProspectiveProject, Meeting
- FE: 4 module đã liệt kê
- Migration data + schema cho các bảng liên quan

### Out-of-scope
- Không đụng snapshot (`form_template_snapshots`, `form_question_snapshots`, `form_group_snapshots`, `form_section_snapshots`) — cột `application_id` ở các bảng này giữ nguyên làm dead data, không dùng đến
- Không hỗ trợ multi-select industry cho câu hỏi (UI giữ single)

## 4. Schema DB

### 4.1 Bảng `survey_questions`

| Thay đổi | Cột |
|---|---|
| DROP | `application_id` |
| GIỮ | `scope_id` (int, nullable), `industry_id` (int, nullable) — single |
| GIỮ | `application_scope` (tinyint): `1 = Tất cả`, `2 = Theo nhóm giải pháp` |

### 4.2 Bảng `form_templates`

| Thay đổi | Cột |
|---|---|
| DROP | `application_id` |
| GIỮ | `scope_id` (int), `industry_id` (int) |
| Constraint logic | Mỗi `industry_id` có tối đa 1 row `status = 2 (Published)` |

### 4.3 Bảng pivot — DROP toàn bộ

- `survey_question_scopes`
- `survey_question_industries`
- `survey_question_applications`

### 4.4 Snapshots — KHÔNG đụng

Các bảng `form_template_snapshots`, `form_question_snapshots`, `form_group_snapshots`, `form_section_snapshots` giữ nguyên, kể cả cột `application_id`. Đây là dead column, không dùng đến sau khi ship.

## 5. Migration script

Tạo 1 file migration duy nhất, thực hiện tuần tự trong `DB::transaction`:

```php
// 2026_04_18_000000_migrate_question_form_to_industry_level.php

public function up()
{
    DB::transaction(function () {
        // Step 1: Backfill survey_questions.industry_id từ pivot (nếu single col đang null)
        DB::statement("
            UPDATE survey_questions sq
            INNER JOIN survey_question_industries sqi ON sqi.survey_question_id = sq.id
            SET sq.industry_id = sqi.industry_id
            WHERE sq.industry_id IS NULL
        ");

        DB::statement("
            UPDATE survey_questions sq
            INNER JOIN survey_question_scopes sqs ON sqs.survey_question_id = sq.id
            SET sq.scope_id = sqs.scope_id
            WHERE sq.scope_id IS NULL
        ");

        // Step 2: Backfill form_templates.industry_id từ application nếu null
        // application.industry_ids là JSON/pivot → lấy industry đầu tiên
        $templates = DB::table('form_templates')
            ->whereNull('industry_id')
            ->whereNotNull('application_id')
            ->get();

        foreach ($templates as $tpl) {
            $industryId = DB::table('application_industries')
                ->where('application_id', $tpl->application_id)
                ->value('industry_id');
            if ($industryId) {
                DB::table('form_templates')->where('id', $tpl->id)->update(['industry_id' => $industryId]);
            }
        }

        // Step 3: Dedupe form_templates Published cùng industry
        // Giữ cái created_at mới nhất ở Published, còn lại → Locked (status = 3)
        $duplicates = DB::table('form_templates')
            ->select('industry_id', DB::raw('COUNT(*) as cnt'))
            ->where('status', 2) // Published
            ->whereNotNull('industry_id')
            ->groupBy('industry_id')
            ->having('cnt', '>', 1)
            ->pluck('industry_id');

        foreach ($duplicates as $industryId) {
            $latest = DB::table('form_templates')
                ->where('industry_id', $industryId)
                ->where('status', 2)
                ->orderByDesc('created_at')
                ->orderByDesc('id')
                ->first();

            DB::table('form_templates')
                ->where('industry_id', $industryId)
                ->where('status', 2)
                ->where('id', '!=', $latest->id)
                ->update(['status' => 3]); // Locked
        }

        // Step 4: Drop cột application_id
        Schema::table('survey_questions', function (Blueprint $table) {
            $table->dropColumn('application_id');
        });
        Schema::table('form_templates', function (Blueprint $table) {
            $table->dropColumn('application_id');
        });

        // Step 5: Drop pivot tables
        Schema::dropIfExists('survey_question_scopes');
        Schema::dropIfExists('survey_question_industries');
        Schema::dropIfExists('survey_question_applications');
    });
}
```

**Lưu ý:** rollback (`down()`) chỉ restore schema, data pivot mất luôn — business chấp nhận (không revert).

## 6. Model changes

### 6.1 `SurveyQuestion.php`

```php
// Bỏ khỏi $fillable
// - 'application_id'

// Giữ
protected $fillable = [
    'scope_id',
    'industry_id',
    'application_scope',
    'title',
    'description',
    'data_type',
    'status',
];

// Xoá các relationship:
// - scopes() (belongsToMany → pivot survey_question_scopes)
// - industries() (belongsToMany → pivot survey_question_industries)
// - applications() (belongsToMany → pivot survey_question_applications)
// - application() (belongsTo)

// Giữ: scope(), industry(), answers(), questionRelations(), parentQuestionRelations(),
//      childQuestions(), parentQuestions(), formQuestions(), formGroups()

// Constants giữ nguyên:
const APPLICATION_SCOPE_ALL = 1;
const APPLICATION_SCOPE_APPLICATION = 2; // Rename comment thành "Theo nhóm giải pháp" nhưng giữ tên const để không breaking
```

### 6.2 `FormTemplate.php`

```php
protected $fillable = [
    'name',
    'scope_id',
    'industry_id',
    'status',
    'meta',
    'created_by',
    'updated_by',
];

// Bỏ relationship application()
// Giữ scope(), industry(), sections(), questions(), prospectiveProjects()
```

## 7. Service changes

### 7.1 `SurveyQuestionService.php`

- **Bỏ method:** `syncScopes()`, `syncIndustries()`, `syncApplications()`
- **Bỏ array `$relations`:** loại `'scopes'`, `'industries'`, `'applications'`
- **`index()`:** filter `application_id` chuyển thành filter `industry_id`:
  ```php
  $query->when($request->industry_id, fn($q) => $q->where('industry_id', $request->industry_id));
  $query->when($request->scope_id, fn($q) => $q->where('scope_id', $request->scope_id));
  // Filter có include câu hỏi "Tất cả":
  $query->when($request->include_all_scope, fn($q) => $q->orWhere('application_scope', 1));
  ```
- **`payload()`:** bỏ `$applicationIds`, bỏ set `application_id`. `scope_id`, `industry_id` lấy từ request dạng single int (FE sẽ gửi thẳng):
  ```php
  if ($applicationScope == SurveyQuestion::APPLICATION_SCOPE_ALL) {
      $data['scope_id'] = null;
      $data['industry_id'] = null;
  } else {
      $data['scope_id'] = $request->input('scope_id');
      $data['industry_id'] = $request->input('industry_id');
  }
  ```
- **`store()` / `update()`:** bỏ 3 lời gọi `syncScopes/syncIndustries/syncApplications`
- **`destroy()`:** bỏ xoá pivot

### 7.2 `FormTemplateService.php`

- **Khi tạo/update với status = Published:** check rule 1 industry - 1 form active
  ```php
  // Chỉ check khi TẠO mới với status = Published, hoặc khi chuyển Draft → Published
  if ($request->status == FormTemplate::STATUS_PUBLISHED) {
      $query = FormTemplate::where('industry_id', $request->industry_id)
          ->where('status', FormTemplate::STATUS_PUBLISHED);
      if ($formTemplate) { // update
          $query->where('id', '!=', $formTemplate->id);
      }
      if ($query->exists()) {
          throw new \Exception('Nhóm giải pháp này đã có phiếu thu thập đang hoạt động');
      }
  }
  ```
  (Chi tiết logic validation xem mục 8)
- Bỏ `application_id` khỏi payload create/update

### 7.3 `ProspectiveProjectService.php` + `MeetingService.php`

- Hàm `matchFormTemplate($industryId)`: tìm `FormTemplate::where('industry_id', $industryId)->where('status', Published)->first()`
- Khi tạo snapshot, vẫn copy data từ form_template hiện tại (snapshot cũ giữ `application_id` chết, không block)

## 8. Validation

### 8.1 `FormTemplateRequest.php`

```php
public function rules()
{
    return [
        'name' => ['required', 'string', 'max:255'],
        'scope_id' => ['required', 'integer', 'exists:scopes,id'],
        'industry_id' => ['required', 'integer', 'exists:industries,id'],
        'status' => ['required', 'in:1,2,3'],
        // Bỏ: 'application_id'
    ];
}

public function withValidator($validator)
{
    $validator->after(function ($v) {
        // Chặn cứng chỉ khi TẠO MỚI với status Published
        // Edit được sửa thoải mái (quyết định #8, snapshot đã khoá lịch sử)
        $isCreate = !$this->route('formTemplate');
        if ($isCreate && $this->status == 2) {
            $exists = FormTemplate::where('industry_id', $this->industry_id)
                ->where('status', 2)
                ->exists();
            if ($exists) {
                $v->errors()->add('industry_id', 'Nhóm giải pháp này đã có phiếu thu thập đang hoạt động');
            }
        }
    });
}
```

### 8.2 `SurveyQuestionRequest.php`

```php
public function rules()
{
    $scope = $this->input('application_scope');
    return [
        'title' => ['required', 'string'],
        'data_type' => ['required', Rule::in(SurveyQuestion::DATA_TYPES)],
        'application_scope' => ['required', 'in:1,2'],
        'scope_id' => $scope == 2 ? ['required', 'integer'] : ['nullable'],
        'industry_id' => $scope == 2 ? ['required', 'integer'] : ['nullable'],
        'status' => ['required', 'in:1,2'],
        // Bỏ: 'application_ids', 'scope_ids', 'industry_ids'
    ];
}
```

## 9. API contract thay đổi

### 9.1 `POST /assign/questions`, `PUT /assign/questions/{id}`

**Payload cũ:**
```json
{
  "application_scope": 2,
  "scope_ids": [1],
  "industry_ids": [5],
  "application_ids": [10],
  ...
}
```

**Payload mới:**
```json
{
  "application_scope": 2,
  "scope_id": 1,
  "industry_id": 5,
  ...
}
```

### 9.2 `POST /assign/form-templates`, `PUT /assign/form-templates/{id}`

**Payload cũ:** `{ name, scope_id, industry_id, application_id, status, meta }`
**Payload mới:** `{ name, scope_id, industry_id, status, meta }`

### 9.3 `GET /assign/questions` (list filter)

- Bỏ query param `application_id`
- Thêm/giữ `industry_id`, `scope_id`
- Option: thêm `include_all_scope=1` để gộp câu hỏi `application_scope = 1`

### 9.4 Response Resource

`SurveyQuestionsResource.php`:
- Bỏ các field `scopes`, `industries`, `applications` (array)
- Giữ `scope`, `industry` (single)

`FormTemplatesResource.php`:
- Bỏ field `application`, `application_id`, `application_name`
- Giữ `scope`, `industry`

## 10. Frontend changes chi tiết

### 10.1 `pages/assign/questions/components/QuestionForm.vue`

- **Data changes:**
  - Bỏ `scopeId`, `industryId`, `applicationId` (computed array)
  - Bỏ prop state `scope_ids`, `industry_ids`, `application_ids` trong `formSubmit`
  - Thêm `scope_id`, `industry_id` (single int) trong `formSubmit`
- **Template:**
  - Bỏ cột `Ứng dụng` và `V2BaseSelect application_ids`
  - Đổi 2 option của `applicationScopeOptions`: `{ id: 2, text: 'Theo nhóm giải pháp' }`
- **Methods:**
  - `onChangeApplicationScope`: khi về 1 → set `scope_id = null`, `industry_id = null`
  - `onChangeScope`: reset `industry_id`
  - Bỏ `onChangeIndustry` reset `application_ids`
- **Watcher:**
  - Bỏ watcher `formSubmit.scope_ids`, `formSubmit.industry_ids`
  - Thêm watcher `formSubmit.scope_id` → reset `industry_id` nếu không còn thuộc scope

### 10.2 `pages/assign/questions/add.vue` + `_id/edit.vue`

- Trong `formSubmit` init: bỏ `scope_ids`, `industry_ids`, `application_ids`; thêm `scope_id: null`, `industry_id: null`

### 10.3 `pages/assign/form-templates/components/FormMeta.vue`

- Bỏ cột Ứng dụng (col-md-3 cuối)
- 3 cột còn lại: Tên form + Nhóm ngành + Nhóm giải pháp → đổi layout `col-md-4` mỗi cột
- Bỏ prop `applicationsAll`, computed `appOptions`, watcher `industryId → appId`
- Bỏ field `appId` khỏi model `localForm`

### 10.4 `pages/assign/form-templates/add.vue` & `_id/edit.vue`

- Bỏ `application_id`/`appId` khỏi payload
- Bỏ `applicationsAll` khỏi state
- Nếu BE trả lỗi 422 field `industry_id` → hiển thị trên FormMeta

### 10.5 `pages/assign/prospective-projects/components/ProjectInfoSection.vue`

- UI giữ nguyên cascading 3 dropdown
- Thêm emit `@industry-changed` khi `formSubmit.industry_id` thay đổi
- Parent `add.vue` / `edit.vue` nghe `@industry-changed` → call API load form_template theo industry:
  ```js
  async onIndustryChanged(industryId) {
      if (!industryId) {
          this.formSubmit.form_template_id = null
          this.formTemplate = null
          return
      }
      const { data } = await this.$store.dispatch('apiGetMethod',
          `assign/form-templates/by-industry/${industryId}`)
      this.formSubmit.form_template_id = data?.id || null
      this.formTemplate = data
  }
  ```
- Khi đổi application trong cùng industry → **KHÔNG** reset form_template_id

### 10.6 `pages/assign/meeting/components/MeetingProject.vue`

- Sửa watcher `application_id` (~dòng 938-941): bỏ reset `form_template_id` khi đổi application cùng industry
- Thêm watcher `industry_id` → reset `form_template_id` và load lại theo industry

### 10.7 FormBuilder — filter câu hỏi

- `pages/assign/form-templates/components/QuestionLibrary.vue`:
  - Filter `application_id` → `industry_id` (lấy từ `form.industry_id` của FormMeta)
  - Bổ sung thêm param `include_all_scope=1` để lấy cả câu hỏi `application_scope = 1`

## 11. API mới/đổi

### 11.1 `GET /assign/form-templates/by-industry/{industryId}` (mới)

- Trả về form template Published của industry đó
- Response: `{ data: { id, name, industry_id, scope_id, sections: [...], ... } | null }`
- Dùng thay cho API cũ `GET /assign/form-templates/by-application/{appId}`

### 11.2 API cũ `GET /assign/form-templates/by-application/{appId}`

- Deprecated (xoá hoặc giữ để tránh break). Vì release BE+FE cùng lúc → có thể xoá luôn.

## 12. Business rules

| ID | Rule |
|---|---|
| BR-1 | Mỗi `industry_id` có tối đa 1 `FormTemplate` với `status = Published` |
| BR-2 | Câu hỏi `application_scope = 1` dùng được cho mọi nhóm giải pháp |
| BR-3 | Câu hỏi `application_scope = 2` phải có cả `scope_id` và `industry_id` |
| BR-4 | FormBuilder filter câu hỏi theo industry của form, cộng thêm câu hỏi BR-2 |
| BR-5 | Dự án TKT / Meeting: form_template match theo `industry_id`; đổi application cùng industry KHÔNG đổi form |
| BR-6 | Edit FormTemplate được phép đổi industry thoải mái (snapshot đã khoá lịch sử) |
| BR-7 | Không thể chuyển FormTemplate từ Draft → Published nếu industry đã có form Published khác (trừ chính nó) |

## 13. Edge cases

| # | Case | Xử lý |
|---|---|---|
| 1 | Industry hiện có nhiều form Published (data cũ) | Migration dedupe: cái mới nhất giữ Published, còn lại → Locked |
| 2 | User tạo form mới cho industry đã có Locked form | Cho phép (Locked ≠ Published) |
| 3 | Snapshot cũ có `application_id` nhưng không có `industry_id` | Không đụng; đọc như cũ |
| 4 | Dự án TKT trỏ đến form bị Locked sau migration | OK — dự án dùng snapshot riêng |
| 5 | Câu hỏi cũ có `application_id` nhưng pivot industry rỗng | Migration backfill từ `application.industry_ids[0]` |
| 6 | FormBuilder: user đổi industry của form có câu hỏi | Cảnh báo nhưng giữ câu hỏi, không auto xoá |
| 7 | Câu hỏi `application_scope = 1` có `scope_id/industry_id` cũ | Migration: set cả 2 về null |

## 14. Downstream cần verify trước khi ship

Chạy các grep sau trong repo để tìm các chỗ còn dùng field cũ, fix nếu có:

```bash
# BE
grep -rn "application_id" hrm-api/Modules/Assign/Transformers/SurveyQuestionsResource/
grep -rn "application_id" hrm-api/Modules/Assign/Transformers/FormTemplatesResource/
grep -rn "survey_question_applications" hrm-api/
grep -rn "FormTemplate::.*application" hrm-api/
grep -rn "->applications()" hrm-api/Modules/Assign/

# FE
grep -rn "application_ids" hrm-client/pages/assign/
grep -rn "by-application" hrm-client/pages/assign/
grep -rn "form_template" hrm-client/pages/assign/
```

Các báo cáo trong `Modules/Assign/Services/Report/*` nếu có join tới `form_templates.application_id` → cần update.

## 15. Rollout

1. **PR 1 (BE data migration only):** migration backfill industry_id + dedupe form Published. Deploy riêng, không gãy UI cũ.
2. **PR 2 (BE + FE code):** drop cột + pivot, update model/service/request/resource + FE thay đổi toàn bộ. Deploy cùng release (BE drop cột → FE cũ gãy ngay nếu deploy lệch).

## 16. Testing

Manual test cases sẽ viết sau theo format của `feedback_testcase_end_user`:
- Câu hỏi: tạo mới với scope `Tất cả` / `Theo nhóm giải pháp`, edit, xoá
- Mẫu phiếu: tạo mới với industry chưa có → OK; tạo mới với industry đã có Published → chặn cứng; edit (cho phép đổi industry)
- Dự án TKT: chọn industry → form template auto-load; đổi application cùng industry → form giữ nguyên; đổi industry → reset form
- Meeting: tạo nhanh dự án TKT, cùng các case như trên
