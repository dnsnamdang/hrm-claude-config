# Phủ hết màn duyệt — nhóm Chấm công · Nhân sự · Tính lương · Meeting (#phiếu chờ duyệt tập trung) — @cuong61n

> 17/11/2026, nhánh `hrm-api` = `gop_db-main`. Làm theo `BRIEF-dinh-nghia-loai-phieu.md` + `BRIEF-bo-sung-phu-het-man-duyet.md` (mọi màn duyệt trên HRM phải vào Trung tâm phê duyệt; BE không chốt quyền ⇒ lấy điều kiện giao diện).
> Manifest dọn dữ liệu thử: `hrm-api/storage/app/wave2-timesheet.json` (đã dọn bằng `approval-center:clean-test --manifest=wave2-timesheet.json`).

## 1. Loại phiếu MỚI đăng ký (5)

| doc_type | Màn gốc (menu) | Cấp | Gate = điều kiện giao diện | BE chốt? |
|---|---|---|---|---|
| `business_trip_employee_request` (Gia hạn/kết thúc phiếu công tác) | Chấm công › Phê duyệt › `/timesheet/business_trip_assigns/finish-extend` | 1: status 1 "Gửi duyệt" → 2 Đã duyệt / **0** Từ chối | mã `assign.phieu_di_cong_tac.manage` (menu `menu.js:469-474`) ở công ty C **và** dòng nằm trong danh sách = `business_trip_employees.company_id` = C (`BusinessTripAssignService.php:370-377`, inner join nhân viên + hồ sơ; Resource bỏ dòng mất phiếu gốc `BusinessTripEmployeeRequestResource.php`) **và** nút = status 1 (Resource `canApprove`) | KHÔNG: `finishExtendApprove` (`BusinessTripAssignController.php:498`) không kiểm quyền / trạng thái / quản lý |
| `timekeeping_device` (Thiết bị chấm công) | Chấm công › Phê duyệt › `/timesheet/devices` | 1: status 1 → 2 / 3 (2 làm các máy đã duyệt cũ của người đó thành 4 "Hết hạn") | mã `timesheet.thiet_bi_cham_cong.approve` (menu `menu.js:459-464`) ở công ty C **và** nhân viên gửi có `employee_infos.company_id` = C (`DeviceService.php:19-57`) **và** status 1 (`DeviceListResource.php:23-24`) | KHÔNG: `DeviceController::approve` `:112` / `DeviceService::approve` `:83` |
| `employee_info_update_request` (Quản lý hồ sơ tự khai) | Thông tin nhân sự › Hồ sơ nhân sự › `/human/employee_info/request-update` (chi tiết `/{id}`) | 1: `employee_update_request_status` 1 "Chờ duyệt" → 2 / 3 "Không duyệt" | mã `human.ho_so_tu_khai.manage` (nút `request-update/index.vue:131,150,328`) **và** phiếu trong danh sách theo PHẠM VI của `human.ho_so_tu_khai.view` ở công ty đang làm (`EmployeeInfoUpdateRequestService.php:87-102`): Tổng cty = tất cả · Công ty = `company_id` phiếu · Phòng ban = phòng HOẶC bộ phận mình quản lý · Bộ phận = bộ phận mình quản lý · không có phạm vi = phiếu của chính mình | KHÔNG: `storeApprove` `:116` và `store` `:157` không kiểm quyền |
| `self_notification` (Thông báo nội bộ) | Văn bản - Hồ sơ pháp lý › `/human/self-notification/{id}/approve` | 1: status 2 "Đã gửi thông báo" (= chờ duyệt) → 3 Đã duyệt / 4 Huỷ duyệt | `SelfNotifications::canApprove()` `:87` = quyền tên cũ **"Duyệt thông báo nội bộ"** — KHÔNG có trong Catalog / `permissions` / `permission_aliases` ⇒ **không ai duyệt được** (người duyệt = rỗng, `blocked_reason` ghi rõ) | KHÔNG: `toggleApprove` `:113` không kiểm gì, phát thông báo toàn công ty |
| `meeting_room_service_request` (Yêu cầu dịch vụ phòng họp) | Meeting › Đăng ký phòng họp, popup chi tiết phiếu (`/meeting/bookings?open_booking={id}`) | 1: `service_status` 1 "Chờ chuẩn bị" → 2 "Đã chuẩn bị" / 3 "Từ chối" | chỉ người PHỤ TRÁCH ĐÚNG PHÒNG (`meeting_room_managers`), mọi công ty; phiếu chưa Hủy/Từ chối; không hạn giờ | CÓ: `assertCanHandleServiceRequest` `MeetingRoomBookingService.php:1314` (403/423/409) — truth gọi nguyên hàm này |

Ghi chú thiết kế:
- Mã quyền viết cứng trong test (không lấy từ Definition) để bắt tra nhầm mã. Người gửi tự duyệt được ở cả 5 loại (code không chặn) ⇒ `excludeOwn() = false`.
- `meeting_room_service_request` cùng bảng với `meeting_room_booking` (UNIQUE `doc_type + source_id` cho phép 2 loại cùng `source_id`); model `MeetingRoomBooking` có thêm hook `booted()` để sync loại thứ hai (trait chỉ gắn được 1 loại).
- `business_trip_employee_request`: bảng không có `created_by` (không biết quản lý nào tạo hộ) ⇒ `requester_id` = nhân viên đi công tác. 9/55 dòng chờ trong DB local là dòng mồ côi (không còn nhân viên công tác / phiếu gốc) — màn gốc không hiện nên Definition bỏ qua (describe null).
- `employee_info_update_request`: nút Duyệt ở màn **chi tiết** (`components/human-components/employee_info/request-update/EmployeeInfoForm.vue:3352-3357`) chỉ gate theo `can_reject` (status 1), không gate `manage` — ai gõ URL chi tiết đều thấy nút. Bảng gom theo cổng của danh sách (nút chính thức).

## 2. Bảng kiểm kê toàn bộ luồng của 4 module

| # | Luồng | Màn FE | doc_type | Ghi chú / bằng chứng nếu bỏ |
|---|---|---|---|---|
| 1 | Đơn xin nghỉ (2 cấp) | `/timesheet/attendance/approve`, `/{id}/approve` | `attendance` | đợt 1 |
| 2 | Đơn kết thúc nghỉ phép | `/timesheet/attendance/attendances-extend-request` | `attendances_extend_request` | đợt 1 |
| 3 | Đăng ký đi muộn về sớm | `/timesheet/late-in-early-out/approve` | `late_early_out` | đợt 1 |
| 4 | Đơn kết thúc đăng ký đi muộn về sớm | `/timesheet/late-in-early-out/change-end-request` | `late_early_out_change_end_request` | đợt 1 |
| 5 | Đăng ký / Phân công làm thêm | `/timesheet/overtime-assignment/approve`, `/timesheet/overtime-allocation` | `overtime_assignment` | đợt 1 |
| 6 | Phiếu yêu cầu làm thêm | `/timesheet/overtime-requirement/approve` | `overtime_requirement` | đợt 1 |
| 7 | Đề nghị tra soát công (2 cấp) | `/timesheet/request-update-working/approve` | `request_update_timesheet` | đợt 1 |
| 8 | Phiếu giao việc trong ngày | `/timesheet/jobassignment/approve` | `job_assignment_note` | đợt 1 |
| 9 | Phiếu đi công tác | `/timesheet/business_trip_assigns/approve` | `business_trip_assign` | đợt 1 |
| 10 | **Gia hạn / kết thúc phiếu công tác** | `/timesheet/business_trip_assigns/finish-extend` | `business_trip_employee_request` | **MỚI** |
| 11 | **Thiết bị chấm công** | `/timesheet/devices` | `timekeeping_device` | **MỚI** |
| 12 | Tra soát công do admin lập (`admin-request-update-workings`) | `/timesheet/admin-request-update-workings` | — bỏ | không có bước duyệt: `AdminRequestUpdateTimeSheetService.php:56-62` đoạn lọc status đã comment; route `Timesheet/Routes/api.php:161-167` không có approve |
| 13 | Việc của tôi (`self-jobassignment`, `job-assignment-employee/approve`) | `/timesheet/self-jobassignment` | — bỏ | chỉ liệt kê việc được giao cho chính mình (`JobAssignmentEmployeeService.php:26-41` lọc `employee_id` = người đăng nhập), chỉ hiện nhãn trạng thái (`_id/index.vue:274-282`) |
| 14 | Lưu kết quả công tác / kết quả giao việc (`storeResult`) | form phiếu | — bỏ | nhân viên tự ghi văn bản kết quả, không đổi trạng thái (`BusinessTripAssignService.php:182-191`, `JobAssignmentNoteService.php:351-360`) — tên middleware "Duyệt kết quả công tác" chỉ là nhãn cấu hình ERP |
| 15 | Công tác của tôi (`selfIndex`, `self-list`) | `/timesheet/business_trip_assigns/self-list` | — bỏ | danh sách cá nhân, chỉ nhãn trạng thái |
| 16 | Khoá / mở khoá ca làm việc, loại nghỉ | cấu hình | — bỏ | khoá danh mục, không có người chờ duyệt (`Timesheet/Routes/api.php:95,224-225`) |
| 17 | **Hồ sơ tự khai** | `/human/employee_info/request-update` | `employee_info_update_request` | **MỚI** |
| 18 | **Thông báo nội bộ** | `/human/self-notification/{id}/approve` | `self_notification` | **MỚI** (người duyệt rỗng — lỗi cấu hình quyền) |
| 19 | Phòng ban / bộ phận / team / ngành / công ty / lịch sử chức vụ — "LƯU và GỬI DUYỆT" | `pages/human/{department,part,team,major}/…`, `company/_id/config_settlement_period.vue`, `employee_info/_id/history_*.vue` | — bỏ | nút đã bị comment (`department/add.vue:12`, `department/_id/index.vue:19`, `part/_id/index.vue:19`, `major/_id/index.vue:19`, `team/_id/index.vue:19`, `history_positions.vue:12`, `history_statuses.vue:12`, `config_settlement_period.vue:12`) |
| 20 | Khoá/mở khoá danh mục Human | nhiều màn | — bỏ | thao tác của người quản lý danh mục, không có hàng chờ |
| 21 | Bảng chia thưởng | `/payroll/bonus-distribution` | `bonus_distribution` | đợt 1 |
| 22 | **Thu nhập P3** (`p3_salaries`) | `/payroll/salary-data/p3-salary/approve`, `/{id}/approve` | — **CHƯA ĐĂNG KÝ, báo điều phối** | xem mục 3 |
| 23 | **Ứng lương** (`salary_advances`) | `/payroll/salary/salary-advance` | — bỏ | bảng KHÔNG có cột trạng thái (`SHOW COLUMNS`: apply_date, company_id, created_*, department_id, id, part_id, percent, table_name, updated_*; `Entities/SalaryAdvance.php:14-22`); `Routes/api.php:219-225` không có route duyệt; `SalaryAdvanceController::approve` `:40` gọi `salaryAdvanceService->approve()` **không tồn tại** (code chết); FE `pages/payroll/salary/salary-advance/` không có nút duyệt |
| 24 | Thu nhập khác / Khấu trừ khác / Phụ cấp khác | `/payroll/salary-data/other-*` | — bỏ | chưa có chức năng: `other-income/_id/index.vue:17`, `other-allowance/_id/index.vue:18` ghi `TODO: Thêm chức năng duyệt` |
| 25 | Khoá bảng lương (`salaries/{id}/lock`) | bảng lương | — bỏ | người lập tự khoá (`SalaryController.php:337`), không chờ người khác |
| 26 | Phiếu đặt phòng họp | `/meeting/bookings` | `meeting_room_booking` | đợt 1 |
| 27 | **Yêu cầu dịch vụ phòng họp** | `/meeting/bookings?open_booking=` | `meeting_room_service_request` | **MỚI** |
| 28 | Check-in / check-out QR (`scan/confirm`) | màn quét QR | — bỏ | xác nhận có mặt của người dùng phòng (`MeetingRoomQrController.php:44`, action checkin/checkout), không phải bước duyệt; Hủy phiếu do người đặt tự hủy |

Đợt 1 đã rà lại, KHÔNG phát hiện sai / thiếu cấp phải sửa (không tăng `version()` Definition nào của đợt 1). Các lỗi code gốc đã ghi ở `03-cham-cong-nhan-su.md` mục 13 và `dinh-nghia-cham-cong-a.md` mục 4 vẫn nguyên.

## 3. CẦN NGƯỜI ĐIỀU PHỐI QUYẾT — Thu nhập P3 (chưa đăng ký)

Không có BẤT KỲ gate nào ⇒ theo phụ lục, dừng và báo (không đoán):
- BE: `POST payroll/p3_salaries` (`P3SalaryController::store`, nhận `status` từ body), `POST …/cancel_approve` `:98`, `GET …/approve` — route không có `checkPermission` (`Payroll/Routes/api.php:152-158`), `P3SalaryService::approve` (`:46-60`) trả mọi bảng khác "Đang tạo", không lọc công ty / quyền.
- FE: `p3-salary/approve.vue` và `_id/approve.vue` **không có mục menu / liên kết** nào dẫn vào (chỉ gõ URL; `components/menu.js:603-605` chỉ có `/payroll/salary-data/p3-salary`); nút Duyệt/Từ chối chỉ theo `status == 1` (`_id/approve.vue:18-24`); nút **"Gửi duyệt" ở `_id/index.vue:17-19` đã bị comment** ⇒ từ UI không thể đưa bảng sang "Chờ duyệt" (DB local: 44/44 bảng P3 đang ở "Đang tạo").
- Catalog `app/Support/Permissions/Catalog/payroll.php:89-137` chỉ có `payroll.dinh_muc_thuong_p3.view/create/update/delete`, **không có mã duyệt**.
- Đề xuất: (a) nếu nghiệp vụ còn dùng P3 duyệt → thêm mã `payroll.dinh_muc_thuong_p3.approve` (scope không phạm vi), gate BE bằng `checkPermission`, bỏ comment nút Gửi duyệt, thêm mục menu "Duyệt định mức thưởng P3"; người duyệt = người giữ mã ở công ty = `p3_salaries.company_id` (cột đã ghi lúc lưu `P3SalaryService::save`). (b) Hoặc, nếu chưa dùng, giữ nguyên không đăng ký. Khi chốt xong chỉ cần thêm 1 file Definition (`Definitions/Payroll/P3SalaryDefinition.php`, trait trên `P3Salary` — đã `extends BaseModel`).

## 4. "BE không chốt quyền" — danh sách chuyển người phụ trách module vá BE

| Module | Endpoint không chốt | Việc đề xuất |
|---|---|---|
| Timesheet | `POST timesheet/business_trip_assigns/listFinishExtend/{id}` (`BusinessTripAssignController.php:498`) | `checkPermission:assign.phieu_di_cong_tac.manage` + kiểm `status == 1` + kiểm công ty |
| Timesheet | `POST timesheet/devices/approve/{id}` (`DeviceController.php:112`) | `checkPermission:timesheet.thiet_bi_cham_cong.approve` + kiểm `status == 1` + công ty |
| Human | `POST human/employee-update-requests/approve/{id}` (`EmployeeInfoUpdateRequestController.php:116`) và `POST …/{id}` type=update status=2 (`:157`) — ghi dữ liệu thẳng vào hồ sơ nhân viên | `checkPermission:human.ho_so_tu_khai.manage` + kiểm phạm vi `…view` + trạng thái chờ (nghiêm trọng nhất) |
| Human | `PUT human/self-notifications/{id}/toggle-approve` (`SelfNotificationsController.php:113`) — phát thông báo TOÀN công ty | thêm mã `human.thong_bao_noi_bo.approve` vào Catalog + `checkPermission` + `status == 2`; sửa `SelfNotifications::canApprove()` (`:87`) dùng mã đó |
| Payroll | P3 (mục 3) | như mục 3 |
Đợt 1 còn: Đơn kết thúc nghỉ phép, Phiếu giao việc, Phiếu đi công tác (đã ghi ở các báo cáo cũ).

## 5. Kiểm chứng

- Test PHPUnit mới (5 file, 43 test): `tests/Feature/ApprovalCenter/Timesheet/{DeviceDefinitionTest,BusinessTripEmployeeRequestDefinitionTest}.php` · `Human/{EmployeeInfoUpdateRequestDefinitionTest,SelfNotificationDefinitionTest}.php` · `Meeting/MeetingRoomServiceRequestDefinitionTest.php`.
- Đột biến (cố ý làm sai Definition, test phải đỏ): Device 7/7 · Gia hạn công tác 10/10 · Hồ sơ tự khai 12/13 (1 đột biến tương đương: `(int) null` = 0 không khớp id nào) · Thông báo nội bộ 8/8 · Dịch vụ phòng họp 8/9 (1 tương đương: bỏ `=== null` vì `(int) null !== 1`). Các ca ban đầu SỐNG sót (truth bỏ điều kiện status; công ty cố định = 1; dòng mồ côi) đã bổ sung ca test cho tới khi bị bắt.
- `approval-inbox:verify` (kèm phiếu thử, sample 40) — so / được duyệt thật / chênh lệch: Device 7.992 / 83 / 0 · Gia hạn công tác 27.508 / 2.325 / 0 · Hồ sơ tự khai 3.114 / 165 / 0 · Thông báo nội bộ 6.400 / **0** / 0 (không ai có quyền — đúng bản chất) · Dịch vụ phòng họp 2.400 / 0 (mẫu ngẫu nhiên không trúng người phụ trách) và **77.940 / 40 / 0** khi thử đủ nhân viên.
- Đối soát lại trên dữ liệu THẬT sau khi dọn phiếu thử (sample 40): Device 12 phiếu / 5.328 cặp / 63 được duyệt / 0 chênh lệch · Gia hạn công tác 46 / 24.334 / 2.254 / 0 · Thông báo nội bộ 10 / 4.000 / 0 / 0.
- Phiếu pending THẬT trong DB local (không tính phiếu thử): Device 12 · Gia hạn công tác 55 (46 hiện được trên màn, 9 mồ côi) · Hồ sơ tự khai 0 · Thông báo nội bộ 10 (status 2 — không ai duyệt được) · Dịch vụ phòng họp 0.
- API thật `GET /api/v1/approval-center/inbox?doc_type=…` (JWT dựng bằng `auth('api')->claims`): trả đúng hàng, `status_text`/`status_color`/`handler_path`/`requester_name` cho 4 loại có người duyệt; `handler_path` 5 loại đều là route FE có thật (`pages/timesheet/devices/index.vue`, `pages/timesheet/business_trip_assigns/finish-extend.vue`, `pages/human/employee_info/request-update/_id/index.vue`, `pages/human/self-notification/_id/approve.vue`, `pages/meeting/bookings/index.vue` xử lý `open_booking`). Chưa chạy Playwright.

## 6. File đã tạo / sửa

Tạo: `Modules/ApprovalCenter/Definitions/Timesheet/{DeviceDefinition,BusinessTripEmployeeRequestDefinition}.php` · `Definitions/Human/{EmployeeInfoUpdateRequestDefinition,SelfNotificationDefinition}.php` · `Definitions/Meeting/MeetingRoomServiceRequestDefinition.php` + 5 file test ở mục 5.
Sửa (chỉ thêm trait `SyncsApprovalInbox` + `approvalInboxDocType()`): `Modules/Timesheet/Entities/{BusinessTripEmployeeRequest,Device}.php`, `Modules/Human/Entities/{EmployeeInfoUpdateRequest,SelfNotifications}.php`; `Modules/Meeting/Entities/MeetingRoomBooking.php` thêm hook `booted()` cho loại thứ hai.
Chỗ ghi bằng query builder: rà `app/` + `Modules/` cho 5 bảng — chỉ có `DeviceService::approve` `Device::where(...)->update(['status' => Exprired])` (đổi máy đã duyệt → hết hạn, không đụng phiếu đang chờ nên không cần `scheduleSync`) và `SendMeetingRoomBookingReminders` (cột nhắc giờ). Mọi đường đổi trạng thái khác đi qua Eloquent `save()/create()`. Không chạy migration nào.
