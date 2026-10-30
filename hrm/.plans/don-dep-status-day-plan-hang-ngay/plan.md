# Dọn STATUS.md + tự đẩy plan hằng ngày lên hrm-claude-config — @cuong61n

Mục tiêu: admin tổng hợp công việc hằng ngày từ commit `.plans/` trên hrm-claude-config, nên STATUS phải đúng người, đúng trạng thái và plan phải được đẩy lên đều đặn.

## Phase 1 — Dọn STATUS.md (28/10)
- [x] Ignore thư mục `backup/` trong `.plans` (bản .patch/.tgz sao lưu worktree gop_db, chỉ dùng ở máy) (28/10)
- [x] Rà người phụ trách bằng `git log -S` (ai thêm dòng đầu tiên): sửa 32 mục ghi nhầm `@namdangit`/`@dnsnamdang` về `@cuong61n` (14 ở STATUS.md, 18 ở gop-db/STATUS.md) + gộp 88 mục `@manhcuong` về `@cuong61n` (28/10)
- [x] Sửa tên người phụ trách ở đầu 7 plan/design chưa đẩy (quotation-gap-0308, app-ui-redesign, notification-content, bao-cao-gp-phong-kd-sai-ten-quyen, manpower-planning-perf, thiet-ke-lai-phan-quyen) (28/10)
- [x] Chuyển 34 mục đã code xong/đã test/đã push sang "Hoàn thành" (20 ở STATUS.md, 14 ở gop-db/STATUS.md) — trước đó bị kẹt ở "Đang làm" vì quy tắc chỉ chuyển khi merge (28/10)

## Phase 2 — Tự đẩy plan hằng ngày (28/10)
- [x] Script `~/bin/push-plans.sh`: chỉ add `*/.plans/`, commit message liệt kê từng feature + số Redmine + task vừa tick, merge origin/main (tự cất tạm file dùng chung), push (28/10)
- [x] Launchd `com.cuong61n.push-plans` chạy 17:30 T2–T6 + 12:00 T7 (CN nghỉ — đổi theo yêu cầu 28/10), log `~/Library/Logs/push-plans.log` (28/10)
- [x] Lần đẩy đầu: gom toàn bộ plan tồn đọng (88 file), gỡ conflict gop-db/STATUS.md (2 bên cùng chèn mục → giữ cả hai), đã push `main` (28/10)
- [x] Ghi quy tắc vào memory + `~/.claude/CLAUDE.md` cá nhân: mọi việc (kể cả bug nhỏ) phải có plan.md chi tiết theo task, tự đẩy không cần hỏi (28/10)

### Checkpoint — 28/10/2026 18:05
Vừa hoàn thành: dọn STATUS + dựng cơ chế đẩy plan hằng ngày
Đang làm dở: —
Bước tiếp theo: các phiên sau tự ghi plan + chạy push-plans.sh khi xong việc
Blocked:

## Phase 3 — Ngừng tự đẩy sau mỗi việc (29–30/10)
- [x] Đổi quy tắc trong `~/.claude/CLAUDE.md` + memory: KHÔNG tự chạy push-plans.sh sau mỗi việc, chỉ launchd đẩy 17:30 T2–T6 / 12:00 T7, chạy tay khi Cường bảo (29/10 15:24)
- [x] Điều tra vì sao tối 29/10 vẫn ~20 commit (18:00–22:55): không phải launchd/hook; do phiên Claude `f0c380e6` mở từ 20/10 còn giữ luật cũ, tự gọi script sau mỗi việc (đối chiếu transcript ↔ `push-plans.log`) (30/10)
- [x] Sửa 2 memory còn câu "tự đẩy" sót: `feedback_small_task_no_process.md`, `feedback_git_push_xin_phep_tung_lan.md` (30/10)
- [x] Gửi tin nhắn cross-session nhắc luật mới cho các phiên mở trước 15:24 29/10 (hrm-dc, hrm-bf, hrm-bd, hrm-72, hrm-0e, sphacy-29) (30/10)

### Checkpoint — 30/10/2026 09:10
Vừa hoàn thành: chặn việc phiên cũ tự đẩy plan liên tục
Đang làm dở: —
Bước tiếp theo: theo dõi `~/Library/Logs/push-plans.log` hôm nay, chỉ nên có 1 lần đẩy lúc 17:30
Blocked:
