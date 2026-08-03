# Plan — Khách hàng thụ hưởng cuối cho Dự án TKT

Feature: `prospective-project-end-customer` · @manhcuong
Spec: `docs/superpowers/specs/2026-06-25-prospective-project-end-customer-design.md`

## Phase 1 — KH thụ hưởng cuối (KHÔNG đụng Ứng dụng)

### BE (hrm-api / Modules/Assign)
- [x] Migration `2026_06_25_000001_add_end_customer_fields_to_prospective_projects_table` — thêm `is_intermediary_customer` + bộ cột `customer_benefit_*` (id/code/phone/email/contact_*/scope_id/scope_group_id)
- [x] Model `ProspectiveProject` — fillable cột mới + relation `customerBenefitScope()`, `customerBenefitScopeGroup()`
- [x] `ProspectiveProjectRequest` — rule nullable cho field mới (email KH cuối nếu nhập) + attributes nhãn
- [x] Service `applyBeneficiary($project,$request)` gọi trong store/update — nguồn scope theo KH cuối/fallback + copy snapshot KH trực tiếp khi bỏ trống + ép benefit_id=customer_id khi checkbox false
- [x] `DetailProspectiveProjectResource` — trả field benefit đầy đủ + `is_intermediary_customer` + mask `customer_benefit_phone`/`customer_benefit_contact_phone` + tên scope/group qua relation
- [x] `php -l` các file BE — sạch

### FE (hrm-client / pages/assign/prospective-projects)
- [x] Tách sub-component `components/CustomerBlock.vue` (variant direct|benefit): chọn KH, box readonly, Loại hình/Lĩnh vực + icon (i) tooltip, email, người liên hệ + thêm nhanh; emit update/open-picker/open-quick-add
- [x] `CustomerInfoSection.vue` — dùng CustomerBlock cho trực tiếp; checkbox "KH thương mại dịch vụ"; CustomerBlock benefit ẩn/hiện theo checkbox; 1 instance modal + `pickerTarget` định tuyến
- [x] `add.vue` — đổi thứ tự Customer↔Project; thêm field benefit + is_intermediary_customer vào formSubmit
- [x] `_id/edit.vue` — đổi thứ tự section; map field benefit khi populate (spread ...data)
- [x] `_id/index.vue` — đổi thứ tự section (detail readonly)

### Verify
- [x] Chạy migration BE (đã migrate thật)
- [x] Playwright (tài khoản namdangit) — 11/11 check chức năng PASS: ADD/DETAIL/EDIT đều "KH đứng trước Dự án"; checkbox ẩn/hiện KH cuối đúng; chọn KH nạp Loại hình/Lĩnh vực; icon (i) tooltip hiện (info-tip)
- [x] Tinker reflection `applyBeneficiary` 3 nhánh PASS (KH cuối có scope→theo cuối; rỗng→fallback trực tiếp; không trung gian→copy snapshot)
- [x] DetailResource benefit fields + scope/group name + masking: owner(211) thấy SĐT thật, NV thường(25) thấy '-' (chỉ che SĐT, tên hiện). Dọn sạch data test.

### Checkpoint — 2026-06-25
Vừa hoàn thành: CODE DONE + VERIFIED Phase 1. BE migration đã chạy thật. Playwright + tinker reflection + DetailResource render đều PASS. Masking SĐT KH cuối đúng (owner thật / NV thường '-').
Đang làm dở: không.
Bước tiếp theo: (nếu user muốn) Phase 2 nhóm Ứng dụng. Lưu ý: lệnh migrate cũng chạy luôn migration pending của feature customer-scope-multi-select (gồm drop cột đơn customers) — backfill pivot chạy trước drop nên data đã chuyển; cần báo @manhcuong.
Blocked:

## Phase 2 — Ứng dụng (ĐANG LÀM 2026-06-25)

Quyết định: cột chính (application_id, customer_scope_id, customer_scope_group_id) = HIỆU LỰC (KH cuối nếu trung gian, else trực tiếp); thêm customer_application_id (app KH trực tiếp) + customer_benefit_application_id (app KH cuối). Ứng dụng* required mọi trường hợp. Form-template suy industry từ application hiệu lực (server).

### BE (DONE)
- [x] Migration `2026_06_25_000002` thêm `customer_application_id` + `customer_benefit_application_id`
- [x] Model: fillable + relation `customerApplication()`, `customerBenefitApplication()` + accessor getEffectiveCustomerScopeId/Group
- [x] Request: scope_id/industry_id/application_id → nullable; customer_application_id required; customer_benefit_application_id required_with:customer_benefit_id
- [x] Service: applyBeneficiary set application_id hiệu lực + sync benefit app; KHÔNG override customer_scope_id (giữ KH trực tiếp — Model B); reorder TRƯỚC autoFillFromApplication (luôn suy scope/industry từ app hiệu lực); code-gen dùng $project->application_id
- [x] SolutionService autofill: customer_scope_id = getEffectiveCustomerScopeId()
- [x] DetailResource: trả customer_application_id/name + customer_benefit_application_id/name
- [x] CustomerDetailResource: thêm customer_scope_groups + customer_scope_pairs (id+name) cho select Loại hình/Lĩnh vực
- [x] Endpoint `GET assign/applications/for-selection` (auth:api) + controller forSelection
- [x] SolutionResource: thêm customer_scope_group_name + customer_benefit_code/name + customer_benefit_scope_group_name
- [x] Controller store/update: thay check 423 scope/industry/application → checkCustomerApplicationsActive (FIX lỗi 423 user gặp)

### FE (DONE)
- [x] add/edit/index formSubmit: thêm customer_application_id/name, customer_benefit_application_id/name + scope_group_options/scope_pair_options (direct+benefit)
- [x] ProjectInfoSection: XÓA khối Nhóm ngành/Nhóm giải pháp/Ứng dụng + nút + SolutionListModal + JS cascade
- [x] CustomerBlock: Loại hình + Lĩnh vực thành SELECT chọn 1 (multi theo KH khai báo, Lĩnh vực lọc theo Loại hình) + Ứng dụng* (for-selection) + icon (i) + cảnh báo rỗng + nút Xem danh sách giải pháp
- [x] CustomerInfoSection: nạp options Loại hình/Lĩnh vực từ customer detail (auto-chọn khi đơn) + watcher nạp lại khi sửa/chi tiết + 1 SolutionListModal route open-solutions
- [x] SolutionListModal: cell "Mã-Tên KH" bỏ Ứng dụng + thêm Loại hình hoạt động; thêm cột "Khách hàng cuối"

### Verify (DONE phần BE/API)
- [x] for-selection lọc đúng (group+scope) + cảnh báo rỗng
- [x] applyBeneficiary 3 nhánh + accessor hiệu lực (tinker reflection)
- [x] POST /assign/prospective-projects với payload thật → 200, app_id hiệu lực=222, scope giữ KH trực tiếp (FIX 423)
- [x] customer detail trả scope_groups + scope_pairs có tên
- [ ] Playwright UI: dev-server timeout login (flaky môi trường, không phải code) — payload browser thật của user xác nhận FE chạy đúng

### Phase 2b — Đồng bộ các màn hiển thị thông tin dự án (2026-06-26)
- [x] TktTab.vue (dùng bởi manager + Yêu cầu làm GP): đảo thứ tự CustomerInfoSection lên trước ProjectInfoSection; bỏ prop thừa is-populating
- [x] CustomerBlock: fallback option cho Loại hình/Lĩnh vực/Ứng dụng (readonly hiện tên đã lưu vì TktTab không lắng @update); ẩn cảnh báo rỗng ở readonly
- [x] manager.vue: bổ sung field benefit/intermediary/scope_group/application/options vào tktForm init + truyền :project (tránh warning)
- [x] RequestSolutionForm.vue: bổ sung field mới vào 2 block tktForm (init + reset)
- [x] index.vue danh sách: thêm cột "Khách hàng cuối" (ProspectiveProjectResource trả customer_benefit_code/name + is_intermediary_customer + customer_scope_group_name)

### Phase 2c — Sync MeetingProject (tab Dự án TKT trong Meeting) (2026-06-26)
BE (refactor dùng chung):
- [x] ProspectiveProjectService: applyBeneficiary đọc từ MODEL (bỏ $request) + method PUBLIC applyCustomerDerivedFields (applyBeneficiary+autoFillFromApplication) + handleFormTemplateSnapshot → public
- [x] MeetingService: mapMeetingProjectToProspectiveProject thêm customer_application_id (fallback app_id) + customer_benefit_* + is_intermediary_customer + customer per-project (ưu tiên project, fallback meeting) + project_address(fallback address)/implementation_type/project_description; syncProjects + saveFormAnswersForProject gọi applyCustomerDerivedFields; fallback handleFormTemplateSnapshot tạo phiếu theo industry suy từ ứng dụng; getDataForShow trả đủ field mới + tên + project_address/implementation_type
- [x] MeetingController store/update: validate active → Ứng dụng KH trực tiếp + KH cuối (thay scope/industry/app_id)
- [x] MeetingCreate/UpdateApiRequest: app_id/scope_id/industry_id → nullable; customer_application_id required; customer_benefit_application_id required_with benefit; is_intermediary_customer boolean
FE:
- [x] MeetingProject.vue: thay khối Thông tin dự án/Thông tin khách hàng bằng CustomerInfoSection + ProjectInfoSection (bind p); onProjectUpdate + projectErrors (map lỗi nested); addProject/normalizeProjects/loadProspectiveProjectFromQuery/saveFormAnswers dùng field mới; tab phiếu gating theo customer_application_id; bỏ watcher criteria scope/industry
Verify:
- [x] tinker: meeting map + applyCustomerDerivedFields → app hiệu lực=222, scope giữ trực tiếp=23, scope/industry suy=6/9, project_address ok
- [x] FIX BUG user: chọn dự án ở tab Thông tin (GeneralInfo) chưa fill Email + Cách triển khai vào tab Dự án TKT. Nguyên nhân: getProspectiveProjects map + handleProjectChange không mang implementation_type/customer_application_id... (chỉ cherry-pick field cũ). Sửa: spread `...item`/`...project` mang toàn bộ field; ProspectiveProjectResource (getForMeeting) bổ sung customer_application_id/name, customer_scope_group_id, customer_tax_code/phone/address, project_description, bộ customer_benefit_* đầy đủ
- [x] Playwright E2E (bypass login = inject access_token vì dev-server login flaky): chọn dự án 4 ở tab Thông tin → tab Dự án TKT fill ĐỦ: Email=emailkh1@gmail.com, Cách triển khai=Liên phòng ban, Loại hình=Sản xuất đồ gỗ, Lĩnh vực, Ứng dụng=UD.EHS1, phân vùng KH thụ hưởng cuối hiện đầy đủ (screenshot xác nhận). Cách triển khai PASS cả 2 lần chạy; Email/Loại hình luân phiên PASS do race đọc headless (UI thực render đủ — screenshot)

### Phase 2d — Gộp Ứng dụng 1 trường + tinh chỉnh form (2026-06-26)
Yêu cầu user: (1) Ngân sách dự kiến bắt buộc; (2) Ứng dụng chỉ của KH cuối (không tick → KH trực tiếp là KH cuối); (3) chỉ còn 1 Ứng dụng → đặt dưới "Tên dự án TKT" + nút Xem danh sách giải pháp; (4) Email KH thu nhỏ (col-4) đặt ngay sau Lĩnh vực kinh doanh.
- [x] BE Request: estimated_budget required; application_id required (1 trường); customer_application_id/benefit → nullable
- [x] BE applyBeneficiary: KHÔNG overwrite application_id (FE gửi trực tiếp); đồng bộ customer_application_id = customer_benefit_application_id = application_id; giữ scope Model B
- [x] BE controller checkCustomerApplicationsActive: chỉ check application_id
- [x] BE meeting: map đọc application_id (1 trường); FormRequest app→nullable (nháp); controller check tolerant null
- [x] FE CustomerBlock: BỎ khối Ứng dụng + nút; Email (col-4) đưa vào cùng hàng ngay sau Lĩnh vực; dọn data/computed/method ứng dụng
- [x] FE ProjectInfoSection: THÊM Ứng dụng (1 trường, lọc theo Loại hình+Lĩnh vực KH CUỐI = endScope) + tooltip + cảnh báo rỗng + nút Xem danh sách giải pháp + SolutionListModal, đặt ngay dưới Tên dự án TKT
- [x] FE CustomerInfoSection: bỏ SolutionListModal + open-solutions (chuyển sang ProjectInfoSection)
- [x] FE FinanceSection: Ngân sách dự kiến required + inline error
- [x] Verify: Playwright (token bypass) — Ứng dụng ở Thông tin dự án (option UD.EHS1 lọc theo KH cuối), bỏ khỏi phân vùng KH, Email cạnh Lĩnh vực, Ngân sách dự kiến hiện (screenshot xác nhận); API 422 đúng khi thiếu estimated_budget + application_id

### Phase 2e — Loại hình/Lĩnh vực cũng chỉ 1 lần (của KH cuối) (2026-06-26)
- [x] BE Request: customer_scope_group_id/customer_scope_id → nullable + withValidator sometimes: required khi !trung gian; customer_benefit_scope_group_id/scope_id required khi trung gian. Nhãn lỗi cập nhật (Loại hình hoạt động/Lĩnh vực kinh doanh + bản KH cuối)
- [x] BE meeting FormRequest: customer_scope_group_id/scope_id → nullable (nháp + ẩn theo điều kiện)
- [x] FE CustomerBlock: thêm prop showScope; ẩn 2 cột Loại hình+Lĩnh vực khi !showScope; nhãn required cố định (khối hiển thị = KH cuối)
- [x] FE CustomerInfoSection: direct :show-scope="!is_intermediary_customer"; benefit mặc định true
- [x] Verify Playwright 7/7: không tick → Loại hình/Lĩnh vực 1 lần ở khối trực tiếp; tick+chọn KH cuối → 1 lần ở khối KH cuối, ẩn ở trực tiếp

### Checkpoint — 2026-06-25 (Phase 2)
Vừa hoàn thành: Phase 2 (Ứng dụng) CODE DONE + fix 423. Loại hình/Lĩnh vực thành select multi theo logic KH mới. POST payload thật → 200.
Bước tiếp theo: user verify UI thêm (tạo + lưu nháp/gửi duyệt, popup GP cột Khách hàng cuối).

### Phase 2f — Required các trường KH thụ hưởng cuối khi tick "KH thương mại dịch vụ" (2026-06-30)
Yêu cầu user: tick "KH thương mại dịch vụ" (is_intermediary_customer) → các trường KH thụ hưởng cuối bắt buộc, đối xứng KH trực tiếp (khách hàng, email, người liên hệ nếu là doanh nghiệp).
- [x] BE Request withValidator: customer_benefit_id required khi trung gian; customer_benefit_email required|email khi trung gian; customer_benefit_contact_name/phone required khi trung gian + KH cuối là doanh nghiệp (benefitCustomerRequiresContact, đối xứng directCustomerRequiresContact)
- [x] BE Request: messages (customer_benefit_id/email .required) + attributes (customer_benefit_id, contact_name/phone)
- [x] FE CustomerInfoSection: benefit block :required-customer="true" (hiện dấu * + inline error cho Khách hàng/Email/Người liên hệ)
