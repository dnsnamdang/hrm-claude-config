# Quyền duyệt từng màn — nhóm Chấm công · Nhân sự · Tính lương · Meeting (#phiếu chờ duyệt tập trung) — @cuong61n

> Điều tra CHỈ ĐỌC, ngày 16/11/2026, nhánh `hrm-api` = `gop_db-main`. Mọi `file:dòng` là dòng thật trong working tree ngày này (số dòng route/entity trong `inventory-hrm.md` đã lệch so với hiện tại, dưới đây dùng số dòng mới).
> Đường dẫn BE viết tắt: `TS/` = `hrm-api/Modules/Timesheet/`, `HU/` = `hrm-api/Modules/Human/`, `PR/` = `hrm-api/Modules/Payroll/`, `MT/` = `hrm-api/Modules/Meeting/`. FE: `hrm-client/`.
> Không đụng nhóm Training (không thuộc phạm vi file này).

## 0. Khái niệm nền (áp cho mọi mục bên dưới)

### 0.1 "Có quyền" = mã quyền kiểm theo CÔNG TY ĐANG LÀM, KHÔNG có phạm vi
- `BaseModel::isCurrentEmployeeHasPermission()` (`app/Models/BaseModel.php:198-201`) → `CurrentPermission::has()` (`app/Support/Permissions/CurrentPermission.php:56-73`) → `PermissionChecker` theo `(employee id, current_company_role)`. Tức là chỉ tính vai trò người đó giữ ở CÔNG TY ĐANG LÀM (`users.current_company_role`), quyền ở công ty khác không tính. Không đăng nhập / không có công ty ⇒ false.
- Tất cả mã duyệt trong tài liệu này khai `scopes => []` trong Catalog (không có cấp Bộ phận/Phòng/Công ty/Tổng công ty): `app/Support/Permissions/Catalog/timesheet.php:139-165, 188-203, 221-236, 274-289, 307-336, 337-352`; `Catalog/assign.php:42-56, 119-133, 286-300`; `Catalog/human.php:282-296`; `Catalog/payroll.php:714-728`; `Catalog/meeting.php:99-112`. Phạm vi "ai được duyệt phiếu của ai" KHÔNG nằm ở quyền mà nằm ở điều kiện QUẢN LÝ (mục 0.2).
- Tên cũ → mã (inventory ghi tên cũ): `PD-Đơn xin nghỉ`=`timesheet.don_xin_nghi.approve` · `NSHC duyệt đơn xin nghỉ`=`timesheet.don_xin_nghi_nshc.approve` · `PD-Đăng ký đi muộn về sớm`=`timesheet.dang_ky_di_muon_ve_som.approve` · `PD-Đăng ký làm thêm`=`timesheet.dang_ky_lam_them.approve` · `PD-Phiếu yêu cầu làm thêm`=`timesheet.phieu_yeu_cau_lam_them.approve` · `XN-Đề nghị tra soát công`=`timesheet.de_nghi_tra_soat_cong.confirm` (cấp 1) · `PD-Đề nghị tra soát công`=`timesheet.de_nghi_tra_soat_cong.approve` (cấp 2) · `PD-Thiết bị chấm công`=`timesheet.thiet_bi_cham_cong.approve` · `Quản lý phiếu giao việc`=`assign.phieu_giao_viec.manage` · `Quản lý phiếu đi công tác`=`assign.phieu_di_cong_tac.manage` · `Gia hạn, kết thúc sớm phiếu công tác`=`assign.gia_han_ket_thuc_som.create` · `Quản lý danh sách hồ sơ tự khai`=`human.ho_so_tu_khai.manage` · `BGĐ duyệt bảng chia thưởng`=`payroll.bang_chia_thuong.approve` · `Duyệt phiếu đặt phòng họp`=`meeting.phieu_dat_phong_hop.approve`.

### 0.2 "Là QUẢN LÝ" = dòng trong `employee_manage_departments` (+ cờ "quản lý tất cả phòng ban")
Nguồn dữ liệu: bảng `employee_manage_departments (employee_id, company_id, department_id, part_ids, all_department)` và `company_employees.all_department`. KHÔNG phải cột trưởng phòng `departments.department_lead_id` (cột này chỉ dùng để gửi thông báo từ chối, `TS/Services/OvertimeRequirementService.php:189-205`).
- `employeeManagesAllDepartmentsIn()` — `app/Helper/PermissionHelper.php:62-85`; `manageDepartmentIdsOf()` — `:98-112`; `listManageDepartmentIds()` — `:209-214`.
- `TimesheetService::listManageEmployeeInfoIds()` (`TS/Services/TimesheetService.php:181-215`): nhân viên (`employee_infos.id`) có `department_id` thuộc các phòng mình quản lý trong công ty đang làm (hoặc cả công ty nếu cờ all_department). KHÔNG xét `part_ids` (bộ phận) ở đường duyệt.
- `ApproveScope::managesEmployee($employeeInfoId)` / `managesDepartment($departmentId)` (`TS/Support/ApproveScope.php:20-45`) bọc 2 hàm trên, nhớ cache trong 1 request. Phòng được xét là **phòng HIỆN TẠI của nhân viên** (`employee_infos.department_id`), không phải phòng ghi sẵn trên phiếu — trừ Phiếu yêu cầu làm thêm (xét `department_id` của phiếu).
- Danh sách người nhận thông báo "chờ duyệt" dùng cùng nguồn: `EmployeeInfoService::listEmployeeInfoHasPermission($quyền, $employee_info_id)` (`TS/Services/EmployeeInfoService.php:544-559`) = người quản lý phòng của `$employee_info_id` (`employeeIdsManagingDepartment`, `PermissionHelper.php:150-175`) ∩ người giữ quyền (`employeeIdsHoldingPermission`, `:505-518`). Lưu ý tham số thứ 2 mặc định là NGƯỜI ĐANG ĐĂNG NHẬP (xem các lệch ở từng mục).

### 0.3 Pattern chốt chặn của nhóm Chấm công
- Cờ `can_approve` / `can_reject` ở Entity (quyền + quản lý + trạng thái + hạn) là **nguồn duy nhất**. Nó được dùng 3 nơi: (1) hiện nút ở màn danh sách / chi tiết, (2) `FormRequest::authorize()` của endpoint duyệt qua trait `AuthorizesApproveAction` (`TS/Http/Requests/Approve/Concerns/AuthorizesApproveAction.php:17-29`: gửi `reject`/`3` thì kiểm `can_reject`, còn lại kiểm `can_approve`; phiếu không tồn tại thì cho qua; sai → 403), (3) không có (3) cho các loại không dùng trait.
- Trait chỉ áp cho 5 FormRequest: Đơn nghỉ, Đi muộn về sớm, Làm thêm (2 loại), Tra soát công (`grep AuthorizesApproveAction`). Phiếu giao việc / Phiếu công tác có FormRequest nhưng `authorize()` luôn `true` (`JobAssignmentNoteApproveRequest.php:28-31`, `BusinessTripAssignApproveRequest.php:79-82`).
- Middleware `checkDueConfigsManager:<tên>` (mục 0.4) gắn trên route duyệt nhưng KHÔNG phải chốt quyền.
- Route nhóm Chấm công tự gắn `auth:api` từng nhóm (`TS/Routes/api.php`). Ngoại lệ lỗi gõ: nhóm `/timesheet/job-assignment` khai `' middleware'` (có dấu cách) nên **mất `auth:api`** — `TS/Routes/api.php:173` (inventory ghi :176).

### 0.4 `checkDueConfigsManager` (điều kiện đặc thù "trưởng phòng còn hàng quá hạn")
- `app/Http/Middleware/CheckDueConfigsManager.php:25-59`. Chỉ chạy khi bảng `master_settings` có `category=use_erp` và `content` thật (`:28-29`). Gọi ERP `GET /api/v1/due-configs/check-manager-block?employee_id=<ERP employees.id của NGƯỜI ĐANG BẤM>&action=<tên>`; ERP trả `blocked=true` ⇒ HRM trả 403 (`:44-49`). Lỗi kết nối ERP ⇒ **cho qua** (`:50-56`).
- Phía ERP: `TanPhatDev/app/Services/DueConfig/DueConfigBlockService.php::isManagerBlocked` — chặn khi (a) action có trong `due_configs` (tab=2) VÀ công ty của người bấm có tick action đó (`company_due_configs`), (b) người bấm có quản lý ≥1 phòng (`employee_manage_departments`), (c) trong các phòng đó có nhân viên còn: hàng giữ quá hạn (prepick), hàng mượn quá hạn, hàng nhập thẳng quá hạn (nếu công ty có cấu hình `overdue_date_export_direct`). Người không quản lý phòng nào ⇒ không bao giờ bị chặn.
- Đặc điểm cần nhớ cho bảng gom: chặn theo NGƯỜI BẤM + HÀNH ĐỘNG, không theo phiếu; chặn cả duyệt lẫn từ chối (cùng route); gắn trên: `Duyệt đơn xin nghỉ` (cả `nshc-approve`), `Duyệt đơn đi muộn về sớm`, `Duyệt phiếu yêu cầu làm thêm`, `Duyệt đăng ký làm thêm`, `Duyệt đề nghị tra soát công`, `Duyệt phiếu giao việc (phân hệ chấm công)`, `Duyệt phiếu đi công tác (phân hệ chấm công)` (`TS/Routes/api.php:153, 178, 190, 207-208, 236, 248, 264`). Các luồng KHÔNG gắn: kết thúc nghỉ phép, kết thúc đi muộn về sớm, finish-extend, thiết bị, mọi luồng Human/Payroll/Meeting.

### 0.5 Hai lỗ hổng chung của nhóm (kiểm ở mức đọc code, chưa chạy thật)
1. **Endpoint tạo/sửa nhận trạng thái từ body** — đa số FormRequest chỉ ràng `status: required` (`LateEarlyOutRequest.php:42` `required|numeric`; `OvertimeAssignmentRequest.php:46,64` `required`; `JobAssignmentNoteRequest.php:49` `required`), không có `in:` và không kiểm quyền duyệt. FE chỉ gửi `2` ("LƯU và DUYỆT") khi user có quyền (`jobassignment/add.vue:20-21`, `business_trip_assigns/add/_id.vue:36-40`, `overtime-allocation/add.vue:14`), nhưng BE không chặn gọi tay `status=2`. Cần chạy thật để khẳng định trước khi đưa vào tài liệu bảo mật.
2. **Người có quyền duyệt tạo phiếu ⇒ tự duyệt ngay lúc tạo** là thiết kế có chủ đích ở Phiếu giao việc, Phiếu công tác, Phân công làm thêm (xem mục 5, 6, 4B).

---

## 1. Đơn xin nghỉ (H1) — 2 cấp, cấp 2 có điều kiện

### 1a. Các cấp
| Cấp | `attendance_status` | Chữ BE trả (`Entities/Attendance.php:100-125`) | Điều kiện vào cấp |
|---|---|---|---|
| 0 | 0 | Đang tạo | nháp |
| C1 | 1 | Gửi TP duyệt | NV bấm gửi |
| C2 | 4 | Chờ NSHC duyệt | TP duyệt C1 VÀ `leave_types.need_nshc_approve = 1` (`AttendanceController.php:165-166`); loại nghỉ không cần NSHC thì C1 duyệt xong là 2 |
| Kết | 2 / 3 | Đã duyệt / Từ chối | |

### 1b. Cấp × người duyệt
| Cấp | Mã quyền | Điều kiện QUẢN LÝ | Điều kiện khác | Nguồn |
|---|---|---|---|---|
| C1 duyệt | `timesheet.don_xin_nghi.approve` | `managesEmployee(phiếu.employee_id)` = người tạo thuộc phòng mình quản lý (phòng HIỆN TẠI của người tạo) | `attendance_start_at` + 1 tháng, ngày 05 ≥ hôm nay (vd nghỉ ngày 12/10 → duyệt được đến hết 05/11) — **chỉ áp cho DUYỆT** | `Attendance.php:158-167` |
| C2 duyệt (NSHC) | `timesheet.don_xin_nghi_nshc.approve` | `managesEmployee(employee_id)` | KHÔNG có hạn ngày | `Attendance.php:164, 235-239` (`canNSHCApprove`) |
| Từ chối (C1, C2, hoặc phiếu đã duyệt còn hiệu lực) | **`timesheet.don_xin_nghi.approve`** (PD), kể cả khi phiếu ở C2 | `managesEmployee` | C1/C2 từ chối không giới hạn ngày; phiếu Đã duyệt chỉ từ chối được khi `attendance_start_at ≥ hôm nay` | `Attendance.php:169-175` |

### 1c. Kiểm ở đâu
- BE: `POST /v1/timesheet/attendance/approve` (`Routes/api.php:207`) → `AttendanceApproveRequest::authorize` (trait) → `can_approve`/`can_reject`. Controller thêm 1 chốt riêng: phiếu đang C2 mà người bấm không có `don_xin_nghi_nshc.approve` ⇒ 403 (`AttendanceController.php:155-159`) — chốt này áp cả cho **từ chối**.
- `POST /v1/timesheet/attendance/{id}/nshc-approve` (`Routes/api.php:208`): controller gọi `canNSHCApprove()` (`AttendanceController.php:200-205`) — không qua FormRequest; trả 400 nếu sai.
- Hệ quả "từ chối ở C2": cần ĐỦ CẢ 2 quyền PD và NSHC (PD qua `can_reject`; NSHC qua chốt `AttendanceController.php:155`). Người chỉ có NSHC: `can_reject=false` (cần PD) ⇒ không từ chối được. Người chỉ có PD: nút Từ chối hiện (can_reject=true) nhưng BE trả 403 ở chốt controller.
- Màn "chờ duyệt" `/timesheet/attendance/approve` → `AttendanceService::approve()` (`TS/Services/AttendanceService.php:66-88`): có PD ⇒ thấy phiếu `status=1` của NV thuộc phòng mình quản lý; có NSHC ⇒ thấy phiếu `status=4` của NV thuộc phòng mình quản lý; có cả hai ⇒ thấy cả hai; không có quyền nào ⇒ chỉ thấy phiếu mình tạo. **Khớp tiêu chí `can_approve`** (trừ hạn ngày 05: phiếu quá hạn vẫn nằm trong danh sách nhưng `can_approve=false`).
- FE menu "Phê duyệt › Đơn xin nghỉ" chỉ gate `timesheet.don_xin_nghi.approve` (`components/menu.js:415-420`) ⇒ người **chỉ có NSHC không thấy menu** (xác nhận inventory mục mơ hồ #9). FE chi tiết: nút "TP duyệt" = `can_approve`, "NSHC duyệt" = `can_nshc_approve`, "Từ chối" = `can_reject` (`pages/timesheet/attendance/_id/approve.vue:13-15, 168-190`). Lưu ý: NSHC có `can_approve=true` ở phiếu C2 nên thấy CẢ 2 nút "TP duyệt" lẫn "NSHC duyệt"; bấm "TP duyệt" cũng đi vào `storeApprove` và qua chốt C2 ⇒ vẫn ra Đã duyệt (loại nghỉ có `need_nshc` nhưng đã ở C2 nên giữ Đã duyệt: `AttendanceController.php:164-166`).
- Dòng trong danh sách "Quản lý đơn" (`/timesheet/attendance`) dùng cùng `can_approve`/`can_reject` (`pages/timesheet/attendance/index.vue:191-194`).

### 1d. Người tạo có tự duyệt được không?
- Trong code có biến `$isNotTP = employee_id != mình || có quyền PD` (`Attendance.php:160, 172`) nhưng **vô hiệu**: `can_approve` đã yêu cầu `có quyền PD` rồi nên `$isNotTP` luôn true khi có PD. Không có chốt nào "người tạo ≠ người duyệt".
- Vậy trưởng phòng (có PD, và phòng mình nằm trong `employee_manage_departments` của chính mình — gần như luôn đúng) tạo đơn → `managesEmployee(chính mình)=true` → **tự duyệt C1 được**. Nếu loại nghỉ cần NSHC thì sau C1 vẫn phải có người có quyền NSHC + quản lý phòng đó duyệt C2 (người đó có thể chính là TP nếu TP giữ cả NSHC, xem 1e).
- NV thường (không có PD): `can_approve=false`.

### 1e. Một người giữ nhiều cấp
- TP giữ cả PD + NSHC, loại nghỉ cần NSHC: duyệt C1 ⇒ phiếu sang status 4 ("Chờ NSHC duyệt"), **KHÔNG tự nhảy cấp** (`AttendanceController.php:165-166` chỉ đổi status, không lặp). Người đó phải mở lại phiếu và bấm "NSHC duyệt" (hoặc "TP duyệt" lần 2) — được phép, vì `can_approve` ở status 4 đúng với NSHC-holder (`Attendance.php:164`) và `canNSHCApprove()` đúng. Kể cả khi người đó là người tạo đơn (không có chốt ngăn).
- Người chỉ có NSHC: không duyệt được C1 (status 1 cần PD).
- ⚠️ Thông báo C2 không bao giờ gửi: `AttendanceService::save()` nhánh cập nhật (có `id`) `return` sớm ngay sau khối Approved/Rejected (`AttendanceService.php:233-250`); khối gửi thông báo "Chờ NSHC duyệt" (`:268-276`) chỉ chạy ở nhánh TẠO MỚI với status=4 (không bao giờ xảy ra). ⇒ NSHC **không nhận thông báo** khi TP duyệt xong C1. Màn danh sách vẫn thấy. (Đọc code, chưa chạy thật.)
- Thông báo gửi cho C1 tính theo phòng của người tạo (`AttendanceService.php:258-266`) — khớp tiêu chí `managesEmployee`.

### 1f. Điều kiện đặc thù
- Hạn duyệt C1 đến ngày 05 tháng sau tháng bắt đầu nghỉ (`Attendance.php:161`). C2 và từ chối C1/C2 không hạn.
- `checkDueConfigsManager:Duyệt đơn xin nghỉ` (cả `/approve` và `/nshc-approve`).
- Duyệt xong status 2 ⇒ queue tính lại công `calc:employee_timesheet` nếu ngày nghỉ ≤ hôm nay (`AttendanceController.php:168-185`).
- **`can_approve=false` (hết khả năng duyệt)** cho NV bất kỳ khi: `status ∉ {1,4}`, hoặc (status=1 và đã qua hạn ngày 05). Với từng người cụ thể còn phụ thuộc quyền + quản lý.

### 1g. Biểu diễn cho bảng gom
Gate cấp: `[status=1 → quyền don_xin_nghi.approve] [status=4 → quyền don_xin_nghi_nshc.approve]` + điều kiện chung `người xem quản lý phòng HIỆN TẠI của phiếu.employee_id`. Biểu diễn được bằng 1 cột gate kiểu "mã quyền + quản lý phòng của người đề nghị" **nếu** Definition cho khai mã quyền theo từng giá trị status. Cần cột `approvable` riêng cho hạn ngày 05 (chỉ C1). Từ chối ở C2 (PD **và** NSHC) là trường hợp 2 quyền đồng thời — nếu bảng gom có nút Từ chối thì không biểu diễn được bằng 1 gate/cấp.

---

## 2. Đơn kết thúc nghỉ phép sớm (H2)

| Cấp | Trạng thái | Mã quyền / điều kiện | Nguồn |
|---|---|---|---|
| Duy nhất | `status=1` "Gửi duyệt" (dùng chung hằng `AttendanceStatus`; `AttendancesExtendRequest.php:46-56`) → 2 Đã duyệt / 3 Từ chối | FE cờ `can_approve`: có `timesheet.don_xin_nghi.approve` (+ `$isNotTP` luôn true vì thuộc tính `employee_id` không tồn tại trên model này ⇒ null ≠ mình) | `AttendancesExtendRequest.php:94-105` |

- **BE KHÔNG chốt gì**: duyệt đi qua `POST /v1/timesheet/attendances-extend-requests/{id}` (`Routes/api.php:460`, `store`); `AttendancesExtendRequest` FormRequest `authorize()=true` (`Http/Requests/AttendancesExtendRequest.php:94-97`); `Service::save()` khi có `id` và `status=2` ghi thẳng `attendance_end_at` mới vào phiếu nghỉ gốc, không kiểm trạng thái hiện tại, không kiểm quyền (`TS/Services/AttendancesExtendRequestService.php:68-82`). Ai đăng nhập cũng duyệt/ghi đè được.
- Không kiểm quản lý ở `can_approve` (chỉ quyền PD). Màn danh sách `/timesheet/attendances-extend-requests` (`AttendancesExtendRequestService::index`, `:20-54`): có PD ⇒ chỉ thấy phiếu mà người TẠO (`created_by.info.department_id`) thuộc phòng mình quản lý; không có PD ⇒ chỉ phiếu mình tạo. Nhánh NSHC là closure rỗng (`:44-46`): nếu người **chỉ có NSHC (không PD)** thì closure `where(function…)` rỗng không lọc ⇒ có khả năng thấy **toàn bộ** phiếu công ty (đọc code, chưa chạy thật).
- Người tạo tự duyệt: `can_approve` không loại người tạo; TP có PD tự tạo yêu cầu rồi tự duyệt được (không chốt).
- Nhiều cấp: không có (1 cấp). Hạn ngày: không (dòng kiểm hạn bị comment, `:97, 102`).
- Menu: `Phê duyệt › Đơn kết thúc nghỉ phép` gate PD (`menu.js:421-426`). FE nút theo `can_approve` (`attendances-extend-request.vue:94,105`).
- Bảng gom: biểu diễn được nhưng KHÔNG khớp BE (gate FE = quyền PD, "quản lý" chỉ ở danh sách theo phòng người tạo). Đề xuất gate: `mã don_xin_nghi.approve + quản lý phòng người tạo`.

---

## 3. Đăng ký đi muộn về sớm (H3) và Đơn kết thúc sớm đăng ký đi muộn về sớm (H4)

### 3A. Đăng ký đi muộn về sớm (H3)
| Cấp | `late_early_out_status` | Chữ BE | Người duyệt |
|---|---|---|---|
| Duy nhất | 1 "Gửi duyệt" → 2 Đã duyệt / 3 Từ chối (`LateEarlyOut.php:195-216`) | `LateEarlyOutStatus.php` | quyền `timesheet.dang_ky_di_muon_ve_som.approve` + `managesEmployee(phiếu.employee_id)` (`LateEarlyOut.php:282-289`) |
| Từ chối thêm | | phiếu Đã duyệt còn hiệu lực (`start_at ≥ hôm nay`) cũng từ chối được (`:291-297`) | |

- Kiểm: `POST /v1/timesheet/late-in-early-out/approve` (`Routes/api.php:190`) → `LateEarlyOutApproveRequest` (trait) → `can_approve`/`can_reject` ⇒ BE chốt đủ quyền + quản lý + trạng thái.
- **KHÔNG có hạn ngày**: biến `$isEditStatus` được tính nhưng dòng `&& $isEditStatus` đã comment (`LateEarlyOut.php:285-287`). ⇒ 28 phiếu cũ trên prod vẫn duyệt được, **trái** với `inventory-hrm.md` mục mơ hồ #1 (gộp đi muộn về sớm vào "đã quá hạn, BE không cho duyệt").
- Danh sách "chờ duyệt" (`LateEarlyOutService::approve`, `TS/Services/LateEarlyOutService.php:48-61`): có quyền ⇒ MỌI trạng thái (≠0) của NV thuộc phòng mình quản lý (FE tự lọc status; BE không lọc theo trạng thái chờ); không có quyền ⇒ phiếu mình tạo. Khớp `managesEmployee` của `can_approve`.
- Người tạo tự duyệt: phiếu luôn do người đăng nhập tạo cho chính mình (`LateEarlyOutService.php:193-195`: `employee_id = employee_info_id` của người tạo). TP có quyền + `managesEmployee(mình)` ⇒ tự duyệt được. Không chốt.
- Nhiều cấp: không có. Thông báo chờ duyệt: người quản lý phòng của người tạo ∩ giữ quyền, **kể cả chính người tạo nếu thoả** (`LateEarlyOutService.php:200-208`).
- `checkDueConfigsManager:Duyệt đơn đi muộn về sớm`.
- Bảng gom: biểu diễn được = `mã dang_ky_di_muon_ve_som.approve + quản lý phòng người tạo`.

### 3B. Đơn kết thúc sớm đăng ký đi muộn về sớm (H4)
- Trạng thái: `status=1` `CHO_DUYET` → 2 Đã duyệt (hằng `LateInEarlyOutChangeEndRequest::DA_DUYET`) / 3 Từ chối.
- `can_approve`/`can_reject` = `status==CHO_DUYET` + quyền `timesheet.dang_ky_di_muon_ve_som.approve`, **không kiểm quản lý** (`TS/Entities/LateInEarlyOutChangeEndRequest.php:101-110`).
- **Khác `inventory-hrm.md`**: BE hiện ĐÃ chốt khi `id` được gửi lên: bắt buộc quyền `timesheet.dang_ky_di_muon_ve_som.approve` (403) và phiếu phải đang `CHO_DUYET` (422) — `LateInEarlyOutChangeEndRequestController.php:47-57`. Thiếu: chốt quản lý phòng, chốt giá trị `status` (chỉ lấy từ body, `:76-83`), chốt người tạo.
- Danh sách (`LateInEarlyOutChangeEndRequestService::index`, `TS/Services/LateInEarlyOutChangeEndRequestService.php:20-46`): có quyền ⇒ phiếu có `department_id ∈ phòng mình quản lý`; không có ⇒ phiếu mình tạo. (Màn gom nên dùng phòng của phiếu `department_id`.)
- Tạo yêu cầu: chỉ người tạo đơn gốc (`LateEarlyOut::canRequestChangeEnd`, controller `:67-70`). Người tạo tự duyệt: nếu có quyền và phòng mình trong phạm vi list thì được; BE không chặn.
- Một cấp; bảng rỗng trên prod (0 phiếu theo inventory, chưa xác minh lại bằng SQL).
- Không gắn `checkDueConfigsManager`.

---

## 4. Làm thêm: Phiếu yêu cầu làm thêm (H5) và Đăng ký / Phân công làm thêm (H6)

### 4A. Phiếu yêu cầu làm thêm (H5)
| Cấp | `overtime_requirement_status` | Người duyệt | Nguồn |
|---|---|---|---|
| Duy nhất | 1 "Gửi duyệt" → 2 / 3 | quyền `timesheet.phieu_yeu_cau_lam_them.approve` + `managesDepartment(phiếu.department_id)` — `department_id` = **"Đơn vị thực hiện"** (FE `overtime-requirement/_id/index.vue:30`), KHÔNG phải phòng yêu cầu (`requirement_department_id`) | `Entities/OvertimeRequirement.php:166-185` |
| Hạn | | `start_at ≥ hôm nay` cho duyệt; từ chối thêm cho phiếu Đã duyệt còn hiệu lực | `:168, 175-177` |

- BE: `OvertimeRequirementApproveRequest` (trait) → `can_approve` ⇒ chốt đủ. Danh sách (`OvertimeRequirementService::approve`, `:46-65`): có quyền ⇒ phiếu có `department_id ∈ manage`; không ⇒ phiếu mình tạo.
- Người tạo tự duyệt: không loại trừ; TP có quyền tạo phiếu với Đơn vị thực hiện = phòng mình quản lý ⇒ tự duyệt được.
- Nhiều cấp: không có.
- ⚠️ Lệch người nhận thông báo: khi gửi duyệt, controller thông báo cho người giữ **`timesheet.dang_ky_lam_them.approve`** (quyền của "Đăng ký làm thêm") trong phòng của đơn vị thực hiện (`OvertimeRequirementController.php:136`), trong khi người DUYỆT thật phải giữ **`phieu_yeu_cau_lam_them.approve`**. Người có quyền A nhưng không có quyền B nhận thông báo nhưng không duyệt được; người có B không có A duyệt được nhưng không được báo.
- Hết khả năng duyệt: `status≠1` hoặc `start_at` < hôm nay (phiếu cũ kẹt vĩnh viễn — đúng inventory H5).
- `checkDueConfigsManager:Duyệt phiếu yêu cầu làm thêm`.
- Bảng gom: biểu diễn được = `mã phieu_yeu_cau_lam_them.approve + quản lý phòng = đơn vị thực hiện (phiếu.department_id)`; cột `approvable` cần `start_at ≥ hôm nay`.

### 4B. Đăng ký làm thêm / Phân công làm thêm (H6)
- `assignment_type` 0 = đăng ký (1 NV), 1 = phân công (nhiều NV) (`Enums/OvertimeAssignmentType.php:10-11`). Một cấp `overtime_assignment_status` 1 → 2 / 3.
- Người duyệt: quyền `timesheet.dang_ky_lam_them.approve` + (loại 1 phân công ⇒ `managesDepartment(phiếu.department_id)`; loại 0 ⇒ `managesEmployee(phiếu.employee_id)`) + `overtime_start_at ≥ hôm nay` (`Entities/OvertimeAssignment.php:252-279`).
- BE: `OvertimeAssignmentApproveRequest` (trait). Controller duyệt kiểm thêm **trần giờ làm thêm/tháng** (`OvertimeAssignmentController.php:126-153`, hàm `checkMonthlyOvertimeLimit`): vượt trần ⇒ 422 kèm `overtime_limit_details`, không duyệt được dù có quyền. Đây là điều kiện hết khả năng duyệt phụ thuộc người/ tháng, không biểu diễn được ở mức cột trạng thái.
- Danh sách `/approve` (`OvertimeAssignmentService::approve`, `:61-74`): có quyền ⇒ `employee_id ∈ NV thuộc phòng mình quản lý` cho MỌI loại. Hệ quả: phiếu **phân công** (loại 1) có `employee_id` null (form `overtime-allocation` chỉ gửi `employees[]`, không gửi `employee_id` — `overtime-allocation/add.vue:499-506`) sẽ **không nằm trong danh sách /approve** dù `can_approve` đúng theo phòng. (Suy từ code, chưa chạy thật.)
- Phân công làm thêm: màn tạo `overtime-allocation/add.vue:13-14` cho "LƯU và DUYỆT" (status 2) trực tiếp, FE không gate quyền duyệt (chỉ gate menu `timesheet.phan_cong_lam_them.view`, `menu.js:375-379`); BE `store` nhận status từ body (`OvertimeAssignmentController.php:165-205`, request chỉ `required`). ⇒ Người tạo phân công tự duyệt; người tạo đăng ký thường (`overtime-assignment/add.vue:14` chỉ "GỬI DUYỆT") thì không.
- Người tạo tự duyệt: loại 0, TP có quyền và `managesEmployee(employee_id=chính mình)` ⇒ duyệt được. Không chốt.
- Thông báo chờ duyệt: người quản lý phòng của **người tạo** (không phải phòng của NV trong phiếu) ∩ giữ `dang_ky_lam_them.approve` (`OvertimeAssignmentController.php:319`) — lệch nếu người tạo ≠ người làm thêm.
- `checkDueConfigsManager:Duyệt đăng ký làm thêm`.
- Bảng gom: biểu diễn được cho loại 0 = `mã dang_ky_lam_them.approve + quản lý phòng của employee_id`; loại 1 = `... + quản lý phòng của phiếu.department_id`. Cần nhánh theo `assignment_type` (gate điều kiện, không thuần cột).

---

## 5. Đề nghị tra soát công (H7) — 2 cấp, 2 quyền KHÁC NHAU

### 5a. Các cấp
| Cấp | `status` | Chữ BE (`RequestUpdateTimeSheet.php:195-205`) | Mã quyền duyệt | Quản lý |
|---|---|---|---|---|
| C1 (Trưởng phòng) | 1 | Gửi duyệt | `timesheet.de_nghi_tra_soat_cong.confirm` ("XN") | `managesEmployee(phiếu.employee_id)` |
| C2 (NSHC) | 4 | Chờ NSHC duyệt | `timesheet.de_nghi_tra_soat_cong.approve` ("PD") | `managesEmployee(phiếu.employee_id)` |
| Kết | 2 / 3 / 5 | Đã duyệt / Từ chối (NSHC) / TP từ chối (cấp 1) | | |

- `can_approve = (confirm ∧ status=1) ∨ (approve ∧ status=4)`, VÀ `phiếu.company_id == công ty đang làm`, VÀ `managesEmployee(employee_id)`; `can_reject = can_approve` (`Entities/RequestUpdateTimeSheet.php:173-187`). Không có hạn ngày.
- BE: `POST /v1/timesheet/request-update-working/storeApprove` (`Routes/api.php:153`) → `RequestUpdateTimeSheetApproveRequest` (trait, `status: approve|reject`) ⇒ chốt đủ.
- Danh sách (`RequestUpdateTimeSheetService::approve`, `:68-93`): PD thấy trạng thái {2,3,4}; XN thấy {1,2,3,4,5}; cả 2 thấy hợp; luôn lọc `employee_id ∈ NV thuộc phòng mình quản lý`; không quyền ⇒ phiếu mình tạo. Khớp `can_approve`. Menu gate cả 2 mã (`menu.js:449-454`).

### 5b. MỘT NGƯỜI GIỮ CẢ HAI QUYỀN — NHẢY CẤP (quan trọng)
`RequestUpdateTimeSheetService::storeApprove` (`TS/Services/RequestUpdateTimeSheetService.php:260-330`): khối kiểm `confirm` đặt `statusInt = TpApproved/TpRejected` (`:267-273`), rồi khối kiểm `approve` đứng sau **ghi đè** `statusInt = Approved/Rejected` (`:275-279`). Hệ quả:
- Người giữ cả `confirm` và `approve` duyệt phiếu ở C1 (status 1) ⇒ phiếu nhảy thẳng **Đã duyệt (2)** (bỏ bước "Chờ NSHC duyệt"), đồng thời tạo 2 bản ghi `Timesheet` "Tra soát công" và dispatch `CalcTimeSheet` (`:283-318`). Từ chối ⇒ **Từ chối (3)**, không phải "TP từ chối (5)".
- Cả hai trường người duyệt được ghi: `approved_department_by` (nếu trống) và `approved_personnel_administration_by` (`:269-278`).
- `can_approve` vẫn đúng ở C1 vì khối `confirm ∧ status=1` thoả — không có chốt nào ngăn.
- Người tạo phiếu cũng có thể tự nhảy cấp nếu giữ cả hai quyền và phòng mình nằm trong quản lý của mình (không loại người tạo).
Người chỉ giữ `approve` (NSHC) ở phiếu status 1: `can_approve=false` ⇒ 403. Người chỉ giữ `confirm` ở status 4: `can_approve=false`.

### 5c. Thông báo
- Gửi duyệt C1: người quản lý phòng của người tạo ∩ giữ `confirm` (`RequestUpdateTimeSheetController.php:118`).
- Sau khi C1 duyệt (status 4): gửi cho giữ `approve` trong phòng của **người vừa duyệt C1** (`auth()->user()->employee_info_id`, `:195`), không phải phòng của người đề nghị ⇒ NSHC (thường quản lý nhiều phòng/cờ tất cả phòng) vẫn nhận được nếu quản lý phòng của TP; nếu NSHC quản lý phòng của NV nhưng không quản lý phòng của TP thì KHÔNG nhận (đọc code, chưa chạy thật).

### 5d. Đặc thù
- `checkDueConfigsManager:Duyệt đề nghị tra soát công` (chặn cả 2 cấp).
- Bảng gom: biểu diễn được = cột gate theo `status`: `status=1 → confirm + quản lý`, `status=4 → approve + quản lý`, thêm `company_id = công ty đang làm`. Cột `approvable` không cần hạn ngày. Trường hợp giữ 2 quyền: Definition cần biết nút "Duyệt" ở C1 sẽ nhảy cấp (để ghi nhận kết quả thật).

---

## 6. Phiếu giao việc trong ngày (H8) — hệ thống chấm công (`job_assignment_notes`)

### 6a. Các cấp
| Cấp | `status` | Ghi chú |
|---|---|---|
| 0 | Đang tạo | |
| 1 | Gửi duyệt (`JobAssignmentNoteStatus::SendApprove`) | người tạo KHÔNG có `assign.phieu_giao_viec.manage` ⇒ FE gửi status=1 (`jobassignment/add.vue:28-35`) |
| 2 / 3 | Đã duyệt / Từ chối | người tạo CÓ `assign.phieu_giao_viec.manage` ⇒ nút "LƯU và DUYỆT" gửi thẳng status=2 (`jobassignment/add.vue:19-27`, `isJobAssigmentManager()` = `hasAPermission('assign.phieu_giao_viec.manage')` ở `_id/index.vue:508-510`) |

### 6b. Ai duyệt
- Cờ `can_approve` = `status==1` ∧ có `assign.phieu_giao_viec.manage` (`TS/Entities/JobAssignmentNote.php:151-155`); `can_reject` = (status 1 ∧ có quyền) ∨ (status 2 ∧ `isEditStatus` = `begin_date ≥ hôm nay` ∧ quyền) (`:162-167`, `getIsEditStatus` `:145-149`). Chỉ gắn vào Detail resource (`Transformers/JobAssignmentResource/JobAssignmentNoteDetailResource.php:39-40`). **Không kiểm quản lý nào** — mã là "quản lý theo mã", không theo phòng.
- BE endpoint `POST /v1/timesheet/job-assignment/approve` (`Routes/api.php:178`): `JobAssignmentNoteApproveRequest::authorize()=true` (`:28-31`); `storeApprove` (`JobAssignmentNoteController.php:143-253`) không kiểm quyền; chỉ kiểm trùng lịch với phiếu đã duyệt. **Fail-open** (đúng inventory); kèm lỗi thiếu `auth:api` do typo `' middleware'` (`Routes/api.php:173`) ⇒ nhóm route job-assignment không bắt đăng nhập ở tầng route (hậu quả thực tế chưa xác minh: phần ghi dữ liệu có thể chạy không cần `auth()`; thông báo/`auth()->user()` có thể ném lỗi sau khi ghi — chưa chạy thật).
- Danh sách người duyệt thấy phiếu: màn "Quản lý phiếu giao việc" `GET /job-assignment` (`JobAssignmentNoteService::index`, `TS/Services/JobAssignmentNoteService.php:23-60`): phiếu có ≥1 NV thuộc phòng mình quản lý, hoặc phiếu mình tạo — KHÔNG lọc theo quyền duyệt. Còn `GET /job-assignment/approve` (`JobAssignmentNoteService::approve`, `:338-349`) trả phiếu mà **mình là người được giao** (qua `job_assignment_employees`), không phải phiếu chờ mình duyệt. ⇒ Không có màn "chờ duyệt" đúng nghĩa cho người duyệt; trang `/timesheet/jobassignment/approve` không nằm trong menu Phê duyệt (`menu.js` mục Phê duyệt không có).
- Thông báo chờ duyệt: người quản lý phòng của người tạo ∩ giữ `assign.phieu_giao_viec.manage` (`JobAssignmentNoteController.php:353, 398`) — người có quyền nhưng không quản lý phòng người tạo không được báo, nhưng vẫn duyệt được qua URL/`can_approve`.

### 6c. Tự duyệt / nhiều cấp
- Người tạo có `phieu_giao_viec.manage` tự duyệt ngay lúc tạo (status=2) — thiết kế FE, BE không chặn kể cả người không có quyền (store nhận status từ body, `JobAssignmentNoteRequest.php:49`).
- Phiếu đã Gửi duyệt: người tạo có quyền cũng tự duyệt được (`can_approve` không loại người tạo).
- Một cấp; không có nhảy cấp.

### 6d. Đặc thù
- `checkDueConfigsManager:Duyệt phiếu giao việc (phân hệ chấm công)` (`Routes/api.php:178`).
- Lúc duyệt BE kiểm trùng thời gian với phiếu đã duyệt (422) và FE bắt nhập lại giờ khi phiếu quá hạn (`JobAssignmentNoteApproveRequest.php:51-77`: `intend_start_at ≥ now`).
- Hết khả năng duyệt: `status≠1` hoặc (phiếu quá hạn thời gian ⇒ không "hết" mà bắt sửa giờ rồi mới duyệt).
- Bảng gom: biểu diễn được là gate "chỉ mã quyền, không quản lý" (`assign.phieu_giao_viec.manage`). Không khớp danh sách thực tế (BE không chốt). Nếu gom theo quản lý phòng của NV trong phiếu (khớp màn Quản lý) thì khác BE.

---

## 7. Phiếu đi công tác (H9) và Gia hạn / kết thúc sớm công tác (H10)

### 7A. Phiếu đi công tác (`business_trip_assigns`)
| Cấp | `status` | Ghi chú |
|---|---|---|
| 1 | Gửi duyệt (`BusinessTripAssignStatus::SendApprove`) | người tạo không có `assign.phieu_di_cong_tac.manage` ⇒ "GỬI DUYỆT" |
| 2/3/Hủy | Đã duyệt / Từ chối / Hủy | người tạo có quyền ⇒ "LƯU và DUYỆT" gửi thẳng status=2 (`business_trip_assigns/add/_id.vue:20-48, 848`) |

- `can_approve` = `status==1` ∧ quyền `assign.phieu_di_cong_tac.manage`; `can_reject` cùng điều kiện (`TS/Entities/BusinessTripAssign.php:197-207`). Không kiểm quản lý.
- BE: `POST /v1/timesheet/business_trip_assigns/approve` (`Routes/api.php:264`): `BusinessTripAssignApproveRequest::authorize()=true` (`:79-82`) — **không chốt quyền**. `storeApprove` (`BusinessTripAssignController.php:133-202`) kiểm trùng phiếu công tác đã duyệt (cả phiếu phân hệ Giao việc `assign_requests`), và FormRequest bắt `from_time/time_to_go ≥ now` khi duyệt (`:46-70`).
- Danh sách: `BusinessTripAssignService::approve` (`TS/Services/BusinessTripAssignService.php:450-465`) khai `$query = $this->model; if (!quyền) $query->where('created_by', …)` — gọi `where` trên model rồi **bỏ kết quả** (không gán lại) ⇒ lọc theo người tạo không bao giờ áp, mọi người thấy mọi phiếu (≠0) (đúng inventory H9; còn nguyên).
- Thông báo chờ duyệt: người quản lý phòng của **từng nhân viên đi công tác** ∩ giữ `assign.phieu_di_cong_tac.manage`, loại người tạo (`BusinessTripAssignController.php:253-275`).
- Tự duyệt / nhiều cấp: như phiếu giao việc.
- `checkDueConfigsManager:Duyệt phiếu đi công tác (phân hệ chấm công)` (`Routes/api.php:264`), cả `storeResult` (`:265`, "Duyệt kết quả công tác trên HRM").

### 7B. Gia hạn / kết thúc sớm công tác (`business_trip_employee_requests`)
- Một cấp: `status=1` → 2 / 3; `type` 1 = kết thúc sớm, 2 = gia hạn.
- Tạo: nhân viên tự gửi (`POST /business_trip_assigns/finish|extend`, không gate), hoặc quản lý tạo hộ cần `assign.gia_han_ket_thuc_som.create` (`BusinessTripAssignController.php:441-476`).
- Duyệt: `POST /v1/timesheet/business_trip_assigns/listFinishExtend/{id}` → `finishExtendApprove` (`:498-519`): **KHÔNG kiểm quyền, KHÔNG kiểm trạng thái chờ, KHÔNG kiểm quản lý**; gia hạn (`type=2`, `status=2`) chỉ kiểm trùng lịch (`validateExtendOverlap`). Resource: `canApprove = (status == 1)` (`Transformers/BusinessTripAssignResource/BusinessTripEmployeeRequestResource.php:22`) — FE nút theo đó (`finish-extend.vue:182,192`), không gate quyền ở trang; chỉ menu gate `assign.phieu_di_cong_tac.manage` (`menu.js:469-474`).
- Danh sách `listFinishExtend` (`BusinessTripAssignService.php:370-…`): lọc `business_trip_employees.company_id = công ty đang làm`; không lọc theo quyền/quản lý.
- Thông báo cho người xử lý: người quản lý phòng của người gửi ∩ giữ `assign.phieu_di_cong_tac.manage` (`:399, 424, 445, 470`).
- Mã duyệt thực tế theo menu là `assign.phieu_di_cong_tac.manage`, KHÔNG phải `assign.gia_han_ket_thuc_som.create` (mã này chỉ cho đường "quản lý tạo hộ"). Tự duyệt: không loại người tạo.
- Bảng gom: biểu diễn được kiểu "mã assign.phieu_di_cong_tac.manage, không quản lý" — nhưng đây là gate chỉ ở menu FE; BE không chốt, nên bảng gom chỉ nên dựa vào gate menu.

---

## 8. Thiết bị chấm công (H11)

- Cấp: `status=1` SendApprove → 2 Đã duyệt (các máy duyệt trước của cùng NV chuyển sang `Exprired`) / 3 Từ chối (`TS/Services/DeviceService.php:83-94`).
- Người duyệt dự định: quyền `timesheet.thiet_bi_cham_cong.approve` — nhưng **chỉ gate menu FE** (`menu.js:459-464`) và **gửi thông báo** cho người giữ quyền trong phòng của người gửi (`DeviceController.php:88`). Trang danh sách: hiện nút Duyệt/Từ chối khi `canApprove = status==SendApprove`, không kiểm quyền (`Transformers/DeviceResource/DeviceListResource.php:23-24`; FE `devices/index.vue:104-124`). Endpoint `POST /v1/timesheet/devices/approve/{id}` (`Routes/api.php:435`) không kiểm quyền/quản lý/trạng thái (`DeviceController.php:~105-111`).
- Danh sách `DeviceService::index` (`:19-57`) chỉ lọc `employee_infos.company_id = công ty đang làm` ⇒ mọi người đăng nhập vào được trang thấy mọi thiết bị công ty; không lọc quản lý.
- Tự duyệt: không chặn. Một cấp. Không gắn dueConfig.
- Bảng gom: biểu diễn được = `mã thiet_bi_cham_cong.approve` (+ tuỳ chọn quản lý phòng của người gửi, khớp phạm vi thông báo, KHÔNG khớp BE). Nên coi gate = mã quyền, vì BE không chốt gì.

---

## 9. Human

### 9A. Hồ sơ tự khai / Yêu cầu cập nhật thông tin cá nhân (H12)
- Cấp: `employee_update_request_status` 1 "Chờ duyệt" → 2 Đã duyệt / 3 Không duyệt (`EmployeeInfoUpdateEnums`; `HU/Services/EmployeeInfoUpdateRequestService.php:589-601`).
- FE gate: nút Duyệt/Không duyệt = `status==1 ∧ isManager`, `isManager = hasAPermission('human.ho_so_tu_khai.manage')` (`hrm-client/pages/human/employee_info/request-update/index.vue:131,150,328`). Mã này không có phạm vi (`Catalog/human.php:282-296`).
- BE: không chốt quyền ở cả 2 đường:
  - Không duyệt: `POST /v1/human/employee-update-requests/approve/{id}` → `storeApprove` chỉ `updateStatus()` (`HU/Http/Controllers/Api/V1/EmployeeInfoUpdateRequestController.php:109-148`) — không kiểm quyền, không kiểm trạng thái chờ.
  - Duyệt (ghi dữ liệu vào hồ sơ NV): `POST /v1/human/employee-update-requests/{id}` → `store` với `type=update`, `status=2` (`:160-170`, service `:600-657`) — `SaveEmployeeInfoUpdateRequest::authorize()=true` (`:252-255`); chỉ chặn nếu phiếu đã ở 2/3 (`:163-166`). Nghĩa là ai đăng nhập cũng có thể áp dữ liệu vào hồ sơ NV (nghiêm trọng, đọc code, chưa chạy thật).
- Quản lý: không có. Người thấy phiếu trong danh sách theo quyền XEM `human.ho_so_tu_khai.view` phạm vi 1-4 (`HU/Services/EmployeeInfoUpdateRequestService.php:87-102`: Tổng công ty/Công ty/Phòng(+Bộ phận)/Bộ phận/chỉ của mình) — **khác** quyền DUYỆT (`manage`). Người có `manage` nhưng `view` thấp hơn chỉ thấy phạm vi của mình.
- Thông báo chờ duyệt: người quản lý phòng của người gửi ∩ giữ `human.ho_so_tu_khai.manage` (`:210`).
- Người tạo tự duyệt: không chặn (phiếu do chính NV tạo; nếu NV đó có `manage` thì tự duyệt được).
- Nhiều cấp: không có. Prod: 0 phiếu chờ (inventory).
- Bảng gom: gate = mã `human.ho_so_tu_khai.manage` + phạm vi xem theo `human.ho_so_tu_khai.view`(scope). Là trường hợp "quyền + phạm vi dữ liệu theo quyền khác" (2 mã), cần Definition khai 2 mã.

### 9B. Thông báo nội bộ (H13)
- Cấp: `status=2` "Đã gửi thông báo" → 3 Đã duyệt (bắn thông báo TOÀN BỘ nhân viên, `SelfNotificationsController.php:120-131`) / 4 Huỷ duyệt.
- Quyền duyệt dự định: `isCurrentEmployeeHasPermission('Duyệt thông báo nội bộ')` (`HU/Entities/SelfNotifications.php:85-88`) — **tên này KHÔNG có trong Catalog** (grep toàn `app/Support/Permissions/Catalog` không thấy; chỉ có `human.thong_bao_noi_bo.manage` cho tạo, `Catalog/human.php:461`). Chuỗi có khoảng trắng nên `CurrentPermission::has` đi nhánh tên cũ `hasLegacy` (`CurrentPermission.php:70-72`) ⇒ trả false ⇒ FE không bao giờ hiện nút (`self-notification/_id/approve.vue:117` đẩy ra nếu `canApprove==false`).
- BE: `PUT /v1/human/self-notifications/{id}/toggle-approve` (`HU/Routes/api.php:358`) không kiểm quyền, không kiểm trạng thái; nhận `status` thẳng từ body (`SelfNotificationsController.php:113-134`) ⇒ ai đăng nhập cũng gọi được, duyệt xong gửi toàn công ty.
- Quản lý: không. Người tạo tự duyệt: không chặn ở BE; qua UI thì không ai duyệt được. Luồng "chết" qua UI (giữ nguyên nhận định inventory).
- Bảng gom: **không biểu diễn được** (quyền không tồn tại); nên loại khỏi bảng gom hoặc chờ nghiệp vụ khai mã mới.

---

## 10. Payroll

### 10A. Thu nhập P3 (H14, `p3_salaries`)
- Cấp: `status` 0 Đang tạo → 1 Chờ duyệt → 2 Đã duyệt / 3 Không duyệt (`PR/Entities/P3Salary.php:25-40`).
- Duyệt: `POST /v1/payroll/p3_salaries` (`store`, nhận `status` từ body, `PR/Http/Controllers/Api/V1/P3SalaryController.php:61-96`), huỷ duyệt: `POST /p3_salaries/cancel_approve` (`:98-115`). **Không chốt quyền ở BE; FE cũng không gate** (nút theo `status==1` thuần, `pages/payroll/salary-data/p3-salary/_id/approve.vue:11-22`; menu gate nhóm `Định mức thưởng P3`, `menu.js:602-605`). Danh sách `/approve` (`P3SalaryService::approve`, `:46-60`) trả mọi bảng khác Đang tạo, không lọc công ty/quyền.
- Quản lý: không. Tự duyệt: không chặn. Một cấp.
- Bảng gom: **không biểu diễn được** (không có gate nào); cần nghiệp vụ chốt mã + phạm vi trước (xem mục mơ hồ #6 trong inventory).

### 10B. Bảng chia thưởng (H15, `bonus_distributions`)
- Cấp: `status` 0 Nháp → 1 Chờ duyệt (`submit`) → 2 Đã duyệt / 3 Từ chối (`PR/Entities/BonusDistribution.php:14-17`).
- Người duyệt: quyền `payroll.bang_chia_thuong.approve` ("BGĐ duyệt bảng chia thưởng", không phạm vi, `Catalog/payroll.php:714-728`). **Khác `inventory-hrm.md`**: BE đã chuyển sang kiểm bằng helper mã quyền, 403 nếu thiếu (`PR/Http/Controllers/Api/V1/BonusDistributionController.php:108, 125`); cờ `can_approve` ở Detail resource = `status===1 ∧ có quyền` (`PR/Transformers/BonusDistributionResource/BonusDistributionDetailResource.php:63`). Không còn lỗi `->can()` trên `TpEmployee`. Còn lại chưa xác minh: có vai trò nào đang giữ mã này không (inventory ghi 0 role cho tên cũ).
- Không kiểm quản lý, không kiểm công ty/phòng của bảng; không loại người tạo (`BonusDistributionService.php:160-188`: chỉ kiểm `status===PENDING`, gán `approved_by = auth()->id()`). Người tạo có quyền BGĐ tự duyệt được.
- Danh sách `index` (`BonusDistributionService.php:25-60`) không áp quyền xem `payroll.bang_chia_thuong.view` (phạm vi 2-4) — chỉ lọc theo tham số.
- Một cấp. Không dueConfig.
- Bảng gom: biểu diễn được = `mã payroll.bang_chia_thuong.approve` (toàn hệ thống, hoặc + công ty của bảng nếu muốn chặt hơn BE).
- Ứng lương (`salary_advances`) và các màn Payroll còn lại: không thấy cột trạng thái duyệt (`PR/Entities/SalaryAdvance.php` không có status; chưa rà toàn bộ module).

---

## 11. Meeting

### 11A. Phiếu đặt phòng họp (H16)
| Cấp | `status` | Chữ (`MeetingRoomBooking::statusText`) | Điều kiện vào |
|---|---|---|---|
| Chờ duyệt | 1 `STATUS_CHO_DUYET` | Chờ duyệt | phòng có `require_approval = 1` (store/update khi đổi giờ/phòng: `MeetingRoomBookingService.php:528-530, 704-707`) |
| Đã duyệt | 2 | | phòng không cần duyệt thì tạo thẳng status 2 |
| Từ chối / Đã hủy / Hoàn thành | 3 / 4 / 5 | | |

- Người duyệt (1 cấp): `canActOnApprovalByRoom($room)` = **người phụ trách ĐÚNG phòng đó** (`meeting_room_managers`, `$room->managerIds()`) **HOẶC** có quyền `meeting.phieu_dat_phong_hop.approve` (`MT/Services/MeetingRoomBookingService.php:1435-1440`; hằng `:48-51`). Quyền không có phạm vi và KHÔNG kiểm phòng thuộc công ty nào: người giữ quyền ở công ty đang làm duyệt được phiếu của MỌI phòng (kể cả phòng công ty khác nếu biết id) — đọc code, chưa chạy thật.
- Kiểm ở BE trong service, trong transaction có khoá (`approve()` `:755-…`, `reject()` `:849-…`): thứ tự 403 quyền → 423 sai trạng thái (chỉ status=1) → 423 đã tới giờ bắt đầu (`now ≥ start_at`) → chống trùng giờ với phiếu đã duyệt (`assertNoOverlap`). Route cố ý không gắn `checkPermission` (comment `MT/Routes/api.php:133-141`).
- Duyệt phiếu thắng ⇒ tự động từ chối mọi phiếu Chờ duyệt khác trùng giờ cùng phòng (`:805-…`).
- Người đặt tự duyệt: **không chặn** — nếu người đặt đồng thời là người phụ trách phòng hoặc giữ quyền duyệt, bấm Duyệt được ở phiếu của chính mình (không có so `booked_by_employee_id` với người duyệt trong `approve()`/`reject()`). Phòng không cần duyệt thì không có bước này.
- Nhiều cấp: không có (không có chuyện nhảy cấp).
- "Ai THẤY phiếu": `applyVisibilityScope` (`:242-270`): quyền `meeting.phieu_dat_phong_hop.view` phạm vi ≥ Tổng công ty ⇒ thấy hết; phạm vi Công ty ⇒ thêm phiếu của phòng thuộc công ty; nếu không thì chỉ phiếu mình đặt / mình được mời / phòng mình phụ trách. ⇒ **người chỉ có quyền DUYỆT (không có XEM, không phụ trách phòng) không thấy phiếu để duyệt** — lệch giữa "được duyệt" và "thấy".
- Cờ ở danh sách: `is_can_approve = status==1 ∧ canActOnApproval` (`MT/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php:73`; FE `pages/meeting/bookings/index.vue:708`).
- Thông báo "Chờ duyệt": chỉ gửi cho người phụ trách phòng (`notifyPendingApproval`, `:1974-1988`), KHÔNG gửi cho người giữ quyền duyệt không phụ trách phòng.
- Hết khả năng duyệt: `status≠1` hoặc `now ≥ start_at` hoặc trùng giờ với phiếu đã duyệt. Không dueConfig.
- Bảng gom: biểu diễn được nhưng cần khai **hai nguồn OR**: (a) mã `meeting.phieu_dat_phong_hop.approve`, hoặc (b) "người đích danh theo bản ghi": `employee_id ∈ meeting_room_managers của phòng`. Không biểu diễn được bằng 1 gate "mã + quản lý phòng ban" thông thường.

### 11B. Yêu cầu dịch vụ trên phiếu đặt phòng (H17)
- `service_status=1` "Chờ chuẩn bị" → 2/3. Chỉ người phụ trách phòng (`assertCanHandleServiceRequest`, `MeetingRoomBookingService.php:1314-1331`); KHÔNG có nhánh "hoặc có quyền"; không phải luồng duyệt phiếu nhưng cùng form. Gate = "người đích danh theo bản ghi" (`managerIds`).

---

## 12. Tóm tắt loại gate để thiết kế Definition

| Loại phiếu | Gate thực sự (BE) | Có "quản lý"? | Phạm vi nào | Biểu diễn bằng 1 cột gate? |
|---|---|---|---|---|
| Đơn xin nghỉ C1 / C2 | mã PD / mã NSHC theo `status` | Có: quản lý phòng hiện tại của người tạo | công ty đang làm | Được (gate theo status); từ chối C2 cần cả 2 mã (không) |
| Kết thúc nghỉ phép | BE không chốt; FE: mã PD | Chỉ ở danh sách (phòng người tạo) | công ty | Được nhưng không khớp BE |
| Đi muộn về sớm | mã `dang_ky_di_muon_ve_som.approve` | Có: phòng người tạo | công ty | Được |
| Kết thúc đăng ký đi muộn về sớm | mã trên (BE chốt), không quản lý | Chỉ ở danh sách (`department_id` phiếu) | công ty | Được (gate = mã) |
| Yêu cầu làm thêm | mã `phieu_yeu_cau_lam_them.approve` | Có: **đơn vị thực hiện** của phiếu | công ty | Được |
| Đăng ký/Phân công làm thêm | mã `dang_ky_lam_them.approve` | Có: phòng của NV (loại 0) hoặc phòng của phiếu (loại 1) | công ty | Gate điều kiện theo `assignment_type` |
| Tra soát công C1 / C2 | mã `confirm` (C1) / mã `approve` (C2) | Có: phòng của NV đề nghị | công ty của phiếu = công ty đang làm | Được (gate theo status); người giữ 2 mã nhảy cấp |
| Phiếu giao việc | mã `assign.phieu_giao_viec.manage` (chỉ FE) | Không | — | Chỉ gate FE (BE fail-open) |
| Phiếu đi công tác | mã `assign.phieu_di_cong_tac.manage` (chỉ FE) | Không | — | Như trên |
| Gia hạn/kết thúc sớm công tác | menu: `assign.phieu_di_cong_tac.manage`; BE không chốt | Không | công ty | Như trên |
| Thiết bị chấm công | menu: `timesheet.thiet_bi_cham_cong.approve`; BE không chốt | (Chỉ thông báo theo phòng) | công ty | Như trên |
| Hồ sơ tự khai | FE: `human.ho_so_tu_khai.manage`; BE không chốt | Không (xem phạm vi theo `.view`) | theo `.view` | Cần 2 mã |
| Thông báo nội bộ | tên quyền không tồn tại | — | — | Không |
| P3 | không có gate | — | — | Không |
| Bảng chia thưởng | mã `payroll.bang_chia_thuong.approve` (BE chốt) | Không | không kiểm | Được |
| Đặt phòng họp | mã `meeting.phieu_dat_phong_hop.approve` **HOẶC** người phụ trách đúng phòng | Theo bản ghi (`meeting_room_managers`) | — | Cần OR (mã, danh sách người theo phòng) |

**Trường hợp không biểu diễn được bằng cột gate đơn giản**
1. Từ chối đơn xin nghỉ ở C2 (đòi cả PD lẫn NSHC cùng lúc).
2. Điều kiện "trưởng phòng bị chặn do hàng quá hạn" (`checkDueConfigsManager`, quyết bằng gọi ERP theo người bấm, không phải theo phiếu) — Definition phải coi là rào chắn tính theo người, không thể sinh cột SQL; lỗi ERP thì cho qua.
3. Trần giờ làm thêm/tháng (kiểm lúc bấm, theo nhân viên/tháng) — chỉ biết kết quả khi gọi hàm kiểm.
4. Hạn ngày: đơn xin nghỉ (ngày 05 tháng sau, chỉ C1), làm thêm (`start_at ≥ hôm nay`) — biểu diễn được bằng cột `approvable` (hàm theo thời gian).
5. Đặt phòng họp: gate là OR giữa mã và quan hệ "người phụ trách của phòng của bản ghi".
6. Người giữ 2 quyền ở Tra soát công nhảy cấp thẳng sang Đã duyệt.

---

## 13. Mâu thuẫn / bổ sung so với `inventory-hrm.md` và `danh-gia-tung-phieu.md`
1. Tên quyền nay là **mã**; ghi theo tên cũ trong inventory vẫn đúng nghĩa (bảng 0.1). Số dòng route/entity trong inventory đã lệch (vd H2 route `api.php:460` chứ không phải `:494`; typo `' middleware'` ở `:173`).
2. **H3 Đi muộn về sớm: KHÔNG có hạn ngày** (`LateEarlyOut.php:285-287` comment `isEditStatus`) — inventory (mục mơ hồ #1) coi 28 phiếu cũ "BE không cho duyệt nữa" là sai cho loại này; chỉ Làm thêm (H5/H6) và Đơn xin nghỉ C1 có hạn.
3. **H4: BE đã chốt quyền + trạng thái chờ** (`LateInEarlyOutChangeEndRequestController.php:47-57`) — inventory ghi "BE không chốt". Vẫn thiếu chốt quản lý.
4. **H15: đã sửa sang mã `payroll.bang_chia_thuong.approve`** (`BonusDistributionController.php:108,125`) — inventory ghi `->can()` luôn false. Còn nguyên: không kiểm công ty/phòng, người tạo tự duyệt được.
5. **H1**: người chỉ có NSHC không thấy menu (đúng) và **không từ chối được**; người chỉ có PD thấy nút Từ chối ở C2 nhưng 403 (chốt `AttendanceController.php:155-159`) — chưa có trong inventory.
6. **H1: NSHC không nhận thông báo** khi TP duyệt xong C1 (`AttendanceService.php:233-250` return sớm) — chưa có trong inventory.
7. **H5: lệch quyền nhận thông báo** (`dang_ky_lam_them.approve` vs `phieu_yeu_cau_lam_them.approve`, `OvertimeRequirementController.php:136`) — chưa có trong inventory.
8. **H6: phiếu phân công làm thêm** có `employee_id` null nên không nằm trong danh sách `/approve` dù `can_approve` đúng theo phòng — chưa có trong inventory (chưa chạy thật).
9. **H7: người giữ cả XN + PD nhảy cấp** thẳng Đã duyệt (`RequestUpdateTimeSheetService.php:267-279`) — chưa có.
10. **H8/H9: người có quyền tạo phiếu ⇒ "LƯU và DUYỆT" tự duyệt** là thiết kế FE; BE không chốt quyền cả ở `store` lẫn `storeApprove`.
11. **H16: người chỉ có quyền duyệt (không XEM, không phụ trách phòng) không thấy phiếu**; thông báo chờ duyệt chỉ đến người phụ trách phòng.
12. Chưa xác minh (cần chạy thật): hậu quả thiếu `auth:api` ở nhóm job-assignment; khả năng gọi tay `status=2` ở các endpoint tạo; người chỉ có NSHC thấy toàn bộ phiếu kết thúc nghỉ phép; prod có role nào giữ `payroll.bang_chia_thuong.approve`; số phiếu thực tế phân công làm thêm có `employee_id` null.
