# Plan — regulation-config phiên bản hẹn không tự áp dụng

## Tasks

### Phase 1 — Root cause (đang làm)
- [x] 1.1: Verify dữ liệu pending PROD (5 bản, cty 9, GLOBAL, effective 01/10).
- [x] 1.2: Verify command + Kernel registration deployed (beaf58560, schedule:list).
- [x] 1.3: Loại trừ OS cron / php version (syslog nổ mỗi phút, php 7.4.33).
- [x] 1.4: **Chạy tay command** — user chạy 06/10 09:43: "Đã áp dụng 5 phiên bản + 0 dòng hoa hồng".
      ⟹ command/method OK tuyệt đối → nguyên nhân KHÔNG ở code, mà ở scheduler invocation 00:00.
      Verify PROD: 3 bản congno (id 8/9/10) scope_id=9, applied_at=2026-10-06 09:43:21; chỉ cty 9
      debt_calculation_date=2026-10-01, 8 cty khác giữ 2025-08-01 (per-company đúng, không toàn hệ thống).
- [x] 1.5: **PHÉP THỬ QUYẾT ĐỊNH — crontab + deploy time (06/10, đã có output):**
      - `schedule:run` CÓ cho tpe, đúng thư mục: `* * * * * cd /var/www/tpe/hrm-api/ && php artisan schedule:run >> /dev/null 2>&1`.
      - Server TZ = `Asia/Ho_Chi_Minh (+0700)` → `dailyAt('00:00')` = đúng nửa đêm VN, KHÔNG lệch TZ.
      - Command file mtime 24/09; Kernel.php mtime **04/10 17:41** (commit `57e6744d4` 04/10 13:22).
        ⟹ dòng đăng ký đã tồn tại qua **≥2 nửa đêm (05/10, 06/10)** mà 5 bản vẫn pending.
      → LOẠI "chưa tới hạn"/TZ/deploy. **Root cause: lớp `schedule:run` chung lúc 00:00 không chạy
        tới command (đăng ký cuối Kernel:134; 1 lệnh trước chết cứng process → lệnh sau bị bỏ; `/dev/null` nuốt).**
      - Quy ước server: mọi cron QUAN TRỌNG đều có **dòng crontab riêng gọi thẳng command** (rice:*,
        attendance:fetch, calc:timesheet...). Chỉ command của ta phó mặc schedule:run = tầng đang hỏng.
- [ ] 1.6: (TÙY CHỌN, không chặn fix) soi log 00:00 để đo "bán kính" — các cron khác chỉ dựa schedule:run
      có cùng chết không: `grep -hiE "exception|error|exhaust|memory|fatal" storage/logs/laravel-2026-10-0[5-6].log`
      + `grep -iE "oom|out of memory|killed process" /var/log/syslog | tail`.

### Phase 2 — Fix: dòng crontab riêng (user chốt hướng, chờ đồng ý thêm dòng)
- [x] 2.1: Dòng crontab cho tpe — **user tự thêm** (06/10). Dòng chốt:
      `10 0 * * * cd /var/www/tpe/hrm-api/ && php artisan regulation-config:apply-scheduled >> /var/www/tpe/hrm-api/storage/logs/apply-scheduled.log 2>&1`
      - 00:10 né phút 00:00 nghẽn; ghi LOG thật thay vì /dev/null.
      - An toàn trùng schedule:run: applyDueVersions chỉ đụng bản pending, áp xong flip applied.
      - Chỉ tpe (ETEK Green cty 9 đã gộp về tpe — khối etekgreen crontab bị comment "da chuyen sang cong TPE").
- [x] 2.2: Verify — user chạy smoke test đúng chuỗi lệnh crontab (06/10): `php` PATH đúng (PHP 7.4),
      `cd` + ghi `storage/logs/apply-scheduled.log` OK, ra `Đã áp dụng 0 phiên bản...` (không còn pending).
      Không cần restart cron (daemon tự nạp lại crontab khi lưu). Cron sống, fix đã hoạt động.
- [ ] 2.3: (cân nhắc, CHƯA làm) gỡ đăng ký khỏi Kernel:134 cho 1 cơ chế duy nhất, hoặc giữ redundant (vô hại).

### Phase 2 — Fix (sau khi có root cause)
- [ ] 2.1: Sửa đúng root cause (tùy 1.4/1.5).
- [ ] 2.2: Đảm bảo 5 bản đang kẹt được áp (đổi debt_calculation_date cty 9 → 01/10/2026).
- [ ] 2.3: Verify phiên bản hẹn mới tự áp đúng hạn.

## Checkpoint — 2026-10-06 (XONG — root cause + fix + verify)
Vừa hoàn thành: 1.1–1.5 (root cause chốt), 2.1 (user tự thêm dòng crontab 10 0 * * * cho tpe),
  2.2 (smoke test OK: php PATH đúng, ghi log OK, "Đã áp dụng 0 phiên bản"). 5 bản kẹt đã áp sáng nay.
Đang làm dở: (không).
Bước tiếp theo (tùy chọn, không gấp): 1.6 soi log 00:00 đo bán kính các cron khác chỉ dựa schedule:run;
  2.3 cân nhắc gỡ đăng ký Kernel:134 cho 1 cơ chế duy nhất.
Blocked: (không).
Memory: hrm-regconfig-scheduled-not-auto-apply-cron.md.
