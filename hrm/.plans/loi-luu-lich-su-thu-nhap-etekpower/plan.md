# Lỗi lưu lịch sử thu nhập ETEK POWER (chưa có số Redmine) — @cuong61n

Báo từ nhóm chat 12/11/2026: thêm lịch sử thu nhập cho NV Phạm Thị Hường (employee_info_id 78, ETEK POWER)
báo "lỗi máy chủ" — `POST payroll/employee-salary-histories` trả `{code:500, message:"fail"}`. Người thao tác: tài khoản Lưu Thu Hiền (employees.id 278).

## Điều tra (12/11/2026)
- [x] 12/11 Đọc log prod etekpower: KHÔNG có dòng lỗi nào về lịch sử lương. Nguyên nhân: `EmployeeSalaryHistoryController::store` bắt `\Exception` rồi trả `'fail'` mà không ghi log.
- [x] 12/11 Đối chiếu schema DB `hrm_power`: không thiếu cột nào trong `$fillable`; bảng phụ cấp thiếu created_by/updated_by nhưng BaseModel đã kiểm tra cột nên không phải nguyên nhân.
- [x] 12/11 Tái hiện trên prod trong transaction + ROLLBACK (NV 78 vẫn 2 bản ghi): lưu + phụ cấp + lịch sử hồ sơ + Resource với 5 kịch bản (sao bản ghi 135, đủ 3 phụ cấp, chức vụ mới id 32 + năng lực 58, bằng tài khoản NV 78 và tài khoản 278) → đều THÀNH CÔNG. Chưa tái hiện được, nguyên nhân gốc CHƯA XÁC ĐỊNH.
- [x] 12/11 Loại trừ: thiếu key do PHP 8 (form gửi đủ key), định biên (`checkDinhBien` = true), `current_company_role` (=1).

## Sửa
- [x] 12/11 Thêm `\Log::error` (message, employee_info_id, payload, file:line, trace) vào `catch` của `store` — sửa trên nhánh `tpe` (code etekpower chạy nhánh này), worktree riêng, mới sửa file, CHƯA commit/push/deploy.
- [x] 12/11 Push `0d71295cf` (nhánh `tpe`) + deploy etekpower bằng `~/build_etekpower.sh` (lỡ build cả FE, site gián đoạn vài phút — lần sau chỉ đổi BE thì `git pull` + `php artisan route:cache`, không chạy cả script).
- [x] 12/11 Bắt được lỗi thật qua log: `SQLSTATE 1048 Column 'moving_expenses_according_salary_ratio' cannot be null` — FE gửi null cho 3 cột `moving/telephone/other_allowances_according_salary_ratio` (cột NOT NULL), `store` thiếu bước đưa 3 cờ này về false như các cờ khác.
- [x] 12/11 Sửa `EmployeeSalaryHistoryController::store`: 3 cờ rỗng → false. Mới sửa trong worktree nhánh `tpe`, CHƯA commit/push/deploy (chờ user đồng ý).
- [x] 12/11 Commit + push `cbec78897` (tpe) + `git pull` & `route:cache` trên etekpower, không build FE. Chờ chị Hiền lưu lại để xác nhận.
- [ ] Bản ghi test id 141 (NV 78, 01/08/2026): user tự xoá.

Trạng thái: đã deploy etekpower 12/11, chờ chị Hiền lưu lại xác nhận.
