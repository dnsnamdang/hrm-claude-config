# Brief Fix-1 — sửa BE hrm-api theo review T1 (`2c-review-t1-t3.md`)

Repo `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api`, nhánh `feat/cdhh-2c-xe` (KHÔNG đổi nhánh/merge/push/stash). DB dev `hrm_erp_giacty`. Đọc `2c-review-t1-t3.md` + `2c-t1-report.md` cùng thư mục `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-hang-hoa/chuyen-danh-muc-xe/`.
Trước artisan/phpunit: `ls bootstrap/cache/config.php` không tồn tại + `php artisan config:clear`. PHP `/opt/homebrew/opt/php@7.4/bin/php`.

## Sửa
1. **C1 — id quyền**: dời 8 quyền 1699–1706 ⇒ **1720–1727** (cùng thứ tự). `origin/develop` đã dùng tới 1711, `origin/gop_db` tới 1698. Trước khi ghi: `git fetch origin` rồi quét MỌI nhánh remote (`git branch -r`) đọc max id seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`; nếu có nhánh đã chạm 1720–1727 thì lấy dải trống kế tiếp và ghi rõ. Sửa seeder + mọi chỗ khác gõ cứng id (test, FE không có). DB `hrm_erp_giacty`: UPDATE id 8 dòng (đã xác nhận chưa role nào gán — kiểm lại `role_has_permissions`/`model_has_permissions`/`employee_has_permissions` = 0 trước khi đổi). Xoá cache quyền (xem cách test làm / `permission:cache-reset`).
2. **I1 — lộ dữ liệu lái xe**: `external-drivers/getAll` (không gate) chỉ trả `id`, `name` (+ `status` nếu khuôn cần) — KHÔNG trả phone/id_card/driver_license/birth_year. Kiểm FE T2 có dùng `getAll` của drives cho việc gì cần trường khác không (`grep` hrm-client nhánh hiện tại) — nếu form xe cần SĐT thì lấy qua endpoint `options` đã gate.
3. **M1** — lịch sử giá nhiên liệu làm tròn mất thập phân: sửa chỗ format/so sánh trong lịch sử cho `fuels.price` giữ 2 chữ số thập phân.
4. **M2** — cắt khoảng trắng (trim) phone/id_card/driver_license/birth_year/name TRƯỚC validate độ dài (prepareForValidation), không dùng trim ở FE.
5. **M3** — Mở khoá xe: chặn nếu biển số của xe đang khoá (status=0) hoặc đã gắn xe đang hoạt động khác (422, câu báo rõ).
6. **M4** — `options/employees` không trả SĐT; chỉ id (employee_infos.id), mã, họ tên, bộ phận/công ty nếu cần hiển thị. Kiểm FE T2 không đọc SĐT từ đó.
7. Bổ sung/ cập nhật PHPUnit cho 1–6 (`VehicleCatalog2cTest`). Chạy file + cả bộ MasterData, báo số (mốc 526/526).

## Không làm
- M5 (tài xế công ty đã nghỉ việc) — ghi nhận, giữ như ERP.
- M6 / N103 (gỡ unique DB) — chờ user.
- M9 — chấp nhận (dọn cột lệch loại khi Lưu).

## Ràng buộc
Giữ EOL; comment tiếng Việt; commit riêng trên nhánh, kết thúc:
```
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3
```
Số dòng bảng sau khi xong: license_plates 163 · drives 72 · vehicles 137 · fuels 4 · vehicle_drivers 110 · vehicle_company_drivers 74. Không dispatch subagent.

## Report
`2c-fix1-report.md` cùng thư mục. Trả lời ngắn: trạng thái, commit, test, lo ngại.
