# Plan — Fix bug màn tạo meeting (?project_id)

## Phase 1 — Bugfix

### FE (hrm-client)
- [x] Bug 1: Bỏ filter `has_customer` theo `isFromProject` trong `meetingTypeOptions` (GeneralInfo.vue) → luôn hiện tất cả loại meeting kể cả khi vào kèm `?project_id`
- [x] Bug 2: Đồng bộ `customer_email` xuống từng project trong 2 vòng sync KH (`autoSelectCustomerFromProject` + `handleCustomerEvent`) → tab "Dự án tiền khả thi" hiện đúng Email khách hàng

### Verify
- [ ] Mở `/assign/meeting/create?project_id=112`: dropdown loại meeting đủ như khi không có project_id; Email khách hàng hiện đúng ở tab dự án
