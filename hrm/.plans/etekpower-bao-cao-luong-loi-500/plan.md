# Lỗi 500 màn Bảng nhân sự và quỹ lương — hrm.etekpower.com.vn (chưa có số Redmine) — @cuong61n

Màn `human/report/employee_salary_report` (API `payroll/salary/report`) báo lỗi 500 trên site etekpower (nhánh `tpe`, PHP 8.1).

## Nguyên nhân
- `employee_salary_histories.other_allowances` là `varchar(255)`; 4 dòng (id 94, 102, 108, 109) lưu chuỗi kiểu VN `6.000.000`.
- PHP 8 báo `A non-numeric value encountered` khi `Collection::sum` ở `SalaryService.php:1141` (PHP 7 bỏ qua). Hiện ra sau khi prod lên PHP 8.1 ngày 03/11/2026.

## Task
- [x] 16/11/2026 Điều tra: đọc log `/var/www/etekpower/hrm-api/storage/logs/laravel.log` trên `hrm-prod`, truy ra dòng 1141 + quét DB các cột tiền khác (chỉ `other_allowances` sai).
- [x] 16/11/2026 Sửa dữ liệu prod `hrm_power`: bỏ dấu chấm 4 dòng → 6000000 / 10000000 / 13380000 / 22485000; kiểm lại còn 0 dòng sai.
- [x] 16/11/2026 Sửa code (nhánh `tpe`, commit `0e236c878`, CHƯA push): `SalaryService::report` ép `other_allowances` về số bằng `CAST(REPLACE(..., CHAR(46), "") AS SIGNED)` ở cột chọn và ở tổng `total`. Kiểm biểu thức SQL trên DB prod (chuỗi lỗi, số thường, 0, NULL đều ra số đúng); `php -l` sạch.
- [ ] Push nhánh `tpe` + deploy etekpower bằng `~/build_tpe.sh`, mở lại màn kiểm.
- [ ] (Đề xuất) Đổi cột `other_allowances` sang kiểu số, và chặn nhập chuỗi có dấu chấm ở form lương.

## Phát sinh 16/11/2026 — không vào được `human/labor-contract` (etekpower)
- [x] 16/11/2026 Nguyên nhân: menu/màn nhánh `tpe` cần quyền `Xem danh mục hợp đồng lao động theo tổng công ty/công ty` (id 910/911, mới tạo 11:55 do seeder trong build), vai trò Admin (id 3, company 1) chỉ có quyền Quản lý (415).
- [x] 16/11/2026 Cấp trên prod `hrm_power`: INSERT `role_has_permissions` (910,3,1) và (911,3,1). Cần đăng nhập lại để nhận quyền. Vai trò khác muốn vào màn phải cấp thêm ở Vai trò & Quyền.
