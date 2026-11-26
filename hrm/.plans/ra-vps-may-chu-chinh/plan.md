# Rà VPS trên máy chủ chính etekserver không còn hoạt động (chưa có số Redmine) — @cuong61n

## Phase 1 — Kiểm kê & đánh giá mức hoạt động 12 VM (26/11/2026)

- [x] 26/11/2026 — Liệt kê VM trên KVM `etekserver` 124.158.4.24 (`virsh list --all`): 12 VM đều running, host uptime 660 ngày, load 12.
  - Kỹ thuật: ánh xạ MAC→IP qua `ip neigh`; đo CPU/mạng từng VM 10s bằng `virsh domstats`; đọc `/etc/nginx/sites-enabled` để biết domain→VM; đếm request 14 ngày theo Referer trong `/var/log/nginx/access.log*` của host.
- [x] 26/11/2026 — SSH song song vào 10/12 VM (user erp_tpe, ProxyJump may-chu-chinh): uptime, `last`, mtime log nginx/laravel, cổng nghe, crontab, `.env` DB_HOST. Không vào được `.101` (tanphat_erp_db) và `.160` (minh_os) — không có khoá.
- [x] 26/11/2026 — Kết luận (báo user):
  - **Không hoạt động lâu ngày (ứng viên tắt/thu hồi):**
    - `tanphat_hrm-base` (.104, 4 CPU/4 GB): nginx access log trống từ 06/2024 (log cuối 26/06/2024), không domain trỏ vào, cron/worker đã tắt 04/11; chỉ còn mysqld chạy nền. Đăng nhập cuối 04/11/2026 (là mình). CPU time tích luỹ 128 triệu giây = từng chạy rất nặng trước đây (Aborted_connects).
    - `admin-hrm` (.112, 4 CPU/4 GB, hostname zitechrm): domain admin.eteksofts.com:8086 chỉ ~377 request/14 ngày toàn bot/scanner (`/misc/drupal.js`, `/api/metrics`), laravel.log cuối 04/11. Cron/worker đã tắt 04/11.
    - `zitec_erp` (.108, 4 CPU/4 GB): /var/www/html chỉ còn index mặc định nginx (21/11/2026), docker không container, log web.eteksofts.com 1–5 dòng/ngày toàn scanner; erp.zitecgroup.com/host.eteksofts.com:9000 (nginx-ui) không ai dùng.
  - **Hoạt động yếu nhưng còn dùng:** `zitec_hrm` (.110) — kasaco + ori còn laravel.log ghi hằng ngày, cron attendance:fetch chạy; thư mục `wit`, `tpe` trên đó chết từ 02/2025 & 10/2025. `tanphat_hrm-duclocson` (.106) — ~2.300 request/14 ngày, cron chạy, còn dùng.
  - **Đang dùng mạnh:** tanphat_erp (.100), tanphat_hrm_db (.103, CPU 650%), tanphat_hrm-app (.102), dev_hrm_new (.111), VPS_DEV (.113 — đĩa 95%), tanphat_erp_db (.101 — DB của EtekGreen/EtekPower/NewErp prod + erp_dev/Stag/uat trên .113), minh_os (.160 — ai.dnsmedia.vn, pos.hoabinhcomputer.com, yensaohuetay.com, luxurycar.group có traffic).
- [ ] Chờ user quyết định tắt VM nào (shutdown trước, giữ image vài tuần rồi mới xoá); chưa thao tác gì trên server.

### Checkpoint — 26/11/2026 15:10
Vừa hoàn thành: kiểm kê + đánh giá 12 VM, báo user 3 VM không hoạt động.
Đang làm dở: —
Bước tiếp theo: user chốt danh sách tắt → `virsh shutdown` + ghi lại, gỡ cổng 2226/2235/2228 và site nginx tương ứng nếu tắt.
Blocked: cần user quyết định.
