# Chặn URL trực tiếp khi thiếu quyền — Danh mục mẫu phiếu thu thập thông tin

Nhánh: `tpe` (worktree `worktrees/tpe-client`)

## FE
- [x] `pages/assign/form-templates/add.vue` — gate `hasAPermission('Quản lý danh mục mẫu phiếu thu thập thông tin')`, không có quyền → redirect `/pages/extras/404`
- [x] `pages/assign/form-templates/_id/edit.vue` — gate tương tự, không gọi API load khi thiếu quyền
- [x] `pages/assign/form-templates/_id/index.vue` — ẩn nút "Sao chép" (dẫn sang màn Tạo mới) khi thiếu quyền

## Quyết định
- Màn XEM chi tiết `/assign/form-templates/{id}` **giữ mở** cho mọi user (chốt với user 2026-09-07): nút "Xem mẫu phiếu" ở màn Dự án tiền khả thi mở tab mới sang URL này.
- BE đã chặn sẵn store/update/destroy/lock/unlock/copy-data/export bằng `checkPermission`; route `show` cố ý không gate vì dùng chung cho luồng dự án/meeting.
