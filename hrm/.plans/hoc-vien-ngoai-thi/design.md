# Học viên ngoài thi khóa exam-mode — Tóm tắt

- **Owner**: @junfoke · **Ngày**: 2026-07-23
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-23-hoc-vien-ngoai-thi-design.md`

## Mục tiêu
Cho **học viên ngoài** (`user_type='learner'`) làm bài **Thi** các khóa `evaluation_mode='exam'` **công khai** (`is_public=1`), thi **ngay trong app elearning** (UI native), tái dùng engine thi của module Training.

## Quyết định lớn
1. Thi native trong elearning — bỏ deep-link HRM cho learner (nhân viên giữ nguyên).
2. Tự chấm trắc nghiệm; tự luận đẩy nhân viên (examiner) chấm như cũ.
3. Phạm vi = khóa exam-mode + `is_public=1` (không thêm toggle).
4. Route tiếng Việt chuẩn `khoa-hoc`: `/khoa-hoc/:slug/thi` + `/khoa-hoc/:slug/thi/ket-qua/:resultId`.
5. Kết quả lưu chung `exam_test_results` — thêm cột `learner_id` (nullable, mirror enrollment).

## Điểm sửa cốt lõi (additive, backward-compatible)
- Nới 2 chặn: `SubjectDetailController::enroll:261` + `examStatus:145` (cho learner khi public).
- `ExamResultService::store:314` — gán `learner_id` khi taker là learner.
- `LearningSessionService::syncSubjectExamCompletion:583` — nhánh learner.
- Endpoint mới Elearning: `GET/POST subjects/{slug}/exam/todo|submit`.
- Màn chấm tự luận HRM hiển thị tên learner.
- FE: `SubjectExamView.vue` + `SubjectExamResultView.vue`.

## Ràng buộc
- KHÔNG đổi luồng thi nhân viên (regression an toàn).
- KHÔNG migrate/seed cho tới khi user ra lệnh rõ ràng.
- Sửa `exam_test_results` (bảng Training dùng chung) — user đã xác nhận.
