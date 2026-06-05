# Phân quyền xem danh sách meeting theo cấp — Design

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-05
**Module:** Assign — màn `assign/meeting`

## Mục tiêu

Bổ sung phân quyền xem danh sách meeting theo 4 cấp tổ chức (tổng công ty / công ty / phòng ban / bộ phận), bám sát đúng pattern màn **giải pháp (solutions)**. Nếu user không có quyền nào trong 4 cấp, vẫn xem được meeting **do mình tạo** hoặc **mình có trong Thành phần — Phía Công ty**.

## Hiện trạng

- Bảng `meetings` đã có `company_id`, `department_id`, `part_id` (migration 2026_01_03) nhưng `store()/update()` **không** gán → tất cả record đang NULL.
- `MeetingCriteria` hiện chỉ lọc `status != Đang tạo OR created_by = mình` → ai cũng xem được mọi meeting đã lên lịch.
- Chưa có permission danh sách meeting trong `PermissionsTableSeeder` (chỉ có danh mục loại meeting + báo cáo meeting).
- FE `index.vue` đã có bộ lọc Công ty → Phòng ban → Bộ phận (`V2BaseCompanyDepartmentFilter`) nhưng hardcode `is_all_company: true`.
- "Thành phần — Phía Công ty" = `meeting_employees` type=1, match qua `employee_id`.

## Quyết định chốt

1. **Logic scope = additive như màn giải pháp**: dùng helper `checkPermissionList()` cho phần phân cấp (helper đã tự cộng `created_by` mỗi cấp), rồi **OR thêm** điều kiện own + participant (Phía Công ty). Own + participant **luôn** thấy bất kể cấp.
2. **Không backfill** dữ liệu cũ: chỉ gán `company_id/department_id/part_id` cho meeting tạo mới. Meeting cũ NULL chỉ hiện qua quyền "tổng công ty" hoặc own/participant.
3. Chỉ tính **Phía Công ty** (`company_members`, type=1); **không** tính khách hàng (`customer_members`, type=2).
4. **Không** gắn `checkPermission` middleware vào route `index`/`export` (user không quyền vẫn xem own/participant; việc lọc do Criteria đảm nhận).
5. `update()` **không** đụng 3 cột org (giữ theo người tạo gốc).

## 4 permission mới (seeder)

`group = 'Quản lý meeting'`, `type = 4`, id từ 1095:

| id | name |
|---|---|
| 1095 | Xem danh sách meeting theo tổng công ty |
| 1096 | Xem danh sách meeting theo công ty |
| 1097 | Xem danh sách meeting theo phòng ban |
| 1098 | Xem danh sách meeting theo bộ phận |

## Phạm vi mỗi cấp

- **Tổng công ty** → tất cả (trừ Đang tạo của người khác).
- **Công ty** → `company_id` = công ty hiện tại + own + participant.
- **Phòng ban** → phòng ban quản lý + bộ phận quản lý + own + participant.
- **Bộ phận** → bộ phận quản lý + own + participant.
- **Không quyền nào** → chỉ own + participant.

## Phạm vi thay đổi

**BE (3 file):**
- `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — thêm 4 permission.
- `Modules/Assign/Repositories/Criteria/MeetingCriteria.php` — rewrite block scope đầu.
- `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php` — gán org fields trong `store()`.
- `Modules/Assign/Entities/Meeting/Meeting.php` — thêm 3 cột vào `$fillable`.

**FE (1 file):**
- `pages/assign/meeting/index.vue` — `permissions` động từ `hasAPermission(...)`, truyền vào `V2BaseCompanyDepartmentFilter`.

**Không** migration backfill. Không đụng hàm dùng chung (`checkPermissionList` dùng nguyên trạng).

## Edge cases

- `auth()->user()->id` = employee id (khớp `created_by` và `company_members.employee_id`) — đã verify qua `Meeting::canEdit()`.
- Meeting cũ NULL org → chỉ hiện ở cấp tổng công ty hoặc own/participant (chấp nhận).
- `current_company_role` = công ty đang chọn của user (dùng trong `checkPermissionList`).
