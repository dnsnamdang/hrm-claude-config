# Plan — Meeting xác nhận tham gia báo chủ trì

## Task
- [x] BE: báo chủ trì khi trạng thái đổi (`MeetingService`), `attendance_open` gồm Lên lịch (`MeetingMineResource`) — hrm-api gop_db local
- [x] Web: cột Xác nhận tham gia chỉ xem ở Lên lịch; realtime qua `realtime-notification` (7 file hrm-client gop_db local)
- [x] App: thẻ "x/y xác nhận", Hub "phản hồi x/y", màn Nhân sự tham gia chế độ RSVP + tự tải lại khi có push (TPE_APP develop, 7 file)
- [x] E2E: sửa `e2e/tests/assign/meeting-participants.spec.ts` (ca Lên lịch); thêm `meeting-attendance-confirm-notify.api.spec.ts` (6 ca) — CHƯA chạy (chỉ chạy khi user bảo)
- [x] Kiểm: BE bằng curl; web bằng Playwright MCP trên worktree `HRM/wt-rsvp` (API 8002 / Nuxt 3002 từ origin/gop_db + patch); app tpeLocal → 8002 (push giả lập qua VM service)
- [ ] User xem lại + quyết định commit / push (gop_db + develop)
- [ ] Kiểm push thật trên máy thật/máy ảo tpeDev sau khi lên dev
- [ ] Dọn worktree `HRM/wt-rsvp` (server 8002/3002 đã tắt 01/11)

### Checkpoint — 01/11/2026 16:40 (wrap up)
Vừa hoàn thành: code + kiểm 3 nền tảng; dữ liệu thử meeting 2618 (local) đã trả về như cũ
Đang làm dở: — (chưa commit: hrm-api 2 file, hrm-client 7 file gop_db; TPE_APP 7 file develop + CLAUDE.md/build_config.dart thay đổi có sẵn; e2e 2 file ngoài git)
Bước tiếp theo: user xem diff, bảo commit/push; sau đó `git worktree remove HRM/wt-rsvp/{hrm-api,hrm-client}`
Blocked: gop_db local đang có merge rbac chưa push ⇒ API :8000 local 500 (`permission_aliases`), kiểm phải dùng worktree từ origin/gop_db
