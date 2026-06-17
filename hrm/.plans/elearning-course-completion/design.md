# elearning-course-completion — Tóm tắt thiết kế

> Owner: @junfoke · 2026-06-03 · Spec đầy đủ: `docs/superpowers/specs/2026-06-03-elearning-course-completion-design.md`

## Mục tiêu
Bổ sung "điểm kết thúc" khi hoàn thành 100% khoá học elearning: modal chúc mừng + chứng chỉ render trong web (in/lưu PDF qua trình duyệt).

## Quyết định lớn
1. Chốt nghiệp vụ hoàn thành (BE) **đã có sẵn** (`enrollment.status=done` + `completed_at`) — không làm lại.
2. Chứng chỉ render trong web (ảnh nền `certificate_template_url` + overlay text theo `subject_certificate_fields`), in qua `window.print()`. KHÔNG sinh PDF ở BE.
3. Chỉ khoá `certificate_enabled = 1` mới cấp chứng chỉ.
4. Vừa đạt 100% → modal chúc mừng (component màn học).
5. Chứng chỉ là trang riêng route `/certificate/:slug`; truy cập từ modal + màn chi tiết + màn học (My Learning để sau).
6. Đổi nhãn nút "Chứng nhận" → "Chứng chỉ"; khoá không có chứng chỉ → nút màn chi tiết thành "Xem lại nội dung".

## Phạm vi
- **BE:** endpoint mới `GET /subjects/{slug}/certificate` (resolve field động) + thêm `certificate_enabled` vào API `/learn`.
- **FE:** `courseCompletionSignal` trong store học, `CourseCompleteModal`, trang `CertificateView` + `CertificateCanvas`, store chứng chỉ, nối/đổi tên các nút.

## Ngoài phạm vi
Nút chứng chỉ ở My Learning · sinh PDF/email BE · QR verify · chứng chỉ cho LearningPath.

## Tài liệu liên quan
- Spec đầy đủ: `docs/superpowers/specs/2026-06-03-elearning-course-completion-design.md`
- Tiếp nối: `learning-session-api`, `scorm-lms-runtime`, `elearning-tracking-fix`
