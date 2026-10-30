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
- [x] Test kỹ site dev tpe (29/10/2026). Cách test: so sánh song song cùng request trên 7.4 (cổng tạm 127.0.0.1:18081, file nginx `zz-tmp-php74-tpe-compare`) và 8.1 (:8081)
  - API GET: 2.219 route (1.552 không tham số + route `{id}` lấy id thật từ danh sách cha); 1.999 giống hệt; bỏ 420 route có tác dụng phụ (sync/calc/send/import/logout…) + 157 route thiếu id
  - Khác biệt: (a) **lỗi thật** `TimesheetService::listManageEmployeeInfoIds()` gọi static ở `SalaryService.php:410,515` → Báo cáo thu nhập tháng/năm + xuất Excel 500 trên 8.1; (b) export nặng hết RAM 128M ở CẢ 2 bản (có sẵn; 8.1 vá CVE nên giết worker → 502 thay vì 500); (c) chỉ khác câu lỗi PHP 8 ("Attempt to read property" thay "Trying to get property") — lỗi có sẵn cả 2 bản; (d) đổi thứ tự dòng có khoá sort bằng nhau (PHP 8 sort ổn định) — dữ liệu đủ; (e) `job_type_name` phiếu làm thêm 227/6756: cột `job_type` chứa nhầm câu mô tả, 7.4 so `"chữ"==0` ra nhãn sai "Khai thác thị trường", 8.1 để trống — **lỗi dữ liệu cũ**, 8.1 đúng hơn
  - Giao diện: Playwright mở 529 trang danh sách (đăng nhập namdangit) → 6 API 500 + 1 trang 404; so 7.4 thì chỉ 2 API báo cáo thu nhập do 8.1, còn lại lỗi có sẵn (rank_details thiếu cột, assign_task_by_province, coursesAssignGrading, employee_infos `other_income_id=undefined`, manpower-allocations 404)
  - Luồng ghi trên 8.1: thêm/xem/sửa/khoá/sửa-khi-khoá/mở khoá/xoá ĐVT, xuất Excel, upload S3, in PDF meeting → đúng; xuất PDF khách hàng hết RAM ở cả 2 bản
  - Cron: 17 lệnh lập lịch an toàn (decision/human/assign/finance…) + calc:timesheet + schedule:run chạy bằng 8.1 exit 0; failed_jobs 0; đăng nhập JWT OK
  - Quét tĩnh toàn bộ code (Reflection) tìm gọi static vào method thường: tpe chỉ có SalaryService (+ `PayrollMailSeeder` chạy tay)
- [x] **Sửa** `Modules/Payroll/Services/SalaryService.php` (local hrm-api nhánh develop, 29/10/2026): 2 chỗ đổi sang `(new TimesheetService(new Attendance()))->listManageEmployeeInfoIds(...)` — copy khuôn `Modules/Timesheet/Support/ApproveScope.php:56`, không sửa hàm dùng chung. Test API local PHP 8.1: income_report_month / year + 2 export → 200. User đồng ý → commit `1b19f762c` push `develop`, deploy dev tpe bằng `~/build_tpe.sh` (BE fast-forward, FE không đổi bỏ qua build) 29/10/2026
- [x] **Rollback 3 site matviet, thanhan, thanhan2 về PHP 7.4** (29/10/2026 ~22:30): quét tĩnh thấy ~16 chỗ gọi static ở lõi chấm công (`Holiday::isHoliday`, `AttendanceWatchRegulation::isWeekend/standard/congWeekend`, `DepartmentManpowerService::checkDinhBien`…); log xác nhận matviet 4 + thanhan2 8 lỗi tính công từ 21:14. Đã đổi nginx 3 site → php7.4-fpm.sock, crontab 13 dòng → `php7.4 artisan`, supervisor 3 worker → `/usr/bin/php7.4`; chạy bù attendance:fetch + calc:timesheet 2 site → exit 0; failed_jobs 0. Bản crontab trước rollback: `/tmp/php81test/crontab.before-rollback3`
- [ ] Các nhánh uat (tpe), demo (tpe), nhatlinh (main), hrm_crm (feat/chuyen-doi-hang-hoa) cũng có lỗi SalaryService y hệt → cần sửa trên từng nhánh
- [x] Verify sau deploy (29/10/2026): chạy lại 63 route từng lệch 7.4↔8.1 → 4 route báo cáo thu nhập hết 500 (month + 2 export giống hệt 7.4; year chỉ khác thứ tự dòng); còn 8 route 502 đều là export nặng ~190MB vượt memory_limit 128M (đo CLI: 7.4 = 187,9MB, 8.1 = 195,5MB) — có sẵn, 7.4 cũng 500/lúc được lúc không. Màn FE `/human/report/income_report_*` tự chuyển về trang chủ vì mục menu đang bị comment trong `components/menu.js` (có sẵn, không liên quan PHP)
- [x] Xoá cổng tạm `zz-tmp-php74-tpe-compare` + /tmp/php81test (có JWT) + php81-smoke.sh (29/10/2026); 8 site trả 422 bình thường
- [ ] Đề xuất (chờ user): nâng `memory_limit` pool php-fpm 8.1 từ 128M → 256M cho các export nặng (meeting/export, customers/export-pdf, product-models/getAll…)
- [ ] Giữ php7.4-fpm chạy song song vài ngày để rollback, sau đó `systemctl disable --now php7.4-fpm` — **đang chờ theo dõi**
- [ ] (tuỳ) Server prod / Đức Lộc Sơn / ERP vẫn PHP 7.4 — chưa làm, chờ quyết định

## Nâng Thành An (thanhan, nhánh `thanhan-dev`) + Demo Thành An (thanhan2, nhánh `master`) + Matviet (nhánh `matviet`) lên 8.1 — yêu cầu 30/10/2026
- [x] Kiểm lại 30/10 08:45: 2 site Thành An chạy 7.4 ổn từ lúc rollback; 5 lỗi static thanhan2 đều trước rollback (22:00–22:20); 2 lỗi lặp có sẵn từ trước đổi PHP (lịch `quotations:notify-expiration` 07:00 mà nhánh master không có lệnh — từ 25/10; máy chấm công `fad40f3a6324.sn.mynetname.net` cURL 7 — từ 28/09)
- [x] Sửa (30/10/2026): repo `DNS-Media/hrm-thanhan-api` (cả 3 site chung repo). Khai `static` cho 7 hàm không dùng `$this` — `AttendanceWatchRegulation::standard/isWeekend/congWeekend/isWeekendLamThem/calcWeekendLabour`, `Holiday::isHoliday`, `DepartmentManpowerService::checkDinhBien` — đúng cách nhánh develop hrm-api đã làm (commit 3b5393388, 5f2ad9d9e, 10/2024); không có class con override. Commit + push: thanhan-dev `aa5e4601`, master `2fc4fbdb`, matviet `90957b8a`. Deploy BE tay (pull + migrate + route:cache + seeder quyền bằng php7.4, không build FE); thanhan2 kéo kèm 1 commit có sẵn của người khác `7d1c7b294`. Quét lại tĩnh: chỉ còn `PayrollMailSeeder` (chạy tay, tpe cũng còn)
- [x] Test tính công 7.4 ↔ 8.1 (checksum nội dung bảng, bỏ cột thời gian): matviet `timesheet_details` 12.873 + `timesheet_summaries` 13.421 + `employee_attendances` GIỐNG HỆT; thanhan2 `timesheet_details` 67.111 + `timesheet_summaries` 68.029 GIỐNG HỆT (lần 7.4 chạy lại lệch do cron attendance:fetch 09:05 kéo lượt quẹt mới)
- [x] So sánh API GET thanhan (526 route) + matviet (429): mọi route lệch đều lỗi ở CẢ 2 bản (chỉ khác câu lỗi PHP 8), hoặc lệch 1 giây / thứ tự / `job_type` dữ liệu cũ. **Khác thật duy nhất: thâm niên `diffInMonths`** — 5/184 NV thanhan vào làm 01/03: 7.4 đếm dư 1 tháng (2009-03-01→2026-10-30: 7.4=212, 8.1=211, đúng=211) → 8.1 ĐÚNG
- [x] Lấy token test: tài khoản namdangit ở 3 site khác mật khẩu → sinh JWT trực tiếp cho user Super admin (id 13 / 1) bằng `auth("api")->login()`, không đổi mật khẩu
- Lưu ý: demothanhan đang có người dùng thật (updated_by 43, 44, 140 sửa dự án/báo giá lúc 09:00)
- [x] So sánh API thanhan2 (525 + 277 route có id): lệch đều là lỗi cả 2 bản / nhiễu tải (getPersonnel/export-data chạy lại tuần tự 2 bản cùng 200, 22.016B); tính công lần 4 (8.1) = lần 3 (7.4) trên cùng dữ liệu
- [x] Luồng ghi trên 8.1 (3 site): thêm Đơn vị tính + Ngân hàng → 200; đã dọn bản ghi test. Phát hiện lỗi CÓ SẴN (7.4 cũng vậy): xoá Đơn vị tính lỗi `UnitController::delete does not exist`; **route `DELETE api/v1/human/banks/{id}` không có `auth:api` → không đăng nhập vẫn xoá được ngân hàng** (lỗ hổng bảo mật, chưa sửa — chờ user)
- [x] **Chuyển 3 site sang 8.1 lúc 09:30 30/10/2026**: nginx 3 file → php8.1-fpm.sock, crontab bỏ `php7.4` (bản trước: `/tmp/php81test/crontab.before-81-3site`), supervisor 3 worker → `command=php`. Kiểm: API + user-profile + domain 200; attendance:fetch + calc:timesheet bằng 8.1 exit 0 (matviet, thanhan2); log 3 site 09:30→09:43 không lỗi, failed_jobs 0; cron 09:40 thanhan2 cập nhật 112 dòng timesheet_summaries. Đã xoá 3 cổng tạm + token test
- Giờ cả 8 site trên dev đều chạy PHP 8.1
- [ ] Test so sánh 7.4 ↔ 8.1 từng site (API GET + cron + luồng ghi) trước khi chuyển
- [ ] Commit + push 2 nhánh, deploy, chuyển nginx / cron / worker 2 site sang 8.1, theo dõi log

## Rollback
update-alternatives --set php /usr/bin/php7.4 · sed fastcgi_pass về php7.4-fpm.sock · nginx reload · supervisorctl restart all
