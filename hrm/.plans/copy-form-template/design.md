# Sao chép mẫu phiếu thu thập thông tin — Design (tóm tắt)

- **Người phụ trách**: @khoipv
- **Module**: Assign — `Modules/Assign` (BE) / `pages/assign/form-templates` (FE)
- **Spec đầy đủ**: `docs/superpowers/specs/2026-06-05-copy-form-template-design.md`

## Mục tiêu
Thêm nút "Sao chép" ở list mẫu phiếu. Click → vào form Tạo mới đã prefill từ mẫu gốc; user chọn lại Nhóm giải pháp rồi Lưu.

## Quyết định chính
- **Hướng A**: BE endpoint `GET /assign/form-templates/{id}/copy-data` trả dữ liệu đã lọc; FE prefill `add.vue`; lưu qua `store` sẵn có.
- Prefill: **Tên** giữ nguyên, **Nhóm ngành** (`scope_id`) giữ nguyên, **Nhóm giải pháp** (`industry_id`) để trống (bắt buộc chọn lại), **Trạng thái** = Nháp.
- **Section**: sao chép 100%, giữ `position` (kể cả section rỗng sau lọc).
- **Câu hỏi**: `application_scope = 1` (Tất cả) → CLONE; `= 2` (Theo nhóm giải pháp) → BỎ QUA. (application_scope nằm trên `SurveyQuestion`, tra qua `survey_question_id`.)
- Phòng thủ: `survey_question_id` null → CLONE; cha/nhóm bị bỏ → con bỏ theo.

## Phân quyền
- Dùng chung quyền `Quản lý danh mục mẫu phiếu thu thập thông tin` (không thêm permission mới, không migration).
- Cho sao chép từ **mọi trạng thái** mẫu gốc.

## Ràng buộc
- Không sửa transformer dùng chung; không auto-save; không tạo record khi chưa bấm Lưu.

## Trạng thái
- Spec + design: xong. Plan: tạo qua writing-plans.
