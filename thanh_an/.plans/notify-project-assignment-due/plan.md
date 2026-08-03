# Plan — Thông báo dự toán chờ phân công sắp hết hạn

**Người phụ trách:** @khoipv · **Ngày:** 2026-07-06

## Phase 1 — Backend

- [x] Tạo command `app/Console/Commands/NotifyProjectAssignmentDue.php`
      (signature `projects:notify-assignment-due`), logic quét status=2 + `expected_time` còn ≤2 NLV → `sendToAllContractNotification` cho người có quyền `'Phân công báo giá'`
- [x] Đăng ký lịch dailyAt 07:00 trong `app/Console/Kernel.php`
- [x] Verify: `php artisan list | grep projects:notify` thấy command
- [x] Verify: chạy tay `php artisan projects:notify-assignment-due` → EXIT=0, log OK, 15 notif/lần tạo đúng payload (project DT-240/2026, url /sale/project/269)
- [x] Verify tinker: `diffInWeekdays` loại T7/CN (+7 ngày=5 NLV); DT-240 hạn 08/07 = 2 NLV → SE GUI, đúng ngưỡng ≤2

## Checkpoint — 2026-07-06
Vừa hoàn thành: BE command + lịch cron + verify end-to-end PASS
Đang làm dở: (không)
Bước tiếp theo: Merge / theo dõi cron thực tế 07:00 hàng ngày
Blocked: (không)

## Ghi chú
- Không đụng FE (type `project` + `url` đã có handler ở `AssignMenu.vue`).
- Không migration, không sửa hàm dùng chung.

## Checkpoint
_(cập nhật khi wrap up)_
