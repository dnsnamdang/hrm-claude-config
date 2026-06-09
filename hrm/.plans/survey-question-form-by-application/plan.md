# Plan — Chuyển câu hỏi & mẫu phiếu sang Ứng dụng

Owner: @manhcuong · Spec: docs/superpowers/specs/2026-06-26-survey-question-form-by-application-design.md

## Phase 1 — DB Migration & Backfill

### BE
- [x] Migration A: re-add `application_id` + backfill từ industry (MAX app) cho `survey_questions`
- [x] Migration B: drop `scope_id`, `industry_id` khỏi `survey_questions`
- [x] Migration C: re-add `application_id` + backfill + dedupe Published cho `form_templates`
- [x] Migration D: drop `scope_id`, `industry_id` khỏi `form_templates`

## Phase 2 — Ngân hàng câu hỏi khảo sát

### BE
- [x] SurveyQuestion: fillable + relation `application()`, đổi comment scope
- [x] SurveyQuestionRequest: bỏ unique title, rule application_id, check trùng 4 yếu tố
- [x] SurveyQuestionService: filter + payload theo application_id
- [x] Resource + Detail: application_id/application_name, bỏ scope/industry
- [x] Controller show/export: load application
- [x] Blade export câu hỏi: cột mới

### FE
- [x] QuestionForm.vue: 1 select Ứng dụng, fetchApplications, isByApplication
- [x] add/edit/_id index: state + map application_id
- [x] index.vue list: cột + filter Ứng dụng, export params
- [x] print.vue: cột Ứng dụng/Phạm vi

## Phase 3 — Mẫu phiếu / Phiếu thu thập

### BE
- [x] FormTemplate: fillable + relation application()
- [x] FormTemplateRequest: rule + unique 1 app = 1 Published
- [x] FormTemplateService: index/payload/clone theo application_id
- [x] Resource: application_id/application_name + question_count
- [x] Controller findByCriteria/unlock/getSnapshot theo application
- [x] Blade export mẫu phiếu: cột mới

### FE
- [x] FormMeta.vue: 1 select Ứng dụng
- [x] add/edit/_id index/copy-data: map application_id
- [x] index.vue list: cột + filter Ứng dụng
- [x] FormPreview + FormTemplatePrintSheet: applicationName

## Phase 4 — Downstream

### BE
- [x] SurveyQuestionService::index: gộp application_id + include_all_scope đúng nhóm
- [x] ProspectiveProjectService: findFormTemplate/handleFormTemplateSnapshot theo application_id
- [x] MeetingService: snapshot theo application_id

### FE
- [x] FormBuilder.loadLibrary: lọc câu hỏi theo applicationId + Tất cả
- [x] AddQuestionQuickModal/QuestionLibrary: props applicationId
- [x] Meeting survey-print/input + TKT formTabInput: applicationName

## Phase 5 — Mẫu in phiếu thu thập (theo file Excel mẫu)

### FE
- [x] util survey-print-rows.js (dựng rows + đánh số section/group/question/child + nhãn loại + options, dùng chung)
- [x] FormTemplatePrintSheet (bản TRỐNG): header Tên mẫu phiếu/Mã/Ứng dụng/Ngày in/Người in + bảng STT|NỘI DUNG|LOẠI CÂU HỎI|GIÁ TRỊ LỰA CHỌN ĐI KÈM
- [x] SurveyPrintSheet (bản CÓ TRẢ LỜI): header Tên KH/Tên dự án/Mã dự án/Ứng dụng/Ngày khảo sát/Người khảo sát + bảng thêm cột ĐÁP ÁN/GIÁ TRỊ THU THẬP
- [x] Parent form-templates _id/index + index: truyền header mới (formName/formCode/printUser)
- [x] Parent answer-column-title 4 chỗ → "ĐÁP ÁN / GIÁ TRỊ THU THẬP"
- [x] Bỏ tiêu đề phụ "THÔNG TIN KHẢO SÁT" ở cả 2 mẫu (theo yêu cầu)
- [x] Icon mẫu phiếu cạnh trường Ứng dụng (ProjectInfoSection): xanh+click mở chi tiết mẫu phiếu khi ứng dụng có mẫu Published (find-by-criteria?application_id=), xám khi chưa có

## Ngoài phạm vi
- Import mẫu phiếu (tạm chưa làm)
