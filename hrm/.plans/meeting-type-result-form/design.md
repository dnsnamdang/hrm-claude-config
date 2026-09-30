# Design — Loại meeting: gán phiếu tổng hợp kết quả (Redmine #11130)

> @junfoke — Nhánh `task_11130` (tách từ `tpe`), cả 2 repo.

## Phạm vi issue #11130 (3 mục)

| # | Nội dung | Trạng thái |
| --- | --- | --- |
| 1 | Danh mục Loại meeting: cấu hình "Gán phiếu tổng hợp kết quả meeting" + bộ câu hỏi | **Phải làm** |
| 2 | Biên bản meeting: tự hiện phiếu theo Loại meeting, render động, chặn Hoàn thành khi thiếu câu bắt buộc | **Phải làm** |
| 3 | Người chủ trì meeting (mặc định = người tạo, chọn được người khác, quyền lưu/chốt lịch) | ✅ **ĐÃ CÓ** trên `tpe` (cột `host_employee_id`, quyền sửa/xem đã mở cho chủ trì) |

Bộ câu hỏi khảo sát đầu tư (câu 1/2/3, bản cập nhật 22/08: Lĩnh vực » Nhóm ngành + mức đầu tư +
icon xoá từng dòng) **đã có sẵn** ở `MeetingInvestmentSurvey.vue` — không làm lại.

## Nền tảng tái sử dụng (đã có, không dựng mới)

- **Engine phiếu động**: `form_templates` → `form_sections` → `form_groups` → `form_questions`
  (+ `form_question_options`, bộ snapshot). Hỗ trợ sẵn: text, number, textarea, date, boolean
  (Có/Không), radio, checkbox, select, file, **câu cha-con** (`parent_question_id`), **rẽ nhánh**
  (`visibility`), **bắt buộc** (`required`).
- **Màn soạn mẫu phiếu**: `pages/assign/form-templates/` (thêm/sửa/xem).
- **Màn nhập render động**: `pages/assign/meeting/_id/survey-input.vue` — đã render đủ loại câu hỏi.
- **Lưu đáp án**: `FormAnswerService::saveFormAnswers($type, $typeId, $formTemplateId, $answers)`;
  bảng `form_answers` đã đa hình sẵn (`type` + `type_id`) → gắn cho meeting không phải đổi schema.

## Quyết định (user chốt 2026-09-11)

1. **Cấu hình = chọn MẪU PHIẾU CÓ SẴN**, không dựng trình soạn câu hỏi riêng trong Loại meeting.
   Form Loại meeting có công tắc "Gán phiếu tổng hợp kết quả meeting" + ô chọn mẫu phiếu (trạng thái
   Published). Tránh đẻ ra 2 nơi soạn câu hỏi khác nhau cho cùng một engine.
2. **Phiếu khảo sát đầu tư hard-code giữ nguyên, chạy song song.** Báo cáo CSKH tiềm năng đang đọc
   `meeting_investment_demands` / `meeting_investment_scopes` — không đụng vào, không có rủi ro vỡ
   báo cáo. Phiếu cấu hình là phần THÊM cho các loại meeting khác.

## Kiến trúc chọn

- `meeting_types` thêm 2 cột: `has_result_form` (bật/tắt) + `form_template_id` (mẫu phiếu gán).
- Biên bản meeting đọc Loại meeting → có phiếu thì render phân vùng "Phiếu tổng hợp kết quả meeting"
  ở **đầu**, ngay dưới thông tin biên bản.
- Đáp án lưu qua `FormAnswerService` với `type = 'meeting'`, `type_id = meeting.id`.
- Chặn Hoàn thành biên bản khi còn câu bắt buộc chưa trả lời — chốt chặn thật ở **BE**, FE chỉ là lớp
  trải nghiệm (hiện lỗi inline tại câu thiếu).
