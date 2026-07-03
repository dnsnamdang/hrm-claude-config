# Plan — prospective-project-customer-erp-scope

@dnsnamdang · 2026-06-09

## Phase 1 — BE (Modules/Assign)
- [x] BE1: Thêm `CustomerService::scopeByCode($code)` đọc TpCustomer (mysql2) → trả scope_group_id/_name, scope_id/_name, customer_type/_text
- [x] BE2: Thêm `CustomerController@scopeByCode` + route mở `GET assign/customers/scope-by-code` (đặt TRƯỚC route `/{id}`)
- [x] BE3: `ProspectiveProjectRequest` — cố định luồng 'scope', bỏ nhánh customer_scope, require đủ 5 field scope + message thiếu KH scope
- [x] BE4: `ProspectiveProjectService::autoFillFromApplication` — gỡ override customer_scope_group_id/customer_scope_id
- [x] BE5: `DetailProspectiveProjectResource` — thêm `customer_type`/`customer_type_text` để edit hiển thị read-only
- [x] BE6: php -l các file BE đã sửa — PASS

## Phase 2 — FE QuickAddCustomerModal
- [x] FE1: Tạo `components/modals/QuickAddCustomerModal.vue` (V2Base, type cá nhân/tổ chức, options ERP geo, CustomerScopeSelect 2 chiều)
- [x] FE2: Validate inline 422 + emit created

## Phase 3 — FE CustomerInfoSection
- [x] FE3: Icon `+` mở QuickAddCustomerModal
- [x] FE4: Gọi scope-by-code khi chọn KH / sau quick-add → set 3 field + name (fillScopeFromErp)
- [x] FE5: Render 3 trường read-only (Nhóm LVKH, Đối tượng tổ chức, Lĩnh vực KH droplist disabled) + V2BaseError
- [x] FE6: Quick-add flow: POST → lấy code → tra HRM theo code (selectCustomerByCode) → auto-select

## Phase 4 — FE ProjectInfoSection
- [x] FE7: Bỏ radio selectionMode + block customer_scope; cố định 'scope' (rewrite file)
- [x] FE8: Bỏ 2 dropdown Nhóm LVKH + Lĩnh vực KH; gỡ khỏi cascade (computed/watch/prune/autofill)
- [x] FE9: `edit.vue` — detectSelectionMode no-op; thêm field name read-only vào formSubmit (add+edit)

## Phase 5 — Verify
- [x] V1: php -l toàn bộ BE PASS; rà soát FE không còn ref customer_scope trong cascade form (list index.vue độc lập, giữ nguyên)
- [ ] V2: User verify browser theo AC1-AC5

## Phase 6 — Popup chọn KH theo nguồn ERP (assign/customers)
Mục tiêu: popup "Chọn khách hàng" ở form Dự án TKT chỉ hiện đúng KH ERP như màn /assign/customers (TpCustomer + lọc phân quyền ERP), thay vì bảng local customers (Timesheet).
- [x] FE10: Tạo modal mới `components/modals/ChooseErpCustomerModal.vue` (id `choose-erp-customer`) — fetch `assign/customers` (apiGetMethod), search keyword/MST/SĐT, phân trang, click chọn emit `choiceCustomer`
- [x] FE11: CustomerInfoSection — thay `<AddCustomer>` bằng modal mới; `showChoiceCustomerFrom` mở id mới
- [x] FE12: `handleCustomerEvent` — id giờ là TpCustomer; lấy chi tiết qua `assign/customers/{id}` (contacts ERP, gán id theo index nếu thiếu); map field từ record list (address dựng sẵn)
- [x] FE13: `selectCustomerByCode` (luồng quick-add) — đổi sang tra `assign/customers?code=` thay vì `customers/`
- [x] FE14: Restyle popup theo skill `modal-popup` — header icon tròn + nút X, search dùng V2BaseLabel/V2BaseInput/V2BaseButton, phân trang V2BasePagination, footer Đóng (tertiary), cho click backdrop đóng, tải dữ liệu khi `@show`
- [x] FE15: SĐT cấp KH (ERP) thường rỗng → fallback số điện thoại người liên hệ đầu tiên (CustomerInfoSection.handleCustomerEvent)
- [x] FE16: Áp dụng popup ERP cho màn Họp (`pages/assign/meeting/components/GeneralInfo.vue`): thay AddCustomer→ChooseErpCustomerModal, `handleCustomerEvent` + `autoSelectCustomerFromProject` đổi sang `assign/customers/{id}` + contacts gán id + fallback SĐT
- [x] BE6: `CustomerService::index` + `applyErpVisibilityScope($query, $exactPhone)` — search SĐT khớp ĐÚNG HOÀN TOÀN thì bypass quyền xem (OR token-match `CONCAT(',',REPLACE(mobile,' ',''),',') LIKE '%,phone,%'`), gated bằng cờ `phone_exact_bypass` → màn /assign/customers KHÔNG đổi
- [x] FE17: Popup gửi `phone_exact_bypass=1` khi search SĐT (ChooseErpCustomerModal.getData)
- [x] BE7: `MeetingController::addContact` — lưu người liên hệ thẳng vào ERP (`TpCustomerContact`, mysql2) theo customer_id ERP, `created_by = erpEmployeeId()`; trả shape {id,fullname,role,phones,email}. KHÔNG gate quyền (theo yêu cầu). Lý do: picker đổi sang nguồn ERP → trước đó addContact ghi vào local `customer_contacts` gây lệch id + mất khi reload

## Phase 7 — Meeting tab "Dự án TKT": Nhóm/Lĩnh vực KH thuộc khách hàng
Mục tiêu: tab Dự án TKT trong meeting giống form TKT độc lập — Nhóm LVKH + Lĩnh vực KH read-only theo khách hàng (Thông tin khách hàng), bỏ trường Lĩnh vực KH ở Thông tin dự án.
- [x] FE18: GeneralInfo — `fillScopeFromErp(code)` (scope-by-code) set form.customer_scope_* + `syncCustomerScopeToProjects()`; gọi sau chọn KH (handleCustomerEvent, autoSelectCustomerFromProject) + cuối handleProjectChange; clearCustomer xóa scope
- [x] FE19: MeetingProject — bỏ select "Lĩnh vực khách hàng" ở Thông tin dự án; thêm 2 trường read-only Nhóm LVKH + Lĩnh vực KH ở Thông tin khách hàng (p.customer_scope_group_name / p.customer_scope_name); addProject lấy scope từ form; bỏ reset customer_scope_id ở onScopeChange/onIndustryChange/onApplicationChange (no-op)
- [x] BE8: MeetingService.mapMeetingProjectToProspectiveProject +customer_scope_group_id; convertedProject (load lại meeting) +customer_scope_group_id + tên Nhóm/Lĩnh vực (join customer_scope_groups/customer_scopes)
- [x] BE9: Create/UpdateApiRequest — `projects.*.customer_scope_group_id` + `projects.*.customer_scope_id` = required + message "… là bắt buộc (khách hàng chưa gắn lĩnh vực)"
- [x] FE20: MeetingProject — 2 trường scope read-only thêm `<Required />` + V2BaseError (formError['projects.N.customer_scope_group_id'|'.customer_scope_id'])
- [ ] FE-verify: User chạy browser — mở form Dự án TKT → popup chỉ hiện KH ERP, chọn KH set đủ field + dropdown Người liên hệ + scope auto. (Lưu ý: popup gate quyền ERP `Xem khách hàng`)

---
## Checkpoint
### Checkpoint — 2026-06-09 (khởi tạo)
Vừa hoàn thành: brainstorm + spec + plan
Đang làm dở: chưa code
Bước tiếp theo: BE1
Blocked:

### Checkpoint — 2026-06-09 (CODE DONE)
Vừa hoàn thành: toàn bộ BE (Phase 1) + FE (Phase 2-4). php -l PASS.
- BE: CustomerService.scopeByCode + CustomerController.scopeByCode + route mở `GET assign/customers/scope-by-code`; ProspectiveProjectRequest cố định luồng scope (5 field required + message KH thiếu scope); ProspectiveProjectService.autoFillFromApplication gỡ override customer_scope; DetailProspectiveProjectResource +customer_type/_text.
- FE: QuickAddCustomerModal.vue mới (post POST assign/customers); CustomerInfoSection (icon +, 3 trường read-only, fillScopeFromErp, selectCustomerByCode, handleCustomerCreated); ProjectInfoSection rewrite (bỏ radio + block customer_scope + 2 dropdown, decouple cascade); add.vue/edit.vue thêm 4 field formSubmit.
Đang làm dở: không
Bước tiếp theo: user verify browser AC1-AC5 (FE chưa build được tại đây — node_modules hrm-client trống)

### Checkpoint — 2026-06-09 (rework modal theo skill)
QuickAddCustomerModal.vue viết lại theo `.claude/skills/modal-popup` + `button-convention`:
- Cấu trúc: hide-footer + custom #modal-header (icon tròn + title + nút X) + modal-body + modal-footer; cho click backdrop đóng (bỏ no-close-on-backdrop).
- Mọi select → `V2BaseSelectInModal` (loại hình, quốc gia/tỉnh/phường, nhóm+lĩnh vực KH); options shape {id,name}.
- Mọi lỗi validate → `V2BaseError` (:message nhận array 422 trực tiếp), bỏ div text-small-error tự chế.
- Footer: V2BaseButton primary "Lưu" (ri-save-3-line) + tertiary "Đóng" (fas fa-arrow-left), đúng thứ tự.
- Scope 2 chiều inline bằng watcher (bỏ phụ thuộc CustomerScopeSelect multiselect).
Cần xác nhận: quyền quick-add (POST assign/customers gated `erpPermission:Thêm khách hàng`) — user tạo dự án không có quyền này sẽ 403 khi thêm nhanh KH. Hỏi user có muốn mở quyền cho quick-add không.
Blocked:
