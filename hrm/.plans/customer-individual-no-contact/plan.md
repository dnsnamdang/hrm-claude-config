# Plan: KH cá nhân không cần người liên hệ

Feature: customer-individual-no-contact | @manhcuong | 2026-06-29
Spec: docs/superpowers/specs/2026-06-29-customer-individual-no-contact-design.md

## Phase 1 — FE

### Prospective Projects
- [x] `CustomerBlock.vue`: computed `isIndividual = Number(val('type')) === 1` (API có thể trả "1")
- [x] `CustomerBlock.vue`: bọc block người liên hệ (select + thêm nhanh + box readonly) bằng `v-if="!isIndividual"`
- [x] `CustomerBlock.vue`: đổi KH sang cá nhân → clearContact() reset 5 key theo prefix variant qua $emit('update'), watcher `immediate: true`

### Meeting
- [x] `GeneralInfo.vue`: computed `isIndividual = Number(form.customer_type) === 1`
- [x] `GeneralInfo.vue`: bọc block người liên hệ + ẩn dòng readonly "Liên hệ" bằng `v-if="!isIndividual"`
- [x] `GeneralInfo.vue`: đổi KH sang cá nhân → clearContactIfIndividual() reset 5 key (handler nhận KH + watcher immediate)
- [x] `MeetingForm.vue` validate(): contact required chỉ khi `Number(customer_type) !== 1` (LƯU Ý: call site validate() đang comment từ trước → inert; user chốt giữ nguyên, dựa BE chặn)

## Phase 2 — BE

- [x] `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`: withValidator + sometimes() required khi có customer_id && (int)customer_type !== 1 && has_customer; cá nhân nullable; fallback tra DB Customer khi type rỗng
- [x] `ProspectiveProjectRequest`: contact block direct required khi (int)customer_type !== 1; benefit giữ optional

## Phase 2b — Fix bug reactivity (phát hiện khi verify)
- [x] BUG: màn Meeting KH cá nhân không ẩn block người liên hệ. Root cause: object `form` (prop, nguồn ở create.vue/edit.vue + resetForm MeetingForm) KHÔNG khai báo key `customer_type` → gán `form.customer_type=1` là thêm prop mới → Vue 2 không reactive → computed `isIndividual` không recompute.
- [x] Fix `create.vue`: thêm customer_type/customer_type_text/customer_contact_email vào form data
- [x] Fix `MeetingForm.vue` resetForm(): thêm 3 key trên
- [x] Fix `_id/edit.vue`: merge default 3 key khi `this.form = data`
- (Prospective không dính vì formSubmit đã có sẵn key qua field())

## Phase 4 — Khoá chọn KH ở tab Dự án TKT của Meeting (yêu cầu bổ sung)
Tab TKT trong Meeting không cho chọn KH độc lập, phải theo KH đã chọn ở tab Thông tin (chốt: chỉ khoá picker KH trực tiếp).
- [x] `CustomerBlock.vue`: thêm prop `lockPicker` (default false) → ẩn nút "Thêm nhanh khách hàng" + chặn `openPicker` + đổi placeholder "Khách hàng theo tab Thông tin"
- [x] `CustomerInfoSection.vue`: thêm prop `lockDirectCustomer` (default false) → truyền `:lock-picker` xuống block direct (benefit không khoá)
- [x] `MeetingProject.vue`: `<CustomerInfoSection :lock-direct-customer="true">`
- [x] Kế thừa `customer_type` xuống project: addProject init từ `this.form.customer_type`; `syncCustomerScopeToProjects()` sync thêm customer_type/_text (để tab TKT ẩn người liên hệ đúng khi KH meeting là cá nhân)
- [x] Verify UI Playwright: tab TKT không có nút chọn/thêm KH, click không mở modal, KH = KH tab Thông tin → PASS; Prospective không bị khoá nhầm → PASS

## Phase 5 — Bug: manager tab 'Dự án' không hiện "Đối tượng tổ chức" KH cuối
Màn /assign/prospective-projects/{id}/manager tab Dự án (TktTab → CustomerInfoSection isShow) hiển thị KH qua val('type_text').
- [x] Xác minh: DetailProspectiveProjectResource trả customer_type/customer_type_text cho KH trực tiếp (tinker PASS), nhưng THIẾU customer_benefit_type/customer_benefit_type_text cho KH cuối → KH cuối hiện '—'.
- [x] Fix BE: thêm customer_benefit_type + customer_benefit_type_text vào DetailProspectiveProjectResource (tra customer_type từ customer_benefit_id, map CUSTOMER_TYPES giống direct)
- [x] Verify tinker/API: resource nay có customer_type_text (direct) + customer_benefit_type/_text (benefit); php -l sạch
- [x] ROOT CAUSE FE: manager.vue dùng `Object.assign(tktForm, project)` (mutate) → key KHÔNG khai báo sẵn trong tktForm thành non-reactive (Vue2); tktForm thiếu khai báo customer_benefit_type/_text → KH cuối không hiện. (edit.vue dùng `this.formSubmit = {...}` reassign nên hiện đúng → khác biệt)
- [x] Fix FE manager.vue: (1) khai báo customer_benefit_type/_text trong tktForm; (2) populateTktFormFromProject chuyển Object.assign → thay nguyên object `this.tktForm = {...tktForm, ...project,...}` (giống edit.vue) → mọi key API reactive
- [ ] User deploy + verify lại trên dev: tab Dự án manager hiện Đối tượng tổ chức cả KH trực tiếp lẫn KH cuối

## Phase 3 — Verify
- [x] tinker BE: Meeting create/update + Prospective — type=2 (int & "2") required contact; type=1 không lỗi. PASS toàn bộ
- [x] Playwright Prospective: DN hiện / cá nhân ẩn → 2/2 PASS
- [x] Playwright Meeting (sau fix reactivity): DN hiện / cá nhân ẩn → PASS
- [x] Playwright tab TKT khoá KH + Prospective không regression → PASS

## Checkpoint — 2026-06-29 (hoàn tất)
Vừa hoàn thành: Toàn bộ feature CODE DONE + VERIFIED. (1) Ẩn người liên hệ khi KH cá nhân ở Prospective + Meeting; (2) BE bắt buộc contact cho DN; (3) fix bug reactivity Meeting (form thiếu customer_type); (4) khoá chọn KH ở tab Dự án TKT của Meeting (theo KH tab Thông tin).
Verify: BE tinker PASS toàn bộ; Playwright PASS hết (Meeting cá nhân ẩn/DN hiện, tab TKT khoá KH, Prospective không regression).
Bước tiếp theo: Chờ user review / merge. KHÔNG git.
Blocked: (không)

## Checkpoint
### Checkpoint — 2026-06-29
Vừa hoàn thành: Code DONE Phase 1 (FE) + Phase 2 (BE), đã review từng task + áp fix (Number() cast, immediate watcher, guard chuỗi rỗng BE, ẩn dòng readonly Liên hệ meeting). php -l sạch.
Đang làm dở: Phase 3 verify (chưa chạy).
Bước tiếp theo: Verify Playwright + tinker/HTTP.
Blocked: (không)
