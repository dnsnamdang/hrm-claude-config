# Người quản lý tất cả phòng ban chỉ duyệt phiếu của trưởng phòng

**Phụ trách:** @khoipv
**Ngày tạo:** 24/09/2026

## Bối cảnh

Sau khi chuyển bước duyệt của Chấm công / HCNS sang phạm vi phòng ban, người được tick
`employees.all_department = 1` vẫn nhận **tất cả** phiếu chờ duyệt của mọi nhân viên,
vì `listManageEmployeeInfoIds()` trả toàn bộ `employee_infos` khi gặp cờ này.

Yêu cầu: người quản lý tất cả phòng ban chỉ nhận phiếu của **trưởng phòng**
(người có bản ghi trong `employee_manage_departments`).

## Quyết định đã chốt (user xác nhận 24/09/2026)

1. **Định nghĩa trưởng phòng** = có bản ghi trong `employee_manage_departments`.
   (Cột `departments.department_lead_id` tồn tại nhưng 0 bản ghi dùng → cột chết, bỏ qua.)
2. **Phòng ban chưa gán trưởng phòng** → không ai duyệt, chấp nhận treo.
   Phải gán trưởng phòng trước khi deploy production.
3. **Cho phép KIÊM NHIỆM** (user chốt 24/09/2026): 1 người vừa tick "Quản lý tất cả phòng ban"
   vừa được gán quản lý phòng ban cụ thể. Khi đó phạm vi duyệt = **hợp 2 tập**:
   toàn bộ trưởng phòng + toàn bộ nhân viên của phòng ban mình trực tiếp quản lý.
4. **Người `all_department` cũng được tính là trưởng phòng** → duyệt chéo phiếu của nhau.
   Hàm đã sẵn loại phiếu của chính mình nên không có chuyện tự duyệt.
5. Chỉ siết nhánh **DUYỆT**. Quyền **XEM** (danh sách NV, bảng lương, dashboard HCNS)
   giữ nguyên toàn quyền cho người `all_department`.

## Số liệu staging `thanhan_stag_22092026`

| | Trước | Sau |
|---|---|---|
| Người `all_department=1` nhìn thấy | 116 NV | 12 người (9 QL phòng ban + 3 `all_department` khác) |
| Phòng ban đang hoạt động | 23 | 23 |
| Phòng ban đã có trưởng phòng | 20/23 | 20/23 |

3 phòng thiếu trưởng phòng (32 NV bị treo phiếu nếu không gán):
- [83] KD — Phòng kinh doanh HN (15 NV)
- [87] KT — Phòng Kế toán (8 NV)
- [90] TH-HCNS — Phòng Tổng hợp - Hành chính nhân sự HN (9 NV)

Thêm 3 NV có `department_id` trỏ phòng đã xóa mềm hoặc để trống → cũng treo.

## Phase 1 — Backend

- [x] Thêm helper `listDepartmentManagerEmployeeInfoIds()` vào `app/Helper/PermissionHelper.php`
      (trả `employee_infos.id` của người có bản ghi `employee_manage_departments`
       HOẶC `employees.all_department = 1`, lọc `status = active`, có cache tĩnh)
- [x] Sửa `listManageEmployeeInfoIdsByDepartment()` — thêm nhánh rẽ theo `all_department`
- [x] Sửa `listEmployeeInfoManageDepartmentHasPermission()` — chỉ nhồi người
      `all_department` vào danh sách nhận thông báo khi người tạo đơn là trưởng phòng
- [x] Sửa `listEmployeeInfoManageDepartmentHasPermission()` — loại chính người tạo đơn
      khỏi danh sách nhận thông báo (user yêu cầu fix luôn 24/09/2026)
- [x] `php -l` sạch

## Phase 2 — Verify

- [x] Tinker: 4/4 người `all_department` → 116 người còn **12 người**
- [x] Tinker: 9/9 trưởng phòng → khớp 100% công thức cũ (PASS), phạm vi KHÔNG đổi
- [x] Tinker: 3 NV thường → 0 người (đúng)
- [x] Tinker: `listEmployeeInfoManageDepartmentHasPermission('PD-Đơn xin nghỉ', …)`
      - NV thường info#5 (phòng 88) → `[10]`, KHÔNG lẫn người `all_department` ✅
      - Trưởng phòng info#3 (phòng 93) → `[1,2,4,34,56]`, CÓ người `all_department` ✅
- [x] Quét toàn bộ 117 NV đang làm việc: 86 NV có người duyệt, 31 NV không có
- [x] Tinker sau fix loại self: 4/4 người `all_department` tự tạo đơn → chỉ 3 người
      `all_department` còn lại, không có chính mình; 4/4 trưởng phòng tự tạo đơn →
      không có chính mình; NV thường không đổi (`[10]`); quét 117 NV → **0 trường hợp
      tự gửi thông báo cho mình**, số NV có/không có người duyệt giữ nguyên 86/31
- [ ] Kiểm tra tab "Chờ duyệt" đơn xin nghỉ / tăng ca / đi muộn về sớm trên UI (chờ user)

## Phase 3 — Cho phép kiêm nhiệm trưởng phòng + quản lý tất cả phòng ban

- [x] FE `pages/timesheet/setting/employees/_id/index.vue:64` — bỏ `v-if="!form.all_department"`
      để ô "Quản lý các phòng ban" luôn hiện, kèm dòng gợi ý giải thích khi đã tick all_department
- [x] BE `listManageEmployeeInfoIdsByDepartment()` — nhánh `all_department` hợp thêm nhân viên
      của các phòng ban trong `employee_manage_departments` của chính người đó
- [x] BE `EmployeeService::storeRole()` — **KHÔNG phải sửa**: `submitSave()` vốn luôn gửi
      `departments` lên (v-if chỉ ẩn render, không xoá `form.departments`) và `storeRole()`
      vốn xoá rồi insert lại đúng danh sách nhận được
- [x] BE `listEmployeeInfoManageDepartmentHasPermission()` — **KHÔNG phải sửa**: vốn query theo
      `department_id` nên người kiêm nhiệm đã nằm sẵn trong danh sách nhận thông báo
- [x] Verify kiêm nhiệm (mô phỏng trong transaction rồi rollback): gán emp#13 (info 1,
      `all_department`) kiêm trưởng phòng [90] TH-HCNS → phạm vi duyệt **12 → 19 người**,
      7/7 NV thường phòng HCNS vào được phạm vi, quyền duyệt **KHỚP** với thông báo ở cả 3 ca
      kiểm tra, NV phòng khác (info#5 phòng 88) vẫn KHÔNG duyệt được, không lẫn chính mình
- [x] Regression trên dữ liệu thật: 4/4 `all_department` vẫn 12 người, 9/9 trưởng phòng lệch 0 ca,
      quét 117 NV vẫn 86/31, tự gửi cho mình 0

## Phase 4 — Chuẩn bị dữ liệu (ngoài code)

Quét thực tế `PD-Đơn xin nghỉ`: **31 NV không có ai duyệt**, phân bố:

| Phòng ban | Tình trạng | Số NV kẹt |
|---|---|---|
| [83] KD — Phòng kinh doanh HN | đang hoạt động, thiếu trưởng phòng | 14 |
| [90] TH-HCNS — Phòng Tổng hợp - HCNS HN | đang hoạt động, thiếu trưởng phòng | 7 |
| [87] KT — Phòng Kế toán | đang hoạt động, thiếu trưởng phòng | 7 |
| [55] KHO — Phòng kho | **đã xóa mềm** 07/11/2025 | 1 |
| [30] PKS — Phòng kỹ thuật | **đã xóa mềm** 07/11/2025 | 1 |
| [71] BGĐ — Ban Giám Đốc | **đã xóa mềm** 07/11/2025 | 1 |

- [ ] Gán trưởng phòng cho 3 phòng đang hoạt động (83, 87, 90) — chờ user quyết người
- [ ] Chuyển 3 NV đang trỏ phòng ban đã xóa mềm (55, 30, 71) sang phòng ban còn hiệu lực

## Không làm

- Không đụng `listManageEmployeeInfoIds()`, `listManageDepartmentIds()`, `listManageDepartments()`
- Không sửa FE (51 điểm gọi tự ăn theo helper)
- Không migration, không thêm cột DB


## Ghi chú kỹ thuật

- `departments` có 96 bản ghi nhưng **73 đã xóa mềm** — mọi thống kê phải kèm
  `whereNull('deleted_at')`. Thực tế chỉ 23 phòng ban đang hoạt động, 20 đã có trưởng phòng.
- Cột `departments.department_lead_id` tồn tại nhưng **0 bản ghi nào dùng** → cột chết,
  không phải nguồn dữ liệu trưởng phòng.
- Model auth là `App\Models\TpEmployee` (không phải `Modules\Timesheet\Entities\Employee`) —
  muốn giả lập login trong tinker phải `auth()->setUser(TpEmployee::find($id))`.
- **Đã fix kèm (bug pre-existing):** `listEmployeeInfoManageDepartmentHasPermission()` không loại
  người tạo đơn ra khỏi danh sách nhận thông báo → người `all_department` và trưởng phòng tự tạo đơn
  vẫn tự nhận thông báo "cần duyệt" của chính mình. Đã thêm `array_diff($result, [$employee_info_id])`
  ở cuối hàm. Đã rà 12 điểm gọi: **tất cả** đều truyền `employee_info_id` của người tạo đơn
  (`auth()->user()->employee_info_id`, riêng `AttendancesExtendRequestService:81` truyền
  `$attributes['created_by_employee_info']`) → không chỗ nào cần chính người đó trong danh sách.
  Nay đồng nhất với `listManageEmployeeInfoIdsByDepartment()` vốn đã loại self.

- **Khe hở đã biến thành tính năng:** FE dùng `v-if` để ẩn ô chọn phòng ban khi tick
  `all_department`, nhưng `submitSave()` vẫn gửi `form.departments` lên BE → dữ liệu kiêm nhiệm
  vẫn lưu được dù UI không cho chọn. Thay vì bịt, user chốt **mở hẳn** cho phép kiêm nhiệm.

### Checkpoint — 24/09/2026
Vừa hoàn thành: Phase 1 (code BE) + Phase 2 (verify) + fix loại self khỏi thông báo
+ Phase 3 (cho phép kiêm nhiệm, sửa 1 file FE + 1 hàm BE) — toàn bộ PASS
Đang làm dở: không
Bước tiếp theo: build lại client + hard refresh; user test UI tab "Chờ duyệt" và màn phân quyền
nhân viên; gán trưởng phòng cho phòng 83/87/90 trước khi deploy
Blocked:

## Phase 5 — Rà soát dashboard "phiếu cần duyệt"

- [x] `Modules/Timesheet/Services/DashboadService.php` (dashboard HCNS) — 9 counter
- [x] `Modules/Payroll/Services/DashboadService.php` — 3 counter
- [x] `Modules/Category/Services/CategoryDashboardService.php` — toàn bộ dùng `ByGroup` (đúng chuẩn module Dự án)
- [x] `Modules/Training/Services/Dashboard/JobWaitingApproveService.php` — không dùng scope phòng ban
- [x] Đối chiếu số đếm dashboard vs accessor `canApprove()` trên 13 tài khoản duyệt → **0 lệch**

### Bug đã fix

`Modules/Timesheet/Services/DashboadService.php:278` — counter "Duyệt kết quả phiếu đi công tác"
dùng `where('created_by', listManageEmployeeIdsByDepartment())` thay vì `whereIn`.
Laravel `where()` gặp mảng sẽ `flattenValue()` → `head()` → **chỉ lấy phần tử đầu tiên**,
sinh SQL `where created_by = 14`. Kết quả đếm 8 thay vì 45. Đã đổi sang `whereIn`.
Đã grep toàn bộ: không còn chỗ nào mắc lỗi tương tự.

### Tồn đọng — chờ user quyết (KHÔNG thuộc scope feature này)

- `DashboadService.php:311-323` — counter "Duyệt thầu"/hợp đồng đếm rộng hơn `Contract::canApprove()`
  (thiếu điều kiện `record_type`) → số trên dashboard có thể lớn hơn số phiếu thật sự duyệt được.
  Đây là lỗi cũ thuộc module Category (nhóm nghiệp vụ), không liên quan đổi scope phòng ban.
- `Modules/Payroll/Services/DashboadService.php` — "Duyệt hợp đồng lao động" và
  "Duyệt thông báo nội bộ" đếm toàn hệ thống, không scope. Đã ghi nhận từ trước: quyền cấp hệ thống,
  chờ chốt nghiệp vụ.
- `RequestUpdateTimeSheet` chỉ có method `canApprove()`, thiếu `getCanApproveAttribute()` như
  `Attendance` / `LateEarlyOut` / `OvertimeAssignment` → FE không đọc được `can_approve` từ resource
  của entity này. Không ảnh hưởng dashboard (dashboard query trực tiếp), nhưng là điểm không đồng nhất.

### Checkpoint — 24/09/2026 (Phase 5)
Vừa hoàn thành: rà 4 dashboard, fix 1 bug đếm sai (`where` → `whereIn`, 8 → 45)
Đang làm dở: không
Bước tiếp theo: user quyết có fix counter Contract (dòng 311-323) không; build client + test
Blocked:
