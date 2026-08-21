# Plan — Phân quyền xem danh sách meeting theo cấp

**Người phụ trách:** @khoipv

## Phase 1 — BE

- [x] T1. Thêm 4 permission vào `PermissionsTableSeeder.php` (id 1095-1098, group 'Quản lý meeting', type 4)
- [x] T2. Thêm `company_id`, `department_id`, `part_id` vào `$fillable` của `Meeting.php`
- [x] T3. Gán org fields từ `auth()->user()->info` trong `MeetingController::store()` (KHÔNG đụng update)
- [x] T4. Rewrite block scope đầu trong `MeetingCriteria::apply()`: `checkPermissionList` + OR own/participant (company_members type=1)

## Phase 2 — FE

- [x] T5. `pages/assign/meeting/index.vue`: thêm `permissions` object động từ `hasAPermission(...)` cho 4 cấp, truyền `:permissions="permissions"` vào `V2BaseCompanyDepartmentFilter` (thay `is_all_company: true` cứng)

## Phase 3 — Chặn xem/sửa bằng URL (canView)

- [x] T7. Thêm `Meeting::canView()` — predicate đồng bộ scope danh sách (own + participant + 4 cấp quyền)
- [x] T8. `MeetingController::show()` → trả 403 nếu `!canView()` (chặn mở trang xem/sửa bằng URL; FE edit cũng load qua show → tự redirect 404)
- [x] T9. `MeetingController::update()` → trả 403 nếu `!canView()` (chặn submit sửa trực tiếp)

## Phase 4 — Xử lý phản hồi test Redmine #10939 (2026-08-11)

- [x] T10. BE `MeetingResource` (danh sách) trả thêm `can_manage` → FE `index.vue` ẩn nút Sửa + Xoá với người chỉ tham gia
- [x] T11. `GeneralInfo.vue`: 2 datepicker Bắt đầu / Kết thúc thiếu `:disabled="isShow"` → màn Xem chi tiết vẫn mở lịch chọn ngày được
- [x] T12. `_id/edit.vue`: GET lỗi (403) không được ở lại màn Sửa với form rỗng (bị hiểu là tạo mới → hiện bộ nút Lưu) → redirect về danh sách
- [x] T13. `Meeting::canManage()` bỏ nhánh `isCurrentEmployeeHasPermission('Xem danh sách meeting theo tổng công ty')` — quyền XEM không được dùng làm quyền THAO TÁC; chỉ người tạo meeting mới Sửa/Hoàn thành/Huỷ/Xoá (user chốt 2026-08-11). Không thêm permission mới, không đụng `MeetingCriteria` (scope danh sách vẫn theo 4 cấp quyền xem)

## Kiểm thử

- [ ] T6. Verify: user có từng cấp quyền thấy đúng phạm vi; user không quyền chỉ thấy own + participant; meeting cũ NULL không lọt cấp công ty/phòng/bộ phận.

## Checkpoint

### Checkpoint — 2026-06-05
Vừa hoàn thành: T1–T5 (toàn bộ code BE + FE). PHP lint sạch 4 file. `hasAPermission` confirm là global mixin.
Đang làm dở: (không)
Bước tiếp theo: User chạy seeder để insert 4 permission mới (id 1095-1098), gán quyền cho role qua màn phân quyền, rồi verify browser (T6).
Blocked:
