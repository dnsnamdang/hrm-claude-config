# Plan — Chặn dấu phẩy (,) và hai chấm (:) trong tên 5 danh mục KH

Người phụ trách: @manhcuong

## Phase 1 — Backend (validate thật, chặn ghi DB) ✅

### BE — FormRequest tạo/sửa (rule `name` array + not_regex + message)
- [x] CustomerScopeRequest (Lĩnh vực kinh doanh KH)
- [x] CustomerScopeGroupRequest (Loại hình hoạt động KH)
- [x] ScopeRequest (Nhóm ngành)
- [x] IndustriesRequest (Nhóm giải pháp)
- [x] ApplicationsRequest (Ứng dụng)

### BE — Service validateImportData (check ký tự trên cột name khi import)
- [x] CustomerScopeService
- [x] CustomerScopeGroupService
- [x] ScopeService
- [x] IndustriesService
- [x] ApplicationService (pattern one-liner khác 4 service kia)

## Phase 2 — Frontend (chỉ hiển thị lỗi) ✅

### FE — Modal tạo/sửa: KHÔNG cần sửa (đã có sẵn hiển thị lỗi name inline từ 422)
- [x] customer-scopes/AddScopeModal.vue — formError['name'] có sẵn
- [x] customer-scope-groups/AddGroupModal.vue — formError['name'] có sẵn
- [x] industry-groups/AddScopeModal.vue — formError['name'] có sẵn
- [x] components/modal/industry-modal.vue — error.name có sẵn
- [x] components/modal/application-modal.vue — error.name có sẵn

### FE — importValidationRules trong index.vue: check ký tự name cho preview import
- [x] customer-scopes/index.vue
- [x] customer-scope-groups/index.vue
- [x] industry-groups/index.vue
- [x] solution-groups/index.vue
- [x] application/index.vue

## Phase 3 — Verify ✅
- [x] php -l 10 file BE — sạch
- [x] Tinker: rule not_regex chặn , và : + message chuẩn; tên hợp lệ vẫn pass
- [x] Tinker: CustomerScopeGroupService::validateImportData chặn dòng import có , / :
- [x] API thật (token JWT emp13 DNS Admin): POST tạo 5/5 endpoint tên có ,/: → 422 errors.name đúng message; tên hợp lệ → không lỗi name
- [x] API thật: /import/validate (customer-scopes + applications) dòng name có ,/: → isValid=false đúng message
- [x] Playwright UI customer-scopes: AC1 mở modal Tạo mới; AC2 tên "Tên sai, có: ký tự cấm" → lỗi đỏ inline dưới ô + không lưu (ac2-name-error.png); AC3 sửa tên hợp lệ → lỗi tên biến mất
- [ ] User verify thêm 4 màn còn lại + luồng import upload file thật (code đối xứng, đã verify BE qua API)

### Checkpoint — 2026-07-14
Vừa hoàn thành: Toàn bộ code BE (10 file) + FE (5 index.vue), verify tinker 2 tầng BE.
Đang làm dở: (không)
Bước tiếp theo: User hard-refresh FE, test tạo/sửa nhập tên có , hoặc : (thấy lỗi đỏ dưới ô, không lưu) + import file có tên chứa , / : (preview báo lỗi, không import).
Blocked:
