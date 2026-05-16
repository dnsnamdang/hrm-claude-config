# Design: Tab "Phiếu công tác" trong "Công việc của tôi"

## Mục tiêu

Đưa màn `Quản lý phiếu giao đi công tác` thành 1 tab trong `/assign/my-job`, UI V2Base
theo phong cách tab "Giải pháp", chỉ hiển thị phiếu liên quan đến user đăng nhập. Tính
năng giữ y hệt màn cũ.

## Scope chính

- **FE:** thêm 1 tab "Phiếu công tác" vào `pages/assign/my-job/index.vue` (sau Meeting,
  trước Chờ duyệt) + 1 component mới `components/AssignBusinessTab.vue`.
- **BE:** thêm 2 endpoint riêng vào `MyJobController` + 1 method service +
  Resource/Export mới. Không đụng code màn cũ.
- **Không đổi:** schema DB, migration, `AssignBusinessController`/Service, permission.

## Quyết định lớn

1. **API riêng**, không reuse `/assign/assign_business?type=all`. Endpoint:
   `GET /assign/my-job/assign-business-list` + `/export`.
2. **Scope "của tôi"**: `created_by = me` OR `AssignRequestEmployee.employee_id = me`.
3. **Cột gom gọn 8 cột** + `column-customization-modal` (table key
   `my_job_assign_business`).
4. **Filter gọn 8 mục** (bỏ công ty/phòng ban/nhân viên vì đã scope). Gộp 3 ô mã phiếu
   (parent_code + wr_assign_task_code + job_request_code) thành 1 ô "Phiếu giao việc/đề
   xuất". Range ngày lọc theo `from_time / to_time`.
5. **Giữ đủ 13 row action** trong dropdown `⋯`, render theo cờ `can_*` từ BE. Tái sử
   dụng toàn bộ modal có sẵn (ExtendTime, EndSoon, ConfirmCancelApprove,
   ConfirmDeleteSelected, ExportModal).
6. **Header actions**: Tạo mới + Xuất Excel + Cấu hình cột.

## Spec chi tiết

→ `docs/superpowers/specs/2026-04-20-my-job-assign-business-tab-design.md`
