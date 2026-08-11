# Plan — training-inuse-status

> Owner: @junfoke · Spec: `docs/superpowers/specs/2026-07-20-training-inuse-status-design.md`

## Phase 1 — BE Training (`Modules/Training`) ✅

### 1.1 Nhãn status lộ trình
- [x] `Entities/LearningPath.php`: `STATUSES` mã 2 "Đang dùng" → "Hoạt động" + map `getStatusTextAttribute`

### 1.2 Hợp nhất "in-use"
- [x] Verify FK `enrollment_lesson_progress` = `subject_lesson_id` (join qua subject_lessons)
- [x] `Entities/Lesson.php`: `isInUse()` (subject published + progress); `canDelete()` dùng `isInUse()`; accessor `getIsCanDeleteAttribute()`
- [x] `Entities/Subject.php`: `isInUse()` (5 downstream + learning_path_subjects published + subject_enrollments); refactor accessor + `canDelete()` dùng chung; "Nháp luôn xóa được"
- [x] `Entities/LearningPath.php`: `isInUse()` (learning_path_enrollments) + accessor

### 1.3 Chặn xóa + nới/gỡ ràng buộc
- [x] `LessonController::delete`: 400 "Bài học đang được sử dụng, không thể xóa"
- [x] `SubjectController::deleteBuilder`: 400 "Khoá học đang được sử dụng, không thể xóa" (guard Nháp)
- [x] `LearningPathController::delete`: thay guard "chỉ Nháp" bằng `isInUse()` → 400 "Lộ trình đang có học viên"
- [x] `LearningPathController::toggleLock`: gỡ chặn ACTIVE; mở khóa LOCKED → HOAT_DONG

### 1.4 Transformer
- [x] `LessonListResource`: thêm `is_can_delete`
- [x] `LearningPathListResource`: đổi sang `$item->is_can_delete`
- [x] `SubjectListResource`: thêm `is_can_delete` (canDelete đã có)

### 1.5 Verify BE ✅
- [x] `php -l` sạch toàn bộ (9 file)
- [x] Test API (Playwright): xóa lesson in-use → 400; khóa LP Hoạt động → 200, mở khóa → Hoạt động; is_can_delete phân biệt đúng (subject 6 xóa được / 35 chặn; path đều chặn vì có enrollment). Đã khôi phục nguyên trạng, không để rác.

## Phase 2 — FE hrm-client ✅
- [x] Sửa hardcode "Đang dùng" → "Hoạt động" (`learning-path/index.vue` + `components/TabInfo.vue`)
- [x] `lessons/index.vue`: nút Xóa `:disabled="!item.is_can_delete"` + tooltip "Đang được sử dụng, không thể xoá"
- [x] `subjects/index.vue`: nút Xóa đã `v-if="item.canDelete"` (theo isInUse); cải thiện toast lỗi hiện message BE
- [x] `learning-path/index.vue`: nút Xóa đã theo `is_can_delete` (giờ enrollment-based); toast BE OK
- [x] Verify UI: LP list hiện "Hoạt động" (dropdown + bảng); lessons list 7 nút Xóa disabled / 3 enabled đúng is_can_delete

## Phase 3 — Elearning (badge "Bị khóa") ✅ (code + compile)
- [x] `MyLearningService`: thêm `locked` + `learnStatusLabel` "Đã khóa" cho block `$paths`
- [x] `StudyCard.vue`: mở rộng `locked` computed bỏ điều kiện `!isPath.value` → badge + khóa nút "Tiếp tục" áp cả lộ trình (badge markup đã có sẵn)
- [x] Verify elearning compile sạch (0 lỗi console)
- [x] Verify badge trực tiếp (LIVE): NV đã enroll path 1 → khóa path → badge "Đã khóa" hiện trên thẻ lộ trình ("Tôi đang học") + nút Tiếp tục disabled; mở khóa khôi phục

## Phase 4 — Chặn HỌC khi lộ trình bị khóa (đồng bộ với khóa học) ✅
> User chốt: khóa lộ trình = chặn hẳn học khóa con (không chỉ hiển thị badge).
- [x] `LearningSessionService::startSession`: thêm guard 423 "Lộ trình đã bị khóa" — chặn khi subject thuộc lộ trình đã ghi danh đang KHÓA và KHÔNG thuộc lộ trình Hoạt động nào khác (tránh chặn nhầm khóa dùng chung)
- [x] `StudyCard.vue`: disable nút "Học" của khóa con (hiện "Đã khóa") khi lộ trình locked
- [x] Verify LIVE: baseline học khóa con 42 = 200; khóa path 1 → học khóa con 42 & 44 = **423 "Lộ trình đã bị khóa"**; control khóa 50 (ngoài path khóa) = 200 (không chặn nhầm); mở khóa khôi phục. php -l sạch, elearning compile OK.

## Phase 5 — UX nút danh sách + dropdown trạng thái ✅
> User feedback: nút Xóa phải hiện+disable (không ẩn); Nháp không cần nút Khóa; lộ trình đang dùng vẫn khóa được; dropdown lưu chính chỉ Hoạt động/Khóa (bỏ Nháp).
- [x] `learning-path/index.vue`: nút Khóa ẩn với Nháp (status 1), BẬT với Hoạt động (bỏ `:disabled=status===2` cũ); nút Xóa luôn hiện + `:disabled` khi !is_can_delete + tooltip
- [x] `subjects/index.vue`: nút Xóa `v-if=canDelete` → luôn hiện + `:disabled=!canDelete` + tooltip; nút Khóa chỉ hiện Hoạt động (`v-else-if status==1`), ẩn Nháp
- [x] Dropdown trạng thái bỏ "Nháp": subjects tabs/TabInfo (bỏ id3) + learning-path TabInfo (bỏ id1); LP `_id/edit.vue` coerce status lưu chính về {2,3}; Subject builder đã có coerce + "Lưu nháp" riêng; Lesson vốn chỉ 2 option
- [x] Verify LIVE: LP list Xóa disabled(đang dùng)/enabled + Khóa bật; set 1 path Nháp → nút Khóa ẩn (6→5); LP+Subject edit dropdown chỉ Hoạt động/Khoá; Subject list Xóa hiện+disable. Data test khôi phục.

## Checkpoint
### Checkpoint — 2026-07-20
Vừa hoàn thành: CODE DONE cả 3 phase + VERIFIED Phase 1 (API) & Phase 2 (UI). Phase 3 code + compile OK.
Đang làm dở: (không) — chờ user verify mắt + quyết định có setup enrollment lộ trình khóa để test badge live.
Bước tiếp theo: User verify UI hrm-client (hard-refresh) + elearning; nếu muốn test badge → setup enrollment + khóa lộ trình.
Blocked:

### Cập nhật sau (2026-07-29) — nới rule chặn học khóa con lộ trình khóa
Rule Phase 4 spec dòng 95-96 ("khóa lộ trình phải chặn thật việc học khóa con") chặn nhầm khóa public/Hoạt động HỌC LẺ được: học viên vào `/subjects/{slug}/learn` báo 423 "Lộ trình đã bị khóa" chỉ vì có ghi danh 1 lộ trình đã khóa chứa khóa đó. Theo yêu cầu user, đã NỚI: lộ trình khóa không còn chặn học lẻ khóa con còn khả dụng, và không promote trạng thái lộ trình khóa khi học lẻ. Chi tiết + code: `.plans/elearning-private-course-access/plan.md` Phase 6.
