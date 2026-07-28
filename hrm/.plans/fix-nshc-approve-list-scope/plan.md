# Fix — Màn phê duyệt đơn xin nghỉ: NSHC xem xuyên công ty

## Bối cảnh
- URL: `/timesheet/attendance/approve` → `GET /timesheet/attendance/approve` → `AttendanceController::approve` → `AttendanceService::approve()`.
- Bug: nhánh quyền `NSHC duyệt đơn xin nghỉ` chỉ `orWhere('attendance_status', CHO_NSHC_DUYET)` — KHÔNG bó theo phòng ban/công ty người duyệt → user NSHC (vd Lê Thị Thuỷ Tiên - Tân Phát Sài Gòn) thấy đơn của mọi công ty khác.
- Nghiệp vụ đúng: NSHC chỉ được xem đơn của **phòng ban mình quản lý** (giống nhánh `PD-Đơn xin nghỉ` đã dùng `listManageEmployeeInfoIds`).

## Phase 1 — Fix BE
- [x] `AttendanceService::approve()`: nhánh `NSHC duyệt đơn xin nghỉ` thêm ràng buộc `whereIn('attendances.employee_id', listManageEmployeeInfoIds(false, null, true))` (bó theo công ty hiện tại + phòng ban quản lý), y như nhánh PD.

## Verify
- [x] User NSHC chỉ thấy đơn "Chờ NSHC duyệt" của nhân viên thuộc phòng ban mình quản lý trong công ty hiện tại.
- [x] Không còn thấy đơn của công ty khác.
- [x] Nhánh PD và nhánh else (tự tạo) giữ nguyên hành vi.

## Phase 2 — Rà soát toàn menu "Phê duyệt" module Chấm công (test empirical với tài khoản Lê Thị Thuỷ Tiên, employee_info 542 / account 550, company 4, DB hrm_prod_local)
- [x] Đơn xin nghỉ (AttendanceService::approve) — nhánh NSHC bỏ trống scope → FIX (whereIn employee thuộc quản lý). Test sau fix: chỉ cty4.
- [x] Phiếu yêu cầu làm thêm (OvertimeRequirementService::approve) — bó nhầm theo `department_id` (phòng thực hiện) → lòi 3 phiếu cty1. FIX: thêm `where company_id = current_company_role`. Test sau fix: total=0 (đúng, cty4 không có phiếu).
- [x] Đăng ký làm thêm (OvertimeAssignmentService::approve) — bó theo `employee_id` (employee_info cty4). Chạy method thật: total=991 chỉ cty4. KHÔNG leak (cấu trúc chỉ 2 nhánh an toàn).
- [x] Đăng ký đi muộn về sớm (LateEarlyOutService::approve) — employee scope, test cty4=22. OK.
- [x] Đề nghị tra soát công (RequestUpdateTimeSheetService::approve) — employee scope, test cty4=10293. OK.
- [x] Đơn kết thúc nghỉ phép (AttendancesExtendRequestService::index) — base `where company_id`. Không leak liên công ty (nhánh NSHC rỗng chỉ over-scope trong công ty).
- [x] Đơn kết thúc đăng ký đi muộn về sớm (LateInEarlyOutChangeEndRequestService::index) — base `where company_id`. OK.

## Ngoài scope menu Phê duyệt chấm công (ghi nhận)
- BusinessTripAssignService::approve (phiếu đi công tác) — nhánh "Quản lý phiếu đi công tác" thiếu scope → leak liên công ty. Fix đã bị revert ngoài; nằm ngoài menu Phê duyệt chấm công.
- Decision waiting-approve — user yêu cầu bỏ qua.
