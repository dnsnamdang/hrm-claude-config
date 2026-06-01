# Plan — Chặn tạo giải pháp / chọn dự án khi phiếu thu thập chưa đủ

Người phụ trách: @namdang

## Phase 1 — Gate theo phiếu thu thập thông tin

### BE
- [x] Tách `RequestSolutionService::isFormAnswersComplete(int): bool` từ `validateFormAnswers()` (dùng lại logic required questions)
- [x] `validateFormAnswers()` gọi `isFormAnswersComplete()`, throw 423 nếu false (giữ behavior cũ)
- [x] `ProspectiveProjectResource` (list) trả thêm `is_form_complete` (chỉ tính khi có `form_template_snapshot_id`)
- [x] `SolutionService::store()` chặn dự án Tự triển khai: status=2 + has_solution + phiếu đủ trường, nếu không → `ValidationException`
- [x] `SolutionController::store()` rethrow `ValidationException` (trả 422 inline thay vì 400)

### FE
- [x] `prospective-projects/index.vue`: thêm điều kiện `is_form_complete !== false` để ẩn nút "Tạo giải pháp"
- [x] `request-solution/components/RequestTab.vue`: filter dropdown loại dự án `is_form_complete === false` (giữ dự án đang chọn)

### Test (thủ công)
- [ ] Dự án tự triển khai, phiếu thiếu trường bắt buộc → KHÔNG hiện nút "Tạo giải pháp"
- [ ] Gọi thẳng API tạo solution cho dự án trên → bị chặn 422
- [ ] Phiếu điền đủ → nút hiện lại + tạo được giải pháp
- [ ] Màn tạo YC làm GP: dự án phiếu chưa đủ không xuất hiện trong dropdown

### Checkpoint — 2026-05-29
Vừa hoàn thành: toàn bộ BE + FE Phase 1.
Bước tiếp theo: User test thủ công 4 case + reload BE.
Blocked: không
