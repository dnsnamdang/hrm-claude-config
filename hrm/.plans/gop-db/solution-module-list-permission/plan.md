# Quyền xem danh sách Hạng mục giải pháp (không có số Redmine) — @cuong61n

Màn `/assign/solution-modules` (menu Làm giải pháp > Hạng mục giải pháp).

## Vấn đề
- BE + FE kiểm 4 tên quyền "Xem danh sách hạng mục dự án theo tổng công ty/công ty/phòng ban/bộ phận" nhưng 4 tên này chưa từng khai trong Catalog / `permission_aliases` → `hasLegacy` luôn false, kể cả Super Admin → ai cũng chỉ thấy hạng mục mình tạo/liên quan.

## Tasks
- [x] 17/11/2026 Khai mã `assign.hang_muc_giai_phap.view` (phạm vi 1–4) vào `Catalog/assign.php`, legacy = 4 tên cũ. Dry-run `permission:catalog-sync` báo "Thêm" đúng mã này.
- [x] 17/11/2026 BE `SolutionModuleService::index()`: lọc bằng `HrmScopeContext::applyCurrent` (record_unit) + giữ "mình tạo / leader / thành viên / PM". Export dùng chung hàm này.
- [x] 17/11/2026 FE `pages/assign/solution-modules/index.vue`: cờ phạm vi lấy từ `permissionScope(mã)`.
- [x] 17/11/2026 Đã push `origin/gop_db` (api 0279124e9, client e0850240d) và deploy prod bằng ~/build_tpe.sh; catalog-sync prod báo thêm `assign.hang_muc_giai_phap.view`.
- [x] 17/11/2026 Fix lỗi do chính mình: phạm vi Tổng công ty không thêm điều kiện nào → bọc trong orWhere thì Laravel bỏ nhóm where rỗng, quyền Tổng công ty bị mất (Nguyễn Thị Lệ, TPE_Super Admin có mã scope 4 nhưng thấy 0/7 hạng mục). Sửa bằng probe query; push d12401051, pull BE prod. Kiểm trên prod bằng tinker (chỉ đọc): Lệ ở công ty 1 và 2 đều thấy 7/7.
- [ ] Cấp quyền ở `/admin/roles` (phạm vi Tổng công ty cho vai trò cần xem tất cả) rồi kiểm lại màn trên prod — việc của user. Chưa test dữ liệu thật.
- Trạng thái: đã deploy prod 17/11/2026, chờ cấp quyền + test.
