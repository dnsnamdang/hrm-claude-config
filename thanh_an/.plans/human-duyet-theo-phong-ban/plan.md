# Hành chính nhân sự: chuyển bước duyệt sang phạm vi phòng ban

**Người phụ trách:** @khoipv
**Ngày tạo:** 18/09/2026
**Liên quan:** `.plans/timesheet-duyet-theo-phong-ban/plan.md` (đã làm trước, cùng nguyên tắc)

## Mục tiêu
Áp dụng cho `Modules/Human` cùng nguyên tắc đã chốt ở phân hệ Chấm công:
- Bước DUYỆT giới hạn theo nhân viên thuộc phòng ban mà người duyệt quản lý (`employee_manage_departments`).
- Thông báo "cần duyệt" gửi cho quản lý phòng ban của người tạo đơn (không gửi theo nhóm nghiệp vụ nữa).
- **Quyền XEM giữ nguyên** (theo yêu cầu).

## Khảo sát — khác biệt so với Chấm công
Trong `Modules/Human` KHÔNG có chỗ nào gọi `listManageEmployeeInfoIdsByGroup()` ở điều kiện duyệt.
Chỉ có **1 điểm** dùng cơ chế nhóm nghiệp vụ: notification hồ sơ tự khai.
Các bước duyệt còn lại hiện **không giới hạn phạm vi nhân viên** (chỉ check trạng thái + quyền).

| Luồng duyệt | Hiện trạng | Xử lý |
|---|---|---|
| Hồ sơ tự khai — notification cần duyệt (`EmployeeInfoUpdateRequestController:186`) | `listEmployeeInfoHasPermission(...)` → quản lý **nhóm** | ĐỔI sang quản lý **phòng ban** |
| Hồ sơ tự khai — `can_approve` / `can_reject` (`EmployeeInfoUpdateRequest:224,228`) | chỉ check trạng thái `SendApprove` → ai vào được màn cũng duyệt được | THÊM ràng buộc phòng ban (khớp với người nhận thông báo) |
| Hồ sơ tự khai — danh sách (`EmployeeInfoUpdateRequestService::getEmployeeInfos`) | không lọc phạm vi | GIỮ NGUYÊN (quyền xem) |
| HĐLĐ — `can_approve_manager` (`EmploymentContract:55`) + notification (`EmploymentContractController:161`) | quyền `Duyệt hợp đồng lao động` cấp toàn hệ thống, gửi cho mọi người có quyền | GIỮ NGUYÊN — chờ chốt nghiệp vụ |
| HĐLĐ — `can_approve_employee` (`EmploymentContract:50`) | NV tự ký HĐ của mình | GIỮ NGUYÊN |
| HĐLĐ — danh sách (`EmploymentContractService:57`) | `checkPermissionList` 4 cấp (có nhánh "theo nhóm") | GIỮ NGUYÊN (quyền xem) |
| Thông báo nội bộ — `canApprove()` (`SelfNotifications:79`) | chỉ check quyền `Duyệt thông báo nội bộ` | GIỮ NGUYÊN — thông báo không gắn nhân viên/phòng ban |

## Task

### Phase 1 — Helper
- [x] Thêm cache tĩnh theo `employee_id` cho `listManageEmployeeInfoIdsByDepartment()` (accessor gọi trong vòng lặp danh sách → tránh N+1)

### Phase 2 — Hồ sơ tự khai (BE)
- [x] `EmployeeInfoUpdateRequest::getCanApproveAttribute` — thêm điều kiện nhân viên thuộc phòng ban mình quản lý
- [x] `EmployeeInfoUpdateRequest::getCanRejectAttribute` — tương tự
- [x] `EmployeeInfoUpdateRequestController:186` — `listEmployeeInfoHasPermission` → `listEmployeeInfoManageDepartmentHasPermission`

### Phase 2b — Rà soát phân hệ Bảng lương (`Modules/Payroll`)
- [x] Rà `Modules/Payroll`: KHÔNG có bước duyệt nào dùng nhóm nghiệp vụ (không gọi `listManageEmployeeInfoIdsByGroup` / `listEmployeeInfoHasPermission`), không có điểm gửi notification nào
- [x] `SalaryService.php:359,463,550,617` dùng `listManageEmployeeInfoIds()` — vốn đã theo phòng ban, là quyền XEM bảng lương → giữ nguyên
- [x] `P3SalaryService::approve`, `SalaryAdvanceController::approve` — duyệt theo BẢNG lương (không gắn nhân viên cụ thể), không có phạm vi nhóm/phòng ban → giữ nguyên
- [x] `Payroll/Services/DashboadService.php:236` (dashboard HCNS) — đếm hồ sơ tự khai chờ duyệt toàn hệ thống → lọc theo `listManageEmployeeInfoIdsByDepartment()` cho khớp điều kiện duyệt mới
- [x] `DashboadService.php:241,246` (HĐLĐ, thông báo nội bộ) — giữ nguyên, khớp với quyết định không siết 2 luồng này

### Phase 3 — Kiểm tra
- [x] `php -l` các file sửa
- [x] Đối chiếu kết quả helper cũ/mới bằng tinker

## Ngoại lệ đã thống nhất
- Quyền XEM (danh sách, báo cáo) giữ nguyên toàn bộ.
- Đề nghị thanh toán công tác phí (Chấm công) giữ nguyên.
- Hợp đồng lao động + Thông báo nội bộ: **chưa siết** — đang là quyền cấp hệ thống, cần chốt nghiệp vụ trước.

## Rủi ro
Giống phân hệ Chấm công: dữ liệu `employee_manage_departments` trên staging còn thiếu → sau thay đổi, người không quản lý phòng ban nào sẽ không duyệt được hồ sơ tự khai (trừ người có `all_department = 1`).

## Checkpoint — 18/09/2026
Vừa hoàn thành: Phase 1-3. `php -l` sạch 3 file. Tinker (employee 74, quản lý PB 30,18,40,50,60,70):
- `listManageEmployeeInfoIdsByDepartment()` = 1 NV (employee_info 76), không gồm chính mình
- Hồ sơ tự khai của NV trong phòng ban → `can_approve = true`; NV ngoài phòng ban → `false`
- Notification cần duyệt: theo nhóm = 3 người → theo phòng ban = 2 người
- Dữ liệu staging: `employee_update_requests` không còn hồ sơ nào ở trạng thái chờ duyệt (149 đã duyệt, 2 từ chối) → thay đổi không làm kẹt hồ sơ đang chạy

Đang làm dở: (không)

### Checkpoint bổ sung — 18/09/2026 (rà Bảng lương)
Vừa hoàn thành: rà `Modules/Payroll`, không có bước duyệt theo nhóm nghiệp vụ. Sửa 1 điểm: dashboard HCNS đếm hồ sơ tự khai chờ duyệt (`Payroll/Services/DashboadService.php:236`) → lọc theo phòng ban quản lý. `php -l` sạch.
Bước tiếp theo: bổ sung `employee_manage_departments` rồi test UI màn Danh sách hồ sơ tự khai; chốt nghiệp vụ Hợp đồng lao động + Thông báo nội bộ có siết theo phòng ban không.
Blocked: (không)

### Checkpoint — 18/09/2026 (wrap up)
Vừa hoàn thành: viết tài liệu wrap up lần đầu của feature — `.plans/human-duyet-theo-phong-ban/design.md` (tóm tắt) và `docs/superpowers/specs/2026-09-18-human-duyet-theo-phong-ban-design.md` (spec đầy đủ: bối cảnh, quy tắc nghiệp vụ, từng file/dòng đã sửa kèm snippet, kết quả test, phần giữ nguyên có chủ đích). Đã bổ sung link design + spec vào `STATUS.md`.
Đang làm dở: (không)
Bước tiếp theo: Test UI màn Danh sách hồ sơ tự khai + dashboard HCNS sau khi có dữ liệu quản lý phòng ban; chốt nghiệp vụ Hợp đồng lao động + Thông báo nội bộ có siết theo phòng ban không.
Blocked: (không)
