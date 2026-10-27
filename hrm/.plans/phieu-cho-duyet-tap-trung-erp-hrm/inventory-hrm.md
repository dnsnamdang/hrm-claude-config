# Kiểm kê luồng duyệt (phiếu chờ duyệt) — HRM

> Đầu vào cho feature **Phiếu chờ duyệt tập trung ERP + HRM**. File song song: `inventory-erp.md` (phía ERP).
> Ngày kiểm: 22/10/2026 · Nguồn code: `HRM/hrm-api` + `HRM/hrm-client`, nhánh `gop_db` (working tree) · DB: `hrm_erp_21_10_prod` (dump prod 21/10/2026, DB gộp ERP + HRM).
> **Chỉ đọc**: không sửa source, chỉ chạy SELECT. Mọi số đếm lấy từ SELECT thật, mọi route có `file:dòng`.

## Cách đọc

- **STT có tiền tố theo phần**: `H` = Timesheet/Human/Payroll/Meeting/Training · `QĐ` = Decision · `AS` = Assign · `F` = Finance · `C` = CustomerCare · `M` = MasterData.
- **[ERP]** ở tên luồng = luồng thao tác trên **bảng do ERP sở hữu** (migration nằm trong `ERP/TanPhatDev`). Các luồng này **trùng phạm vi với `inventory-erp.md`**: cùng một phiếu có thể đang được duyệt ở cả 2 hệ thống.
- "Số phiếu đang chờ" đã tách theo từng cấp. Không bảng nào trong phạm vi có `deleted_at`, trừ `decisions` (đã loại bản xoá mềm), nên phần còn lại đếm thẳng theo cột trạng thái.
- Cột **"Màn chờ duyệt riêng"** ghi trang client đang có, kèm API mà trang đó gọi.

## Các kiểu chốt quyền trong HRM (áp dụng cho mọi phần)

| Ký hiệu | Cơ chế | Lọc theo công ty (`role_has_permissions.company_id`)? | Thấy role `model_type = App\Employee`? | Super admin (role 18) vượt quyền? |
|---|---|---|---|---|
| **MW** | middleware `checkPermission:X\|Y` (`app/Http/Middleware/CheckPermission.php`), spatie `getAllPermissions()` trên `Modules\Timesheet\Entities\Employee` | Không | **Không** (sót) | Không |
| **H / HLP** | helper `isCurrentEmployeeHasPermission()` (`app/Helper/PermissionHelper.php:20`) / `PermissionService` | Có | **Không** (sót) | Không |
| **BM** | `BaseModel::isCurrentEmployeeHasPermission()` (`app/Models/BaseModel.php:204`), spatie | Không | **Không** (sót) | Không |
| **CEP** | trait `Modules/Finance/Entities/Concerns/ChecksEmployeePermission`, query thẳng 3 bảng theo TÊN quyền | **Không** | Có | **Có**, ở khoảng 20 luồng |
| **WRP** | `Modules/CustomerCare/Support/WarrantyRepairPermission::has()`, spatie | Không | **Không** (sót) | Không |
| `dueConfig:X,manager` / `checkDueConfigsManager:X` | Chỉ chặn trưởng phòng đang có hàng quá hạn. **Không phải chốt quyền.** | — | — | — |

- **Khe `model_type`**: `employee_has_roles` có **1.355 dòng `App\Employee`** và chỉ **502 dòng `Modules\Timesheet\Entities\Employee`**. Mọi cơ chế spatie (MW/H/BM/WRP) đều không thấy 1.355 dòng này.
  - Phần 1 (Timesheet…Training) và Decision **không bị ảnh hưởng**: mọi role đang giữ quyền duyệt ở đây đều mang model_type HRM.
  - Bị ảnh hưởng nặng ở **CustomerCare** (0 người qua được), **MasterData** (chỉ 9–26 người trên 26–105 người giữ quyền qua được), **F21** và **F25** (xem Phần 4).
- Rất nhiều luồng **không chốt quyền ở BE** (fail-open): FE ẩn nút, nhưng gọi thẳng API vẫn duyệt được. Các luồng này được đánh dấu "BE không chốt" trong từng bảng.
- Tab **"Chờ duyệt" ở `pages/assign/my-job`** là dữ liệu gán cứng: `my-job/index.vue:142` khai `badge: '4'`, còn `:148` và `:336` gán `approvals = []`, không gọi API nào. HRM **chưa có màn chờ duyệt tập trung nào chạy thật**.


---

## Phần 1 — Timesheet · Human · Payroll · Meeting · Training · Rice

- Nguồn: `HRM/hrm-api` + `HRM/hrm-client` nhánh `gop_db` (working tree), DB `hrm_erp_21_10_prod` (dump prod 21/10/2026). Chỉ đọc, chỉ SELECT.
- Mọi số đếm lấy từ SELECT thật chạy ngày 22/10/2026. Không bảng nào trong phạm vi có cột `deleted_at` (đã kiểm `information_schema`), nên không phải loại bản ghi xoá mềm.
- "Bảng thuộc ERP?": đã grep tên bảng (có nháy) trong `ERP/TanPhatDev/{app,Modules,routes,database}` và tìm class model trùng tên → **không bảng nào trong phần A được ERP dùng** (đối chứng: `products` grep ra kết quả, nên script chạy đúng).
- Các đường dẫn route dưới đây có tiền tố `/api/v1/...` (RouteServiceProvider module gắn `api` + nhóm `/v1`).

**Phát hiện chung về khe `model_type`:** trong phạm vi này **không có luồng nào gắn `checkPermission`** ở route duyệt. Mọi chốt quyền đều đi qua `isCurrentEmployeeHasPermission()` (`app/Helper/PermissionHelper.php:20`, lọc theo `role_has_permissions.company_id`) hoặc `BaseModel::isCurrentEmployeeHasPermission()` (`app/Models/BaseModel.php:204`, `getAllPermissions()` **không** lọc công ty). Cả hai đều đọc vai trò qua `Modules\Timesheet\Entities\Employee`. Đã đếm: mọi dòng `employee_has_roles` của các vai trò đang giữ các quyền duyệt trong phần A đều có `model_type = Modules\Timesheet\Entities\Employee`, **0 dòng `App\Employee`**, nên khe model_type **không làm sót người duyệt nào trong phần A**.

---

### Module Timesheet

| STT | Tên luồng | Bảng · Entity | Trạng thái chờ (giá trị · hằng số) | Ai duyệt từng cấp (chốt thật ở BE) | API duyệt/từ chối | URL chi tiết (client) | Màn "chờ duyệt" riêng | Đang chờ trên DB | Phiếu chờ mới nhất | ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | Đơn xin nghỉ (2 cấp) | `attendances` · `Modules\Timesheet\Entities\Attendance` | `attendance_status`: C1 = 1 `AttendanceStatus::SendApprove` ("Gửi TP duyệt") · C2 = 4 `AttendanceStatus::CHO_NSHC_DUYET` (chỉ khi `leave_types.need_nshc_approve`) | C1: quyền `PD-Đơn xin nghỉ` + nhân viên thuộc phòng mình quản lý (`ApproveScope::managesEmployee`) + còn hạn (tới ngày 05 của tháng sau ngày nghỉ) · C2: quyền `NSHC duyệt đơn xin nghỉ` + phòng mình quản lý. Chốt trong FormRequest `AttendanceApproveRequest::authorize()` → `can_approve`/`can_reject` (`Entities/Attendance.php:142-159`); `nshcApprove` dùng `canNSHCApprove()` (`:219`) | POST `/v1/timesheet/attendance/approve` (`Modules/Timesheet/Routes/api.php:209`) — body `attendance_status` 2/3 hoặc approve/reject · POST `/v1/timesheet/attendance/{id}/nshc-approve` (`:210`) | `/timesheet/attendance/:id/approve` | Có: `/timesheet/attendance/approve` → GET `timesheet/attendance/approve` (`:205`, lọc C1 theo PD, C2 theo NSHC, kèm phòng quản lý) | **33** (C1 = 29 · C2 = 4); 17 phiếu tạo trước 21/09 | 2026-10-21 19:33:09 | Không | Route chỉ gắn `checkDueConfigsManager` (không phải chốt quyền). Menu "Phê duyệt › Đơn xin nghỉ" chỉ hiện với `PD-Đơn xin nghỉ` → người **chỉ có** quyền NSHC không thấy menu. `can_reject` không cho NSHC từ chối nếu thiếu quyền PD. |
| H2 | Đơn kết thúc nghỉ phép sớm | `attendances_extend_requests` · `AttendancesExtendRequest` | `status` = 1 (`AttendanceStatus::SendApprove`) | FE: `can_approve` = `PD-Đơn xin nghỉ` (`Entities/AttendancesExtendRequest.php:94`). **BE không chốt**: duyệt đi chung endpoint `store` truyền `status` | POST `/v1/timesheet/attendances-extend-requests/{id}` (`api.php:494`) | (duyệt ngay trong danh sách) | Có: `/timesheet/attendance/attendances-extend-request` → GET `timesheet/attendances-extend-requests` (`:491`) | **1** | 2025-01-24 13:24:44 | Không | Không có FormRequest authorize/không kiểm quyền → ai đăng nhập cũng đổi được trạng thái. Entity `use SoftDeletes` nhưng bảng không có `deleted_at`. |
| H3 | Đăng ký đi muộn về sớm | `late_early_outs` · `LateEarlyOut` | `late_early_out_status` = 1 (`LateEarlyOutStatus::SendApprove`) | `PD-Đăng ký đi muộn về sớm` + phòng mình quản lý; chốt qua `LateEarlyOutApproveRequest` (trait `AuthorizesApproveAction`) → `can_approve` (`Entities/LateEarlyOut.php:282`) | POST `/v1/timesheet/late-in-early-out/approve` (`api.php:192`) | `/timesheet/late-in-early-out/:id/approve` | Có: `/timesheet/late-in-early-out/approve` → GET `.../late-in-early-out/approve` (`:191`) | **28** (cả 28 tạo trước 21/09) | 2026-07-09 17:25:08 | Không | Phiếu chờ đều cũ ≥ 3 tháng → nghi tồn đọng. |
| H4 | Đơn kết thúc sớm đăng ký đi muộn về sớm | `late_in_early_out_change_end_requests` · `LateInEarlyOutChangeEndRequest` | `status` = 1 (`CHO_DUYET`) | FE: `PD-Đăng ký đi muộn về sớm` (`Entities/LateInEarlyOutChangeEndRequest.php:101`). **BE không chốt** (endpoint store) | POST `/v1/timesheet/late-in-early-out-change-end-requests/{id}` (`api.php:503`) | (duyệt ngay trong danh sách) | Có: `/timesheet/late-in-early-out/change-end-request` → GET `.../late-in-early-out-change-end-requests` (`:500`) | **0** (bảng rỗng) | — | Không | Không kiểm quyền. Bảng chưa từng có dữ liệu trên prod. |
| H5 | Phiếu yêu cầu làm thêm | `overtime_requirements` · `OvertimeRequirement` | `overtime_requirement_status` = 1 (`OvertimeRequirementStatus::SendApprove`) | `PD-Phiếu yêu cầu làm thêm` + phòng của phiếu thuộc phòng mình quản lý (`managesDepartment`) + chưa qua ngày bắt đầu; chốt qua `OvertimeRequirementApproveRequest` (`Entities/OvertimeRequirement.php:166-185`) | POST `/v1/timesheet/overtime-requirement/approve` (`api.php:238`) | `/timesheet/overtime-requirement/:id/approve` | Có: `/timesheet/overtime-requirement/approve` → GET `.../overtime-requirement/approve` (`:236`) | **131** (127 tạo trước 21/09) | 2026-10-19 15:48:57 | Không | `can_approve` yêu cầu ngày bắt đầu ≥ hôm nay → phần lớn 131 phiếu cũ **không còn duyệt được nữa** (kẹt vĩnh viễn ở trạng thái chờ). |
| H6 | Đăng ký (phân công) làm thêm | `overtime_assignments` · `OvertimeAssignment` | `overtime_assignment_status` = 1 (`OvertimeAssignmentStatus::SendApprove`) | `PD-Đăng ký làm thêm` + (loại phân bổ → phòng quản lý, loại thường → nhân viên quản lý) + chưa qua ngày bắt đầu; chốt qua `OvertimeAssignmentApproveRequest` (`Entities/OvertimeAssignment.php:252-279`) | POST `/v1/timesheet/overtime-assignment/approve` (`api.php:250`) | `/timesheet/overtime-assignment/:id/approve` | Có: `/timesheet/overtime-assignment/approve` → GET `.../overtime-assignment/approve` (`:247`) | **212** (203 tạo trước 21/09) | 2026-10-16 18:09:12 | Không | Như dòng 5: hết hạn ngày bắt đầu thì không duyệt được → tồn đọng. |
| H7 | Đề nghị tra soát công (2 cấp) | `request_update_timesheet` · `RequestUpdateTimeSheet` | `status`: C1 = 1 `RequestUpdateTimeSheetStatus::SendApprove` · C2 = 4 `TpApproved` ("Chờ NSHC duyệt") | C1: `XN-Đề nghị tra soát công` · C2: `PD-Đề nghị tra soát công`; cả 2 cấp thêm: `company_id` của phiếu = công ty đang làm + nhân viên thuộc phòng quản lý. Chốt qua `RequestUpdateTimeSheetApproveRequest` (`Entities/RequestUpdateTimeSheet.php:173-187`) | POST `/v1/timesheet/request-update-working/storeApprove` (`api.php:156`) | `/timesheet/request-update-working/:id/approve` | Có: `/timesheet/request-update-working/approve` → GET `.../request-update-working/approve` (`:155`) | **54** (C1 = 41 · C2 = 13) | 2026-10-21 20:07:18 | Không | Tên quyền ngược nghĩa thường gặp: cấp 1 dùng "XN", cấp 2 dùng "PD". Từ chối ở C1 → 5 `TpRejected`. |
| H8 | Phiếu giao việc (phân hệ chấm công) | `job_assignment_notes` · `JobAssignmentNote` | `status` = 1 (`JobAssignmentNoteStatus::SendApprove`) | FE: cờ `getCanApprove` = `Quản lý phiếu giao việc` (`Entities/JobAssignmentNote.php:149`). **BE không chốt**: `JobAssignmentNoteApproveRequest::authorize()` trả `true` | POST `/v1/timesheet/job-assignment/approve` (`api.php:180`) | `/timesheet/jobassignment/:id/approve` | Trang `/timesheet/jobassignment/approve` có nhưng **không nằm trong menu**; GET `.../job-assignment/approve` (`:179`) lại trả phiếu **mình được giao**, không phải phiếu chờ mình duyệt | **521** (503 tạo trước 21/09) | 2026-10-21 18:29:44 | Không | ⚠ Nhóm route khai `' middleware' => 'auth:api'` (thừa dấu cách, `api.php:176`) → **cả nhóm job-assignment không có `auth:api`**. Đây là luồng tồn nhiều nhất của Timesheet. |
| H9 | Phiếu đi công tác (phân hệ chấm công) | `business_trip_assigns` · `BusinessTripAssign` | `status` = 1 (`BusinessTripAssignStatus::SendApprove`) | FE: `can_approve` = `Quản lý phiếu đi công tác` (`Entities/BusinessTripAssign.php:195`). **BE không chốt**: `BusinessTripAssignApproveRequest::authorize()` trả `true` | POST `/v1/timesheet/business_trip_assigns/approve` (`api.php:266`) | `/timesheet/business_trip_assigns/:id/approve` | Trang `/timesheet/business_trip_assigns/approve` có nhưng không nằm trong menu; GET `.../approve` (`:265`) | **225** (214 tạo trước 21/09) | 2026-10-21 12:03:08 | Không | Lỗi lọc ở `BusinessTripAssignService::approve()` (`Services/BusinessTripAssignService.php:441-445`): `$query->where('created_by',…)` không gán lại → người **không** có quyền vẫn thấy toàn bộ phiếu. |
| H10 | Yêu cầu kết thúc sớm / gia hạn công tác | `business_trip_employee_requests` · `BusinessTripEmployeeRequest` | `status` = 1; `type` 1 = kết thúc sớm, 2 = gia hạn | Người nhận thông báo = `Quản lý phiếu đi công tác`; menu gate `Quản lý phiếu đi công tác`. **BE không chốt** (`finishExtendApprove`, `Controllers/Api/V1/BusinessTripAssignController.php:432`) | POST `/v1/timesheet/business_trip_assigns/listFinishExtend/{id}` (`api.php:275`) | (duyệt ngay trong danh sách) | Có: `/timesheet/business_trip_assigns/finish-extend` → GET `.../listFinishExtend` (`:268`, chỉ lọc công ty đang làm) | **57** (kết thúc sớm 52 · gia hạn 5) | 2026-09-24 08:07:58 | Không | Quyền `Gia hạn, kết thúc sớm phiếu công tác` chỉ chốt đường **quản lý tạo hộ** (`manager/finish`, `manager/extend`), không chốt đường duyệt. |
| H11 | Thiết bị chấm công (đăng ký máy) | `devices` · `Device` | `status` = 1 (`DeviceStatus::SendApprove`) | Menu gate `PD-Thiết bị chấm công`. **BE không chốt** (`DeviceService::approve`, `Services/DeviceService.php:83`) | POST `/v1/timesheet/devices/approve/{id}` (`api.php:469`) | (duyệt ngay trong danh sách) | Có: `/timesheet/devices` → GET `timesheet/devices` (`:471`) | **11** (10 tạo trước 21/09) | 2026-09-25 07:57:36 | Không | Duyệt máy mới thì tự đổi máy đã duyệt trước đó sang 4 `Exprired`. |

- Route `/timesheet/job-assignment-employee/approve` (`api.php:199`) **không phải luồng duyệt**: chỉ là danh sách phiếu giao việc của chính mình (bảng `job_assignment_employees` không có cột trạng thái).
- `checkDueConfigsManager:<tên>` trên các route duyệt chỉ hỏi ERP xem phòng có nhân viên quá hạn hay không, lỗi kết nối ERP thì cho qua. Không phải chốt quyền.
- Các luồng 2, 4, 8, 9, 10, 11 **không chốt quyền ở BE**. FE ẩn nút theo quyền, nhưng gọi thẳng API thì vẫn duyệt được (fail-open).
- Phiếu chờ của luồng 5, 6 phải duyệt trước ngày bắt đầu. Qua ngày là `can_approve` = false, phiếu kẹt ở trạng thái chờ vĩnh viễn. Màn tổng hợp nên tách nhóm "quá hạn duyệt".

### Module Human

| STT | Tên luồng | Bảng · Entity | Trạng thái chờ | Ai duyệt | API duyệt/từ chối | URL chi tiết | Màn chờ duyệt riêng | Đang chờ | Phiếu chờ mới nhất | ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H12 | Hồ sơ tự khai (yêu cầu cập nhật thông tin cá nhân) | `employee_update_requests` · `Modules\Human\Entities\EmployeeInfoUpdateRequest` | `employee_update_request_status` = 1 ("Chờ duyệt", `EmployeeInfoUpdateRequestStatus::SendApprove`) | FE: `Quản lý danh sách hồ sơ tự khai` (`pages/human/employee_info/request-update/index.vue:328`). **BE không chốt**: `storeApprove` gọi thẳng `updateStatus()` (`Http/Controllers/Api/V1/EmployeeInfoUpdateRequestController.php:109`) | POST `/v1/human/employee-update-requests/approve/{id}` (`Modules/Human/Routes/api.php:348`) | `/human/employee_info/:id/my-info-request` | Không có màn riêng; lọc trong `/human/employee_info/request-update` → GET `human/employee-update-requests` (`:341`) | **0** (đã duyệt 381 · không duyệt 12) | — (bản ghi mới nhất 2026-10-20) | Không | Không có bản ghi nào ở trạng thái chờ. Nghi luồng gửi đi là duyệt luôn ở bước khác; cần nghiệp vụ xác nhận. |
| H13 | Thông báo nội bộ | `self_notifications` · `SelfNotifications` | `status` = 2 ("Đã gửi thông báo"); duyệt → 3, huỷ duyệt → 4 | `canApprove()` = quyền `Duyệt thông báo nội bộ` (`Entities/SelfNotifications.php:85`), **quyền này không tồn tại trong DB** (dòng seeder bị comment, `PermissionsTableSeeder.php:560`). Endpoint **không chốt quyền** | PUT `/v1/human/self-notifications/{selfNotification}/toggle-approve` (`api.php:358`) | `/human/self-notification/:id/approve` | Không | **13** (cả 13 tạo trước 21/09) | 2026-08-21 17:47:05 | Không | FE chỉ hiện nút khi `canApprove` → **không ai duyệt được qua UI**. Nhưng ai có token cũng gọi thẳng API được. Duyệt (3) xong là bắn thông báo cho **toàn bộ** nhân viên. Luồng chết / legacy. |

### Module Payroll

| STT | Tên luồng | Bảng · Entity | Trạng thái chờ | Ai duyệt | API duyệt/từ chối | URL chi tiết | Màn chờ duyệt riêng | Đang chờ | Phiếu chờ mới nhất | ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H14 | Thu nhập P3 (bảng lương khoán/hoa hồng) | `p3_salaries` · `Modules\Payroll\Entities\P3Salary` | `status` = 1 ("Chờ duyệt", mảng `P3_SALARY_STATUS`) | **Không chốt ở BE lẫn FE theo quyền**: duyệt = POST `/` truyền `status` 2/3; menu chỉ gắn `groups: ['Định mức thưởng P3 (Hoa hồng/lương khoán)']` | POST `/v1/payroll/p3_salaries` (`Modules/Payroll/Routes/api.php:154`) · huỷ duyệt POST `/v1/payroll/p3_salaries/cancel_approve` (`:155`) | `/payroll/salary-data/p3-salary/:id/approve` | Có: `/payroll/salary-data/p3-salary/approve` → GET `payroll/p3_salaries/approve` (`:156`, trả mọi bảng khác Đang tạo, không lọc quyền) | **0** (47 bảng đang ở 0 "Đang tạo") | — | Không | Lỗ hổng: `cancel_approve` không chốt gì cả. Hiện chưa có bảng nào gửi duyệt. |
| H15 | Bảng chia thưởng | `bonus_distributions` · `BonusDistribution` | `status` = 1 `STATUS_PENDING` | `auth()->user()->can('BGĐ duyệt bảng chia thưởng')` (`BonusDistributionController.php:108`, `:125`) | POST `/v1/payroll/bonus-distributions/{id}/approve` (`api.php:347`) · POST `/{id}/reject` (`:348`) | `/payroll/bonus-distribution/:id` | Không | **0** (bảng rỗng) | — | Không | ⚠ User đăng nhập là `App\Models\TpEmployee`, **không có trait `HasRoles`**, nên `->can()` gần như luôn false: chưa chạy thử, chỉ suy từ code. Thêm nữa, quyền `BGĐ duyệt bảng chia thưởng` (id 1053) chưa gán cho vai trò nào (0 role). → Luồng chết. |

### Module Meeting

| STT | Tên luồng | Bảng · Entity | Trạng thái chờ | Ai duyệt | API duyệt/từ chối | URL chi tiết | Màn chờ duyệt riêng | Đang chờ | Phiếu chờ mới nhất | ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H16 | Phiếu đặt phòng họp | `meeting_room_bookings` · `Modules\Meeting\Entities\MeetingRoomBooking` | `status` = 1 `STATUS_CHO_DUYET` | Người phụ trách **đúng phòng đó** (`meeting_room_managers`, `$room->managerIds()`) **hoặc** quyền `Duyệt phiếu đặt phòng họp` (id 1589). Chốt trong service `canActOnApprovalByRoom()` (`Services/MeetingRoomBookingService.php:1073`), chạy trong transaction có khoá | PUT `/v1/meeting/room-bookings/{id}/approve` (`Modules/Meeting/Routes/api.php:163`) · PUT `/{id}/reject` (`:164`) | `/meeting/bookings` (popup/hàng) · `/meeting/room-board` | Không có màn riêng; lọc trong `/meeting/bookings` → GET `meeting/room-bookings` (`:143`) | **0** (bảng rỗng) | — | Không | Chốt quyền đặt có chủ đích trong service (comment `api.php:132-141`). Comment ghi "quyền 1580" nhưng DB hiện là id 1589 (code tra theo tên nên vẫn đúng). |
| H17 | Yêu cầu dịch vụ trên phiếu đặt phòng | `meeting_room_bookings` (cột `service_status`) | `service_status` = 1 `SERVICE_STATUS_CHO_CHUAN_BI` | Chỉ người phụ trách phòng (`assertCanHandleServiceRequest`, `MeetingRoomBookingService.php:952`) | PUT `/{id}/service-prepared` (`api.php:170`) · PUT `/{id}/service-rejected` (`:171`) | `/meeting/bookings` | Không | **0** | — | Không | Đây là xử lý yêu cầu, không hẳn là duyệt. Cần nghiệp vụ quyết có đưa vào màn tổng hợp hay không. |

### Module Training

| STT | Tên luồng | Bảng · Entity | Trạng thái chờ (từng cấp) | Ai duyệt từng cấp | API duyệt/từ chối | URL chi tiết | Màn chờ duyệt riêng | Đang chờ | Phiếu chờ mới nhất | ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H18 | Đề xuất đào tạo (2 cấp) | `training_requests` · `Modules\Training\Entities\TrainingRequest` | C1 = 2 `CHO_TP_DUYET` · C2 = 3 `CHO_QLDT_DUYET` | C1: `Trưởng phòng duyệt đề xuất đào tạo` + phòng của phiếu ∈ `manager_departments` (`canDepartmentHeadApprove`, `Entities/TrainingRequest.php:58`) · C2: `Quản lý đào tạo duyệt đề xuất đào tạo` (`:76`). Từ chối: 1 trong 2 quyền (`canDeny`, `:89`) | Duyệt = POST `/v1/training/training_requests/{id}` + `status_request` 3 (TP) / 4 (QLĐT) (`Modules/Training/Routes/api.php:160`) · Từ chối POST `/{id}/deny` (`:162`) | `/training/training_requests/:id/approve` | Có: `/training/training_requests?type=waiting` + widget dashboard (`JobWaitingApproveService`, qua GET `/v1/training/dashboard/getData` `:547`) | **12** (C1 = 8 · C2 = 4); 11 tạo trước 21/09 | 2026-10-08 13:07:24 | Không | Chốt nằm trong `update()`, rẽ nhánh theo `status_request`. Gửi giá trị khác 1-4 (vd 5) thì bỏ qua mọi kiểm tra. `canDeny` không kiểm phòng quản lý. |
| H19 | Đề xuất mở khóa học (2 cấp) | `course_requests` · `CourseRequest` | C1 = 2 `CHO_TP_DUYET` · C2 = 4 `CHO_BGD_DUYET` | C1: `Trưởng phòng duyệt đề xuất mở khóa học` + phòng quản lý (`Entities/CourseRequest.php:179`) · C2: `Ban giám đốc duyệt đề xuất mở khóa học` (`:197`) | Duyệt = POST `/v1/training/course_requests/{id}` + `status_request` 3 (TP → status 4) / 5 (BGĐ) (`api.php:147`) · Từ chối POST `/{id}/deny` (`:149`) | `/training/course_requests/:id/approve` | Có: `/training/course_requests?type=waiting` + widget dashboard | **0** | — | Không | ⚠ `deny` **không kiểm quyền** (`CourseRequestController.php:309`). Gửi thẳng `status_request` = 4 thì nhảy sang chờ BGĐ mà bỏ qua TP, không bị chặn. |
| H20 | Khóa học (2 cấp) | `courses` · `Course` | C1 = 2 `CHO_TP_DUYET` · C2 = 4 `CHO_BGD_DUYET` | C1: `Trưởng phòng duyệt khóa học` + phòng quản lý (`Entities/Course.php:349`) · C2: `Ban giám đốc duyệt khóa học` (`:367`); từ chối `canDeny` (`:385`) | POST `/v1/training/courses/{id}` + `status_request` 3/5 (`api.php:253`) · POST `/{id}/deny` (`:255`) | `/training/courses/:id/approve` | Có: `/training/courses?type=waiting` + widget dashboard | **1** (C1 = 1 · C2 = 0) | 2025-05-26 14:51:52 | Không | Có cùng kẽ hở `status_request` như dòng 19. Phiếu chờ duy nhất đã treo gần 17 tháng. |
| H21 | Đăng ký khóa học của học viên | `course_registers` · `CourseRegister` | `status` = 5 `CourseRegister::PENDING` (duyệt → 10, từ chối → 15, huỷ 6, hoãn 20) | FE: `Duyệt đăng kí khoá học` (`pages/training/course-registers/_id/approve.vue:214`). **BE không chốt** (`CourseRegisterService::toggleApprove`, `Services/CourseRegister/CourseRegisterService.php:91`) | PUT `/v1/training/course-registers/{courseRegister}/toggle-approve` (`api.php:282`) | `/training/course-registers/:id/approve` | Có: `/training/course-registers?status=5` → GET `training/course-registers` (`:276`) + widget dashboard | **49** (48 tạo trước 21/09) | 2026-10-03 09:29:57 | Không | Fail-open ở BE. |
| H22 | Yêu cầu điểm danh học viên | `course_student_attendances` · `CourseStudentAttendance` | `status` = 1 `CHO_DUYET` (0 = chưa điểm danh, 2 duyệt, 3 không duyệt) | **Không chốt ở cả BE lẫn FE**: nút "Lưu" trong `CourseFormShow.vue:2089` mở `ApproveAttendanceModal`, không có điều kiện quyền | POST `/v1/training/courses/student-attendance/{id}/approve` (`api.php:234`) · POST `/courses/student-attendance/approve-multiple` (`:235`) | Tab học viên trong `/training/courses/:id` | Không (`/training/attendance/request-list` là danh sách yêu cầu **của chính học viên**) | **3,631** (3,498 tạo trước 21/09) | 2026-10-16 10:25:34 | Không | Số tồn rất lớn, phần lớn là dữ liệu cũ. Nghi người phụ trách lớp chỉ duyệt nhưng không xử lý hết. Cần nghiệp vụ quyết có coi đây là "phiếu chờ duyệt" hay không. |
| H23 | Kế hoạch đào tạo | `training_plannings` · `TrainingPlanning` | `status` = 2 ("Chờ duyệt"; 3 duyệt, 4 không duyệt) | FE: `Duyệt kế hoạch đào tạo` (`pages/training/training-survey-planning/_id/approve.vue:126`). **BE không chốt** (`TrainingSurveyPlanningService::toggleApprove`, `:355`) | PUT `/v1/training/training-planning/{trainingPlanning}/toggle-approve` (`api.php:397`) | `/training/training-survey-planning/:id/approve` | Có: `/training/training-survey-planning/need-approve` → GET `training/training-planning?status=2` (`:389`) + widget dashboard | **0** (2 bản Đang tạo) | — | Không | Widget dashboard đếm `status=2` của **mọi** công ty, không lọc phạm vi. |
| H24 | Kế hoạch đánh giá năng lực (2 cấp) | `evaluation_planning_capacities` · `EvaluationPlanningCapacity` | C1 = 2 (chờ QLĐT) · C2 = 3 (chờ BGĐ); 5 = đã duyệt, 4 = từ chối (không có hằng số, suy từ FE `capacity-evaluate-planning/_id/approve.vue:202`) | FE: C1 `Quản lý đào tạo duyệt kế hoạch đánh giá`, C2 `Ban giám đốc duyệt kế hoạch đánh giá`. **BE không chốt** (`CapacityEvaluatePlanningService::toggleApprove`, `:1438`, ghi thẳng `status` từ request) | PUT `/v1/training/capacity-evaluate-planning/{id}/toggle-approve` (`api.php:453`) | `/training/capacity-evaluate-planning/:id/approve` | Không | **0** (16 bản đều = 5) | — | Không | BE nhận mọi giá trị `status`, nhảy cấp tuỳ ý. |
| H25 | Kỳ thi đánh giá năng lực (2 cấp) | `evaluation_capacities` · `EvaluationCapacity` | C1 = 2 (chờ QLĐT) · C2 = 3 (chờ BGĐ); 5 duyệt, 4 từ chối | FE: `Quản lý đào tạo duyệt kỳ thi đánh giá năng lực` / `Ban giám đốc duyệt kỳ thi đánh giá năng lực`. **BE không chốt** (`CapacityEvaluateService::toggleApprove`, `:243`) | PUT `/v1/training/capacity-evaluate/{id}/toggle-approve` (`api.php:472`) | `/training/capacity-evaluate/:id/approve` | Không | **0** (13 bản đều = 5) | — | Không | Giống dòng 24. |
| H26 | Công bố kết quả thi offline | `exam_test_results` · `ExamTestResult` | `result` = 2 ("Đang cập nhật") → 1 Đạt / 3 Không đạt | **Không chốt quyền** (`ExaminerController::approveExamResultOffline`, `:863`) | POST `/v1/training/examiners/approveExamResultOffline` (`api.php:89`) | (màn chấm thi) | Không | (không tính) 1,512 kết quả "Đang cập nhật" | 2026-10-03 10:59:10 | Không | Đây là chốt điểm hàng loạt theo khóa/đề, **không phải luồng duyệt phiếu**. Ghi lại để nghiệp vụ loại trừ. |

- **Route chết:** POST `/v1/training/questions/{id}/deny` (`api.php:176`) và POST `/v1/training/exam_test_results/{id}/deny` (`api.php:321`) trỏ tới method `deny` **không tồn tại** trong `QuestionController` / `ExamResultController` (đã kiểm cả lớp cha `ApiController` của module). Gọi vào sẽ ra lỗi 500. Bảng `questions` chỉ có trạng thái 1 Hoạt động / 2 Khoá, không có luồng duyệt.
- `ApiController` của module Training tự viết `isCurrentEmployeeHasPermission` bằng `getAllPermissions()` (không lọc công ty). `BaseModel` dùng cùng cách. Còn widget dashboard dùng `PermissionService` (có lọc công ty). Hai cơ chế này có thể cho kết quả khác nhau với người có vai trò ở nhiều công ty.
- Course register, training planning, capacity (dòng 21, 23, 24, 25) và student attendance (dòng 22) đều chỉ ẩn nút ở FE, BE fail-open.

### Module Rice

Không có luồng duyệt. Lý do:

- `POST /v1/rice/notification/reject-regular|reject-party|admin-reject-regular|close-waiting-rice-cancel` (`Modules/Rice/Routes/api.php:32-37`) là endpoint cho lịch chạy tự động: tự huỷ suất quá giờ, đóng hàng chờ. Nhóm route **không có `auth:api`**.
- `PUT /personal-registration/{id}/reject-register|reject-waiting-register` (`:102-103`) là nhân viên **tự huỷ** suất của mình.
- `PUT /menu-board/{id}/reject-company` (`:92`, `checkPermission:Quản lý báo cơm`) là bếp huỷ suất của công ty theo ngày.
- `rice_registrations.status_regular` = 6 "Chờ đăng ký" là **hàng chờ** khi hết suất, hệ thống tự đôn lên, không có người duyệt. DB còn **30** dòng = 6, ngày gần nhất 2025-12-02, **0** dòng từ hôm nay trở đi. Đây là rác chưa được dọn, không phải phiếu chờ.

---

### Mục mơ hồ cần nghiệp vụ quyết định

1. **Phiếu quá hạn duyệt.** Làm thêm (131 + 212), đi muộn về sớm (28) và đơn nghỉ đã qua mốc 05 tháng sau đều đã quá hạn, BE không cho duyệt nữa nhưng vẫn mang trạng thái "chờ". Màn tổng hợp có đếm chúng không? Có cần tự đóng/huỷ không?
2. **Phiếu giao việc (521) và phiếu công tác (225).** BE chưa chốt người duyệt, chỉ có quyền "Quản lý phiếu …" phía FE. Chốt lại ai là người duyệt (quản lý trực tiếp? quyền?) trước khi đưa vào màn tổng hợp. Lỗi thiếu `auth:api` ở nhóm job-assignment cần xử lý độc lập.
3. **Yêu cầu điểm danh học viên (3,631).** Đây có phải "phiếu chờ duyệt" của màn tổng hợp không? Ai duyệt: giảng viên, người phụ trách lớp hay quản lý đào tạo? Code hiện không chốt ai cả.
4. **Thông báo nội bộ.** Quyền "Duyệt thông báo nội bộ" đã bị gỡ khỏi seeder. Bỏ hẳn bước duyệt (13 bản ghi treo ở status 2) hay khai lại quyền?
5. **Bảng chia thưởng (Payroll).** `->can()` trên `TpEmployee` gần như chắc chắn luôn false, và chưa role nào giữ quyền. Có còn dùng luồng này không?
6. **Thu nhập P3.** Không có quyền duyệt riêng. Ai được duyệt / huỷ duyệt?
7. **Hồ sơ tự khai.** Không có bản ghi nào ở trạng thái 1 "Chờ duyệt". Luồng thực tế có đi qua trạng thái chờ không?
8. **Yêu cầu dịch vụ phòng họp, công bố kết quả thi offline, hàng chờ báo cơm.** Có xếp vào nhóm "duyệt" không? Đề xuất: không.
9. **Đơn xin nghỉ cấp NSHC.** Menu phê duyệt chỉ hiện với `PD-Đơn xin nghỉ`. Người chỉ có quyền NSHC có cần lối vào riêng không?


---

## Phần 2 — Decision

### Module Decision

Nguồn: `hrm-api/Modules/Decision` + `hrm-client/pages/decision` (working tree, nhánh gop_db) · DB `hrm_erp_21_10_prod` (dump prod 21/10/2026, chỉ SELECT). Đường dẫn route dưới đây đều là `hrm-api/Modules/Decision/Routes/api.php:<dòng>`, prefix `/api/v1/decision/...` (riêng Quy chế chung là `/api/v1/regulations/general`).

**Cơ chế chung của 19 loại "Quyết định"** (dòng 1–19 trong bảng):
- **Một bảng cha dùng chung `decisions`** (Entity `Modules\Decision\Entities\Decision`, có SoftDeletes) với cột phân loại `decisions.type` (hằng `Decision::TYPE_*`, giá trị = tên bảng con). Mỗi loại có thêm **bảng con riêng** nối qua `decision_id`. Bảng con KHÔNG có cột status và KHÔNG có `deleted_at`. Trạng thái nằm ở `decisions.status`.
- Hằng trạng thái (`Entities/Decision.php:23-33`): 1 `STATUS_CREATING` (đang tạo/nháp) · **2 `STATUS_CREATED` = chờ XEM XÉT (cấp 1)** · **3 `STATUS_REVIEWED` = đã xem xét, chờ DUYỆT (cấp 2)** · 4 `STATUS_REJECTED_REVIEW` · 5 `STATUS_APPROVED` · 6 `STATUS_REJECTED_APPROVE` · 7 `STATUS_EFFECTIVE`, 8 `STATUS_EXPIRED` (chỉ dùng để lọc, DB không có dòng nào) · 20 `STATUS_CREATED_LABOR_CONTRACT` (tiếp nhận nhân sự đã sinh HĐLĐ).
- Luồng duyệt 2 cấp: **Xem xét = quyền `Xem xét quyết định` (id 399, guard api)**, chuyển 2 → 3 hoặc 4. **Duyệt = quyền `Duyệt quyết định` (id 400, guard api)**, chuyển 3 → 5 hoặc 6. Ghi lịch sử vào `decision_history_approves` (decision_id, status, action, content). Thông báo: khi status=2 thì gửi cho mọi người có `Xem xét quyết định`, khi status=3 thì gửi cho mọi người có `Duyệt quyết định` (`Services/Decision/DecisionService.php:360-385`).
- Logic chung `DecisionService::toggleApprove()` (`Services/Decision/DecisionService.php:324-346`) **chỉ kiểm quyền cho 2 nhánh**: status=3 cần `Xem xét quyết định`, status=5 cần `Duyệt quyết định` (qua helper `isCurrentEmployeeHasPermission`, `app/Helper/PermissionHelper.php:20`, có lọc theo công ty đang làm `role_has_permissions.company_id`). Nhánh **từ chối (4, 6) không kiểm quyền**, và hàm **không kiểm trạng thái hiện tại** của phiếu.
- Route tham số là **id bảng con** (vd `salary_changes.id`), KHÔNG phải `decisions.id`.
- URL client: `/decision/<type-url>/<id bảng con>` (chi tiết) và `/decision/<type-url>/<id>/approve` (màn duyệt). Cả hai được sinh từ `Decision::TYPE_URL_*` và là link trong thông báo.

| STT | Tên luồng (VN) | Module | Bảng (+ type) | Entity | Cột trạng thái + giá trị chờ | Ai duyệt từng cấp | API duyệt/từ chối | URL chi tiết client | Màn "chờ duyệt" riêng? | Số phiếu đang chờ (DB) | Phiếu chờ gần nhất | Bảng thuộc ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| QĐ1 | QĐ thành lập phòng ban | Decision | `decisions` type=`department_establishments` + `department_establishments` | `Entities\DepartmentEstablishment` | `decisions.status`: 2 `STATUS_CREATED` (chờ xem xét) / 3 `STATUS_REVIEWED` (chờ duyệt) | Xem xét: `Xem xét quyết định` · Duyệt: `Duyệt quyết định`. Middleware `checkPermission:Duyệt quyết định\|Xem xét quyết định` + service | PUT `department-establishment/{id}/toggle-approve`, `api.php:91` | `pages/decision/department-establishment/_id/index.vue`, `_id/approve.vue` | Có: `pages/decision/department-establishment/waiting-approve.vue` (gọi `decision/department-establishment?type=waiting-approve`). Không có trong menu. Có trong màn chung | 0 (cấp 1: 0 · cấp 2: 0). Tổng 8 phiếu, đều đã duyệt | — (chưa có phiếu chờ) | Không | Duyệt mà ngày hiệu lực ≤ hôm nay thì tạo phòng ban ngay |
| QĐ2 | QĐ sửa đổi phòng ban | Decision | `decisions` type=`department_changes` + `department_changes` | `Entities\DepartmentChange` | như dòng 1 | như dòng 1 (có middleware) | `api.php:102` | `department-change/_id/index.vue`, `_id/approve.vue` | Có: `department-change/waiting-approve.vue` (API `decision/department-change`). Có trong màn chung | 0 / 0 (tổng 1) | — | Không | |
| QĐ3 | QĐ giải thể phòng ban | Decision | `decisions` type=`department_dissolutions` + `department_dissolutions` | `Entities\DepartmentDissolution` | như dòng 1 | như dòng 1 (có middleware) | `api.php:116`. Có thêm GET `department-dissolution/waiting-approve` ở `api.php:115` | `department-dissolution/_id/index.vue`, `_id/approve.vue` | Có: `department-dissolution/waiting-approve.vue`, nhưng trang này gọi `decision/department-dissolution`, KHÔNG gọi route `/waiting-approve` riêng. Có trong màn chung | 0 / 0 (tổng 1) | — | Không | |
| QĐ4 | QĐ ban hành định biên | Decision | `decisions` type=`manpower_plannings` + `manpower_plannings` | `Entities\ManpowerPlanning\ManpowerPlanning` | như dòng 1 | như dòng 1 (có middleware) | `api.php:231` | `manpower-planning/_id/index.vue`, `_id/approve.vue` | Có: `manpower-planning/waiting-approve.vue`, nhưng link dòng trỏ nhầm `/decision/department-change/{id}`. Có trong màn chung | 0 / 0 (tổng 8, có 1 nháp) | — | Không | Có hằng `TYPE_MANPOWER_PLANNING_CHANGE` ("sửa đổi định biên") nhưng không có route, DB 0 dòng |
| QĐ5 | QĐ ban hành quy chế lương và hỗ trợ | Decision | `decisions` type=`decision_regulation_salary_alls` + `decision_regulation_salary_alls` | `Entities\DecisionRegulationSalary\DecisionRegulationSalaryAll` | như dòng 1 | như dòng 1 (có middleware) | PUT `regulation-salary/{id}/toggle-approve`, `api.php:242` | `regulations/salary/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung (không có trong `$joins` nhưng vẫn hiện nhờ leftJoin) | 0 / 0 (tổng 10) | — | Không | |
| QĐ6 | QĐ ban hành quy chế chung | Decision | `decisions` type=`regulation_general_alls` + `regulation_general_alls` | `Entities\Regulation\RegulationGeneralAll` | như dòng 1 | như dòng 1 (có middleware) | PUT `/api/v1/regulations/general/{id}/toggle-approve`, `api.php:525` | `regulations/general/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (tổng 6) | — | Không | |
| QĐ7 | QĐ tiếp nhận nhân sự | Decision | `decisions` type=`accept_personnels` + `accept_personnels` | `Entities\AcceptPersonnel\AcceptPersonnel` | như dòng 1 (thêm 20 = đã sinh HĐLĐ) | như dòng 1 (có middleware) | `api.php:270` | `accept-personnel/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (tổng 119: 3 nháp, 50 đã duyệt, 66 status 20) | — | Không | |
| QĐ8 | QĐ khen thưởng | Decision | `decisions` type=`decision_rewards` + `decision_rewards` | `Entities\DecisionReward` | như dòng 1 | **Route KHÔNG có middleware.** Controller (`DecisionRewardController.php:105`) chỉ dựa vào service: kiểm `Xem xét quyết định` khi status=3 và `Duyệt quyết định` khi status=5. Từ chối (4/6) **không kiểm quyền** | `api.php:131`. Có thêm GET `decision-reward/waiting-approve` ở `api.php:130` | `decision-reward/_id/index.vue`, `_id/approve.vue` | Có `decision-reward/waiting-approve.vue`, nhưng **hỏng**: chép từ giải thể phòng ban, gọi API `decision/department-dissolution` nên ra dữ liệu giải thể. Có trong màn chung | 0 / 0 (tổng 8, có 2 nháp) | — | Không | Trước khi đổi status còn ghi giá trị khen thưởng đã xem xét/đã duyệt (`updateReviewedValue` / `updateApprovedValue`) |
| QĐ9 | QĐ thưởng lương tháng 13 | Decision | `decisions` type=`decision_salary_bonuses` + `decision_salary_bonuses` | `Entities\DecisionSalaryBonus` | như dòng 1 | **Route KHÔNG có middleware.** Chỉ có kiểm tra trong service như dòng 8 (từ chối không kiểm quyền) | `api.php:145`. Có thêm GET `decision-salary-bonus/waiting-approve` ở `api.php:144` | `decision-salary-bonus/_id/index.vue`, `_id/approve.vue` | Có `decision-salary-bonus/waiting-approve.vue`, nhưng **hỏng** y như dòng 8 (gọi `decision/department-dissolution`). Có trong màn chung | 0 / 0 (DB chưa có phiếu nào) | — | Không | |
| QĐ10 | QĐ kỷ luật nhân sự | Decision | `decisions` type=`employee_disciplines` + `employee_disciplines` | `Entities\EmployeeDiscipline` | như dòng 1 | **Route KHÔNG có middleware.** Chỉ có kiểm tra trong service như dòng 8 | `api.php:308` | `employee-discipline/_id/index.vue`, `_id/approve.vue` | Có `employee-discipline/waiting-approve.vue` (API `decision/employee-discipline?type=waiting-approve`). Có trong màn chung | 0 / 0 (tổng 2) | — | Không | Cập nhật `meeting_participants.state_of_discipline` theo kết quả. Duyệt có hiệu lực thì khoá nhân viên |
| QĐ11 | QĐ bổ nhiệm nhân sự | Decision | `decisions` type=`decision_appoint_personnels` + `decision_appoint_personnels` | `Entities\DecisionAppointPersonnel\DecisionAppointPersonnel` | như dòng 1 | như dòng 1 (có middleware) | `api.php:324` | `appoint-personnel/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Màn chung **chỉ hiện nếu HĐLĐ gắn kèm có `end_date >= hôm nay`** (xem bất thường 1) | 0 / 0 (tổng 4) | — | Không | Duyệt thì tự sinh phụ lục HĐLĐ. Thiếu mẫu in thì trả 422 |
| QĐ12 | QĐ điều chuyển nhân sự | Decision | `decisions` type=`decision_transfer_personnels` + `decision_transfer_personnels` | `Entities\DecisionTransferPersonnel\DecisionTransferPersonnel` | như dòng 1 | như dòng 1 (có middleware) | `api.php:337` | `transfer-personnel/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Màn chung có cùng điều kiện HĐLĐ như dòng 11. **Phiếu đang chờ bị ẩn khỏi màn chung** | **1** (cấp 1: 0 · **cấp 2 chờ Duyệt: 1**). decisions.id=747, bảng con id=43, công ty 9, Đỗ Thị Tố Uyên đã xem xét lúc 20/10 17:33 | 2026-10-20 17:32:49 | Không | Phiếu 747 gắn HĐLĐ 753 có `end_date` NULL (HĐ không thời hạn) nên màn `/decision/waiting-approve` lọc mất. Chỉ thấy qua thông báo hoặc số đếm dashboard |
| QĐ13 | QĐ ký hợp đồng lao động (gia hạn) | Decision | `decisions` type=`renew_labor_contracts` + `renew_labor_contracts` | `Entities\RenewLaborContract\RenewLaborContract` | như dòng 1 | như dòng 1 (có middleware) | `api.php:351` | `renew-labor-contract/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (tổng 1) | — | Không | |
| QĐ14 | QĐ điều chỉnh lương nhân sự | Decision | `decisions` type=`salary_changes` + `salary_changes` | `Entities\SalaryChange\SalaryChange` | như dòng 1 | như dòng 1 (có middleware) | `api.php:363` | `salary-change/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (tổng 376: 3 nháp, 373 đã duyệt) | — | Không | Duyệt thì sinh phụ lục HĐLĐ |
| QĐ15 | QĐ cử đi đào tạo | Decision | `decisions` type=`assign_trainings` + `assign_trainings` (cột `status` riêng, toàn NULL) | `Entities\AssignTraining` | như dòng 1 | **Route KHÔNG có middleware.** Chỉ có kiểm tra trong service như dòng 8 | `api.php:371` | `assign-training/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (tổng 2) | — | Không | |
| QĐ16 | QĐ chấm dứt hợp đồng lao động | Decision | `decisions` type=`termination_labor_contracts` + `termination_labor_contracts` | `Entities\TerminationLaborContract\TerminationLaborContract` | như dòng 1 | như dòng 1 (có middleware) | `api.php:388` | `termination-labor-contract/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung (phiếu chờ có hiện trong query mô phỏng) | **1** (**cấp 1 chờ Xem xét: 1** · cấp 2: 0). decisions.id=748, bảng con id=64, công ty 1, người tạo employees.id 883 | 2026-10-21 13:21:31 | Không | Duyệt có hiệu lực thì đồng bộ nghỉ việc. Có thể cập nhật `employee_department_dissolutions` |
| QĐ17 | QĐ nghỉ hưu | Decision | `decisions` type=`retirements` + `retirements` | `Entities\Retirement\Retirement` | như dòng 1 | như dòng 1 (có middleware) | `api.php:399` | `retirement/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (DB chưa có phiếu) | — | Không | Code đồng bộ sau khi duyệt đang bị comment |
| QĐ18 | QĐ tạm hoãn hợp đồng lao động | Decision | `decisions` type=`suspend_labor_contracts` + `suspend_labor_contracts` | `Entities\SuspendLaborContract\SuspendLaborContract` | như dòng 1 | như dòng 1 (có middleware) | `api.php:411` | `suspend-labor-contract/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (DB chưa có phiếu) | — | Không | |
| QĐ19 | QĐ tăng lương thâm niên | Decision | `decisions` type=`increase_seniorities` + `increase_seniorities` | `Entities\IncreaseSeniority\IncreaseSeniority` | như dòng 1 | như dòng 1 (có middleware) | `api.php:437` | `increase-seniority/_id/index.vue`, `_id/approve.vue` | Không có màn riêng. Có trong màn chung | 0 / 0 (DB chưa có phiếu) | — | Không | Duyệt thì sinh phụ lục HĐLĐ |
| QĐ20 | Biên bản xử lý sự cố | Decision | Bảng riêng `trouble_shooting_reports` (không dùng `decisions`) | `Entities\TroubleShootingReport` | `trouble_shooting_reports.status`: **1 cấp**, 2 `STATUS_CREATED` = chờ duyệt (3 `APPROVED`, 4 `REJECTED_APPROVE`) | Quyền nghiệp vụ là `Duyệt biên bản xử lý sự cố` (id 900, api). Quyền này chỉ dùng để gửi thông báo và lọc màn chờ duyệt. **Route KHÔNG có middleware, và `TroubleShootingReportService::toggleApprove` (`Services/TroubleShootingReport/TroubleShootingReportService.php:300`) KHÔNG kiểm quyền nào**: ai đăng nhập cũng duyệt/từ chối được | `api.php:283` | `category/trouble-shooting-reports/_id/index.vue`, `_id/approve.vue` | Có: `category/trouble-shooting-reports/waiting-approve.vue`, có trong menu `components/subsystem-menu/operation-hub.js:297`. API `decision/trouble-shooting-report?type=waiting-approve`, lọc theo `Duyệt biên bản xử lý sự cố` (`TroubleShootingReportService.php:111-122`). **Không** có trong màn chung | 0 (tổng 3, đều status 3) | — | Không | Không SoftDeletes. Mỗi lần toggle đều set lại `code` (≠3 thì `code = null`) |
| QĐ21 | Phiếu đăng ký bảo hiểm | Decision | Bảng riêng `insurance_registers` | `Entities\InsuranceRegister\InsuranceRegister` | `insurance_registers.status`: **1 cấp**, 2 `STATUS_CREATED` = chờ duyệt (3 APPROVED, 4 REJECTED_APPROVE, 5/6 hiệu lực/hết hạn, 7 CANCELLED) | Quyền `Duyệt phiếu đăng ký bảo hiểm` (id 955, api). **Route KHÔNG có middleware.** `InsuranceService::toggleApprove` (`Services/Insurance/InsuranceService.php:725-729`) **chỉ kiểm quyền khi TỪ CHỐI (status 4)**; **DUYỆT (status 3) không kiểm quyền** | `api.php:469` (thêm `cancel` ở `api.php:474`) | `insurance/_id/index.vue`, `_id/approve.vue` | Có: `insurance/waiting-approve.vue` (menu `components/subsystem-menu/insurance.js:114`). API `decision/insurance?status=2`, không lọc theo người duyệt. **Không** có trong màn chung | 0 (tổng 718: 668 duyệt, 35 từ chối, 10 huỷ, 5 nháp) | — | Không | Không SoftDeletes |
| QĐ22 | Hợp đồng đào tạo | Decision | Bảng riêng `training_contracts` | `Entities\TrainingContract` | `status`: 1 `STATUS_CREATING`, 2 `STATUS_APPROVED`. Không có trạng thái "chờ" | Không xác định. Route không middleware, quyền liên quan chỉ có `Tạo hợp đồng đào tạo` (912) | `api.php:419`. **Route chết**: `TrainingContractController` KHÔNG có method `toggleApprove` nên gọi vào sẽ lỗi 500 | `category/training-contract/_id/index.vue` (không có approve.vue) | Không | 0 (4 phiếu, đều status 1) | — | Không | Có route duyệt nhưng thực tế không có luồng duyệt |

**Màn chờ duyệt chung — `GET /api/v1/decision/waiting-approve`** (`api.php:69` → `DecisionController::getWaitingApprove` `Http/Controllers/V1/DecisionController.php:251` → `Services/Decision/WaitingApproveService.php:156-309`). Client: `pages/decision/waiting-approve.vue` (gọi ở dòng 485-486), menu `components/subsystem-menu/operation-hub.js:292`. Export ở `api.php:70`.
- **Lọc theo người duyệt**: ai có `Xem xét quyết định` thấy status 2, ai có `Duyệt quyết định` thấy status 3 (`WaitingApproveService.php:187-195`). Người không có quyền nào thì `whereIn(status, [])` nên ra rỗng. Quyền xét theo **công ty đang làm**, nhưng query **không lọc `decisions.company_id`** (trừ khi FE truyền `company_id`). Kết quả: người có quyền ở công ty A thấy phiếu chờ của mọi công ty. Nhưng khi bấm duyệt, service lại kiểm quyền theo công ty đang làm, còn middleware thì không phân công ty.
- **Phạm vi**: mọi `decisions` chưa xoá mềm, gồm cả 19 type. `$joins` (`:158-176`) không liệt kê `regulation_general_alls` / `decision_regulation_salary_alls`, nhưng đều là leftJoin nên 2 loại quy chế vẫn hiện (chỉ thiếu cột riêng).
- **Bỏ sót**:
  1. Biên bản xử lý sự cố (bảng riêng, có màn chờ riêng).
  2. Phiếu đăng ký bảo hiểm (bảng riêng, có màn chờ riêng).
  3. **QĐ bổ nhiệm và điều chuyển mà HĐLĐ gắn kèm có `end_date` NULL hoặc đã qua**. Lọc ở `:236-241`: `whereDate(decision_labor_contracts.end_date, '>=', today)`, NULL coi như loại. Trên DB: điều chuyển 29/42 phiếu có HĐ `end_date` NULL, 7 phiếu HĐ đã hết hạn. Bổ nhiệm 4/4 phiếu có `end_date` NULL. **Phiếu đang chờ duyệt 747 hiện đang bị ẩn vì lý do này.**
- Các route `waiting-approve` riêng (`api.php:115,130,144`) và các màn `*/waiting-approve.vue` riêng đều dùng `DecisionService::filterDecision` với `type=waiting-approve` (`Services/Decision/DecisionService.php:175-190`). Logic lọc theo quyền giống màn chung nhưng không có điều kiện HĐLĐ. Ngoài 3 màn của 3 dòng 20/21 và màn chung, không màn riêng nào có trong menu.
- **Dashboard** `GET dashboard/waiting-approve` (`api.php:491` → `Services/Dashboard/DashboardService.php:454`): đếm `decisions` status 2 (chờ xem xét) và 3 (chờ duyệt), thêm số "quá 1 ngày" (`effective_date < hôm nay`) và số biên bản xử lý sự cố status 2. Có lọc theo công ty và phạm vi xem (`checkPermissionListWithCompanyFilter`). Ngoài 2 quyền duyệt, **thêm `Quản lý quyết định` cũng được xem số này**. **Không có điều kiện HĐLĐ**, nên dashboard vẫn đếm phiếu 747 trong khi bấm link sang `/decision/waiting-approve` thì không thấy. Không đếm bảo hiểm. `dashboard/not-approve` (`api.php:492`, `DashboardService.php:557`) đếm status 4/6 và biên bản xử lý sự cố bị từ chối.

**Bất thường**
- **Phiếu đang chờ bị ẩn khỏi màn chờ duyệt chung**: decisions.id=747 (QĐ điều chuyển, chờ Duyệt cấp 2, công ty 9). Nguyên nhân là bộ lọc `decision_labor_contracts.end_date >= today` loại bỏ HĐ không thời hạn (`WaitingApproveService.php:236-241`). Lỗi này ảnh hưởng gần như mọi QĐ bổ nhiệm và điều chuyển.
- **Route duyệt không gắn middleware**: khen thưởng (`api.php:131`), thưởng lương tháng 13 (`:145`), kỷ luật (`:308`), cử đi đào tạo (`:371`), biên bản xử lý sự cố (`:283`), bảo hiểm (`:469`), hợp đồng đào tạo (`:419`).
  - Với 4 loại QĐ, **từ chối (4/6) không cần quyền**.
  - Với biên bản xử lý sự cố, **duyệt và từ chối đều không cần quyền**.
  - Với bảo hiểm, **duyệt không cần quyền** (chỉ từ chối mới kiểm).
- **`DecisionService::toggleApprove` không kiểm trạng thái hiện tại**: người có `Duyệt quyết định` có thể gửi thẳng status=5 khi phiếu còn ở 1/2 (bỏ cấp Xem xét), duyệt lại phiếu đã duyệt, hoặc từ chối phiếu đã duyệt. Middleware `Duyệt quyết định|Xem xét quyết định` là OR, nên người chỉ có `Xem xét` vẫn gọi được status=6 (từ chối duyệt cấp 2).
- **Hai bộ kiểm quyền lệch nhau**: middleware `checkPermission` dùng spatie `getAllPermissions()` trên `Modules\Timesheet\Entities\Employee` (không theo công ty, bỏ sót role có `model_type='App\Employee'`). Service dùng `isCurrentEmployeeHasPermission` (theo công ty đang làm). Trên DB, các vai trò đang giữ quyền 399/400/900/955 đều gắn `model_type = Modules\Timesheet\Entities\Employee`, nên với 4 quyền này chưa có người nào bị bỏ sót vì `App\Employee`. Số người theo công ty: Xem xét QĐ 7–20 người/công ty, Duyệt QĐ 7–16 người/công ty.
- **Màn chờ duyệt riêng chép sai**: `decision-reward/waiting-approve.vue` và `decision-salary-bonus/waiting-approve.vue` gọi API `decision/department-dissolution` và link sang `/decision/department-dissolution/...`. `manpower-planning/waiting-approve.vue` link sang `/decision/department-change/...`. Các màn này không có trong menu.
- **Route và trang chết**: route `training-contract/{id}/toggle-approve` (`api.php:419`) trỏ tới method không tồn tại. Trang `pages/decision/appendix-labor-contract/_id/approve.vue` (dòng 118-119, 151-152) gọi `decision/appendix-labor-contract/{id}/toggle-approve` nhưng route này không có trong `api.php` (nhóm `api.php:443-454`). `appendix_labor_contracts` có 415 dòng, đều status 2 (`STATUS_APPROVED`), không có phiếu chờ.
- Không có phiếu chờ nào bị xoá mềm (`decisions` có `deleted_at` và status 2/3: 0 dòng). Hai phiếu đang chờ đều có dòng bảng con tương ứng.
- Không bảng nào trong module này được ERP (`ERP/TanPhatDev` thư mục app/database/routes) tham chiếu.

**Mục mơ hồ cần nghiệp vụ quyết định**
1. Màn chờ duyệt chung có cố ý ẩn QĐ bổ nhiệm/điều chuyển khi HĐLĐ không thời hạn hoặc đã hết hạn không? Theo nghiệp vụ thì HĐ không thời hạn nên được hiện (phiếu 747 đang kẹt).
2. Người có quyền ở công ty A có được thấy và duyệt phiếu chờ của công ty B trong màn chung không? Hiện list không lọc công ty, nhưng service khi duyệt lại kiểm quyền theo công ty đang làm.
3. Từ chối (4/6) có cần quyền tương ứng cấp đó không, và có bắt buộc đúng thứ tự 2 → 3 → 5 (không cho nhảy cấp) không?
4. Biên bản xử lý sự cố và phiếu đăng ký bảo hiểm (duyệt 1 cấp) có cần đưa vào màn chờ duyệt chung / registry chung không? Duyệt hai loại này có phải gate bằng `Duyệt biên bản xử lý sự cố` / `Duyệt phiếu đăng ký bảo hiểm` không? Hiện chưa gate.
5. Hợp đồng đào tạo và phụ lục HĐLĐ có luồng duyệt thật không, hay bỏ route/trang duyệt đang chết?
6. Dashboard cho người chỉ có `Quản lý quyết định` thấy số "chờ xem xét/chờ duyệt". Có đúng ý đồ không? Người này bấm link sang màn chung sẽ thấy danh sách rỗng.


---

## Phần 3 — Assign

### Module Assign

Nguồn: `HRM/hrm-api` + `HRM/hrm-client` nhánh `gop_db` (working tree), DB `hrm_erp_21_10_prod` (dump prod 21/10/2026). Mọi số đếm đều lấy từ SELECT thật. Không bảng nào trong danh sách dưới có cột `deleted_at` (đã kiểm `information_schema`), nên số đếm là toàn bảng. Route ghi `api.php:N` là `Modules/Assign/Routes/api.php`; các route con nằm ở `Modules/Assign/Routes/<X>/api.php`.

Ký hiệu cổng quyền:
- **[MW]** = middleware `checkPermission:` (spatie `getAllPermissions()` trên `Modules\Timesheet\Entities\Employee`, KHÔNG lọc theo công ty).
- **[H]** = helper `isCurrentEmployeeHasPermission()` / `PermissionService` (lọc `role_has_permissions.company_id` = công ty đang làm).
- **[BM]** = `BaseModel::isCurrentEmployeeHasPermission` (spatie, không lọc công ty).

Cả 3 cách đều đọc role qua morph `Modules\Timesheet\Entities\Employee`. Trong `employee_has_roles` có 1355 dòng `model_type='App\Employee'` và 502 dòng `Modules\Timesheet\Entities\Employee`, nên **mọi cổng quyền dưới đây đều bỏ sót các role gắn kiểu App\Employee**.

`dueConfig:` / `checkDueConfigsManager:` chỉ chặn người quản lý đang có hàng quá hạn, KHÔNG phải cổng quyền.

| STT | Tên luồng | Module | Bảng | Entity | Cột trạng thái · giá trị chờ | Ai duyệt từng cấp | API duyệt / từ chối | URL chi tiết (client) | Màn "chờ duyệt" riêng | Số phiếu đang chờ (DB) | Phiếu chờ gần nhất | Bảng thuộc ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AS1 | Báo giá BOM (duyệt giá 3 cấp) | Assign | `quotations` (`is_summary=0`) | `Modules\Assign\Entities\Quotation` | `status`: `STATUS_CHO_TP_DUYET=2`, `STATUS_CHO_BGD_DUYET=3`; cấp ở `price_approval_level` (`LEVEL_1` tự duyệt, `LEVEL_2` TP, `LEVEL_3` TP→BGĐ) | Cấp 1: người lập tự duyệt (`ensureEditableByCreator`). TP: "Trưởng phòng duyệt giá Bom giải pháp" [MW+H] + quản lý phòng của BG (`ensureTpCanApprove`). BGĐ: "Ban giám đốc duyệt giá Bom giải pháp" [MW+H] + cùng `company_id` (`ensureBgdCanApprove`) | self-approve `api.php:650`; tp-approve `:651`; bgd-approve `:653`; reject `:655`; ds chờ `:611` (Service `QuotationService.php:3953/3990/4041/4099`) | `/assign/quotations/:id` (`pages/assign/quotations/_id/index.vue`) | CÓ: `pages/assign/quotations/pending-approval/index.vue` (scope `applyPendingApprovalScope` `QuotationService.php:4399`) | **35**: chờ TP 35 (cấp 2: 24, cấp 3: 11); chờ BGĐ 0; chờ tự duyệt (status 1 + level 1) 0 | created 2026-10-16 15:44:14; submitted 2026-10-19 15:07:31 | Bảng là của HRM (có `is_summary`, KHÔNG có `quotation_type`). ERP còn model cũ `App\Quotation`, `App\Model\Sale\NormalQuotation`/`LiquidationQuotation`/`CostFixingQuotation` trỏ `quotations` (trùng tên, xem bất thường). ERP thật dùng `firm_quotations` | Duyệt xong thì đồng bộ sang ERP (`syncToErpAfterApproval`). Quyền TP có ở 5 role, BGĐ ở 6 role |
| AS2 | Báo giá tổng hợp (1 cấp) | Assign | `quotations` (`is_summary=1`) | `Quotation` (bộ `SUMMARY_STATUS_*`) | `status`: `SUMMARY_STATUS_CHO_DUYET=2` (trùng số với "Chờ TP duyệt" của BG thường) | "Trưởng phòng duyệt giá Bom giải pháp" [MW+H] + quản lý phòng (`SummaryQuotationService::ensureCanApprove` `:1064`) | approve `api.php:594`; reject `:596` | `/assign/summary-quotations/:id` | KHÔNG (bị loại khỏi pending-approval bằng `is_summary=false`) | **0** (bảng không có dòng `is_summary=1` nào) | — | Không | Chưa có dữ liệu thật |
| AS3 | Đề xuất gia hạn dự án TKT | Assign | `prospective_project_extension_requests` | `ProspectiveProjectExtensionRequest` | `status`: `STATUS_CHO_TP_DUYET=1`, `STATUS_CHO_BGD_DUYET=2`; `approval_level` (`LEVEL_TP=1`, `LEVEL_BGD=2`) | TP: "Trưởng phòng duyệt gia hạn dự án TKT" [MW+H] + quản lý phòng. BGĐ: "Ban giám đốc duyệt gia hạn dự án TKT" [MW+H] + cùng công ty | tp-approve `api.php:505`; bgd-approve `:507`; reject `:509`; ds chờ `:503` | Tab trong `/assign/prospective-projects/:id/manager` (`ProspectiveProjectExtensionsTab.vue`) | CÓ: `pages/assign/prospective-projects/extension-requests/index.vue` | **1** (chờ TP, cấp BGĐ) | 2026-10-19 16:53:17 | Không | ⚠️ Cả 2 quyền TP/BGĐ guard api có **0 role** → phiếu đang chờ không ai duyệt được |
| AS4 | Hợp đồng HRM | Assign | `hrm_contracts` | `Entities\Contract\Contract` | `status`: `STATUS_CHO_DUYET=2` | "Duyệt hợp đồng" [MW + H trong controller] | approve `api.php:846`; reject `:847` (`ContractController.php:574/608`) | `/assign/contracts/:id` | KHÔNG | **0** (bảng rỗng) | — | ERP có model đọc (`app/Model/Assign/HrmContract.php`, `app/Model/Hrm/HrmContract.php`, dùng ở `ProductExportRequestsController`), không có luồng duyệt bên ERP | ⚠️ "Duyệt hợp đồng" guard api có **0 role** (bản guard web có 21 role). BE không kiểm phòng/công ty |
| AS5 | Phiếu bàn giao công việc (TP duyệt) | Assign | `handovers` | `Handover` | `status`: `STATUS_PENDING=2` | "Duyệt bàn giao công việc" [MW]. Danh sách chờ lọc theo `listManageDepartmentIdsWithOwn()`, còn `approve`/`reject` thì KHÔNG kiểm phòng | approve `api.php:1432`; reject `:1434`; ds chờ `:1420` | `/assign/handover/:id` | CÓ: `pages/assign/handover/pending.vue` | **0** (bảng rỗng) | — | Không | |
| AS6 | Tiếp nhận mục bàn giao | Assign | `handover_items` | `HandoverItem` | `receive_status`: `STATUS_PENDING=0` (khi phiếu cha `APPROVED=3`) | Người nhận: `receiver_id == auth()->id()` (`HandoverService::acceptItem` `:955`, `rejectItem` `:1003`) | accept `api.php:1436`; reject `:1437`; accept-all `:1438`; ds `:1423` (receiving) | `/assign/handover/:id/receive` | CÓ: `pages/assign/handover/receiving.vue` | **0** (bảng rỗng) | — | Không | Theo vai trò, không theo quyền |
| AS7 | Yêu cầu làm giải pháp (tiếp nhận / từ chối) | Assign | `request_solutions` | `RequestSolution` | `status`: `STATUS_CHO_TIEP_NHAN=2` | "Tiếp nhận yêu cầu làm giải pháp" [MW]. Danh sách chờ lọc thêm theo `receive_dept` ∈ phòng quản lý (`RequestSolutionService` ~`:190`). `receive`/`reject` KHÔNG kiểm phòng | receive `api.php:421`; reject `:423`; ds chờ `:417` | `/assign/request-solution/:id` | CÓ: `pages/assign/request-solution/pending.vue` | **9** | 2026-09-11 14:35:34 | Không | Có quyền ở phòng A thì gọi API tiếp nhận được YC của phòng B |
| AS8 | Yêu cầu điều chỉnh giải pháp | Assign | `solution_adjustment_requests` | `SolutionAdjustmentRequest` | `status`: `STATUS_DA_GUI=1` | Ý đồ: PM giải pháp hoặc TP phòng nhận (`isCurrentUserTPOrPM`, accessor `is_can_accept` `Entity:84`), nhưng **chỉ FE dùng** | accept `api.php:408`; reject `:409` | Tab `SolutionAdjustmentTab.vue` trong `/assign/prospective-projects/:id/manager` | KHÔNG | **1** | 2026-08-21 16:22:04 | Không | ⚠️ FAIL-OPEN: controller/service không kiểm quyền, cũng không kiểm trạng thái → user đăng nhập bất kỳ accept/reject được, kể cả phiếu đã xử lý |
| AS9 | Hồ sơ trình duyệt giải pháp | Assign | `solution_review_profiles` | `SolutionReviewProfile` | `status`: `'pending'` (`STATUS_PENDING`) | Người tạo giải pháp (`solution.created_by == auth()->id()`, `SolutionService::reviewSolutionProfileDecision` `:2697`). Dự án tự triển khai: tự duyệt | decision `api.php:467` | `/assign/solutions/:id/manager` | KHÔNG (chỉ modal `PendingApprovalModal` trong manager, `api.php:474`) | **0** (approved 11, draft 2, expired 1, finalized 1) | — | Không | Đổi trạng thái BOM theo hồ sơ (`BomListService::syncStatusFromSubmission`): `bom_lists.status=3` là hệ quả, không phải luồng riêng |
| AS10 | Hồ sơ trình duyệt hạng mục | Assign | `solution_module_review_profiles` | `SolutionModuleReviewProfile` | `status`: `'pending'` | PM giải pháp hoặc PM ghi trên hồ sơ (`SolutionModuleService::reviewModuleProfileDecision` `:1397`) | decision `api.php:888` | `/assign/solution-modules/:id/manager` | KHÔNG (modal, `api.php:882`) | **0** (bảng rỗng) | — | Không | `solution_modules.status=6` (CHO_DUYET_HO_SO) có 0 dòng |
| AS11 | Giải pháp chờ PM / Leader duyệt | Assign | `solutions` | `Solution` | `status`: `STATUS_CHO_PM_DUYET=3`, `STATUS_CHO_LEADER_DUYET=5`, `STATUS_CHO_DUYET_GIAI_PHAP=9` | PM (`pm_id`) / Leader hạng mục (`leader_id`); cổng `Solution::canEdit()` (`SolutionController.php:135`) | Chuyển trạng thái qua PUT update `api.php:440` (không có route approve riêng) | `/assign/solutions/:id/manager` | KHÔNG | **1** (status 3, id 29 `HN_KD3.UD.0100.2026.DA004_GP29`, pm_id 65); status 5 và 9: 0 | 2026-07-27 11:29:05 (updated 2026-09-04) | Không | Là bước "tiếp nhận/phân công" hơn là duyệt. Cần nghiệp vụ xác nhận có tính vào tổng hợp không |
| AS12 | Task: duyệt triển khai + duyệt kết quả | Assign | `tasks` | `Entities\Task\Task` | `status`: `PENDING_APPROVAL=2` (duyệt triển khai), `REVIEW=6` (duyệt kết quả) | Triển khai: "Duyệt triển khai task" [H] + quản lý phòng của người xử lý (`Task::canStartApprove` `:253`). Kết quả: `approver_id == auth()->id()` (`canResultApprove` `:280`) | Qua PUT update `api.php:1085` (`TaskService` ~`:470`, kiểm `getAllowedNextStatuses`) | Modal trong `/assign/tasks` và trong manager giải pháp | KHÔNG (modal `pending-approvals` `api.php:474/882`; màn my-todo có `can_approve`) | **2**: duyệt triển khai 0, duyệt kết quả 2 (cả 2 đều có approver) | 2026-07-27 11:41:14 | Không | |
| AS13 | Duyệt bình luận task | Assign | `comments` (gói laravel-comment) | `Comment` | `approved=0` | KHÔNG có cổng (`TaskCommentController::approve` `:197`) | `api.php:1095` | — | KHÔNG | **0** (1 bình luận, approved=1) | — | Không | Không phải luồng nghiệp vụ, mặc định approved=1. Endpoint fail-open |
| AS14 | ~~Yêu cầu xuất hàng~~ (TRÙNG F25 — chỉ tính ở F25) **[ERP]** Yêu cầu xuất hàng: "Không duyệt" phía HRM | Assign | `product_export_requests` | `Entities\Warehouse\ProductExportRequest` | `status`: `STATUS_CHO_DUYET=2` (còn `DOI_TP_DUYET=10`, `DOI_BGD_DUYET=11`, `CHO_DUYET_NHAP=14` là cấp ERP) | Reject: "Kế toán kho" [H] + cùng công ty (`canReject` `Entity:358`). HRM không có route duyệt | reject `api.php:747` | `/finance/product-export-requests/:id` | KHÔNG (bên HRM) | **16** status 2 (0 phiếu loại HRM 20/21); thêm status 10: 1, status 14: 1 (luồng ERP) | 2026-10-21 15:45:57 | **CÓ, bảng ERP** (`app/Model/Warehouse/ProductExportRequest.php`). ERP duyệt ở `ERP routes/web.php:1034` (`manager-approve`, `switch-board-of-manager`) | ⚠️ "Kế toán kho" guard api có **0 role** (guard web 12) → nút Không duyệt bên HRM chết |
| AS15 | Issue: người duyệt xác nhận đã xử lý | Assign | `issues` | `Issue` | `status='resolved'` + `approver_id` | `approver_id == auth()->id()` (`Issue::canHandle` `:158`) | `api.php:1107` (PATCH status) | Panel Issue | KHÔNG | **0** (bảng rỗng) | — | Không | |
| AS16 | Phiếu đề xuất / Phiếu công tác (legacy) | Assign | `assign_requests` | `AssignRequest` (controller `AssignBusinessController`) | `status`: `CHO_DUYET=2`; chờ duyệt kết quả `DA_NHAP_KET_QUA=5`; `type`: `PHIEU_DE_XUAT=1`, `PHIEU_CONG_TAC=2` | Duyệt: "Trưởng phòng duyệt phiếu giao công tác" [BM] + `department_id` ∈ `manager_departments` (`canApproveAssignBusiness` `:774`, cho duyệt cả khi `DANG_TAO`). Duyệt KQ: "Trưởng phòng duyệt kết quả công tác" [BM] (`:820`) | Duyệt / duyệt KQ qua update `api.php:1213` (`status_request=3`, `action=approve_result`); deny `:1221` | `/assign/assign_business/:id/approve`, `/assign/assign_business/:id/approve_result` | CÓ (chỉ cho KQ): `pages/assign/assign_waiting_approve_result/index.vue` (gọi `assign/assign_business?status=5`) | **118**: type 1: 33, type 2: 85; chờ duyệt KQ (status 5): 0 | type 1: 2026-09-17 08:06:36; type 2: 2026-10-08 14:52:30 | Không (ERP có `assign_business` riêng, xem 23) | Đang dùng (7661 phiếu, mới nhất 21/10). Ở `deny` gọi `canApprove…()` TRƯỚC khi kiểm null |
| AS17 | Phiếu đề xuất công việc (legacy) | Assign | `job_requests` | `JobRequest` (cùng bảng với `TpJobRequest`) | `status`: `CHO_DUYET=2`; bước 2 `CHO_GIAO_VIEC=3` | Duyệt: "Trưởng phòng duyệt phiếu đề xuất công việc" [BM] + quản lý `department_request_id` (`canApprove` `:92`). Giao việc: "Trưởng phòng giao đi công tác" [BM] + quản lý `department_implement_id` (`canAssign` `:103`) | Duyệt qua update `api.php:1361` (gate `JobRequestController.php:205`); deny `:1365` | `/assign/job_requests/:id/approve` | KHÔNG | **20**: chờ duyệt 2 + chờ giao việc 18 | duyệt: 2026-07-24 11:10:01; giao: 2026-09-11 07:42:34 | Có model ERP `app/Model/Assign/JobRequest.php` (chỉ đọc) | Phiếu mới nhất 11/09/2026 → gần như ngừng dùng |
| AS18 | Phiếu giao việc + duyệt kết quả (legacy) | Assign | `assign_jobs` | `AssignJob` | `status`: `CHO_DUYET=2`; chờ duyệt KQ `DA_NHAP_KET_QUA=5` | Ý đồ: "Trưởng phòng duyệt phiếu giao công việc" / "Trưởng phòng duyệt kết quả công việc" [BM] + `manager_departments` (`canApprove` `:89`, `canApproveResult` `:97`) | Duyệt qua update `api.php:1374`; approveResult `:1376`; deny `:1381` | `/assign/assign_jobs/:id/approve`, `/assign/assign_jobs/:id/approve_result` | CÓ (cho KQ): `pages/assign/assign_job_waiting_approve_result/index.vue` | **13**: chờ duyệt 7 + chờ duyệt KQ 6 | duyệt: 2026-03-11 06:58:25; KQ: 2024-11-08 08:48:38 | Không | ⚠️ FAIL-OPEN: `AssignJobController` không gọi `canApprove()`/`canApproveResult()` ở update/approveResult/deny, chỉ trả cờ cho FE. Dữ liệu chờ đã cũ |
| AS19 | Hồ sơ thanh toán công tác (legacy) | Assign | `payment_profiles` | `PaymentProfile` | `status`: `CHO_DUYET=2` | "Duyệt hồ sơ thanh toán" [H] (`canApprove` `:135`), KHÔNG kiểm phòng/công ty | approve `Routes/PaymentProfile/api.php:24` (không có route từ chối) | `/assign/payment_profile/:id/show` | KHÔNG | **292** | 2026-06-02 15:19:06 | Không (ERP có hồ sơ thanh toán riêng trên `assign_business`, `ERP routes/web.php:2114` `submitApproved`) | Tồn đọng lớn, không phiếu mới từ 06/2026 → có thể là rác tồn |
| AS20 | Đề nghị thanh toán công tác (2 cấp, legacy) | Assign | `payment_business_requests` | `PaymentBusinessRequest\PaymentBusinessRequest` | `status`: `CHO_TP_DUYET=2`, `CHO_KT_DUYET=3` | TP: "TP Duyệt đề nghị thanh toán" [H]. KT: "KT Duyệt đề nghị thanh toán" [H] (`canTpApprove` `:190`, `canKtApprove` `:196`). Không kiểm phòng | approve `Routes/PaymentBusinessRequest/api.php:25`; ktApprove `:26`; disApprove `:27`; ktDisApprove `:28` | `/assign/payment_business_request/:id/show` | KHÔNG | **1041**: chờ TP 821 + chờ KT 220 | TP: 2026-10-19 13:38:24; KT: 2026-08-04 16:34:49 | Không | Lượng chờ lớn nhất module. Không nằm trong danh sách brief nhưng là luồng duyệt thật |
| AS21 | Quyết toán công theo HĐ (HRM, 2 cấp) | Assign | `hrm_settlement_contracts` (log: `settlement_contract_history_approves`) | `SettlementContract\SettlementContract` + `SettlementContractHistoryApprove` | `status`: `CHO_TP_DUYET=2`, `CHO_KT_DUYET=3` | TP: "TP duyệt quyết toán hợp đồng" [H]. KT: "KT duyệt quyết toán hợp đồng" [H]. Không kiểm phòng | approve `Routes/SettlementContract/api.php:27`; ktApprove `:28`; tpReject `:29`; ktReject `:30` | `/assign/settlement_contract/:id/show` | KHÔNG | **0** (4 phiếu, đều đã duyệt; bảng log rỗng) | — | Bảng `hrm_settlement_contracts` là HRM. ERP có `settlement_contracts` riêng (`app/Model/Sale/SettlementContract.php`, chờ TP 18, KT 204, ngoài phạm vi Assign) | Gần như không dùng |
| AS22 | Gia hạn / kết thúc sớm phiếu công tác | Assign | `extend_end_soon_requests` | `ExtendEndSoonRequest` | `status`: `CHO_DUYET=2` | "Trưởng phòng duyệt phiếu giao công tác" [H] (`canApprove` `:112`), không kiểm phòng | approve `Routes/ExtendEndSoonRequest/api.php:26`; reject `:27` | `/assign/extend-end-soon-request/:id/show` | KHÔNG | **97** | 2026-10-21 17:02:11 | Không | Đang dùng hằng ngày |
| AS23 | Loại giảm giá: duyệt danh mục | Assign | `discount_types` | `DiscountType` | `status`: `STATUS_PENDING=3` | "Quản lý danh mục loại giảm giá" [MW] | GET approve `api.php:1063` | `/assign/discount-types` | KHÔNG | **0** (1 dòng, active) | — | Không | Là danh mục do báo giá sinh ra, chờ duyệt kích hoạt. Không phải luồng phiếu, đề xuất loại khỏi tổng hợp |

**Tổng phiếu đang chờ, tính các luồng 1–22 (bỏ 23): 1.646**
= 35 + 1 + 9 + 1 + 1 + 2 + 16 + 118 + 20 + 13 + 292 + 1.041 + 97.

Nếu bỏ các luồng legacy 16–20 và 22 thì còn 66.

#### Bất thường

- **Quyền guard api không gán cho role nào** (đếm `role_has_permissions`): "Trưởng phòng duyệt gia hạn dự án TKT" và "Ban giám đốc duyệt gia hạn dự án TKT" (1 phiếu chờ bị kẹt), "Duyệt hợp đồng" (chỉ guard web có 21 role), "Kế toán kho" (chỉ guard web có 12 role). Các nút duyệt tương ứng trên HRM đang chết với mọi người dùng.
- **Fail-open (BE không chặn):**
  - Điều chỉnh giải pháp accept/reject (`api.php:408-409`): không kiểm quyền, không kiểm trạng thái.
  - Phiếu giao việc `AssignJobController` duyệt / duyệt KQ / từ chối: chỉ chặn quản lý quá hạn.
  - Duyệt bình luận task (`api.php:1095`).
- **Thiếu kiểm phạm vi phòng/công ty ở API thao tác** (danh sách chờ có lọc, API duyệt thì không):
  - Bàn giao approve/reject.
  - Yêu cầu giải pháp receive/reject.
  - Hợp đồng HRM approve/reject.
  - Hồ sơ thanh toán, Đề nghị thanh toán, Quyết toán HĐ, Gia hạn/kết thúc sớm.
- **Lệch cách tính quyền:** [MW] và [BM] dùng `getAllPermissions()` không lọc công ty, còn [H] lọc `role_has_permissions.company_id`. Báo giá dùng cả hai lớp, nên người có quyền ở công ty khác qua được middleware rồi bị service chặn.
- **Hở model_type:** cả 3 cách đều bỏ sót 1355 dòng role `App\Employee` (xem đầu file).
- **Trùng tên bảng `quotations`:** bảng trên DB gộp là của HRM (không có cột `quotation_type`). ERP vẫn còn `App\Quotation` (table mặc định `quotations`) cùng các lớp con `NormalQuotation`/`LiquidationQuotation`/`CostFixingQuotation` (`whereIn('quotation_type', …)`), vẫn được `QuotationsController`, `ContractsController`, `HomeController`… import. Màn ERP cũ nào còn chạy sẽ đọc nhầm bảng HRM hoặc lỗi cột.
- **Nhập nhằng số trạng thái trên `quotations`:** `status=2` là "Chờ TP duyệt" (BG thường) nhưng là "Chờ duyệt" (BG tổng). Mọi đếm phải tách theo `is_summary`.
- **`pages/assign/my-job` tab "Chờ duyệt": XÁC NHẬN dữ liệu gán cứng.** `my-job/index.vue:142` khai `badge: '4'`; `:148` khai `approvals: []`; `:336` gán lại `this.approvals = []`, không gọi API nào. `ApprovalsTab.vue:74` chỉ nhận prop mảng rỗng. Badge luôn hiện "4" nhưng bảng luôn trống.
- `AssignBusinessController::deny` (`AssignBusinessController.php:883-889`) gọi `$object->canApproveAssignBusiness()` trước `if (!$object)`, nên id không tồn tại sẽ ra lỗi 500 thay vì 404. `canApproveAssignBusiness` cũng cho duyệt phiếu đang ở trạng thái `DANG_TAO`.
- `bom_price_approval_configs` (`api.php:522`) chỉ là cấu hình ngưỡng cấp duyệt giá, không phải luồng. `contract_approver_histories` là bảng ERP (`app/Model/Sale/ContractApproveHistory.php`), Assign không đụng tới.
- `WarehouseExportRequest` / `WarehouseExport` (`STATUS_CHO_DUYET=2`) là bảng ERP do HRM tạo phiếu. Các route Assign không có API duyệt cho 2 bảng này nên không đưa vào bảng trên.

#### Mục mơ hồ cần nghiệp vụ quyết định

1. Các luồng legacy 16–20 và 22 (phiếu công tác, đề xuất công việc, giao việc, hồ sơ và đề nghị thanh toán, gia hạn/kết thúc sớm) có đưa vào màn tổng hợp chờ duyệt không? Riêng Đề nghị thanh toán chiếm 1.041 trên 1.646 phiếu.
2. 292 hồ sơ thanh toán (mới nhất 02/06/2026), 6 phiếu giao việc chờ duyệt KQ từ năm 2024, và 7 phiếu giao việc chờ duyệt (mới nhất 03/2026) là việc tồn thật hay rác cần đóng?
3. "Giải pháp chờ PM duyệt" và "Phiếu đề xuất công việc chờ giao việc" là bước *tiếp nhận/phân công*, không phải *duyệt*. Có tính là "chờ duyệt" không?
4. "Yêu cầu làm giải pháp chờ tiếp nhận" và "Mục bàn giao chờ tiếp nhận" có xếp vào nhóm duyệt không, hay để thành nhóm "Chờ tiếp nhận" riêng?
5. Yêu cầu xuất hàng: HRM chỉ có "Không duyệt", còn duyệt nằm bên ERP. Đưa vào tổng hợp của HRM, của ERP, hay cả hai? Ai là người duyệt khi quyền "Kế toán kho" guard api chưa có role nào?
6. Báo giá cấp 1 (tự duyệt): có xem là "chờ người lập tự duyệt" không? Hiện có 0 phiếu.
7. Các quyền đang có 0 role (gia hạn TKT TP/BGĐ, "Duyệt hợp đồng" api, "Kế toán kho" api): gán cho role nào? Hay đổi code sang dùng quyền guard web?
8. Duyệt bình luận task và duyệt loại giảm giá có bỏ khỏi phạm vi không? Đề xuất là bỏ.


---

## Phần 4 — Finance · CustomerCare · MasterData (hầu hết trên bảng ERP)

- Nguồn: `HRM/hrm-api` + `HRM/hrm-client` nhánh `gop_db` (working tree), DB `hrm_erp_21_10_prod` (dump prod 21/10/2026), chỉ chạy SELECT.
- Đường dẫn route viết tắt: `Fin` = `Modules/Finance/Routes/api.php`, `CC` = `Modules/CustomerCare/Routes/api.php`, `MD` = `Modules/MasterData/Routes/api.php`, `Asg` = `Modules/Assign/Routes/api.php`. Entity viết tắt từ `Modules/<Module>/Entities/`.
- Không bảng nào trong phạm vi có cột `deleted_at` (đã soát `information_schema`) ⇒ không có xoá mềm, đếm thẳng theo `status`. Phiếu "đã huỷ" có mã trạng thái riêng nên tự rơi khỏi bộ đếm.
- "Bảng thuộc ERP": căn cứ là migration tạo/sửa bảng nằm trong `ERP/TanPhatDev/database/migrations`.
- Kiểu gate, viết tắt trong bảng:
  - **CEP** = trait `Modules/Finance/Entities/Concerns/ChecksEmployeePermission`. Query thẳng `employee_has_permissions` + `employee_has_roles` (mọi model_type) + `role_has_permissions` theo TÊN quyền ⇒ **không sót** role `App\Employee`, nhưng **KHÔNG lọc `role_has_permissions.company_id`** và nhận cả quyền guard `web`. `currentEmployeeIsSuperAdmin()` = có role id 18 ⇒ nhiều luồng cho super admin vượt quyền.
  - **MW** = middleware `checkPermission:X` (spatie `getAllPermissions()` trên `Modules\Timesheet\Entities\Employee`) ⇒ **sót** role gán với model_type `App\Employee`. Không có ngoại lệ cho super admin.
  - **WRP** = `Modules/CustomerCare/Support/WarrantyRepairPermission::has()`, cũng là spatie `getAllPermissions()` ⇒ cùng lỗ hổng với MW.
  - **HLP** = helper toàn cục `isCurrentEmployeeHasPermission()` (`app/Helper/PermissionHelper.php:20`) hoặc `app/CommonServices/PermissionService`. Đi qua `$employee->roles` của spatie (sót `App\Employee`), có lọc `role_has_permissions.company_id = current_company_role`, bỏ qua `employee_has_permissions`.
  - `dueConfig:X,manager` chỉ chặn trưởng phòng có hàng quá hạn, KHÔNG phải gate quyền, nên không ghi vào cột "Ai duyệt".

### Số người giữ quyền duyệt trên DB (đọc số này cùng cột "Ai duyệt")

`all` = số NV có quyền qua role, mọi model_type (cách CEP thấy). `HRM-type` = chỉ role gán model_type `Modules\Timesheet\Entities\Employee` (cách MW/WRP/HLP thấy). `employee_has_permissions` không có dòng nào cho các quyền này. Có 7 NV giữ role 18 (super admin), đều mang model_type HRM.

| Quyền | id:guard | all | HRM-type |
|---|---|---|---|
| Kế toán kho | 1136:api, 100080:web | 75 | 3 (chỉ qua bản web) |
| Thủ quỹ duyệt phiếu thu | 1502:api, 100178:web | 46 | 2 |
| Quản lý phiếu báo có | 1542:api, 100243:web | 62 | 2 |
| Thủ quỹ duyệt phiếu chi / Kế toán trưởng duyệt phiếu chi | 1503 / 1504 api + web | 51 / 48 | 2 / 2 |
| Trưởng phòng duyệt yêu cầu nhập hàng | 1166:api, 100984:web | 40 | 0 |
| Ban kiểm soát duyệt giá nhập hàng trả lại / BGD duyệt giá nhập hàng trả lại | 1167 / 1168 api + web | 17 / 23 | 1 / 1 |
| Ban kiểm soát duyệt kết quả kiểm kê | 101059:api, 100474:web | 50 | 2 |
| Quản lý giữ hàng | **chỉ 100427:web** | 584 | 3 |
| Trưởng phòng / Ban giám đốc / Kế toán duyệt hàng giữ | **chỉ web** (100836/100837/100838) | 107 / 29 / 48 | 2 / 2 / 2 |
| TP / KT công nợ / KT trưởng / BGĐ duyệt đề nghị thanh toán | 1154/1155/1156/1157 api + web | 70 / 48 / 43 / 21 | 0 / 2 / 2 / 0 |
| Kế toán thanh toán | 1152:api, 100177:web | 55 | 2 |
| TP / BGĐ duyệt xuất hàng vượt hạn mức công nợ | 1572 / 1573 api + web | 39 / 28 | 0 / 1 |
| Trưởng phòng / Ban giám đốc duyệt hàng mượn | **chỉ web** (100842 / 100952) | 97 / 65 | 2 / 3 |
| Trưởng phòng duyệt yêu cầu mua dịch vụ / Ban kiểm soát duyệt giá mua dịch vụ | **chỉ web** (100814 / 100813) | 59 / 6 | 0 / 0 |
| Hạch toán mua dịch vụ | 1702:api, 100819:web | 41 | 2 (chỉ qua bản web) |
| Kế toán | **chỉ 100079:web** | 67 | 2 |
| Xử lý yêu cầu sửa chữa | 1510:api, 100412:web | 41 | **0** |
| Tạo phiếu cung cấp thông tin | 1514:api, 100413:web | 41 | **0** |
| Tạo phiếu giao việc | **chỉ 100417:web** | 41 | **0** |
| PTKD duyệt yêu cầu hỏi giá | 101106:api, 101003:web | 105 | 26 |
| XNK xử lý yêu cầu hỏi giá | 101107:api | 84 | 17 |
| Tính giá bán hàng hoá | 101108:api | 63 | 22 |
| Duyệt giá bán hàng hoá | 101104:api | 26 | 9 |

---

### Module Finance

| STT | Tên luồng (VN) | Module | Bảng | Entity | Cột trạng thái + giá trị chờ | Ai duyệt từng cấp | API duyệt/từ chối | URL chi tiết (client) | Màn "chờ duyệt" riêng | Số phiếu chờ (DB) | Phiếu chờ gần nhất | Bảng ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | **[ERP]** Yêu cầu chuyển hàng — Không duyệt | Finance | product_transfer_requests | ProductTransferRequest/ProductTransferRequest | `status` 2 = Chờ duyệt (`STATUSES`, không đặt tên hằng) | CEP `Kế toán kho` hoặc SA (role 18), VÀ công ty phiếu = công ty đang làm (`canApprove` :265) | reject Fin:312 (cố ý không gắn MW, comment :306-311) | pages/finance/product-transfer-requests/_id/index.vue | Không | **9** | 2026-10-21 15:58:44 | YES. ERP reject web.php:1023 | Bước "duyệt" thật = KT kho lập Phiếu điều chuyển (`/finance/product-transfers`), HRM không có endpoint approve riêng |
| F2 | **[ERP]** Phiếu thu — Thủ quỹ duyệt / Huỷ | Finance | bill_incomes | BillIncome/BillIncome + BillIncomeAccess | `status` 2 = `STATUS_AWAITING_APPROVE` | CEP `Thủ quỹ duyệt phiếu thu` hoặc SA (`isTreasurer` :178) | approve Fin:402 · cancel Fin:403 | pages/finance/bill-incomes/_id/index.vue | Không (menu gộp 1 màn, finance.js:103) | **0** | — (DB chỉ có status 3 và 4) | YES | `canApprove` không so công ty |
| F3 | **[ERP]** Phiếu báo có — Duyệt (ghi sổ) | Finance | bill_income_reports | BillIncomeReport/BillIncomeReport + Access | `status` 1 = `STATUS_CREATING`, duyệt từ trạng thái "Đang tạo" ⇒ 2 | CEP `Quản lý phiếu báo có` hoặc SA (`canManage` :212) | approve Fin:431 | pages/finance/bill-income-reports/_id/index.vue | Không | **0** | — (cả 4.798 phiếu đều =2) | YES. ERP có `/approved` web.php:6528 | Không có trạng thái "chờ" riêng |
| F4 | **[ERP]** Phiếu chi — Thủ quỹ / KT trưởng duyệt / Huỷ | Finance | bill_payments | BillPayment/BillPayment + BillPaymentAccess | `status` 2 = `STATUS_AWAITING_APPROVE` (chờ Thủ quỹ); 5 = `STATUS_AWAITING_ACCOUNTING_APPROVE` (chờ KT trưởng, nhánh B) | Cấp 5: CEP `Kế toán trưởng duyệt phiếu chi`. Cấp 2: CEP `Thủ quỹ duyệt phiếu chi`. Cả hai bắt buộc cùng công ty (`canApprove` :155), không vượt quyền SA | submit Fin:457 · approve Fin:458 · cancel Fin:459 | pages/finance/bill-payments/_id/index.vue | Không | **2** (st2 = 2, st5 = 0) | 2026-10-19 13:23:25 | YES. ERP duyệt qua PUT update đổi status (comment Fin:455) | — |
| F5 | **[ERP]** Yêu cầu nhập hàng — Không duyệt + 3 cấp duyệt giá | Finance | product_import_requests | ProductImportRequest/ProductImportRequest | `status` 12 `CHO_TP_DUYET` → 10 `CHO_BAN_KIEM_SOAT_DUYET` → 11 `CHO_BGD_DUYET`; 2 `CHO_DUYET` (chờ KT kho tiếp nhận) | TP: CEP `Trưởng phòng duyệt yêu cầu nhập hàng`/SA (:1113). BKS: CEP `Ban kiểm soát duyệt giá nhập hàng trả lại`/SA (:1123). BGĐ: CEP `BGD duyệt giá nhập hàng trả lại`/SA (:1133). Không duyệt ở st2: CEP `Kế toán kho`/SA; loại 6 chỉ người tạo; loại 7 thì người lập YCXH gốc cũng được (:1077, :1158) | deny Fin:566 · TP Fin:568 · BKS Fin:569 · BGĐ Fin:570 | pages/finance/product-import-requests/_id/index.vue | Không (bỏ preset từ 21/08, index.vue:235) | **36**: st12 = 9 (5 thường + 4 nhập thẳng), st10 = 0, st11 = 0, st2 = 27 (19 thường + 8 nhập thẳng) | st12: 2026-10-21 19:10:29 · st2: 2026-10-21 18:10:06 | YES. ERP deny/approve web.php:1411-1415 | **TP duyệt không kiểm phòng ban, không kiểm công ty**: ai có quyền đều duyệt được mọi phiếu chờ TP. 40 người giữ quyền TP, HRM-type = 0 |
| F6 | **[ERP]** Đề nghị nhập kho — Thủ kho từ chối / Người tạo huỷ | Finance | warehouse_import_requests | WarehouseImportRequest/WarehouseImportRequest | `status` 2 = `STATUS_CHO_DUYET` (đã gửi thủ kho) | Thủ kho của đúng kho (`warehouse_stockers.stocker_id`), hoặc role tên "super admin" (so theo TÊN role, `assertCanStockerApprove` WarehouseImportRequestController:999). Không dùng quyền | deny Fin:616 · cancel Fin:615 | pages/finance/warehouse-import-requests/_id/index.vue | Không | **50** | 2026-10-21 19:05:52 | YES. ERP deny web.php:1438 | Bước DUYỆT (lập phiếu nhập kho) không có route HRM, thủ kho làm trên ERP (comment Fin:612-613) |
| F7 | **[ERP]** Phiếu nhập kho — Không duyệt | Finance | warehouse_imports | WarehouseImport/WarehouseImport | `status` 2 = `CHO_DUYET` | CEP `Kế toán kho`/SA, cùng công ty (SA vượt cả điều kiện công ty), trừ các loại `NO_DENY_TYPES` (:261, :270) | deny Fin:650 · cancel Fin:651 | pages/finance/warehouse-imports/_id/index.vue | Không (KT kho lọc trạng thái Chờ duyệt, finance.js:153) | **12** | 2026-10-21 16:39:36 | YES. ERP deny web.php:1473 + excShortage approve :1494 | Duyệt/hạch toán không có route HRM riêng |
| F8 | **[ERP]** Phiếu kiểm kê theo hàng hoá — BKS duyệt / không duyệt kết quả | Finance (màn ở warehouse) | self_inventories | SelfInventory/SelfInventory | `status` 2 = `CHO_KT_DUYET` | CEP `Ban kiểm soát duyệt kết quả kiểm kê`/SA (:220). Không kiểm công ty | approve Fin:718 · reject Fin:719 | pages/warehouse/self-inventories/_id/index.vue | **Có**: `/warehouse/self-inventories?type=wait-approve` (finance.js:348) | **0** | — | YES. ERP approve/unApprove/stockApprove web.php:1790-1792 | DB có 1 phiếu status 0, ngoài STATUSES |
| F9 | **[ERP]** Kết quả kiểm kê theo vị trí — duyệt / không duyệt | Finance (màn ở warehouse) | position_inventories (global scope `type` = 1) | PositionInventory/PositionInventoryResult | `status` 2 = `CHO_DUYET` | CEP `Ban kiểm soát duyệt kết quả kiểm kê`/SA (:225) | approve Fin:766 · reject Fin:767 | pages/warehouse/position-inventory-results/_id/index.vue | Không | **0** (type 1: st3 = 30, st4 = 1, st5 = 44) | — | YES. ERP approve/unApprove web.php:1884-1885 | 13 phiếu type 0 (kế hoạch) đang st2, ngoài luồng này |
| F10 | **[ERP]** Phiếu chuyển hàng nhập thẳng — duyệt / không duyệt | Finance | product_import_direct_transfers | ProductImportDirectTransfer/ProductImportDirectTransfer | `status` 2 = `CHO_DUYET` | CEP `Kế toán kho`/SA, cùng công ty (:196) | approve Fin:845 · reject Fin:846 · (GET receivers Fin:835 chỉ là danh sách chọn Người nhận) | pages/finance/product-import-direct-transfers/_id/index.vue | Không (bỏ preset "Chờ tôi duyệt", index.vue:256) | **1** | 2026-10-21 15:20:02 | YES. ERP approve web.php:1002 | "Người nhận" KHÔNG có bước xác nhận |
| F11 | **[ERP]** Yêu cầu huỷ giữ — Không duyệt | Finance | prepick_cancel_requests | PrepickCancel/PrepickCancelRequest | `status` 2 = `CHO_DUYET` | CEP `Quản lý giữ hàng` (**chỉ guard web**)/SA (:214). Không kiểm công ty | reject Fin:879 | pages/finance/prepick-cancel-requests/_id/index.vue | Không | **1** | 2026-10-20 11:26:30 | YES. ERP deny web.php:1724 | Duyệt = lập Phiếu huỷ giữ (`/finance/prepick-cancels`) |
| F12 | **[ERP]** Gia hạn hàng giữ — 3 cấp | Finance | prepick_extend_requests | PrepickExtend/PrepickExtendRequest | `status` 5 `CHO_TP_DUYET` → 4 `CHO_BGD_DUYET` → 2 `CHO_KT_DUYET` | TP: CEP `Trưởng phòng duyệt hàng giữ` + phòng mình quản lý (`manageableDepartmentIds`). BGĐ: `Ban giám đốc duyệt hàng giữ`. KT: `Kế toán duyệt hàng giữ`. Cả 3 đều chỉ có guard web, đều cùng công ty, SA vượt (:211-244) | approve (1 endpoint/3 cấp) Fin:909 · reject Fin:910 | pages/finance/prepick-extend-requests/_id/index.vue | Không | **4**: TP = 0, BGĐ = 1, KT = 3 | BGĐ: 2026-10-21 15:40:51 · KT: 2026-10-21 12:04:53 | YES. ERP deny/approve web.php:1996-1997 | — |
| F13 | **[ERP]** Yêu cầu xuất giữ — TP/BGĐ duyệt, không duyệt | Finance | product_prepick_requests | PrepickExport/ProductPrepickRequest | `status` 6 `CHO_TP_DUYET` → 4 `CHO_BGD_DUYET` → 2 `CHO_KT_DUYET` | TP: `Trưởng phòng duyệt hàng giữ` + phòng quản lý. BGĐ: `Ban giám đốc duyệt hàng giữ`. KT (chỉ để không duyệt): `Kế toán duyệt hàng giữ`. Cả 3 chỉ guard web, CEP, cùng công ty, SA vượt (:358-405) | approve (TP/BGĐ) Fin:949 · reject Fin:951 | pages/finance/product-prepick-requests/_id/index.vue | Không | **6**: TP = 2, BGĐ = 1, KT = 3 | TP: 2026-10-21 16:15:56 · KT: 2026-10-21 14:57:30 | YES. ERP approve/deny web.php:1130-1131 | Cấp KT st2 đi tiếp bằng màn Phiếu xuất giữ (`warehouse-prepick-requests`) |
| F14 | **[ERP]** Điều chuyển hàng giữ — 3 cấp | Finance | prepick_transfer2 | PrepickTransfer/PrepickTransferRequest | `status` 5 `CHO_TP_DUYET` → 4 `CHO_BGD_DUYET` → 2 `CHO_KT_DUYET` | Như F12. TP xét phòng của NV NHẬN (`toEmployeeDepartmentId`) (:239-277) | approve Fin:1013 · reject Fin:1014 | pages/finance/prepick-transfer-requests/_id/index.vue | Không | **2**: TP = 1, BGĐ = 0, KT = 1 | KT: 2026-10-21 11:45:38 · TP: **2025-10-27** (tồn gần 1 năm) | YES (ERP model `PrepickTransfer2`). ERP approve web.php:1385 | — |
| F15 | **[ERP]** Đề nghị thanh toán — 5 vai duyệt + không duyệt | Finance | bill_payment_requests | BillPaymentRequest/BillPaymentRequest | `status` 2 `STATUS_AWAITING_MANAGE` → 3 `_ACCOUNTING_DEPT` → 4 `_CHIEF_ACCOUNTANT` → 5 `_BOARD_OF_MANAGER` → 6 `_CREATE_BILL_PAYMENT` | st2: CEP `Trưởng phòng duyệt đề nghị thanh toán` + `employee_manage_departments` cùng công ty. st3: `Kế toán công nợ duyệt đề nghị thanh toán`. st4: `Kế toán trưởng duyệt đề nghi thanh toán`. st5: `Ban giám đốc duyệt đề nghi thanh toán`. st6: `Kế toán thanh toán`. Tất cả bắt buộc cùng công ty, không vượt quyền SA (`canApproveAtCurrentStatus` :875) | approve Fin:1093 · không duyệt = change-status Fin:1094 · danh sách chờ GET Fin:1067 | pages/finance/bill-payment-requests/_id/index.vue | **Có**: `/finance/bill-payment-requests?mode=pending` (finance.js:577) | **195**: st2 = 8, st3 = 60, st4 = 70, st5 = 1, st6 = 56 | 2026-10-21 17:58:00 | YES. ERP for-approved/change-status web.php:6593, :6609 | Bảng giữ nhiều phiếu chờ nhất. Cùng 1 người có thể giữ nhiều vai |
| F16 | **[ERP]** Yêu cầu xuất bán hàng mượn — TP/BGĐ duyệt, không duyệt | Finance | borrow_sell_requests | BorrowSellRequest/BorrowSellRequest | `status` 10 `CHO_TP_DUYET` → 11 `CHO_BGD_DUYET`; 2 `CHO_KE_TOAN_KHO` | TP: CEP `Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ` + phòng quản lý. BGĐ: `Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ`. KT kho (chỉ để không duyệt): `Kế toán kho`. Không vượt SA, không kiểm công ty (:156-181) | deny Fin:1244 · TP Fin:1245 · chuyển BGĐ Fin:1246 · BGĐ Fin:1247 | pages/finance/borrow-sell-requests/_id/index.vue | Một nửa: `?type=waiting_approve` có trong index.vue:189 nhưng không có mục menu | **0** (DB chỉ có st1 và st4) | — | YES. ERP managerApprove/deny web.php:1142, :1153 | Bước KT kho = lập Phiếu xuất bán hàng mượn (`borrow-sells`) |
| F17 | **[ERP]** Gia hạn hàng mượn — 3 cấp | Finance | borrow_extend_requests | BorrowExtend/BorrowExtendRequest | `status` 4 `CHO_TP_DUYET` → 5 `CHO_BGD_DUYET` → 2 `CHO_KT_DUYET` | TP: `Trưởng phòng duyệt hàng mượn` + phòng quản lý. BGĐ: `Ban giám đốc duyệt hàng mượn` (cả 2 chỉ guard web). KT: `Kế toán kho`. CEP, cùng công ty, SA vượt (:219-260) | approve Fin:1326 · reject Fin:1328 | pages/finance/borrow-extend-requests/_id/index.vue | **Có**: `?type=for-approve` (finance.js:623) | **2**: TP = 0, BGĐ = 1, KT = 1 | BGĐ: 2026-10-21 09:28:54 · KT: 09:01:27 | YES. ERP deny/approve web.php:2012-2013 | — |
| F18 | **[ERP]** Yêu cầu vận chuyển — Thủ kho duyệt / từ chối | Finance | delivery_requests | DeliveryRequest/DeliveryRequest | `status` 2 = `STATUS_AWAITING_APPROVE` | Thủ kho của các kho trong YCXH nguồn (`isCurrentStocker` :323) hoặc SA (:415). Không dùng quyền | approve Fin:1351 · reject Fin:1352 | pages/finance/delivery-requests/_id/index.vue | Không | **0** (**bảng rỗng, 0 dòng**) | — | YES. ERP for-approve/approve/reject web.php:6459-6461 | Có màn ERP "for-approve" nhưng HRM chưa có |
| F19 | **[ERP]** Yêu cầu xuất mượn — Không duyệt | Finance | borrow_export_requests | BorrowExport/BorrowExportRequest | `status` 2 = `CHO_DUYET` | CEP `Kế toán kho`/SA (`isAccountant`, :259). Không kiểm công ty | reject Fin:1478 | pages/finance/borrow-export-requests/_id/index.vue | Không (menu `?type=accounting`, finance.js:214) | **0** | — | YES. ERP deny web.php:1182 | Duyệt = lập Phiếu xuất mượn (`borrow-exports`) |
| F20 | **[ERP]** Yêu cầu mua dịch vụ — TP + BKS duyệt | Finance | buy_service_requests | BuyServiceRequest/BuyServiceRequest | `status` 2 `CHO_TP_DUYET` → 3 `CHO_KS_DUYET` | TP: CEP `Trưởng phòng duyệt yêu cầu mua dịch vụ`/SA. **Không kiểm phòng, không kiểm công ty** (:291). BKS: `Ban kiểm soát duyệt giá mua dịch vụ`/SA, cùng công ty (:298). Cả 2 chỉ guard web | TP Fin:1547 · BKS Fin:1549 · gửi BKS lại Fin:1550 · huỷ Fin:1551 · không duyệt Fin:1552 | pages/finance/buy-service-requests/_id/index.vue | Không | **0** (st2 = 0, st3 = 0) | — | YES. ERP reject/departmentApprove/ksApprove web.php:3097-3099 | — |
| F21 | **[ERP]** Yêu cầu hạch toán mua dịch vụ — Không duyệt | Finance | buy_service_accounting_requests | BuyServiceAccountingRequest/BuyServiceAccountingRequest | `status` 2 = `CHO_DUYET` | **2 lớp gate**: MW `checkPermission:Hạch toán mua dịch vụ` (Fin:1583) rồi CEP `canAccounting()` | reject Fin:1582 | pages/finance/buy-service-accounting-requests/_id/index.vue | Không | **2** | 2026-10-19 10:53:12 | YES. ERP reject web.php:3133 | Lớp MW chỉ cho 2/41 người giữ quyền qua (HRM-type) |
| F22 | **[ERP]** Đề nghị thu tiền — KT không duyệt | Finance | bill_income_requests | BillIncomeRequest/BillIncomeRequest | `status` 2 = `STATUS_AWAITING_APPROVE` (Chờ KT duyệt) | CEP `Kế toán thanh toán`/SA (`isAccountant`, :619) | change-status Fin:382 | pages/finance/bill-income-requests/_id/index.vue | **Có**: pages/finance/bill-income-requests/pending.vue | **3** | 2026-10-21 19:53:28 | YES. ERP approved/change-status web.php:6495, :6506 | Ngoài danh sách được giao. Duyệt = lập Phiếu thu |
| F23 | **[ERP]** Yêu cầu điều chỉnh công nợ — KT từ chối | Finance | bill_adjust_dept_requests | BillAdjustDeptRequest/BillAdjustDeptRequest | `status` 2 = `STATUS_AWAITING_APPROVE` | CEP `Kế toán thanh toán`, cùng công ty (:474) | change-status Fin:1128 | pages/finance/bill-adjust-dept-requests/_id/index.vue | **Có**: `?mode=pending` (finance.js:593) | **26** | 2026-10-21 19:50:48 | YES. ERP change-status web.php:6568 | Ngoài danh sách được giao |
| F24 | **[ERP]** Yêu cầu hạch toán bổ sung — KT từ chối | Finance | addition_accounting_requests | AdditionAccountingRequest/AdditionAccountingRequest | `status` 2 = `STATUS_AWAITING_APPROVE` | CEP `Kế toán thanh toán` (+ `Kế toán`, chỉ guard web, cho phạm vi hỗ trợ), đúng công ty hoặc phạm vi hỗ trợ (:685) | change-status Fin:1218 | pages/finance/addition-accounting-requests/_id/index.vue | **Có**: `?mode=pending` (finance.js:585) | **39** | 2026-10-21 16:23:20 | YES. ERP reject web.php:6658 | Ngoài danh sách được giao |
| F25 | **[ERP]** Yêu cầu xuất hàng (YCXH) — KT kho không duyệt | Assign (màn ở finance) | product_export_requests | Modules/Assign/Entities/Warehouse/ProductExportRequest | `status` 2 = `STATUS_CHO_DUYET`; 10 = `STATUS_DOI_TP_DUYET`, 11 = `STATUS_DOI_BGD_DUYET` | Không duyệt st2: **HLP** `isCurrentEmployeeHasPermission('Kế toán kho')`, cùng công ty (loại 7 so `export_company_id`) (:358). **TP/BGĐ: HRM KHÔNG có route** | reject Asg:747 (lập đề nghị xuất kho Asg:736-737) | pages/finance/product-export-requests/_id/index.vue | Không | **17**: st2 = 16, st10 = 1 (id 44418), st11 = 0 | st2: 2026-10-21 15:45:57 · st10: 2026-10-21 14:53:40 | YES. ERP managerApprove/deny web.php:1034, :1061 | HLP chỉ thấy 3/75 người giữ `Kế toán kho`. Phiếu st10 chỉ duyệt được trên ERP |

**Điểm bất thường — Finance**
- **Vượt quyền super admin (role 18) có ở nhiều luồng**, trái quy tắc đã chốt "Super admin không mặc định có quyền": F1, F2, F3, F5, F7, F8, F9, F10, F11, F12, F13, F14, F17, F18, F19, F20, F22. F6 cũng vượt, nhưng so theo TÊN role "super admin" (`LOWER(roles.name)`), không theo id 18. Không vượt: F4, F15, F16, F21 (lớp MW), F25.
- **CEP không lọc `role_has_permissions.company_id`**: được cấp quyền ở công ty A là dùng được ở mọi công ty. Một số luồng bù bằng điều kiện "công ty phiếu = công ty đang làm" (F1, F4, F7, F10, F12-F15, F17, F20 cấp BKS, F23). Các luồng **không có điều kiện công ty nào**: F2, F3, F5 (cả 3 cấp + không duyệt), F8, F9, F11, F16, F19, F20 cấp TP, F22.
- **Duyệt cấp trưởng phòng không kiểm phòng ban**: F5 (TP duyệt yêu cầu nhập hàng) và F20 (TP duyệt mua dịch vụ) chỉ xét quyền. Ai có quyền đều duyệt được phiếu của mọi phòng, mọi công ty.
- **Quyền chỉ có guard web (ERP) nhưng HRM dùng làm gate**: `Quản lý giữ hàng`, `Trưởng phòng/Ban giám đốc/Kế toán duyệt hàng giữ`, `Trưởng phòng/Ban giám đốc duyệt hàng mượn`, `Trưởng phòng duyệt yêu cầu mua dịch vụ`, `Ban kiểm soát duyệt giá mua dịch vụ`, `Kế toán`. CEP so theo tên nên vẫn chạy, nhưng màn phân quyền HRM (guard api) **không cấp hay gỡ được** các quyền này.
- **F21 bị 2 lớp gate**: lớp MW spatie chặn 39/41 người giữ quyền `Hạch toán mua dịch vụ` (role ERP mang `App\Employee`). F25 dùng HLP: chỉ 3/75 kế toán kho bấm được "Không duyệt".
- **Thiếu endpoint HRM ở chỗ đang có phiếu chờ**: YCXH st10 (1 phiếu chờ TP duyệt vượt hạn mức) chỉ duyệt được trên ERP. Bước "duyệt/tiếp nhận" của F1, F6, F7, F11, F16 (st2), F19, F21 là lập chứng từ kế tiếp, chủ yếu vẫn làm trên ERP.
- **Hai cổng song song**: mọi luồng Finance ở trên vẫn còn route duyệt/từ chối riêng trên ERP (`web.php`), không có middleware chuyển hướng kiểu `productMovedToHrm` ⇒ cùng một phiếu duyệt được ở cả 2 nơi.
- **Dữ liệu tồn lâu**: `prepick_transfer2` có 1 phiếu chờ TP từ 2025-10-27. `delivery_requests` rỗng (0 dòng) dù ERP có màn for-approve.
- `self_inventories` có 1 dòng `status = 0`, không thuộc `STATUSES`.

---

### Module CustomerCare

| STT | Tên luồng (VN) | Module | Bảng | Entity | Cột trạng thái + giá trị chờ | Ai duyệt từng cấp | API duyệt/từ chối | URL chi tiết (client) | Màn "chờ duyệt" riêng | Số phiếu chờ (DB) | Phiếu chờ gần nhất | Bảng ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | **[ERP]** Yêu cầu đi kiểm tra SC-BH — Phòng tiếp nhận từ chối / chuyển phòng | CustomerCare | warranty_repair_requests | WarrantyRepairRequest/WarrantyRepairRequest | `status` 2 = `STATUS_WAITING_HANDLE`, và chưa có phiếu xử lý | MW `checkPermission:Xử lý yêu cầu sửa chữa` (CC:265, CC:267), rồi WRP cùng quyền + `department_reception_id` = phòng của user. SA (role 18) vượt điều kiện phòng (:289-315) | reject CC:264 · transfer-department CC:266 | pages/customer-care/warranty-repair-requests/_id/index.vue | Không (menu `?type=all`) | **137** (st2, chưa có phiếu xử lý) | 2026-10-21 19:19:30 | YES. ERP reject web.php:5972 | **0 người HRM-type giữ quyền** ⇒ thực tế chỉ ai có quyền gán qua role HRM (hiện 0) mới qua được MW |
| C2 | **[ERP]** Phiếu xử lý yêu cầu — Không duyệt (người lập CCTT) | CustomerCare | warranty_repair_handle_requests | WarrantyRepairHandleRequest/WarrantyRepairHandleRequest | `status` 2 = `STATUS_AWAIT_INFORMATION` (Chờ CCTT) | MW `checkPermission:Tạo phiếu cung cấp thông tin` (CC:299) + WRP cùng quyền (:201-210) | reject CC:298 | pages/customer-care/warranty-repair-handle-requests/_id/index.vue | Không | **27** | 2026-08-25 13:47:34 (gần 2 tháng không có phiếu mới) | YES. ERP reject web.php:5990 | 0 người HRM-type giữ quyền. `STATUS_AWAIT_EXTEND_INFORMATION` = 4 không được tính là chờ |
| C3 | **[ERP]** Phiếu cung cấp thông tin — Từ chối tiếp nhận (người lập YC) | CustomerCare | wr_service_quotations (`type` = 0) | WrServiceQuotation/WrServiceQuotation | `status` 2 = `STATUS_WAITING_QUOTATION` | Không dùng quyền: chỉ **người lập Phiếu yêu cầu gốc** (`warrantyRepairRequest.created_by`), và phiếu phải có dòng sửa chữa, mỗi thiết bị ≤ 1 lỗi (:399-442) | reject CC:332 (cố ý không gắn MW, comment CC:331) | pages/customer-care/wr-information-requests/_id/index.vue | Một phần: `?type=waiting_create_quotation` (sale-hub.js:96) | **4.686** (1.617 phiếu năm 2025, 3.069 phiếu năm 2026) | 2026-10-21 17:10:34 | YES | **Số rất lớn, nghi là tồn đọng không bao giờ đóng** (gần bằng 4.544 phiếu bảo hành type 2). Đây là hàng chờ "làm báo giá" của người lập, không phải hàng chờ duyệt |
| C4 | **[ERP]** Hợp đồng dịch vụ SC-BH — Duyệt / Không duyệt / Huỷ duyệt | CustomerCare | wr_service_contracts (`type` = 1) | WrServiceContract/WrServiceContract | `status` 2 = `HD_WAITING`; huỷ duyệt tính từ 3 = `HD_EFFECTIVE` | Duyệt/không duyệt: `approver_id` nếu có, không thì trưởng phòng quản lý `department_id`. SA vượt. **Không dùng quyền** (`getIsCanApproveAttribute` :376). Huỷ duyệt: TP quản lý phòng/SA, và chưa có chứng từ sau (:399) | approve CC:369 · reject CC:370 · un-approve CC:371 · close CC:372 | pages/customer-care/wr-service-contracts/_id/index.vue | **Có**: `?type=for-approve` (sale-hub.js:305) | **0** (type 1, st2) | — | YES. ERP approve/reject/unApproveContract web.php:6032, :6034, :6044 | Phụ lục type 3 đang có **1 phiếu st2** (2026-10-21 19:16:02) nhưng HRM chỉ duyệt type 1 |
| C5 | **[ERP]** Hợp đồng dịch vụ — Phòng tiếp nhận từ chối tiếp nhận / đổi phòng | CustomerCare | wr_service_contracts (`type` = 1) | WrServiceContract/WrServiceContract | `status` 3 = `HD_EFFECTIVE` + có `department_reception_id` + chưa có `wr_assign_tasks` (trừ status 9) | Từ chối: WRP `Tạo phiếu giao việc` (**chỉ guard web**) + đúng phòng tiếp nhận, SA vượt (:457). Đổi phòng: người lập HĐ (:436) | reject-reception CC:375 · change-reception CC:374 | như C4 | Không | **243** | 2026-10-21 15:45:50 | YES | 0 người HRM-type giữ `Tạo phiếu giao việc`. Số 243 có thể gồm HĐ cũ đã làm ngoài hệ thống |

**Điểm bất thường — CustomerCare**
- **Toàn bộ gate theo quyền của CustomerCare dùng spatie (MW + WRP)**. Trên DB, cả 3 quyền `Xử lý yêu cầu sửa chữa`, `Tạo phiếu cung cấp thông tin`, `Tạo phiếu giao việc` đều có **0 người giữ qua role HRM-type** (41 người giữ qua role `App\Employee`), và `employee_has_permissions` rỗng ⇒ C1, C2 và nút từ chối tiếp nhận của C5 trả 403 cho cả 41 người. C1 và C5 vẫn có ngoại lệ SA bên trong Entity, nhưng lớp MW ở C1/C2 không có ngoại lệ SA. Chưa kiểm spatie có lọc thêm theo guard hay không.
- `Tạo phiếu giao việc` chỉ có bản guard web ⇒ màn phân quyền HRM không cấp được.
- C4 và C5 cho SA vượt điều kiện phòng/approver (trái quy tắc super admin).
- C3 có 4.686 phiếu "Chờ làm báo giá", phần lớn tồn từ trước. Không nên coi là phiếu chờ duyệt thật.
- Hai cổng: ERP còn đủ route reject/approve cho 4 chứng từ (web.php:5972, :5990, :6032-6044).

---

### Module MasterData

| STT | Tên luồng (VN) | Module | Bảng | Entity | Cột trạng thái + giá trị chờ | Ai duyệt từng cấp | API duyệt/từ chối | URL chi tiết (client) | Màn "chờ duyệt" riêng | Số phiếu chờ (DB) | Phiếu chờ gần nhất | Bảng ERP? | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | **[ERP]** Yêu cầu hỏi giá (YCHG) — PTKD duyệt / không duyệt | MasterData (màn ở sale) | price_asking_requests | PriceCalculation/PriceAskingRequest | `status` 2 = `STATUS_WAITING_PTKD` | MW `checkPermission:PTKD duyệt yêu cầu hỏi giá` (MD:372, MD:374), rồi HLP/PermissionService cùng quyền + phiếu thuộc công ty đang làm (`PriceAskingAccess::canPtkd` :119). Không vượt SA | approve MD:371 · reject MD:373 | pages/sale/price-asking-requests/_id/index.vue | Không | **5** | 2026-10-21 16:39:46 | YES (ERP model `Order/PriceAskingRequest`). Route ERP web.php:2260-2262 đã chuyển sang HRM bằng `productMovedToHrm` | Người giữ quyền theo HRM-type: 26/105 |
| M2 | **[ERP]** Hàng tạm trong YCHG — PTKD đồng ý / không duyệt | MasterData | product_company_coefficients (cột `status` do HRM thêm, migration 2026_10_04) | Product/ProductCompany (ghi qua `PriceAskingRequestWriter::setTempStatus`) | `status` 6 = `STATUS_TEMP` (chờ PTKD); 7 = đã đồng ý, chờ duyệt phiếu | MW `PTKD duyệt yêu cầu hỏi giá` (group MD:376) + service kiểm công ty phiếu | temp approve MD:381 · temp reject MD:382 (lưu nháp MD:380) | pages/sale/price-asking-requests/_id/temp/_productId.vue | Không | **1** (st6) · st7 = 0 | 2026-10-21 16:38:20 | YES (bảng ERP, cột status do HRM thêm) | — |
| M3 | Nhóm hàng của YCHG — XNK duyệt / báo không có giá / huỷ | MasterData | price_asking_request_groups | PriceCalculation/PriceAskingRequestGroup | `status` 5 = `STATUS_WAITING_XNK` (chờ XNK duyệt); 1 = `STATUS_WAITING_YCTG` (XNK đã duyệt, chờ lập YCTG) | MW `XNK xử lý yêu cầu hỏi giá` (MD:384) + là XNK phân công HIỆN HÀNH theo thương hiệu × hãng × công ty (`isGroupXnk` :145) | group approve MD:385 · no-price MD:386 · cancel MD:387 | pages/sale/price-asking-requests/_id/index.vue | Không | **24** (st5, phiếu cha đang ở `ASKING_STATUSES`) · thêm 51 nhóm st1 chờ lập YCTG | 2026-10-21 17:29:20 | **NO** (bảng HRM, migration 2026_10_11) | Ngoài ra 583 nhóm `status` NULL (theo quy ước của mã, NULL cũng được tính là đang ở bước XNK) |
| M4 | **[ERP]** Yêu cầu tính giá (YCTG) — KTMH từ chối | MasterData | price_calculate_requests | PriceCalculation/PriceCalculateRequest | `status` 2 = `STATUS_WAITING` (chờ tính giá); 6 = `STATUS_WAITING_APPROVAL` | MW `Tính giá bán hàng hoá` (MD:409) + `PriceCalculateRequestAccess::canReject` (:147: st2, công ty đang làm, nhóm chưa đóng) | reject MD:409 | pages/sale/price-calculate-requests/_id/index.vue | Không | **5** (st2) · st6 = 0 | 2026-10-21 16:12:57 | YES (ERP model `Order/PriceCalculateRequest`). ERP reject web.php:2278 đã chuyển sang HRM | Người giữ quyền theo HRM-type: 22/63 |
| M5 | **[ERP]** Duyệt giá bán (yêu cầu theo hàng × ĐVT × công ty) — duyệt / không duyệt / hàng loạt | MasterData (màn ở finance) | product_approves (+ product_approve_prices) | Product/ProductApprove, Product/ProductApprovePrice | **Có dòng là đang chờ** (xử lý xong thì XOÁ CỨNG pa + pap). Cột `status` không dùng (NULL) | MW `checkPermission:Duyệt giá bán hàng hoá` trên cả group (MD:438). Phạm vi: `pa.company_id` = công ty đang làm (`ProductPriceApprovalService::query` :264) | bulk approve MD:445 · bulk reject MD:446 · approve MD:447 · reject MD:448 | (không có trang chi tiết, xử lý ngay trên danh sách) | **Có**: pages/finance/product-price-approvals/index.vue (menu finance.js:461 và :610) | **1** (id 1, sản phẩm 51682, công ty 8, 6 dòng giá) | 2026-10-12 15:30:28 | YES (ERP `ProductApprovePrice`). Route ERP web.php:596 đã chuyển sang HRM | Người giữ quyền theo HRM-type: 9/26 |

**Điểm bất thường — MasterData**
- Mọi gate MasterData đều qua spatie (MW + HLP/PermissionService có lọc công ty) ⇒ sót người giữ quyền qua role `App\Employee`: PTKD 26/105, XNK 17/84, Tính giá 22/63, Duyệt giá bán 9/26. Ưu điểm so với CEP: lọc đúng `role_has_permissions.company_id`, và không vượt quyền SA.
- `PTKD duyệt yêu cầu hỏi giá` có cả bản web (101003) lẫn api (101106). 9 người HRM-type chỉ có bản web.
- MasterData là module duy nhất mà route ERP tương ứng đã khoá bằng `productMovedToHrm`, nên không bị duyệt ở 2 nơi.
- `product_approves` dùng kiểu "có dòng là chờ" (xử lý xong xoá cứng) ⇒ không truy được lịch sử duyệt từ bảng này.

---

### Mục mơ hồ cần nghiệp vụ quyết định

1. **Super admin vượt quyền** ở khoảng 20 luồng (F1-F20, C1, C4, C5): giữ như ERP hay bỏ theo quy tắc "SA không mặc định có quyền"? Riêng F6 nhận SA theo TÊN role, cần thống nhất với cách nhận theo id 18.
2. **Trưởng phòng duyệt yêu cầu nhập hàng (F5) và TP duyệt mua dịch vụ (F20)** không giới hạn theo phòng/công ty. ERP có chủ đích như vậy không, hay phải giới hạn theo `employee_manage_departments` như F12-F17?
3. **Quyền theo công ty**: CEP bỏ qua `role_has_permissions.company_id`. Người được cấp `Kế toán kho` ở công ty A có được thao tác phiếu công ty B khi đang làm ở B không (với F5, F8, F9, F11, F16, F19, F22 thì hiện là ĐƯỢC)?
4. **Quyền chỉ có guard web** (hàng giữ, hàng mượn, mua dịch vụ, `Kế toán`, `Quản lý giữ hàng`, `Tạo phiếu giao việc`): tạo bản guard api để quản lý trên HRM, hay tiếp tục quản lý trên ERP?
5. **CustomerCare C1, C2, C5 thực tế bị khoá cho mọi người** (0 người HRM-type giữ quyền): sửa gate sang CEP, hay gán lại role trên HRM?
6. **F21 và F25**: bỏ lớp MW/HLP (đang chặn 39/41 và 72/75 người giữ quyền) để chỉ còn gate trong Entity?
7. **Bước "duyệt" thật của F1, F6, F7, F11, F16, F19, F21, F22** là lập chứng từ kế tiếp. Màn "chờ duyệt" tổng hợp có tính những phiếu này là "chờ" không, và ai là người chờ (KT kho / thủ kho)?
8. **YCXH chờ TP/BGĐ (st10/11)**: HRM chưa có route duyệt, 1 phiếu đang chờ (id 44418). Port sang HRM hay để ERP xử lý?
9. **Hợp đồng dịch vụ, phụ lục (type 3/4) st2**: HRM chỉ duyệt type 1, trong khi có 1 phụ lục đang chờ. Ai duyệt phụ lục?
10. **C3 (4.686 phiếu "Chờ làm báo giá") và C5 (243 HĐ chờ tiếp nhận)** có phải tồn đọng cần dọn/đóng hàng loạt trước khi đưa vào màn chờ duyệt không?
11. **Hai cổng duyệt**: các luồng Finance và CustomerCare vẫn duyệt được trên ERP. Có khoá phía ERP (kiểu `productMovedToHrm`) không?
12. **Màn chờ duyệt còn thiếu**: Borrow-sell `?type=waiting_approve` có trang nhưng không có mục menu. Delivery-requests ERP có màn for-approve còn HRM không có (bảng hiện rỗng).
13. **Phiếu tồn lâu**: `prepick_transfer2` có 1 phiếu chờ TP từ 2025-10-27, `warranty_repair_handle_requests` có 27 phiếu chờ CCTT không có phiếu mới từ 25/08. Xử lý tay hay huỷ?

---

### Tổng hợp nhanh

- Số luồng kiểm kê: 35 (25 Finance/Assign + 5 CustomerCare + 5 MasterData).
- Trên bảng ERP: 34/35 (chỉ M3 `price_asking_request_groups` là bảng HRM).
- Luồng có phiếu chờ > 0: 26 (F1, F4-F7, F10-F15, F17, F21-F25, C1-C3, C5, M1-M5).
- Tổng phiếu chờ (đếm theo định nghĩa cột "Số phiếu chờ"): Finance 407 (F1 9 + F4 2 + F5 36 + F6 50 + F7 12 + F10 1 + F11 1 + F12 4 + F13 6 + F14 2 + F15 195 + F17 2 + F21 2 + F22 3 + F23 26 + F24 39 + F25 17) · CustomerCare 5.093 (C1 137 + C2 27 + C3 4.686 + C5 243) · MasterData 36 (M1 5 + M2 1 + M3 24 + M4 5 + M5 1) ⇒ **5.536**. Nếu bỏ C3 (nghi tồn đọng) thì còn **850**.


---

## Tổng kết

### Số liệu theo phần

AS14 (Yêu cầu xuất hàng) trùng với F25 nên chỉ tính một lần, ở F25.

| Phần | Số dòng kiểm kê | Luồng có phiếu chờ > 0 | Tổng phiếu đang chờ | Luồng trên bảng ERP |
|---|---|---|---|---|
| Timesheet (H1–H11) | 11 | 10 | 1.273 | 0 |
| Human (H12–H13) | 2 | 1 | 13 | 0 |
| Payroll (H14–H15) | 2 | 0 | 0 | 0 |
| Meeting (H16–H17) | 2 | 0 | 0 | 0 |
| Training (H18–H26) | 9 | 4 | 3.693 (riêng H22 điểm danh: 3.631) | 0 |
| Rice | 0 (không có luồng duyệt) | — | — | — |
| Decision (QĐ1–QĐ22) | 22 | 2 | 2 | 0 |
| Assign (AS1–AS23, bỏ AS14) | 22 | 12 | 1.630 (riêng legacy: 1.581) | 0 (bảng của HRM; ERP chỉ có model đọc) |
| Finance (F1–F25) | 25 | 17 | 407 | 25 |
| CustomerCare (C1–C5) | 5 | 4 | 5.093 (riêng C3: 4.686) | 5 |
| MasterData (M1–M5) | 5 | 5 | 36 | 4 (trừ M3) |
| **Tổng** | **105** | **55** | **12.147** | **34** |

- **Không phải luồng duyệt phiếu, nên loại khỏi màn tổng hợp (5 dòng):**
  - H17: yêu cầu dịch vụ phòng họp.
  - H26: công bố kết quả thi offline.
  - AS13: duyệt bình luận task.
  - AS23: duyệt loại giảm giá.
  - QĐ22: hợp đồng đào tạo, không có trạng thái chờ và route trỏ tới hàm không tồn tại.

  Bỏ 5 dòng này thì còn **100 luồng ứng viên**.
- **Lượng tồn nghi là rác hoặc tồn đọng** chiếm phần lớn tổng số:
  - C3: 4.686 phiếu "Chờ làm báo giá".
  - H22: 3.631 yêu cầu điểm danh học viên.
  - Assign legacy, 1.581 phiếu:
    - AS20 Đề nghị thanh toán công tác: 1.041
    - AS19 Hồ sơ thanh toán: 292
    - AS16 Phiếu đề xuất/công tác: 118
    - AS22 Gia hạn/kết thúc sớm: 97
    - AS17 Phiếu đề xuất công việc: 20
    - AS18 Phiếu giao việc: 13

  Bỏ 3 nhóm này thì còn khoảng **2.249 phiếu**. Trong số còn lại vẫn có nhiều phiếu đã quá hạn duyệt, BE không cho duyệt nữa:
  - H5 Phiếu yêu cầu làm thêm: 131
  - H6 Đăng ký làm thêm: 212
  - H3 Đi muộn về sớm: 28
- **Luồng tồn nhiều nhất còn sống**:
  - F15 Đề nghị thanh toán: 195
  - H8 Phiếu giao việc chấm công: 521
  - H9 Phiếu đi công tác: 225
  - C5 HĐ dịch vụ chờ tiếp nhận: 243
  - C1 Yêu cầu sửa chữa: 137
  - H7 Tra soát công: 54
  - F6 Đề nghị nhập kho: 50
  - AS1 Báo giá BOM chờ TP: 35
  - F5 Yêu cầu nhập hàng: 36
  - H1 Đơn xin nghỉ: 33

### 34 luồng trên bảng ERP (trùng với `inventory-erp.md`)

- **Gồm**: F1–F25, C1–C5, M1, M2, M4, M5.
- **Đều có route duyệt/từ chối ở cả 2 nơi**: mọi luồng Finance và CustomerCare vẫn còn route tương ứng trên ERP (`ERP/TanPhatDev/routes/web.php`). Phía ERP **không** có middleware chặn, nên cùng một phiếu duyệt được ở cả 2 hệ thống.
  - Riêng MasterData (M1, M2, M4, M5): ERP đã khoá bằng `productMovedToHrm`, chỉ còn duyệt trên HRM.
- **HRM chỉ có nửa luồng** ở nhiều chỗ: HRM chỉ có nút "Không duyệt", còn bước duyệt thật (lập chứng từ kế tiếp hoặc TP/BGĐ duyệt) vẫn nằm trên ERP.
  - Luồng bị như vậy: F1, F6, F7, F11, F16, F19, F21, F22, F25.
  - F25 st10 có 1 phiếu (id 44418) chờ TP duyệt vượt hạn mức, chỉ duyệt được trên ERP.
  - C4: HRM chỉ duyệt HĐ type 1, trong khi có 1 phụ lục type 3 đang chờ.
- AS1 (bảng `quotations`) là bảng HRM. ERP còn model cũ `App\Quotation` trỏ cùng tên bảng nhưng không dùng để duyệt, nên không tính vào 34.

### Màn "chờ duyệt" riêng đã có trên HRM

| Phân hệ | Trang (client) |
|---|---|
| Timesheet | `/timesheet/attendance/approve` · `/timesheet/late-in-early-out/approve` · `/timesheet/overtime-requirement/approve` · `/timesheet/overtime-assignment/approve` · `/timesheet/request-update-working/approve` · `/timesheet/attendance/attendances-extend-request` · `/timesheet/late-in-early-out/change-end-request` · `/timesheet/business_trip_assigns/finish-extend` · `/timesheet/devices`.<br>`/timesheet/jobassignment/approve` và `/timesheet/business_trip_assigns/approve` có trang nhưng **không có trong menu**. Trang jobassignment còn trả **phiếu được giao cho mình**, không phải phiếu chờ mình duyệt. |
| Payroll | `/payroll/salary-data/p3-salary/approve` (không lọc quyền) |
| Training | `/training/training_requests?type=waiting` · `/training/course_requests?type=waiting` · `/training/courses?type=waiting` · `/training/course-registers?status=5` · `/training/training-survey-planning/need-approve`, kèm widget dashboard `JobWaitingApproveService` |
| Decision | **Màn chung `/decision/waiting-approve`** (GET `decision/waiting-approve`): gồm 19 loại QĐ trên bảng `decisions`.<br>Màn này **bỏ sót** biên bản xử lý sự cố, bảo hiểm, và QĐ bổ nhiệm/điều chuyển có HĐLĐ `end_date` NULL hoặc đã quá hạn. Phiếu 747 đang bị ẩn vì lý do này.<br>Thêm `category/trouble-shooting-reports/waiting-approve`, `insurance/waiting-approve`, và 7 màn `*/waiting-approve.vue` riêng ngoài menu (3 màn chép sai API/link). |
| Assign | `/assign/quotations/pending-approval` · `/assign/prospective-projects/extension-requests` · `/assign/handover/pending` · `/assign/handover/receiving` · `/assign/request-solution/pending` · `/assign/assign_waiting_approve_result` · `/assign/assign_job_waiting_approve_result`.<br>Tab `my-job › Chờ duyệt` là **gán cứng, rỗng**. |
| Finance | `/finance/bill-income-requests/pending` · `/finance/bill-payment-requests?mode=pending` · `/finance/addition-accounting-requests?mode=pending` · `/finance/bill-adjust-dept-requests?mode=pending` · `/finance/borrow-extend-requests?type=for-approve` · `/warehouse/self-inventories?type=wait-approve` · `/finance/product-price-approvals`.<br>`borrow-sell-requests?type=waiting_approve` có trang nhưng không có trong menu. |
| CustomerCare | `/customer-care/wr-service-contracts?type=for-approve` · `wr-information-requests?type=waiting_create_quotation` (một phần) |
| Meeting / Human | Không có màn riêng. Duyệt bằng lọc trong danh sách. |

### Lỗi và rủi ro phát hiện khi kiểm kê

Phần này chỉ ghi lại, chưa sửa gì. Chi tiết nằm ở từng phần.

1. **Thiếu đăng nhập**: nhóm route job-assignment (`Modules/Timesheet/Routes/api.php:176`) khai `' middleware'` có dấu cách thừa, nên cả nhóm **không có `auth:api`**.
2. **Fail-open ở BE** (FE ẩn nút nhưng gọi thẳng API vẫn duyệt được):
   - H2, H4, H8, H9, H10, H11 (Timesheet)
   - H12, H13 (Human)
   - H14 (Payroll)
   - H19 deny, H21–H25 (Training)
   - QĐ8–10, QĐ15 khi từ chối; QĐ20 cả duyệt lẫn từ chối; QĐ21 khi duyệt
   - AS8, AS13, AS18
3. **Không kiểm trạng thái hoặc cho nhảy cấp**:
   - Decision `toggleApprove`: gửi thẳng status 5, bỏ qua cấp Xem xét.
   - Training `status_request` (H18–H20, H24, H25).
4. **Quyền có 0 role guard api**, nên nút duyệt trên HRM chết:
   - Gia hạn TKT TP/BGĐ (AS3): 1 phiếu đang kẹt.
   - `Duyệt hợp đồng` (AS4)
   - `Kế toán kho` api (AS14/F25)
   - `Duyệt thông báo nội bộ` (H13, quyền không tồn tại)
   - `BGĐ duyệt bảng chia thưởng` (H15)
5. **Quyền chỉ có guard web nhưng HRM dùng làm gate**, nên màn phân quyền HRM không cấp hay gỡ được: hàng giữ, hàng mượn, mua dịch vụ, `Kế toán`, `Quản lý giữ hàng`, `Tạo phiếu giao việc`.
6. **CEP**:
   - Bỏ qua `company_id` của quyền.
   - Super admin vượt quyền ở khoảng 20 luồng.
   - F5 và F20: TP duyệt không kiểm phòng ban.
7. **Lộ dữ liệu**: `BusinessTripAssignService::approve()` (`:441-445`) không gán lại `$query`, nên ai cũng thấy toàn bộ phiếu công tác.
8. **Route chết, gọi vào ra 500**:
   - Training `questions/{id}/deny`, `exam_test_results/{id}/deny`
   - Decision `training-contract/{id}/toggle-approve`
   - Trang `decision/appendix-labor-contract/_id/approve.vue` gọi route không tồn tại

### Mục mơ hồ cần nghiệp vụ quyết định

Danh sách đầy đủ ở cuối từng phần: Phần 1 có 9 mục, Decision 6, Assign 8, Finance/CC/MD 13. Dưới đây là các câu chặn thiết kế màn tập trung:

1. **Phạm vi "chờ duyệt"**: có tính bước *tiếp nhận / xử lý / lập chứng từ kế tiếp* không?
   - Tiếp nhận: AS6, AS7, C5.
   - Xử lý / lập chứng từ kế tiếp: F1, F6, F7, F11, F16, F19, F22, AS11, AS17 bước giao việc, C3.
   - Hay chỉ tính *duyệt / không duyệt* thật?
2. **Luồng legacy Assign** (AS16–AS20, AS22; 1.581 phiếu, riêng AS20 là 1.041): có đưa vào màn tổng hợp không?
3. **Tồn đọng**: dọn hoặc đóng hàng loạt trước khi go-live, hay hiển thị và tách nhóm "quá hạn"?
   - C3: 4.686 phiếu
   - H22: 3.631 phiếu
   - Phiếu làm thêm / đi muộn đã quá hạn duyệt
   - AS19, AS18 cũ
   - `prepick_transfer2` chờ TP từ 2025-10-27
4. **Luồng 2 nơi**: 34 luồng trên bảng ERP hiện vẫn duyệt được trên cả ERP và HRM.
   - Màn tập trung hiển thị ở đâu, bấm duyệt ở đâu?
   - Có khoá phía ERP theo kiểu `productMovedToHrm` không?
5. **Người duyệt chưa xác định**: hiện chỉ có quyền "Quản lý…" ở FE hoặc không có gate nào. Cần chốt ai duyệt:
   - H8 phiếu giao việc
   - H9 phiếu công tác
   - H14 thu nhập P3
   - H22 điểm danh học viên
   - H13 thông báo nội bộ
6. **Quy tắc quyền** khi đưa lên màn tập trung:
   - Super admin có tự thấy và duyệt được không?
   - Quyền cấp ở công ty A có áp sang phiếu công ty B không?
   - Sửa gate spatie để thấy role `App\Employee`, hay gán lại role HRM? (Khi chưa sửa, CustomerCare đang khoá với mọi người.)
7. **Decision**: màn chung có cố ý ẩn QĐ có HĐLĐ không thời hạn không? Phiếu 747 đang kẹt. Danh sách chờ có lọc theo công ty đang làm không?
8. **Phụ lục HĐ dịch vụ (C4 type 3/4)** và **YCXH chờ TP/BGĐ (F25 st10/11)**: port phần duyệt sang HRM hay để ERP xử lý?
