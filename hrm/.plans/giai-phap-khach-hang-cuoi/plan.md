# Plan — Giải pháp: Nhóm ngành/Nhóm giải pháp/Ứng dụng + Khách hàng cuối

Feature: `giai-phap-khach-hang-cuoi` · @manhcuong · 2026-06-26
Màn: Quản lý GP (form tạo/sửa/chi tiết InfoTab + manager ProjectInfoTab + danh sách solutions/index)

Quyết định: Nhóm ngành/Nhóm giải pháp = options theo Ứng dụng (kế thừa từ dự án), cho chọn 1, KHÔNG default theo dự án; Ứng dụng readonly kế thừa. KH cuối + Loại hình + Lĩnh vực readonly kế thừa từ dự án (KHÔNG thêm cột solutions). Filter danh sách qua whereHas('prospectiveProject').

## BE
- [ ] SolutionService::buildPayload — scope_id/industry_id nhận từ request (user chọn); application_id + customer_scope_id kế thừa từ dự án
- [ ] SolutionService::index — thêm filter customer_scope_group_id + customer_benefit_id (whereHas prospectiveProject); giữ customer_scope_id
- [ ] SolutionService::show — eager-load thêm: solution scope/industry/application/customerScope + project customerScopeGroup/customerBenefitScope/customerBenefitScopeGroup/scope/application
- [ ] DetailSolutionResource — thêm scope_id/scope_name + application_id/application_name + industry từ solution; customer_scope_id/name (Lĩnh vực) + customer_scope_group_name (Loại hình); is_intermediary_customer + customer_benefit_* (id/code/name/tax/phone/email/address/contact_*) + customer_benefit_scope_group_name/scope_name
- [ ] SolutionRequest — scope_id + industry_id required (Nhóm ngành*/Nhóm giải pháp*)
- [ ] SolutionResource (list) — đảm bảo customer_benefit_code/name + customer_scope_group_name + customer_scope (đã có); thêm customer_benefit_scope_group_name nếu thiếu

## FE
- [ ] SolutionForm: fetch options scopes/industries/applications; populateSolutionFromProject kế thừa application_id/name + benefit + is_intermediary + loại hình/lĩnh vực names; loadSolution map scope/industry; pass options + field xuống InfoTab
- [ ] InfoTab "Thông tin GP": thêm Nhóm ngành (select options theo app) + Nhóm giải pháp (select) + Ứng dụng (readonly) + icon (i) tooltip
- [ ] InfoTab "Thông tin dự án": thêm "Khách hàng cuối" dưới Khách hàng (khi is_intermediary + benefit ≠ direct)
- [ ] manager.vue: projectData thêm customer_benefit_* + is_intermediary + loại hình/lĩnh vực
- [ ] ProjectInfoTab: thêm "Khách hàng cuối" vào THÔNG TIN KHÁCH HÀNG (khi có)
- [ ] solutions/index.vue: cột "Khách hàng cuối" (customer_benefit_code/name) + "Loại hình hoạt động" (customer_scope_group_name) + cell; filter Khách hàng cuối + Loại hình + Lĩnh vực

## Verify
- [x] API store nhận scope_id/industry_id; detail trả benefit; list filter; Playwright form + danh sách

### Checkpoint — 2026-06-26
Vừa hoàn thành: TẤT CẢ (BE + FE). BE: buildPayload nhận scope/industry, application/customer_scope kế thừa; index filter customer_scope_group_id + customer_benefit_id (whereHas); show eager-load mở rộng; DetailSolutionResource trả scope/industry/application + Lĩnh vực/Loại hình + KH cuối; SolutionRequest required scope_id/industry_id + attributes. FE: InfoTab thêm 3 trường (Nhóm ngành/Nhóm giải pháp select theo app + Ứng dụng readonly + tooltip) + Khách hàng cuối row; SolutionForm init+populate kế thừa application/benefit; manager.vue projectData + ProjectInfoTab KH cuối; solutions/index thêm 2 cột (Khách hàng cuối + Loại hình) + 3 filter (Loại hình/Lĩnh vực/Khách hàng cuối).
Verify: BE filter 200, validation 422 (scope_id+industry_id), detail trả đủ field; Playwright 7/7 (form 3 trường + Ứng dụng readonly kế thừa "Áp dụng công việc tại Tân Phát" + list 3 filter). Screenshot xác nhận layout.
Bước tiếp theo: chờ user kiểm tra trực quan + test luồng tạo GP có KH cuối (dự án trung gian).
Blocked: 
