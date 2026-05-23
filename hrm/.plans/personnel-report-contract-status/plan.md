# Plan — personnel-report-contract-status

## Phase 1 — Logic trạng thái HĐLĐ theo ngày còn lại

### BE

- [ ] Sửa `Modules/Human/Entities/EmployeeInfo.php` — accessor `getLaborContractStatusAttribute()` trả về 1 trong 4 string: `effective` / `expiring_soon` / `expired` / `none`
- [ ] Thêm helper `expiredDecisionLaborContract()` trên EmployeeInfo: query HĐLĐ approved có `end_date < today` mới nhất (chỉ dùng khi current null)
- [ ] Bổ sung cột "Hạn HĐLĐ" + "Trạng thái HĐLĐ" vào `app/ExcelExport/PersonnelExport.php` (format text VN)

### FE

- [ ] Sửa `pages/human/personnel/index.vue` — `getStatusTextLaborContract()` map 4 string → text VN ("Có hiệu lực" / "Sắp hết hạn" / "Hết hiệu lực" / "Chưa có HĐLĐ")
- [ ] Sửa `pages/human/personnel/index.vue` — `getStatusClass()` map 4 string → badge xanh / vàng / đỏ / xám
- [ ] Kiểm tra `pages/human/personnel/print.vue` — nếu có cột HĐLĐ thì đồng bộ logic

### Test

- [ ] Test 4 case: NV có HĐLĐ vô thời hạn → "Có hiệu lực"
- [ ] Test NV có HĐLĐ còn 20 ngày → "Có hiệu lực"
- [ ] Test NV có HĐLĐ còn 15/10/0 ngày → "Sắp hết hạn"
- [ ] Test NV có HĐLĐ đã quá hạn (không gia hạn) → "Hết hiệu lực"
- [ ] Test NV chưa có HĐLĐ approved → "Chưa có HĐLĐ"
- [ ] Test export Excel hiển thị đúng text VN ở 2 cột mới
