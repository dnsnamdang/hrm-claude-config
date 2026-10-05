# Chấm công: chuyển bước duyệt từ nhóm nghiệp vụ sang phòng ban

**Người phụ trách:** @khoipv · **Ngày:** 18/09/2026
**Spec chi tiết:** `docs/superpowers/specs/2026-09-18-timesheet-duyet-theo-phong-ban-design.md`

## Mục tiêu
Các bước DUYỆT của phân hệ Chấm công đang lấy phạm vi theo **nhóm nghiệp vụ** (`listManageEmployeeInfoIdsByGroup()`).
Đổi sang phạm vi **nhân viên thuộc phòng ban mà người duyệt quản lý** (`employee_manage_departments`).

## Scope
| Tầng | Nội dung | Làm? |
|---|---|---|
| A | Điều kiện duyệt (accessor `can_approve` của 7 entity) | ✅ |
| B | Tab "Chờ duyệt" (6 service) | ✅ |
| C | Quyền XEM danh sách / báo cáo | ❌ giữ nguyên |
| D | Thông báo "cần duyệt" (11 điểm) | ✅ gửi cho quản lý phòng ban của người tạo đơn |
| E | Dashboard đếm việc chờ duyệt (6 dòng) | ✅ |

## Quyết định lớn
1. **Không sửa helper cũ.** `listEmployeeInfoHasPermission()` đang được module Category dùng → viết 3 helper mới trong `app/Helper/PermissionHelper.php`:
   `listManageEmployeeInfoIdsByDepartment()`, `listManageEmployeeIdsByDepartment()`, `listEmployeeInfoManageDepartmentHasPermission()`.
2. **Nguồn phòng ban:** bảng `employee_manage_departments` (+ `employees.all_department = 1` quản lý tất cả).
3. **Biên:** không tự duyệt đơn của chính mình; chỉ tính nhân viên đang làm việc (`employee_infos.status = active`).
4. **Thông báo:** dùng `sendToAllNotification` với danh sách quản lý phòng ban của người tạo đơn, thay vì quản lý nhóm.

## Ngoại lệ (giữ nguyên theo yêu cầu)
- Toàn bộ luồng **Đề nghị thanh toán công tác phí**.
- Bước `XN-Đề nghị tra soát công` (`RequestUpdateTimeSheetController:157,168`) — ở đó `auth()` là người vừa duyệt, không phải người tạo đơn.
- Dashboard phần Dự án (báo giá, gói thầu) và thông báo tới BGĐ.

## Rủi ro vận hành
Staging: 43 phòng ban có gán quản lý, 24 phòng ban có NV active, nhưng chỉ **2 phòng ban vừa có quản lý vừa có NV**; 9 người quản lý phòng ban so với 27 người quản lý nhóm; 1.503 đơn nghỉ đang chờ duyệt.
→ Phải bổ sung dữ liệu `employee_manage_departments` trước khi bật trên môi trường thật.
