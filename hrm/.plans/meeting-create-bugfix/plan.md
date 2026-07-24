# Plan — Fix bug màn tạo meeting (?project_id)

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
