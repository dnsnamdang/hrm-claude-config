# Elearning — Fix 3 bug luồng học lộ trình (tóm tắt)

> Owner: @junfoke · 2026-07-22 · Spec đầy đủ: `docs/superpowers/specs/2026-07-22-elearning-learning-flow-fixes-design.md`

## Mục tiêu
Sửa 3 bug user báo về luồng lộ trình → khóa học ở portal elearning (học viên ngoài). Không đổi business
rule; chỉ sửa lỗi điều hướng/đếm.

## 3 bug & root cause
1. **Bug 1** — Lộ trình có khóa A (admin KHÓA) + B (hoạt động): "Tiếp tục học" kẹt ở A, không tới B.
2. **Bug 3** — Lộ trình công khai, A public (đã xong) + B private: nút "Xem lại nội dung" trỏ vào B
   "Không còn khả dụng" (423). → **Cùng root với Bug 1**.
   - Root chung: FE `handleStartLearn`/`nextCourse` chọn khóa đích chỉ lọc `!locked && slug`, THIẾU
     `available` → trỏ vào khóa không khả dụng (admin KHÓA hoặc private với học viên ngoài).
3. **Bug 2** — Góc học tập đếm "x bài học" gồm cả bài admin-KHÓA, trong khi tiến độ loại bài KHÓA → "Bài x/y" lệch.

## Quyết định lớn
- **KHÔNG đổi rule private**: học viên ngoài vẫn bị chặn học khóa private (đúng Phase 3 của
  `elearning-private-course-access`). Chỉ sửa để nút không trỏ vào khóa không khả dụng.
- Bug 1 sửa **cả FE + BE**: FE loại khóa `available=false` khi chọn đích; BE lộ trình tuần tự không để
  khóa không-khả-dụng chặn vĩnh viễn khóa sau.
- Bug 2 phạm vi = **góc học tập** (MyLearningService), loại bài `STATUS_LOCKED` khỏi đếm cho khớp tiến độ.
- **Đã loại bỏ** hướng auto-enroll (chẩn sai ban đầu — tưởng 403 thiếu enrollment, thực ra 423 private).

## Files
- BE: `Modules/Elearning/Services/MyLearningService.php`,
  `Modules/Training/Transformers/LearningPathResource/LearningPathLearnerResource.php`
- FE: `src/composables/useContentDetail.js`, `src/views/subject/SubjectLearnView.vue`,
  `src/views/ContentDetailView.vue`

## Trạng thái
CODE DONE (2026-07-22). php -l sạch, tinker verify bug 2 PASS. Chờ user deploy FE remote + verify browser.
Không git/migration. Phát hiện phụ (chưa fix): 23 enrollment gap trên DB dev — vấn đề độc lập.
