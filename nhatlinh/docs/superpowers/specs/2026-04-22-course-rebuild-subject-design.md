# Course Rebuild Subject — Design Spec

**Ngày:** 2026-04-22
**Owner:** @manhcuong
**Trạng thái:** Draft — chờ user review

---

## 1. Mục tiêu

- Rebuild FE màn tạo/sửa `subjects` (module Training) theo prototype `hrm-client/pages/training/subjects/Course_create.html` — 4 tab đầy đủ: Thông tin + builder chương/bài, Cấu hình đánh giá, Cấu hình người học, Chứng chỉ.
- Đổi label hiển thị "Môn học" → "Khoá học" **chỉ trên các màn trực tiếp** của subjects (index/add/edit/builder) + sidebar menu. Các màn downstream (training_programs, courses, training_plans, reports...) giữ nguyên label "Môn học".
- BE thêm cột/bảng mới support tính năng còn thiếu, migrate data cũ.
- Logic các luồng downstream (kế hoạch, gán học viên, báo cáo) **không thay đổi** — subjects vẫn hoạt động như cũ.

## 2. Ranh giới (scope)

### In scope
- FE: `pages/training/subjects/index.vue`, `add.vue`, `_id/index.vue`, `_id/show.vue`, `components/SubjectBuilderForm.vue` (rebuild 4 tab thành shell + 4 sub-tab), `components/SubjectLessonCompletionOverride.vue` (label only).
- FE: xoá `components/SubjectForm.vue` (62KB, deprecated).
- FE: sidebar menu item Training — rename label "Môn học" → "Khoá học".
- BE: entity `Subject` + service `SubjectService` + controller + FormRequest + resource. Upload cert template tái sử dụng endpoint chung `POST /files/upload` (không thêm route mới).
- BE: 4 bảng mới + 12 cột mới vào `subjects`.
- Migration backfill data hiện có.
- Migration rename permission `Quản lý môn học` → `Quản lý khoá học` (cập nhật cả `PermissionsTableSeeder.php`).

### Out of scope
- Màn downstream: giữ label "Môn học" và logic cũ.
- Export Excel subjects — giữ format cũ.
- Luồng auto-assign onboarding thực tế (chỉ lưu config, job auto-assign là feature riêng sau).
- Luồng render PDF chứng chỉ thực tế khi cấp cho học viên (chỉ lưu config, preview ở form).
- Entity `courses` (khoá học cũ trong DB) — không động tới.

## 3. Kiến trúc tổng thể

### 3.1. Luồng user
1. User vào `/training/subjects` — page "Danh sách khoá học".
2. Nhấn "Thêm" → `SubjectBuilderForm` render 4 tab.
3. User điền tab 1 → tab 2 → tab 3 → tab 4 (có thể nhảy tab tự do, state giữ trong component shell).
4. "Lưu tạm" = submit với `status=3 (DRAFT)`, skip hầu hết validation.
5. "Lưu" = submit với `status=1 (HOAT_DONG)` hoặc `2 (KHOA)`, validate đầy đủ.
6. Edit: `GET /subjects/{id}/builder` trả đủ 4 tab data → sửa → `POST /subjects/{id}/builder`.

### 3.2. FE component tree (thư mục `pages/training/subjects/components/`)
```
SubjectBuilderForm.vue           (shell — giữ state 4 tab, tab switcher, footer actions)
├── TabInfo.vue                  (Tab 1: info + builder chương/bài drag-drop)
│   └── SubjectLessonCompletionOverride.vue (tái sử dụng)
├── TabEvaluation.vue            (Tab 2: completion vs exam config)
├── TabLearners.vue              (Tab 3: onboarding + mandatory/recommended)
└── TabCertificate.vue           (Tab 4: upload ảnh + 4 field + canvas preview)
```
- `SubjectForm.vue` — XOÁ.

## 4. Database schema

### 4.1. Cột thêm vào `subjects`

| Cột | Type | Nullable | Default | Ghi chú |
|---|---|---|---|---|
| `exam_score_rule` | enum('highest','last','average') | YES | null | Áp khi evaluation_mode=exam |
| `exam_attempt_limit` | int | YES | null | Số lần thi tối đa |
| `exam_participation_required` | tinyint | NO | 0 | 0=không, 1=bắt buộc học trước |
| `exam_min_required_percent` | int | YES | null | % tối thiểu khi =1 |
| `onboarding_enabled` | tinyint | NO | 0 | |
| `onboarding_new_employee_days` | int | YES | null | 0 = luôn coi là mới |
| `onboarding_must_finish_days` | int | YES | null | 0 = không giới hạn |
| `mandatory_assignee_type` | enum('department','position','capability') | YES | null | Type pill Mandatory |
| `recommended_assignee_type` | enum('department','position','capability') | YES | null | Type pill Recommended |
| `certificate_enabled` | tinyint | NO | 0 | |
| `certificate_template_url` | string(500) | YES | null | S3 URL ảnh mẫu |

Cột `status` đã tồn tại (tinyint) — thêm giá trị `3=DRAFT` (không đổi type).

### 4.2. Bảng `subject_exams`
```
id                       unsignedBigInteger PK
subject_id               unsignedBigInteger  -- FK soft → subjects
exam_id                  unsignedBigInteger  -- FK soft → exams
time_limit_min           int default 0
pass_score_percent       int default 60
sort_order               int default 0
created_at, updated_at
```
Index: `(subject_id, exam_id)` unique, `(subject_id)`.

### 4.3. Bảng `subject_exam_graders`
```
id                       unsignedBigInteger PK
subject_exam_id          unsignedBigInteger  -- FK soft → subject_exams
employee_id              unsignedBigInteger  -- FK soft → employees
created_at, updated_at
```
Index: `(subject_exam_id, employee_id)` unique. Chỉ insert khi exam có essay questions.

### 4.4. Bảng `subject_assignees` (polymorphic)
```
id                       unsignedBigInteger PK
subject_id               unsignedBigInteger
assignee_type            enum('department','position','capability')
assignee_id              unsignedBigInteger  -- FK soft tương ứng
is_mandatory             tinyint   -- 0=recommended, 1=mandatory
created_at, updated_at
```
Index: `(subject_id, assignee_type, assignee_id, is_mandatory)` unique, `(subject_id, is_mandatory)`.

### 4.5. Bảng `subject_certificate_fields`
```
id                       unsignedBigInteger PK
subject_id               unsignedBigInteger  -- FK soft → subjects
field_key                enum('course_name','employee_name','issued_date','signer')
text                     string(255) nullable  -- course_name/signer cố định; employee_name/issued_date null (fill runtime)
x                        int default 800
y                        int default 450
font_size                int default 32
font_weight              int default 500
created_at, updated_at
```
Index: `(subject_id, field_key)` unique. Max 4 row/subject.

### 4.6. Backfill

1. **Parse `subjects.evaluation_config` JSON** (nếu có):
   - `evaluation_config.exams[]` → insert `subject_exams` (time_limit_min, pass_score_percent từ JSON; thiếu → default 0, 60).
   - `evaluation_config.score_rule` → `subjects.exam_score_rule`.
   - `evaluation_config.attempt_limit` → `subjects.exam_attempt_limit`.
   - **Giữ nguyên JSON** cho backward-compat, không xoá.
2. **`working_position_subjects` pivot:**
   - `is_encouraged=true` → `subject_assignees(type=position, is_mandatory=0)`.
   - `is_encouraged=false` → `subject_assignees(type=position, is_mandatory=1)`.
   - Set `subjects.mandatory_assignee_type='position'` / `recommended_assignee_type='position'` tuỳ có row tương ứng.
3. **`capability_subjects`:** → `subject_assignees(type=capability, is_mandatory=1)`.
4. **Default** các cột mới: `onboarding_enabled=0`, `certificate_enabled=0`, `exam_participation_required=0`.
5. **Không migrate** record có `exam_kit_id` nhưng không có JSON `exams` — user tự nhập khi edit.

## 5. API contract

### 5.1. Endpoints

| Method | Path | Mục đích |
|---|---|---|
| `GET` | `/api/v1/training/subjects` | List — không đổi |
| `GET` | `/api/v1/training/subjects/{id}/builder` | Load 4 tab data (mở rộng response) |
| `POST` | `/api/v1/training/subjects/store-builder` | Tạo mới (mở rộng payload) |
| `POST` | `/api/v1/training/subjects/{id}/builder` | Cập nhật (mở rộng payload) |
| `DELETE` | `/api/v1/training/subjects/{id}/builder` | Xoá — không đổi |

Upload ảnh cert template dùng endpoint chung `POST /api/v1/files/upload` (store action `uploadImage`) — giống pattern `FileAttachmentTable.vue`. **Không tạo endpoint riêng** cho subject.

### 5.2. Payload `store-builder` / `{id}/builder`

```json
{
  "code": "SUB-0001",
  "name": "Khoá A",
  "training_type_id": 1,
  "status": 3,
  "use_chapters": 1,
  "linear_required": 2,
  "description": "...",
  "chapters": [{"code": "CH-01", "name": "...", "sort_order": 1, "lessons": [...]}],
  "subject_lessons": [
    {"lesson_id": 10, "sort_order": 1, "required": 1, "weight": 2,
     "override_completion": 1, "tracking_completion_override": {...},
     "prerequisite_mode": "ALL", "prerequisite_subject_lesson_ids": []}
  ],

  "evaluation_mode": "exam",
  "evaluation_config": {"rule": "percent", "percent": 80, "percent_mode": "required_only"},
  "exam_kit_id": null,
  "exam_score_rule": "highest",
  "exam_attempt_limit": 3,
  "exam_participation_required": 1,
  "exam_min_required_percent": 80,
  "subject_exams": [
    {"exam_id": 10, "time_limit_min": 60, "pass_score_percent": 70, "sort_order": 1, "grader_ids": [5, 6]}
  ],

  "onboarding_enabled": 1,
  "onboarding_new_employee_days": 30,
  "onboarding_must_finish_days": 60,
  "mandatory_assignee_type": "position",
  "recommended_assignee_type": "department",
  "subject_assignees": [
    {"assignee_type": "position", "assignee_id": 12, "is_mandatory": 1},
    {"assignee_type": "department", "assignee_id": 3, "is_mandatory": 0}
  ],

  "certificate_enabled": 1,
  "certificate_template_url": "https://s3.../cert-template-xyz.png",
  "certificate_fields": [
    {"field_key": "course_name",   "text": "{course}", "x": 800, "y": 380, "font_size": 40, "font_weight": 700},
    {"field_key": "employee_name", "text": null,       "x": 800, "y": 470, "font_size": 36, "font_weight": 600},
    {"field_key": "issued_date",   "text": null,       "x": 800, "y": 560, "font_size": 24, "font_weight": 400},
    {"field_key": "signer",        "text": "Nguyễn A", "x": 1200,"y": 720, "font_size": 24, "font_weight": 500}
  ]
}
```

### 5.3. Response `GET /{id}/builder`
Trả tất cả field trên + `id`, `created_at`, `updated_at`, `is_can_delete`. 1 Detail Resource duy nhất.
- `subject_exams[]` embed `exam: {id, name, mcq_count, essay_count}` + `grader_ids[]`.
- `subject_assignees[]` raw array, FE group client-side.
- `certificate_fields[]` sort theo `field_key` enum order.

### 5.4. Upload cert template
- Dùng store action có sẵn `uploadImage` → `POST /api/v1/files/upload` (giống `FileAttachmentTable.vue`).
- FE: khi user chọn file → `FormData.append('attachments[]', file)` → `this.$store.dispatch('uploadImage', formData)` → nhận URL (file_path) từ response → set vào `certificate_template_url` → submit chung khi lưu subject.
- Validate FE: image png/jpg, max 5MB (client-side).
- File mồ côi (user cancel form hoặc đổi template) — chấp nhận, không cleanup.

### 5.5. FormRequest `SubjectBuilderRequest`
- Nếu `status=3 (DRAFT)` → chỉ require `name`, `code`, skip mọi validation khác.
- Nếu `status≠3`:
  - `evaluation_mode=exam` → `subject_exams.required|array|min:1`, `exam_attempt_limit.required|int|min:1`, `exam_score_rule.required|in:highest,last,average`.
  - `evaluation_mode=completion` → `evaluation_config.rule.required|in:all_required,percent,weighted`.
  - `onboarding_enabled=1` → `onboarding_new_employee_days.required|int|min:0`, `onboarding_must_finish_days.required|int|min:0`.
  - `certificate_enabled=1` → `certificate_template_url.required|url`, `certificate_fields.required|array|size:4`.
  - Nếu bất kỳ `subject_exams[i].exam` có essay → `subject_exams[i].grader_ids.required|array|min:1`.

## 6. Business rules

### 6.1. Đánh giá (Tab 2)
**Completion mode:**
- `rule=all_required`: đạt khi hoàn thành tất cả lesson `required=1`.
- `rule=percent`: `% hoàn thành >= evaluation_config.percent`, cách tính theo `percent_mode`:
  - `required_only`: (completed required) / (total required)
  - `all`: (completed) / (total lessons)
  - `by_chapter`: mọi chương đạt ngưỡng
- `rule=weighted`: `sum(weight đã hoàn thành) / sum(weight required) >= evaluation_config.percent`.

**Exam mode:**
- Học viên thi các exam trong `subject_exams`, tối đa `exam_attempt_limit` lần/exam.
- Điểm cuối/exam = theo `exam_score_rule` (highest/last/average).
- Đạt exam: `score >= pass_score_percent`. Đạt khoá: đạt **tất cả** exam.
- Nếu `exam_participation_required=1`: học viên phải hoàn thành ≥ `exam_min_required_percent`% bài required trước khi được thi.

### 6.2. Người học (Tab 3)
- `mandatory_assignee_type` / `recommended_assignee_type` = type pill hiện chọn trên UI (giữ để restore khi edit). Không hạn chế dữ liệu lưu: `subject_assignees` có thể chứa nhiều type cùng lúc (khi user switch pill, data cũ giữ lại).
- Onboarding auto-assign = **downstream feature**, không implement trong scope này. Chỉ lưu config.

### 6.3. Chứng chỉ (Tab 4)
- Khi `certificate_enabled=1`: enforce tồn tại đủ 4 row `subject_certificate_fields`.
- `employee_name` và `issued_date`: `text=null`, runtime thay bằng tên học viên + ngày cấp.
- `course_name` và `signer`: user nhập cứng.
- Canvas preview FE 1600×900: render ảnh template + 4 text overlay. PDF download dùng `jspdf` (client-side).
- Render PDF thực khi cấp = downstream.

### 6.4. Accessor `is_can_delete`
Cấm xoá khi tồn tại tham chiếu từ:
- `course_requests`
- `training_requests`
- `training_planning_subjects`
- `training_program_subject`
- `courses`

DRAFT (status=3) **luôn xoá được**, bỏ qua rule trên.

## 7. Edge cases

| Case | Xử lý |
|---|---|
| DRAFT save → edit lại tab 2/3/4 trống | OK, default. Validate chỉ khi đổi status. |
| Đổi `evaluation_mode` exam→completion đã có `subject_exams` | Xoá sạch `subject_exams` + `subject_exam_graders`. Không cảnh báo. |
| Đổi `use_chapters` 1→2 đã có chapters | Set `subject_lessons.chapter_id=null`, xoá `subject_chapters`. Không cảnh báo. |
| Xoá lesson đang là prerequisite | Service clean `prerequisite_subject_lesson_ids` của lessons còn lại. |
| Exam có essay chưa chọn grader | Validate 422. |
| Upload cert S3 → user cancel form | File mồ côi, không cleanup (chấp nhận). |
| User đổi template khi edit | URL cũ mồ côi, không cleanup. |
| `onboarding_new_employee_days=0` | Áp cho tất cả nhân viên mandatory, không filter ngày. |
| `onboarding_must_finish_days=0` | Không có deadline. |
| Đổi `exam_score_rule` khi đã có attempt | Áp từ attempt mới, attempt cũ giữ. |
| Record cũ có `exam_kit_id` nhưng JSON không có `exams` | Không migrate, user tự nhập khi edit. |

## 8. Label rename

### 8.1. Files FE đổi label "Môn học" → "Khoá học"
- `pages/training/subjects/index.vue` — page title, breadcrumb, header, filter label, empty state, confirm dialog.
- `pages/training/subjects/add.vue` — page title.
- `pages/training/subjects/_id/index.vue`, `show.vue`, `section.vue` — page title, header.
- `pages/training/subjects/print.vue` — title.
- `pages/training/subjects/components/SubjectBuilderForm.vue` + 4 sub-tab — toàn bộ label/placeholder/toast/button.
- `pages/training/subjects/components/SubjectLessonCompletionOverride.vue` — label có "môn học".
- Sidebar Training menu (trong `training-components/` hoặc `layouts/training.vue`) — menu item.

### 8.2. Không đổi
- File ngoài `pages/training/subjects/` (training_programs, courses cũ, training_plans, reports...).
- Message `resources/lang/vi/validation.php` — chỉ đổi key nào CHỈ dùng trên màn subjects.
- Permission **key DB** — giữ nguyên logic, nhưng migration rename string `Quản lý môn học` → `Quản lý khoá học` (cả `permissions.name` và `PermissionsTableSeeder.php`). role_has_permissions dùng `permission_id` nên không vỡ gán quyền.

## 9. Rollout

Toàn bộ 7 migration đặt ở **project-level** `hrm-api/database/migrations/` (consistency với file cũ `2026_03_07_122321_add_subject_config_columns_to_subjects_table.php`).

1. Chạy 7 migration theo thứ tự (schema trước, backfill, rename permission).
2. Deploy code.
3. Không cần feature flag (cột mới nullable/default, không vỡ code cũ).
4. Rollback: `migrate:rollback --step=7`.

## 10. Open questions

Không còn. Mọi quyết định đã confirmed trong brainstorming 2026-04-22.

## 11. Downstream impact

Không có. Các bảng pivot cũ (`working_position_subjects`, `capability_subjects`) giữ nguyên schema — backfill chỉ đọc từ đó sang `subject_assignees`, không xoá. Các module khác query `subjects` qua `id`/`code`/`name` vẫn hoạt động bình thường.
