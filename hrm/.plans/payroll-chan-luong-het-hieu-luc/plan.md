# Plan — Chặn thêm nhân sự lương hết hiệu lực

## Phase 1 — Backend

### BE
- [x] Thêm helper `getBlockedSalaryEmployeeIds($salary, $candidateIds)` trong `SalaryService` — trả về id nhân sự có latest-record hết hiệu lực (`end_date < apply_date`)
- [x] `EmployeeInfoService::query` nhánh `salary_id`: gọi helper, thêm `whereNotIn('employee_infos.id', $blockedIds)` để ẩn khỏi modal
- [x] Thêm `assertEmployeesSalaryEffective($salaryId, $employeeIds)` trong `SalaryService` — throw `ValidationException` nếu có nhân sự hết hiệu lực
- [x] `SalaryController::saveEmployee`: gọi assert trước khi đổi `status = 3` và dispatch job (đặt ngoài try để không nuốt ValidationException)
- [x] Test tay (Playwright + API) trên salary 641 (apply_date 2026-06-01): end_date rỗng → hiện/thêm được; end_date<apply → ẩn khỏi modal + API 422; đã khôi phục data test

### FE
- [x] Không đổi (danh sách BE đã lọc)

## Checkpoint
### Checkpoint — 2026-07-01
Vừa hoàn thành: 3 thay đổi BE (helper + ẩn modal + assert khi lưu), `php -l` sạch cả 3 file
Đang làm dở: chưa có
Bước tiếp theo: test tay trên UI màn /payroll/salary/{id} với 4 trường hợp end_date
Blocked:
