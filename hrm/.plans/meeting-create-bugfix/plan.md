# Plan — Fix bug màn tạo meeting (?project_id)

## Phase 2 — Bugfix 400 "projects.0.address: Bắt buộc phải nhập" (2026-07-23)

### Nguyên nhân
- Form nhập dự án TKT trong meeting (ProjectInfoSection dùng chung) bind địa điểm vào `project_address`; field `address` khởi tạo rỗng ở `addProject()` và không được sync khi submit.
- `getProjectData()` (MeetingProject.vue) spread nguyên object → gửi `projects[0][address]=''` trong khi BE `MeetingCreateApiRequest` validate `projects.*.address => required` → 400 dù user đã nhập địa điểm.
- Các flow khác (saveFormAnswersForProject, loadProspectiveProjectFromQuery) đã có sync `address = project_address || address` — riêng getProjectData thiếu.

### FE (hrm-client)
- [x] `getProjectData()` trong `pages/assign/meeting/components/MeetingProject.vue`: sync `address`/`project_address` (lấy `project_address || address`) trước khi push vào payload — giống pattern dòng 947-948

### Verify
- [x] Replay API trên dev-hrm (curl, tài khoản namdangit): payload gốc của user → 400 `projects.0.address`; thêm `projects[0][address]` (như FE sau fix) → validate pass, meeting tạo thành công (id 48, 49 — đã xóa qua API delete)
- [x] Compile check MeetingProject.vue: vue-template-compiler 0 lỗi template + babel parse script OK
- [ ] Verify UI trên browser sau khi deploy code FE lên dev: tạo meeting có dự án TKT nhập tay → lưu thành công

### Checkpoint — 2026-07-23
Vừa hoàn thành: fix sync address trong getProjectData() (MeetingProject.vue) + verify API dev
Đang làm dở: (không)
Bước tiếp theo: user deploy hrm-client lên dev + verify UI tạo meeting
Blocked: (không)

## Phase 1 — Bugfix

### FE (hrm-client)
- [x] Bug 1: Bỏ filter `has_customer` theo `isFromProject` trong `meetingTypeOptions` (GeneralInfo.vue) → luôn hiện tất cả loại meeting kể cả khi vào kèm `?project_id`
- [x] Bug 2: Đồng bộ `customer_email` xuống từng project trong 2 vòng sync KH (`autoSelectCustomerFromProject` + `handleCustomerEvent`) → tab "Dự án tiền khả thi" hiện đúng Email khách hàng
- [x] Bug 3: Lỗi 400 `projects.0.is_intermediary_customer must be true or false` khi tạo meeting từ dự án. Nguyên nhân: `buildFormData` ép JS boolean thành chuỗi `"false"/"true"` khi build FormData, rule `boolean` của Laravel không nhận. Fix: trong `buildFormData` convert boolean → `1/0` trước khi `append`. Sửa 3 bản copy: `create.vue`, `_id/edit.vue`, `components/MeetingForm.vue`

### Verify
- [ ] Mở `/assign/meeting/create?project_id=112`: dropdown loại meeting đủ như khi không có project_id; Email khách hàng hiện đúng ở tab dự án
- [ ] Tạo meeting từ `?project_id=38` lưu thành công, không còn lỗi 400 `is_intermediary_customer`

### BE (hrm-api) — bổ sung 2026-07-17
- [x] Bug 4: Email khách hàng nhập ở màn sửa meeting không lưu vào dự án TKT khi customer chỉ tồn tại ở ERP (chưa sync sang bảng `customers` HRM). Nguyên nhân: `MeetingService::mapMeetingProjectToProspectiveProject` chỉ gán `customer_email/phone/tax_code/address` khi `Customer::find($resolvedCustomerId)` tìm thấy; nếu null → bỏ qua toàn bộ → mất dữ liệu user nhập. Fix: luôn ưu tiên giá trị FE gửi lên, `optional($customer)` chỉ để fallback khi FE bỏ trống.

### Verify (bổ sung)
- [ ] Tạo dự án TKT từ màn sửa meeting với KH (nhập Email KH) → mở chi tiết dự án: Email khách hàng hiển thị đúng giá trị đã nhập (kể cả KH ERP-only)
