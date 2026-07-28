# Plan — Chặn học viên ngoài truy cập khóa học đã chuyển public → private

Phụ trách: @junfoke

## Bối cảnh (bug)
Khóa học đang public → học viên ngoài (learner) tham gia thành công → admin chuyển khóa sang **private** (`is_public = 0`, `status` vẫn HOẠT_ĐỘNG).
Hiện tượng lỗi (data test 014, 015):
- Học viên vẫn vào học tiếp được (kể cả reload).
- Vẫn ghi được tiến độ (heartbeat / scorm).
- Khóa vẫn nằm trong "Góc học tập > Đang học".

## Nguyên nhân gốc
Kiểm tra `is_public` chỉ có ở màn chi tiết (`SubjectDetailController::show`), THIẾU ở tầng học nội dung và góc học tập:
- `LearningSessionService::checkSubjectAccessLock` chỉ chặn khi `status = KHÓA` (423), không xét `is_public`.
- `MyLearningService::getInProgress` chỉ gắn cờ `locked` khi `status = KHÓA`, không xét `is_public`.

Đây là bản sinh đôi của feature `elearning-learning-path-visibility` (feature đó chỉ vá tầng DUYỆT/tìm kiếm, chưa vá tầng truy cập của người đã enroll).

## Quyết định (user chốt)
1. Góc học tập: khóa private vẫn HIỆN nhưng gắn cờ `locked` + nhãn "Không còn khả dụng", chặn nút Tiếp tục.
2. Nhân viên nội bộ (`user_type = employee`) KHÔNG bị ảnh hưởng bởi private — chỉ chặn học viên ngoài.
3. Không gây regression: khóa private là khóa CON của lộ trình đang hoạt động mà học viên đã ghi danh → vẫn cho học (truy cập hợp lệ qua lộ trình).

## Task
### BE (hrm-api, Modules/Elearning — branch tpe-develop-elearning)
- [x] `LearningSessionService::checkSubjectAccessLock`: thêm gate — `user_type != 'employee'` && `!is_public` && không vào qua lộ trình ACTIVE đã ghi danh → trả 423 `scope='private'`, message "Khóa học không còn khả dụng". (Tự động phủ getSessionData + heartbeat + scorm-commit vì cả 3 gọi hàm này.) Refactor query lộ trình chứa khóa để dùng chung 1 lần cho cả check private + check path-locked.
- [x] `MyLearningService`: truyền `$userType` xuống `getInProgress`; card khóa lẻ gắn `locked = true` + `learnStatusLabel = 'Không còn khả dụng'` khi `learner` && `!is_public` (cộng dồn với điều kiện KHÓA cũ). Khóa con của lộ trình đã bị filter khỏi danh sách khóa lẻ nên không đụng.
- [x] `SubjectDetailController::enroll`: chặn learner ngoài ghi danh khóa private qua API trực tiếp (403) — defense-in-depth, nhất quán với `show`.

### FE (elearning)
- [x] `StudyCard.vue`: render nhãn khóa theo `item.learnStatusLabel` (fallback 'Đã khóa') thay vì hardcode, để phân biệt "Đã khóa" (admin) vs "Không còn khả dụng" (private).
- [x] `stores/learningSession.js` `fetchCourseData`: bắt `scope` từ response 423 → lưu `lockScope`.
- [x] `views/subject/SubjectLearnView.vue`: màn chặn hiển thị tiêu đề/nội dung theo `lockScope` ('private' → "Khóa học không còn khả dụng").
- [x] `composables/useHeartbeat.js`: map `scope='private'` → reason `course_locked` (chặn cả khóa khi flip private giữa phiên), thay vì hiểu nhầm là khóa 1 bài.

### Verify
- [x] Học viên ngoài: khóa public→private → vào `/learn` bị chặn, heartbeat 423, góc học tập card locked. (PASS tinker 2026-07-20: [1B] learner+private=423 scope=private; [1D] card locked "Không còn khả dụng")
- [x] Nhân viên: vẫn học bình thường. ([1C] employee+private KHÔNG ra scope=private)
- [x] Khóa private là con của lộ trình ACTIVE+public đã ghi danh → vẫn học được. ([2A]/[2B] PASS)

### Checkpoint — 2026-07-20
Vừa hoàn thành: Toàn bộ code fix BE (3 điểm) + FE (4 file). Lint PHP sạch. Root cause: thiếu check `is_public` ở tầng học nội dung + góc học tập (chỉ có ở màn chi tiết).
Đang làm dở: không
Bước tiếp theo: user verify trên trình duyệt (hoặc dùng Playwright) — 3 case ở mục Verify.
Blocked:

## Task — Phase 2: áp dụng cho LỘ TRÌNH (learning path) public → private
User yêu cầu xử lý luôn (2026-07-20). Học lộ trình = học khóa con qua `subject-learn`, nên lỗ hổng tinh vi hơn.
Hiện trạng: `LearningPathDetailController::show` ĐÃ 403 cho học viên ngoài + lộ trình private. Thiếu ở 3 điểm:
- [x] `LearningPathDetailController::enroll`: chặn học viên ngoài ghi danh lộ trình private (403).
- [x] `LearningSessionService::checkSubjectAccessLock`: siết ngoại lệ "khóa private truy cập qua lộ trình" — chỉ cho khi lộ trình ACTIVE **và CÔNG KHAI** (trước đó chỉ xét ACTIVE). Vì vậy lộ trình private + khóa con private → chặn 423 scope='private'. Lấy thêm `is_public` của lộ trình chứa khóa (query dùng chung).
- [x] `MyLearningService::getInProgress` ($paths): card lộ trình private gắn `locked=true` + nhãn "Không còn khả dụng" cho học viên ngoài (cộng dồn điều kiện LOCKED cũ).
- [x] FE: không cần sửa thêm — `StudyCard.vue` đã dùng `item.learnStatusLabel` chung cho cả card lộ trình; nút "Học" khóa con dùng cờ `locked` của lộ trình.

### Verify Phase 2
- [x] Học viên ngoài: lộ trình public→private → góc học tập card locked "Không còn khả dụng" ([2C] PASS); học khóa con private của lộ trình private bị chặn 423 ([2D] PASS).
- [x] Khóa con PUBLIC của lộ trình private → vẫn học được ([2B] PASS).
- [x] Nhân viên: không ảnh hưởng ([1C] PASS).

Ghi chú verify: dùng tinker gọi thẳng LearningSessionService::getSessionData + MyLearningService::build với data thật (learner 5, khóa 45/52 standalone, LP 1 + khóa con 42), flip is_public tạm rồi khôi phục (try/finally, net DB không đổi — đã xác nhận subject 42/44/45/49/52 + LP1 đều is_public=1 sau test). KHÔNG dùng browser vì tài khoản dev có sẵn là employee (không tái hiện được bug vốn chỉ ảnh hưởng learner ngoài).

### Checkpoint — 2026-07-20 (Phase 2)
Vừa hoàn thành: mở rộng fix sang lộ trình private (3 điểm BE), FE tái dùng. Root cause bổ sung: ngoại lệ path-access trong checkSubjectAccessLock chỉ xét ACTIVE → lộ trình private vẫn cho học khóa con private. php -l sạch.
Đang làm dở: không
Bước tiếp theo: user verify browser cả Phase 1 (khóa) + Phase 2 (lộ trình).
Blocked:

## Task — Phase 3: ĐẢO quyết định — khóa private LUÔN chặn học viên ngoài (kể cả trong lộ trình public)
User yêu cầu (2026-07-21). Đảo ngược **Quyết định #3** (dòng 22 & task [2]/dòng 39): trước đây "khóa con private của lộ trình ACTIVE + công khai đã ghi danh → vẫn cho học"; giờ coi đây là BUG.

Hiện tượng: Lộ trình (public, active) chứa khóa public → học viên ngoài ghi danh lộ trình → admin chuyển khóa sang private (chưa khóa) → học viên ngoài vẫn vào học, ghi tiến độ, xem được khóa + còn trong góc học tập. Nguyên nhân: ngoại lệ `viaAccessiblePath` cố tình cho phép.

Quyết định mới (user chốt 2026-07-21):
- Private = CHỈ nội bộ, bất kể đường vào → bỏ hoàn toàn ngoại lệ `viaAccessiblePath`.
- KHÔNG chặn ở bước ghi danh lộ trình (lộ trình vẫn public → vẫn cho tham gia; khóa private trong đó hiện "Không còn khả dụng", học tiếp các khóa public khác).
- Nhân viên nội bộ KHÔNG bị ảnh hưởng (giữ nguyên).

### BE (hrm-api, Modules/Elearning — non-shared)
- [x] `LearningSessionService::checkSubjectAccessLock`: bỏ ngoại lệ `viaAccessiblePath` — `user_type != 'employee'` && `!is_public` → LUÔN 423 `scope='private'`. Giữ query lộ trình chứa khóa vì check path-locked bên dưới còn dùng `$containingPathStatuses`. (Phủ getSessionData + heartbeat + scorm.)
- [x] `MyLearningService::childLockState`: bỏ ngoại lệ `viaAccessiblePath` — `isExternal` && `!is_public` → LUÔN `locked` + "Không còn khả dụng". (Filter `getInProgress` không cần đổi: childLockState mới sẽ khóa khóa con private trong thẻ lộ trình; card khóa lẻ dòng 137 đã xử lý sẵn từ Phase 1.)

### Polish UX trang chi tiết lộ trình (user OK sửa hàm dùng chung + FE, 2026-07-21)
- [x] `LearningPathLearnerResource::mapSubjectWithProgress` (Modules/Training — DÙNG CHUNG): thêm cờ additive `available` (false khi `user_type != employee` && khóa private) + `unavailable_label`="Không còn khả dụng". Truyền `$userType` xuống. Employee/HRM nội bộ mặc định `available=true` → không đổi hành vi. php -l sạch.
- [x] FE elearning (`elearning/`): stores/learningPathDetail.js `mapCourses` map `available`/`unavailableLabel` (default true); PathOutline.vue badge "Không còn khả dụng" cho khóa con; PathLessonRow.vue nút "Vào học" disabled + nhãn khi `course.available===false`.

### Verify Phase 3 (tinker 2026-07-21, learner 5, LP1 public+active, khóa con 42 flip private tạm rồi khôi phục)
- [x] Học viên ngoài: khóa con private của lộ trình PUBLIC đã ghi danh → getSessionData 423 scope='private' (phủ /learn + heartbeat + scorm vì cùng chốt). ([1] PASS)
- [x] Học viên ngoài vẫn học khóa PUBLIC khác cùng lộ trình (sub 44). ([2] OK-session)
- [x] Nhân viên nội bộ: không dính scope=private ([3] 403 chưa-ghi-danh, không phải private).
- [x] Góc học tập: thẻ LP1 khóa con 42 locked+"Không còn khả dụng"; khóa con 44 public vẫn "Đang học". ([4]/[4b] PASS)
- [ ] (user) verify browser: FE trang chi tiết lộ trình khóa con private hiện "Không còn khả dụng", nút "Vào học" disabled.
- Ghi chú: KHÔNG chặn ghi danh lộ trình (giữ nguyên); DB net không đổi (is_public 42 khôi phục=1).

### Checkpoint — 2026-07-21
Vừa hoàn thành: Phase 3 full — BE bỏ ngoại lệ `viaAccessiblePath` (2 file Elearning) + cờ `available` ở transformer dùng chung LearningPathLearnerResource + FE elearning (store + 2 component) khóa thẻ khóa con private. Verify tinker 5/5 PASS, DB khôi phục. php -l sạch 3 file BE.
Đang làm dở: không
Bước tiếp theo: user verify browser (FE elearning chưa build-verify, chỉ sửa additive). KHÔNG git/migration.
Blocked:

## Task — Phase 4: Tiến trình lộ trình + Guard đổi visibility (user yêu cầu 2026-07-21)
Spec: docs/superpowers/specs/2026-07-21-elearning-private-progress-guard-design.md | Plan chi tiết: docs/superpowers/plans/2026-07-21-elearning-private-progress-guard.md

Vấn đề: (1) khóa con private/khóa giữa chừng khiến lộ trình kẹt < 100% (tiến trình tính cả khóa không học được); (2) đổi visibility quá dễ, không cảnh báo tác động.

Quyết định user: (A) loại khóa con không khả dụng khỏi tử+mẫu số % lộ trình (động); (B) cảnh báo xác nhận (không chặn cứng) khi khóa public→private, KHÓA khóa, lộ trình public→private; không notification; 1 modal FE chung.

### Phần A — Tính tiến trình (BE) — DONE 2026-07-21 (tinker PASS, DB khôi phục)
- [x] A1 `MyLearningService::getInProgress` ($paths): % + courses/coursesDone chỉ trên khóa con khả dụng (bỏ children `locked`). Verify: courses 2→1, progress 88→100 khi khóa 42 private.
- [x] A2 `LearningSessionService::syncLearningPathCompletion`: doneCount/tổng chỉ trên khóa con khả dụng (KHOA loại mọi người; private loại học viên ngoài); 0 khả dụng → không auto-done.
- [x] A3 `LearningPathLearnerResource` (DÙNG CHUNG): progress avg + checkPathDone trên tập `available!==false`. Mở rộng cờ `available` (review Important): KHOA → available=false + "Đã khóa" cho MỌI người (nhất quán §3); private → false + "Không còn khả dụng" cho học viên ngoài. Employee giữ nguyên với khóa public.

### Phần B — Guard cảnh báo (BE + FE hrm-client)
- [x] B0 `Modules/Training/Helpers/VisibilityImpactHelper.php` (4 method). Count lọc theo trạng thái "đang học" (enrolled/learning), không đếm DONE (review Minor). Verify: sub42 impact→LP1 learner_count=2 external=5; LP1 hasExternal=true.
- [x] B1 `SubjectController::updateBuilder`: is_public 1→0 + thuộc lộ trình công khai + chưa confirm → 409 action='subject_private'. LƯU Ý (review Important): guard KHÔNG đặt ở `update()` classic vì endpoint đó không lưu is_public (dead code) — đã gỡ.
- [x] B2 `SubjectController::lock` (đổi signature nhận Request): khóa thuộc lộ trình công khai + chưa confirm → 409 action='subject_lock'. Route lock là GET → FE resubmit confirm qua QUERY STRING.
- [x] B3 `LearningPathController::update`: is_public 1→0 + có học viên ngoài đang học + chưa confirm → 409 action='path_private'.
- [ ] B4 FE hrm-client: `VisibilityImpactModal.vue` chung (đọc skill modal-popup + button-convention) + tích hợp SubjectBuilderForm / subjects index (nút Khóa, gửi confirm qua query) / learning-path form → bắt 409 → gửi lại `confirm=1`.

### Verify Phase 4 (subagent-driven, 2026-07-21)
- [x] Tinker A1: LP1 courses 2→1, progress 88→100 khi khóa 42 private (children vẫn hiện đủ).
- [x] Tinker A3: sub42 available=false; private→"Không còn khả dụng" (learner), KHOA→"Đã khóa" (mọi người kể cả employee); progress avg loại khóa 42.
- [x] Tinker A2 (read-only mô phỏng): learner availableIds=[44] (loại 42 private) → lộ trình không kẹt; employee availableIds=[42,44] (không loại private).
- [x] Tinker B0: subjectImpact(42)→LP1 learner_count=2, external=5; pathImpact(LP1) external=2 (đã lọc trạng thái đang học).
- [ ] Browser hrm-client (user verify): B1 sửa khóa→private / B2 nút Khóa / B3 lộ trình→private → hiện modal xác nhận, Đồng ý lưu OK; không tác động → không hỏi.
- [ ] Browser elearning (user verify): lộ trình có khóa con private/KHÓA → % + hoàn thành đúng (không kẹt), thẻ khóa con hiện "Không còn khả dụng"/"Đã khóa".
- [x] DB khôi phục nguyên trạng (mọi tinker try/finally, is_public 42=1).

Reviewer (subagent) mỗi phần: Part A ✅ (fix Important: A3 loại cả KHOA cho nhất quán §3); Part B BE ✅ (fix Important: gỡ dead guard ở update() classic; Minor: count lọc trạng thái đang học); Part B4 FE ✅ (chỉ Minor màu nút). php -l sạch toàn bộ BE.

### Checkpoint — 2026-07-21 (Phase 4)
Vừa hoàn thành: Phase 4 code + verify tinker toàn bộ (subagent-driven: 3 cụm implement + review + fix). Phần A (3 file BE tính tiến trình loại khóa không khả dụng) + Phần B (helper VisibilityImpactHelper + guard 409 ở SubjectController updateBuilder/lock + LearningPathController update + FE hrm-client VisibilityImpactModal tích hợp 3 điểm). DB khôi phục. KHÔNG git/migration.
Đang làm dở: không
Bước tiếp theo: user verify browser (hrm-client 3 case guard + elearning tiến trình lộ trình). FE hrm-client Docker/dev tự build.
Blocked:

## Ghi chú
- (Đã xử lý ở Phase 2) Lộ trình private cho người đã enroll.
- (Phase 3, 2026-07-21) ĐẢO Quyết định #3: khóa private không còn "truy cập hợp lệ qua lộ trình public".
- (Phase 4, 2026-07-21) Tiến trình loại khóa không khả dụng + guard cảnh báo đổi visibility (chưa code, đã có spec+plan).
- (Phase 3, 2026-07-21) ĐẢO Quyết định #3: khóa private không còn được "truy cập hợp lệ qua lộ trình public" — private = chỉ nội bộ tuyệt đối với học viên ngoài.
