# Plan — personnel-report-contract-status

## Phase 1 — Logic trạng thái HĐLĐ theo ngày còn lại

### BE

- [x] Sửa `Modules/Human/Entities/EmployeeInfo.php` — accessor `getLaborContractStatusAttribute()` trả về 1 trong 4 string: `effective` / `expiring_soon` / `expired` / `none` (inline exists() check, không cần thêm relation riêng)
- [x] Bổ sung 2 cột "Hạn HĐLĐ" + "Trạng thái HĐLĐ" vào `resources/views/exports/personnel_report.blade.php` (chèn trước cột "Tổng thu nhập" + helper `laborContractStatusText`)

### FE

- [x] Sửa `pages/human/personnel/index.vue` — `getStatusTextLaborContract()` map 4 string → text VN ("Có hiệu lực" / "Sắp hết hạn" / "Hết hiệu lực" / "Chưa có HĐLĐ")
- [x] Sửa `pages/human/personnel/index.vue` — `getStatusClass()` map 4 string → badge xanh / vàng / đỏ / xám
- [x] Kiểm tra `pages/human/personnel/print.vue` — không có cột HĐLĐ, skip

### Checkpoint — 2026-05-23
Vừa hoàn thành: Phase 1 BE + FE + Excel export đã code xong.
Đang làm dở: chưa test
Bước tiếp theo: user test 6 case dưới
Blocked: -

### Test

- [ ] Test 4 case: NV có HĐLĐ vô thời hạn → "Có hiệu lực"
- [ ] Test NV có HĐLĐ còn 20 ngày → "Có hiệu lực"
- [ ] Test NV có HĐLĐ còn 15/10/0 ngày → "Sắp hết hạn"
- [ ] Test NV có HĐLĐ đã quá hạn (không gia hạn) → "Hết hiệu lực"
- [ ] Test NV chưa có HĐLĐ approved → "Chưa có HĐLĐ"
- [ ] Test export Excel hiển thị đúng text VN ở 2 cột mới
