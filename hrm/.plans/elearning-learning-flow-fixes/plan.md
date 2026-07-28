# Plan — Fix 3 bug luồng học lộ trình elearning

> Owner: @junfoke · Bắt đầu: 2026-07-22

## Bối cảnh
3 bug do user báo (2026-07-22) về luồng: lộ trình → tiếp tục học → khóa tiếp theo, và đếm bài ở góc học tập.
Root cause đã điều tra + xác nhận bằng code lẫn dữ liệu thật (tinker).

## Bug 1 — "Tiếp tục học"/"Khóa tiếp theo" kẹt ở khóa không khả dụng
Root: FE chọn khóa đích chỉ lọc `!locked && slug`, bỏ sót `available` → chọn nhầm khóa admin-KHÓA
(available=false) → 423 kẹt. Lộ trình tuần tự: khóa KHÓA (không bao giờ done) khóa vĩnh viễn khóa sau.
Quyết định user: sửa **cả FE + BE**.

- [x] BE `LearningPathLearnerResource` (Modules/Training, dùng chung): linear-lock bỏ qua khóa
      `available=false` khi tính `prevAllDone` (không coi là "chặn" khóa sau)
- [x] FE `useContentDetail.js` `handleStartLearn`: thêm điều kiện `c.available` khi lọc khóa đích
- [x] FE `SubjectLearnView.vue` watch `courseCompletionSignal` (nextCourse): thêm `c.available`

## Bug 2 — Đếm số bài học ở góc học tập sai khi có bài bị khóa
Root: đếm "x bài học" gồm cả bài admin-KHÓA (Lesson STATUS_LOCKED), trong khi mẫu số tiến độ loại bài KHÓA
→ lệch "Bài x/y". Phạm vi: **góc học tập** (MyLearningService).

- [ ] MyLearningService: helper `learnableLessonCount()` loại bài STATUS_LOCKED (cache lockedLessonIds)
- [ ] Áp cho 4 chỗ đếm: in_progress khóa lẻ (:115), required khóa (:341), required lộ trình (:367),
      pathChildren (:481). `lessonsDone` (:126) tự đúng theo `lessons` mới.

## Bug 3 — "Xem lại nội dung"/"Tiếp tục học" trỏ vào khóa không khả dụng
CHẨN ĐOÁN LẠI (sau khi user gửi repro thật): KHÔNG phải lỗi thiếu enrollment (giả thuyết auto-enroll
ban đầu đã GỠ). Repro thật: lộ trình CÔNG KHAI #23, khóa A public (Đạt), khóa B private (is_public=0,
"Không còn khả dụng" với học viên ngoài). Học xong A, nhấn "Xem lại nội dung" trên lộ trình đã hoàn thành
→ `handleStartLearn` chọn nhầm khóa B (available=false) làm đích → màn khóa 423.
=> CÙNG root cause với Bug 1 (handleStartLearn không loại khóa available=false). User xác nhận: GIỮ
chặn học khóa private (đúng Phase 3), chỉ cần nút không trỏ vào khóa không khả dụng.

- [x] Fix chính = bản Bug 1 (`useContentDetail.js` thêm `c.available`) → nút trỏ sang khóa A khả dụng
- [x] FE `ContentDetailView.handleOpenLesson` (nhánh path): thêm guard `course.available === false`
      → toast "Không còn khả dụng" thay vì nhảy vào màn 423 (nhất quán click trực tiếp trong outline)
- [x] KHÔNG đổi logic private / KHÔNG đảo Phase 3 / KHÔNG auto-enroll (đã gỡ)

## Bug 4 — Lộ trình ở góc học tập bị "Đã hoàn thành" dù còn khóa chưa học
Repro: LP#24 "Lộ trình test 022" (public, REQUIRED_ONLY), learner#2 xong 1/3 khóa nhưng
`learning_path_enrollments.status=DONE` → góc học tập xếp vào "Đã hoàn thành" + biến mất khỏi "Đang học".
Root: status DONE bị CŨ — khóa 82/84 thêm vào lộ trình SAU khi hoàn thành (lúc đó lộ trình chỉ có 83).
Code demote `recalcEnrollmentsAfterRebuild` (LearningPathService::update) ĐÃ đúng (repro local PASS +
user re-save fix được), chỉ chạy khi lộ trình được SỬA → bản ghi cũ kẹt tới khi có tác động. Local sạch
(0 ca) → không phải lỗi hệ thống. User chọn hướng (b): guard hiển thị.

- [x] BE `MyLearningService` helper `pathTrulyComplete()` (mirror syncLearningPathCompletion, CHỈ đọc)
- [x] `getInProgress`: nạp thêm status=DONE + kéo lộ trình DONE-nhưng-chưa-xong-thật về "Đang học"
- [x] `getCompleted`: bỏ qua lộ trình DONE-chưa-xong-thật
- [x] `getCertificates`: không cấp chứng chỉ lộ trình khi chưa xong thật
- [x] KHÔNG ghi DB (guard chỉ hiển thị) — status lưu vẫn tự đúng khi lộ trình được sửa
- Verify tinker 2 pha PASS (stale→Đang học; xong thật→Đã hoàn thành), rollback sạch

## Bug 5 — Vào học khóa thêm-sau-ghi-danh báo 403 "không tìm thấy" (auto-enroll)
Gap: user ghi danh lộ trình (khóa A,B) → admin thêm khóa C → user vào học C → thiếu SubjectEnrollment
(enrollPath chỉ enroll lúc ghi danh) → getSessionData `findEnrollment` null → 403 → FE "Không tìm thấy".
DB dev có 23 gap thật. User yêu cầu fix (2026-07-22). Chọn Cách 2 (runtime lazy-enroll — tự vá cả gap
cũ lẫn mới, gọn 1 chỗ, không bulk/backfill).

- [x] BE `LearningSessionService::getSessionData`: thiếu enrollment NHƯNG khóa thuộc lộ trình user đã
      ghi danh (qua `belongsToEnrolledPath`, đã qua checkSubjectAccessLock) → `autoEnrollSubject`
      (firstOrCreate) rồi cho học. Khóa standalone không thuộc lộ trình đã ghi danh vẫn giữ 403.
- Verify tinker: gap employee#28 khóa#62 → OK auto-enroll (enrollment tạo ra); control standalone → 403 giữ nguyên. Rollback sạch.

## Verify
- [x] php -l 3 file BE (sạch)
- [x] tinker Bug 2: khóa 1 bài → learnableLessonCount giảm đúng 1, rollback sạch
- [x] Bug 1/3: trace logic trên data thật LP#23 (public, A available, B available=false → nút trỏ A)
- [x] Không git/migration; DB nguyên trạng (mọi test transaction rollback)
- [ ] FE elearning: deploy lên remote → user verify browser (Docker/deploy)

## Phát hiện phụ (chưa fix — chờ user)
- 23 khóa con thuộc lộ trình đã ghi danh nhưng thiếu `SubjectEnrollment` (thêm vào lộ trình sau khi
  ghi danh) → nhân viên vào bị 403 "không tìm thấy". Vấn đề độc lập, không thuộc 3 bug này.

---

### Checkpoint — 2026-07-22
Vừa hoàn thành: Fix cả 3 bug (bug 1+3 chung root `handleStartLearn` thiếu `c.available`; bug 2 đếm bài
loại STATUS_LOCKED). Đã gỡ bản auto-enroll chẩn sai. php -l sạch, tinker verify bug 2 PASS.
Đang làm dở: (không) — code hoàn tất.
Bước tiếp theo: user deploy FE elearning lên remote eteksofts.com → verify browser (Akira Lee, học viên
ngoài): "Xem lại nội dung" trỏ về khóa A + góc học tập đếm bài đúng khi có bài khóa.
Blocked:
