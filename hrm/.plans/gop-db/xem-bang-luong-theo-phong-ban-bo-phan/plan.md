# Xem bảng lương theo Phòng ban / Bộ phận (chưa có số Redmine) — @cuong61n

Nguồn: tin nhắn 12/11/2026 trên dev-hrm `/admin/roles/8/permissions`: quyền "Xem bảng lương" chỉ có Không xem / Công ty / Tổng công ty, thiếu Phòng ban + Bộ phận.
Trước đây (quyền cũ) cũng chỉ có 2 quyền "theo tổng công ty / theo công ty" → đây là tính năng MỚI, không phải mất quyền khi chuyển mã.

## Quyết định (giả định, chờ user xác nhận nếu khác)
- Làm cả 2 mức: Phòng ban (2) + Bộ phận (1). Phòng ban/Bộ phận = nơi người xem được gán QUẢN LÝ (cùng ngữ nghĩa HrmScopeContext::departmentIds/partIds).
- Danh sách bảng lương (user chốt 12/11/2026): Phòng ban / Bộ phận thấy MỌI bảng của công ty, kể cả chưa khoá; lọc theo phòng/bộ phận nằm ở dòng nhân viên trong chi tiết. Mã có nhưng không phạm vi (null) giữ luật cũ: đã khoá hoặc do mình tạo.
- Chi tiết bảng lương: Phòng ban → NV có phòng ∈ phòng quản lý HOẶC bộ phận ∈ bộ phận quản lý HOẶC chính mình; Bộ phận → bộ phận ∈ bộ phận quản lý HOẶC chính mình.
- Cột lọc: salary_employees.employee_department_id / employee_part_id (snapshot lúc lập bảng lương).

## Phase 1
### BE
- [x] (12/11/2026) Catalog `payroll.bang_luong.view`: scopes [1,2,3,4] (payroll.php) — FE PermissionTree đọc allowed_scopes từ API nên không phải sửa FE
- [x] (12/11/2026) SalaryService::getSalaryEmployee: thêm nhánh Phòng ban / Bộ phận (dùng HrmScopeContext::departmentIds/partIds + luôn kèm chính mình)
- [x] (12/11/2026) permission:catalog-sync trên DB local → allowed_scopes = [1,2,3,4]. Dev/prod: chạy ~/build_tpe.sh rồi vào /admin/roles cấp lại mức mới
### Test (nhiều tài khoản / nhiều mức)
- [x] (12/11/2026) 21/21 ca đạt (tinker in-process, DB local, transaction rollback, NV 411 công ty 3, bảng lương #667): không quyền / scope NULL / Bộ phận / Phòng ban / Công ty / Tổng công ty — chi tiết + danh sách
- [x] (12/11/2026) Quản lý 1 / nhiều phòng, part_ids có khoảng trắng, phòng + bộ phận cùng lúc, quản lý phòng nhưng mức Bộ phận không lọt phòng, không quản lý gì → chỉ mình
- [x] (12/11/2026) Lọc department_id ngoài quyền → 0 dòng; keyword rác → 0
- [x] (12/11/2026) UI local /admin/roles/10/permissions (Playwright): dropdown 'Xem bảng lương' ra đủ Không xem / Tổng công ty / Công ty / Phòng ban / Bộ phận

### Checkpoint — 2026-11-12
Vừa hoàn thành: sửa Catalog + SalaryService (danh sách thấy cả bảng chưa khoá), test BE 22/22 + UI; đã push develop (commit 4d23bd9b5, 12/11/2026); đang build dev
Bước tiếp theo: vào dev /admin/roles cấp mức mới cho vai trò và thử bằng tài khoản thật
Chưa làm (ngoài phạm vi): export / send_mail / show / báo cáo thu nhập chưa lọc theo mức này
