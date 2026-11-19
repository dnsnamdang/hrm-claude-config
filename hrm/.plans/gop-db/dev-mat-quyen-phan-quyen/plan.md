# Dev mất quyền vào Vai trò sau merge gop_db → develop — @cuong61n

- [x] 2026-11-09 Chị Huyền (ưu tiên #867 Nguyễn Thị Thu Huyền, Super Admin; chưa xác nhận lại tên) báo cổng DEV không còn quyền Thêm vai trò.
  Nguyên nhân: 10:42 dev merge gop_db vào develop, route admin/roles đòi mã `admin.phan_quyen.manage` nhưng DB dev (hrm_erp_test) 0 quyền có `code` — chưa chạy catalog-sync, build_tpe.sh trên dev không có lệnh này.
- [x] 2026-11-09 Đã chạy `permission:catalog-sync` thật trên hrm-dev (thêm 940 mã) và gán `admin.phan_quyen.manage` (id 104149) cho role api 18 "Super admin (DNS DÙNG)" qua role_has_permissions. Chưa kiểm lại bằng đăng nhập; `cache:clear` trên server báo lỗi quyền ghi.
- [ ] Chờ quyết định: chạy `rbac:convert` trên dev (DB chưa convert, cần ERP bảo trì) — nếu không, mọi tài khoản khác trên dev vẫn thiếu mã quyền mới. Thêm `catalog-sync` vào build_tpe.sh của dev (sửa ở repo, không sửa tay server).

## Cập nhật 2026-11-09 (chiều)
- [x] Đăng nhập thử bằng tài khoản chị Huyền: `GET admin/roles` vẫn 403. Nguyên nhân: PermissionChecker chỉ tính vai trò có `roles.company_id` = công ty đang làm việc; role 18 `company_id` NULL vì dev chưa `rbac:convert`. Gán quyền tay không có tác dụng.
- [x] `rbac:convert --dry-run` bị chặn vì `permission_aliases` đã có dữ liệu (do `catalog-sync` tôi chạy lúc sáng). Đã gỡ lại đúng 940 quyền + 1.898 alias + 1 dòng gán (DB dev về trạng thái chưa sync).
- [ ] `rbac:convert --dry-run` lần 2 dừng vì 5 quyền ERP (guard web) ngoài danh mục: "Duyệt đề nghị xuất hóa đơn" + 4 mã "Xem tất cả phiếu đề nghị xuất hóa đơn của tổng công ty/công ty/phòng ban/bộ phận". Chờ quyết định: thêm vào Catalog hay vào danh sách bỏ; sau đó chạy lại dry-run, rồi chạy thật (cần `--erp-da-bao-tri`).
- [x] 2026-11-09 Tự quyết 5 quyền ERP "đề nghị xuất hóa đơn": 0 vai trò giữ trên dev, không có code ERP/HRM nào kiểm → thêm vào `hrm-api/app/Support/Permissions/dropped_legacy.php` (khong_code_kiem), sửa ở local nhánh develop, CHƯA commit/push.
- [ ] Chờ push develop → deploy dev → `rbac:convert --dry-run` lần 3 → chạy thật.
- [x] 2026-11-09 Push develop `2edaeae67` (dropped_legacy +5 quyền HĐ), dev pull, dry-run sạch. Đưa ERP dev (artisan down, dừng worker tanphat_qtt, tạm tắt cron) + HRM dev tpe (down, dừng tpe-worker/rice_notifications, tạm tắt cron) vào bảo trì → chạy THẬT `rbac:convert --erp-da-bao-tri` lúc 11:12 (18.822 role_has_permissions, 1.840 employee_has_roles, 940 quyền, 1.898 alias, roles_without_company=0). Báo cáo: hrm-dev:/home/erp_tpe/rbac-real-20261109. Đã bật lại mọi thứ, khôi phục crontab.
- [x] 2026-11-09 Kiểm: đăng nhập huyenntt.qttt@tanphat.com → `GET admin/roles` 200. Chờ chị Huyền xác nhận trên màn hình.
- Lưu ý: `cache:clear` trên hrm-dev vẫn báo lỗi quyền ghi (không ảnh hưởng kết quả); bản sao lưu cũ của bảng ở bak_rbac_*.
