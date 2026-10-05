# Plan — Chấm công: chuyển bước duyệt từ nhóm nghiệp vụ sang phòng ban

**Người phụ trách:** @khoipv
**Ngày tạo:** 18/09/2026

## Mục tiêu
Trong phân hệ Chấm công (`Modules/Timesheet`), mọi bước DUYỆT đang xác định phạm vi bằng
`listManageEmployeeInfoIdsByGroup()` / `listManageEmployeeIdsByGroup()` (nhóm nghiệp vụ)
→ đổi sang **nhân viên thuộc các phòng ban mà người duyệt quản lý** (`employee_manage_departments`).

## Quyết định đã chốt với user
- Phạm vi: **A (điều kiện duyệt) + B (tab Chờ duyệt) + E (dashboard đếm)**. Tầng C (danh sách chính, nhánh `is_group` của permission "…theo nhóm") **GIỮ NGUYÊN** — đó là quyền xem, không phải duyệt.
- Nguồn phòng ban: `employee_manage_departments` (có tính cờ `employees.all_department = 1`).
- Notification "cần duyệt": lấy **danh sách người quản lý phòng ban của người tạo đơn** rồi gửi `sendToAllNotification`. Viết **helper mới**, KHÔNG sửa `listEmployeeInfoHasPermission()` cũ (Category đang dùng).
- Không tự duyệt đơn của chính mình; chỉ nhân viên đang làm việc (status active).
- Phần dashboard đếm báo giá / gói thầu / hợp đồng (module Category) trong `DashboadService` → GIỮ NGUYÊN theo nhóm.
- **Đề nghị thanh toán công tác phí → GIỮ NGUYÊN toàn bộ theo nhóm** (user chốt 18/09/2026): không đụng `RequestPaymentWorkingFee`, `RequestPaymentWorkingFreeService`, và dòng đếm công tác phí trên dashboard.

## Phase 1 — Helper dùng chung (BE)
- [x] `listManageEmployeeInfoIdsByDepartment()` — trả `employee_infos.id` của NV active thuộc phòng ban mình quản lý, **loại trừ chính mình**
- [x] `listManageEmployeeIdsByDepartment()` — bản trả `employees.id` (cho các bảng lưu `created_by` là employee id)
- [x] `listEmployeeInfoManageDepartmentHasPermission($permission, $employee_info_id)` — tìm người quản lý phòng ban của người tạo đơn + có quyền duyệt, trả `employee_infos.id` để gửi notification

## Phase 2 — Tầng A: điều kiện duyệt (accessor trong Entities)
- [x] `Attendance.php:149,154,161` — đơn xin nghỉ (can_approve / can_reject / canCancel)
- [x] `AttendancesExtendRequest.php:95,99` — gia hạn đơn nghỉ
- [x] `LateEarlyOut.php:277,282` — đi muộn về sớm
- [x] `OvertimeAssignment.php:223,229` — đăng ký tăng ca
- [x] `RequestUpdateTimeSheet.php:168,174` — đề nghị tra soát công
- [x] `BusinessTripAssign.php:279,294` — phiếu công tác
- [x] `JobAssignmentNote.php:176` — phiếu giao việc

## Phase 3 — Tầng B: tab "Chờ duyệt" (query trong Services)
- [x] `AttendanceService.php:67`
- [x] `AttendancesExtendRequestService.php:27`
- [x] `LateEarlyOutService.php:53`
- [x] `OvertimeAssignmentService.php:57`
- [x] `RequestUpdateTimeSheetService.php:80`
- [x] `BusinessTripAssignService.php:305` (listFinishExtend)

## Phase 4 — Tầng E: dashboard đếm việc chờ duyệt
- [x] `DashboadService.php:248` — đơn xin nghỉ
- [x] `DashboadService.php:257` — đi muộn về sớm
- [x] `DashboadService.php:264` — tra soát công
- [x] `DashboadService.php:273` — tăng ca
- [x] `DashboadService.php:278` — duyệt kết quả phiếu công tác (lưu ý bug sẵn có: `where('created_by', <array>)` thiếu `whereIn`)
- [x] `DashboadService.php:288` — phiếu giao việc

## Phase 5 — Tầng D: notification "cần duyệt"
- [x] `AttendanceService.php:219`
- [x] `AttendancesExtendRequestService.php:81`
- [x] `LateEarlyOutService.php:235`
- [x] `RequestUpdateTimeSheetController.php:123` (gui đơn) — **GIỮ NGUYÊN dòng 157 (`XN-Đề nghị tra soát công`) và 168**: ở 2 chỗ này `auth()` là người vừa duyệt chứ không phải người tạo đơn, đổi sang phòng ban sẽ gửi nhầm cho quản lý phòng ban của người duyệt
- [x] `OvertimeAssignmentController.php:297`
- [x] `OvertimeRequirementController.php:136`
- [x] `BusinessTripAssignController.php:276,312,335`
- [x] `JobAssignmentNoteController.php:202,249`
- [x] Giữ nguyên các chỗ KHÔNG truyền employee_info_id (BGĐ duyệt đơn nghỉ, PD-Thiết bị chấm công) — vốn đã gửi toàn hệ thống
- [x] Giữ nguyên notification của công tác phí

## Phase 6 — Verify
- [x] `php -l` toàn bộ file đã sửa
- [x] Rà lại: không còn `…ByGroup()` nào trong luồng duyệt của Timesheet
- [x] Đối chiếu dữ liệu DB: user có phòng ban quản lý → đếm số đơn thấy được trước/sau

## Checkpoint — 18/09/2026

Vừa hoàn thành: Toàn bộ Phase 1-6. 3 helper mới trong `app/Helper/PermissionHelper.php`; 7 entity đổi accessor duyệt; 6 service đổi query tab chờ duyệt; 6 dòng dashboard; 11 điểm notification. `php -l` sạch toàn bộ, chạy thử helper bằng tinker OK.

Đang làm dở: (không)

Bước tiếp theo: **User bổ sung dữ liệu `employee_manage_departments`** rồi test lại trên giao diện.

Blocked: **Dữ liệu staging chưa sẵn sàng** — 43 phòng ban có gán quản lý, 24 phòng ban có NV đang làm việc, nhưng chỉ **2 phòng ban vừa có quản lý vừa có NV**. Hiện có 1503 đơn nghỉ chờ duyệt; sau thay đổi hầu hết sẽ không ai duyệt được cho tới khi gán đủ quản lý phòng ban. So sánh: 27 người đang làm quản lý nhóm, chỉ 9 người được gán quản lý phòng ban.

## Ngoại lệ đã thống nhất (không đổi)
- Đề nghị thanh toán công tác phí — toàn bộ giữ theo nhóm
- Tầng C (quyền xem, nhánh permission "…theo nhóm"): `AttendanceService:44`, `LateEarlyOutService:34`, `OvertimeAssignmentService:38`, `RequestUpdateTimeSheetService:50`, `BusinessTripAssignService:142`, `JobAssignmentNoteService:100`, `TimekeeperService:39`, `ReportService:129,675`, `TimesheetSummaryController:57`
- Dashboard phần Dự án (báo giá `:298`, gói thầu `:311`) và công tác phí (`:283`)
- Notification không truyền employee_info_id (BGĐ duyệt đơn nghỉ, PD-Thiết bị chấm công) — vốn gửi toàn hệ thống

### Checkpoint — 18/09/2026 (wrap up)
Vừa hoàn thành: viết tài liệu wrap up lần đầu của feature — `.plans/timesheet-duyet-theo-phong-ban/design.md` (tóm tắt) và `docs/superpowers/specs/2026-09-18-timesheet-duyet-theo-phong-ban-design.md` (spec đầy đủ: bối cảnh, quy tắc nghiệp vụ, từng file/dòng đã sửa kèm snippet, kết quả test, phần giữ nguyên có chủ đích). Đã bổ sung link design + spec vào `STATUS.md`.
Đang làm dở: (không)
Bước tiếp theo: User bổ sung dữ liệu `employee_manage_departments` rồi test UI phân hệ Chấm công (tab Chờ duyệt + dashboard).
Blocked: (không)
