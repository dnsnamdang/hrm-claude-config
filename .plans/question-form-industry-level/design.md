# Design — Đổi cấp gán Câu hỏi / Phiếu thu thập từ Ứng dụng sang Nhóm giải pháp

**Owner:** @manhcuong
**Ngày:** 2026-04-18
**Spec chi tiết:** [docs/superpowers/specs/2026-04-18-question-form-industry-level-design.md](../../docs/superpowers/specs/2026-04-18-question-form-industry-level-design.md)

## Mục tiêu

Câu hỏi (`survey_questions`) và Mẫu phiếu (`form_templates`) không còn gán cấp Ứng dụng. Mỗi Nhóm giải pháp có tối đa 1 Mẫu phiếu Published. Dự án TKT / Meeting match Mẫu phiếu theo Nhóm giải pháp.

## Scope

- BE `Modules/Assign`: SurveyQuestion, FormTemplate, ProspectiveProject, Meeting
- FE: `pages/assign/questions`, `pages/assign/form-templates`, `pages/assign/prospective-projects`, `pages/assign/meeting`

## Các quyết định chốt từ brainstorming

1. **Migration tự động** suy industry từ application cũ
2. **UI Câu hỏi** giữ dropdown "Phạm vi áp dụng" = `Tất cả` / `Theo nhóm giải pháp` (bỏ bước chọn Ứng dụng)
3. **UI Mẫu phiếu** bắt buộc Nhóm ngành + Nhóm giải pháp (bỏ Ứng dụng)
4. **1 Nhóm giải pháp — 1 Mẫu phiếu Published**: tạo mới mà đã có Published → chặn cứng
5. **Migrate data cũ**: cái mới nhất giữ Published, các cái cũ hơn → Locked
6. **Snapshots**: giữ nguyên, cột `application_id` thành dead data
7. **Câu hỏi thoải mái** không ràng buộc 1-1 với industry
8. **Edit Mẫu phiếu đã Published** được phép đổi industry (snapshot khoá lịch sử rồi)
9. **Dự án TKT / Meeting**: đổi industry → reset form_template; đổi application cùng industry → giữ form_template
10. **FormBuilder** filter câu hỏi theo industry của form + câu hỏi `application_scope = Tất cả`
11. **Cleanup tranh thủ**: DROP cả 3 pivot `survey_question_scopes/industries/applications` (UI chỉ chọn 1 → pivot redundant)

## Downstream impact

- Báo cáo `Modules/Assign/Services/Report/*` nếu join tới `form_templates.application_id` → update
- FE store `optionsSelect` fetch form templates theo app → đổi thành theo industry
- Endpoint `GET /assign/form-templates/by-application/{appId}` → thay bằng `GET /assign/form-templates/by-industry/{industryId}`

## Rollout

1. PR1 (BE data): migration backfill + dedupe (không gãy UI cũ)
2. PR2 (BE + FE code): drop cột/pivot + update toàn bộ; deploy cùng release
