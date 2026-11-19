# Vá lỗ hổng quyền đọc (Công việc · Chấm công · Lương) — GHI LẠI, LÀM SAU

> Phát hiện 11/11/2026 khi rà code cho TPE SMART AGENT (spec `docs/superpowers/specs/agent-chat/2026-11-11-tpe-smart-agent-design.md` §11).
> User 11/11: *"ok, vá lỗi sau (ghi lại)"* ⇒ đợt riêng, chưa có lệnh code. Nên xong trước khi đưa Agent lên prod TPE.
> Chỉ cổng TPE trước (cổng khác cập nhật sau).

| # | Chỗ | Lỗi | Đã kiểm bằng |
|---|---|---|---|
| 1 | `GET v1/payroll/employee-salary-histories` (+ `/report`, `/{id}`) → `Modules/Payroll/Services/EmployeeSalaryHistoryService.php:31` | Lấy `employee_info_id` từ request, không kiểm quyền ⇒ ai đăng nhập cũng xem lịch sử lương người khác | Đọc code (route chỉ `auth:api`); chưa gọi thử có token |
| 2 | `v1/timesheet/reports/*` (`Modules/Timesheet/Routes/api.php:373`) | Nhóm route KHÔNG có `auth:api` | Gọi local không token: 7 route 500 (vô tình chặn), `business_trip_assign_report_` trả 200 — **chưa kiểm xong** mức lộ khi truyền tham số |
| 3 | `AttendanceController::getTotalLeaveDay` (`Modules/Timesheet/Http/Controllers/Api/V1/AttendanceController.php:309`) | Dùng `employee_id` từ request, không kiểm quyền ⇒ xem số ngày phép người khác | Đọc code |
| 4 | `SalaryService::employeeShow` (`Modules/Payroll/Services/SalaryService.php:1239`) | Không kiểm bảng lương đã chốt (status 2) ⇒ đọc phiếu lương nháp của mình; không có tên trong bảng ⇒ 500 | Đọc code |
| 5 | `TimesheetMonthSummaryService::employeeShow` (:43) | Như #4 với bảng tổng hợp công | Theo báo cáo rà code, chưa tự đọc lại |
| 6 | `TaskController::show` (`Modules/Assign/Http/Controllers/Api/V1/TaskController.php:156`) | Không kiểm quyền xem nhiệm vụ (đã có trong plan Phân hệ Công việc GĐ1) | Đọc code + route + không global scope/policy. **Tái hiện 11/11**: NV 39 (danh sách task 0 bản ghi) gọi `GET assign/tasks/532` ⇒ 200 trả mã + tiêu đề |
| 7 | `DashboadService::hcns` (nhận `company_id`), `SalaryService::show`, `TimesheetSummaryService::detail` (nhận `employee_info_id`), phần lớn mã `payroll.*.view` không kiểm ở BE | Thiếu kiểm quyền | Theo báo cáo rà code, chưa tự đọc lại từng chỗ |
| 8 | `GET v1/timesheet/dashboad/hcns` → `DashboadService::hcns` + `listManageEmployeeInfoIds()` (`TimesheetService:181`) | Không kiểm mã quyền; NV không có mã chấm công nào (vd local NV 1345) vẫn được coi là "quản lý tất cả phòng" ⇒ xem số đi làm/vắng cả công ty | Đọc code + tinker (agent Task 6c, 11/11); chưa gọi API bằng token |
| 9 | Nhóm route `v1/timesheet/reports/*` (`Modules/Timesheet/Routes/api.php:373`: timekeeper_report, attendance_report, overtime_report, payroll_info…) | Không gắn `auth:api` | Đọc route (11/11). Gọi `attendance_report` không token ⇒ HTTP 500 (chưa kiểm có lộ dữ liệu ở endpoint khác không) |
| 10 | `ReportService::timekeeper_report` (`Modules/Timesheet/Services/ReportService.php:64`) | `from`/`to` từ request ghép thẳng vào SQL thô (`DB::raw … BETWEEN '$from' AND '$to'`) ⇒ nguy cơ SQL injection, cộng thêm việc route không cần đăng nhập (#9) | Đọc code (11/11) |
| 11 | `AttendanceController::getTotalLeaveDay` (`GET v1/timesheet/attendance/get-total-leave-day`) | Nhận `employee_id` bất kỳ, không kiểm quyền ⇒ xem số phép người khác | Theo báo cáo rà code 11/11, chưa tự đọc lại |
| 12 | `TimeWorkingController::index` (`GET v1/timesheet/timeworking/list`) | Không kiểm `timesheet.du_lieu_cham_cong.view`; `department_id` thay hẳn query nên mất lọc công ty | Theo báo cáo rà code 11/11, chưa tự đọc lại |
| 13 | `TimesheetMonthSummaryService::index` (không scope) + `show` (`:161-163` keyword `orWhere` không gom nhóm ⇒ thoát điều kiện phạm vi) | Lộ danh sách / dòng bảng công tổng hợp ngoài phạm vi | Theo báo cáo rà code 11/11, chưa tự đọc lại |
| 14 | `AssignBusinessService::searchByFilter` (`:77-202`) | Không truyền `type` (khác all/waiting/…) ⇒ không áp phạm vi quyền | Đọc code dòng 77-90 (11/11); chưa gọi API |
| 15 | `SolutionService::getAll` (`:248-362`), `show` (`:364-388`), endpoint `v1/assign/solutions/{solution}/manager/*` | Không kiểm quyền xem giải pháp (chỉ middleware chặn thành viên bị khoá); `getAll` truyền `sort_field`/`sort_dir` thẳng vào `orderBy` | Theo báo cáo rà code 11/11, chưa tự đọc lại |
| 16 | `ProspectiveProjectController::show` (`:185`) | Không kiểm quyền xem dự án TKT (chỉ route-model binding) — `visibleIdsQuery()` có sẵn nhưng không dùng ở show | Theo báo cáo rà code 11/11, chưa tự đọc lại |
| 17 | `IssueController::show` (`Modules/Assign/Http/Controllers/Api/V1/IssueController.php:78`), route `GET v1/assign/issues/{issue}` (`Modules/Assign/Routes/api.php:1210`) | Không kiểm quyền xem vấn đề (route không middleware, chỉ route-model binding, `Issue` không global scope) ⇒ ai đăng nhập cũng đọc trọn chi tiết vấn đề người khác (cả lịch sử, người theo dõi, tệp) | **Đã tái hiện 11/11**: NV 39 (danh sách vấn đề 0 bản ghi) gọi `GET assign/issues/345` (vấn đề tạm do NV 13 tạo) ⇒ 200 trả đủ mã + tiêu đề; đã xoá vấn đề tạm |
| 18 | `HandoverService::index` (`Modules/Assign/Services/HandoverService.php:62`) + `show` (`:736`), route `GET v1/assign/handovers` + `/{handover}` | Danh sách phiếu bàn giao không lọc quyền (chỉ ẩn nháp người khác), chi tiết không kiểm ⇒ ai cũng thấy mọi phiếu + tiêu đề task/vấn đề trong phiếu | Đọc code 11/11, CHƯA gọi thử (DB local không có phiếu). User chốt 11/11: vá đợt sau, không gộp vào #6/#17 |
| 19 | `AssignBusinessController::show` (`Modules/Assign/Http/Controllers/Api/V1/AssignBusinessController.php:100`), route `GET v1/assign/assign_business/{id}` (`Routes/api.php:1341`) | Không kiểm quyền xem phiếu công tác (không middleware, `getDetail` không xét phạm vi `assign.danh_sach_phieu_giao_cong_tac.view`) | Đọc code 11/11 (khảo sát Agent phiếu công tác), CHƯA gọi thử |
| 20 | `AssignJobController::show` (`AssignJobController.php:74`), route `GET v1/assign/assign_jobs/{id}` (`Routes/api.php:1504`) | Không kiểm quyền xem phiếu giao việc; `catch` gọi `dd($exception)` ⇒ dump lỗi ra response | Đọc code 11/11, CHƯA gọi thử |

Phương án chi tiết #6 + #17 (chờ duyệt): `phuong-an-6-17-xem-task-issue.md` — kèm ứng viên #18 `HandoverService::show` không kiểm quyền (chưa gọi thử, DB local không có phiếu).

Khi vá #6 / #17: điều kiện xem mới PHẢI bao trọn phạm vi mà Agent đang trả (`TaskService::index` / `IssueService::index` + việc của tôi ở `MyTodoService`), nếu không panel mở từ `/agent` sẽ ra trống (đã kiểm 11/11: meeting không lệch — `MeetingCriteria` ⊆ `Meeting::canView`).

Trước khi vá: kiểm lại từng dòng tới gốc (CLAUDE.md "Kiểm code tới tận gốc"), tái hiện bằng gọi API có token trên DB local, viết test có quyền / không quyền.
