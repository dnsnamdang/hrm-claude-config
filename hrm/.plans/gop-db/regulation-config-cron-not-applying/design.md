# Regulation-config: phiên bản đã hẹn KHÔNG tự áp dụng (cron)

## Vấn đề
Màn `/finance/regulation-config`, công ty "ETEK GREEN" (DB company id=9), tab "Công nợ & tài chính".
Có các phiên bản hẹn hiệu lực **01/10/2026** nhưng tới **06/10/2026** vẫn "Chờ áp dụng" (pending),
không tự áp dụng dù đã quá ngày 5 hôm.

## Cơ chế đúng (theo code)
2 đường áp phiên bản hẹn:
- (a) **Áp ngay lúc lưu**: `createVersion/createGlobalVersion/createDepartmentVersion` gọi
  `applyDueVersions(null, $scopeId, $tabKey)` đồng bộ khi `effective_date <= hôm nay`.
- (b) **Cron hằng ngày 00:00**: command `regulation-config:apply-scheduled`
  (`app/Console/Commands/MasterData/ApplyScheduledRegulationsCommand.php`) →
  `applyDueVersions()` (tabKey null → đường whitelist) + `applyDueGridRows()`.
  Đăng ký ở `app/Console/Kernel.php:134` `->dailyAt('00:00')->timezone('Asia/Ho_Chi_Minh')->withoutOverlapping()`.

## Dữ liệu PROD (đã verify, read-only)
- 5 phiên bản pending toàn hệ thống, đều **company 9, scope GLOBAL**, `applied_at=NULL`:
  - congno id 8/9/10 payload `{"debt_calculation_date":"2026-10-01"}`
  - xnk id 5/6 payload `{"warning_day":7}`
  - tất cả `effective_date=2026-10-01`.
- 8 phiên bản đã applied đều có `applied_at == created_at` → **chỉ từng áp đồng bộ lúc lưu, cron CHƯA áp lần nào**.
- Company 9 CÓ dòng `configs` (id=9) → không dính `abort_if 500`.

## Tác động khi áp 5 phiên bản
- xnk: `warning_day` 7→7 (không đổi).
- congno: `debt_calculation_date` của cty 9: **2025-08-01 → 2026-10-01** (thay đổi THẬT duy nhất — ngày chốt công nợ).

## Điều tra — đã loại trừ
1. ❌ "cron không chạy" — crontab có `schedule:run` cho tpe + toyota.
2. ❌ "cron thiếu cho deployment hrm_erp_gop" — `/var/www/tpe/hrm-api/` chính là nơi chạy db hrm_erp_gop.
3. ❌ "1 version lỗi chặn cả lô (không try/catch)" — chỉ 5 pending, không có gì xếp trước để ném.
4. ❌ "command chưa deploy" — deployed `beaf58560` (mới hơn b7a7609cc), Kernel:134 có, `schedule:list`
   hiện command, Next Due 2026-10-07 00:00:00.
5. ❌ "OS cron không nổ / sai php" — syslog: cron nổ `schedule:run` cho tpe **mỗi phút**;
   `php` = /usr/bin/php → PHP 7.4.33 (đúng).

## Nghi vấn còn lại (chưa xác định root cause)
Mọi thứ về code, đăng ký, và OS cron đều OK, nhưng lệnh `apply-scheduled` đến hạn 00:00 không áp 5 bản
suốt 5 đêm. Lỗi phải nằm ở **hành vi runtime lúc 00:00**: command ném lỗi (output bị `>> /dev/null 2>&1`
nuốt), hoặc `withoutOverlapping` kẹt mutex, hoặc `applyDueVersions` không khớp lúc chạy thật.
→ Phép thử quyết định: chạy tay command để tách "command/method có lỗi" vs "chỉ scheduler lỗi".

## Blocked
DB trỏ PROD → chỉ SELECT/read-only. Chạy command (ghi DB) cần user cho phép.
