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

## Phase 12 — Bug fix error handling + evaluation_config mismatch (2026-04-25, @junfoke)

- [x] Thêm method `applyBackendErrors()` trong `SubjectBuilderForm.vue`: map toàn bộ key lỗi 422 từ backend vào `this.error` (lấy phần tử đầu nếu là array), tự động chuyển đúng tab (0=Thông tin, 1=Đánh giá, 2=Người học, 3=Chứng chỉ) dựa trên key lỗi
- [x] Fix `save()`: thay logic cứng 3 key (`code`, `subject_lessons`, `chapters`) bằng `applyBackendErrors()`. Không còn set `formError` generic khi validate client-side thất bại
- [x] Fix `saveDraft()`: trước đây bỏ qua toàn bộ lỗi field khi có lỗi server 422; nay gọi `applyBackendErrors()`. Fix lỗi tên trống hiển thị banner đỏ thay vì inline dưới field — đổi thành `this.error = { name: 'Vui lòng nhập tên khoá học' }` + switch tab 0
- [x] Fix mismatch tên field `evaluation_config`: frontend dùng `completion_rule`/`required_percent`/`percent_count_mode` nhưng backend validate `rule`/`percent`/`percent_mode`. Fix trong `buildEvaluationConfigPayload()` (remap khi gửi lên) và `loadBuilder()` (map ngược khi đọc về, có fallback cả 2 tên)

**File thay đổi:** `hrm-client/pages/training/subjects/components/SubjectBuilderForm.vue`

---

## Phase 10b — Bug fix round 1 (2026-04-25, @junfoke)

- [x] Fix `TabCertificate.vue` — `downloadPdf()` dùng `localPreviewDataUrl` thay vì canvas → không có text overlay. Fix: luôn dùng `canvas.toDataURL()`, thêm `crossOrigin='anonymous'` trong `loadTemplateImage()` (có fallback khi S3 chưa cấu hình CORS), thêm `renderOffscreen()` dùng canvas mới khi main canvas bị taint (SecurityError)
- [x] Fix `index.vue` — `getStatusText()`/`getStatusClass()` chỉ check status 1, mọi status khác đều trả về "Khoá". Thêm case status 3 → "Nháp" + badge xám (`badge-secondary`)
- [x] Fix `index.vue` — `.row-actions` không sát viền phải. Fix: `position: absolute; right: 8px; top: 50%; transform: translateY(-50%)` + wrapper cell thêm `position-relative`
- [x] Fix `Subject.php` — `canEdit()` chỉ cho phép `HOAT_DONG`. Fix: thêm `STATUS_DRAFT` vào mảng `in_array()` để nút sửa hiện với khoá học Nháp
- [x] Fix `add.vue`, `_id/index.vue`, `_id/show.vue` — sidebar menu đè lên nội dung form (do `custom.scss` set `.content-page { margin-left: 0 }`, sidebar fixed-position không nhường chỗ). Fix: thêm `mounted() { document.body.setAttribute('data-sidebar-size', 'condensed') }` vào cả 3 page

**File thay đổi:** `TabCertificate.vue`, `index.vue`, `Subject.php`, `add.vue`, `_id/index.vue`, `_id/show.vue`

---

## Phase 10c — Bug fix modal Ngân hàng bài học + UI prototype (2026-04-25, @junfoke)

- [x] Điều tra modal "Ngân hàng bài học" hiển thị trống: nguyên nhân là bảng `lessons` không có dữ liệu (0 rows). Fix tạm: seed 8 lesson test qua `php artisan tinker` với `company_id=1` + `tracking_completion` JSON. Code fetch (`training/lessons/getAll`) là đúng
- [x] Fix UI modal lần 1 (sai): thêm `picker-filter-bar` phức tạp (dropdown loại bài học + nút reset) — user từ chối vì không đúng prototype
- [x] Fix UI modal lần 2 (đúng): đọc prototype `Course_create.html` (line ~1515-1583) và implement đúng theo mẫu:
  - Info row "Thêm bài học vào: [chương]" + mini-badge số lượng
  - `searchbox` đơn giản (icon + input + nút ×), không có type filter
  - Table 5 cột: Mã / Tên bài học / Loại / Tiêu chí hoàn thành (mặc định) / Thêm
  - Cột "Tiêu chí hoàn thành" dùng `formatDefaultCompletion(les)`
  - `hint-box` ở dưới với chuẩn nghiệp vụ
- [x] Thêm computed `pickerTargetLabel` trong `TabInfo.vue`
- [x] Dọn sạch CSS `picker-filter-bar` từ lần thử đầu trong `subject-builder.scss`

**Bài học quan trọng:** Luôn đọc `Course_create.html` trước khi thay đổi UI bất kỳ màn nào trong subject builder.

**File thay đổi:** `TabInfo.vue`, `subject-builder.scss`

---

## Phase 11 — Bug fix UI / Modal (2026-04-25, @junfoke)

- [x] Fix UI filter trong modal "Ngân hàng bài học" (`subject-lesson-picker-modal` trong `TabInfo.vue`): thay `.searchbox` tự viết bằng `form-row` chuẩn V2Base — `V2BaseInput` (tìm kiếm) + `b-form-select` (Loại bài học) + `V2BaseButton` (Reset)
- [x] Fix lỗi `Cannot read properties of undefined (reading 'addListener')`: do V2BaseSelect/V2BaseSelectInModal dùng jQuery Select2 khởi tạo trong b-modal → đổi sang `b-form-select` (Bootstrap-Vue native, không phụ thuộc jQuery)
- [x] Thêm computed `lessonTypeOptionsFilter` với format `{value, text}` phù hợp `b-form-select`
- [x] Dọn file sai: đã tạo nhầm `.plans/course-rebuild-subject/` ở root → cần xoá thủ công nếu cần

**File thay đổi:** `hrm-client/pages/training/subjects/components/tabs/TabInfo.vue`

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

---

## Phase 13 — Bug fix Tab Đánh giá + prerequisite + người chấm (2026-04-28, @junfoke)

- [x] Fix mất hiển thị prerequisite khi reopen modal — `TabInfo.vue`: đồng bộ option id theo `lesson_id` thay vì `subject_lesson.id/_localId`; so sánh exclude bài đang chỉnh cũng theo `lesson_id` → tránh mismatch khi map lại sau khi đóng/mở modal
- [x] Fix nguồn dữ liệu `examKitOptions` sai/thiếu — `SubjectBuilderForm.vue`: ưu tiên gọi `training/exams?getForCourse=1&limit=1000` (dữ liệu đầy đủ hơn); fallback sang `training/exams/get-all-select` nếu cần; chuẩn hoá field `count` qua helper `toNumberOrNull()` để chịu nhiều key backend (`number_questions`, `question_count`, …)
- [x] Fix so sánh `exam_id` lệch kiểu string/number — `TabEvaluation.vue`: wrap `Number(...)` trong `getMeta`, `findExamKit`, `isExamSelected`, `toggleExam`
- [x] Bổ sung `number_questions`, `essay_count`, `mcq_count` trong `ExamKitListResource.php` — tính `essay_count` = số câu có `type in [6,7]`; `mcq_count = number_questions - essay_count`; UI dùng để bật/ẩn khối "Người chấm thi" đúng
- [x] Fix danh sách người chấm rỗng — `TabEvaluation.vue`: đổi nguồn chính sang `training/employees/all`; giữ fallback cũ `apiGetMasterSelectAll('employees')`; thêm lazy fetch khi mở dropdown nếu `employeeOptions` đang rỗng

**File thay đổi:** `TabInfo.vue`, `SubjectBuilderForm.vue`, `TabEvaluation.vue`, `ExamKitListResource.php`

**Giải quyết tồn đọng:** `ExamKit.mcq_count/essay_count` đã implement → FE không còn hiển thị 0. Còn tồn đọng: `withValidator` grader-theo-essay vẫn comment out.

---

## Phase 14 — Bug fix UX + multi-select + validation (2026-04-28, @junfoke)

- [x] Fix multi-select prerequisite (Ctrl/Command chọn nhiều) — `V2BaseSelectInModal.vue`: thêm prop `multiple`, directive check `$select.prop('multiple')` trước khi close on unselect, method `_initMultipleSelect2()` bypass library + reinit DOM, `updateHeight()` skip khi multiple, CSS cho `select2-selection--multiple`
- [x] Thêm inline validation error `TabEvaluation.vue` — `V2BaseError` dưới: `exam_attempt_limit`, `exam_score_rule`, `subject_exams`, `exam_participation_required`, `exam_min_required_percent`, `subject_exams.{idx}.grader_ids`; bỏ generic `formError` trong tab
- [x] Validate + error bắt buộc người chấm khi đề có tự luận — `SubjectBuilderForm.vue` `validate()`: kiểm tra `essay_count > 0 && !grader_ids.length`; `getTabForKey()` tự chuyển đúng tab có lỗi FE; `applyBackendErrors()` thêm `exam_attempt_limit`, `exam_score_rule`, `exam_participation_required`, `exam_min_required_percent` vào TAB_EVAL_KEYS; `save()` bỏ hardcode `currentMainTab = 0`
- [x] Thêm search trong popup chọn người chấm — `TabEvaluation.vue`: `ui.graderSearch`, computed `filteredEmployeeOptions`, search input dùng `ms-search` class, reset khi mở dropdown mới
- [x] Redesign tooltip Onboarding — `TabLearners.vue`: layout có cấu trúc (badge Auto-assign + divider + 2 rule số); `scss/_index.scss`: thêm classes `.tt-row`, `.tt-divider`, `.tt-rule`, `.tt-rule-num`, `.tt-rule-label`, `.tt-rule-formula`; đổi nền tối → nền trắng (`#fff` + shadow nhẹ)
- [x] Fix duplicate error message `TabLearners.vue` — xóa `V2BaseError` generic (parent đã hiển thị)
- [x] Fix "Không yêu cầu" không chọn được — `TabEvaluation.vue`: `participationRequiredOptions` đổi `{ id: 0 }` → `{ id: 2 }`; value binding `=== 1 ? 1 : 2`; handler convert ngược `Number(v) === 1 ? 1 : 0` trước khi emit
- [x] Chuyển SCSS về đúng chuẩn project — `components/subject-builder.scss` → `pages/training/subjects/scss/_index.scss`; cập nhật import trong `SubjectBuilderForm.vue` → `../scss/_index.scss`; thêm `.tab-content { padding-top: 10px }`

- [x] Fix tab Cấu hình người học không tự mở pill đã chọn khi edit — `TabLearners.vue`: thay init trong `mounted()` bằng `watch: { 'value.subject_assignees': { immediate: true } }` + flag `_typesInitialized` để chỉ init 1 lần từ server data, tránh reset khi user tương tác
- [x] Fix khoá học Nháp không xóa được — `Subject.php` `canDelete()`: DRAFT luôn trả `true` nếu có quyền, bỏ qua check reference (`capabilities`, `questions`, `exams`, `courseRequests`, `trainingRequests`)
- [x] Redesign dialog xác nhận khoá/mở khoá — `subjects/index.vue`: thay `confirm-lock-timesheet` + `confirm-un-lock-selected` (generic xấu) bằng `BaseConfirmModal` duy nhất (pattern lessons); title/message/button text động theo `item.status`; gộp lock + unlock vào `handleConfirmToggleLock()`

- [x] Fix mã khoá học không tự sinh khi không nhấn nút tạo ngẫu nhiên — `SubjectService.php` `storeWithStructure()`: sau `save()` lần đầu, nếu `code` rỗng thì auto-gen `SUB-` + `Helper::generateCode(4, $id)` và save lại; thêm `use Modules\Human\Helper\Helper`
- [x] Fix `override_completion` luôn reset về "Dùng mặc định" sau khi lưu — `SubjectBuilderForm.vue` `buildSubjectLessonPayload()`: thay `toOneTwo(sl.override_completion)` bằng check đúng chiều (`true`/`2` → gửi `2`, còn lại → `1`); nguyên nhân: `toOneTwo` map `true→1` nhưng BE convention `2=ghi đè, 1=mặc định`
- [x] Modal xác nhận khoá/mở khoá dùng component sai (generic timesheet) → `subjects/index.vue`: thay bằng `BaseConfirmModal` + `itemToLock`, computed `lockConfirmTitle/Message/Action`, gộp `handleConfirmToggleLock()`
- [x] Tab Cấu hình người học không tự mở pill đã chọn khi edit — `TabLearners.vue`: `watch 'value.subject_assignees' immediate:true` + flag `_typesInitialized`
- [x] Khoá học Nháp không xóa được — `Subject.php` `canDelete()`: DRAFT luôn `true` nếu có quyền, bỏ qua check reference
- [x] Modal info bài học thiếu thông tin — `TabInfo.vue`: size `md→lg`, thêm hint-box (type pill + tiêu chí mặc định + ghi chú Ghi đè), divider, phần Mô tả (`summary`); phân biệt state "đang ghi đè" vs "chưa ghi đè"
- [x] `openLessonInfoModal` chỉ nhận `lesson`, không biết trạng thái override — đổi sang nhận `sl` (subject_lesson), lưu thêm `infoSubjectLesson`; modal hiện màu xanh + text "Đang ghi đè" khi `override_completion=true`
- [x] Format tiêu chí hoàn thành thiếu giây — refactor thành `_formatCompletionFromCriteria(c, t)`: Video `XEM ≥ X% hoặc ≥ Ys`; Bài viết `ĐỌC ≥ Ys & TIẾN ĐỘ ≥ X%`; Tài liệu `ĐỌC ≥ Ys & TIẾN ĐỘ ≥ X%` (không phải XEM); SCORM `SCORM = status, điểm ≥ X`
- [x] Labels mapping modal chưa tiếng Việt — đổi "Override completion"→"Ghi đè tiêu chí hoàn thành", "Tracking & Validate"→"Theo dõi & kiểm tra", "Default/Effective"→"Mặc định/Áp dụng thực tế", options "Dùng mặc định/Ghi đè"→"Không (dùng mặc định)/Có (ghi đè)"
- [x] Labels prerequisite section chưa tiếng Việt — "Bật prerequisite"→"Bật điều kiện mở khoá", options "Có/Không"→"Bật/Tắt", gợi ý "Ctrl/Command…"→"Chọn nhiều bài ở dưới"; thêm hint-box "Chuẩn nghiệp vụ: điều kiện mở khoá dựa trên trạng thái Đã hoàn thành"

**File thay đổi:** `V2BaseSelectInModal.vue`, `TabEvaluation.vue`, `SubjectBuilderForm.vue`, `TabLearners.vue`, `TabInfo.vue`, `SubjectLessonCompletionOverride.vue`, `pages/training/subjects/scss/_index.scss`, `Subject.php`, `SubjectService.php`, `pages/training/subjects/index.vue`

---

## Checkpoint — 2026-04-28 (latest)

**Vừa hoàn thành:** Phase 14 — Multi-select prerequisite, inline error validation, validate người chấm tự luận, search grader, tooltip Onboarding redesign, fix duplicate error TabLearners, fix "Không yêu cầu" falsy id, chuẩn hóa SCSS về đúng vị trí.
**Đang làm dở:** Không.
**Bước tiếp theo:** Tiếp tục Phase 10 manual test (còn 10 test case chưa tick). Ưu tiên: test chọn đề thi có tự luận → xem khối "Người chấm thi" + grader validation hiển thị đúng.
**Blocked:** `withValidator` grader-theo-essay vẫn comment out — cần clarify shape `exam_questions.type` trước khi unlock.
