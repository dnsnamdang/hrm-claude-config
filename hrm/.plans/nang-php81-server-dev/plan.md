# Nâng PHP 7.4 → 8.1 server dev HRM (devhrmnew) — @cuong61n

Lý do: lỗ hổng PHP2Shell (CVE-2026-109618 / CVE-2026-109619, CVSS 9.2, vá 21/10/2026). PHP 7.4 không còn bản vá chính thức.
Phạm vi: cả 8 site trên máy dev (tpe, uat, hrm_crm, demo, nhatlinh, matviet, thanhan, thanhan2) + PHP CLI mặc định (cron, supervisor worker).

## Hiện trạng (rà 29/10/2026)
- Ubuntu 22.04, PPA ondrej, PHP 7.4.33, 1 pool chung `php7.4-fpm.sock`, 8 file nginx `sites-enabled` trỏ vào pool đó
- Cả 8 site là Laravel 8.83.x (hỗ trợ chính thức PHP 8.1); hrm-api local nhánh develop đã chạy PHP 8.1.32 hằng ngày
- Vài gói khai trần PHP ~8.0 (kreait/firebase, lcobucci/jwt 3.4, laminas-code…) → chỉ chặn `composer install`, runtime vẫn chạy; trên dev KHÔNG chạy composer install bằng 8.1 (nếu cần thì `--ignore-platform-req=php`)
- 8.1 đã EOL bảo mật 31/12/2025 → chỉ được vá nếu gói ondrej có backport; dù sao cũng tắt `session.upload_progress`

## Tasks
- [x] Sao lưu cấu hình nginx / php 7.4 / supervisor / crontab (29/10/2026) — `/home/erp_tpe/backup-php81-20261029-2110/`
- [x] apt update (cần `--allow-releaseinfo-change` vì PPA ondrej đổi Label), cài php8.1 **8.1.34-9** + bcmath curl gd mbstring mysql opcache readline xml zip (29/10/2026). Changelog gói xác nhận đã backport vá CVE-2026-109618/109619 từ 8.2.35
- [x] Tuỳ biến 8.1 (29/10/2026): `conf.d/90-hrm-custom.ini` cho fpm (post 100M, upload 20M) + cli (memory -1, max_exec 300, post 128M…) chép đúng phần lệch so với php.ini-production của 7.4; `99-opcache-tuning.ini` chép nguyên; pool www 8.1 = bản 7.4 đổi socket + `php_admin_value[session.upload_progress.enabled]=0`; `php-fpm8.1 -t` OK
- [x] Smoke test trước khi chuyển (29/10/2026): lint app/Modules/config/routes/database 8 site bằng php8.1 → 0 lỗi; `artisan route:list` 8.1 cho kết quả giống hệt 7.4 (5 site tpe/uat/hrm_crm/demo/nhatlinh lỗi sẵn "Target class RiceController/DecisionController does not exist" ở cả 7.4 — route hỏng có từ trước, không thuộc việc này)
- [x] PHP CLI mặc định → 8.1 (29/10/2026): alternatives ở auto mode nên tự chuyển khi cài; `schedule:list` đã dùng `/usr/bin/php8.1`
- [x] Đổi fastcgi_pass 8 file nginx sang `php8.1-fpm.sock`, `nginx -t` OK, reload (29/10/2026 ~21:14). API login 8 site qua cổng nội bộ trả 422 "Tên đăng nhập hoặc mật khẩu…" giống mốc 7.4, đã ấm opcache 0,02–0,17s
- [x] `supervisorctl restart all` (29/10/2026): 8/8 worker RUNNING, exe = /usr/bin/php8.1; log laravel 8 site sau chuyển không có lỗi mới. Domain dev-hrm / hrm-crm 200; uat-hrm lỗi SSL tên miền không khớp chứng chỉ (có sẵn, tầng TLS)
- [ ] Test kỹ site dev tpe (yêu cầu 29/10/2026): so sánh song song 7.4 ↔ 8.1 toàn bộ API GET (cổng tạm 127.0.0.1:18081 trỏ pool 7.4) · luồng ghi (thêm/sửa/xoá) · xuất Excel / in PDF / upload · cron + queue · giao diện Playwright
- [ ] Giữ php7.4-fpm chạy song song vài ngày để rollback, sau đó `systemctl disable --now php7.4-fpm` — **đang chờ theo dõi**
- [ ] (tuỳ) Server prod / Đức Lộc Sơn / ERP vẫn PHP 7.4 — chưa làm, chờ quyết định

## Rollback
update-alternatives --set php /usr/bin/php7.4 · sed fastcgi_pass về php7.4-fpm.sock · nginx reload · supervisorctl restart all
