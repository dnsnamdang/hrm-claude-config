# Elearning — Học liền mạch lộ trình — Plan

> Owner: @junfoke · Spec: `docs/superpowers/specs/2026-06-03-elearning-learning-path-seamless-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-06-03-elearning-learning-path-seamless.md`
> Không migration. Không commit git. Verify browser (Docker Node ≥18) + API thật.

## Phase 1 — BE: lock cấp khoá (linear_required)
- [x] Task 1: `LearningPathLearnerResource` — thêm cờ `locked` cấp khoá (linear_required && có khoá trước chưa done)

## Phase 2 — BE: chứng chỉ lộ trình
- [x] Task 2: `CertificateFieldResolver` (helper tên học viên dùng chung, không sửa CertificateService khoá)
- [x] Task 3: `LearningPathCertificateService` (check path done theo result_rule + resolve field từ certificate_fields JSON + ngày cấp = completed_at trễ nhất)
- [x] Task 4: `LearningPathCertificateController` + route `GET /learning-paths/{slug}/certificate` (elearning.auth)

## Phase 3 — FE: context ?lp, lock khoá, điều hướng
- [x] Task 5: store `learningPathDetail.mapCourses` — map `locked` cấp khoá
- [x] Task 6: `PathOutline` — badge 🔒 Khoá ở header khoá bị lock
- [x] Task 7: `ContentDetailView.handleOpenLesson` (chặn khoá lock + ?lp) + `goCertificate` (route LP) + `useContentDetail.handleStartLearn` (resume xuyên khoá + bỏ khoá lock + ?lp)

## Phase 4 — FE: SubjectLearnView LP mode + modal 3 biến thể
- [x] Task 8: `SubjectLearnView` — đọc ?lp, Quay lại về lộ trình, refetch LP khi xong khoá, truyền props modal
- [x] Task 9: `CourseCompleteModal` — 3 biến thể (khoá tiếp theo / hoàn thành lộ trình + cert / khoá lẻ cũ)

## Phase 5 — FE: trang chứng chỉ lộ trình
- [x] Task 10: store `certificate.fetchPathCertificate`
- [x] Task 11: `CertificateView` theo `route.meta.entityType` + route `/chung-chi-lo-trinh/:slug`
- [x] Task 12: Verify nút "Chứng chỉ" trang lộ trình (DetailEnrollCard đã emit sẵn, chỉ cần goCertificate route đúng)

## Phase 6 — Verify
- [x] Task 13: 8 kịch bản end-to-end (browser + API)

## Ghi chú
- Cần xác nhận khi code: tên route danh sách lộ trình; cast `certificate_fields`/`certificate_enabled` trên LearningPath; style khai báo route api.php.

### Checkpoint — 2026-06-03
Vừa hoàn thành: CODE DONE 13/13 task (6 phase) qua subagent-driven. BE 5 file (LearningPathLearnerResource +locked, CertificateFieldResolver, LearningPathCertificateService, LearningPathCertificateController, route). FE 8 file (store learningPathDetail +locked, PathOutline badge khoá, ContentDetailView handleOpenLesson+goCertificate, useContentDetail handleStartLearn resume xuyên khoá, SubjectLearnView LP mode + initCourse re-fetch khi đổi slug, CourseCompleteModal 3 biến thể, certificate store fetchPathCertificate, CertificateView theo entityType, router route learning-path-certificate).
Xác nhận khi code: LearningPath đã có sẵn cast certificate_fields/certificate_enabled (không sửa entity); route api.php dùng class import; route list lộ trình tên `learning-path-list`.
Fix phát sinh khi review: SubjectLearnView trước chỉ fetchCourseData trong onMounted → bấm "Học khoá tiếp theo" (đổi slug, cùng component) không nạp khoá mới. Đã tách `initCourse()` + watch route.params.slug (teardown heartbeat/scorm cũ trước khi re-init).
Fix phát sinh khi user test: đổi bài trong màn học (`handleSelectLesson` + resume `router.replace`) dùng `router.push({params})` KHÔNG truyền query → Vue Router xoá `?lp`, mất context lộ trình. Đã thêm `query: { ...route.query }` vào cả push (đổi bài) và replace (resume). Next/Prev/Prereq đi qua handleSelectLesson nên được bao phủ.

## Phase 11: Hoàn thiện học tuần tự cấp khoá (2026-06-03)
Quyết định: chặn MỀM (UI, không hard-enforce BE); khoá tuỳ chọn VẪN chặn theo thứ tự.
- [x] Task 55: BE `LearningPathLearnerResource` — khoá đã `done` KHÔNG bị khoá (`locked = linear && !prevAllDone && learn_status !== 'done'`). Sửa kịch bản: học xong khoá lẻ trước rồi mới tham gia lộ trình tuần tự → khoá đó vẫn xem lại được.
- [x] Task 56: FE `PathLessonRow` — khoá bị khoá → nút "Vào học" đổi thành nút "Khoá" disabled (cursor-not-allowed + title), tránh ấn nhầm. Toast ở handleOpenLesson giữ làm backstop.

### Fix (2026-06-03): khoá có bài đang học vẫn hiện "Chưa học"
`SubjectEnrollment.status` chỉ lên LEARNING khi đã có bài DONE (recalc theo progress, không bump khi bài mới chỉ learning). → outline khoá hiện "Chưa học" dù bài đã "Đang học". Fix read-side `LearningPathLearnerResource.mapSubjectWithProgress`: nếu status='enrolled' nhưng có bài learning/done trong `lessonStatusByLessonId` → suy ra 'learning'. (Không sửa recalc heartbeat — core dùng chung; lag tương tự ở trang chi tiết khoá lẻ chưa report nên giữ nguyên.)

### Fix race condition (2026-06-03): modal hoàn thành khoá bắn SAI khi "Học khoá tiếp theo"
Triệu chứng: bấm "Học khoá tiếp theo" sang khoá cuối, vừa vào (bài 1 đang học, bài 2 chưa học) đã hiện modal "Chúc mừng hoàn thành khoá". Outline lộ trình vẫn đúng (khoá đó "Chưa học") → lỗi thuần FE.
Nguyên nhân: `initCourse` gọi `heartbeat.teardown()`/`scormCommit.flush()` cho khoá CŨ (fire-and-forget) RỒI `fetchCourseData` khoá mới. Response commit khoá cũ (`enrollment_status=done`) vọng về SAU khi `this.enrollment` đã là khoá mới → `handleHeartbeatResponse` gán nhầm done + `courseCompletionSignal++` → modal sai. BE không bị ảnh hưởng (outline đúng).
Fix: `learningSession.handleHeartbeatResponse` — early return nếu `subject_lesson_id` của response không thuộc khoá đang mở (`!lesson`). Chặn luôn toast "hoàn thành bài" sai. File: `elearning/src/stores/learningSession.js`.

### Quyết định (2026-06-03): lock cấp BÀI ở outline
Lock cấp bài (linear_required của khoá + prerequisite) CHỈ enforce trong màn học (LessonLockResolver BE + recomputeLocks FE); vào bài bị khoá → tự nhảy về bài được phép. Outline lộ trình KHÔNG hiển thị 🔒 cấp bài (hardcode locked=false) — nhất quán với outline khoá lẻ. User chốt GIỮ NGUYÊN, không thêm tính `locked` cấp bài vào outline.
Đang làm dở: không.
Bước tiếp theo: User chạy dev server Docker (Node ≥18) → verify 8 kịch bản Phase 6. KHÔNG migration. BE test bằng gọi API thật.
Blocked: không.
