# Design: Training — Elearning (Umbrella)

## 1. Mục đích
Mở rộng module Training (hiện chỉ hỗ trợ khóa học offline) để hỗ trợ học online (elearning):
- Học viên xem bài học (video/text/SCORM/file) trên web/mobile
- Tracking tiến độ học từng bài (% hoàn thành) — KHÔNG chỉ dùng config có sẵn (tracking_completion) mà phải lưu thực tế
- Làm quiz online sau bài học, auto-grade MCQ/multiple choice, chấm tay essay/practice
- Dashboard tiến độ cá nhân + báo cáo cho manager

## 2. Hiện trạng (chi tiết tại `docs/training.md`)

### 2.1. Asset hiện có (~60-65%)
- **BE**: 30+ Entities, 21 endpoint groups; lesson + question infrastructure đã có; FCM/notification ready
- **FE**: 51 folder pages; CRUD lesson, my_courses dashboard, course mgmt, exam, capability... đã có
- **Lesson type**: Video/Text/File/SCORM (constants 1-4)
- **`tracking_completion` JSON schema**: 18 trường đã định nghĩa nhưng chỉ là CONFIG, KHÔNG có bảng PROGRESS thực
- **Question 10 loại**: 6 loại auto-grade (TrueFalse/MCQ/Multiple/Matching/FillBlank/Numeric/Date), 2 loại chấm tay (Essay/Practice), 2 loại đặc biệt (File/Practice)

### 2.2. Gap chính cần build cho elearning
**Priority 1 (Must-have)**:
- DB: `lesson_progress` (employee_id, lesson_id, course_id, percent_completed, last_watched_at, completed_at, data JSON)
- DB: `course_lessons` (link Course ↔ Lesson trực tiếp, không qua Subject)
- DB: `lesson_quiz_results` (employee_id, lesson_id, question_id, answer, score, attempt_date)
- API: `POST /lessons/{id}/complete`
- API: `POST /lessons/{id}/quiz-submit` (auto-grade những loại có thể)
- API: `GET /my-courses/{id}/progress` (dashboard)
- FE: trang học bài (player video/text/file/SCORM) — cho từng lesson type
- FE: quiz inline trong trang học bài
- FE: extend `my_courses/` thêm tab/section "Khóa học online"
- FE: update `components/menu-sidebar.js` thêm item Elearning

**Priority 2 (Important)**:
- Field `course.delivery_mode` ENUM (synchronous/asynchronous/blended) + flag `is_elearning`
- DB: `course_lesson_requisite` (prerequisite ở cấp Lesson, chi tiết hơn Subject)
- SCORM xAPI runtime tracking (cmi.* statements)
- Notification: nhắc học viên hoàn thành bài, hết hạn

**Priority 3 (Enhancement)**:
- Activity log (view count, play/pause, scroll position)
- Gamification (badge, point, leaderboard)
- Adaptive learning (branch logic theo quiz score)

## 3. Scope

### Trong scope
- BE: bảng + endpoint cho lesson progress, quiz submission, course-lesson mapping, dashboard progress
- FE: trang học bài cho employee (player + quiz + progress), extend my_courses
- FE: extend màn quản lý course để hỗ trợ elearning mode
- FE: update sidebar menu

### Ngoài scope (giai đoạn này)
- Mobile native app (chỉ làm web responsive)
- Live streaming (chỉ async)
- Adaptive learning / branch logic
- Gamification
- xAPI / LRS ngoại vi

## 4. User personas
- **Học viên (Employee)**: xem bài, làm quiz, theo dõi tiến độ
- **Giáo viên (Teacher)**: tạo Course online, gắn Lesson sequence, quản lý quiz
- **Manager**: xem báo cáo tiến độ học của nhân viên
- **Admin Training**: cấu hình master data (Subject/Lesson/Question/Course online)

## 5. Constraints + Convention bắt buộc tuân theo

### BE
- Service pattern hiện tại (KHÔNG có Repository) — Service query Model trực tiếp
- Permission filter 4 cấp `checkPermissionList()` (Tổng cty / Cty / PB / BP)
- Notification qua `EmployeeInfoService::sendToAllNotification()`
- Auth: `auth:api` middleware
- Routes prefix: `/v1/training/...`
- Response format: `responseJson()` chuẩn
- Exception code: 422 (validation), 423 (nghiệp vụ), 403 (permission)

### FE
- Layout: `default-sidebar`
- Components V2: `V2BaseFilterPanel`, `V2BaseDataTable`, `V2BaseSelect/Label/Input/Textarea/DatePicker/Error`
- Editor: CKEditor 5 Classic
- Store action: `apiGetMethod` / `apiPostMethod` / `apiDeleteMethod`
- Permission: `hasAPermission()` mixin
- Date: DD/MM/YYYY display, YYYY-MM-DD API
- Form validation: `error.fieldName` object + `<V2BaseError>` inline
- Naming folder mới: **kebab-case** (vd `lesson-player/`, `lesson-progress/`)
- TRÁNH: layout `exam_todo.vue` cũ; subfolder `pages/training/pages/` legacy; mở rộng `LessonForm.vue` 116KB monolith

## 6. Reference assets từ user
- File demo HTML + Vue 2 (user sẽ cung cấp riêng cho từng feature mai)

## 7. Roadmap
- **Phase 0**: Khảo sát + tạo `docs/training.md` ← ✅ Done 2026-04-18
- **Phase 1+**: Wait spec từng feature (user mô tả + cung cấp file demo) → tạo plan riêng

## 8. Decisions sẽ chốt khi vào từng phase
- Mỗi feature elearning sẽ có plan riêng `.plans/training-elearning-<feature>/`
- Pattern FE: theo style training hiện tại (V2 components + Permission mixin) hay style Assign mới (PageTitleMixin, BaseConfirmModal...)?
- BE: mở rộng Service hiện có hay tạo Service mới (vd `LessonProgressService`)?
- Cần version API riêng (V2) hay extend V1?
- SCORM xAPI: làm phase 1 luôn hay phase sau?

## 9. Risk + Lưu ý đặc biệt
- 🚩 **Hardcoded dev email** trong `SendMailCapacityEvaluateNotification:54` — fix khi đụng tới Capacity flow
- ⚠️ `tracking_completion` ở Lesson + SubjectLesson chỉ là CONFIG → đừng nhầm là PROGRESS
- ⚠️ `ExamTestResult` hiện chỉ lưu offline import → KHÔNG reuse cho online quiz, phải tạo bảng mới hoặc thêm field phân biệt
- ⚠️ `LessonForm.vue` 116KB monolith — extend cho elearning cần tách component nhỏ hơn
- ⚠️ `getStatusClass` duplicate 50+ chỗ — có thể extract `V2StatusBadge` khi tiện
- ⚠️ Naming inconsistent kebab-case vs snake_case — folder mới chọn kebab
