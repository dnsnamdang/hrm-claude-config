# Fix trùng nhân sự popup sơ đồ cơ cấu tổ chức (/human/company-struct)

## BE
- [x] Sửa `EmployeeInfoService::syncEmployeeConcurrentlyDepartmentHasPosition()` — bỏ `new` thừa (luôn INSERT thay vì UPDATE) + ghép dòng không có id với bản ghi cũ theo (NV, phòng ban, chức vụ) để giữ `position_order_index`
- [x] Seeder dọn dữ liệu trùng `RemoveDuplicateEmployeeConcurrentlyDepartmentPositionSeeder` — đã chạy: 157 → 47 dòng (xóa 110, 16 nhóm)
- [x] Verify: BAN ĐIỀU HÀNH 38 → 7 người, toàn sơ đồ hết node trùng; lưu lại nhiều lần không nhân đôi

### Checkpoint — 2026-08-22
Vừa hoàn thành: fix code + dọn data + verify
Đang làm dở: không
Bước tiếp theo: chạy seeder trên các môi trường còn lại (dev/staging/prod)
Blocked:
