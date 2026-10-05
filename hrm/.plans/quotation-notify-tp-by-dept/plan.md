# Thông báo báo giá chỉ gửi TP đúng phòng ban — @namdangit (nhánh tpe)

Bug etekpower: TP phòng KD Nhiệt (Phạm Anh Tuấn) nhận thông báo gửi duyệt/đã duyệt báo giá của phòng KD Năng lượng.

- [x] QuotationService: thêm tpApproverInfoIds() (listEmployeeInfoByPermissionAndDepartment theo department_id/company_id báo giá), dùng cho notifyByPermission cấp TP + notifyApproved
- [x] ProspectiveProjectService::collectCloseNotifyTargets (c): TP theo từng phòng của báo giá Chờ TP duyệt
- [x] Rà PricingRequestService:270 — đã lọc theo phòng sẵn, không sửa
- [ ] Commit/push nhánh tpe + deploy etekpower (chờ user)
