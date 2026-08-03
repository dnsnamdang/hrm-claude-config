# Design — Chuyển câu hỏi & mẫu phiếu sang liên kết theo Ứng dụng

**Owner:** @manhcuong
**Ngày:** 2026-06-26
**Spec chi tiết:** [docs/superpowers/specs/2026-06-26-survey-question-form-by-application-design.md](../../docs/superpowers/specs/2026-06-26-survey-question-form-by-application-design.md)

## Mục tiêu

Đổi trục liên kết của **Ngân hàng câu hỏi khảo sát** và **Mẫu phiếu / Phiếu thu thập thông tin** từ cặp `scope_id` (Nhóm ngành) + `industry_id` (Nhóm giải pháp) sang `application_id` (Ứng dụng). Bỏ (drop) Nhóm ngành/Nhóm giải pháp ở cả 2 màn. Thêm logic chặn trùng câu hỏi theo 4 yếu tố.

## Scope

- BE `Modules/Assign`: SurveyQuestion, FormTemplate, ProspectiveProject, Meeting (downstream)
- FE: `pages/assign/questions`, `pages/assign/form-templates`, `components/modals/AddSurveyQuestionModal`, TKT/Meeting print

## Các quyết định chốt từ brainstorming

1. **FormBuilder + Mẫu phiếu cũng chuyển sang Ứng dụng** (không để lệch trục).
2. **Backfill data cũ**: industry → chọn `application_id` lớn nhất (mới nhất) qua pivot `application_industries`.
3. **Drop cột** `scope_id`, `industry_id` ở `survey_questions` và `form_templates` (re-add `application_id`).
4. **Mẫu phiếu**: ràng buộc 1 Ứng dụng = 1 mẫu phiếu (unique application_id, áp dụng cho bản Published).
5. **Chặn trùng câu hỏi 4 yếu tố**: [title + data_type + đáp án (chuẩn hóa, không phân biệt thứ tự/hoa-thường) + phạm vi]. Phạm vi=Tất cả → quét nhóm Tất cả; Phạm vi=Theo ứng dụng → quét cùng application_id. Bỏ rule unique title toàn cục.
6. **Export**: theo đúng cột người dùng cung cấp (xem spec). **Import: tạm chưa làm.**

## Phase

- **Phase 1** — DB migration & backfill (questions + form_templates)
- **Phase 2** — Ngân hàng câu hỏi khảo sát (BE + FE)
- **Phase 3** — Mẫu phiếu / Phiếu thu thập (BE + FE + clone + export + print)
- **Phase 4** — Downstream: FormBuilder thư viện câu hỏi theo application + TKT/Meeting match/in phiếu theo application

## Downstream impact

- `ProspectiveProjectService::findFormTemplate` / `handleFormTemplateSnapshot`: match theo `application_id`
- `MeetingService` snapshot: dùng `application_id`
- `FormBuilder.vue` / `QuestionLibrary` / `AddQuestionQuickModal`: lọc câu hỏi theo application
- Export blade `form_templates.blade.php` đang đọc `application_name` (hiện rỗng) → resource bổ sung

## Lưu ý kế thừa

- `form_template_snapshots` đã có sẵn `application_id`.
- `prospective_projects` đã dùng `application_id` làm trục chính (đã có `applyDerivedScopeIndustry`).
- Tham khảo backfill: migration `2026_04_18_100001` (industry MIN/GROUP BY) + seeder `BackfillCustomerScopeFieldsSeeder`.
