# Plan — Xử lý bài học bị xóa/khóa khi học viên đang học (elearning)

Owner: @junfoke
Ngày tạo: 2026-07-19

## Bối cảnh lỗi

Khi học viên đang học / đang xem video mà admin cấu hình **xóa bài học** (hoặc bài bị **khóa** do prerequisite thay đổi):
- Hiện tại: sau khi tải lại / thao tác → màn trắng (LessonViewer crash do `lesson.content.url` khi content null; hoặc `currentLesson` = null không có empty state rõ ràng); heartbeat trả 422/423 nhưng FE nuốt lỗi im lặng.
- Mong muốn (đã chốt với user):
  1. Hiện toast "Bài học đã bị xóa/khóa" + **tự chuyển sang bài hợp lệ gần nhất** (bài trước/đang học dở). Hết bài hợp lệ → empty state rõ ràng.
  2. Xử lý **cả khi đang xem video** (không cần reload) — dựa vào heartbeat trả 422 (xóa) / 423 (khóa) mà BE ĐÃ có sẵn.

## Phát hiện chính

- BE `LearningSessionService::processHeartbeat` đã trả `422` ("Bài học không thuộc khoá học này" = bị xóa) và `423` ("Bài học đang bị khoá") → **không cần sửa BE**.
- `responseJson($msg, $code)` set HTTP status = code → axios đọc `error.response.status`.
- FE `useHeartbeat`/`useScormCommit` đang retry 1 lần rồi nuốt lỗi.

## Tasks

### FE — elearning/
- [x] `composables/useHeartbeat.js`: thêm callback `onUnavailable(subjectLessonId, reason)`; bắt 422→'removed', 423→'locked'; KHÔNG retry lỗi này.
- [x] `composables/useScormCommit.js`: wire cùng `onUnavailable`.
- [x] `stores/learningSession.js`: thêm `removeLessonBySubjectLessonId()`, `markLessonLockedBySubjectLessonId()`, helper `prevValidFromSubjectLessonId()` (bài hợp lệ trước bài bị gỡ).
- [x] `views/subject/SubjectLearnView.vue`:
  - Wire `onUnavailable` vào heartbeat/scorm → `handleLessonUnavailable()` (toast + gỡ/khóa bài + chuyển bài hợp lệ). Chống xử lý lặp bằng Set.
  - `initCourse`: khi URL `lessonId` không resolve → phân biệt xóa/khóa → toast + resume. Chỉ toast khi có `lessonId` tường minh.
- [x] `components/learning/LessonViewer.vue`: guard `lesson.content` (defense-in-depth) → không crash màn trắng, hiện "Nội dung bài học không khả dụng".

### Verify
- [x] `vite build` (Node 24) pass sạch toàn bộ file đã sửa.
- [x] Reload màn học với `lessonId` không tồn tại → toast "Bài học đã bị xóa. Đã chuyển bạn sang bài phù hợp." + tự chuyển sang bài hợp lệ, KHÔNG màn trắng (Playwright, tài khoản employee SSO).
- [x] Live: mock heartbeat trả 422 khi đang xem → bài bị gỡ khỏi store + empty state "Chọn 1 bài ở sidebar", KHÔNG màn trắng (verify 2 lần, có screenshot).

## Checkpoint — 2026-07-19
Vừa hoàn thành: Toàn bộ FE fix + verify Playwright (cả reload lẫn live 422). BE không cần sửa (đã trả sẵn 422/423).
Đang làm dở: (không)
Bước tiếp theo: User review; nếu OK có thể bổ sung test-case/HDSD nếu cần.
Blocked: (không)

## Phase 2 — Bài học / Khóa học bị admin "Khóa" (status) khi đã có người học

Chi tiết + quyết định: xem [design-locked-status.md](design-locked-status.md).

### Tasks (đã xong)
- [x] BE transformer: ẩn bài `lesson.status = LOCKED`.
- [x] BE `recalculateCourseProgress`: loại bài khóa khỏi mẫu số tiến độ.
- [x] BE `LessonLockResolver`: bỏ bài khóa khỏi linear/prerequisite (+ isLessonLocked load `.lesson`).
- [x] BE heartbeat/scormCommit: bài khóa → 422 (FE tái dùng luồng "bài đã xóa").
- [x] BE `getSessionData`: `subject.status = KHOA` → 423 (chặn khi reload).
- [x] BE `MyLearningService@getInProgress`: cờ `locked` + nhãn "Đã khóa".
- [x] FE store `courseLocked` từ 423; `SubjectLearnView` màn chặn "Khóa học đã bị khóa".
- [x] FE `StudyCard` + `MyLearningView`: badge "Đã khóa" + chặn nút Tiếp tục.
- [x] Verify: php -l + vite build sạch; Playwright màn chặn 423 + badge "Đã khóa".

## Checkpoint — 2026-07-20
Vừa hoàn thành: Phase 2 — xử lý bài/khóa bị admin KHÓA khi đã có người học (BE + FE, verify Playwright FE).
Đang làm dở: (không)
Bước tiếp theo: User tự khóa 1 khóa/bài thật để xác nhận E2E toàn trình (mình không đổi DB).
Blocked: (không)

## Phase 3 — Bug fix: KHÓA cả khóa/lộ trình giữa lúc đang học không chặn ngay (chỉ chặn khi reload)

Triệu chứng: đang học, admin KHÓA khóa học → heartbeat vẫn trả 200, trạng thái bài vẫn đổi bình thường; phải reload mới hiện màn "Khóa học đã bị khóa".

Root cause: `processHeartbeat` + `processScormCommit` KHÔNG check `subject.status = KHOA` (chỉ `getSessionData` lúc reload mới check). 423 lại đang bị dùng cho cả "khóa 1 bài do prerequisite" nên không thể trả 423 trần → FE hiểu nhầm.

### Tasks (đã xong)
- [x] BE `LearningSessionService`: tách helper `checkSubjectAccessLock()` từ `getSessionData` (Subject KHOA + Lộ trình khóa); dùng lại trong `getSessionData`, `processHeartbeat`, `processScormCommit`. Trả 423 kèm `data.scope` = `course`/`path`.
- [x] BE `LearningSessionController`: truyền `$result['data']` xuống `responseJson` (heartbeat/scorm/show).
- [x] FE `useHeartbeat.js` + `useScormCommit.js`: `handleUnavailable` đọc `body.data.scope`; 423 có scope → reason `course_locked`, 423 trần → `locked` (giữ nguyên). Truyền `e.response?.data` vào.
- [x] FE `SubjectLearnView.vue`: `handleLessonUnavailable` thêm nhánh `course_locked` → stop heartbeat/scorm + `store.courseLocked = true` → màn chặn hiện ngay.

### Verify
- [x] php -l 2 file BE + vite build (Node 24) sạch.
- [x] E2E Playwright: đang học bài text (khóa `onboarding-nhan-vien-moi`), route-mock heartbeat trả `423 + data.scope=course` → tới nhịp heartbeat màn "Khóa học đã bị khóa" hiện NGAY, không reload (không đụng DB).
- [ ] E2E thật: user tự KHÓA 1 khóa lúc đang học để xác nhận toàn trình BE→FE.

## Checkpoint — 2026-07-20
Vừa hoàn thành: Phase 3 — code + verify Playwright (mock 423+scope → màn khóa hiện ngay không reload). php -l + vite build sạch.
Đang làm dở: (không)
Bước tiếp theo: User khóa 1 khóa thật lúc đang học để xác nhận E2E toàn trình (mình không đổi DB).
Blocked: (không)

## Phase 4 — Cải thiện xử lý xóa bài khi đang xem video (theo phản hồi end-user)

Yêu cầu end-user: đang học bài mà bị xóa → toast + chuyển sang BÀI KẾ TIẾP; nếu khóa chỉ còn 1 bài (hết bài hợp lệ) → về màn CHI TIẾT KHÓA. Phát sinh: video done/pause thì handleProgress không bắn heartbeat nên xóa bài / khóa khóa không được phát hiện live.

### Tasks (đã xong)
- [x] FE store `learningSession.js`: thêm getter `nextValidFromSubjectLessonId()` (ưu tiên bài kế tiếp, lùi về bài trước nếu hết, null nếu không còn bài).
- [x] FE `SubjectLearnView.vue` `handleLessonUnavailable`: dùng `nextValidFromSubjectLessonId` (thay `prevValid`); hết bài hợp lệ → `router.replace({ name: 'subject-detail' })` (màn chi tiết khóa) thay vì empty state. Áp cho cả reason `removed` lẫn `locked`.
- [x] FE `SubjectLearnView.vue`: thêm ping "kiểm tra khả dụng" định kỳ 30s (`startAvailabilityPing`/`stopAvailabilityPing`) — gửi heartbeat với tiến độ đã lưu bất kể video done/pause/đang phát (BE lấy max nên không tụt), để phát hiện xóa bài / khóa khóa đúng hạn mọi trạng thái. Dừng ping khi course_locked, khi rời màn, khi đổi khóa trong lộ trình.

### Verify
- [x] vite build (Node 24) sạch.
- [x] E2E Playwright: đang học bài text khóa `onboarding-nhan-vien-moi` (1 bài), mock heartbeat 422 → tới nhịp (~30s) tự redirect về màn chi tiết khóa (`subject-detail`), không kẹt empty state, không về trang chủ. Screenshot xác nhận.
- [ ] E2E đa-bài: xóa bài giữa chừng → chuyển sang bài kế tiếp (chưa có data nhiều bài để test; logic mirror `prevValid` đã test).

## Checkpoint — 2026-07-20
Vừa hoàn thành: Phase 4 — nextValid + redirect chi tiết khóa khi hết bài + ping khả dụng 30s. Verify Playwright case 1-bài redirect OK.
Đang làm dở: (không)
Bước tiếp theo: Khi có khóa nhiều bài, verify chuyển-sang-bài-kế-tiếp; user xóa bài thật lúc đang xem video để xác nhận E2E.
Blocked: (không)

## Phase 5 — Ẩn bài `lesson.status = LOCKED` ở màn CHI TIẾT khóa học + lộ trình

Triệu chứng (user báo): màn chi tiết lộ trình / chi tiết khóa vẫn hiện bài bị admin KHÓA kèm nút "Vào học", trong khi màn HỌC đã ẩn (Phase 2). Gap đã ghi trong [design-locked-status.md](design-locked-status.md) §1 ("Danh sách bài ở trang chi tiết ❌ Không xét").

Root cause: `LearningSessionResource` (màn học) lọc bài LOCKED qua `isLessonHidden`, nhưng transformer chi tiết `SubjectDetailResource` + `LearningPathLearnerResource`/`LearningPathPublicResource` KHÔNG lọc. Hai transformer này **dùng chung với màn quản trị HRM** (`Training\SubjectController`, `Training\LearningPathController`) — admin cần thấy bài khóa để sửa → KHÔNG sửa trong transformer.

Giải pháp: lọc ở **cấp controller elearning** (gỡ bài LOCKED khỏi relation đã load trước khi transform) → chỉ ảnh hưởng endpoint elearning, admin nguyên vẹn. Tổng bài/tiến độ tự loại theo (nhất quán `recalculateCourseProgress`).

### Tasks
- [x] BE: tạo helper `Modules/Elearning/Support/LockedLessonFilter.php` — gỡ bài `lesson.status = LOCKED` khỏi `subject->subjectLessons` + `chapters->subjectLessons` (dùng `setRelation` in-place, chỉ trong request).
- [x] BE `SubjectDetailController@show`: gọi filter sau `$subject->load(...)`.
- [x] BE `LearningPathDetailController@show`: gọi filter cho từng `learningPathSubjects->subject` (trước khi branch learner/public → cả 2 transformer đều được lọc).
- [x] Verify: `php -l` sạch 3 file. [ ] User tự khóa 1 bài thật để xác nhận màn chi tiết ẩn bài + nút "Vào học" (không đổi DB được nên chưa E2E).

## Checkpoint — 2026-07-28
Vừa hoàn thành: Phase 5 — ẩn bài LOCKED ở màn chi tiết khóa + lộ trình. Filter ở tầng controller elearning (helper `LockedLessonFilter`), KHÔNG đụng transformer dùng chung với admin HRM. php -l sạch.
Đang làm dở: (không)
Bước tiếp theo: User khóa 1 bài thật rồi mở màn chi tiết khóa + chi tiết lộ trình để xác nhận bài khóa biến mất (và tổng số bài giảm theo).
Blocked: (không) — không đổi được DB nên E2E thật do user thực hiện.

## Phase 6 — Admin HRM: chặn LƯU khóa học còn chứa bài học bị KHÓA (lesson.status = LOCKED)

Triệu chứng (user báo): màn Sửa khóa học (hrm-client) cho lưu bình thường dù trong khóa còn bài học đang ở trạng thái KHÓA, không cảnh báo gì.

Bối cảnh: picker chọn bài (`LessonService::getAllForSelect`) đã lọc `STATUS_ACTIVE` → không thêm MỚI bài khóa được. Lỗ hổng: bài thêm lúc active, sau đó admin khóa → nằm im trong khóa. Mirror y pattern "bài học lỗi (đã bị xóa khỏi ngân hàng)" đã có sẵn (banner + dòng đỏ + chặn Lưu).

Quyết định (2026-07-28): (a) hiển thị GIỐNG HỆT bài lỗi (dòng đỏ + banner + chặn Lưu); (b) chặn cả Lưu nháp.

### Tasks
- [x] BE `SubjectDetailResource::mapSubjectLessons`: thêm `'status' => (int) $lesson->status` vào object `lesson` (để FE nhận biết bài khóa). Additive.
- [x] BE `SubjectBuilderRequest::withValidator`: after-check → có `lesson_id` status=LOCKED → add lỗi `locked_lessons` (áp cả nháp, không skip DRAFT). FormRequest tự throw ValidationException 422.
- [x] FE `tabs/TabInfo.vue`: `isLockedLesson` + `lockedLessonCount` + banner + class đỏ per-row (`lesson-row--broken` dùng chung) + text "Bài học đã bị khóa — vui lòng gỡ..." + `error.locked_lessons`; ẩn nút cấu hình mapping cho bài khóa (chỉ còn nút Xoá).
- [x] FE `SubjectBuilderForm.vue`: `countLockedSubjectLessons()`; chặn trong `validate()` + `saveDraft()`; key `locked_lessons` map về tab info qua `getTabForKey` (default) + `applyBackendErrors` surface lỗi BE.
- [x] Verify: `php -l` sạch 2 file BE. FE mirror y pattern broken-lesson (không có eslint trong repo, build nặng → user verify browser). [ ] User tự khóa 1 bài đang thuộc khóa rồi mở Sửa → thấy cảnh báo đỏ + không lưu được.

## Checkpoint — 2026-07-28
Vừa hoàn thành: Phase 6 — admin HRM chặn lưu khóa học còn chứa bài bị KHÓA. BE: expose lesson.status + validate `locked_lessons`. FE: banner + dòng đỏ + chặn Lưu & Lưu nháp (mirror broken-lesson). php -l sạch.
Đang làm dở: (không)
Bước tiếp theo: User khóa 1 bài đang thuộc 1 khóa học, mở Sửa khóa đó → xác nhận dòng bài đỏ + banner + bấm Lưu/Lưu nháp bị chặn với lỗi inline.
Blocked: (không)
