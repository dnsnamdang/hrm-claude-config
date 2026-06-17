# elearning-course-completion — Plan

> Owner: @junfoke · Plan chi tiết: `docs/superpowers/plans/2026-06-03-elearning-course-completion.md` · Spec: `docs/superpowers/specs/2026-06-03-elearning-course-completion-design.md`

## Phase 1 — Backend
- [x] Task 1: `CertificateService` — resolve dữ liệu chứng chỉ (check done + enabled + template, resolve field động)
- [x] Task 2: `CertificateController` + route `GET /subjects/{slug}/certificate` (elearning.auth)
- [x] Task 3: Thêm `certificate_enabled` vào `LearningSessionResource` (API /learn)

## Phase 2 — FE trang chứng chỉ
- [x] Task 4: Store `certificate.js` (fetchCertificate)
- [x] Task 5: `CertificateCanvas.vue` — ảnh nền + overlay text theo x/y/font
- [x] Task 6: `CertificateView.vue` + route `/certificate/:slug` + print CSS

## Phase 3 — FE modal hoàn thành
- [x] Task 7: `courseCompletionSignal` trong store học (bắt chuyển tiếp → done)
- [x] Task 8: `CourseCompleteModal.vue` (có/không chứng chỉ)
- [x] Task 9: Tích hợp modal vào `SubjectLearnView` (watch signal)

## Phase 4 — FE nối/đổi tên nút
- [x] Task 10: Map `certificateEnabled` vào store `subjectDetail`
- [x] Task 11: `DetailEnrollCard` — đổi "Chứng nhận"→"Chứng chỉ" + điều kiện enabled + nút "Xem lại nội dung"
- [x] Task 12: `ContentDetailView` — nối nút chứng chỉ sang router
- [x] Task 13: Nút "Chứng chỉ" trong sidebar màn học

## Checkpoint — 2026-06-03
Vừa hoàn thành: CODE DONE toàn bộ 13/13 task (4 phase). BE 4 file (2 mới + 2 sửa), FE 9 file (5 mới + 4 sửa).
Đang làm dở: (không)
Bước tiếp theo: User chạy dev server trong Docker (Node ≥18) → verify browser: (1) học nốt khoá test đạt 100% → modal chúc mừng, (2) khoá có cert → nút "Xem chứng chỉ" → trang in được, (3) khoá không cert → "Khám phá khoá khác" + màn chi tiết "Xem lại nội dung", (4) vào thẳng /certificate khoá chưa xong → báo lỗi 403.
Blocked: (không — chỉ chờ verify browser vì máy local Node 14 không build/chạy Vite 5 được)

## Checkpoint — 2026-06-03 (sau verify browser)
Đã verify trên browser — PASS. Phát sinh 2 fix:
- FIX1 (vị trí lệch): CertificateCanvas đổi sang hệ toạ độ chuẩn 1600×900 + chữ canh center `translate(-50%,-50%)` + scale theo bề rộng khung (ResizeObserver), ảnh `object-fill` — khớp preview admin.
- FIX2 (tên người học rỗng): CertificateService — cột learner đúng là `fullname` (không phải `name`); `$learner->name` → `$learner->fullname`. Tên người học giờ tự gán đúng.
Trạng thái: vị trí + tên người học hiển thị đúng (user xác nhận). Còn lại: verify các kịch bản khoá không-cert + 403 (nếu chưa).

## Checkpoint — 2026-06-03 (UX học lại)
Phát sinh 2 fix UX cho khoá đã hoàn thành:
- FIX3: nút "Mở" từng bài ở "Nội dung môn học" (ContentDetailView.handleOpenLesson, nhánh subject) trước chỉ toast → nay router.push `subject-learn` với `lessonId: lesson.lessonId` (vào thẳng bài). Guard: chưa đăng nhập / chưa ghi danh → toast nhắc.
- FIX4: khoá done + có cert (DetailEnrollCard) trước chỉ có nút "Chứng chỉ" → nay hiện CẢ "Chứng chỉ" (chính) + "Xem lại nội dung" (phụ, emit continue), để học lại được như khoá không-cert.
Bước tiếp: user verify browser nút "Mở" bài + 2 nút ở khoá done+cert.

## Ghi chú
- KHÔNG commit git (theo quy ước dự án).
- Verify trên browser sau khi user chạy dev server (Docker, Node ≥18).
- Phương án chứng chỉ: endpoint riêng (A), in/lưu PDF qua trình duyệt.
