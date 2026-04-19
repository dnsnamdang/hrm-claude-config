# Module Training (Đào tạo) — Codebase Map

> Tài liệu này mô tả các bounded context, entity, endpoint, workflow của module Training (BE: `hrm-api/Modules/Training/`, FE: `hrm-client/pages/training/`). Dùng cho dev mới onboard hoặc lên plan feature mới (đặc biệt là phần elearning).

**Cập nhật**: 2026-04-18 (khảo sát BE + FE)

---

## 1. Bounded Contexts (10 nhóm chức năng)

### A. Capability & Capacity Framework — Khung năng lực
Quản lý năng lực theo vị trí công việc, đánh giá nhân viên theo cấp độ.

- **Entities**: `Capability`, `CapabilityGroup`, `CapabilityLevel`, `CapacityFramework`, `CapacityFrameworkCapabilityGroup`, `CapacityFrameworkCompetency`, `CapacityFrameworkHistory`
- **Workflow**: Định nghĩa năng lực → group → khung năng lực theo position/department → áp dụng đánh giá

### B. Course (Khóa học — hiện chỉ offline)
Tạo, đăng ký, điểm danh, đánh giá khóa học.

- **Entities**: `Course`, `CourseStudent`, `CourseStudentAttendance`, `CourseSession`, `CourseTeacher`, `CoursePersonCharge`, `CourseNotification`, `CourseRegister`, `CourseRegisterConfig`
- **Field quan trọng**: `Course.platform` ENUM (1=Online, 2=Offline, 3=Hybrid) — đã có sẵn nhưng logic platform=1 chưa wire đầy đủ
- **Status flow** xem mục §3

### C. Subject & Lesson (Môn học & Bài học)
Định nghĩa nội dung học (môn → bài học → media/quiz).

- **Entities**: `Subject`, `SubjectLesson` (pivot), `SubjectChapter`, `SubjectVideo`, `SubjectDocument`, `Lesson`, `LessonAttachment`, `LessonQuestion`
- **Lesson types**: Video, Text, File, SCORM (field type)
- **`SubjectLesson.tracking_completion`** (JSON): cấu hình tiêu chí hoàn thành (`video_watch_percent`, `text_read_percent`, `file_view_percent`, `scorm_completion`); cho phép override per Subject
- **Prerequisite mode**: ALL / ANY (qua `SubjectLesson`)

### D. Exam & Question (Đề thi & Câu hỏi)
Ngân hàng câu hỏi + đề thi (hiện thiên về offline).

- **Entities**: `ExamKit`, `ExamQuestion`, `Question`, `QuestionAnswer`, `QuestionClassify`, `ExamTestResult`, `ExamTestResultDetail`
- **10 loại câu hỏi**: MCQ, Multiple, Essay, Matching, ... (xem `Question::TYPES`)
- **Hiện trạng**: `ExamTestResult` chủ yếu lưu kết quả **offline** (import sau khi thi); chưa có flow online quiz attempt/submit thật sự cho elearning

### E. Course Evaluation (Đánh giá khóa học sau học)
Khảo sát phản hồi sau khóa học.

- **Entities**: `CourseEvaluation`, `CourseEvaluationQuestion`, `CourseEvaluationPersonal`, `CourseEvaluationPersonalQuestion`, `CourseEvaluationTeacher`

### F. Capacity Evaluate (Đánh giá năng lực)
Quy trình đánh giá năng lực: lập kế hoạch → thi → chấm điểm → kết quả.

- **Entities**: `EvaluationCapacity`, `EvaluationCapacityNeed`, `EvaluationCapacityNeedEmployee`, `EvaluationCapacityNeedLevel`, `CapacityEvaluatePlanning`

### G. Training Request & Planning (Nhu cầu & Kế hoạch đào tạo)
Phòng ban đề xuất nhu cầu → tổng hợp thành kế hoạch.

- **Entities**: `TrainingRequest`, `TrainingRequestStudent`, `TrainingPlanning`, `TrainingPlanningSubject`, `TrainingPlanningSubjectTime`

### H. Survey (Khảo sát nhu cầu)
Thu thập nhu cầu đào tạo từ nhân viên/phòng ban.

- **Entities**: `TrainingSurvey`, `TrainingSurveyRespondent`, `StaffTrainingSurvey`, `DepartmentTrainingSurvey`

### I. Cost Training (Chi phí đào tạo)
Quản lý chi phí học viên + doanh thu khóa học.

- **Entities**: `CostTraining`, `CostTrainingLog`, `CourseCostPayment`, `CourseCostRevenue`, `CourseRequestCostPayment`

### J. Career Progression (Lộ trình sự nghiệp)
Lộ trình phát triển theo khung năng lực.

- **Entities**: `CareerProgression`, `EmployeeAssignment`

---

## 2. Endpoint Groups (route prefix `/training`)

| Prefix | Controller | Actions chính | Ghi chú |
|--------|-----------|---------------|---------|
| `/teachers` | TeacherController | CRUD, lock/unlock, getLog | Giáo viên |
| `/training_types` | TrainingTypeController | CRUD, getAll | Loại đào tạo (Nội bộ/Thuê ngoài) |
| `/subjects` | SubjectController | CRUD, **showBuilder/storeBuilder** | Môn học + builder visual (CMS) |
| `/courses` | CourseController | CRUD, **register**, **closeRegistration**, **sendAttendanceRequest**, **summaryResultCourse**, 12 reportXXX | Khóa học (focus offline) |
| `/course-registers` | CourseRegisterController | index, show, cancel, toggleApprove | Phê duyệt đăng ký |
| `/course-notifications` | CourseNotificationController | store, index, show, detailCourse | Thông báo khóa học |
| `/lessons` | LessonController | CRUD, **uploadFile**, lock/unlock | Bài học (S3/local) |
| `/exams` | ExamKitController | CRUD, getAll, getAllSelect | Đề thi offline |
| `/questions` | QuestionController | CRUD, lock/unlock, deny, getListAll | Ngân hàng câu hỏi |
| `/exam_test_results` | ExamResultController | CRUD, **updateResultEssayQuestion**, **summaryResultExamTest** | Kết quả thi (chủ yếu offline) |
| `/capability_groups` | CapabilityGroupController | CRUD | |
| `/capabilities` | CapabilityController | CRUD, getByGroup, getAllByGroup | |
| `/capability-frameworks` | CapacityFrameworkController | CRUD, getHistory, updateStatus | |
| `/capacity-evaluate` | CapacityEvaluateController | CRUD, summaryResultExamTest, notification, toggleApprove | |
| `/capacity-evaluate-personal` | CapacityEvaluatePersonalController | needJoin, joined, scheduleTest, result, **postponeAssessment** | Employee view |
| `/training_surveys` | TrainingSurveyController | CRUD, export | |
| `/training-planning` | TrainingPlanningController | CRUD, checkExistTime, toggleApprove, getAllByTrainingSurvey | |
| `/cost_trainings` | CostTrainingController | CRUD, getAll | |
| `/my-courses` | MyCourseController | needJoinList, getCoursesLearned, registerCourse, getExamSchedule, getExamResults | **Employee view** — nền tảng cho elearning UI |
| `/attendance` | AttendanceController | index, show, **studentAttendance**, storeStudentAttendance | Điểm danh |
| `/dashboard` | DashboardController | getData, statisticalCourse (12 stats), getLayout, saveLayout | Dashboard có save layout |

---

## 3. Workflow khóa học offline (đã hoàn thiện)

### Course Approval Flow
```
DANG_TAO (1)
  → CHO_TP_DUYET (2)
  → CHO_BGD_DUYET (4)
  → DA_DUYET (5)        [hoặc KHONG_DUYET (6)]
```

### Course Lifecycle (sau APPROVED)
```
SAPBATDAU (1)  →  DANGHOC (2)  →  KETTHUC (3)
                       ↓
                   TAMDUNG (4)
```

### Tables tham gia một course offline
- `courses` (info, platform=2)
- `course_registers` (đăng ký + duyệt)
- `course_students` (đã duyệt → học viên chính thức)
- `course_sessions` (buổi học)
- `course_student_attendance` (điểm danh từng buổi)
- `course_exams` (đề thi gắn vào course)
- `exam_test_results` (điểm thi)
- `course_evaluations` + `course_evaluation_personal` (khảo sát sau học)

---

## 4. Sẵn sàng cho elearning — Asset hiện có vs Gap

### ✅ Đã có (~60%)
| Asset | Mô tả |
|-------|-------|
| `Lesson` entity | Type Video/Text/File/SCORM, có upload S3/local |
| `SubjectLesson.tracking_completion` (JSON) | Cấu hình ngưỡng hoàn thành |
| `LessonAttachment` | File đính kèm (S3/local) |
| `LessonQuestion` mapping | Câu hỏi gắn với bài học (sort_order) |
| `Question` + `QuestionAnswer` | 10 loại câu hỏi (MCQ, multiple, essay, matching...) |
| `Course.platform` | ENUM 1=Online, 2=Offline, 3=Hybrid (chưa wire đầy đủ logic Online) |
| File upload infrastructure | `LessonController.uploadFile`, S3 |
| `MyCourseController` | Khung sẵn cho employee view (xem khóa cần học, đã học, lịch thi, kết quả) |

### ❌ Gap — cần bổ sung cho elearning

#### Priority 1 (Critical — không có thì không chạy được)
- [ ] **Bảng `lesson_progress`**: `(employee_id, lesson_id, course_id?, percent_completed, last_watched_at, completed_at, data JSON)`
- [ ] **Bảng `course_lessons`** (hoặc dùng SubjectLesson với scope course): mapping Course → Lesson cụ thể (không qua Subject)
- [ ] **Endpoint POST `/lessons/{id}/complete`**: đánh dấu hoàn thành bài, lưu progress
- [ ] **Bảng `lesson_quiz_results`**: `(employee_id, lesson_id, question_id, answer, score, attempt_date)`
- [ ] **Endpoint POST `/lessons/{id}/quiz-submit`**: nộp đáp án, auto-grade MCQ/multiple, trả kết quả

#### Priority 2 (Important)
- [ ] **Bảng `course_lesson_requisite`**: prerequisite ở mức Lesson (chi tiết hơn Subject)
- [ ] **Field `course.delivery_mode`** ENUM (synchronous/asynchronous/blended) + flag `is_elearning`
- [ ] **Endpoint GET `/my-courses/{id}/progress`**: dashboard tiến độ học (lessons completed, quiz score, time spent)
- [ ] **SCORM xAPI integration**: capture SCORM runtime (cmi.* statements, xAPI format)

#### Priority 3 (Enhancement)
- [ ] Activity log (view count, play/pause, scroll position)
- [ ] Gamification (badges, points, leaderboard)
- [ ] Adaptive learning (branch logic theo quiz score)

---

## 5. FE — `pages/training/` (51 folder)

FE đã triển khai khá đầy đủ. Group theo bounded context tương ứng BE:

### Theo bounded context

| BE Context | FE Folders chính |
|-----------|------------------|
| Course (offline) | `courses/`, `course_requests/`, `course-registers/`, `course-notification/`, `course-evaluation/`, `course-evaluation-personal/`, `course-evaluation-personal-result/`, `course-evaluation-result-manager/`, `attendance/` |
| Subject & Lesson | `subjects/`, `lessons/` ← CRUD đã có (`index/add/edit/_id/detail/_id`) |
| Exam & Question | `exam_kits/`, `exam_results/`, `questions/`, `examiners/`, `summary-exam/` |
| Capability | `capability/`, `capability_groups/`, `capacity-framework/` |
| Capacity Evaluate | `capacity-evaluate/`, `capacity-evaluate-notification/`, `capacity-evaluate-personal/`, `capacity-evaluate-planning/`, `capacity-evaluate-report/`, `capacity-exam-summary/`, `summary-result-exam-by-capacity/`, `summary-result-exam-capacity/`, `evaluation-capacity-need/`, `evaluation-capacity-need-level/`, `capacity-report/` |
| Career | `career-progressions/`, `career-progression-report/` |
| Survey | `training_surveys/`, `training-survey-planning/`, `training-survey-report/`, `personal-survey/`, `personal-survey-manager/`, `personal-survey-result/`, `department-personal-survey/`, `department-survey-forms/`, `department-survey-manager/` |
| Master | `teachers/`, `teacher-assigned-course/`, `training_types/`, `training_requests/`, `training-results-plans/`, `cost_trainings/` |
| Employee view | **`my_courses/`** ← KHUNG sẵn cho elearning |
| Khác | `dashboard/`, `report/`, `pages/` (folder con tên `pages` — có vẻ legacy/backup) |

### `pages/training/lessons/` — đã có CRUD lesson
```
lessons/
├── index.vue         # Danh sách lesson
├── add.vue           # Tạo mới
├── edit/_id.vue      # Sửa
└── detail/_id.vue    # Xem chi tiết
```
→ **Quản lý lesson đã có**, nhưng chưa có **trang học bài** (player video/text/SCORM cho học viên).

### `pages/training/my_courses/` — Employee view
```
my_courses/
├── index.vue                        # Dashboard cá nhân
├── components/
│   ├── CourseList.vue
│   ├── CourseRegister.vue
│   ├── ExamResult.vue               # Kết quả thi
│   ├── ExamSchedule.vue             # Lịch thi
│   ├── JoinedCourseList.vue         # Đã tham gia
│   ├── JoiningCourseList.vue        # Đang học
│   └── NeedJoinCourseList.vue       # Cần tham gia
├── course-registers/
└── register_course/
```
→ Component đã có sẵn nhưng **focus offline** (Joined/Joining/NeedJoin theo session offline). Cần extend cho elearning: thêm component "LessonProgress", trang học bài, quiz player.

### `pages/training/courses/` — Quản lý course
```
courses/
├── index.vue, add.vue, print.vue
├── _id/
│   ├── index.vue, show.vue, register.vue, approve.vue
│   └── exam_kits/
├── components/
├── course-assign-grading.vue
└── summary-course-result.vue
```

### Naming convention không đồng nhất
FE training mix cả 2 style:
- **kebab-case**: `course-evaluation`, `capacity-framework`, `career-progressions`, `training-survey-planning`
- **snake_case**: `course_requests`, `cost_trainings`, `exam_kits`, `training_types`, `my_courses`

→ **Lưu ý**: khi tạo folder mới cho elearning, nên thống nhất 1 style (đề xuất dùng kebab-case theo Vue/Nuxt convention chuẩn).

---

## 6. Top files để đọc khi onboard

| # | File | Lý do |
|---|------|-------|
| 1 | `Modules/Training/Entities/Course.php` | Khóa học core, status flow, platform field |
| 2 | `Modules/Training/Entities/Lesson.php` | Lesson type + tracking_completion JSON schema |
| 3 | `Modules/Training/Entities/SubjectLesson.php` | Mapping với prerequisite + override completion |
| 4 | `Modules/Training/Entities/Question.php` + `QuestionAnswer.php` | Ngân hàng câu hỏi, 10 loại |
| 5 | `Modules/Training/Http/Controllers/V1/CourseController.php` | Workflow course: register, attendance, summary |
| 6 | `Modules/Training/Http/Controllers/V1/LessonController.php` | Upload, lock/unlock, lưu media |
| 7 | `Modules/Training/Services/Lesson/LessonService.php` | Logic search, store, file handling |
| 8 | `Modules/Training/Services/Course/CourseService.php` | Logic course: search, register, attendance approval |
| 9 | `Modules/Training/Http/Controllers/V1/MyCourseController.php` | Employee view — cần mở rộng cho elearning UI |
| 10 | `Modules/Training/Routes/api.php` | Toàn bộ route map |

Migrations quan trọng:
- `2026_02_28_153204_create_lessons_table.php` — Lesson schema (type, duration, content JSON)
- `2024_02_*_create_training_*_table.php` — các bảng training core
- `2024_03_*_create_training_surveys_*_table.php` — survey

---

## 7. Lưu ý onboard

- **Naming**: Folder BE là `Modules/Training/` (đúng); CLAUDE.md trước đây ghi sai là `Tranning` — đã sửa
- **Controller version**: routes dùng `Http/Controllers/V1/...` — không phải `Api/V1/` như Assign
- **Soft delete**: Course/Lesson dùng SoftDelete (cần check khi query)
- **`Course.platform` chưa wire logic Online**: field có nhưng các endpoint chưa filter/branch theo platform=1
- **`tracking_completion` là CONFIG, không phải PROGRESS**: đừng nhầm — config nằm ở `SubjectLesson`, progress thật sự cần bảng mới
- **Exam hiện thiên về offline**: `ExamTestResult` lưu kết quả import; cần build flow online attempt riêng cho elearning

---

## 8. Workflow chi tiết các flow phức tạp

### 8.1. Capacity Evaluate (Đánh giá năng lực)

```
[Manager]
  └─ Tạo CapacityEvaluatePlanning (DANG_TAO=1 → CHO_DUYET → DA_DUYET)
       └─ Tạo EvaluationCapacity (kỳ thi)
            ├─ EvaluationCapacityNeed (per Capability)
            │    ├─ EvaluationCapacityNeedLevel (per Level: link ExamKit + deadline + exam_form online/offline)
            │    └─ EvaluationCapacityNeedEmployee (status: 1=scheduled, 2=postponed)
            └─ Job SendNotiEvaluationCapacity → Employee
[Employee]
  └─ scheduleTest() → xem lịch
  └─ postponeAssessment() → status=2
  └─ (Online attempt CHƯA CÓ) hoặc thi offline
[Examiner]
  └─ Import result → ExamTestResult + ExamTestResultDetail
[System]
  └─ summaryResultExamTest() → tính điểm per level/capability
```

### 8.2. Training Survey (Khảo sát nhu cầu)
- `TrainingSurvey` (master) — `respondents` ENUM (staff/dept/company), `status` (public/private)
- Khi gửi:
  - **Staff**: tạo `StaffTrainingSurvey` per nhân viên (status 1=chờ, 2=đã trả lời) → `StaffTrainingSurveySubject`
  - **Dept**: tạo `DepartmentTrainingSurvey` per phòng → `DepartmentTrainingSurveyEmployee` (link nhân viên trong phòng)
- `PersonalSurvey` (legacy?) — route `/training-survey-personals`, ít dùng

### 8.3. TrainingRequest → TrainingPlanning → Course
```
TrainingRequest (DANG_TAO=1 → CHO_TP_DUYET=2 → CHO_QLDT_DUYET=3 → DA_DUYET=4 | KHONG_DUYET=5)
  ↓ (link với survey, tổng hợp Staff + Dept respondents)
TrainingPlanning
  └─ TrainingPlanningSubject
       └─ TrainingPlanningSubjectTime (buổi học chi tiết)
  ↓
Course (platform: 1=online, 2=offline, 3=hybrid)
```
- `TrainingSurveyPlanningService.getAllByTrainingSurvey()` (line 23-50) merge logic phức tạp giữa Staff+Dept survey, cộng dồn nếu trùng subject+date.

### 8.4. Course Evaluation (sau học)
- Trigger: sau course `KETTHUC`
- 2 đối tượng đánh giá: **course** + **teacher**
- `CourseEvaluation` (master) → `CourseEvaluationQuestion` (type: course/teacher) + `CourseEvaluationTeacher`
- `CourseEvaluationPersonal` (per nhân viên) → `CourseEvaluationPersonalQuestion` + `CourseEvaluationPersonalTeacher`
- Manager xem tổng hợp ở `CourseEvaluationResultManagerController`

### 8.5. Career Progression
- `CareerProgression` ↔ `WorkingPosition` (N:M qua `career_progression_working_positions`)
- **Chưa có liên kết logic trực tiếp** với Capacity Evaluate result trong code (workflow dự kiến chỉ trên doc)

---

## 9. Lesson `tracking_completion` JSON schema (đầy đủ)

Lưu ở `Lesson.tracking_completion` (config mặc định), override per Subject ở `SubjectLesson.tracking_completion_override`.

### Lesson.type constants (`Lesson.php:17-20`)
```php
const TYPE_VIDEO = 1;
const TYPE_TEXT = 2;
const TYPE_FILE = 3;
const TYPE_SCORM = 4;
```

### Schema chi tiết
```json
{
  "video_watch_percent": 0-100,
  "video_min_watch_seconds": 0,
  "video_heartbeat_seconds": 30,
  "video_allow_seek": true,
  "video_max_seek_percent": 80,
  "video_require_active_tab": true,

  "text_read_percent": 0-100,
  "text_min_read_seconds": 0,
  "text_min_scroll_percent": 50,
  "text_min_dwell_per_page_seconds": 10,
  "text_require_scroll_end": true,

  "file_view_percent": 0-100,
  "file_min_read_seconds": 0,
  "file_min_scroll_percent": 50,
  "file_min_dwell_per_page_seconds": 10,
  "file_allow_download": false,

  "scorm_completion": 100,
  "scorm_min_score": 70
}
```

### Question 10 loại (`Question::TYPES`)
```
1=Đúng/sai     2=Lựa chọn một    3=Lựa chọn nhiều   4=Ghép đáp án   5=Điền từ
6=Tự luận       7=Thực hành        8=Số                9=File           10=Ngày tháng
```

### `ExamTestResultDetail` (đáp án + chấm)
- `question_id, question_type, answer, result, grading_status, created_by`
- `result`: 1=đúng, 0=sai, null=chưa chấm
- Type 6 (Essay) + 7 (Practice) → cần chấm tay → `grading_status=2` (đang chấm)

---

## 10. Permission Model + Service Pattern

### Middleware
- `auth:api` cho toàn module Training

### Permission strings (16 nhóm chính)
| Lĩnh vực | Permission |
|---------|-----------|
| Course | Xem DS khóa học theo tổng cty/cty/PB/BP; Tạo khóa học; TP duyệt; BGĐ duyệt |
| Exam/Question | Quản lý đề thi; Quản lý câu hỏi; Xem examiners |
| Lesson/Subject | Quản lý môn học; Quản lý bài học; Quản lý loại đào tạo |
| Capacity Evaluate | Xem DS kỳ thi đánh giá theo 4 cấp; BGĐ duyệt; QLDT duyệt |
| Capacity Framework | Quản lý khung năng lực; Quản lý năng lực; Xem DS khung 4 cấp |
| Training Survey | Xem DS khảo sát đào tạo theo 4 cấp |
| Training Request | Xem DS đề xuất đào tạo 4 cấp; TP duyệt; QLDT duyệt |
| Career | Khai báo lộ trình; Xem báo cáo lộ trình 4 cấp |

### Filter cấp tổ chức (chuẩn)
`checkPermissionList()` helper (vd `CapacityEvaluateService:65-71`) — 4 cấp: Tổng công ty > Công ty > Phòng ban > Bộ phận. Không có quyền nào → chỉ thấy của mình.

### Service Layer
- `BaseService` chứa permission helpers (`checkPermissionHavePart`, `checkPermissionHasCompanyAndDepartment`)
- **Repository**: KHÔNG dùng — Service query Model trực tiếp
- Service inject vào Controller qua constructor
- `DB::transaction()` thường ở Controller, không ở Service
- Notification qua `EmployeeInfoService::sendToAllNotification()` + Job (Redis queue)

### Jobs hiện có
- `SendMailCapacityEvaluateNotification`
- `SendNotificationToEmployee` (Redis + SMS)
- `SendNotiEvaluationCapacity`
- `SendMailSummaryResultExamCapacity`
- `SendNotiAttendanceForStudent`

---

## 11. FE Patterns chi tiết

### Layout & Routing
- Layout: `default-sidebar` (~140 pages dùng)
- Sidebar register tại `components/menu-sidebar.js:343+` → `menuItemsTraining`
- Permission menu: `isShow: ['Quản lý bài học']` + computed `hasAPermission()` từ Permission mixin (`utils/mixins/Permission`)

### V2 Components đã dùng trong Training
| Component | Dùng tại | Mục đích |
|-----------|---------|----------|
| `V2BaseFilterPanel` | `lessons/index.vue` | Collapse + quick search + advanced filters |
| `V2BaseDataTable` | `lessons/index.vue` | Table với sort, pagination |
| `V2BaseSelect` / `V2BaseLabel` / `V2BaseInput` / `V2BaseTextarea` / `V2BaseDatePicker` | `LessonForm`, `SubjectBuilderForm` | Form input chuẩn |
| `V2BaseError` | Mọi form | Inline validation error |
| `V2BaseMetaInfo` | `LessonForm` | Hiện created_at + updated_by chip |
| `V2BaseCodeInput` | `SubjectBuilderForm` | Code input có prefix |
| `V2BaseSelectInModal` | `LessonForm` | Select dropdown trong modal |

> **Modal common**: Training KHÔNG dùng `BaseConfirmModal`/`BaseDeleteModal` (mà Assign dùng) — dùng `b-modal` của Bootstrap-Vue hoặc tự viết.
> **Editor**: CKEditor 5 Classic (ExamForm, ExamToDoForm). Quill chỉ ở Assign.

### Components quan trọng có sẵn
| File | Size | Lý do quan trọng |
|------|------|-----------------|
| `components/forms/LessonForm.vue` | **116KB** ⚠️ | Form modal khổng lồ (2 tabs, file upload, question picker) — sẽ reuse cho elearning lesson config |
| `pages/training/subjects/components/SubjectBuilderForm.vue` | 2.4KB | Visual builder Subject + Chapter + Lesson |
| `pages/training/exam_kits/components/ExamForm.vue` | 1.8KB | Đề thi + CKEditor — dùng cho lesson quiz builder |
| `pages/training/exam_kits/_id/todo.vue` + layout `exam_todo.vue` | — | Player thi offline — **REFERENCE** để build lesson player (nhưng nên không reuse layout cũ) |
| `pages/training/my_courses/index.vue` | — | Dashboard học viên — extend cho elearning tabs |

### Store & API call
```javascript
// Toàn bộ training dùng 3 method nhất quán:
this.$store.dispatch('apiGetMethod', 'training/...')
this.$store.dispatch('apiPostMethod', { path: 'training/...', payload: {...} })
this.$store.dispatch('apiDeleteMethod', 'training/...')
```
- KHÔNG có store module riêng `store/modules/training/` — mọi action ở `store/actions.js`
- Permission check: `this.hasAPermission('Quản lý bài học')` từ Permission mixin

### UI Convention
- **Icon**: RemixIcon (`ri-*`) chính; fallback MDI/FontAwesome ở vài chỗ legacy
- **Status badge**: function cứng `getStatusClass(item)` từ `utils/common.js` — KHÔNG lookup `status_color` từ BE
- **Form validation**: `error.fieldName` object + `<V2BaseError v-if="error.X">`
- **Date format**: Display DD/MM/YYYY (vue2-datepicker), API YYYY-MM-DD

### Mixin
- **PageTitleMixin**: KHÔNG dùng trong Training (dùng PageHeader component + `head()` hook thay)
- **Permission**: dùng nhiều — `hasAPermission()`, `isCurrentEmployeeHasPermission()`

---

## 12. Quirks & Pitfalls (BE + FE)

### BE
| # | Vấn đề | File | Tác động |
|---|--------|------|---------|
| 1 | Naming không đồng nhất route vs service | Routes:411 (`/training-planning` → `TrainingSurveyPlanningService`) | Confusion |
| 2 | Merge survey logic loop array | `TrainingSurveyPlanningService:41-68` | Phức tạp, nên SQL join |
| 3 | DB::raw GROUP_CONCAT MySQL-only | `TeacherController:92`, `ExaminerController:150+` | Không portable |
| 4 | `tracking_completion` chỉ là **CONFIG**, không có PROGRESS thực | `Lesson.php:28`, `SubjectLesson.php:20` | **Phải build `lesson_progress` table mới** |
| 5 | Exam offline-only, không có online attempt | `ExamTestResult.php` | **Phải build endpoint `/quiz-submit`** |
| 6 | `CourseService.searchByFilter()` duplicate 5 lần | `CourseService:45-110` | 5 if-else permission cấp |
| 7 | 🚩 **Hardcode email dev** | `SendMailCapacityEvaluateNotification:54` (`hongthainguyen2901@gmail.com`) | Production risk |
| 8 | `survey_number` mutator on-the-fly | `TrainingSurvey.php:39-42` | Filter ở controller phải loop map |
| 9 | `EvaluationCapacityNeedEmployee.status=2` không có constant rõ | `EvaluationCapacityNeedEmployee.php:14` | Magic number |
| 10 | `CapacityEvaluateService.store()` tự tạo EvaluationCapacity | `CapacityEvaluateService:79-85` | Logic gắn trong store |

### FE
| # | Vấn đề | Tác động |
|---|--------|---------|
| 1 | Naming mix kebab-case + snake_case | Folder mới phải chọn 1 style (đề xuất kebab) |
| 2 | `_id.vue` vs `_id/index.vue` không nhất quán | Dùng `_id/index.vue` |
| 3 | Folder `pages/training/pages/` legacy/dead | Đừng đụng |
| 4 | `LessonForm.vue` 116KB monolith | Nếu extend cho elearning, nên tách component |
| 5 | `getStatusClass` duplicate ở 50+ chỗ | Nên extract `V2StatusBadge` |
| 6 | Layout `exam_todo.vue` cơ chế cũ | Tránh dùng cho lesson player elearning |
| 7 | Async component import KHÔNG dùng | Có thể tối ưu lazy-load nếu cần |

---

## 13. Đề xuất roadmap elearning (sơ bộ)

| Phase | Scope | Output |
|-------|-------|--------|
| **0** | Khảo sát + bổ sung CLAUDE.md docs | ✅ `docs/training.md` (file này) |
| **1** | DB + Model bổ sung | Migration `lesson_progress`, `lesson_quiz_results`, `course_lessons`; Entity tương ứng |
| **2** | API học bài + nộp quiz | `POST /lessons/{id}/complete`, `POST /lessons/{id}/quiz-submit`, `GET /my-courses/{id}/progress` |
| **3** | FE Employee — màn học bài | `pages/training/my-courses/_id.vue` (player video/text/SCORM, quiz, progress bar) |
| **4** | FE Manager — quản lý course online | `pages/training/courses/...` (extend màn course offline cho mode online) |
| **5** | Dashboard + Report elearning | Stats: số người hoàn thành, tỷ lệ pass quiz, thời gian học trung bình |

→ Mỗi phase tách `.plans/training-elearning-phase-N/` riêng để tracking độc lập.
