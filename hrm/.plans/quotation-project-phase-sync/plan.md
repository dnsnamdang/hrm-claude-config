# Plan — #11016 phản hồi QA

## Phase 1 — BE (hrm-api, nhánh tpe)
- [x] `QuotationService::create()`: bỏ `syncProjectPhase` (báo giá mới luôn nháp)
- [x] `QuotationService::update()`: bỏ `syncProjectPhase` + ghi rõ lý do (hàm chỉ chạy khi nháp)
- [x] `QuotationService::submit()`: thêm `syncProjectPhase` trước nhánh cấp 1
- [x] `RequestSolutionService::create()/update()`: chỉ sync khi `status !== STATUS_TAO_NHAP`

## Phase 2 — Kiểm chứng
- [x] Lưu nháp báo giá đổi giai đoạn → dự án GIỮ NGUYÊN (báo giá 120: phase 8→9, dự án 198 vẫn 8)
- [x] Gửi duyệt báo giá → dự án đồng bộ (dự án 198: 8→9), rollback sạch
- [x] Yêu cầu giải pháp: nháp → bỏ qua sync; chuyển "Chờ tiếp nhận" → sync
- [x] #5 dropdown giai đoạn khoá: thử 2 kịch bản, không tái hiện
- [x] Dọn dữ liệu test: project_phases, quotations, prospective_projects, request_solutions về nguyên trạng

## Phase 3 — AC1: bắt buộc Giai đoạn dự án (user chốt: giữ hiện tại, lưu nháp KHÔNG chặn)
- [x] Rà FE: `quotations/_id/edit.vue` — `validateForm()` chỉ chạy khi `strict` (Gửi duyệt) → lưu nháp vốn đã không chặn, KHÔNG phải sửa
- [x] Rà FE: `quotations/create.vue` chỉ `extends` edit.vue → cùng hành vi
- [x] Rà FE: Yêu cầu giải pháp (`RequestTab.vue`) chỉ hiển thị `formError` từ BE, không validate cứng
- [x] Rà BE: `RequestSolutionRequest` đã `required` khi status=2, `nullable` khi nháp; `QuotationUpdateRequest` nullable
- [x] Test UI thật (báo giá 202): xoá Giai đoạn → **Lưu nháp thành công** (phase=NULL), dự án 241 giữ nguyên phase=1
- [x] Test UI thật: **Gửi duyệt** khi để trống → chặn, lỗi inline "Vui lòng chọn giai đoạn dự án"
- [x] Dọn: trả `created_by` + `project_phase_id` của báo giá 202, `company_role` tài khoản test

### Checkpoint — 2026-09-16
Vừa hoàn thành: fix #6 (BE) + kiểm chứng #5 + xác minh AC1 theo hướng user chốt
Bước tiếp theo: chờ user duyệt commit; phản hồi QA về #5
Blocked:
