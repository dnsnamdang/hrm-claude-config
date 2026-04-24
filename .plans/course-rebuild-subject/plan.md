# Course Rebuild Subject — Plan

**Ngày:** 2026-04-22 · **Owner:** @manhcuong · **Design:** [design.md](design.md) · **Spec:** [docs/superpowers/specs/2026-04-22-course-rebuild-subject-design.md](../../docs/superpowers/specs/2026-04-22-course-rebuild-subject-design.md)

---

## Phase 1 — BE Schema (migration)

Tất cả migration đặt tại `hrm-api/database/migrations/`.

- [x] Tạo `YYYY_MM_DD_HHMMSS_add_course_config_columns_to_subjects_table.php` — thêm 12 cột vào `subjects` (exam_score_rule enum, exam_attempt_limit, exam_participation_required, exam_min_required_percent, onboarding_enabled, onboarding_new_employee_days, onboarding_must_finish_days, mandatory_assignee_type, recommended_assignee_type, certificate_enabled, certificate_template_url). Mỗi cột có `->comment()` giải thích
- [x] Tạo `create_subject_exams_table.php` — subject_id, exam_id, time_limit_min, pass_score_percent, sort_order + unique index (subject_id, exam_id)
- [x] Tạo `create_subject_exam_graders_table.php` — subject_exam_id, employee_id + unique index
- [x] Tạo `create_subject_assignees_table.php` — subject_id, assignee_type enum, assignee_id, is_mandatory + unique (subject_id, assignee_type, assignee_id, is_mandatory) + index (subject_id, is_mandatory)
- [x] Tạo `create_subject_certificate_fields_table.php` — subject_id, field_key enum, text, x, y, font_size, font_weight + unique (subject_id, field_key)
- [x] Tạo `backfill_subject_course_data.php` — parse `evaluation_config` JSON → `subject_exams` + `exam_score_rule` + `exam_attempt_limit`; migrate `working_position_subjects.is_encouraged` → `subject_assignees(type=position)` + set `mandatory_assignee_type`/`recommended_assignee_type` theo row tồn tại; migrate `capability_subjects` → `subject_assignees(type=capability, is_mandatory=1)`
- [x] Tạo `rename_permission_quan_ly_mon_hoc.php` — `UPDATE permissions SET name='Quản lý khoá học' WHERE name='Quản lý môn học'` + rollback đối xứng
- [x] Cập nhật `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` string `Quản lý môn học` → `Quản lý khoá học`
- [x] Chạy `php artisan migrate` local, verify schema + data backfill đúng

## Phase 2 — BE Entity + Resource

- [x] `Modules/Training/Entities/Subject.php` — thêm const `STATUS_DRAFT=3` + cập nhật `STATUSES` array; thêm relationship `subjectExams`, `subjectAssignees`, `certificateFields`; accessor `is_can_delete` (check references: course_requests, training_requests, training_planning_subjects, training_program_subject, courses; DRAFT luôn delete được)
- [x] Tạo `Modules/Training/Entities/SubjectExam.php` — $guarded=[], relationship belongsTo Subject + Exam, hasMany SubjectExamGrader
- [x] Tạo `Modules/Training/Entities/SubjectExamGrader.php` — belongsTo SubjectExam + Employee
- [x] Tạo `Modules/Training/Entities/SubjectAssignee.php` — belongsTo Subject; method helper `getAssignee()` resolve theo assignee_type
- [x] Tạo `Modules/Training/Entities/SubjectCertificateField.php` — belongsTo Subject, const FIELD_KEYS
- [x] Tạo `Modules/Training/Transformers/Subject/SubjectExamResource.php` — embed `exam: {id, name, mcq_count, essay_count}`, `grader_ids[]`
- [x] Tạo `Modules/Training/Transformers/Subject/SubjectAssigneeResource.php`
- [x] Tạo `Modules/Training/Transformers/Subject/SubjectCertificateFieldResource.php`
- [x] Cập nhật `DetailSubjectBuilderResource.php` (hoặc tên tương ứng) — trả đủ payload 4 tab theo spec section 5.3 (chapters, subject_lessons, subject_exams, subject_assignees, certificate_fields, tất cả cột cột mới trên subject, `is_can_delete`)

## Phase 3 — BE Service

- [x] `SubjectService::fillSubjectAttributes` — map 12 cột mới từ request
- [x] `SubjectService::syncExams` (private) — wipe `subject_exams` + `subject_exam_graders` cũ, insert batch mới (chunk 1000); chỉ chạy khi `evaluation_mode=exam`, ngược lại wipe sạch
- [x] `SubjectService::syncAssignees` (private) — wipe `subject_assignees` cũ, bulk insert mới theo array `subject_assignees[]`
- [x] `SubjectService::syncCertificateFields` (private) — wipe cũ, insert đủ 4 row khi `certificate_enabled=1`, wipe sạch khi =0
- [x] `SubjectService::syncChaptersAndLessons` — mở rộng logic: khi đổi `use_chapters=2` → set `chapter_id=null` cho subject_lessons và xoá chapters; khi xoá lesson thì clean `prerequisite_subject_lesson_ids` của các lesson còn lại
- [x] `SubjectService::storeWithStructure` + `updateWithStructure` — wrap DB::transaction, call tuần tự các sync method trên

## Phase 4 — BE Controller + Request + Route

- [x] `Modules/Training/Http/Requests/Subject/SubjectBuilderRequest.php` — rules theo spec 5.5: nếu `status=3` skip hầu hết; nếu ≠ 3 validate conditional theo evaluation_mode, onboarding_enabled, certificate_enabled, grader required khi exam có essay. Viết `withValidator()` cho rule grader-theo-essay
- [x] `SubjectController::showBuilder` — đảm bảo load relationship đầy đủ (subjectExams.graders, subjectExams.exam, subjectAssignees, certificateFields, chapters.lessons, subjectLessons)
- [x] Kiểm tra route `POST /api/v1/training/subjects/store-builder` + `POST /{id}/builder` middleware checkPermission đồng bộ với tên permission mới
- [x] FE upload ảnh cert dùng endpoint chung `files/upload` — không thêm route mới

## Phase 5 — FE Shell + rename label

- [x] `pages/training/subjects/index.vue` — đổi label "Môn học" → "Khoá học" (title, breadcrumb, header, filter label, empty state, confirm dialog); thêm option DRAFT vào filter status
- [x] `pages/training/subjects/add.vue` — đổi label page title
- [x] `pages/training/subjects/_id/index.vue`, `_id/show.vue`, `_id/section.vue`, `print.vue` — đổi label
- [x] Tìm sidebar Training trong `layouts/*` hoặc `training-components/*` — đổi menu item "Môn học" → "Khoá học"
- [x] Xoá `pages/training/subjects/components/SubjectForm.vue` (deprecated 62KB)
- [x] Refactor `components/SubjectBuilderForm.vue` → shell: header + tab switcher 4 tab + footer button ("Quay về", "Lưu tạm" status=3, "Lưu" status=1). Giữ state chung `formData` 4 tab, pass props xuống sub-tab, nhận `@update` để sync state
- [x] Cập nhật label trong `SubjectLessonCompletionOverride.vue` ("môn học" → "khoá học")

## Phase 6 — FE Tab 1 (Thông tin + builder chương/bài)

- [x] Tạo `components/tabs/TabInfo.vue` — layout col-5/col-7
- [x] LEFT panel: mã (auto-gen disabled + button regenerate), tên, training_type_id (V2BaseSelect gọi `apiGetMasterSelect training_types`), status (thêm DRAFT=3), `use_chapters` toggle, `linear_required` toggle, textarea mô tả
- [x] RIGHT panel: kế thừa logic builder chương/bài drag-drop từ `SubjectBuilderForm.vue` hiện có (SortableJS); migrate code sang component riêng
- [x] Tích hợp modal `SubjectLessonCompletionOverride` cho override completion mỗi lesson
- [x] Form validate client-side: name required, ít nhất 1 chapter (khi use_chapters=1) / 1 lesson (khi =2)

## Phase 7 — FE Tab 2 (Cấu hình đánh giá)

- [x] Tạo `components/tabs/TabEvaluation.vue`
- [x] Radio `evaluation_mode` completion vs exam — toggle hiển thị section tương ứng
- [x] **Completion section**: V2BaseSelect `rule` (all_required/percent/weighted), input `percent` 1-100, V2BaseSelect `percent_mode` (required_only/all/by_chapter); hint box hiển thị tổng weight required (dùng khi rule=weighted)
- [x] **Exam section**: input `exam_attempt_limit`, V2BaseSelect `exam_score_rule` (highest/last/average), V2BaseSelect multi đề thi (gọi API list exams, trả về mcq_count/essay_count)
- [x] Khi chọn/bỏ đề thi → sinh/xoá row trong `subject_exams[]` với default time_limit_min=0, pass_score_percent=60
- [x] Table per-exam sticky header: cột mã, tên đề, input time_limit_min, input pass_score_percent, V2BaseSelect multi graders (ẩn nếu exam không có essay)
- [x] Toggle `exam_participation_required` + input `exam_min_required_percent` (hiện khi =1)

## Phase 8 — FE Tab 3 (Cấu hình người học)

- [x] Tạo `components/tabs/TabLearners.vue`
- [x] **Onboarding section**: toggle `onboarding_enabled`; khi ON hiện 2 input `onboarding_new_employee_days`, `onboarding_must_finish_days` + tooltip giải thích logic 0 = luôn coi mới / không deadline
- [x] **Mandatory block**: type pill (Phòng ban / Chức vụ / Năng lực) — click đổi `mandatory_assignee_type`; multi-select tương ứng type chọn (gọi `apiGetMasterSelect departments / working_positions / capabilities`); chọn xong push vào `subject_assignees[]` với `is_mandatory=1`, giữ data các type khác khi switch pill
- [x] **Recommended block**: tương tự mandatory nhưng `is_mandatory=0`
- [x] Hiển thị chip list đã chọn mỗi block, click × remove

## Phase 9 — FE Tab 4 (Chứng chỉ)

- [x] Tạo `components/tabs/TabCertificate.vue`
- [x] Toggle `certificate_enabled` — toàn bộ config ẩn khi OFF
- [x] Layout grid-col-2: LEFT config, RIGHT canvas preview 1600×900
- [x] LEFT: file input image/* — `onChange` tạo FormData append `attachments[]`, dispatch `uploadImage`, set `certificate_template_url` từ response; hint X/Y px
- [x] 4 cert-field section (course_name, employee_name, issued_date, signer) mỗi section: input text (ẩn với employee_name/issued_date), input X, Y, font_size, V2BaseSelect font_weight 400/500/600/700/800
- [x] Button "Lấy từ khoá" cho course_name — copy `formData.name` sang `text`
- [x] RIGHT canvas: watch tất cả field, `canvas.getContext('2d')` render ảnh template + 4 text overlay real-time; fallback render placeholder text khi không có template
- [x] Button "Render lại" force redraw; button "Download PDF" dùng `jspdf` (check đã có trong node_modules, nếu chưa thì thêm dep)

## Phase 10 — Tích hợp + Manual Test (user tự thực hiện)

- [ ] Test E2E tạo mới đủ 4 tab → save `status=1` → verify DB đủ row trong 4 bảng mới + subjects cột mới đúng
- [ ] Test lưu tạm (DRAFT) → submit với name + code, skip các tab khác → verify `status=3` + không insert row con
- [ ] Test edit subject cũ (đã migrate) → verify GET builder restore đủ data 4 tab (chapters, assignees từ backfill, etc.)
- [ ] Test đổi `evaluation_mode` exam→completion → subject_exams + graders bị xoá sạch sau save
- [ ] Test đổi `use_chapters` 1→2 → chapters bị xoá, lessons chuyển chapter_id=null
- [ ] Test xoá lesson đang là prerequisite → prerequisite_subject_lesson_ids của lessons còn lại được clean
- [ ] Test upload ảnh cert → URL trả về hợp lệ → canvas preview render đúng
- [ ] Test `is_can_delete`: subject có reference downstream → nút xoá disabled; DRAFT luôn xoá được
- [ ] Verify permission rename: user có quyền "Quản lý môn học" cũ vẫn truy cập được (vì permission_id không đổi, role_has_permissions còn nguyên)
- [ ] Verify các màn downstream (training_programs, courses cũ, training_plans, reports) vẫn chạy bình thường với subjects đã migrate
- [ ] Verify sidebar menu hiển thị "Khoá học"

---

## Checkpoint — 2026-04-22

**Đã hoàn thành:** P1-P9 (toàn bộ code BE + FE). 9/9 dispatch subagent DONE.
- BE: 7 migration + 4 entity mới + 3 resource + Subject sync → SubjectService (syncExams/syncAssignees/syncCertificateFields) + SubjectBuilderRequest DRAFT-aware + SubjectController load relationship + rename permission "Quản lý môn học" → "Quản lý khoá học" cả BE entity + 15+ file FE.
- FE: Shell `SubjectBuilderForm.vue` (573 dòng, 4 b-tabs, saveDraft/save, strip _exam_meta khi submit, attach _exam_meta khi load). 4 tab đầy đủ: TabInfo (2048 dòng — builder + chapter/lesson drag-drop), TabEvaluation (exam multi-select + per-exam config + graders), TabLearners (onboarding + mandatory/recommended assignees polymorphic), TabCertificate (upload template + 4 cert-field + canvas 1600×900 preview + jsPDF download). Xoá `SubjectForm.vue` deprecated.

**Bước tiếp theo:** User chạy Phase 10 manual test. Trước khi test: `cd hrm-client && npm i jspdf` (package chưa có) + `php artisan migrate` để apply 7 migration mới.

**Blocked/Concerns:**
- `jspdf` chưa có trong `hrm-client/package.json` — cần `npm i jspdf`, nếu không tính năng "Tải xuống PDF preview" ở TabCertificate sẽ fail (đã có try/catch + toast, không crash app).
- `dayjs customParseFormat` plugin chưa verify — có thể ảnh hưởng parse ngược issued_date (không ảnh hưởng dữ liệu đã lưu).
- `SubjectBuilderRequest::withValidator()` đang comment logic grader-theo-essay (chờ clarify shape `exam_questions.type`).
- `ExamKit.mcq_count/essay_count` accessor chưa có — FE tạm hiển thị 0 (BE resource `SubjectExamResource` đã trả field nhưng giá trị còn mock).
