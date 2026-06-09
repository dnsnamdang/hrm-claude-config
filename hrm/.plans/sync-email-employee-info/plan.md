# Plan — Đồng bộ email employees ↔ employee_infos

## Phase 1 — Sync runtime + fix data cũ

### BE
- [x] Thêm sync chiều ngược `employees.email → employee_infos.email` trong `EmployeeService::updateEmployee` (dùng `saveQuietly`, chỉ chạy khi khác nhau) — `EmployeeService.php:274-279`
- [x] Tạo command `human:sync-employee-email` (`--dry-run`): set `employees.email = employee_infos.email` ở bản ghi lệch, bỏ qua khi `employee_infos.email` rỗng — `app/Console/Commands/SyncEmployeeEmailFromInfo.php`
- [x] `php -l` 2 file pass

### FE
- [ ] Không đổi (chiều hồ sơ → tài khoản đã có sẵn)

### Verify (user chạy)
- [ ] `php artisan human:sync-employee-email --dry-run` → xem danh sách lệch
- [ ] `php artisan human:sync-employee-email` → đồng bộ
- [ ] Sửa email tài khoản ở màn nhân viên → kiểm tra hồ sơ cập nhật theo
- [ ] Sửa email công ty ở hồ sơ → kiểm tra tài khoản cập nhật theo
